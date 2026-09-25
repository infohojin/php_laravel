---
layout: docs
title: "04강: 데이터베이스 시더(Seeder) & 1,000권 도서 한 방 구축 (`migrate:fresh --seed`)"
---

{% raw %}
# 04강: 데이터베이스 시더(Seeder) & 1,000권 도서 한 방 구축 (`migrate:fresh --seed`)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 계층형 카테고리 시딩, 1,000권 도서 대량 시더(`BookSeeder`), `migrate:fresh --seed` 원클릭 데이터베이스 초기화  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [시딩 (Seeding)](../docs/07_database/seeding_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리가 만든 카테고리, 저자, 출판사, 책 팩토리들을 하나의 완벽한 서점으로 조립하려면 어떻게 해야 해요? 새 팀원이 프로젝트를 내려받았을 때 터미널에서 명령어 딱 한 번만 치면 1,000권의 알록달록한 책들과 카테고리가 촤르륵 세팅되게 만들 수 있을까요?"

🐱 **지니**: "물론이지 도로시! 라라벨의 **데이터베이스 시더(Database Seeder)**가 바로 그 마법 지휘봉이란다! `DatabaseSeeder` 클래스에 실행 순서를 정해두고, `php artisan migrate:fresh --seed` 명령어를 실행하면, 기존 테이블을 깨끗이 밀어버리고(fresh) 마이그레이션과 1,000권 시딩을 단 3초 만에 완벽하게 적재해 준단다!"

🐶 **토토**: "멍멍! 대량 데이터를 넣을 때는 메모리가 터지지 않게 청크(Chunk) 단위로 쪼개어 시딩하는 것이 꿀팁이다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 서점의 실제 대분류/중분류 카테고리를 체계적으로 적재하는 `CategorySeeder`를 작성합니다.
2. 20개 출판사, 50명의 저자, 1,000권의 다채로운 도서를 대량 생성하는 `BookSeeder`를 구현합니다.
3. `php artisan migrate:fresh --seed` 명령어로 완벽하게 초기화된 서점 데이터베이스를 구축합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 개별 시더 파일 생성

아티산 명령어로 역할별 시더 클래스를 생성합니다:

```bash
php artisan make:seeder CategorySeeder
php artisan make:seeder BookSeeder
```

---

### [Step 2] `CategorySeeder.php` 계층형 카테고리 트리 작성

`database/seeders/CategorySeeder.php`에 대분류와 하위 소분류 트리를 정의합니다:

```php
namespace Database\Seeders;

use App\Models\Category;
use Illuminate\Database\Seeder;
use Illuminate\Support\Str;

class CategorySeeder extends Seeder
{
    public function run(): void
    {
        $catalog = [
            'IT / 컴퓨터' => [
                '웹 프로그래밍 (PHP, JS, Python)',
                '모바일 앱 개발 (Flutter, Swift)',
                '인공지능 및 딥러닝',
                '클라우드 및 DevOps',
                '데이터베이스 및 SQL',
            ],
            '경제 / 경영' => [
                '재테크 및 투자',
                '스타트업 창업 스토리',
                '마케팅 및 브랜딩',
            ],
            '인문 / 사회' => [
                '서양 철학',
                '역사와 문화',
                '심리학 이야기',
            ],
            '소설 / 문학' => [
                '한국 현대 소설',
                'SF 및 판타지',
                '에세이와 시',
            ],
        ];

        $order = 1;
        foreach ($catalog as $parentName => $subCategories) {
            // 대분류 생성
            $parent = Category::create([
                'name' => $parentName,
                'slug' => Str::slug($parentName),
                'order_num' => $order++,
                'parent_id' => null,
            ]);

            // 소분류 생성
            foreach ($subCategories as $subName) {
                Category::create([
                    'name' => $subName,
                    'slug' => Str::slug($subName),
                    'order_num' => $order++,
                    'parent_id' => $parent->id,
                ]);
            }
        }
    }
}
```

---

### [Step 3] `BookSeeder.php` 1,000권 도서 대량 시딩 작성

`database/seeders/BookSeeder.php`에서 출판사, 저자를 미리 생성하고 1,000권의 도서를 골고루 분배하여 생성합니다:

