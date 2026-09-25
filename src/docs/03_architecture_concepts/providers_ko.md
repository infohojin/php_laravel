---
layout: docs
title: "서비스 제공업체"
---

{% raw %}
# 서비스 제공업체

- [소개](#introduction)
- [Writing Service Providers](#writing-service-providers)
- The Register Method(#the-register-method)
- 부팅 방법 (#the-boot-method)
- [등록 제공자](#registering-providers)
- [연기된 제공자](#deferred-providers)

<a name="introduction"></a>
## 소개

서비스 제공자는 모든 Laravel 애플리케이션 부트스트랩의 중앙 위치입니다. 자체 애플리케이션과 모든 Laravel 핵심 서비스는 서비스 제공자를 통해 부트스트랩됩니다。

그러나 “부트스트랩” 이란 무엇을 의미합니까？ 일반적으로 서비스 컨테이너 바인딩， 이벤트 리스너， 미들웨어， 심지어 경로 등을 등록하는 것을 의미합니다. 서비스 제공자는 애플리케이션을 구성하는 중앙 위치입니다。

Laravel 은 내부적으로 수십 개의 서비스 제공업체를 사용하여 메일러， 대기열， 캐시 등과 같은 핵심 서비스를 부트스트랩합니다. 이러한 제공업체 중 다수는 “지연된” 제공업체로， 즉 모든 요청에 로드되지 않고 제공하는 서비스가 실제로 필요할 때만 로드됩니다。

모든 사용자 정의 서비스 제공자는 `bootstrap/providers.php` 파일에 등록됩니다. 다음 설명서에서는 자체 서비스 제공자를 작성하고 Laravel 애플리케이션에 등록하는 방법을 알아봅니다。

> [!NOTE]
> Laravel 이 요청을 처리하고 내부적으로 작동하는 방법에 대해 자세히 알아보려면 Laravel [요청 라이프사이클](/docs/{{version}}/lifecycle) 에 대한 설명서를 확인하세요。

<a name="writing-service-providers"></a>
## 쓰기 서비스 제공업체

모든 서비스 제공자는 `Illuminate\Support\ServiceProvider` 클래스를 확장합니다. 대부분의 서비스 제공자에는 `register` 및 `boot` 메서드가 포함되어 있습니다. `register` 메서드 내에서는 사물을 [서비스 컨테이너](/docs/{{version}}/container)** 에만 바인딩해야 합니다. `register` 메서드 내에서 이벤트 리스너， 경로 또는 기타 기능을 등록하려고 시도하지 마십시오。

아티잔 CLI 는 `make:provider` 명령을 통해 새 제공자를 생성할 수 있습니다. Laravel 은 애플리케이션의 `bootstrap/providers.php` 파일에 새 제공자를 자동으로 등록합니다：

```shell
php artisan make:provider RiakServiceProvider

```

<a name="the-register-method"></a>
### 등록 메서드

앞서 언급했듯이, `register` 메서드 내에서는 반드시 [서비스 컨테이너](/docs/{{version}}/container)에만 항목을 바인딩해야 합니다. `register` 메서드 내에서 이벤트 리스너, 라우트 또는 다른 기능을 등록하려고 시도해서는 안 됩니다. 그렇지 않으면 아직 로드되지 않은 서비스 제공자가 제공하는 서비스를 실수로 사용할 수 있습니다.

기본적인 서비스 제공자를 살펴보겠습니다. 서비스 제공자의 어떤 메서드 내에서도 `$app` 속성에 항상 접근할 수 있으며, 이를 통해 서비스 컨테이너에 접근할 수 있습니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection(config('riak'));
        });
    }
}

```

이 서비스 제공자는 `register` 메서드만 정의하며, 해당 메서드를 사용하여 서비스 컨테이너에서 `App\Services\Riak\Connection`의 구현을 정의합니다. Laravel의 서비스 컨테이너에 아직 익숙하지 않다면 [문서](/docs/{{version}}/container)를 확인하세요.

<a name="the-bindings-and-singletons-properties"></a>
#### `bindings` 및 `singletons` 속성

서비스 제공자가 많은 간단한 바인딩을 등록하는 경우, 각 컨테이너 바인딩을 수동으로 등록하는 대신 `bindings` 및 `singletons` 속성을 사용하는 것이 좋습니다. 프레임워크가 서비스 제공자를 로드하면 자동으로 이러한 속성을 확인하고 바인딩을 등록합니다:

```php
<?php

namespace App\Providers;

use App\Contracts\DowntimeNotifier;
use App\Contracts\ServerProvider;
use App\Services\DigitalOceanServerProvider;
use App\Services\PingdomDowntimeNotifier;
use App\Services\ServerToolsProvider;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * All of the container bindings that should be registered.
     *
     * @var array
     */
    public $bindings = [
        ServerProvider::class => DigitalOceanServerProvider::class,
    ];

    /**
     * All of the container singletons that should be registered.
     *
     * @var array
     */
    public $singletons = [
        DowntimeNotifier::class => PingdomDowntimeNotifier::class,
        ServerProvider::class => ServerToolsProvider::class,
    ];
}

```

<a name="the-boot-method"></a>
### 부트 메소드

그렇다면 서비스 제공자 내에서 [뷰 컴포저](/docs/{{version}}/views#view-composers)를 등록해야 한다면 어떻게 할까요? 이는 `boot` 메소드 내에서 수행해야 합니다. **이 메소드는 다른 모든 서비스 제공자가 등록된 후에 호출되므로**, 프레임워크에서 등록된 다른 모든 서비스에 접근할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\View;
use Illuminate\Support\ServiceProvider;

class ComposerServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        View::composer('view', function () {
            // ...
        });
    }
}

```

<a name="boot-method-dependency-injection"></a>
#### 부트 메서드 의존성 주입

서비스 제공자의 `boot` 메서드에 대해 타입 힌트로 의존성을 지정할 수 있습니다. [서비스 컨테이너](/docs/{{version}}/container)가 필요한 모든 의존성을 자동으로 주입합니다:

```php
use Illuminate\Contracts\Routing\ResponseFactory;

/**
 * Bootstrap any application services.
 */
public function boot(ResponseFactory $response): void
{
    $response->macro('serialized', function (mixed $value) {
        // ...
    });
}

```

<a name="registering-providers"></a>
## 공급자 등록

모든 서비스 공급자는 `bootstrap/providers.php` 구성 파일에 등록됩니다. 이 파일은 애플리케이션의 서비스 공급자 클래스 이름을 포함하는 배열을 반환합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
];

