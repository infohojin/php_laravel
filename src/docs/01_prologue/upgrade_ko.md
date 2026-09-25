---
layout: docs
title: "업그레이드 안내"
---

{% raw %}
# 업그레이드 안내

- [12.x에서 13.0으로 업그레이드](#upgrade-13.0)
    - [AI를 이용한 업그레이드](#upgrading-using-ai)

<a name="high-impact-changes"></a>
## 큰 영향을 미치는 변경 사항

<div class="content-list" markdown="1">

- [종속성 업데이트](#updating-dependencies)
- [Laravel 설치 프로그램 업데이트](#updating-the-laravel-installer)
- [위변조방지요청](#request-forgery-protection)

</div>

<a name="medium-impact-changes"></a>
## 중간 정도의 영향 변경

<div class="content-list" markdown="1">

- [캐시 `serializable_classes` 구성](#cache-serializable_classes-configuration)
- [MySQL 또는 MariaDB를 사용하는 데이터베이스 `upsert`](#database-upsert-mariadb-mysql)

</div>

<a name="low-impact-changes"></a>
## 영향이 적은 변경 사항

<div class="content-list" markdown="1">

- [캐시 접두사 및 세션 쿠키 이름](#cache-prefixes-and-session-cookie-names)
- [컬렉션 모델 직렬화로 Eager-Loaded 관계 복원](#collection-model-serialization-restores-eager-loaded-relations)
- [`Container::call` 및 Nullable 클래스 기본값](#containercall-and-nullable-class-defaults)
- [도메인 경로 등록 우선순위](#domain-route-registration-precedence)
- [`JobAttempted` 이벤트 예외 페이로드](#jobattempted-event-exception-payload)
- [관리자 `extend` 콜백 바인딩](#manager-extend-callback-binding)
- [`JOIN`, `ORDER BY` 및 `LIMIT`를 사용한 MySQL `DELETE` 쿼리](#mysql-delete-queries-with-join-order-by-and-limit)
- [페이지 매김 부트스트랩 뷰 이름](#pagination-bootstrap-view-names)
- [다형성 피벗 테이블 이름 생성](#polymorphic-pivot-table-name-generation)
- [`QueueBusy` 이벤트 속성 이름 변경](#queuebusy-event-property-rename)
- [세션 `serialization` 구성](#session-serialization-configuration)
- [테스트 사이에 `Str` 공장 재설정](#str-factories-reset-between-tests)

</div>

<a name="upgrade-13.0"></a>
## 12.x에서 13.0으로 업그레이드

#### 예상 업그레이드 시간: 10분

> [!NOTE]
> 우리는 가능한 모든 주요 변경 사항을 문서화하려고 시도합니다. 이러한 주요 변경 사항 중 일부는 프레임워크의 모호한 부분에 있으므로 이러한 변경 사항 중 일부만 실제로 애플리케이션에 영향을 미칠 수 있습니다. 시간을 절약하려면 [Shift](https://laravelshift.com)를 사용할 수 있습니다. Shift는 Laravel 업그레이드를 자동화하는 커뮤니티 유지 서비스입니다.

<a name="upgrading-using-ai"></a>
### AI를 활용한 업그레이드

[Laravel Boost](https://github.com/laravel/boost)를 사용하여 업그레이드를 자동화할 수 있습니다. Boost는 AI 도우미에게 업그레이드 안내 메시지를 제공하는 자사 MCP 서버입니다. 일단 Laravel 12 애플리케이션에 설치하면 Claude Code, Cursor, OpenCode, Gemini 또는 VS Code에서 `/upgrade-laravel-v13` 슬래시 명령을 사용하여 Laravel 13으로 업그레이드를 시작합니다. 이 명령에는 Laravel Boost `^2.0`가 필요합니다.

<a name="updating-dependencies"></a>
### 종속성 업데이트

**영향 가능성: 높음**

애플리케이션의 `composer.json` 파일에서 다음 종속성을 업데이트해야 합니다.

<div class="content-list" markdown="1">

- `laravel/framework` ~ `^13.0`
- `laravel/boost`에서 `^2.0`로
- `laravel/tinker`에서 `^3.0`까지
- `phpunit/phpunit` ~ `^12.0`
- `pestphp/pest` ~ `^4.0`

</div>

<a name="updating-the-laravel-installer"></a>
### Laravel 설치 프로그램 업데이트

Laravel 설치 프로그램 CLI 도구를 사용하여 새로운 Laravel 애플리케이션을 생성하는 경우 Laravel 13.x 호환성을 위해 설치 프로그램 설치를 업데이트해야 합니다.

`composer global require`를 통해 Laravel 설치 프로그램을 설치한 경우 `composer global update`를 사용하여 설치 프로그램을 업데이트할 수 있습니다:

```shell
composer global update laravel/installer

```

또는 [Laravel Herd's](https://herd.laravel.com) 번들 설치 프로그램 Laravel 설치 프로그램을 사용하는 경우 Herd 설치를 최신 릴리스로 업데이트해야 합니다.

<a name="cache"></a>
### 캐시

<a name="cache-prefixes-and-session-cookie-names"></a>
#### 캐시 접두사 및 세션 쿠키 이름

**영향 가능성: 낮음**

Laravel의 기본 캐시와 Redis 키 접두사는 이제 하이픈으로 연결된 접미사를 사용합니다.

대부분의 애플리케이션에서는 애플리케이션 수준 구성 파일이 이미 이러한 값을 정의하므로 이 변경 사항이 적용되지 않습니다. 이는 해당 애플리케이션 구성 값이 없을 때 프레임워크 수준 대체 구성에 의존하는 애플리케이션에 주로 영향을 미칩니다.

애플리케이션이 생성된 기본값을 사용하는 경우 업그레이드 후 캐시 키와 세션 쿠키 이름이 변경될 수 있습니다.

```php
// Laravel <= 12.x
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_cache_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_database_';
Str::slug((string) env('APP_NAME', 'laravel'), '_').'_session';

// Laravel >= 13.x
Str::slug((string) env('APP_NAME', 'laravel')).'-cache-';
Str::slug((string) env('APP_NAME', 'laravel')).'-database-';
Str::slug((string) env('APP_NAME', 'laravel')).'-session';

```

이전 동작을 유지하려면 환경에서 `CACHE_PREFIX`, `REDIS_PREFIX` 및 `SESSION_COOKIE`를 명시적으로 구성하십시오.

<a name="store-and-repository-contracts-touch"></a>
#### `Store` 및 `Repository` 계약: `touch`

**영향 가능성: 매우 낮음**

이제 캐시 계약에는 항목 TTL을 확장하기 위한 `touch` 방법이 포함됩니다. 사용자 정의 캐시 저장소 구현을 유지하는 경우 다음 메소드를 추가해야 합니다.

```php
// Illuminate\Contracts\Cache\Store
public function touch($key, $seconds);

```

<a name="cache-serializable_classes-configuration"></a>
#### 캐시 `serializable_classes` 구성

**영향 가능성: 중간**

기본 애플리케이션 `cache` 구성에는 이제 `false`로 설정된 `serializable_classes` 옵션이 포함됩니다. 이는 애플리케이션의 `APP_KEY`가 유출된 경우 PHP 역직렬화 가젯 체인 공격을 방지하는 데 도움이 되도록 캐시 역직렬화 동작을 강화합니다. 애플리케이션이 의도적으로 PHP 객체를 캐시에 저장하는 경우 직렬화 해제될 수 있는 클래스를 명시적으로 나열해야 합니다.

```php
'serializable_classes' => [
    App\Data\CachedDashboardStats::class,
    App\Support\CachedPricingSnapshot::class,
],

```

이전에 애플리케이션이 임의의 캐시된 객체를 직렬화 해제하는 데 의존했다면 해당 사용법을 명시적 클래스 허용 목록 또는 비객체 캐시 페이로드(예: 배열)로 마이그레이션해야 합니다.

<a name="container"></a>
### 컨테이너

<a name="containercall-and-nullable-class-defaults"></a>
#### `Container::call` 및 Nullable 클래스 기본값

**영향 가능성: 낮음**

`Container::call`는 이제 바인딩이 없을 때 nullable 클래스 매개변수 기본값을 존중하며 Laravel 12에 도입된 생성자 주입 동작과 일치합니다.

```php
$container->call(function (?Carbon $date = null) {
    return $date;
});

// Laravel <= 12.x: Carbon instance
// Laravel >= 13.x: null

```

메서드 호출 주입 논리가 이전 동작에 의존하는 경우 이를 업데이트해야 할 수도 있습니다.

<a name="contracts"></a>
### 계약

<a name="dispatcher-contract-dispatchafterresponse"></a>
#### `Dispatcher` 계약: `dispatchAfterResponse`

**영향 가능성: 매우 낮음**

이제 `Illuminate\Contracts\Bus\Dispatcher` 계약에는 `dispatchAfterResponse($command, $handler = null)` 방법이 포함됩니다.

사용자 정의 디스패처 구현을 유지하는 경우 이 메서드를 클래스에 추가하세요.

<a name="responsefactory-contract-eventstream"></a>
#### `ResponseFactory` 계약: `eventStream`

**영향 가능성: 매우 낮음**

이제 `Illuminate\Contracts\Routing\ResponseFactory` 계약에는 `eventStream` 서명이 포함됩니다.

이 계약의 사용자 정의 구현을 유지하는 경우 이 메서드를 추가해야 합니다.

<a name="mustverifyemail-contract-markemailasunverified"></a>
#### `MustVerifyEmail` 계약: `markEmailAsUnverified`

**영향 가능성: 매우 낮음**

이제 `Illuminate\Contracts\Auth\MustVerifyEmail` 계약에는 `markEmailAsUnverified()`가 포함됩니다.

이 계약의 사용자 정의 구현을 제공하는 경우 호환성을 유지하려면 이 메서드를 추가하세요.

<a name="database"></a>
### 데이터베이스

<a name="database-upsert-mariadb-mysql"></a>
#### MySQL 또는 MariaDB를 사용하는 데이터베이스 `upsert`

**영향 가능성: 중간**

이제 Laravel은 호출자가 `uniqueBy`에 대해 비어 있지 않은 값을 제공하는지 확인하고 잘못된 SQL을 생성하는 대신 `InvalidArgumentException`를 발생시킵니다.

MariaDB 및 MySQL 데이터베이스 드라이버는 `uniqueBy` 값을 무시하고 항상 테이블의 기본 및 고유 인덱스를 사용하여 기존 레코드를 검색하지만 유효성 검사는 계속 적용됩니다. `uniqueBy`가 비어 있으면 `InvalidArgumentException`가 발생합니다.

<a name="mysql-delete-queries-with-join-order-by-and-limit"></a>
#### `JOIN`, `ORDER BY` 및 `LIMIT`를 사용한 MySQL `DELETE` 쿼리

**영향 가능성: 낮음**

Laravel은 이제 MySQL 문법용 `ORDER BY` 및 `LIMIT`를 포함한 전체 `DELETE ... JOIN` 쿼리를 컴파일합니다.

이전 버전에서는 결합 삭제 시 `ORDER BY` / `LIMIT` 절이 자동으로 무시될 수 있었습니다. Laravel 13에서는 이러한 절이 생성된 SQL에 포함됩니다. 결과적으로 이 구문을 지원하지 않는 데이터베이스 엔진(예: 표준 MySQL/MariaDB 변형)은 이제 무제한 삭제를 실행하는 대신 `QueryException`를 발생시킬 수 있습니다.

<a name="eloquent"></a>
### Eloquent

<a name="model-booting-and-nested-instantiation"></a>
#### Model Booting and Nested Instantiation

**Likelihood Of Impact: Very Low**

Creating a new model instance while that model is still booting is now disallowed and throws a `LogicException`.

This affects code that instantiates models from inside model `boot` methods or trait `boot*` methods:

```php
protected static function boot()
{
    parent::boot();

    // No longer allowed during booting...
    (new static())->getTable();
}

```

Move this logic outside the boot cycle to avoid nested booting.

<a name="polymorphic-pivot-table-name-generation"></a>
#### Polymorphic Pivot Table Name Generation

**Likelihood Of Impact: Low**

When table names are inferred for polymorphic pivot models using custom pivot model classes, Laravel now generates pluralized names.

If your application depended on the previous singular inferred names for morph pivot tables and used custom pivot classes, you should explicitly define the table name on your pivot model.

<a name="collection-model-serialization-restores-eager-loaded-relations"></a>
#### Collection Model Serialization Restores Eager-Loaded Relations

**Likelihood Of Impact: Low**

When Eloquent model collections are serialized and restored (such as in queued jobs), eager-loaded relations are now restored for the collection's models.

If your code depended on relations not being present after deserialization, you may need to adjust that logic.

<a name="http-client"></a>
### HTTP Client

<a name="http-client-response-throw-and-throwif-signatures"></a>
#### HTTP Client `Response::throw` and `throwIf` Signatures

**Likelihood Of Impact: Very Low**

The HTTP client response methods now declare their callback parameters in the method signatures:

```php
public function throw($callback = null);
public function throwIf($condition, $callback = null);

```

If you override these methods in custom response classes, ensure your method signatures are compatible.

<a name="notifications"></a>
### Notifications

<a name="default-password-reset-subject"></a>
#### Default Password Reset Subject

**Likelihood Of Impact: Very Low**

Laravel's default password reset mail subject has changed:

```text
// Laravel <= 12.x
Reset Password Notification

// Laravel >= 13.x
Reset your password

```

If your tests, assertions, or translation overrides depend on the previous default string, update them accordingly.

<a name="queued-notifications-and-missing-models"></a>
#### Queued Notifications and Missing Models

**Likelihood Of Impact: Very Low**

Queued notifications now respect the `#[DeleteWhenMissingModels]` attribute and `$deleteWhenMissingModels` property defined on the notification class.

In previous versions, missing models could still cause queued notification jobs to fail in cases where you expected them to be deleted.

<a name="queue"></a>
### Queue

<a name="jobattempted-event-exception-payload"></a>
#### `JobAttempted` Event Exception Payload

**Likelihood Of Impact: Low**

The `Illuminate\Queue\Events\JobAttempted` event now exposes the exception object (or `null`) via `$exception`, replacing the previous boolean `$exceptionOccurred` property:

```php
// Laravel <= 12.x
$event->exceptionOccurred;

// Laravel >= 13.x
$event->exception;

```

If you listen for this event, update your listener code accordingly.

<a name="queuebusy-event-property-rename"></a>
#### `QueueBusy` Event Property Rename

**Likelihood Of Impact: Low**

The `Illuminate\Queue\Events\QueueBusy` event property `$connection` has been renamed to `$connectionName` for consistency with other queue events.

If your listeners reference `$connection`, update them to `$connectionName`.

<a name="queue-contract-method-additions"></a>
#### `Queue` Contract Method Additions

**Likelihood Of Impact: Very Low**

The `Illuminate\Contracts\Queue\Queue` contract now includes queue size inspection methods that were previously only declared in docblocks.

If you maintain custom queue driver implementations of this contract, add implementations for:

<div class="content-list" markdown="1">

- `pendingSize`
- `delayedSize`
- `reservedSize`
- `creationTimeOfOldestPendingJob`

</div>

<a name="routing"></a>
### Routing

<a name="domain-route-registration-precedence"></a>
#### Domain Route Registration Precedence

**Likelihood Of Impact: Low**

Routes with an explicit domain are now prioritized before non-domain routes in route matching.

This allows catch-all subdomain routes to behave consistently even when non-domain routes are registered earlier. If your application relied on previous registration precedence between domain and non-domain routes, review route matching behavior.

<a name="session"></a>
### Session

<a name="session-serialization-configuration"></a>
#### Session `serialization` Configuration

**Likelihood Of Impact: Low**

To help prevent PHP deserialization gadget chain attacks, the default application skeleton now sets the session `serialization` option to `json` in the `config/session.php` file.

If you are upgrading an existing application and syncing your configuration files with the Laravel 13 skeleton, updating this value from `php` to `json` will invalidate all active user sessions.

If you wish to seamlessly maintain active sessions during your upgrade, you should ensure this value remains set to `php`. However, if your application does not store PHP objects in the session and you are comfortable requiring your users to re-authenticate, we recommend updating this value to `json` for improved security.

<a name="scheduling"></a>
### Scheduling

<a name="withscheduling-registration-timing"></a>
#### `withScheduling` Registration Timing

**Likelihood Of Impact: Very Low**

Schedules registered via `ApplicationBuilder::withScheduling()` are now deferred until `Schedule` is resolved.

If your application relied on immediate schedule registration timing during bootstrap, you may need to adjust that logic.

<a name="security"></a>
### Security

<a name="request-forgery-protection"></a>
#### Request Forgery Protection

**Likelihood Of Impact: High**

Laravel's CSRF middleware has been renamed from `VerifyCsrfToken` to `PreventRequestForgery`, and now includes request-origin verification using the `Sec-Fetch-Site` header.

`VerifyCsrfToken` and `ValidateCsrfToken` remain as deprecated aliases, but direct references should be updated to `PreventRequestForgery`, especially when excluding middleware in tests or route definitions:

```php
use Illuminate\Foundation\Http\Middleware\PreventRequestForgery;
use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken;

// Laravel <= 12.x
->withoutMiddleware([VerifyCsrfToken::class]);

// Laravel >= 13.x
->withoutMiddleware([PreventRequestForgery::class]);

```

The middleware configuration API now also provides `preventRequestForgery(...)`.

<a name="support"></a>
### Support

<a name="manager-extend-callback-binding"></a>
#### Manager `extend` Callback Binding

**Likelihood Of Impact: Low**

Custom driver closures registered via manager `extend` methods are now bound to the manager instance.

If you previously relied on another bound object (such as a service provider instance) as `$this` inside these callbacks, you should move those values into closure captures using `use (...)`.

<a name="str-factories-reset-between-tests"></a>
#### `Str` Factories Reset Between Tests

**Likelihood Of Impact: Low**

Laravel now resets custom `Str` factories during test teardown.

If your tests depended on custom UUID / ULID / random string factories persisting between test methods, you should set them in each relevant test or setup hook.

<a name="jsfrom-uses-unescaped-unicode-by-default"></a>
#### `Js::from` Uses Unescaped Unicode By Default

**Likelihood Of Impact: Very Low**

`Illuminate\Support\Js::from` now uses `JSON_UNESCAPED_UNICODE` by default.

If your tests or frontend output comparisons depended on escaped Unicode sequences (for example `\u00e8`), update your expectations.

<a name="utilities"></a>
### Utilities

<a name="symfony-polyfill"></a>
#### Symfony PHP 8.5 Polyfill and Global Function Conflicts

**Likelihood Of Impact: Low**

Laravel 13 introduces a dependency on `symfony/polyfill-php85`. On PHP versions below 8.5, this polyfill defines global functions such as `array_first()` and `array_last()` unless they have already been defined earlier during bootstrap.

These functions may conflict with legacy helper packages like `laravel/helpers` or custom global helpers using the same names. For example, the historical `array_first()` helper accepted a callback to return the first matching element, while the polyfilled version only returns the first element of the array.

To avoid conflicts and ensure consistent behavior across PHP versions, you should prefer the `Illuminate\Support\Arr` methods:

```php
use Illuminate\Support\Arr;

Arr::first($array, function ($value) {
  return /* condition */;
});

```

<a name="views"></a>
### Views

<a name="pagination-bootstrap-view-names"></a>
#### Pagination Bootstrap View Names

**Likelihood Of Impact: Low**

The internal pagination view names for Bootstrap 3 defaults are now explicit:

```text
// Laravel <= 12.x
pagination::default
pagination::simple-default

// Laravel >= 13.x
pagination::bootstrap-3
pagination::simple-bootstrap-3

```

If your application references the old pagination view names directly, update those references.

<a name="miscellaneous"></a>
### Miscellaneous

We also encourage you to view the changes in the `laravel/laravel` [GitHub repository](https://github.com/laravel/laravel). While many of these changes are not required, you may wish to keep these files in sync with your application. Some of these changes will be covered in this upgrade guide, but others, such as changes to configuration files or comments, will not be. You can easily view the changes with the [GitHub comparison tool](https://github.com/laravel/laravel/compare/12.x...13.x) and choose which updates are important to you.
{% endraw %}
