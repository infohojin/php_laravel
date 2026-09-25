---
layout: docs
title: "미들웨어"
---

{% raw %}
# 미들웨어

- [소개](#introduction)
- [정의 중간 소프트웨어](#defining-middleware)
- 레지스터링 미들웨어 (#registering-middleware)
- 글로벌 미들웨어 (#global-middleware)
- 미들웨어를 경로에 할당 (#assigning-middleware-to-routes)
- 미들웨어 그룹 (#middleware-groups)
- [Middleware Aliases](#middleware-aliases)
- [Sorting Middleware](#sorting-middleware)
- 미들웨어 파라미터 (#middleware-parameters)
- [Terminable Middleware](#terminable-middleware)

<a name="introduction"></a>
## 소개

미들웨어는 애플리케이션에 들어오는 HTTP 요청을 검사하고 필터링하는 편리한 메커니즘을 제공합니다. 예를 들어， Laravel 에는 애플리케이션의 사용자가 인증되었는지 확인하는 미들웨어가 포함되어 있습니다. 사용자가 인증되지 않은 경우， 미들웨어는 사용자를 애플리케이션의 로그인 화면으로 리디렉션합니다. 그러나 사용자가 인증되었다면， 미들웨어는 요청이 애플리케이션 내에서 더 진행되도록 허용합니다。

추가 미들웨어를 작성하여 인증 외에도 다양한 작업을 수행할 수 있습니다. 예를 들어， 로깅 미들웨어는 애플리케이션에 대한 모든 수신 요청을 로깅할 수 있습니다. Laravel 에는 인증 및 CSRF 보호를 위한 미들웨어를 포함하여 다양한 미들웨어가 포함되어 있습니다. 그러나 모든 사용자 정의 미들웨어는 일반적으로 애플리케이션의 `app/Http/Middleware` 디렉터리에 있습니다。

<a name="defining-middleware"></a>
## 미들웨어 정의

새로운 미들웨어를 생성하려면 `make:middleware` Artisan 명령을 사용하세요：

```shell
php artisan make:middleware EnsureTokenIsValid
```



이 명령은 `app/Http/Middleware` 디렉터리 내에 새로운 `EnsureTokenIsValid` 클래스를 배치합니다. 이 미들웨어에서는 제공된 `token` 입력이 지정된 값과 일치하는 경우에만 해당 경로에 대한 접근을 허용합니다. 그렇지 않으면 사용자를 `/home` URI로 다시 리디렉션합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureTokenIsValid
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        if ($request->input('token') !== 'my-secret-token') {
            return redirect('/home');
        }

        return $next($request);
    }
}
```



보시다시피, 주어진 `token`가 우리의 비밀 토큰과 일치하지 않으면, 미들웨어는 클라이언트에게 HTTP 리디렉션을 반환합니다. 그렇지 않으면 요청은 애플리케이션으로 더 전달됩니다. 요청을 애플리케이션 내부로 전달하려면(미들웨어가 "통과"하도록 하려면), `$next` 콜백을 `$request`와 함께 호출해야 합니다.

미들웨어를 애플리케이션에 도달하기 전에 HTTP 요청이 통과해야 하는 일련의 "레이어"로 상상하는 것이 가장 좋습니다. 각 레이어는 요청을 검토하고 심지어 완전히 거부할 수도 있습니다.

> [!NOTE]
> 모든 미들웨어는 [서비스 컨테이너](/docs/{{version}}/container)를 통해 해결되므로, 미들웨어 생성자 내에서 필요한 모든 의존성을 타입 힌트로 지정할 수 있습니다.

<a name="middleware-and-responses"></a>
#### 미들웨어와 응답

물론 미들웨어는 요청을 애플리케이션 내부로 전달하기 전이나 후에 작업을 수행할 수 있습니다. 예를 들어, 다음 미들웨어는 요청이 애플리케이션에서 처리되기 **전에** 일부 작업을 수행합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class BeforeMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        // Perform action

        return $next($request);
    }
}
```



하지만 이 미들웨어는 요청이 애플리케이션에 의해 처리된 **후에** 작업을 수행합니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class AfterMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        // Perform action

        return $response;
    }
}
```



<a name="registering-middleware"></a>
## 미들웨어 등록

<a name="global-middleware"></a>
### 전역 미들웨어

애플리케이션의 모든 HTTP 요청 동안 미들웨어를 실행하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에 있는 전역 미들웨어 스택에 추가할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

->withMiddleware(function (Middleware $middleware): void {
     $middleware->append(EnsureTokenIsValid::class);
})
```



`withMiddleware` 클로저에 제공되는 `$middleware` 객체는 `Illuminate\Foundation\Configuration\Middleware`의 인스턴스이며, 애플리케이션의 라우트에 할당된 미들웨어를 관리하는 역할을 합니다. `append` 메서드는 전역 미들웨어 목록의 끝에 미들웨어를 추가합니다. 목록의 처음에 미들웨어를 추가하고 싶다면, `prepend` 메서드를 사용해야 합니다.

<a name="manually-managing-laravels-default-global-middleware"></a>
#### Laravel의 기본 전역 미들웨어 수동 관리

Laravel의 전역 미들웨어 스택을 수동으로 관리하고 싶다면, Laravel의 기본 전역 미들웨어 스택을 `use` 메서드에 제공할 수 있습니다. 그런 다음 필요에 따라 기본 미들웨어 스택을 조정할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->use([
        \Illuminate\Foundation\Http\Middleware\InvokeDeferredCallbacks::class,
        // \Illuminate\Http\Middleware\TrustHosts::class,
        \Illuminate\Http\Middleware\TrustProxies::class,
        \Illuminate\Http\Middleware\HandleCors::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestsDuringMaintenance::class,
        \Illuminate\Http\Middleware\ValidatePostSize::class,
        \Illuminate\Foundation\Http\Middleware\TrimStrings::class,
        \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
    ]);
})
```



<a name="assigning-middleware-to-routes"></a>
### 미들웨어를 라우트에 할당하기

특정 라우트에 미들웨어를 할당하고 싶다면, 라우트를 정의할 때 `middleware` 메서드를 호출할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::get('/profile', function () {
    // ...
})->middleware(EnsureTokenIsValid::class);
```



`middleware` 메서드에 미들웨어 이름 배열을 전달하여 경로에 여러 미들웨어를 지정할 수 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware([First::class, Second::class]);
```



<a name="excluding-middleware"></a>
#### 미들웨어 제외

라우트 그룹에 미들웨어를 할당할 때, 때때로 그룹 내의 개별 라우트에 미들웨어가 적용되지 않도록 해야 할 필요가 있습니다. 이는 `withoutMiddleware` 메서드를 사용하여 수행할 수 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::middleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/', function () {
        // ...
    });

    Route::get('/profile', function () {
        // ...
    })->withoutMiddleware([EnsureTokenIsValid::class]);
});
```



특정 미들웨어 집합을 전체 [그룹](/docs/{{version}}/routing#route-groups)의 라우트 정의에서 제외할 수도 있습니다:

```php
use App\Http\Middleware\EnsureTokenIsValid;

Route::withoutMiddleware([EnsureTokenIsValid::class])->group(function () {
    Route::get('/profile', function () {
        // ...
    });
});
```



`withoutMiddleware` 메서드는 경로 미들웨어만 제거할 수 있으며 [글로벌 미들웨어](#global-middleware)에는 적용되지 않습니다.

<a name="middleware-groups"></a>
### 미들웨어 그룹

때때로 여러 미들웨어를 단일 키 아래에 그룹화하여 경로에 할당하기 쉽게 만들고 싶을 수 있습니다. 이러한 작업은 애플리케이션의 `bootstrap/app.php` 파일 내에서 `appendToGroup` 메서드를 사용하여 수행할 수 있습니다:

```php
use App\Http\Middleware\First;
use App\Http\Middleware\Second;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->appendToGroup('group-name', [
        First::class,
        Second::class,
    ]);

    $middleware->prependToGroup('group-name', [
        First::class,
        Second::class,
    ]);
})
```



미들웨어 그룹은 개별 미들웨어와 동일한 구문을 사용하여 라우트 및 컨트롤러 동작에 할당될 수 있습니다:

```php
Route::get('/', function () {
    // ...
})->middleware('group-name');

Route::middleware(['group-name'])->group(function () {
    // ...
});
```



<a name="laravels-default-middleware-groups"></a>
#### Laravel 의 기본 미들웨어 그룹

Laravel 에는 웹 및 API 경로에 적용할 수 있는 일반적인 미들웨어를 포함하는 미리 정의된 `web` 및 `api` 미들웨어 그룹이 포함되어 있습니다. Laravel 은 이러한 미들웨어 그룹을 해당하는 `routes/web.php` 및 `routes/api.php` 파일에 자동으로 적용합니다。

<div class="overflow-auto">

| `web` 미들웨어 그룹             |
| ——————————————————————————
| `Illuminate\Cookie\Middleware\EncryptCookies` |
| `Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse` |
| `Illuminate\Session\Middleware\StartSession`     |
| `Illuminate\View\Middleware\ShareErrorsFromSession` |
| `Illuminate\Foundation\Http\Middleware\PreventRequestForgery` |
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

<div class="overflow-auto">

| `api` 미들웨어 그룹 |
| ——————————————————————————
| `Illuminate\Routing\Middleware\SubstituteBindings` |

</div>

이러한 그룹에 미들웨어를 추가하거나 전달하려는 경우 애플리케이션의 `bootstrap/app.php` 파일 내에서 `web` 및 `api` 메서드를 사용할 수 있습니다. `web` 및 `api` 메서드는 `appendToGroup` 메서드에 대한 편리한 대안입니다：

```php
use App\Http\Middleware\EnsureTokenIsValid;
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        EnsureUserIsSubscribed::class,
    ]);

    $middleware->api(prepend: [
        EnsureTokenIsValid::class,
    ]);
})
```



Laravel의 기본 미들웨어 그룹 항목 중 하나를 자신만의 커스텀 미들웨어로 교체할 수도 있습니다:

```php
use App\Http\Middleware\StartCustomSession;
use Illuminate\Session\Middleware\StartSession;

$middleware->web(replace: [
    StartSession::class => StartCustomSession::class,
]);
```



또는 미들웨어를 완전히 제거할 수 있습니다:

```php
$middleware->web(remove: [
    StartSession::class,
]);
```



<a name="manually-managing-laravels-default-middleware-groups"></a>
#### Laravel의 기본 미들웨어 그룹 수동 관리

Laravel의 기본 `web` 및 `api` 미들웨어 그룹 내의 모든 미들웨어를 수동으로 관리하고 싶다면, 그룹을 완전히 다시 정의할 수 있습니다. 아래 예제는 기본 미들웨어와 함께 `web` 및 `api` 미들웨어 그룹을 정의하여 필요에 따라 사용자 지정할 수 있도록 합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->group('web', [
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        // \Illuminate\Session\Middleware\AuthenticateSession::class,
    ]);

    $middleware->group('api', [
        // \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        // 'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ]);
})
```



> [!NOTE]
> 기본적으로 `bootstrap/app.php` 파일에 의해 `web` 및 `api` 미들웨어 그룹이 애플리케이션의 해당 `routes/web.php` 및 `routes/api.php` 파일에 자동으로 적용됩니다.

<a name="middleware-aliases"></a>
### 미들웨어 별칭

애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어에 별칭을 지정할 수 있습니다. 미들웨어 별칭을 사용하면 특정 미들웨어 클래스에 대한 짧은 별칭을 정의할 수 있으며, 이는 클래스 이름이 긴 미들웨어에 특히 유용할 수 있습니다:

```php
use App\Http\Middleware\EnsureUserIsSubscribed;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'subscribed' => EnsureUserIsSubscribed::class
    ]);
})
```



애플리케이션의 `bootstrap/app.php` 파일에서 미들웨어 별칭이 정의되면, 미들웨어를 라우트에 할당할 때 해당 별칭을 사용할 수 있습니다:

```php
Route::get('/profile', function () {
    // ...
})->middleware('subscribed');
```



편의상 Laravel 의 일부 내장 미들웨어는 기본적으로 별칭이 있습니다. 예를 들어 `auth` 미들웨어는 `Illuminate\Auth\Middleware\Authenticate` 미들웨어의 별칭입니다. 기본 미들웨어 별칭 목록은 다음과 같습니다：

<div class="overflow-auto">

| 알리아스             | 미들웨어           
| —————————————————————————————————————————————————
| `auth`    | `Illuminate\Auth\Middleware\Authenticate`            
| `auth.basic` | `Illuminate\Auth\Middleware\AuthenticateWithBasicAuth`
| `auth.session` | `Illuminate\Session\Middleware\AuthenticateSession`
| `cache.headers` | `Illuminate\Http\Middleware\SetCacheHeaders`
| `can` 피 피 피 | `Illuminate\Auth\Middleware\Authorize` 피 피 피
| `guest`     | `Illuminate\Auth\Middleware\RedirectIfAuthenticated`            
| `password.confirm` | `Illuminate\Auth\Middleware\RequirePassword` 자 자 자 자 자
| `precognitive` | `Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests`
| `signed`    | `Illuminate\Routing\Middleware\ValidateSignature`         
| `subscribed` | `\Spark\Http\Middleware\VerifyBillableIsSubscribed` 아            
| `throttle` | `Illuminate\Routing\Middleware\ThrottleRequests` 또는 `Illuminate\Routing\Middleware\ThrottleRequestsWithRedis` |
| `verified`   | `Illuminate\Auth\Middleware\EnsureEmailIsVerified`

</div>

<a name="sorting-middleware"></a>
### 미들웨어 분류

드문 경우이지만， 미들웨어를 특정 순서로 실행해야 하지만 경로에 할당될 때 미들웨어의 순서를 제어할 수 없을 수 있습니다. 이러한 상황에서는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 메서드를 사용하여 미들웨어 우선순위를 지정할 수 있습니다：

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->priority([
        \Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests::class,
        \Illuminate\Cookie\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \Illuminate\Foundation\Http\Middleware\PreventRequestForgery::class,
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
        \Illuminate\Routing\Middleware\ThrottleRequests::class,
        \Illuminate\Routing\Middleware\ThrottleRequestsWithRedis::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \Illuminate\Contracts\Auth\Middleware\AuthenticatesRequests::class,
        \Illuminate\Auth\Middleware\Authorize::class,
    ]);
})
```



기존 우선순위 목록을 교체하지 않고 미들웨어를 추가하고 싶다면, `prependToPriorityList` 또는 `appendToPriorityList` 메서드를 사용할 수 있습니다. `prependToPriorityList` 메서드는 주어진 미들웨어를 다른 미들웨어 앞에 삽입하고, `appendToPriorityList` 메서드는 다른 미들웨어 뒤에 삽입합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\EnsureTokenIsValid::class,
    );

    $middleware->appendToPriorityList(
        after: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        append: \App\Http\Middleware\EnsureUserIsSubscribed::class,
    );
})
```



`before`와 `after` 인수는 미들웨어 클래스의 배열일 수도 있습니다.

<a name="middleware-parameters"></a>
## 미들웨어 매개변수

미들웨어는 추가 매개변수도 받을 수 있습니다. 예를 들어, 애플리케이션이 특정 동작을 수행하기 전에 인증된 사용자가 특정 "역할(role)"을 가지고 있는지 확인해야 하는 경우, 역할 이름을 추가 인수로 받는 `EnsureUserHasRole` 미들웨어를 만들 수 있습니다.

추가 미들웨어 매개변수는 `$next` 인수 뒤에 미들웨어로 전달됩니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class EnsureUserHasRole
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next, string $role): Response
    {
        if (! $request->user()->hasRole($role)) {
            // Redirect...
        }

        return $next($request);
    }
}
```



