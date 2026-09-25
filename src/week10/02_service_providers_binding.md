---
layout: docs
title: "02강: 서비스 프로바이더(Service Provider) & 결제 모듈 싱글톤 바인딩"
---

{% raw %}
# 02강: 서비스 프로바이더(Service Provider) & 결제 모듈 싱글톤 바인딩

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 라라벨 부트스트래핑의 핵심 `PaymentServiceProvider`, `register()` vs `boot()`, 환경별(운영 vs 로컬 테스트) 동적 바인딩  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [서비스 프로바이더 (Service Providers)](../docs/03_architecture_concepts/providers_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 지난 1강에서 인터페이스는 `new`로 직접 만들 수 없어서 에러가 난다고 했잖아요. 그럼 라라벨한테 '누군가 `PaymentGatewayContract`를 요구하면, 테스트 환경일 땐 `MockPaymentGateway`를 주고 운영 환경일 땐 진짜 `TossPaymentGateway`를 줘!' 라고 알려주는 매칭 장부는 어디에 적어야 해요?"

🐱 **지니**: "도로시, 바로 그 조립 설명서가 라라벨 부트스트래핑의 심장인 **서비스 프로바이더(Service Provider)**란다! `register()` 메서드 안에 단 몇 줄의 바인딩 코드만 적어두면, 컨테이너가 서점 환경 설정(`.env`)을 읽어서 알맞은 결제 객체를 싱글톤(Singleton)으로 만들어 전달해 주지!"

🐶 **토토**: "멍멍! `register()`에서는 순수 등록만 해야 하고, 다른 서비스와 통신하는 초기화 작업은 반드시 `boot()`에서 해야 안전하다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 결제 모듈 등록을 전담할 커스텀 `PaymentServiceProvider`를 생성합니다.
2. `.env`의 `PAYMENT_DRIVER` 설정값에 따라 Mock과 실제 PG사를 스위칭하는 조건부 바인딩을 작성합니다.
3. 라라벨 13의 `bootstrap/providers.php`에 프로바이더를 등록하고 Tinker로 해결(Resolve)을 검증합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `PaymentServiceProvider` 아티산 생성

터미널에서 프로바이더 클래스를 생성합니다:

```bash
php artisan make:provider PaymentServiceProvider
```

---

### [Step 2] 동적 바인딩 로직 작성 (`register()`)

`app/Providers/PaymentServiceProvider.php` 파일을 작성합니다:

```php
namespace App\Providers;

use App\Contracts\PaymentGatewayContract;
use App\Services\Payment\MockPaymentGateway;
use App\Services\Payment\TossPaymentGateway;
use Illuminate\Support\ServiceProvider;

class PaymentServiceProvider extends ServiceProvider
{
    /**
     * 컨테이너에 서비스 바인딩 등록 (오직 바인딩만 수행!)
     */
    public function register(): void
    {
        // 싱글톤으로 바인딩: 요청 주기 내내 단 하나의 객체만 재사용!
        $this->app->singleton(PaymentGatewayContract::class, function ($app) {
            $driver = config('services.payment.driver', 'mock');

            return match ($driver) {
                'toss' => new TossPaymentGateway(
                    apiKey: config('services.toss.api_key', 'test_key'),
                    secretKey: config('services.toss.secret_key', 'test_secret')
                ),
                default => new MockPaymentGateway(), // 로컬 및 테스트 환경 기본값
            };
        });
    }

    /**
     * 모든 서비스가 등록된 후 초기화 작업 수행
     */
    public function boot(): void
    {
        // 필요시 결제 이벤트 리스너나 커스텀 유효성 검사 등록
    }
}
```

---

### [Step 3] `bootstrap/providers.php`에 프로바이더 등록

라라벨 13에서는 `bootstrap/providers.php` 파일에 프로바이더 목록이 배열로 관리됩니다:

```php
// bootstrap/providers.php
return [
    App\Providers\AppServiceProvider::class,
    App\Providers\PaymentServiceProvider::class, // 🚀 결제 프로바이더 등록!
];
```

---

### [Step 4] Tinker에서 인터페이스 자동 해결(Resolution) 테스트

이제 실제로 컨테이너가 인터페이스를 요구받았을 때 알맞은 객체를 찍어내는지 확인합니다:

```bash
php artisan tinker
```

```php
// 컨테이너에게 인터페이스 인스턴스 요구
$gateway = app(App\Contracts\PaymentGatewayContract::class);

echo "해결된 클래스 이름: " . get_class($gateway) . PHP_EOL;
// 출력: 해결된 클래스 이름: App\Services\Payment\MockPaymentGateway

// 결제 실행 테스트
$result = $gateway->charge(35000, ['order_id' => 1]);
echo "결제 성공 여부: " . ($result->success ? '성공' : '실패') . PHP_EOL;
echo "거래 번호: " . $result->transactionId . PHP_EOL;
```

> **지니의 감탄:**  
> 컨트롤러든 콘솔 명령어든 어디서든 `app(PaymentGatewayContract::class)`를 부르면 즉시 완벽히 조립된 결제 인스턴스가 튀어나온단다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `bind()` vs `singleton()`
- `$this->app->bind()`: 컨테이너에서 객체를 꺼낼 때마다 매번 `new`로 새로운 인스턴스를 생성합니다.
- `$this->app->singleton()`: 최초 1회만 객체를 생성하고 메모리에 캐싱해 둡니다. 이후 동일한 요청 주기 안에서는 언제나 똑같은 인스턴스를 공유하므로 메모리와 네트워크 연결을 대폭 절약합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`register()` 안에서 다른 프로바이더의 모델을 조회하면 왜 안 되나요?**  
>    라라벨이 시작될 때 모든 프로바이더의 `register()`가 먼저 다 끝난 뒤에 `boot()`가 실행되기 때문이다멍! 아직 등록되지도 않은 다른 서비스를 부르면 `null` 에러가 터진다멍!

---

## 💡 6. 2강 자가진단 과제

1. `.env` 파일에 `PAYMENT_DRIVER=toss`를 지정하고, tinker에서 `get_class(app(PaymentGatewayContract::class))`를 실행했을 때 `TossPaymentGateway`로 바뀌는지 확인하세요.
2. 다시 `PAYMENT_DRIVER=mock`으로 바꾸면 무수정으로 `MockPaymentGateway`로 전환되는지 확인하세요.
{% endraw %}
