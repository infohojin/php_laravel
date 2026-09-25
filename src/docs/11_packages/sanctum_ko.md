---
layout: docs
title: "라라벨 성역"
---

{% raw %}
# 라라벨 성역

- [소개](#introduction)
- [How It Works](#how-it-works)
- [설치](#installation)
- [구성](#configuration)
- 오버라이딩 디폴트 모델 (#overriding-default-models)
- [API 토큰 인증](#api-token-authentication)
- [API 토큰 발행](#issuing-api-tokens)
- [토큰 능력](#token-abilities)
- [루트 보호](#protecting-routes)
- [Revoking Tokens](#revoking-tokens)
- [토큰 만료](#token-expiration)
- SPA 인증 (#spa-authentication)
- [구성](#spa-configuration)
- [인증](#spa-authenticating)
- [경로 보호](#protecting-spa-routes)
- [프라이빗 브로드캐스트 채널 인증](#authorizing-private-broadcast-channels)
- 모바일 애플리케이션 인증 (#mobile-application-authentication)
- [API 토큰 발행](#issuing-mobile-api-tokens)
- [루트 보호](#protecting-mobile-api-routes)
- [Revoking Tokens](#revoking-mobile-api-tokens)
- 테스팅 (#testing)

<a name="introduction"></a>
## 소개

[Laravel Sanctum](https://github.com/laravel/sanctum) 은 SPA(단일 페이지 애플리케이션), 모바일 애플리케이션 및 간단한 토큰 기반 API 를 위한 가벼운 인증 시스템을 제공합니다. Sanctum 을 사용하면 애플리케이션의 각 사용자가 자신의 계정에 대해 여러 API 토큰을 생성할 수 있습니다. 이러한 토큰에는 토큰이 수행할 수 있는 작업을 지정하는 기능/범위가 부여될 수 있습니다。

<a name="how-it-works"></a>
### 어떻게 작동하는가

라라벨 성소는 두 가지 별개의 문제를 해결하기 위해 존재한다. 도서관을 더 깊이 파고들기 전에 각각에 대해 논의해 보자。

<a name="how-it-works-api-tokens"></a>
#### API 토큰

첫째， Sanctum 은 OAuth 의 복잡성 없이 사용자에게 API 토큰을 발급하는 데 사용할 수 있는 간단한 패키지입니다. 이 기능은 “개인 액세스 토큰” 을 발급하는 GitHub 및 기타 애플리케이션에서 영감을 받았습니다. 예를 들어， 애플리케이션의 “계정 설정” 에 사용자가 자신의 계정에 대한 API 토큰을 생성할 수 있는 화면이 있다고 가정해 보겠습니다. Sanctum 을 사용하여 이러한 토큰을 생성하고 관리할 수 있습니다. 이러한 토큰은 일반적으로 매우 긴 만료 기간 (몇 년) 이 있지만， 사용자가 언제든지 수동으로

Laravel Sanctum 은 사용자 API 토큰을 단일 데이터베이스 테이블에 저장하고 유효한 API 토큰이 포함되어야 하는 `Authorization` 헤더를 통해 수신 HTTP 요청을 인증하여 이 기능을 제공합니다。

<a name="how-it-works-spa-authentication"></a>
#### SPA 인증



둘째， Sanctum 은 Laravel 기반 API 와 통신해야 하는 단일 페이지 애플리케이션 (SPA) 을 인증하는 간단한 방법을 제공하기 위해 존재합니다. 이러한 SPA 는 Laravel 애플리케이션과 동일한 리포지토리에 존재할 수도 있고 Next.js 또는 Nuxt 를 사용하여 생성된 SPA 와 같이 완전히 별도의 리포지토리일 수도 있습니다。

이 기능을 위해 Sanctum 은 어떤 종류의 토큰도 사용하지 않습니다. 대신 Sanctum 은 Laravel 의 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 일반적으로 Sanctum 은 Laravel 의 `web` 인증 가드를 사용하여 이를 달성합니다. 이는 CSRF 보호， 세션 인증의 이점을 제공하며， XSS 를 통한 인증 자격 증명 유출로부터 보호합니다。

Sanctum 은 수신 요청이 자체 SPA 프론트엔드에서 오는 경우에만 쿠키를 사용하여 인증을 시도합니다. Sanctum 이 수신 HTTP 요청을 검사할 때 먼저 인증 쿠키를 확인하고， 쿠키가 없는 경우 `Authorization` 헤더에서 유효한 API 토큰을 검사합니다。

> [!NOTE]
> Sanctum 을 API 토큰 인증에만 사용하거나 SPA 인증에만 사용하는 것은 완벽하게 괜찮습니다. Sanctum 을 사용한다고 해서 그것이 제공하는 두 기능을 모두 사용해야 한다는 의미는 아닙니다。

<a name="installation"></a>
## 설치

`install:api` Artisan 명령을 통해 Laravel Sanctum 을 설치할 수 있습니다：

```shell
php artisan install:api
```



다음으로, Sanctum을 사용하여 SPA를 인증할 계획이라면, 이 문서의 [SPA 인증](#spa-authentication) 섹션을 참조하십시오.

<a name="configuration"></a>
## 구성

<a name="overriding-default-models"></a>
### 기본 모델 재정의

일반적으로 필요하지는 않지만, Sanctum 내부에서 사용하는 `PersonalAccessToken` 모델을 자유롭게 확장할 수 있습니다:

```php
use Laravel\Sanctum\PersonalAccessToken as SanctumPersonalAccessToken;

class PersonalAccessToken extends SanctumPersonalAccessToken
{
    // ...
}
```



그런 다음, Sanctum이 제공한 `usePersonalAccessTokenModel` 방법을 통해 당신의 맞춤 모델을 사용하도록 지시할 수 있습니다. 일반적으로, 이 방법은 애플리케이션의 `AppServiceProvider` 파일의 `boot` 메서드에서 호출해야 합니다:

```php
use App\Models\Sanctum\PersonalAccessToken;
use Laravel\Sanctum\Sanctum;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Sanctum::usePersonalAccessTokenModel(PersonalAccessToken::class);
}
```



<a name="api-token-authentication"></a>
## API 토큰 인증

> [!NOTE]
> 자신의 퍼스트파티 SPA를 인증하기 위해 API 토큰을 사용해서는 안 됩니다. 대신, Sanctum의 내장 [SPA 인증 기능](#spa-authentication)을 사용하세요.

<a name="issuing-api-tokens"></a>
### API 토큰 발급

Sanctum은 API 요청을 인증하는 데 사용할 수 있는 API 토큰/개인 액세스 토큰을 발급할 수 있게 합니다. API 토큰을 사용하여 요청을 할 때, 토큰은 `Authorization` 헤더에 `Bearer` 토큰으로 포함되어야 합니다.

사용자에 대한 토큰 발급을 시작하려면, User 모델이 `Laravel\Sanctum\HasApiTokens` 트레이트를 사용해야 합니다:

```php
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```



토큰을 발급하려면 `createToken` 방법을 사용할 수 있습니다. `createToken` 방법은 `Laravel\Sanctum\NewAccessToken` 인스턴스를 반환합니다. API 토큰은 데이터베이스에 저장되기 전에 SHA-256 해싱을 사용하여 해시되지만, `NewAccessToken` 인스턴스의 `plainTextToken` 속성을 통해 토큰의 일반 텍스트 값을 액세스할 수 있습니다. 토큰이 생성된 직후 이 값을 사용자에게 표시해야 합니다:

```php
use Illuminate\Http\Request;

Route::post('/tokens/create', function (Request $request) {
    $token = $request->user()->createToken($request->token_name);

    return ['token' => $token->plainTextToken];
});
```



`HasApiTokens` 트레이트가 제공하는 `tokens` Eloquent 관계를 사용하여 사용자의 모든 토큰에 접근할 수 있습니다:

```php
foreach ($user->tokens as $token) {
    // ...
}
```



<a name="token-abilities"></a>
### 토큰 능력

Sanctum은 토큰에 "능력"을 할당할 수 있게 합니다. 능력은 OAuth의 "범위(scopes)"와 유사한 목적을 제공합니다. `createToken` 메서드에 두 번째 인수로 문자열 능력 배열을 전달할 수 있습니다:

```php
return $user->createToken('token-name', ['server:update'])->plainTextToken;
```



Sanctum으로 인증된 들어오는 요청을 처리할 때, `tokenCan` 또는 `tokenCant` 메서드를 사용하여 토큰에 특정 능력이 있는지 확인할 수 있습니다:

```php
if ($user->tokenCan('server:update')) {
    // ...
}

if ($user->tokenCant('server:update')) {
    // ...
}
```



<a name="token-ability-middleware"></a>
#### 토큰 권한 미들웨어

Sanctum은 또한 들어오는 요청이 특정 권한이 부여된 토큰으로 인증되었는지 확인하는 데 사용할 수 있는 두 가지 미들웨어를 포함합니다. 시작하려면 애플리케이션의 `bootstrap/app.php` 파일에 다음 미들웨어 별칭을 정의하세요:

```php
use Laravel\Sanctum\Http\Middleware\CheckAbilities;
use Laravel\Sanctum\Http\Middleware\CheckForAnyAbility;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->alias([
        'abilities' => CheckAbilities::class,
        'ability' => CheckForAnyAbility::class,
    ]);
})
```



`abilities` 미들웨어는 들어오는 요청의 토큰이 나열된 모든 권한을 가지고 있는지 확인하기 위해 경로에 할당될 수 있습니다:

```php
Route::get('/orders', function () {
    // Token has both "check-status" and "place-orders" abilities...
})->middleware(['auth:sanctum', 'abilities:check-status,place-orders']);
```



`ability` 미들웨어는 들어오는 요청의 토큰이 나열된 능력 중 *적어도 하나*를 가지고 있는지 확인하기 위해 라우트에 할당될 수 있습니다:

```php
Route::get('/orders', function () {
    // Token has the "check-status" or "place-orders" ability...
})->middleware(['auth:sanctum', 'ability:check-status,place-orders']);
```



<a name="first-party-ui-initiated-requests"></a>
#### 1인칭 UI에서 시작된 요청

편의를 위해, `tokenCan` 메서드는 들어오는 인증된 요청이 귀하의 1인칭 SPA에서 온 경우 및 Sanctum의 내장 [SPA 인증](#spa-authentication)을 사용하는 경우 항상 `true`를 반환합니다.

하지만, 이것이 반드시 애플리케이션이 사용자가 해당 동작을 수행하도록 허용해야 함을 의미하지는 않습니다. 일반적으로 애플리케이션의 [권한 정책](/docs/{{version}}/authorization#creating-policies)은 토큰이 능력을 수행할 권한이 부여되었는지 확인하고, 사용자의 인스턴스 자체가 해당 동작을 수행하도록 허용되어야 하는지도 확인합니다.

예를 들어, 서버를 관리하는 애플리케이션을 상상해본다면, 이는 토큰이 서버를 업데이트할 권한이 있는지 **그리고** 서버가 사용자의 소유인지 확인하는 것을 의미할 수 있습니다:

```php
return $request->user()->id === $server->user_id &&
       $request->user()->tokenCan('server:update');
```



처음에는 `tokenCan` 메서드를 호출하도록 허용하고 제 1 자 UI 에서 시작된 요청에 대해 항상 `true` 를 반환하는 것이 이상해 보일 수 있습니다. 그러나 API 토큰을 항상 사용할 수 있고 `tokenCan` 메서드를 통해 검사할 수 있다고 가정하는 것이 편리합니다. 이 접근 방식을 사용하면 요청이 애플리케이션 UI 에서 트리거되었는지 또는 API 의 제 3 자 소비자 중 한 명에 의해 시작되었는지에 대해 걱정하지 않고도 애플리케이션의 권한 부여 정책 내에서 `tokenCan` 메서드를 항상 호출할 수 있습니다。

<a name="protecting-routes"></a>
### 경로 보호

모든 수신 요청을 인증해야 하도록 경로를 보호하려면 `routes/web.php` 및 `routes/api.php` 경로 파일 내의 보호된 경로에 `sanctum` 인증 가드를 연결해야 합니다. 이 가드는 수신 요청이 상태 저장， 쿠키 인증 요청으로 인증되거나， 요청이 타사에서 온 경우 유효한 API 토큰 헤더를 포함하도록 보장합니다。

`sanctum` 가드를 사용하여 애플리케이션의 `routes/web.php` 파일 내 경로를 인증하도록 제안하는 이유를 궁금해할 수 있습니다. Sanctum 은 먼저 Laravel 의 일반적인 세션 인증 쿠키를 사용하여 수신 요청을 인증하려고 시도합니다. 해당 쿠키가 없는 경우 Sanctum 은 요청의 `Authorization` 헤더에 있는 토큰을 사용하여 요청을 인증하려고 합니다. 또한 Sanctum 을 사용하여 모든 요청을 인증하면 현재 인증된 사용자 인스턴스에서 `tokenCan` 메서드를 항상 호출할 수 있습니다：

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```



<a name="revoking-tokens"></a>
### 토큰 취소

`Laravel\Sanctum\HasApiTokens` 특성이 제공하는 `tokens` 관계를 사용하여 데이터베이스에서 토큰을 삭제함으로써 토큰을 "취소"할 수 있습니다:

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke the token that was used to authenticate the current request...
$request->user()->currentAccessToken()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```



<a name="token-expiration"></a>
### 토큰 만료

기본적으로 Sanctum 토큰은 만료되지 않으며 [토큰 취소](#revoking-tokens)를 통해서만 무효화될 수 있습니다. 그러나 애플리케이션의 API 토큰에 대한 만료 시간을 구성하고 싶다면, 애플리케이션의 `sanctum` 구성 파일에 정의된 `expiration` 구성 옵션을 통해 설정할 수 있습니다. 이 구성 옵션은 발급된 토큰이 만료된 것으로 간주될 때까지의 분 수를 정의합니다:

```php
'expiration' => 525600,
```



각 토큰의 만료 시간을 개별적으로 지정하고 싶다면, `createToken` 메서드의 세 번째 인수로 만료 시간을 제공하여 그렇게 할 수 있습니다:

```php
return $user->createToken(
    'token-name', ['*'], now()->plus(weeks: 1)
)->plainTextToken;
```



애플리케이션에 토큰 만료 시간을 설정한 경우, 애플리케이션의 만료된 토큰을 정리하기 위해 [작업을 예약](/docs/{{version}}/scheduling)하고 싶을 수도 있습니다. 다행히도, Sanctum에는 이를 수행할 수 있는 `sanctum:prune-expired` Artisan 명령어가 포함되어 있습니다. 예를 들어, 최소 24시간 동안 만료된 모든 토큰 데이터베이스 레코드를 삭제하도록 예약된 작업을 구성할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('sanctum:prune-expired --hours=24')->daily();
```

<a name="spa-authentication"></a>
## SPA 인증

Sanctum 은 Laravel 기반 API 와 통신해야 하는 단일 페이지 애플리케이션 (SPA) 을 인증하는 간단한 방법을 제공하기 위해 존재합니다. 이러한 SPA 는 Laravel 애플리케이션과 동일한 저장소에 존재할 수도 있고 완전히 별도의 저장소일 수도 있습니다。

이 기능을 위해 Sanctum 은 어떤 종류의 토큰도 사용하지 않습니다. 대신 Sanctum 은 Laravel 의 내장된 쿠키 기반 세션 인증 서비스를 사용합니다. 이러한 인증 접근 방식은 CSRF 보호， 세션 인증뿐만 아니라 XSS 를 통한 인증 자격 증명 유출로부터 보호하는 이점을 제공합니다。

> [!WARNING]
> 인증을 위해서는 SPA 와 API 가 동일한 최상위 도메인을 공유해야 합니다. 그러나 서로 다른 하위 도메인에 배치될 수 있습니다. 또한 요청과 함께 `Accept: application/json` 헤더와 `Referer` 또는 `Origin` 헤더를 보내야 합니다。

<a name="spa-configuration"></a>
### 구성

<a name="configuring-your-first-party-domains"></a>
#### 자사 도메인 구성

먼저 SPA 가 요청을 수행할 도메인을 구성해야 합니다. `sanctum` 구성 파일의 `stateful` 구성 옵션을 사용하여 이러한 도메인을 구성할 수 있습니다. 이 구성 설정은 API 에 요청할 때 Laravel 세션 쿠키를 사용하여 “상태 저장” 인증을 유지할 도메인을 결정합니다。

제 1 자 상태 저장 도메인을 설정하는 데 도움이 되도록 Sanctum 은 구성에 포함할 수 있는 두 가지 도우미 함수를 제공합니다. 첫째， `Sanctum::currentApplicationUrlWithPort()` 는 `APP_URL` 환경 변수에서 현재 애플리케이션 URL 을 반환하고， `Sanctum::currentRequestHost()` 는 상태 저장 도메인 목록에 위치 지정자를 삽입합니다. 이 위치 지정자는 런타임에 현재 요청의 호스트로 대체되므로 동일한 도메인의 모든 요청이 상태 저장된 것으로 간주됩니다。

> [!WARNING]
> 포트 (`127.0.0.1:8000`) 가 포함된 URL 을 통해 애플리케이션에 액세스하는 경우 도메인과 함께 포트 번호를 포함해야 합니다。

<a name="sanctum-middleware"></a>
#### 성역 미들웨어



다음으로, SPA에서 오는 요청이 Laravel의 세션 쿠키를 사용하여 인증할 수 있도록 Laravel에 지시하면서도, 제3자나 모바일 애플리케이션에서 오는 요청은 API 토큰을 사용하여 인증할 수 있도록 허용해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `statefulApi` 미들웨어 메서드를 호출하여 쉽게 수행할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->statefulApi();
})
```



<a name="cors-and-cookies"></a>
#### CORS 및 쿠키

별도의 서브도메인에서 실행되는 SPA에서 애플리케이션 인증에 문제가 발생하는 경우, CORS(교차 출처 리소스 공유) 또는 세션 쿠키 설정을 잘못 구성했을 가능성이 높습니다.

`config/cors.php` 구성 파일은 기본적으로 게시되지 않습니다. Laravel의 CORS 옵션을 사용자 정의해야 하는 경우, `config:publish` Artisan 명령을 사용하여 전체 `cors` 구성 파일을 게시해야 합니다:

```shell
php artisan config:publish cors
```



다음으로, 애플리케이션의 CORS 설정이 `Access-Control-Allow-Credentials` 헤더를 `True` 값으로 반환하도록 해야 합니다. 이는 애플리케이션의 `config/cors.php` 설정 파일 내에서 `supports_credentials` 옵션을 `true`로 설정하여 수행할 수 있습니다.

또한, 애플리케이션의 전역 `axios` 인스턴스에서 `withCredentials` 및 `withXSRFToken` 옵션을 활성화해야 합니다. 이는 `resources/js/app.js` 파일에서 수행할 수 있습니다. 프런트엔드에서 Axios를 사용하여 HTTP 요청을 하지 않는 경우, 자체 HTTP 클라이언트에서 동일한 구성을 수행해야 합니다.

```js
axios.defaults.withCredentials = true;
axios.defaults.withXSRFToken = true;
```



마지막으로, 애플리케이션의 세션 쿠키 도메인 설정이 루트 도메인의 모든 서브도메인을 지원하는지 확인해야 합니다. 애플리케이션의 `config/session.php` 구성 파일 내에서 도메인 앞에 `.`를 접두사로 붙이면 이를 달성할 수 있습니다:

```php
'domain' => '.domain.com',
```



<a name="spa-authenticating"></a>
### 인증

<a name="csrf-protection"></a>
#### CSRF 보호

SPA를 인증하려면, SPA의 "로그인" 페이지가 먼저 `/sanctum/csrf-cookie` 엔드포인트에 요청을 보내 애플리케이션의 CSRF 보호를 초기화해야 합니다:

```js
axios.get('/sanctum/csrf-cookie').then(response => {
    // Login...
});
```

이 요청 중에 Laravel 은 현재 CSRF 토큰을 포함하는 `XSRF-TOKEN` 쿠키를 설정합니다. 그런 다음 이 토큰은 URL 로 디코딩되어 후속 요청에서 `X-XSRF-TOKEN` 헤더로 전달되어야 합니다. 이는 Axios 및 Angular HttpClient 와 같은 일부 HTTP 클라이언트 라이브러리가 자동으로 수행합니다. JavaScript HTTP 라이브러리가 값을 설정하지 않는 경우， 이 경로에 의해 설정된 `XSRF-TOKEN` 쿠키의 URL 로 디코딩된 값과 일치하도록 `X-XSRF-TOKEN` 헤더를 수동으로 설정해야 합니다。

<a name="logging-in"></a>
#### 로그인

CSRF 보호가 초기화되면 Laravel 애플리케이션의 `/login` 경로에 `POST` 요청을 수행해야 합니다. 이 `/login` 경로는 [수동 구현](/docs/{{version}}/authentication#authenticating-users) 이거나 [Laravel Fortify](/docs/{{version}}/fortify) 와 같은 헤드리스 인증 패키지를 사용할 수 있습니다。

로그인 요청이 성공하면 인증을 받게 되며， 애플리케이션의 경로에 대한 후속 요청은 Laravel 애플리케이션이 클라이언트에 발급한 세션 쿠키를 통해 자동으로 인증됩니다. 또한 애플리케이션이 이미 `/sanctum/csrf-cookie` 경로에 대한 요청을 했기 때문에， JavaScript HTTP 클라이언트가 `X-XSRF-TOKEN` 헤더에서 `XSRF-TOKEN` 쿠키의 값을 전송하는 한 후속 요청은 자동으로 CSRF 보호를 받아야 합니다。

물론， 활동 부족으로 인해 사용자의 세션이 만료되면 Laravel 애플리케이션에 대한 후속 요청에서 401 또는 419 HTTP 오류 응답을 받을 수 있습니다. 이 경우 사용자를 SPA 의 로그인 페이지로 리디렉션해야 합니다。

SPA 인증에 대한 이 접근 방식은 세션 기반이므로 [“remember me”](/docs/{{version}}/authentication#remembering-users) 기능을 포함하여 Laravel 의 표준 인증 서비스를 사용할 수 있습니다。

> [!WARNING]
> 자신만의 `/login` 엔드포인트를 자유롭게 작성할 수 있습니다. 하지만 표준인 [Laravel 이 제공하는 세션 기반 인증 서비스](/docs/{{version}}/authentication#authenticating-users) 를 사용하여 사용자를 인증해야 합니다. 일반적으로 이는 `web` 인증 가드를 사용한다는 의미입니다。

<a name="protecting-spa-routes"></a>
### 경로 보호



모든 들어오는 요청이 인증되도록 경로를 보호하려면, `routes/api.php` 파일 내의 API 경로에 `sanctum` 인증 가드를 첨부해야 합니다. 이 가드는 들어오는 요청이 SPA에서 온 상태 기반 인증 요청인지, 또는 요청이 제3자로부터 온 경우 유효한 API 토큰 헤더를 포함하는지 확인합니다:

```php
use Illuminate\Http\Request;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```



<a name="authorizing-private-broadcast-channels"></a>
### 개인 방송 채널 권한 부여

만약 당신의 SPA가 [개인 / 프리젠스 방송 채널](/docs/{{version}}/broadcasting#authorizing-channels)과 인증해야 한다면, 애플리케이션의 `bootstrap/app.php` 파일에 포함된 `withRouting` 메서드에서 `channels` 항목을 제거해야 합니다. 대신, 애플리케이션의 방송 경로에 올바른 미들웨어를 지정할 수 있도록 `withBroadcasting` 메서드를 호출해야 합니다:

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        // ...
    )
    ->withBroadcasting(
        __DIR__.'/../routes/channels.php',
        ['prefix' => 'api', 'middleware' => ['api', 'auth:sanctum']],
    )
    ->create();
```



다음으로, Pusher의 인증 요청이 성공하려면 [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)를 초기화할 때 커스텀 Pusher `authorizer`를 제공해야 합니다. 이를 통해 애플리케이션에서 Pusher가 [교차 도메인 요청에 적절히 구성된](#cors-and-cookies) `axios` 인스턴스를 사용하도록 설정할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: "pusher",
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    encrypted: true,
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    authorizer: (channel, options) => {
        return {
            authorize: (socketId, callback) => {
                axios.post('/api/broadcasting/auth', {
                    socket_id: socketId,
                    channel_name: channel.name
                })
                .then(response => {
                    callback(false, response.data);
                })
                .catch(error => {
                    callback(true, error);
                });
            }
        };
    },
})
```



<a name="mobile-application-authentication"></a>
## 모바일 애플리케이션 인증

Sanctum 토큰을 사용하여 모바일 애플리케이션에서 API 로의 요청을 인증할 수도 있습니다. 모바일 애플리케이션 요청을 인증하는 프로세스는 타사 API 요청을 인증하는 것과 유사합니다. 단， API 토큰을 발급하는 방법에는 약간의 차이가 있습니다。

<a name="issuing-mobile-api-tokens"></a>
### API 토큰 발행

시작하려면 사용자의 이메일/사용자 이름， 비밀번호 및 장치 이름을 수락하는 경로를 생성한 다음， 이러한 자격 증명을 새 Sanctum 토큰과 교환합니다. 이 끝점에 제공되는 “장치 이름” 은 정보 제공 목적으로 사용되며 원하는 어떤 값이든 될 수 있습니다. 일반적으로 장치 이름 값은 “Nuno 의 iPhone 17” 과 같이 사용자가 인식할 수 있는 이름이어야 합니다。

일반적으로 모바일 애플리케이션의 “로그인” 화면에서 토큰 엔드포인트에 요청을 하게 됩니다. 엔드포인트는 일반 텍스트 API 토큰을 반환하며， 이는 모바일 디바이스에 저장되어 추가 API 요청을 하는 데 사용될 수 있습니다：

```php
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

Route::post('/sanctum/token', function (Request $request) {
    $request->validate([
        'email' => 'required|email',
        'password' => 'required',
        'device_name' => 'required',
    ]);

    $user = User::where('email', $request->email)->first();

    if (! $user || ! Hash::check($request->password, $user->password)) {
        throw ValidationException::withMessages([
            'email' => ['The provided credentials are incorrect.'],
        ]);
    }

    return $user->createToken($request->device_name)->plainTextToken;
});
```



모바일 애플리케이션이 토큰을 사용하여 귀하의 애플리케이션에 API 요청을 할 때, 토큰을 `Authorization` 헤더에 `Bearer` 토큰으로 전달해야 합니다.

> [!NOTE]
> 모바일 애플리케이션용 토큰을 발급할 때 [토큰 권한](#token-abilities)을 지정할 수도 있습니다.

<a name="protecting-mobile-api-routes"></a>
### 경로 보호

앞서 문서화된 바와 같이, 모든 들어오는 요청이 인증되도록 경로를 보호할 수 있으며, 이를 위해 `sanctum` 인증 가드를 경로에 첨부하면 됩니다:

```php
Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```



<a name="revoking-mobile-api-tokens"></a>
### 토큰 취소

사용자가 모바일 기기에 발급된 API 토큰을 취소할 수 있도록 하려면, 웹 애플리케이션 UI의 '계정 설정' 부분에서 이름과 함께 '취소' 버튼을 나열할 수 있습니다. 사용자가 '취소' 버튼을 클릭하면 데이터베이스에서 토큰을 삭제할 수 있습니다. `Laravel\Sanctum\HasApiTokens` 트레이트에서 제공하는 `tokens` 관계를 통해 사용자의 API 토큰에 접근할 수 있다는 것을 기억하세요:

```php
// Revoke all tokens...
$user->tokens()->delete();

// Revoke a specific token...
$user->tokens()->where('id', $tokenId)->delete();
```



<a name="testing"></a>
## 테스트

테스트하는 동안, `Sanctum::actingAs` 방법을 사용하여 사용자를 인증하고 그들의 토큰에 부여될 능력을 지정할 수 있습니다:```php tab=Pest
use App\Models\User;
use Laravel\Sanctum\Sanctum;

test('task list can be retrieved', function () {
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Sanctum\Sanctum;

public function test_task_list_can_be_retrieved(): void
{
    Sanctum::actingAs(
        User::factory()->create(),
        ['view-tasks']
    );

    $response = $this->get('/api/task');

    $response->assertOk();
}
```



토큰에 모든 능력을 부여하려면 `actingAs` 메서드에 제공된 능력 목록에 `*`를 포함해야 합니다:

```php
Sanctum::actingAs(
    User::factory()->create(),
    ['*']
);
```
{% endraw %}