미들웨어 매개변수는 미들웨어 이름과 매개변수를 `:`로 구분하여 경로를 정의할 때 지정할 수 있습니다:

```php
use App\Http\Middleware\EnsureUserHasRole;

Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor');
```



여러 매개변수는 쉼표로 구분될 수 있습니다:

```php
Route::put('/post/{id}', function (string $id) {
    // ...
})->middleware(EnsureUserHasRole::class.':editor,publisher');
```



<a name="terminable-middleware"></a>
## 종료 가능한 미들웨어

때때로 미들웨어는 HTTP 응답이 브라우저로 전송된 후에 작업을 수행해야 할 때가 있습니다. 미들웨어에 `terminate` 메서드를 정의하고 웹 서버가 [FastCGI](https://www.php.net/manual/en/install.fpm.php)를 사용 중이라면, `terminate` 메서드는 응답이 브라우저로 전송된 후 자동으로 호출됩니다:

```php
<?php

namespace Illuminate\Session\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class TerminatingMiddleware
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        return $next($request);
    }

    /**
     * Handle tasks after the response has been sent to the browser.
     */
    public function terminate(Request $request, Response $response): void
    {
        // ...
    }
}
```



`terminate` 메서드는 요청과 응답을 모두 받아야 합니다. 종료 가능한 미들웨어를 정의한 후에는 애플리케이션의 `bootstrap/app.php` 파일에서 라우트 목록이나 글로벌 미들웨어에 추가해야 합니다.

미들웨어에서 `terminate` 메서드를 호출할 때, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)에서 미들웨어의 새로운 인스턴스를 해결합니다. `handle` 및 `terminate` 메서드가 호출될 때 동일한 미들웨어 인스턴스를 사용하려면, 컨테이너의 `singleton` 메서드를 사용하여 미들웨어를 컨테이너에 등록해야 합니다. 일반적으로 이는 `AppServiceProvider`의 `register` 메서드에서 수행되어야 합니다.

```php
use App\Http\Middleware\TerminatingMiddleware;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(TerminatingMiddleware::class);
}
```
{% endraw %}
