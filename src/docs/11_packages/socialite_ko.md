---
layout: docs
title: "socialite_ko"
---

{% raw %}
#라라벨 소셜라이트

- [소개](#introduction)
- [설치](#installation)
- 업그레이딩 소셜라이트 (#upgrading-socialite)
- 컨피그레이션 (#configuration)
- [인증](#authentication)
- [라우팅](#routing)
- [Authentication and Storage](#authentication-and-storage)
- [액세스 스코프](#access-scopes)
- [슬랙 봇 스코프](#slack-bot-scopes)
- [옵션 파라미터](#optional-parameters)
- [사용자 세부 정보 검색](#retrieving-user-details)
- [테스팅](#testing)

<a name="introduction"></a>
## 소개

일반적인 형식 기반 인증 외에도 Laravel 은 [Laravel Socialite](https://github.com/laravel/socialite) 를 사용하여 OAuth 제공자와 인증할 수 있는 간단하고 편리한 방법을 제공합니다. Socialite 는 현재 Facebook, X, LinkedIn, Google, GitHub, GitLab, Bitbucket 및 Slack 을 통한 인증을 지원합니다。

> [!NOTE]
> 다른 플랫폼용 어댑터는 커뮤니티 주도 [Socialite Providers](https://socialiteproviders.com/) 웹사이트를 통해 사용할 수 있습니다。

<a name="installation"></a>
## 설치

Socialite 를 시작하려면 Composer 패키지 관리자를 사용하여 프로젝트의 종속성에 패키지를 추가합니다：

```shell
composer require laravel/socialite

```

<a name="upgrading-socialite"></a>
## 소셜라이트 업그레이드

소셜라이트의 새로운 주요 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/socialite/blob/master/UPGRADE.md)를 꼼꼼히 검토하는 것이 중요합니다.

<a name="configuration"></a>
## 구성

소셜라이트를 사용하기 전에, 애플리케이션에서 사용하는 OAuth 제공자의 자격 증명을 추가해야 합니다. 일반적으로 이러한 자격 증명은 인증을 수행할 서비스 대시보드에서 "개발자 애플리케이션"을 생성하여 가져올 수 있습니다.

이 자격 증명은 애플리케이션의 `config/services.php` 구성 파일에 배치해야 하며, 애플리케이션에서 필요한 제공자에 따라 `facebook`, `x`, `linkedin-openid`, `google`, `github`, `gitlab`, `bitbucket`, `slack` 또는 `slack-openid` 키를 사용해야 합니다:

```php
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => 'http://example.com/callback-url',
],

```

> [!NOTE]
> `redirect` 옵션에 상대 경로가 포함된 경우, 자동으로 완전한 URL로 변환됩니다.

<a name="authentication"></a>
## 인증

<a name="routing"></a>
### 라우팅

OAuth 제공자를 사용하여 사용자를 인증하려면 두 개의 라우트가 필요합니다: 하나는 사용자를 OAuth 제공자로 리디렉션하는 용도이고, 다른 하나는 인증 후 제공자로부터 콜백을 받는 용도입니다. 아래 예제 라우트는 두 라우트 모두의 구현을 보여줍니다:

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/redirect', function () {
    return Socialite::driver('github')->redirect();
});

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // $user->token
});

```



`Socialite` 퍼사드가 제공하는 `redirect` 메서드는 사용자를 OAuth 제공자에게 리디렉션하는 작업을 처리하며, `user` 메서드는 들어오는 요청을 검사하고 인증 요청이 승인된 후 제공자로부터 사용자의 정보를 가져옵니다.

<a name="authentication-and-storage"></a>
### 인증 및 저장

OAuth 제공자에서 사용자를 가져온 후, 애플리케이션 데이터베이스에서 사용자가 존재하는지 확인하고 [사용자를 인증](/docs/{{version}}/authentication#authenticate-a-user-instance)할 수 있습니다. 사용자가 애플리케이션 데이터베이스에 존재하지 않는 경우, 일반적으로 사용자를 나타내기 위해 데이터베이스에 새 레코드를 생성합니다.

```php
use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $githubUser = Socialite::driver('github')->user();

    $user = User::updateOrCreate([
        'github_id' => $githubUser->id,
    ], [
        'name' => $githubUser->name,
        'email' => $githubUser->email,
        'github_token' => $githubUser->token,
        'github_refresh_token' => $githubUser->refreshToken,
    ]);

    Auth::login($user);

    return redirect('/dashboard');
});

```

> [!NOTE]
> 특정 OAuth 제공업체에서 어떤 사용자 정보를 사용할 수 있는지에 대한 자세한 내용은 [사용자 정보 가져오기](#retrieving-user-details) 문서를 참조하십시오.

<a name="access-scopes"></a>
### 액세스 범위

사용자를 리디렉션하기 전에 `scopes` 메서드를 사용하여 인증 요청에 포함되어야 하는 "범위"를 지정할 수 있습니다. 이 메서드는 이전에 지정된 모든 범위와 사용자가 지정한 범위를 병합합니다:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('github')
    ->scopes(['read:user', 'public_repo'])
    ->redirect();

```



`setScopes` 메서드를 사용하여 인증 요청에서 모든 기존 범위를 덮어쓸 수 있습니다:

```php
return Socialite::driver('github')
    ->setScopes(['read:user', 'public_repo'])
    ->redirect();

```

<a name="slack-bot-scopes"></a>
### Slack 봇 권한 범위

Slack의 API는 [다양한 유형의 액세스 토큰](https://api.slack.com/authentication/token-types)을 제공하며, 각 토큰은 [권한 범위](https://api.slack.com/scopes)가 다릅니다. Socialite는 다음 두 가지 Slack 액세스 토큰 유형과 호환됩니다:

<div class="content-list" markdown="1">

- 봇 (접두사 `xoxb-` 사용)
- 사용자 (접두사 `xoxp-` 사용)

</div>

기본적으로, `slack` 드라이버는 `user` 토큰을 생성하며 드라이버의 `user` 메서드를 호출하면 사용자의 세부 정보를 반환합니다.

봇 토큰은 주로 애플리케이션의 사용자가 소유한 외부 Slack 작업 공간에 알림을 보낼 경우 유용합니다. 봇 토큰을 생성하려면 사용자를 Slack 인증 페이지로 리디렉션하기 전에 `asBotUser` 메서드를 호출하세요:

```php
return Socialite::driver('slack')
    ->asBotUser()
    ->setScopes(['chat:write', 'chat:write.public', 'chat:write.customize'])
    ->redirect();

```

또한, 사용자가 인증 후 Slack이 귀하의 애플리케이션으로 다시 리디렉션한 후 `user` 메서드를 호출하기 전에 `asBotUser` 메서드를 호출해야 합니다:

```php
$user = Socialite::driver('slack')->asBotUser()->user();

```

봇 토큰을 생성할 때, `user` 메서드는 여전히 `Laravel\Socialite\Two\User` 인스턴스를 반환하지만, `token` 속성만 초기화됩니다. 이 토큰은 [인증된 사용자의 Slack 작업 공간에 알림을 보내는 데](/docs/{{version}}/notifications#notifying-external-slack-workspaces) 저장할 수 있습니다.

<a name="optional-parameters"></a>
### 선택적 매개변수

많은 OAuth 제공자는 리디렉션 요청에서 다른 선택적 매개변수를 지원합니다. 요청에 선택적 매개변수를 포함하려면, 연관 배열과 함께 `with` 메서드를 호출하십시오:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')
    ->with(['hd' => 'example.com'])
    ->redirect();

```

> [!WARNING]
> `with` 방법을 사용할 때, `state` 또는 `response_type`와 같은 예약어를 전달하지 않도록 주의하세요.

<a name="retrieving-user-details"></a>
## 사용자 세부 정보 가져오기

사용자가 애플리케이션의 인증 콜백 경로로 리디렉션된 후, Socialite의 `user` 메서드를 사용하여 사용자의 세부 정보를 가져올 수 있습니다. `user` 메서드가 반환하는 사용자 객체는 사용자의 정보를 자체 데이터베이스에 저장하는 데 사용할 수 있는 다양한 속성과 메서드를 제공합니다.

OAuth 공급자가 OAuth 1.0을 지원하는지 또는 OAuth 2.0을 지원하는지에 따라 이 객체에서 사용할 수 있는 속성과 메서드는 다를 수 있습니다.

```php
use Laravel\Socialite\Socialite;

Route::get('/auth/callback', function () {
    $user = Socialite::driver('github')->user();

    // OAuth 2.0 providers...
    $token = $user->token;
    $refreshToken = $user->refreshToken;
    $expiresIn = $user->expiresIn;

    // OAuth 1.0 providers...
    $token = $user->token;
    $tokenSecret = $user->tokenSecret;

    // All providers...
    $user->getId();
    $user->getNickname();
    $user->getName();
    $user->getEmail();
    $user->getAvatar();
});

```

<a name="retrieving-user-details-from-a-token-oauth2"></a>
#### 토큰에서 사용자 세부 정보 가져오기

사용자에 대한 유효한 액세스 토큰이 이미 있는 경우, Socialite의 `userFromToken` 메서드를 사용하여 해당 사용자의 세부 정보를 가져올 수 있습니다:

```php
use Laravel\Socialite\Socialite;

$user = Socialite::driver('github')->userFromToken($token);

```

iOS 애플리케이션을 통해 Facebook 제한 로그인(Facebook Limited Login)을 사용하는 경우, Facebook은 액세스 토큰 대신 OIDC 토큰을 반환합니다. OIDC 토큰에서 사용자 정보를 가져오려면 로그인 시작 시 사용한 nonce를 `userFromToken` 메서드에 제공하십시오:

```php
$user = Socialite::driver('facebook')->userFromToken($token, $nonce);

```

<a name="stateless-authentication"></a>
#### 상태 없는 인증

`stateless` 방법은 세션 상태 검증을 비활성화하는 데 사용될 수 있습니다. 이것은 쿠키 기반 세션을 사용하지 않는 상태 없는 API에 소셜 인증을 추가할 때 유용합니다:

```php
use Laravel\Socialite\Socialite;

return Socialite::driver('google')->stateless()->user();

```

<a name="testing"></a>
## 테스트

Laravel Socialite는 실제 OAuth 제공자에게 요청을 보내지 않고도 OAuth 인증 흐름을 테스트할 수 있는 편리한 방법을 제공합니다. `fake` 메서드는 OAuth 제공자의 동작을 모의(mock)하고 반환되어야 하는 사용자 데이터를 정의할 수 있게 해줍니다.

<a name="faking-the-redirect"></a>
#### 리디렉션 가짜 처리

애플리케이션이 사용자를 OAuth 제공자로 올바르게 리디렉션하는지를 테스트하려면, 리디렉션 경로에 요청을 보내기 전에 `fake` 메서드를 호출할 수 있습니다. 이 메서드는 Socialite가 실제 OAuth 제공자로 리디렉션하는 대신 가짜 인증 URL로 리디렉션을 반환하게 합니다:

```php
use Laravel\Socialite\Socialite;

test('user is redirected to github', function () {
    Socialite::fake('github');

    $response = $this->get('/auth/github/redirect');

    $response->assertRedirect();
});

```

<a name="faking-the-callback"></a>
#### 콜백 위조

애플리케이션의 콜백 경로를 테스트하기 위해 `fake` 메서드를 호출하고, 애플리케이션이 공급자로부터 사용자의 세부 정보를 요청할 때 반환되어야 하는 `User` 인스턴스를 제공할 수 있습니다. `User` 인스턴스는 `fake` 메서드를 사용하여 생성할 수 있습니다:

```php
use Laravel\Socialite\Socialite;
use Laravel\Socialite\Two\User;

test('user can login with github', function () {
    Socialite::fake('github', User::fake([
        'id' => 'github-123',
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
    ]));

    $response = $this->get('/auth/github/callback');

    $response->assertRedirect('/dashboard');

    $this->assertDatabaseHas('users', [
        'name' => 'Jason Beggs',
        'email' => 'jason@example.com',
        'github_id' => 'github-123',
    ]);
});

```

기본적으로 `User` 인스턴스에는 가짜 OAuth 토큰 값이 포함됩니다. 필요하다면 `fake` 메서드에 추가 속성을 전달하여 이러한 값을 재정의할 수 있습니다:

```php
$fakeUser = User::fake([
    'id' => 'github-123',
    'name' => 'Jason Beggs',
    'email' => 'jason@example.com',
    'token' => 'fake-token',
    'refreshToken' => 'fake-refresh-token',
    'expiresIn' => 3600,
    'approvedScopes' => ['read', 'write'],
]);

```

OAuth 1 사용자는 `Laravel\Socialite\One\User` 클래스를 사용하여 가짜로 만들 수 있습니다.
{% endraw %}