```php
namespace Database\Seeders;

use App\Models\Author;
use App\Models\Book;
use App\Models\Category;
use App\Models\Publisher;
use Illuminate\Database\Seeder;

class BookSeeder extends Seeder
{
    public function run(): void
    {
        // 1. 기본 출판사 15개 생성
        $publishers = Publisher::factory()->count(15)->create();

        // 2. 기본 저자 40명 생성
        $authors = Author::factory()->count(40)->create();

        // 3. 기존 등록된 소분류 카테고리 수집
        $categories = Category::whereNotNull('parent_id')->get();

        $this->command->info('📚 지니샵 1,000권의 도서 데이터를 시딩하는 중입니다...');

        // 4. 도서 1,000권 대량 생성 (할인 도서 및 전자책 비율 분배)
        for ($i = 0; $i < 1000; $i++) {
            $author = $authors->random();
            $publisher = $publishers->random();
            $category = $categories->random();

            $factory = Book::factory()->for($author)->for($publisher)->for($category);

            // 20% 확률로 10~30% 할인 도서 적용
            if (fake()->boolean(20)) {
                $factory = $factory->discounted(fake()->randomElement([10, 15, 20, 30]));
            }

            // 30% 확률로 전자책(eBook) 적용
            if (fake()->boolean(30)) {
                $factory = $factory->ebook();
            }

            // 5% 확률로 품절 도서 적용
            if (fake()->boolean(5)) {
                $factory = $factory->outOfStock();
            }

            $factory->create();
        }

        $this->command->info('✅ 1,000권의 도서 시딩 완료!');
    }
}
```

---

### [Step 4] `DatabaseSeeder.php` 통합 연결

`database/seeders/DatabaseSeeder.php`에서 시더 실행 순서를 조립합니다:

```php
namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // 1. 카테고리 먼저 적재
        $this->call(CategorySeeder::class);

        // 2. 출판사, 저자 및 1,000권 도서 적재
        $this->call(BookSeeder::class);
    }
}
```

---

### [Step 5] 원클릭 초기화 실행 (`migrate:fresh --seed`)

터미널에서 마법의 명령어를 가동합니다:

```bash
php artisan migrate:fresh --seed
```

> **터미널 출력:**
> ```text
>   Dropped all tables successfully.
>    INFO  Running migrations.
>   2026_09_25_000001_create_publishers_table .................... 12ms DONE
>   2026_09_25_000002_create_authors_table ....................... 10ms DONE
>   2026_09_25_000003_create_categories_table .................... 11ms DONE
>   2026_09_25_000004_create_books_table ......................... 18ms DONE
> 
>    INFO  Seeding database.
>   📚 지니샵 1,000권의 도서 데이터를 시딩하는 중입니다...
>   ✅ 1,000권의 도서 시딩 완료!
> ```

---

### [Step 6] 적재된 데이터 검증

Tinker로 시딩 결과를 즉시 검증합니다:

```bash
php artisan tinker --execute="echo '총 도서 수: ' . App\Models\Book::count() . '권 / 전자책: ' . App\Models\Book::where('format', 'ebook')->count() . '권';"
```
> **출력:** `총 도서 수: 1000권 / 전자책: 약 300권`

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 운영 서버에서의 `migrate:fresh` 방지 안전장치
- `migrate:fresh`는 기존 테이블과 데이터를 무조건 삭제하기 때문에, 만약 실제 상용(Production) 서버에서 실수로 실행하면 서비스 전체 데이터가 소실되는 대참사가 일어납니다.
- 라라벨은 `APP_ENV=production` 환경에서 파괴적인 명령어가 실행되면 자동으로 경고 프롬프트(`Do you really wish to run this command?`)를 띄우고 기본 실행을 차단하는 든든한 방패를 내장하고 있습니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **시더를 실행하다가 `Foreign key constraint fails` 에러가 나요!**  
>    자식 테이블을 시딩하기 전에 부모 데이터(`CategorySeeder`)가 먼저 실행되었는지 `DatabaseSeeder.php`의 `$this->call()` 순서를 꼭 점검하라멍!

---

## 💡 6. 4강 자가진단 과제

1. `Book::where('status', 'out_of_stock')->count()`로 품절 처리된 도서 수를 조회해 보세요.
2. `Book::whereNotNull('sale_price')->count()`로 할인 중인 도서 수를 확인해 보세요.
3. 이제 다음 5주차에서 이 1,000권의 도서를 브라우저 화면에서 페이징하고 정렬할 준비가 완벽히 끝났습니다!
{% endraw %}
