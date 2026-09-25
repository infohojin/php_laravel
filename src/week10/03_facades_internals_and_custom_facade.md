---
layout: docs
title: "03강: 파사드(Facade)의 가면을 벗기다 — `Payment` 커스텀 파사드 제작"
---

{% raw %}
# 03강: 파사드(Facade)의 가면을 벗기다 — `Payment` 커스텀 파사드 제작

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 정적 문법 뒤에 숨겨진 동적 컨테이너 인스턴스, `Facade`와 `__callStatic()`, 서점 결제 전용 `Payment` 커스텀 파사드  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [파사드 (Facades)](../docs/03_architecture_concepts/facades_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 라라벨 코드를 볼 때마다 항상 풀리지 않던 수수께끼가 있어요! `Route::get()`, `Cache::put()`, `Log::info()` 처럼 클래스를 `new`로 생성하지도 않고 정적 메서드(`::`)로 부르는데, 뒤에서는 어떻게 데이터베이스 연결이나 캐시 객체가 정상적으로 돌아가는 거예요? 순수 정적(Static) 클래스는 테스트하기도 힘들다고 들었는데 라라벨은 어떻게 파사드를 테스트하죠?"

🐱 **지니**: "후후, 도로시가 드디어 라라벨의 가장 신비로운 마법의 가면을 벗겨낼 준비가 되었구나! **파사드(Facade, 건축물의 정면/가면)**는 진짜 정적 클래스가 아니란다! PHP의 `__callStatic()` 마술을 이용해, 정적 호출이 들어오는 순간 가면 뒤에 숨어있는 **진짜 서비스 컨테이너 인스턴스**를 꺼내어 대신 일하게 만드는 프록시(Proxy) 통로란다! 덕분에 개발자는 간결한 문법을 누리면서도 테스트할 때는 `Payment::shouldReceive()`로 완벽한 가짜 객체 모킹을 할 수 있지!"

🐶 **토토**: "멍멍! 우리 지니샵에도 `Payment::charge()` 한 줄로 결제를 실행하는 멋진 커스텀 파사드를 만들어보자멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨 파사드의 내부 동작 메커니즘(`__callStatic` $\rightarrow$ `getFacadeAccessor` $\rightarrow$ 컨테이너 해결)을 완전히 파헤칩니다.
2. 서점 결제 모듈을 정적 문법으로 편리하게 호출할 수 있는 `App\Facades\Payment` 커스텀 파사드를 만듭니다.
3. 파사드의 강력한 테스트 모킹(`Payment::shouldReceive()`)을 실습합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 파사드 동작 원리 4단계 다이어그램

```text
[개발자 코드] Payment::charge(35000, $orderData)
                     │
                     ▼
[1. PHP 매직 메서드]  Facade::__callStatic('charge', [35000, ...])
                     │
                     ▼
[2. 접근자 확인]      Payment::getFacadeAccessor() ➔ 'App\Contracts\PaymentGatewayContract'
                     │
                     ▼
[3. 컨테이너 해결]    app()->make('App\Contracts\PaymentGatewayContract') ➔ MockPaymentGateway 인스턴스 획득!
                     │
                     ▼
[4. 동적 메서드 실행]  $mockPaymentGateway->charge(35000, $orderData) ➔ 결과 반환!
```

---

### [Step 2] `Payment` 커스텀 파사드 작성

`app/Facades/Payment.php` 파일을 생성합니다:

```php
namespace App\Facades;

use App\Contracts\PaymentGatewayContract;
use Illuminate\Support\Facades\Facade;

/**
 * @method static \App\Contracts\PaymentResult charge(int $amount, array $orderData)
 * @method static bool refund(string $transactionId, int $amount)
 *
 * @see \App\Contracts\PaymentGatewayContract
 */
class Payment extends Facade
{
    /**
     * 서비스 컨테이너에서 찾아올 바인딩 키 또는 인터페이스 반환
     */
    protected static function getFacadeAccessor(): string
    {
        return PaymentGatewayContract::class;
    }
}
```

> **지니의 감탄:**  
> 단 10줄의 코드만으로 완벽한 파사드가 완성되었단다! 상단의 PHPDoc 주석을 달아두면 VS Code나 PhpStorm 에디터에서 자동완성까지 완벽하게 지원하지!

---

### [Step 3] 컨트롤러에서 우아한 한 줄 결제 호출

컨트롤러에서 생성자 주입이나 번거로운 코드 없이 파사드로 깔끔하게 결제를 집행합니다:

```php
// app/Http/Controllers/CheckoutController.php
use App\Facades\Payment; // 우리가 만든 커스텀 파사드!
use App\Services\CartService;
use Illuminate\Http\Request;

class CheckoutController extends Controller
{
    public function process(Request $request, CartService $cart)
    {
        // 🚀 파사드를 통한 극도로 간결한 결제 실행!
        $result = Payment::charge($cart->totalPrice(), [
            'order_name' => '지니샵 도서 주문',
        ]);

        if (! $result->success) {
            return back()->with('error', $result->errorMessage);
        }

        $cart->clear();

        return redirect()->route('home')->with('success', '주문 완료!');
    }
}
```

---

### [Step 4] Tinker에서 파사드 테스트

```bash
php artisan tinker
```

```php
use App\Facades\Payment;

$result = Payment::charge(45000, ['order_id' => 99]);

echo "결제 결과: " . ($result->success ? '성공' : '실패') . PHP_EOL;
echo "거래 번호: " . $result->transactionId . PHP_EOL;
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 파사드가 단위 테스트에서 사랑받는 이유
순수 정적 클래스는 테스트 시 메서드를 가로채거나 가짜 값으로 모킹(Mocking)하기가 극도로 어렵습니다.  
하지만 라라벨 파사드는 뒤에 실제 객체가 숨어있기 때문에, 테스트 코드에서 다음과 같이 손쉽게 가짜 결제를 흉내 낼 수 있습니다:

```php
// 테스트 코드에서 실제 결제 모듈 실행을 가짜로 가로챔!
Payment::shouldReceive('charge')
    ->once()
    ->with(35000, Mockery::any())
    ->andReturn(new PaymentResult(true, 'TEST-TX-1234', 35000));
```

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **실시간 파사드(Real-time Facades)란 무엇인가요?**  
>    파사드 파일을 따로 만들지 않아도, 네임스페이스 앞에 `Facades\`만 붙이면 라라벨이 런타임에 파사드를 즉석에서 가상 생성해 준다멍! (예: `Facades\App\Services\CartService::totalPrice()`)

---

## 💡 6. 3강 자가진단 과제

1. `Payment` 파사드에 `refund()` 메서드를 호출하는 테스트 코드를 작성해 보세요.
2. Tinker에서 `Payment::getFacadeRoot()`를 호출하여 파사드 뒤에 숨어있는 실제 구현체 객체가 무엇인지 눈으로 확인하세요.
{% endraw %}
