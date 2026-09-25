---
layout: docs
title: "03강: Faker 한국어 팩토리 & 1,000권 도서 데이터 생성 공장"
---

{% raw %}
# 03강: Faker 한국어 팩토리 & 1,000권 도서 데이터 생성 공장

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** Eloquent Model Factory, Faker 한국어 로케일, 현실적인 도서/저자/출판사 데이터 공장 및 팩토리 상태(State)  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 팩토리 (Eloquent Factories)](../docs/08_eloquent_orm/eloquent-factories_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 데이터베이스 테이블은 멋지게 만들었는데, 개발하고 테스트하려면 책 데이터가 수백, 수천 권은 들어있어야 페이지네이션도 시험하고 검색 기능도 테스트할 수 있잖아요! 수작업으로 1,000권의 책 제목과 ISBN, 가격을 엑셀로 치려면 일주일도 모자라요!"

🐱 **지니**: "후후, 도로시! 현대의 라라벨 개발자는 절대 손으로 데이터를 입력하지 않는단다. 우리에겐 **Eloquent 모델 팩토리(Model Factory)**와 **Faker 데이터 생성 엔진**이라는 자동화 공장이 있거든! 단 3초 만에 그럴듯한 한국어 책 제목, 13자리 고유 ISBN 번호, 저자 소개글을 가진 1,000권의 도서 데이터를 번개처럼 찍어낼 수 있단다!"

🐶 **토토**: "멍멍! 팩토리에 `->ebook()`, `->discounted()` 같은 상태(State) 메서드를 붙여두면 '20% 할인된 전자책' 같은 특수 조건 데이터도 레고처럼 뚝딱 만들 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. `Publisher`, `Author`, `Category`, `Book` 모델과 팩토리 파일을 한 번에 생성합니다.
2. Faker 라이브러리를 활용해 현실적인 한국어 책 제목, ISBN-13, 가격, 출간일을 정의합니다.
3. 팩토리 상태(State) 메서드로 '베스트셀러', '할인 도서', '품절 도서' 분기를 구현합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 모델과 팩토리 파일 일괄 생성

아티산의 `-f` 옵션을 주면 모델 생성과 동시에 팩토리 클래스를 짝지어 만들어 줍니다:

```bash
php artisan make:model Publisher -f
php artisan make:model Author -f
php artisan make:model Category -f
php artisan make:model Book -f
```

---

### [Step 2] 팩토리 정의 작성

#### 1) 출판사 팩토리 (`database/factories/PublisherFactory.php`)
```php
public function definition(): array
{
    $publishers = ['지니서적', '도로시미디어', '토토북스', '위키북스', '인사이트', '한빛미디어', '에이콘출판', '길벗'];
    $name = fake()->unique()->randomElement($publishers) ?? fake()->company().'출판사';

    return [
        'name' => $name,
        'code' => 'PUB-'.fake()->unique()->numerify('####'),
        'contact_email' => fake()->safeEmail(),
        'website_url' => fake()->url(),
    ];
}
```

#### 2) 저자 팩토리 (`database/factories/AuthorFactory.php`)
```php
public function definition(): array
{
    return [
        'name' => fake()->name(),
        'email' => fake()->unique()->safeEmail(),
        'bio' => fake()->realText(120),
        'profile_photo_url' => 'https://i.pravatar.cc/150?u='.fake()->uuid(),
    ];
}
```

#### 3) 도서 핵심 팩토리 (`database/factories/BookFactory.php`)
```php
namespace Database\Factories;

use App\Models\Author;
use App\Models\Category;
use App\Models\Publisher;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

class BookFactory extends Factory
{
    public function definition(): array
    {
        $prefixes = ['초보자를 위한', '실전', '우아한', '핵심만 골라 배우는', '러닝', '한 권으로 끝내는'];
        $topics = ['라라벨 13 프로그래밍', '모던 PHP 아키텍처', '클라우드 인프라 구축', '도커와 쿠버네티스', '알고리즘과 자료구조', 'TDD 테스트 자동화', '데이터베이스 쿼리 최적화'];
        $title = fake()->randomElement($prefixes).' '.fake()->randomElement($topics).' #'.fake()->numberBetween(1, 99);

        $price = fake()->numberBetween(15, 60) * 1000; // 15,000원 ~ 60,000원

        return [
            'isbn' => fake()->unique()->isbn13(),
            'title' => $title,
            'slug' => Str::slug($title).'-'.fake()->randomNumber(4),
            'author_id' => Author::factory(),
            'publisher_id' => Publisher::factory(),
            'category_id' => Category::factory(),
            'price' => $price,
            'sale_price' => null,
            'stock_quantity' => fake()->numberBetween(10, 500),
            'format' => fake()->randomElement(['paperback', 'hardcover', 'ebook']),
            'page_count' => fake()->numberBetween(200, 800),
            'published_at' => fake()->dateTimeBetween('-3 years', 'now')->format('Y-m-d'),
            'description' => fake()->realText(300),
            'status' => 'published',
        ];
    }

    /**
     * 상태 1: 할인 중인 도서
     */
    public function discounted(int $percent = 10): static
    {
        return $this->state(fn (array $attributes) => [
            'sale_price' => (int) ($attributes['price'] * (1 - $percent / 100)),
        ]);
    }

    /**
     * 상태 2: 전자책(eBook)
     */
    public function ebook(): static
    {
        return $this->state(fn (array $attributes) => [
            'format' => 'ebook',
            'stock_quantity' => 99999, // 전자책은 무제한 재고
            'ebook_file_path' => 'ebooks/'.fake()->uuid().'.epub',
        ]);
    }

    /**
     * 상태 3: 품절 도서
     */
    public function outOfStock(): static
    {
        return $this->state(fn (array $attributes) => [
            'stock_quantity' => 0,
            'status' => 'out_of_stock',
        ]);
    }
}
```

---

### [Step 3] Tinker에서 실시간 팩토리 생성 테스트

터미널에서 `php artisan tinker`를 열고 팩토리가 정상 동작하는지 테스트합니다:

```bash
php artisan tinker
```

```php
// 단 한 권의 책과 연관 저자/출판사/카테고리 즉석 생성
App\Models\Book::factory()->discounted(20)->create();

// 생성된 책 확인
App\Models\Book::first();
```

> **결과:**
> ```text
> => App\Models\Book {#6012
>      id: 1,
>      isbn: "9780201633610",
>      title: "실전 모던 PHP 아키텍처 #42",
>      price: 32000,
>      sale_price: 25600,
>      format: "paperback",
>      ...
>    }
> ```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 팩토리의 연관 관계 자동 해결 (`Sub-factories`)
- `BookFactory`의 정의를 보면 `'author_id' => Author::factory()`처럼 적혀 있습니다.
- 개발자가 저자(Author)를 따로 넘겨주지 않아도, 라라벨이 알아서 `Author` 레코드를 먼저 생성하고 그 ID 값을 `author_id`에 외래키로 채워 넣습니다!
- 만약 기존 저자를 재사용하고 싶다면 `Book::factory()->for($existingAuthor)->create()` 처럼 지정할 수도 있습니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **한국어 이름 대신 영문 이름(John Doe)이 나와요!**  
>    `config/app.php`의 `'faker_locale' => env('APP_FAKER_LOCALE', 'ko_KR')` 설정을 확인하라멍! `.env` 파일에 `APP_FAKER_LOCALE=ko_KR`을 적어두면 홍길동, 김철수 같은 친근한 한국어 이름이 나온다멍!

---

## 💡 6. 3강 자가진단 과제

1. `tinker`에서 `Book::factory()->count(10)->ebook()->create();`를 실행하여 전자책 10권이 생성되는지 확인하세요.
2. `Book::where('format', 'ebook')->count();`로 정확히 10권이 조회되는지 검증하세요.
{% endraw %}
