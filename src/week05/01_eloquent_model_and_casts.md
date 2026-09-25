---
layout: docs
title: "01강: Eloquent 모델, `casts()` 메서드 & 가격/할인율 접근자(Accessors)"
---

{% raw %}
# 01강: Eloquent 모델, `casts()` 메서드 & 가격/할인율 접근자(Accessors)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** Eloquent Active Record 기본, `$fillable` 보안, 라라벨 13의 `casts()` 메서드, 원화 표기 및 할인율 계산 접근자  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 시작하기 (Eloquent)](../docs/08_eloquent_orm/eloquent_ko.md), [뮤테이터와 캐스트 (Mutators & Casts)](../docs/08_eloquent_orm/eloquent-mutators_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 데이터베이스에는 책 가격이 `32000`이라는 순수 정수로 들어있잖아요. 화면에 보여줄 때마다 매번 `number_format($book->price) . '원'`을 붙이려니까 귀찮고, 출간일(`published_at`)도 날짜 객체(`Carbon`)로 다루고 싶어요. 모델이 스스로 똑똑하게 변환해 줄 수는 없나요?"

🐱 **지니**: "후후, 도로시! 바로 그것이 **Eloquent ORM**의 강력한 매력이란다! 데이터베이스 테이블 한 행이 살아있는 PHP 객체로 승격되는 거지. 라라벨 13의 최신 **`casts()` 메서드**를 사용하면 날짜와 JSON, 불리언을 알아서 변환해주고, **접근자(Accessor)**를 만들어두면 `$book->formatted_price`나 `$book->discount_rate`를 부르는 즉시 예쁜 원화 표시와 계산된 할인율을 돌려준단다!"

🐶 **토토**: "멍멍! 예전 버전처럼 `$casts` 프로퍼티를 쓰지 않고 라라벨 11~13에서는 `protected function casts(): array` 메서드를 쓰는 것이 공식 권장 스타일이다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. `Book` Eloquent 모델에 대량 할당 보호(`$fillable`)를 적용합니다.
2. 라라벨 13 표준 `casts()` 메서드로 `published_at`을 날짜 객체로 자동 변환합니다.
3. 원화 포맷팅(`formatted_price`)과 실시간 할인율(`discount_rate`) 접근자를 구현합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `app/Models/Book.php` 모델 작성

`app/Models/Book.php` 파일을 열고 다음과 같이 현대적인 라라벨 13 스타일로 작성합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Book extends Model
{
    use HasFactory, SoftDeletes;

    /**
     * 대량 할당 허용 컬럼 (보안 가드)
     */
    protected $fillable = [
        'isbn',
        'title',
        'slug',
        'author_id',
        'publisher_id',
        'category_id',
        'price',
        'sale_price',
        'stock_quantity',
        'format',
        'ebook_file_path',
        'page_count',
        'published_at',
        'description',
        'status',
    ];

    /**
     * 라라벨 13 속성 캐스팅 정의
     */
    protected function casts(): array
    {
        return [
            'price' => 'integer',
            'sale_price' => 'integer',
            'stock_quantity' => 'integer',
            'page_count' => 'integer',
            'published_at' => 'date:Y-m-d',
        ];
    }

    /**
     * 1. 가격 원화 표기 접근자 ($book->formatted_price)
     */
    protected function formattedPrice(): Attribute
    {
        return Attribute::make(
            get: fn () => number_format($this->price).'원'
        );
    }

    /**
     * 2. 할인 판매가 원화 표기 접근자 ($book->formatted_sale_price)
     */
    protected function formattedSalePrice(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->sale_price ? number_format($this->sale_price).'원' : null
        );
    }

    /**
     * 3. 실시간 할인율 계산 접근자 ($book->discount_rate)
     */
    protected function discountRate(): Attribute
    {
        return Attribute::make(
            get: function () {
                if (! $this->sale_price || $this->sale_price >= $this->price) {
                    return 0;
                }
                return (int) round((($this->price - $this->sale_price) / $this->price) * 100);
            }
        );
    }
}
```

---

### [Step 2] Tinker에서 접근자 실시간 검증

터미널에서 `php artisan tinker`를 열고 방금 작성한 접근자를 테스트합니다:

```bash
php artisan tinker
```

```php
// 할인 도서 1권 조회
$book = App\Models\Book::whereNotNull('sale_price')->first();

echo "도서명: " . $book->title . PHP_EOL;
echo "정가: " . $book->formatted_price . PHP_EOL;
echo "할인가: " . $book->formatted_sale_price . PHP_EOL;
echo "할인율: " . $book->discount_rate . "% 할인" . PHP_EOL;
echo "출간일 Carbon 요일: " . $book->published_at->format('Y년 m월 d일 (l)') . PHP_EOL;
```

> **출력 결과:**
> ```text
> 도서명: 초보자를 위한 라라벨 13 프로그래밍 #12
> 정가: 35,000원
> 할인가: 28,000원
> 할인율: 20% 할인
> 출간일 Carbon 요일: 2024년 08월 15일 (Thursday)
> ```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 대량 할당(Mass Assignment) 취약점 방어
- 만약 `$fillable`이나 `$guarded` 설정을 소홀히 하면, 악의적인 해커가 도서 등록 폼을 조작하여 `['is_admin' => 1]`이나 `['price' => 0]` 같은 파라미터를 보냈을 때 그대로 데이터베이스에 업데이트되는 대형 보안 사고가 발생합니다.
- Eloquent는 `$fillable`에 명시된 화이트리스트 컬럼만 `create()`나 `update()`로 갱신되도록 철통같이 차단합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **접근자 이름은 어떻게 부르나요?**  
>    메서드 이름이 카멜케이스 `formattedPrice()`라면, 사용할 때는 스네이크케이스 `$book->formatted_price` 속성으로 접근한다멍! 괄호 `()`를 붙이지 않는 것이 핵심이다멍!

---

## 💡 6. 1강 자가진단 과제

1. 재고 수량에 따라 "재고 있음" 또는 "품절"을 반환하는 `$book->stock_status` 접근자를 만들어 보세요.
2. `tinker`에서 `$book->published_at->diffForHumans()`를 호출하여 "2개월 전", "1년 전"과 같은 상대적 출간 기간이 한글로 계산되는지 확인하세요.
{% endraw %}
