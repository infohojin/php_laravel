---
layout: docs
title: "02강: 다형성 관계(Polymorphic Relations) — 서평(Review) & 도서 이미지"
---

{% raw %}
# 02강: 다형성 관계(Polymorphic Relations) — 서평(Review) & 도서 이미지

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 하나의 테이블로 여러 엔티티에 유연하게 결합하는 다형성 관계(`morphMany`, `morphTo`), 서평/평점 및 이미지 시스템  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 관계 (Eloquent Relationships)](../docs/08_eloquent_orm/eloquent-relationships_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리 서점에서 책에 독자 서평(별점, 한줄평)을 달 수 있어야 하잖아요. 그런데 나중에는 '저자 소개 페이지'에도 팬 리뷰를 달고 싶고, '출판사 페이지'에도 서평을 달고 싶대요! 그럼 `book_reviews`, `author_reviews`, `publisher_reviews` 테이블을 3개나 따로 만들어야 하나요? 이미지 첨부 파일도 마찬가지고요!"

🐱 **지니**: "후후, 도로시! 그럴 때 테이블을 무한정 늘리면 스키마가 누더기가 된단다. 이 문제를 단칼에 해결하는 객체지향적 비기가 바로 **다형성 관계(Polymorphic Relations)**란다! 단 하나의 `reviews` 테이블에 `reviewable_id`와 `reviewable_type` 두 개의 컬럼만 두면, 책에도 달리고 저자에게도 달리는 카멜레온 서평 시스템을 구축할 수 있지!"

🐶 **토토**: "멍멍! 데이터베이스에 긴 클래스 이름(`App\Models\Book`) 대신 `'book'`이라는 짧은 별칭을 저장하려면 `Relation::enforceMorphMap()`을 등록하는 것이 실무 모범 표준이다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 단일 서평 테이블(`reviews`)로 책과 저자 모두에게 별점 리뷰를 매길 수 있는 다형성 스키마를 설계합니다.
2. `morphMany`와 `morphTo` 관계 메서드를 모델에 연결합니다.
3. `enforceMorphMap()`을 적용하여 데이터베이스 저장 공간과 가독성을 최적화합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 다형성 서평(Review) 마이그레이션 생성

```bash
php artisan make:migration create_reviews_table
```

```php
// database/migrations/..._create_reviews_table.php
public function up(): void
{
    Schema::create('reviews', function (Blueprint $table) {
        $table->id();
        
        // reviewable_type(문자열)과 reviewable_id(부호없는 정수) 컬럼 및 복합 인덱스 자동 생성!
        $table->morphs('reviewable');

        $table->unsignedTinyInteger('rating')->comment('별점 1~5점');
        $table->string('reviewer_name')->comment('작성자 닉네임');
        $table->text('content')->comment('서평 내용');
        $table->timestamps();
    });
}
```

```bash
php artisan migrate
```

---

### [Step 2] `Review` 모델 및 다형성 관계 선언

#### 1) `app/Models/Review.php`
```php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Review extends Model
{
    protected $fillable = ['rating', 'reviewer_name', 'content'];

    /**
     * 서평이 달린 부모 대상 (책 또는 저자)
     */
    public function reviewable(): MorphTo
    {
        return $this->morphTo();
    }
}
```

#### 2) `app/Models/Book.php`에 `morphMany` 연결
```php
use App\Models\Review;
use Illuminate\Database\Eloquent\Relations\MorphMany;

public function reviews(): MorphMany
{
    return $this->morphMany(Review::class, 'reviewable');
}
```

#### 3) `app/Models/Author.php`에도 동일한 리뷰 연결 가능!
```php
public function reviews(): MorphMany
{
    return $this->morphMany(Review::class, 'reviewable');
}
```

---

### [Step 3] `AppServiceProvider`에 Morph Map 별칭 등록

데이터베이스에 `App\Models\Book`이라는 20바이트짜리 긴 문자열 대신 `'book'`, `'author'`라는 직관적인 별칭을 저장하도록 매핑합니다:

```php
// app/Providers/AppServiceProvider.php
use Illuminate\Database\Eloquent\Relations\Relation;
use App\Models\Book;
use App\Models\Author;

public function boot(): void
{
    Relation::enforceMorphMap([
        'book' => Book::class,
        'author' => Author::class,
    ]);
}
```

---

### [Step 4] Tinker에서 다형성 서평 작성 및 조회 실습

```bash
php artisan tinker
```

```php
// 1. 특정 책에 5점 만점 서평 남기기
$book = App\Models\Book::first();

$book->reviews()->create([
    'rating' => 5,
    'reviewer_name' => '열혈독자 도로시',
    'content' => '라라벨 13의 모든 비결이 담긴 최고의 서적입니다! 강력 추천합니다!',
]);

// 2. 책에서 서평 목록 및 평균 별점 조회
echo "등록된 서평 수: " . $book->reviews()->count() . "개" . PHP_EOL;
echo "평균 평점: " . $book->reviews()->avg('rating') . "점" . PHP_EOL;

// 3. 서평에서 역방향으로 대상 책 조회 (morphTo)
$review = App\Models\Review::first();
echo "서평 대상: [" . $review->reviewable->title . "]" . PHP_EOL;
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `enforceMorphMap()`의 안전성
- Morph Map을 강제하면, 실수로 등록되지 않은 모델 클래스 이름을 다형성 컬럼에 저장하려 할 때 라라벨이 `ClassMorphViolationException`을 발생시켜 데이터 오염을 완벽히 방지합니다.
- 향후 클래스 네임스페이스를 리팩토링하더라도 데이터베이스에 저장된 문자열(`'book'`)은 변경할 필요가 없어 마이그레이션 안정성이 뛰어납니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **책 목록에서 별점을 일일이 계산하면 너무 느려지지 않나요?**  
>    맞다멍! 책마다 서평을 다 긁어오지 않고 `Book::withAvg('reviews', 'rating')`을 쓰면 데이터베이스가 단일 쿼리로 `reviews_avg_rating`을 0.001초 만에 계산해 준다멍!

---

## 💡 6. 2강 자가진단 과제

1. 특정 도서의 평균 별점을 구하는 `Book::withAvg('reviews', 'rating')->first()` 쿼리를 실행해 보세요.
2. `Review` 테이블에 직접 SQL 조회를 날려 `reviewable_type` 컬럼에 `'book'`이라는 별칭이 예쁘게 저장되어 있는지 확인하세요.
{% endraw %}
