---
layout: docs
title: "01강: IoC 서비스 컨테이너 & 결제 게이트웨이 인터페이스(`Contract`) 추상화"
---

{% raw %}
# 01강: IoC 서비스 컨테이너 & 결제 게이트웨이 인터페이스(`Contract`) 추상화

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 제어의 역전(IoC), 의존성 주입(DI), `PaymentGatewayContract` 인터페이스 추상화, 결제 모듈(토스/카카오/Mock) 교체 설계  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [서비스 컨테이너 (Service Container)](../docs/03_architecture_concepts/container_ko.md), [컨트랙트 (Contracts)](../docs/05_digging_deeper/contracts_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리 서점에서 책 결제를 붙일 때, 컨트롤러에서 직접 `new TossPaymentsAPI()`를 생성해서 결제 코드를 짜면 안 되나요? 왜 굳이 인터페이스를 만들고 복잡하게 의존성을 주입해야 해요?"

🐱 **지니**: "후후, 도로시! 만약 결제 수수료가 더 저렴한 다른 PG사(예: 카카오페이, 스트라이프)로 변경하거나, 로컬에서 실제 내 신용카드를 긁지 않고 가짜 결제 테스트를 하고 싶다면 어떻게 할래? 컨트롤러에 특정 회사의 코드가 하드코딩되어 있다면 수백 줄을 다 뜯어고쳐야 한단다! 하지만 **`PaymentGatewayContract` 인터페이스**를 세워두면, 컨트롤러는 인터페이스만 바라보고, 진짜 구현체는 라라벨의 심장인 **서비스 컨테이너(Service Container)**가 마법처럼 쏙 갈아 끼워준단다!"

🐶 **토토**: "멍멍! 이것이 바로 객체지향 5대 원칙(SOLID) 중 의존 역전 원칙(DIP)이다멍! 테스트할 때는 `MockPaymentGateway`를 꽂아서 0원 결제 테스트를 맘껏 할 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨의 핵심 심장부인 IoC(Inversion of Control) 서비스 컨테이너의 개념을 이해합니다.
2. PG사 교체에 유연하게 대응하는 `PaymentGatewayContract` 인터페이스를 설계합니다.
3. 실제 결제용 `TossPaymentGateway`와 테스트용 `MockPaymentGateway`를 구현합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 결제 결과 DTO 및 인터페이스 정의

`app/Contracts/PaymentGatewayContract.php` 파일을 생성합니다:

```php
namespace App\Contracts;

/**
 * 결제 결과 데이터 전송 객체
 */
class PaymentResult
{
    public function __construct(
        public bool $success,
        public string $transactionId,
        public int $amount,
        public ?string $errorMessage = null,
    ) {}
}

/**
 * 모든 결제 모듈이 반드시 지켜야 할 계약(Contract)
 */
interface PaymentGatewayContract
{
    /**
     * 결제 승인 요청
     */
    public function charge(int $amount, array $orderData): PaymentResult;

    /**
     * 결제 취소 및 환불
     */
    public function refund(string $transactionId, int $amount): bool;
}
```

---

### [Step 2] 두 가지 구현체 작성 (실제 PG사 vs 로컬 테스트용 Mock)

#### 1) 로컬 개발/테스트용 `MockPaymentGateway`
실제 돈이 빠져나가지 않고 테스트를 100% 성공시키는 가짜 결제 모듈입니다:

```php
// app/Services/Payment/MockPaymentGateway.php
namespace App\Services\Payment;

use App\Contracts\PaymentGatewayContract;
use App\Contracts\PaymentResult;
use Illuminate\Support\Str;

class MockPaymentGateway implements PaymentGatewayContract
{
    public function charge(int $amount, array $orderData): PaymentResult
    {
        // 100% 성공 시뮬레이션
        return new PaymentResult(
            success: true,
            transactionId: 'MOCK-TX-' . Str::upper(Str::random(12)),
            amount: $amount
        );
    }

    public function refund(string $transactionId, int $amount): bool
    {
        return true;
    }
}
```

#### 2) 실제 상용 통신용 `TossPaymentGateway`
```php
// app/Services/Payment/TossPaymentGateway.php
namespace App\Services\Payment;

use App\Contracts\PaymentGatewayContract;
use App\Contracts\PaymentResult;

class TossPaymentGateway implements PaymentGatewayContract
{
    public function __construct(
        protected string $apiKey,
        protected string $secretKey,
    ) {}

    public function charge(int $amount, array $orderData): PaymentResult
    {
        // (4강에서 라라벨 HTTP 클라이언트로 실제 PG사 API 통신을 구현합니다)
        return new PaymentResult(
            success: true,
            transactionId: 'TOSS-TX-' . time(),
            amount: $amount
        );
    }

    public function refund(string $transactionId, int $amount): bool
    {
        return true;
    }
}
```

---

### [Step 3] 컨트롤러에서 인터페이스 의존성 자동 주입(Auto-wiring)

컨트롤러는 구체적인 PG사 이름을 전혀 몰라도 인터페이스 타입 힌트만으로 결제를 집행할 수 있습니다:

```php
// app/Http/Controllers/CheckoutController.php
namespace App\Http\Controllers;

use App\Contracts\PaymentGatewayContract;
use App\Services\CartService;
use Illuminate\Http\Request;

class CheckoutController extends Controller
{
    /**
     * 라라벨 서비스 컨테이너가 PaymentGatewayContract 구현체를 자동으로 주입!
     */
    public function process(
        Request $request,
        CartService $cart,
        PaymentGatewayContract $paymentGateway // 🚀 자동 의존성 주입!
    ) {
        $totalPrice = $cart->totalPrice();

        // 결제 집행!
        $result = $paymentGateway->charge($totalPrice, [
            'order_name' => '지니샵 도서 ' . $cart->totalCount() . '권 주문',
            'customer_email' => auth()->user()?->email,
        ]);

        if (! $result->success) {
            return back()->with('error', '결제 실패: ' . $result->errorMessage);
        }

        return redirect()->route('orders.success', ['tx' => $result->transactionId])
            ->with('success', '도서 주문 및 결제가 안전하게 완료되었습니다!');
    }
}
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 리플렉션(Reflection) 기반 Auto-wiring
- 컨트롤러 생성자나 메서드에 `PaymentGatewayContract $paymentGateway`를 선언하면, 라라벨 컨테이너는 PHP의 리플렉션 API를 이용해 파라미터 타입을 분석합니다.
- 다음 2강에서 배울 **서비스 프로바이더(Service Provider)**에 바인딩된 구현체를 찾아 인스턴스를 자동으로 생성하여 넘겨줍니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`Target [App\Contracts\PaymentGatewayContract] is not instantiable` 에러가 나요!**  
>    인터페이스는 `new`로 직접 객체를 만들 수 없기 때문이다멍! 라라벨에게 "이 인터페이스를 찾으면 이 클래스를 만들어줘!" 하고 서비스 프로바이더에서 짝을 지어줘야 한다멍! 바로 2강으로 넘어가자멍!

---

## 💡 6. 1강 자가진단 과제

1. 왜 컨트롤러에서 `new TossPaymentGateway()`를 직접 생성하지 않고 인터페이스를 거치는지 장점 2가지를 설명해 보세요.
2. `PaymentGatewayContract`에 결제 승인 전 영수증 조회를 위한 `verify()` 메서드를 추가로 설계해 보세요.
{% endraw %}
