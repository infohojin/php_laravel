---
layout: docs
title: "Laravel Pennant"
---

{% raw %}
---
layout: docs
title: "Laravel Pennant"
---

# Laravel Pennant

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Defining Features](#defining-features)
    - [Class Based Features](#class-based-features)
- [Checking Features](#checking-features)
    - [Conditional Execution](#conditional-execution)
    - [The `HasFeatures` Trait](#the-has-features-trait)
    - [Blade Directive](#blade-directive)
    - [Middleware](#middleware)
    - [Intercepting Feature Checks](#intercepting-feature-checks)
    - [In-Memory Cache](#in-memory-cache)
- [Scope](#scope)
    - [Specifying the Scope](#specifying-the-scope)
    - [Global Scope](#global-scope)
    - [Default Scope](#default-scope)
    - [Nullable Scope](#nullable-scope)
    - [Identifying Scope](#identifying-scope)
    - [Serializing Scope](#serializing-scope)
- [Rich Feature Values](#rich-feature-values)
- [Retrieving Multiple Features](#retrieving-multiple-features)
- [Eager Loading](#eager-loading)
- [Updating Values](#updating-values)
    - [Bulk Updates](#bulk-updates)
    - [Purging Features](#purging-features)
- [Testing](#testing)
- [Adding Custom Pennant Drivers](#adding-custom-pennant-drivers)
    - [Implementing the Driver](#implementing-the-driver)
    - [Registering the Driver](#registering-the-driver)
    - [Defining Features Externally](#defining-features-externally)
- [Events](#events)

<a name="introduction"></a>
## Introduction

[Laravel Pennant](https://github.com/laravel/pennant) is a simple and light-weight feature flag package - without the cruft. Feature flags enable you to incrementally roll out new application features with confidence, A/B test new interface designs, complement a trunk-based development strategy, and much more.

<a name="installation"></a>
## Installation

First, install Pennant into your project using the Composer package manager:

```shell
composer require laravel/pennant
```



다음으로, `vendor:publish` Artisan 명령어를 사용하여 Pennant 설정 및 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
```



마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이렇게 하면 Pennant가 `database` 드라이버를 작동시키는 데 사용하는 `features` 테이블이 생성됩니다:

```shell
php artisan migrate
```



<a name="configuration"></a>
## Configuration

After publishing Pennant's assets, its configuration file will be located at `config/pennant.php`. This configuration file allows you to specify the default storage mechanism that will be used by Pennant to store resolved feature flag values.

Pennant includes support for storing resolved feature flag values in an in-memory array via the `array` driver. Or, Pennant can store resolved feature flag values persistently in a relational database via the `database` driver, which is the default storage mechanism used by Pennant.

<a name="defining-features"></a>
## Defining Features

To define a feature, you may use the `define` method offered by the `Feature` facade. You will need to provide a name for the feature, as well as a closure that will be invoked to resolve the feature's initial value.

Typically, features are defined in a service provider using the `Feature` facade. The closure will receive the "scope" for the feature check. Most commonly, the scope is the currently authenticated user. In this example, we will define a feature for incrementally rolling out a new API to our application's users:

```php
<?php

namespace App\Providers;

use App\Models\User;
use Illuminate\Support\Lottery;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::define('new-api', fn (User $user) => match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        });
    }
}
```



As you can see, we have the following rules for our feature:

- All internal team members should be using the new API.
- Any high traffic customers should not be using the new API.
- Otherwise, the feature should be randomly assigned to users with a 1 in 100 chance of being active.

The first time the `new-api` feature is checked for a given user, the result of the closure will be stored by the storage driver. The next time the feature is checked against the same user, the value will be retrieved from storage and the closure will not be invoked.

For convenience, if a feature definition only returns a lottery, you may omit the closure completely:

Feature::define('site-redesign', Lottery::odds(1, 1000));

<a name="class-based-features"></a>
### Class Based Features

Pennant also allows you to define class-based features. Unlike closure-based feature definitions, there is no need to register a class-based feature in a service provider. To create a class-based feature, you may invoke the `pennant:feature` Artisan command. By default, the feature class will be placed in your application's `app/Features` directory:

```shell
php artisan pennant:feature NewApi
```



피처 클래스를 작성할 때는 `resolve` 메서드만 정의하면 되며, 이 메서드는 주어진 범위에 대한 피처의 초기 값을 해결하기 위해 호출됩니다. 다시 말하지만, 범위는 일반적으로 현재 인증된 사용자가 됩니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```



클래스 기반 기능의 인스턴스를 수동으로 해결하려는 경우, `Feature` 퍼사드에서 `instance` 메서드를 호출할 수 있습니다:

```php
use App\Features\NewApi;
use Laravel\Pennant\Feature;

$instance = Feature::instance(NewApi::class);
```



> [!NOTE]
> 기능 클래스는 [컨테이너](/docs/{{version}}/container)를 통해 해결되므로, 필요할 경우 기능 클래스의 생성자에 의존성을 주입할 수 있습니다.

#### 저장된 기능 이름 사용자 지정

기본적으로 Pennant는 기능 클래스의 완전한 클래스 이름을 저장합니다. 저장된 기능 이름을 애플리케이션의 내부 구조와 분리하고 싶다면, 기능 클래스에 `Name` 속성을 추가할 수 있습니다. 이 속성의 값이 클래스 이름 대신 저장됩니다:

```php
<?php

namespace App\Features;

use Laravel\Pennant\Attributes\Name;

#[Name('new-api')]
class NewApi
{
    // ...
}
```



<a name="checking-features"></a>
## 기능 확인

기능이 활성 상태인지 확인하려면 `Feature` 퍼사드에서 `active` 메서드를 사용할 수 있습니다. 기본적으로 기능은 현재 인증된 사용자에 대해 확인됩니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active('new-api')
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```



기능은 기본적으로 현재 인증된 사용자를 기준으로 확인되지만, 다른 사용자나 [범위](#scope)에 대해 기능을 쉽게 확인할 수 있습니다. 이를 수행하려면 `Feature` 파사드에서 제공하는 `for` 메서드를 사용하세요:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```



Pennant는 또한 기능이 활성화되어 있는지 여부를 확인할 때 유용할 수 있는 몇 가지 추가 편의 메서드를 제공합니다:

```php
// Determine if all of the given features are active...
Feature::allAreActive(['new-api', 'site-redesign']);

// Determine if any of the given features are active...
Feature::someAreActive(['new-api', 'site-redesign']);

// Determine if a feature is inactive...
Feature::inactive('new-api');

// Determine if all of the given features are inactive...
Feature::allAreInactive(['new-api', 'site-redesign']);

// Determine if any of the given features are inactive...
Feature::someAreInactive(['new-api', 'site-redesign']);
```



> [!NOTE]
> Pennant을 Artisan 명령어나 대기열 작업과 같이 HTTP 컨텍스트 외부에서 사용할 때는 일반적으로 [특성의 범위를 명시적으로 지정](#specifying-the-scope)해야 합니다. 또는 인증된 HTTP 컨텍스트와 비인증 컨텍스트를 모두 고려하는 [기본 범위](#default-scope)를 정의할 수도 있습니다.

<a name="checking-class-based-features"></a>
#### 클래스 기반 기능 확인

클래스 기반 기능의 경우, 기능을 확인할 때 클래스 이름을 제공해야 합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::active(NewApi::class)
            ? $this->resolveNewApiResponse($request)
            : $this->resolveLegacyApiResponse($request);
    }

    // ...
}
```



<a name="conditional-execution"></a>
### 조건부 실행

`when` 메서드는 기능이 활성화된 경우 주어진 클로저를 유창하게 실행하는 데 사용할 수 있습니다. 또한 두 번째 클로저를 제공할 수 있으며, 기능이 비활성화된 경우 실행됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Features\NewApi;
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Feature;

class PodcastController
{
    /**
     * Display a listing of the resource.
     */
    public function index(Request $request): Response
    {
        return Feature::when(NewApi::class,
            fn () => $this->resolveNewApiResponse($request),
            fn () => $this->resolveLegacyApiResponse($request),
        );
    }

    // ...
}
```



`unless` 방법은 `when` 방법의 역으로 작용하며, 해당 기능이 비활성화된 경우 첫 번째 클로저를 실행합니다:

```php
return Feature::unless(NewApi::class,
    fn () => $this->resolveLegacyApiResponse($request),
    fn () => $this->resolveNewApiResponse($request),
);
```



<a name="the-has-features-trait"></a>
### `HasFeatures` 특성

Pennant의 `HasFeatures` 특성은 애플리케이션의 `User` 모델(또는 기능이 있는 다른 모델)에 추가하여 모델에서 직접 기능을 편리하고 자연스럽게 확인할 수 있는 방법을 제공할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Pennant\Concerns\HasFeatures;

class User extends Authenticatable
{
    use HasFeatures;

    // ...
}
```



특성이 모델에 추가되면 `features` 메서드를 호출하여 기능을 쉽게 확인할 수 있습니다:

```php
if ($user->features()->active('new-api')) {
    // ...
}
```



물론, `features` 방법은 기능과 상호작용할 수 있는 다른 많은 편리한 방법에 접근할 수 있도록 제공합니다:

```php
// Values...
$value = $user->features()->value('purchase-button')
$values = $user->features()->values(['new-api', 'purchase-button']);

// State...
$user->features()->active('new-api');
$user->features()->allAreActive(['new-api', 'server-api']);
$user->features()->someAreActive(['new-api', 'server-api']);

$user->features()->inactive('new-api');
$user->features()->allAreInactive(['new-api', 'server-api']);
$user->features()->someAreInactive(['new-api', 'server-api']);

// Conditional execution...
$user->features()->when('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);

$user->features()->unless('new-api',
    fn () => /* ... */,
    fn () => /* ... */,
);
```



<a name="blade-directive"></a>
### 블레이드 지시문

블레이드에서 기능을 확인하는 경험을 원활하게 하기 위해, Pennant는 `@feature`와 `@featureany` 지시문을 제공합니다:

```blade
@feature('site-redesign')
    <!-- 'site-redesign' is active -->
@else
    <!-- 'site-redesign' is inactive -->
@endfeature

@featureany(['site-redesign', 'beta'])
    <!-- 'site-redesign' or `beta` is active -->
@endfeatureany
```



<a name="middleware"></a>
### 미들웨어

Pennant는 또한 [미들웨어](/docs/{{version}}/middleware)를 포함하고 있으며, 이를 사용하면 현재 인증된 사용자가 라우트가 호출되기 전에 특정 기능에 접근할 권한이 있는지 확인할 수 있습니다. 미들웨어를 라우트에 할당하고 해당 라우트에 접근하기 위해 필요한 기능을 지정할 수 있습니다. 지정된 기능 중 현재 인증된 사용자에 대해 비활성화된 것이 있는 경우, 라우트에서 `400 Bad Request` HTTP 응답이 반환됩니다. 여러 기능을 정적 `using` 메서드에 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Route;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

Route::get('/api/servers', function () {
    // ...
})->middleware(EnsureFeaturesAreActive::using('new-api', 'servers-api'));
```



<a name="customizing-the-response"></a>
#### 응답 맞춤 설정

나열된 기능 중 하나가 비활성화되어 있을 때 미들웨어가 반환하는 응답을 맞춤 설정하고 싶다면, `EnsureFeaturesAreActive` 미들웨어에서 제공하는 `whenInactive` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 서비스 제공자 중 하나의 `boot` 메서드 내에서 호출해야 합니다:

```php
use Illuminate\Http\Request;
use Illuminate\Http\Response;
use Laravel\Pennant\Middleware\EnsureFeaturesAreActive;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    EnsureFeaturesAreActive::whenInactive(
        function (Request $request, array $features) {
            return new Response(status: 403);
        }
    );

    // ...
}
```



<a name="intercepting-feature-checks"></a>
### 기능 검사 가로채기

때때로 특정 기능의 저장된 값을 가져오기 전에 메모리 내에서 일부 검사를 수행하는 것이 유용할 수 있습니다. 기능 플래그 뒤에 새로운 API를 개발하고 있으며, 저장소에 있는 해결된 기능 값을 잃지 않고 새로운 API를 비활성화할 수 있는 기능이 필요하다고 상상해 보세요. 새로운 API에서 버그를 발견하면 내부 팀 구성원을 제외한 모든 사용자에 대해 쉽게 비활성화하고, 버그를 수정한 후 이전에 기능에 접근할 수 있었던 사용자들에게 새로운 API를 다시 활성화할 수 있습니다.

이는 [클래스 기반 기능의](#class-based-features) `before` 메서드를 사용하여 달성할 수 있습니다. 해당 메서드가 있을 경우, `before` 메서드는 항상 저장소에서 값을 가져오기 전에 메모리 내에서 실행됩니다. 메서드에서 `null`가 아닌 값이 반환되면, 요청 동안 기능의 저장된 값을 대신하여 사용됩니다:

```php
<?php

namespace App\Features;

use App\Models\User;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Lottery;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }
    }

    /**
     * Resolve the feature's initial value.
     */
    public function resolve(User $user): mixed
    {
        return match (true) {
            $user->isInternalTeamMember() => true,
            $user->isHighTrafficCustomer() => false,
            default => Lottery::odds(1 / 100),
        };
    }
}
```



이 기능을 사용하여 이전에 기능 플래그 뒤에 있었던 기능의 글로벌 롤아웃을 일정에 맞춰 예약할 수도 있습니다:

```php
<?php

namespace App\Features;

use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Config;

class NewApi
{
    /**
     * Run an always-in-memory check before the stored value is retrieved.
     */
    public function before(User $user): mixed
    {
        if (Config::get('features.new-api.disabled')) {
            return $user->isInternalTeamMember();
        }

        if (Carbon::parse(Config::get('features.new-api.rollout-date'))->isPast()) {
            return true;
        }
    }

    // ...
}
```



<a name="in-memory-cache"></a>
### 메모리 내 캐시

기능을 확인할 때, Pennant는 결과의 메모리 내 캐시를 생성합니다. `database` 드라이버를 사용하는 경우, 이는 동일한 요청 내에서 동일한 기능 플래그를 다시 확인해도 추가 데이터베이스 쿼리가 발생하지 않음을 의미합니다. 또한 이는 요청이 지속되는 동안 기능이 일관된 결과를 가지도록 보장합니다.

메모리 내 캐시를 수동으로 초기화해야 하는 경우, `Feature` 퍼사드가 제공하는 `flushCache` 메서드를 사용할 수 있습니다:

```php
Feature::flushCache();
```



<a name="scope"></a>
## 범위

<a name="specifying-the-scope"></a>
### 범위 지정

논의된 바와 같이, 기능은 일반적으로 현재 인증된 사용자에 대해 확인됩니다. 그러나 이것이 항상 귀하의 필요에 맞는 것은 아닐 수 있습니다. 따라서 `Feature` 파사드의 `for` 메서드를 통해 특정 기능을 확인하고자 하는 범위를 지정할 수 있습니다:

```php
return Feature::for($user)->active('new-api')
    ? $this->resolveNewApiResponse($request)
    : $this->resolveLegacyApiResponse($request);
```



물론, 기능 범위는 '사용자'에 국한되지 않습니다. 전체 팀에 개별 사용자가 아닌 새 청구 경험을 도입한다고 상상해 보세요. 아마도 가장 오래된 팀이 새로운 팀보다 더 느린 롤아웃을 하기를 원할 수 있습니다. 기능 해결 종료는 다음과 비슷하게 보일 수 있습니다:

```php
use App\Models\Team;
use Illuminate\Support\Carbon;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('billing-v2', function (Team $team) {
    if ($team->created_at->isAfter(new Carbon('1st Jan, 2023'))) {
        return true;
    }

    if ($team->created_at->isAfter(new Carbon('1st Jan, 2019'))) {
        return Lottery::odds(1 / 100);
    }

    return Lottery::odds(1 / 1000);
});
```



정의한 클로저가 `User`를 기대하지 않고 대신 `Team` 모델을 기대하고 있다는 것을 알게 될 것입니다. 사용자의 팀에 대해 이 기능이 활성화되어 있는지 확인하려면 `Feature` 파사드에서 제공하는 `for` 메서드에 팀을 전달해야 합니다:

```php
if (Feature::for($user->team)->active('billing-v2')) {
    return redirect('/billing/v2');
}

// ...
```



<a name="global-scope"></a>
### 전역 범위

구성된 기본 범위 해결자와 상관없이 전역 범위를 사용하여 기능을 확인하거나 상호작용하려면 `globally` 메서드를 사용하세요. 이는 일시적으로 유지보수 동작을 활성화하거나 모든 사용자에게 기능을 롤아웃하는 것과 같은 애플리케이션 전체 기능 플래그에 유용합니다:

```php
Feature::globally()->active('new-api');

Feature::globally()->activate('new-api');
```



<a name="default-scope"></a>
### 기본 범위

Pennant가 기능을 확인할 때 사용하는 기본 범위를 사용자 정의할 수도 있습니다. 예를 들어, 모든 기능을 현재 인증된 사용자가 아닌 사용자의 팀을 기준으로 확인할 수 있습니다. 기능을 확인할 때마다 `Feature::for($user->team)`를 호출하는 대신 팀을 기본 범위로 지정할 수 있습니다. 일반적으로 이러한 설정은 애플리케이션의 서비스 제공자 중 하나에서 수행해야 합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Auth;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::resolveScopeUsing(fn ($driver) => Auth::user()?->team);

        // ...
    }
}
```



`for` 메서드를 통해 명시적으로 범위가 제공되지 않으면, 기능 검사는 이제 현재 인증된 사용자의 팀을 기본 범위로 사용합니다:

```php
Feature::active('billing-v2');

// Is now equivalent to...

Feature::for($user->team)->active('billing-v2');
```



<a name="nullable-scope"></a>
### 널러블 범위

특성을 확인할 때 제공하는 범위가 `null`이고, 특성 정의가 널러블 타입을 통해 또는 유니언 타입에 `null`를 포함하여 `null`를 지원하지 않으면, Pennant는 자동으로 특성의 결과 값으로 `false`를 반환합니다.

따라서, 특성에 전달하는 범위가 잠재적으로 `null`일 수 있고, 특성의 값 해결자가 호출되기를 원한다면, 이를 특성 정의에서 고려해야 합니다. Artisan 명령, 대기열 작업 또는 인증되지 않은 경로 내에서 특성을 확인할 경우 `null` 범위가 발생할 수 있습니다. 이러한 컨텍스트에서는 일반적으로 인증된 사용자가 없기 때문에 기본 범위는 `null`가 됩니다.

[특성 범위를 명시적으로 지정](#specifying-the-scope)하지 않는 경우, 범위의 타입을 "널러블"로 설정하고 특성 정의 로직 내에서 `null` 범위 값을 처리해야 합니다:

```php
use App\Models\User;
use Illuminate\Support\Lottery;
use Laravel\Pennant\Feature;

Feature::define('new-api', fn (User $user) => match (true) {// [tl! remove]
Feature::define('new-api', fn (User|null $user) => match (true) {// [tl! add]
    $user === null => true,// [tl! add]
    $user->isInternalTeamMember() => true,
    $user->isHighTrafficCustomer() => false,
    default => Lottery::odds(1 / 100),
});
```



<a name="identifying-scope"></a>
### Identifying Scope

Pennant's built-in `array` and `database` storage drivers know how to properly store scope identifiers for all PHP data types as well as Eloquent models. However, if your application utilizes a third-party Pennant driver, that driver may not know how to properly store an identifier for an Eloquent model or other custom types in your application.

In light of this, Pennant allows you to format scope values for storage by implementing the `FeatureScopeable` contract on the objects in your application that are used as Pennant scopes.

For example, imagine you are using two different feature drivers in a single application: the built-in `database` driver and a third-party "Flag Rocket" driver. The "Flag Rocket" driver does not know how to properly store an Eloquent model. Instead, it requires a `FlagRocketUser` instance. By implementing the `toFeatureIdentifier` defined by the `FeatureScopeable` contract, we can customize the storable scope value provided to each driver used by our application:

```php
<?php

namespace App\Models;

use FlagRocket\FlagRocketUser;
use Illuminate\Database\Eloquent\Model;
use Laravel\Pennant\Contracts\FeatureScopeable;

class User extends Model implements FeatureScopeable
{
    /**
     * Cast the object to a feature scope identifier for the given driver.
     */
    public function toFeatureIdentifier(string $driver): mixed
    {
        return match($driver) {
            'database' => $this,
            'flag-rocket' => FlagRocketUser::fromId($this->flag_rocket_id),
        };
    }
}
```



<a name="serializing-scope"></a>
### 범위 직렬화

기본적으로 Pennant는 Eloquent 모델과 연결된 기능을 저장할 때 완전한 클래스 이름을 사용합니다. 이미 [Eloquent morph 맵](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types)을 사용하고 있다면, Pennant가 morph 맵을 사용하여 저장된 기능을 애플리케이션 구조와 분리하도록 선택할 수 있습니다.

이를 달성하려면 서비스 프로바이더에서 Eloquent morph 맵을 정의한 후, `Feature` 페이사드의 `useMorphMap` 메서드를 호출하면 됩니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;
use Laravel\Pennant\Feature;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);

Feature::useMorphMap();
```



<a name="rich-feature-values"></a>
## 풍부한 기능 값

지금까지 우리는 주로 기능을 이진 상태로 보여주었는데, 이는 기능이 '활성' 또는 '비활성' 상태라는 것을 의미합니다. 하지만 Pennant는 풍부한 값도 저장할 수 있습니다.

예를 들어, 애플리케이션의 '지금 구매' 버튼에 대해 세 가지 새로운 색상을 테스트한다고 가정해 보겠습니다. 기능 정의에서 `true` 또는 `false`을 반환하는 대신, 문자열을 반환할 수 있습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn (User $user) => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```



`value` 메서드를 사용하여 `purchase-button` 기능의 값을 가져올 수 있습니다:

```php
$color = Feature::value('purchase-button');
```



Pennant에 포함된 Blade 지시문은 현재 기능 값에 따라 콘텐츠를 조건부로 렌더링하는 것도 쉽게 만듭니다:

```blade
@feature('purchase-button', 'blue-sapphire')
    <!-- 'blue-sapphire' is active -->
@elsefeature('purchase-button', 'seafoam-green')
    <!-- 'seafoam-green' is active -->
@elsefeature('purchase-button', 'tart-orange')
    <!-- 'tart-orange' is active -->
@endfeature
```



> [!NOTE]
> 풍부한 값을 사용할 때, 기능이 `false`이 아닌 다른 값을 가지고 있을 때 '활성' 상태로 간주된다는 것을 아는 것이 중요합니다.

[조건부 `when`](#conditional-execution) 메서드를 호출할 때, 기능의 풍부한 값이 첫 번째 클로저에 제공됩니다:

```php
Feature::when('purchase-button',
    fn ($color) => /* ... */,
    fn () => /* ... */,
);
```



마찬가지로, 조건부 `unless` 메서드를 호출할 때, 특성의 풍부한 값이 선택적인 두 번째 클로저에 제공됩니다:

```php
Feature::unless('purchase-button',
    fn () => /* ... */,
    fn ($color) => /* ... */,
);
```



<a name="retrieving-multiple-features"></a>
## 여러 기능 가져오기

`values` 메서드는 주어진 범위에 대한 여러 기능을 가져올 수 있게 합니다:

```php
Feature::values(['billing-v2', 'purchase-button']);

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
// ]
```



또는 `all` 방법을 사용하여 특정 범위에 대해 정의된 모든 기능의 값을 검색할 수 있습니다:

```php
Feature::all();

// [
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```



그러나 클래스 기반 기능은 동적으로 등록되며, 명시적으로 확인될 때까지 Pennant에서는 알 수 없습니다. 이는 현재 요청 동안 아직 확인되지 않은 경우, 애플리케이션의 클래스 기반 기능이 `all` 메서드가 반환하는 결과에 나타나지 않을 수 있음을 의미합니다.

`all` 메서드를 사용할 때 항상 기능 클래스가 포함되도록 하려면 Pennant의 기능 발견 기능을 사용할 수 있습니다. 시작하려면 애플리케이션의 서비스 제공자 중 하나에서 `discover` 메서드를 호출하십시오:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::discover();

        // ...
    }
}
```



`discover` 메서드는 애플리케이션의 `app/Features` 디렉토리에 있는 모든 기능 클래스를 등록할 것입니다. `all` 메서드는 현재 요청 중에 확인되었는지 여부와 상관없이 이제 이러한 클래스를 결과에 포함할 것입니다:

```php
Feature::all();

// [
//     'App\Features\NewApi' => true,
//     'billing-v2' => false,
//     'purchase-button' => 'blue-sapphire',
//     'site-redesign' => true,
// ]
```



<a name="eager-loading"></a>
## 미리 로딩(Eager Loading)

Pennant은 단일 요청에 대해 모든 해결된 기능의 메모리 내 캐시를 유지하지만, 여전히 성능 문제가 발생할 수 있습니다. 이를 완화하기 위해 Pennant은 기능 값을 미리 로딩할 수 있는 기능을 제공합니다.

이를 설명하기 위해, 루프 내에서 기능이 활성화되어 있는지 확인한다고 가정해 보겠습니다:

```php
use Laravel\Pennant\Feature;

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```



데이터베이스 드라이버를 사용한다고 가정하면, 이 코드는 루프 내의 모든 사용자에 대해 데이터베이스 쿼리를 실행하게 되므로 잠재적으로 수백 개의 쿼리를 실행하게 됩니다. 그러나 Pennant의 `load` 메서드를 사용하면, 사용자 또는 범위의 컬렉션에 대한 기능 값을 미리 로드하여 이러한 잠재적 성능 병목 현상을 제거할 수 있습니다:

```php
Feature::for($users)->load(['notifications-beta']);

foreach ($users as $user) {
    if (Feature::for($user)->active('notifications-beta')) {
        $user->notify(new RegistrationSuccess);
    }
}
```



특징 값을 아직 로드하지 않은 경우에만 로드하려면, `loadMissing` 방법을 사용할 수 있습니다:

```php
Feature::for($users)->loadMissing([
    'new-api',
    'purchase-button',
    'notifications-beta',
]);
```



`loadAll` 방법을 사용하여 정의된 모든 기능을 로드할 수 있습니다:

```php
Feature::for($users)->loadAll();
```



<a name="updating-values"></a>
## 값 업데이트

특성(feature)의 값이 처음으로 결정될 때, 기본 드라이버는 결과를 저장소에 저장합니다. 이는 사용자가 여러 요청에서 일관된 경험을 할 수 있도록 하는 데 자주 필요합니다. 그러나 때때로 특성의 저장된 값을 수동으로 업데이트하고 싶을 때가 있습니다.

이를 수행하기 위해, 특성을 "켬" 또는 "끔"으로 전환하기 위해 `activate` 및 `deactivate` 메서드를 사용할 수 있습니다:

```php
use Laravel\Pennant\Feature;

// Activate the feature for the default scope...
Feature::activate('new-api');

// Deactivate the feature for the given scope...
Feature::for($user->team)->deactivate('billing-v2');
```



`activate` 메서드에 두 번째 인수를 제공하여 기능에 대한 풍부한 값을 수동으로 설정하는 것도 가능합니다:

```php
Feature::activate('purchase-button', 'seafoam-green');
```



펜넌트에게 특정 기능에 대한 저장된 값을 잊도록 지시하려면 `forget` 메서드를 사용할 수 있습니다. 기능이 다시 확인될 때, 펜넌트는 기능 정의에서 해당 기능의 값을 결정합니다:

```php
Feature::forget('purchase-button');
```



<a name="bulk-updates"></a>
### 대량 업데이트

저장된 기능 값을 대량으로 업데이트하려면 `activateForEveryone` 및 `deactivateForEveryone` 메서드를 사용할 수 있습니다.

예를 들어, 이제 `new-api` 기능의 안정성에 대해 확신이 생겼고 결제 흐름에 가장 적합한 `'purchase-button'` 색상을 찾았다면 - 모든 사용자에 대해 저장된 값을 그에 맞게 업데이트할 수 있습니다:

```php
use Laravel\Pennant\Feature;

Feature::activateForEveryone('new-api');

Feature::activateForEveryone('purchase-button', 'seafoam-green');
```



또는 모든 사용자를 위해 기능을 비활성화할 수 있습니다:

```php
Feature::deactivateForEveryone('new-api');
```



> [!NOTE]
> 이것은 Pennant의 저장 드라이버에 의해 저장된 해결된 기능 값만 업데이트합니다. 또한 애플리케이션에서 기능 정의를 업데이트해야 합니다.

<a name="purging-features"></a>
### 기능 삭제

때때로 저장소에서 전체 기능을 삭제하는 것이 유용할 수 있습니다. 이는 일반적으로 애플리케이션에서 기능을 제거했거나 기능 정의에 대한 조정을 모든 사용자에게 적용하려는 경우 필요합니다.

`purge` 메서드를 사용하여 기능에 저장된 모든 값을 제거할 수 있습니다:

```php
// Purging a single feature...
Feature::purge('new-api');

// Purging multiple features...
Feature::purge(['new-api', 'purchase-button']);
```



저장소에서 모든 기능을 제거하려면, 인수 없이 `purge` 메서드를 호출할 수 있습니다:

```php
Feature::purge();
```



애플리케이션 배포 파이프라인의 일부로 기능을 정리하는 것이 유용할 수 있으므로, Pennant에는 제공된 기능을 저장소에서 정리하는 `pennant:purge` Artisan 명령어가 포함되어 있습니다:

```shell
php artisan pennant:purge new-api

php artisan pennant:purge new-api purchase-button
```



지정된 기능 목록에 있는 기능을 _제외한_ 모든 기능을 제거하는 것도 가능합니다. 예를 들어, 모든 기능을 제거하되 저장소에 있는 "new-api" 및 "purchase-button" 기능의 값만 유지하고 싶다고 가정해 보겠습니다. 이를 달성하려면 해당 기능 이름을 `--except` 옵션에 전달하면 됩니다:

```shell
php artisan pennant:purge --except=new-api --except=purchase-button
```



편의를 위해 `pennant:purge` 명령은 `--except-registered` 플래그도 지원합니다. 이 플래그는 서비스 제공자에 명시적으로 등록된 기능을 제외한 모든 기능이 제거되어야 함을 나타냅니다:

```shell
php artisan pennant:purge --except-registered
```



<a name="testing"></a>
## 테스트

기능 플래그와 상호작용하는 코드를 테스트할 때, 테스트에서 기능 플래그가 반환하는 값을 제어하는 가장 쉬운 방법은 단순히 기능을 다시 정의하는 것입니다. 예를 들어, 애플리케이션의 서비스 제공자 중 하나에서 다음과 같은 기능이 정의되어 있다고 가정해 보겠습니다:

```php
use Illuminate\Support\Arr;
use Laravel\Pennant\Feature;

Feature::define('purchase-button', fn () => Arr::random([
    'blue-sapphire',
    'seafoam-green',
    'tart-orange',
]));
```



테스트에서 기능의 반환 값을 수정하려면 테스트 시작 시 기능을 다시 정의할 수 있습니다. 다음 테스트는 서비스 제공자에 여전히 `Arr::random()` 구현이 존재함에도 항상 통과합니다:```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define('purchase-button', 'seafoam-green');

    expect(Feature::value('purchase-button'))->toBe('seafoam-green');
});
```

```php tab=PHPUnit
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define('purchase-button', 'seafoam-green');

    $this->assertSame('seafoam-green', Feature::value('purchase-button'));
}
```



같은 접근 방식을 클래스 기반 기능에도 사용할 수 있습니다:```php tab=Pest
use Laravel\Pennant\Feature;

test('it can control feature values', function () {
    Feature::define(NewApi::class, true);

    expect(Feature::value(NewApi::class))->toBeTrue();
});
```

```php tab=PHPUnit
use App\Features\NewApi;
use Laravel\Pennant\Feature;

public function test_it_can_control_feature_values()
{
    Feature::define(NewApi::class, true);

    $this->assertTrue(Feature::value(NewApi::class));
}
```



만약 당신의 기능이 `Lottery` 인스턴스를 반환한다면, 사용할 수 있는 몇 가지 유용한 [테스트 도구](/docs/{{version}}/helpers#testing-lotteries)가 있습니다.

<a name="store-configuration"></a>
#### 스토어 구성

Pennant가 테스트 동안 사용할 스토어는 애플리케이션의 `phpunit.xml` 파일에서 `PENNANT_STORE` 환경 변수를 정의하여 구성할 수 있습니다:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit colors="true">
    <!-- ... -->
    <php>
        <env name="PENNANT_STORE" value="array"/>
        <!-- ... -->
    </php>
</phpunit>
```



<a name="adding-custom-pennant-drivers"></a>
## 맞춤 펜넌트 드라이버 추가

<a name="implementing-the-driver"></a>
#### 드라이버 구현

펜넌트의 기존 저장 드라이버가 애플리케이션의 요구 사항에 맞지 않는 경우, 직접 저장 드라이버를 작성할 수 있습니다. 맞춤 드라이버는 `Laravel\Pennant\Contracts\Driver` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;

class RedisFeatureDriver implements Driver
{
    public function define(string $feature, callable $resolver): void {}
    public function defined(): array {}
    public function getAll(array $features): array {}
    public function get(string $feature, mixed $scope): mixed {}
    public function set(string $feature, mixed $scope, mixed $value): void {}
    public function setForAllScopes(string $feature, mixed $value): void {}
    public function delete(string $feature, mixed $scope): void {}
    public function purge(array|null $features): void {}
}
```



이제, 우리는 Redis 연결을 사용하여 각 메서드를 구현하기만 하면 됩니다. 각 메서드를 구현하는 방법의 예시는 [Pennant 소스 코드](https://github.com/laravel/pennant/blob/1.x/src/Drivers/DatabaseDriver.php)에서 `Laravel\Pennant\Drivers\DatabaseDriver`를 확인하세요.

> [!NOTE]
> Laravel은 확장 기능을 담을 디렉터리를 내장하고 있지 않습니다. 원하는 위치 어디든 자유롭게 배치할 수 있습니다. 이 예제에서는 `RedisFeatureDriver`를 담기 위해 `Extensions` 디렉터리를 만들었습니다.

<a name="registering-the-driver"></a>
#### 드라이버 등록하기

드라이버를 구현한 후에는 Laravel에 이를 등록할 준비가 된 것입니다. Pennant에 추가 드라이버를 추가하려면, `Feature` 패사드에서 제공하는 `extend` 메서드를 사용할 수 있습니다. 애플리케이션의 [서비스 제공자](/docs/{{version}}/providers) 중 하나의 `boot` 메서드에서 `extend` 메서드를 호출해야 합니다.

```php
<?php

namespace App\Providers;

use App\Extensions\RedisFeatureDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;
use Laravel\Pennant\Feature;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Feature::extend('redis', function (Application $app) {
            return new RedisFeatureDriver($app->make('redis'), $app->make('events'), []);
        });
    }
}
```



드라이버가 등록되면 애플리케이션의 `config/pennant.php` 구성 파일에서 `redis` 드라이버를 사용할 수 있습니다:

```php
'stores' => [

    'redis' => [
        'driver' => 'redis',
        'connection' => null,
    ],

    // ...

],
```



<a name="defining-features-externally"></a>
### 외부에서 기능 정의하기

드라이버가 서드파티 기능 플래그 플랫폼을 감싸는 래퍼라면, 아마도 Pennant의 `Feature::define` 방법을 사용하는 대신 플랫폼에서 기능을 정의하게 될 것입니다. 그렇다면, 맞춤형 드라이버도 `Laravel\Pennant\Contracts\DefinesFeaturesExternally` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\Extensions;

use Laravel\Pennant\Contracts\Driver;
use Laravel\Pennant\Contracts\DefinesFeaturesExternally;

class FeatureFlagServiceDriver implements Driver, DefinesFeaturesExternally
{
    /**
     * Get the features defined for the given scope.
     */
    public function definedFeaturesForScope(mixed $scope): array {}

    /* ... */
}
```



`definedFeaturesForScope` 메서드는 제공된 범위에 대해 정의된 기능 이름 목록을 반환해야 합니다.

<a name="events"></a>
## 이벤트

Pennant는 애플리케이션 전반에서 기능 플래그를 추적할 때 유용할 수 있는 다양한 이벤트를 전송합니다.

### `Laravel\Pennant\Events\FeatureRetrieved`

이 이벤트는 [기능이 확인될 때](#checking-features)마다 전송됩니다. 이 이벤트는 애플리케이션 전반에서 기능 플래그 사용에 대한 메트릭을 생성하고 추적하는 데 유용할 수 있습니다.

### `Laravel\Pennant\Events\FeatureResolved`

이 이벤트는 특정 범위에 대해 기능의 값이 처음으로 확인될 때 전송됩니다.

### `Laravel\Pennant\Events\UnknownFeatureResolved`

이 이벤트는 특정 범위에 대해 알 수 없는 기능이 처음으로 확인될 때 전송됩니다. 이 이벤트를 수신하면 기능 플래그를 제거하려고 했으나 애플리케이션 전반에 걸쳐 의도치 않게 남은 참조가 있는 경우 유용할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnknownFeatureResolved;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::listen(function (UnknownFeatureResolved $event) {
            Log::error("Resolving unknown feature [{$event->feature}].");
        });
    }
}
```



### `Laravel\Pennant\Events\DynamicallyRegisteringFeatureClass`

이 이벤트는 [클래스 기반 기능](#class-based-features)이 요청 중 처음으로 동적으로 확인될 때 발생합니다.

### `Laravel\Pennant\Events\UnexpectedNullScopeEncountered`

이 이벤트는 `null` 범위가 [null을 지원하지 않는](#nullable-scope) 기능 정의에 전달될 때 발생합니다.

이 상황은 정상적으로 처리되며 기능은 `false`를 반환합니다. 그러나 이 기능의 기본 정상 처리 동작을 사용하지 않으려면, 애플리케이션의 `AppServiceProvider`의 `boot` 메소드에서 이 이벤트에 대한 리스너를 등록할 수 있습니다.

```php
use Illuminate\Support\Facades\Log;
use Laravel\Pennant\Events\UnexpectedNullScopeEncountered;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(UnexpectedNullScopeEncountered::class, fn () => abort(500));
}
```

### `Laravel\Pennant\Events\FeatureUpdated`

이 이벤트는 보통 `activate` 또는 `deactivate`를 호출하여 스코프의 기능을 업데이트할 때 발송됩니다.

### `Laravel\Pennant\Events\FeatureUpdatedForAllScopes`

이 이벤트는 보통 `activateForEveryone` 또는 `deactivateForEveryone`를 호출하여 모든 스코프의 기능을 업데이트할 때 발송됩니다.

### `Laravel\Pennant\Events\FeatureDeleted`

이 이벤트는 보통 `forget`를 호출하여 스코프의 기능을 삭제할 때 발송됩니다.

### `Laravel\Pennant\Events\FeaturesPurged`

이 이벤트는 특정 기능을 정리할 때 발송됩니다.

### `Laravel\Pennant\Events\AllFeaturesPurged`

이 이벤트는 모든 기능을 정리할 때 발송됩니다.
{% endraw %}
