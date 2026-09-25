---
layout: docs
title: "Redis"
---

{% raw %}
# Redis

- [인트로듀션](#introduction)
- [컨피그레이션](#configuration)
- 클러스터 (#clusters)
- 프레디스 (#predis)
- [PhpRedis](#phpredis)
- [Interacting With Redis](#interacting-with-redis)
- [Transactions](#transactions)
- [파이프라인 명령](#pipelining-commands)
- [Pub/Sub](#pubsub)

<a name="introduction"></a>
## 소개

[Redis](https://redis.io) 는 오픈 소스의 고급 키 - 값 저장소입니다. 키에 [string](https://redis.io/docs/latest/develop/data-types/strings/), [hash](https://redis.io/docs/latest/develop/data-types/hashes/), [lists](https://redis.io/docs/latest/develop/data-types/lists/), [sets](https://redis.io/docs/latest/develop/data-types/sets/) 및 [sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/) 가 포함될 수 있기 때문에 종종 데이터 구조 서버라고 불립니다。

Laravel 에서 Redis 를 사용하기 전에 PECL 을 통해 [PhpRedis](https://github.com/phpredis/phpredis) PHP 확장을 설치하고 사용하는 것이 좋습니다. 이 확장은 “사용자 랜드” PHP 패키지에 비해 설치가 더 복잡하지만 Redis 를 많이 사용하는 애플리케이션에서 더 나은 성능을 제공할 수 있습니다. [Laravel Sail](/docs/{{version}}/sail) 를 사용하는 경우， 이 확장은 애플리케이션의 Docker 컨테이너에 이미 설치되어 있습니다。

PhpRedis 확장을 설치할 수 없는 경우 Composer 를 통해 `predis/predis` 패키지를 설치할 수 있습니다. Predis 는 전적으로 PHP 로 작성된 Redis 클라이언트이며 추가 확장이 필요하지 않습니다：

```shell
composer require predis/predis

```

<a name="configuration"></a>
## 구성

`config/database.php` 구성 파일을 통해 애플리케이션의 Redis 설정을 구성할 수 있습니다. 이 파일 내에서 애플리케이션이 사용하는 Redis 서버를 포함하는 `redis` 배열을 볼 수 있습니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_DB', '0'),
    ],

    'cache' => [
        'url' => env('REDIS_URL'),
        'host' => env('REDIS_HOST', '127.0.0.1'),
        'username' => env('REDIS_USERNAME'),
        'password' => env('REDIS_PASSWORD'),
        'port' => env('REDIS_PORT', '6379'),
        'database' => env('REDIS_CACHE_DB', '1'),
    ],

],

```

구성 파일에 정의된 각 Redis 서버는 Redis 연결을 나타내는 단일 URL을 정의하지 않는 한 이름, 호스트 및 포트를 가져야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'default' => [
        'url' => 'tcp://127.0.0.1:6379?database=0',
    ],

    'cache' => [
        'url' => 'tls://user:password@127.0.0.1:6380?database=1',
    ],

],

```

<a name="configuring-the-connection-scheme"></a>
#### 연결 스킴 구성

기본적으로 Redis 클라이언트는 Redis 서버에 연결할 때 `tcp` 스킴을 사용합니다. 그러나 Redis 서버의 구성 배열에서 `scheme` 구성 옵션을 지정하여 TLS / SSL 암호화를 사용할 수 있습니다:

```php
'default' => [
    'scheme' => 'tls',
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
],

```

<a name="clusters"></a>
### 클러스터

애플리케이션이 Redis 서버 클러스터를 사용하고 있는 경우, 이러한 클러스터를 Redis 구성의 `clusters` 키 내에 정의해야 합니다. 이 구성 키는 기본적으로 존재하지 않으므로 애플리케이션의 `config/database.php` 구성 파일 내에서 생성해야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
    ],

    'clusters' => [
        'default' => [
            [
                'url' => env('REDIS_URL'),
                'host' => env('REDIS_HOST', '127.0.0.1'),
                'username' => env('REDIS_USERNAME'),
                'password' => env('REDIS_PASSWORD'),
                'port' => env('REDIS_PORT', '6379'),
                'database' => env('REDIS_DB', '0'),
            ],
        ],
    ],

    // ...
],

```

기본적으로, Laravel은 `options.cluster` 구성 값이 `redis`로 설정되어 있기 때문에 네이티브 Redis 클러스터링을 사용합니다. Redis 클러스터링은 장애 조치를 원활하게 처리하므로 훌륭한 기본 옵션입니다.

Laravel은 또한 Predis를 사용할 때 클라이언트 측 샤딩을 지원합니다. 하지만 클라이언트 측 샤딩은 장애 조치를 처리하지 않으므로 주로 다른 기본 데이터 저장소에서 가져올 수 있는 일시적인 캐시된 데이터에 적합합니다.

네이티브 Redis 클러스터링 대신 클라이언트 측 샤딩을 사용하고 싶다면, 애플리케이션의 `config/database.php` 구성 파일 내에서 `options.cluster` 구성 값을 제거할 수 있습니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'clusters' => [
        // ...
    ],

    // ...
],

```

<a name="predis"></a>
### Predis

애플리케이션이 Predis 패키지를 통해 Redis와 상호작용하기를 원한다면, `REDIS_CLIENT` 환경 변수의 값이 `predis`인지 확인해야 합니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'predis'),

    // ...
],

```

기본 구성 옵션 외에도, Predis는 각 Redis 서버에 대해 정의될 수 있는 추가 [연결 매개변수](https://github.com/nrk/predis/wiki/Connection-Parameters)를 지원합니다. 이러한 추가 구성 옵션을 활용하려면, 애플리케이션의 `config/database.php` 구성 파일에서 Redis 서버 구성에 추가하면 됩니다:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_write_timeout' => 60,
],

```

<a name="phpredis"></a>
### PhpRedis

기본적으로 Laravel은 Redis와 통신하기 위해 PhpRedis 확장을 사용합니다. Laravel이 Redis와 통신할 때 사용할 클라이언트는 일반적으로 `REDIS_CLIENT` 환경 변수의 값을 반영하는 `redis.client` 구성 옵션의 값에 의해 결정됩니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    // ...
],

```

기본 구성 옵션 외에도, PhpRedis는 다음과 같은 추가 연결 매개변수를 지원합니다: `name`, `persistent`, `persistent_id`, `prefix`, `read_timeout`, `retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, `backoff_cap`, `timeout`, 및 `context`. 이러한 옵션 중 어느 것이든 `config/database.php` 구성 파일에서 Redis 서버 구성에 추가할 수 있습니다:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'read_timeout' => 60,
    'context' => [
        // 'auth' => ['username', 'secret'],
        // 'stream' => ['verify_peer' => false],
    ],
],

```

<a name="retry-and-backoff-configuration"></a>
#### 재시도 및 백오프 구성

`retry_interval`, `max_retries`, `backoff_algorithm`, `backoff_base`, 및 `backoff_cap` 옵션은 PhpRedis 클라이언트가 Redis 서버에 재연결을 시도하는 방법을 구성하는 데 사용할 수 있습니다. 다음 백오프 알고리즘이 지원됩니다: `default`, `decorrelated_jitter`, `equal_jitter`, `exponential`, `uniform`, 및 `constant`:

```php
'default' => [
    'url' => env('REDIS_URL'),
    'host' => env('REDIS_HOST', '127.0.0.1'),
    'username' => env('REDIS_USERNAME'),
    'password' => env('REDIS_PASSWORD'),
    'port' => env('REDIS_PORT', '6379'),
    'database' => env('REDIS_DB', '0'),
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
    'backoff_algorithm' => env('REDIS_BACKOFF_ALGORITHM', 'decorrelated_jitter'),
    'backoff_base' => env('REDIS_BACKOFF_BASE', 100),
    'backoff_cap' => env('REDIS_BACKOFF_CAP', 1000),
],

```

Laravel은 일시적인 연결 실패가 발생하면 안전한 읽기 명령을 한 번 자동으로 재시도합니다. 모든 Redis 명령에 대한 재시도 횟수를 구성하려면 `command_retries` 옵션을 사용할 수 있습니다:

```php
'default' => [
    // ...
    'command_retries' => env('REDIS_COMMAND_RETRIES', 0),
],

```

Predis 3.4.0 및 이후 버전은 `Retry` 클래스를 통해 내장된 재시도 및 백오프 구성을 지원합니다. `max_retries` 옵션을 사용하여 재시도를 구성할 수 있으며, `retry` 옵션을 사용하여 백오프 전략을 구성할 수 있습니다. `retry` 옵션은 다음 전략 클래스 중 하나를 키로 하는 배열이어야 합니다: `NoBackoff`, `EqualBackoff`, 또는 `ExponentialBackoff`:

```php
use Predis\Retry\Strategy\ExponentialBackoff;

'default' => [
    'url' => env('REDIS_URL'),
    // ...
    'retry' => [
        ExponentialBackoff::class => [
            env('REDIS_BACKOFF_BASE', 100),
            env('REDIS_BACKOFF_CAP', 1000),
            true, // Enable jitter...
        ],
    ],
    'max_retries' => env('REDIS_MAX_RETRIES', 3),
],

```

Predis를 Redis 클러스터와 함께 사용할 때 클러스터 구성의 `parameters` 옵션에 재시도 구성을 정의할 수 있습니다:

```php
use Predis\Retry\Strategy\NoBackoff;

'clusters' => [
    'default' => [
        // ...
    ],
],

'options' => [
    'cluster' => env('REDIS_CLUSTER', 'redis'),
    'parameters' => [
        'retry' => [
            NoBackoff::class => [],
        ],
        'max_retries' => env('REDIS_MAX_RETRIES', 3),
    ],
],

```

<a name="unix-socket-connections"></a>
#### 유닉스 소켓 연결

Redis 연결은 TCP 대신 유닉스 소켓을 사용하도록 구성할 수도 있습니다. 이는 애플리케이션과 동일한 서버의 Redis 인스턴스에 대한 연결에서 TCP 오버헤드를 제거하여 성능을 향상시킬 수 있습니다. Redis를 유닉스 소켓을 사용하도록 구성하려면 `REDIS_HOST` 환경 변수를 Redis 소켓 경로로 설정하고 `REDIS_PORT` 환경 변수를 `0`로 설정하세요:

```env
REDIS_HOST=/run/redis/redis.sock
REDIS_PORT=0

```

<a name="phpredis-serialization"></a>
#### PhpRedis 직렬화 및 압축

PhpRedis 확장은 다양한 직렬화기 및 압축 알고리즘을 사용하도록 구성할 수도 있습니다. 이러한 알고리즘은 Redis 설정의 `options` 배열을 통해 구성할 수 있습니다:

```php
'redis' => [

    'client' => env('REDIS_CLIENT', 'phpredis'),

    'options' => [
        'cluster' => env('REDIS_CLUSTER', 'redis'),
        'prefix' => env('REDIS_PREFIX', Str::slug(env('APP_NAME', 'laravel'), '_').'_database_'),
        'serializer' => Redis::SERIALIZER_MSGPACK,
        'compression' => Redis::COMPRESSION_LZ4,
    ],

    // ...
],

```

현재 지원되는 직렬화 도구에는 `Redis::SERIALIZER_NONE`(기본값), `Redis::SERIALIZER_PHP`, `Redis::SERIALIZER_JSON`, `Redis::SERIALIZER_IGBINARY`, `Redis::SERIALIZER_MSGPACK`가 포함됩니다.

지원되는 압축 알고리즘에는 `Redis::COMPRESSION_NONE`(기본값), `Redis::COMPRESSION_LZF`, `Redis::COMPRESSION_ZSTD`, `Redis::COMPRESSION_LZ4`가 포함됩니다.

<a name="interacting-with-redis"></a>
## Redis와 상호작용하기

`Redis` [파사드](/docs/{{version}}/facades)의 다양한 메서드를 호출하여 Redis와 상호작용할 수 있습니다. `Redis` 파사드는 동적 메서드를 지원하므로, 파사드에서 모든 [Redis 명령](https://redis.io/commands)을 호출할 수 있으며, 해당 명령은 직접 Redis로 전달됩니다. 이 예제에서는 `Redis` 파사드에서 `get` 메서드를 호출하여 Redis `GET` 명령을 호출합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Redis;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => Redis::get('user:profile:'.$id)
        ]);
    }
}

```

앞서 언급했듯이, Redis의 어떤 명령이든 `Redis` 퍼사드에서 호출할 수 있습니다. Laravel은 매직 메서드를 사용하여 명령을 Redis 서버로 전달합니다. Redis 명령이 인수를 필요로 하는 경우, 해당 인수를 퍼사드의 대응 메서드에 전달해야 합니다:

```php
use Illuminate\Support\Facades\Redis;

Redis::set('name', 'Taylor');

$values = Redis::lrange('names', 5, 10);

```

또는 `Redis` 퍼사드의 `command` 메서드를 사용하여 서버에 명령을 전달할 수 있으며, 이 메서드는 첫 번째 인수로 명령 이름을, 두 번째 인수로 값의 배열을 받습니다:

```php
$values = Redis::command('lrange', ['name', 5, 10]);

```

<a name="using-multiple-redis-connections"></a>
#### 여러 Redis 연결 사용하기

애플리케이션의 `config/database.php` 구성 파일에서는 여러 Redis 연결/서버를 정의할 수 있습니다. 특정 Redis 연결에 대한 연결은 `Redis` 퍼사드의 `connection` 메서드를 사용하여 얻을 수 있습니다:

```php
$redis = Redis::connection('connection-name');

```

기본 Redis 연결의 인스턴스를 얻으려면 추가 인수 없이 `connection` 메서드를 호출할 수 있습니다:

```php
$redis = Redis::connection();

```

<a name="transactions"></a>
### 거래

`Redis` 퍼사드의 `transaction` 메서드는 Redis의 기본 `MULTI` 및 `EXEC` 명령어를 편리하게 감싸는 래퍼를 제공합니다. `transaction` 메서드는 클로저를 유일한 인자로 받습니다. 이 클로저는 Redis 연결 인스턴스를 받게 되며, 해당 인스턴스에 원하는 명령어를 자유롭게 실행할 수 있습니다. 클로저 내에서 실행된 모든 Redis 명령어는 단일 원자 트랜잭션으로 실행됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::transaction(function (Redis $redis) {
    $redis->incr('user_visits', 1);
    $redis->incr('total_visits', 1);
});

```

> [!WARNING]
Redis 트랜잭션을 정의할 때 Redis 연결에서 값을 검색하지 못할 수 있습니다. 트랜잭션은 단일한 원자 작업으로 실행되며， 전체 종료가 명령 실행을 완료할 때까지 해당 작업은 실행되지 않습니다。

#### 루아 스크립트

`eval` 메서드는 단일 원자 작업에서 여러 Redis 명령을 실행하는 또 다른 방법을 제공합니다. 그러나 `eval` 메서드는 해당 작업 중에 Redis 키 값과 상호 작용하고 검사할 수 있다는 장점이 있습니다. Redis 스크립트는 [Lua 프로그래밍 언어](https://www.lua.org) 로 작성됩니다。

`eval` 메서드는 처음에는 조금 무서울 수 있지만， 얼음을 깨기 위해 기본적인 예를 살펴보겠습니다. `eval` 메서드는 여러 개의 인수를 요구합니다. 첫째， 루아 스크립트 (문자열로) 를 메서드에 전달해야 합니다. 둘째， 스크립트가 상호작용하는 키의 수 (정수로) 를 전달해야 합니다. 셋째， 해당 키의 이름을 전달해야 합니다. 마지막으로， 스크립트 내에서 액세스해야 하는 추가 인수를 전달할 수 있습니다。

이 예제에서는 카운터를 증가시키고， 새 값을 검사하며， 첫 번째 카운터의 값이 5 보다 크면 두 번째 카운터를 증가시킵니다. 마지막으로， 첫 번째 카운터 값을 반환합니다：

```php
$value = Redis::eval(<<<'LUA'
    local counter = redis.call("incr", KEYS[1])

    if counter > 5 then
        redis.call("incr", KEYS[2])
    end

    return counter
LUA, 2, 'first-counter', 'second-counter');

```

> [!WARNING]
> Redis 스크립팅에 대한 자세한 내용은 [Redis 문서](https://redis.io/commands/eval)를 참조하세요.

<a name="pipelining-commands"></a>
### 명령어 파이프라이닝

때때로 수십 개의 Redis 명령을 실행해야 할 때가 있습니다. 각 명령마다 Redis 서버로 네트워크 요청을 보내는 대신, `pipeline` 메서드를 사용할 수 있습니다. `pipeline` 메서드는 하나의 인수를 받습니다: Redis 인스턴스를 받는 클로저입니다. 이 Redis 인스턴스에 모든 명령을 발행할 수 있으며, 모든 명령은 동시에 Redis 서버로 전송되어 서버로의 네트워크 요청을 줄입니다. 명령은 발행된 순서대로 여전히 실행됩니다:

```php
use Redis;
use Illuminate\Support\Facades;

Facades\Redis::pipeline(function (Redis $pipe) {
    for ($i = 0; $i < 1000; $i++) {
        $pipe->set("key:$i", $i);
    }
});

```

<a name="pubsub"></a>
## 발행 / 구독

Laravel은 Redis `publish` 및 `subscribe` 명령어에 대한 편리한 인터페이스를 제공합니다. 이 Redis 명령어를 사용하면 특정 "채널"에서 메시지를 수신할 수 있습니다. 다른 애플리케이션이나 다른 프로그래밍 언어를 사용하여 채널에 메시지를 발행할 수 있어 애플리케이션과 프로세스 간의 쉬운 통신이 가능합니다.

먼저, `subscribe` 메서드를 사용하여 채널 리스너를 설정해 보겠습니다. `subscribe` 메서드를 호출하면 장기 실행 프로세스가 시작되기 때문에 이 메서드 호출을 [Artisan 명령](/docs/{{version}}/artisan) 내에 배치합니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Redis;

class RedisSubscribe extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'redis:subscribe';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Subscribe to a Redis channel';

    /**
     * Execute the console command.
     */
    public function handle(): void
    {
        Redis::subscribe(['test-channel'], function (string $message) {
            echo $message;
        });
    }
}

```

이제 `publish` 메서드를 사용하여 채널에 메시지를 게시할 수 있습니다:

```php
use Illuminate\Support\Facades\Redis;

Route::get('/publish', function () {
    // ...

    Redis::publish('test-channel', json_encode([
        'name' => 'Adam Wathan'
    ]));
});

```

<a name="wildcard-subscriptions"></a>
#### 와일드카드 구독

`psubscribe` 방법을 사용하면 모든 채널의 모든 메시지를 수신하는 데 유용할 수 있는 와일드카드 채널을 구독할 수 있습니다. 채널 이름은 제공된 클로저에 두 번째 인수로 전달됩니다:

```php
Redis::psubscribe(['*'], function (string $message, string $channel) {
    echo $message;
});

Redis::psubscribe(['users.*'], function (string $message, string $channel) {
    echo $message;
});

```
{% endraw %}
