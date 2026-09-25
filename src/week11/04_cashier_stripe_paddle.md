---
layout: docs
title: "11주차 04강: 라라벨 캐셔(Cashier Stripe & Paddle)를 이용한 정기 구독 및 글로벌 결제"
---

{% raw %}
# 📖 11주차 04강: 라라벨 캐셔(Cashier Stripe & Paddle)를 이용한 정기 구독 및 글로벌 결제

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** '이달의 책 정기 배송 북클럽' 멤버십 구독 비즈니스 모델을 구현하기 위해 라라벨 공식 결제 패키지인 Cashier(Stripe & Paddle)를 연동하고, 구독 생성/취소/유예기간(Grace Period) 및 웹훅(Webhook) 처리 방식을 마스터합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리 지니샵에서 '북클럽 멤버십' 서비스를 런칭하기로 했어! 매월 19,900원씩 정기 결제하면 매달 베스트셀러 1권 무료 배송에 전자책 무제한 대여 혜택을 주는 거야. 그런데 정기 결제 날짜 계산, 카드 변경, 결제 실패 시 재시도, 환불, 영수증 발행까지 직접 다 구현하려니까 머리가 터질 것 같아!"  
🐱 **지니**: "도로시, 바로 그럴 때 전 세계 수많은 SaaS와 이커머스가 사용하는 **라라벨 캐셔(Laravel Cashier)**를 쓰는 거란다! Stripe와 Paddle을 위한 라라벨 공식 패키지로, 복잡한 구독 라이프사이클을 Eloquent 메소드 몇 개로 완전히 정복할 수 있지!"  
🐶 **토토**: "멍멍! 게다가 해외 독자들을 위한 글로벌 결제나 국가별 부가세(VAT) 자동 계산까지 필요하다면 **Cashier Paddle**이 환상적인 대안이 된다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **라라벨 캐셔(Cashier Stripe) 패키지 설치 및 마이그레이션:** `Billable` 트레이트 연동
2. **단건 결제 및 정기 구독(Subscription) 생성:** 북클럽 정기 구독 결제 폼 연동
3. **구독 상태 조회 및 권한 제어:** `subscribed()`, `cancelled()`, `onGracePeriod()`
4. **글로벌 판매를 위한 Cashier Paddle의 개념과 특징 이해**
5. **웹훅(Webhook) 보안 처리:** 결제 성공/실패 시 비동기 DB 상태 동기화

---

## 🛠️ 단계별 실습 절차

### 1단계: Cashier 패키지 설치 및 환경 설정

터미널에서 Cashier Stripe 패키지를 설치합니다:

```bash
composer require laravel/cashier
php artisan migrate
```

> 💡 **Cashier 마이그레이션 내용:**  
> `users` 테이블에 `stripe_id`, `pm_type`, `pm_last_four`, `trial_ends_at` 컬럼이 추가되고, `subscriptions` 및 `subscription_items` 테이블이 생성되어 구독 내역을 자동으로 추적합니다!

`.env` 파일에 Stripe API 키를 입력합니다 (Stripe 대시보드 테스트 키 발급):

```env
STRIPE_KEY=pk_test_51...
STRIPE_SECRET=sk_test_51...
STRIPE_WEBHOOK_SECRET=whsec_...
CASHIER_CURRENCY=krw
```

---

### 2단계: User 모델에 `Billable` 트레이트 추가

`app/Models/User.php`에 `Laravel\Cashier\Billable` 트레이트를 추가합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use HasFactory, Notifiable, Billable;

    // ... 기존 코드 유지
}
```

---

### 3단계: 북클럽 구독 결제 페이지 및 SetupIntent 발급

신용카드 정보를 안전하게 Stripe 서버로 직접 전송(PCI-DSS 준수)하기 위해 클라이언트 비밀키(SetupIntent)를 발급받는 컨트롤러를 작성합니다.

`app/Http/Controllers/SubscriptionController.php`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class SubscriptionController extends Controller
{
    /**
     * 북클럽 멤버십 안내 및 카드 등록 폼
     */
    public function show()
    {
        $user = auth()->user();

        return view('subscriptions.checkout', [
            'intent' => $user->createSetupIntent(),
            'monthlyPrice' => 19900,
        ]);
    }

    /**
     * 북클럽 정기 구독 생성 처리
     */
    public function store(Request $request)
    {
        $user = $request->user();
        $paymentMethod = $request->payment_method;

        // Stripe 가격 플랜 ID (Stripe 대시보드에서 생성한 Product Price ID)
        $stripePriceId = config('services.stripe.book_club_price_id', 'price_1Nxxxxxxxxxxx');

        try {
            // 새 구독 생성 (신용카드 등록 + 즉시 첫 결제 진행)
            $user->newSubscription('book-club', $stripePriceId)
                ->create($paymentMethod);

            return redirect()->route('subscriptions.index')
                ->with('status', '지니샵 북클럽 정기 회원이 되신 것을 축하합니다! 📚');
        } catch (\Exception $e) {
            return back()->withErrors(['error' => '결제 승인 중 오류가 발생했습니다: ' . $e->getMessage()]);
        }
    }
}
```

---

### 4단계: 북클럽 회원 전용 혜택 페이지 및 상태 체크

독자가 북클럽 멤버십을 유지하고 있는지 검사하여 전자책 무제한 열람 권한을 부여합니다:

```php
// 컨트롤러 또는 미들웨어에서의 검증
if ($user->subscribed('book-club')) {
    // 북클럽 정회원 전용 혜택 제공 (신간 도서 무료 다운로드 등)
}

// 구독 취소 후 잔여 기간(유예 기간) 이용 중인지 확인
if ($user->subscription('book-club')->onGracePeriod()) {
    // "이번 결제 주기(2026-10-25)까지는 혜택이 유지됩니다" 배너 노출
}
```

