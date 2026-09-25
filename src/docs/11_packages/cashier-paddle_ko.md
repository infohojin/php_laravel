---
layout: docs
title: "라라벨 캐셔 (패들)"
---

{% raw %}
# 라라벨 캐셔 (패들)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
    - [Paddle Sandbox](#paddle-sandbox)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Paddle JS](#paddle-js)
    - [Currency Configuration](#currency-configuration)
    - [Overriding Default Models](#overriding-default-models)
- [Quickstart](#quickstart)
    - [Selling Products](#quickstart-selling-products)
    - [Selling Subscriptions](#quickstart-selling-subscriptions)
- [Checkout Sessions](#checkout-sessions)
    - [Overlay Checkout](#overlay-checkout)
    - [Inline Checkout](#inline-checkout)
    - [Guest Checkouts](#guest-checkouts)
- [Price Previews](#price-previews)
    - [Customer Price Previews](#customer-price-previews)
    - [Discounts](#price-discounts)
- [Customers](#customers)
    - [Customer Defaults](#customer-defaults)
    - [Retrieving Customers](#retrieving-customers)
    - [Creating Customers](#creating-customers)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Subscription Single Charges](#subscription-single-charges)
    - [Updating Payment Information](#updating-payment-information)
    - [Changing Plans](#changing-plans)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)
    - [Multiple Subscriptions](#multiple-subscriptions)
    - [Pausing Subscriptions](#pausing-subscriptions)
    - [Canceling Subscriptions](#canceling-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
    - [Extend or Activate a Trial](#extend-or-activate-a-trial)
- [Handling Paddle Webhooks](#handling-paddle-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Charging for Products](#charging-for-products)
    - [Refunding Transactions](#refunding-transactions)
    - [Crediting Transactions](#crediting-transactions)
- [Transactions](#transactions)
    - [Past and Upcoming Payments](#past-and-upcoming-payments)
- [Testing](#testing)

<a name="introduction"></a>
## Introduction



> [!WARNING]
> This documentation is for Cashier Paddle 2.x's integration with Paddle Billing. If you're still using Paddle Classic, you should use [Cashier Paddle 1.x](https://github.com/laravel/cashier-paddle/tree/1.x).

[Laravel Cashier Paddle](https://github.com/laravel/cashier-paddle) provides an expressive, fluent interface to [Paddle's](https://paddle.com) subscription billing services. It handles almost all of the boilerplate subscription billing code you are dreading. In addition to basic subscription management, Cashier can handle: swapping subscriptions, subscription "quantities", subscription pausing, cancelation grace periods, and more.

Before digging into Cashier Paddle, we recommend you also review Paddle's [concept guides](https://developer.paddle.com/concepts/overview) and [API documentation](https://developer.paddle.com/api-reference/overview).

<a name="upgrading-cashier"></a>
## Upgrading Cashier

When upgrading to a new version of Cashier, it's important that you carefully review [the upgrade guide](https://github.com/laravel/cashier-paddle/blob/master/UPGRADE.md).

<a name="installation"></a>
## Installation

First, install the Cashier package for Paddle using the Composer package manager:

```shell
composer require laravel/cashier-paddle
```



다음으로, `vendor:publish` Artisan 명령어를 사용하여 Cashier 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```



그런 다음, 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. Cashier 마이그레이션은 새로운 `customers` 테이블을 생성할 것입니다. 추가로, 새로운 `subscriptions` 및 `subscription_items` 테이블이 생성되어 고객의 모든 구독 정보를 저장하게 됩니다. 마지막으로, 새로운 `transactions` 테이블이 생성되어 고객과 관련된 모든 Paddle 거래를 저장하게 됩니다:

```shell
php artisan migrate
```



> [!WARNING]
> Cashier가 모든 Paddle 이벤트를 올바르게 처리하도록 하려면, [Cashier의 웹훅 처리 설정](#handling-paddle-webhooks)을 기억하세요.

<a name="paddle-sandbox"></a>
### Paddle 샌드박스

로컬 및 스테이징 개발 중에는 [Paddle 샌드박스 계정 등록](https://sandbox-login.paddle.com/signup)을 해야 합니다. 이 계정은 실제 결제를 하지 않고도 애플리케이션을 테스트하고 개발할 수 있는 샌드박스 환경을 제공합니다. Paddle의 [테스트 카드 번호](https://developer.paddle.com/concepts/payment-methods/credit-debit-card#test-payment-method)를 사용하여 다양한 결제 시나리오를 시뮬레이션할 수 있습니다.

Paddle 샌드박스 환경을 사용할 때, 애플리케이션의 `.env` 파일 내에서 환경 변수 `PADDLE_SANDBOX`를 `true`로 설정해야 합니다:

```ini
PADDLE_SANDBOX=true
```



애플리케이션 개발을 완료한 후, [Paddle 판매자 계정에 신청](https://paddle.com)할 수 있습니다. 귀하의 신청이 실제 운영 환경에 배치되기 전, Paddle은 귀하 애플리케이션의 도메인을 승인해야 합니다.

<a name="configuration"></a>
## 구성

<a name="billable-model"></a>
### 청구 모델

Cashier를 사용하기 전에, 사용자 모델 정의에 `Billable` 트레이트를 추가해야 합니다. 이 트레이트는 구독 생성, 결제 수단 정보 업데이트 같은 일반적인 청구 작업을 수행할 수 있는 다양한 메서드를 제공합니다:

```php
use Laravel\Paddle\Billable;

class User extends Authenticatable
{
    use Billable;
}
```



청구 가능한 항목이 사용자 외의 것이라면, 해당 클래스에도 속성을 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;
use Laravel\Paddle\Billable;

class Team extends Model
{
    use Billable;
}
```



<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에서 Paddle 키를 구성해야 합니다. Paddle API 키는 Paddle 제어판에서 가져올 수 있습니다:

```ini
PADDLE_CLIENT_SIDE_TOKEN=your-paddle-client-side-token
PADDLE_API_KEY=your-paddle-api-key
PADDLE_RETAIN_KEY=your-paddle-retain-key
PADDLE_WEBHOOK_SECRET="your-paddle-webhook-secret"
PADDLE_SANDBOX=true
```



`PADDLE_SANDBOX` 환경 변수는 [Paddle의 샌드박스 환경](#paddle-sandbox)을 사용할 때 `true`로 설정해야 합니다. 애플리케이션을 프로덕션 환경에 배포하고 Paddle의 라이브 벤더 환경을 사용하는 경우에는 `PADDLE_SANDBOX` 변수를 `false`로 설정해야 합니다.

`PADDLE_RETAIN_KEY`는 선택 사항이며, [Retain](https://developer.paddle.com/concepts/retain/overview)과 함께 Paddle을 사용하는 경우에만 설정해야 합니다.

<a name="paddle-js"></a>
### Paddle JS

Paddle은 Paddle 체크아웃 위젯을 시작하기 위해 자체 JavaScript 라이브러리에 의존합니다. 애플리케이션 레이아웃의 닫는 `</head>` 태그 바로 앞에 `@paddleJS` 블레이드 지시문을 배치하여 JavaScript 라이브러리를 로드할 수 있습니다:

```blade
<head>
    ...

    @paddleJS
</head>
```



<a name="currency-configuration"></a>
### 통화 구성

청구서에 금액을 표시할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로, Cashier는 통화 로케일을 설정하기 위해 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```



> [!WARNING]
> `en` 이외의 로케일을 사용하려면 서버에 `ext-intl` PHP 확장이 설치되고 구성되어 있는지 확인하십시오.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

Cashier에서 내부적으로 사용하는 모델을 확장하려면 자신만의 모델을 정의하고 해당 Cashier 모델을 확장하면 됩니다:

```php
use Laravel\Paddle\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```



모델을 정의한 후, `Laravel\Paddle\Cashier` 클래스를 통해 Cashier가 사용자 정의 모델을 사용하도록 지시할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 Cashier에게 사용자 정의 모델에 대해 알려야 합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\Transaction;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useTransactionModel(Transaction::class);
}
```



<a name="quickstart"></a>
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 제품 판매

> [!NOTE]
> Paddle Checkout을 사용하기 전에, Paddle 대시보드에서 고정 가격이 있는 제품을 정의해야 합니다. 또한, [Paddle의 웹훅 처리 설정](#handling-paddle-webhooks)을 해야 합니다.

애플리케이션을 통해 제품과 구독 결제를 제공하는 것은 위협적으로 느껴질 수 있습니다. 하지만 Cashier와 [Paddle의 Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout) 덕분에 현대적이고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

반복되지 않는 단일 결제 제품에 대해 고객에게 요금을 청구하려면, Cashier를 사용하여 Paddle의 Checkout Overlay로 고객 결제를 처리할 것입니다. 고객은 결제 정보를 제공하고 구매를 확인하게 됩니다. Checkout Overlay를 통해 결제가 완료되면, 고객은 애플리케이션 내에서 선택한 성공 URL로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout('pri_deluxe_album')
        ->returnTo(route('dashboard'));

    return view('buy', ['checkout' => $checkout]);
})->name('checkout');
```



위 예시에서 볼 수 있듯이, 우리는 Cashier가 제공하는 `checkout` 메서드를 사용하여 체크아웃 객체를 생성하고, 주어진 '가격 식별자'에 대해 고객에게 Paddle 체크아웃 오버레이를 제공합니다. Paddle을 사용할 때 '가격'은 [특정 제품에 대해 정의된 가격](https://developer.paddle.com/build/products/create-products-prices)을 의미합니다.

필요한 경우, `checkout` 메서드는 Paddle에서 자동으로 고객을 생성하고, 해당 Paddle 고객 기록을 애플리케이션 데이터베이스의 해당 사용자와 연결합니다. 체크아웃 세션이 완료되면, 고객은 전용 성공 페이지로 리디렉션되며, 그곳에서 고객에게 정보성 메시지를 표시할 수 있습니다.

`buy` 뷰에서는 체크아웃 오버레이를 표시하는 버튼을 포함할 예정입니다. `paddle-button` Blade 컴포넌트는 Cashier Paddle에 포함되어 있지만, [수동으로 오버레이 체크아웃을 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다.

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy Product
</x-paddle-button>
```



<a name="providing-meta-data-to-paddle-checkout"></a>
#### Paddle 결제에 메타 데이터 제공하기

제품을 판매할 때, 완료된 주문과 구매한 제품을 자신의 애플리케이션에서 정의한 `Cart` 및 `Order` 모델을 통해 추적하는 것이 일반적입니다. 고객이 구매를 완료하기 위해 Paddle의 결제 오버레이로 리디렉션될 때, 기존 주문 식별자를 제공해야 할 수도 있습니다. 이렇게 하면 고객이 애플리케이션으로 다시 리디렉션될 때 완료된 구매를 해당 주문과 연결할 수 있습니다.

이를 수행하려면, `checkout` 메서드에 사용자 지정 데이터 배열을 제공할 수 있습니다. 사용자가 결제 과정을 시작할 때 애플리케이션 내에서 보류 중인 `Order`가 생성된다고 가정해 봅시다. 이 예제에서 `Cart` 및 `Order` 모델은 설명을 위한 것이며 Cashier에서 제공하는 것은 아닙니다. 자신의 애플리케이션 요구에 맞게 이러한 개념을 자유롭게 구현할 수 있습니다:

```php
use App\Models\Cart;
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/cart/{cart}/checkout', function (Request $request, Cart $cart) {
    $order = Order::create([
        'cart_id' => $cart->id,
        'price_ids' => $cart->price_ids,
        'status' => 'incomplete',
    ]);

    $checkout = $request->user()->checkout($order->price_ids)
        ->customData(['order_id' => $order->id]);

    return view('billing', ['checkout' => $checkout]);
})->name('checkout');
```



위 예시에서 보시다시피, 사용자가 결제 과정을 시작하면, 우리는 장바구니/주문과 관련된 모든 Paddle 가격 식별자를 `checkout` 메서드에 제공합니다. 물론, 고객이 항목을 추가할 때 해당 항목들을 '쇼핑 카트' 또는 주문과 연계하는 것은 귀하의 애플리케이션 책임입니다. 또한, 주문 ID를 `customData` 메서드를 통해 Paddle Checkout Overlay에 제공합니다.

물론, 고객이 결제 과정을 마치면 주문을 '완료'로 표시하고 싶으실 겁니다. 이를 수행하려면, Paddle이 전송하고 Cashier가 이벤트를 통해 발생시키는 웹훅을 청취하여 데이터베이스에 주문 정보를 저장할 수 있습니다.

시작하려면, Cashier가 전송하는 `TransactionCompleted` 이벤트를 청취하십시오. 일반적으로, 애플리케이션의 `AppServiceProvider`에서 `boot` 메서드에 이벤트 리스너를 등록해야 합니다:

```php
use App\Listeners\CompleteOrder;
use Illuminate\Support\Facades\Event;
use Laravel\Paddle\Events\TransactionCompleted;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(TransactionCompleted::class, CompleteOrder::class);
}
```



이 예제에서 `CompleteOrder` 리스너는 다음과 같이 보일 수 있습니다:

```php
namespace App\Listeners;

use App\Models\Order;
use Laravel\Paddle\Cashier;
use Laravel\Paddle\Events\TransactionCompleted;

class CompleteOrder
{
    /**
     * Handle the incoming Cashier webhook event.
     */
    public function handle(TransactionCompleted $event): void
    {
        $orderId = $event->payload['data']['custom_data']['order_id'] ?? null;

        $order = Order::findOrFail($orderId);

        $order->update(['status' => 'completed']);
    }
}
```



Please refer to Paddle's documentation for more information on the [data contained by the `transaction.completed` event](https://developer.paddle.com/webhooks/transactions/transaction-completed).

<a name="quickstart-selling-subscriptions"></a>
### Selling Subscriptions

> [!NOTE]
> Before utilizing Paddle Checkout, you should define Products with fixed prices in your Paddle dashboard. In addition, you should [configure Paddle's webhook handling](#handling-paddle-webhooks).

Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Paddle's Checkout Overlay](https://developer.paddle.com/concepts/sell/overlay-checkout), you can easily build modern, robust payment integrations.

To learn how to sell subscriptions using Cashier and Paddle's Checkout Overlay, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Paddle dashboard. In addition, our subscription service might offer an "Expert" plan as `pro_expert`.

First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button will invoke a Paddle Checkout Overlay for their chosen plan. To get started, let's initiate a checkout session via the `checkout` method:

```php
use Illuminate\Http\Request;

Route::get('/subscribe', function (Request $request) {
    $checkout = $request->user()->checkout('price_basic_monthly')
        ->returnTo(route('dashboard'));

    return view('subscribe', ['checkout' => $checkout]);
})->name('subscribe');
```



`subscribe` 뷰에서는 체크아웃 오버레이를 표시하는 버튼을 포함할 예정입니다. `paddle-button` 블레이드 컴포넌트는 Cashier Paddle에 포함되어 있지만, [오버레이 체크아웃을 수동으로 렌더링](#manually-rendering-an-overlay-checkout)할 수도 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```



이제 구독 버튼을 클릭하면 고객이 결제 정보를 입력하고 구독을 시작할 수 있습니다. 일부 결제 수단은 처리에 몇 초가 걸리므로, 구독이 실제로 시작되었는지 확인하려면 [Cashier의 웹훅 처리 설정](#handling-paddle-webhooks)도 해야 합니다.

이제 고객이 구독을 시작할 수 있으므로, 특정 애플리케이션 부분은 구독한 사용자만 접근할 수 있도록 제한할 필요가 있습니다. 물론 Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 통해 사용자의 현재 구독 상태를 항상 확인할 수 있습니다.

```blade
@if ($user->subscribed())
    <p>You are subscribed.</p>
@endif
```



우리는 사용자가 특정 제품이나 요금제에 구독되어 있는지 여부도 쉽게 확인할 수 있습니다:

```blade
@if ($user->subscribedToProduct('pro_basic'))
    <p>You are subscribed to our Basic product.</p>
@endif

@if ($user->subscribedToPrice('price_basic_monthly'))
    <p>You are subscribed to our monthly Basic plan.</p>
@endif
```



<a name="quickstart-building-a-subscribed-middleware"></a>
#### 구독된 미들웨어 구축

편의를 위해, 들어오는 요청이 구독된 사용자로부터 온 것인지 판단하는 [미들웨어](/docs/{{version}}/middleware)를 생성할 수 있습니다. 이 미들웨어가 정의되면, 구독하지 않은 사용자가 해당 경로에 접근하지 못하도록 경로에 쉽게 할당할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class Subscribed
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        if (! $request->user()?->subscribed()) {
            // Redirect user to billing page and ask them to subscribe...
            return redirect('/subscribe');
        }

        return $next($request);
    }
}
```



미들웨어가 정의되면, 이를 라우트에 할당할 수 있습니다:

```php
use App\Http\Middleware\Subscribed;

Route::get('/dashboard', function () {
    // ...
})->middleware([Subscribed::class]);
```



<a name="quickstart-allowing-customers-to-manage-their-billing-plan"></a>
#### 고객이 청구 요금제를 관리할 수 있도록 허용하기

물론, 고객은 다른 제품이나 "등급"으로 구독 요금제를 변경하고 싶어할 수 있습니다. 위의 예에서 우리는 고객이 요금제를 월간 구독에서 연간 구독으로 변경할 수 있도록 허용하고자 합니다. 이를 위해 아래 경로로 연결되는 버튼과 같은 것을 구현해야 합니다:

```php
use Illuminate\Http\Request;

Route::put('/subscription/{price}/swap', function (Request $request, $price) {
    $user->subscription()->swap($price); // With "$price" being "price_basic_yearly" for this example.

    return redirect()->route('dashboard');
})->name('subscription.swap');
```



플랜을 교체하는 것 외에도 고객이 구독을 취소할 수 있도록 허용해야 합니다. 플랜을 교체하는 것처럼, 다음 경로로 연결되는 버튼을 제공하세요:

```php
use Illuminate\Http\Request;

Route::put('/subscription/cancel', function (Request $request, $price) {
    $user->subscription()->cancel();

    return redirect()->route('dashboard');
})->name('subscription.cancel');
```



And now your subscription will get canceled at the end of its billing period.

> [!NOTE]
> As long as you have configured Cashier's webhook handling, Cashier will automatically keep your application's Cashier-related database tables in sync by inspecting the incoming webhooks from Paddle. So, for example, when you cancel a customer's subscription via Paddle's dashboard, Cashier will receive the corresponding webhook and mark the subscription as "canceled" in your application's database.

<a name="checkout-sessions"></a>
## Checkout Sessions

Most operations to bill customers are performed using "checkouts" via Paddle's [Checkout Overlay widget](https://developer.paddle.com/build/checkout/build-overlay-checkout) or by utilizing [inline checkout](https://developer.paddle.com/build/checkout/build-branded-inline-checkout).

Before processing checkout payments using Paddle, you should define your application's [default payment link](https://developer.paddle.com/build/transactions/default-payment-link#set-default-link) in your Paddle checkout settings dashboard.

<a name="overlay-checkout"></a>
### Overlay Checkout

Before displaying the Checkout Overlay widget, you must generate a checkout session using Cashier. A checkout session will inform the checkout widget of the billing operation that should be performed:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```



캐셔에는 `paddle-button` [블레이드 컴포넌트](/docs/{{version}}/blade#components)가 포함되어 있습니다. 이 컴포넌트에 체크아웃 세션을 "prop"으로 전달할 수 있습니다. 그런 다음 이 버튼을 클릭하면 Paddle의 체크아웃 위젯이 표시됩니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```



기본적으로, 이것은 Paddle의 기본 스타일을 사용하여 위젯을 표시합니다. `data-theme='light'` 속성과 같은 [Paddle 지원 속성](https://developer.paddle.com/paddlejs/html-data-attributes)을 구성 요소에 추가하여 위젯을 사용자 정의할 수 있습니다:

```html
<x-paddle-button :checkout="$checkout" class="px-8 py-4" data-theme="light">
    Subscribe
</x-paddle-button>
```



Paddle 결제 위젯은 비동기식입니다. 사용자가 위젯 내에서 구독을 생성하면, Paddle은 애플리케이션에 웹훅을 전송하여 애플리케이션 데이터베이스에서 구독 상태를 올바르게 업데이트할 수 있도록 합니다. 따라서 Paddle의 상태 변경을 수용할 수 있도록 웹훅을 [적절히 설정](#handling-paddle-webhooks)하는 것이 중요합니다.

> [!WARNING]
> 구독 상태 변경 후 해당 웹훅을 받는 지연 시간은 일반적으로 최소이지만, 사용자가 결제를 완료한 직후에도 구독이 즉시 사용 가능하지 않을 수 있음을 고려하여 애플리케이션에서 이를 처리해야 합니다.

<a name="manually-rendering-an-overlay-checkout"></a>
#### 오버레이 결제 창 수동 렌더링

Laravel의 내장 Blade 컴포넌트를 사용하지 않고도 오버레이 결제 창을 수동으로 렌더링할 수 있습니다. 시작하려면, 이전 예제에서 설명한 것처럼 [결제 세션을 생성](#overlay-checkout)하세요:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```



다음으로, Paddle.js를 사용하여 결제를 초기화할 수 있습니다. 이 예제에서는 `paddle_button` 클래스가 지정된 링크를 생성할 것입니다. Paddle.js는 이 클래스를 감지하고 링크를 클릭하면 오버레이 결제를 표시합니다:

```blade
<?php
$items = $checkout->getItems();
$customer = $checkout->getCustomer();
$custom = $checkout->getCustomData();
?>

<a
    href='#!'
    class='paddle_button'
    data-items='{!! json_encode($items) !!}'
    @if ($customer) data-customer-id='{{ $customer->paddle_id }}' @endif
    @if ($custom) data-custom-data='{{ json_encode($custom) }}' @endif
    @if ($returnUrl = $checkout->getReturnUrl()) data-success-url='{{ $returnUrl }}' @endif
>
    Buy Product
</a>
```



<a name="inline-checkout"></a>
### 인라인 체크아웃

Paddle의 "오버레이" 스타일 체크아웃 위젯을 사용하고 싶지 않은 경우, Paddle은 위젯을 인라인으로 표시하는 옵션도 제공합니다. 이 방법은 체크아웃의 HTML 필드를 조정할 수는 없지만, 위젯을 애플리케이션 내에 삽입할 수 있게 해줍니다.

인라인 체크아웃을 쉽게 시작할 수 있도록, Cashier는 `paddle-checkout` Blade 구성 요소를 포함합니다. 시작하려면, [체크아웃 세션을 생성](#overlay-checkout)해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```



그런 다음, 체크아웃 세션을 컴포넌트의 `checkout` 속성에 전달할 수 있습니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" />
```



인라인 결제 컴포넌트의 높이를 조절하려면, Blade 컴포넌트에 `height` 속성을 전달할 수 있습니다:

```blade
<x-paddle-checkout :checkout="$checkout" class="w-full" height="500" />
```



자세한 내용은 Paddle의 [인라인 체크아웃 가이드](https://developer.paddle.com/build/checkout/build-branded-inline-checkout) 및 [사용 가능한 체크아웃 설정](https://developer.paddle.com/build/checkout/set-up-checkout-default-settings)을 참조하여 인라인 체크아웃의 맞춤 설정 옵션을 확인하세요.

<a name="manually-rendering-an-inline-checkout"></a>
#### 인라인 체크아웃 수동 렌더링

Laravel의 내장 Blade 컴포넌트를 사용하지 않고 인라인 체크아웃을 수동으로 렌더링할 수도 있습니다. 시작하려면 [이전 예제에서 설명한 것처럼](#inline-checkout) 체크아웃 세션을 생성하세요.

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $user->checkout('pri_34567')
        ->returnTo(route('dashboard'));

    return view('billing', ['checkout' => $checkout]);
});
```



다음으로, Paddle.js를 사용하여 결제를 초기화할 수 있습니다. 이 예제에서는 [Alpine.js](https://github.com/alpinejs/alpine)를 사용하여 이를 시연할 것이지만, 자신의 프론트엔드 스택에 맞게 이 예제를 자유롭게 수정할 수 있습니다:

```blade
<?php
$options = $checkout->options();

$options['settings']['frameTarget'] = 'paddle-checkout';
$options['settings']['frameInitialHeight'] = 366;
?>

<div class="paddle-checkout" x-data="{}" x-init="
    Paddle.Checkout.open(@json($options));
">
</div>
```



<a name="guest-checkouts"></a>
### 게스트 체크아웃

때때로, 애플리케이션 계정이 필요 없는 사용자를 위해 체크아웃 세션을 생성해야 할 때가 있습니다. 이를 위해, `guest` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Checkout;

Route::get('/buy', function (Request $request) {
    $checkout = Checkout::guest(['pri_34567'])
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```



그런 다음, 체크아웃 세션을 [Paddle 버튼](#overlay-checkout) 또는 [인라인 체크아웃](#inline-checkout) Blade 컴포넌트에 제공할 수 있습니다.

<a name="price-previews"></a>
## 가격 미리보기

Paddle은 통화별로 가격을 맞춤 설정할 수 있도록 하여 본질적으로 다양한 국가에 대해 다른 가격을 구성할 수 있게 합니다. Cashier Paddle은 `previewPrices` 메서드를 사용하여 이러한 모든 가격을 가져올 수 있습니다. 이 메서드는 가격을 가져오려는 가격 ID를 받습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456']);
```



통화는 요청의 IP 주소를 기준으로 결정됩니다. 그러나 가격을 확인하기 위해 특정 국가를 선택적으로 지정할 수 있습니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], ['address' => [
    'country_code' => 'BE',
    'postal_code' => '1234',
]]);
```



가격을 가져온 후에는 원하는 방식으로 표시할 수 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```



소계 가격과 세금 금액을 따로 표시할 수도 있습니다:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->subtotal() }} (+ {{ $price->tax() }} tax)</li>
    @endforeach
</ul>
```



자세한 정보는 [가격 미리보기에 관한 Paddle의 API 문서](https://developer.paddle.com/api-reference/pricing-preview/preview-prices)를 참고하세요.

<a name="customer-price-previews"></a>
### 고객 가격 미리보기

사용자가 이미 고객인 경우, 해당 고객에게 적용되는 가격을 표시하고 싶다면 고객 인스턴스에서 직접 가격을 가져와 표시할 수 있습니다:

```php
use App\Models\User;

$prices = User::find(1)->previewPrices(['pri_123', 'pri_456']);
```



내부적으로 Cashier는 사용자의 고객 ID를 사용하여 해당 사용자의 통화로 가격을 조회합니다. 예를 들어, 미국에 거주하는 사용자는 미국 달러로 가격을, 벨기에에 거주하는 사용자는 유로로 가격을 보게 됩니다. 일치하는 통화를 찾을 수 없는 경우, 제품의 기본 통화가 사용됩니다. 제품 또는 구독 플랜의 모든 가격은 Paddle 제어판에서 사용자 지정할 수 있습니다.

<a name="price-discounts"></a>
### 할인

할인 후 가격을 표시하도록 선택할 수도 있습니다. `previewPrices` 메서드를 호출할 때, `discount_id` 옵션을 통해 할인 ID를 제공합니다:

```php
use Laravel\Paddle\Cashier;

$prices = Cashier::previewPrices(['pri_123', 'pri_456'], [
    'discount_id' => 'dsc_123'
]);
```



그런 다음, 계산된 가격을 표시하세요:

```blade
<ul>
    @foreach ($prices as $price)
        <li>{{ $price->product['name'] }} - {{ $price->total() }}</li>
    @endforeach
</ul>
```



<a name="customers"></a>
## 고객

<a name="customer-defaults"></a>
### 고객 기본 설정

캐셔는 체크아웃 세션을 생성할 때 고객에게 유용한 기본 설정을 정의할 수 있게 해줍니다. 이러한 기본 설정을 지정하면 고객의 이메일 주소와 이름을 미리 채워서 고객이 즉시 체크아웃 위젯의 결제 부분으로 이동할 수 있습니다. 이러한 기본 설정은 청구 가능한 모델에서 다음 메서드를 재정의하여 설정할 수 있습니다:

```php
/**
 * Get the customer's name to associate with Paddle.
 */
public function paddleName(): string|null
{
    return $this->name;
}

/**
 * Get the customer's email address to associate with Paddle.
 */
public function paddleEmail(): string|null
{
    return $this->email;
}
```



이 기본 설정은 [체크아웃 세션](#checkout-sessions)을 생성하는 Cashier의 모든 작업에 사용됩니다.

<a name="retrieving-customers"></a>
### 고객 조회

Paddle 고객 ID를 사용하여 `Cashier::findBillable` 메서드로 고객을 조회할 수 있습니다. 이 메서드는 청구 가능 모델의 인스턴스를 반환합니다:

```php
use Laravel\Paddle\Cashier;

$user = Cashier::findBillable($customerId);
```



<a name="creating-customers"></a>
### 고객 생성

가끔은 구독을 시작하지 않고 Paddle 고객을 생성하고 싶을 수 있습니다. `createAsCustomer` 방법을 사용하여 이를 수행할 수 있습니다:

```php
$customer = $user->createAsCustomer();
```



`Laravel\Paddle\Customer`의 인스턴스가 반환됩니다. 고객이 Paddle에서 생성되면 나중에 구독을 시작할 수 있습니다. 선택적으로 `$options` 배열을 제공하여 Paddle API에서 지원하는 추가 [고객 생성 매개변수](https://developer.paddle.com/api-reference/customers/create-customer)를 전달할 수 있습니다:

```php
$customer = $user->createAsCustomer($options);
```



<a name="subscriptions"></a>
## 구독

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면 먼저 데이터베이스에서 청구 가능한 모델 인스턴스를 가져와야 하며, 일반적으로 이는 `App\Models\User` 인스턴스가 됩니다. 모델 인스턴스를 가져왔으면 `subscribe` 메서드를 사용하여 모델의 체크아웃 세션을 생성할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```



`subscribe` 메서드에 전달되는 첫 번째 인수는 사용자가 구독하는 특정 가격입니다. 이 값은 Paddle의 가격 식별자와 일치해야 합니다. `returnTo` 메서드는 사용자가 결제를 성공적으로 완료한 후 리디렉션될 URL을 받습니다. `subscribe` 메서드에 전달되는 두 번째 인수는 구독의 내부 "type"이어야 합니다. 애플리케이션에서 단일 구독만 제공하는 경우, 이를 `default` 또는 `primary`라고 부를 수 있습니다. 이 구독 유형은 내부 애플리케이션 용도로만 사용되며 사용자가 볼 수 있도록 표시되지 않습니다. 또한 공백을 포함하면 안 되며, 구독을 생성한 후에는 절대 변경되지 않아야 합니다.

`customData` 메서드를 사용하여 구독과 관련된 사용자 정의 메타데이터 배열을 제공할 수도 있습니다:

```php
$checkout = $request->user()->subscribe($premium = 'pri_123', 'default')
    ->customData(['key' => 'value'])
    ->returnTo(route('home'));
```



구독 결제 세션이 생성되면, 결제 세션은 Cashier Paddle에 포함된 `paddle-button` [Blade 컴포넌트](#overlay-checkout)에 제공될 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Subscribe
</x-paddle-button>
```



사용자가 체크아웃을 완료하면 Paddle에서 `subscription_created` 웹후크가 전송됩니다. Cashier는 이 웹후크를 수신하고 고객을 위한 구독을 설정합니다. 모든 웹후크가 귀하의 애플리케이션에서 올바르게 수신되고 처리되도록 하려면, [웹후크 처리 설정](#handling-paddle-webhooks)을 올바르게 했는지 확인하세요.

<a name="checking-subscription-status"></a>
### 구독 상태 확인

사용자가 귀하의 애플리케이션에 구독하면, 다양한 편리한 방법을 사용하여 구독 상태를 확인할 수 있습니다. 먼저, `subscribed` 메서드는 사용자가 유효한 구독을 가지고 있으면, 구독이 현재 체험 기간에 있더라도 `true`를 반환합니다.

```php
if ($user->subscribed()) {
    // ...
}
```



애플리케이션이 여러 구독을 제공하는 경우, `subscribed` 메서드를 호출할 때 구독을 지정할 수 있습니다:

```php
if ($user->subscribed('default')) {
    // ...
}
```



`subscribed` 방법은 또한 [라우트 미들웨어](/docs/{{version}}/middleware)로 훌륭한 후보가 되어, 사용자의 구독 상태에 따라 라우트와 컨트롤러에 대한 접근을 필터링할 수 있게 해줍니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserIsSubscribed
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->user() && ! $request->user()->subscribed()) {
            // This user is not a paying customer...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```



사용자가 아직 체험 기간에 있는지 확인하고 싶다면 `onTrial` 방법을 사용할 수 있습니다. 이 방법은 사용자가 여전히 체험 기간에 있음을 경고해야 할지 결정하는 데 유용할 수 있습니다:

```php
if ($user->subscription()->onTrial()) {
    // ...
}
```



`subscribedToPrice` 방법은 사용자가 주어진 Paddle 가격 ID에 따라 특정 요금제에 가입되어 있는지 확인하는 데 사용될 수 있습니다. 이 예제에서는 사용자의 `default` 구독이 월별 요금제에 활성적으로 가입되어 있는지 확인할 것입니다:

```php
if ($user->subscribedToPrice($monthly = 'pri_123', 'default')) {
    // ...
}
```



`recurring` 방법은 사용자가 현재 활성 구독 중인지, 더 이상 체험 기간 또는 유예 기간에 속하지 않는지를 확인하는 데 사용할 수 있습니다:

```php
if ($user->subscription()->recurring()) {
    // ...
}
```



<a name="canceled-subscription-status"></a>
#### 취소된 구독 상태

사용자가 한때 활성 구독자였지만 구독을 취소했는지 확인하려면 `canceled` 방법을 사용할 수 있습니다:

```php
if ($user->subscription()->canceled()) {
    // ...
}
```



사용자가 구독을 취소했지만 구독이 완전히 만료될 때까지 '유예 기간(grace period)'에 있는지 여부도 확인할 수 있습니다. 예를 들어, 사용자가 원래 3월 10일에 만료될 예정이었던 구독을 3월 5일에 취소한 경우, 사용자는 3월 10일까지 '유예 기간'에 있습니다. 또한 이 기간 동안 `subscribed` 메서드는 여전히 `true`를 반환합니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```



<a name="past-due-status"></a>
#### 연체 상태

구독 결제가 실패하면 `past_due`로 표시됩니다. 구독이 이 상태일 때는 고객이 결제 정보를 업데이트할 때까지 활성 상태가 되지 않습니다. 구독 인스턴스에서 `pastDue` 메서드를 사용하여 구독이 연체 상태인지 확인할 수 있습니다:

```php
if ($user->subscription()->pastDue()) {
    // ...
}
```



구독이 연체된 경우, 사용자가 [결제 정보를 업데이트](#updating-payment-information)하도록 안내해야 합니다.

구독이 `past_due`일 때에도 여전히 유효한 것으로 간주되기를 원하는 경우, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 방법을 사용할 수 있습니다. 일반적으로 이 방법은 `AppServiceProvider`의 `register` 메서드에서 호출되어야 합니다:

```php
use Laravel\Paddle\Cashier;

/**
 * Register any application services.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
}
```



> [!WARNING]
> 구독이 `past_due` 상태일 때는 결제 정보가 업데이트될 때까지 변경할 수 없습니다. 따라서, 구독이 `past_due` 상태일 경우 `swap` 및 `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 범위

대부분의 구독 상태는 쿼리 범위로도 제공되어, 특정 상태에 있는 구독을 데이터베이스에서 쉽게 조회할 수 있습니다:

```php
// Get all valid subscriptions...
$subscriptions = Subscription::query()->valid()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```



사용 가능한 모든 범위 목록은 아래에서 확인할 수 있습니다:

```php
Subscription::query()->valid();
Subscription::query()->onTrial();
Subscription::query()->expiredTrial();
Subscription::query()->notOnTrial();
Subscription::query()->active();
Subscription::query()->recurring();
Subscription::query()->pastDue();
Subscription::query()->paused();
Subscription::query()->notPaused();
Subscription::query()->onPausedGracePeriod();
Subscription::query()->notOnPausedGracePeriod();
Subscription::query()->canceled();
Subscription::query()->notCanceled();
Subscription::query()->onGracePeriod();
Subscription::query()->notOnGracePeriod();
```



<a name="subscription-single-charges"></a>
### 구독 단일 요금

구독 단일 요금은 구독자에게 구독 요금 외에 일회성 요금을 부과할 수 있게 합니다. `charge` 메서드를 호출할 때 하나 이상의 가격 ID를 제공해야 합니다:

```php
// Charge a single price...
$response = $user->subscription()->charge('pri_123');

// Charge multiple prices at once...
$response = $user->subscription()->charge(['pri_123', 'pri_456']);
```



`charge` 방법은 실제로 고객에게 요금을 청구하지 않고, 구독의 다음 청구 기간까지 기다립니다. 고객에게 즉시 요금을 청구하고 싶다면 대신 `chargeAndInvoice` 방법을 사용할 수 있습니다:

```php
$response = $user->subscription()->chargeAndInvoice('pri_123');
```



<a name="updating-payment-information"></a>
### 결제 정보 업데이트

Paddle은 항상 구독별로 결제 수단을 저장합니다. 구독의 기본 결제 수단을 업데이트하려면, 구독 모델에서 `redirectToUpdatePaymentMethod` 방법을 사용하여 고객을 Paddle 호스팅 결제 수단 업데이트 페이지로 리디렉션해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/update-payment-method', function (Request $request) {
    $user = $request->user();

    return $user->subscription()->redirectToUpdatePaymentMethod();
});
```



사용자가 정보를 업데이트를 마치면, Paddle에서 `subscription_updated` 웹훅이 발송되고 구독 세부 정보가 애플리케이션의 데이터베이스에 업데이트됩니다.

<a name="changing-plans"></a>
### 요금제 변경

사용자가 애플리케이션을 구독한 후에는 때때로 새로운 구독 요금제로 변경하고자 할 수 있습니다. 사용자의 구독 요금제를 업데이트하려면, Paddle 가격 식별자를 구독의 `swap` 메서드에 전달해야 합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription()->swap($premium = 'pri_456');
```



다음 결제 주기를 기다리지 않고 계획을 변경하고 즉시 사용자에게 청구서를 발송하려면 `swapAndInvoice` 방법을 사용할 수 있습니다:

```php
$user = User::find(1);

$user->subscription()->swapAndInvoice($premium = 'pri_456');
```



<a name="prorations"></a>
#### 비례 배분

기본적으로 Paddle은 요금제를 변경할 때 요금을 비례 배분합니다. 요금을 비례 배분하지 않고 구독을 업데이트하려면 `noProrate` 방법을 사용할 수 있습니다:

```php
$user->subscription('default')->noProrate()->swap($premium = 'pri_456');
```



만약 요금 비례 배분을 비활성화하고 고객에게 즉시 청구서를 발송하고 싶다면, `noProrate`와 함께 `swapAndInvoice` 방법을 사용할 수 있습니다:

```php
$user->subscription('default')->noProrate()->swapAndInvoice($premium = 'pri_456');
```



또는 구독 변경에 대해 고객에게 청구하지 않으려면, `doNotBill` 방법을 사용할 수 있습니다:

```php
$user->subscription('default')->doNotBill()->swap($premium = 'pri_456');
```



Paddle의 비례 배분(proration) 정책에 대한 자세한 정보는 Paddle의 [비례 배분 문서](https://developer.paddle.com/concepts/subscriptions/proration)를 참조하십시오.

<a name="subscription-quantity"></a>
### 구독 수량

때때로 구독에는 "수량"이 영향을 미칠 수 있습니다. 예를 들어, 프로젝트 관리 애플리케이션은 프로젝트당 월 $10를 청구할 수 있습니다. 구독 수량을 쉽게 증가시키거나 감소시키려면, `incrementQuantity` 및 `decrementQuantity` 메서드를 사용하십시오:

```php
$user = User::find(1);

$user->subscription()->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription()->incrementQuantity(5);

$user->subscription()->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription()->decrementQuantity(5);
```



또는 `updateQuantity` 방법을 사용하여 특정 수량을 설정할 수 있습니다:

```php
$user->subscription()->updateQuantity(10);
```



`noProrate` 방법은 요금을 비례 조정하지 않고 구독 수량을 업데이트하는 데 사용할 수 있습니다:

```php
$user->subscription()->noProrate()->updateQuantity(10);
```



<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 제품이 포함된 구독의 수량

구독이 [여러 제품이 포함된 구독](#subscriptions-with-multiple-products)인 경우, 수량을 증가시키거나 감소시키고자 하는 가격의 ID를 증감 메서드의 두 번째 인수로 전달해야 합니다:

```php
$user->subscription()->incrementQuantity(1, 'price_chat');
```



<a name="subscriptions-with-multiple-products"></a>
### 여러 제품이 포함된 구독

[여러 제품이 포함된 구독](https://developer.paddle.com/build/subscriptions/add-remove-products-prices-addons)은 단일 구독에 여러 청구 제품을 할당할 수 있습니다. 예를 들어, 월 기본 구독료가 $10인 고객 서비스 "헬프데스크" 애플리케이션을 구축하면서 월 $15의 추가 비용으로 라이브 채팅 애드온 제품을 제공한다고 가정해 보세요.

구독 체크아웃 세션을 생성할 때, `subscribe` 메서드의 첫 번째 인수로 가격 배열을 전달하여 특정 구독에 여러 제품을 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe([
        'price_monthly',
        'price_chat',
    ]);

    return view('billing', ['checkout' => $checkout]);
});
```



위의 예제에서, 고객은 `default` 구독에 두 가지 가격이 붙게 됩니다. 두 가격 모두 해당 청구 주기에 따라 청구됩니다. 필요한 경우, 각 가격에 대해 특정 수량을 나타내기 위해 키/값 쌍의 연관 배열을 전달할 수 있습니다:

```php
$user = User::find(1);

$checkout = $user->subscribe('default', ['price_monthly', 'price_chat' => 5]);
```



기존 구독에 다른 가격을 추가하고 싶다면, 구독의 `swap` 메서드를 사용해야 합니다. `swap` 메서드를 호출할 때는 구독의 현재 가격과 수량도 포함해야 합니다:

```php
$user = User::find(1);

$user->subscription()->swap(['price_chat', 'price_original' => 2]);
```



위의 예시는 새로운 가격을 추가하지만, 고객은 다음 청구 주기까지 요금이 부과되지 않습니다. 고객에게 즉시 청구하려면 `swapAndInvoice` 방법을 사용할 수 있습니다:

```php
$user->subscription()->swapAndInvoice(['price_chat', 'price_original' => 2]);
```



`swap` 방법을 사용하고 제거하려는 가격을 생략하여 구독에서 가격을 제거할 수 있습니다:

```php
$user->subscription()->swap(['price_original' => 2]);
```



> [!WARNING]
> 구독의 마지막 가격을 제거할 수 없습니다. 대신, 단순히 구독을 취소해야 합니다.

<a name="multiple-subscriptions"></a>
### 다중 구독

Paddle은 고객이 동시에 여러 구독을 가질 수 있도록 허용합니다. 예를 들어, 체육관을 운영한다고 가정하면, 수영 구독과 웨이트 트레이닝 구독을 제공할 수 있으며, 각 구독은 서로 다른 가격을 가질 수 있습니다. 물론 고객은 각각의 구독이나 두 가지 구독 모두에 가입할 수 있어야 합니다.

애플리케이션이 구독을 생성할 때, 구독의 유형을 두 번째 인수로 `subscribe` 메서드에 제공할 수 있습니다. 유형은 사용자가 시작하려는 구독 유형을 나타내는 모든 문자열이 될 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $checkout = $request->user()->subscribe($swimmingMonthly = 'pri_123', 'swimming');

    return view('billing', ['checkout' => $checkout]);
});
```



이 예제에서 우리는 고객을 위해 월간 수영 구독을 시작했습니다. 하지만 나중에 연간 구독으로 변경하고 싶어할 수도 있습니다. 고객의 구독을 조정할 때는 `swimming` 구독의 가격만 간단히 변경하면 됩니다:

```php
$user->subscription('swimming')->swap($swimmingYearly = 'pri_456');
```



물론, 구독을 완전히 취소할 수도 있습니다:

```php
$user->subscription('swimming')->cancel();
```



<a name="pausing-subscriptions"></a>
### 구독 일시 중지

구독을 일시 중지하려면 사용자의 구독에서 `pause` 메서드를 호출하세요:

```php
$user->subscription()->pause();
```



구독이 일시 중지되면, Cashier는 자동으로 데이터베이스의 `paused_at` 열을 설정합니다. 이 열은 `paused` 메서드가 언제 `true`를 반환하기 시작해야 하는지를 결정하는 데 사용됩니다. 예를 들어, 고객이 3월 1일에 구독을 일시 중지했지만 구독이 3월 5일까지 반복되지 않도록 예약되어 있었다면, `paused` 메서드는 3월 5일까지 계속 `false`를 반환합니다. 이는 일반적으로 사용자가 청구 주기 종료 시점까지 애플리케이션을 계속 사용하도록 허용되기 때문입니다.

기본적으로 일시 중지는 다음 청구 주기에 발생하므로 고객은 이미 지불한 기간의 나머지를 사용할 수 있습니다. 구독을 즉시 일시 중지하려면 `pauseNow` 메서드를 사용할 수 있습니다:

```php
$user->subscription()->pauseNow();
```



`pauseUntil` 방법을 사용하면 특정 시점까지 구독을 일시 중지할 수 있습니다:

```php
$user->subscription()->pauseUntil(now()->plus(months: 1));
```



또는 주어진 시점까지 구독을 즉시 일시 중지하려면 `pauseNowUntil` 방법을 사용할 수 있습니다:

```php
$user->subscription()->pauseNowUntil(now()->plus(months: 1));
```



사용자가 구독을 일시 중지했지만 여전히 '유예 기간'에 있는지 여부는 `onPausedGracePeriod` 방법을 사용하여 확인할 수 있습니다:

```php
if ($user->subscription()->onPausedGracePeriod()) {
    // ...
}
```



일시 중단된 구독을 재개하려면 구독에서 `resume` 메서드를 호출할 수 있습니다:

```php
$user->subscription()->resume();
```



> [!WARNING]
> 구독은 일시 중지된 상태에서 수정할 수 없습니다. 다른 요금제로 변경하거나 수량을 업데이트하려면 먼저 구독을 재개해야 합니다.

<a name="canceling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 사용자 구독에서 `cancel` 메서드를 호출하십시오:

```php
$user->subscription()->cancel();
```



구독이 취소되면, Cashier는 자동으로 데이터베이스의 `ends_at` 열을 설정합니다. 이 열은 `subscribed` 메서드가 언제 `false`를 반환하기 시작해야 하는지를 결정하는 데 사용됩니다. 예를 들어, 고객이 3월 1일에 구독을 취소했지만 구독이 3월 5일까지 종료될 예정이었다면, `subscribed` 메서드는 3월 5일까지 계속해서 `true`를 반환합니다. 이는 사용자가 일반적으로 청구 주기 종료 시점까지 애플리케이션을 계속 사용할 수 있도록 허용되기 때문에 이루어집니다.

`onGracePeriod` 메서드를 사용하여 사용자가 구독을 취소했지만 여전히 "유예 기간"에 있는지 확인할 수 있습니다:

```php
if ($user->subscription()->onGracePeriod()) {
    // ...
}
```



구독을 즉시 취소하고자 하는 경우, 구독에서 `cancelNow` 메서드를 호출할 수 있습니다:

```php
$user->subscription()->cancelNow();
```



유예 기간 동안 구독 취소를 막으려면, `stopCancelation` 방법을 호출할 수 있습니다:

```php
$user->subscription()->stopCancelation();
```



> [!WARNING]
> Paddle의 구독은 취소 후 재개할 수 없습니다. 고객이 구독을 재개하고자 하는 경우, 새 구독을 생성해야 합니다.

<a name="subscription-trials"></a>
## 구독 체험판

<a name="with-payment-method-up-front"></a>
### 사전 결제 방식

고객에게 체험 기간을 제공하면서도 결제 정보 수집을 원하면, 고객이 구독하는 가격에서 Paddle 대시보드에서 체험 기간을 설정해야 합니다. 그런 다음 결제 세션을 정상적으로 시작합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```



사용자의 애플리케이션이 `subscription_created` 이벤트를 수신하면, Cashier는 애플리케이션 데이터베이스 내 구독 기록에 시험 사용 기간 종료 날짜를 설정하고, 이 날짜가 지나기 전까지 Paddle이 고객에게 과금하지 않도록 지시합니다.

> [!WARNING]
> 고객의 구독이 시험 사용 종료 날짜 전에 취소되지 않으면, 시험 사용 기간이 만료되자마자 요금이 부과되므로 사용자가 시험 사용 종료 날짜를 알 수 있도록 반드시 통지해야 합니다.

사용자가 시험 사용 기간에 있는지 여부는 사용자 인스턴스의 `onTrial` 메서드를 사용하여 확인할 수 있습니다:

```php
if ($user->onTrial()) {
    // ...
}
```



기존 평가판이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다:

```php
if ($user->hasExpiredTrial()) {
    // ...
}
```



사용자가 특정 구독 유형에 대해 체험 중인지 확인하려면 `onTrial` 또는 `hasExpiredTrial` 메서드에 해당 유형을 제공할 수 있습니다:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->hasExpiredTrial('default')) {
    // ...
}
```



<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 시작

사용자의 결제 수단 정보를 미리 수집하지 않고 체험 기간을 제공하려면, 사용자에게 연결된 고객 기록의 `trial_ends_at` 열을 원하는 체험 종료 날짜로 설정할 수 있습니다. 이는 일반적으로 사용자 등록 시에 수행됩니다:

```php
use App\Models\User;

$user = User::create([
    // ...
]);

$user->createAsCustomer([
    'trial_ends_at' => now()->plus(days: 10)
]);
```



캐셔는 이 유형의 체험을 '일반 체험'이라고 부르는데, 이는 기존 구독과 연결되어 있지 않기 때문입니다. `User` 인스턴스의 `onTrial` 메서드는 현재 날짜가 `trial_ends_at`의 값보다 지나지 않았다면 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```



사용자를 위해 실제 구독을 생성할 준비가 되면, 평소처럼 `subscribe` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/user/subscribe', function (Request $request) {
    $checkout = $request->user()
        ->subscribe('pri_monthly')
        ->returnTo(route('home'));

    return view('billing', ['checkout' => $checkout]);
});
```



사용자의 체험 종료 날짜를 가져오기 위해서는 `trialEndsAt` 메서드를 사용할 수 있습니다. 사용자가 체험 중인 경우 이 메서드는 Carbon 날짜 인스턴스를 반환하고, 체험 중이 아니라면 `null`를 반환합니다. 또한 기본 구독이 아닌 특정 구독에 대한 체험 종료 날짜를 가져오고 싶다면 선택적 구독 유형 매개변수를 전달할 수도 있습니다:

```php
if ($user->onTrial('default')) {
    $trialEndsAt = $user->trialEndsAt();
}
```



사용자가 실제 구독을 생성하지 않고 '일반' 체험 기간 내에 있는지 구체적으로 알고 싶다면 `onGenericTrial` 방법을 사용할 수 있습니다:

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```



<a name="extend-or-activate-a-trial"></a>
### 체험 기간 연장 또는 활성화

`extendTrial` 메서드를 호출하고 체험이 끝날 시점을 지정하면 구독의 기존 체험 기간을 연장할 수 있습니다:

```php
$user->subscription()->extendTrial(now()->plus(days: 5));
```



또는 구독에서 `activate` 메서드를 호출하여 체험판을 종료함으로써 즉시 구독을 활성화할 수 있습니다:

```php
$user->subscription()->activate();
```



<a name="handling-paddle-webhooks"></a>
## Handling Paddle Webhooks

Paddle can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is registered by the Cashier service provider. This controller will handle all incoming webhook requests.

By default, this controller will automatically handle canceling subscriptions that have too many failed charges, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Paddle webhook event you like.

To ensure your application can handle Paddle webhooks, be sure to [configure the webhook URL in the Paddle control panel](https://vendors.paddle.com/notifications-v2). By default, Cashier's webhook controller responds to the `/paddle/webhook` URL path. The full list of all webhooks you should enable in the Paddle control panel are:

- Customer Updated
- Transaction Completed
- Transaction Updated
- Subscription Created
- Subscription Updated
- Subscription Paused
- Subscription Canceled

> [!WARNING]
> Make sure you protect incoming requests with Cashier's included [webhook signature verification](/docs/{{version}}/cashier-paddle#verifying-webhook-signatures) middleware.

<a name="webhooks-csrf-protection"></a>
#### Webhooks and CSRF Protection

Since Paddle webhooks need to bypass Laravel's [CSRF protection](/docs/{{version}}/csrf), you should ensure that Laravel does not attempt to verify the CSRF token for incoming Paddle webhooks. To accomplish this, you should exclude `paddle/*` from CSRF protection in your application's `bootstrap/app.php` file:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'paddle/*',
    ]);
})
```



<a name="webhooks-local-development"></a>
#### 웹훅과 로컬 개발

Paddle이 로컬 개발 중에 애플리케이션에 웹훅을 보낼 수 있으려면, [Ngrok](https://ngrok.com/) 또는 [Expose](https://expose.dev/docs/introduction)와 같은 사이트 공유 서비스를 통해 애플리케이션을 노출해야 합니다. 만약 [Laravel Sail](/docs/{{version}}/sail)을 사용하여 로컬에서 애플리케이션을 개발 중이라면, Sail의 [사이트 공유 명령어](/docs/{{version}}/sail#sharing-your-site)를 사용할 수 있습니다.

<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 실패한 결제로 인한 구독 취소 및 다른 일반적인 Paddle 웹훅을 자동으로 처리합니다. 그러나 처리하고 싶은 추가 웹훅 이벤트가 있다면, Cashier에서 발송하는 다음 이벤트들을 수신하여 처리할 수 있습니다:

- `Laravel\Paddle\Events\WebhookReceived`
- `Laravel\Paddle\Events\WebhookHandled`

두 이벤트 모두 Paddle 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `transaction.billed` 웹훅을 처리하고 싶다면, 이벤트를 처리할 [리스너](/docs/{{version}}/events#defining-listeners)를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Laravel\Paddle\Events\WebhookReceived;

class PaddleEventListener
{
    /**
     * Handle received Paddle webhooks.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['event_type'] === 'transaction.billed') {
            // Handle the incoming event...
        }
    }
}
```



캐셔는 수신된 웹훅의 유형에 전용 이벤트도 발생시킵니다. Paddle에서 받은 전체 페이로드 외에도, 웹훅을 처리하는 데 사용된 관련 모델들도 포함되어 있습니다. 예를 들어 청구 가능 모델, 구독, 영수증 등이 있습니다:

<div class="content-list" markdown="1">

- `Laravel\Paddle\Events\CustomerUpdated`
- `Laravel\Paddle\Events\TransactionCompleted`
- `Laravel\Paddle\Events\TransactionUpdated`
- `Laravel\Paddle\Events\SubscriptionCreated`
- `Laravel\Paddle\Events\SubscriptionUpdated`
- `Laravel\Paddle\Events\SubscriptionPaused`
- `Laravel\Paddle\Events\SubscriptionCanceled`

</div>

응용 프로그램의 `.env` 파일에서 `CASHIER_WEBHOOK` 환경 변수를 정의하여 기본 내장 웹훅 경로를 재정의할 수도 있습니다. 이 값은 웹훅 경로의 전체 URL이어야 하며, Paddle 제어판에 설정된 URL과 일치해야 합니다:

```ini
CASHIER_WEBHOOK=https://example.com/my-paddle-webhook-url
```



<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅을 안전하게 보호하기 위해 [Paddle의 웹훅 서명](https://developer.paddle.com/webhooks/signature-verification)을 사용할 수 있습니다. 편의를 위해, Cashier는 들어오는 Paddle 웹훅 요청이 유효한지를 검증하는 미들웨어를 자동으로 포함합니다.

웹훅 검증을 활성화하려면, `PADDLE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 정의되어 있는지 확인하십시오. 웹훅 비밀은 Paddle 계정 대시보드에서 가져올 수 있습니다.

<a name="single-charges"></a>
## 단일 요금

<a name="charging-for-products"></a>
### 제품 요금 부과

고객의 제품 구매를 시작하려면, 청구 가능한 모델 인스턴스에서 `checkout` 메서드를 사용하여 구매를 위한 체크아웃 세션을 생성할 수 있습니다. `checkout` 메서드는 하나 이상의 가격 ID를 받습니다. 필요 시, 구입 중인 제품의 수량을 제공하기 위해 연관 배열을 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/buy', function (Request $request) {
    $checkout = $request->user()->checkout(['pri_tshirt', 'pri_socks' => 5]);

    return view('buy', ['checkout' => $checkout]);
});
```



체크아웃 세션을 생성한 후, 사용자가 Paddle 체크아웃 위젯을 보고 구매를 완료할 수 있도록 Cashier가 제공하는 `paddle-button` [Blade 컴포넌트](#overlay-checkout)를 사용할 수 있습니다:

```blade
<x-paddle-button :checkout="$checkout" class="px-8 py-4">
    Buy
</x-paddle-button>
```



체크아웃 세션에는 `customData` 메서드가 있어 기본 거래 생성에 원하는 모든 커스텀 데이터를 전달할 수 있습니다. 커스텀 데이터를 전달할 때 사용할 수 있는 옵션에 대해 자세히 알아보려면 [Paddle 문서](https://developer.paddle.com/build/transactions/custom-data)를 참조하십시오:

```php
$checkout = $user->checkout('pri_tshirt')
    ->customData([
        'custom_option' => $value,
    ]);
```



<a name="refunding-transactions"></a>
### 거래 환불

거래 환불은 구매 시 사용된 고객의 결제 수단으로 환불 금액을 반환합니다. Paddle 구매를 환불해야 하는 경우, `Cashier\Paddle\Transaction` 모델에서 `refund` 방법을 사용할 수 있습니다. 이 방법은 첫 번째 인수로 사유를 받고, 하나 이상의 가격 ID와 선택적 금액을 연관 배열로 환불할 수 있습니다. `transactions` 방법을 사용하여 특정 청구 모델의 거래 내역을 검색할 수 있습니다.

예를 들어, 가격 `pri_123`와 `pri_456`에 대한 특정 거래를 환불하고자 한다고 가정해봅시다. `pri_123`는 전액 환불하고, `pri_456`는 2달러만 환불하고 싶습니다:

```php
use App\Models\User;

$user = User::find(1);

$transaction = $user->transactions()->first();

$response = $transaction->refund('Accidental charge', [
    'pri_123', // Fully refund this price...
    'pri_456' => 200, // Only partially refund this price...
]);
```



위의 예제는 거래에서 특정 항목을 환불합니다. 전체 거래를 환불하려면, 이유를 제공하기만 하면 됩니다:

```php
$response = $transaction->refund('Accidental charge');
```



환불에 대한 자세한 정보는 [Paddle의 환불 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참조하십시오.

> [!WARNING]
> 환불은 전액 처리되기 전에 항상 Paddle의 승인을 받아야 합니다.

<a name="crediting-transactions"></a>
### 거래 크레딧 처리

환불과 마찬가지로 거래를 크레딧 처리할 수도 있습니다. 거래를 크레딧 처리하면 고객의 잔액에 자금이 추가되어 미래 구매에 사용할 수 있습니다. 거래 크레딧 처리는 수동으로 수집된 거래에만 가능하며 자동으로 수집된 거래(예: 구독)에는 적용되지 않습니다. 이유는 Paddle이 구독 크레딧을 자동으로 처리하기 때문입니다.

```php
$transaction = $user->transactions()->first();

// Credit a specific line item fully...
$response = $transaction->credit('Compensation', 'pri_123');
```



자세한 정보는 [Paddle의 크레딧 관련 문서](https://developer.paddle.com/build/transactions/create-transaction-adjustments)를 참조하세요.

> [!WARNING]
> 크레딧은 수동으로 수집된 거래에만 적용될 수 있습니다. 자동으로 수집된 거래는 Paddle이 직접 크레딧을 부여합니다.

<a name="transactions"></a>
## 거래

청구 가능한 모델의 거래 배열은 `transactions` 속성을 통해 쉽게 가져올 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$transactions = $user->transactions;
```



거래는 귀하의 제품 및 구매에 대한 지불을 나타내며 송장과 함께 제공됩니다. 완료된 거래만 귀하의 애플리케이션 데이터베이스에 저장됩니다.

고객의 거래를 나열할 때 거래 인스턴스의 메서드를 사용하여 관련 지불 정보를 표시할 수 있습니다. 예를 들어, 사용자가 모든 송장을 쉽게 다운로드할 수 있도록 모든 거래를 표에 나열할 수 있습니다:

```html
<table>
    @foreach ($transactions as $transaction)
        <tr>
            <td>{{ $transaction->billed_at->toFormattedDateString() }}</td>
            <td>{{ $transaction->total() }}</td>
            <td>{{ $transaction->tax() }}</td>
            <td><a href="{{ route('download-invoice', $transaction->id) }}" target="_blank">Download</a></td>
        </tr>
    @endforeach
</table>
```



`download-invoice` 경로는 다음과 같이 보일 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Paddle\Transaction;

Route::get('/download-invoice/{transaction}', function (Request $request, Transaction $transaction) {
    return $transaction->redirectToInvoicePdf();
})->name('download-invoice');
```



<a name="past-and-upcoming-payments"></a>
### 과거 및 예정된 결제

`lastPayment` 및 `nextPayment` 방법을 사용하여 반복 구독에 대한 고객의 과거 또는 예정된 결제를 조회하고 표시할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscription = $user->subscription();

$lastPayment = $subscription->lastPayment();
$nextPayment = $subscription->nextPayment();
```



이 두 방법 모두 `Laravel\Paddle\Payment` 인스턴스를 반환합니다. 그러나 `lastPayment`는 웹훅으로 트랜잭션이 아직 동기화되지 않았을 때 `null`를 반환하는 반면, `nextPayment`는 청구 주기가 종료되었을 때(예: 구독이 취소된 경우) `null`를 반환합니다:

```blade
Next payment: {{ $nextPayment->amount() }} due on {{ $nextPayment->date()->format('d/m/Y') }}
```

<a name="testing"></a>
## 테스트

테스트하는 동안에는 통합이 예상대로 작동하는지 확인하기 위해 결제 흐름을 수동으로 테스트해야 합니다.

CI 환경 내에서 실행되는 테스트를 포함한 자동화된 테스트의 경우, [Laravel의 HTTP 클라이언트](/docs/{{version}}/http-client#testing)를 사용하여 Paddle에 대한 HTTP 호출을 가짜로 만들 수 있습니다. 이것은 실제 Paddle의 응답을 테스트하지는 않지만, 실제로 Paddle의 API를 호출하지 않고도 애플리케이션을 테스트할 수 있는 방법을 제공합니다.
{% endraw %}
