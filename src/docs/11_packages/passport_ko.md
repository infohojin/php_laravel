---
layout: docs
title: "라라벨 패스포트"
---

{% raw %}
# 라라벨 패스포트

- [Introduction](#introduction)
    - [Passport or Sanctum?](#passport-or-sanctum)
- [Installation](#installation)
    - [Deploying Passport](#deploying-passport)
    - [Upgrading Passport](#upgrading-passport)
- [Configuration](#configuration)
    - [Token Lifetimes](#token-lifetimes)
    - [Overriding Default Models](#overriding-default-models)
    - [Overriding Routes](#overriding-routes)
- [Authorization Code Grant](#authorization-code-grant)
    - [Managing Clients](#managing-clients)
    - [Requesting Tokens](#requesting-tokens)
    - [Managing Tokens](#managing-tokens)
    - [Refreshing Tokens](#refreshing-tokens)
    - [Revoking Tokens](#revoking-tokens)
    - [Purging Tokens](#purging-tokens)
- [Authorization Code Grant With PKCE](#code-grant-pkce)
    - [Creating the Client](#creating-a-auth-pkce-grant-client)
    - [Requesting Tokens](#requesting-auth-pkce-grant-tokens)
- [Device Authorization Grant](#device-authorization-grant)
    - [Creating a Device Authorization Grant Client](#creating-a-device-authorization-grant-client)
    - [Requesting Tokens](#requesting-device-authorization-grant-tokens)
- [Password Grant](#password-grant)
    - [Creating a Password Grant Client](#creating-a-password-grant-client)
    - [Requesting Tokens](#requesting-password-grant-tokens)
    - [Requesting All Scopes](#requesting-all-scopes)
    - [Customizing the User Provider](#customizing-the-user-provider)
    - [Customizing the Username Field](#customizing-the-username-field)
    - [Customizing the Password Validation](#customizing-the-password-validation)
- [Implicit Grant](#implicit-grant)
- [Client Credentials Grant](#client-credentials-grant)
    - [Retrieving Tokens](#retrieving-tokens)
- [Personal Access Tokens](#personal-access-tokens)
    - [Creating a Personal Access Client](#creating-a-personal-access-client)
    - [Customizing the User Provider](#customizing-the-user-provider-for-pat)
    - [Managing Personal Access Tokens](#managing-personal-access-tokens)
- [Protecting Routes](#protecting-routes)
    - [Via Middleware](#via-middleware)
    - [Passing the Access Token](#passing-the-access-token)
- [Token Scopes](#token-scopes)
    - [Defining Scopes](#defining-scopes)
    - [Default Scope](#default-scope)
    - [Assigning Scopes to Tokens](#assigning-scopes-to-tokens)
    - [Checking Scopes](#checking-scopes)
- [SPA Authentication](#spa-authentication)
- [Events](#events)
- [Testing](#testing)

<a name="introduction"></a>
## Introduction



[Laravel Passport](https://github.com/laravel/passport) provides a full OAuth2 server implementation for your Laravel application in a matter of minutes. Passport is built on top of the [League OAuth2 server](https://github.com/thephpleague/oauth2-server) that is maintained by Andy Millington and Simon Hamp.

> [!NOTE]
> This documentation assumes you are already familiar with OAuth2. If you do not know anything about OAuth2, consider familiarizing yourself with the general [terminology](https://oauth2.thephpleague.com/terminology/) and features of OAuth2 before continuing.

<a name="passport-or-sanctum"></a>
### Passport or Sanctum?

Before getting started, you may wish to determine if your application would be better served by Laravel Passport or [Laravel Sanctum](/docs/{{version}}/sanctum). If your application absolutely needs to support OAuth2, then you should use Laravel Passport.

However, if you are attempting to authenticate a single-page application, mobile application, or issue API tokens, you should use [Laravel Sanctum](/docs/{{version}}/sanctum). Laravel Sanctum does not support OAuth2; however, it provides a much simpler API authentication development experience.

<a name="installation"></a>
## Installation

You may install Laravel Passport via the `install:api` Artisan command:

```shell
php artisan install:api --passport
```



이 명령어는 애플리케이션이 OAuth2 클라이언트와 액세스 토큰을 저장하는 데 필요한 테이블을 생성하기 위해 필요한 데이터베이스 마이그레이션을 게시하고 실행합니다. 또한 보안 액세스 토큰을 생성하는 데 필요한 암호화 키도 생성합니다.

`install:api` 명령어를 실행한 후, `App\Models\User` 모델에 `Laravel\Passport\HasApiTokens` 트레이트와 `Laravel\Passport\Contracts\OAuthenticatable` 인터페이스를 추가하세요. 이 트레이트는 인증된 사용자의 토큰과 범위를 검사할 수 있는 몇 가지 도우미 메서드를 모델에 제공합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, HasFactory, Notifiable;
}
```



마지막으로, 애플리케이션의 `config/auth.php` 구성 파일에서 `api` 인증 가드를 정의하고 `driver` 옵션을 `passport`로 설정해야 합니다. 이렇게 하면 애플리케이션이 들어오는 API 요청을 인증할 때 Passport의 `TokenGuard`를 사용하도록 지시하게 됩니다:

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],

    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],
],
```



<a name="deploying-passport"></a>
### Passport 배포

애플리케이션 서버에 Passport를 처음 배포할 때, `passport:keys` 명령어를 실행해야 할 가능성이 높습니다. 이 명령어는 Passport가 액세스 토큰을 생성하는 데 필요한 암호화 키를 생성합니다. 생성된 키는 일반적으로 소스 관리에 보관되지 않습니다:

```shell
php artisan passport:keys
```



필요한 경우, Passport의 키를 로드해야 하는 경로를 정의할 수 있습니다. 이를 수행하기 위해 `Passport::loadKeysFrom` 방법을 사용할 수 있습니다. 일반적으로 이 방법은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출되어야 합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::loadKeysFrom(__DIR__.'/../secrets/oauth');
}
```



<a name="loading-keys-from-the-environment"></a>
#### 환경에서 키 로드하기

또는 `vendor:publish` Artisan 명령을 사용하여 Passport의 구성 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=passport-config
```



구성 파일이 게시된 후, 애플리케이션의 암호화 키를 환경 변수로 정의하여 불러올 수 있습니다:

```ini
PASSPORT_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
<private key here>
-----END RSA PRIVATE KEY-----"

PASSPORT_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
<public key here>
-----END PUBLIC KEY-----"
```



<a name="upgrading-passport"></a>
### 패스포트 업그레이드

패스포트의 새로운 주요 버전으로 업그레이드할 때, [업그레이드 가이드](https://github.com/laravel/passport/blob/master/UPGRADE.md)를 주의 깊게 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 구성

<a name="token-lifetimes"></a>
### 토큰 수명

기본적으로 패스포트는 만료 기간이 1년인 장기 액세스 토큰을 발급합니다. 토큰 수명을 더 길거나 짧게 설정하고 싶은 경우, `tokensExpireIn`, `refreshTokensExpireIn`, `personalAccessTokensExpireIn` 메서드를 사용할 수 있습니다. 이 메서드들은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출되어야 합니다:

```php
use Carbon\CarbonInterval;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensExpireIn(CarbonInterval::days(15));
    Passport::refreshTokensExpireIn(CarbonInterval::days(30));
    Passport::personalAccessTokensExpireIn(CarbonInterval::months(6));
}
```



> [!WARNING]
> Passport 데이터베이스 테이블의 `expires_at` 열은 읽기 전용이며 표시 목적으로만 사용됩니다. 토큰을 발급할 때, Passport는 서명되고 암호화된 토큰 내에 만료 정보를 저장합니다. 토큰을 무효화해야 하는 경우 [해지](#revoking-tokens)해야 합니다.

<a name="overriding-default-models"></a>
### 기본 모델 재정의

자체 모델을 정의하고 해당 Passport 모델을 확장하여 Passport에서 내부적으로 사용하는 모델을 자유롭게 확장할 수 있습니다:

```php
use Laravel\Passport\Client as PassportClient;

class Client extends PassportClient
{
    // ...
}
```



모델을 정의한 후에는 `Laravel\Passport\Passport` 클래스를 통해 Passport가 사용자 정의 모델을 사용하도록 지시할 수 있습니다. 일반적으로 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 Passport에 사용자 정의 모델을 알리는 것이 좋습니다:

```php
use App\Models\Passport\AuthCode;
use App\Models\Passport\Client;
use App\Models\Passport\DeviceCode;
use App\Models\Passport\RefreshToken;
use App\Models\Passport\Token;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::useTokenModel(Token::class);
    Passport::useRefreshTokenModel(RefreshToken::class);
    Passport::useAuthCodeModel(AuthCode::class);
    Passport::useClientModel(Client::class);
    Passport::useDeviceCodeModel(DeviceCode::class);
}
```



<a name="overriding-routes"></a>
### 경로 재정의

때때로 Passport에 의해 정의된 경로를 사용자 정의하고 싶을 수 있습니다. 이를 위해 먼저 Passport가 등록한 경로를 무시해야 하며, 애플리케이션의 `AppServiceProvider`의 `register` 메서드에 `Passport::ignoreRoutes`를 추가하면 됩니다:

```php
use Laravel\Passport\Passport;

/**
 * Register any application services.
 */
public function register(): void
{
    Passport::ignoreRoutes();
}
```



그런 다음, Passport가 [그의 라우트 파일](https://github.com/laravel/passport/blob/master/routes/web.php)에 정의한 라우트를 애플리케이션의 `routes/web.php` 파일로 복사하고 원하는 대로 수정할 수 있습니다:

```php
Route::group([
    'as' => 'passport.',
    'prefix' => config('passport.path', 'oauth'),
    'namespace' => '\Laravel\Passport\Http\Controllers',
], function () {
    // Passport routes...
});
```



<a name="authorization-code-grant"></a>
## 인증 코드 그랜트

인증 코드를 통해 OAuth2를 사용하는 것은 대부분의 개발자가 OAuth2에 익숙해지는 방법입니다. 인증 코드를 사용할 때, 클라이언트 애플리케이션은 사용자를 귀하의 서버로 리디렉션하며, 사용자는 클라이언트에 액세스 토큰을 발급 요청을 승인하거나 거부하게 됩니다.

시작하려면, Passport가 우리의 "authorization" 뷰를 반환하도록 지시해야 합니다.

모든 인증 뷰의 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공되는 적절한 메서드를 사용하여 사용자 정의할 수 있습니다. 일반적으로, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이 메서드를 호출해야 합니다:

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::authorizationView('auth.oauth.authorize');

    // By providing a closure...
    Passport::authorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );
}
```



Passport will automatically define the `/oauth/authorize` route that returns this view. Your `auth.oauth.authorize` template should include a form that makes a POST request to the `passport.authorizations.approve` route to approve the authorization and a form that makes a DELETE request to the `passport.authorizations.deny` route to deny the authorization. The `passport.authorizations.approve` and `passport.authorizations.deny` routes expect `state`, `client_id`, and `auth_token` fields.

<a name="managing-clients"></a>
### Managing Clients

Developers building applications that need to interact with your application's API will need to register their application with yours by creating a "client". Typically, this consists of providing the name of their application and a URI that your application can redirect to after users approve their request for authorization.

<a name="managing-first-party-clients"></a>
#### First-Party Clients

The simplest way to create a client is using the `passport:client` Artisan command. This command may be used to create first-party clients or testing your OAuth2 functionality. When you run the `passport:client` command, Passport will prompt you for more information about your client and will provide you with a client ID and secret:

```shell
php artisan passport:client
```



클라이언트에 대해 여러 리디렉션 URI를 허용하려면 `passport:client` 명령어에서 URI를 요청할 때 쉼표로 구분된 목록을 사용하여 지정할 수 있습니다. 쉼표가 포함된 URI는 URI 인코딩해야 합니다:

```shell
https://third-party-app.com/callback,https://example.com/oauth/redirect
```



<a name="managing-third-party-clients"></a>
#### 제3자 클라이언트

귀하의 애플리케이션 사용자는 `passport:client` 명령을 사용할 수 없기 때문에, `Laravel\Passport\ClientRepository` 클래스의 `createAuthorizationCodeGrantClient` 메서드를 사용하여 특정 사용자에 대한 클라이언트를 등록할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

// Creating an OAuth app client that belongs to the given user...
$client = app(ClientRepository::class)->createAuthorizationCodeGrantClient(
    user: $user,
    name: 'Example App',
    redirectUris: ['https://third-party-app.com/callback'],
    confidential: false,
    enableDeviceFlow: true
);

// Retrieving all the OAuth app clients that belong to the user...
$clients = $user->oauthApps()->get();
```



`createAuthorizationCodeGrantClient` 메서드는 `Laravel\Passport\Client`의 인스턴스를 반환합니다. 사용자는 `$client->id`를 클라이언트 ID로, `$client->plainSecret`를 클라이언트 시크릿으로 표시할 수 있습니다.

<a name="requesting-tokens"></a>
### 토큰 요청

<a name="requesting-tokens-redirecting-for-authorization"></a>
#### 권한 부여를 위한 리디렉션

클라이언트가 생성되면, 개발자는 자신의 클라이언트 ID와 시크릿을 사용하여 귀하의 애플리케이션에서 권한 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 소비하는 애플리케이션은 다음과 같이 귀하의 애플리케이션 `/oauth/authorize` 경로로 리디렉션 요청을 수행해야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```



The `prompt` parameter may be used to specify the authentication behavior of the Passport application.

If the `prompt` value is `none`, Passport will always throw an authentication error if the user is not already authenticated with the Passport application. If the value is `consent`, Passport will always display the authorization approval screen, even if all scopes were previously granted to the consuming application. When the value is `login`, the Passport application will always prompt the user to re-login to the application, even if they already have an existing session.

If no `prompt` value is provided, the user will be prompted for authorization only if they have not previously authorized access to the consuming application for the requested scopes.

> [!NOTE]
> Remember, the `/oauth/authorize` route is already defined by Passport. You do not need to manually define this route.

<a name="approving-the-request"></a>
#### Approving the Request

When receiving authorization requests, Passport will automatically respond based on the value of `prompt` parameter (if present) and may display a template to the user allowing them to approve or deny the authorization request. If they approve the request, they will be redirected back to the `redirect_uri` that was specified by the consuming application. The `redirect_uri` must match the `redirect` URL that was specified when the client was created.

Sometimes you may wish to skip the authorization prompt, such as when authorizing a first-party client. You may accomplish this by [extending the `Client` model](#overriding-default-models) and defining a `skipsAuthorization` method. If `skipsAuthorization` returns `true` the client will be approved and the user will be redirected back to the `redirect_uri` immediately, unless the consuming application has explicitly set the `prompt` parameter when redirecting for authorization:

```php
<?php

namespace App\Models\Passport;

use Illuminate\Contracts\Auth\Authenticatable;
use Laravel\Passport\Client as BaseClient;

class Client extends BaseClient
{
    /**
     * Determine if the client should skip the authorization prompt.
     *
     * @param  \Laravel\Passport\Scope[]  $scopes
     */
    public function skipsAuthorization(Authenticatable $user, array $scopes): bool
    {
        return $this->firstParty();
    }
}
```



<a name="requesting-tokens-converting-authorization-codes-to-access-tokens"></a>
#### 인증 코드(Authorization Codes)를 액세스 토큰(Access Tokens)으로 변환하기

사용자가 인증 요청을 승인하면, 사용자는 소비 애플리케이션으로 다시 리디렉션됩니다. 소비자는 리디렉션 이전에 저장된 값과 `state` 매개변수를 먼저 확인해야 합니다. 상태(state) 매개변수가 일치하면, 소비자는 애플리케이션에 `POST` 요청을 보내 액세스 토큰을 요청해야 합니다. 요청에는 사용자가 인증 요청을 승인할 때 애플리케이션에서 발급한 인증 코드가 포함되어야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class,
        'Invalid state value.'
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code' => $request->code,
    ]);

    return $response->json();
});
```



이 `/oauth/token` 경로는 `access_token`, `refresh_token` 및 `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성은 액세스 토큰이 만료될 때까지 남은 초 수를 포함합니다.

> [!NOTE]
> `/oauth/authorize` 경로와 마찬가지로, `/oauth/token` 경로는 Passport에서 자동으로 정의됩니다. 이 경로를 수동으로 정의할 필요가 없습니다.

<a name="managing-tokens"></a>
### 토큰 관리

사용자의 승인된 토큰은 `Laravel\Passport\HasApiTokens` 트레이트의 `tokens` 메서드를 사용하여 검색할 수 있습니다. 예를 들어, 이는 사용자가 제3자 애플리케이션과의 연결 상태를 추적할 수 있는 대시보드를 제공하는 데 사용될 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Retrieving all of the valid tokens for the user...
$tokens = $user->tokens()
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get();

// Retrieving all the user's connections to third-party OAuth app clients...
$connections = $tokens->load('client')
    ->reject(fn (Token $token) => $token->client->firstParty())
    ->groupBy('client_id')
    ->map(fn (Collection $tokens) => [
        'client' => $tokens->first()->client,
        'scopes' => $tokens->pluck('scopes')->flatten()->unique()->values()->all(),
        'tokens_count' => $tokens->count(),
    ])
    ->values();
```



<a name="refreshing-tokens"></a>
### 토큰 갱신

귀하의 애플리케이션이 단기 액세스 토큰을 발급하는 경우, 사용자는 액세스 토큰이 발급될 때 제공된 리프레시 토큰을 통해 액세스 토큰을 갱신해야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'refresh_token',
    'refresh_token' => 'the-refresh-token',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'scope' => 'user:read orders:create',
]);

return $response->json();
```



이 `/oauth/token` 경로는 `access_token`, `refresh_token` 및 `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료될 때까지 남은 초가 포함되어 있습니다.

<a name="revoking-tokens"></a>
### 토큰 취소

`Laravel\Passport\Token` 모델에서 `revoke` 메서드를 사용하여 토큰을 취소할 수 있습니다. `Laravel\Passport\RefreshToken` 모델에서 `revoke` 메서드를 사용하여 토큰의 리프레시 토큰을 취소할 수 있습니다:

```php
use Laravel\Passport\Passport;
use Laravel\Passport\Token;

$token = Passport::token()->find($tokenId);

// Revoke an access token...
$token->revoke();

// Revoke the token's refresh token...
$token->refreshToken?->revoke();

// Revoke all of the user's tokens...
User::find($userId)->tokens()->each(function (Token $token) {
    $token->revoke();
    $token->refreshToken?->revoke();
});
```



<a name="purging-tokens"></a>
### 토큰 정리

토큰이 취소되거나 만료된 경우, 데이터베이스에서 이를 정리하고 싶을 수 있습니다. Passport에 포함된 `passport:purge` Artisan 명령이 이를 수행할 수 있습니다:

```shell
# Purge revoked and expired tokens, auth codes, and device codes...
php artisan passport:purge

# Only purge tokens expired for more than 6 hours...
php artisan passport:purge --hours=6

# Only purge revoked tokens, auth codes, and device codes...
php artisan passport:purge --revoked

# Only purge expired tokens, auth codes, and device codes...
php artisan passport:purge --expired
```



애플리케이션의 `routes/console.php` 파일에서 [예약 작업](/docs/{{version}}/scheduling)을 구성하여 토큰을 정기적으로 자동 삭제하도록 할 수도 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('passport:purge')->hourly();
```



<a name="code-grant-pkce"></a>
## PKCE를 이용한 인증 코드 부여

"코드 교환을 위한 증명 키(PKCE)"를 사용하는 인증 코드 부여는 단일 페이지 애플리케이션이나 모바일 애플리케이션이 API에 접근할 때 보안을 강화하는 방법입니다. 이 부여 방식은 클라이언트 비밀을 안전하게 저장할 수 없거나 공격자가 인증 코드를 가로챌 위험을 완화해야 할 때 사용해야 합니다. "코드 검증기"와 "코드 챌린지"의 조합은 인증 코드를 액세스 토큰으로 교환할 때 클라이언트 비밀을 대체합니다.

<a name="creating-a-auth-pkce-grant-client"></a>
### 클라이언트 생성

애플리케이션이 PKCE를 이용한 인증 코드 방식을 통해 토큰을 발급할 수 있기 전에, PKCE를 지원하는 클라이언트를 생성해야 합니다. 이는 `passport:client` Artisan 명령어와 `--public` 옵션을 사용하여 수행할 수 있습니다:

```shell
php artisan passport:client --public
```



<a name="requesting-auth-pkce-grant-tokens"></a>
### 토큰 요청

<a name="code-verifier-code-challenge"></a>
#### 코드 검증기와 코드 챌린지

이 인증 부여는 클라이언트 시크릿을 제공하지 않으므로, 개발자는 토큰을 요청하기 위해 코드 검증기와 코드 챌린지의 조합을 생성해야 합니다.

코드 검증기는 [RFC 7636 사양](https://tools.ietf.org/html/rfc7636)에 정의된 대로, 문자, 숫자 및 `"-"`, `"."`, `"_"`, `"~"` 문자를 포함한 43~128자의 임의 문자열이어야 합니다.

코드 챌린지는 URL 및 파일 이름에 안전한 문자로 인코딩된 Base64 문자열이어야 합니다. 끝부분의 `'='` 문자는 제거해야 하며, 줄 바꿈, 공백이나 기타 추가 문자가 존재하지 않아야 합니다.

```php
$encoded = base64_encode(hash('sha256', $codeVerifier, true));

$codeChallenge = strtr(rtrim($encoded, '='), '+/', '-_');
```



<a name="code-grant-pkce-redirecting-for-authorization"></a>
#### 권한 부여를 위해 리디렉션

클라이언트가 생성되면, 클라이언트 ID와 생성된 코드 검증기 및 코드 챌린지를 사용하여 애플리케이션에서 권한 코드와 액세스 토큰을 요청할 수 있습니다. 먼저, 사용하는 애플리케이션은 애플리케이션의 `/oauth/authorize` 경로로 리디렉션 요청을 해야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Str;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $request->session()->put(
        'code_verifier', $codeVerifier = Str::random(128)
    );

    $codeChallenge = strtr(rtrim(
        base64_encode(hash('sha256', $codeVerifier, true))
    , '='), '+/', '-_');

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
        'state' => $state,
        'code_challenge' => $codeChallenge,
        'code_challenge_method' => 'S256',
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```



<a name="code-grant-pkce-converting-authorization-codes-to-access-tokens"></a>
#### 인가 코드를 액세스 토큰으로 변환하기

사용자가 인가 요청을 승인하면 소비자 애플리케이션으로 다시 리디렉션됩니다. 소비자는 표준 인가 코드 부여 방식과 마찬가지로 리디렉션 전에 저장된 값과 `state` 파라미터를 확인해야 합니다.

state 파라미터가 일치하면 소비자는 액세스 토큰을 요청하기 위해 애플리케이션에 `POST` 요청을 발행해야 합니다. 요청에는 사용자가 인가 요청을 승인할 때 애플리케이션에서 발급한 인가 코드와 원래 생성된 코드 검증자(code verifier)를 포함해야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

Route::get('/callback', function (Request $request) {
    $state = $request->session()->pull('state');

    $codeVerifier = $request->session()->pull('code_verifier');

    throw_unless(
        strlen($state) > 0 && $state === $request->state,
        InvalidArgumentException::class
    );

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'authorization_code',
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'code_verifier' => $codeVerifier,
        'code' => $request->code,
    ]);

    return $response->json();
});
```



<a name="device-authorization-grant"></a>
## 디바이스 인증 부여

OAuth2 디바이스 인증 부여는 TV나 게임 콘솔과 같이 브라우저가 없거나 입력이 제한된 디바이스가 "디바이스 코드"를 교환하여 액세스 토큰을 얻을 수 있도록 합니다. 디바이스 플로우를 사용할 때, 디바이스 클라이언트는 사용자가 컴퓨터나 스마트폰과 같은 보조 디바이스를 사용하여 서버에 접속하고 제공된 "사용자 코드"를 입력하여 액세스 요청을 승인하거나 거부하도록 안내합니다.

시작하려면 Passport에 "사용자 코드"와 "인증" 뷰를 반환하도록 지시해야 합니다.

모든 인증 뷰의 렌더링 로직은 `Laravel\Passport\Passport` 클래스에서 제공하는 적절한 메서드를 사용하여 커스터마이즈할 수 있습니다. 일반적으로, 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 이 메서드를 호출해야 합니다.

```php
use Inertia\Inertia;
use Laravel\Passport\Passport;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    // By providing a view name...
    Passport::deviceUserCodeView('auth.oauth.device.user-code');
    Passport::deviceAuthorizationView('auth.oauth.device.authorize');

    // By providing a closure...
    Passport::deviceUserCodeView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/UserCode')
    );

    Passport::deviceAuthorizationView(
        fn ($parameters) => Inertia::render('Auth/OAuth/Device/Authorize', [
            'request' => $parameters['request'],
            'authToken' => $parameters['authToken'],
            'client' => $parameters['client'],
            'user' => $parameters['user'],
            'scopes' => $parameters['scopes'],
        ])
    );

    // ...
}
```



여권(Passport)은 이러한 뷰를 반환하는 경로를 자동으로 정의합니다. 귀하의 `auth.oauth.device.user-code` 템플릿에는 `passport.device.authorizations.authorize` 경로에 GET 요청을 보내는 폼이 포함되어 있어야 합니다. `passport.device.authorizations.authorize` 경로는 `user_code` 쿼리 매개변수를 기대합니다.

귀하의 `auth.oauth.device.authorize` 템플릿에는 권한을 승인하기 위해 `passport.device.authorizations.approve` 경로로 POST 요청을 보내는 폼과, 권한을 거부하기 위해 `passport.device.authorizations.deny` 경로로 DELETE 요청을 보내는 폼이 포함되어야 합니다. `passport.device.authorizations.approve` 및 `passport.device.authorizations.deny` 경로는 `state`, `client_id`, `auth_token` 필드를 기대합니다.

<a name="creating-a-device-authorization-grant-client"></a>
### 디바이스 권한 부여 클라이언트 생성

응용 프로그램이 디바이스 권한 부여 장치를 통해 토큰을 발급할 수 있으려면, 디바이스 플로우가 활성화된 클라이언트를 생성해야 합니다. 이는 `passport:client` Artisan 명령과 `--device` 옵션을 사용하여 수행할 수 있습니다. 이 명령은 1차 장치 플로우가 활성화된 클라이언트를 생성하고 클라이언트 ID와 시크릿을 제공합니다:

```shell
php artisan passport:client --device
```



또한, 지정된 사용자에 속하는 타사 클라이언트를 등록하기 위해 `ClientRepository` 클래스에서 `createDeviceAuthorizationGrantClient` 메서드를 사용할 수 있습니다:

```php
use App\Models\User;
use Laravel\Passport\ClientRepository;

$user = User::find($userId);

$client = app(ClientRepository::class)->createDeviceAuthorizationGrantClient(
    user: $user,
    name: 'Example Device',
    confidential: false,
);
```



<a name="requesting-device-authorization-grant-tokens"></a>
### 토큰 요청

<a name="device-code"></a>
#### 장치 코드 요청

클라이언트가 생성되면, 개발자는 클라이언트 ID를 사용하여 애플리케이션에서 장치 코드를 요청할 수 있습니다. 먼저, 소비 장치는 `POST` 요청을 애플리케이션의 `/oauth/device/code` 경로로 보내 장치 코드를 요청해야 합니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/device/code', [
    'client_id' => 'your-client-id',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```



This will return a JSON response containing `device_code`, `user_code`, `verification_uri`, `interval`, and `expires_in` attributes. The `expires_in` attribute contains the number of seconds until the device code expires. The `interval` attribute contains the number of seconds the consuming device should wait between requests when polling `/oauth/token` route to avoid rate limit errors.

> [!NOTE]
> Remember, the `/oauth/device/code` route is already defined by Passport. You do not need to manually define this route.

<a name="user-code"></a>
#### Displaying the Verification URI and User Code

Once a device code request has been obtained, the consuming device should instruct the user to use another device and visit the provided `verification_uri` and enter the `user_code` in order to approve the authorization request.

<a name="polling-token-request"></a>
#### Polling Token Request

Since the user will be using a separate device to grant (or deny) access, the consuming device should poll your application's `/oauth/token` route to determine when the user has responded to the request. The consuming device should use the minimum polling `interval` provided in the JSON response when requesting device code to avoid rate limit errors:

```php
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Sleep;

$interval = 5;

do {
    Sleep::for($interval)->seconds();

    $response = Http::asForm()->post('https://passport-app.test/oauth/token', [
        'grant_type' => 'urn:ietf:params:oauth:grant-type:device_code',
        'client_id' => 'your-client-id',
        'client_secret' => 'your-client-secret', // Required for confidential clients only...
        'device_code' => 'the-device-code',
    ]);

    if ($response->json('error') === 'slow_down') {
        $interval += 5;
    }
} while (in_array($response->json('error'), ['authorization_pending', 'slow_down']));

return $response->json();
```



사용자가 승인 요청을 승인한 경우, 이는 `access_token`, `refresh_token` 및 `expires_in` 속성을 포함하는 JSON 응답을 반환합니다. `expires_in` 속성에는 액세스 토큰이 만료될 때까지 남은 초 수가 포함됩니다.

<a name="password-grant"></a>
## 비밀번호 부여

> [!WARNING]
> 더 이상 비밀번호 부여 토큰 사용을 권장하지 않습니다. 대신 [현재 OAuth2 서버에서 권장하는 부여 유형](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

OAuth2 비밀번호 부여는 모바일 애플리케이션과 같은 다른 1차 클라이언트가 이메일 주소/사용자 이름과 비밀번호를 사용하여 액세스 토큰을 얻을 수 있도록 합니다. 이를 통해 사용자가 전체 OAuth2 승인 코드 리디렉션 흐름을 거치지 않고도 1차 클라이언트에 안전하게 액세스 토큰을 발급할 수 있습니다.

비밀번호 부여를 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스 내 `boot` 메서드에서 `enablePasswordGrant` 메서드를 호출하십시오:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enablePasswordGrant();
}
```



<a name="creating-a-password-grant-client"></a>
### 비밀번호 그랜트 클라이언트 생성

애플리케이션이 비밀번호 그랜트를 통해 토큰을 발급할 수 있으려면 비밀번호 그랜트 클라이언트를 생성해야 합니다. 이는 `passport:client` Artisan 명령어에 `--password` 옵션을 사용하여 수행할 수 있습니다.

```shell
php artisan passport:client --password
```



<a name="requesting-password-grant-tokens"></a>
### 토큰 요청

권한 부여를 활성화하고 패스워드 권한 클라이언트를 생성한 후, 사용자의 이메일 주소와 비밀번호를 사용하여 `/oauth/token` 경로에 `POST` 요청을 보내 액세스 토큰을 요청할 수 있습니다. 이 경로는 이미 Passport에 의해 등록되어 있으므로 수동으로 정의할 필요가 없습니다. 요청이 성공하면, 서버의 JSON 응답에서 `access_token`와 `refresh_token`를 받게 됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => 'user:read orders:create',
]);

return $response->json();
```



> [!NOTE]
> 기억하세요, 액세스 토큰은 기본적으로 장기 유효합니다. 그러나 필요하다면 [최대 액세스 토큰 수명](#configuration)을 자유롭게 구성할 수 있습니다.

<a name="requesting-all-scopes"></a>
### 모든 범위 요청

비밀번호 그랜트나 클라이언트 자격 증명 그랜트를 사용할 때, 애플리케이션에서 지원하는 모든 범위에 대해 토큰을 승인하고자 할 수 있습니다. 이는 `*` 범위를 요청함으로써 가능합니다. `*` 범위를 요청하면 토큰 인스턴스의 `can` 메서드는 항상 `true`를 반환합니다. 이 범위는 `password` 또는 `client_credentials` 그랜트를 사용하여 발급된 토큰에만 할당될 수 있습니다.

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'password',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret', // Required for confidential clients only...
    'username' => 'taylor@laravel.com',
    'password' => 'my-password',
    'scope' => '*',
]);
```



<a name="customizing-the-user-provider"></a>
### 사용자 제공자(Customizing the User Provider) 맞춤 설정

애플리케이션에서 둘 이상의 [인증 사용자 제공자](/docs/{{version}}/authentication#introduction)를 사용하는 경우, `artisan passport:client --password` 명령을 통해 클라이언트를 생성할 때 `--provider` 옵션을 제공하여 비밀번호 부여 클라이언트가 사용할 사용자 제공자를 지정할 수 있습니다. 제공된 제공자 이름은 애플리케이션의 `config/auth.php` 구성 파일에 정의된 유효한 제공자와 일치해야 합니다. 그런 다음 [미들웨어를 사용하여 경로를 보호](#multiple-authentication-guards)하여 가드의 지정된 제공자에 속한 사용자만 권한이 있는지 확인할 수 있습니다.

<a name="customizing-the-username-field"></a>
### 사용자 이름 필드(Customizing the Username Field) 맞춤 설정

비밀번호 부여를 사용하여 인증할 때, Passport는 인증 가능한 모델의 `email` 속성을 "사용자 이름"으로 사용합니다. 그러나 모델에 `findForPassport` 메서드를 정의하여 이 동작을 사용자 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Passport\Bridge\Client;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Find the user instance for the given username.
     */
    public function findForPassport(string $username, Client $client): User
    {
        return $this->where('username', $username)->first();
    }
}
```



<a name="customizing-the-password-validation"></a>
### 비밀번호 검증 커스터마이징

비밀번호 그랜트를 사용하여 인증할 때, Passport는 주어진 비밀번호를 검증하기 위해 모델의 `password` 속성을 사용합니다. 모델에 `password` 속성이 없거나 비밀번호 검증 로직을 커스터마이징하고자 하는 경우, 모델에 `validateForPassportPasswordGrant` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Support\Facades\Hash;
use Laravel\Passport\Contracts\OAuthenticatable;
use Laravel\Passport\HasApiTokens;

class User extends Authenticatable implements OAuthenticatable
{
    use HasApiTokens, Notifiable;

    /**
     * Validate the password of the user for the Passport password grant.
     */
    public function validateForPassportPasswordGrant(string $password): bool
    {
        return Hash::check($password, $this->password);
    }
}
```



<a name="implicit-grant"></a>
## 암시적 승인

> [!WARNING]
> 더 이상 암시적 승인 토큰 사용을 권장하지 않습니다. 대신 [OAuth2 서버에서 현재 권장하는 승인 유형](https://oauth2.thephpleague.com/authorization-server/which-grant/)을 선택해야 합니다.

암시적 승인은 권한 부여 코드 승인과 유사하지만, 토큰이 권한 부여 코드를 교환하지 않고 클라이언트에 반환됩니다. 이 승인은 클라이언트 자격 증명을 안전하게 저장할 수 없는 JavaScript 또는 모바일 애플리케이션에서 가장 일반적으로 사용됩니다. 승인을 활성화하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enableImplicitGrant` 메서드를 호출하세요:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::enableImplicitGrant();
}
```



귀하의 애플리케이션이 암묵적 승인(implicit grant)을 통해 토큰을 발급하기 전에, 암묵적 승인 클라이언트를 생성해야 합니다. 이는 `--implicit` 옵션과 함께 `passport:client` Artisan 명령어를 사용하여 수행할 수 있습니다.

```shell
php artisan passport:client --implicit
```



일단 그랜트가 활성화되고 암묵적인 클라이언트가 생성되면, 개발자는 자신의 클라이언트 ID를 사용하여 애플리케이션에서 액세스 토큰을 요청할 수 있습니다. 사용하는 애플리케이션은 다음과 같이 귀하의 애플리케이션 `/oauth/authorize` 경로로 리디렉션 요청을 해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/redirect', function (Request $request) {
    $request->session()->put('state', $state = Str::random(40));

    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'token',
        'scope' => 'user:read orders:create',
        'state' => $state,
        // 'prompt' => '', // "none", "consent", or "login"
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```



> [!NOTE]
> 참고로, `/oauth/authorize` 경로는 Passport에 의해 이미 정의되어 있습니다. 이 경로를 수동으로 정의할 필요가 없습니다.

<a name="client-credentials-grant"></a>
## 클라이언트 자격 증명 인증(Client Credentials Grant)

클라이언트 자격 증명 인증은 기계 대 기계(Machine-to-Machine) 인증에 적합합니다. 예를 들어, API를 통해 유지보수 작업을 수행하는 예약된 작업에서 이 인증을 사용할 수 있습니다.

애플리케이션에서 클라이언트 자격 증명 인증을 통해 토큰을 발급하기 전에 클라이언트 자격 증명 인증용 클라이언트를 생성해야 합니다. 이는 `passport:client` Artisan 명령의 `--client` 옵션을 사용하여 수행할 수 있습니다:

```shell
php artisan passport:client --client
```



다음으로, `Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어를 라우트에 할당합니다:

```php
use Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner;

Route::get('/orders', function (Request $request) {
    // Access token is valid and the client is resource owner...
})->middleware(EnsureClientIsResourceOwner::class);
```



특정 범위로 경로에 대한 접근을 제한하려면, `using` 메서드에 필요한 범위 목록을 제공할 수 있습니다:

```php
Route::get('/orders', function (Request $request) {
    // Access token is valid, the client is resource owner, and has both "servers:read" and "servers:create" scopes...
})->middleware(EnsureClientIsResourceOwner::using('servers:read', 'servers:create'));
```



> [!WARNING]
> [기본 OAuth2 서버](https://oauth2.thephpleague.com/database-setup/#:~:text=Please%20note%20that,the%20bearer%20token.)는 클라이언트 자격 증명 토큰의 경우 토큰의 `sub` 클레임을 클라이언트의 식별자로 설정합니다. 기본적으로 Passport는 클라이언트에 UUID를 사용하므로 사용자의 정수형 기본 키와 충돌할 수 없습니다. 그러나 `Passport::$clientUuids`를 `false`로 설정한 경우, 클라이언트 자격 증명 토큰이 클라이언트의 ID와 일치하는 사용자를 의도치 않게 해결할 수 있습니다. 이러한 경우 이 미들웨어를 사용하면 들어오는 토큰이 클라이언트 자격 증명 토큰임을 보장할 수 없습니다.

<a name="retrieving-tokens"></a>
### 토큰 가져오기

이 부여 유형을 사용하여 토큰을 가져오려면 `oauth/token` 엔드포인트에 요청을 하십시오:

```php
use Illuminate\Support\Facades\Http;

$response = Http::asForm()->post('https://passport-app.test/oauth/token', [
    'grant_type' => 'client_credentials',
    'client_id' => 'your-client-id',
    'client_secret' => 'your-client-secret',
    'scope' => 'servers:read servers:create',
]);

return $response->json()['access_token'];
```



<a name="personal-access-tokens"></a>
## 개인 접근 토큰

때로는 사용자가 일반적인 인증 코드 리다이렉션 과정을 거치지 않고 자신에게 액세스 토큰을 발급하고 싶어 할 수도 있습니다. 애플리케이션의 UI를 통해 사용자가 자신에게 토큰을 발급할 수 있도록 허용하는 것은 API를 실험할 수 있게 하거나, 일반적으로 접근 토큰을 발급하는 더 간단한 접근법이 될 수 있습니다.

> [!NOTE]
> 만약 귀하의 애플리케이션이 주로 개인 액세스 토큰 발급에 Passport를 사용한다면, API 접근 토큰 발급을 위한 Laravel의 경량 1자 라이브러리인 [Laravel Sanctum](/docs/{{version}}/sanctum) 사용을 고려해 보세요.

<a name="creating-a-personal-access-client"></a>
### 개인 액세스 클라이언트 생성

애플리케이션이 개인 접근 토큰을 발급하기 전에 개인 접근 클라이언트를 생성해야 합니다. `--personal` 옵션으로 `passport:client` Artisan 명령을 실행하면 가능합니다. 이미 `passport:install` 명령을 실행했다면 다음 명령어를 실행할 필요가 없습니다:

```shell
php artisan passport:client --personal
```



<a name="customizing-the-user-provider-for-pat"></a>
### 사용자 제공자 사용자 정의

애플리케이션에서 하나 이상의 [인증 사용자 제공자](/docs/{{version}}/authentication#introduction)를 사용하는 경우, `artisan passport:client --personal` 명령을 통해 클라이언트를 생성할 때 `--provider` 옵션을 제공하여 개인 액세스 그랜트 클라이언트가 사용할 사용자 제공자를 지정할 수 있습니다. 제공된 제공자 이름은 애플리케이션의 `config/auth.php` 구성 파일에 정의된 유효한 제공자와 일치해야 합니다. 그런 다음 [미들웨어를 사용하여 라우트를 보호](#multiple-authentication-guards)하여 지정된 제공자의 사용자만 권한이 있도록 할 수 있습니다.

<a name="managing-personal-access-tokens"></a>
### 개인 액세스 토큰 관리

개인 액세스 클라이언트를 생성한 후, `App\Models\User` 모델 인스턴스의 `createToken` 메서드를 사용하여 특정 사용자에 대한 토큰을 발급할 수 있습니다. `createToken` 메서드는 첫 번째 인수로 토큰의 이름을 받고, 두 번째 인수로 선택적 [범위](#token-scopes) 배열을 받습니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Date;
use Laravel\Passport\Token;

$user = User::find($userId);

// Creating a token without scopes...
$token = $user->createToken('My Token')->accessToken;

// Creating a token with scopes...
$token = $user->createToken('My Token', ['user:read', 'orders:create'])->accessToken;

// Creating a token with all scopes...
$token = $user->createToken('My Token', ['*'])->accessToken;

// Retrieving all the valid personal access tokens that belong to the user...
$tokens = $user->tokens()
    ->with('client')
    ->where('revoked', false)
    ->where('expires_at', '>', Date::now())
    ->get()
    ->filter(fn (Token $token) => $token->client->hasGrantType('personal_access'));
```



<a name="protecting-routes"></a>
## 경로 보호

<a name="via-middleware"></a>
### 미들웨어를 통해

Passport에는 들어오는 요청의 액세스 토큰을 검증하는 [인증 가드](/docs/{{version}}/authentication#adding-custom-guards)가 포함되어 있습니다. `api` 가드를 `passport` 드라이버를 사용하도록 구성한 후에는, 유효한 액세스 토큰이 필요하도록 하는 모든 경로에 `auth:api` 미들웨어만 지정하면 됩니다:

```php
Route::get('/user', function () {
    // Only API authenticated users may access this route...
})->middleware('auth:api');
```



> [!WARNING]
> [클라이언트 자격 증명 그랜트](#client-credentials-grant)를 사용하고 있다면, `auth:api` 미들웨어 대신 [`Laravel\Passport\Http\Middleware\EnsureClientIsResourceOwner` 미들웨어](#client-credentials-grant)를 사용하여 경로를 보호해야 합니다.

<a name="multiple-authentication-guards"></a>
#### 여러 인증 가드

애플리케이션이 서로 완전히 다른 Eloquent 모델을 사용할 수 있는 다양한 유형의 사용자를 인증하는 경우, 애플리케이션의 각 사용자 공급자 유형에 대해 가드 구성을 정의해야 할 가능성이 높습니다. 이렇게 하면 특정 사용자 공급자를 위한 요청을 보호할 수 있습니다. 예를 들어, 다음과 같은 가드 구성이 있다고 가정하면 `config/auth.php` 구성 파일:

```php
'guards' => [
    'api' => [
        'driver' => 'passport',
        'provider' => 'users',
    ],

    'api-customers' => [
        'driver' => 'passport',
        'provider' => 'customers',
    ],
],
```



다음 경로는 들어오는 요청을 인증하기 위해 `customers` 사용자 제공자를 사용하는 `api-customers` 가드를 사용할 것입니다:

```php
Route::get('/customer', function () {
    // ...
})->middleware('auth:api-customers');
```



> [!NOTE]
> Passport와 함께 여러 사용자 공급자를 사용하는 방법에 대한 자세한 내용은 [개인 액세스 토큰 문서](#customizing-the-user-provider-for-pat)와 [비밀번호 부여 문서](#customizing-the-user-provider)를 참조하십시오.

<a name="passing-the-access-token"></a>
### 액세스 토큰 전달

Passport로 보호되는 경로를 호출할 때, 애플리케이션의 API 소비자는 요청의 `Authorization` 헤더에 `Bearer` 토큰으로 액세스 토큰을 지정해야 합니다. 예를 들어, `Http` Facade를 사용할 때:

```php
use Illuminate\Support\Facades\Http;

$response = Http::withHeaders([
    'Accept' => 'application/json',
    'Authorization' => "Bearer $accessToken",
])->get('https://passport-app.test/api/user');

return $response->json();
```



<a name="token-scopes"></a>
## 토큰 범위

범위(Scopes)는 API 클라이언트가 계정에 접근하기 위한 권한을 요청할 때 특정 권한 집합을 요청할 수 있도록 합니다. 예를 들어, 전자상거래 애플리케이션을 만들고 있는 경우, 모든 API 사용자가 주문을 할 수 있는 권한이 필요하지 않을 수 있습니다. 대신, 사용자가 주문 배송 상태에 접근할 수 있는 권한만 요청하도록 허용할 수 있습니다. 다시 말해, 범위는 애플리케이션 사용자가 타사 애플리케이션이 자신의 대신 수행할 수 있는 작업을 제한할 수 있게 합니다.

<a name="defining-scopes"></a>
### 범위 정의하기

애플리케이션의 `App\Providers\AppServiceProvider` 클래스에서 `boot` 메서드의 `Passport::tokensCan` 메서드를 사용하여 API 범위를 정의할 수 있습니다. `tokensCan` 메서드는 범위 이름과 범위 설명이 담긴 배열을 받습니다. 범위 설명은 원하는 무엇이든 될 수 있으며, 권한 승인 화면에서 사용자에게 표시됩니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::tokensCan([
        'user:read' => 'Retrieve the user info',
        'orders:create' => 'Place orders',
        'orders:read:status' => 'Check order status',
    ]);
}
```



<a name="default-scope"></a>
### 기본 범위

클라이언트가 특정 범위를 요청하지 않는 경우, Passport 서버가 `defaultScopes` 메서드를 사용하여 토큰에 기본 범위를 첨부하도록 구성할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출해야 합니다:

```php
use Laravel\Passport\Passport;

Passport::tokensCan([
    'user:read' => 'Retrieve the user info',
    'orders:create' => 'Place orders',
    'orders:read:status' => 'Check order status',
]);

Passport::defaultScopes([
    'user:read',
    'orders:create',
]);
```



<a name="assigning-scopes-to-tokens"></a>
### 토큰에 권한 범위 할당

<a name="when-requesting-authorization-codes"></a>
#### 인가 코드 요청 시

인가 코드 부여를 사용하여 액세스 토큰을 요청할 때, 사용자는 원하는 권한 범위를 `scope` 쿼리 문자열 매개변수로 지정해야 합니다. `scope` 매개변수는 공백으로 구분된 권한 범위 목록이어야 합니다:

```php
Route::get('/redirect', function () {
    $query = http_build_query([
        'client_id' => 'your-client-id',
        'redirect_uri' => 'https://third-party-app.com/callback',
        'response_type' => 'code',
        'scope' => 'user:read orders:create',
    ]);

    return redirect('https://passport-app.test/oauth/authorize?'.$query);
});
```



<a name="when-issuing-personal-access-tokens"></a>
#### 개인 액세스 토큰 발급 시

`App\Models\User` 모델의 `createToken` 메서드를 사용하여 개인 액세스 토큰을 발급하는 경우, 원하는 범위의 배열을 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
$token = $user->createToken('My Token', ['orders:create'])->accessToken;
```



<a name="checking-scopes"></a>
### 스코프 확인

Passport에는 들어오는 요청이 특정 스코프가 부여된 토큰으로 인증되었는지 확인하는 데 사용할 수 있는 두 가지 미들웨어가 포함되어 있습니다.

<a name="check-for-all-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckToken` 미들웨어는 들어오는 요청의 액세스 토큰에 나열된 모든 스코프가 있는지 확인하기 위해 라우트에 지정될 수 있습니다:

```php
use Laravel\Passport\Http\Middleware\CheckToken;

Route::get('/orders', function () {
    // Access token has both "orders:read" and "orders:create" scopes...
})->middleware(['auth:api', CheckToken::using('orders:read', 'orders:create')]);
```



<a name="check-for-any-scopes"></a>
#### 모든 스코프 확인

`Laravel\Passport\Http\Middleware\CheckTokenForAnyScope` 미들웨어는 들어오는 요청의 액세스 토큰이 나열된 스코프 중 *하나 이상*을 가지고 있는지 확인하기 위해 라우트에 할당될 수 있습니다:

```php
use Laravel\Passport\Http\Middleware\CheckTokenForAnyScope;

Route::get('/orders', function () {
    // Access token has either "orders:read" or "orders:create" scope...
})->middleware(['auth:api', CheckTokenForAnyScope::using('orders:read', 'orders:create')]);
```



<a name="scope-attributes"></a>
#### 범위 속성

응용 프로그램에서 [컨트롤러 미들웨어 속성](/docs/{{version}}/controllers#middleware-attributes)을 사용하는 경우, Passport의 범위 미들웨어를 위한 편리한 바로 가기로 `Laravel\Passport\Attributes\AuthorizeToken` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Laravel\Passport\Attributes\AuthorizeToken;

#[AuthorizeToken('orders:read')]
#[AuthorizeToken('orders:create', only: ['store'])]
class OrderController
{
    #[AuthorizeToken(['orders:read', 'orders:create'], anyScope: true)]
    public function index()
    {
        // Access token has either "orders:read" or "orders:create" scope...
    }

    public function store()
    {
        // Access token has both "orders:read" and "orders:create" scopes...
    }
}
```



기본적으로 `AuthorizeToken` 속성은 모든 지정된 범위를 요구합니다. `anyScope: true`를 전달하면, 토큰이 지정된 범위 중 하나 이상을 포함할 때 요청이 승인됩니다.

<a name="checking-scopes-on-a-token-instance"></a>
#### 토큰 인스턴스에서 범위 확인

액세스 토큰이 인증된 요청으로 애플리케이션에 들어온 후에도, 인증된 `App\Models\User` 인스턴스에서 `tokenCan` 메서드를 사용하여 토큰에 특정 범위가 있는지 확인할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    if ($request->user()->tokenCan('orders:create')) {
        // ...
    }
});
```



<a name="additional-scope-methods"></a>
#### 추가 범위 메서드

`scopeIds` 메서드는 정의된 모든 ID / 이름의 배열을 반환합니다:

```php
use Laravel\Passport\Passport;

Passport::scopeIds();
```



`scopes` 메서드는 모든 정의된 스코프를 `Laravel\Passport\Scope`의 인스턴스로 배열 형태로 반환합니다:

```php
Passport::scopes();
```



`scopesFor` 메서드는 주어진 ID/이름과 일치하는 `Laravel\Passport\Scope` 인스턴스 배열을 반환합니다:

```php
Passport::scopesFor(['user:read', 'orders:create']);
```



다음과 같이 `hasScope` 방법을 사용하여 주어진 범위가 정의되었는지 확인할 수 있습니다:

```php
Passport::hasScope('orders:create');
```



<a name="spa-authentication"></a>
## SPA 인증

API를 구축할 때, JavaScript 애플리케이션에서 자신이 만든 API를 사용할 수 있는 기능은 매우 유용할 수 있습니다. 이러한 API 개발 접근 방식은 자신의 애플리케이션이 세계와 공유하는 동일한 API를 사용할 수 있도록 합니다. 동일한 API는 웹 애플리케이션, 모바일 애플리케이션, 서드파티 애플리케이션 및 다양한 패키지 관리자에서 배포할 수 있는 SDK에서도 사용할 수 있습니다.

일반적으로 JavaScript 애플리케이션에서 API를 사용하려면, 애플리케이션으로 직접 액세스 토큰을 보내고 각 요청마다 함께 전달해야 합니다. 그러나 Passport에는 이를 대신 처리할 수 있는 미들웨어가 포함되어 있습니다. 해야 할 일은 애플리케이션의 `bootstrap/app.php` 파일에서 `web` 미들웨어 그룹에 `CreateFreshApiToken` 미들웨어를 추가하는 것뿐입니다:

```php
use Laravel\Passport\Http\Middleware\CreateFreshApiToken;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->web(append: [
        CreateFreshApiToken::class,
    ]);
})
```



> [!WARNING]
> `CreateFreshApiToken` 미들웨어가 미들웨어 스택에서 마지막으로 나열되도록 해야 합니다.

이 미들웨어는 나가는 응답에 `laravel_token` 쿠키를 첨부합니다. 이 쿠키에는 Passport가 JavaScript 애플리케이션에서 API 요청을 인증하는 데 사용할 암호화된 JWT가 포함되어 있습니다. JWT의 유효 기간은 `session.lifetime` 구성 값과 동일합니다. 이제 브라우저가 모든 후속 요청에 대해 쿠키를 자동으로 전송하므로, 액세스 토큰을 명시적으로 전달하지 않고도 애플리케이션의 API에 요청을 보낼 수 있습니다:

```js
axios.get('/api/user')
    .then(response => {
        console.log(response.data);
    });
```



<a name="customizing-the-cookie-name"></a>
#### 쿠키 이름 사용자 정의

필요한 경우, `Passport::cookie` 메서드를 사용하여 `laravel_token` 쿠키의 이름을 사용자 정의할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 호출되어야 합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Passport::cookie('custom_name');
}
```



<a name="csrf-protection"></a>
#### CSRF Protection

When using this method of authentication, you will need to ensure a valid CSRF token header is included in your requests. The default Laravel JavaScript scaffolding included with the skeleton application and all starter kits includes an [Axios](https://github.com/axios/axios) instance, which will automatically use the encrypted `XSRF-TOKEN` cookie value to send an `X-XSRF-TOKEN` header on same-origin requests.

> [!NOTE]
> If you choose to send the `X-CSRF-TOKEN` header instead of `X-XSRF-TOKEN`, you will need to use the unencrypted token provided by `csrf_token()`.

<a name="events"></a>
## Events

Passport raises events when issuing access tokens and refresh tokens. You may [listen for these events](/docs/{{version}}/events) to prune or revoke other access tokens in your database:

<div class="overflow-auto">

| Event Name                                    |
| --------------------------------------------- |
| `Laravel\Passport\Events\AccessTokenCreated`  |
| `Laravel\Passport\Events\AccessTokenRevoked`  |
| `Laravel\Passport\Events\RefreshTokenCreated` |

</div>

<a name="testing"></a>
## Testing

Passport's `actingAs` method may be used to specify the currently authenticated user as well as its scopes. The first argument given to the `actingAs` method is the user instance and the second is an array of scopes that should be granted to the user's token:```php tab=Pest
use App\Models\User;
use Laravel\Passport\Passport;

test('orders can be created', function () {
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
use App\Models\User;
use Laravel\Passport\Passport;

public function test_orders_can_be_created(): void
{
    Passport::actingAs(
        User::factory()->create(),
        ['orders:create']
    );

    $response = $this->post('/api/orders');

    $response->assertStatus(201);
}
```



Passport의 `actingAsClient` 메서드는 현재 인증된 클라이언트와 그 범위를 지정하는 데 사용될 수 있습니다. `actingAsClient` 메서드에 주어진 첫 번째 인수는 클라이언트 인스턴스이고, 두 번째 인수는 클라이언트의 토큰에 부여되어야 하는 범위의 배열입니다:```php tab=Pest
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

test('servers can be retrieved', function () {
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
use Laravel\Passport\Client;
use Laravel\Passport\Passport;

public function test_servers_can_be_retrieved(): void
{
    Passport::actingAsClient(
        Client::factory()->create(),
        ['servers:read']
    );

    $response = $this->get('/api/servers');

    $response->assertStatus(200);
}
```
{% endraw %}