블레이드 뷰(`resources/views/subscriptions/index.blade.php`):

```blade
<div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow">
    <h2 class="text-2xl font-bold mb-4">내 멤버십 관리</h2>

    @if(auth()->user()->subscribed('book-club'))
        <div class="p-4 bg-green-50 border border-green-200 rounded">
            <h3 class="text-lg font-bold text-green-800">✅ 지니샵 북클럽 정기 회원 이용 중</h3>
            <p class="text-green-700">다음 결제 예정일: {{ auth()->user()->subscription('book-club')->asStripeSubscription()->current_period_end ? date('Y-m-d', auth()->user()->subscription('book-club')->asStripeSubscription()->current_period_end) : '확인 중' }}</p>
        </div>

        @if(auth()->user()->subscription('book-club')->onGracePeriod())
            <div class="mt-4 p-3 bg-yellow-50 text-yellow-700 rounded">
                ⚠️ 멤버십 취소 신청이 완료되었습니다. 서비스 이용 종료일까지는 정상 이용 가능합니다.
            </div>
            <!-- 멤버십 다시 유지하기 -->
            <form action="{{ route('subscriptions.resume') }}" method="POST" class="mt-2">
                @csrf
                <button type="submit" class="text-blue-600 underline">멤버십 구독 다시 이어가기</button>
            </form>
        @else
            <!-- 멤버십 취소 버튼 -->
            <form action="{{ route('subscriptions.cancel') }}" method="POST" class="mt-4">
                @csrf
                <button type="submit" class="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700">
                    멤버십 구독 해지
                </button>
            </form>
        @endif
    @else
        <p class="text-gray-600 mb-4">현재 가입된 멤버십이 없습니다. 매월 엄선된 도서와 함께해 보세요!</p>
        <a href="{{ route('subscriptions.create') }}" class="px-5 py-2 bg-indigo-600 text-white rounded">
            북클럽 시작하기 (월 19,900원)
        </a>
    @endif
</div>
```

---

### 5단계: 구독 취소 및 재개(Resume) 처리

```php
// 구독 취소 (즉시 끊지 않고, 이번 결제 주기가 끝날 때까지 혜택 유지)
$user->subscription('book-club')->cancel();

// 즉시 강제 취소
$user->subscription('book-club')->cancelNow();

// 유예 기간(Grace Period) 중 마음이 바뀌어 취소 철회(재개)
$user->subscription('book-club')->resume();
```

---

### 6단계: 웹훅(Webhook) 처리 및 Cashier Paddle 비교

사용자의 카드가 만료되어 2회차 정기 결제가 실패했거나, Stripe 대시보드에서 직접 구독을 중지했을 때 우리 서버 DB와 동기화하려면 **Stripe 웹훅**을 수신해야 합니다.

Cashier는 웹훅 컨트롤러를 내장하고 있으므로 `routes/web.php`에 라우트만 등록해 주면 끝납니다:

```php
use Laravel\Cashier\Http\Controllers\WebhookController;

Route::post('/stripe/webhook', [WebhookController::class, 'handleWebhook']);
```

> ⚠️ **주의 (CSRF 예외 처리):**  
> 외부 Stripe 서버에서 전송하는 POST 요청이므로 `bootstrap/app.php`에서 CSRF 검증을 면제해야 합니다:
> ```php
> ->withMiddleware(function (Middleware $middleware) {
>     $middleware->validateCsrfTokens(except: [
>         'stripe/*',
>     ]);
> })
> ```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### Cashier Stripe vs Cashier Paddle 비교

| 비교 항목 | Laravel Cashier (Stripe) | Laravel Cashier (Paddle) |
| :--- | :--- | :--- |
| **판매자 지위** | 가맹점(Merchant of Record)이 우리 회사 | Paddle이 MoR(대행 판매자) 지위 가짐 |
| **해외 세금(VAT/GST)** | 국가별 부가세 신고/납부를 직접 해야 함 | Paddle이 전 세계 세금을 자동 징수/납부 |
| **커스터마이징** | UI/UX 및 카드 결제창을 100% 완전 커스텀 가능 | Paddle의 호스팅 결제 오버레이 팝업 활용 |
| **적합한 비즈니스** | 국내 중심의 정밀한 결제/구독 비즈니스 | 전 세계 고객을 대상으로 하는 디지털 콘텐츠/전자책 |

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **Stripe CLI를 이용한 로컬 웹훅 테스트:**  
   로컬 개발 환경(`localhost`)에서는 Stripe 웹훅을 직접 수신할 수 없습니다. 터미널에서 Stripe CLI를 설치하고 다음 명령어를 실행하면 로컬 포트로 웹훅을 터널링해 줍니다:
   ```bash
   stripe listen --forward-to localhost:8000/stripe/webhook
   ```
2. **단건 도서 구매 결제(`charge`):**  
   정기 구독이 아니라 도서 1권 단건 결제에도 Cashier를 쓸 수 있습니다:
   ```php
   // 25,000원 단건 결제
   $user->charge(25000, $paymentMethodId, [
       'description' => '도서 [라라벨 마스터 가이드] 1권 구매',
   ]);
   ```

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 사용자가 정기 구독을 취소했으나, 이번 결제 주기 마감일까지 잔여 이용 권한을 유지하고 있는 상태를 검사하는 Cashier 메소드는 무엇일까요?
   - 정답: `$user->subscription('플랜명')->onGracePeriod()`
2. **과제:** 지니샵 북클럽 회원이 플랜을 월간 결제(19,900원)에서 연간 결제(199,000원, 2개월 무료 할인)로 즉시 변경하는 `swap('price_annual')` 로직을 구현해 보세요!
{% endraw %}
