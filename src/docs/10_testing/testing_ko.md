---
layout: docs
title: "테스트: 시작하기"
---

{% raw %}
# 테스트: 시작하기

- [소개](#introduction)
- 환경 (#environment)
- [Creating Tests](#creating-tests)
- [Running Tests](#running-tests)
- [병렬 실행 테스트](#running-tests-in-parallel)
- [보고 테스트 커버리지](#reporting-test-coverage)
- [프로파일링 테스트](#profiling-tests)
- [구성 캐싱](#configuration-caching)

<a name="introduction"></a>
## 소개

Laravel 은 테스트를 염두에 두고 제작되었습니다. 실제로 [Pest](https://pestphp.com) 및 [PHPUnit](https://phpunit.de) 을 사용한 테스트에 대한 지원이 기본적으로 포함되어 있으며， 애플리케이션에 대해 `phpunit.xml` 파일이 이미 설정되어 있습니다. 또한 프레임워크에는 애플리케이션을 명확하게 테스트할 수 있는 편리한 도우미 방법이 포함되어 있습니다。

기본적으로 애플리케이션의 `tests` 디렉토리에는 `Feature` 및 `Unit` 라는 두 디렉토리가 포함되어 있습니다. 단위 테스트는 코드의 매우 작고 격리된 부분에 초점을 맞춘 테스트입니다. 실제로 대부분의 단위 테스트는 아마도 단일 방법에 초점을 맞출 것입니다. “단위” 테스트 디렉토리 내의 테스트는 Laravel 애플리케이션을 부팅하지 않으므로 애플리케이션의 데이터베이스나 기타 프레임워크 서비스에 액세스할 수 없습니다。

기능 테스트는 여러 개체가 서로 상호 작용하는 방식 또는 JSON 엔드포인트에 대한 전체 HTTP 요청을 포함하여 코드의 더 큰 부분을 테스트할 수 있습니다. ** 일반적으로 테스트의 대부분은 기능 테스트여야 합니다. 이러한 유형의 테스트는 시스템 전체가 의도한 대로 작동하고 있다는 가장 큰 확신을 제공합니다. **

`ExampleTest.php` 파일은 `Feature` 및 `Unit` 테스트 디렉토리 모두에 제공됩니다. 새 Laravel 애플리케이션을 설치한 후 `vendor/bin/pest`, `vendor/bin/phpunit` 또는 `php artisan test` 명령을 실행하여 테스트를 실행합니다。

<a name="environment"></a>
## 환경

테스트를 실행할 때 Laravel 은 `phpunit.xml` 파일에 정의된 환경 변수로 인해 [구성 환경](/docs/{{version}}/configuration#environment-configuration) 을 자동으로 `testing` 로 설정합니다. Laravel 은 또한 테스트 중에 세션 또는 캐시 데이터가 유지되지 않도록 `array` 드라이버에 대한 세션 및 캐시를 자동으로 구성합니다。

필요에 따라 다른 테스트 환경 구성 값을 자유롭게 정의할 수 있습니다. `testing` 환경 변수는 애플리케이션의 `phpunit.xml` 파일에서 구성될 수 있지만， 테스트를 실행하기 전에 `config:clear` Artisan 명령을 사용하여 구성 캐시를 지워야 합니다！



<a name="the-env-testing-environment-file"></a>
#### `.env.testing` 환경 파일

또한, 프로젝트 루트에 `.env.testing` 파일을 생성할 수 있습니다. 이 파일은 Pest 및 PHPUnit 테스트를 실행하거나 `--env=testing` 옵션과 함께 Artisan 명령을 실행할 때 `.env` 파일 대신 사용됩니다.

<a name="creating-tests"></a>
## 테스트 생성

새로운 테스트 케이스를 생성하려면 `make:test` Artisan 명령을 사용하십시오. 기본적으로 테스트는 `tests/Feature` 디렉터리에 배치됩니다:

```shell
php artisan make:test UserTest

```



`tests/Unit` 디렉토리 내에서 테스트를 만들고 싶다면 `make:test` 명령을 실행할 때 `--unit` 옵션을 사용할 수 있습니다:

```shell
php artisan make:test UserTest --unit

```

만약 대부분 Laravel의 테스트 기능에 의존하는 테스트 클래스가 있지만, 특정 테스트 메서드는 프레임워크를 부팅할 필요가 없다면, 그 메서드에 `#[UnitTest]` 속성을 적용하여 해당 테스트에 대해서만 애플리케이션 부팅을 건너뛸 수 있습니다.

```

php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\Attributes\UnitTest;
use Tests\TestCase;

class LocationServiceTest extends TestCase
{
    public function test_get_coordinates_resolves_address(): void
    {
        // This test uses Laravel's testing features...
    }

    #[UnitTest]
    public function test_get_state_returns_state_from_abbreviation(): void
    {
        // This test runs without booting the application...
    }
}

```

> [!NOTE]
> 테스트 스텁은 [스텁 게시](/docs/{{version}}/artisan#stub-customization)를 사용하여 사용자 정의할 수 있습니다.

테스트가 생성되면, 통상적으로 Pest 또는 PHPUnit를 사용하여 테스트를 정의할 수 있습니다. 테스트를 실행하려면 터미널에서 `vendor/bin/pest`, `vendor/bin/phpunit`, 또는 `php artisan test` 명령어를 실행하세요:

```

php tab=Pest
<?php

test('basic', function () {
    expect(true)->toBeTrue();
});

```

```

php tab=PHPUnit
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $this->assertTrue(true);
    }
}

```

> [!WARNING]
> 테스트 클래스 내에서 자신의 `setUp` / `tearDown` 메서드를 정의하는 경우, 반드시 부모 클래스의 해당 `parent::setUp()` / `parent::tearDown()` 메서드를 호출해야 합니다. 일반적으로 자신의 `setUp` 메서드 시작 시 `parent::setUp()`를 호출하고, `tearDown` 메서드 끝에서는 `parent::tearDown()`를 호출해야 합니다.

<a name="running-tests"></a>
## 테스트 실행

앞서 언급했듯이, 테스트를 작성한 후에는 `pest` 또는 `phpunit`를 사용하여 이를 실행할 수 있습니다:

```

shell tab=Pest
./vendor/bin/pest

```

```

shell tab=PHPUnit
./vendor/bin/phpunit

```



`pest` 또는 `phpunit` 명령 외에도 `test` Artisan 명령을 사용하여 테스트를 실행할 수 있습니다. Artisan 테스트 러너는 개발 및 디버깅을 용이하게 하기 위해 상세한 테스트 보고서를 제공합니다:

```shell
php artisan test

```



`pest` 또는 `phpunit` 명령어에 전달할 수 있는 모든 인수는 Artisan `test` 명령어에도 전달할 수 있습니다:

```shell
php artisan test --testsuite=Feature --stop-on-failure

```

<a name="running-tests-in-parallel"></a>
### 테스트를 병렬로 실행하기

기본적으로 Laravel과 Pest / PHPUnit은 단일 프로세스 내에서 테스트를 순차적으로 실행합니다. 그러나 여러 프로세스에서 테스트를 동시에 실행하면 테스트 실행 시간을 크게 줄일 수 있습니다. 시작하려면 `brianium/paratest` Composer 패키지를 "dev" 의존성으로 설치해야 합니다. 그런 다음, `test` Artisan 명령을 실행할 때 `--parallel` 옵션을 포함하세요:

```shell
composer require brianium/paratest --dev

php artisan test --parallel

```

기본적으로 Laravel은 사용자의 기기에 있는 CPU 코어 수만큼 프로세스를 생성합니다. 그러나 `--processes` 옵션을 사용하여 프로세스 수를 조정할 수 있습니다:

```shell
php artisan test --parallel --processes=4

```

> [!WARNING]
> 테스트를 병렬로 실행할 때 일부 Pest / PHPUnit 옵션(`--do-not-cache-result` 등)은 사용이 불가능할 수 있습니다.

<a name="parallel-testing-and-databases"></a>
#### 병렬 테스트와 데이터베이스

기본 데이터베이스 연결을 구성한 경우, Laravel은 자동으로 각 병렬 프로세스에서 테스트 데이터베이스를 생성하고 마이그레이션합니다. 테스트 데이터베이스는 프로세스마다 고유한 프로세스 토큰이 접미사로 붙게 됩니다. 예를 들어, 두 개의 병렬 테스트 프로세스가 있는 경우, Laravel은 `your_db_test_1` 및 `your_db_test_2` 테스트 데이터베이스를 생성하고 사용합니다.

기본적으로 테스트 데이터베이스는 `test` Artisan 명령 호출 사이에서 유지되어, 이후 `test` 호출에서도 다시 사용할 수 있습니다. 하지만 `--recreate-databases` 옵션을 사용하여 다시 생성할 수도 있습니다:

```shell
php artisan test --parallel --recreate-databases

```

<a name="parallel-testing-hooks"></a>
#### 병렬 테스트 훅

가끔 애플리케이션 테스트에서 사용되는 특정 리소스를 준비해야 할 경우가 있으며, 이렇게 하면 여러 테스트 프로세스에서 안전하게 사용할 수 있습니다.

`ParallelTesting` 퍼사드를 사용하면 프로세스나 테스트 케이스의 `setUp`와 `tearDown`에서 실행될 코드를 지정할 수 있습니다. 주어진 클로저는 각각 프로세스 토큰과 현재 테스트 케이스를 포함하는 `$token`와 `$testCase` 변수를 받습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\ParallelTesting;
use Illuminate\Support\ServiceProvider;
use PHPUnit\Framework\TestCase;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        ParallelTesting::setUpProcess(function (int $token) {
            // ...
        });

        ParallelTesting::setUpTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        // Executed when a test database is created...
        ParallelTesting::setUpTestDatabase(function (string $database, int $token) {
            Artisan::call('db:seed');
        });

        ParallelTesting::tearDownTestCase(function (int $token, TestCase $testCase) {
            // ...
        });

        ParallelTesting::tearDownProcess(function (int $token) {
            // ...
        });
    }
}

```

<a name="accessing-the-parallel-testing-token"></a>
#### 병렬 테스트 토큰 접근

응용 프로그램의 테스트 코드에서 다른 위치에서 현재 병렬 프로세스 "토큰"에 접근하고 싶다면 `token` 메서드를 사용할 수 있습니다. 이 토큰은 개별 테스트 프로세스의 고유 문자열 식별자이며, 병렬 테스트 프로세스 간에 리소스를 분할하는 데 사용할 수 있습니다. 예를 들어, Laravel은 각 병렬 테스트 프로세스에서 생성된 테스트 데이터베이스 끝에 자동으로 이 토큰을 추가합니다:

$token = ParallelTesting::token();

<a name="reporting-test-coverage"></a>
### 테스트 커버리지 보고

> [!WARNING]
> 이 기능은 [Xdebug](https://xdebug.org) 또는 [PCOV](https://pecl.php.net/package/pcov)가 필요합니다.

응용 프로그램 테스트를 실행할 때 테스트 케이스가 실제로 응용 프로그램 코드를 얼마나 커버하는지, 테스트 실행 시 얼마나 많은 응용 프로그램 코드가 사용되는지를 확인하고 싶을 수 있습니다. 이를 달성하기 위해 `test` 명령을 호출할 때 `--coverage` 옵션을 제공할 수 있습니다:

```shell
php artisan test --coverage

```

<a name="enforcing-a-minimum-coverage-threshold"></a>
#### 최소 커버리지 기준 적용

응용 프로그램에 대한 최소 테스트 커버리지 기준을 정의하려면 `--min` 옵션을 사용할 수 있습니다. 이 기준이 충족되지 않으면 테스트 스위트가 실패합니다:

```shell
php artisan test --coverage --min=80.3

```

<a name="profiling-tests"></a>
### 프로파일링 테스트

아티산 테스트 러너에는 애플리케이션에서 가장 느린 테스트를 나열할 수 있는 편리한 메커니즘도 포함되어 있습니다. `test` 명령을 `--profile` 옵션과 함께 호출하면 가장 느린 10개의 테스트 목록이 표시되어 테스트 스위트를 더 빠르게 만들기 위해 개선할 수 있는 테스트를 쉽게 조사할 수 있습니다:

```shell
php artisan test --profile

```

<a name="configuration-caching"></a>
## 구성 캐싱

테스트를 실행할 때, Laravel은 각 개별 테스트 메서드마다 애플리케이션을 부트합니다. 캐시된 구성 파일이 없으면, 애플리케이션의 각 구성 파일을 테스트 시작 시 로드해야 합니다. 구성을 한 번만 빌드하고 단일 실행에서 모든 테스트에 재사용하려면, `Illuminate\Foundation\Testing\WithCachedConfig` 트레이트를 사용할 수 있습니다:

```

php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithCachedConfig;

pest()->use(WithCachedConfig::class);

// ...

```

```

php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithCachedConfig;
use Tests\TestCase;

class ConfigTest extends TestCase
{
    use WithCachedConfig;

    // ...
}

```
{% endraw %}
