---
layout: docs
title: "02강: 도서 서점 핵심 스키마 마이그레이션(Migration) 설계"
---

{% raw %}
# 02강: 도서 서점 핵심 스키마 마이그레이션(Migration) 설계

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 출판사, 저자, 카테고리, 도서 테이블 스키마 설계, 외래키 제약조건 및 마이그레이션 라이프사이클  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [마이그레이션 (Migrations)](../docs/07_database/migrations_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 책(`books`) 한 권이 서점에 등록되려면 쓴 사람(**저자**, Author)이 있어야 하고, 책을 펴낸 **출판사**(Publisher)가 있어야 하고, 'IT/프로그래밍' 같은 **카테고리**(Category)에 속해야 하잖아요. 이 복잡한 외래키 연결과 테이블들을 팀원들과 협업할 때 어떻게 스키마 충돌 없이 관리할 수 있나요?"

🐱 **지니**: "도로시의 엔티티 관계 분석이 정말 정확하구나! 바로 그래서 라라벨의 **마이그레이션(Migration)**을 쓴단다. 데이터베이스 스키마를 순수 PHP 코드로 작성하여 깃(Git)으로 형상 관리하기 때문에, 팀원 누구든 `php artisan migrate` 한 줄만 치면 1초 만에 동일한 데이터베이스 구조를 얻게 되지. 실수가 있으면 `migrate:rollback`으로 타임머신처럼 되돌릴 수도 있단다!"

🐶 **토토**: "멍멍! `foreignId('author_id')->constrained()->cascadeOnDelete()` 처럼 우아한 플루언트 체이닝 문법을 쓰면 외래키 인덱스까지 자동으로 생성된다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 출판사(`publishers`), 저자(`authors`), 카테고리(`categories`), 도서(`books`) 테이블 마이그레이션을 순서대로 생성합니다.
2. 테이블 간 외래키(FK) 제약조건과 검색 속도 향상을 위한 인덱스를 설정합니다.
3. `php artisan migrate:status`와 `migrate:rollback` 명령어로 마이그레이션 라이프사이클을 실습합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 마이그레이션 파일 4종 생성

참조 무결성을 위해 외래키가 없는 부모 테이블부터 순서대로 아티산으로 생성합니다:

```bash
# 1. 출판사 테이블
php artisan make:migration create_publishers_table

# 2. 저자 테이블
php artisan make:migration create_authors_table

# 3. 계층형 카테고리 테이블
php artisan make:migration create_categories_table

# 4. 도서 테이블
php artisan make:migration create_books_table
```

---

### [Step 2] 각 마이그레이션 스키마 코드 작성

#### 1) 출판사 테이블 (`create_publishers_table.php`)
```php
public function up(): void
{
    Schema::create('publishers', function (Blueprint $table) {
        $table->id();
        $table->string('name')->comment('출판사 상호명');
        $table->string('code')->unique()->comment('출판사 고유 코드');
        $table->string('contact_email')->nullable();
        $table->string('website_url')->nullable();
        $table->timestamps();
    });
}
```

#### 2) 저자 테이블 (`create_authors_table.php`)
```php
public function up(): void
{
    Schema::create('authors', function (Blueprint $table) {
        $table->id();
        $table->string('name')->comment('저자 이름');
        $table->string('email')->nullable();
        $table->text('bio')->nullable()->comment('저자 약력 및 소개');
        $table->string('profile_photo_url')->nullable();
        $table->timestamps();
    });
}
```

#### 3) 계층형 카테고리 테이블 (`create_categories_table.php`)
```php
public function up(): void
{
    Schema::create('categories', function (Blueprint $table) {
        $table->id();
        // 상위 카테고리 (대분류일 경우 null, 하위분류일 경우 부모 ID 참조)
        $table->foreignId('parent_id')->nullable()->constrained('categories')->nullOnDelete();
        $table->string('name');
        $table->string('slug')->unique();
        $table->unsignedInteger('order_num')->default(0)->comment('전시 순서');
        $table->timestamps();
    });
}
```

#### 4) 도서 핵심 테이블 (`create_books_table.php`)
```php
public function up(): void
{
    Schema::create('books', function (Blueprint $table) {
        $table->id();
        $table->string('isbn', 13)->unique()->comment('국제표준도서번호 13자리');
        $table->string('title')->comment('도서 제목');
        $table->string('slug')->comment('SEO 친화적 URL 슬러그');
        
        // 외래키 관계 연결
        $table->foreignId('author_id')->constrained()->cascadeOnDelete();
        $table->foreignId('publisher_id')->constrained()->cascadeOnDelete();
        $table->foreignId('category_id')->constrained()->cascadeOnDelete();

        // 가격 및 재고
        $table->unsignedInteger('price')->comment('도서 정가');
        $table->unsignedInteger('sale_price')->nullable()->comment('할인 판매가');
        $table->unsignedInteger('stock_quantity')->default(0)->comment('실물 재고 수량');

        // 형태 및 파일 (종이책 / 전자책)
        $table->enum('format', ['paperback', 'hardcover', 'ebook'])->default('paperback');
        $table->string('ebook_file_path')->nullable()->comment('암호화된 eBook 파일 저장 경로');

        // 상세 정보
        $table->unsignedSmallInteger('page_count')->default(0)->comment('총 쪽수');
        $table->date('published_at')->comment('출간일');
        $table->text('description')->nullable()->comment('책 소개글');
        $table->enum('status', ['draft', 'published', 'out_of_stock'])->default('published');

        $table->timestamps();
        $table->softDeletes(); // 품절/절판 보존용 소프트 삭제

        // 복합 검색 속도 최적화를 위한 인덱스 지정
        $table->index(['category_id', 'status', 'published_at']);
        $table->index('price');
    });
}
```

---

### [Step 3] 마이그레이션 실행 및 상태 확인

터미널에서 마이그레이션을 가동합니다:

```bash
php artisan migrate
```

> **터미널 출력:**
> ```text
>    INFO  Running migrations.
> 
>   2026_09_25_000001_create_publishers_table .................... 12ms DONE
>   2026_09_25_000002_create_authors_table ....................... 10ms DONE
>   2026_09_25_000003_create_categories_table .................... 11ms DONE
>   2026_09_25_000004_create_books_table ......................... 18ms DONE
> ```

마이그레이션 진행 상태를 확인합니다:
```bash
php artisan migrate:status
```
모든 테이블의 Batch 번호와 함께 `Ran: Yes`가 표시되면 완벽합니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `softDeletes()` 소프트 삭제의 가치
- 일반적인 전자상거래에서 고객이 이미 주문한 책 데이터를 테이블에서 영구 삭제(`DELETE FROM books`)해버리면, 과거 주문 내역서의 외래키가 깨져서 정산 및 영수증 조회가 불가능해집니다.
- 라라벨의 `$table->softDeletes()`는 레코드를 물리적으로 지우지 않고 `deleted_at` 타임스탬프만 찍어둡니다.
- Eloquent ORM은 이후 쿼리할 때 `WHERE deleted_at IS NULL` 조건을 자동으로 붙여주므로 일반 검색에서는 숨겨지고, 관리자 정산 화면에서는 안전하게 조회할 수 있습니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`General error: 1215 Cannot add foreign key constraint` 에러가 나요!**  
>    참조하려는 부모 테이블(`authors`)이 아직 생성되지 않았는데 자식 테이블(`books`)을 먼저 만들려고 해서 그렇다멍! 마이그레이션 파일명 앞의 타임스탬프 날짜 순서를 꼭 부모 $\rightarrow$ 자식 순으로 맞춰야 한다멍!

---

## 💡 6. 2강 자가진단 과제

1. `php artisan migrate:rollback --step=1`을 실행하여 `books` 테이블만 깔끔하게 롤백되는지 확인하세요.
2. 다시 `php artisan migrate`를 실행하여 복구해 보세요.
3. `php artisan db:table books` 명령어로 외래키와 인덱스가 완벽히 세팅되었는지 확인하세요.
{% endraw %}
