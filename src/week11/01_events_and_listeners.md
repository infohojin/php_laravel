---
layout: docs
title: "11주차 01강: 이벤트(Events)와 리스너(Listeners)를 활용한 주문 완료 도메인 분리"
---

{% raw %}
# 📖 11주차 01강: 이벤트(Events)와 리스너(Listeners)를 활용한 주문 완료 도메인 분리

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 주문 완료 후 실행되는 다양한 후속 작업(재고 차감, 장바구니 비우기, 감사 로깅)을 `OrderPlaced` 이벤트와 독립 리스너들로 분리하여 비즈니스 로직의 결합도를 낮추고 유지보수성을 극대화합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 책을 결제하고 나면 주문 테이블에 저장하는 것 말고도 해야 할 일이 너무 많아! 서고에서 재고 수량도 깎아야 하고, 장바구니도 비워야 하고, 감사 로그도 남겨야 하고, 고객한테 메일도 보내야 해... `CheckoutController`의 `completeOrder()` 함수가 200줄이 넘어가고 있어!"  
🐱 **지니**: "도로시, 바로 그럴 때 객체지향의 핵심 원칙인 **관심사의 분리(Separation of Concerns)**와 라라벨의 **이벤트-리스너(Event-Listener)** 패턴을 쓰는 거란다! 주문 컨트롤러는 오직 주문 저장만 담당하고, '주문이 성공적으로 일어났습니다!'라는 소식을 세상에 방송(`Event::dispatch()`)하기만 하면 돼. 그러면 각 업무를 담당하는 리스너들이 각자 알아서 움직이지!"  
🐶 **토토**: "멍멍! 라라벨 11부터는 옛날처럼 `EventServiceProvider`에 일일이 리스너를 수동 등록할 필요 없이, 타입 힌트만 적어두면 라라벨이 알아서 척척 찾아주는 **자동 이벤트 발견(Event Discovery)**이 기본 지원된다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **`OrderPlaced` 이벤트 생성:** 결제 완료된 `Order` 모델 인스턴스를 담는 도메인 이벤트 정의
2. **다중 독립 리스너 구현:**
   - `DeductBookStock`: 주문한 도서들의 재고(`stock`) 수량 즉시 차감 및 품절 상태 전환
   - `ClearUserCart`: 주문 완료 후 장바구니 세션 및 DB 장바구니 비우기
   - `LogOrderAudit`: 보안 감사 로그 기록
3. **이벤트 디스패치(`dispatch`):** 결제 컨트롤러에서 우아하게 이벤트를 발생시키고 실행 흐름 검증
4. **라라벨 11 이벤트 디스커버리(Event Discovery) 및 구독자(Event Subscriber) 이해**

---

## 🛠️ 단계별 실습 절차

### 1단계: 주문 완료 이벤트(`OrderPlaced`) 생성

터미널에서 Artisan 명령어로 이벤트를 생성합니다.

```bash
php artisan make:event OrderPlaced
```

