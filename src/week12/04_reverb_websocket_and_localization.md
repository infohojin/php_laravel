---
layout: docs
title: "12주차 04강: 라라벨 리버브(Reverb) 웹소켓 실시간 알림 & 다국어(Localization)"
---

{% raw %}
# 📖 12주차 04강: 라라벨 리버브(Reverb) 웹소켓 실시간 알림 & 다국어(Localization)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 라라벨 공식 1등 웹소켓 서버인 리버브(Reverb)를 설치하여 신규 도서 주문 시 관리자 화면에 새로고침 없이 실시간 토스트 알림을 띄우고, 글로벌 고객을 위한 다국어(한국어/영어/일본어) 언어팩과 통화 변환을 구축합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 책을 주문했을 때 관리자 페이지에서 F5 새로고침을 누르지 않아도 배달의민족처럼 '배달의민족 주문~!' 하고 실시간 알림 팝업이 뾰로롱 뜨게 할 수는 없을까? 외부 유료 서비스인 Pusher는 너무 비싸서 못 쓰겠어!"  
🐱 **지니**: "도로시, 바로 그런 웹소켓을 위해 라라벨 팀이 자체 제작한 **라라벨 리버브(Laravel Reverb)**가 있단다! Node.js나 복잡한 외부 서버 필요 없이, 라라벨 안에서 수만 개의 동시 웹소켓 연결을 초고속으로 소화해 내지!"  
🐶 **토토**: "멍멍! 게다가 해외 도서 바이어들을 위해서 한국어, 영어, 일본어 다국어 언어팩(`lang/`)과 통화(KRW/USD) 표기 변환 스위처도 오늘 함께 완성해 보자멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **라라벨 브로드캐스팅 및 Reverb 설치:** `php artisan install:broadcasting` 및 Reverb 서버 구동
2. **실시간 브로드캐스트 이벤트 작성:** `NewBookOrderPlaced` (`implements ShouldBroadcast`)
3. **프론트엔드 Laravel Echo 연동:** 웹소켓 수신 시 실시간 오디오 효과음 및 토스트 알림 렌더링
4. **다국어 지원(Localization) 구축:**
   - 언어팩 디렉토리(`lang/ko`, `lang/en`, `lang/ja`) 작성
   - 단수/복수형 표현(`trans_choice`) 및 파라미터 치환
   - 언어 변경 미들웨어(`SetLocale`) 및 통화 환율 변환 헬퍼

---

## 🛠️ 단계별 실습 절차

### 1단계: 라라벨 리버브(Reverb) 설치

라라벨 11에서는 단 한 줄의 명령어로 브로드캐스팅 및 Reverb 웹소켓 환경을 한 번에 세팅할 수 있습니다:

```bash
php artisan install:broadcasting
```

> 💡 **명령어 자동 실행 내용:**  
> - `composer require laravel/reverb` 설치  
> - `npm install --save-dev laravel-echo pusher-js` 프론트엔드 패키지 설치  
> - `.env`에 `BROADCAST_CONNECTION=reverb` 및 웹소켓 포트(8080) 구성  
> - `routes/channels.php` 생성  

`.env`의 Reverb 설정 확인:

```env
BROADCAST_CONNECTION=reverb

REVERB_APP_ID=jinyshop
REVERB_APP_KEY=jinyshopkey
REVERB_APP_SECRET=jinyshopsecret
REVERB_HOST="localhost"
REVERB_PORT=8080
REVERB_SCHEME=http

VITE_REVERB_APP_KEY="${REVERB_APP_KEY}"
VITE_REVERB_HOST="${REVERB_HOST}"
VITE_REVERB_PORT="${REVERB_PORT}"
VITE_REVERB_SCHEME="${REVERB_SCHEME}"
```

---

### 2단계: 실시간 브로드캐스트 이벤트 생성

신규 주문 발생 시 웹소켓으로 쏠 이벤트를 생성합니다:

```bash
php artisan make:event NewBookOrderPlaced
```

`app/Events/NewBookOrderPlaced.php`를 다음과 같이 작성합니다:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class NewBookOrderPlaced implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * 새 이벤트 인스턴스 생성
     */
    public function __construct(
        public Order $order
    ) {}

    /**
     * 이벤트를 브로드캐스트할 채널 정의 (관리자 공용 채널)
     */
    public function broadcastOn(): array
    {
        return [
            new Channel('admin-orders'), // 퍼블릭 채널 (보안 필요 시 PrivateChannel 사용)
        ];
    }

    /**
     * 프론트엔드로 전송할 브로드캐스트 이벤트 이름
     */
    public function broadcastAs(): string
    {
        return 'order.placed';
    }

    /**
     * 프론트엔드로 전달할 페이로드 데이터 커스터마이징
     */
    public function broadcastWith(): array
    {
        return [
            'order_id' => $this->order->id,
            'order_number' => $this->order->order_number,
            'customer_name' => $this->order->user ? $this->order->user->name : '비회원',
            'book_title' => $this->order->items->first()?->book->title ?? '도서',
            'total_amount' => number_format($this->order->total_amount),
            'placed_at' => now()->format('H:i:s'),
        ];
    }
}
```

---

### 3단계: 프론트엔드 Laravel Echo 수신 및 토스트 알림

`resources/js/echo.js`를 확인합니다:

```javascript
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

관리자 대시보드 블레이드 뷰(`resources/views/admin/dashboard.blade.php`)에 실시간 알림 리스너를 심어줍니다:

