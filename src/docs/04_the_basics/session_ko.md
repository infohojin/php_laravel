---
layout: docs
title: "HTTP 세션"
---

{% raw %}
# HTTP 세션

- [소개](#introduction)
- [컨피그레이션](#configuration)
- [드라이버 사전 요구 사항](#driver-prerequisites)
- 세션과 상호작용 (#interacting-with-the-session)
- [데이터 검색](#retrieving-data)
- [저장 데이터](#storing-data)
- [플래시 데이터](#flash-data)
- [삭제 데이터](#deleting-data)
- [세션 ID 재생성](#regenerating-the-session-id)
- [세션 캐시](#session-cache)
- [세션 차단](#session-blocking)
- [맞춤형 세션 드라이버 추가](#adding-custom-session-drivers)
- [드라이버 구현](#implementing-the-driver)
- [드라이버 등록](#registering-the-driver)

<a name="introduction"></a>
## 소개

HTTP 기반 애플리케이션은 상태 비저장이므로， 세션은 여러 요청에 걸쳐 사용자에 대한 정보를 저장하는 방법을 제공합니다. 해당 사용자 정보는 일반적으로 후속 요청에서 액세스할 수 있는 영구 저장소/백엔드에 배치됩니다。

Laravel 은 표현력 있고 통합된 API 를 통해 액세스할 수 있는 다양한 세션 백엔드를 제공합니다. [Memcached](https://memcached.org), [Redis](https://redis.io) 및 데이터베이스와 같은 인기 있는 백엔드에 대한 지원이 포함되어 있습니다。

<a name="configuration"></a>
### 구성

애플리케이션의 세션 구성 파일은 `config/session.php` 에 저장됩니다. 이 파일에서 사용할 수 있는 옵션을 반드시 검토하십시오. 기본적으로 Laravel 은 `database` 세션 드라이버를 사용하도록 구성됩니다。

세션 `driver` 구성 옵션은 각 요청에 대해 세션 데이터가 저장될 위치를 정의합니다. Laravel 에는 다양한 드라이버가 포함되어 있습니다：

<div class="content-list" markdown="1">

- `file` - 세션이 `storage/framework/sessions` 에 저장됩니다。
- `cookie` - 세션은 안전하고 암호화된 쿠키에 저장됩니다。
- `database` - 세션은 관계형 데이터베이스에 저장됩니다。
- `memcached` / `redis` - 세션은 이러한 빠른 캐시 기반 저장소 중 하나에 저장됩니다。
- `dynamodb` - 세션은 AWS DynamoDB 에 저장됩니다。
- `array` - 세션은 PHP 어레이에 저장되며 지속되지 않습니다。

</div>

> [!NOTE]
> 어레이 드라이버는 주로 [테스트] 중에 사용되며 (/docs/{{version}}/testing) 세션에 저장된 데이터가 유지되지 않도록 합니다。

<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="database"></a>
#### 데이터베이스



`database` 세션 드라이버를 사용할 때, 세션 데이터를 저장할 데이터베이스 테이블이 있는지 확인해야 합니다. 일반적으로 이는 Laravel의 기본 `0001_01_01_000000_create_users_table.php` [데이터베이스 마이그레이션](/docs/{{version}}/migrations)에 포함되어 있습니다. 그러나 어떤 이유로든 `sessions` 테이블이 없다면, `make:session-table` Artisan 명령어를 사용하여 이 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:session-table

php artisan migrate

```

<a name="redis"></a>
#### Redis

Laravel에서 Redis 세션을 사용하기 전에, PECL을 통해 PhpRedis PHP 확장을 설치하거나 Composer를 통해 `predis/predis` 패키지를 설치해야 합니다. Redis 구성에 대한 자세한 정보는 Laravel의 [Redis 문서](/docs/{{version}}/redis#configuration)를 참조하십시오.

> [!NOTE]
> 세션 저장에 사용할 Redis 연결을 지정하려면 `SESSION_CONNECTION` 환경 변수 또는 `session.php` 구성 파일의 `connection` 옵션을 사용할 수 있습니다.

<a name="interacting-with-the-session"></a>
## 세션 상호 작용

<a name="retrieving-data"></a>
### 데이터 가져오기

Laravel에서 세션 데이터를 다루는 주요 방법은 두 가지입니다: 글로벌 `session` 헬퍼와 `Request` 인스턴스를 사용하는 방법입니다. 먼저 `Request` 인스턴스를 통해 세션에 접근하는 방법을 살펴보겠습니다. 이는 라우트 클로저나 컨트롤러 메서드에서 타입 힌트를 사용할 수 있습니다. 컨트롤러 메서드 의존성은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 주입된다는 점을 기억하십시오:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(Request $request, string $id): View
    {
        $value = $request->session()->get('key');

        // ...

        $user = $this->users->find($id);

        return view('user.profile', ['user' => $user]);
    }
}

```

세션에서 항목을 가져올 때, 두 번째 인수로 `get` 메서드에 기본값을 전달할 수도 있습니다. 지정된 키가 세션에 존재하지 않으면 이 기본값이 반환됩니다. 만약 요청된 키가 존재하지 않을 경우, `get` 메서드에 기본값으로 클로저를 전달하면 클로저가 실행되고 그 결과가 반환됩니다:

```php
$value = $request->session()->get('key', 'default');

$value = $request->session()->get('key', function () {
    return 'default';
});

```

<a name="the-global-session-helper"></a>
#### 글로벌 세션 도우미

세션에서 데이터를 가져오고 저장하기 위해 글로벌 `session` PHP 함수를 사용할 수도 있습니다. `session` 도우미가 단일 문자열 인수로 호출되면 해당 세션 키의 값이 반환됩니다. 도우미가 키/값 쌍의 배열로 호출되면, 해당 값들이 세션에 저장됩니다:

```php
Route::get('/home', function () {
    // Retrieve a piece of data from the session...
    $value = session('key');

    // Specifying a default value...
    $value = session('key', 'default');

    // Store a piece of data in the session...
    session(['key' => 'value']);
});

```

> [!NOTE]
> HTTP 요청 인스턴스를 통해 세션을 사용하는 것과 전역 `session` 헬퍼를 사용하는 것 사이에는 실제적인 차이가 거의 없습니다. 두 방법 모두 모든 테스트 케이스에서 사용할 수 있는 `assertSessionHas` 메서드를 통해 [테스트 가능](/docs/{{version}}/testing)합니다.

<a name="retrieving-all-session-data"></a>
#### 모든 세션 데이터 가져오기

세션의 모든 데이터를 가져오고 싶다면 `all` 메서드를 사용할 수 있습니다:

```php
$data = $request->session()->all();

```

<a name="retrieving-a-portion-of-the-session-data"></a>
#### 세션 데이터의 일부 가져오기

`only` 및 `except` 메서드는 세션 데이터의 하위 집합을 가져오는 데 사용할 수 있습니다:

```php
$data = $request->session()->only(['username', 'email']);

$data = $request->session()->except(['username', 'email']);

```

<a name="determining-if-an-item-exists-in-the-session"></a>
#### 세션에 항목이 존재하는지 확인하기

세션에 항목이 있는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 항목이 존재하고 `null`가 아닌 경우 `true`를 반환합니다:

```php
if ($request->session()->has('users')) {
    // ...
}

```

세션에 항목이 존재하는지 확인하려면, 값이 `null`일지라도 다음 `exists` 방법을 사용할 수 있습니다:

```php
if ($request->session()->exists('users')) {
    // ...
}

```

세션에 항목이 존재하지 않는지 확인하려면 `missing` 메서드를 사용할 수 있습니다. 항목이 존재하지 않으면 `missing` 메서드는 `true`를 반환합니다:

```php
if ($request->session()->missing('users')) {
    // ...
}

```

<a name="storing-data"></a>
### 데이터 저장

세션에 데이터를 저장하려면 일반적으로 request 인스턴스의 `put` 메서드나 전역 `session` 헬퍼를 사용합니다:

```php
// Via a request instance...
$request->session()->put('key', 'value');

// Via the global "session" helper...
session(['key' => 'value']);

```

<a name="pushing-to-array-session-values"></a>
#### 배열 세션 값에 추가하기

`push` 메서드는 세션 값이 배열일 때 새 값을 배열에 추가하는 데 사용할 수 있습니다. 예를 들어, `user.teams` 키에 팀 이름 배열이 포함되어 있다면, 다음과 같이 배열에 새 값을 추가할 수 있습니다:

```php
$request->session()->push('user.teams', 'developers');

```

<a name="retrieving-deleting-an-item"></a>
#### 항목 가져오기 및 삭제

`pull` 메서드는 한 문장에서 세션에서 항목을 가져오고 삭제합니다:

```php
$value = $request->session()->pull('key', 'default');

```

<a name="incrementing-and-decrementing-session-values"></a>
#### 세션 값 증가 및 감소

세션 데이터에 증가시키거나 감소시키고 싶은 정수가 포함되어 있다면, `increment`와 `decrement` 메서드를 사용할 수 있습니다:

```php
$request->session()->increment('count');

$request->session()->increment('count', $incrementBy = 2);

$request->session()->decrement('count');

$request->session()->decrement('count', $decrementBy = 2);

```

<a name="flash-data"></a>
### 플래시 데이터

때때로 다음 요청을 위해 세션에 항목을 저장하고 싶을 때가 있습니다. `flash` 메서드를 사용하여 그렇게 할 수 있습니다. 이 방법을 사용하여 세션에 저장된 데이터는 즉시 사용 가능하며 다음 HTTP 요청 동안 사용할 수 있습니다. 다음 HTTP 요청 이후에는 플래시 데이터가 삭제됩니다. 플래시 데이터는 주로 단기 상태 메시지에 유용합니다:

```php
$request->session()->flash('status', 'Task was successful!');

```

여러 요청에 걸쳐 플래시 데이터를 유지해야 하는 경우, 모든 플래시 데이터를 추가 요청 동안 유지하는 `reflash` 메서드를 사용할 수 있습니다. 특정 플래시 데이터만 유지해야 하는 경우에는 `keep` 메서드를 사용할 수 있습니다:

```php
$request->session()->reflash();

$request->session()->keep(['username', 'email']);

```

플래시 데이터를 현재 요청에만 유지하려면, `now` 메서드를 사용할 수 있습니다:

```php
$request->session()->now('status', 'Task was successful!');

```

<a name="deleting-data"></a>
### 데이터 삭제

`forget` 메서드는 세션에서 데이터를 제거합니다. 세션의 모든 데이터를 제거하고 싶다면 `flush` 메서드를 사용할 수 있습니다:

```php
// Forget a single key...
$request->session()->forget('name');

// Forget multiple keys...
$request->session()->forget(['name', 'status']);

$request->session()->flush();

```

<a name="regenerating-the-session-id"></a>
### 세션 ID 재생성

세션 ID를 재생성하는 것은 종종 악의적인 사용자가 애플리케이션에서 [세션 고정](https://owasp.org/www-community/attacks/Session_fixation) 공격을 악용하는 것을 방지하기 위해 수행됩니다.

Laravel은 Laravel [애플리케이션 스타터 키트](/docs/{{version}}/starter-kits)나 [Laravel Fortify](/docs/{{version}}/fortify)를 사용하는 경우 인증 중에 세션 ID를 자동으로 재생성합니다. 그러나 수동으로 세션 ID를 재생성해야 하는 경우, `regenerate` 메서드를 사용할 수 있습니다:

```php
$request->session()->regenerate();

```

세션 ID를 재생성하고 한 번의 명령으로 세션의 모든 데이터를 제거해야 하는 경우, `invalidate` 메서드를 사용할 수 있습니다:

```php
$request->session()->invalidate();

```

<a name="session-cache"></a>
## 세션 캐시

Laravel의 세션 캐시는 개별 사용자 세션에 제한된 데이터를 캐시할 수 있는 편리한 방법을 제공합니다. 전역 애플리케이션 캐시와 달리, 세션 캐시 데이터는 세션별로 자동으로 분리되며 세션이 만료되거나 삭제될 때 정리됩니다. 세션 캐시는 `get`, `put`, `remember`, `forget` 등과 같은 익숙한 [Laravel 캐시 메서드](/docs/{{version}}/cache)를 지원하지만, 현재 세션에 한정됩니다.

세션 캐시는 동일한 세션 내에서 여러 요청에 걸쳐 유지하길 원하지만 영구적으로 저장할 필요가 없는 임시 사용자별 데이터를 저장하는 데 적합합니다. 여기에는 폼 데이터, 임시 계산, API 응답 또는 특정 사용자 세션에 연결되어야 하는 기타 일시적 데이터와 같은 항목이 포함됩니다.

세션 캐시는 세션의 `cache` 메서드를 통해 접근할 수 있습니다:

```php
$discount = $request->session()->cache()->get('discount');

$request->session()->cache()->put(
    'discount', 10, now()->plus(minutes: 5)
);

```

Laravel 의 캐시 메서드에 대한 자세한 내용은 [캐시 문서](/docs/{{version}}/cache) 를 참조하십시오。

<a name="session-blocking"></a>
## 세션 차단

> [!WARNING]
> 세션 차단을 사용하려면 애플리케이션에서 [atomic locks](/docs/{{version}}/cache#atomic-locks) 를 지원하는 캐시 드라이버를 사용해야 합니다. 현재 이러한 캐시 드라이버에는 `memcached`, `dynamodb`, `redis`, `mongodb`(공식 `mongodb/laravel-mongodb` 패키지에 포함됨), `database`, `file` 및 `array` 드라이버가 포함됩니다. 또한 `cookie` 세션 드라이버를 사용하지 않을 수도 있습니다。

기본적으로 Laravel 은 동일한 세션을 사용하는 요청을 동시에 실행할 수 있도록 허용합니다. 따라서 예를 들어 JavaScript HTTP 라이브러리를 사용하여 애플리케이션에 대해 두 개의 HTTP 요청을 하면 둘 다 동시에 실행됩니다. 많은 애플리케이션에서 이는 문제가 되지 않습니다. 하지만 세션에 데이터를 쓰는 두 개의 서로 다른 애플리케이션 엔드포인트에 대해 동시에 요청하는 소수의 애플리케이션에서는 세션 데이터 손실이 발생할 수 있습니다。

이를 완화하기 위해 Laravel 은 주어진 세션에 대한 동시 요청을 제한할 수 있는 기능을 제공합니다. 시작하려면 `block` 메서드를 경로 정의에 연결하기만 하면 됩니다. 이 예에서 `/profile` 끝점에 대한 수신 요청은 세션 잠금을 획득합니다. 이 잠금이 유지되는 동안 동일한 세션 ID 를 공유하는 `/profile` 또는 `/order` 끝점에 대한 모든 수신 요청은 첫 번째 요청의 실행이 완료될 때까지 기다렸다가 실행을 계속합니다：

```php
Route::post('/profile', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

Route::post('/order', function () {
    // ...
})->block($lockSeconds = 10, $waitSeconds = 10);

```



`block` 메서드는 두 개의 선택적 인수를 허용합니다. `block` 메서드가 허용하는 첫 번째 인수는 세션 잠금이 해제되기 전에 유지되어야 하는 최대 초 수입니다. 물론 요청이 이 시간 이전에 실행을 완료하면 잠금은 더 일찍 해제됩니다.

`block` 메서드가 허용하는 두 번째 인수는 요청이 세션 잠금을 얻으려고 시도하는 동안 기다려야 하는 초 수입니다. 주어진 초 수 내에 요청이 세션 잠금을 얻지 못하면 `Illuminate\Contracts\Cache\LockTimeoutException`가 발생합니다.

이 인수들이 전달되지 않으면, 잠금은 최대 10초 동안 유지되며 요청은 잠금을 얻기 위해 최대 10초까지 기다립니다:

```php
Route::post('/profile', function () {
    // ...
})->block();

```

<a name="adding-custom-session-drivers"></a>
## 사용자 정의 세션 드라이버 추가

<a name="implementing-the-driver"></a>
### 드라이버 구현

기존의 세션 드라이버가 애플리케이션의 요구에 맞지 않는 경우, Laravel에서는 자체 세션 핸들러를 작성할 수 있습니다. 사용자 정의 세션 드라이버는 PHP의 내장 `SessionHandlerInterface`를 구현해야 합니다. 이 인터페이스는 몇 가지 간단한 메서드만 포함하고 있습니다. 스텁 형태의 MongoDB 구현은 다음과 같습니다:

```php
<?php

namespace App\Extensions;

class MongoSessionHandler implements \SessionHandlerInterface
{
    public function open($savePath, $sessionName) {}
    public function close() {}
    public function read($sessionId) {}
    public function write($sessionId, $data) {}
    public function destroy($sessionId) {}
    public function gc($lifetime) {}
}

```

Laravel 에는 확장 프로그램을 호스팅할 기본 디렉토리가 포함되어 있지 않으므로 원하는 곳에 자유롭게 배치할 수 있습니다. 이 예에서는 `MongoSessionHandler` 를 호스팅할 `Extensions` 디렉토리를 생성했습니다。

이러한 방법들의 목적이 쉽게 이해되지 않기 때문에， 다음은 각 방법의 목적에 대한 개요입니다：

<div class="content-list" markdown="1">

- `open` 메서드는 일반적으로 파일 기반 세션 스토어 시스템에서 사용됩니다. Laravel 에는 `file` 세션 드라이버가 포함되어 있으므로 이 메서드에 아무것도 넣을 필요가 거의 없습니다. 이 메서드를 그냥 비워 둘 수 있습니다。
- `close` 메서드는 `open` 메서드와 마찬가지로 일반적으로 무시할 수도 있습니다. 대부분의 드라이버에서는 필요하지 않습니다。
- `read` 메서드는 주어진 `$sessionId` 와 연결된 세션 데이터의 문자열 버전을 반환해야 합니다. Laravel 이 직접 직렬화를 수행하므로， 드라이버에서 세션 데이터를 검색하거나 저장할 때 직렬화나 기타 인코딩을 수행할 필요가 없습니다。
- `write` 메서드는 `$sessionId` 와 연결된 주어진 `$data` 문자열을 MongoDB 또는 선택한 다른 스토리지 시스템과 같은 영구 스토리지 시스템에 작성해야 합니다. 다시 말하지만， 직렬화는 수행하지 마십시오 - Laravel 이 이미 처리했을 것입니다。
- `destroy` 메서드는 영구 스토리지에서 `$sessionId` 와 연결된 데이터를 제거해야 합니다。
- `gc` 메서드는 UNIX 타임스탬프인 주어진 `$lifetime` 보다 오래된 모든 세션 데이터를 파기해야 합니다. Memcached 및 Redis 와 같은 자동 만료 시스템의 경우 이 메서드를 비워둘 수 있습니다。

</div>

<a name="registering-the-driver"></a>
### 드라이버 등록

드라이버가 구현되면 Laravel 에 등록할 준비가 되었습니다. Laravel 의 세션 백엔드에 추가 드라이버를 추가하려면 `Session` [facade](/docs/{{version}}/facades) 에서 제공하는 `extend` 메서드를 사용할 수 있습니다. [service provider](/docs/{{version}}/providers) 의 `boot` 메서드에서 `extend` 메서드를 호출해야 합니다. 기존 `App\Providers\AppServiceProvider` 에서 이를 수행하거나 완전히 새로운 제공자를 생성할 수 있습니다：

```php
<?php

namespace App\Providers;

use App\Extensions\MongoSessionHandler;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Session;
use Illuminate\Support\ServiceProvider;

class SessionServiceProvider extends ServiceProvider
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
        Session::extend('mongo', function (Application $app) {
            // Return an implementation of SessionHandlerInterface...
            return new MongoSessionHandler;
        });
    }
}

```

세션 드라이버가 등록되면 `SESSION_DRIVER` 환경 변수나 애플리케이션의 `config/session.php` 구성 파일 내에서 `mongo` 드라이버를 애플리케이션의 세션 드라이버로 지정할 수 있습니다.
{% endraw %}