```



`make:provider` Artisan 명령을 실행하면 Laravel은 생성된 제공자를 `bootstrap/providers.php` 파일에 자동으로 추가합니다. 그러나 제공자 클래스를 수동으로 생성한 경우에는 제공자 클래스를 배열에 수동으로 추가해야 합니다:

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\ComposerServiceProvider::class, // [tl! add]
];

```

<a name="deferred-providers"></a>
## 지연 제공자

만약 당신의 제공자가 [서비스 컨테이너](/docs/{{version}}/container)에 바인딩만 등록하고 있다면, 등록된 바인딩 중 실제로 필요할 때까지 등록을 지연시키도록 선택할 수 있습니다. 이러한 제공자의 로딩을 지연시키면 매 요청마다 파일 시스템에서 로드되지 않기 때문에 애플리케이션 성능이 향상됩니다.

Laravel은 지연된 서비스 제공자가 제공하는 모든 서비스와 해당 서비스 제공자 클래스의 이름 목록을 컴파일하여 저장합니다. 그런 다음 이러한 서비스 중 하나를 해결하려고 시도할 때만 Laravel이 서비스 제공자를 로드합니다.

제공자의 로딩을 지연시키려면 `\Illuminate\Contracts\Support\DeferrableProvider` 인터페이스를 구현하고 `provides` 메서드를 정의하십시오. `provides` 메서드는 제공자가 등록한 서비스 컨테이너 바인딩을 반환해야 합니다:

```php
<?php

namespace App\Providers;

use App\Services\Riak\Connection;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;

class RiakServiceProvider extends ServiceProvider implements DeferrableProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->singleton(Connection::class, function (Application $app) {
            return new Connection($app['config']['riak']);
        });
    }

    /**
     * Get the services provided by the provider.
     *
     * @return array<int, string>
     */
    public function provides(): array
    {
        return [Connection::class];
    }
}

```
{% endraw %}
