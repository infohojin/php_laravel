---
layout: docs
title: "Laravel Fortify"
---

{% raw %}
# Laravel Fortify

- [Introduction](#introduction)
    - [What is Fortify?](#what-is-fortify)
    - [When Should I Use Fortify?](#when-should-i-use-fortify)
- [Installation](#installation)
    - [Fortify Features](#fortify-features)
    - [Disabling Views](#disabling-views)
- [Authentication](#authentication)
    - [Customizing User Authentication](#customizing-user-authentication)
    - [Customizing the Authentication Pipeline](#customizing-the-authentication-pipeline)
    - [Customizing Redirects](#customizing-authentication-redirects)
- [Two-Factor Authentication](#two-factor-authentication)
    - [Enabling Two-Factor Authentication](#enabling-two-factor-authentication)
    - [Authenticating With Two-Factor Authentication](#authenticating-with-two-factor-authentication)
    - [Disabling Two-Factor Authentication](#disabling-two-factor-authentication)
- [Passkeys](#passkeys)
    - [Enabling Passkeys](#enabling-passkeys)
    - [JavaScript Client](#passkeys-javascript-client)
    - [Authenticating With Passkeys](#authenticating-with-passkeys)
    - [Confirming Password With Passkeys](#confirming-password-with-passkeys)
    - [Registering Passkeys](#registering-passkeys)
    - [Deleting Passkeys](#deleting-passkeys)
- [Registration](#registration)
    - [Customizing Registration](#customizing-registration)
- [Password Reset](#password-reset)
    - [Requesting a Password Reset Link](#requesting-a-password-reset-link)
    - [Resetting the Password](#resetting-the-password)
    - [Customizing Password Resets](#customizing-password-resets)
- [Email Verification](#email-verification)
    - [Protecting Routes](#protecting-routes)
- [Password Confirmation](#password-confirmation)

<a name="introduction"></a>
## Introduction

[Laravel Fortify](https://github.com/laravel/fortify) is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more. After installing Fortify, you may run the `route:list` Artisan command to see the routes that Fortify has registered.

Since Fortify does not provide its own user interface, it is meant to be paired with your own user interface which makes requests to the routes it registers. We will discuss exactly how to make requests to these routes in the remainder of this documentation.

> [!NOTE]
> Remember, Fortify is a package that is meant to give you a head start implementing Laravel's authentication features. **You are not required to use it.** You are always free to manually interact with Laravel's authentication services by following the documentation available in the [authentication](/docs/{{version}}/authentication), [password reset](/docs/{{version}}/passwords), and [email verification](/docs/{{version}}/verification) documentation.

<a name="what-is-fortify"></a>
### What is Fortify?

As mentioned previously, Laravel Fortify is a frontend agnostic authentication backend implementation for Laravel. Fortify registers the routes and controllers needed to implement all of Laravel's authentication features, including login, registration, password reset, email verification, and more.

**You are not required to use Fortify in order to use Laravel's authentication features.** You are always free to manually interact with Laravel's authentication services by following the documentation available in the [authentication](/docs/{{version}}/authentication), [password reset](/docs/{{version}}/passwords), and [email verification](/docs/{{version}}/verification) documentation.

If you are new to Laravel, you may wish to explore [our application starter kits](/docs/{{version}}/starter-kits). Laravel's application starter kits use Fortify internally to provide authentication scaffolding for your application that includes a user interface built with [Tailwind CSS](https://tailwindcss.com). This allows you to study and get comfortable with Laravel's authentication features.

Laravel Fortify essentially takes the routes and controllers of our application starter kits and offers them as a package that does not include a user interface. This allows you to still quickly scaffold the backend implementation of your application's authentication layer without being tied to any particular frontend opinions.

<a name="when-should-i-use-fortify"></a>
### When Should I Use Fortify?

You may be wondering when it is appropriate to use Laravel Fortify. First, if you are using one of Laravel's [application starter kits](/docs/{{version}}/starter-kits), you do not need to install Laravel Fortify since all of Laravel's application starter kits use Fortify and already provide a full authentication implementation.



If you are not using an application starter kit and your application needs authentication features, you have two options: manually implement your application's authentication features or use Laravel Fortify to provide the backend implementation of these features.

If you choose to install Fortify, your user interface will make requests to Fortify's authentication routes that are detailed in this documentation in order to authenticate and register users.

If you choose to manually interact with Laravel's authentication services instead of using Fortify, you may do so by following the documentation available in the [authentication](/docs/{{version}}/authentication), [password reset](/docs/{{version}}/passwords), and [email verification](/docs/{{version}}/verification) documentation.

<a name="laravel-fortify-and-laravel-sanctum"></a>
#### Laravel Fortify and Laravel Sanctum

Some developers become confused regarding the difference between [Laravel Sanctum](/docs/{{version}}/sanctum) and Laravel Fortify. Because the two packages solve two different but related problems, Laravel Fortify and Laravel Sanctum are not mutually exclusive or competing packages.

Laravel Sanctum is only concerned with managing API tokens and authenticating existing users using session cookies or tokens. Sanctum does not provide any routes that handle user registration, password reset, etc.

If you are attempting to manually build the authentication layer for an application that offers an API or serves as the backend for a single-page application, it is entirely possible that you will utilize both Laravel Fortify (for user registration, password reset, etc.) and Laravel Sanctum (API token management, session authentication).

<a name="installation"></a>
## Installation

To get started, install Fortify using the Composer package manager:

```shell
composer require laravel/fortify
```



다음으로, `fortify:install` Artisan 명령을 사용하여 Fortify의 리소스를 게시하세요:

```shell
php artisan fortify:install
```



이 명령은 Fortify의 작업을 `app/Actions` 디렉토리에 게시합니다. 해당 디렉토리가 존재하지 않으면 생성됩니다. 또한 `FortifyServiceProvider` 구성 파일과 모든 필요한 데이터베이스 마이그레이션이 게시됩니다.

다음으로, 데이터베이스를 마이그레이션해야 합니다:

```shell
php artisan migrate
```



<a name="fortify-features"></a>
### Fortify 기능

`fortify` 구성 파일에는 `features` 구성 배열이 포함되어 있습니다. 이 배열은 Fortify가 기본적으로 노출할 백엔드 경로/기능을 정의합니다. 대부분의 Laravel 애플리케이션에서 제공하는 기본 인증 기능인 다음 기능만 활성화하는 것을 권장합니다:

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
],
```



<a name="disabling-views"></a>
### 뷰 비활성화

기본적으로 Fortify는 로그인 화면이나 등록 화면과 같이 뷰를 반환하도록 의도된 라우트를 정의합니다. 그러나 JavaScript 기반 싱글 페이지 애플리케이션을 구축하는 경우 이러한 라우트가 필요하지 않을 수 있습니다. 이러한 이유로, 애플리케이션의 `config/fortify.php` 설정 파일 내에서 `views` 구성 값을 `false`로 설정하여 이러한 라우트를 완전히 비활성화할 수 있습니다:

```php
'views' => false,
```



<a name="disabling-views-and-password-reset"></a>
#### Disabling Views and Password Reset

If you choose to disable Fortify's views and you will be implementing password reset features for your application, you should still define a route named `password.reset` that is responsible for displaying your application's "reset password" view. This is necessary because Laravel's `Illuminate\Auth\Notifications\ResetPassword` notification will generate the password reset URL via the `password.reset` named route.

<a name="authentication"></a>
## Authentication

To get started, we need to instruct Fortify how to return our "login" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/{{version}}/starter-kits).

All of the authentication view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class. Fortify will take care of defining the `/login` route that returns this view:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ...
}
```



Your login template should include a form that makes a POST request to `/login`. The `/login` endpoint expects a string `email` / `username` and a `password`. The name of the email / username field should match the `username` value within the `config/fortify.php` configuration file. In addition, a boolean `remember` field may be provided to indicate that the user would like to use the "remember me" functionality provided by Laravel.

If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned.

If the request was not successful, the user will be redirected back to the login screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/{{version}}/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with the 422 HTTP response.

<a name="customizing-user-authentication"></a>
### Customizing User Authentication

Fortify will automatically retrieve and authenticate the user based on the provided credentials and the authentication guard that is configured for your application. However, you may sometimes wish to have full customization over how login credentials are authenticated and users are retrieved. Thankfully, Fortify allows you to easily accomplish this using the `Fortify::authenticateUsing` method.

This method accepts a closure which receives the incoming HTTP request. The closure is responsible for validating the login credentials attached to the request and returning the associated user instance. If the credentials are invalid or no user can be found, `null` or `false` should be returned by the closure. Typically, this method should be called from the `boot` method of your `FortifyServiceProvider`:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::authenticateUsing(function (Request $request) {
        $user = User::where('email', $request->email)->first();

        if ($user &&
            Hash::check($request->password, $user->password)) {
            return $user;
        }
    });

    // ...
}
```



<a name="authentication-guard"></a>
#### Authentication Guard

You may customize the authentication guard used by Fortify within your application's `fortify` configuration file. However, you should ensure that the configured guard is an implementation of `Illuminate\Contracts\Auth\StatefulGuard`. If you are attempting to use Laravel Fortify to authenticate an SPA, you should use Laravel's default `web` guard in combination with [Laravel Sanctum](https://laravel.com/docs/sanctum).

<a name="customizing-the-authentication-pipeline"></a>
### Customizing the Authentication Pipeline

Laravel Fortify authenticates login requests through a pipeline of invokable classes. If you would like, you may define a custom pipeline of classes that login requests should be piped through. Each class should have an `__invoke` method which receives the incoming `Illuminate\Http\Request` instance and, like [middleware](/docs/{{version}}/middleware), a `$next` variable that is invoked in order to pass the request to the next class in the pipeline.

To define your custom pipeline, you may use the `Fortify::authenticateThrough` method. This method accepts a closure which should return the array of classes to pipe the login request through. Typically, this method should be called from the `boot` method of your `App\Providers\FortifyServiceProvider` class.

The example below contains the default pipeline definition that you may use as a starting point when making your own modifications:

```php
use Laravel\Fortify\Actions\AttemptToAuthenticate;
use Laravel\Fortify\Actions\CanonicalizeUsername;
use Laravel\Fortify\Actions\EnsureLoginIsNotThrottled;
use Laravel\Fortify\Actions\PrepareAuthenticatedSession;
use Laravel\Fortify\Actions\RedirectIfTwoFactorAuthenticatable;
use Laravel\Fortify\Features;
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

Fortify::authenticateThrough(function (Request $request) {
    return array_filter([
            config('fortify.limiters.login') ? null : EnsureLoginIsNotThrottled::class,
            config('fortify.lowercase_usernames') ? CanonicalizeUsername::class : null,
            Features::enabled(Features::twoFactorAuthentication()) ? RedirectIfTwoFactorAuthenticatable::class : null,
            AttemptToAuthenticate::class,
            PrepareAuthenticatedSession::class,
    ]);
});
```



#### Authentication Throttling

By default, Fortify will throttle authentication attempts using the `EnsureLoginIsNotThrottled` middleware. This middleware throttles attempts that are unique to a username and IP address combination.

Some applications may require a different approach to throttling authentication attempts, such as throttling by IP address alone. Therefore, Fortify allows you to specify your own [rate limiter](/docs/{{version}}/routing#rate-limiting) via the `fortify.limiters.login` configuration option. Of course, this configuration option is located in your application's `config/fortify.php` configuration file.

> [!NOTE]
> Utilizing a mixture of throttling, [two-factor authentication](/docs/{{version}}/fortify#two-factor-authentication), and an external web application firewall (WAF) will provide the most robust defense for your legitimate application users.

<a name="customizing-authentication-redirects"></a>
### Customizing Redirects

If the login attempt is successful, Fortify will redirect you to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 200 HTTP response will be returned. After a user logs out of the application, the user will be redirected to the `/` URI.

If you need advanced customization of this behavior, you may bind implementations of the `LoginResponse` and `LogoutResponse` contracts into the Laravel [service container](/docs/{{version}}/container). Typically, this should be done within the `register` method of your application's `App\Providers\FortifyServiceProvider` class:

```php
use Laravel\Fortify\Contracts\LogoutResponse;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->instance(LogoutResponse::class, new class implements LogoutResponse {
        public function toResponse($request)
        {
            return redirect('/');
        }
    });
}
```



<a name="two-factor-authentication"></a>
## 2단계 인증

Fortify의 2단계 인증 기능이 활성화되면, 사용자는 인증 과정에서 6자리 숫자 토큰을 입력해야 합니다. 이 토큰은 시간 기반 일회용 비밀번호(TOTP)를 사용하여 생성되며, Google Authenticator와 같은 TOTP 호환 모바일 인증 애플리케이션에서 확인할 수 있습니다.

시작하기 전에, 먼저 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\TwoFactorAuthenticatable` 트레이트를 사용하는지 확인해야 합니다.

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\TwoFactorAuthenticatable;

class User extends Authenticatable
{
    use Notifiable, TwoFactorAuthenticatable;
}
```



Next, you should build a screen within your application where users can manage their two-factor authentication settings. This screen should allow the user to enable and disable two-factor authentication, as well as regenerate their two-factor authentication recovery codes.

> By default, the `features` array of the `fortify` configuration file instructs Fortify's two-factor authentication settings to require password confirmation before modification. Therefore, your application should implement Fortify's [password confirmation](#password-confirmation) feature before continuing.

<a name="enabling-two-factor-authentication"></a>
### Enabling Two-Factor Authentication

To begin enabling two-factor authentication, your application should make a POST request to the `/user/two-factor-authentication` endpoint defined by Fortify. If the request is successful, the user will be redirected back to the previous URL and the `status` session variable will be set to `two-factor-authentication-enabled`. You may detect this `status` session variable within your templates to display the appropriate success message. If the request was an XHR request, `200` HTTP response will be returned.

After choosing to enable two-factor authentication, the user must still "confirm" their two-factor authentication configuration by providing a valid two-factor authentication code. So, your "success" message should instruct the user that two-factor authentication confirmation is still required:

```html
@if (session('status') == 'two-factor-authentication-enabled')
    <div class="mb-4 font-medium text-sm">
        Please finish configuring two-factor authentication below.
    </div>
@endif
```



다음으로, 사용자가 인증기 애플리케이션에 스캔할 수 있도록 이중 인증 QR 코드를 표시해야 합니다. 애플리케이션의 프런트엔드를 Blade를 사용하여 렌더링하는 경우, 사용자 인스턴스에서 사용할 수 있는 `twoFactorQrCodeSvg` 메서드를 사용하여 QR 코드 SVG를 가져올 수 있습니다:

```php
$request->user()->twoFactorQrCodeSvg();
```



만약 자바스크립트 기반 프런트엔드를 구축하고 있다면, 사용자의 이중 인증 QR 코드를 가져오기 위해 `/user/two-factor-qr-code` 엔드포인트에 XHR GET 요청을 할 수 있습니다. 이 엔드포인트는 `svg` 키를 포함한 JSON 객체를 반환합니다.

<a name="confirming-two-factor-authentication"></a>
#### 이중 인증 확인

사용자의 이중 인증 QR 코드를 표시하는 것 외에도, 사용자가 유효한 인증 코드를 입력하여 이중 인증 구성을 "확인"할 수 있는 텍스트 입력란을 제공해야 합니다. 이 코드는 Fortify에서 정의한 `/user/confirmed-two-factor-authentication` 엔드포인트로 POST 요청을 통해 라라벨(Laravel) 애플리케이션에 전달되어야 합니다.

요청이 성공하면, 사용자는 이전 URL로 리디렉션되며 `status` 세션 변수는 `two-factor-authentication-confirmed`로 설정됩니다:

```html
@if (session('status') == 'two-factor-authentication-confirmed')
    <div class="mb-4 font-medium text-sm">
        Two-factor authentication confirmed and enabled successfully.
    </div>
@endif
```



두 요소 인증 확인 엔드포인트에 대한 요청이 XHR 요청을 통해 이루어진 경우, `200` HTTP 응답이 반환됩니다.

<a name="displaying-the-recovery-codes"></a>
#### 복구 코드 표시

사용자의 두 요소 복구 코드도 표시해야 합니다. 이 복구 코드를 통해 사용자는 모바일 기기에 접근할 수 없는 경우에도 인증할 수 있습니다. 애플리케이션의 프론트엔드를 Blade로 렌더링하는 경우, 인증된 사용자 인스턴스를 통해 복구 코드에 접근할 수 있습니다:

```php
(array) $request->user()->recoveryCodes();
```



If you are building a JavaScript powered frontend, you may make an XHR GET request to the `/user/two-factor-recovery-codes` endpoint. This endpoint will return a JSON array containing the user's recovery codes.

To regenerate the user's recovery codes, your application should make a POST request to the `/user/two-factor-recovery-codes` endpoint.

<a name="authenticating-with-two-factor-authentication"></a>
### Authenticating With Two-Factor Authentication

During the authentication process, Fortify will automatically redirect the user to your application's two-factor authentication challenge screen. However, if your application is making an XHR login request, the JSON response returned after a successful authentication attempt will contain a JSON object that has a `two_factor` boolean property. You should inspect this value to know whether you should redirect to your application's two-factor authentication challenge screen.

To begin implementing two-factor authentication functionality, we need to instruct Fortify how to return our two-factor authentication challenge view. All of Fortify's authentication view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::twoFactorChallengeView(function () {
        return view('auth.two-factor-challenge');
    });

    // ...
}
```



Fortify will take care of defining the `/two-factor-challenge` route that returns this view. Your `two-factor-challenge` template should include a form that makes a POST request to the `/two-factor-challenge` endpoint. The `/two-factor-challenge` action expects a `code` field that contains a valid TOTP token or a `recovery_code` field that contains one of the user's recovery codes.

If the login attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the login request was an XHR request, a 204 HTTP response will be returned.

If the request was not successful, the user will be redirected back to the two-factor challenge screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/{{version}}/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response.

<a name="disabling-two-factor-authentication"></a>
### Disabling Two-Factor Authentication

To disable two-factor authentication, your application should make a DELETE request to the `/user/two-factor-authentication` endpoint. Remember, Fortify's two-factor authentication endpoints require [password confirmation](#password-confirmation) prior to being called.

<a name="passkeys"></a>
## Passkeys

Fortify supports passkey authentication using WebAuthn. Passkeys allow users to authenticate without passwords using platform authenticators such as Face ID, Touch ID, Windows Hello, or hardware security keys.

<a name="enabling-passkeys"></a>
### Enabling Passkeys

To get started, ensure the `passkeys` feature is enabled in your application's `fortify` configuration file:

```php
use Laravel\Fortify\Features;

'features' => [
    // ...
    Features::passkeys([
        'confirmPassword' => true,
    ]),
],
```



`confirmPassword` 옵션은 Fortify가 패스키를 등록하거나 삭제하기 전에 [비밀번호 확인](#password-confirmation)을 요구할지 여부를 결정합니다.

다음으로, 애플리케이션의 `App\Models\User` 모델이 `Laravel\Fortify\Contracts\PasskeyUser`를 구현하고 `Laravel\Fortify\PasskeyAuthenticatable` 트레이트를 사용하는지 확인하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Fortify\Contracts\PasskeyUser;
use Laravel\Fortify\PasskeyAuthenticatable;

class User extends Authenticatable implements PasskeyUser
{
    use Notifiable, PasskeyAuthenticatable;
}
```



Fortify의 패스키 구성 옵션은 애플리케이션의 `config/fortify.php` 파일에 있는 `passkeys` 구성 배열을 사용하여 사용자 정의할 수 있습니다:

```php
'passkeys' => [
    'relying_party_id' => parse_url(config('app.url'), PHP_URL_HOST),
    'allowed_origins' => [config('app.url')],
    'user_handle_secret' => config('app.key'),
    'timeout' => 60000,
],
```



> [!NOTE]
> Fortify wraps the `laravel/passkeys` Composer package and configures it for you. If you are using Fortify's passkeys feature, you should configure passkeys using your application's `config/fortify.php` file. You do not need to publish the `laravel/passkeys` configuration file, and any values defined there will be overridden by Fortify.

The `relying_party_id` should match your application's domain. The `allowed_origins` array lists the browser origins that may complete passkey registration and authentication. The `user_handle_secret` is used to derive opaque user identifiers, ensuring the same user is recognized across passkey registrations. The `timeout` option controls how long passkey registration and authentication operations may remain active.

Fortify applies a dedicated passkeys rate limiter to its passkey login, confirmation, and registration routes. If needed, you may customize it using the `fortify.limiters.passkeys` configuration option and a corresponding `RateLimiter::for(...)` definition.

<a name="passkeys-javascript-client"></a>
### JavaScript Client

If you are building a custom frontend, including a Blade application with browser-side scripts, you may use the official [`@laravel/passkeys`](https://www.npmjs.com/package/@laravel/passkeys) package. This package handles browser WebAuthn ceremonies and sends requests to Fortify's passkey endpoints.

Install the package via npm:

```shell
npm install @laravel/passkeys
```



그런 다음, 프론트엔드에서 패스키 등록 및 인증을 시작할 수 있습니다:

```js
import { Passkeys } from "@laravel/passkeys";

await Passkeys.register({ name: "MacBook Pro" });
await Passkeys.verify();
```



애플리케이션이 사용자 정의 패스키 엔드포인트 URI를 사용하는 경우, 호출별로 라우트를 재정의할 수 있습니다:

```js
await Passkeys.verify({
    routes: {
        options: "/passkeys/confirm/options",
        submit: "/passkeys/confirm",
    },
});

await Passkeys.register({
    name: "MacBook Pro",
    routes: {
        options: "/user/passkeys/options",
        submit: "/user/passkeys",
    },
});
```

The package also provides React, Vue, and Svelte helpers via `@laravel/passkeys/react`, `@laravel/passkeys/vue`, and `@laravel/passkeys/svelte`.

<a name="authenticating-with-passkeys"></a>
### Authenticating With Passkeys

To authenticate a user with a passkey, your application should first make a GET request to the `/passkeys/login/options` endpoint. This endpoint returns the WebAuthn challenge options that your frontend should pass to `navigator.credentials.get(...)`.

After the browser returns a credential, your application should make a POST request to `/passkeys/login` with the credential payload. You may also include a boolean `remember` field.

If the request is successful, Fortify will log the user into the configured guard and return either:

<div class="content-list" markdown="1">

- A redirect response to your intended destination for standard requests.
- A `200` HTTP response containing a JSON payload with a `redirect` key for XHR requests.

</div>

<a name="confirming-password-with-passkeys"></a>
### Confirming Password With Passkeys

For authenticated sessions, Fortify provides passkey confirmation endpoints that satisfy Laravel's password confirmation requirement for the current session.

To confirm with a passkey, your application should first make a GET request to `/passkeys/confirm/options`. This endpoint returns the WebAuthn challenge options that your frontend should pass to `navigator.credentials.get(...)`.

After the browser returns a credential, your application should make a POST request to `/passkeys/confirm` with the credential payload.

If the request is successful, Fortify marks the current session as password confirmed and returns either:

<div class="content-list" markdown="1">

- A redirect response to your intended destination for standard requests.
- A `200` HTTP response containing a JSON payload with a `redirect` key for XHR requests.

</div>

<a name="registering-passkeys"></a>
### Registering Passkeys

To register a passkey for an authenticated user, your application should first make a GET request to `/user/passkeys/options`. This endpoint returns the WebAuthn creation options that your frontend should pass to `navigator.credentials.create(...)`.



After the browser returns a credential, your application should make a POST request to `/user/passkeys` with a `name` field and a `credential` field containing the serialized [`PublicKeyCredential`](https://developer.mozilla.org/en-US/docs/Web/API/PublicKeyCredential) object returned by `navigator.credentials.create(...)`.

If the request is successful, Fortify will return either:

<div class="content-list" markdown="1">

- A redirect back response with a `passkey-registered` status in the session for standard requests.
- A `200` HTTP response with a JSON payload containing a `status` key, along with the newly registered passkey's `id` and `name`.

</div>

<a name="deleting-passkeys"></a>
### Deleting Passkeys

To delete a passkey, your application should make a DELETE request to `/user/passkeys/{passkey}`.

If the request is successful, Fortify will return either:

<div class="content-list" markdown="1">

- A redirect back response with a `passkey-deleted` status in the session for standard requests.
- A `200` HTTP response with a JSON payload containing a `status` key for XHR requests.

</div>

<a name="registration"></a>
## Registration

To begin implementing our application's registration functionality, we need to instruct Fortify how to return our "register" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/{{version}}/starter-kits).

All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your `App\Providers\FortifyServiceProvider` class:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ...
}
```



Fortify will take care of defining the `/register` route that returns this view. Your `register` template should include a form that makes a POST request to the `/register` endpoint defined by Fortify.

The `/register` endpoint expects a string `name`, string email address / username, `password`, and `password_confirmation` fields. The name of the email / username field should match the `username` configuration value defined within your application's `fortify` configuration file.

If the registration attempt is successful, Fortify will redirect the user to the URI configured via the `home` configuration option within your application's `fortify` configuration file. If the request was an XHR request, a 201 HTTP response will be returned.

If the request was not successful, the user will be redirected back to the registration screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/{{version}}/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response.

<a name="customizing-registration"></a>
### Customizing Registration

The user validation and creation process may be customized by modifying the `App\Actions\Fortify\CreateNewUser` action that was generated when you installed Laravel Fortify.

<a name="password-reset"></a>
## Password Reset

<a name="requesting-a-password-reset-link"></a>
### Requesting a Password Reset Link

To begin implementing our application's password reset functionality, we need to instruct Fortify how to return our "forgot password" view. Remember, Fortify is a headless authentication library. If you would like a frontend implementation of Laravel's authentication features that are already completed for you, you should use an [application starter kit](/docs/{{version}}/starter-kits).

All of Fortify's view rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::requestPasswordResetLinkView(function () {
        return view('auth.forgot-password');
    });

    // ...
}
```



Fortify will take care of defining the `/forgot-password` endpoint that returns this view. Your `forgot-password` template should include a form that makes a POST request to the `/forgot-password` endpoint.

The `/forgot-password` endpoint expects a string `email` field. The name of this field / database column should match the `email` configuration value within your application's `fortify` configuration file.

<a name="handling-the-password-reset-link-request-response"></a>
#### Handling the Password Reset Link Request Response

If the password reset link request was successful, Fortify will redirect the user back to the `/forgot-password` endpoint and send an email to the user with a secure link they can use to reset their password. If the request was an XHR request, a 200 HTTP response will be returned.

After being redirected back to the `/forgot-password` endpoint after a successful request, the `status` session variable may be used to display the status of the password reset link request attempt.

The value of the `$status` session variable will match one of the translation strings defined within your application's `passwords` [language file](/docs/{{version}}/localization). If you would like to customize this value and have not published Laravel's language files, you may do so via the `lang:publish` Artisan command:

```html
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```



요청이 성공하지 못한 경우, 사용자는 요청 비밀번호 재설정 링크 화면으로 다시 리다이렉트되며, 검증 오류는 공유된 `$errors` [Blade 템플릿 변수](/docs/{{version}}/validation#quick-displaying-the-validation-errors)를 통해 확인할 수 있습니다. 또는 XHR 요청의 경우, 검증 오류는 422 HTTP 응답과 함께 반환됩니다.

<a name="resetting-the-password"></a>
### 비밀번호 재설정

애플리케이션의 비밀번호 재설정 기능을 구현을 완료하기 위해, Fortify에게 "비밀번호 재설정" 뷰를 반환하는 방법을 알려줄 필요가 있습니다.

Fortify의 모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스에서 제공하는 적절한 메서드를 사용하여 커스터마이즈할 수 있습니다. 일반적으로, 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 이 메서드를 호출해야 합니다:

```php
use Laravel\Fortify\Fortify;
use Illuminate\Http\Request;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::resetPasswordView(function (Request $request) {
        return view('auth.reset-password', ['request' => $request]);
    });

    // ...
}
```



Fortify는 이 뷰를 표시할 경로를 정의하는 작업을 처리합니다. 귀하의 `reset-password` 템플릿에는 `/reset-password`로 POST 요청을 보내는 폼이 포함되어야 합니다.

`/reset-password` 엔드포인트는 문자열 `email` 필드, `password` 필드, `password_confirmation` 필드와 `request()->route('token')` 값을 포함한 `token`라는 이름의 숨겨진 필드를 기대합니다. "email" 필드/데이터베이스 열의 이름은 애플리케이션의 `fortify` 구성 파일 내에 정의된 `email` 구성 값과 일치해야 합니다.

<a name="handling-the-password-reset-response"></a>
#### 비밀번호 재설정 응답 처리

비밀번호 재설정 요청이 성공하면 Fortify는 사용자가 새 비밀번호로 로그인할 수 있도록 `/login` 경로로 다시 리디렉션합니다. 또한 `status` 세션 변수가 설정되어 로그인 화면에서 재설정 성공 상태를 표시할 수 있습니다.

```blade
@if (session('status'))
    <div class="mb-4 font-medium text-sm text-green-600">
        {{ session('status') }}
    </div>
@endif
```



If the request was an XHR request, a 200 HTTP response will be returned.

If the request was not successful, the user will be redirected back to the reset password screen and the validation errors will be available to you via the shared `$errors` [Blade template variable](/docs/{{version}}/validation#quick-displaying-the-validation-errors). Or, in the case of an XHR request, the validation errors will be returned with a 422 HTTP response.

<a name="customizing-password-resets"></a>
### Customizing Password Resets

The password reset process may be customized by modifying the `App\Actions\ResetUserPassword` action that was generated when you installed Laravel Fortify.

<a name="email-verification"></a>
## Email Verification

After registration, you may wish for users to verify their email address before they continue accessing your application. To get started, ensure the `emailVerification` feature is enabled in your `fortify` configuration file's `features` array. Next, you should ensure that your `App\Models\User` class implements the `Illuminate\Contracts\Auth\MustVerifyEmail` interface.

Once these two setup steps have been completed, newly registered users will receive an email prompting them to verify their email address ownership. However, we need to inform Fortify how to display the email verification screen which informs the user that they need to go click the verification link in the email.

All of Fortify's view's rendering logic may be customized using the appropriate methods available via the `Laravel\Fortify\Fortify` class. Typically, you should call this method from the `boot` method of your application's `App\Providers\FortifyServiceProvider` class:

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::verifyEmailView(function () {
        return view('auth.verify-email');
    });

    // ...
}
```



Fortify will take care of defining the route that displays this view when a user is redirected to the `/email/verify` endpoint by Laravel's built-in `verified` middleware.

Your `verify-email` template should include an informational message instructing the user to click the email verification link that was sent to their email address.

<a name="resending-email-verification-links"></a>
#### Resending Email Verification Links

If you wish, you may add a button to your application's `verify-email` template that triggers a POST request to the `/email/verification-notification` endpoint. When this endpoint receives a request, a new verification email link will be emailed to the user, allowing the user to get a new verification link if the previous one was accidentally deleted or lost.

If the request to resend the verification link email was successful, Fortify will redirect the user back to the `/email/verify` endpoint with a `status` session variable, allowing you to display an informational message to the user informing them the operation was successful. If the request was an XHR request, a 202 HTTP response will be returned:

```blade
@if (session('status') == 'verification-link-sent')
    <div class="mb-4 font-medium text-sm text-green-600">
        A new email verification link has been emailed to you!
    </div>
@endif
```



<a name="protecting-routes"></a>
### 라우트 보호

라우트나 라우트 그룹이 사용자가 이메일 주소를 확인했는지 요구하도록 지정하려면, Laravel의 내장 `verified` 미들웨어를 라우트에 연결해야 합니다. `verified` 미들웨어 별칭은 Laravel에 의해 자동으로 등록되며, `Illuminate\Auth\Middleware\EnsureEmailIsVerified` 미들웨어의 별칭으로 사용됩니다:

```php
Route::get('/dashboard', function () {
    // ...
})->middleware(['verified']);
```



<a name="password-confirmation"></a>
## 비밀번호 확인

애플리케이션을 개발하는 동안, 특정 작업을 수행하기 전에 사용자가 비밀번호를 확인하도록 요구해야 하는 경우가 있습니다. 일반적으로 이러한 경로는 Laravel의 내장 `password.confirm` 미들웨어로 보호됩니다.

비밀번호 확인 기능을 구현하려면, Fortify에게 애플리케이션의 '비밀번호 확인' 뷰를 반환하는 방법을 알려야 합니다. Fortify는 헤드리스 인증 라이브러리라는 점을 기억하세요. 이미 완성된 Laravel 인증 기능의 프런트엔드 구현을 원하신다면 [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)를 사용하셔야 합니다.

Fortify의 모든 뷰 렌더링 로직은 `Laravel\Fortify\Fortify` 클래스를 통해 제공되는 적절한 메서드를 사용하여 사용자 정의할 수 있습니다. 일반적으로, 애플리케이션의 `App\Providers\FortifyServiceProvider` 클래스의 `boot` 메서드에서 이 메서드를 호출해야 합니다.

```php
use Laravel\Fortify\Fortify;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Fortify::confirmPasswordView(function () {
        return view('auth.confirm-password');
    });

    // ...
}
```

Fortify는 이 뷰를 반환하는 `/user/confirm-password` 엔드포인트를 정의하는 작업을 처리합니다. 귀하의 `confirm-password` 템플릿에는 `/user/confirm-password` 엔드포인트로 POST 요청을 보내는 폼이 포함되어야 합니다. `/user/confirm-password` 엔드포인트는 사용자의 현재 비밀번호를 포함하는 `password` 필드를 기대합니다.

비밀번호가 사용자의 현재 비밀번호와 일치하면, Fortify는 사용자를 접근하려던 경로로 리디렉션합니다. 요청이 XHR 요청인 경우, 201 HTTP 응답이 반환됩니다.

요청이 성공하지 못하면, 사용자는 비밀번호 확인 화면으로 다시 리디렉션되며 검증 오류는 공유된 `$errors` Blade 템플릿 변수에서 확인할 수 있습니다. 또는 XHR 요청의 경우, 검증 오류가 422 HTTP 응답과 함께 반환됩니다.
{% endraw %}