생성된 `app/Events/OrderPlaced.php` 파일을 열고, 주문 정보를 전달받도록 수정합니다.

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderPlaced
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * 새로운 이벤트 인스턴스 생성
     */
    public function __construct(
        public Order $order
    ) {
        // public 프로퍼티로 선언하여 리스너에서 $event->order로 바로 접근 가능합니다.
    }
}
```

> 💡 **SerializesModels 트레이트의 비밀:**  
> 이벤트를 큐(Queue)로 전달할 때 Eloquent 모델의 모든 데이터 대신 모델의 ID와 클래스명만 직렬화하고, 백그라운드 워커에서 읽을 때 DB에서 다시 신선하게 불러옵니다!

---

### 2단계: 도서 재고 차감 리스너(`DeductBookStock`) 작성

주문된 도서들의 재고를 안전하게 차감하는 리스너를 생성합니다.

```bash
php artisan make:listener DeductBookStock --event=OrderPlaced
```

`app/Listeners/DeductBookStock.php` 파일을 다음과 같이 작성합니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderPlaced;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class DeductBookStock
{
    /**
     * 이벤트 처리 (도서 재고 차감)
     */
    public function handle(OrderPlaced $event): void
    {
        $order = $event->order;

        Log::info("[이벤트] 주문 #{$order->order_number} 도서 재고 차감 시작");

        // 트랜잭션 내에서 비관적 잠금(Lock for update)과 함께 재고 차감
        DB::transaction(function () use ($order) {
            foreach ($order->items as $item) {
                $book = $item->book;

                if ($book->stock < $item->quantity) {
                    Log::warning("[재고부족 경고] 도서 '{$book->title}'(ID: {$book->id})의 재고({$book->stock}권)가 주문량({$item->quantity}권)보다 적습니다.");
                }

                // 음수 재고 방지를 고려한 재고 차감
                $book->decrement('stock', $item->quantity);

                // 품절 도서 처리 (재고가 0이 되면 상태 플래그 갱신)
                if ($book->fresh()->stock <= 0) {
                    $book->update(['is_sold_out' => true]);
                    Log::alert("[품절 알림] 도서 '{$book->title}'이 완판되어 품절 처리되었습니다!");
                }
            }
        });
    }
}
```

---

### 3단계: 장바구니 비우기 및 감사 로깅 리스너 작성

장바구니 비우기 리스너와 감사 로깅 리스너를 연달아 생성합니다.

```bash
php artisan make:listener ClearUserCart --event=OrderPlaced
php artisan make:listener LogOrderAudit --event=OrderPlaced
```

`app/Listeners/ClearUserCart.php`:
```php
<?php

namespace App\Listeners;

use App\Events\OrderPlaced;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Session;

class ClearUserCart
{
    public function handle(OrderPlaced $event): void
    {
        $order = $event->order;

        // 세션 기반 장바구니 초기화
        Session::forget('cart');

        // 회원 장바구니 DB 테이블이 있을 경우 함께 초기화
        if ($order->user_id) {
            $order->user->cartItems()->delete();
        }

        Log::info("[이벤트] 주문 #{$order->order_number}에 대한 장바구니를 성공적으로 비웠습니다.");
    }
}
```

`app/Listeners/LogOrderAudit.php`:
```php
<?php

namespace App\Listeners;

use App\Events\OrderPlaced;
use Illuminate\Support\Facades\Log;

class LogOrderAudit
{
    public function handle(OrderPlaced $event): void
    {
        $order = $event->order;

        Log::channel('daily')->info('ORDER_PLACED_AUDIT', [
            'order_id' => $order->id,
            'order_number' => $order->order_number,
            'user_id' => $order->user_id,
            'total_amount' => $order->total_amount,
            'placed_at' => now()->toIso8601String(),
            'ip' => request()->ip(),
        ]);
    }
}
```

---

### 4단계: 라라벨 11 이벤트 디스커버리(Event Discovery) 확인

라라벨 11에서는 `App/Listeners` 디렉토리 내의 리스너 메소드 `handle(OrderPlaced $event)`의 **타입 힌트**를 분석하여 자동으로 이벤트를 연결합니다!

아래 명령어로 이벤트와 리스너가 제대로 자동 연결되었는지 즉시 확인합니다:

```bash
php artisan event:list
```

출력 예시:
```text
App\Events\OrderPlaced
  ⇂ App\Listeners\DeductBookStock
  ⇂ App\Listeners\ClearUserCart
  ⇂ App\Listeners\LogOrderAudit
```

> 🐶 **토토의 팁!**  
> "만약 특정 리스너를 수동으로 바인딩하거나 실행 순서를 제어하고 싶다면 `bootstrap/app.php` 또는 `AppServiceProvider::boot()`에서 `Event::listen(OrderPlaced::class, DeductBookStock::class)`를 쓸 수 있다멍!"

---

### 5단계: 주문 완료 컨트롤러에서 이벤트 디스패치(`OrderPlaced::dispatch`)

`app/Http/Controllers/CheckoutController.php`의 주문 완료 로직에 이벤트를 연동합니다.

