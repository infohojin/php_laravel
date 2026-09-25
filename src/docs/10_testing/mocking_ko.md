---
layout: docs
title: "조롱"
---

{% raw %}
# 조롱

- [소개](#introduction)
- [모킹 오브젝트](#mocking-objects)
- 모킹 페이스 (#mocking-facades)
- [Facade Spies](#facade-spies)
- [시간과 상호작용](#interacting-with-time)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 테스트할 때， 특정 테스트 중에 실제로 실행되지 않도록 애플리케이션의 특정 측면을 “모방” 하고자 할 수 있습니다. 예를 들어， 이벤트를 전송하는 컨트롤러를 테스트할 때， 테스트 중에 실제로는 실행되지 않도록 이벤트 리스너를 모방하고자 할 수 있습니 다. 이를 통해 이벤트 리스너는 자체 테스트 케이스에서 테스트할 수 있으므로， 이벤트 리스너의 실행에 대해 걱정하지 않고 컨트롤러의 HTTP 응답만 테스트할 수 있습니다。

Laravel 은 이벤트， 작업 및 기타 패싯을 즉시 조롱할 수 있는 유용한 메서드를 제공합니다. 이러한 도우미는 주로 복잡한 Mockery 메서드 호출을 수동으로 수행할 필요가 없도록 Mockery 위에 편의성 계층을 제공합니다。

<a name="mocking-objects"></a>
## 조롱하는 물체들

Laravel 의 [서비스 컨테이너](/docs/{{version}}/container) 를 통해 애플리케이션에 주입될 객체를 조롱할 때， 조롱된 인스턴스를 `instance` 바인딩으로 컨테이너에 바인딩해야 합니다. 이렇게 하면 컨테이너가 객체 자체를 구축하는 대신 조롱된 객체 인스턴스를 사용하도록 지시합니다：

```

php tab=Pest
use App\Service;
use Mockery;
use Mockery\MockInterface;

test('something can be mocked', function () {
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->expects('process');
        })
    );
});

```

```

php tab=PHPUnit
use App\Service;
use Mockery;
use Mockery\MockInterface;

public function test_something_can_be_mocked(): void
{
    $this->instance(
        Service::class,
        Mockery::mock(Service::class, function (MockInterface $mock) {
            $mock->expects('process');
        })
    );
}

```

이를 더 편리하게 만들기 위해, Laravel의 기본 테스트 케이스 클래스에서 제공하는 `mock` 방법을 사용할 수 있습니다. 예를 들어, 다음 예제는 위의 예제와 동일합니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->mock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});

```

객체의 몇 가지 메소드만 모킹해야 할 때 `partialMock` 방법을 사용할 수 있습니다. 모킹되지 않은 메소드는 호출될 때 정상적으로 실행됩니다:

```php
use App\Service;
use Mockery\MockInterface;

$mock = $this->partialMock(Service::class, function (MockInterface $mock) {
    $mock->expects('process');
});

```

마찬가지로, 객체를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶다면, Laravel의 기본 테스트 케이스 클래스는 `Mockery::spy` 메서드 주위에 편리한 래퍼로서 `spy` 메서드를 제공합니다. 스파이는 목(mock)과 유사하지만, 스파이는 스파이와 테스트되는 코드 사이의 모든 상호작용을 기록하여 코드 실행 후에 어설션을 할 수 있게 합니다:

```php
use App\Service;

$spy = $this->spy(Service::class);

// ...

$spy->shouldHaveReceived('process');

```

<a name="mocking-facades"></a>
## 모킹된 퍼사드

전통적인 정적 메서드 호출과 달리, [퍼사드](/docs/{{version}}/facades) (포함하여 [실시간 퍼사드](/docs/{{version}}/facades#real-time-facades))는 모킹될 수 있습니다. 이는 전통적인 정적 메서드에 비해 큰 장점을 제공하며, 전통적인 의존성 주입을 사용할 때와 동일한 테스트 용이성을 제공합니다. 테스트 시에는 종종 컨트롤러 중 하나에서 발생하는 라라벨 퍼사드 호출을 모킹하고 싶을 수 있습니다. 예를 들어, 다음과 같은 컨트롤러 액션을 고려해 보십시오:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Cache;

class UserController extends Controller
{
    /**
     * Retrieve a list of all users of the application.
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



`expects` 메서드를 사용하여 `Cache` 파사드 호출을 모의(Mock)할 수 있으며, 이는 [Mockery](https://github.com/padraic/mockery) 모ック 인스턴스를 반환합니다. 파사드는 실제로 Laravel [서비스 컨테이너](/docs/{{version}}/container)에 의해 해결되고 관리되기 때문에 일반적인 정적 클래스보다 테스트 가능성이 훨씬 높습니다. 예를 들어, `Cache` 파사드의 `get` 메서드 호출을 모의해 봅시다:

```

php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('get index', function () {
    Cache::expects('get')
        ->with('key')
        ->andReturn('value');

    $response = $this->get('/users');

    // ...
});

```

```

php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Support\Facades\Cache;
use Tests\TestCase;

class UserControllerTest extends TestCase
{
    public function test_get_index(): void
    {
        Cache::expects('get')
            ->with('key')
            ->andReturn('value');

        $response = $this->get('/users');

        // ...
    }
}

```

> [!WARNING]
> `Request` 퍼사드를 조롱해서는 안 됩니다. 대신, 테스트를 실행할 때 원하는 입력을 `get` 및 `post`와 같은 [HTTP 테스트 메서드](/docs/{{version}}/http-tests)에 전달하십시오. 마찬가지로 `Config` 퍼사드를 모킹하는 대신 테스트에서 `Config::set` 메서드를 호출하십시오.

<a name="facade-spies"></a>
### 퍼사드 스파이

퍼사드를 [스파이](http://docs.mockery.io/en/latest/reference/spies.html)하고 싶다면, 해당 퍼사드에서 `spy` 메서드를 호출할 수 있습니다. 스파이는 모킹과 유사하지만, 스파이는 테스트 중인 코드와 스파이 간의 모든 상호작용을 기록하여 코드 실행 후에 어설션을 수행할 수 있게 합니다:

```

php tab=Pest
<?php

use Illuminate\Support\Facades\Cache;

test('values are stored in cache', function () {
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
});

```

```

php tab=PHPUnit
use Illuminate\Support\Facades\Cache;

public function test_values_are_stored_in_cache(): void
{
    Cache::spy();

    $response = $this->get('/');

    $response->assertStatus(200);

    Cache::shouldHaveReceived('put')->with('name', 'Taylor', 10);
}

```

<a name="interacting-with-time"></a>
## 시간과 상호작용하기

테스트할 때, `now`나 `Illuminate\Support\Carbon::now()`와 같은 헬퍼가 반환하는 시간을 가끔 수정해야 할 수도 있습니다. 다행히도, Laravel의 기본 기능 테스트 클래스에는 현재 시간을 조작할 수 있는 헬퍼가 포함되어 있습니다:

```

php tab=Pest
test('time can be manipulated', function () {
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->minus(hours: 6));

    // Return back to the present time...
    $this->travelBack();
});

```

```

php tab=PHPUnit
public function test_time_can_be_manipulated(): void
{
    // Travel into the future...
    $this->travel(5)->milliseconds();
    $this->travel(5)->seconds();
    $this->travel(5)->minutes();
    $this->travel(5)->hours();
    $this->travel(5)->days();
    $this->travel(5)->weeks();
    $this->travel(5)->years();

    // Travel into the past...
    $this->travel(-5)->hours();

    // Travel to an explicit time...
    $this->travelTo(now()->minus(hours: 6));

    // Return back to the present time...
    $this->travelBack();
}

```

또한 다양한 시간 여행 방법에 대한 클로저를 제공할 수 있습니다. 클로저는 지정된 시간에 시간이 멈춘 상태에서 호출됩니다. 클로저가 실행된 후에는 시간이 정상적으로 다시 진행됩니다:

```php
$this->travel(5)->days(function () {
    // Test something five days into the future...
});

$this->travelTo(now()->mins(days: 10), function () {
    // Test something during a given moment...
});

```



`freezeTime` 메서드는 현재 시간을 고정하는 데 사용할 수 있습니다. 마찬가지로, `freezeSecond` 메서드는 현재 시간을 고정하지만 현재 초의 시작 시점에서 고정합니다:

```php
use Illuminate\Support\Carbon;

// Freeze time and resume normal time after executing closure...
$this->freezeTime(function (Carbon $time) {
    // ...
});

// Freeze time at the current second and resume normal time after executing closure...
$this->freezeSecond(function (Carbon $time) {
    // ...
});

```

예상할 수 있듯이, 위에서 논의된 모든 방법들은 주로 토론 포럼에서 비활성 게시물을 잠그는 것과 같은 시간에 민감한 애플리케이션 동작을 테스트하는 데 유용합니다:

```

php tab=Pest
use App\Models\Thread;

test('forum threads lock after one week of inactivity', function () {
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    expect($thread->isLockedByInactivity())->toBeTrue();
});

```

```

php tab=PHPUnit
use App\Models\Thread;

public function test_forum_threads_lock_after_one_week_of_inactivity()
{
    $thread = Thread::factory()->create();

    $this->travel(1)->week();

    $this->assertTrue($thread->isLockedByInactivity());
}

```
{% endraw %}
