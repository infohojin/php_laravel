---
layout: docs
title: "03강: 관리자 전용 미들웨어(`EnsureUserIsAdmin`) & 서점 백오피스 대시보드"
---

{% raw %}
# 03강: 관리자 전용 미들웨어(`EnsureUserIsAdmin`) & 서점 백오피스 대시보드

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** HTTP 요청 전후 검문소 미들웨어, 라라벨 13의 `bootstrap/app.php` 미들웨어 별칭 등록, 서점 관리자 백오피스 대시보드  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [미들웨어 (Middleware)](../docs/04_the_basics/middleware_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 일반 고객이 주소창에 `jinyshop.test/admin/books`나 `/admin/sales`를 직접 치고 들어오면 매출 통계나 정산 내역이 다 털리잖아요! 관리자 권한(`is_admin === true`)이 없는 일반 사용자가 `/admin`으로 시작하는 모든 주소에 발도 못 붙이게 철통같이 지키려면 어떻게 해야 해요?"

🐱 **지니**: "도로시, 바로 그럴 때 사용하는 최고의 경비원이 **미들웨어(Middleware)**란다! 미들웨어는 컨트롤러 문앞에 서 있는 든든한 문지기와 같지. 요청이 들어왔을 때 '너 관리자 맞아?' 하고 신분증을 검사하여, 일반 독자나 비로그인 손님이면 컨트롤러 방을 보여주지도 않고 즉시 문전박대(403 Forbidden)한단다!"

🐶 **토토**: "멍멍! 라라벨 13에서는 구식 `Kernel.php` 파일 대신 `bootstrap/app.php`의 `->withMiddleware()` 체이닝에서 미들웨어 별칭(`'admin'`)을 등록하면 깔끔하게 끝난다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 관리자 권한을 엄격히 판별하는 커스텀 미들웨어 `EnsureUserIsAdmin`을 작성합니다.
2. 라라벨 13의 `bootstrap/app.php`에 미들웨어 별칭을 등록합니다.
3. 총 도서 수, 품절 도서, 오늘 매출을 요약해 보여주는 `/admin/dashboard` 백오피스를 구축합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `EnsureUserIsAdmin` 미들웨어 생성

아티산 명령어로 미들웨어를 생성합니다:

```bash
php artisan make:middleware EnsureUserIsAdmin
```

`app/Http/Middleware/EnsureUserIsAdmin.php`에 검문 로직을 작성합니다:

```php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsAdmin
{
    /**
     * 들어오는 요청을 검사
     */
    public function handle(Request $request, Closure $next): Response
    {
        // 1. 비로그인 손님이거나 관리자가 아닌 경우 차단!
        if (! $request->user() || ! $request->user()->is_admin) {
            abort(403, '⛔ 이 페이지는 지니샵 관리자만 접근할 수 있는 비밀 구역입니다.');
        }

        // 2. 관리자 통과! 다음 미들웨어 또는 컨트롤러로 요청 전달
        return $next($request);
    }
}
```

---

### [Step 2] `bootstrap/app.php`에 미들웨어 별칭 등록

라라벨 13 표준 방식으로 미들웨어 별칭(`alias`)을 정의합니다:

```php
// bootstrap/app.php
use App\Http\Middleware\EnsureUserIsAdmin;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    // ... 기존 라우팅 설정 ...
    ->withMiddleware(function (Middleware $middleware) {
        // 미들웨어 별칭 등록 (라우트에서 'admin' 이름으로 호출 가능!)
        $middleware->alias([
            'admin' => EnsureUserIsAdmin::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
```

---

### [Step 3] 백오피스 라우트 그룹 및 대시보드 뷰 구성

`routes/web.php`에 관리자 전용 라우트 그룹을 `['auth', 'admin']`으로 감쌉니다:

```php
// routes/web.php
use App\Models\Book;
use App\Models\Order;
use App\Models\Review;

Route::prefix('admin')->name('admin.')->middleware(['auth', 'admin'])->group(function () {
    Route::get('/dashboard', function () {
        // 실시간 서점 운영 지표 집계
        $stats = [
            'total_books' => Book::count(),
            'out_of_stock_books' => Book::where('status', 'out_of_stock')->orWhere('stock_quantity', 0)->count(),
            'total_sales' => Order::where('status', 'paid')->sum('total_amount'),
            'recent_reviews_count' => Review::whereDate('created_at', today())->count(),
        ];

        return view('admin.dashboard', compact('stats'));
    })->name('dashboard');

    // 기타 관리자 도서 관리 라우트들...
});
```

`resources/views/admin/dashboard.blade.php` 템플릿:
```html
<x-layouts.app>
    <x-slot:title>지니샵 백오피스 관리자 대시보드</x-slot:title>

    <div class="max-w-6xl mx-auto py-6">
        <h1 class="text-2xl font-bold text-slate-800 mb-6 flex items-center space-x-2">
            <span>🛡️</span>
            <span>지니샵 총괄 관리자 관제탑</span>
        </h1>

        <!-- 4개 핵심 운영 지표 카드 -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <span class="text-xs font-bold text-indigo-500 uppercase">전체 등록 도서</span>
                <p class="text-3xl font-extrabold text-slate-800 mt-2">{{ number_format($stats['total_books']) }}권</p>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <span class="text-xs font-bold text-rose-500 uppercase">품절 / 재고 부족</span>
                <p class="text-3xl font-extrabold text-rose-600 mt-2">{{ number_format($stats['out_of_stock_books']) }}권</p>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <span class="text-xs font-bold text-emerald-500 uppercase">총 누적 매출액</span>
                <p class="text-3xl font-extrabold text-emerald-600 mt-2">{{ number_format($stats['total_sales']) }}원</p>
            </div>

            <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
                <span class="text-xs font-bold text-amber-500 uppercase">오늘 등록된 서평</span>
                <p class="text-3xl font-extrabold text-amber-600 mt-2">{{ number_format($stats['recent_reviews_count']) }}개</p>
            </div>
        </div>
    </div>
</x-layouts.app>
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 전처리 미들웨어 vs 후처리(Terminating) 미들웨어
- `handle()` 메서드에서 `$next($request)`를 호출하기 **전**에 코드를 실행하면 **전처리(Pre-middleware, 권한 검사, 로깅 시작)**가 됩니다.
- `$response = $next($request)`를 호출한 **후**에 코드를 실행하면 **후처리(Post-middleware, 응답 헤더 추가, 캐시 헤더 부여)**가 됩니다.
- 나아가 `terminate(Request $request, Response $response)` 메서드를 구현하면 브라우저에 화면이 전송된 직후 무거운 사후 작업(접속 통계 기록 등)을 비동기처럼 처리할 수 있습니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **관리자 계정은 어떻게 만드나요?**  
>    Tinker에서 `$user = User::first(); $user->is_admin = true; $user->save();` 한 줄만 치면 1초 만에 도로시가 서점 총괄 관리자가 된다멍!

---

## 💡 6. 3강 자가진단 과제

1. 일반 독자 계정으로 로그인한 상태에서 `http://127.0.0.1:8000/admin/dashboard`에 접속해 보세요. 403 Forbidden 차단 메시지가 뜨는지 확인하세요.
2. 관리자 권한을 부여한 뒤 접속하여 도서 수량과 총매출액이 실시간 집계되어 카드로 표시되는지 검증하세요.
{% endraw %}
