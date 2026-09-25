---
layout: docs
title: "04강: 컬렉션(Collections) 함수형 가공 & OOM 방지 지연 컬렉션(LazyCollection)"
---

{% raw %}
# 04강: 컬렉션(Collections) 함수형 가공 & OOM 방지 지연 컬렉션(LazyCollection)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** Eloquent Collection 함수형 체이닝(`map`, `filter`, `groupBy`, `sum`), OOM(Out of Memory) 메모리 고갈 방지 `LazyCollection::cursor()` 정산 스크립트  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 컬렉션 (Eloquent Collections)](../docs/08_eloquent_orm/eloquent-collections_ko.md), [컬렉션 심화 (Collections)](../docs/05_digging_deeper/collections_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 월말이 되어서 서점의 도서 판매 내역을 분석하고 싶은데요. 카테고리별로 매출을 묶고(`groupBy`), 실물 책과 전자책 비율을 나누고(`filter`), 총매출액을 합산(`sum`)하고 싶어요. 복잡한 for 루프나 2차원 배열 조작 없이 깔끔하게 처리하는 방법이 없을까요? 그리고 주문이 10만 건 넘게 쌓이면 메모리 부족 에러(Out Of Memory)로 서버가 뻗지 않을까요?"

🐱 **지니**: "도로시가 라라벨 개발자들의 최애 기능인 **컬렉션(Collection)**의 세계로 들어섰구나! 라라벨의 컬렉션은 배열을 감싼 '슈퍼 파워 마법 지팡이'란다. `map`, `filter`, `groupBy`, `sum` 같은 수백 가지의 고차 함수를 체이닝할 수 있지. 그리고 10만 건의 대용량 데이터를 처리할 때는 PHP 제너레이터(Generator) 기반의 **`LazyCollection`**을 쓰면, 메모리를 단 10MB도 쓰지 않고 물 흐르듯 가볍게 스트리밍 정산할 수 있단다!"

🐶 **토토**: "멍멍! `Order::cursor()` 한 줄이면 100만 건 주문도 메모리 초과 걱정 없이 꼬리를 살랑이며 계산할 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. Eloquent Collection의 풍부한 함수형 메서드로 서점 도서 통계(카테고리별 도서 수, 최고가 도서, 총 재고 가치)를 집계합니다.
2. 수만 건의 대량 주문 데이터 처리 시 발생하는 OOM 위험성을 이해합니다.
3. `cursor()` 제너레이터를 활용한 **LazyCollection**으로 메모리 10MB 미만의 초경량 월간 정산 스크립트를 구현합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 컬렉션 함수형 체이닝 도서 통계 실습

Tinker에서 현재 시딩된 1,000권의 도서를 컬렉션 함수로 자유자재로 요약 분석해 봅니다:

```bash
php artisan tinker
```

```php
// 출판사, 카테고리가 즉시 로드된 100권 추출
$books = App\Models\Book::with(['category', 'author'])->take(100)->get();

// 1. 카테고리별로 도서 그룹화 (groupBy)
$grouped = $books->groupBy('category.name');

// 2. 카테고리별 권수 및 평균 가격 계산 (map)
$categoryStats = $grouped->map(function ($items, $categoryName) {
    return [
        'count' => $items->count(),
        'avg_price' => (int) $items->avg('price'),
        'total_stock' => $items->sum('stock_quantity'),
    ];
});

// 3. 평균 가격이 높은 순으로 정렬 (sortByDesc)
$sortedStats = $categoryStats->sortByDesc('avg_price');

print_r($sortedStats->take(3)->toArray());
```

> **지니의 감탄:**  
> 단 서너 줄의 함수형 체이닝만으로 SQL 쿼리 없이도 메모리 상에서 복잡한 다차원 통계를 우아하게 뽑아냈단다!

---

## 🔍 4. 대용량 처리를 위한 Lazy Collection (`Order::cursor()`)

만약 10만 건의 주문 내역을 `Order::all()`로 메모리에 올리면 PHP의 `memory_limit`(기본 128MB)가 터지면서 서버가 다운됩니다:

```text
Fatal error: Allowed memory size of 134217728 bytes exhausted
```

하지만 **`cursor()`**를 호출하면 라라벨은 내부적으로 PHP 제너레이터(`yield`)를 생성하여, **한 번에 단 하나의 레코드만 메모리에 올리고 처리 후 즉시 버리는 스트리밍 방식**으로 동작합니다:

```php
// routes/web.php 에 대용량 정산 시뮬레이션 라우트 작성
use App\Models\Book;
use Illuminate\Support\Facades\Route;

Route::get('/admin/settlement-simulation', function () {
    $initialMemory = memory_get_usage(true) / 1024 / 1024;

    $totalCalculatedValue = 0;
    $processedCount = 0;

    // cursor()는 전체 데이터를 한꺼번에 올리지 않고 1권씩 스트리밍 처리합니다!
    Book::cursor()->each(function (Book $book) use (&$totalCalculatedValue, &$processedCount) {
        $totalCalculatedValue += ($book->price * $book->stock_quantity);
        $processedCount++;
    });

    $finalMemory = memory_get_usage(true) / 1024 / 1024;

    return response()->json([
        'message' => '대용량 도서 재고 가치 정산 완료!',
        'processed_books_count' => $processedCount,
        'total_inventory_value' => number_format($totalCalculatedValue) . '원',
        'initial_memory_mb' => round($initialMemory, 2),
        'final_memory_mb' => round($finalMemory, 2),
        'memory_diff_mb' => round($finalMemory - $initialMemory, 2),
    ]);
});
```

브라우저에서 `http://127.0.0.1:8000/admin/settlement-simulation`을 호출합니다:

```json
{
  "message": "대용량 도서 재고 가치 정산 완료!",
  "processed_books_count": 1000,
  "total_inventory_value": "8,420,000,000원",
  "initial_memory_mb": 18.0,
  "final_memory_mb": 18.0,
  "memory_diff_mb": 0.0
}
```
> **메모리 증가량: 0.0 MB!**  
> 1,000권이든 1,000만 권이든 일정한 메모리만 점유하며 정산이 안전하게 완료됩니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`LazyCollection`에서 배열 인덱스로 `$lazy[0]`처럼 접근할 수 있나요?**  
>    안 된다멍! 제너레이터는 순방향 스트림이라서 인덱스 직접 접근이 불가능하다멍! 첫 번째 값을 꺼내려면 `$lazy->first()`를 쓰라멍!

---

## 💡 6. 4강 자가진단 과제

1. `Book::cursor()`를 활용하여 '종이책'들의 총 재고 수량과 '전자책' 권수를 단일 루프로 집계하는 스크립트를 작성해 보세요.
2. `books` 컬렉션에서 `filter(fn ($b) => $b->discount_rate >= 20)`로 20% 이상 파격 할인 중인 도서만 추출해 보세요.
{% endraw %}
