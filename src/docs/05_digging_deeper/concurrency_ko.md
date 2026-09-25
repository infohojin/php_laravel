---
layout: docs
title: "동시성"
---

{% raw %}
# 동시성

- [소개](#introduction)
- [동시 작업 실행](#running-concurrent-tasks)
- [명명 결과](#named-results)
- [작업 시간 초과](#task-timeouts)
- [동시 작업 연기](#deferring-concurrent-tasks)

<a name="introduction"></a>
## 소개

때로는 서로 의존하지 않는 여러 개의 느린 작업을 실행해야 할 수 있습니다. 많은 경우 작업을 동시에 실행하면 상당한 성능 향상을 달성할 수 있습니다. Laravel 의 `Concurrency` 패싯은 폐쇄를 동시에 실행하기 위한 간단하고 편리한 API 를 제공합니다。

<a name="how-it-works"></a>
#### 어떻게 작동하는가

Laravel 은 주어진 종료를 직렬화하고 숨겨진 Artisan CLI 명령으로 전송하여 동시성을 달성합니다. 이 명령은 종료를 비정규화하고 자체 PHP 프로세스 내에서 호출합니다. 종료가 호출된 후， 결과 값이 상위 프로세스로 다시 직렬화됩니다。

`Concurrency` 정면은 `process`(기본값), `fork`, `sync` 의 세 가지 드라이버를 지원합니다。

`fork` 드라이버는 기본 `process` 드라이버에 비해 향상된 성능을 제공하지만， PHP 는 웹 요청 중 포킹을 지원하지 않으므로 PHP 의 CLI 컨텍스트 내에서만 사용할 수 있습니다. `fork` 드라이버를 사용하기 전에 `spatie/fork` 패키지를 설치해야 합니다：

```shell
composer require spatie/fork

```



`sync` 드라이버는 주로 테스트 중에 유용하며, 이때는 모든 동시성을 비활성화하고 주 프로세스 내에서 주어진 클로저를 순차적으로 실행하고자 할 때 사용됩니다.

<a name="running-concurrent-tasks"></a>
## 동시 작업 실행

동시 작업을 실행하려면 `Concurrency` 퍼사드의 `run` 메서드를 호출할 수 있습니다. `run` 메서드는 자식 PHP 프로세스에서 동시에 실행되어야 하는 클로저 배열을 받습니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
]);

```

특정 드라이버를 사용하려면 `driver` 방법을 사용할 수 있습니다:

```php
$results = Concurrency::driver('fork')->run(...);

```

또는 기본 동시성 드라이버를 변경하려면 `config:publish` Artisan 명령을 통해 `concurrency` 구성 파일을 게시하고 파일 내의 `default` 옵션을 업데이트해야 합니다:

```shell
php artisan config:publish concurrency

```

<a name="named-results"></a>
### 명명된 결과

위치가 아니라 이름으로 동시에 실행되는 작업 결과에 접근하고 싶다면, 닫힘(클로저)의 연관 배열을 제공할 수 있습니다. 각 결과는 해당 닫힘과 동일한 키를 사용하여 반환됩니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

$results = Concurrency::run([
    'users' => fn () => DB::table('users')->count(),
    'orders' => fn () => DB::table('orders')->count(),
]);

$userCount = $results['users'];
$orderCount = $results['orders'];

```

<a name="task-timeouts"></a>
### 작업 제한 시간

`process` 드라이버(기본)를 사용할 때, `run` 메서드에 제한 시간을 제공하여 동시 작업이 종료되기 전에 실행할 수 있는 최대 시간을 초 단위로 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\DB;

[$userCount, $orderCount] = Concurrency::run([
    fn () => DB::table('users')->count(),
    fn () => DB::table('orders')->count(),
], timeout: 30);

```

더 표현력 있는 타임아웃 정의를 원한다면 `CarbonInterval` 인스턴스를 제공할 수도 있습니다:

```php
use Illuminate\Support\Facades\Concurrency;

use function Illuminate\Support\seconds;

Concurrency::run([...], timeout: seconds(30));

```

<a name="deferring-concurrent-tasks"></a>
## 동시 작업 지연

클로저 배열을 동시에 실행하고 싶지만, 해당 클로저들이 반환하는 결과에는 관심이 없다면 `defer` 메서드를 사용하는 것을 고려해야 합니다. `defer` 메서드가 호출되면, 주어진 클로저는 즉시 실행되지 않습니다. 대신, Laravel은 HTTP 응답이 사용자에게 전송된 후 클로저를 동시에 실행합니다:

```php
use App\Services\Metrics;
use Illuminate\Support\Facades\Concurrency;

Concurrency::defer([
    fn () => Metrics::report('users'),
    fn () => Metrics::report('orders'),
]);

```
{% endraw %}
