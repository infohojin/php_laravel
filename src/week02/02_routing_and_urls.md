---
layout: docs
title: "02강: 도서 서점 라우팅 설계 & 보안 서명된 URL (Signed URLs)"
---

{% raw %}
# 02강: 도서 서점 라우팅 설계 & 보안 서명된 URL (Signed URLs)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** HTTP 라우팅 설계, 파라미터 제약조건, 라우트 그룹, 전자책 샘플 다운로드를 위한 Signed URLs  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [라우팅 (Routing)](../docs/04_the_basics/routing_ko.md), [URL 생성 (URL Generation)](../docs/04_the_basics/urls_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리 서점에는 책 목록 조회(`/books`), 책 상세 보기(`/books/978896626`), 장바구니 담기, 주문 결제까지 주소가 수십 개는 필요하잖아요. 나중에 주소 체계를 바꿀 때 HTML 링크를 일일이 다 고치지 않으려면 어떻게 설계해야 해요? 그리고 전자책(eBook) 미리보기 샘플 PDF 링크를 누군가 인터넷에 무단 배포하면 어쩌죠?"

🐱 **지니**: "도로시의 고민은 실무에서도 매일 부딪히는 문제란다! 라라벨에서는 첫째, **명명된 라우트(Named Routes)**를 사용하면 URL 주소가 바뀌어도 링크가 절대 깨지지 않는단다. 둘째, 전자책 파일이나 주문 영수증처럼 민감한 URL에는 **서명된 URL(Signed URLs)** 마법을 걸 수 있지! 유효기간(예: 30분)과 변조 방지 디지털 서명이 포함되어, 링크를 복사해 가거나 URL 파라미터를 조작하면 즉시 403 Forbidden으로 튕겨낸단다!"

🐶 **토토**: "멍멍! 라우트 파라미터에 숫자가 와야 하는 책 ID 자리에 문자가 들어오지 못하게 `whereNumber('id')` 정규식 가드도 걸어주면 해킹 시도를 원천 차단할 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 지니샵 도서 쇼핑몰의 RESTful URL 구조를 체계적으로 설계합니다.
2. 명명된 라우트(`name()`)와 라우트 그룹(`prefix`, `as`)을 활용해 유지보수성을 극대화합니다.
3. 전자책 미리보기 샘플 다운로드를 위한 30분 유효기간의 **Signed URL**을 생성하고 검증합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `routes/web.php`에 도서 서점 라우트 체계 구축

`routes/web.php`를 열고 서점의 핵심 URL 경로를 그룹 단위로 정의합니다.

```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\URL;

// 1. 서점 메인 홈
Route::get('/', function () {
    return view('welcome');
})->name('home');

// 2. 도서(Books) 라우트 그룹
Route::prefix('books')->name('books.')->group(function () {
    // 도서 카탈로그 목록 (GET /books)
    Route::get('/', function () {
        return "📚 지니샵 전체 도서 목록 화면입니다.";
    })->name('index');

    // 베스트셀러 목록 (GET /books/bestsellers)
    Route::get('/bestsellers', function () {
        return "🔥 이번 주 베스트셀러 도서 목록입니다.";
    })->name('bestsellers');

    // 도서 상세 보기 (GET /books/{id}) - 숫자 ID 제약조건 부여
    Route::get('/{id}', function (string $id) {
        return "📖 도서 ID [{$id}]번 상세 정보 화면입니다.";
    })->whereNumber('id')->name('show');

    // ISBN 검색 (GET /books/isbn/{isbn}) - 13자리 숫자 제약
    Route::get('/isbn/{isbn}', function (string $isbn) {
        return "🔍 ISBN [{$isbn}] 도서 검색 결과입니다.";
    })->where('isbn', '^[0-9]{13}$')->name('isbn');
});
```

---

### [Step 2] 라우트 목록 확인 (`route:list`)

터미널에서 방금 등록한 서점 라우트들이 올바르게 등록되었는지 검사합니다:

```bash
php artisan route:list --path=books
```

