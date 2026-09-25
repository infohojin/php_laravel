---
layout: docs
title: "03강: N+1 쿼리 폭발의 정체 & 즉시 로딩(Eager Loading) 극적 최적화"
---

{% raw %}
# 03강: N+1 쿼리 폭발의 정체 & 즉시 로딩(Eager Loading) 극적 최적화

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** N+1 쿼리 병목 진단(Telescope), 즉시 로딩(`with`), 서평 개수 최적화(`withCount`), Lazy Loading 전면 차단(`preventLazyLoading`)  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 관계 (Eager Loading)](../docs/08_eloquent_orm/eloquent-relationships_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 큰일 났어요! 도서 카탈로그 화면에 책 제목 옆에 '저자 이름'과 '출판사 이름'을 띄우려고 Blade 루프에서 `{{ $book->author->name }}`을 적었더니, Telescope 대시보드가 온통 빨간 불로 뒤덮였어요! 화면 하나 띄우는데 SQL 쿼리가 101개나 실행되면서 서버가 덜덜 떨리고 있어요!"

🐱 **지니**: "하하, 도로시! 드디어 모든 웹 백엔드 개발자들의 통과의례인 **'N+1 쿼리 폭발 문제'**를 만났구나! 책 50권을 가져오는 쿼리 1개(1)에, 책마다 저자를 하나씩 따로 조회하는 쿼리 50개(N)가 루프 안에서 무차별적으로 터져 나온 거란다. 하지만 걱정 마렴! 우리에겐 마법의 치료약 **즉시 로딩(Eager Loading, `with()`)**이 있거든. 101개였던 쿼리를 단 3개로 압축해 100배 빠른 번개 응답을 만들어 줄 수 있단다!"

🐶 **토토**: "멍멍! `AppServiceProvider`에 `Model::preventLazyLoading()`을 켜두면, 개발 중에 깜빡하고 N+1 실수를 저질렀을 때 라라벨이 '도로시! 즉시 로딩을 빼먹었어!' 하고 즉시 경고창을 띄워준다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. Telescope를 통해 N+1 쿼리 폭발 현상을 직접 재현하고 병목 원인을 분석합니다.
2. `with(['author', 'publisher', 'category'])` 즉시 로딩으로 쿼리 수를 극적으로 줄입니다.
3. 메모리를 절약하며 서평 개수만 세는 `withCount('reviews')`를 적용합니다.
4. 개발 환경에서 N+1 실수를 원천 차단하는 `preventLazyLoading` 가드를 구축합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] N+1 쿼리 폭발 현상 재현

`routes/web.php`에 고의로 지연 로딩(Lazy Loading)을 발생시키는 테스트 라우트를 작성합니다:

```php
// routes/web.php
use App\Models\Book;

Route::get('/test-n-plus-one', function () {
    // 1. 책 30권 조회 (쿼리 1회)
    $books = Book::published()->take(30)->get();

    $output = [];
    foreach ($books as $book) {
        // 루프 돌 때마다 author와 publisher를 매번 개별 SQL로 질의! (쿼리 30회 + 30회 = 총 61회 폭발!)
        $output[] = [
            'title' => $book->title,
            'author' => $book->author->name,
            'publisher' => $book->publisher->name,
        ];
    }

    return response()->json([
        'message' => 'N+1 쿼리 재현 완료!',
        'count' => count($output),
    ]);
});
```

브라우저에서 `http://127.0.0.1:8000/test-n-plus-one` 을 호출한 뒤, Telescope 대시보드(`http://127.0.0.1:8000/telescope/queries`)를 확인합니다:

> **Telescope 관측 결과:**  
> `select * from books limit 30` (1회)  
> `select * from authors where id = 1`  
> `select * from publishers where id = 1`  
> ... (동일한 쿼리가 30번 반복 실행되며 총 61개 쿼리 폭발!)

---

### [Step 2] `with()` 즉시 로딩(Eager Loading)으로 100배 압축

컨트롤러 쿼리에 `with(['author', 'publisher'])`를 단 한 줄 추가합니다:

```php
Route::get('/test-eager-loading', function () {
    // 단 3개의 쿼리로 30권의 책과 연관 저자, 출판사를 일괄 사전 적재!
    $books = Book::query()
        ->published()
        ->with(['author', 'publisher']) // 🚀 즉시 로딩!
        ->take(30)
        ->get();

    $output = [];
    foreach ($books as $book) {
        // 이미 메모리에 로드되어 있으므로 추가 SQL 쿼리가 0개 발생!
        $output[] = [
            'title' => $book->title,
            'author' => $book->author->name,
            'publisher' => $book->publisher->name,
        ];
    }

    return response()->json([
        'message' => '즉시 로딩 최적화 완료!',
        'count' => count($output),
    ]);
});
```

> **Telescope 쿼리 재확인:**  
> 1. `select * from books where status = 'published' limit 30;`  
> 2. `select * from authors where id in (1, 3, 7, ...);` (IN 쿼리 1회)  
> 3. `select * from publishers where id in (2, 4, 8, ...);` (IN 쿼리 1회)  
> **총 쿼리 수: 61개 $\rightarrow$ 단 3개로 압축 (95% DB 부하 감소!)**

---

### [Step 3] 서평 개수 최적화 (`withCount`)

도서 카드에 '서평 12개'를 표시하기 위해 수천 개의 서평 텍스트를 메모리에 다 올리면 메모리(OOM)가 고갈됩니다.  
`withCount('reviews')`를 쓰면 서평 데이터는 읽지 않고 개수(`reviews_count`)만 서브쿼리로 가져옵니다:

```php
$books = Book::query()
    ->published()
    ->with(['author', 'publisher'])
    ->withCount('reviews') // $book->reviews_count 컬럼 자동 생성!
    ->paginate(12);
```

Blade 화면:
```html
<span class="text-xs text-slate-400">
    💬 서평 ({{ $book->reviews_count }}개)
</span>
```

---

### [Step 4] N+1 방지 가드 가동 (`preventLazyLoading`)

`app/Providers/AppServiceProvider.php`에 로컬 개발 중 Lazy Loading을 만나면 즉시 예외를 터뜨려 개발자에게 경고하는 안전장치를 설치합니다:

```php
// app/Providers/AppServiceProvider.php
use Illuminate\Database\Eloquent\Model;

public function boot(): void
{
    // 로컬 개발 환경에서는 N+1(Lazy Loading) 발생 시 즉시 빨간 에러 화면을 띄워 실수 방지!
    Model::preventLazyLoading(! app()->isProduction());
}
```

이제 개발 중 누군가 `with()`를 빼먹고 루프를 돌면, 라라벨이 친절하게 다음 에러를 띄워줍니다:
> `Attempted to lazy load [author] on model [App\Models\Book] but lazy loading is disabled.`

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 중첩 관계 즉시 로딩 (Nested Eager Loading)
- 도서 $\rightarrow$ 저자 $\rightarrow$ 저자의 소속 단체까지 깊은 관계를 가져와야 할 때도 점 표기법으로 한 번에 로드할 수 있습니다:
  ```php
  Book::with(['author.agency', 'reviews.user'])->get();
  ```
- 라라벨 내부의 관계 해결 엔진이 외래키를 수집하여 알아서 가장 최적화된 최소한의 `IN (?, ?, ?)` 쿼리 세트로 치환합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **별점이 5점인 서평만 골라서 가져오고 싶어요!**  
>    클로저를 넘겨주면 된다멍!  
>    `Book::with(['reviews' => fn ($q) => $q->where('rating', 5)])->get();` 처럼 관계 쿼리에 조건을 걸 수 있다멍!

---

## 💡 6. 3강 자가진단 과제

1. `BookController@index` 메서드에 `with(['author', 'publisher', 'category'])`와 `withCount('reviews')`를 적용하세요.
2. 브라우저에서 `/books` 페이지를 열고 Telescope에서 12권의 책을 표시하는 데 발생한 총 쿼리 수가 4개 이하인지 직접 확인하세요.
{% endraw %}
