---
layout: docs
title: "Cache"
---

{% raw %}
# Cache

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
- [Cache Usage](#cache-usage)
    - [Obtaining a Cache Instance](#obtaining-a-cache-instance)
    - [Retrieving Items From the Cache](#retrieving-items-from-the-cache)
    - [Storing Items in the Cache](#storing-items-in-the-cache)
    - [Extending Item Lifetime](#extending-item-lifetime)
    - [Removing Items From the Cache](#removing-items-from-the-cache)
    - [Cache Memoization](#cache-memoization)
    - [The Cache Helper](#the-cache-helper)
- [Cache Tags](#cache-tags)
    - [Storing Tagged Cache Items](#storing-tagged-cache-items)
    - [Accessing Tagged Cache Items](#accessing-tagged-cache-items)
    - [Removing Tagged Cache Items](#removing-tagged-cache-items)
- [Atomic Locks](#atomic-locks)
    - [Managing Locks](#managing-locks)
    - [Managing Locks Across Processes](#managing-locks-across-processes)
    - [Refreshing Locks](#refreshing-locks)
    - [Concurrency Limiting](#concurrency-limiting)
- [Cache Failover](#cache-failover)
- [Adding Custom Cache Drivers](#adding-custom-cache-drivers)
    - [Writing the Driver](#writing-the-driver)
    - [Registering the Driver](#registering-the-driver)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Some of the data retrieval or processing tasks performed by your application could be CPU intensive or take several seconds to complete. When this is the case, it is common to cache the retrieved data for a time so it can be retrieved quickly on subsequent requests for the same data. The cached data is usually stored in a very fast data store such as [Memcached](https://memcached.org) or [Redis](https://redis.io).

Thankfully, Laravel provides an expressive, unified API for various cache backends, allowing you to take advantage of their blazing fast data retrieval and speed up your web application.

<a name="configuration"></a>
## Configuration



Your application's cache configuration file is located at `config/cache.php`. In this file, you may specify which cache store you would like to be used by default throughout your application. Laravel supports popular caching backends like [Memcached](https://memcached.org), [Redis](https://redis.io), [DynamoDB](https://aws.amazon.com/dynamodb), relational databases, and filesystem disks out of the box. In addition, a file based cache driver is available, while `array` and `null` cache drivers provide convenient cache backends for your automated tests.

The cache configuration file also contains a variety of other options that you may review. By default, Laravel is configured to use the `database` cache driver, which stores the serialized, cached objects in your application's database.

<a name="driver-prerequisites"></a>
### Driver Prerequisites

<a name="prerequisites-database"></a>
#### Database

When using the `database` cache driver, you will need a database table to contain the cache data. Typically, this is included in Laravel's default `0001_01_01_000001_create_cache_table.php` [database migration](/docs/{{version}}/migrations); however, if your application does not contain this migration, you may use the `make:cache-table` Artisan command to create it:

```shell
php artisan make:cache-table

php artisan migrate
```



<a name="memcached"></a>
#### Memcached

Memcached 드라이버를 사용하려면 [Memcached PECL 패키지](https://pecl.php.net/package/memcached)가 설치되어 있어야 합니다. 모든 Memcached 서버를 `config/cache.php` 구성 파일에 나열할 수 있습니다. 이 파일에는 시작하는 데 도움이 되는 `memcached.servers` 항목이 이미 포함되어 있습니다:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => env('MEMCACHED_HOST', '127.0.0.1'),
            'port' => env('MEMCACHED_PORT', 11211),
            'weight' => 100,
        ],
    ],
],
```



필요하다면 `host` 옵션을 UNIX 소켓 경로로 설정할 수 있습니다. 이렇게 하는 경우, `port` 옵션은 `0`로 설정해야 합니다:

```php
'memcached' => [
    // ...

    'servers' => [
        [
            'host' => '/var/run/memcached/memcached.sock',
            'port' => 0,
            'weight' => 100
        ],
    ],
],
```



<a name="redis"></a>
#### 레디스

Laravel에서 Redis 캐시를 사용하기 전에 PECL을 통해 PhpRedis PHP 확장 프로그램을 설치하거나 Composer를 통해 `predis/predis` 패키지를 설치해야 합니다. [Laravel Sail](/docs/{{version}}/sail)에는 이미 이 확장 프로그램이 포함되어 있습니다. 또한 [Laravel Cloud](https://cloud.laravel.com) 및 [Laravel Forge](https://forge.laravel.com)와 같은 공식 Laravel 애플리케이션 플랫폼에는 PhpRedis 확장이 기본적으로 설치되어 있습니다.

Redis 구성에 대한 자세한 내용은 해당 [Laravel 문서 페이지](/docs/{{version}}/redis#configuration)를 참조하십시오.

<a name="storage"></a>
#### 스토리지

`storage` 캐시 드라이버를 사용하면 애플리케이션에서 구성한 [파일 시스템 디스크](/docs/{{version}}/filesystem) 중 어느 곳에든 캐시된 값을 저장할 수 있습니다. 이는 S3 디스크와 같은 기존 디스크를 키/값 캐시 저장소로 사용하려는 경우 유용할 수 있습니다:

```php
'storage' => [
    'driver' => 'storage',
    'disk' => env('CACHE_STORAGE_DISK'),
    'path' => env('CACHE_STORAGE_PATH', 'framework/cache/data'),
],
```



<a name="dynamodb"></a>
#### DynamoDB

[DynamoDB](https://aws.amazon.com/dynamodb) 캐시 드라이버를 사용하기 전에, 모든 캐시된 데이터를 저장할 DynamoDB 테이블을 생성해야 합니다. 일반적으로 이 테이블의 이름은 `cache`이어야 합니다. 그러나 이 테이블의 이름은 `cache` 구성 파일 내 `stores.dynamodb.table` 구성 값에 따라 지정해야 합니다. 테이블 이름은 `DYNAMODB_CACHE_TABLE` 환경 변수를 통해서도 설정할 수 있습니다.

이 테이블에는 애플리케이션의 `cache` 구성 파일 내 `stores.dynamodb.attributes.key` 구성 항목 값과 일치하는 이름의 문자열 분할 키도 있어야 합니다. 기본적으로 분할 키의 이름은 `key`이어야 합니다.

일반적으로 DynamoDB는 테이블에서 만료된 항목을 능동적으로 제거하지 않습니다. 따라서 테이블에서 [TTL(Time to Live)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 활성화해야 합니다. 테이블의 TTL 설정을 구성할 때 TTL 속성 이름을 `expires_at`로 설정해야 합니다.

다음으로, Laravel 애플리케이션이 DynamoDB와 통신할 수 있도록 AWS SDK를 설치합니다:

```shell
composer require aws/aws-sdk-php
```



또한 DynamoDB 캐시 스토어 구성 옵션에 대한 값이 제공되었는지 확인해야 합니다. 일반적으로 `AWS_ACCESS_KEY_ID` 및 `AWS_SECRET_ACCESS_KEY`과 같은 이러한 옵션은 애플리케이션의 `.env` 구성 파일에 정의되어야 합니다:

```php
'dynamodb' => [
    'driver' => 'dynamodb',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => env('DYNAMODB_CACHE_TABLE', 'cache'),
    'endpoint' => env('DYNAMODB_ENDPOINT'),
],
```



<a name="mongodb"></a>
#### MongoDB

MongoDB를 사용하는 경우, `mongodb` 캐시 드라이버가 공식 `mongodb/laravel-mongodb` 패키지에 의해 제공되며 `mongodb` 데이터베이스 연결을 사용하여 구성할 수 있습니다. MongoDB는 TTL 인덱스를 지원하며, 이를 사용하여 만료된 캐시 항목을 자동으로 삭제할 수 있습니다.

MongoDB 구성에 대한 자세한 정보는 MongoDB [캐시 및 잠금 문서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/)를 참조하십시오.

<a name="cache-usage"></a>
## 캐시 사용

<a name="obtaining-a-cache-instance"></a>
### 캐시 인스턴스 얻기

캐시 스토어 인스턴스를 얻으려면, `Cache` 퍼사드를 사용할 수 있으며, 이 문서 전체에서 이를 사용할 것입니다. `Cache` 퍼사드는 Laravel 캐시 계약의 기본 구현에 편리하고 간결하게 접근할 수 있게 해줍니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Show a list of all users of the application.
     */
    public function index(): array
    {
        $value = Cache::get('key');

        return [
            // ...
        ];
    }
}
```



<a name="accessing-multiple-cache-stores"></a>
#### 다중 캐시 스토어 접근하기

`Cache` 퍼사드를 사용하면 `store` 메서드를 통해 다양한 캐시 스토어에 접근할 수 있습니다. `store` 메서드에 전달된 키는 `cache` 구성 파일의 `stores` 구성 배열에 나열된 스토어 중 하나와 일치해야 합니다:

```php
$value = Cache::store('file')->get('foo');

Cache::store('redis')->put('bar', 'baz', 600); // 10 Minutes
```



<a name="retrieving-items-from-the-cache"></a>
### 캐시에서 항목 가져오기

`Cache` 퍼사드의 `get` 메서드는 캐시에서 항목을 가져오는 데 사용됩니다. 항목이 캐시에 존재하지 않으면 `null`가 반환됩니다. 원하신다면, 항목이 존재하지 않을 경우 반환될 기본 값을 지정하여 `get` 메서드에 두 번째 인수를 전달할 수 있습니다:

```php
$value = Cache::get('key');

$value = Cache::get('key', 'default');
```



기본값으로 클로저를 전달할 수도 있습니다. 지정된 항목이 캐시에 존재하지 않으면 클로저의 결과가 반환됩니다. 클로저를 전달하면 데이터베이스나 기타 외부 서비스에서 기본값을 가져오는 작업을 지연시킬 수 있습니다:

```php
$value = Cache::get('key', function () {
    return DB::table(/* ... */)->get();
});
```



<a name="determining-item-existence"></a>
#### 항목 존재 여부 결정

`has` 메서드는 캐시에 항목이 존재하는지 여부를 결정하는 데 사용될 수 있습니다. 이 메서드는 또한 항목이 존재하지만 그 값이 `null`일 경우 `false`를 반환합니다:

```php
if (Cache::has('key')) {
    // ...
}
```



<a name="incrementing-decrementing-values"></a>
#### 값 증가 / 감소

`increment`와 `decrement` 메소드는 캐시에 있는 정수 항목의 값을 조정하는 데 사용할 수 있습니다. 이 두 메소드는 항목의 값을 증가시키거나 감소시킬 양을 나타내는 선택적 두 번째 인수를 받습니다:

```php
// Initialize the value if it does not exist...
Cache::add('key', 0, now()->plus(hours: 4));

// Increment or decrement the value...
Cache::increment('key');
Cache::increment('key', $amount);
Cache::decrement('key');
Cache::decrement('key', $amount);
```



<a name="retrieve-store"></a>
#### 검색 및 저장

때때로 캐시에서 항목을 검색하고, 요청한 항목이 존재하지 않을 경우 기본값을 저장하고 싶을 수 있습니다. 예를 들어, 캐시에서 모든 사용자를 검색하거나, 존재하지 않는 경우 데이터베이스에서 가져와 캐시에 추가하고 싶을 수 있습니다. 이는 `Cache::remember` 메서드를 사용하여 수행할 수 있습니다:

```php
$value = Cache::remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```



항목이 캐시에 존재하지 않는 경우, `remember` 메서드에 전달된 클로저가 실행되고 그 결과가 캐시에 저장됩니다.

항목이 주어진 클로저를 실행하여 가져온 것이 아니라 캐시에서 가져온 것인지 여부를 확인해야 하는 경우, `rememberWithWarmth` 메서드를 사용할 수 있습니다. 이 메서드는 캐시된 값과 항목이 "웜"인지 여부를 나타내는 부울 값을 포함하는 배열을 반환합니다. 여기서 "웜"은 항목이 클로저에서 해결되지 않고 캐시에서 가져온 것임을 의미합니다.

```php
[$value, $warm] = Cache::rememberWithWarmth('users', $seconds, function () {
    return DB::table('users')->get();
});
```



캐시에서 항목을 가져오거나 존재하지 않을 경우 영구적으로 저장하기 위해 `rememberForever` 방법을 사용할 수 있습니다:

```php
$value = Cache::rememberForever('users', function () {
    return DB::table('users')->get();
});
```



<a name="swr"></a>
#### Stale While Revalidate

When using the `Cache::remember` method, some users may experience slow response times if the cached value has expired. For certain types of data, it can be useful to allow partially stale data to be served while the cached value is recalculated in the background, preventing some users from experiencing slow response times while cached values are calculated. This is often referred to as the "stale-while-revalidate" pattern, and the `Cache::flexible` method provides an implementation of this pattern.

The flexible method accepts an array that specifies how long the cached value is considered "fresh" and when it becomes "stale". The first value in the array represents the number of seconds the cache is considered fresh, while the second value defines how long it can be served as stale data before recalculation is necessary.

If a request is made within the fresh period (before the first value), the cache is returned immediately without recalculation. If a request is made during the stale period (between the two values), the stale value is served to the user, and a [deferred function](/docs/{{version}}/helpers#deferred-functions) is registered to refresh the cached value after the response is sent to the user. If a request is made after the second value, the cache is considered expired, and the value is recalculated immediately, which may result in a slower response for the user:

```php
$value = Cache::flexible('users', [5, 10], function () {
    return DB::table('users')->get();
});
```



<a name="retrieve-delete"></a>
#### 조회 및 삭제

캐시에서 항목을 조회한 후 삭제해야 하는 경우, `pull` 메서드를 사용할 수 있습니다. `get` 메서드와 마찬가지로, 캐시에 항목이 존재하지 않으면 `null`가 반환됩니다:

```php
$value = Cache::pull('key');

$value = Cache::pull('key', 'default');
```



<a name="storing-items-in-the-cache"></a>
### 캐시에 아이템 저장하기

캐시에 아이템을 저장하려면 `Cache` 퍼사드에서 `put` 메서드를 사용할 수 있습니다:

```php
Cache::put('key', 'value', $seconds = 10);
```



저장 시간이 `put` 메서드에 전달되지 않으면, 항목은 무기한 저장됩니다:

```php
Cache::put('key', 'value');
```



정수를 초 단위로 전달하는 대신, 캐시된 항목의 원하는 만료 시간을 나타내는 `DateTime` 인스턴스를 전달할 수도 있습니다:

```php
Cache::put('key', 'value', now()->plus(minutes: 10));
```



<a name="store-if-not-present"></a>
#### 존재하지 않으면 저장

`add` 메서드는 항목이 캐시 저장소에 이미 존재하지 않을 경우에만 항목을 캐시에 추가합니다. 항목이 실제로 캐시에 추가되면 메서드는 `true`를 반환합니다. 그렇지 않으면 메서드는 `false`를 반환합니다. `add` 메서드는 원자적 연산입니다:

```php
Cache::add('key', 'value', $seconds);
```



<a name="extending-item-lifetime"></a>
### 항목 수명 연장

`touch` 메서드는 기존 캐시 항목의 수명(TTL)을 연장할 수 있습니다. `touch` 메서드는 캐시 항목이 존재하고 만료 시간이 성공적으로 연장되면 `true`를 반환합니다. 항목이 캐시에 존재하지 않으면, 메서드는 `false`를 반환합니다:

```php
Cache::touch('key', 3600);
```



정확한 만료 시간을 지정하려면 `DateTimeInterface`, `DateInterval` 또는 `Carbon` 인스턴스를 제공할 수 있습니다:

```php
Cache::touch('key', now()->addHours(2));
```



<a name="storing-items-forever"></a>
#### 아이템을 영구 저장하기

`forever` 방법은 아이템을 캐시에 영구적으로 저장하는 데 사용할 수 있습니다. 이 아이템들은 만료되지 않으므로, `forget` 방법을 사용하여 캐시에서 수동으로 제거해야 합니다:

```php
Cache::forever('key', 'value');
```



> [!NOTE]
> Memcached 드라이버를 사용하는 경우, '영구'로 저장된 항목도 캐시가 용량 한도에 도달하면 제거될 수 있습니다.

<a name="removing-items-from-the-cache"></a>
### 캐시에서 항목 제거하기

`forget` 메서드를 사용하여 캐시에서 항목을 제거할 수 있습니다:

```php
Cache::forget('key');
```



만료 시간을 0 또는 음수로 제공하여 항목을 제거할 수도 있습니다:

```php
Cache::put('key', 'value', 0);

Cache::put('key', 'value', -5);
```



`flush` 방법을 사용하여 전체 캐시를 지울 수 있습니다:

```php
Cache::flush();
```



`flushLocks` 메서드를 사용하여 캐시의 모든 원자 잠금을 해제할 수 있습니다:

```php
Cache::flushLocks();
```



> [!WARNING]
> 캐시를 플러시하면 구성된 캐시 "접두사"가 무시되며 캐시의 모든 항목이 제거됩니다. 다른 애플리케이션과 공유되는 캐시를 지울 때는 이를 신중히 고려하십시오.

<a name="cache-memoization"></a>
### 캐시 메모이제이션

Laravel의 `memo` 캐시 드라이버를 사용하면 단일 요청 또는 작업 실행 중에 해결된 캐시 값을 메모리에 일시적으로 저장할 수 있습니다. 이는 같은 실행 내에서 반복적인 캐시 조회를 방지하여 성능을 크게 향상시킵니다.

메모이제이션된 캐시를 사용하려면 `memo` 메서드를 호출하십시오:

```php
use Illuminate\Support\Facades\Cache;

$value = Cache::memo()->get('key');
```



`memo` 메서드는 선택적으로 캐시 저장소의 이름을 허용하며, 이는 메모이제이션된 드라이버가 장식할 기본 캐시 저장소를 지정합니다:

```php
// Using the default cache store...
$value = Cache::memo()->get('key');

// Using the Redis cache store...
$value = Cache::memo('redis')->get('key');
```



주어진 키에 대한 첫 번째 `get` 호출은 캐시 저장소에서 값을 가져오지만, 동일한 요청이나 작업 내에서 이후 호출은 메모리에서 값을 가져옵니다:

```php
// Hits the cache...
$value = Cache::memo()->get('key');

// Does not hit the cache, returns memoized value...
$value = Cache::memo()->get('key');
```



캐시 값을 수정하는 메서드(`put`, `increment`, `remember` 등)를 호출할 때, 메모이제이션된 캐시는 자동으로 메모이제이션된 값을 잊고, 변형 메서드 호출을 기본 캐시 저장소로 위임합니다:

```php
Cache::memo()->put('name', 'Taylor'); // Writes to underlying cache...
Cache::memo()->get('name');           // Hits underlying cache...
Cache::memo()->get('name');           // Memoized, does not hit cache...

Cache::memo()->put('name', 'Tim');    // Forgets memoized value, writes new value...
Cache::memo()->get('name');           // Hits underlying cache again...
```



<a name="the-cache-helper"></a>
### 캐시 헬퍼

`Cache` 파사드를 사용하는 것 외에도, 글로벌 `cache` 함수를 사용하여 캐시를 통해 데이터를 가져오고 저장할 수 있습니다. `cache` 함수가 하나의 문자열 인수와 함께 호출되면, 주어진 키의 값을 반환합니다:

```php
$value = cache('key');
```



함수에 키/값 쌍 배열과 만료 시간을 제공하면, 지정된 기간 동안 값을 캐시에 저장합니다:

```php
cache(['key' => 'value'], $seconds);

cache(['key' => 'value'], now()->plus(minutes: 10));
```



`cache` 함수가 인수 없이 호출되면 `Illuminate\Contracts\Cache\Factory` 구현의 인스턴스를 반환하며, 이를 통해 다른 캐싱 메서드를 호출할 수 있습니다:

```php
cache()->remember('users', $seconds, function () {
    return DB::table('users')->get();
});
```



> [!NOTE]
> 전역 `cache` 함수에 대한 호출을 테스트할 때, [파사드 테스트](/docs/{{version}}/mocking#mocking-facades)를 하는 것처럼 `Cache::shouldReceive` 메서드를 사용할 수 있습니다.

<a name="cache-tags"></a>
## 캐시 태그

> [!WARNING]
> 캐시 태그는 `file`, `dynamodb`, `database` 또는 `storage` 캐시 드라이버를 사용할 때는 지원되지 않습니다.

<a name="storing-tagged-cache-items"></a>
### 태그된 캐시 항목 저장

캐시 태그를 사용하면 캐시에서 관련 항목에 태그를 지정한 다음, 특정 태그가 할당된 모든 캐시 값을 플러시할 수 있습니다. 태그 이름의 정렬된 배열을 전달하여 태그된 캐시 항목에 접근할 수 있습니다. 예를 들어, 태그된 캐시에 접근하여 `put` 값을 캐시에 저장해봅시다:

```php
use Illuminate\Support\Facades\Cache;

Cache::tags(['people', 'artists'])->put('John', $john, $seconds);
Cache::tags(['people', 'authors'])->put('Anne', $anne, $seconds);
```



<a name="accessing-tagged-cache-items"></a>
### 태그된 캐시 항목 접근

태그를 통해 저장된 항목은 값을 저장할 때 사용된 태그를 함께 제공하지 않으면 접근할 수 없습니다. 태그된 캐시 항목을 가져오려면, `tags` 메서드에 동일한 순서의 태그 목록을 전달한 다음, 가져오려는 키와 함께 `get` 메서드를 호출하십시오:

```php
$john = Cache::tags(['people', 'artists'])->get('John');

$anne = Cache::tags(['people', 'authors'])->get('Anne');
```



<a name="removing-tagged-cache-items"></a>
### 태그가 지정된 캐시 항목 제거

태그 또는 태그 목록이 지정된 모든 항목을 플러시할 수 있습니다. 예를 들어, 다음 코드는 `people`, `authors` 중 하나 또는 둘 모두로 태그가 지정된 모든 캐시를 제거합니다. 따라서 `Anne`와 `John`가 캐시에서 제거됩니다:

```php
Cache::tags(['people', 'authors'])->flush();
```



반대로, 아래 코드는 `authors`로 태그된 캐시된 값만 제거하므로, `Anne`는 제거되지만 `John`는 제거되지 않습니다:

```php
Cache::tags('authors')->flush();
```



<a name="atomic-locks"></a>
## 원자적 잠금

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션이 `memcached`, `redis`, `dynamodb`, `database`, `file`, 또는 `array` 캐시 드라이버를 애플리케이션의 기본 캐시 드라이버로 사용하고 있어야 합니다. 또한, 모든 서버는 동일한 중앙 캐시 서버와 통신하고 있어야 합니다.

<a name="managing-locks"></a>
### 잠금 관리

원자적 잠금은 경쟁 조건을 걱정하지 않고 분산 잠금을 조작할 수 있게 해줍니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)는 원자적 잠금을 사용하여 한 번에 한 서버에서만 원격 작업이 실행되도록 보장합니다. `Cache::lock` 메서드를 사용하여 잠금을 생성하고 관리할 수 있습니다:

```php
use Illuminate\Support\Facades\Cache;

$lock = Cache::lock('foo', 10);

if ($lock->get()) {
    // Lock acquired for 10 seconds...

    $lock->release();
}
```



`get` 메서드도 클로저를 허용합니다. 클로저가 실행된 후, Laravel은 자동으로 락을 해제합니다:

```php
Cache::lock('foo', 10)->get(function () {
    // Lock acquired for 10 seconds and automatically released...
});
```



잠금이 요청 시점에 사용 가능하지 않은 경우, Laravel에 지정된 초 동안 대기하도록 지시할 수 있습니다. 지정된 시간 내에 잠금을 획득할 수 없으면 `Illuminate\Contracts\Cache\LockTimeoutException`이 발생합니다:

```php
use Illuminate\Contracts\Cache\LockTimeoutException;

$lock = Cache::lock('foo', 10);

try {
    $lock->block(5);

    // Lock acquired after waiting a maximum of 5 seconds...
} catch (LockTimeoutException $e) {
    // Unable to acquire lock...
} finally {
    $lock->release();
}
```



위의 예제는 `block` 메서드에 클로저를 전달함으로써 단순화할 수 있습니다. 이 메서드에 클로저를 전달하면, Laravel은 지정된 초 동안 잠금을 획득하려 시도하며, 클로저가 실행된 후에는 잠금을 자동으로 해제합니다:

```php
Cache::lock('foo', 10)->block(5, function () {
    // Lock acquired for 10 seconds after waiting a maximum of 5 seconds...
});
```



<a name="managing-locks-across-processes"></a>
### 프로세스 간 락 관리

때때로 하나의 프로세스에서 락을 획득하고 다른 프로세스에서 풀기를 원할 때가 있습니다. 예를 들어, 웹 요청 중에 락을 획득하고 해당 요청으로 트리거되는 큐 작업이 끝날 때 락을 해제하고 싶을 수 있습니다. 이 시나리오에서는 락의 범위 내 "소유자 토큰"을 큐 작업에 전달하여 작업이 주어진 토큰을 사용해 락을 다시 인스턴스화할 수 있도록 해야 합니다.

아래 예제에서는 락이 성공적으로 획득되면 큐 작업을 디스패치합니다. 또한 락의 소유자 토큰을 락의 `owner` 메서드를 통해 큐 작업에 전달합니다:

```php
$podcast = Podcast::find($id);

$lock = Cache::lock('processing', 120);

if ($lock->get()) {
    ProcessPodcast::dispatch($podcast, $lock->owner());
}
```



우리 애플리케이션의 `ProcessPodcast` 작업 내에서 소유자 토큰을 사용하여 잠금을 복원하고 해제할 수 있습니다:

```php
Cache::restoreLock('processing', $this->owner)->release();
```



현재 소유자를 존중하지 않고 잠금을 해제하려는 경우, `forceRelease` 방법을 사용할 수 있습니다:

```php
Cache::lock('processing')->forceRelease();
```



<a name="refreshing-locks"></a>
### 잠금 갱신

현재 소유하고 있는 잠금의 만료 시간을 연장해야 하는 경우, `refresh` 메서드를 사용할 수 있습니다. 초 단위의 숫자가 제공되지 않으면 잠금의 원래 기간이 사용됩니다. 이는 장시간 실행되는 작업에서, 매우 긴 만료 시간을 가진 잠금을 획득하는 대신 짧은 잠금을 획득하고 주기적으로 연장하는 것이 바람직할 때 유용합니다:

```php
$lock = Cache::lock('generate-reports', 60);

if ($lock->get()) {
    foreach ($reports as $report) {
        $report->generate();

        // Extend the lock for another 60 seconds...
        $lock->refresh();
    }

    $lock->release();
}
```



<a name="concurrency-limiting"></a>
### 동시 실행 제한

Laravel의 원자적 잠금 기능은 클로저의 동시 실행을 제한하는 몇 가지 방법도 제공합니다. `withoutOverlapping`를 사용하면 인프라 전체에서 동시에 하나의 인스턴스만 실행되도록 허용할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired after waiting a maximum of 10 seconds...
});
```



기본적으로, 잠금은 클로저 실행이 끝날 때까지 유지되며, 메서드는 잠금을 획득하기 위해 최대 10초까지 기다립니다. 이러한 값들은 추가 인수를 사용하여 사용자 지정할 수 있습니다:

```php
Cache::withoutOverlapping('foo', function () {
    // Lock acquired for 120 seconds after waiting a maximum of 5 seconds...
}, lockFor: 120, waitFor: 5);
```



지정된 대기 시간 내에 잠금을 획득할 수 없으면 `Illuminate\Contracts\Cache\LockTimeoutException`가 발생합니다.

제어된 병렬 처리를 원하면 `funnel` 메서드를 사용하여 최대 동시 실행 수를 설정하세요. `funnel` 메서드는 잠금을 지원하는 모든 캐시 드라이버에서 작동합니다:

```php
Cache::funnel('foo')
    ->limit(3)
    ->releaseAfter(60)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired...
    }, function () {
        // Could not acquire concurrency lock...
    });
```



`funnel` 키는 제한되고 있는 자원을 식별합니다. `limit` 메서드는 최대 동시 실행 수를 정의합니다. `releaseAfter` 메서드는 획득한 슬롯이 자동으로 해제되기 전의 안전 타임아웃(초)을 설정합니다. `block` 메서드는 사용 가능한 슬롯을 기다리는 시간을 초 단위로 설정합니다.

실패 클로저를 제공하는 대신 예외를 통해 타임아웃을 처리하려면 두 번째 클로저를 생략할 수 있습니다. 지정된 대기 시간 안에 락을 획득할 수 없으면 `Illuminate\Cache\Limiters\LimiterTimeoutException`가 발생합니다:

```php
use Illuminate\Cache\Limiters\LimiterTimeoutException;

try {
    Cache::funnel('foo')
        ->limit(3)
        ->releaseAfter(60)
        ->block(10)
        ->then(function () {
            // Concurrency lock acquired...
        });
} catch (LimiterTimeoutException $e) {
    // Unable to acquire concurrency lock...
}
```



동시성 제한기(concurrency limiter)에 특정 캐시 저장소를 사용하고 싶다면, 원하는 저장소에서 `funnel` 메서드를 호출할 수 있습니다:

```php
Cache::store('redis')->funnel('foo')
    ->limit(3)
    ->block(10)
    ->then(function () {
        // Concurrency lock acquired using the "redis" store...
    });
```



> [!NOTE]
> `funnel` 메서드는 캐시 스토어가 `Illuminate\Contracts\Cache\LockProvider` 인터페이스를 구현할 것을 요구합니다. 잠금을 지원하지 않는 캐시 스토어에서 `funnel`를 사용하려고 하면 `BadMethodCallException`가 발생합니다.

<a name="cache-failover"></a>
## 캐시 장애 조치

`failover` 캐시 드라이버는 캐시와 상호작용할 때 자동 장애 조치 기능을 제공합니다. `failover` 스토어의 기본 캐시 스토어가 어떤 이유로든 실패하면, Laravel은 자동으로 목록에 있는 다음 구성된 스토어를 사용하려고 시도합니다. 이는 특히 캐시 신뢰성이 중요한 프로덕션 환경에서 높은 가용성을 보장하는 데 유용합니다.

장애 조치 캐시 스토어를 구성하려면 `failover` 드라이버를 지정하고 시도할 스토어 이름의 배열을 제공하면 됩니다. 기본적으로 Laravel은 애플리케이션의 `config/cache.php` 구성 파일에 예제 장애 조치 구성을 포함합니다.

```php
'failover' => [
    'driver' => 'failover',
    'stores' => [
        'database',
        'array',
    ],
],
```



`failover` 드라이버를 사용하는 스토어를 구성한 후에는 페일오버 기능을 사용하기 위해 애플리케이션의 `.env` 파일에서 페일오버 스토어를 기본 캐시 스토어로 설정해야 합니다:

```ini
CACHE_STORE=failover
```



캐시 저장 작업이 실패하고 장애 조치(failover)가 활성화되면, Laravel은 `Illuminate\Cache\Events\CacheFailedOver` 이벤트를 발행하여 캐시 저장소가 실패했음을 보고하거나 기록할 수 있게 합니다.

<a name="adding-custom-cache-drivers"></a>
## 사용자 정의 캐시 드라이버 추가하기

<a name="writing-the-driver"></a>
### 드라이버 작성하기

사용자 정의 캐시 드라이버를 만들려면 먼저 `Illuminate\Contracts\Cache\Store` [계약](/docs/{{version}}/contracts)을 구현해야 합니다. 따라서, MongoDB 캐시 구현은 대략 다음과 같이 보일 수 있습니다:

```php
<?php

namespace App\Extensions;

use Illuminate\Contracts\Cache\Store;

class MongoStore implements Store
{
    public function get($key) {}
    public function many(array $keys) {}
    public function put($key, $value, $seconds) {}
    public function putMany(array $values, $seconds) {}
    public function increment($key, $value = 1) {}
    public function decrement($key, $value = 1) {}
    public function forever($key, $value) {}
    public function forget($key) {}
    public function flush() {}
    public function getPrefix() {}
}
```



우리는 단순히 MongoDB 연결을 사용하여 이러한 각 메서드를 구현하면 됩니다. 이러한 각 메서드를 구현하는 방법의 예시는 [Laravel 프레임워크 소스 코드](https://github.com/laravel/framework)에서 `Illuminate\Cache\MemcachedStore`를 참고하세요. 구현이 완료되면 `Cache` 파사드의 `extend` 메서드를 호출하여 커스텀 드라이버 등록을 완료할 수 있습니다:

```php
Cache::extend('mongo', function (Application $app) {
    return Cache::repository(new MongoStore);
});
```



> [!NOTE]
> 커스텀 캐시 드라이버 코드를 어디에 넣어야 할지 고민된다면, `app` 디렉토리 내에 `Extensions` 네임스페이스를 생성할 수 있습니다. 하지만 Laravel은 엄격한 애플리케이션 구조를 요구하지 않으므로, 애플리케이션을 자신의 선호에 따라 자유롭게 구성할 수 있다는 점을 명심하세요.

<a name="registering-the-driver"></a>
### 드라이버 등록

Laravel에 커스텀 캐시 드라이버를 등록하기 위해 `Cache` 파사드에서 `extend` 메서드를 사용할 것입니다. 다른 서비스 프로바이더가 `boot` 메서드 내에서 캐시된 값을 읽으려고 시도할 수 있으므로, `booting` 콜백 내에서 커스텀 드라이버를 등록할 것입니다. `booting` 콜백을 사용하면 애플리케이션의 서비스 프로바이더에서 `boot` 메서드가 호출되기 직전에, 하지만 모든 서비스 프로바이더에서 `register` 메서드가 호출된 후에 커스텀 드라이버가 등록되도록 보장할 수 있습니다. `booting` 콜백은 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `register` 메서드 내에서 등록할 것입니다:

```php
<?php

namespace App\Providers;

use App\Extensions\MongoStore;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        $this->app->booting(function () {
             Cache::extend('mongo', function (Application $app) {
                 return Cache::repository(new MongoStore);
             });
         });
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        // ...
    }
}
```



The first argument passed to the `extend` method is the name of the driver. This will correspond to your `driver` option in the `config/cache.php` configuration file. The second argument is a closure that should return an `Illuminate\Cache\Repository` instance. The closure will be passed an `$app` instance, which is an instance of the [service container](/docs/{{version}}/container).

Once your extension is registered, update the `CACHE_STORE` environment variable or `default` option within your application's `config/cache.php` configuration file to the name of your extension.

<a name="events"></a>
## Events

To execute code on every cache operation, you may listen for various [events](/docs/{{version}}/events) dispatched by the cache:

<div class="overflow-auto">

| Event Name                                      |
|-------------------------------------------------|
| `Illuminate\Cache\Events\CacheFlushed`          |
| `Illuminate\Cache\Events\CacheFlushing`         |
| `Illuminate\Cache\Events\CacheFlushFailed`      |
| `Illuminate\Cache\Events\CacheLocksFlushed`     |
| `Illuminate\Cache\Events\CacheLocksFlushing`    |
| `Illuminate\Cache\Events\CacheLocksFlushFailed` |
| `Illuminate\Cache\Events\CacheHit`              |
| `Illuminate\Cache\Events\CacheMissed`           |
| `Illuminate\Cache\Events\ForgettingKey`         |
| `Illuminate\Cache\Events\KeyForgetFailed`       |
| `Illuminate\Cache\Events\KeyForgotten`          |
| `Illuminate\Cache\Events\KeyWriteFailed`        |
| `Illuminate\Cache\Events\KeyWritten`            |
| `Illuminate\Cache\Events\RetrievingKey`         |
| `Illuminate\Cache\Events\RetrievingManyKeys`    |
| `Illuminate\Cache\Events\WritingKey`            |
| `Illuminate\Cache\Events\WritingManyKeys`       |

</div>

To increase performance, you may disable cache events by setting the `events` configuration option to `false` for a given cache store in your application's `config/cache.php` configuration file:

```php
'database' => [
    'driver' => 'database',
    // ...
    'events' => false,
],
```
{% endraw %}