> **터미널 출력:**
> ```text
>   GET|HEAD   books ................................ books.index
>   GET|HEAD   books/bestsellers .................... books.bestsellers
>   GET|HEAD   books/isbn/{isbn} .................... books.isbn
>   GET|HEAD   books/{id} ........................... books.show
> ```

---

### [Step 3] 30분 만료 서명된 URL(Signed URL) 생성 실습

전자책(eBook) 미리보기 샘플 PDF를 안전하게 다운로드할 수 있는 임시 링크 생성 엔드포인트를 구현합니다.

```php
// routes/web.php 에 추가

// 1. 임시 다운로드 링크 발급 엔드포인트
Route::get('/books/{id}/generate-preview-url', function (int $id) {
    // 현재 시간으로부터 30분 동안만 유효한 암호화 서명된 URL 생성
    $downloadUrl = URL::temporarySignedRoute(
        'books.download-preview',
        now()->addMinutes(30),
        ['id' => $id, 'format' => 'pdf']
    );

    return response()->json([
        'book_id' => $id,
        'signed_download_url' => $downloadUrl,
        'expires_in' => '30분',
    ]);
})->name('books.generate-preview');

// 2. 실제 파일 다운로드 라우트 (signed 미들웨어로 보호!)
Route::get('/books/{id}/download-preview', function (Request $request, int $id) {
    // signed 미들웨어가 위조나 만료 여부를 자동 검증함
    return "✅ 디지털 서명 검증 성공! [{$id}]번 도서의 샘플 eBook 다운로드를 시작합니다.";
})->name('books.download-preview')->middleware('signed');
```

---

### [Step 4] 브라우저에서 Signed URL 위변조 방어 테스트

1. 브라우저에서 `http://127.0.0.1:8000/books/101/generate-preview-url` 에 접속합니다.
2. 발급된 `signed_download_url` 주소를 복사하여 새 탭에 붙여넣습니다:
   - URL 예시: `http://127.0.0.1:8000/books/101/download-preview?expires=...&signature=...`
   - 정상 접속되어 다운로드 메시지가 뜹니다.
3. 이제 주소창에서 `signature=...` 뒤의 글자 하나를 임의로 바꾸고 엔터를 칩니다!
4. **결과:** 라라벨이 디지털 서명 위조를 즉시 감지하고 **`403 Invalid Signature`** 에러 화면으로 차단합니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `route()` 헬퍼 함수의 우아함
- 뷰 템플릿에서 `<a href="/books/{{ $book->id }}">`처럼 URL 문자열을 하드코딩하면 나중에 경로를 `/shop/books/...`로 바꿀 때 전수 수정을 해야 합니다.
- 대신 `<a href="{{ route('books.show', $book->id) }}">`를 사용하면, 라우트 정의만 수정해도 전 사이트의 링크가 일제히 자동 갱신됩니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **도서 상세 라우트(`books/{id}`)가 베스트셀러(`books/bestsellers`)를 먹어버려요!**  
>    라우트는 위에서부터 차례대로 매칭된다멍! 와일드카드 파라미터(`{id}`)보다 고정된 주소(`bestsellers`)를 반드시 위쪽에 먼저 선언해야 한다멍!
> 
> 2. **모바일 손님이 Signed URL을 누를 때 앱 주소가 다르면 서명이 깨지나요?**  
>    `.env`의 `APP_URL`과 실제 접속 도메인이 다르면 서명 검증이 실패할 수 있으니 `APP_URL`을 정확히 일치시켜야 한다멍!

---

## 💡 6. 2강 자가진단 과제

1. 도서 출판 연도별 아카이브 라우트(`GET /books/year/{year}`)를 선언하고, 4자리 연도만 들어오도록 `where('year', '^[0-9]{4}$')` 제약조건을 걸어보세요.
2. 유효기간이 5초인 임시 링크를 생성한 뒤, 6초 후에 접속하여 만료된 링크가 403 에러로 방어되는지 확인해 보세요.
{% endraw %}
