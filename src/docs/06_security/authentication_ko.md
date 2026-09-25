---
layout: docs
title: "Authentication"
---

{% raw %}
# Authentication

- [Introduction](#introduction)
    - [Starter Kits](#starter-kits)
    - [Database Considerations](#introduction-database-considerations)
    - [Ecosystem Overview](#ecosystem-overview)
- [Authentication Quickstart](#authentication-quickstart)
    - [Install a Starter Kit](#install-a-starter-kit)
    - [Retrieving the Authenticated User](#retrieving-the-authenticated-user)
    - [Protecting Routes](#protecting-routes)
    - [Login Throttling](#login-throttling)
- [Manually Authenticating Users](#authenticating-users)
    - [Remembering Users](#remembering-users)
    - [Other Authentication Methods](#other-authentication-methods)
- [HTTP Basic Authentication](#http-basic-authentication)
    - [Stateless HTTP Basic Authentication](#stateless-http-basic-authentication)
- [Logging Out](#logging-out)
    - [Invalidating Sessions on Other Devices](#invalidating-sessions-on-other-devices)
- [Password Confirmation](#password-confirmation)
    - [Configuration](#password-confirmation-configuration)
    - [Routing](#password-confirmation-routing)
    - [Protecting Routes](#password-confirmation-protecting-routes)
- [Adding Custom Guards](#adding-custom-guards)
    - [Closure Request Guards](#closure-request-guards)
- [Adding Custom User Providers](#adding-custom-user-providers)
    - [The User Provider Contract](#the-user-provider-contract)
    - [The Authenticatable Contract](#the-authenticatable-contract)
- [Automatic Password Rehashing](#automatic-password-rehashing)
- [Social Authentication](/docs/{{version}}/socialite)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Many web applications provide a way for their users to authenticate with the application and "login". Implementing this feature in web applications can be a complex and potentially risky endeavor. For this reason, Laravel strives to give you the tools you need to implement authentication quickly, securely, and easily.

At its core, Laravel's authentication facilities are made up of "guards" and "providers". Guards define how users are authenticated for each request. For example, Laravel ships with a `session` guard which maintains state using session storage and cookies.

Providers define how users are retrieved from your persistent storage. Laravel ships with support for retrieving users using [Eloquent](/docs/{{version}}/eloquent) and the database query builder. However, you are free to define additional providers as needed for your application.

Your application's authentication configuration file is located at `config/auth.php`. This file contains several well-documented options for tweaking the behavior of Laravel's authentication services.

> [!NOTE]
> Guards and providers should not be confused with "roles" and "permissions". To learn more about authorizing user actions via permissions, please refer to the [authorization](/docs/{{version}}/authorization) documentation.

<a name="starter-kits"></a>
### Starter Kits

Want to get started fast? Install a [Laravel application starter kit](/docs/{{version}}/starter-kits) in a fresh Laravel application. After migrating your database, navigate your browser to `/register` or any other URL that is assigned to your application. The starter kits will take care of scaffolding your entire authentication system!

**Even if you choose not to use a starter kit in your final Laravel application, installing a [starter kit](/docs/{{version}}/starter-kits) can be a wonderful opportunity to learn how to implement all of Laravel's authentication functionality in an actual Laravel project.** Since the Laravel starter kits contain authentication controllers, routes, and views for you, you can examine the code within these files to learn how Laravel's authentication features may be implemented.

<a name="introduction-database-considerations"></a>
### Database Considerations

By default, Laravel includes an `App\Models\User` [Eloquent model](/docs/{{version}}/eloquent) in your `app/Models` directory. This model may be used with the default Eloquent authentication driver.

If your application is not using Eloquent, you may use the `database` authentication provider which uses the Laravel query builder. If your application is using MongoDB, check out MongoDB's official [Laravel user authentication documentation](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/user-authentication/).

When building the database schema for the `App\Models\User` model, make sure the password column is at least 60 characters in length. Of course, the `users` table migration that is included in new Laravel applications already creates a column that exceeds this length.

Also, you should verify that your `users` (or equivalent) table contains a nullable, string `remember_token` column of 100 characters. This column will be used to store a token for users that select the "remember me" option when logging into your application. Again, the default `users` table migration that is included in new Laravel applications already contains this column.

<a name="ecosystem-overview"></a>
### Ecosystem Overview

Laravel offers several packages related to authentication. Before continuing, we'll review the general authentication ecosystem in Laravel and discuss each package's intended purpose.

First, consider how authentication works. When using a web browser, a user will provide their username and password via a login form. If these credentials are correct, the application will store information about the authenticated user in the user's [session](/docs/{{version}}/session). A cookie issued to the browser contains the session ID so that subsequent requests to the application can associate the user with the correct session. After the session cookie is received, the application will retrieve the session data based on the session ID, note that the authentication information has been stored in the session, and will consider the user as "authenticated".

When a remote service needs to authenticate to access an API, cookies are not typically used for authentication because there is no web browser. Instead, the remote service sends an API token to the API on each request. The application may validate the incoming token against a table of valid API tokens and "authenticate" the request as being performed by the user associated with that API token.

<a name="laravels-built-in-browser-authentication-services"></a>
#### Laravel's Built-in Browser Authentication Services

Laravel includes built-in authentication and session services which are typically accessed via the `Auth` and `Session` facades. These features provide cookie-based authentication for requests that are initiated from web browsers. They provide methods that allow you to verify a user's credentials and authenticate the user. In addition, these services will automatically store the proper authentication data in the user's session and issue the user's session cookie. A discussion of how to use these services is contained within this documentation.

**Application Starter Kits**

As discussed in this documentation, you can interact with these authentication services manually to build your application's own authentication layer. However, to help you get started more quickly, we have released [free starter kits](/docs/{{version}}/starter-kits) that provide robust, modern scaffolding of the entire authentication layer.

<a name="laravels-api-authentication-services"></a>
#### Laravel's API Authentication Services

Laravel provides two optional packages to assist you in managing API tokens and authenticating requests made with API tokens: [Passport](/docs/{{version}}/passport) and [Sanctum](/docs/{{version}}/sanctum). Please note that these libraries and Laravel's built-in cookie based authentication libraries are not mutually exclusive. These libraries primarily focus on API token authentication while the built-in authentication services focus on cookie based browser authentication. Many applications will use both Laravel's built-in cookie based authentication services and one of Laravel's API authentication packages.

**Passport**

Passport is an OAuth2 authentication provider, offering a variety of OAuth2 "grant types" which allow you to issue various types of tokens. In general, this is a robust and complex package for API authentication. However, most applications do not require the complex features offered by the OAuth2 spec, which can be confusing for both users and developers. In addition, developers have been historically confused about how to authenticate SPA applications or mobile applications using OAuth2 authentication providers like Passport.

**Sanctum**

In response to the complexity of OAuth2 and developer confusion, we set out to build a simpler, more streamlined authentication package that could handle both first-party web requests from a web browser and API requests via tokens. This goal was realized with the release of [Laravel Sanctum](/docs/{{version}}/sanctum), which should be considered the preferred and recommended authentication package for applications that will be offering a first-party web UI in addition to an API, or will be powered by a single-page application (SPA) that exists separately from the backend Laravel application, or applications that offer a mobile client.

Laravel Sanctum is a hybrid web / API authentication package that can manage your application's entire authentication process. This is possible because when Sanctum based applications receive a request, Sanctum will first determine if the request includes a session cookie that references an authenticated session. Sanctum accomplishes this by calling Laravel's built-in authentication services which we discussed earlier. If the request is not being authenticated via a session cookie, Sanctum will inspect the request for an API token. If an API token is present, Sanctum will authenticate the request using that token. To learn more about this process, please consult Sanctum's ["how it works"](/docs/{{version}}/sanctum#how-it-works) documentation.

<a name="summary-choosing-your-stack"></a>
#### Summary and Choosing Your Stack

In summary, if your application will be accessed using a browser and you are building a monolithic Laravel application, your application will use Laravel's built-in authentication services.

Next, if your application offers an API that will be consumed by third parties, you will choose between [Passport](/docs/{{version}}/passport) or [Sanctum](/docs/{{version}}/sanctum) to provide API token authentication for your application. In general, Sanctum should be preferred when possible since it is a simple, complete solution for API authentication, SPA authentication, and mobile authentication, including support for "scopes" or "abilities".

If you are building a single-page application (SPA) that will be powered by a Laravel backend, you should use [Laravel Sanctum](/docs/{{version}}/sanctum). When using Sanctum, you will either need to [manually implement your own backend authentication routes](#authenticating-users) or utilize [Laravel Fortify](/docs/{{version}}/fortify) as a headless authentication backend service that provides routes and controllers for features such as registration, password reset, email verification, and more.

Passport may be chosen when your application absolutely needs all of the features provided by the OAuth2 specification. Additionally, if you are building an [MCP server](/docs/{{version}}/mcp) that will be accessed by AI clients, you should use Passport, as MCP clients typically expect to [authenticate using OAuth](/docs/{{version}}/mcp#oauth).



And, if you would like to get started quickly, we are pleased to recommend [our application starter kits](/docs/{{version}}/starter-kits) as a quick way to start a new Laravel application that already uses our preferred authentication stack of Laravel's built-in authentication services.

<a name="authentication-quickstart"></a>
## Authentication Quickstart

> [!WARNING]
> This portion of the documentation discusses authenticating users via the [Laravel application starter kits](/docs/{{version}}/starter-kits), which includes UI scaffolding to help you get started quickly. If you would like to integrate with Laravel's authentication systems directly, check out the documentation on [manually authenticating users](#authenticating-users).

<a name="install-a-starter-kit"></a>
### Install a Starter Kit

First, you should [install a Laravel application starter kit](/docs/{{version}}/starter-kits). Our starter kits offer beautifully designed starting points for incorporating authentication into your fresh Laravel application.

<a name="retrieving-the-authenticated-user"></a>
### Retrieving the Authenticated User

After creating an application from a starter kit and allowing users to register and authenticate with your application, you will often need to interact with the currently authenticated user. While handling an incoming request, you may access the authenticated user via the `Auth` facade's `user` method:

```php
use Illuminate\Support\Facades\Auth;

// Retrieve the currently authenticated user...
$user = Auth::user();

// Retrieve the currently authenticated user's ID...
$id = Auth::id();
```



또는 사용자가 인증되면 `Illuminate\Http\Request` 인스턴스를 통해 인증된 사용자에 접근할 수 있습니다. 타입 힌트가 있는 클래스는 자동으로 컨트롤러 메서드에 주입된다는 점을 기억하세요. `Illuminate\Http\Request` 객체에 타입 힌트를 지정하면 요청의 `user` 메서드를 통해 애플리케이션의 모든 컨트롤러 메서드에서 인증된 사용자에 편리하게 접근할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Update the flight information for an existing flight.
     */
    public function update(Request $request): RedirectResponse
    {
        $user = $request->user();

        // ...

        return redirect('/flights');
    }
}
```



<a name="determining-if-the-current-user-is-authenticated"></a>
#### 현재 사용자가 인증되었는지 확인하기

수신된 HTTP 요청을 하는 사용자가 인증되었는지 확인하려면 `Auth` 퍼사드에서 `check` 메서드를 사용할 수 있습니다. 사용자가 인증된 경우 이 메서드는 `true`를 반환합니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::check()) {
    // The user is logged in...
}
```



> [!NOTE]
> `check` 방식을 사용하여 사용자가 인증되었는지 여부를 확인할 수 있지만, 일반적으로 사용자가 특정 경로/컨트롤러에 접근하기 전에 인증되었는지 확인하기 위해 미들웨어를 사용합니다. 이에 대해 더 알아보려면 [경로 보호](/docs/{{version}}/authentication#protecting-routes) 문서를 참고하십시오.

<a name="protecting-routes"></a>
### 경로 보호

[경로 미들웨어](/docs/{{version}}/middleware)는 인증된 사용자만 특정 경로에 접근할 수 있도록 하는 데 사용할 수 있습니다. Laravel은 `auth` 미들웨어를 제공하며, 이는 `Illuminate\Auth\Middleware\Authenticate` 클래스에 대한 [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)입니다. 이 미들웨어는 내부적으로 Laravel에서 이미 별칭이 지정되어 있으므로, 경로 정의에 미들웨어를 연결하기만 하면 됩니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth');
```



<a name="redirecting-unauthenticated-users"></a>
#### 인증되지 않은 사용자 리디렉션

`auth` 미들웨어가 인증되지 않은 사용자를 감지하면, 사용자를 `login` [명명된 라우트](/docs/{{version}}/routing#named-routes)로 리디렉션합니다. 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectGuestsTo` 메서드를 사용하여 이 동작을 수정할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectGuestsTo('/login');

    // Using a closure...
    $middleware->redirectGuestsTo(fn (Request $request) => route('login'));
})
```



<a name="redirecting-authenticated-users"></a>
#### 인증된 사용자 리디렉션

`guest` 미들웨어가 인증된 사용자를 감지하면, 사용자를 `dashboard` 또는 `home` 명명된 경로로 리디렉션합니다. 이 동작은 애플리케이션의 `bootstrap/app.php` 파일 내에서 `redirectUsersTo` 메서드를 사용하여 수정할 수 있습니다:

```php
use Illuminate\Http\Request;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->redirectUsersTo('/panel');

    // Using a closure...
    $middleware->redirectUsersTo(fn (Request $request) => route('panel'));
})
```



<a name="specifying-a-guard"></a>
#### 가드 지정하기

라우트에 `auth` 미들웨어를 첨부할 때, 사용자 인증에 사용할 "가드"를 지정할 수도 있습니다. 지정된 가드는 `auth.php` 구성 파일의 `guards` 배열에 있는 키 중 하나와 일치해야 합니다:

```php
Route::get('/flights', function () {
    // Only authenticated users may access this route...
})->middleware('auth:admin');
```



<a name="login-throttling"></a>
### Login Throttling

If you are using one of our [application starter kits](/docs/{{version}}/starter-kits), rate limiting will automatically be applied to login attempts. By default, the user will not be able to login for one minute if they fail to provide the correct credentials after several attempts. The throttling is unique to the user's username / email address and their IP address.

> [!NOTE]
> If you would like to rate limit other routes in your application, check out the [rate limiting documentation](/docs/{{version}}/routing#rate-limiting).

<a name="authenticating-users"></a>
## Manually Authenticating Users

You are not required to use the authentication scaffolding included with Laravel's [application starter kits](/docs/{{version}}/starter-kits). If you choose not to use this scaffolding, you will need to manage user authentication using the Laravel authentication classes directly. Don't worry, it's a cinch!

We will access Laravel's authentication services via the `Auth` [facade](/docs/{{version}}/facades), so we'll need to make sure to import the `Auth` facade at the top of the class. Next, let's check out the `attempt` method. The `attempt` method is normally used to handle authentication attempts from your application's "login" form. If authentication is successful, you should regenerate the user's [session](/docs/{{version}}/session) to prevent [session fixation](https://en.wikipedia.org/wiki/Session_fixation):

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    /**
     * Handle an authentication attempt.
     */
    public function authenticate(Request $request): RedirectResponse
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended('dashboard');
        }

        return back()->withErrors([
            'email' => 'The provided credentials do not match our records.',
        ])->onlyInput('email');
    }
}
```



The `attempt` method accepts an array of key / value pairs as its first argument. The values in the array will be used to find the user in your database table. So, in the example above, the user will be retrieved by the value of the `email` column. If the user is found, the hashed password stored in the database will be compared with the `password` value passed to the method via the array. You should not hash the incoming request's `password` value, since the framework will automatically hash the value before comparing it to the hashed password in the database. An authenticated session will be started for the user if the two hashed passwords match.

Remember, Laravel's authentication services will retrieve users from your database based on your authentication guard's "provider" configuration. In the default `config/auth.php` configuration file, the Eloquent user provider is specified and it is instructed to use the `App\Models\User` model when retrieving users. You may change these values within your configuration file based on the needs of your application.

The `attempt` method will return `true` if authentication was successful. Otherwise, `false` will be returned.

The `intended` method provided by Laravel's redirector will redirect the user to the URL they were attempting to access before being intercepted by the authentication middleware. A fallback URI may be given to this method in case the intended destination is not available.

<a name="specifying-additional-conditions"></a>
#### Specifying Additional Conditions

If you wish, you may also add extra query conditions to the authentication query in addition to the user's email and password. To accomplish this, we may simply add the query conditions to the array passed to the `attempt` method. For example, we may verify that the user is marked as "active":

```php
if (Auth::attempt(['email' => $email, 'password' => $password, 'active' => 1])) {
    // Authentication was successful...
}
```



복잡한 쿼리 조건의 경우, 자격 증명 배열에 클로저를 제공할 수 있습니다. 이 클로저는 쿼리 인스턴스와 함께 호출되어 애플리케이션의 필요에 따라 쿼리를 사용자 정의할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

if (Auth::attempt([
    'email' => $email,
    'password' => $password,
    fn (Builder $query) => $query->has('activeSubscription'),
])) {
    // Authentication was successful...
}
```



> [!WARNING]
> 이 예제에서 `email`는 필수 옵션이 아니며, 단지 예제로 사용되었습니다. 데이터베이스 테이블에서 'username'에 해당하는 열 이름을 사용해야 합니다.

두 번째 인수로 클로저를 받는 `attemptWhen` 메서드는 실제로 사용자를 인증하기 전에 잠재적인 사용자에 대한 보다 광범위한 검사를 수행하는 데 사용할 수 있습니다. 클로저는 잠재적인 사용자를 받고, 사용자를 인증할 수 있는지 여부를 표시하기 위해 `true` 또는 `false`를 반환해야 합니다:

```php
if (Auth::attemptWhen([
    'email' => $email,
    'password' => $password,
], function (User $user) {
    return $user->isNotBanned();
})) {
    // Authentication was successful...
}
```



<a name="accessing-specific-guard-instances"></a>
#### 특정 가드 인스턴스 접근

`Auth` 파사드의 `guard` 메서드를 통해, 사용자 인증 시 사용할 가드 인스턴스를 지정할 수 있습니다. 이를 통해 완전히 별개의 인증 가능 모델이나 사용자 테이블을 사용하여 애플리케이션의 서로 다른 부분에 대한 인증을 관리할 수 있습니다.

`guard` 메서드에 전달되는 가드 이름은 `auth.php` 구성 파일에 설정된 가드 중 하나와 일치해야 합니다:

```php
if (Auth::guard('admin')->attempt($credentials)) {
    // ...
}
```



<a name="remembering-users"></a>
### 사용자 기억하기

많은 웹 애플리케이션은 로그인 폼에 '나를 기억하기' 체크박스를 제공합니다. 애플리케이션에서 '나를 기억하기' 기능을 제공하고 싶다면, `attempt` 메서드의 두 번째 인수로 불리언 값을 전달할 수 있습니다.

이 값이 `true`일 때, Laravel은 사용자가 수동으로 로그아웃할 때까지 혹은 무한정 사용자를 인증 상태로 유지합니다. `users` 테이블에는 '나를 기억하기' 토큰을 저장하는 데 사용되는 `remember_token` 문자열 컬럼이 포함되어 있어야 합니다. 새 Laravel 애플리케이션과 함께 제공되는 `users` 테이블 마이그레이션에는 이미 이 컬럼이 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::attempt(['email' => $email, 'password' => $password], $remember)) {
    // The user is being remembered...
}
```



애플리케이션에서 '나를 기억하기' 기능을 제공하는 경우, 현재 인증된 사용자가 '나를 기억하기' 쿠키를 사용하여 인증되었는지 확인하기 위해 `viaRemember` 방법을 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;

if (Auth::viaRemember()) {
    // ...
}
```



<a name="other-authentication-methods"></a>
### 다른 인증 방법

<a name="authenticate-a-user-instance"></a>
#### 사용자 인스턴스 인증하기

기존 사용자 인스턴스를 현재 인증된 사용자로 설정해야 하는 경우, 해당 사용자 인스턴스를 `Auth` 파사드의 `login` 메서드에 전달할 수 있습니다. 주어진 사용자 인스턴스는 `Illuminate\Contracts\Auth\Authenticatable` [계약](/docs/{{version}}/contracts)의 구현체여야 합니다. Laravel에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하고 있습니다. 이 인증 방법은 사용자가 애플리케이션에 등록한 직후처럼 이미 유효한 사용자 인스턴스를 가지고 있는 경우에 유용합니다.

```php
use Illuminate\Support\Facades\Auth;

Auth::login($user);
```



두 번째 인수로 `login` 메서드에 불리언 값을 전달할 수 있습니다. 이 값은 인증된 세션에 대해 '나를 기억하기' 기능이 필요한지를 나타냅니다. 이는 세션이 무기한으로 인증되거나 사용자가 애플리케이션에서 수동으로 로그아웃할 때까지 유지됨을 의미합니다:

```php
Auth::login($user, $remember = true);
```



필요한 경우 `login` 메서드를 호출하기 전에 인증 가드를 지정할 수 있습니다:

```php
Auth::guard('admin')->login($user);
```



<a name="authenticate-a-user-by-id"></a>
#### ID로 사용자 인증하기

데이터베이스 기록의 기본 키를 사용하여 사용자를 인증하려면 `loginUsingId` 메서드를 사용할 수 있습니다. 이 메서드는 인증하려는 사용자의 기본 키를 받습니다:

```php
Auth::loginUsingId(1);
```



`loginUsingId` 메서드의 `remember` 인수에 부울 값을 전달할 수 있습니다. 이 값은 인증된 세션에 대해 "나를 기억하기" 기능을 원하는지 여부를 나타냅니다. 이것은 세션이 무기한으로 인증되거나 사용자가 애플리케이션에서 수동으로 로그아웃할 때까지 인증된 상태를 유지한다는 것을 의미합니다:

```php
Auth::loginUsingId(1, remember: true);
```



<a name="authenticate-a-user-once"></a>
#### 사용자 한 번 인증하기

단일 요청에 대해 애플리케이션에서 사용자를 인증하려면 `once` 방법을 사용할 수 있습니다. 이 방법을 호출할 때 세션이나 쿠키는 사용되지 않으며, `Login` 이벤트는 전송되지 않습니다:

```php
if (Auth::once($credentials)) {
    // ...
}
```



<a name="http-basic-authentication"></a>
## HTTP 기본 인증

[HTTP 기본 인증](https://en.wikipedia.org/wiki/Basic_access_authentication)은 전용 "로그인" 페이지를 설정하지 않고 애플리케이션 사용자를 인증하는 빠른 방법을 제공합니다. 시작하려면, `auth.basic` [미들웨어](/docs/{{version}}/middleware)를 라우트에 첨부하세요. `auth.basic` 미들웨어는 Laravel 프레임워크에 포함되어 있으므로, 정의할 필요가 없습니다:

```php
Route::get('/profile', function () {
    // Only authenticated users may access this route...
})->middleware('auth.basic');
```



미들웨어가 라우트에 연결되면 브라우저에서 라우트에 접근할 때 자동으로 자격 증명을 요청받게 됩니다. 기본적으로, `auth.basic` 미들웨어는 `users` 데이터베이스 테이블의 `email` 열을 사용자의 "사용자 이름"으로 간주합니다.

<a name="a-note-on-fastcgi"></a>
#### FastCGI에 대한 참고 사항

Laravel 애플리케이션을 제공하기 위해 [PHP FastCGI](https://www.php.net/manual/en/install.fpm.php)와 Apache를 사용 중인 경우, HTTP 기본 인증이 올바르게 작동하지 않을 수 있습니다. 이러한 문제를 수정하려면, 다음 줄을 애플리케이션의 `.htaccess` 파일에 추가할 수 있습니다:

```apache
RewriteCond %{HTTP:Authorization} ^(.+)$
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
```



<a name="stateless-http-basic-authentication"></a>
### 상태 비저장(Stateless) HTTP 기본 인증(Basic Authentication)

세션에서 사용자 식별자 쿠키를 설정하지 않고 HTTP 기본 인증을 사용할 수도 있습니다. 이는 주로 HTTP 인증을 사용하여 애플리케이션의 API 요청을 인증하려는 경우에 유용합니다. 이를 수행하려면 [미들웨어를 정의](/docs/{{version}}/middleware)하고 `onceBasic` 메서드를 호출하십시오. `onceBasic` 메서드에서 응답이 반환되지 않으면 요청을 애플리케이션 내에서 계속 처리할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateOnceWithBasicAuth
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return Auth::onceBasic() ?: $next($request);
    }

}
```



다음으로, 미들웨어를 라우트에 연결합니다:

```php
Route::get('/api/user', function () {
    // Only authenticated users may access this route...
})->middleware(AuthenticateOnceWithBasicAuth::class);
```



<a name="logging-out"></a>
## 로그아웃

애플리케이션에서 사용자를 수동으로 로그아웃시키려면 `Auth` 퍼사드에서 제공하는 `logout` 메서드를 사용할 수 있습니다. 이 방법은 사용자의 세션에서 인증 정보를 제거하여 이후 요청이 인증되지 않도록 합니다.

`logout` 메서드를 호출하는 것 외에도, 사용자의 세션을 무효화하고 [CSRF 토큰](/docs/{{version}}/csrf)을 재생성하는 것이 권장됩니다. 사용자를 로그아웃시킨 후에는 일반적으로 사용자를 애플리케이션의 루트로 리디렉션합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;

/**
 * Log the user out of the application.
 */
public function logout(Request $request): RedirectResponse
{
    Auth::logout();

    $request->session()->invalidate();

    $request->session()->regenerateToken();

    return redirect('/');
}
```



<a name="invalidating-sessions-on-other-devices"></a>
### 다른 기기에서 세션 무효화

Laravel은 또한 사용자가 현재 사용 중인 기기에서는 세션을 무효화하지 않고 다른 기기에서 활성화된 사용자의 세션을 무효화하고 '로그아웃'하는 메커니즘을 제공합니다. 이 기능은 일반적으로 사용자가 비밀번호를 변경하거나 업데이트할 때 사용하며, 현재 기기는 인증된 상태로 유지하면서 다른 기기의 세션을 무효화하려고 할 때 사용됩니다.

시작하기 전에 `Illuminate\Session\Middleware\AuthenticateSession` 미들웨어가 세션 인증을 받아야 하는 경로에 포함되어 있는지 확인해야 합니다. 일반적으로 이 미들웨어는 라우트 그룹 정의에 배치하여 애플리케이션의 대부분의 경로에 적용되도록 합니다. 기본적으로 `AuthenticateSession` 미들웨어는 `auth.session` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)을 사용하여 라우트에 연결될 수 있습니다:

```php
Route::middleware(['auth', 'auth.session'])->group(function () {
    Route::get('/', function () {
        // ...
    });
});
```



그런 다음, `Auth` 퍼사드에서 제공하는 `logoutOtherDevices` 메서드를 사용할 수 있습니다. 이 메서드는 사용자가 현재 비밀번호를 확인하도록 요구하며, 귀하의 애플리케이션은 이를 입력 폼을 통해 받아야 합니다:

```php
use Illuminate\Support\Facades\Auth;

Auth::logoutOtherDevices($currentPassword);
```



When the `logoutOtherDevices` method is invoked, the user's other sessions will be invalidated entirely, meaning they will be "logged out" of all guards they were previously authenticated by.

<a name="password-confirmation"></a>
## Password Confirmation

While building your application, you may occasionally have actions that should require the user to confirm their password before the action is performed or before the user is redirected to a sensitive area of the application. Laravel includes built-in middleware to make this process a breeze. Implementing this feature will require you to define two routes: one route to display a view asking the user to confirm their password and another route to confirm that the password is valid and redirect the user to their intended destination.

> [!NOTE]
> The following documentation discusses how to integrate with Laravel's password confirmation features directly; however, if you would like to get started more quickly, the [Laravel application starter kits](/docs/{{version}}/starter-kits) include support for this feature!

<a name="password-confirmation-configuration"></a>
### Configuration

After confirming their password, a user will not be asked to confirm their password again for three hours. However, you may configure the length of time before the user is re-prompted for their password by changing the value of the `password_timeout` configuration value within your application's `config/auth.php` configuration file.

<a name="password-confirmation-routing"></a>
### Routing

<a name="the-password-confirmation-form"></a>
#### The Password Confirmation Form

First, we will define a route to display a view that requests the user to confirm their password:

```php
Route::get('/confirm-password', function () {
    return view('auth.confirm-password');
})->middleware('auth')->name('password.confirm');
```



예상할 수 있듯이, 이 경로에서 반환되는 뷰는 `password` 필드를 포함하는 폼을 가져야 합니다. 또한, 뷰 안에 사용자가 애플리케이션의 보호된 영역에 접근하고 있으며 비밀번호를 확인해야 함을 설명하는 텍스트를 자유롭게 포함할 수 있습니다.

<a name="confirming-the-password"></a>
#### 비밀번호 확인

다음으로, "비밀번호 확인" 뷰에서 폼 요청을 처리할 경로를 정의하겠습니다. 이 경로는 비밀번호를 검증하고 사용자를 의도한 목적지로 리디렉션하는 역할을 하게 됩니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

Route::post('/confirm-password', function (Request $request) {
    if (! Hash::check($request->password, $request->user()->password)) {
        return back()->withErrors([
            'password' => ['The provided password does not match our records.']
        ]);
    }

    $request->session()->passwordConfirmed();

    return redirect()->intended();
})->middleware(['auth', 'throttle:6,1']);
```



Before moving on, let's examine this route in more detail. First, the request's `password` field is determined to actually match the authenticated user's password. If the password is valid, we need to inform Laravel's session that the user has confirmed their password. The `passwordConfirmed` method will set a timestamp in the user's session that Laravel can use to determine when the user last confirmed their password. Finally, we can redirect the user to their intended destination.

<a name="password-confirmation-protecting-routes"></a>
### Protecting Routes

You should ensure that any route that performs an action which requires recent password confirmation is assigned the `password.confirm` middleware. This middleware is included with the default installation of Laravel and will automatically store the user's intended destination in the session so that the user may be redirected to that location after confirming their password. After storing the user's intended destination in the session, the middleware will redirect the user to the `password.confirm` [named route](/docs/{{version}}/routing#named-routes):

```php
Route::get('/settings', function () {
    // ...
})->middleware(['password.confirm']);

Route::post('/settings', function () {
    // ...
})->middleware(['password.confirm']);
```



<a name="adding-custom-guards"></a>
## 커스텀 가드 추가하기

`Auth` 파사드의 `extend` 메서드를 사용하여 자신만의 인증 가드를 정의할 수 있습니다. `extend` 메서드 호출은 [서비스 제공자](/docs/{{version}}/providers) 내에 배치해야 합니다. Laravel은 이미 `AppServiceProvider`을 제공하므로, 해당 코드도 그 제공자에 배치할 수 있습니다:

```php
<?php

namespace App\Providers;

use App\Services\Auth\JwtGuard;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::extend('jwt', function (Application $app, string $name, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\Guard...

            return new JwtGuard(Auth::createUserProvider($config['provider']));
        });
    }
}
```



위 예에서 볼 수 있듯이, `extend` 메서드에 전달된 콜백은 `Illuminate\Contracts\Auth\Guard`의 구현을 반환해야 합니다. 이 인터페이스에는 사용자 정의 가드를 정의하기 위해 구현해야 하는 몇 가지 메서드가 포함되어 있습니다. 사용자 정의 가드를 정의한 후에는 `auth.php` 구성 파일의 `guards` 구성에서 해당 가드를 참조할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'jwt',
        'provider' => 'users',
    ],
],
```



<a name="closure-request-guards"></a>
### 클로저 요청 가드

사용자 정의 HTTP 요청 기반 인증 시스템을 구현하는 가장 간단한 방법은 `Auth::viaRequest` 메서드를 사용하는 것입니다. 이 메서드를 사용하면 단일 클로저를 사용하여 인증 프로세스를 빠르게 정의할 수 있습니다.

시작하려면 애플리케이션의 `AppServiceProvider`에서 `boot` 메서드 내에서 `Auth::viaRequest` 메서드를 호출하세요. `viaRequest` 메서드는 인증 드라이버 이름을 첫 번째 인수로 받습니다. 이 이름은 사용자 정의 가드를 설명하는 어떤 문자열도 될 수 있습니다. 메서드에 전달된 두 번째 인수는 들어오는 HTTP 요청을 받고 사용자 인스턴스를 반환하거나, 인증에 실패할 경우 `null`를 반환하는 클로저여야 합니다:

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Auth::viaRequest('custom-token', function (Request $request) {
        return User::where('token', (string) $request->token)->first();
    });
}
```



사용자 정의 인증 드라이버가 정의되면 `auth.php` 구성 파일의 `guards` 구성 내에서 드라이버로 설정할 수 있습니다:

```php
'guards' => [
    'api' => [
        'driver' => 'custom-token',
    ],
],
```



마지막으로, 인증 미들웨어를 경로에 할당할 때 가드를 참조할 수 있습니다:

```php
Route::middleware('auth:api')->group(function () {
    // ...
});
```



<a name="adding-custom-user-providers"></a>
## 사용자 정의 사용자 제공자 추가

사용자를 저장하기 위해 전통적인 관계형 데이터베이스를 사용하지 않는 경우, 자체 인증 사용자 제공자로 Laravel을 확장해야 합니다. 사용자 정의 사용자 제공자를 정의하기 위해 `Auth` 파사드에서 `provider` 메서드를 사용할 것입니다. 사용자 제공자 해결자는 `Illuminate\Contracts\Auth\UserProvider`의 구현을 반환해야 합니다:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoUserProvider;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    // ...

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Auth::provider('mongo', function (Application $app, array $config) {
            // Return an instance of Illuminate\Contracts\Auth\UserProvider...

            return new MongoUserProvider($app->make('mongo.connection'));
        });
    }
}
```



`provider` 방법을 사용하여 공급자를 등록한 후에는 `auth.php` 구성 파일에서 새 사용자 공급자로 전환할 수 있습니다. 먼저 새 드라이버를 사용하는 `provider`를 정의하십시오:

```php
'providers' => [
    'users' => [
        'driver' => 'mongo',
    ],
],
```



마지막으로, `guards` 구성에서 이 공급자를 참조할 수 있습니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],
],
```



<a name="the-user-provider-contract"></a>
### 사용자 제공자 계약

`Illuminate\Contracts\Auth\UserProvider` 구현체는 MySQL, MongoDB 등과 같은 지속적 저장소 시스템에서 `Illuminate\Contracts\Auth\Authenticatable` 구현체를 가져오는 일을 담당합니다. 이 두 인터페이스는 사용자 데이터가 어떻게 저장되는지 또는 인증된 사용자를 나타내는 클래스 유형이 무엇인지에 상관없이 Laravel 인증 메커니즘이 계속 작동하도록 합니다:

`Illuminate\Contracts\Auth\UserProvider` 계약을 살펴보겠습니다:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface UserProvider
{
    public function retrieveById($identifier);
    public function retrieveByToken($identifier, $token);
    public function updateRememberToken(Authenticatable $user, $token);
    public function retrieveByCredentials(array $credentials);
    public function validateCredentials(Authenticatable $user, array $credentials);
    public function rehashPasswordIfRequired(Authenticatable $user, array $credentials, bool $force = false);
}
```



The `retrieveById` function typically receives a key representing the user, such as an auto-incrementing ID from a MySQL database. The `Authenticatable` implementation matching the ID should be retrieved and returned by the method.

The `retrieveByToken` function retrieves a user by their unique `$identifier` and "remember me" `$token`, typically stored in a database column like `remember_token`. As with the previous method, the `Authenticatable` implementation with a matching token value should be returned by this method.

The `updateRememberToken` method updates the `$user` instance's `remember_token` with the new `$token`. A fresh token is assigned to users on a successful "remember me" authentication attempt or when the user is logging out.

The `retrieveByCredentials` method receives the array of credentials passed to the `Auth::attempt` method when attempting to authenticate with an application. The method should then "query" the underlying persistent storage for the user matching those credentials. Typically, this method will run a query with a "where" condition that searches for a user record with a "username" matching the value of `$credentials['username']`. The method should return an implementation of `Authenticatable`. **This method should not attempt to do any password validation or authentication.**

The `validateCredentials` method should compare the given `$user` with the `$credentials` to authenticate the user. For example, this method will typically use the `Hash::check` method to compare the value of `$user->getAuthPassword()` to the value of `$credentials['password']`. This method should return `true` or `false` indicating whether the password is valid.

The `rehashPasswordIfRequired` method should rehash the given `$user`'s password if required and supported. For example, this method will typically use the `Hash::needsRehash` method to determine if the `$credentials['password']` value needs to be rehashed. If the password needs to be rehashed, the method should use the `Hash::make` method to rehash the password and update the user's record in the underlying persistent storage.

<a name="the-authenticatable-contract"></a>
### The Authenticatable Contract

Now that we have explored each of the methods on the `UserProvider`, let's take a look at the `Authenticatable` contract. Remember, user providers should return implementations of this interface from the `retrieveById`, `retrieveByToken`, and `retrieveByCredentials` methods:

```php
<?php

namespace Illuminate\Contracts\Auth;

interface Authenticatable
{
    public function getAuthIdentifierName();
    public function getAuthIdentifier();
    public function getAuthPasswordName();
    public function getAuthPassword();
    public function getRememberToken();
    public function setRememberToken($value);
    public function getRememberTokenName();
}
```



This interface is simple. The `getAuthIdentifierName` method should return the name of the "primary key" column for the user and the `getAuthIdentifier` method should return the "primary key" of the user. When using a MySQL back-end, this would likely be the auto-incrementing primary key assigned to the user record. The `getAuthPasswordName` method should return the name of the user's password column. The `getAuthPassword` method should return the user's hashed password.

This interface allows the authentication system to work with any "user" class, regardless of what ORM or storage abstraction layer you are using. By default, Laravel includes an `App\Models\User` class in the `app/Models` directory which implements this interface.

<a name="automatic-password-rehashing"></a>
## Automatic Password Rehashing

Laravel's default password hashing algorithm is bcrypt. The "work factor" for bcrypt hashes can be adjusted via your application's `config/hashing.php` configuration file or the `BCRYPT_ROUNDS` environment variable.

Typically, the bcrypt work factor should be increased over time as CPU / GPU processing power increases. If you increase the bcrypt work factor for your application, Laravel will gracefully and automatically rehash user passwords as users authenticate with your application via Laravel's starter kits or when you [manually authenticate users](#authenticating-users) via the `attempt` method.

Typically, automatic password rehashing should not disrupt your application; however, you may disable this behavior by publishing the `hashing` configuration file:

```shell
php artisan config:publish hashing
```



구성 파일이 게시되면 `rehash_on_login` 구성 값을 `false`로 설정할 수 있습니다:

```php
'rehash_on_login' => false,
```

<a name="events"></a>
## 이벤트

Laravel은 인증 과정에서 다양한 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 다음 이벤트 중 어떤 것에 대해서도 [리스너를 정의](/docs/{{version}}/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름 |
| ---------------------------------------------- |
| `Illuminate\Auth\Events\Registered` |
| `Illuminate\Auth\Events\Attempting` |
| `Illuminate\Auth\Events\Authenticated` |
| `Illuminate\Auth\Events\Login` |
| `Illuminate\Auth\Events\Failed` |
| `Illuminate\Auth\Events\Validated` |
| `Illuminate\Auth\Events\Verified` |
| `Illuminate\Auth\Events\Logout` |
| `Illuminate\Auth\Events\CurrentDeviceLogout` |
| `Illuminate\Auth\Events\OtherDeviceLogout` |
| `Illuminate\Auth\Events\Lockout` |
| `Illuminate\Auth\Events\PasswordReset` |
| `Illuminate\Auth\Events\PasswordResetLinkSent` |

</div>
{% endraw %}
