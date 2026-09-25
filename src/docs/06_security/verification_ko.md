---
layout: docs
title: "이메일 확인"
---

{% raw %}
# 이메일 확인

- [소개](#introduction)
- [모델 준비](#model-preparation)
- [데이터베이스 준비](#database-preparation)
- [라우팅](#verification-routing)
- The Email Verification Notice(#the-email-verification-notice)
- The Email Verification Handler(#the-email-verification-handler)
- [확인 이메일 재전송](#resending-the-verification-email)
- [루트 보호](#protecting-routes)
- 커스터마이징 (#customization)
- 이벤트 (#events)

<a name="introduction"></a>
## 소개

많은 웹 애플리케이션에서는 사용자가 애플리케이션을 사용하기 전에 이메일 주소를 확인해야 합니다. Laravel 은 생성하는 각 애플리케이션에 대해 이 기능을 수동으로 다시 구현하도록 강제하는 대신， 이메일 확인 요청을 전송하고 확인하기 위한 편리한 내장 서비스를 제공합니다。

> [!NOTE]
> 빠르게 시작하고 싶으신가요？ 새로운 Laravel 애플리케이션에 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 설치하세요. 스타터 키트는 이메일 확인 지원을 포함한 전체 인증 시스템의 구축을 처리합니다。

<a name="model-preparation"></a>
### 모델 준비

시작하기 전에 `App\Models\User` 모델이 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약을 구현하는지 확인하세요：

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail
{
    use Notifiable;

    // ...
}

```

이 인터페이스가 모델에 추가되면, 새로 등록된 사용자에게 자동으로 이메일 인증 링크가 포함된 이메일이 발송됩니다. 이는 Laravel이 `Illuminate\Auth\Events\Registered` 이벤트에 대해 `Illuminate\Auth\Listeners\SendEmailVerificationNotification` [리스너](/docs/{{version}}/events)를 자동으로 등록하기 때문에 원활하게 이루어집니다.

[스타터 키트](/docs/{{version}}/starter-kits)를 사용하지 않고 애플리케이션 내에서 수동으로 등록을 구현하는 경우, 사용자의 등록이 성공한 후 `Illuminate\Auth\Events\Registered` 이벤트를 발송하고 있는지 확인해야 합니다:

```php
use Illuminate\Auth\Events\Registered;

event(new Registered($user));

```

<a name="database-preparation"></a>
### 데이터베이스 준비

다음으로， `users` 테이블에는 사용자의 이메일 주소가 확인된 날짜와 시간을 저장하는 `email_verified_at` 열이 포함되어야 합니다. 일반적으로 이는 Laravel 의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함됩니다。

<a name="verification-routing"></a>
## 라우팅

이메일 확인을 올바르게 구현하려면 세 가지 경로를 정의해야 합니다. 첫째， 등록 후 Laravel 이 보낸 확인 이메일의 이메일 확인 링크를 클릭해야 한다는 알림을 사용자에게 표시하는 경로가 필요합니다。

둘째， 사용자가 이메일에서 이메일 확인 링크를 클릭할 때 생성되는 요청을 처리하는 경로가 필요합니다。

셋째， 사용자가 실수로 첫 번째 확인 링크를 잃어버린 경우 확인 링크를 다시 전송하는 경로가 필요합니다。

<a name="the-email-verification-notice"></a>
### 이메일 확인 통지

앞서 언급했듯이， 등록 후 Laravel 이 이메일로 보낸 이메일 확인 링크를 클릭하도록 사용자에게 지시하는 뷰를 반환하는 경로를 정의해야 합니다. 이 뷰는 사용자가 먼저 이메일 주소를 확인하지 않고 애플리케이션의 다른 부분에 액세스하려고 할 때 표시됩니다. `App\Models\User` 모델이 `MustVerifyEmail` 인터페이스를 구현하는 한， 링크가 사용자에게 자동으로 이메일로 전송된다는 점을 기억하세요：

```php
Route::get('/email/verify', function () {
    return view('auth.verify-email');
})->middleware('auth')->name('verification.notice');

```

이메일 확인 알림을 반환하는 경로는 `verification.notice`로 이름을 지정해야 합니다. 사용자가 이메일 주소를 확인하지 않은 경우 `verified` 미들웨어 [Laravel에 포함됨](#protecting-routes)이 자동으로 이 경로 이름으로 리디렉션하기 때문에 경로에 정확히 이 이름을 지정하는 것이 중요합니다.

> [!NOTE]
> 이메일 확인을 수동으로 구현할 때는 확인 알림 뷰의 내용을 직접 정의해야 합니다. 필요한 모든 인증 및 확인 뷰가 포함된 스캐폴딩을 원하신다면 [Laravel 애플리케이션 스타터 킷](/docs/{{version}}/starter-kits)을 확인하세요.

<a name="the-email-verification-handler"></a>
### 이메일 확인 핸들러

다음으로, 사용자가 이메일로 받은 확인 링크를 클릭했을 때 생성되는 요청을 처리할 경로를 정의해야 합니다. 이 경로는 `verification.verify`로 이름을 지정하고 `auth` 및 `signed` 미들웨어를 할당해야 합니다:

```php
use Illuminate\Foundation\Auth\EmailVerificationRequest;

Route::get('/email/verify/{id}/{hash}', function (EmailVerificationRequest $request) {
    $request->fulfill();

    return redirect('/home');
})->middleware(['auth', 'signed'])->name('verification.verify');

```

계속하기 전에 이 경로를 자세히 살펴보겠습니다. 먼저， 일반적인 `Illuminate\Http\Request` 인스턴스 대신 `EmailVerificationRequest` 요청 유형을 사용하고 있음을 알 수 있습니다. `EmailVerificationRequest` 는 Laravel 에 포함된 [형식 요청](/docs/{{version}}/validation#form-request-validation) 입니다. 이 요청은 요청의 `id` 및 `hash` 파라미터를 자동으로 검증합니다。

다음으로， 요청에서 `fulfill` 메서드를 직접 호출할 수 있습니다. 이 메서드는 인증된 사용자에 대해 `markEmailAsVerified` 메서드를 호출하고 `Illuminate\Auth\Events\Verified` 이벤트를 전송합니다. `markEmailAsVerified` 메서드는 `Illuminate\Foundation\Auth\User` 기본 클래스를 통해 기본 `App\Models\User` 모델에서 사용할 수 있습니다. 사용자의 이메일 주소가 확인되면 원하는 곳으로 리디렉션할 수 있습니다。

<a name="resending-the-verification-email"></a>
### 확인 이메일 재전송

때때로 사용자가 이메일 주소 확인 이메일을 잘못 찾거나 실수로 삭제할 수 있습니다. 이를 수용하기 위해 사용자가 확인 이메일을 삭제하도록 요청할 수 있는 경로를 정의할 수 있습니다. 그런 다음 [확인 알림 뷰](#the-email-verification-notice) 내에 간단한 양식 제출 버튼을 배치하여 이 경로에 요청할 수 있습니다：

```php
use Illuminate\Http\Request;

Route::post('/email/verification-notification', function (Request $request) {
    $request->user()->sendEmailVerificationNotification();

    return back()->with('message', 'Verification link sent!');
})->middleware(['auth', 'throttle:6,1'])->name('verification.send');

```

<a name="protecting-routes"></a>
### 라우트 보호하기

[라우트 미들웨어](/docs/{{version}}/middleware)는 특정 라우트에 대해 인증된 사용자만 접근할 수 있도록 하는 데 사용될 수 있습니다. Laravel에는 `verified` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)이 포함되어 있으며, 이는 `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어 클래스의 별칭입니다. 이 별칭은 이미 Laravel에 의해 자동으로 등록되어 있으므로, 라우트 정의에 `verified` 미들웨어를 붙이기만 하면 됩니다. 일반적으로 이 미들웨어는 `auth` 미들웨어와 함께 사용됩니다:

```php
Route::get('/profile', function () {
    // Only verified users may access this route...
})->middleware(['auth', 'verified']);

```

검증되지 않은 사용자가 이 미들웨어가 할당된 경로에 접근하려고 하면, 자동으로 `verification.notice` [명명된 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션됩니다.

<a name="customization"></a>
## 사용자 정의

<a name="verification-email-customization"></a>
#### 이메일 인증 사용자 정의

기본 이메일 인증 알림은 대부분의 애플리케이션 요구 사항을 충족하지만, Laravel에서는 이메일 인증 메일 메시지가 구성되는 방법을 사용자 정의할 수 있습니다.

시작하려면 `Illuminate\Auth\Notifications\VerifyEmail` 알림에서 제공하는 `toMailUsing` 메서드에 클로저를 전달하십시오. 클로저는 알림을 받는 노티파이 가능 모델 인스턴스와 이메일 주소를 인증하기 위해 사용자가 방문해야 하는 서명된 이메일 인증 URL을 받게 됩니다. 클로저는 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다. 일반적으로 애플리케이션의 `AppServiceProvider` 클래스에서 `boot` 메서드로부터 `toMailUsing` 메서드를 호출해야 합니다.

```php
use Illuminate\Auth\Notifications\VerifyEmail;
use Illuminate\Notifications\Messages\MailMessage;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // ...

    VerifyEmail::toMailUsing(function (object $notifiable, string $url) {
        return (new MailMessage)
            ->subject('Verify Email Address')
            ->line('Click the button below to verify your email address.')
            ->action('Verify Email Address', $url);
    });
}

```

> [!NOTE]
> 메일 알림에 대해 더 알아보려면, [메일 알림 문서](/docs/{{version}}/notifications#mail-notifications)를 참고하십시오.

<a name="events"></a>
## 이벤트

[Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용할 때, Laravel은 이메일 인증 과정 중에 `Illuminate\Auth\Events\Verified` [이벤트](/docs/{{version}}/events)를 발생시킵니다. 애플리케이션에서 이메일 인증을 수동으로 처리하는 경우, 인증 완료 후 이러한 이벤트를 수동으로 발생시키고자 할 수 있습니다.
{% endraw %}