```blade
<!-- 실시간 토스트 알림 컨테이너 -->
<div id="toast-container" class="fixed bottom-5 right-5 space-y-3 z-50"></div>

<script type="module">
    window.Echo.channel('admin-orders')
        .listen('.order.placed', (e) => {
            console.log('실시간 신규 주문 수신:', e);

            // 1. 알림 토스트 UI 동적 생성
            const toast = document.createElement('div');
            toast.className = 'p-4 bg-indigo-600 text-white rounded-lg shadow-xl flex items-center space-x-3 transition transform duration-300';
            toast.innerHTML = `
                <span class="text-2xl">🔔</span>
                <div>
                    <h4 class="font-bold">신규 도서 주문 접수!</h4>
                    <p class="text-sm opacity-90">${e.customer_name}님이 [${e.book_title}] 외 도서를 주문하셨습니다. (${e.total_amount}원)</p>
                </div>
            `;
            document.getElementById('toast-container').appendChild(toast);

            // 5초 뒤 자동 소멸
            setTimeout(() => toast.remove(), 5000);
        });
</script>
```

---

### 4단계: Reverb 웹소켓 서버 실행 및 테스트

터미널을 열고 Reverb 서버를 가동합니다:

```bash
php artisan reverb:start --debug
```

그리고 Tinker를 열어 이벤트를 테스트 디스패치해 봅니다:

```bash
php artisan tinker
> App\Events\NewBookOrderPlaced::dispatch(App\Models\Order::first());
```

관리자 페이지 화면 우측 하단에 브라우저 새로고침 없이 즉시 보라색 토스트 알림 팝업이 솟아오릅니다!

---

### 5단계: 다국어(Localization) 언어팩 구축

라라벨 11에서 언어팩 파일을 생성합니다:

```bash
php artisan lang:publish
```

`lang/ko/messages.php` (한국어):
```php
<?php

return [
    'welcome' => '지니샵에 오신 것을 환영합니다!',
    'book_title' => '도서명',
    'author' => '저자',
    'cart_items' => '{0} 장바구니가 비어 있습니다.|{1} 도서 :count권이 담겨 있습니다.|[2,*] 도서 총 :count권이 담겨 있습니다.',
    'checkout' => '주문 결제하기',
];
```

`lang/en/messages.php` (영어):
```php
<?php

return [
    'welcome' => 'Welcome to JinyShop Bookstore!',
    'book_title' => 'Book Title',
    'author' => 'Author',
    'cart_items' => '{0} Your cart is empty.|{1} :count book in cart.|[2,*] :count books in cart.',
    'checkout' => 'Proceed to Checkout',
];
```

블레이드 템플릿에서의 사용:
```blade
<h1>{{ __('messages.welcome') }}</h1>
<p>{{ trans_choice('messages.cart_items', $cartCount, ['count' => $cartCount]) }}</p>
```

---

### 6단계: 언어 전환 라우트 및 미들웨어 (`SetLocale`)

사용자가 한국어/영어를 선택하면 세션에 저장하고 적용하는 미들웨어를 만듭니다:

```php
// routes/web.php
Route::get('/locale/{lang}', function (string $lang) {
    if (in_array($lang, ['ko', 'en', 'ja'])) {
        session(['locale' => $lang]);
    }
    return back();
})->name('locale.switch');
```

`app/Http/Middleware/SetLocale.php`:
```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;

class SetLocale
{
    public function handle(Request $request, Closure $next)
    {
        $locale = session('locale', config('app.locale', 'ko'));
        App::setLocale($locale);

        return $next($request);
    }
}
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. 프라이빗 채널(PrivateChannel)과 권한 인가 (Channel Authorization)

주문 내역처럼 고객 본인의 주문만 본인에게 브로드캐스팅해야 할 때는 `PrivateChannel`을 사용합니다:

```php
// Event
public function broadcastOn(): array
{
    return [new PrivateChannel('orders.' . $this->order->user_id)];
}

// routes/channels.php
Broadcast::channel('orders.{userId}', function ($user, $userId) {
    return (int) $user->id === (int) $userId;
});
```

### 2. 단수/복수형 번역 규칙 (`trans_choice`)

영어권에서는 책이 1권일 때 `1 book`, 2권 이상일 때 `2 books`로 문법이 바뀝니다. `trans_choice()`는 파이프(`|`) 구분자와 범위 표기법(`{0}`, `{1}`, `[2,*]`)을 통해 자연스러운 다국어 문법을 완벽히 지원합니다.

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **Reverb 포트 방화벽 개방:**  
   운영 서버에서 Reverb를 배포할 때는 웹소켓 포트(기본 `8080`)가 인바운드 방화벽에서 열려 있거나, Nginx 리버스 프록시(`location /app { proxy_pass http://127.0.0.1:8080; ... }`)를 통해 443(HTTPS/WSS) 포트로 우회 연결해 주어야 브라우저 혼합 콘텐츠(Mixed Content) 에러를 방지할 수 있습니다!
2. **이벤트 클래스의 Public 프로퍼티 노출 주의:**  
   `ShouldBroadcast`를 구현한 이벤트의 모든 `public` 프로퍼티는 프론트엔드 JSON으로 고스란히 전송됩니다. 비밀번호나 주민등록번호 같은 민감 정보가 있다면 반드시 `broadcastWith()` 메소드를 선언하여 노출할 필드만 엄격히 걸러내세요!

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 라라벨 이벤트를 웹소켓으로 자동 전송하도록 프레임워크에 지시하는 인터페이스 이름은 무엇일까요?
   - 정답: `ShouldBroadcast` (또는 지연 큐를 거치는 `ShouldBroadcastNow`)
2. **과제:** 책의 상세 페이지에서 다른 독자가 방금 이 책을 주문했을 때, 상세 페이지 화면 하단에 "[서울시 마포구 독자님이 방금 이 책을 주문하셨습니다]"라는 실시간 구매 알림을 브로드캐스팅해 보세요!
{% endraw %}
