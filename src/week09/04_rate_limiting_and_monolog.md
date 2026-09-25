---
layout: docs
title: "04강: Rate Limiting 악의적 봇 방어 & 감사 로깅/커스텀 에러 페이지"
---

{% raw %}
# 04강: Rate Limiting 악의적 봇 방어 & 감사 로깅/커스텀 에러 페이지

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 분당 요청 제한(Rate Limiting), 429 Too Many Requests 방어선, Monolog 일별 감사 로깅, 예쁜 404/500 에러 페이지 커스터마이징  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [속도 제한 (Rate Limiting)](../docs/05_digging_deeper/rate-limiting_ko.md), [에러 핸들링 (Error Handling)](../docs/04_the_basics/errors_ko.md), [로깅 (Logging)](../docs/04_the_basics/logging_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 악성 크롤러 봇들이 우리 서점의 도서 검색창에 1초에 1,000번씩 검색 쿼리를 날려서 데이터베이스를 다운시키려고 해요! 그리고 결제 버튼을 연속으로 마구 연타하는 매크로 공격은 어떻게 막아야 하나요? 게다가 고객이 오타를 내서 404가 떴을 때 검은색 영문 에러 창 대신 귀여운 지니샵 캐릭터가 사과하는 예쁜 에러 화면을 보여주고 싶어요!"

🐱 **지니**: "도로시, 백엔드 엔지니어링의 정수를 꿰뚫었구나! 라라벨의 **Rate Limiter(속도 제한기)**는 IP나 사용자 ID별로 '분당 최대 30회' 같은 임계치를 두어, 봇이 한계를 넘는 순간 **`429 Too Many Requests`**로 즉시 셧다운시키지. 그리고 모든 수상한 행위는 **Monolog** 채널에 감사 로그로 남긴단다. 또한 `resources/views/errors/404.blade.php` 파일 하나만 만들면 라라벨이 자동으로 사랑스러운 커스텀 에러 화면을 띄워준단다!"

🐶 **토토**: "멍멍! 슬랙(Slack) 채널 웹훅을 연결해 두면, 서버에 500 치명적 에러가 났을 때 개발팀 폰으로 삐뽀삐뽀 즉각 알림이 울린다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 도서 검색 및 장바구니 결제 요청에 분당 횟수 제한(Rate Limiting)을 겁니다.
2. `Log::warning()`과 `Log::error()`를 사용해 일별 회전(`daily`) 보안 감사 로그를 기록합니다.
3. 지니와 토토 캐릭터가 들어간 감성적인 404 Not Found 커스텀 에러 뷰를 제작합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 도서 검색 전용 Rate Limiter 정의

`app/Providers/AppServiceProvider.php`에 도서 검색용 쓰로틀링(Throttling) 규칙을 선언합니다:

```php
// app/Providers/AppServiceProvider.php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Http\Request;

public function boot(): void
{
    // 동일 IP당 1분에 최대 30회까지만 검색 허용!
    RateLimiter::for('book-search', function (Request $request) {
        return Limit::perMinute(30)->by($request->ip())->response(function () {
            return response()->json([
                'error' => 'Too Many Requests',
                'message' => '🚨 단시간에 너무 많은 도서 검색 요청이 감지되었습니다. 1분 후 다시 시도해 주세요.',
            ], 429);
        });
    });
}
```

`routes/web.php` 라우트에 미들웨어 연결:
```php
Route::get('/books', [BookController::class, 'index'])
    ->middleware('throttle:book-search')
    ->name('books.index');
```

---

### [Step 2] 보안 감사 로깅 (`config/logging.php`)

비정상 결제 시도나 품절 도서 강제 요청 발생 시 일별 회전 로그 파일에 기록합니다:

```php
// app/Http/Controllers/CartController.php 등에서
use Illuminate\Support\Facades\Log;

if ($suspiciousActivity) {
    Log::channel('daily')->warning('🚨 비정상 대량 장바구니 담기 감지!', [
        'ip' => request()->ip(),
        'user_id' => auth()->id() ?? 'guest',
        'requested_qty' => $quantity,
        'user_agent' => request()->userAgent(),
    ]);
}
```

> **`storage/logs/laravel-2026-09-25.log` 에 찍힌 기록:**
> ```text
> [2026-09-25 02:26:00] local.WARNING: 🚨 비정상 대량 장바구니 담기 감지! {"ip":"127.0.0.1","user_id":"guest","requested_qty":999}
> ```

---

### [Step 3] 커스텀 404 Not Found 에러 화면 제작

라라벨은 `resources/views/errors/{상태코드}.blade.php` 파일이 존재하면 에러 발생 시 기본 뷰 대신 해당 파일을 우선 렌더링합니다:

`resources/views/errors/404.blade.php`:
```html
<x-layouts.app>
    <x-slot:title>책을 찾을 수 없습니다 — 404 에러</x-slot:title>

    <div class="py-20 text-center max-w-lg mx-auto">
        <span class="text-7xl">🐱🔍</span>
        <h1 class="text-3xl font-extrabold text-slate-800 mt-6">길을 잃은 책을 찾고 계신가요?</h1>
        <p class="text-slate-500 mt-2 text-sm">
            요청하신 도서 페이지가 절판되었거나, 주소가 잘못 입력되었습니다.<br>
            지니와 도로시가 다른 좋은 책들을 찾아 드릴게요!
        </p>

        <div class="mt-8 flex justify-center space-x-4">
            <a href="{{ route('home') }}" class="px-5 py-2.5 bg-indigo-600 text-white font-bold rounded-xl shadow hover:bg-indigo-700 transition">
                서점 홈으로 이동
            </a>
            <a href="{{ route('books.index') }}" class="px-5 py-2.5 bg-slate-100 text-slate-700 font-bold rounded-xl hover:bg-slate-200 transition">
                전체 도서 둘러보기
            </a>
        </div>
    </div>
</x-layouts.app>
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `abort(404)`의 우아한 마법
- 컨트롤러 내부에서 원하는 책을 찾지 못했을 때 `$book = Book::where('slug', $slug)->firstOrFail();` 또는 `abort(404);`를 호출하기만 하면 됩니다.
- 라라벨의 예외 처리 관제탑(`bootstrap/app.php`)이 이를 가로채어 앞서 만든 예쁜 `resources/views/errors/404.blade.php` 화면으로 알아서 포워딩합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **테스트할 때 Rate Limit에 걸려서 내가 쫓겨났어요!**  
>    터미널에 `php artisan cache:clear`를 치면 캐시에 기록된 IP별 호출 횟수가 싹 초기화된다멍!

---

## 💡 6. 4강 자가진단 과제

1. 브라우저 주소창에 존재하지 않는 도서 주소(`http://127.0.0.1:8000/books/unknown-never-exist`)를 쳤을 때 우리가 만든 귀여운 지니 404 에러 화면이 뜨는지 확인하세요.
2. 새로고침을 31번 연속으로 눌렀을 때 31번째 요청에서 429 Too Many Requests 에러가 뜨는지 확인하세요.
{% endraw %}
