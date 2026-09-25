---
layout: docs
title: "02강: 쿼리 스코프(Query Scopes) & 도서 다중 필터링/정렬 체이닝"
---

{% raw %}
# 02강: 쿼리 스코프(Query Scopes) & 도서 다중 필터링/정렬 체이닝

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 비즈니스 조건 캡슐화 로컬 스코프(`scopePublished`, `scopeInStock`), 다중 조건 플루언트 쿼리(`when`), 가격/인기순 정렬  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 시작하기 (Eloquent)](../docs/08_eloquent_orm/eloquent_ko.md), [쿼리 빌더 (Queries)](../docs/07_database/queries_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 도서 목록을 가져올 때마다 매번 `where('status', 'published')->where('stock_quantity', '>', 0)`을 중복해서 적다 보니까 실수가 잦아져요. '출판 완료된 도서'나 '재고 있는 도서' 같은 서점의 기본 규칙을 모델에 딱 한 번만 적어두고 재사용할 수는 없나요?"

🐱 **지니**: "도로시, 바로 그럴 때 사용하는 마법이 **로컬 쿼리 스코프(Local Query Scopes)**란다! 모델 안에 `scopePublished()`나 `scopeInStock()`처럼 정의해두면, 밖에서는 `Book::published()->inStock()->get()` 처럼 마치 영어를 읽듯이 자연스러운 체이닝으로 쿼리를 작성할 수 있지! 게다가 쿼리 빌더의 `when()` 메서드를 조합하면 검색어가 있을 때만 조건절을 동적으로 붙이는 명품 컨트롤러를 완성할 수 있단다!"

🐶 **토토**: "멍멍! `if ($keyword) { $query->where(...) }` 처럼 지저분한 if문을 덕지덕지 쓰지 않고 `$query->when($keyword, ...)`을 쓰는 것이 라라벨 고수들의 비법이다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. `Book` 모델에 자주 쓰이는 5대 비즈니스 로컬 쿼리 스코프를 정의합니다.
2. `when()` 헬퍼를 활용해 카테고리, 검색어, 가격대, 재고 유무를 조건부 결합하는 유연한 쿼리를 작성합니다.
3. 인기순, 신간순, 낮은 가격순, 높은 가격순 정렬 스위칭을 구현합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `Book` 모델에 쿼리 스코프 추가

`app/Models/Book.php`에 다음 스코프 메서드들을 작성합니다:

```php
// app/Models/Book.php 내부에 추가
use Illuminate\Database\Eloquent\Builder;

/**
 * 1. 출판 완료된 정상 도서만 조회
 */
public function scopePublished(Builder $query): void
{
    $query->where('status', 'published');
}

/**
 * 2. 실물 재고가 남아있는 도서만 조회 (또는 무제한 전자책)
 */
public function scopeInStock(Builder $query): void
{
    $query->where(function (Builder $q) {
        $q->where('stock_quantity', '>', 0)
          ->orWhere('format', 'ebook');
    });
}

/**
 * 3. 할인 중인 도서만 조회
 */
public function scopeDiscounted(Builder $query): void
{
    $query->whereNotNull('sale_price')
          ->whereColumn('sale_price', '<', 'price');
}

/**
 * 4. 도서명 및 소개글 키워드 검색 스코프
 */
public function scopeSearch(Builder $query, ?string $keyword): void
{
    if (empty($keyword)) {
        return;
    }

    $query->where(function (Builder $q) use ($keyword) {
        $q->where('title', 'like', "%{$keyword}%")
          ->orWhere('isbn', 'like', "%{$keyword}%")
          ->orWhere('description', 'like', "%{$keyword}%");
    });
}

/**
 * 5. 정렬 기준 적용 스코프
 */
public function scopeSortBy(Builder $query, string $sort): void
{
    match ($sort) {
        'price_asc' => $query->orderByRaw('COALESCE(sale_price, price) ASC'),
        'price_desc' => $query->orderByRaw('COALESCE(sale_price, price) DESC'),
        'latest' => $query->orderBy('published_at', 'desc'),
        default => $query->orderBy('id', 'desc'), // 기본 최신순
    };
}
```

---

### [Step 2] `BookController@index`에서 우아한 체이닝 조립

`app/Http/Controllers/BookController.php`의 `index()` 메서드를 쿼리 스코프 기반으로 전면 리팩토링합니다:

```php
// app/Http/Controllers/BookController.php
use App\Models\Book;
use Illuminate\Http\Request;

public function index(Request $request)
{
    $keyword = $request->string('keyword')->trim()->value();
    $categoryId = $request->integer('category_id');
    $inStockOnly = $request->boolean('in_stock_only', false);
    $discountOnly = $request->boolean('discount_only', false);
    $sort = $request->input('sort', 'latest');

    // 1. 기본 쿼리 빌더 시작 (출판 완료 도서)
    $books = Book::query()
        ->published()
        // 검색어가 있으면 search 스코프 적용
        ->when($keyword, fn ($q) => $q->search($keyword))
        // 카테고리 필터가 있으면 적용
        ->when($categoryId, fn ($q) => $q->where('category_id', $categoryId))
        // 재고 필터 플래그가 켜져 있으면 inStock 적용
        ->when($inStockOnly, fn ($q) => $q->inStock())
        // 할인 도서 플래그
        ->when($discountOnly, fn ($q) => $q->discounted())
        // 정렬 적용
        ->sortBy($sort)
        // 3강에서 배울 12권씩 페이징 적용
        ->paginate(12)
        ->withQueryString(); // 검색 쿼리스트링 파라미터 링크 유지!

    return view('books.index', compact('books', 'keyword', 'categoryId', 'inStockOnly', 'discountOnly', 'sort'));
}
```

---

### [Step 3] 브라우저에서 다중 검색 필터링 테스트

로컬 서버에서 다양한 URL 조건을 전달해 봅니다:

1. **라라벨 검색어 필터**:  
   `http://127.0.0.1:8000/books?keyword=라라벨`
2. **할인 중인 도서만 낮은 가격순 정렬**:  
   `http://127.0.0.1:8000/books?discount_only=1&sort=price_asc`
3. **재고 있는 책 중 높은 가격순**:  
   `http://127.0.0.1:8000/books?in_stock_only=1&sort=price_desc`

단 하나의 깔끔한 컨트롤러 메서드가 수십 가지의 복합 조합을 에러 없이 초고속으로 처리합니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `when()` 메서드의 조건부 실행 미학
- `$query->when($value, $callback, $defaultCallback)`
- `$value`가 참(truthy, 즉 null이나 빈 문자열이 아님)일 때만 콜백을 실행하여 쿼리 조건을 추가합니다.
- 복잡한 검색 폼이 주어졌을 때 if-else 블록으로 쿼리를 쪼개지 않고 단일 플루언트 파이프라인으로 연결할 수 있어 가독성과 유지보수성이 극대화됩니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **할인가와 정가가 섞여 있을 때 가격순 정렬은 어떻게 하나요?**  
>    SQL의 `COALESCE(sale_price, price)` 구문을 쓰면 할인가가 있으면 할인가를, 없으면 정가를 기준으로 정확하게 정렬된다멍!

---

## 💡 6. 2강 자가진단 과제

1. `scopeBetweenPrices($query, $min, $max)` 스코프를 만들어 최소/최대 가격 범위 검색 기능을 추가해 보세요.
2. Telescope의 **Queries** 탭에서 생성된 실제 SQL 질의문과 바인딩 파라미터를 눈으로 확인해 보세요.
{% endraw %}
