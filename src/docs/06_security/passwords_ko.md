---
layout: docs
title: "비밀번호 재설정"
---

{% raw %}
# 비밀번호 재설정

- [소개](#introduction)
- [컨피그레이션](#configuration)
- [드라이버 사전 요구 사항](#driver-prerequisites)
- [모델 준비](#model-preparation)
- [신뢰할 수 있는 호스트 구성](#configuring-trusted-hosts)
- [라우팅](#routing)
- [비밀번호 재설정 링크 요청](#requesting-the-password-reset-link)
- [비밀번호 재설정](#resetting-the-password)
- [만료 토큰 삭제](#deleting-expired-tokens)
- 커스터마이즈 (#password-customization)

<a name="introduction"></a>
## 소개

대부분의 웹 애플리케이션은 사용자가 잊어버린 비밀번호를 재설정할 수 있는 방법을 제공합니다. Laravel 은 생성하는 모든 애플리케이션에 대해 이를 수동으로 다시 구현하도록 강제하는 대신， 비밀번호 재설정 링크를 보내고 비밀번호를 안전하게 재설정하는 편리한 서비스를 제공합니다。

> [!NOTE]
> 빠르게 시작하고 싶으신가요？ 새로운 Laravel 애플리케이션에 Laravel [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 를 설치하세요. Laravel 의 스타터 키트는 잊어버린 비밀번호 재설정을 포함하여 전체 인증 시스템의 구축을 처리합니다。

<a name="configuration"></a>
### 구성

애플리케이션의 비밀번호 재설정 구성 파일은 `config/auth.php` 에 저장됩니다. 이 파일에서 사용할 수 있는 옵션을 반드시 검토하십시오. 기본적으로 Laravel 은 `database` 비밀번호 재설정 드라이버를 사용하도록 구성됩니다。

비밀번호 재설정 `driver` 구성 옵션은 비밀번호 재설정 데이터가 저장될 위치를 정의합니다. Laravel 에는 다음 두 가지 드라이버가 포함되어 있습니다：

<div class="content-list" markdown="1">

- `database` - 암호 재설정 데이터가 관계형 데이터베이스에 저장됩니다。
- `cache` - 암호 재설정 데이터는 캐시 기반 저장소 중 하나에 저장됩니다。

</div>

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="database"></a>
#### 데이터베이스

기본 `database` 드라이버를 사용할 때는 애플리케이션의 암호 재설정 토큰을 저장하기 위해 테이블을 생성해야 합니다. 일반적으로 이는 Laravel 의 기본 `0001_01_01_000000_create_users_table.php` 데이터베이스 마이그레이션에 포함되어 있습니다。

<a name="cache"></a>
#### 캐시

전용 데이터베이스 테이블이 필요하지 않은 암호 재설정 처리를 위해 사용할 수 있는 캐시 드라이버도 있습니다. 항목은 사용자의 이메일 주소로 키화되므로， 애플리케이션의 다른 곳에서 이메일 주소를 캐시 키로 사용하지 않도록 하십시오：

```php
'passwords' => [
    'users' => [
        'driver' => 'cache',
        'provider' => 'users',
        'store' => 'passwords', // Optional...
        'expire' => 60,
        'throttle' => 60,
    ],
],

```

`artisan cache:clear` 에 대한 호출로 암호 재설정 데이터가 플래시되지 않도록 하려면 `store` 구성 키로 별도의 캐시 저장소를 선택적으로 지정할 수 있습니다. 이 값은 `config/cache.php` 구성 값에 구성된 저장소와 일치해야 합니다。

<a name="model-preparation"></a>
### 모델 준비

Laravel 의 비밀번호 재설정 기능을 사용하기 전에 애플리케이션의 `App\Models\User` 모델에서 `Illuminate\Notifications\Notifiable` 특성을 사용해야 합니다. 일반적으로 이 특성은 새 Laravel 애플리케이션으로 생성되는 기본 `App\Models\User` 모델에 이미 포함되어 있습니다。

다음으로， `App\Models\User` 모델이 `Illuminate\Contracts\Auth\CanResetPassword` 계약을 구현하는지 확인합니다. 프레임워크에 포함된 `App\Models\User` 모델은 이미 이 인터페이스를 구현하며， `Illuminate\Auth\Passwords\CanResetPassword` 특성을 사용하여 인터페이스를 구현하는 데 필요한 메서드를 포함합니다。

<a name="configuring-trusted-hosts"></a>
### 신뢰할 수 있는 호스트 구성

기본적으로 Laravel 은 HTTP 요청의 `Host` 헤더 내용과 관계없이 수신하는 모든 요청에 응답합니다. 또한 `Host` 헤더의 값은 웹 요청 중에 애플리케이션에 대한 절대 URL 을 생성할 때 사용됩니다。

일반적으로 Nginx 또는 Apache 와 같은 웹 서버는 주어진 호스트 이름과 일치하는 요청만 애플리케이션에 전송하도록 구성해야 합니다. 그러나 웹 서버를 직접 사용자 지정할 수 없고 Laravel 에게 특정 호스트 이름에만 응답하도록 지시해야 하는 경우， 애플리케이션의 `bootstrap/app.php` 파일에서 `trustHosts` 미들웨어 방법을 사용하여 이를 수행할 수 있습니다. 이는 애플리케이션에서 암호 재설정 기능을 제공할 때 특히 중요합니다。

이 미들웨어 방법에 대해 자세히 알아보려면 [TrustHosts 미들웨어 문서](/docs/{{version}}/requests#configuring-trusted-hosts) 를 참조하세요。

<a name="routing"></a>
## 라우팅

사용자가 비밀번호를 재설정할 수 있도록 지원을 적절히 구현하려면 여러 경로를 정의해야 합니다. 첫째， 사용자가 이메일 주소를 통해 비밀번호 재설정 링크를 요청할 수 있도록 하는 경로 쌍이 필요합니다. 둘째， 사용자가 이메일로 전송된 비밀번호 재설정 링克을 방문하고 비밀번호 재설정 양식을 완료한 후 실제로 비밀번호 재설정을 처리하는 경로 쌍이 필요할 것입니다。

<a name="requesting-the-password-reset-link"></a>
### 비밀번호 재설정 링크 요청



<a name="the-password-reset-link-request-form"></a>
#### 비밀번호 재설정 링크 요청 폼

먼저, 비밀번호 재설정 링크를 요청하는 데 필요한 라우트를 정의하겠습니다. 시작하려면, 비밀번호 재설정 링크 요청 폼이 포함된 뷰를 반환하는 라우트를 정의하겠습니다:

```php
Route::get('/forgot-password', function () {
    return view('auth.forgot-password');
})->middleware('guest')->name('password.request');

```

이 경로에서 반환되는 뷰에는 `email` 필드를 포함하는 폼이 있어야 하며, 사용자가 특정 이메일 주소에 대한 비밀번호 재설정 링크를 요청할 수 있도록 합니다.

<a name="password-reset-link-handling-the-form-submission"></a>
#### 폼 제출 처리

다음으로, '비밀번호를 잊으셨나요' 뷰에서 폼 제출 요청을 처리하는 경로를 정의합니다. 이 경로는 이메일 주소를 검증하고 해당 사용자에게 비밀번호 재설정 요청을 보내는 역할을 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Password;

Route::post('/forgot-password', function (Request $request) {
    $request->validate(['email' => 'required|email']);

    $status = Password::sendResetLink(
        $request->only('email')
    );

    return $status === Password::ResetLinkSent
        ? back()->with(['status' => __($status)])
        : back()->withErrors(['email' => __($status)]);
})->middleware('guest')->name('password.email');

```

계속하기 전에 이 경로를 더 자세히 살펴보겠습니다. 먼저 요청의 `email` 속성이 검증됩니다. 다음으로 Laravel 의 내장된 “비밀번호 브로커”(`Password` 정면을 통해) 를 사용하여 비밀번호 재설정 링크를 사용자에게 전송합니다. 비밀번호 브로커는 주어진 필드 (이 경우 이메일 주소) 를 통해 사용자를 검색하고 Laravel 의 내장 [알림 시스템](/docs/{{version}}/notifications) 을 통해 비밀번호 재설정 링克을 사용자에게 전송할 것입니다。

`sendResetLink` 메서드는 “상태” 슬러그를 반환합니다. 이 상태는 Laravel 의 [localization](/docs/{{version}}/localization) 도우미를 사용하여 변환될 수 있으며， 요청의 상태에 대한 사용자 친화적인 메시지를 사용자에게 표시합니다. 비밀번호 재설정 상태의 변환은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 의해 결정됩니다. 상태 슬러그의 가능한 각 값에 대한 항목은 `passwords` 언어 파일 내에 위치합니다。

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel 의 언어 파일을 사용자 지정하려면 `lang:publish` Artisan 명령을 통해 게시할 수 있습니다。

`Password` 패싯의 `sendResetLink` 메서드를 호출할 때 Laravel 이 애플리케이션의 데이터베이스에서 사용자 레코드를 검색하는 방법을 어떻게 알고 있는지 궁금할 수 있습니다. Laravel 암호 브로커는 인증 시스템의 “사용자 제공자” 를 사용하여 데이터베이스 레코드를 검색합니다. 암호 브로커에서 사용하는 사용자 제공자는 `config/auth.php` 구성 파일의 `passwords` 구성 배열 내에서 구성됩니다. 사용자 지정 사용자 제공자 작성에 대한 자세한 내용은 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers) 를 참조하십시오。

> [!NOTE]
> 비밀번호 재설정을 수동으로 구현할 때는 뷰와 경로의 내용을 직접 정의해야 합니다. 필요한 모든 인증 및 확인 로직이 포함된 스캐폴딩을 원한다면 [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 를 확인하세요。

<a name="resetting-the-password"></a>
### 비밀번호 재설정

<a name="the-password-reset-form"></a>
#### 비밀번호 재설정 양식



다음으로, 사용자가 이메일로 전송된 비밀번호 재설정 링크를 클릭하고 새 비밀번호를 제공하면 실제로 비밀번호를 재설정하는 데 필요한 라우트를 정의할 것입니다. 먼저, 사용자가 비밀번호 재설정 링크를 클릭할 때 표시되는 비밀번호 재설정 폼을 표시하는 라우트를 정의해 보겠습니다. 이 라우트는 나중에 비밀번호 재설정 요청을 확인하는 데 사용할 `token` 매개변수를 받습니다:

```php
Route::get('/reset-password/{token}', function (string $token) {
    return view('auth.reset-password', ['token' => $token]);
})->middleware('guest')->name('password.reset');

```

이 경로에서 반환되는 뷰는 `email` 필드, `password` 필드, `password_confirmation` 필드와 숨겨진 `token` 필드를 포함한 폼을 표시해야 하며, 이 숨겨진 필드에는 우리 경로에서 받은 비밀 `$token`의 값이 포함되어야 합니다.

<a name="password-reset-handling-the-form-submission"></a>
#### 폼 제출 처리

물론, 실제로 비밀번호 재설정 폼 제출을 처리할 경로를 정의해야 합니다. 이 경로는 들어오는 요청을 검증하고 사용자의 비밀번호를 데이터베이스에서 업데이트하는 역할을 합니다:

```php
use App\Models\User;
use Illuminate\Auth\Events\PasswordReset;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;

Route::post('/reset-password', function (Request $request) {
    $request->validate([
        'token' => 'required',
        'email' => 'required|email',
        'password' => 'required|min:8|confirmed',
    ]);

    $status = Password::reset(
        $request->only('email', 'password', 'password_confirmation', 'token'),
        function (User $user, string $password) {
            $user->forceFill([
                'password' => Hash::make($password)
            ])->setRememberToken(Str::random(60));

            $user->save();

            event(new PasswordReset($user));
        }
    );

    return $status === Password::PasswordReset
        ? redirect()->route('login')->with('status', __($status))
        : back()->withErrors(['email' => [__($status)]]);
})->middleware('guest')->name('password.update');

```

계속하기 전에 이 경로를 더 자세히 살펴보겠습니다. 먼저 요청의 `token`, `email` 및 `password` 속성이 검증됩니다. 다음으로 Laravel 의 내장된 “비밀번호 브로커”(`Password` 패싯을 통해) 를 사용하여 비밀번호 재설정 요청 자격 증명을 검증합니다。

비밀번호 브로커에 제공된 토큰， 이메일 주소 및 비밀번호가 유효한 경우 `reset` 메서드에 전달된 종료가 호출됩니다. 이 종료 내에서 비밀번호 재설정 양식에 제공된 사용자 인스턴스 및 일반 텍스트 비밀번호를 수신하며， 데이터베이스에서 사용자 비밀번호를 업데이트할 수 있습니다。

`reset` 메서드는 “상태” 슬러그를 반환합니다. 이 상태는 Laravel 의 [localization](/docs/{{version}}/localization) 헬퍼를 사용하여 변환될 수 있으며， 요청의 상태에 대한 사용자 친화적인 메시지를 사용자에게 표시합니다. 비밀번호 재설정 상태의 변환은 애플리케이션의 `lang/{lang}/passwords.php` 언어 파일에 의해 결정됩니다. 상태 슬러그의 각 가능한 값에 대한 항목은 `passwords` 언어 파일 내에 위치합니다. 애플리케이션에 `lang` 디렉토리가 포함되어 있지 않은 경우 `lang:publish` Artisan 명령을 사용하여 디렉토리를 생성할 수 있습니다。

계속하기 전에， `Password` 패싯의 `reset` 메서드를 호출할 때 Laravel 이 애플리케이션의 데이터베이스에서 사용자 레코드를 검색하는 방법을 어떻게 알고 있는지 궁금할 수 있습니다. Laravel 암호 브로커는 인증 시스템의 “사용자 제공자” 를 사용하여 데이터베이스 레코드를 검색합니다. 암호 브로커에서 사용하는 사용자 제공자는 `config/auth.php` 구성 파일의 `passwords` 구성 배열 내에서 구성됩니다. 사용자 지정 사용자 제공자 작성에 대한 자세한 내용은 [인증 문서](/docs/{{version}}/authentication#adding-custom-user-providers) 를 참조하십시오。

<a name="deleting-expired-tokens"></a>
## 만료된 토큰 삭제

`database` 드라이버를 사용하는 경우， 만료된 비밀번호 재설정 토큰은 여전히 데이터베이스에 존재합니다. 그러나 `auth:clear-resets` Artisan 명령을 사용하여 이러한 레코드를 쉽게 삭제할 수 있습니다：

```shell
php artisan auth:clear-resets

```

이 프로세스를 자동화하고 싶다면, 애플리케이션의 [스케줄러](/docs/{{version}}/scheduling)에 명령을 추가하는 것을 고려하세요:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('auth:clear-resets')->everyFifteenMinutes();

```

<a name="password-customization"></a>
## 사용자 정의

<a name="reset-link-customization"></a>
#### 비밀번호 재설정 링크 사용자 정의

`ResetPassword` 알림 클래스에서 제공하는 `createUrlUsing` 메서드를 사용하여 비밀번호 재설정 링크 URL을 사용자 정의할 수 있습니다. 이 메서드는 알림을 받는 사용자 인스턴스와 비밀번호 재설정 링크 토큰을 받는 클로저를 허용합니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출해야 합니다:

```php
use App\Models\User;
use Illuminate\Auth\Notifications\ResetPassword;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    ResetPassword::createUrlUsing(function (User $user, string $token) {
        return 'https://example.com/reset-password?token='.$token;
    });
}

```

<a name="reset-email-customization"></a>
#### 이메일 사용자 지정 재설정

사용자에게 비밀번호 재설정 링크를 보내는 데 사용되는 알림 클래스를 쉽게 수정할 수 있습니다. 시작하려면 `App\Models\User` 모델에서 `sendPasswordResetNotification` 메서드를 재정의하세요. 이 메서드 내에서 본인이 만든 [알림 클래스](/docs/{{version}}/notifications)를 사용하여 알림을 보낼 수 있습니다. 비밀번호 재설정 `$token`는 메서드가 받는 첫 번째 인수입니다. 이 `$token`를 사용하여 원하는 비밀번호 재설정 URL을 만들고 사용자에게 알림을 보낼 수 있습니다.

```php
use App\Notifications\ResetPasswordNotification;

/**
 * Send a password reset notification to the user.
 *
 * @param  string  $token
 */
public function sendPasswordResetNotification($token): void
{
    $url = 'https://example.com/reset-password?token='.$token;

    $this->notify(new ResetPasswordNotification($url));
}

```
{% endraw %}
