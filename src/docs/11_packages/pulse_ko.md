---
layout: docs
title: "Laravel Pulse"
---

{% raw %}
---
layout: docs
title: "Laravel Pulse"
---

# Laravel Pulse

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
- [Dashboard](#dashboard)
    - [Authorization](#dashboard-authorization)
    - [Customization](#dashboard-customization)
    - [Resolving Users](#dashboard-resolving-users)
    - [Cards](#dashboard-cards)
- [Capturing Entries](#capturing-entries)
    - [Recorders](#recorders)
    - [Filtering](#filtering)
- [Performance](#performance)
    - [Using a Different Database](#using-a-different-database)
    - [Redis Ingest](#ingest)
    - [Sampling](#sampling)
    - [Trimming](#trimming)
    - [Handling Pulse Exceptions](#pulse-exceptions)
- [Custom Cards](#custom-cards)
    - [Card Components](#custom-card-components)
    - [Styling](#custom-card-styling)
    - [Data Capture and Aggregation](#custom-card-data)

<a name="introduction"></a>
## Introduction

[Laravel Pulse](https://github.com/laravel/pulse) delivers at-a-glance insights into your application's performance and usage. With Pulse, you can track down bottlenecks like slow jobs and endpoints, find your most active users, and more.

For in-depth debugging of individual events, check out [Laravel Telescope](/docs/{{version}}/telescope).

<a name="installation"></a>
## Installation

> [!WARNING]
> Pulse's first-party storage implementation currently requires a MySQL, MariaDB, or PostgreSQL database. If you are using a different database engine, you will need a separate MySQL, MariaDB, or PostgreSQL database for your Pulse data.

You may install Pulse using the Composer package manager:

```shell
composer require laravel/pulse
```



다음으로, `vendor:publish` Artisan 명령을 사용하여 Pulse 구성 및 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pulse\PulseServiceProvider"
```



마지막으로, Pulse의 데이터를 저장하는 데 필요한 테이블을 생성하기 위해 `migrate` 명령을 실행해야 합니다:

```shell
php artisan migrate
```



Pulse의 데이터베이스 마이그레이션이 완료되면 `/pulse` 경로를 통해 Pulse 대시보드에 접근할 수 있습니다.

> [!NOTE]
> Pulse 데이터를 애플리케이션의 기본 데이터베이스에 저장하고 싶지 않은 경우, [전용 데이터베이스 연결을 지정](#using-a-different-database)할 수 있습니다.

<a name="configuration"></a>
### 구성

Pulse의 많은 구성 옵션은 환경 변수를 사용하여 제어할 수 있습니다. 사용 가능한 옵션을 확인하거나, 새로운 레코더를 등록하거나, 고급 옵션을 구성하려면 `config/pulse.php` 구성 파일을 발행할 수 있습니다:

```shell
php artisan vendor:publish --tag=pulse-config
```



<a name="dashboard"></a>
## 대시보드

<a name="dashboard-authorization"></a>
### 권한 부여

Pulse 대시보드는 `/pulse` 경로를 통해 접근할 수 있습니다. 기본적으로, 이 대시보드는 `local` 환경에서만 접근할 수 있으므로, `'viewPulse'` 권한 게이트를 사용자 정의하여 프로덕션 환경에 대한 권한을 구성해야 합니다. 이는 애플리케이션의 `app/Providers/AppServiceProvider.php` 파일 내에서 수행할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('viewPulse', function (User $user) {
        return $user->isAdmin();
    });

    // ...
}
```



<a name="dashboard-customization"></a>
### 맞춤 설정

Pulse 대시보드 카드와 레이아웃은 대시보드 보기를 게시하여 구성할 수 있습니다. 대시보드 보기는 `resources/views/vendor/pulse/dashboard.blade.php`에 게시됩니다:

```shell
php artisan vendor:publish --tag=pulse-dashboard
```



대시보드는 [Livewire](https://livewire.laravel.com/)로 구동되며, JavaScript 자산을 다시 빌드할 필요 없이 카드와 레이아웃을 사용자 정의할 수 있습니다.

이 파일 내에서 `<x-pulse>` 컴포넌트는 대시보드를 렌더링하는 역할을 하며, 카드에 대한 그리드 레이아웃을 제공합니다. 대시보드를 화면 전체 너비로 표시하고 싶다면, 컴포넌트에 `full-width` 속성을 제공할 수 있습니다:

```blade
<x-pulse full-width>
    ...
</x-pulse>
```



기본적으로 `<x-pulse>` 구성 요소는 12열 그리드를 생성하지만, `cols` 속성을 사용하여 이를 사용자 정의할 수 있습니다:

```blade
<x-pulse cols="16">
    ...
</x-pulse>
```



각 카드에서는 공간과 위치를 제어하기 위해 `cols` 및 `rows` 속성을 사용할 수 있습니다:

```blade
<livewire:pulse.usage cols="4" rows="2" />
```



대부분의 카드도 스크롤 대신 전체 카드를 표시하기 위해 `expand` 속성을 허용합니다:

```blade
<livewire:pulse.slow-queries expand />
```



<a name="dashboard-resolving-users"></a>
### 사용자 해결

사용자에 대한 정보를 표시하는 카드(예: 애플리케이션 사용 카드)의 경우, Pulse는 사용자의 ID만 기록합니다. 대시보드를 렌더링할 때, Pulse는 기본 `Authenticatable` 모델에서 `name` 및 `email` 필드를 해결하고 Gravatar 웹 서비스를 사용하여 아바타를 표시합니다.

애플리케이션 `App\Providers\AppServiceProvider` 클래스 내에서 `Pulse::user` 메서드를 호출하여 필드와 아바타를 사용자 정의할 수 있습니다.

`user` 메서드는 표시할 `Authenticatable` 모델을 받는 클로저를 허용하며, 사용자에 대한 `name`, `extra` 및 `avatar` 정보를 포함하는 배열을 반환해야 합니다:

```php
use Laravel\Pulse\Facades\Pulse;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::user(fn ($user) => [
        'name' => $user->name,
        'extra' => $user->email,
        'avatar' => $user->avatar_url,
    ]);

    // ...
}
```



> [!NOTE]
> 인증된 사용자가 캡처되고 검색되는 방식을 완전히 사용자 정의하려면 `Laravel\Pulse\Contracts\ResolvesUsers` 계약을 구현하고 Laravel의 [서비스 컨테이너](/docs/{{version}}/container#binding-a-singleton)에 바인딩하면 됩니다.

<a name="dashboard-cards"></a>
### 카드

<a name="servers-card"></a>
#### 서버

`<livewire:pulse.servers />` 카드는 `pulse:check` 명령을 실행하는 모든 서버의 시스템 리소스 사용량을 표시합니다. 시스템 리소스 보고에 대한 자세한 정보는 [서버 기록기](#servers-recorder) 문서를 참조하십시오.

인프라에서 서버를 교체하는 경우, 일정 기간 이후에는 비활성 서버를 Pulse 대시보드에서 표시하지 않도록 하고 싶을 수 있습니다. 이는 `ignore-after` 속성을 사용하여 수행할 수 있으며, 비활성 서버를 Pulse 대시보드에서 제거할 때까지의 시간을 초 단위로 지정할 수 있습니다. 또는 `1 hour` 또는 `3 days and 1 hour`와 같은 상대 시간 형식 문자열을 제공할 수도 있습니다.

```blade
<livewire:pulse.servers ignore-after="3 hours" />
```



<a name="application-usage-card"></a>
#### 애플리케이션 사용

`<livewire:pulse.usage />` 카드에는 귀하의 애플리케이션에 요청을 보내고 작업을 배치하며 느린 요청을 경험하는 상위 10명의 사용자가 표시됩니다.

모든 사용 지표를 화면에서 동시에 보고 싶다면, 카드를 여러 번 포함하고 `type` 속성을 지정할 수 있습니다:

```blade
<livewire:pulse.usage type="requests" />
<livewire:pulse.usage type="slow_requests" />
<livewire:pulse.usage type="jobs" />
```



To learn how to customize how Pulse retrieves and displays user information, consult our documentation on [resolving users](#dashboard-resolving-users).

> [!NOTE]
> If your application receives a lot of requests or dispatches a lot of jobs, you may wish to enable [sampling](#sampling). See the [user requests recorder](#user-requests-recorder), [user jobs recorder](#user-jobs-recorder), and [slow jobs recorder](#slow-jobs-recorder) documentation for more information.

<a name="exceptions-card"></a>
#### Exceptions

The `<livewire:pulse.exceptions />` card shows the frequency and recency of exceptions occurring in your application. By default, exceptions are grouped based on the exception class and location where it occurred. See the [exceptions recorder](#exceptions-recorder) documentation for more information.

<a name="queues-card"></a>
#### Queues

The `<livewire:pulse.queues />` card shows the throughput of the queues in your application, including the number of jobs queued, processing, processed, released, and failed. See the [queues recorder](#queues-recorder) documentation for more information.

<a name="slow-requests-card"></a>
#### Slow Requests

The `<livewire:pulse.slow-requests />` card shows incoming requests to your application that exceed the configured threshold, which is 1,000ms by default. See the [slow requests recorder](#slow-requests-recorder) documentation for more information.

<a name="slow-jobs-card"></a>
#### Slow Jobs

The `<livewire:pulse.slow-jobs />` card shows the queued jobs in your application that exceed the configured threshold, which is 1,000ms by default. See the [slow jobs recorder](#slow-jobs-recorder) documentation for more information.

<a name="slow-queries-card"></a>
#### Slow Queries

The `<livewire:pulse.slow-queries />` card shows the database queries in your application that exceed the configured threshold, which is 1,000ms by default.

By default, slow queries are grouped based on the SQL query (without bindings) and the location where it occurred, but you may choose to not capture the location if you wish to group solely on the SQL query.

If you encounter rendering performance issues due to extremely large SQL queries receiving syntax highlighting, you may disable highlighting by adding the `without-highlighting` prop:

```blade
<livewire:pulse.slow-queries without-highlighting />
```



See the [slow queries recorder](#slow-queries-recorder) documentation for more information.

<a name="slow-outgoing-requests-card"></a>
#### Slow Outgoing Requests

The `<livewire:pulse.slow-outgoing-requests />` card shows outgoing requests made using Laravel's [HTTP client](/docs/{{version}}/http-client) that exceed the configured threshold, which is 1,000ms by default.

By default, entries will be grouped by the full URL. However, you may wish to normalize or group similar outgoing requests using regular expressions. See the [slow outgoing requests recorder](#slow-outgoing-requests-recorder) documentation for more information.

<a name="cache-card"></a>
#### Cache

The `<livewire:pulse.cache />` card shows the cache hit and miss statistics for your application, both globally and for individual keys.

By default, entries will be grouped by key. However, you may wish to normalize or group similar keys using regular expressions. See the [cache interactions recorder](#cache-interactions-recorder) documentation for more information.

<a name="capturing-entries"></a>
## Capturing Entries

Most Pulse recorders will automatically capture entries based on framework events dispatched by Laravel. However, the [servers recorder](#servers-recorder) and some third-party cards must poll for information regularly. To use these cards, you must run the `pulse:check` daemon on all of your individual application servers:

```shell
php artisan pulse:check
```



> [!NOTE]
> `pulse:check` 프로세스를 백그라운드에서 영구적으로 실행하려면, 명령어가 중단되지 않도록 Supervisor와 같은 프로세스 모니터를 사용해야 합니다.

`pulse:check` 명령어는 오래 실행되는 프로세스이므로, 재시작하지 않으면 코드베이스 변경 사항을 반영하지 못합니다. 애플리케이션 배포 과정에서 `pulse:restart` 명령어를 호출하여 명령어를 정상적으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```



> [!NOTE]
> Pulse uses the [cache](/docs/{{version}}/cache) to store restart signals, so you should verify that a cache driver is properly configured for your application before using this feature.

<a name="recorders"></a>
### Recorders

Recorders are responsible for capturing entries from your application to be recorded in the Pulse database. Recorders are registered and configured in the `recorders` section of the [Pulse configuration file](#configuration).

<a name="cache-interactions-recorder"></a>
#### Cache Interactions

The `CacheInteractions` recorder captures information about the [cache](/docs/{{version}}/cache) hits and misses occurring in your application for display on the [Cache](#cache-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored key patterns.

You may also configure key grouping so that similar keys are grouped as a single entry. For example, you may wish to remove unique IDs from keys caching the same type of information. Groups are configured using a regular expression to "find and replace" parts of the key. An example is included in the configuration file:

```php
Recorders\CacheInteractions::class => [
    // ...
    'groups' => [
        // '/:\d+/' => ':*',
    ],
],
```



The first pattern that matches will be used. If no patterns match, then the key will be captured as-is.

<a name="exceptions-recorder"></a>
#### Exceptions

The `Exceptions` recorder captures information about reportable exceptions occurring in your application for display on the [Exceptions](#exceptions-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored exception patterns. You may also configure whether to capture the location that the exception originated from. The captured location will be displayed on the Pulse dashboard which can help to track down the exception origin; however, if the same exception occurs in multiple locations then it will appear multiple times for each unique location.

<a name="queues-recorder"></a>
#### Queues

The `Queues` recorder captures information about your application's queues for display on the [Queues](#queues-card).

You may optionally adjust the [sample rate](#sampling) and ignored jobs patterns.

<a name="slow-jobs-recorder"></a>
#### Slow Jobs

The `SlowJobs` recorder captures information about slow jobs occurring in your application for display on the [Slow Jobs](#slow-jobs-recorder) card.

You may optionally adjust the slow job threshold, [sample rate](#sampling), and ignored job patterns.

You may have some jobs that you expect to take longer than others. In those cases, you may configure per-job thresholds:

```php
Recorders\SlowJobs::class => [
    // ...
    'threshold' => [
        '#^App\\Jobs\\GenerateYearlyReports$#' => 5000,
        'default' => env('PULSE_SLOW_JOBS_THRESHOLD', 1000),
    ],
],
```



만약 어떤 정규식 패턴도 작업의 클래스 이름과 일치하지 않으면, `'default'` 값이 사용됩니다.

<a name="slow-outgoing-requests-recorder"></a>
#### 느린 발신 요청

`SlowOutgoingRequests` 기록기는 Laravel의 [HTTP 클라이언트](/docs/{{version}}/http-client)를 사용하여 수행된 외부 HTTP 요청 중 구성된 임계값을 초과하는 요청에 대한 정보를 [느린 발신 요청](#slow-outgoing-requests-card) 카드에 표시하기 위해 캡처합니다.

선택적으로 느린 발신 요청 임계값, [샘플링 비율](#sampling), 및 무시할 URL 패턴을 조정할 수 있습니다.

일부 발신 요청은 다른 요청보다 더 오래 걸릴 것으로 예상될 수 있습니다. 이러한 경우, 요청별 임계값을 구성할 수 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'threshold' => [
        '#backup.zip$#' => 5000,
        'default' => env('PULSE_SLOW_OUTGOING_REQUESTS_THRESHOLD', 1000),
    ],
],
```



요청의 URL과 일치하는 정규 표현식 패턴이 없으면 `'default'` 값이 사용됩니다.

유사한 URL을 단일 항목으로 그룹화하도록 URL 그룹화를 구성할 수도 있습니다. 예를 들어, URL 경로에서 고유 ID를 제거하거나 도메인 기준으로 그룹화할 수 있습니다. 그룹은 URL의 일부를 "찾아서 교체"하는 정규 표현식을 사용하여 구성됩니다. 몇 가지 예제는 구성 파일에 포함되어 있습니다:

```php
Recorders\SlowOutgoingRequests::class => [
    // ...
    'groups' => [
        // '#^https://api\.github\.com/repos/.*$#' => 'api.github.com/repos/*',
        // '#^https?://([^/]*).*$#' => '\1',
        // '#/\d+#' => '/*',
    ],
],
```



일치하는 첫 번째 패턴이 사용됩니다. 패턴이 일치하지 않으면 URL이 있는 그대로 캡처됩니다.

<a name="slow-queries-recorder"></a>
#### 느린 쿼리

`SlowQueries` 레코더는 애플리케이션에서 구성된 임계값을 초과하는 모든 데이터베이스 쿼리를 캡처하여 [느린 쿼리](#slow-queries-card) 카드에 표시합니다.

선택적으로 느린 쿼리 임계값, [샘플 비율](#sampling) 및 무시할 쿼리 패턴을 조정할 수 있습니다. 쿼리 위치를 캡처할지 여부 또한 구성할 수 있습니다. 캡처된 위치는 Pulse 대시보드에 표시되어 쿼리 출처를 추적하는 데 도움이 됩니다; 그러나 동일한 쿼리가 여러 위치에서 수행되면 고유 위치별로 여러 번 표시됩니다.

일부 쿼리는 다른 쿼리보다 더 오래 걸릴 것으로 예상될 수 있습니다. 그런 경우 개별 쿼리별 임계값을 구성할 수 있습니다:

```php
Recorders\SlowQueries::class => [
    // ...
    'threshold' => [
        '#^insert into `yearly_reports`#' => 5000,
        'default' => env('PULSE_SLOW_QUERIES_THRESHOLD', 1000),
    ],
],
```



쿼리의 SQL과 일치하는 정규식 패턴이 없으면 `'default'` 값이 사용됩니다.

<a name="slow-requests-recorder"></a>
#### 느린 요청

`Requests` 레코더는 애플리케이션에 대한 요청 정보를 캡처하여 [느린 요청](#slow-requests-card) 및 [애플리케이션 사용](#application-usage-card) 카드에 표시합니다.

느린 경로 임계값, [샘플 비율](#sampling), 무시된 경로를 선택적으로 조정할 수 있습니다.

일부 요청은 다른 요청보다 시간이 더 걸릴 것으로 예상될 수 있습니다. 이러한 경우, 요청별 임계값을 구성할 수 있습니다:

```php
Recorders\SlowRequests::class => [
    // ...
    'threshold' => [
        '#^/admin/#' => 5000,
        'default' => env('PULSE_SLOW_REQUESTS_THRESHOLD', 1000),
    ],
],
```



요청의 URL과 일치하는 정규 표현식 패턴이 없으면 `'default'` 값이 사용됩니다.

<a name="servers-recorder"></a>
#### 서버

`Servers` 레코더는 애플리케이션을 지원하는 서버의 CPU, 메모리 및 저장소 사용량을 [서버](#servers-card) 카드에 표시하기 위해 캡처합니다. 이 레코더는 모니터링하려는 각 서버에서 [pulse:check 명령](#capturing-entries)이 실행 중이어야 합니다.

각 보고 서버는 고유한 이름을 가져야 합니다. 기본적으로 Pulse는 PHP의 `gethostname` 함수가 반환하는 값을 사용합니다. 이를 맞춤 설정하려면 `PULSE_SERVER_NAME` 환경 변수를 설정할 수 있습니다:

```env
PULSE_SERVER_NAME=load-balancer
```



The Pulse configuration file also allows you to customize the directories that are monitored.

<a name="user-jobs-recorder"></a>
#### User Jobs

The `UserJobs` recorder captures information about the users dispatching jobs in your application for display on the [Application Usage](#application-usage-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored job patterns.

<a name="user-requests-recorder"></a>
#### User Requests

The `UserRequests` recorder captures information about the users making requests to your application for display on the [Application Usage](#application-usage-card) card.

You may optionally adjust the [sample rate](#sampling) and ignored URL patterns.

<a name="filtering"></a>
### Filtering

As we have seen, many [recorders](#recorders) offer the ability to, via configuration, "ignore" incoming entries based on their value, such as a request's URL. But, sometimes it may be useful to filter out records based on other factors, such as the currently authenticated user. To filter out these records, you may pass a closure to Pulse's `filter` method. Typically, the `filter` method should be invoked within the `boot` method of your application's `AppServiceProvider`:

```php
use Illuminate\Support\Facades\Auth;
use Laravel\Pulse\Entry;
use Laravel\Pulse\Facades\Pulse;
use Laravel\Pulse\Value;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pulse::filter(function (Entry|Value $entry) {
        return Auth::user()->isNotAdmin();
    });

    // ...
}
```



<a name="performance"></a>
## 성능

Pulse는 추가 인프라 없이 기존 애플리케이션에 바로 통합되도록 설계되었습니다. 그러나 트래픽이 많은 애플리케이션의 경우, Pulse가 애플리케이션 성능에 미치는 영향을 최소화하는 여러 방법이 있습니다.

<a name="using-a-different-database"></a>
### 다른 데이터베이스 사용하기

트래픽이 많은 애플리케이션의 경우, 애플리케이션 데이터베이스에 영향을 주지 않도록 Pulse 전용 데이터베이스 연결을 사용하는 것이 좋습니다.

Pulse에서 사용하는 [데이터베이스 연결](/docs/{{version}}/database#configuration)을 `PULSE_DB_CONNECTION` 환경 변수를 설정하여 맞춤 설정할 수 있습니다.

```env
PULSE_DB_CONNECTION=pulse
```



<a name="ingest"></a>
### Redis 수집

> [!WARNING]
> Redis 수집은 Redis 6.2 이상과 애플리케이션이 구성한 Redis 클라이언트 드라이버로 `phpredis` 또는 `predis`가 필요합니다.

기본적으로, Pulse는 HTTP 응답이 클라이언트에게 전송되거나 작업이 처리된 후 [구성된 데이터베이스 연결](#using-a-different-database)에 항목을 직접 저장합니다. 그러나 Pulse의 Redis 수집 드라이버를 사용하여 항목을 Redis 스트림으로 보낼 수도 있습니다. 이것은 `PULSE_INGEST_DRIVER` 환경 변수를 구성하여 활성화할 수 있습니다:

```ini
PULSE_INGEST_DRIVER=redis
```



Pulse는 기본적으로 기본 [Redis 연결](/docs/{{version}}/redis#configuration)을 사용하지만, `PULSE_REDIS_CONNECTION` 환경 변수를 통해 이를 사용자 지정할 수 있습니다:

```ini
PULSE_REDIS_CONNECTION=pulse
```



> [!WARNING]
> Redis 수집 드라이버를 사용할 때, Pulse 설치는 해당되는 경우 Redis 기반 큐와 다른 Redis 연결을 항상 사용해야 합니다.

Redis 수집을 사용할 때, `pulse:work` 명령을 실행하여 스트림을 모니터링하고 Redis에서 Pulse의 데이터베이스 테이블로 항목을 이동해야 합니다.

```shell
php artisan pulse:work
```



> [!NOTE]
> `pulse:work` 프로세스를 백그라운드에서 항상 실행 상태로 유지하려면, Supervisor와 같은 프로세스 모니터를 사용하여 Pulse 워커가 실행을 멈추지 않도록 해야 합니다.

`pulse:work` 명령은 장기 실행 프로세스이므로, 재시작하지 않으면 코드베이스의 변경 사항을 감지하지 못합니다. 애플리케이션 배포 과정에서 `pulse:restart` 명령을 호출하여 명령을 정상적으로 재시작해야 합니다:

```shell
php artisan pulse:restart
```



> [!NOTE]
> Pulse uses the [cache](/docs/{{version}}/cache) to store restart signals, so you should verify that a cache driver is properly configured for your application before using this feature.

<a name="sampling"></a>
### Sampling

By default, Pulse will capture every relevant event that occurs in your application. For high-traffic applications, this can result in needing to aggregate millions of database rows in the dashboard, especially for longer time periods.

You may instead choose to enable "sampling" on certain Pulse data recorders. For example, setting the sample rate to `0.1` on the [User Requests](#user-requests-recorder) recorder will mean that you only record approximately 10% of the requests to your application. In the dashboard, the values will be scaled up and prefixed with a `~` to indicate that they are an approximation.

In general, the more entries you have for a particular metric, the lower you can safely set the sample rate without sacrificing too much accuracy.

<a name="trimming"></a>
### Trimming

Pulse will automatically trim its stored entries once they are outside of the dashboard window. Trimming occurs when ingesting data using a lottery system which may be customized in the Pulse [configuration file](#configuration).

<a name="pulse-exceptions"></a>
### Handling Pulse Exceptions

If an exception occurs while capturing Pulse data, such as being unable to connect to the storage database, Pulse will silently fail to avoid impacting your application.

If you wish to customize how these exceptions are handled, you may provide a closure to the `handleExceptionsUsing` method:

```php
use Laravel\Pulse\Facades\Pulse;
use Illuminate\Support\Facades\Log;

Pulse::handleExceptionsUsing(function ($e) {
    Log::debug('An exception happened in Pulse', [
        'message' => $e->getMessage(),
        'stack' => $e->getTraceAsString(),
    ]);
});
```



<a name="custom-cards"></a>
## 커스텀 카드

Pulse를 사용하면 애플리케이션의 특정 요구 사항과 관련된 데이터를 표시하기 위해 커스텀 카드를 만들 수 있습니다. Pulse는 [Livewire](https://livewire.laravel.com)를 사용하므로, 첫 번째 커스텀 카드를 만들기 전에 [문서를 검토](https://livewire.laravel.com/docs)하는 것이 좋습니다.

<a name="custom-card-components"></a>
### 카드 구성 요소

Laravel Pulse에서 커스텀 카드를 만들려면 기본 `Card` Livewire 구성 요소를 확장하고 해당 뷰를 정의하는 것으로 시작합니다:

```php
namespace App\Livewire\Pulse;

use Laravel\Pulse\Livewire\Card;
use Livewire\Attributes\Lazy;

#[Lazy]
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers');
    }
}
```



Livewire의 [지연 로딩](https://livewire.laravel.com/docs/lazy) 기능을 사용할 때, `Card` 컴포넌트는 컴포넌트에 전달된 `cols` 및 `rows` 속성을 존중하는 자리 표시자를 자동으로 제공합니다.

Pulse 카드의 해당 뷰를 작성할 때, 일관된 모양과 느낌을 위해 Pulse의 Blade 컴포넌트를 활용할 수 있습니다:

```blade
<x-pulse::card :cols="$cols" :rows="$rows" :class="$class" wire:poll.5s="">
    <x-pulse::card-header name="Top Sellers">
        <x-slot:icon>
            ...
        </x-slot:icon>
    </x-pulse::card-header>

    <x-pulse::scroll :expand="$expand">
        ...
    </x-pulse::scroll>
</x-pulse::card>
```



`$cols`, `$rows`, `$class` 및 `$expand` 변수는 각각의 Blade 컴포넌트에 전달되어 카드 레이아웃을 대시보드 뷰에서 맞춤 설정할 수 있어야 합니다. 또한 카드를 자동으로 업데이트하려면 `wire:poll.5s=""` 속성을 뷰에 포함시키는 것이 좋습니다.

Livewire 컴포넌트와 템플릿을 정의한 후에는 카드가 [대시보드 뷰](#dashboard-customization)에 포함될 수 있습니다:

```blade
<x-pulse>
    ...

    <livewire:pulse.top-sellers cols="4" />
</x-pulse>
```



> [!NOTE]
> 카드가 패키지에 포함된 경우, `Livewire::component` 방법을 사용하여 Livewire에 구성 요소를 등록해야 합니다.

<a name="custom-card-styling"></a>
### 스타일링

카드가 Pulse에 포함된 클래스 및 구성 요소를 넘어 추가 스타일링이 필요한 경우, 카드에 대한 사용자 정의 CSS를 포함할 수 있는 몇 가지 옵션이 있습니다.

<a name="custom-card-styling-vite"></a>
#### Laravel Vite 통합

사용자 정의 카드가 애플리케이션 코드베이스 내에 있고 Laravel의 [Vite 통합](/docs/{{version}}/vite)을 사용하는 경우, 카드에 전용 CSS 진입점을 포함하도록 `vite.config.js` 파일을 업데이트할 수 있습니다:

```js
laravel({
    input: [
        'resources/css/pulse/top-sellers.css',
        // ...
    ],
}),
```



그런 다음 [대시보드 보기](#dashboard-customization)에서 `@vite` 블레이드 지시문을 사용하여 카드의 CSS 진입점을 지정할 수 있습니다:

```blade
<x-pulse>
    @vite('resources/css/pulse/top-sellers.css')

    ...
</x-pulse>
```



<a name="custom-card-styling-css"></a>
#### CSS 파일

패키지에 포함된 Pulse 카드를 포함한 다른 사용 사례의 경우, Livewire 컴포넌트에서 `css` 메서드를 정의하여 CSS 파일의 경로를 반환하도록 Pulse에 추가 스타일시트를 로드하도록 지시할 수 있습니다:

```php
class TopSellers extends Card
{
    // ...

    protected function css()
    {
        return __DIR__.'/../../dist/top-sellers.css';
    }
}
```



이 카드를 대시보드에 포함하면, Pulse는 이 파일의 내용을 `<style>` 태그 안에 자동으로 포함하므로 `public` 디렉토리에 게시할 필요가 없습니다.

<a name="custom-card-styling-tailwind"></a>
#### Tailwind CSS

Tailwind CSS를 사용할 때는 전용 CSS 진입점을 만들어야 합니다. 다음 예제는 Pulse에 이미 포함되어 있는 Tailwind의 [Preflight](https://tailwindcss.com/docs/preflight) 기본 스타일을 제외하고, CSS 선택자를 사용하여 Tailwind를 범위 지정하여 Pulse의 Tailwind 클래스와 충돌을 피하도록 합니다:

```css
@import "tailwindcss/theme.css";

@custom-variant dark (&:where(.dark, .dark *));
@source "./../../views/livewire/pulse/top-sellers.blade.php";

@theme {
  /* ... */
}

#top-sellers {
  @import "tailwindcss/utilities.css" source(none);
}
```



또한 엔트리포인트의 CSS 선택자와 일치하는 `id` 또는 `class` 속성을 카드의 뷰에 포함해야 합니다:

```blade
<x-pulse::card id="top-sellers" :cols="$cols" :rows="$rows" class="$class">
    ...
</x-pulse::card>
```



<a name="custom-card-data"></a>
### 데이터 수집 및 집계

맞춤 카드에서는 어디서든 데이터를 가져와 표시할 수 있습니다. 그러나 Pulse의 강력하고 효율적인 데이터 기록 및 집계 시스템을 활용하고자 할 수 있습니다.

<a name="custom-card-data-capture"></a>
#### 항목 기록

Pulse에서는 `Pulse::record` 방식을 사용하여 '항목'을 기록할 수 있습니다:

```php
use Laravel\Pulse\Facades\Pulse;

Pulse::record('user_sale', $user->id, $sale->amount)
    ->sum()
    ->count();
```



The first argument provided to the `record` method is the `type` for the entry you are recording, while the second argument is the `key` that determines how the aggregated data should be grouped. For most aggregation methods you will also need to specify a `value` to be aggregated. In the example above, the value being aggregated is `$sale->amount`. You may then invoke one or more aggregation methods (such as `sum`) so that Pulse may capture pre-aggregated values into "buckets" for efficient retrieval later.

The available aggregation methods are:

* `avg`
* `count`
* `max`
* `min`
* `sum`

> [!NOTE]
> When building a card package that captures the currently authenticated user ID, you should use the `Pulse::resolveAuthenticatedUserId()` method, which respects any [user resolver customizations](#dashboard-resolving-users) made to the application.

<a name="custom-card-data-retrieval"></a>
#### Retrieving Aggregate Data

When extending Pulse's `Card` Livewire component, you may use the `aggregate` method to retrieve aggregated data for the period being viewed in the dashboard:

```php
class TopSellers extends Card
{
    public function render()
    {
        return view('livewire.pulse.top-sellers', [
            'topSellers' => $this->aggregate('user_sale', ['sum', 'count'])
        ]);
    }
}
```



`aggregate` 메서드는 PHP `stdClass` 객체 컬렉션을 반환합니다. 각 객체는 이전에 캡처된 `key` 속성과 요청된 각 집계에 대한 키를 포함하게 됩니다:

```blade
@foreach ($topSellers as $seller)
    {{ $seller->key }}
    {{ $seller->sum }}
    {{ $seller->count }}
@endforeach
```



Pulse는 주로 미리 집계된 버킷에서 데이터를 가져올 것입니다. 따라서 지정된 집계는 `Pulse::record` 방법을 사용하여 사전에 캡처되어야 합니다. 가장 오래된 버킷은 일반적으로 기간의 일부 밖에 걸쳐 있을 것이므로, Pulse는 전체 기간에 대한 정확한 값을 제공하고 격차를 메우기 위해 가장 오래된 항목을 집계할 것이며, 각 폴 요청마다 전체 기간을 집계할 필요는 없습니다.

또한 `aggregateTotal` 방법을 사용하여 주어진 유형의 총값을 가져올 수도 있습니다. 예를 들어, 다음 방법은 사용자를 기준으로 그룹화하는 대신 모든 사용자 판매의 총합을 가져올 것입니다.

```php
$total = $this->aggregateTotal('user_sale', 'sum');
```



<a name="custom-card-displaying-users"></a>
#### 사용자 표시

사용자 ID를 키로 기록하는 집계를 작업할 때, `Pulse::resolveUsers` 방법을 사용하여 키를 사용자 기록으로 확인할 수 있습니다:

```php
$aggregates = $this->aggregate('user_sale', ['sum', 'count']);

$users = Pulse::resolveUsers($aggregates->pluck('key'));

return view('livewire.pulse.top-sellers', [
    'sellers' => $aggregates->map(fn ($aggregate) => (object) [
        'user' => $users->find($aggregate->key),
        'sum' => $aggregate->sum,
        'count' => $aggregate->count,
    ])
]);
```



`find` 메서드는 `name`, `extra` 및 `avatar` 키를 포함하는 객체를 반환하며, 이를 선택적으로 `<x-pulse::user-card>` Blade 컴포넌트에 직접 전달할 수 있습니다:

```blade
<x-pulse::user-card :user="{{ $seller->user }}" :stats="{{ $seller->sum }}" />
```



<a name="custom-recorders"></a>
#### 맞춤 기록기

패키지 작성자는 사용자가 데이터 캡처를 구성할 수 있도록 기록기 클래스를 제공하고 싶어할 수 있습니다.

기록기는 애플리케이션의 `config/pulse.php` 구성 파일의 `recorders` 섹션에 등록됩니다:

```php
[
    // ...
    'recorders' => [
        Acme\Recorders\Deployments::class => [
            // ...
        ],

        // ...
    ],
]
```



기록자는 `$listen` 속성을 지정하여 이벤트를 들을 수 있습니다. Pulse는 자동으로 리스너를 등록하고 기록자의 `record` 메서드를 호출합니다:

```php
<?php

namespace Acme\Recorders;

use Acme\Events\Deployment;
use Illuminate\Support\Facades\Config;
use Laravel\Pulse\Facades\Pulse;

class Deployments
{
    /**
     * The events to listen for.
     *
     * @var array<int, class-string>
     */
    public array $listen = [
        Deployment::class,
    ];

    /**
     * Record the deployment.
     */
    public function record(Deployment $event): void
    {
        $config = Config::get('pulse.recorders.'.static::class);

        Pulse::record(
            // ...
        );
    }
}
```
{% endraw %}
