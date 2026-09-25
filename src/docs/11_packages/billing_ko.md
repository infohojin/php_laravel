---
layout: docs
title: "라라벨 캐셔 (Stripe)"
---

{% raw %}
# 라라벨 캐셔 (Stripe)

- [Introduction](#introduction)
- [Upgrading Cashier](#upgrading-cashier)
- [Installation](#installation)
- [Configuration](#configuration)
    - [Billable Model](#billable-model)
    - [API Keys](#api-keys)
    - [Currency Configuration](#currency-configuration)
    - [Tax Configuration](#tax-configuration)
    - [Logging](#logging)
    - [Using Custom Models](#using-custom-models)
- [Quickstart](#quickstart)
    - [Selling Products](#quickstart-selling-products)
    - [Selling Subscriptions](#quickstart-selling-subscriptions)
- [Customers](#customers)
    - [Retrieving Customers](#retrieving-customers)
    - [Creating Customers](#creating-customers)
    - [Updating Customers](#updating-customers)
    - [Balances](#balances)
    - [Tax IDs](#tax-ids)
    - [Syncing Customer Data With Stripe](#syncing-customer-data-with-stripe)
    - [Billing Portal](#billing-portal)
- [Payment Methods](#payment-methods)
    - [Storing Payment Methods](#storing-payment-methods)
    - [Retrieving Payment Methods](#retrieving-payment-methods)
    - [Payment Method Presence](#payment-method-presence)
    - [Updating the Default Payment Method](#updating-the-default-payment-method)
    - [Adding Payment Methods](#adding-payment-methods)
    - [Deleting Payment Methods](#deleting-payment-methods)
- [Subscriptions](#subscriptions)
    - [Creating Subscriptions](#creating-subscriptions)
    - [Checking Subscription Status](#checking-subscription-status)
    - [Changing Prices](#changing-prices)
    - [Subscription Quantity](#subscription-quantity)
    - [Subscriptions With Multiple Products](#subscriptions-with-multiple-products)
    - [Multiple Subscriptions](#multiple-subscriptions)
    - [Usage Based Billing](#usage-based-billing)
    - [Subscription Taxes](#subscription-taxes)
    - [Subscription Anchor Date](#subscription-anchor-date)
    - [Canceling Subscriptions](#cancelling-subscriptions)
    - [Resuming Subscriptions](#resuming-subscriptions)
- [Subscription Trials](#subscription-trials)
    - [With Payment Method Up Front](#with-payment-method-up-front)
    - [Without Payment Method Up Front](#without-payment-method-up-front)
    - [Extending Trials](#extending-trials)
- [Handling Stripe Webhooks](#handling-stripe-webhooks)
    - [Defining Webhook Event Handlers](#defining-webhook-event-handlers)
    - [Verifying Webhook Signatures](#verifying-webhook-signatures)
- [Single Charges](#single-charges)
    - [Simple Charge](#simple-charge)
    - [Charge With Invoice](#charge-with-invoice)
    - [Creating Payment Intents](#creating-payment-intents)
    - [Refunding Charges](#refunding-charges)
- [Invoices](#invoices)
    - [Retrieving Invoices](#retrieving-invoices)
    - [Upcoming Invoices](#upcoming-invoices)
    - [Previewing Subscription Invoices](#previewing-subscription-invoices)
    - [Generating Invoice PDFs](#generating-invoice-pdfs)
- [Checkout](#checkout)
    - [Product Checkouts](#product-checkouts)
    - [Single Charge Checkouts](#single-charge-checkouts)
    - [Subscription Checkouts](#subscription-checkouts)
    - [Collecting Tax IDs](#collecting-tax-ids)
    - [Guest Checkouts](#guest-checkouts)
- [Handling Failed Payments](#handling-failed-payments)
    - [Confirming Payments](#confirming-payments)
- [Strong Customer Authentication (SCA)](#strong-customer-authentication)
    - [Payments Requiring Additional Confirmation](#payments-requiring-additional-confirmation)
    - [Off-session Payment Notifications](#off-session-payment-notifications)
- [Stripe SDK](#stripe-sdk)
- [Testing](#testing)



<a name="introduction"></a>
## 소개

[Laravel Cashier Stripe](https://github.com/laravel/cashier-stripe)는 [Stripe](https://stripe.com)의 구독 결제 서비스를 위한 표현적이고 유연한 인터페이스를 제공합니다. 이는 작성하기 귀찮은 대부분의 구독 결제 기본 코드를 처리합니다. 기본 구독 관리 외에도 Cashier는 쿠폰 처리, 구독 전환, 구독 "수량", 취소 유예 기간 관리 및 심지어 송장 PDF 생성까지 처리할 수 있습니다.

<a name="upgrading-cashier"></a>
## Cashier 업그레이드

새로운 버전의 Cashier로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/cashier-stripe/blob/16.x/UPGRADE.md)를 신중히 검토하는 것이 중요합니다.

> [!WARNING]
> 변경 사항 파괴를 방지하기 위해 Cashier는 고정된 Stripe API 버전을 사용합니다. Cashier 16은 Stripe API 버전 `2025-06-30.basil`를 사용합니다. Stripe API 버전은 새로운 Stripe 기능과 개선사항을 활용하기 위해 마이너 릴리스 시 업데이트됩니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 Stripe용 Cashier 패키지를 설치합니다:

```shell
composer require laravel/cashier
```



패키지를 설치한 후, `vendor:publish` Artisan 명령을 사용하여 Cashier의 마이그레이션을 게시하세요:

```shell
php artisan vendor:publish --tag="cashier-migrations"
```



그런 다음, 데이터베이스를 마이그레이션하세요:

```shell
php artisan migrate
```



캐셔의 마이그레이션은 `users` 테이블에 여러 열을 추가할 것입니다. 또한 모든 고객의 구독을 저장할 `subscriptions` 테이블과 여러 가격이 있는 구독을 위한 `subscription_items` 테이블을 생성할 것입니다.

원하신다면, `vendor:publish` Artisan 명령을 사용하여 캐셔의 구성 파일을 게시할 수도 있습니다:

```shell
php artisan vendor:publish --tag="cashier-config"
```



마지막으로, Cashier가 모든 Stripe 이벤트를 제대로 처리하도록 하려면 [Cashier의 웹훅 처리 설정](#handling-stripe-webhooks)을 수행하는 것을 기억하세요.

> [!WARNING]
> Stripe는 Stripe 식별자를 저장하는 데 사용되는 모든 열이 대소문자를 구분해야 한다고 권장합니다. 따라서 MySQL을 사용할 때 `stripe_id` 열의 컬레이션이 `utf8_bin`로 설정되어 있는지 확인해야 합니다. 자세한 내용은 [Stripe 문서](https://stripe.com/docs/upgrades#what-changes-does-stripe-consider-to-be-backwards-compatible)에서 확인할 수 있습니다.

<a name="configuration"></a>
## 구성

<a name="billable-model"></a>
### 결제 가능한 모델

Cashier를 사용하기 전에 결제 가능한 모델 정의에 `Billable` 트레이트를 추가하세요. 일반적으로 이는 `App\Models\User` 모델이 됩니다. 이 트레이트는 구독 생성, 쿠폰 적용, 결제 수단 정보 업데이트와 같은 일반적인 청구 작업을 수행할 수 있는 다양한 메서드를 제공합니다:

```php
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```



Cashier는 청구 가능한 모델이 Laravel과 함께 제공되는 `App\Models\User` 클래스일 것으로 가정합니다. 이를 변경하려면 `useCustomerModel` 메서드를 통해 다른 모델을 지정할 수 있습니다. 이 메서드는 일반적으로 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

```php
use App\Models\Cashier\User;
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useCustomerModel(User::class);
}
```



> [!WARNING]
> Laravel에서 제공하는 `App\Models\User` 모델이 아닌 다른 모델을 사용하는 경우, 제공된 [Cashier 마이그레이션](#installation)을 게시하고 대체 모델의 테이블 이름에 맞게 변경해야 합니다.

<a name="api-keys"></a>
### API 키

다음으로, 애플리케이션의 `.env` 파일에서 Stripe API 키를 구성해야 합니다. Stripe 제어판에서 Stripe API 키를 가져올 수 있습니다:

```ini
STRIPE_KEY=your-stripe-key
STRIPE_SECRET=your-stripe-secret
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
```



> [!WARNING]
> 이 변수는 들어오는 웹훅이 실제로 Stripe에서 온 것인지 확인하는 데 사용되므로, `STRIPE_WEBHOOK_SECRET` 환경 변수가 애플리케이션의 `.env` 파일에 정의되어 있는지 확인해야 합니다.

<a name="currency-configuration"></a>
### 통화 설정

기본 Cashier 통화는 미국 달러(USD)입니다. 애플리케이션의 `.env` 파일 내에서 `CASHIER_CURRENCY` 환경 변수를 설정하여 기본 통화를 변경할 수 있습니다:

```ini
CASHIER_CURRENCY=eur
```



현금 출납원의 통화를 설정하는 것 외에도, 송장에 표시할 금액을 서식화할 때 사용할 로케일을 지정할 수 있습니다. 내부적으로, 현금 출납원은 통화 로케일을 설정하기 위해 [PHP의 `NumberFormatter` 클래스](https://www.php.net/manual/en/class.numberformatter.php)를 사용합니다:

```ini
CASHIER_CURRENCY_LOCALE=nl_BE
```



> [!WARNING]
> `en` 이외의 로케일을 사용하려면, `ext-intl` PHP 확장 모듈이 서버에 설치되고 구성되어 있는지 확인하세요.

<a name="tax-configuration"></a>
### 세금 구성

[Stripe Tax](https://stripe.com/tax) 덕분에, Stripe에서 생성된 모든 청구서에 대해 자동으로 세금을 계산할 수 있습니다. 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `boot` 메서드 내에서 `calculateTaxes` 메서드를 호출하여 자동 세금 계산을 활성화할 수 있습니다:

```php
use Laravel\Cashier\Cashier;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::calculateTaxes();
}
```



세금 계산이 활성화되면, 생성되는 모든 신규 구독과 일회성 인보이스에 자동으로 세금 계산이 적용됩니다.

이 기능이 제대로 작동하려면 고객의 이름, 주소, 세금 ID와 같은 청구 세부 정보가 Stripe와 동기화되어 있어야 합니다. 이를 위해 Cashier에서 제공하는 [고객 데이터 동기화](#syncing-customer-data-with-stripe) 및 [세금 ID](#tax-ids) 방법을 사용할 수 있습니다.

<a name="logging"></a>
### 로깅

Cashier는 치명적인 Stripe 오류를 로깅할 때 사용할 로그 채널을 지정할 수 있습니다. 로그 채널은 애플리케이션의 `.env` 파일 내에서 `CASHIER_LOGGER` 환경 변수를 정의하여 지정할 수 있습니다.

```ini
CASHIER_LOGGER=stack
```



Stripe에 대한 API 호출로 생성된 예외는 애플리케이션의 기본 로그 채널을 통해 기록됩니다.

<a name="using-custom-models"></a>
### 사용자 정의 모델 사용

자신의 모델을 정의하고 해당 Cashier 모델을 확장하여 Cashier에서 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다:

```php
use Laravel\Cashier\Subscription as CashierSubscription;

class Subscription extends CashierSubscription
{
    // ...
}
```



모델을 정의한 후, `Laravel\Cashier\Cashier` 클래스를 통해 Cashier가 사용자 정의 모델을 사용하도록 지시할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스에 있는 `boot` 메서드에서 Cashier에게 사용자 정의 모델에 대해 알려야 합니다:

```php
use App\Models\Cashier\Subscription;
use App\Models\Cashier\SubscriptionItem;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Cashier::useSubscriptionModel(Subscription::class);
    Cashier::useSubscriptionItemModel(SubscriptionItem::class);
}
```



<a name="quickstart"></a>
## 빠른 시작

<a name="quickstart-selling-products"></a>
### 제품 판매

> [!NOTE]
> Stripe Checkout을 사용하기 전에 Stripe 대시보드에서 고정 가격이 있는 제품을 정의해야 합니다. 또한 [Cashier의 웹훅 처리 설정](#handling-stripe-webhooks)을 구성해야 합니다.

응용 프로그램을 통해 제품 및 구독 청구를 제공하는 것은 부담스러울 수 있습니다. 그러나 Cashier와 [Stripe Checkout](https://stripe.com/payments/checkout)을 사용하면 현대적이고 견고한 결제 통합을 쉽게 구축할 수 있습니다.

비반복적 단일 결제 제품에 대해 고객에게 요금을 청구하기 위해 Cashier를 사용하여 고객을 Stripe Checkout으로 안내하고, 고객은 결제 정보를 제공하고 구매를 확인하게 됩니다. 결제가 Checkout을 통해 완료되면 고객은 응용 프로그램 내에서 선택한 성공 URL로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/checkout', function (Request $request) {
    $stripePriceId = 'price_deluxe_album';

    $quantity = 1;

    return $request->user()->checkout([$stripePriceId => $quantity], [
        'success_url' => route('checkout-success'),
        'cancel_url' => route('checkout-cancel'),
    ]);
})->name('checkout');

Route::view('/checkout/success', 'checkout.success')->name('checkout-success');
Route::view('/checkout/cancel', 'checkout.cancel')->name('checkout-cancel');
```



As you can see in the example above, we will utilize Cashier's provided `checkout` method to redirect the customer to Stripe Checkout for a given "price identifier". When using Stripe, "prices" refer to [defined prices for specific products](https://stripe.com/docs/products-prices/how-products-and-prices-work).

If necessary, the `checkout` method will automatically create a customer in Stripe and connect that Stripe customer record to the corresponding user in your application's database. After completing the checkout session, the customer will be redirected to a dedicated success or cancellation page where you can display an informational message to the customer.

<a name="providing-meta-data-to-stripe-checkout"></a>
#### Providing Meta Data to Stripe Checkout

When selling products, it's common to keep track of completed orders and purchased products via `Cart` and `Order` models defined by your own application. When redirecting customers to Stripe Checkout to complete a purchase, you may need to provide an existing order identifier so that you can associate the completed purchase with the corresponding order when the customer is redirected back to your application.

To accomplish this, you may provide an array of `metadata` to the `checkout` method. Let's imagine that a pending `Order` is created within our application when a user begins the checkout process. Remember, the `Cart` and `Order` models in this example are illustrative and not provided by Cashier. You are free to implement these concepts based on the needs of your own application:

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

    return $request->user()->checkout($order->price_ids, [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
        'metadata' => ['order_id' => $order->id],
    ]);
})->name('checkout');
```



위의 예에서 볼 수 있듯이, 사용자가 결제 과정을 시작하면 우리는 모든 장바구니/주문과 관련된 Stripe 가격 식별자를 `checkout` 메서드에 제공합니다. 물론, 사용자가 항목을 추가할 때 이러한 항목을 '장바구니' 또는 주문과 연결하는 것은 귀하의 애플리케이션 책임입니다. 또한 주문 ID를 `metadata` 배열을 통해 Stripe Checkout 세션에 제공합니다. 마지막으로, 우리는 Checkout 성공 경로에 `CHECKOUT_SESSION_ID` 템플릿 변수를 추가했습니다. Stripe가 고객을 귀하의 애플리케이션으로 다시 리디렉션할 때, 이 템플릿 변수는 Checkout 세션 ID로 자동 채워집니다.

다음으로, Checkout 성공 경로를 구축해봅시다. 이 경로는 사용자가 Stripe Checkout을 통해 구매를 완료한 후 리디렉션될 경로입니다. 이 경로 내에서 Stripe Checkout 세션 ID와 관련된 Stripe Checkout 인스턴스를 가져와서 제공된 메타 데이터를 접근하고 고객의 주문을 적절히 업데이트할 수 있습니다.

```php
use App\Models\Order;
use Illuminate\Http\Request;
use Laravel\Cashier\Cashier;

Route::get('/checkout/success', function (Request $request) {
    $sessionId = $request->get('session_id');

    if ($sessionId === null) {
        return;
    }

    $session = Cashier::stripe()->checkout->sessions->retrieve($sessionId);

    if ($session->payment_status !== 'paid') {
        return;
    }

    $orderId = $session['metadata']['order_id'] ?? null;

    $order = Order::findOrFail($orderId);

    $order->update(['status' => 'completed']);

    return view('checkout-success', ['order' => $order]);
})->name('checkout-success');
```



Please refer to Stripe's documentation for more information on the [data contained by the Checkout session object](https://stripe.com/docs/api/checkout/sessions/object).

<a name="quickstart-selling-subscriptions"></a>
### Selling Subscriptions

> [!NOTE]
> Before utilizing Stripe Checkout, you should define Products with fixed prices in your Stripe dashboard. In addition, you should [configure Cashier's webhook handling](#handling-stripe-webhooks).

Offering product and subscription billing via your application can be intimidating. However, thanks to Cashier and [Stripe Checkout](https://stripe.com/payments/checkout), you can easily build modern, robust payment integrations.

To learn how to sell subscriptions using Cashier and Stripe Checkout, let's consider the simple scenario of a subscription service with a basic monthly (`price_basic_monthly`) and yearly (`price_basic_yearly`) plan. These two prices could be grouped under a "Basic" product (`pro_basic`) in our Stripe dashboard. In addition, our subscription service might offer an Expert plan as `pro_expert`.

First, let's discover how a customer can subscribe to our services. Of course, you can imagine the customer might click a "subscribe" button for the Basic plan on our application's pricing page. This button or link should direct the user to a Laravel route which creates the Stripe Checkout session for their chosen plan:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_basic_monthly')
        ->trialDays(5)
        ->allowPromotionCodes()
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```



위의 예에서 볼 수 있듯이, 우리는 고객을 Stripe Checkout 세션으로 리디렉션하여 Basic 요금제에 가입할 수 있도록 할 것입니다. 결제가 성공적으로 완료되거나 취소된 후, 고객은 우리가 `checkout` 메서드에 제공한 URL로 다시 리디렉션됩니다. 일부 결제 수단은 처리하는 데 몇 초가 걸리므로 실제로 구독이 시작되었는지 확인하려면 [Cashier의 웹훅 처리 설정](#handling-stripe-webhooks)도 필요합니다.

이제 고객이 구독을 시작할 수 있으므로, 구독한 사용자만 접근할 수 있도록 애플리케이션의 특정 부분을 제한해야 합니다. 물론, Cashier의 `Billable` 트레이트가 제공하는 `subscribed` 메서드를 통해 사용자의 현재 구독 상태를 항상 확인할 수 있습니다.

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
            return redirect('/billing');
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
#### 고객이 청구 요금제를 관리할 수 있도록 허용

물론, 고객은 자신의 구독 요금제를 다른 상품이나 '등급'으로 변경하고 싶어할 수 있습니다. 이를 허용하는 가장 쉬운 방법은 고객에게 Stripe의 [고객 청구 포털](https://stripe.com/docs/no-code/customer-portal)로 안내하는 것입니다. 이 포털은 고객이 청구서를 다운로드하고, 결제 수단을 업데이트하며, 구독 요금제를 변경할 수 있는 호스팅된 사용자 인터페이스를 제공합니다.

먼저 애플리케이션 내에서 사용자를 Laravel 라우트로 안내하는 링크나 버튼을 정의하십시오. 이를 통해 우리는 청구 포털 세션을 시작할 것입니다:

```blade
<a href="{{ route('billing') }}">
    Billing
</a>
```



다음으로, Stripe 고객 청구 포털 세션을 시작하고 사용자를 포털로 리디렉션하는 경로를 정의해 보겠습니다. `redirectToBillingPortal` 메서드는 사용자가 포털을 나갈 때 돌아가야 할 URL을 받습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware(['auth'])->name('billing');
```



> [!NOTE]
> 캐셔의 웹훅 처리를 설정한 경우, 캐셔는 Stripe로부터 들어오는 웹훅을 검사하여 애플리케이션의 캐셔 관련 데이터베이스 테이블을 자동으로 동기화합니다. 예를 들어, 사용자가 Stripe의 고객 청구 포털을 통해 구독을 취소하면, 캐셔는 해당 웹훅을 수신하고 애플리케이션의 데이터베이스에서 구독을 "취소됨"으로 표시합니다.

<a name="customers"></a>
## 고객

<a name="retrieving-customers"></a>
### 고객 조회

Stripe ID를 사용하여 고객을 `Cashier::findBillable` 메서드로 조회할 수 있습니다. 이 메서드는 청구 가능한 모델의 인스턴스를 반환합니다:

```php
use Laravel\Cashier\Cashier;

$user = Cashier::findBillable($stripeId);
```



<a name="creating-customers"></a>
### 고객 생성

가끔은 구독을 시작하지 않고 Stripe 고객을 생성하고 싶을 수 있습니다. `createAsStripeCustomer` 방법을 사용하여 이를 수행할 수 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer();
```



고객이 Stripe에 생성되면 나중에 구독을 시작할 수 있습니다. Stripe API에서 지원되는 추가 [고객 생성 매개변수](https://stripe.com/docs/api/customers/create)를 전달하기 위해 선택적으로 `$options` 배열을 제공할 수 있습니다:

```php
$stripeCustomer = $user->createAsStripeCustomer($options);
```



청구 가능한 모델에 대한 Stripe 고객 객체를 반환하려면 `asStripeCustomer` 방법을 사용할 수 있습니다:

```php
$stripeCustomer = $user->asStripeCustomer();
```



청구 가능한 모델에 대한 Stripe 고객 객체를 가져오고 싶지만 해당 청구 가능한 모델이 이미 Stripe 내에 고객인지 확실하지 않은 경우 `createOrGetStripeCustomer` 메서드를 사용할 수 있습니다. 이 메서드는 고객이 아직 존재하지 않는 경우 Stripe에 새 고객을 생성합니다:

```php
$stripeCustomer = $user->createOrGetStripeCustomer();
```



<a name="updating-customers"></a>
### 고객 업데이트

때때로 Stripe 고객에게 추가 정보를 직접 업데이트하고 싶을 수 있습니다. 이는 `updateStripeCustomer` 메서드를 사용하여 수행할 수 있습니다. 이 메서드는 [Stripe API에서 지원하는 고객 업데이트 옵션](https://stripe.com/docs/api/customers/update)의 배열을 허용합니다.

```php
$stripeCustomer = $user->updateStripeCustomer($options);
```



<a name="balances"></a>
### 잔액

Stripe를 사용하면 고객의 "잔액"을 입금하거나 출금할 수 있습니다. 나중에 이 잔액은 새 청구서에서 입금되거나 출금됩니다. 고객의 총 잔액을 확인하려면 청구 가능 모델에서 사용할 수 있는 `balance` 메서드를 사용할 수 있습니다. `balance` 메서드는 고객 통화로 형식화된 잔액 문자열 표현을 반환합니다:

```php
$balance = $user->balance();
```



고객의 잔액을 입금하려면 `creditBalance` 메서드에 값을 제공할 수 있습니다. 원하신다면 설명도 제공할 수 있습니다:

```php
$user->creditBalance(500, 'Premium customer top-up.');
```



`debitBalance` 메서드에 값을 제공하면 고객의 잔액이 차감됩니다:

```php
$user->debitBalance(300, 'Bad usage penalty.');
```



`applyBalance` 메서드는 고객을 위한 새로운 고객 잔액 거래를 생성합니다. 이러한 거래 기록은 `balanceTransactions` 메서드를 사용하여 가져올 수 있으며, 고객이 검토할 수 있는 신용 및 차변 내역 로그를 제공하는 데 유용할 수 있습니다:

```php
// Retrieve all transactions...
$transactions = $user->balanceTransactions();

foreach ($transactions as $transaction) {
    // Transaction amount...
    $amount = $transaction->amount(); // $2.31

    // Retrieve the related invoice when available...
    $invoice = $transaction->invoice();
}
```



<a name="tax-ids"></a>
### 세금 ID

카시어는 고객의 세금 ID를 쉽게 관리할 수 있는 방법을 제공합니다. 예를 들어, `taxIds` 메서드를 사용하여 고객에게 할당된 모든 [세금 ID](https://stripe.com/docs/api/customer_tax_ids/object)를 컬렉션으로 가져올 수 있습니다:

```php
$taxIds = $user->taxIds();
```



식별자를 통해 고객의 특정 세금 ID를 조회할 수도 있습니다:

```php
$taxId = $user->findTaxId('txi_belgium');
```



유효한 [type](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-type)과 값을 `createTaxId` 메서드에 제공하여 새 세금 ID를 생성할 수 있습니다:

```php
$taxId = $user->createTaxId('eu_vat', 'BE0123456789');
```



`createTaxId` 메서드는 고객 계정에 VAT ID를 즉시 추가합니다. [VAT ID 확인은 Stripe에서도 수행됩니다](https://stripe.com/docs/invoicing/customer/tax-ids#validation); 그러나 이 과정은 비동기적으로 진행됩니다. `customer.tax_id.updated` 웹훅 이벤트를 구독하고 [VAT ID `verification` 매개변수](https://stripe.com/docs/api/customer_tax_ids/object#tax_id_object-verification)를 확인하면 확인 업데이트에 대한 알림을 받을 수 있습니다. 웹훅 처리 방법에 대한 자세한 내용은 [웹훅 핸들러 정의 문서](#handling-stripe-webhooks)를 참조하십시오.

`deleteTaxId` 메서드를 사용하여 세금 ID를 삭제할 수 있습니다:

```php
$user->deleteTaxId('txi_belgium');
```



<a name="syncing-customer-data-with-stripe"></a>
### Stripe와 고객 데이터 동기화

일반적으로, 애플리케이션 사용자가 이름, 이메일 주소 또는 Stripe에 저장된 다른 정보를 업데이트할 때, 해당 업데이트를 Stripe에 알려야 합니다. 이렇게 하면 Stripe의 정보 복사본이 애플리케이션의 정보와 동기화됩니다.

이를 자동화하려면, 청구 가능한 모델에서 모델의 `updated` 이벤트에 반응하는 이벤트 리스너를 정의할 수 있습니다. 그런 다음 이벤트 리스너 내에서 모델의 `syncStripeCustomerDetails` 메서드를 호출할 수 있습니다:

```php
use App\Models\User;
use function Illuminate\Events\queueable;

/**
 * The "booted" method of the model.
 */
protected static function booted(): void
{
    static::updated(queueable(function (User $customer) {
        if ($customer->hasStripeId()) {
            $customer->syncStripeCustomerDetails();
        }
    }));
}
```



이제 고객 모델이 업데이트될 때마다 해당 정보가 Stripe와 동기화됩니다. 편의를 위해, Cashier는 고객이 처음 생성될 때 고객 정보를 자동으로 Stripe와 동기화합니다.

Cashier에서 제공하는 다양한 메서드를 재정의하여 Stripe로 고객 정보를 동기화할 때 사용되는 열을 사용자 정의할 수 있습니다. 예를 들어, `stripeName` 메서드를 재정의하여 Cashier가 고객 정보를 Stripe에 동기화할 때 고려해야 할 고객의 "이름" 속성을 사용자 정의할 수 있습니다:

```php
/**
 * Get the customer name that should be synced to Stripe.
 */
public function stripeName(): string|null
{
    return $this->company_name;
}
```



마찬가지로, `stripeEmail`, `stripePhone`(최대 20자), `stripeAddress`, `stripePreferredLocales` 메서드를 재정의할 수 있습니다. 이 메서드들은 [Stripe 고객 객체 업데이트](https://stripe.com/docs/api/customers/update) 시 해당 고객 파라미터와 정보를 동기화합니다. 고객 정보 동기화 과정을 완전히 제어하고 싶다면, `syncStripeCustomerDetails` 메서드를 재정의할 수 있습니다.

<a name="billing-portal"></a>
### 청구 포털

Stripe는 [고객이 구독, 결제 수단을 관리하고 청구 내역을 확인할 수 있는 청구 포털을 쉽게 설정하는 방법](https://stripe.com/docs/billing/subscriptions/customer-portal)을 제공합니다. 사용자를 컨트롤러나 라우트에서 청구 가능한 모델의 `redirectToBillingPortal` 메서드를 호출하여 청구 포털로 리디렉션할 수 있습니다.

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal();
});
```



기본적으로 사용자가 구독 관리를 마치면 Stripe 청구 포털 내의 링크를 통해 애플리케이션의 `home` 경로로 돌아갈 수 있습니다. 사용자가 돌아가야 할 맞춤 URL을 `redirectToBillingPortal` 메서드에 URL을 인수로 전달하여 제공할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/billing-portal', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('billing'));
});
```



HTTP 리디렉션 응답을 생성하지 않고 결제 포털로 가는 URL을 생성하려면 `billingPortalUrl` 메서드를 호출할 수 있습니다:

```php
$url = $request->user()->billingPortalUrl(route('billing'));
```



<a name="payment-methods"></a>
## 결제 방법

<a name="storing-payment-methods"></a>
### 결제 방법 저장

Stripe로 구독을 생성하거나 '일회성' 결제를 수행하려면, 애플리케이션이 고객으로부터 결제 정보를 안전하게 수집해야 합니다. 이 작업을 수행하는 방식은 결제 수단을 미래 구독을 위해 저장할지 아니면 즉시 단일 결제를 처리할지에 따라 다르므로, 아래에서 둘 다 살펴보겠습니다.

Stripe의 [결제 요소](https://stripe.com/docs/payments/payment-element)는 카드, Apple Pay, Google Pay, iDEAL과 같은 여러 결제 수단을 지원하는 데 사용할 수 있습니다.

<a name="payment-element-for-subscriptions"></a>
#### 구독을 위한 결제 요소

먼저, 설정 의도를 생성하고 이를 뷰에 전달하십시오:

```php
return view('subscribe', [
    'intent' => $user->createSetupIntent()
]);
```



Setup Intent의 `client_secret`를 사용하여 결제 요소를 장착하세요:

```html
<div id="payment-element"></div>
<button id="submit">Subscribe</button>

<script src="https://js.stripe.com/v3/"></script>
<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements({
        clientSecret: '{{ $intent->client_secret }}'
    });

    const paymentElement = elements.create('payment');

    paymentElement.mount('#payment-element');

    document.getElementById('submit').addEventListener('click', async () => {
        const { error } = await stripe.confirmSetup({
            elements,
            confirmParams: {
                return_url: '{{ route("subscription.complete") }}',
            },
        });

        if (error) {
            // Display "error.message" to the user...
        }
    });
</script>
```



스트라이프가 귀하의 `return_url`로 리디렉션한 후, `setup_intent` ID는 쿼리 문자열 매개변수로 사용 가능하게 됩니다. 이 값을 사용하여 결제 수단을 가져오고 구독을 생성할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription/complete', function (Request $request) {
    $setupIntent = $request->user()->findSetupIntent(
        $request->setup_intent
    );

    $paymentMethod = $setupIntent->payment_method;

    $request->user()
        ->newSubscription('default', 'price_xxx')
        ->create($paymentMethod);

    return redirect('/dashboard');
})->name('subscription.complete');
```



결제를 생성하는 대신 고객의 기본 결제 수단을 업데이트하기 위해 결제 요소(Payment Element)를 사용하는 경우, 결제 수단 식별자를 [`updateDefaultPaymentMethod`](#updating-the-default-payment-method) 메서드에 전달할 수 있습니다.

<a name="payment-element-for-single-charges"></a>
#### 단일 결제를 위한 결제 요소

일회성 결제의 경우, Cashier의 `pay` 메서드를 사용하여 결제 인텐트(Payment Intent)를 생성하십시오. 일반적으로 Stripe가 고객을 귀하의 애플리케이션으로 다시 리디렉션한 후 주문을 조회할 수 있도록, 애플리케이션의 해당 주문에 결제 인텐트 ID를 저장하는 것이 좋습니다. 다음 예시는 귀하의 애플리케이션에 `Order` 모델이 `user_id`, `amount`, `status` 및 `stripe_payment_intent_id` 열과 함께 존재한다고 가정합니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $amount = 1000;

    $payment = $request->user()->pay($amount);

    $order = Order::create([
        'user_id' => $request->user()->id,
        'amount' => $amount,
        'status' => 'pending',
        'stripe_payment_intent_id' => $payment->id,
    ]);

    return view('checkout', [
        'clientSecret' => $payment->client_secret,
        'order' => $order,
    ]);
});
```



그런 다음, 결제 요소를 마운트하고 결제를 확인하세요:

```html
<div id="payment-element"></div>
<button id="submit">Pay Now</button>

<script src="https://js.stripe.com/v3/"></script>
<script>
    const stripe = Stripe('stripe-public-key');

    const elements = stripe.elements({
        clientSecret: '{{ $clientSecret }}'
    });

    const paymentElement = elements.create('payment');

    paymentElement.mount('#payment-element');

    document.getElementById('submit').addEventListener('click', async () => {
        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: '{{ route("payment.complete") }}',
            },
        });

        if (error) {
            // Display "error.message" to the user...
        }
    });
</script>
```



리디렉션 후에 `payment_intent` 쿼리 문자열 매개변수를 사용하여 해당 주문과 결제 의도를 조회할 수 있습니다. 주문을 이행하기 전에 해당 주문이 인증된 고객에게 속하는지, 결제 의도가 인증된 고객에게 속하며 성공했는지 확인해야 합니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/payment/complete', function (Request $request) {
    $order = Order::where('user_id', $request->user()->id)
        ->where('stripe_payment_intent_id', $request->payment_intent)
        ->firstOrFail();

    $paymentIntent = $request->user()
        ->stripe()
        ->paymentIntents
        ->retrieve($request->payment_intent);

    if ($paymentIntent->customer === $request->user()->stripe_id &&
        $paymentIntent->status === 'succeeded') {
        $order->update(['status' => 'paid']);

        // Fulfill the order...
    }

    return redirect('/dashboard');
})->name('payment.complete');
```



<a name="retrieving-payment-methods"></a>
### 결제 수단 가져오기

청구 모델 인스턴스의 `paymentMethods` 메서드는 `Laravel\Cashier\PaymentMethod` 인스턴스의 컬렉션을 반환합니다:

```php
$paymentMethods = $user->paymentMethods();
```



기본적으로, 이 메서드는 모든 유형의 결제 수단을 반환합니다. 특정 유형의 결제 수단을 가져오려면 메서드에 `type`를 인수로 전달할 수 있습니다:

```php
$paymentMethods = $user->paymentMethods('sepa_debit');
```



고객의 기본 결제 수단을 조회하려면 `defaultPaymentMethod` 메서드를 사용할 수 있습니다:

```php
$paymentMethod = $user->defaultPaymentMethod();
```



`findPaymentMethod` 메서드를 사용하여 청구 가능 모델에 연결된 특정 결제 수단을 검색할 수 있습니다:

```php
$paymentMethod = $user->findPaymentMethod($paymentMethodId);
```



<a name="payment-method-presence"></a>
### 결제 수단 존재 여부

청구 가능한 모델 계정에 기본 결제 수단이 연결되어 있는지 확인하려면, `hasDefaultPaymentMethod` 메서드를 호출하십시오:

```php
if ($user->hasDefaultPaymentMethod()) {
    // ...
}
```



청구 가능한 모델의 계정에 최소한 하나의 결제 수단이 연결되어 있는지 확인하려면 `hasPaymentMethod` 방법을 사용할 수 있습니다:

```php
if ($user->hasPaymentMethod()) {
    // ...
}
```



이 메서드는 청구 가능한 모델에 결제 수단이 전혀 있는지 여부를 결정합니다. 모델에 특정 유형의 결제 수단이 존재하는지 확인하려면 `type`를 메서드의 인수로 전달할 수 있습니다:

```php
if ($user->hasPaymentMethod('sepa_debit')) {
    // ...
}
```



<a name="updating-the-default-payment-method"></a>
### 기본 결제 수단 업데이트

`updateDefaultPaymentMethod` 메서드는 고객의 기본 결제 수단 정보를 업데이트하는 데 사용할 수 있습니다. 이 메서드는 Stripe 결제 수단 식별자를 받아 새로운 결제 수단을 기본 청구 결제 수단으로 지정합니다:

```php
$user->updateDefaultPaymentMethod($paymentMethod);
```



Stripe에서 고객의 기본 결제 수단 정보와 기본 결제 수단 정보를 동기화하려면 `updateDefaultPaymentMethodFromStripe` 메서드를 사용할 수 있습니다:

```php
$user->updateDefaultPaymentMethodFromStripe();
```



> [!WARNING]
> 고객의 기본 결제 수단은 청구서 발행 및 새로운 구독 생성에만 사용할 수 있습니다. Stripe에서 부과한 제한으로 인해 단일 결제에는 사용할 수 없습니다.

<a name="adding-payment-methods"></a>
### 결제 수단 추가

새 결제 수단을 추가하려면 결제 가능 모델에서 `addPaymentMethod` 메서드를 호출하고 결제 수단 식별자를 전달하면 됩니다:

```php
$user->addPaymentMethod($paymentMethod);
```



> [!NOTE]
> 결제 수단 식별자를 가져오는 방법을 배우려면 [결제 수단 저장 문서](#storing-payment-methods)를 참조하십시오.

<a name="deleting-payment-methods"></a>
### 결제 수단 삭제

결제 수단을 삭제하려면 삭제하려는 `Laravel\Cashier\PaymentMethod` 인스턴스에서 `delete` 메서드를 호출할 수 있습니다:

```php
$paymentMethod->delete();
```



`deletePaymentMethod` 방법은 청구 가능한 모델에서 특정 결제 수단을 삭제합니다:

```php
$user->deletePaymentMethod('pm_visa');
```



`deletePaymentMethods` 방법은 청구 가능한 모델의 모든 결제 수단 정보를 삭제합니다:

```php
$user->deletePaymentMethods();
```



기본적으로 이 메서드는 모든 유형의 결제 수단을 삭제합니다. 특정 유형의 결제 수단을 삭제하려면 메서드에 `type`를 인수로 전달할 수 있습니다:

```php
$user->deletePaymentMethods('sepa_debit');
```



> [!WARNING]
> 사용자가 활성 구독을 가지고 있는 경우, 애플리케이션은 사용자가 기본 결제 수단을 삭제하지 못하게 해야 합니다.

<a name="subscriptions"></a>
## 구독

구독은 고객에 대한 반복 결제를 설정하는 방법을 제공합니다. Cashier로 관리되는 Stripe 구독은 여러 구독 가격, 구독 수량, 체험판 등을 지원합니다.

<a name="creating-subscriptions"></a>
### 구독 생성

구독을 생성하려면 먼저 일반적으로 `App\Models\User`의 인스턴스일 청구 가능한 모델의 인스턴스를 가져옵니다. 모델 인스턴스를 가져온 후, `newSubscription` 메서드를 사용하여 모델의 구독을 생성할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription(
        'default', 'price_monthly'
    )->create($request->paymentMethodId);

    // ...
});
```



The first argument passed to the `newSubscription` method should be the internal type of the subscription. If your application only offers a single subscription, you might call this `default` or `primary`. This subscription type is only for internal application usage and is not meant to be shown to users. In addition, it should not contain spaces and it should never be changed after creating the subscription. The second argument is the specific price the user is subscribing to. This value should correspond to the price's identifier in Stripe.

The `create` method, which accepts [a Stripe payment method identifier](#storing-payment-methods) or Stripe `PaymentMethod` object, will begin the subscription as well as update your database with the billable model's Stripe customer ID and other relevant billing information.

> [!WARNING]
> Passing a payment method identifier directly to the `create` subscription method will also automatically add it to the user's stored payment methods.

<a name="collecting-recurring-payments-via-invoice-emails"></a>
#### Collecting Recurring Payments via Invoice Emails

Instead of collecting a customer's recurring payments automatically, you may instruct Stripe to email an invoice to the customer each time their recurring payment is due. Then, the customer may manually pay the invoice once they receive it. The customer does not need to provide a payment method up front when collecting recurring payments via invoices:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice();
```



고객이 구독이 취소되기 전에 송장 대금을 지불할 수 있는 기간은 `days_until_due` 옵션에 의해 결정됩니다. 기본값은 30일이지만, 원하신다면 이 옵션에 대해 특정 값을 제공할 수 있습니다:

```php
$user->newSubscription('default', 'price_monthly')->createAndSendInvoice([], [
    'days_until_due' => 30
]);
```



<a name="subscription-quantities"></a>
#### 수량

구독을 생성할 때 가격에 대한 특정 [수량](https://stripe.com/docs/billing/subscriptions/quantities)을 설정하고 싶다면, 구독을 생성하기 전에 구독 빌더에서 `quantity` 메서드를 호출해야 합니다:

```php
$user->newSubscription('default', 'price_monthly')
    ->quantity(5)
    ->create($paymentMethod);
```



<a name="additional-details"></a>
#### 추가 세부 사항

Stripe에서 지원하는 추가 [고객](https://stripe.com/docs/api/customers/create) 또는 [구독](https://stripe.com/docs/api/subscriptions/create) 옵션을 지정하려면, `create` 메서드의 두 번째 및 세 번째 인수로 전달하면 됩니다:

```php
$user->newSubscription('default', 'price_monthly')->create($paymentMethod, [
    'email' => $email,
], [
    'metadata' => ['note' => 'Some extra information.'],
]);
```



<a name="coupons"></a>
#### 쿠폰

구독을 생성할 때 쿠폰을 적용하고 싶다면, `withCoupon` 방법을 사용할 수 있습니다:

```php
$user->newSubscription('default', 'price_monthly')
    ->withCoupon('code')
    ->create($paymentMethod);
```



또는 [Stripe 프로모션 코드](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 적용하고 싶다면, `withPromotionCode` 방법을 사용할 수 있습니다:

```php
$user->newSubscription('default', 'price_monthly')
    ->withPromotionCode('promo_code_id')
    ->create($paymentMethod);
```



주어진 프로모션 코드 ID는 프로모션 코드에 할당된 Stripe API ID여야 하며, 고객이 보는 프로모션 코드가 아니어야 합니다. 고객이 보는 프로모션 코드를 기반으로 프로모션 코드 ID를 찾아야 하는 경우, `findPromotionCode` 방법을 사용할 수 있습니다:

```php
// Find a promotion code ID by its customer facing code...
$promotionCode = $user->findPromotionCode('SUMMERSALE');

// Find an active promotion code ID by its customer facing code...
$promotionCode = $user->findActivePromotionCode('SUMMERSALE');
```



위의 예제에서 반환된 `$promotionCode` 객체는 `Laravel\Cashier\PromotionCode`의 인스턴스입니다. 이 클래스는 기본 `Stripe\PromotionCode` 객체를 장식합니다. `coupon` 메서드를 호출하여 프로모션 코드와 관련된 쿠폰을 가져올 수 있습니다:

```php
$coupon = $user->findPromotionCode('SUMMERSALE')->coupon();
```



쿠폰 인스턴스를 통해 할인 금액과 쿠폰이 고정 할인인지 또는 비율 기반 할인인지를 결정할 수 있습니다:

```php
if ($coupon->isPercentage()) {
    return $coupon->percentOff().'%'; // 21.5%
} else {
    return $coupon->amountOff(); // $5.99
}
```



현재 고객이나 구독에 적용된 할인도 조회할 수 있습니다:

```php
$discount = $billable->discount();

$discount = $subscription->discount();
```



반환된 `Laravel\Cashier\Discount` 인스턴스는 기본 `Stripe\Discount` 객체 인스턴스를 장식합니다. 이 할인을 관련된 쿠폰을 `coupon` 메서드를 호출하여 가져올 수 있습니다:

```php
$coupon = $subscription->discount()->coupon();
```



고객이나 구독에 새 쿠폰 또는 프로모션 코드를 적용하려면 `applyCoupon` 또는 `applyPromotionCode` 메소드를 통해 할 수 있습니다:

```php
$billable->applyCoupon('coupon_id');
$billable->applyPromotionCode('promotion_code_id');

$subscription->applyCoupon('coupon_id');
$subscription->applyPromotionCode('promotion_code_id');
```



기억하세요, 고객에게 보여지는 프로모션 코드가 아닌 프로모션 코드에 할당된 Stripe API ID를 사용해야 합니다. 한 번에 한 명의 고객이나 구독에 대해 하나의 쿠폰 또는 프로모션 코드만 적용할 수 있습니다.

이 주제에 대한 자세한 정보는 Stripe 문서에서 [쿠폰](https://stripe.com/docs/billing/subscriptions/coupons)과 [프로모션 코드](https://stripe.com/docs/billing/subscriptions/coupons/codes)를 참조하세요.

<a name="adding-subscriptions"></a>
#### 구독 추가하기

이미 기본 결제 수단을 가진 고객에게 구독을 추가하려면 구독 빌더에서 `add` 메서드를 호출할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->add();
```



<a name="creating-subscriptions-from-the-stripe-dashboard"></a>
#### Creating Subscriptions From the Stripe Dashboard

You may also create subscriptions from the Stripe dashboard itself. When doing so, Cashier will sync newly added subscriptions and assign them a type of `default`. To customize the subscription type that is assigned to dashboard created subscriptions, [define webhook event handlers](#defining-webhook-event-handlers).

In addition, you may only create one type of subscription via the Stripe dashboard. If your application offers multiple subscriptions that use different types, only one type of subscription may be added through the Stripe dashboard.

Finally, you should always make sure to only add one active subscription per type of subscription offered by your application. If a customer has two `default` subscriptions, only the most recently added subscription will be used by Cashier even though both would be synced with your application's database.

<a name="checking-subscription-status"></a>
### Checking Subscription Status

Once a customer is subscribed to your application, you may easily check their subscription status using a variety of convenient methods. First, the `subscribed` method returns `true` if the customer has an active subscription, even if the subscription is currently within its trial period. The `subscribed` method accepts the type of the subscription as its first argument:

```php
if ($user->subscribed('default')) {
    // ...
}
```



`subscribed` 방법은 또한 [라우트 미들웨어](/docs/{{version}}/middleware)로 훌륭한 후보가 되어, 사용자의 구독 상태에 따라 라우트와 컨트롤러에 대한 접근을 필터링할 수 있습니다:

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
        if ($request->user() && ! $request->user()->subscribed('default')) {
            // This user is not a paying customer...
            return redirect('/billing');
        }

        return $next($request);
    }
}
```



사용자가 아직 체험 기간에 있는지 확인하고 싶다면 `onTrial` 방법을 사용할 수 있습니다. 이 방법은 사용자가 여전히 체험 기간에 있음을 경고해야 할지 결정하는 데 유용할 수 있습니다:

```php
if ($user->subscription('default')->onTrial()) {
    // ...
}
```



`subscribedToProduct` 방법은 주어진 Stripe 제품의 식별자를 기반으로 사용자가 특정 제품을 구독했는지 여부를 확인하는 데 사용할 수 있습니다. Stripe에서 제품은 가격 모음입니다. 이 예제에서는 사용자의 `default` 구독이 애플리케이션의 "프리미엄" 제품에 활발히 구독되어 있는지 확인합니다. 주어진 Stripe 제품 식별자는 Stripe 대시보드에서 귀하의 제품 식별자 중 하나에 해당해야 합니다:

```php
if ($user->subscribedToProduct('prod_premium', 'default')) {
    // ...
}
```



`subscribedToProduct` 메서드에 배열을 전달함으로써 사용자의 `default` 구독이 애플리케이션의 '기본' 또는 '프리미엄' 상품에 적극적으로 가입되어 있는지 확인할 수 있습니다:

```php
if ($user->subscribedToProduct(['prod_basic', 'prod_premium'], 'default')) {
    // ...
}
```



`subscribedToPrice` 방법은 고객의 구독이 특정 가격 ID에 해당하는지 확인하는 데 사용될 수 있습니다:

```php
if ($user->subscribedToPrice('price_basic_monthly', 'default')) {
    // ...
}
```



`recurring` 방법은 사용자가 현재 구독 중인지, 더 이상 체험 기간에 속하지 않는지를 확인하는 데 사용할 수 있습니다:

```php
if ($user->subscription('default')->recurring()) {
    // ...
}
```



> [!WARNING]
> 사용자가 동일한 유형의 구독을 두 개 가지고 있는 경우, 가장 최근 구독은 항상 `subscription` 메서드에 의해 반환됩니다. 예를 들어, 사용자가 `default` 유형의 구독 기록을 두 개 가지고 있을 수 있습니다. 그러나 한 구독은 오래된 만료된 구독일 수 있고, 다른 구독은 현재 활성 구독일 수 있습니다. 가장 최근 구독은 항상 반환되며, 오래된 구독은 역사적 검토를 위해 데이터베이스에 보관됩니다.

<a name="cancelled-subscription-status"></a>
#### 취소된 구독 상태

사용자가 한때 활성 구독자였으나 구독을 취소했는지 확인하려면, `canceled` 메서드를 사용할 수 있습니다:

```php
if ($user->subscription('default')->canceled()) {
    // ...
}
```



사용자가 구독을 취소했지만 구독이 완전히 만료되기 전까지 여전히 '유예 기간(grace period)'에 있는지 여부도 확인할 수 있습니다. 예를 들어, 사용자가 원래 3월 10일에 만료될 예정이었던 구독을 3월 5일에 취소한 경우, 사용자는 3월 10일까지 '유예 기간'에 있습니다. 이 동안에도 `subscribed` 메서드는 여전히 `true`를 반환한다는 점에 유의하세요:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```



사용자가 구독을 취소했는지, 그리고 더 이상 '유예 기간'에 있지 않은지를 확인하려면, `ended` 방법을 사용할 수 있습니다:

```php
if ($user->subscription('default')->ended()) {
    // ...
}
```



<a name="incomplete-and-past-due-status"></a>
#### 미완료 및 연체 상태

구독 생성 후 추가 결제 조치가 필요한 경우 구독은 `incomplete`로 표시됩니다. 구독 상태는 Cashier의 `subscriptions` 데이터베이스 테이블의 `stripe_status` 열에 저장됩니다.

마찬가지로, 가격을 변경할 때 추가 결제 조치가 필요한 경우 구독은 `past_due`로 표시됩니다. 구독이 이러한 상태 중 하나에 있는 동안 고객이 결제를 확인하기 전까지 활성 상태가 되지 않습니다. 구독의 결제가 미완료인지 확인하는 것은 청구 가능한 모델이나 구독 인스턴스에서 `hasIncompletePayment` 메서드를 사용하여 수행할 수 있습니다.

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```



구독에 결제가 완료되지 않은 경우, 사용자를 Cashier의 결제 확인 페이지로 안내하고 `latestPayment` 식별자를 전달해야 합니다. 이 식별자는 구독 인스턴스에서 사용 가능한 `latestPayment` 메서드를 사용하여 가져올 수 있습니다:

```html
<a href="{{ route('cashier.payment', $subscription->latestPayment()->id) }}">
    Please confirm your payment.
</a>
```



구독이 `past_due` 또는 `incomplete` 상태일 때에도 활성 상태로 간주되기를 원한다면, Cashier에서 제공하는 `keepPastDueSubscriptionsActive` 및 `keepIncompleteSubscriptionsActive` 메서드를 사용할 수 있습니다. 일반적으로 이러한 메서드는 `App\Providers\AppServiceProvider`의 `register` 메서드에서 호출되어야 합니다:

```php
use Laravel\Cashier\Cashier;

/**
 * Register any application services.
 */
public function register(): void
{
    Cashier::keepPastDueSubscriptionsActive();
    Cashier::keepIncompleteSubscriptionsActive();
}
```



> [!WARNING]
> 구독이 `incomplete` 상태일 때는 결제가 확인될 때까지 변경할 수 없습니다. 따라서 구독이 `incomplete` 상태일 때 `swap` 및 `updateQuantity` 메서드는 예외를 발생시킵니다.

<a name="subscription-scopes"></a>
#### 구독 범위

대부분의 구독 상태는 쿼리 범위로도 제공되므로 특정 상태에 있는 구독을 데이터베이스에서 쉽게 쿼리할 수 있습니다:

```php
// Get all active subscriptions...
$subscriptions = Subscription::query()->active()->get();

// Get all of the canceled subscriptions for a user...
$subscriptions = $user->subscriptions()->canceled()->get();
```



사용 가능한 모든 범위 목록은 아래에서 확인할 수 있습니다:

```php
Subscription::query()->active();
Subscription::query()->canceled();
Subscription::query()->ended();
Subscription::query()->incomplete();
Subscription::query()->notCanceled();
Subscription::query()->notOnGracePeriod();
Subscription::query()->notOnTrial();
Subscription::query()->onGracePeriod();
Subscription::query()->onTrial();
Subscription::query()->pastDue();
Subscription::query()->recurring();
```



<a name="changing-prices"></a>
### 가격 변경

고객이 귀하의 애플리케이션에 가입한 후, 가끔 새 구독 가격으로 변경하기를 원할 수 있습니다. 고객의 구독 가격을 새 가격으로 변경하려면, Stripe 가격 식별자를 `swap` 메서드에 전달하세요. 가격을 변경할 때, 사용자가 이전에 구독을 취소한 경우 다시 활성화하고자 하는 것으로 간주됩니다. 지정된 가격 식별자는 Stripe 대시보드에서 사용할 수 있는 Stripe 가격 식별자와 일치해야 합니다:

```php
use App\Models\User;

$user = App\Models\User::find(1);

$user->subscription('default')->swap('price_yearly');
```



고객이 체험 중인 경우, 체험 기간은 유지됩니다. 또한, 구독에 "수량"이 있는 경우, 해당 수량도 유지됩니다.

고객이 현재 사용 중인 체험 기간을 취소하고 가격을 교체하려면, `skipTrial` 메서드를 호출할 수 있습니다:

```php
$user->subscription('default')
    ->skipTrial()
    ->swap('price_yearly');
```



다음 결제 주기를 기다리지 않고 가격을 교체하고 즉시 고객에게 청구서를 발행하고 싶다면, `swapAndInvoice` 방법을 사용할 수 있습니다:

```php
$user = User::find(1);

$user->subscription('default')->swapAndInvoice('price_yearly');
```



<a name="prorations"></a>
#### 비례 배분

기본적으로 Stripe는 가격을 변경할 때 요금을 비례 배분합니다. `noProrate` 방법을 사용하여 요금을 비례 배분하지 않고 구독 가격을 업데이트할 수 있습니다:

```php
$user->subscription('default')->noProrate()->swap('price_yearly');
```



구독 비례 배분에 대한 자세한 정보는 [Stripe 문서](https://stripe.com/docs/billing/subscriptions/prorations)를 참조하세요.

> [!WARNING]
> `swapAndInvoice` 메서드 전에 `noProrate` 메서드를 실행해도 비례 배분에는 영향을 미치지 않습니다. 인보이스는 항상 발행됩니다.

<a name="subscription-quantity"></a>
### 구독 수량

때때로 구독은 "수량"에 영향을 받습니다. 예를 들어, 프로젝트 관리 애플리케이션은 프로젝트당 매월 $10를 청구할 수 있습니다. `incrementQuantity` 및 `decrementQuantity` 메서드를 사용하여 구독 수량을 쉽게 증가시키거나 감소시킬 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->incrementQuantity();

// Add five to the subscription's current quantity...
$user->subscription('default')->incrementQuantity(5);

$user->subscription('default')->decrementQuantity();

// Subtract five from the subscription's current quantity...
$user->subscription('default')->decrementQuantity(5);
```



또는 `updateQuantity` 방법을 사용하여 특정 수량을 설정할 수 있습니다:

```php
$user->subscription('default')->updateQuantity(10);
```



`noProrate` 방법은 요금을 비례 계산하지 않고 구독 수량을 업데이트하는 데 사용할 수 있습니다:

```php
$user->subscription('default')->noProrate()->updateQuantity(10);
```



구독 수량에 대한 자세한 정보는 [Stripe 문서](https://stripe.com/docs/subscriptions/quantities)를 참조하세요.

<a name="quantities-for-subscription-with-multiple-products"></a>
#### 여러 제품이 포함된 구독의 수량

귀하의 구독이 [여러 제품이 포함된 구독](#subscriptions-with-multiple-products)인 경우, 증가 / 감소 메서드의 두 번째 인수로 수량을 증가 또는 감소시키려는 가격의 ID를 전달해야 합니다:

```php
$user->subscription('default')->incrementQuantity(1, 'price_chat');
```



<a name="subscriptions-with-multiple-products"></a>
### 여러 제품을 포함하는 구독

[여러 제품을 포함한 구독](https://stripe.com/docs/billing/subscriptions/multiple-products)은 단일 구독에 여러 청구 제품을 할당할 수 있게 해줍니다. 예를 들어, 기본 구독 가격이 월 $10인 고객 서비스 "헬프데스크" 애플리케이션을 구축하고 추가로 라이브 채팅 애드온 제품을 월 $15에 제공한다고 가정해 보세요. 여러 제품을 포함한 구독에 대한 정보는 Cashier의 `subscription_items` 데이터베이스 테이블에 저장됩니다.

`newSubscription` 메서드에 두 번째 인수로 가격 배열을 전달하여 특정 구독에 여러 제품을 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', [
        'price_monthly',
        'price_chat',
    ])->create($request->paymentMethodId);

    // ...
});
```



위 예제에서, 고객은 `default` 구독에 두 가지 가격이 연결될 것입니다. 두 가격 모두 각자의 청구 주기에 따라 청구됩니다. 필요하다면, 각각의 가격에 대해 특정 수량을 표시하기 위해 `quantity` 방법을 사용할 수 있습니다:

```php
$user = User::find(1);

$user->newSubscription('default', ['price_monthly', 'price_chat'])
    ->quantity(5, 'price_chat')
    ->create($paymentMethod);
```



기존 구독에 다른 가격을 추가하려면 구독의 `addPrice` 메서드를 호출할 수 있습니다:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat');
```



위의 예시는 새로운 가격을 추가하며 고객은 다음 청구 주기에 이에 대한 요금을 청구받게 됩니다. 고객에게 즉시 청구하고 싶다면 `addPriceAndInvoice` 방법을 사용할 수 있습니다:

```php
$user->subscription('default')->addPriceAndInvoice('price_chat');
```



특정 수량과 함께 가격을 추가하고 싶다면 `addPrice` 또는 `addPriceAndInvoice` 메서드의 두 번째 인수로 수량을 전달할 수 있습니다:

```php
$user = User::find(1);

$user->subscription('default')->addPrice('price_chat', 5);
```



`removePrice` 방법을 사용하여 구독 가격을 제거할 수 있습니다:

```php
$user->subscription('default')->removePrice('price_chat');
```



> [!WARNING]
> 구독의 마지막 가격을 제거할 수 없습니다. 대신, 단순히 구독을 취소해야 합니다.

<a name="swapping-prices"></a>
#### 가격 교체

여러 제품이 포함된 구독의 가격도 변경할 수 있습니다. 예를 들어, 고객이 `price_basic` 구독과 `price_chat` 부가 제품을 가지고 있고, 고객을 `price_basic` 가격에서 `price_pro` 가격으로 업그레이드하고 싶다고 가정해 보겠습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->subscription('default')->swap(['price_pro', 'price_chat']);
```



위의 예제를 실행하면 `price_basic`가 있는 기본 구독 항목은 삭제되고 `price_chat`가 있는 항목은 유지됩니다. 또한 `price_pro`에 대한 새 구독 항목이 생성됩니다.

`swap` 메서드에 키/값 쌍 배열을 전달하여 구독 항목 옵션을 지정할 수도 있습니다. 예를 들어, 구독 가격 수량을 지정해야 할 수도 있습니다:

```php
$user = User::find(1);

$user->subscription('default')->swap([
    'price_pro' => ['quantity' => 5],
    'price_chat'
]);
```



구독에서 단일 가격을 변경하고 싶다면, 구독 항목 자체에서 `swap` 방법을 사용하여 변경할 수 있습니다. 이 방법은 구독의 다른 가격에 있는 모든 기존 메타데이터를 유지하고 싶을 때 특히 유용합니다:

```php
$user = User::find(1);

$user->subscription('default')
    ->findItemOrFail('price_basic')
    ->swap('price_pro');
```



<a name="proration"></a>
#### 비례 배분

기본적으로 Stripe는 다중 상품 구독에서 가격을 추가하거나 제거할 때 요금을 비례 배분합니다. 비례 배분 없이 가격 조정을 하려면, 가격 작업에 `noProrate` 메서드를 연결해야 합니다:

```php
$user->subscription('default')->noProrate()->removePrice('price_chat');
```



<a name="swapping-quantities"></a>
#### 수량

개별 구독 가격의 수량을 업데이트하려면, [기존 수량 방법](#subscription-quantity)을 사용하여 가격의 ID를 메서드에 추가 인수로 전달하면 됩니다:

```php
$user = User::find(1);

$user->subscription('default')->incrementQuantity(5, 'price_chat');

$user->subscription('default')->decrementQuantity(3, 'price_chat');

$user->subscription('default')->updateQuantity(10, 'price_chat');
```



> [!WARNING]
> 구독에 여러 가격이 있는 경우 `Subscription` 모델의 `stripe_price` 및 `quantity` 속성은 `null`가 됩니다. 개별 가격 속성에 접근하려면 `Subscription` 모델에서 사용할 수 있는 `items` 관계를 사용해야 합니다.

<a name="subscription-items"></a>
#### 구독 항목

구독에 여러 가격이 있는 경우, 데이터베이스의 `subscription_items` 테이블에 여러 구독 "항목"이 저장됩니다. 구독에서 `items` 관계를 통해 이러한 항목에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$subscriptionItem = $user->subscription('default')->items->first();

// Retrieve the Stripe price and quantity for a specific item...
$stripePrice = $subscriptionItem->stripe_price;
$quantity = $subscriptionItem->quantity;
```



`findItemOrFail` 방법을 사용하여 특정 가격을 검색할 수도 있습니다:

```php
$user = User::find(1);

$subscriptionItem = $user->subscription('default')->findItemOrFail('price_chat');
```



<a name="multiple-subscriptions"></a>
### 다중 구독

Stripe는 고객이 동시에 여러 구독을 가질 수 있도록 허용합니다. 예를 들어, 수영 구독과 웨이트 트레이닝 구독을 제공하는 체육관을 운영할 수 있으며, 각 구독은 서로 다른 가격을 가질 수 있습니다. 물론 고객은 두 가지 중 하나 또는 모두에 가입할 수 있어야 합니다.

애플리케이션이 구독을 생성할 때 `newSubscription` 메서드에 구독 유형을 제공할 수 있습니다. 유형은 사용자가 시작하는 구독 유형을 나타내는 임의의 문자열일 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/swimming/subscribe', function (Request $request) {
    $request->user()->newSubscription('swimming')
        ->price('price_swimming_monthly')
        ->create($request->paymentMethodId);

    // ...
});
```



이 예제에서 우리는 고객을 위해 월간 수영 구독을 시작했습니다. 하지만 나중에 연간 구독으로 변경하고 싶어할 수도 있습니다. 고객의 구독을 조정할 때는 `swimming` 구독의 가격만 간단히 변경하면 됩니다:

```php
$user->subscription('swimming')->swap('price_swimming_yearly');
```



물론, 구독을 완전히 취소할 수도 있습니다:

```php
$user->subscription('swimming')->cancel();
```



<a name="usage-based-billing"></a>
### 사용량 기반 청구

[사용량 기반 청구](https://stripe.com/docs/billing/subscriptions/metered-billing)를 사용하면 청구 주기 동안 고객의 제품 사용량에 따라 요금을 청구할 수 있습니다. 예를 들어, 고객이 한 달에 보내는 문자 메시지나 이메일 수에 따라 요금을 청구할 수 있습니다.

사용량 청구를 시작하려면 먼저 Stripe 대시보드에서 [사용량 기반 청구 모델](https://docs.stripe.com/billing/subscriptions/usage-based/implementation-guide)과 [미터](https://docs.stripe.com/billing/subscriptions/usage-based/recording-usage#configure-meter)가 포함된 새 제품을 생성해야 합니다. 미터를 생성한 후, 사용량을 보고하고 검색하는 데 필요한 관련 이벤트 이름과 미터 ID를 저장합니다. 그런 다음 `meteredPrice` 메서드를 사용하여 계량 가격 ID를 고객 구독에 추가합니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default')
        ->meteredPrice('price_metered')
        ->create($request->paymentMethodId);

    // ...
});
```



또한 [Stripe Checkout](#checkout)를 통해 종량제 구독을 시작할 수도 있습니다:

```php
$checkout = Auth::user()
    ->newSubscription('default', [])
    ->meteredPrice('price_metered')
    ->checkout();

return view('your-checkout-view', [
    'checkout' => $checkout,
]);
```



<a name="reporting-usage"></a>
#### 사용 보고

고객이 귀하의 애플리케이션을 사용할 때, 정확한 청구를 위해 그들의 사용량을 Stripe에 보고하게 됩니다. 계량된 이벤트의 사용량을 보고하려면, `Billable` 모델에서 `reportMeterEvent` 메서드를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent');
```



기본적으로 청구 기간에 '사용량' 1이 추가됩니다. 또는 청구 기간 동안 고객의 사용량에 추가할 특정 '사용량'을 전달할 수 있습니다:

```php
$user = User::find(1);

$user->reportMeterEvent('emails-sent', quantity: 15);
```



미터에 대한 고객의 이벤트 요약을 검색하려면 `Billable` 인스턴스의 `meterEventSummaries` 메서드를 사용할 수 있습니다:

```php
$user = User::find(1);

$meterUsage = $user->meterEventSummaries($meterId);

$meterUsage->first()->aggregated_value; // 10
```



Meter 이벤트 요약에 대한 자세한 정보는 Stripe의 [Meter Event Summary 객체 문서](https://docs.stripe.com/api/billing/meter-event_summary/object)를 참조하십시오.

모든 미터를 [나열하려면](https://docs.stripe.com/api/billing/meter/list), `Billable` 인스턴스의 `meters` 메서드를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->meters();
```



<a name="subscription-taxes"></a>
### 구독 세금

> [!WARNING]
> 세율을 수동으로 계산하는 대신, [Stripe Tax를 사용하여 세금을 자동으로 계산](#tax-configuration)할 수 있습니다.

사용자가 구독 시 지불하는 세율을 지정하려면, 청구 가능한 모델에서 `taxRates` 메서드를 구현하고 Stripe 세율 ID를 포함하는 배열을 반환해야 합니다. 이러한 세율은 [Stripe 대시보드](https://dashboard.stripe.com/test/tax-rates)에서 정의할 수 있습니다.

```php
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array<int, string>
 */
public function taxRates(): array
{
    return ['txr_id'];
}
```



`taxRates` 방법은 고객별로 세율을 적용할 수 있도록 하여, 여러 국가와 세율에 걸친 사용자 기반에 유용할 수 있습니다.

여러 제품이 포함된 구독을 제공하는 경우, 청구 가능한 모델에 `priceTaxRates` 방법을 구현하여 각 가격에 대해 다른 세율을 정의할 수 있습니다:

```php
/**
 * The tax rates that should apply to the customer's subscriptions.
 *
 * @return array<string, array<int, string>>
 */
public function priceTaxRates(): array
{
    return [
        'price_monthly' => ['txr_id'],
    ];
}
```



> [!WARNING]
> `taxRates` 방법은 구독 요금에만 적용됩니다. Cashier를 사용하여 '일회성' 요금을 청구하는 경우, 그 시점에 세율을 수동으로 지정해야 합니다.

<a name="syncing-tax-rates"></a>
#### 세율 동기화

`taxRates` 메서드가 반환하는 하드코딩된 세율 ID를 변경할 때, 해당 사용자의 기존 구독에 대한 세금 설정은 그대로 유지됩니다. 기존 구독의 세금 값을 새로운 `taxRates` 값으로 업데이트하려면 사용자의 구독 인스턴스에서 `syncTaxRates` 메서드를 호출해야 합니다:

```php
$user->subscription('default')->syncTaxRates();
```



이 기능은 또한 여러 제품이 포함된 구독의 모든 항목 세율을 동기화합니다. 애플리케이션에서 여러 제품이 포함된 구독을 제공하는 경우, 청구 모델이 위에서 논의한 `priceTaxRates` 메서드를 구현하도록 해야 합니다 [위 논의 참고](#subscription-taxes).

<a name="tax-exemption"></a>
#### 세금 면제

Cashier는 또한 고객이 세금 면제인지 여부를 결정하기 위해 `isNotTaxExempt`, `isTaxExempt`, `reverseChargeApplies` 메서드를 제공합니다. 이 메서드들은 Stripe API를 호출하여 고객의 세금 면제 상태를 확인합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->isTaxExempt();
$user->isNotTaxExempt();
$user->reverseChargeApplies();
```



> [!WARNING]
> 이 메서드들은 모든 `Laravel\Cashier\Invoice` 객체에서도 사용할 수 있습니다. 그러나 `Invoice` 객체에서 호출될 경우, 이 메서드들은 인보이스가 생성된 시점의 면제 상태를 결정합니다.

<a name="subscription-anchor-date"></a>
### 구독 기준일

기본적으로, 청구 주기 기준일은 구독이 생성된 날짜이거나 시험 기간이 사용될 경우 시험이 끝나는 날짜입니다. 청구 기준일을 수정하고 싶은 경우, `anchorBillingCycleOn` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $anchor = Carbon::parse('first day of next month');

    $request->user()->newSubscription('default', 'price_monthly')
        ->anchorBillingCycleOn($anchor->startOfDay())
        ->create($request->paymentMethodId);

    // ...
});
```



구독 청구 주기 관리를 위한 자세한 정보는 [Stripe 청구 주기 문서](https://stripe.com/docs/billing/subscriptions/billing-cycle)를 참조하세요.

<a name="cancelling-subscriptions"></a>
### 구독 취소

구독을 취소하려면 사용자의 구독에서 `cancel` 메서드를 호출하세요:

```php
$user->subscription('default')->cancel();
```



구독이 취소되면 Cashier는 자동으로 `subscriptions` 데이터베이스 테이블의 `ends_at` 열을 설정합니다. 이 열은 `subscribed` 메서드가 언제 `false`을 반환하기 시작해야 하는지를 알기 위해 사용됩니다.

예를 들어, 고객이 3월 1일에 구독을 취소했지만 구독이 3월 5일에 종료될 예정이었다면, `subscribed` 메서드는 3월 5일까지 계속 `true`를 반환합니다. 이는 사용자가 일반적으로 청구 주기 종료까지 애플리케이션 사용을 계속할 수 있도록 허용되기 때문에 이루어집니다.

사용자가 구독을 취소했지만 여전히 “유예 기간”에 있는지를 확인하려면 `onGracePeriod` 메서드를 사용할 수 있습니다:

```php
if ($user->subscription('default')->onGracePeriod()) {
    // ...
}
```



구독을 즉시 취소하려면 사용자의 구독에서 `cancelNow` 메서드를 호출하세요:

```php
$user->subscription('default')->cancelNow();
```



구독을 즉시 취소하고 남아 있는 미청구량 또는 새로운/대기 중인 비례 청구 항목을 청구하고 싶다면, 사용자의 구독에서 `cancelNowAndInvoice` 메서드를 호출하세요:

```php
$user->subscription('default')->cancelNowAndInvoice();
```



특정 시점에 구독을 취소하도록 선택할 수도 있습니다:

```php
$user->subscription('default')->cancelAt(
    now()->plus(days: 10)
);
```



마지막으로, 관련 사용자 모델을 삭제하기 전에 항상 사용자 구독을 취소해야 합니다:

```php
$user->subscription('default')->cancelNow();

$user->delete();
```



<a name="resuming-subscriptions"></a>
### 구독 재개

고객이 구독을 취소했지만 이를 재개하고자 하는 경우, 구독에서 `resume` 메서드를 호출할 수 있습니다. 구독을 재개하려면 고객이 여전히 "유예 기간" 내에 있어야 합니다:

```php
$user->subscription('default')->resume();
```



고객이 구독을 취소한 후 구독이 완전히 만료되기 전에 다시 구독을 재개하는 경우, 고객은 즉시 청구되지 않습니다. 대신 그들의 구독이 다시 활성화되며, 원래의 청구 주기에 따라 청구됩니다.

<a name="subscription-trials"></a>
## 구독 체험

<a name="with-payment-method-up-front"></a>
### 선불 결제 방식

고객에게 체험 기간을 제공하면서도 결제 수단 정보를 미리 수집하고 싶다면, 구독을 생성할 때 `trialDays` 방식을 사용해야 합니다:

```php
use Illuminate\Http\Request;

Route::post('/user/subscribe', function (Request $request) {
    $request->user()->newSubscription('default', 'price_monthly')
        ->trialDays(10)
        ->create($request->paymentMethodId);

    // ...
});
```



이 방법은 데이터베이스 내 구독 기록에 체험 기간 종료 날짜를 설정하고, Stripe에 고객에게 청구를 이 날짜 이후로 시작하도록 지시합니다. `trialDays` 방법을 사용할 경우, Cashier는 Stripe에서 가격에 대해 설정된 기본 체험 기간을 덮어씁니다.

> [!WARNING]
> 고객의 구독이 체험 기간 종료일 이전에 취소되지 않으면 체험이 종료되자마자 요금이 청구되기 때문에, 사용자에게 체험 종료 날짜를 반드시 알려야 합니다.

`trialUntil` 방법을 사용하면 `DateTime` 인스턴스를 제공하여 체험 기간이 언제 종료될지 지정할 수 있습니다:

```php
use Illuminate\Support\Carbon;

$user->newSubscription('default', 'price_monthly')
    ->trialUntil(Carbon::now()->plus(days: 10))
    ->create($paymentMethod);
```



사용자가 체험 기간에 있는지 여부는 사용자 인스턴스의 `onTrial` 메서드 또는 구독 인스턴스의 `onTrial` 메서드를 사용하여 확인할 수 있습니다. 아래의 두 예는 동일합니다:

```php
if ($user->onTrial('default')) {
    // ...
}

if ($user->subscription('default')->onTrial()) {
    // ...
}
```



구독 체험을 즉시 종료하려면 `endTrial` 방법을 사용할 수 있습니다:

```php
$user->subscription('default')->endTrial();
```



기존 평가판이 만료되었는지 확인하려면 `hasExpiredTrial` 메서드를 사용할 수 있습니다:

```php
if ($user->hasExpiredTrial('default')) {
    // ...
}

if ($user->subscription('default')->hasExpiredTrial()) {
    // ...
}
```



<a name="defining-trial-days-in-stripe-cashier"></a>
#### Stripe / Cashier에서 체험 기간 정의하기

Stripe 대시보드에서 가격에 대한 체험 일수를 정의하거나 항상 Cashier를 사용하여 명시적으로 전달할 수 있습니다. 가격의 체험 기간을 Stripe에서 정의하기로 선택한 경우, 이전에 구독을 했던 고객을 포함한 새로운 구독은 명시적으로 `skipTrial()` 메서드를 호출하지 않는 한 항상 체험 기간을 받게 된다는 점을 알아야 합니다.

<a name="without-payment-method-up-front"></a>
### 결제 수단 없이 선결제 없이

사용자의 결제 수단 정보를 미리 수집하지 않고 체험 기간을 제공하려면, 사용자 레코드의 `trial_ends_at` 열을 원하는 체험 종료 날짜로 설정할 수 있습니다. 이는 일반적으로 사용자 등록 중에 이루어집니다:

```php
use App\Models\User;

$user = User::create([
    // ...
    'trial_ends_at' => now()->plus(days: 10),
]);
```



> [!WARNING]
> 청구 가능한 모델 클래스 정의 내 `trial_ends_at` 속성에 대해 [날짜 캐스트](/docs/{{version}}/eloquent-mutators#date-casting)를 반드시 추가하세요.

Cashier는 이 유형의 무료 체험을 기존 구독에 연결되지 않았기 때문에 "일반 체험(generic trial)"이라고 합니다. 청구 가능한 모델 인스턴스에서 `onTrial` 메서드는 현재 날짜가 `trial_ends_at` 값 이후가 아니면 `true`를 반환합니다:

```php
if ($user->onTrial()) {
    // User is within their trial period...
}
```



사용자에 대한 실제 구독을 생성할 준비가 되면, 평소처럼 `newSubscription` 방법을 사용할 수 있습니다:

```php
$user = User::find(1);

$user->newSubscription('default', 'price_monthly')->create($paymentMethod);
```



사용자의 체험 종료 날짜를 가져오기 위해서는 `trialEndsAt` 메서드를 사용할 수 있습니다. 사용자가 체험 중인 경우 이 메서드는 Carbon 날짜 인스턴스를 반환하고, 체험 중이 아니라면 `null`를 반환합니다. 기본 구독이 아닌 특정 구독에 대한 체험 종료 날짜를 얻고 싶다면 선택적 구독 유형 매개변수를 전달할 수도 있습니다:

```php
if ($user->onTrial()) {
    $trialEndsAt = $user->trialEndsAt('main');
}
```



사용자가 '일반적인' 체험 기간 내에 있으며 아직 실제 구독을 생성하지 않았는지 구체적으로 알고 싶다면 `onGenericTrial` 방법을 사용할 수도 있습니다:

```php
if ($user->onGenericTrial()) {
    // User is within their "generic" trial period...
}
```



<a name="extending-trials"></a>
### 체험 기간 연장

`extendTrial` 방법을 사용하면 구독이 생성된 후에도 구독의 체험 기간을 연장할 수 있습니다. 체험 기간이 이미 만료되고 고객이 이미 구독 요금을 청구받고 있는 경우에도 확장된 체험 기간을 제공할 수 있습니다. 체험 기간 동안 사용된 시간은 고객의 다음 청구서에서 차감됩니다:

```php
use App\Models\User;

$subscription = User::find(1)->subscription('default');

// End the trial 7 days from now...
$subscription->extendTrial(
    now()->plus(days: 7)
);

// Add an additional 5 days to the trial...
$subscription->extendTrial(
    $subscription->trial_ends_at->plus(days: 5)
);
```



<a name="handling-stripe-webhooks"></a>
## Handling Stripe Webhooks

> [!NOTE]
> You may use [the Stripe CLI](https://stripe.com/docs/stripe-cli) to help test webhooks during local development.

Stripe can notify your application of a variety of events via webhooks. By default, a route that points to Cashier's webhook controller is automatically registered by the Cashier service provider. This controller will handle all incoming webhook requests.

By default, the Cashier webhook controller will automatically handle cancelling subscriptions that have too many failed charges (as defined by your Stripe settings), customer updates, customer deletions, subscription updates, and payment method changes; however, as we'll soon discover, you can extend this controller to handle any Stripe webhook event you like.

To ensure your application can handle Stripe webhooks, be sure to configure the webhook URL in the Stripe control panel. By default, Cashier's webhook controller responds to the `/stripe/webhook` URL path. The full list of all webhooks you should enable in the Stripe control panel are:

- `customer.subscription.created`
- `customer.subscription.updated`
- `customer.subscription.deleted`
- `customer.updated`
- `customer.deleted`
- `payment_method.automatically_updated`
- `invoice.payment_action_required`
- `invoice.payment_succeeded`

For convenience, Cashier includes a `cashier:webhook` Artisan command. This command will create a webhook in Stripe that listens to all of the events required by Cashier:

```shell
php artisan cashier:webhook
```



기본적으로 생성된 웹훅은 `APP_URL` 환경 변수와 Cashier에 포함된 `cashier.webhook` 경로로 정의된 URL을 가리킵니다. 다른 URL을 사용하려는 경우 명령을 호출할 때 `--url` 옵션을 제공할 수 있습니다:

```shell
php artisan cashier:webhook --url "https://example.com/stripe/webhook"
```



생성된 웹후크는 사용 중인 Cashier 버전과 호환되는 Stripe API 버전을 사용합니다. 다른 Stripe 버전을 사용하고 싶다면, `--api-version` 옵션을 제공할 수 있습니다:

```shell
php artisan cashier:webhook --api-version="2019-12-03"
```



생성 후 웹훅은 즉시 활성화됩니다. 웹훅을 생성하되 준비될 때까지 비활성 상태로 두고 싶다면, 명령을 호출할 때 `--disabled` 옵션을 제공할 수 있습니다:

```shell
php artisan cashier:webhook --disabled
```



> [!WARNING]
> 수신되는 Stripe 웹훅 요청을 Cashier에 포함된 [웹훅 서명 검증](#verifying-webhook-signatures) 미들웨어로 보호해야 합니다.

<a name="webhooks-csrf-protection"></a>
#### 웹훅과 CSRF 보호

Stripe 웹훅은 Laravel의 [CSRF 보호](/docs/{{version}}/csrf)를 우회해야 하므로, Laravel이 수신되는 Stripe 웹훅에 대해 CSRF 토큰을 검증하지 않도록 해야 합니다. 이를 위해, 애플리케이션의 `bootstrap/app.php` 파일에서 `stripe/*`을 CSRF 보호에서 제외해야 합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'stripe/*',
    ]);
})
```



<a name="defining-webhook-event-handlers"></a>
### 웹훅 이벤트 핸들러 정의

Cashier는 실패한 결제와 기타 일반적인 Stripe 웹훅 이벤트에 대해 구독 취소를 자동으로 처리합니다. 그러나 추가로 처리하고 싶은 웹훅 이벤트가 있는 경우, Cashier가 전달하는 다음 이벤트를 수신하여 처리할 수 있습니다:

- `Laravel\Cashier\Events\WebhookReceived`
- `Laravel\Cashier\Events\WebhookHandled`

두 이벤트 모두 Stripe 웹훅의 전체 페이로드를 포함합니다. 예를 들어, `invoice.payment_succeeded` 웹훅을 처리하려는 경우 이벤트를 처리할 [리스너](/docs/{{version}}/events#defining-listeners)를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Laravel\Cashier\Events\WebhookReceived;

class StripeEventListener
{
    /**
     * Handle received Stripe webhooks.
     */
    public function handle(WebhookReceived $event): void
    {
        if ($event->payload['type'] === 'invoice.payment_succeeded') {
            // Handle the incoming event...
        }
    }
}
```



<a name="verifying-webhook-signatures"></a>
### 웹훅 서명 검증

웹훅을 안전하게 보호하려면 [Stripe의 웹훅 서명](https://stripe.com/docs/webhooks/signatures)을 사용할 수 있습니다. 편의를 위해 Cashier는 자동으로 미들웨어를 포함하여 들어오는 Stripe 웹훅 요청이 유효한지 검증합니다.

웹훅 검증을 활성화하려면 애플리케이션의 `.env` 파일에 `STRIPE_WEBHOOK_SECRET` 환경 변수가 설정되어 있는지 확인하십시오. 웹훅 `secret`는 Stripe 계정 대시보드에서 확인할 수 있습니다.

<a name="single-charges"></a>
## 단일 청구

<a name="simple-charge"></a>
### 간단 청구

결제 수단 식별자를 사용하여 고객에게 일회성 청구를 하려면 청구 가능한 모델 인스턴스에서 `charge` 메서드를 사용할 수 있습니다. 일회성 청구를 처리하기 전에 고객으로부터 결제 정보를 수집해야 하는 경우, [단일 청구를 위한 결제 요소](#payment-element-for-single-charges) 문서를 참조하십시오:

```php
use Illuminate\Http\Request;

Route::post('/purchase', function (Request $request) {
    $payment = $request->user()->charge(
        100, $request->paymentMethodId
    );

    // ...
});
```



`charge` 메서드는 세 번째 인수로 배열을 받아 Stripe 결제 의도 생성에 원하는 옵션을 전달할 수 있습니다. 결제 의도를 생성할 때 사용할 수 있는 옵션에 대한 자세한 내용은 [Stripe 문서](https://stripe.com/docs/api/payment_intents/create)에서 확인할 수 있습니다.

```php
$user->charge(100, $paymentMethod, [
    'custom_option' => $value,
]);
```



기본 고객이나 사용자가 없어도 `charge` 방법을 사용할 수 있습니다. 이를 수행하려면 애플리케이션의 청구 모델 새 인스턴스에서 `charge` 방법을 호출하십시오:

```php
use App\Models\User;

$payment = (new User)->charge(100, $paymentMethod);
```



청구가 실패하면 `charge` 메서드는 예외를 발생시킵니다. 청구가 성공하면 `Laravel\Cashier\Payment`의 인스턴스가 메서드에서 반환됩니다:

```php
try {
    $payment = $user->charge(100, $paymentMethod);
} catch (Exception $e) {
    // ...
}
```



> [!WARNING]
> `charge` 메서드는 귀하의 애플리케이션에서 사용하는 통화의 최하위 단위로 지불 금액을 받습니다. 예를 들어, 고객이 미국 달러로 결제하는 경우 금액을 페니 단위로 지정해야 합니다.

<a name="charge-with-invoice"></a>
### 인보이스로 결제하기

때때로 일회성 요금을 청구하고 고객에게 PDF 인보이스를 제공해야 할 수도 있습니다. `invoicePrice` 메서드를 사용하면 정확히 그 작업을 수행할 수 있습니다. 예를 들어, 고객에게 새 셔츠 5개에 대한 인보이스를 발행해보겠습니다:

```php
$user->invoicePrice('price_tshirt', 5);
```



청구서는 사용자의 기본 결제 수단으로 즉시 청구됩니다. `invoicePrice` 메서드는 세 번째 인수로 배열도 허용합니다. 이 배열에는 청구 항목에 대한 청구 옵션이 포함되어 있습니다. 메서드가 허용하는 네 번째 인수도 배열이며, 이 배열에는 청구서 자체에 대한 청구 옵션이 포함되어야 합니다:

```php
$user->invoicePrice('price_tshirt', 5, [
    'discounts' => [
        ['coupon' => 'SUMMER21SALE']
    ],
], [
    'default_tax_rates' => ['txr_id'],
]);
```



`invoicePrice`와 마찬가지로, 고객의 "계정"에 항목을 추가한 후 청구하여 여러 항목(청구서당 최대 250개 항목)에 대해 일회성 요금을 생성하기 위해 `tabPrice` 방법을 사용할 수 있습니다. 예를 들어, 고객에게 다섯 개의 셔츠와 두 개의 머그컵에 대해 청구할 수 있습니다:

```php
$user->tabPrice('price_tshirt', 5);
$user->tabPrice('price_mug', 2);
$user->invoice();
```



또는 `invoiceFor` 방법을 사용하여 고객의 기본 결제 수단에 '일회성' 요금을 부과할 수 있습니다:

```php
$user->invoiceFor('One Time Fee', 500);
```



`invoiceFor` 방법을 사용할 수는 있지만, 미리 정의된 가격과 함께 `invoicePrice` 및 `tabPrice` 방법을 사용하는 것이 권장됩니다. 이렇게 하면 제품별 판매에 대한 Stripe 대시보드에서 더 나은 분석 및 데이터를 이용할 수 있습니다.

> [!WARNING]
> `invoice`, `invoicePrice` 및 `invoiceFor` 방법은 Stripe 청구서를 생성하며, 실패한 청구 시도를 재시도합니다. 실패한 청구를 재시도하지 않으려면 첫 번째 실패한 청구 후 Stripe API를 사용하여 청구서를 종료해야 합니다.

<a name="creating-payment-intents"></a>
### 결제 의도 생성

청구 가능한 모델 인스턴스에서 `pay` 방식을 호출하여 새로운 Stripe 결제 의도를 생성할 수 있습니다. 이 메서드를 호출하면 `Laravel\Cashier\Payment` 인스턴스로 래핑된 결제 의도가 생성됩니다.

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->pay(
        $request->get('amount')
    );

    return $payment->client_secret;
});
```



결제 인텐트를 생성한 후에는 클라이언트 시크릿을 애플리케이션 프론트엔드로 반환하여 사용자가 브라우저에서 결제를 완료할 수 있도록 할 수 있습니다. Stripe 결제 인텐트를 사용하여 전체 결제 흐름을 구축하는 방법에 대해 더 읽고 싶다면 [Stripe 문서](https://stripe.com/docs/payments/accept-a-payment?platform=web)를 참조하세요.

`pay` 방법을 사용할 때, Stripe 대시보드에서 활성화된 기본 결제 수단이 고객에게 제공됩니다. 또는 특정 결제 수단만 허용하고 싶다면 `payWith` 방법을 사용할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/pay', function (Request $request) {
    $payment = $request->user()->payWith(
        $request->get('amount'), ['card', 'bancontact']
    );

    return $payment->client_secret;
});
```



> [!WARNING]
> `pay` 및 `payWith` 메서드는 애플리케이션에서 사용하는 통화의 가장 낮은 단위로 결제 금액을 받습니다. 예를 들어, 고객이 미국 달러로 결제하는 경우 금액은 페니 단위로 지정해야 합니다.

<a name="refunding-charges"></a>
### 요금 환불

Stripe 결제를 환불해야 하는 경우, `refund` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인수로 Stripe 결제 의도 ID를 받습니다:

```php
$payment = $user->charge(100, $paymentMethodId);

$user->refund($payment->id);
```



<a name="invoices"></a>
## 인보이스

<a name="retrieving-invoices"></a>
### 인보이스 가져오기

`invoices` 메서드를 사용하면 청구 가능한 모델의 인보이스 배열을 쉽게 가져올 수 있습니다. `invoices` 메서드는 `Laravel\Cashier\Invoice` 인스턴스의 컬렉션을 반환합니다:

```php
$invoices = $user->invoices();
```



결과에 보류 중인 송장을 포함하고 싶다면, `invoicesIncludingPending` 방법을 사용할 수 있습니다:

```php
$invoices = $user->invoicesIncludingPending();
```



특정 청구서를 ID로 조회하기 위해 `findInvoice` 방법을 사용할 수 있습니다:

```php
$invoice = $user->findInvoice($invoiceId);
```



<a name="displaying-invoice-information"></a>
#### 송장 정보 표시

고객의 송장을 나열할 때, 관련 송장 정보를 표시하기 위해 송장의 메서드를 사용할 수 있습니다. 예를 들어, 모든 송장을 표에 나열하여 사용자가 쉽게 원하는 송장을 다운로드할 수 있도록 할 수 있습니다:

```blade
<table>
    @foreach ($invoices as $invoice)
        <tr>
            <td>{{ $invoice->date()->toFormattedDateString() }}</td>
            <td>{{ $invoice->total() }}</td>
            <td><a href="/user/invoice/{{ $invoice->id }}">Download</a></td>
        </tr>
    @endforeach
</table>
```



<a name="upcoming-invoices"></a>
### 다가오는 송장

고객의 다가오는 송장을 가져오려면 `upcomingInvoice` 메서드를 사용할 수 있습니다:

```php
$invoice = $user->upcomingInvoice();
```



마찬가지로, 고객이 여러 구독을 가지고 있는 경우 특정 구독의 예정된 청구서를 조회할 수도 있습니다:

```php
$invoice = $user->subscription('default')->upcomingInvoice();
```



<a name="previewing-subscription-invoices"></a>
### 구독 청구서 미리보기

`previewInvoice` 방법을 사용하면 가격을 변경하기 전에 청구서를 미리 볼 수 있습니다. 이를 통해 특정 가격 변경이 이루어졌을 때 고객의 청구서가 어떻게 보일지 확인할 수 있습니다:

```php
$invoice = $user->subscription('default')->previewInvoice('price_yearly');
```



여러 새 가격으로 청구서를 미리 보려면 `previewInvoice` 메서드에 가격 배열을 전달할 수 있습니다:

```php
$invoice = $user->subscription('default')->previewInvoice(['price_yearly', 'price_metered']);
```



<a name="generating-invoice-pdfs"></a>
### 인보이스 PDF 생성

인보이스 PDF를 생성하기 전에, 기본 인보이스 렌더러인 Dompdf 라이브러리를 설치하기 위해 Composer를 사용해야 합니다:

```shell
composer require dompdf/dompdf
```



라우트나 컨트롤러 내에서 `downloadInvoice` 메서드를 사용하여 특정 인보이스의 PDF 다운로드를 생성할 수 있습니다. 이 메서드는 인보이스를 다운로드하는 데 필요한 적절한 HTTP 응답을 자동으로 생성합니다:

```php
use Illuminate\Http\Request;

Route::get('/user/invoice/{invoice}', function (Request $request, string $invoiceId) {
    return $request->user()->downloadInvoice($invoiceId);
});
```



기본적으로 청구서의 모든 데이터는 Stripe에 저장된 고객 및 청구서 데이터에서 파생됩니다. 파일 이름은 `app.name` 구성 값에 따라 결정됩니다. 그러나 `downloadInvoice` 메서드에 두 번째 인수로 배열을 제공하여 이러한 데이터 중 일부를 사용자 정의할 수 있습니다. 이 배열을 통해 회사 및 제품 세부 정보와 같은 정보를 사용자 정의할 수 있습니다:

```php
return $request->user()->downloadInvoice($invoiceId, [
    'vendor' => 'Your Company',
    'product' => 'Your Product',
    'street' => 'Main Str. 1',
    'location' => '2000 Antwerp, Belgium',
    'phone' => '+32 499 00 00 00',
    'email' => 'info@example.com',
    'url' => 'https://example.com',
    'vendorVat' => 'BE123456789',
]);
```



`downloadInvoice` 방법은 세 번째 인수를 통해 사용자 지정 파일 이름도 허용합니다. 이 파일 이름에는 자동으로 `.pdf`가 접미사로 붙습니다:

```php
return $request->user()->downloadInvoice($invoiceId, [], 'my-invoice');
```



<a name="custom-invoice-render"></a>
#### 맞춤 인보이스 렌더러

Cashier는 맞춤 인보이스 렌더러를 사용하는 것도 가능합니다. 기본적으로 Cashier는 `DompdfInvoiceRenderer` 구현을 사용하며, 이는 [dompdf](https://github.com/dompdf/dompdf) PHP 라이브러리를 이용하여 Cashier의 인보이스를 생성합니다. 그러나 `Laravel\Cashier\Contracts\InvoiceRenderer` 인터페이스를 구현함으로써 원하는 렌더러를 사용할 수 있습니다. 예를 들어, 제3자 PDF 렌더링 서비스에 API 호출을 하여 인보이스 PDF를 렌더링할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;
use Laravel\Cashier\Contracts\InvoiceRenderer;
use Laravel\Cashier\Invoice;

class ApiInvoiceRenderer implements InvoiceRenderer
{
    /**
     * Render the given invoice and return the raw PDF bytes.
     */
    public function render(Invoice $invoice, array $data = [], array $options = []): string
    {
        $html = $invoice->view($data)->render();

        return Http::get('https://example.com/html-to-pdf', ['html' => $html])->get()->body();
    }
}
```



Once you have implemented the invoice renderer contract, you should update the `cashier.invoices.renderer` configuration value in your application's `config/cashier.php` configuration file. This configuration value should be set to the class name of your custom renderer implementation.

<a name="checkout"></a>
## Checkout

Cashier Stripe also provides support for [Stripe Checkout](https://stripe.com/payments/checkout). Stripe Checkout takes the pain out of implementing custom pages to accept payments by providing a pre-built, hosted payment page.

The following documentation contains information on how to get started using Stripe Checkout with Cashier. To learn more about Stripe Checkout, you should also consider reviewing [Stripe's own documentation on Checkout](https://stripe.com/docs/payments/checkout).

<a name="product-checkouts"></a>
### Product Checkouts

You may perform a checkout for an existing product that has been created within your Stripe dashboard using the `checkout` method on a billable model. The `checkout` method will initiate a new Stripe Checkout session. By default, you're required to pass a Stripe Price ID:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout('price_tshirt');
});
```



필요한 경우, 제품 수량을 지정할 수도 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 15]);
});
```



고객이 이 경로를 방문하면 Stripe의 결제 페이지로 리디렉션됩니다. 기본적으로 사용자가 구매를 성공적으로 완료하거나 취소하면 `home` 경로 위치로 리디렉션되지만, `success_url` 및 `cancel_url` 옵션을 사용하여 커스텀 콜백 URL을 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```



`success_url` 결제 옵션을 정의할 때, Stripe에 귀하의 URL을 호출할 때 결제 세션 ID를 쿼리 문자열 매개변수로 추가하도록 지시할 수 있습니다. 이렇게 하려면 `success_url` 쿼리 문자열에 문자 그대로 `{CHECKOUT_SESSION_ID}`를 추가하세요. Stripe는 이 자리 표시자를 실제 결제 세션 ID로 대체합니다:

```php
use Illuminate\Http\Request;
use Stripe\Checkout\Session;
use Stripe\Customer;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()->checkout(['price_tshirt' => 1], [
        'success_url' => route('checkout-success').'?session_id={CHECKOUT_SESSION_ID}',
        'cancel_url' => route('checkout-cancel'),
    ]);
});

Route::get('/checkout-success', function (Request $request) {
    $checkoutSession = $request->user()->stripe()->checkout->sessions->retrieve($request->get('session_id'));

    return view('checkout.success', ['checkoutSession' => $checkoutSession]);
})->name('checkout-success');
```



<a name="checkout-promotion-codes"></a>
#### 프로모션 코드

기본적으로 Stripe Checkout은 [사용자가 사용할 수 있는 프로모션 코드](https://stripe.com/docs/billing/subscriptions/discounts/codes)를 허용하지 않습니다. 다행히, Checkout 페이지에서 이를 활성화하는 쉬운 방법이 있습니다. 이를 위해 `allowPromotionCodes` 메서드를 호출할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/product-checkout', function (Request $request) {
    return $request->user()
        ->allowPromotionCodes()
        ->checkout('price_tshirt');
});
```



<a name="single-charge-checkouts"></a>
### 단일 결제 체크아웃

Stripe 대시보드에서 생성되지 않은 임시 제품에 대해서도 간단한 결제를 수행할 수 있습니다. 이를 위해 청구 가능한 모델에서 `checkoutCharge` 메서드를 사용하고, 청구 가능한 금액, 제품 이름, 선택 사항으로 수량을 전달할 수 있습니다. 고객이 이 경로를 방문하면 Stripe의 체크아웃 페이지로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/charge-checkout', function (Request $request) {
    return $request->user()->checkoutCharge(1200, 'T-Shirt', 5);
});
```



> [!WARNING]
> `checkoutCharge` 방식을 사용할 때, Stripe는 항상 Stripe 대시보드에 새로운 상품과 가격을 생성합니다. 따라서, Stripe 대시보드에서 미리 상품을 생성하고 대신 `checkout` 방식을 사용하는 것을 권장합니다.

<a name="subscription-checkouts"></a>
### 구독 체크아웃

> [!WARNING]
> 구독을 위해 Stripe Checkout을 사용하려면 Stripe 대시보드에서 `customer.subscription.created` 웹훅을 활성화해야 합니다. 이 웹훅은 데이터베이스에 구독 기록을 생성하고 모든 관련 구독 항목을 저장합니다.

또한 Stripe Checkout을 사용하여 구독을 시작할 수도 있습니다. Cashier의 구독 빌더 메서드로 구독을 정의한 후, `checkout ` 메서드를 호출할 수 있습니다. 고객이 이 경로를 방문하면 Stripe의 Checkout 페이지로 리디렉션됩니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout();
});
```



제품 결제와 마찬가지로, 성공 및 취소 URL을 사용자 지정할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->checkout([
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```



물론, 구독 결제에 대한 프로모션 코드를 활성화할 수도 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/subscription-checkout', function (Request $request) {
    return $request->user()
        ->newSubscription('default', 'price_monthly')
        ->allowPromotionCodes()
        ->checkout();
});
```



> [!WARNING]
> 불행히도 Stripe Checkout은 구독을 시작할 때 모든 구독 청구 옵션을 지원하지 않습니다. 구독 빌더에서 `anchorBillingCycleOn` 방법을 사용하거나, 프라레이션(proration) 동작을 설정하거나, 결제 동작(payment behavior)을 설정해도 Stripe Checkout 세션에서는 아무런 효과가 없습니다. 어떤 매개변수가 사용 가능한지 확인하려면 [Stripe Checkout 세션 API 문서](https://stripe.com/docs/api/checkout/sessions/create)를 참조하십시오.

<a name="stripe-checkout-trial-periods"></a>
#### Stripe Checkout과 체험 기간

물론 Stripe Checkout을 사용하여 완료될 구독을 생성할 때 체험 기간을 정의할 수 있습니다:

```php
$checkout = Auth::user()->newSubscription('default', 'price_monthly')
    ->trialDays(3)
    ->checkout();
```



그러나 체험 기간은 최소 48시간이어야 하며, 이는 Stripe Checkout에서 지원하는 최소 체험 시간입니다.

<a name="stripe-checkout-subscriptions-and-webhooks"></a>
#### 구독 및 웹훅

Stripe와 Cashier는 웹훅을 통해 구독 상태를 업데이트하므로, 고객이 결제 정보를 입력한 후 애플리케이션으로 돌아올 때 구독이 아직 활성화되지 않았을 가능성이 있습니다. 이 시나리오를 처리하기 위해 사용자가 결제 또는 구독이 보류 중임을 알리는 메시지를 표시할 수 있습니다.

<a name="collecting-tax-ids"></a>
### 세금 ID 수집

Checkout은 고객의 세금 ID 수집도 지원합니다. 체크아웃 세션에서 이를 활성화하려면 세션을 생성할 때 `collectTaxIds` 메서드를 호출하십시오:

```php
$checkout = $user->collectTaxIds()->checkout('price_tshirt');
```



이 메서드가 호출되면, 고객이 회사로서 구매하는지 여부를 표시할 수 있는 새 체크박스가 제공됩니다. 만약 그렇다면, 고객은 자신의 세금 ID 번호를 제공할 기회를 갖게 됩니다.

> [!WARNING]
> 이미 애플리케이션의 서비스 제공업체에서 [자동 세금 징수](#tax-configuration)를 구성한 경우, 이 기능은 자동으로 활성화되며 `collectTaxIds` 메서드를 호출할 필요가 없습니다.

<a name="guest-checkouts"></a>
### 게스트 체크아웃

`Checkout::guest` 메서드를 사용하여, 계정이 없는 애플리케이션의 게스트를 위한 체크아웃 세션을 시작할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()->create('price_tshirt', [
        'success_url' => route('your-success-route'),
        'cancel_url' => route('your-cancel-route'),
    ]);
});
```



기존 사용자를 위한 결제 세션을 만들 때와 마찬가지로, `Laravel\Cashier\CheckoutBuilder` 인스턴스에서 제공되는 추가 메서드를 활용하여 게스트 결제 세션을 사용자 정의할 수 있습니다:

```php
use Illuminate\Http\Request;
use Laravel\Cashier\Checkout;

Route::get('/product-checkout', function (Request $request) {
    return Checkout::guest()
        ->withPromotionCode('promo-code')
        ->create('price_tshirt', [
            'success_url' => route('your-success-route'),
            'cancel_url' => route('your-cancel-route'),
        ]);
});
```



After a guest checkout has been completed, Stripe can dispatch a `checkout.session.completed` webhook event, so make sure to [configure your Stripe webhook](https://dashboard.stripe.com/webhooks) to actually send this event to your application. Once the webhook has been enabled within the Stripe dashboard, you may [handle the webhook with Cashier](#handling-stripe-webhooks). The object contained in the webhook payload will be a [checkout object](https://stripe.com/docs/api/checkout/sessions/object) that you may inspect in order to fulfill your customer's order.

<a name="handling-failed-payments"></a>
## Handling Failed Payments

Sometimes, payments for subscriptions or single charges can fail. When this happens, Cashier will throw an `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that this happened. After catching this exception, you have two options on how to proceed.

First, you could redirect your customer to the dedicated payment confirmation page which is included with Cashier. This page already has an associated named route that is registered via Cashier's service provider. So, you may catch the `IncompletePayment` exception and redirect the user to the payment confirmation page:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $subscription = $user->newSubscription('default', 'price_monthly')
        ->create($paymentMethod);
} catch (IncompletePayment $exception) {
    return redirect()->route(
        'cashier.payment',
        [$exception->payment->id, 'redirect' => route('home')]
    );
}
```



On the payment confirmation page, the customer will be prompted to enter their credit card information again and perform any additional actions required by Stripe, such as "3D Secure" confirmation. After confirming their payment, the user will be redirected to the URL provided by the `redirect` parameter specified above. Upon redirection, `message` (string) and `success` (integer) query string variables will be added to the URL. The payment page currently supports the following payment method types:

<div class="content-list" markdown="1">

- Credit Cards
- Alipay
- Bancontact
- BECS Direct Debit
- EPS
- Giropay
- iDEAL
- SEPA Direct Debit

</div>

Alternatively, you could allow Stripe to handle the payment confirmation for you. In this case, instead of redirecting to the payment confirmation page, you may [set up Stripe's automatic billing emails](https://dashboard.stripe.com/account/billing/automatic) in your Stripe dashboard. However, if an `IncompletePayment` exception is caught, you should still inform the user they will receive an email with further payment confirmation instructions.

Payment exceptions may be thrown for the following methods: `charge`, `invoiceFor`, and `invoice` on models using the `Billable` trait. When interacting with subscriptions, the `create` method on the `SubscriptionBuilder`, and the `incrementAndInvoice` and `swapAndInvoice` methods on the `Subscription` and `SubscriptionItem` models may throw incomplete payment exceptions.

Determining if an existing subscription has an incomplete payment may be accomplished using the `hasIncompletePayment` method on the billable model or a subscription instance:

```php
if ($user->hasIncompletePayment('default')) {
    // ...
}

if ($user->subscription('default')->hasIncompletePayment()) {
    // ...
}
```



예외 인스턴스에서 `payment` 속성을 검사하여 미완료 결제의 구체적인 상태를 확인할 수 있습니다:

```php
use Laravel\Cashier\Exceptions\IncompletePayment;

try {
    $user->charge(1000, 'pm_card_threeDSecure2Required');
} catch (IncompletePayment $exception) {
    // Get the payment intent status...
    $exception->payment->status;

    // Check specific conditions...
    if ($exception->payment->requiresPaymentMethod()) {
        // ...
    } elseif ($exception->payment->requiresConfirmation()) {
        // ...
    }
}
```



<a name="confirming-payments"></a>
### 결제 확인

일부 결제 수단은 결제를 확인하기 위해 추가 데이터가 필요합니다. 예를 들어, SEPA 결제 수단은 결제 과정 중 추가적인 "권한" 데이터가 필요합니다. 이 데이터를 `withPaymentConfirmationOptions` 방식을 사용하여 Cashier에 제공할 수 있습니다:

```php
$subscription->withPaymentConfirmationOptions([
    'mandate_data' => '...',
])->swap('price_xxx');
```

You may consult the [Stripe API documentation](https://stripe.com/docs/api/payment_intents/confirm) to review all of the options accepted when confirming payments.

<a name="strong-customer-authentication"></a>
## Strong Customer Authentication

If your business or one of your customers is based in Europe you will need to abide by the EU's Strong Customer Authentication (SCA) regulations. These regulations were imposed in September 2019 by the European Union to prevent payment fraud. Luckily, Stripe and Cashier are prepared for building SCA compliant applications.

> [!WARNING]
> Before getting started, review [Stripe's guide on PSD2 and SCA](https://stripe.com/guides/strong-customer-authentication) as well as their [documentation on the new SCA APIs](https://stripe.com/docs/strong-customer-authentication).

<a name="payments-requiring-additional-confirmation"></a>
### Payments Requiring Additional Confirmation

SCA regulations often require extra verification in order to confirm and process a payment. When this happens, Cashier will throw a `Laravel\Cashier\Exceptions\IncompletePayment` exception that informs you that extra verification is needed. More information on how to handle these exceptions can be found in the documentation on [handling failed payments](#handling-failed-payments).

Payment confirmation screens presented by Stripe or Cashier may be tailored to a specific bank or card issuer's payment flow and can include additional card confirmation, a temporary small charge, separate device authentication, or other forms of verification.

<a name="incomplete-and-past-due-state"></a>
#### Incomplete and Past Due State

When a payment needs additional confirmation, the subscription will remain in an `incomplete` or `past_due` state as indicated by its `stripe_status` database column. Cashier will automatically activate the customer's subscription as soon as payment confirmation is complete and your application is notified by Stripe via webhook of its completion.

For more information on `incomplete` and `past_due` states, please refer to [our additional documentation on these states](#incomplete-and-past-due-status).

<a name="off-session-payment-notifications"></a>
### Off-Session Payment Notifications



SCA 규정은 고객이 구독이 활성 상태일 때에도 가끔 결제 정보를 확인하도록 요구하므로, Cashier는 세션 외 결제 확인이 필요할 때 고객에게 알림을 보낼 수 있습니다. 예를 들어, 이는 구독이 갱신될 때 발생할 수 있습니다. Cashier의 결제 알림은 `CASHIER_PAYMENT_NOTIFICATION` 환경 변수를 알림 클래스로 설정하여 활성화할 수 있습니다. 기본적으로 이 알림은 비활성화되어 있습니다. 물론, Cashier에는 이 목적을 위해 사용할 수 있는 알림 클래스가 포함되어 있지만, 원한다면 자체 알림 클래스를 제공할 수도 있습니다:

```ini
CASHIER_PAYMENT_NOTIFICATION=Laravel\Cashier\Notifications\ConfirmPayment
```



To ensure that off-session payment confirmation notifications are delivered, verify that [Stripe webhooks are configured](#handling-stripe-webhooks) for your application and the `invoice.payment_action_required` webhook is enabled in your Stripe dashboard. In addition, your `Billable` model should also use Laravel's `Illuminate\Notifications\Notifiable` trait.

> [!WARNING]
> Notifications will be sent even when customers are manually making a payment that requires additional confirmation. Unfortunately, there is no way for Stripe to know that the payment was done manually or "off-session". But, a customer will simply see a "Payment Successful" message if they visit the payment page after already confirming their payment. The customer will not be allowed to accidentally confirm the same payment twice and incur an accidental second charge.

<a name="stripe-sdk"></a>
## Stripe SDK

Many of Cashier's objects are wrappers around Stripe SDK objects. If you would like to interact with the Stripe objects directly, you may conveniently retrieve them using the `asStripe` method:

```php
$stripeSubscription = $subscription->asStripeSubscription();

$stripeSubscription->application_fee_percent = 5;

$stripeSubscription->save();
```



Stripe 구독을 직접 업데이트하려면 `updateStripeSubscription` 방법을 사용할 수도 있습니다:

```php
$subscription->updateStripeSubscription(['application_fee_percent' => 5]);
```



`Stripe\StripeClient` 클라이언트를 직접 사용하고 싶다면 `Cashier` 클래스에서 `stripe` 메서드를 호출할 수 있습니다. 예를 들어, 이 메서드를 사용하여 `StripeClient` 인스턴스에 접근하고 Stripe 계정에서 가격 목록을 가져올 수 있습니다:

```php
use Laravel\Cashier\Cashier;

$prices = Cashier::stripe()->prices->all();
```



<a name="testing"></a>
## 테스트

Cashier를 사용하는 애플리케이션을 테스트할 때 Stripe API에 대한 실제 HTTP 요청을 모킹할 수 있지만, 이는 Cashier 자체 동작을 일부 다시 구현해야 합니다. 따라서 테스트가 실제 Stripe API에 접근하도록 허용하는 것이 좋습니다. 이것은 느리지만, 애플리케이션이 예상대로 작동하고 있다는 더 큰 신뢰를 제공합니다. 느린 테스트는 별도의 Pest / PHPUnit 테스트 그룹에 넣을 수 있습니다.

테스트할 때, Cashier 자체가 이미 훌륭한 테스트 스위트를 가지고 있으므로, 자체 애플리케이션의 구독 및 결제 흐름 테스트에만 집중하고 모든 기반 Cashier 동작을 테스트할 필요는 없습니다.

시작하려면, `phpunit.xml` 파일에 Stripe 비밀키의 **testing** 버전을 추가하세요:

```xml
<env name="STRIPE_SECRET" value="sk_test_<your-key>"/>
```

이제 테스트하는 동안 Cashier와 상호작용할 때 실제 API 요청이 Stripe 테스트 환경으로 전송됩니다. 편의를 위해 테스트 중 사용할 수 있는 구독/가격으로 Stripe 테스트 계정을 미리 채워 두는 것이 좋습니다.

> [!NOTE]
> 신용카드 거부 및 실패와 같은 다양한 결제 시나리오를 테스트하기 위해 Stripe에서 제공하는 [테스트용 카드 번호 및 토큰](https://stripe.com/docs/testing)을 광범위하게 사용할 수 있습니다.
{% endraw %}
