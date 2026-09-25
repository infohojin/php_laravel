---
layout: docs
title: "04강: 응답(Response)의 다양한 변신 & 리다이렉트와 플래시 메시지"
---

{% raw %}
# 04강: 응답(Response)의 다양한 변신 & 리다이렉트와 플래시 메시지

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** Blade 뷰 반환, JSON 응답, 전자책 샘플 PDF 다운로드, 리다이렉트 및 1회성 플래시 세션 메시지  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [응답 (Responses)](../docs/04_the_basics/responses_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 컨트롤러에서 항상 문자열이나 JSON만 돌려줄 수는 없잖아요. 독자가 웹 브라우저로 들어오면 예쁜 HTML 화면을 보여줘야 하고, 모바일 앱에서 들어오면 JSON 데이터를 줘야 하고, 전자책 미리보기 버튼을 누르면 PDF 파일을 바로 다운로드시켜 줘야 하잖아요. 그리고 책을 장바구니에 담은 뒤에는 '장바구니에 담겼습니다!'라는 안내와 함께 장바구니 화면으로 보내주려면 어떻게 해야 해요?"

🐱 **지니**: "도로시가 서점의 모든 고객 여정을 완벽하게 꿰뚫어 보고 있구나! 라라벨의 `Response` 팩토리는 카멜레온처럼 원하는 모든 형태로 변신할 수 있단다. `view()`로 HTML 템플릿을 렌더링하고, `response()->json()`으로 모바일 데이터를 쏘아주고, `response()->download()`로 책 파일을 전송하지. 그리고 `redirect()->route()->with()`를 쓰면 다음 화면에만 반짝 나타났다 사라지는 **플래시 메시지(Flash Message)**를 띄울 수 있단다!"

🐶 **토토**: "멍멍! HTTP 상태 코드도 중요해! 새 도서가 성공적으로 등록되었을 땐 200이 아니라 201 Created를 돌려주고, 품절되었을 땐 404나 410을 돌려주는 것이 웹 표준 매너다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨 `response()` 헬퍼가 제공하는 다양한 응답 유형(View, JSON, Download, Stream)을 구현합니다.
2. 새 도서 등록 후 상세 페이지로 이동시키는 안전한 리다이렉트 흐름을 만듭니다.
3. 세션 기반 1회성 플래시 메시지(`with('status', '...')`)를 생성하고 뷰에서 표시합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 응답 유형별 컨트롤러 메서드 구현

`app/Http/Controllers/BookController.php`에 다양한 응답을 반환하는 메서드들을 추가합니다:

```php
// app/Http/Controllers/BookController.php 에 추가

use Symfony\Component\HttpFoundation\BinaryFileResponse;
use Illuminate\Http\RedirectResponse;

/**
 * 1. 신규 도서 등록 처리 후 리다이렉트 (PRG 패턴)
 */
public function store(Request $request): RedirectResponse
{
    // (4주차에서 실제 데이터베이스에 저장할 예정입니다)
    $newBookId = 101;

    // 도서 상세 화면으로 리다이렉트하면서 1회성 성공 플래시 메시지 전달
    return redirect()
        ->route('books.show', $newBookId)
        ->with('success', '🎉 새 도서가 지니샵에 성공적으로 등록되었습니다!');
}

/**
 * 2. 전자책(eBook) 미리보기 샘플 PDF 다운로드 응답
 */
public function downloadSample(int $id): BinaryFileResponse
{
    // storage/app/samples/book_sample.pdf 파일 경로 지정
    $filePath = storage_path('app/samples/laravel13_sample.pdf');

    // 파일이 없을 경우 더미 파일 즉석 생성 (실습용)
    if (!file_exists($filePath)) {
        if (!is_dir(dirname($filePath))) {
            mkdir(dirname($filePath), 0755, true);
        }
        file_put_contents($filePath, "%PDF-1.4 지니샵 도서 미리보기 샘플 내용...");
    }

    // 다운로드 시 브라우저에 표시될 파일명 지정
    return response()->download($filePath, "JinyShop_도서샘플_{$id}.pdf", [
        'Content-Type' => 'application/pdf',
    ]);
}
```

---

### [Step 2] 플래시 메시지를 표시하는 Blade 뷰 작성

`resources/views/books/show.blade.php` 파일을 생성하여 리다이렉트된 플래시 메시지와 도서 정보를 렌더링합니다.

```html
<!-- resources/views/books/show.blade.php -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>지니샵 도서 상세 - {{ $book['title'] }}</title>
    <style>
        body { font-family: sans-serif; padding: 2rem; background: #f8fafc; }
        .alert-success { background: #dcfce7; border: 1px solid #86efac; color: #166534; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); max-width: 600px; }
        .btn { display: inline-block; background: #4f46e5; color: white; padding: 0.5rem 1rem; border-radius: 6px; text-decoration: none; margin-top: 1rem; }
    </style>
</head>
<body>
    <div class="card">
        <!-- 세션 플래시 메시지가 있을 때만 반짝 렌더링 -->
        @if (session('success'))
            <div class="alert-success">
                {{ session('success') }}
            </div>
        @endif

        <h1>📖 {{ $book['title'] }}</h1>
        <p><strong>저자:</strong> {{ $book['author'] }}</p>
        <p><strong>출판사:</strong> {{ $book['publisher'] }}</p>
        <p><strong>정가:</strong> {{ number_format($book['price']) }}원</p>

        <a href="{{ route('books.download-sample', $book['id']) }}" class="btn">
            📥 전자책 미리보기 샘플 다운로드 (PDF)
        </a>
    </div>
</body>
</html>
```

---

### [Step 3] `BookController@show`에서 뷰 반환 연결

`BookController@show` 메서드가 위 Blade 템플릿을 반환하도록 수정합니다:

```php
public function show(string $id)
{
    $book = [
        'id' => (int) $id,
        'title' => '라라벨 13 마스터 클래스',
        'author' => '지니 & 도로시',
        'publisher' => '지니서적',
        'price' => 32000,
    ];

    return view('books.show', compact('book'));
}
```

---

### [Step 4] 라우트 등록 및 브라우저 테스트

`routes/web.php`에 샘플 다운로드 라우트를 연결합니다:

```php
Route::get('/books/{id}/download-sample', [BookController::class, 'downloadSample'])
    ->name('books.download-sample');
```

1. 브라우저에서 `http://127.0.0.1:8000/books/1` 에 접속하여 도서 상세 카드 화면을 확인합니다.
2. [전자책 미리보기 샘플 다운로드] 버튼을 클릭하면 `JinyShop_도서샘플_1.pdf` 파일이 브라우저 다운로드 창에 즉시 저장됩니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### Post-Redirect-Get (PRG) 패턴
- 서점에서 사용자가 폼으로 책을 주문하거나 등록(`POST /books`)한 뒤 바로 뷰를 반환하면, 고객이 브라우저에서 'F5(새로고침)'를 누를 때마다 중복 주문이 발생합니다.
- 라라벨은 항상 `POST` 처리 후 `redirect()->route()`를 통해 `GET` 주소로 리다이렉트하는 **PRG 패턴**을 기본 준수하도록 설계되어 있습니다.
- 이때 세션 플래시 데이터(`with('success', ...)`)는 오직 다음번 단 한 번의 HTTP 요청 동안만 메모리에 유지된 뒤 자동 소멸합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **고객이 결제하다가 이전 페이지로 돌아가게 하고 싶어요!**  
>    `return back()->withInput()`을 쓰면 고객이 이전에 입력했던 주소와 전화번호를 그대로 유지한 채 이전 화면으로 쓩 돌아간다멍! 폼 다시 채우게 하면 손님들이 화낸다멍!

---

## 💡 6. 4강 자가진단 과제

1. `routes/web.php`에 임의의 `POST /books/test-store` 라우트를 만들고, 브라우저나 Postman에서 호출했을 때 `books.show` 화면으로 리다이렉트되며 녹색 성공 플래시 알림이 뜨는지 확인하세요.
2. `response()->json()`을 사용하여 201 Created HTTP 상태 코드를 포함한 JSON 응답을 반환하는 테스트 엔드포인트를 만들어 보세요.
{% endraw %}
