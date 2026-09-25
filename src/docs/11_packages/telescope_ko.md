---
layout: docs
title: "라라벨 망원경"
---

{% raw %}
# 라라벨 망원경

- [소개](#introduction)
- [설치](#installation)
- 로컬 오직 설치 (#local-only-installation)
- [구성](#configuration)
- 데이터 가지치기 (#data-pruning)
- 대시보드 권한 부여 (#dashboard-authorization)
- 업그레이드 망원경 (#upgrading-telescope)
- 필터링 (#filtering)
- 엔트리 (#filtering-entries)
- 배치 (#filtering-batches)
- [태깅](#tagging)
- [사용 가능한 관찰자](#available-watchers)
- [배치 관찰자](#batch-watcher)
- 캐시 워처 (#cache-watcher)
- Command Watcher (#command-watcher)
- [덤프 워처](#dump-watcher)
- 이벤트 워처 (#event-watcher)
- [예외 관찰자](#exception-watcher)
- 게이트 워처 (#gate-watcher)
- [HTTP Client Watcher](#http-client-watcher)
- [Job Watcher](#job-watcher)
- [Log Watcher](#log-watcher)
- [메일 감시자](#mail-watcher)
- [모델 워처](#model-watcher)
- [알림 감시자](#notification-watcher)
- 쿼리 워처 (#query-watcher)
- 레디스 워처 (#redis-watcher)
- [Request Watcher](#request-watcher)
- [스케줄 워처](#schedule-watcher)
- 뷰 워처 (#view-watcher)
- [디스플레이 유저 아바타](#displaying-user-avatars)

<a name="introduction"></a>
## 소개

[Laravel Telescope](https://github.com/laravel/telescope) 는 로컬 Laravel 개발 환경의 훌륭한 동반자입니다. Telescope 는 애플리케이션에 수신되는 요청， 예외， 로그 항목， 데이터베이스 쿼리， 대기열 작업， 메일， 알림， 캐시 작업， 예약된 작업， 변수 덤프 등에 대한 인사이트를 제공합니다。

<img src="https://laravel.com/img/docs/telescope-example.png">

<a name="installation"></a>
## 설치

Composer 패키지 관리자를 사용하여 Laravel 프로젝트에 Telescope 를 설치할 수 있습니다：

```shell
composer require laravel/telescope

```

Telescope를 설치한 후 `telescope:install` Artisan 명령어를 사용하여 해당 자산과 마이그레이션을 게시하십시오. Telescope를 설치한 후에는 Telescope의 데이터를 저장하는 데 필요한 테이블을 생성하기 위해 `migrate` 명령어도 실행해야 합니다:

```shell
php artisan telescope:install

php artisan migrate

```

마지막으로, `/telescope` 경로를 통해 Telescope 대시보드에 접근할 수 있습니다.

<a name="local-only-installation"></a>
### 로컬 전용 설치

만약 Telescope를 로컬 개발 지원에만 사용하려는 경우, `--dev` 플래그를 사용하여 Telescope를 설치할 수 있습니다:

```shell
composer require laravel/telescope --dev

php artisan telescope:install

php artisan migrate

```



`telescope:install`를 실행한 후에는 애플리케이션의 `bootstrap/providers.php` 구성 파일에서 `TelescopeServiceProvider` 서비스 제공자 등록을 제거해야 합니다. 대신, `App\Providers\AppServiceProvider` 클래스의 `register` 메서드에서 Telescope의 서비스 제공자를 수동으로 등록하십시오. 서비스 제공자를 등록하기 전에 현재 환경이 `local`인지 확인하겠습니다:

```php
/**
 * Register any application services.
 */
public function register(): void
{
    if ($this->app->environment('local') && class_exists(\Laravel\Telescope\TelescopeServiceProvider::class)) {
        $this->app->register(\Laravel\Telescope\TelescopeServiceProvider::class);
        $this->app->register(TelescopeServiceProvider::class);
    }
}

```

마지막으로, 다음을 `composer.json` 파일에 추가하여 Telescope 패키지가 [자동 발견](/docs/{{version}}/packages#package-discovery)되지 않도록 해야 합니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "laravel/telescope"
        ]
    }
},

```

<a name="configuration"></a>
### 구성

Telescope의 자산을 게시한 후, 주요 구성 파일은 `config/telescope.php`에 위치하게 됩니다. 이 구성 파일을 통해 [감시자 옵션](#available-watchers)을 설정할 수 있습니다. 각 구성 옵션에는 목적에 대한 설명이 포함되어 있으므로, 반드시 이 파일을 철저히 살펴보세요.

원한다면 `enabled` 구성 옵션을 사용하여 Telescope의 데이터 수집을 완전히 비활성화할 수 있습니다:

```php
'enabled' => env('TELESCOPE_ENABLED', true),

```

<a name="content-security-policy-csp-nonce"></a>
#### 콘텐츠 보안 정책(CSP) 난스

Telescope 뷰에서 사용되는 스크립트 및 스타일 태그에 [난스 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/nonce)을 [콘텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일부로 사용하고 싶다면, 사용할 난스를 지정하기 위해 `Telescope::cspNonce` 메서드를 사용할 수 있습니다. 이 메서드는 일반적으로 각 요청마다 새 난스가 할당되도록 미들웨어 내에서 호출해야 합니다:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Telescope\Telescope;
use Symfony\Component\HttpFoundation\Response;

public function handle(Request $request, Closure $next): Response
{
    Telescope::cspNonce('csp-nonce');

    return $next($request);
}

```

이 미들웨어를 애플리케이션의 `config/telescope.php` 설정 파일에 있는 `middleware` 옵션에 추가할 수 있습니다:

```php
'middleware' => [
    'web',
    App\Http\Middleware\AddTelescopeCspNonce::class,
    Authorize::class,
],

```

<a name="data-pruning"></a>
### 데이터 정리

데이터 정리가 없으면 `telescope_entries` 테이블은 매우 빠르게 레코드를 쌓을 수 있습니다. 이를 완화하기 위해 `telescope:prune` Artisan 명령을 매일 실행하도록 [일정](/docs/{{version}}/scheduling)을 잡아야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune')->daily();

```

기본적으로, 24시간 이상 된 모든 항목은 삭제됩니다. 명령을 호출할 때 `hours` 옵션을 사용하여 Telescope 데이터를 얼마나 오래 유지할지 결정할 수 있습니다. 예를 들어, 다음 명령은 48시간 이상 전에 생성된 모든 기록을 삭제합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('telescope:prune --hours=48')->daily();

```

<a name="dashboard-authorization"></a>
### 대시보드 권한

Telescope 대시보드는 `/telescope` 경로를 통해 접근할 수 있습니다. 기본적으로, 이 대시보드에는 `local` 환경에서만 접근할 수 있습니다. `app/Providers/TelescopeServiceProvider.php` 파일 안에는 [권한 게이트](/docs/{{version}}/authorization#gates) 정의가 있습니다. 이 권한 게이트는 **비-로컬** 환경에서 Telescope 접근을 제어합니다. 필요에 따라 이 게이트를 수정하여 Telescope 설치에 대한 접근을 제한할 수 있습니다:

```php
use App\Models\User;

/**
 * Register the Telescope gate.
 *
 * This gate determines who can access Telescope in non-local environments.
 */
protected function gate(): void
{
    Gate::define('viewTelescope', function (User $user) {
        return in_array($user->email, [
            'taylor@laravel.com',
        ]);
    });
}

```

> [!WARNING]
> 운영 환경에서 `APP_ENV` 환경 변수를 `production`로 변경했는지 확인해야 합니다. 그렇지 않으면 텔레스코프 설치가 공개적으로 노출될 수 있습니다.

<a name="upgrading-telescope"></a>
## 텔레스코프 업그레이드

텔레스코프의 새로운 메이저 버전으로 업그레이드할 때는 [업그레이드 가이드](https://github.com/laravel/telescope/blob/master/UPGRADE.md)를 주의 깊게 검토하는 것이 중요합니다.

또한, 텔레스코프의 모든 새 버전으로 업그레이드할 때는 텔레스코프의 자산을 다시 게시해야 합니다:

```shell
php artisan telescope:publish

```

자산을 최신 상태로 유지하고 향후 업데이트에서 문제를 피하기 위해, 애플리케이션의 `composer.json` 파일에 있는 `post-update-cmd` 스크립트에 `vendor:publish --tag=laravel-assets` 명령을 추가할 수 있습니다:

```json
{
    "scripts": {
        "post-update-cmd": [
            "@php artisan vendor:publish --tag=laravel-assets --ansi --force"
        ]
    }
}

```

<a name="filtering"></a>
## 필터링

<a name="filtering-entries"></a>
### 항목

Telescope에 의해 기록된 데이터를 `App\Providers\TelescopeServiceProvider` 클래스에서 정의된 `filter` 클로저를 통해 필터링할 수 있습니다. 기본적으로 이 클로저는 `local` 환경의 모든 데이터와 예외, 실패한 작업, 예약된 작업, 모니터링된 태그가 있는 다른 모든 환경의 데이터를 기록합니다:

```php
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filter(function (IncomingEntry $entry) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entry->isReportableException() ||
            $entry->isFailedJob() ||
            $entry->isScheduledTask() ||
            $entry->isSlowQuery() ||
            $entry->hasMonitoredTag();
    });
}

```

<a name="filtering-batches"></a>
### 배치

`filter` 클로저가 개별 항목의 데이터를 필터링하는 동안, `filterBatch` 메서드를 사용하여 특정 요청이나 콘솔 명령에 대한 모든 데이터를 필터링하는 클로저를 등록할 수 있습니다. 클로저가 `true`를 반환하면 모든 항목이 Telescope에 기록됩니다:

```php
use Illuminate\Support\Collection;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::filterBatch(function (Collection $entries) {
        if ($this->app->environment('local')) {
            return true;
        }

        return $entries->contains(function (IncomingEntry $entry) {
            return $entry->isReportableException() ||
                $entry->isFailedJob() ||
                $entry->isScheduledTask() ||
                $entry->isSlowQuery() ||
                $entry->hasMonitoredTag();
            });
    });
}

```

<a name="tagging"></a>
## 태깅

Telescope를 사용하면 "태그"로 항목을 검색할 수 있습니다. 일반적으로 태그는 Eloquent 모델 클래스 이름이나 Telescope가 항목에 자동으로 추가하는 인증된 사용자 ID입니다. 가끔 항목에 사용자 정의 태그를 추가하고 싶을 수도 있습니다. 이를 수행하려면 `Telescope::tag` 메서드를 사용할 수 있습니다. `tag` 메서드는 태그의 배열을 반환해야 하는 클로저를 인수로 받습니다. 클로저가 반환한 태그는 Telescope가 자동으로 항목에 추가하는 태그와 병합됩니다. 일반적으로 `tag` 메서드는 `App\Providers\TelescopeServiceProvider` 클래스의 `register` 메서드 내에서 호출해야 합니다.

```php
use Laravel\Telescope\EntryType;
use Laravel\Telescope\IncomingEntry;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->hideSensitiveRequestDetails();

    Telescope::tag(function (IncomingEntry $entry) {
        return $entry->type === EntryType::REQUEST
            ? ['status:'.$entry->content['response_status']]
            : [];
    });
}

```

<a name="available-watchers"></a>
## 사용 가능한 감시자

텔레스코프 "감시자"는 요청이나 콘솔 명령이 실행될 때 애플리케이션 데이터를 수집합니다. `config/telescope.php` 구성 파일 내에서 활성화할 감시자의 목록을 사용자 정의할 수 있습니다:

```php
'watchers' => [
    Watchers\CacheWatcher::class => true,
    Watchers\CommandWatcher::class => true,
    // ...
],

```

일부 감시자들은 추가 사용자 지정 옵션을 제공할 수 있도록 허용하기도 합니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 100,
    ],
    // ...
],

```

<a name="batch-watcher"></a>
### 배치 감시기

배치 감시기는 작업 및 연결 정보를 포함하여 대기 중인 [배치](/docs/{{version}}/queues#job-batching)에 대한 정보를 기록합니다.

<a name="cache-watcher"></a>
### 캐시 감시기

캐시 감시기는 캐시 키가 적중, 누락, 업데이트되거나 잊혀질 때 데이터를 기록합니다.

<a name="command-watcher"></a>
### 명령 감시기

명령 감시기는 Artisan 명령이 실행될 때마다 인수, 옵션, 종료 코드 및 출력을 기록합니다. 특정 명령이 감시기에 의해 기록되지 않도록 하려면 `config/telescope.php` 파일 내의 `ignore` 옵션에 해당 명령을 지정할 수 있습니다:

```php
'watchers' => [
    Watchers\CommandWatcher::class => [
        'enabled' => env('TELESCOPE_COMMAND_WATCHER', true),
        'ignore' => ['key:generate'],
    ],
    // ...
],

```

<a name="dump-watcher"></a>
### 덤프 워처

덤프 관찰자는 변수 덤프를 기록하고 Telescope 에 표시합니다. Laravel 을 사용할 때 글로벌 `dump` 함수를 사용하여 변수를 덤프할 수 있습니다. 덤프를 기록하려면 브라우저에서 덤프 관찰자 탭을 열어야 합니다. 그렇지 않으면 덤프가 관찰자에 의해 무시됩니다。

<a name="event-watcher"></a>
### 이벤트 관찰자

이벤트 모니터는 애플리케이션에서 전송된 모든 [이벤트](/docs/{{version}}/events) 에 대한 페이로드， 리스너 및 브로드캐스트 데이터를 기록합니다. Laravel 프레임워크의 내부 이벤트는 이벤트 모니터에서 무시됩니다。

<a name="exception-watcher"></a>
### 예외 관찰자

예외 관찰자는 애플리케이션에서 생성된 보고 가능한 예외에 대한 데이터와 스택 추적을 기록합니다。

<a name="gate-watcher"></a>
### 게이트 워처

게이트 감시기는 애플리케이션에 의한 [gate and policy](/docs/{{version}}/authorization) 검사의 데이터와 결과를 기록합니다. 감시기에 의한 기록에서 특정 기능을 제외하려는 경우 `config/telescope.php` 파일의 `ignore_abilities` 옵션에서 지정할 수 있습니다：

```php
'watchers' => [
    Watchers\GateWatcher::class => [
        'enabled' => env('TELESCOPE_GATE_WATCHER', true),
        'ignore_abilities' => ['viewNova'],
    ],
    // ...
],

```

<a name="http-client-watcher"></a>
### HTTP 클라이언트 감시기

HTTP 클라이언트 감시기는 애플리케이션에서 이루어지는 [HTTP 클라이언트 요청](/docs/{{version}}/http-client)을 기록합니다.

<a name="job-watcher"></a>
### 작업 감시기

작업 감시기는 애플리케이션에서 실행되는 모든 [작업](/docs/{{version}}/queues)의 데이터와 상태를 기록합니다.

<a name="log-watcher"></a>
### 로그 감시기

로그 감시기는 애플리케이션에서 작성된 모든 로그에 대한 [로그 데이터](/docs/{{version}}/logging)를 기록합니다.

기본적으로, Telescope는 `error` 수준 이상의 로그만 기록합니다. 그러나 애플리케이션의 `config/telescope.php` 설정 파일에서 `level` 옵션을 수정하여 이 동작을 변경할 수 있습니다:

```php
'watchers' => [
    Watchers\LogWatcher::class => [
        'enabled' => env('TELESCOPE_LOG_WATCHER', true),
        'level' => 'debug',
    ],

    // ...
],

```

<a name="mail-watcher"></a>
### 메일 감시기

메일 감시기를 사용하면 애플리케이션에서 전송된 [이메일](/docs/{{version}}/mail)과 그에 관련된 데이터를 브라우저 내에서 미리 볼 수 있습니다. 또한 이메일을 `.eml` 파일로 다운로드할 수도 있습니다.

<a name="model-watcher"></a>
### 모델 감시기

모델 감시기는 Eloquent [모델 이벤트](/docs/{{version}}/eloquent#events)가 발생할 때마다 모델 변경 사항을 기록합니다. 감시기의 `events` 옵션을 통해 어떤 모델 이벤트를 기록할지 지정할 수 있습니다.

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
    ],
    // ...
],

```

특정 요청 동안 수화된 모델 수를 기록하고 싶다면, `hydrations` 옵션을 활성화하세요:

```php
'watchers' => [
    Watchers\ModelWatcher::class => [
        'enabled' => env('TELESCOPE_MODEL_WATCHER', true),
        'events' => ['eloquent.created*', 'eloquent.updated*'],
        'hydrations' => true,
    ],
    // ...
],

```

<a name="notification-watcher"></a>
### 알림 감시기

알림 감시기는 애플리케이션에서 보내는 모든 [알림](/docs/{{version}}/notifications)을 기록합니다. 알림이 이메일을 트리거하고 메일 감시기가 활성화되어 있다면, 이메일도 메일 감시기 화면에서 미리보기할 수 있습니다.

<a name="query-watcher"></a>
### 쿼리 감시기

쿼리 감시기는 애플리케이션에서 실행되는 모든 쿼리의 원시 SQL, 바인딩, 실행 시간을 기록합니다. 감시기는 100밀리초보다 느린 쿼리를 `slow`로 태그합니다. 감시기의 `slow` 옵션을 사용하여 느린 쿼리 기준을 사용자 정의할 수 있습니다:

```php
'watchers' => [
    Watchers\QueryWatcher::class => [
        'enabled' => env('TELESCOPE_QUERY_WATCHER', true),
        'slow' => 50,
    ],
    // ...
],

```

<a name="redis-watcher"></a>
### Redis 감시자

Redis 감시자는 애플리케이션에서 실행된 모든 [Redis](/docs/{{version}}/redis) 명령을 기록합니다. Redis를 캐싱에 사용하는 경우, 캐시 명령 또한 Redis 감시자에 의해 기록됩니다.

<a name="request-watcher"></a>
### 요청 감시자

요청 감시자는 애플리케이션에서 처리된 모든 요청과 관련된 요청, 헤더, 세션, 응답 데이터를 기록합니다. `size_limit`(킬로바이트 단위) 옵션을 통해 기록되는 응답 데이터를 제한할 수 있습니다:

```php
'watchers' => [
    Watchers\RequestWatcher::class => [
        'enabled' => env('TELESCOPE_REQUEST_WATCHER', true),
        'size_limit' => env('TELESCOPE_RESPONSE_SIZE_LIMIT', 64),
    ],
    // ...
],

```

<a name="schedule-watcher"></a>
### 스케줄 감시기

스케줄 감시기는 애플리케이션에서 실행된 [예약 작업](/docs/{{version}}/scheduling)의 명령과 출력을 기록합니다.

<a name="view-watcher"></a>
### 뷰 감시기

뷰 감시기는 뷰를 렌더링할 때 사용된 [뷰](/docs/{{version}}/views) 이름, 경로, 데이터 및 "composer"를 기록합니다.

<a name="displaying-user-avatars"></a>
## 사용자 아바타 표시

Telescope 대시보드는 특정 항목이 저장될 때 인증된 사용자의 아바타를 표시합니다. 기본적으로 Telescope는 Gravatar 웹 서비스를 통해 아바타를 가져옵니다. 그러나 `App\Providers\TelescopeServiceProvider` 클래스에서 콜백을 등록하여 아바타 URL을 사용자 정의할 수 있습니다. 콜백은 사용자의 ID와 이메일 주소를 받으며, 사용자의 아바타 이미지 URL을 반환해야 합니다:

```php
use App\Models\User;
use Laravel\Telescope\Telescope;

/**
 * Register any application services.
 */
public function register(): void
{
    // ...

    Telescope::avatar(function (?string $id, ?string $email) {
        return ! is_null($id)
            ? '/avatars/'.User::find($id)->avatar_path
            : '/generic-avatar.jpg';
    });
}

```
{% endraw %}
