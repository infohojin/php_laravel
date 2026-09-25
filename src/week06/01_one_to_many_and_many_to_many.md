---
layout: docs
title: "01강: 도서 데이터 관계망 — 1:N 관계 & N:M 주문 피벗(Pivot) 테이블"
---

{% raw %}
# 01강: 도서 데이터 관계망 — 1:N 관계 & N:M 주문 피벗(Pivot) 테이블

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 저자-도서/출판사-도서 1:N 관계, 주문-도서 N:M 관계와 `order_items` 피벗 테이블 추가 속성  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 관계 (Eloquent Relationships)](../docs/08_eloquent_orm/eloquent-relationships_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 한 명의 저자가 여러 권의 책을 쓸 수 있고(`Author -> Books`), 한 고객의 주문서 안에는 '라라벨 책 2권', 'PHP 책 1권' 처럼 여러 권의 도서가 들어갈 수 있잖아요(`Order <-> Books`). 반대로 한 권의 책도 여러 번 주문될 수 있고요! 이 복잡한 그물망 같은 관계를 Eloquent에서는 어떻게 코드로 연결하나요?"

🐱 **지니**: "도로시, 바로 그것이 관계형 데이터베이스(RDBMS)의 진정한 힘이란다! 1:N 관계는 `hasMany`와 `belongsTo`라는 직관적인 메서드로 연결되고, N:M 관계는 중간에 **피벗 테이블(`order_items`)**이라는 완충 다리를 놓아 `belongsToMany`로 연결하지! 게다가 `withPivot('quantity', 'unit_price')`를 선언하면 주문 당시의 가격과 수량까지 깔끔하게 꺼내올 수 있단다!"

🐶 **토토**: "멍멍! `$book->author->name` 이나 `$order->books` 처럼 마치 객체 프로퍼티를 부르듯이 부모/자식 데이터를 슉슉 넘나들 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. `Author` $\leftrightarrow$ `Book`, `Publisher` $\leftrightarrow$ `Book` 1:N 관계를 정의합니다.
2. `Order` $\leftrightarrow$ `Book` N:M 피벗 관계를 맺고 주문 수량(`quantity`)과 결제 단가(`unit_price`)를 피벗 속성으로 추출합니다.
3. 역방향 관계(`belongsTo`, `belongsToMany`) 탐색을 Tinker로 검증합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 1:N 관계 정의 (`Author`, `Publisher`, `Book`)

#### 1) `app/Models/Author.php` (한 명의 저자는 여러 권의 책을 가짐)
```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Author extends Model
{
    protected $fillable = ['name', 'email', 'bio', 'profile_photo_url'];

    public function books(): HasMany
    {
        return $this->hasMany(Book::class);
    }
}
```

#### 2) `app/Models/Book.php` (책은 특정 저자, 출판사, 카테고리에 속함)
```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    // ... 이전 코드 ...

    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    public function publisher(): BelongsTo
    {
        return $this->belongsTo(Publisher::class);
    }

    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }
}
```

---

### [Step 2] N:M 피벗 관계 정의 (`Order` $\leftrightarrow$ `Book`)

한 고객의 주문(`Order`)은 여러 권의 책을 담고, 한 권의 책도 여러 주문에 포함될 수 있습니다.

#### 1) 피벗 테이블 마이그레이션 생성
```bash
php artisan make:migration create_orders_and_order_items_tables
```

```php
public function up(): void
{
    // 주문 테이블
    Schema::create('orders', function (Blueprint $table) {
        $table->id();
        $table->string('order_number')->unique();
        $table->unsignedInteger('total_amount');
        $table->string('status')->default('paid');
        $table->timestamps();
    });

    // 주문-도서 N:M 피벗 테이블 (추가 속성: quantity, unit_price)
    Schema::create('order_items', function (Blueprint $table) {
        $table->id();
        $table->foreignId('order_id')->constrained()->cascadeOnDelete();
        $table->foreignId('book_id')->constrained()->cascadeOnDelete();
        $table->unsignedInteger('quantity')->default(1);
        $table->unsignedInteger('unit_price')->comment('주문 당시 판매 단가');
        $table->timestamps();
    });
}
```

```bash
php artisan migrate
```

#### 2) `Order` 모델에 `belongsToMany` 관계 선언
```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Order extends Model
{
    protected $fillable = ['order_number', 'total_amount', 'status'];

    public function books(): BelongsToMany
    {
        return $this->belongsToMany(Book::class, 'order_items')
            ->withPivot('quantity', 'unit_price') // 피벗 속성 추가 로드!
            ->withTimestamps();
    }
}
```

---

### [Step 3] Tinker에서 관계 탐색 및 피벗 데이터 조회 실습

```bash
php artisan tinker
```

```php
// 1. 특정 책의 저자와 출판사 이름 조회
$book = App\Models\Book::first();
echo "책: " . $book->title . PHP_EOL;
echo "저자: " . $book->author->name . PHP_EOL;
echo "출판사: " . $book->publisher->name . PHP_EOL;

// 2. 가상 주문 및 도서 담기 테스트
$order = App\Models\Order::create([
    'order_number' => 'ORD-2026-0001',
    'total_amount' => 50000,
]);

// 주문에 책 2권 담기 (수량 2권, 단가 25,000원)
$order->books()->attach($book->id, [
    'quantity' => 2,
    'unit_price' => 25000,
]);

// 주문에 담긴 책과 피벗 데이터 조회
$orderedBook = $order->books()->first();
echo "주문 도서: " . $orderedBook->title . PHP_EOL;
echo "주문 수량: " . $orderedBook->pivot->quantity . "권" . PHP_EOL;
echo "주문 당시 단가: " . number_format($orderedBook->pivot->unit_price) . "원" . PHP_EOL;
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 피벗 테이블의 `attach()`, `detach()`, `sync()`
- `attach($bookId, $attributes)`: 피벗 테이블에 관계를 새로 추가합니다.
- `detach($bookId)`: 특정 관계를 해제(삭제)합니다.
- `sync([$id1 => [...], $id2 => [...]])`: 쇼핑몰 장바구니에서 가장 강력한 메서드로, 넘겨준 ID 목록만 남기고 나머지는 자동으로 삭제하여 현재 상태와 완벽히 동기화합니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **피벗 테이블 이름을 지을 땐 단수형 알파벳 순서가 기본 규칙이에요!**  
>    `books`와 `orders`의 피벗 테이블은 알파벳 순서에 따라 기본적으로 `book_order`를 찾는다멍! 만약 우리처럼 `order_items`라는 이름을 쓰고 싶다면 `belongsToMany(Book::class, 'order_items')` 처럼 두 번째 인자에 테이블명을 꼭 적어줘야 한다멍!

---

## 💡 6. 1강 자가진단 과제

1. 특정 저자가 집필한 도서 권수를 `$author->books()->count()`로 확인해 보세요.
2. `order_items` 피벗 테이블에서 특정 주문의 총 결제 금액을 `$order->books->sum(fn ($b) => $b->pivot->quantity * $b->pivot->unit_price)` 수식으로 계산해 보세요.
{% endraw %}
