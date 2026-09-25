---
layout: docs
title: "Service Container"
---

{% raw %}
# Service Container

- [Introduction](#introduction)
    - [Zero Configuration Resolution](#zero-configuration-resolution)
    - [When to Utilize the Container](#when-to-use-the-container)
- [Binding](#binding)
    - [Binding Basics](#binding-basics)
    - [Binding Interfaces to Implementations](#binding-interfaces-to-implementations)
    - [Contextual Binding](#contextual-binding)
    - [Contextual Attributes](#contextual-attributes)
    - [Binding Primitives](#binding-primitives)
    - [Binding Typed Variadics](#binding-typed-variadics)
    - [Tagging](#tagging)
    - [Extending Bindings](#extending-bindings)
- [Resolving](#resolving)
    - [The Make Method](#the-make-method)
    - [Automatic Injection](#automatic-injection)
- [Method Invocation and Injection](#method-invocation-and-injection)
- [Container Events](#container-events)
    - [Rebinding](#rebinding)
- [PSR-11](#psr-11)

<a name="introduction"></a>
## Introduction

The Laravel service container is a powerful tool for managing class dependencies and performing dependency injection. Dependency injection is a fancy phrase that essentially means this: class dependencies are "injected" into the class via the constructor or, in some cases, "setter" methods.

Let's look at a simple example:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;
use Illuminate\View\View;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): View
    {
        return view('podcasts.show', [
            'podcast' => $this->apple->findPodcast($id)
        ]);
    }
}
```



이 예제에서, `PodcastController`는 Apple Music과 같은 데이터 소스에서 팟캐스트를 가져와야 합니다. 따라서 우리는 팟캐스트를 가져올 수 있는 서비스를 **주입**할 것입니다. 서비스가 주입되었기 때문에, 애플리케이션을 테스트할 때 `AppleMusic` 서비스의 모의(Mock) 또는 더미 구현을 쉽게 생성할 수 있습니다.

강력하고 대규모 애플리케이션을 구축하거나 Laravel 코어 자체에 기여하기 위해서는 Laravel 서비스 컨테이너에 대한 깊은 이해가 필수적입니다.

<a name="zero-configuration-resolution"></a>
### 제로 설정 해석

클래스가 의존성이 없거나 다른 구체 클래스(인터페이스가 아닌)에만 의존하는 경우, 컨테이너는 해당 클래스를 어떻게 해석할지 지시할 필요가 없습니다. 예를 들어, 다음 코드를 `routes/web.php` 파일에 넣을 수 있습니다:

```php
<?php

class Service
{
    // ...
}

Route::get('/', function (Service $service) {
    dd($service::class);
});
```



In this example, hitting your application's `/` route will automatically resolve the `Service` class and inject it into your route's handler. This is game changing. It means you can develop your application and take advantage of dependency injection without worrying about bloated configuration files.

Thankfully, many of the classes you will be writing when building a Laravel application automatically receive their dependencies via the container, including [controllers](/docs/{{version}}/controllers), [event listeners](/docs/{{version}}/events), [middleware](/docs/{{version}}/middleware), and more. Additionally, you may type-hint dependencies in the `handle` method of [queued jobs](/docs/{{version}}/queues). Once you taste the power of automatic and zero configuration dependency injection it feels impossible to develop without it.

<a name="when-to-use-the-container"></a>
### When to Utilize the Container

Thanks to zero configuration resolution, you will often type-hint dependencies on routes, controllers, event listeners, and elsewhere without ever manually interacting with the container. For example, you might type-hint the `Illuminate\Http\Request` object on your route definition so that you can easily access the current request. Even though we never have to interact with the container to write this code, it is managing the injection of these dependencies behind the scenes:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```



In many cases, thanks to automatic dependency injection and [facades](/docs/{{version}}/facades), you can build Laravel applications without **ever** manually binding or resolving anything from the container. **So, when would you ever manually interact with the container?** Let's examine two situations.

First, if you write a class that implements an interface and you wish to type-hint that interface on a route or class constructor, you must [tell the container how to resolve that interface](#binding-interfaces-to-implementations). Secondly, if you are [writing a Laravel package](/docs/{{version}}/packages) that you plan to share with other Laravel developers, you may need to bind your package's services into the container.

<a name="binding"></a>
## Binding

<a name="binding-basics"></a>
### Binding Basics

<a name="simple-bindings"></a>
#### Simple Bindings

Almost all of your service container bindings will be registered within [service providers](/docs/{{version}}/providers), so most of these examples will demonstrate using the container in that context.

Within a service provider, you always have access to the container via the `$this->app` property. We can register a binding using the `bind` method, passing the class or interface name that we wish to register along with a closure that returns an instance of the class:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```



해당 컨테이너 자체를 리졸버의 인수로 받는다는 점을 참고하세요. 그런 다음 컨테이너를 사용하여 우리가 생성하고 있는 객체의 하위 의존성을 해결할 수 있습니다.

앞서 언급했듯이, 일반적으로 서비스 제공자 내부에서 컨테이너와 상호작용하게 되지만, 서비스 제공자 외부에서 컨테이너와 상호작용하고 싶다면 `App` [파사드](/docs/{{version}}/facades)를 통해 그렇게 할 수 있습니다.

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\App;

App::bind(Transistor::class, function (Application $app) {
    // ...
});
```



주어진 타입에 대해 이미 바인딩이 등록되지 않은 경우에만 `bindIf` 방법을 사용하여 컨테이너 바인딩을 등록할 수 있습니다:

```php
$this->app->bindIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```



편의를 위해 등록하려는 클래스 또는 인터페이스 이름을 별도 인수로 제공하지 않고, 대신 `bind` 메서드에 제공한 클로저의 반환 타입에서 Laravel이 타입을 추론하도록 할 수 있습니다:

```php
App::bind(function (Application $app): Transistor {
    return new Transistor($app->make(PodcastParser::class));
});
```



> [!NOTE]
> 클래스가 어떤 인터페이스에도 의존하지 않는다면, 컨테이너에 클래스를 바인딩할 필요가 없습니다. 컨테이너는 이러한 객체를 어떻게 생성해야 하는지 지시할 필요가 없으며, 리플렉션을 사용하여 자동으로 객체를 해결할 수 있습니다.

<a name="binding-a-singleton"></a>
#### 싱글톤 바인딩

`singleton` 메서드는 컨테이너에 한 번만 해결되어야 하는 클래스나 인터페이스를 바인딩합니다. 싱글톤 바인딩이 해결되면, 이후 컨테이너에 호출될 때 동일한 객체 인스턴스가 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->singleton(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```



주어진 타입에 대해 이미 바인딩이 등록되지 않은 경우에만 싱글톤 컨테이너 바인딩을 등록하기 위해 `singletonIf` 메서드를 사용할 수 있습니다:

```php
$this->app->singletonIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```



<a name="singleton-attribute"></a>
#### 싱글톤 속성

또는 인터페이스나 클래스에 `#[Singleton]` 속성을 표시하여 컨테이너가 한 번만 해결하도록 지시할 수 있습니다:

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Singleton;

#[Singleton]
class Transistor
{
    // ...
}
```



<a name="binding-scoped"></a>
#### 범위 지정 싱글톤 바인딩

`scoped` 메서드는 클래스나 인터페이스를 컨테이너에 바인딩하며, 해당 Laravel 요청/잡 생명주기 내에서 한 번만 해결되어야 합니다. 이 메서드는 `singleton` 메서드와 유사하지만, `scoped` 메서드를 사용하여 등록된 인스턴스는 Laravel 애플리케이션이 새 "생명주기"를 시작할 때마다 플러시됩니다. 예를 들어, [Laravel Octane](/docs/{{version}}/octane) 워커가 새 요청을 처리하거나 Laravel [큐 워커](/docs/{{version}}/queues)가 새 잡을 처리할 때 발생합니다.

```php
use App\Services\Transistor;
use App\Services\PodcastParser;
use Illuminate\Contracts\Foundation\Application;

$this->app->scoped(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```



주어진 타입에 대해 이미 바인딩이 등록되지 않은 경우에만 스코프된 컨테이너 바인딩을 등록하기 위해 `scopedIf` 메서드를 사용할 수 있습니다:

```php
$this->app->scopedIf(Transistor::class, function (Application $app) {
    return new Transistor($app->make(PodcastParser::class));
});
```



<a name="scoped-attribute"></a>
#### 범위 속성

또는 `#[Scoped]` 속성으로 인터페이스나 클래스를 표시하여 컨테이너가 주어진 Laravel 요청/작업 수명 주기 내에서 한 번만 해결되도록 표시할 수 있습니다:

```php
<?php

namespace App\Services;

use Illuminate\Container\Attributes\Scoped;

#[Scoped]
class Transistor
{
    // ...
}
```



<a name="binding-instances"></a>
#### 인스턴스 바인딩

이미 존재하는 객체 인스턴스를 `instance` 메서드를 사용하여 컨테이너에 바인딩할 수도 있습니다. 주어진 인스턴스는 이후 컨테이너에 대한 호출 시 항상 반환됩니다:

```php
use App\Services\Transistor;
use App\Services\PodcastParser;

$service = new Transistor(new PodcastParser);

$this->app->instance(Transistor::class, $service);
```



<a name="binding-interfaces-to-implementations"></a>
### 인터페이스를 구현체에 바인딩하기

서비스 컨테이너의 매우 강력한 기능 중 하나는 인터페이스를 특정 구현체에 바인딩할 수 있는 능력입니다. 예를 들어, `EventPusher` 인터페이스와 `RedisEventPusher` 구현체가 있다고 가정해 봅시다. 이 인터페이스에 대한 `RedisEventPusher` 구현을 코딩한 후, 다음과 같이 서비스 컨테이너에 등록할 수 있습니다:

```php
use App\Contracts\EventPusher;
use App\Services\RedisEventPusher;

$this->app->bind(EventPusher::class, RedisEventPusher::class);
```



이 구문은 클래스가 `EventPusher`의 구현을 필요로 할 때 컨테이너가 `RedisEventPusher`를 주입해야 한다고 컨테이너에 알려줍니다. 이제 컨테이너에 의해 해결되는 클래스의 생성자에서 `EventPusher` 인터페이스를 타입 힌트할 수 있습니다. 컨트롤러, 이벤트 리스너, 미들웨어 및 Laravel 애플리케이션 내의 다양한 다른 유형의 클래스들은 항상 컨테이너를 사용하여 해결된다는 점을 기억하세요:

```php
use App\Contracts\EventPusher;

/**
 * Create a new class instance.
 */
public function __construct(
    protected EventPusher $pusher,
) {}
```



<a name="bind-attribute"></a>
#### 바인드 속성

Laravel은 또한 추가적인 편의를 위해 `Bind` 속성을 제공합니다. 이 속성은 어떤 인터페이스에든 적용할 수 있으며, 해당 인터페이스가 요청될 때 Laravel이 자동으로 주입해야 할 구현체를 지정할 수 있습니다. `Bind` 속성을 사용할 때는 애플리케이션의 서비스 제공자에서 추가적인 서비스 등록을 수행할 필요가 없습니다.

또한, 동일한 인터페이스에 여러 `Bind` 속성을 배치하여 특정 환경 세트에 대해 주입될 다른 구현체를 구성할 수 있습니다:

```php
<?php

namespace App\Contracts;

use App\Services\FakeEventPusher;
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;

#[Bind(RedisEventPusher::class)]
#[Bind(FakeEventPusher::class, environments: ['local', 'testing'])]
interface EventPusher
{
    // ...
}
```



더욱이, [Singleton](#singleton-attribute) 및 [Scoped](#scoped-attribute) 속성은 컨테이너 바인딩이 한 번만 해결되어야 하는지 또는 요청/작업 라이프사이클마다 한 번씩 해결되어야 하는지를 나타내기 위해 적용될 수 있습니다:

```php
use App\Services\RedisEventPusher;
use Illuminate\Container\Attributes\Bind;
use Illuminate\Container\Attributes\Singleton;

#[Bind(RedisEventPusher::class)]
#[Singleton]
interface EventPusher
{
    // ...
}
```



임의 조건에 따라 달라지는 바인딩의 경우 `BindWhen` 속성을 사용할 수 있습니다. 클로저는 컨테이너를 받을 수 있으며 바인딩을 적용해야 할 때 `true`를 반환해야 합니다. `Bind` 및 `BindWhen` 속성은 선언된 순서대로 평가됩니다:

```php
use App\Services\BetaEventPusher;
use Illuminate\Container\Attributes\BindWhen;
use Laravel\Pennant\Feature;

#[BindWhen(BetaEventPusher::class, static fn () => Feature::active('beta-events'))]
interface EventPusher
{
    // ...
}
```



> [!NOTE]
> `BindWhen` 속성은 PHP 8.5 이상을 요구합니다.

<a name="contextual-binding"></a>
### 컨텍스트 바인딩

때때로 동일한 인터페이스를 사용하는 두 개의 클래스가 있지만, 각 클래스에 다른 구현체를 주입하고 싶을 수 있습니다. 예를 들어, 두 개의 컨트롤러가 `Illuminate\Contracts\Filesystem\Filesystem` [계약](/docs/{{version}}/contracts)의 서로 다른 구현에 의존할 수 있습니다. Laravel은 이 동작을 정의하기 위한 간단하고 유창한 인터페이스를 제공합니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\UploadController;
use App\Http\Controllers\VideoController;
use Illuminate\Contracts\Filesystem\Filesystem;
use Illuminate\Support\Facades\Storage;

$this->app->when(PhotoController::class)
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('local');
    });

$this->app->when([VideoController::class, UploadController::class])
    ->needs(Filesystem::class)
    ->give(function () {
        return Storage::disk('s3');
    });
```



<a name="contextual-attributes"></a>
### 컨텍스트 속성

컨텍스트 바인딩은 드라이버 구현이나 구성 값을 주입할 때 자주 사용되기 때문에, Laravel은 서비스 제공자에서 컨텍스트 바인딩을 수동으로 정의하지 않고도 이러한 유형의 값을 주입할 수 있는 다양한 컨텍스트 바인딩 속성을 제공합니다.

예를 들어, `Storage` 속성은 특정 [스토리지 디스크](/docs/{{version}}/filesystem)를 주입하는 데 사용될 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Container\Attributes\Storage;
use Illuminate\Contracts\Filesystem\Filesystem;

class PhotoController extends Controller
{
    public function __construct(
        #[Storage('local')] protected Filesystem $filesystem
    ) {
        // ...
    }
}
```



`Storage` 속성 외에도, Laravel은 `Auth`, `Cache`, `Config`, `Context`, `DB`, `Give`, `Log`, `RequestAttribute`, `RouteParameter` 및 [Tag](#tagging) 속성을 제공합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Contracts\UserRepository;
use App\Models\Organization;
use App\Models\Photo;
use App\Repositories\DatabaseRepository;
use Illuminate\Container\Attributes\Auth;
use Illuminate\Container\Attributes\Cache;
use Illuminate\Container\Attributes\Config;
use Illuminate\Container\Attributes\Context;
use Illuminate\Container\Attributes\DB;
use Illuminate\Container\Attributes\Give;
use Illuminate\Container\Attributes\Log;
use Illuminate\Container\Attributes\RequestAttribute;
use Illuminate\Container\Attributes\RouteParameter;
use Illuminate\Container\Attributes\Tag;
use Illuminate\Contracts\Auth\Guard;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Database\Connection;
use Psr\Log\LoggerInterface;

class PhotoController extends Controller
{
    public function __construct(
        #[Auth('web')] protected Guard $auth,
        #[Cache('redis')] protected Repository $cache,
        #[Config('app.timezone')] protected string $timezone,
        #[Context('uuid')] protected string $uuid,
        #[Context('ulid', hidden: true)] protected string $ulid,
        #[DB('mysql')] protected Connection $connection,
        #[Give(DatabaseRepository::class)] protected UserRepository $users,
        #[Log('daily')] protected LoggerInterface $log,
        #[RequestAttribute('organization')] protected Organization $organization,
        #[RouteParameter] protected Photo $photo,
        #[Tag('reports')] protected iterable $reports,
    ) {
        // ...
    }
}
```



`RouteParameter` 속성은 변수 이름과 일치하는 라우트 매개변수를 해결합니다. 필요한 경우 라우트 매개변수 이름을 명시적으로 지정할 수 있습니다: `#[RouteParameter('photo')]`.

`RequestAttribute` 속성은 현재 요청의 [속성 가방](https://symfony.com/doc/current/components/http_foundation.html#accessing-request-data)에 저장된 키의 값을 해결합니다: `#[RequestAttribute('organization')]`.

또한, Laravel은 주어진 라우트나 클래스에 현재 인증된 사용자를 주입하기 위해 `CurrentUser` 속성을 제공합니다:

```php
use App\Models\User;
use Illuminate\Container\Attributes\CurrentUser;

Route::get('/user', function (#[CurrentUser] User $user) {
    return $user;
})->middleware('auth');
```



<a name="defining-custom-attributes"></a>
#### 사용자 정의 속성 정의

`Illuminate\Contracts\Container\ContextualAttribute` 계약을 구현하여 고유한 컨텍스트 속성을 생성할 수 있습니다. 컨테이너는 속성의 `resolve` 메서드를 호출하며, 이 메서드는 속성을 사용하는 클래스에 주입되어야 하는 값을 해결해야 합니다. 아래 예제에서는 Laravel의 내장 `Config` 속성을 다시 구현할 것입니다:

```php
<?php

namespace App\Attributes;

use Attribute;
use Illuminate\Contracts\Container\Container;
use Illuminate\Contracts\Container\ContextualAttribute;
use ReflectionParameter;

#[Attribute(Attribute::TARGET_PARAMETER)]
class Config implements ContextualAttribute
{
    /**
     * Create a new attribute instance.
     */
    public function __construct(public string $key, public mixed $default = null)
    {
    }

    /**
     * Resolve the configuration value.
     *
     * @param  self  $attribute
     * @param  \Illuminate\Contracts\Container\Container  $container
     * @param  \ReflectionParameter  $parameter
     * @return mixed
     */
    public static function resolve(self $attribute, Container $container, ReflectionParameter $parameter)
    {
        return $container->make('config')->get($attribute->key, $attribute->default);
    }
}
```



<a name="binding-primitives"></a>
### 바인딩 원시값

때때로 어떤 클래스가 몇몇 주입된 클래스를 받을 수 있지만, 정수와 같은 주입된 원시값도 필요할 수 있습니다. 클래스가 필요로 하는 모든 값을 주입하기 위해 컨텍스트 바인딩을 쉽게 사용할 수 있습니다:

```php
use App\Http\Controllers\UserController;

$this->app->when(UserController::class)
    ->needs('$variableName')
    ->give($value);
```



때때로 클래스가 [tagged](#tagging) 인스턴스 배열에 의존할 수 있습니다. `giveTagged` 메서드를 사용하면 모든 컨테이너 바인딩에 해당 태그를 쉽게 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$reports')
    ->giveTagged('reports');
```



애플리케이션의 구성 파일 중 하나에서 값을 주입해야 하는 경우, `giveConfig` 방법을 사용할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs('$timezone')
    ->giveConfig('app.timezone');
```



<a name="binding-typed-variadics"></a>
### 타입이 지정된 가변 인자 바인딩

때때로, 가변 생성자 인자를 사용하여 타입이 지정된 객체 배열을 받는 클래스가 있을 수 있습니다:

```php
<?php

use App\Models\Filter;
use App\Services\Logger;

class Firewall
{
    /**
     * The filter instances.
     *
     * @var array
     */
    protected $filters;

    /**
     * Create a new class instance.
     */
    public function __construct(
        protected Logger $logger,
        Filter ...$filters,
    ) {
        $this->filters = $filters;
    }
}
```



컨텍스트 바인딩을 사용하면 `give` 메서드에 해결된 `Filter` 인스턴스 배열을 반환하는 클로저를 제공하여 이 종속성을 해결할 수 있습니다:

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give(function (Application $app) {
          return [
              $app->make(NullFilter::class),
              $app->make(ProfanityFilter::class),
              $app->make(TooLongFilter::class),
          ];
    });
```



편의를 위해, `Firewall`가 `Filter` 인스턴스를 필요로 할 때 컨테이너가 해결할 클래스 이름 배열만 제공할 수도 있습니다:

```php
$this->app->when(Firewall::class)
    ->needs(Filter::class)
    ->give([
        NullFilter::class,
        ProfanityFilter::class,
        TooLongFilter::class,
    ]);
```



<a name="variadic-tag-dependencies"></a>
#### 가변 태그 종속성

때때로 클래스는 특정 클래스(`Report ...$reports`)로 타입 힌트된 가변 종속성을 가질 수 있습니다. `needs` 및 `giveTagged` 메서드를 사용하면 해당 종속성에 대해 [태그](#tagging)가 지정된 모든 컨테이너 바인딩을 쉽게 주입할 수 있습니다:

```php
$this->app->when(ReportAggregator::class)
    ->needs(Report::class)
    ->giveTagged('reports');
```



<a name="tagging"></a>
### 태깅

때때로 특정 "카테고리"의 바인딩을 모두 해결해야 할 필요가 있을 수 있습니다. 예를 들어, 여러 가지 `Report` 인터페이스 구현 배열을 받는 보고서 분석기를 구축하고 있다고 가정해 보겠습니다. `Report` 구현을 등록한 후에는 `tag` 메서드를 사용하여 태그를 할당할 수 있습니다:

```php
$this->app->bind(CpuReport::class, function () {
    // ...
});

$this->app->bind(MemoryReport::class, function () {
    // ...
});

$this->app->tag([CpuReport::class, MemoryReport::class], 'reports');
```



서비스가 태그되면 컨테이너의 `tagged` 메서드를 통해 모든 서비스를 쉽게 해결할 수 있습니다:

```php
$this->app->bind(ReportAnalyzer::class, function (Application $app) {
    return new ReportAnalyzer($app->tagged('reports'));
});
```



<a name="extending-bindings"></a>
### 바인딩 확장

`extend` 메서드는 해결된 서비스를 수정할 수 있게 해줍니다. 예를 들어 서비스가 해결될 때, 서비스에 장식하거나 구성하기 위해 추가 코드를 실행할 수 있습니다. `extend` 메서드는 두 개의 인수를 받습니다. 확장하려는 서비스 클래스와 수정된 서비스를 반환해야 하는 클로저입니다. 클로저는 해결 중인 서비스와 컨테이너 인스턴스를 받습니다:

```php
$this->app->extend(Service::class, function (Service $service, Application $app) {
    return new DecoratedService($service);
});
```



<a name="resolving"></a>
## 해결

<a name="the-make-method"></a>
### `make` 방법

컨테이너에서 클래스 인스턴스를 해결하려면 `make` 방법을 사용할 수 있습니다. `make` 방법은 해결하려는 클래스 또는 인터페이스의 이름을 받습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->make(Transistor::class);
```



클래스의 일부 의존성을 컨테이너를 통해 해결할 수 없는 경우, `makeWith` 메서드에 연관 배열로 전달하여 주입할 수 있습니다. 예를 들어, `Transistor` 서비스에서 필요한 `$id` 생성자 인수를 수동으로 전달할 수 있습니다:

```php
use App\Services\Transistor;

$transistor = $this->app->makeWith(Transistor::class, ['id' => 1]);
```



`bound` 방법은 클래스나 인터페이스가 컨테이너에서 명시적으로 바인딩되었는지 확인하는 데 사용할 수 있습니다:

```php
if ($this->app->bound(Transistor::class)) {
    // ...
}
```



코드에서 `$app` 변수에 접근할 수 없는 위치에서 서비스 제공자 외부에 있는 경우, 컨테이너에서 클래스 인스턴스를 해결하기 위해 `App` [퍼사드](/docs/{{version}}/facades) 또는 `app` [헬퍼](/docs/{{version}}/helpers#method-app)를 사용할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Support\Facades\App;

$transistor = App::make(Transistor::class);

$transistor = app(Transistor::class);
```



컨테이너에서 해결되고 있는 클래스에 Laravel 컨테이너 인스턴스 자체를 주입하고 싶다면, 클래스의 생성자에서 `Illuminate\Container\Container` 클래스를 타입 힌트할 수 있습니다:

```php
use Illuminate\Container\Container;

/**
 * Create a new class instance.
 */
public function __construct(
    protected Container $container,
) {}
```



<a name="automatic-injection"></a>
### 자동 주입

또는, 그리고 중요하게도, 컨테이너가 해결하는 클래스의 생성자에서 종속성을 타입 힌트할 수 있습니다. 여기에는 [컨트롤러](/docs/{{version}}/controllers), [이벤트 리스너](/docs/{{version}}/events), [미들웨어](/docs/{{version}}/middleware) 등이 포함됩니다. 또한, [큐에 있는 작업](/docs/{{version}}/queues)의 `handle` 메서드에서 종속성을 타입 힌트할 수도 있습니다. 실제로 대부분의 객체는 컨테이너에 의해 이렇게 해결되어야 합니다.

예를 들어, 컨트롤러의 생성자에서 애플리케이션에 정의된 서비스를 타입 힌트할 수 있습니다. 이 서비스는 자동으로 해결되어 클래스에 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Services\AppleMusic;

class PodcastController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected AppleMusic $apple,
    ) {}

    /**
     * Show information about the given podcast.
     */
    public function show(string $id): Podcast
    {
        return $this->apple->findPodcast($id);
    }
}
```



<a name="method-invocation-and-injection"></a>
## 메서드 호출 및 주입

때때로 컨테이너가 해당 메서드의 의존성을 자동으로 주입하도록 허용하면서 객체 인스턴스에서 메서드를 호출하고 싶을 때가 있습니다. 예를 들어, 다음 클래스가 주어졌다고 합시다:

```php
<?php

namespace App;

use App\Services\AppleMusic;

class PodcastStats
{
    /**
     * Generate a new podcast stats report.
     */
    public function generate(AppleMusic $apple): array
    {
        return [
            // ...
        ];
    }
}
```



다음과 같이 컨테이너를 통해 `generate` 메서드를 호출할 수 있습니다:

```php
use App\PodcastStats;
use Illuminate\Support\Facades\App;

$stats = App::call([new PodcastStats, 'generate']);
```



`call` 메서드는 모든 PHP 호출 가능(callable)을 허용합니다. 컨테이너의 `call` 메서드는 클로저를 호출하면서 자동으로 종속성을 주입하는 데에도 사용할 수 있습니다:

```php
use App\Services\AppleMusic;
use Illuminate\Support\Facades\App;

$result = App::call(function (AppleMusic $apple) {
    // ...
});
```



<a name="container-events"></a>
## 컨테이너 이벤트

서비스 컨테이너는 객체를 해결할 때마다 이벤트를 발생시킵니다. 이 이벤트는 `resolving` 메서드를 사용하여 수신할 수 있습니다:

```php
use App\Services\Transistor;
use Illuminate\Contracts\Foundation\Application;

$this->app->resolving(Transistor::class, function (Transistor $transistor, Application $app) {
    // Called when container resolves objects of type "Transistor"...
});

$this->app->resolving(function (mixed $object, Application $app) {
    // Called when container resolves object of any type...
});
```



보시다시피, 해결되는 객체는 콜백으로 전달되며, 이를 통해 객체가 사용자에게 전달되기 전에 추가 속성을 설정할 수 있습니다.

<a name="rebinding"></a>
### 재바인딩

`rebinding` 메서드는 서비스가 컨테이너에 다시 바인딩될 때, 즉 초기 바인딩 후에 다시 등록되거나 덮어쓰여질 때를 감지할 수 있게 해줍니다. 이는 특정 바인딩이 업데이트될 때마다 종속성을 업데이트하거나 동작을 수정해야 할 때 유용할 수 있습니다.

```php
use App\Contracts\PodcastPublisher;
use App\Services\SpotifyPublisher;
use App\Services\TransistorPublisher;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(PodcastPublisher::class, SpotifyPublisher::class);

$this->app->rebinding(
    PodcastPublisher::class,
    function (Application $app, PodcastPublisher $newInstance) {
        //
    },
);

// New binding will trigger rebinding closure...
$this->app->bind(PodcastPublisher::class, TransistorPublisher::class);
```



<a name="psr-11"></a>
## PSR-11

Laravel의 서비스 컨테이너는 [PSR-11](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-11-container.md) 인터페이스를 구현합니다. 따라서 Laravel 컨테이너 인스턴스를 얻기 위해 PSR-11 컨테이너 인터페이스를 타입 힌트할 수 있습니다:

```php
use App\Services\Transistor;
use Psr\Container\ContainerInterface;

Route::get('/', function (ContainerInterface $container) {
    $service = $container->get(Transistor::class);

    // ...
});
```

주어진 식별자를 확인할 수 없는 경우 예외가 발생합니다. 식별자가 한 번도 바인딩되지 않은 경우 예외는 `Psr\Container\NotFoundExceptionInterface`의 인스턴스가 됩니다. 식별자가 바인딩되었지만 확인할 수 없는 경우에는 `Psr\Container\ContainerExceptionInterface`의 인스턴스가 발생합니다.
{% endraw %}
