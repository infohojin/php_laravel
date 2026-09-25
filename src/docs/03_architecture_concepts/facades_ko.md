---
layout: docs
title: "표면"
---

{% raw %}
# 표면

- [소개](#introduction)
- [면을 활용할 때](#when-to-use-facades)
- [Facades vs. Dependency Injection](#facades-vs-dependency-injection)
- [Facades vs. Helper Functions](#facades-vs-helper-functions)
- [Facades 작동 방식](#how-facades-work)
- [Real-Time Facades](#real-time-facades)
- [Facade Class Reference](#facade-class-reference)

<a name="introduction"></a>
## 소개

Laravel 설명서 전체에서 “패시드” 를 통해 Laravel 기능과 상호 작용하는 코드 예제를 볼 수 있습니다. 패시드는 애플리케이션의 [서비스 컨테이너](/docs/{{version}}/container) 에서 사용할 수 있는 클래스에 “정적” 인터페이스를 제공합니다. Laravel 은 거의 모든 Laravel 기능에 대한 액세스를 제공하는 여러 패시드를 제공합니다。

Laravel 페이스는 서비스 컨테이너의 기본 클래스에 대한 “정적 프록시” 역할을 하며， 전통적인 정적 방법보다 더 많은 테스트 가능성과 유연성을 유지하면서도 간결하고 표현력 있는 구문의 이점을 제공합니다. 페이스가 어떻게 작동하는지 완전히 이해하지 못해도 상관없습니다 - 그냥 흐름에 따라 Laravel 에 대한 학습을 계속하세요。

라라벨의 모든 페이스는 `Illuminate\Support\Facades` 네임스페이스에서 정의됩니다. 따라서 다음과 같은 페이스에 쉽게 액세스할 수 있습니다：

```php
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Route;

Route::get('/cache', function () {
    return Cache::get('key');
});

```

라라벨 문서 전반에 걸쳐, 많은 예제들이 프레임워크의 다양한 기능을 보여주기 위해 퍼사드를 사용할 것입니다.

<a name="helper-functions"></a>
#### 도우미 함수

페이사드를 보완하기 위해, Laravel은 일반적인 Laravel 기능과 상호작용을 더욱 쉽게 만들어주는 다양한 전역 '도움 함수(helper functions)'를 제공합니다. 여러분이 상호작용할 수 있는 일반적인 도움 함수로는 `view`, `response`, `url`, `config` 등이 있습니다. Laravel에서 제공하는 각 도움 함수는 해당 기능과 함께 문서화되어 있지만, 전체 목록은 전용 [도움말 문서](/docs/{{version}}/helpers)에서 확인할 수 있습니다.

예를 들어, JSON 응답을 생성하기 위해 `Illuminate\Support\Facades\Response` 파사드를 사용하는 대신, `response` 함수를 간단히 사용할 수 있습니다. 헬퍼 함수는 전역적으로 사용 가능하기 때문에, 이를 사용하기 위해 어떤 클래스도 임포트할 필요가 없습니다:

```php
use Illuminate\Support\Facades\Response;

Route::get('/users', function () {
    return Response::json([
        // ...
    ]);
});

Route::get('/users', function () {
    return response()->json([
        // ...
    ]);
});

```

<a name="when-to-use-facades"></a>
## 표면을 사용할 때

페이스에는 많은 장점이 있습니다. 간결하고 기억하기 쉬운 구문을 제공하여 수동으로 삽입하거나 구성해야 하는 긴 클래스 이름을 기억하지 않고 Laravel 의 기능을 사용할 수 있습니다. 또한 PHP 의 동적 메서드를 고유하게 사용하기 때문에 테스트가 용이합니다。

하지만 패싯을 사용할 때는 주의를 기울여야 합니다. 패싯의 주요 위험은 클래스 “범위 확장” 입니다. 패싯은 사용하기가 매우 쉽고 주입이 필요하지 않기 때문에， 클래스를 계속 성장시키고 하나의 클래스에서 여러 패싯을 사용하는 것이 쉽습니다. 종속성 주입을 사용하면， 이 잠재력은 대형 구성자가 클래스가 너무 크게 성장하고 있다는 시각적 피드백을 제공함으로써 완화됩니다. 따라서 패싯을 사용할 때는， 클래스의 책임 범위가 좁게 유지되도록 클래스의 크기에 특별히 주의하십시오. 클래스가 너무 커지고 있다면， 여러 개의 더 작은 클래스로 분할하는 것을 고려하십시오。

<a name="facades-vs-dependency-injection"></a>
### 가면 vs. 의존성 주사

종속성 주입의 주요 이점 중 하나는 주입된 클래스의 구현을 교체할 수 있는 기능입니다. 이는 모의 또는 스텁을 주입하고 스텁에서 다양한 메서드가 호출되었다고 주장할 수 있기 때문에 테스트 중에 유용합니다。

일반적으로， 정말로 정적인 클래스 메서드를 모방하거나 스텁하는 것은 가능하지 않습니다. 그러나 페이스는 동적 메서드를 사용하여 서비스 컨테이너에서 해결된 객체에 대한 메서드 호출을 프록시하기 때문에， 실제로 주입된 클래스 인스턴스를 테스트하는 것처럼 페이스를 테스트할 수 있습니다. 예를 들어， 다음 경로가 주어진다면：

```php
use Illuminate\Support\Facades\Cache;

Route::get('/cache', function () {
    return Cache::get('key');
});

```

Laravel의 파사드(facade) 테스트 방법을 사용하여, 다음과 같은 테스트를 작성하여 `Cache::get` 메서드가 우리가 예상한 인수로 호출되었는지 확인할 수 있습니다:```php tab=Pest
use Illuminate\Support\Facades\Cache;

test('basic example', function () {
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
});

```

```

php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}

```

<a name="facades-vs-helper-functions"></a>
### 퍼사드와 헬퍼 함수

퍼사드 외에도, Laravel에는 뷰 생성, 이벤트 발생, 작업 디스패치, HTTP 응답 전송과 같은 일반적인 작업을 수행할 수 있는 다양한 "헬퍼" 함수가 포함되어 있습니다. 이러한 헬퍼 함수 중 많은 것들이 해당 퍼사드와 동일한 기능을 수행합니다. 예를 들어, 이 퍼사드 호출과 헬퍼 호출은 동일합니다:

```php
return Illuminate\Support\Facades\View::make('profile');

return view('profile');

```

퍼사드(facade)와 헬퍼(helper) 함수 간에는 실질적인 차이가 전혀 없습니다. 헬퍼 함수를 사용할 때에도 해당 퍼사드와 똑같이 테스트할 수 있습니다. 예를 들어, 다음과 같은 라우트를 고려해보십시오:

```php
Route::get('/cache', function () {
    return cache('key');
});

```



`cache` 헬퍼는 `Cache` 퍼사드에 기반한 클래스에서 `get` 메서드를 호출할 것입니다. 따라서 비록 우리가 헬퍼 함수를 사용하고 있지만, 다음 테스트를 작성하여 메서드가 우리가 기대했던 인수로 호출되었는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

/**
 * A basic functional test example.
 */
public function test_basic_example(): void
{
    Cache::shouldReceive('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/cache');

    $response->assertSee('value');
}

```

<a name="how-facades-work"></a>
## 파사드(Facade)의 동작 방식

Laravel 애플리케이션에서 파사드는 컨테이너의 객체에 접근할 수 있는 클래스를 말합니다. 이를 가능하게 하는 메커니즘은 `Facade` 클래스에 있습니다. Laravel의 파사드와 사용자가 생성하는 모든 커스텀 파사드는 기본 `Illuminate\Support\Facades\Facade` 클래스를 확장하게 됩니다.

`Facade` 기본 클래스는 `__callStatic()` 매직 메소드를 사용하여, 파사드로부터 컨테이너에서 해결된 객체로의 호출을 지연시킵니다. 아래 예제에서, Laravel 캐시 시스템에 호출이 이루어집니다. 이 코드를 보면, `Cache` 클래스에서 정적 `get` 메소드가 호출되는 것으로 생각할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function showProfile(string $id): View
    {
        $user = Cache::get('user:'.$id);

        return view('profile', ['user' => $user]);
    }
}

```

파일 상단 근처에서 `Cache` 파사드를 "임포트"하고 있다는 것을 주목하세요. 이 파사드는 `Illuminate\Contracts\Cache\Factory` 인터페이스의 기본 구현에 접근하기 위한 프록시 역할을 합니다. 우리가 파사드를 사용하여 수행하는 모든 호출은 Laravel의 캐시 서비스의 기본 인스턴스로 전달됩니다.

`Illuminate\Support\Facades\Cache` 클래스를 보면, `get`라는 정적 메서드는 없다는 것을 알 수 있습니다:

```php
class Cache extends Facade
{
    /**
     * Get the registered name of the component.
     */
    protected static function getFacadeAccessor(): string
    {
        return 'cache';
    }
}

```

대신, `Cache` 파사드는 기본 `Facade` 클래스를 확장하고 `getFacadeAccessor()` 메서드를 정의합니다. 이 메서드의 역할은 서비스 컨테이너 바인딩의 이름을 반환하는 것입니다. 사용자가 `Cache` 파사드의 정적 메서드를 참조할 때마다, Laravel은 [서비스 컨테이너](/docs/{{version}}/container)에서 `cache` 바인딩을 해결하고 요청된 메서드(이 경우 `get`)를 해당 객체에 대해 실행합니다.

<a name="real-time-facades"></a>
## 실시간 파사드

실시간 파사드를 사용하면 애플리케이션의 모든 클래스를 마치 파사드인 것처럼 취급할 수 있습니다. 이를 어떻게 사용할 수 있는지 설명하기 위해, 먼저 실시간 파사드를 사용하지 않은 코드 일부를 살펴보겠습니다. 예를 들어, `Podcast` 모델에 `publish` 메서드가 있다고 가정해봅시다. 하지만 팟캐스트를 게시하기 위해서는 `Publisher` 인스턴스를 주입해야 합니다.

```php
<?php

namespace App\Models;

use App\Contracts\Publisher;
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this);
    }
}

```

메서드에 퍼블리셔 구현을 주입하면 주입된 퍼블리셔를 모킹할 수 있기 때문에 메서드를 독립적으로 쉽게 테스트할 수 있습니다. 그러나 `publish` 메서드를 호출할 때마다 항상 퍼블리셔 인스턴스를 전달해야 한다는 점이 필요합니다. 실시간 퍼사드를 사용하면 `Publisher` 인스턴스를 명시적으로 전달하지 않아도 동일한 테스트 가능성을 유지할 수 있습니다. 실시간 퍼사드를 생성하려면, 가져온 클래스의 네임스페이스 앞에 `Facades`를 접두사로 붙이십시오:

```php
<?php

namespace App\Models;

use App\Contracts\Publisher; // [tl! remove]
use Facades\App\Contracts\Publisher; // [tl! add]
use Illuminate\Database\Eloquent\Model;

class Podcast extends Model
{
    /**
     * Publish the podcast.
     */
    public function publish(Publisher $publisher): void // [tl! remove]
    public function publish(): void // [tl! add]
    {
        $this->update(['publishing' => now()]);

        $publisher->publish($this); // [tl! remove]
        Publisher::publish($this); // [tl! add]
    }
}

```

실시간 퍼사드를 사용할 때, 퍼블리셔 구현은 `Facades` 접두사 뒤에 나타나는 인터페이스 또는 클래스 이름 부분을 사용하여 서비스 컨테이너에서 해결됩니다. 테스트할 때, 우리는 Laravel의 내장 퍼사드 테스트 도우미를 사용하여 이 메서드 호출을 모킹할 수 있습니다:```php tab=Pest
<?php

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;

pest()->use(RefreshDatabase::class);

test('podcast can be published', function () {
    $podcast = Podcast::factory()->create();

    Publisher::shouldReceive('publish')->once()->with($podcast);

    $podcast->publish();
});

```

```

php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\Podcast;
use Facades\App\Contracts\Publisher;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PodcastTest extends TestCase
{
    use RefreshDatabase;

    /**
     * A test example.
     */
    public function test_podcast_can_be_published(): void
    {
        $podcast = Podcast::factory()->create();

        Publisher::shouldReceive('publish')->once()->with($podcast);

        $podcast->publish();
    }
}

```

<a name="facade-class-reference"></a>
## 퍼사드 클래스 참조

아래에서는 모든 퍼사드와 해당 기본 클래스를 확인할 수 있습니다. 이는 특정 퍼사드 루트에 대한 API 문서를 빠르게 탐색하는 데 유용한 도구입니다. 적용 가능한 경우 [서비스 컨테이너 바인딩](/docs/{{version}}/container) 키도 포함되어 있습니다.

<div class="overflow-auto">

| 패시드 | 클래스 | 서비스 컨테이너 바인딩 |
| --- | --- | --- |
| 앱 | [Illuminate\Foundation\Application](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Application.html) | `app` |
| 장인 | [Illuminate\Contracts\Console\Kernel](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Console/Kernel.html) | `artisan` |
| 인스턴스 (Auth) | [Illuminate\Contracts\Auth\Guard](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Guard.html) | `auth.driver` |
| Auth | [Illuminate\Auth\AuthManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/AuthManager.html) | `auth` |
| Blade | [Illuminate\View\Compilers\BladeCompiler](https://api.laravel.com/docs/{{version}}/Illuminate/View/Compilers/BladeCompiler.html) | `blade.compiler` |
| 브로드캐스트 (인스턴스) | [Illuminate\Contracts\Broadcasting\Broadcaster](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Broadcaster.html) | &nbsp; |
| 브로드캐스트 | [Illuminate\Contracts\Broadcasting\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Broadcasting/Factory.html) | &nbsp; |
| 버스 | [Illuminate\Contracts\Bus\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Bus/Dispatcher.html) | &nbsp; |
| 캐시 (인스턴스) | [Illuminate\Cache\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/Repository.html) | `cache.store` |
| Cache | [Illuminate\Cache\CacheManager](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/CacheManager.html) | `cache` |
| Cloud | [Illuminate\Foundation\Cloud\CloudManager](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Cloud/CloudManager.html) | &nbsp; |
| Config | [Illuminate\Config\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Config/Repository.html) | `config` |
| 컨텍스트 | [Illuminate\Log\Context\Repository](https://api.laravel.com/docs/{{version}}/Illuminate/Log/Context/Repository.html) | &nbsp; |
| Cookie | [Illuminate\Cookie\CookieJar](https://api.laravel.com/docs/{{version}}/Illuminate/Cookie/CookieJar.html) | `cookie` |
| Crypt | [Illuminate\Encryption\Encrypter](https://api.laravel.com/docs/{{version}}/Illuminate/Encryption/Encrypter.html) | `encrypter` |
| 날짜 | [Illuminate\Support\DateFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Support/DateFactory.html) | `date` |
| DB(인스턴스) | [Illuminate\Database\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Connection.html) | `db.connection` |
DB [Illuminate\Database\DatabaseManager](https://api.laravel.com/docs/{{version}}/Illuminate/Database/DatabaseManager.html) `db`
| 이벤트 | [Illuminate\Events\Dispatcher](https://api.laravel.com/docs/{{version}}/Illuminate/Events/Dispatcher.html) | `events` |
| 예외 (Instance) | [Illuminate\Contracts\Debug\ExceptionHandler](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Debug/ExceptionHandler.html) | &nbsp; |
| 예외 | [Illuminate\Foundation\Exception\Handler](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Exceptions/Handler.html) | &nbsp; |
| 파일 | [Illuminate\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/Filesystem.html) | `files` |
| 게이트 | [Illuminate\Contracts\Auth\Access\Gate](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Auth/Access/Gate.html) | &nbsp; |
| 해시 | [Illuminate\Contracts\Hashing\Hasher](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Hashing/Hasher.html) | `hash` |
| http | [Illuminate\Http\Client\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Client/Factory.html) | &nbsp; |
Lang | [Illuminate\Translation\Translator](https://api.laravel.com/docs/{{version}}/Illuminate/Translation/Translator.html) | `translator` |
| Log | [Illuminate\Log\LogManager](https://api.laravel.com/docs/{{version}}/Illuminate/Log/LogManager.html) | `log` |
| Mail | [Illuminate\Mail\Mailer](https://api.laravel.com/docs/{{version}}/Illuminate/Mail/Mailer.html) | `mailer` |
| 알림 | [Illuminate\Notifications\ChannelManager](https://api.laravel.com/docs/{{version}}/Illuminate/Notifications/ChannelManager.html) | &nbsp; |
| 암호 (인스턴스) | [Illuminate\Auth\Passwords\PasswordBroker](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBroker.html) | `auth.password.broker` |
| Password | [Illuminate\Auth\Passwords\PasswordBrokerManager](https://api.laravel.com/docs/{{version}}/Illuminate/Auth/Passwords/PasswordBrokerManager.html) | `auth.password` |
| 파이프라인 (인스턴스) | [Illuminate\Pipeline\Pipeline](https://api.laravel.com/docs/{{version}}/Illuminate/Pipeline/Pipeline.html) | &nbsp; |
| Process | [Illuminate\Process\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Process/Factory.html) | &nbsp; |
Queue(기본 클래스) | [Illuminate\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/Queue.html) | &nbsp; |
Queue (Instance) | [Illuminate\Contracts\Queue\Queue](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Queue/Queue.html) | `queue.connection` |
Queue [Illuminate\Queue\QueueManager](https://api.laravel.com/docs/{{version}}/Illuminate/Queue/QueueManager.html) `queue`
| RateLimiter | [Illuminate\Cache\RateLimiter](https://api.laravel.com/docs/{{version}}/Illuminate/Cache/RateLimiter.html) | &nbsp; |
| 리디렉션 | [Illuminate\Routing\Redirector](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Redirector.html) | `redirect` |
| Redis(인스턴스) | [Illuminate\Redis\Connections\Connection](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/Connections/Connection.html) | `redis.connection` |
| Redis | [Illuminate\Redis\RedisManager](https://api.laravel.com/docs/{{version}}/Illuminate/Redis/RedisManager.html) | `redis` |
| 요청 | [Illuminate\Http\Request](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Request.html) | `request` |
| 응답 (인스턴스) | [Illuminate\Http\Response](https://api.laravel.com/docs/{{version}}/Illuminate/Http/Response.html) | &nbsp; |
| 응답 | [Illuminate\Contracts\Routing\ResponseFactory](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Routing/ResponseFactory.html) | &nbsp; |
| Route | [Illuminate\Routing\Router](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/Router.html) | `router` |
| 스케줄 | [Illuminate\Console\Scheduling\Schedule](https://api.laravel.com/docs/{{version}}/Illuminate/Console/Scheduling/Schedule.html) | &nbsp; |
| 스키마 | [Illuminate\Database\Schema\Builder](https://api.laravel.com/docs/{{version}}/Illuminate/Database/Schema/Builder.html) | &nbsp; |
| 세션 (인스턴스) | [Illuminate\Session\Store](https://api.laravel.com/docs/{{version}}/Illuminate/Session/Store.html) | `session.store` |
| 세션 | [Illuminate\Session\SessionManager](https://api.laravel.com/docs/{{version}}/Illuminate/Session/SessionManager.html) | `session` |
| 저장소 (인스턴스) | [Illuminate\Contracts\Filesystem\Filesystem](https://api.laravel.com/docs/{{version}}/Illuminate/Contracts/Filesystem/Filesystem.html) | `filesystem.disk` |
| 스토리지 | [Illuminate\Filesystem\FilesystemManager](https://api.laravel.com/docs/{{version}}/Illuminate/Filesystem/FilesystemManager.html) | `filesystem` |
URL [Illuminate\Routing\UrlGenerator](https://api.laravel.com/docs/{{version}}/Illuminate/Routing/UrlGenerator.html) `url`
| 검증자 (인스턴스) | [Illuminate\Validation\Validator](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Validator.html) | &nbsp; |
| 검증자 | [Illuminate\Validation\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/Validation/Factory.html) | `validator` |
| View (Instance) | [Illuminate\View\View](https://api.laravel.com/docs/{{version}}/Illuminate/View/View.html) | &nbsp; |
| View | [Illuminate\View\Factory](https://api.laravel.com/docs/{{version}}/Illuminate/View/Factory.html) | `view` |
| Vite | [Illuminate\Foundation\Vite](https://api.laravel.com/docs/{{version}}/Illuminate/Foundation/Vite.html) | &nbsp; |

</div>
{% endraw %}
