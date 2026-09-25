---
layout: docs
title: "04강: SEO 친화적 슬러그(`Str::slug`) & 소프트 삭제(`SoftDeletes`) 복구"
---

{% raw %}
# 04강: SEO 친화적 슬러그(`Str::slug`) & 소프트 삭제(`SoftDeletes`) 복구

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 문자열 조작(`Str::slug`), 라우트 모델 바인딩 커스텀 키(`{book:slug}`), 소프트 삭제의 수명주기(`trashed`, `restore`, `forceDelete`)  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Eloquent 시작하기 (Eloquent)](../docs/08_eloquent_orm/eloquent_ko.md), [문자열 (Strings)](../docs/05_digging_deeper/strings_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 책 주소가 `jinyshop.test/books/142` 처럼 숫자 ID로 되어 있으면 구글 검색엔진이 이 책이 무슨 책인지 알기 어렵잖아요. `jinyshop.test/books/laravel-13-master-class` 처럼 예쁜 영문 슬러그(Slug) 주소로 바꿀 수 있나요? 그리고 만약 서점 관리자가 실수로 베스트셀러 책을 삭제 버튼 눌러버리면 어떻게 복구하나요?"

🐱 **지니**: "도로시, 바로 그 두 가지가 실무 서비스의 완성도를 결정짓는 디테일이란다! 라라벨의 **`Str::slug()`** 헬퍼를 쓰면 한글 책 제목도 군더더기 없는 완벽한 SEO 슬러그로 변환할 수 있고, 라우트 모델 바인딩 `{book:slug}`를 쓰면 컨트롤러에서 ID 대신 슬러그로 즉시 책을 찾아내지! 그리고 실수로 삭제한 책은 **`SoftDeletes`** 마법 덕분에 `restore()` 한 줄이면 휴지통에서 새 책처럼 완벽 복원된단다!"

🐶 **토토**: "멍멍! 관리자 화면에서는 `Book::onlyTrashed()`로 삭제된 도서 목록만 모아서 조회하고 영구 삭제(`forceDelete`)할 수도 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. `Str::slug()` 및 모델 라이프사이클 이벤트(`booted`)를 통해 책 제목으로부터 고유 슬러그를 자동 생성합니다.
2. 숫자 ID 대신 슬러그로 책을 조회하는 커스텀 라우트 모델 바인딩(`books/{book:slug}`)을 적용합니다.
3. 소프트 삭제된 도서 조회, 복원(`restore()`), 영구 삭제(`forceDelete()`) 절차를 실습합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `Book` 모델에 자동 슬러그 생성 로직 추가

`app/Models/Book.php`에 모델 이벤트 훅 `booted()`를 선언합니다:

```php
// app/Models/Book.php
use Illuminate\Support\Str;

protected static function booted(): void
{
    // 신규 도서 저장 시 slug가 비어있으면 제목 기반 자동 생성
    static::creating(function (Book $book) {
        if (empty($book->slug)) {
            // 한글 및 특수문자 안전 변환 + 고유성 유지를 위한 랜덤 숫자 접미사
            $baseSlug = Str::slug($book->title);
            $book->slug = $baseSlug ?: 'book-'.fake()->numerify('####');
        }
    });
}
```

---

### [Step 2] 슬러그 기반 라우트 모델 바인딩 설정

`routes/web.php`의 도서 상세 라우트를 ID 대신 `slug`로 조회하도록 수정합니다:

```php
// routes/web.php
use App\Models\Book;

// {book:slug} 표기법: 라라벨이 URL의 문자열로 Book::where('slug', $slug)->firstOrFail() 자동 수행!
Route::get('/books/{book:slug}', function (Book $book) {
    return view('books.show', compact('book'));
})->name('books.show');
```

> **지니의 감탄:**  
> 컨트롤러에서 `$book = Book::where('slug', $slug)->firstOrFail();`을 직접 작성하지 않아도 라라벨이 인젝션 단계에서 자동으로 조회하고 404 예외까지 처리해 준단다!

---

### [Step 3] 소프트 삭제(Soft Deletes) 수명주기 실습

Tinker를 열어 도서 삭제 및 복구 프로세스를 직접 실행해 봅니다:

```bash
php artisan tinker
```

```php
// 1. 도서 한 권 조회
$book = App\Models\Book::first();
echo "책 제목: " . $book->title;

// 2. 도서 삭제 실행
$book->delete();

// 3. 삭제 여부 확인
echo "삭제 상태인가요? " . ($book->trashed() ? '네, 휴지통에 있습니다.' : '아니오');
// 결과: 네, 휴지통에 있습니다.

// 4. 일반 도서 조회 쿼리에서는 자동으로 제외됨!
$found = App\Models\Book::find($book->id);
echo "일반 조회 결과: " . ($found ? '조회됨' : '자동 제외됨 (null)');
// 결과: 자동 제외됨 (null)

// 5. 휴지통 포함 조회 (관리자용)
$trashedBook = App\Models\Book::withTrashed()->find($book->id);
echo "휴지통 조회 결과: " . $trashedBook->title;

// 6. 삭제된 도서 기적의 복구!
$trashedBook->restore();
echo "복구 후 상태: " . ($trashedBook->trashed() ? '삭제상태' : '정상 출판 상태로 복원 완료!');
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `Str::of()` Fluent Stringable 인터페이스
라라벨의 `Str` 파사드는 문자열을 물 흐르듯 다듬는 Fluent 인터페이스를 제공합니다:

```php
$summary = Str::of($book->description)
    ->trim()
    ->limit(100, '... (더보기)')
    ->title();
```
도서 상세 소개글에서 앞 100자만 잘라내어 목록 카드에 표시할 때 매우 유용합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **휴지통에 있는 책을 영구히 지우려면요?**  
>    `$book->forceDelete()`를 호출하면 데이터베이스에서 레코드가 물리적으로 완전히 지워진다멍! 되돌릴 수 없으니 관리자 비밀번호 확인이 필수다멍!

---

## 💡 6. 4강 자가진단 과제

1. 브라우저에서 실제 시딩된 책 중 하나의 슬러그 주소(예: `http://127.0.0.1:8000/books/실제슬러그문자열`)로 접속하여 상세 페이지가 성공적으로 열리는지 확인하세요.
2. 특정 도서를 `$book->delete()` 한 뒤 브라우저에서 해당 슬러그로 접속했을 때 라라벨이 자동으로 `404 Not Found` 화면을 띄우는지 확인해 보세요.
{% endraw %}
