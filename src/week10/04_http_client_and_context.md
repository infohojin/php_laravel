---
layout: docs
title: "04강: HTTP 클라이언트 PG사 연동 & Context 트레이스 헬퍼"
---

{% raw %}
# 04강: HTTP 클라이언트 PG사 연동 & Context 트레이스 헬퍼

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 라라벨 HTTP 클라이언트(`Http::retry()`), PG사 REST 통신, `Http::fake()` 가상 모킹, Context 요청 트레이스 추적 및 전역 헬퍼 함수  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [HTTP 클라이언트 (HTTP Client)](../docs/05_digging_deeper/http-client_ko.md), [컨텍스트 (Context)](../docs/05_digging_deeper/context_ko.md), [헬퍼 (Helpers)](../docs/05_digging_deeper/helpers_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 실제 토스페이먼츠나 카카오페이 서버로 결제 승인을 요청할 때 네트워크가 잠깐 끊기거나 PG사 서버가 1초 동안 응답이 없으면 우리 서점 결제가 다 튕겨 나가잖아요! 외부 통신을 안전하게 재시도(Retry)하고 타임아웃을 거는 방법은 없나요? 그리고 복잡한 주문 흐름 속에서 이 결제가 어떤 독자의 어떤 장바구니에서 시작되었는지 로그를 추적하려면 어떻게 해야 해요?"

🐱 **지니**: "도로시, 바로 그럴 때 사용하는 최고의 도구가 바로 **라라벨 HTTP 클라이언트**란다! Guzzle을 바탕으로 감싸진 플루언트 API 덕분에 `Http::timeout(5)->retry(3, 100)` 한 줄이면 네트워크 불안정 시 100ms 간격으로 3번까지 자동 재시도해 주지. 그리고 라라벨 11~13에 도입된 **Context** 기능을 쓰면 주문 고유 `trace_id`를 모든 로그와 외부 HTTP 요청 헤더에 자동으로 실어 보낼 수 있단다!"

🐶 **토토**: "멍멍! 테스트 코드에서는 `Http::fake()`를 쓰면 실제 인터넷 연결 없이도 가짜 PG사 승인 JSON을 즉석에서 돌려받을 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨 `Http` 파사드를 이용해 안전한 타임아웃과 자동 재시도(Retry)가 적용된 외부 통신을 구현합니다.
2. 테스트 환경에서 실제 API 호출을 가로채는 `Http::fake()` 모킹을 익힙니다.
3. 요청 수명주기 동안 주문 번호와 사용자 정보를 추적하는 `Context` 및 전역 헬퍼를 작성합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `TossPaymentGateway`에 실제 HTTP 클라이언트 통신 탑재

`app/Services/Payment/TossPaymentGateway.php`의 `charge` 메서드를 라라벨 HTTP 클라이언트로 구현합니다:

```php
namespace App\Services\Payment;

use App\Contracts\PaymentGatewayContract;
use App\Contracts\PaymentResult;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class TossPaymentGateway implements PaymentGatewayContract
{
    public function __construct(
        protected string $apiKey,
        protected string $secretKey,
    ) {}

    public function charge(int $amount, array $orderData): PaymentResult
    {
        try {
            // 🚀 5초 타임아웃, 네트워크 실패 시 100ms 간격으로 최대 3회 자동 재시도!
            $response = Http::withBasicAuth($this->secretKey, '')
                ->timeout(5)
                ->retry(3, 100)
                ->withHeaders([
                    'X-JinyShop-Trace-Id' => \Illuminate\Support\Facades\Context::get('trace_id'),
                ])
                ->post('https://api.tosspayments.com/v1/payments/confirm', [
                    'paymentKey' => $orderData['payment_key'] ?? 'test_pk',
                    'orderId' => $orderData['order_id'] ?? 'ORD-' . time(),
                    'amount' => $amount,
                ]);

            if ($response->successful()) {
                $data = $response->json();
                return new PaymentResult(
                    success: true,
                    transactionId: $data['paymentKey'] ?? 'TX-'.time(),
                    amount: $amount
                );
            }

            // PG사에서 거절된 경우
            Log::warning('PG 결제 승인 거절: ' . $response->body());
            return new PaymentResult(
                success: false,
                transactionId: '',
                amount: $amount,
                errorMessage: $response->json('message') ?? '결제 승인이 거절되었습니다.'
            );
        } catch (\Throwable $e) {
            Log::error('PG사 네트워크 통신 장애: ' . $e->getMessage());
            return new PaymentResult(
                success: false,
                transactionId: '',
                amount: $amount,
                errorMessage: '결제 대행사 통신 연결 실패'
            );
        }
    }

    public function refund(string $transactionId, int $amount): bool
    {
        return true;
    }
}
```

---

### [Step 2] `Http::fake()`로 가짜 PG사 승인 테스트 실습

실제 토스 계정이나 돈이 없어도 `Http::fake()`를 쓰면 단위 테스트나 로컬 시뮬레이션을 완벽히 수행할 수 있습니다:

```bash
php artisan tinker
```

```php
use Illuminate\Support\Facades\Http;

// 1. 토스 API URL로 가는 요청을 가상 승인 응답으로 가로채기!
Http::fake([
    'https://api.tosspayments.com/*' => Http::response([
        'paymentKey' => 'REAL-LIKE-TOSS-KEY-999',
        'status' => 'DONE',
        'totalAmount' => 35000,
    ], 200),
]);

// 2. 게이트웨이 실행
$gateway = new App\Services\Payment\TossPaymentGateway('key', 'secret');
$result = $gateway->charge(35000, ['order_id' => 'ORD-123']);

echo "가상 통신 성공 여부: " . ($result->success ? '성공!' : '실패') . PHP_EOL;
echo "거래 키: " . $result->transactionId . PHP_EOL;
```

> **출력:** `가상 통신 성공 여부: 성공! / 거래 키: REAL-LIKE-TOSS-KEY-999`

---

### [Step 3] `Context` 파사드로 주문 추적 ID 전파

`Context`를 사용하면 요청이 시작될 때 생성된 고유 `trace_id`가 모든 로그와 쿼리, 외부 API 헤더에 자동으로 각인됩니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

// 미들웨어나 요청 시작점에서 Context 부여
Context::add('trace_id', Str::uuid()->toString());
Context::add('user_id', auth()->id() ?? 'guest');

// 이후 Log::info()를 호출하면 Context 데이터가 로그에 자동으로 함께 기록됩니다!
Log::info('도서 결제 요청 시작');
```

---

### [Step 4] 전역 헬퍼 함수 작성 (`app/helpers.php`)

서점 전역에서 간편하게 금액을 원화로 표기하는 헬퍼 함수를 만듭니다:

`app/helpers.php`:
```php
<?php

if (! function_exists('currency_krw')) {
    function currency_krw(int|float $amount): string
    {
        return number_format($amount) . '원';
    }
}
```

`composer.json`의 `autoload` 섹션에 파일 등록:
```json
"autoload": {
    "files": [
        "app/helpers.php"
    ]
}
```
터미널에서 `composer dump-autoload`를 실행하면 모든 Blade 템플릿과 코드에서 `currency_krw(35000)`을 즉시 사용할 수 있습니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `Http::retry()`의 백오프(Exponential Backoff) 전략
- `Http::retry(3, 100)`는 단순히 세 번 연속 찌르는 것이 아니라, 순간적인 네트워크 혼잡이 풀릴 수 있도록 100ms, 200ms, 400ms 처럼 점진적으로 대기 시간을 늘리는 **지수 백오프** 전략을 지원합니다.
- 외부 PG사 서버의 일시적인 순단 장애 시 주문 성공률을 99.9%로 끌어올리는 비결입니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **테스트할 때 실제 외부 사이트로 진짜 요청이 나가버렸어요!**  
>    테스트 시작 전에 `Http::preventStrayRequests()`를 선언해 두면, `Http::fake()`로 등록되지 않은 외부 인터넷 요청이 나갈 때 즉시 에러를 터뜨려 안전을 지켜준다멍!

---

## 💡 6. 4강 자가진단 과제

1. `Http::fake()`를 사용해 400 Bad Request ("잔액 부족") 에러 응답을 시뮬레이션하고, 게이트웨이가 `errorMessage`를 올바르게 반환하는지 테스트하세요.
2. 뷰 화면에서 `currency_krw(125000)` 헬퍼 함수를 호출하여 `125,000원`으로 예쁘게 렌더링되는지 확인하세요.
{% endraw %}