```php
<?php

namespace App\Http\Controllers;

use App\Events\OrderPlaced;
use App\Models\Order;
use App\Models\OrderItem;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

class CheckoutController extends Controller
{
    public function processOrder(Request $request)
    {
        // 1. 주문 데이터 DB 저장
        $order = DB::transaction(function () use ($request) {
            $order = Order::create([
                'user_id' => auth()->id(),
                'order_number' => 'ORD-' . strtoupper(Str::random(10)),
                'status' => 'paid',
                'total_amount' => 45000,
                'shipping_address' => '서울시 강남구 테헤란로 123',
            ]);

            // 주문 상세 항목 생성 (예: 도서 ID 1번 2권)
            OrderItem::create([
                'order_id' => $order->id,
                'book_id' => 1,
                'quantity' => 2,
                'unit_price' => 22500,
            ]);

            return $order;
        });

        // 2. 주문 완료 이벤트 발행! (단 한 줄로 후속 도메인 작업 트리거)
        OrderPlaced::dispatch($order);

        // 3. 0.1초 만에 깔끔하게 응답 반환
        return redirect()->route('orders.show', $order)
            ->with('status', '도서 주문이 성공적으로 완료되었습니다!');
    }
}
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. 이벤트 디스패치 방법 3가지

라라벨 공식 문서에 따르면 이벤트를 호출하는 방법은 세 가지가 있습니다:

```php
// 1. Dispatchable 트레이트가 제공하는 정적 메소드 (가장 권장)
OrderPlaced::dispatch($order);

// 2. 조건부 디스패치 (특정 조건이 참일 때만 발동)
OrderPlaced::dispatchIf($order->total_amount > 100000, $order);
OrderPlaced::dispatchUnless($order->is_guest, $order);

// 3. Event 파사드 직접 호출
use Illuminate\Support\Facades\Event;
Event::dispatch(new OrderPlaced($order));
```

### 2. 이벤트 전파 중단 (Stopping Event Propagation)

만약 어떤 리스너에서 치명적인 문제(예: 블랙리스트 사기 주문 감지)가 발생하여 다음 리스너들이 실행되지 않도록 막아야 한다면, `handle()` 메소드에서 `false`를 반환하면 됩니다:

```php
public function handle(OrderPlaced $event): bool
{
    if ($event->order->isFraudulent()) {
        Log::emergency("사기 주문 감지로 후속 이벤트 실행을 전면 중단합니다!");
        return false; // 다음 순번의 리스너 실행이 즉각 취소됩니다!
    }

    return true;
}
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **`php artisan event:cache` 프로덕션 최적화:**  
   운영(배포) 서버에서는 매 요청마다 리스너 클래스를 리플렉션으로 탐색하지 않도록 `php artisan event:cache`를 실행하여 부팅 속도를 극대화해야 합니다. 코드를 수정했을 때는 반드시 `php artisan event:clear`를 해주는 것 잊지 마세요!
2. **트랜잭션 커밋 후 이벤트 발송(`afterCommit`):**  
   DB 트랜잭션 안에서 이벤트를 바로 디스패치하면, 비동기 리스너가 실행되는 순간 아직 DB에 주문 레코드가 커밋되지 않아 `ModelNotFoundException`이 터질 수 있습니다! 이럴 때는 `OrderPlaced` 이벤트에 `use Dispatchable;`와 함께 `$order->save();` 후 트랜잭션 바깥에서 디스패치하거나 이벤트 클래스에 `public bool $afterCommit = true;`를 명시하세요.

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 라라벨 11에서 리스너가 이벤트를 자동으로 감지할 수 있도록 하는 핵심 기준은 무엇일까요?
   - 정답: 리스너 클래스의 `handle()` 메소드 첫 번째 파라미터에 지정된 이벤트 클래스 타입 힌트(`OrderPlaced $event`).
2. **과제:** `OrderPlaced` 이벤트가 발생했을 때 VIP 회원(누적 구매액 50만원 이상)인 경우 적립금을 5% 추가 지급하는 `AwardVipPoints` 리스너를 제작하고 `php artisan event:list`로 등록을 확인해 보세요!
{% endraw %}
