---
layout: docs
title: "HTTP 테스트"
---

{% raw %}
---
layout: docs
title: "HTTP 테스트"
---

# HTTP 테스트

- [소개](#introduction)
- [요청 만들기](#making-requests)
    - [요청 헤더 사용자 정의](#customizing-request-headers)
    - [쿠키](#cookies)
    - [세션 / 인증](#session-and-authentication)
    - [응답 디버깅](#debugging-responses)
    - [예외 처리](#exception-handling)
- [JSON API 테스트](#testing-json-apis)
    - [유창한 JSON 테스트](#fluent-json-testing)
- [파일 업로드 테스트](#testing-file-uploads)
- [뷰 테스트](#testing-views)
    - [블레이드 및 컴포넌트 렌더링](#rendering-blade-and-components)
- [라우트 캐싱](#caching-routes)
- [사용 가능한 단언](#available-assertions)
    - [응답 단언](#response-assertions)
    - [인증 단언](#authentication-assertions)
    - [검증 단언](#validation-assertions)

<a name="introduction"></a>
## 소개

Laravel은 애플리케이션에 HTTP 요청을 보내고 응답을 검토할 수 있는 매우 유창한 API를 제공합니다. 예를 들어, 아래 정의된 기능 테스트를 살펴보세요:```php tab=Pest
<?php

test('the application returns a successful response', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_the_application_returns_a_successful_response(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```



`get` 메서드는 애플리케이션에 `GET` 요청을 보내고, `assertStatus` 메서드는 반환된 응답이 주어진 HTTP 상태 코드를 가져야 한다고 단언합니다. 이 단순한 단언 외에도, Laravel은 응답 헤더, 내용, JSON 구조 등을 검사하기 위한 다양한 단언을 포함하고 있습니다.

<a name="making-requests"></a>
## 요청 만들기

애플리케이션에 요청을 만들기 위해 테스트 내에서 `get`, `post`, `put`, `patch` 또는 `delete` 메서드를 호출할 수 있습니다. 이 메서드들은 실제로 애플리케이션에 "실제" HTTP 요청을 보내지 않습니다. 대신 전체 네트워크 요청이 내부적으로 시뮬레이션됩니다.

`Illuminate\Http\Response` 인스턴스를 반환하는 대신, 테스트 요청 메서드는 `Illuminate\Testing\TestResponse` 인스턴스를 반환하며, 이는 애플리케이션의 응답을 검사할 수 있는 [다양한 유용한 단언](#available-assertions)을 제공합니다:```php tab=Pest
<?php

test('basic request', function () {
    $response = $this->get('/');

    $response->assertStatus(200);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_a_basic_request(): void
    {
        $response = $this->get('/');

        $response->assertStatus(200);
    }
}
```



일반적으로 각 테스트는 애플리케이션에 단일 요청만 해야 합니다. 단일 테스트 메서드 내에서 여러 요청이 실행되면 예상치 못한 동작이 발생할 수 있습니다.

> [!NOTE]
> 편의를 위해 테스트를 실행할 때 CSRF 미들웨어는 자동으로 비활성화됩니다.

<a name="customizing-request-headers"></a>
### 요청 헤더 사용자 정의

애플리케이션에 요청을 보내기 전에 요청의 헤더를 사용자 정의하려면 `withHeaders` 메서드를 사용할 수 있습니다. 이 메서드를 사용하면 요청에 원하는 모든 사용자 정의 헤더를 추가할 수 있습니다:```php tab=Pest
<?php

test('interacting with headers', function () {
    $response = $this->withHeaders([
        'X-Header' => 'Value',
    ])->post('/user', ['name' => 'Sally']);

    $response->assertStatus(201);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_interacting_with_headers(): void
    {
        $response = $this->withHeaders([
            'X-Header' => 'Value',
        ])->post('/user', ['name' => 'Sally']);

        $response->assertStatus(201);
    }
}
```



<a name="cookies"></a>
### 쿠키

요청을 하기 전에 `withCookie` 또는 `withCookies` 메서드를 사용하여 쿠키 값을 설정할 수 있습니다. `withCookie` 메서드는 쿠키 이름과 값을 두 개의 인수로 받아들이며, `withCookies` 메서드는 이름/값 쌍의 배열을 받아들입니다:```php tab=Pest
<?php

test('interacting with cookies', function () {
    $response = $this->withCookie('color', 'blue')->get('/');

    $response = $this->withCookies([
        'color' => 'blue',
        'name' => 'Taylor',
    ])->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_cookies(): void
    {
        $response = $this->withCookie('color', 'blue')->get('/');

        $response = $this->withCookies([
            'color' => 'blue',
            'name' => 'Taylor',
        ])->get('/');

        //
    }
}
```



<a name="session-and-authentication"></a>
### 세션 / 인증

Laravel은 HTTP 테스트 중에 세션과 상호작용할 수 있는 여러 헬퍼를 제공합니다. 먼저, `withSession` 메서드를 사용하여 세션 데이터를 주어진 배열로 설정할 수 있습니다. 이는 애플리케이션에 요청을 보내기 전에 세션에 데이터를 로드하는 데 유용합니다:```php tab=Pest
<?php

test('interacting with the session', function () {
    $response = $this->withSession(['banned' => false])->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_interacting_with_the_session(): void
    {
        $response = $this->withSession(['banned' => false])->get('/');

        //
    }
}
```



라라벨의 세션은 일반적으로 현재 인증된 사용자의 상태를 유지하는 데 사용됩니다. 따라서 `actingAs` 헬퍼 메서드는 특정 사용자를 현재 사용자로 인증하는 간단한 방법을 제공합니다. 예를 들어, 우리는 [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용하여 사용자를 생성하고 인증할 수 있습니다:```php tab=Pest
<?php

use App\Models\User;

test('an action that requires authentication', function () {
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->withSession(['banned' => false])
        ->get('/');

    //
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_an_action_that_requires_authentication(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
            ->withSession(['banned' => false])
            ->get('/');

        //
    }
}
```



`actingAs` 메서드에 두 번째 인수로 가드 이름을 전달하면 주어진 사용자를 인증하는 데 사용할 가드를 지정할 수도 있습니다. `actingAs` 메서드에 제공된 가드는 테스트 기간 동안 기본 가드가 되기도 합니다:

```php
$this->actingAs($user, 'web');
```



요청이 인증되지 않았는지 확인하고 싶다면, `actingAsGuest` 방법을 사용할 수 있습니다:

```php
$this->actingAsGuest();
```



<a name="debugging-responses"></a>
### 응답 디버깅

애플리케이션에 테스트 요청을 한 후, `dump`, `dumpHeaders`, 및 `dumpSession` 메서드를 사용하여 응답 내용을 검사하고 디버깅할 수 있습니다:```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dump();
    $response->dumpHeaders();
    $response->dumpSession();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dump();
        $response->dumpHeaders();
        $response->dumpSession();
    }
}
```



또는 `dd`, `ddHeaders`, `ddBody`, `ddJson`, `ddSession` 메서드를 사용하여 응답에 대한 정보를 추출한 후 실행을 중지할 수 있습니다:```php tab=Pest
<?php

test('basic test', function () {
    $response = $this->get('/');

    $response->dd();
    $response->ddHeaders();
    $response->ddBody();
    $response->ddJson();
    $response->ddSession();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_basic_test(): void
    {
        $response = $this->get('/');

        $response->dd();
        $response->ddHeaders();
        $response->ddBody();
        $response->ddJson();
        $response->ddSession();
    }
}
```



<a name="exception-handling"></a>
### 예외 처리

때때로 애플리케이션이 특정 예외를 발생시키는지 테스트해야 할 수 있습니다. 이를 달성하기 위해, `Exceptions` 퍼사드를 통해 예외 처리기를 '가짜'로 만들 수 있습니다. 예외 처리기가 가짜로 설정되면, `assertReported` 및 `assertNotReported` 메서드를 사용하여 요청 중에 발생한 예외에 대해 단언(assertion)을 수행할 수 있습니다:```php tab=Pest
<?php

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;

test('exception is thrown', function () {
    Exceptions::fake();

    $response = $this->get('/order/1');

    // Assert an exception was thrown...
    Exceptions::assertReported(InvalidOrderException::class);

    // Assert against the exception...
    Exceptions::assertReported(function (InvalidOrderException $e) {
        return $e->getMessage() === 'The order was invalid.';
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Exceptions\InvalidOrderException;
use Illuminate\Support\Facades\Exceptions;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic test example.
     */
    public function test_exception_is_thrown(): void
    {
        Exceptions::fake();

        $response = $this->get('/');

        // Assert an exception was thrown...
        Exceptions::assertReported(InvalidOrderException::class);

        // Assert against the exception...
        Exceptions::assertReported(function (InvalidOrderException $e) {
            return $e->getMessage() === 'The order was invalid.';
        });
    }
}
```



`assertNotReported` 및 `assertNothingReported` 메서드는 요청 중에 특정 예외가 발생하지 않았음을 확인하거나 예외가 전혀 발생하지 않았음을 확인하는 데 사용할 수 있습니다:

```php
Exceptions::assertNotReported(InvalidOrderException::class);

Exceptions::assertNothingReported();
```



요청을 하기 전에 `withoutExceptionHandling` 메서드를 호출하여 특정 요청에 대한 예외 처리를 완전히 비활성화할 수 있습니다:

```php
$response = $this->withoutExceptionHandling()->get('/');
```



또한, 애플리케이션이 PHP 언어나 사용하는 라이브러리에서 폐기된 기능을 사용하지 않는지 확인하고 싶다면, 요청을 하기 전에 `withoutDeprecationHandling` 메서드를 호출할 수 있습니다. 폐기성 처리가 비활성화되면 폐기성 경고가 예외로 전환되어 테스트가 실패하게 됩니다:

```php
$response = $this->withoutDeprecationHandling()->get('/');
```



`assertThrows` 방법은 주어진 클로저 내의 코드가 지정된 유형의 예외를 발생시키는지 확인하는 데 사용할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    OrderInvalid::class
);
```



만약 발생한 예외를 검사하고 주장(assertions)을 하고 싶다면, `assertThrows` 메서드의 두 번째 인자로 클로저를 제공할 수 있습니다:

```php
$this->assertThrows(
    fn () => (new ProcessOrder)->execute(),
    fn (OrderInvalid $e) => $e->orderId() === 123
);
```



`assertDoesntThrow` 방법은 주어진 클로저 안의 코드가 어떠한 예외도 발생시키지 않는다고 주장하는 데 사용될 수 있습니다:

```php
$this->assertDoesntThrow(fn () => (new ProcessOrder)->execute());
```



<a name="testing-json-apis"></a>
## JSON API 테스트

Laravel은 JSON API와 그 응답을 테스트하기 위한 여러 헬퍼도 제공합니다. 예를 들어, `json`, `getJson`, `postJson`, `putJson`, `patchJson`, `deleteJson`, `optionsJson` 메소드를 사용하여 다양한 HTTP 동사로 JSON 요청을 보낼 수 있습니다. 또한 이러한 메소드에 데이터와 헤더를 쉽게 전달할 수 있습니다. 시작하려면 `/api/user`에 `POST` 요청을 보내고 예상된 JSON 데이터가 반환되었는지 확인하는 테스트를 작성해 보겠습니다:```php tab=Pest
<?php

test('making an api request', function () {
    $response = $this->postJson('/api/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJson([
            'created' => true,
        ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_making_an_api_request(): void
    {
        $response = $this->postJson('/api/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJson([
                'created' => true,
            ]);
    }
}
```



또한, JSON 응답 데이터는 응답에서 배열 변수로 접근할 수 있어 JSON 응답 내에서 반환된 개별 값을 확인하는 데 편리합니다:```php tab=Pest
expect($response['created'])->toBeTrue();
```

```php tab=PHPUnit
$this->assertTrue($response['created']);
```



> [!NOTE]
> `assertJson` 메서드는 응답을 배열로 변환하여 주어진 배열이 애플리케이션이 반환한 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 있더라도, 주어진 조각이 존재한다면 이 테스트는 여전히 통과합니다.

<a name="verifying-exact-match"></a>
#### 정확한 JSON 일치 여부 검증

앞서 언급한 바와 같이, `assertJson` 메서드는 JSON 응답 내에 JSON 조각이 존재하는지 검증하는 데 사용될 수 있습니다. 만약 주어진 배열이 애플리케이션이 반환한 JSON과 **정확히 일치하는지** 확인하고 싶다면, `assertExactJson` 메서드를 사용해야 합니다:```php tab=Pest
<?php

test('asserting an exact json match', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertExactJson([
            'created' => true,
        ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_asserting_an_exact_json_match(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertExactJson([
                'created' => true,
            ]);
    }
}
```



<a name="verifying-json-paths"></a>
#### JSON 경로에서 어설션하기

JSON 응답에 지정된 경로에 주어진 데이터가 포함되어 있는지 확인하고 싶다면, `assertJsonPath` 방법을 사용해야 합니다:```php tab=Pest
<?php

test('asserting a json path value', function () {
    $response = $this->postJson('/user', ['name' => 'Sally']);

    $response
        ->assertStatus(201)
        ->assertJsonPath('team.owner.name', 'Darian');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * A basic functional test example.
     */
    public function test_asserting_a_json_paths_value(): void
    {
        $response = $this->postJson('/user', ['name' => 'Sally']);

        $response
            ->assertStatus(201)
            ->assertJsonPath('team.owner.name', 'Darian');
    }
}
```



`assertJsonPath` 방법은 또한 클로저를 허용하며, 이를 사용하여 단언이 통과해야 하는지를 동적으로 결정할 수 있습니다:

```php
$response->assertJsonPath('team.owner.name', fn (string $name) => strlen($name) >= 3);
```



여러 JSON 경로를 한 번에 검증해야 하는 경우, `assertJsonPaths` 방법을 사용할 수 있습니다. 각 경로에 대한 예상 값은 클로저일 수도 있습니다:

```php
$response->assertJsonPaths([
    'team.owner.name' => 'Darian',
    'team.owner.email' => fn (string $email) => str($email)->is('*@laravel.com'),
    'team.members.0.name' => 'Sally',
]);
```



응답에서 여러 JSON 경로가 누락되었음을 주장하기 위해 `assertJsonMissingPaths` 방법을 사용할 수 있습니다:

```php
$response->assertJsonMissingPaths([
    'team.owner.password',
    'team.members.0.api_token',
]);
```



<a name="fluent-json-testing"></a>
### 유창한 JSON 테스트

Laravel은 또한 애플리케이션의 JSON 응답을 유창하게 테스트할 수 있는 아름다운 방법을 제공합니다. 시작하려면 `assertJson` 메서드에 클로저를 전달하면 됩니다. 이 클로저는 애플리케이션에서 반환된 JSON에 대해 검증을 수행할 수 있는 `Illuminate\Testing\Fluent\AssertableJson` 인스턴스와 함께 호출됩니다. `where` 메서드는 JSON의 특정 속성에 대해 검증을 수행하는 데 사용할 수 있으며, `missing` 메서드는 JSON에서 특정 속성이 누락되었는지 검증하는 데 사용할 수 있습니다:```php tab=Pest
use Illuminate\Testing\Fluent\AssertableJson;

test('fluent json', function () {
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                ->where('name', 'Victoria Faith')
                ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                ->whereNot('status', 'pending')
                ->missing('password')
                ->etc()
        );
});
```

```php tab=PHPUnit
use Illuminate\Testing\Fluent\AssertableJson;

/**
 * A basic functional test example.
 */
public function test_fluent_json(): void
{
    $response = $this->getJson('/users/1');

    $response
        ->assertJson(fn (AssertableJson $json) =>
            $json->where('id', 1)
                ->where('name', 'Victoria Faith')
                ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                ->whereNot('status', 'pending')
                ->missing('password')
                ->etc()
        );
}
```



#### Understanding the `etc` Method

In the example above, you may have noticed we invoked the `etc` method at the end of our assertion chain. This method informs Laravel that there may be other attributes present on the JSON object. If the `etc` method is not used, the test will fail if other attributes that you did not make assertions against exist on the JSON object.

The intention behind this behavior is to protect you from unintentionally exposing sensitive information in your JSON responses by forcing you to either explicitly make an assertion against the attribute or explicitly allow additional attributes via the `etc` method.

However, you should be aware that not including the `etc` method in your assertion chain does not ensure that additional attributes are not being added to arrays that are nested within your JSON object. The `etc` method only ensures that no additional attributes exist at the nesting level in which the `etc` method is invoked.

<a name="asserting-json-attribute-presence-and-absence"></a>
#### Asserting Attribute Presence / Absence

To assert that an attribute is present or absent, you may use the `has` and `missing` methods:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('data')
        ->missing('message')
);
```



또한, `hasAll` 및 `missingAll` 메서드는 여러 속성의 존재 여부를 동시에 확인할 수 있게 합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->hasAll(['status', 'data'])
        ->missingAll(['message', 'code'])
);
```



다음과 같이 `hasAny` 방법을 사용하여 주어진 속성 목록 중 적어도 하나가 존재하는지 확인할 수 있습니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->has('status')
        ->hasAny('data', 'message', 'code')
);
```



<a name="asserting-against-json-collections"></a>
#### JSON 컬렉션에 대한 검증

종종, 당신의 경로는 여러 개의 항목을 포함하는 JSON 응답을 반환할 것입니다, 예를 들어 여러 사용자를:

```php
Route::get('/users', function () {
    return User::all();
});
```



이러한 상황에서, 우리는 응답에 포함된 사용자에 대해 단언을 하기 위해 fluent JSON 객체의 `has` 메서드를 사용할 수 있습니다. 예를 들어, JSON 응답에 세 명의 사용자가 포함되어 있는지 단언해 봅시다. 다음으로, `first` 메서드를 사용하여 컬렉션의 첫 번째 사용자에 대한 몇 가지 단언을 하겠습니다. `first` 메서드는 클로저를 받아들이며, 이 클로저는 우리가 JSON 컬렉션의 첫 번째 객체에 대해 단언을 할 수 있는 또 다른 단언 가능한 JSON 문자열을 받습니다:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has(3)
            ->first(fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```



JSON 컬렉션의 모든 항목에 대해 동일한 주장을 하고 싶다면, `each` 메서드를 사용할 수 있습니다:

```php
$response
  ->assertJson(fn (AssertableJson $json) =>
      $json->has(3)
          ->each(fn (AssertableJson $json) =>
              $json->whereType('id', 'integer')
                  ->whereType('name', 'string')
                  ->whereType('email', 'string')
                  ->missing('password')
                  ->etc()
          )
  );
```



<a name="scoping-json-collection-assertions"></a>
#### JSON 컬렉션 어설션 범위 지정

때때로, 애플리케이션의 라우트가 이름이 지정된 키에 할당된 JSON 컬렉션을 반환하기도 합니다:

```php
Route::get('/users', function () {
    return [
        'meta' => [...],
        'users' => User::all(),
    ];
})
```



이 경로를 테스트할 때 `has` 메서드를 사용하여 컬렉션의 항목 수를 확인할 수 있습니다. 또한 `has` 메서드를 사용하여 일련의 검증 범위를 지정할 수 있습니다:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
            ->has('users', 3)
            ->has('users.0', fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```



그러나 `users` 컬렉션에 대해 `has` 메서드를 두 번 호출하는 대신, 세 번째 매개변수로 클로저를 제공하는 단일 호출을 할 수 있습니다. 이렇게 하면 클로저가 자동으로 호출되며 컬렉션의 첫 번째 항목에 범위가 지정됩니다:

```php
$response
    ->assertJson(fn (AssertableJson $json) =>
        $json->has('meta')
            ->has('users', 3, fn (AssertableJson $json) =>
                $json->where('id', 1)
                    ->where('name', 'Victoria Faith')
                    ->where('email', fn (string $email) => str($email)->is('victoria@gmail.com'))
                    ->missing('password')
                    ->etc()
            )
    );
```



<a name="asserting-json-types"></a>
#### JSON 유형 확인

JSON 응답의 속성이 특정 유형인지 확인하고 싶을 수 있습니다. `Illuminate\Testing\Fluent\AssertableJson` 클래스는 바로 이를 위해 `whereType` 및 `whereAllType` 메서드를 제공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('id', 'integer')
        ->whereAllType([
            'users.0.name' => 'string',
            'meta' => 'array'
        ])
);
```



`|` 문자를 사용하여 여러 유형을 지정하거나, `whereType` 메서드의 두 번째 매개변수로 유형 배열을 전달할 수 있습니다. 응답 값이 나열된 유형 중 어느 것이든 일치하면 단언이 성공합니다:

```php
$response->assertJson(fn (AssertableJson $json) =>
    $json->whereType('name', 'string|null')
        ->whereType('id', ['string', 'integer'])
);
```



`whereType` 및 `whereAllType` 메서드는 다음 유형을 인식합니다: `string`, `integer`, `double`, `boolean`, `array`, 및 `null`.

<a name="testing-file-uploads"></a>
## 파일 업로드 테스트

`Illuminate\Http\UploadedFile` 클래스는 테스트용 더미 파일 또는 이미지를 생성하는 데 사용할 수 있는 `fake` 메서드를 제공합니다. 이는 `Storage` 퍼사드의 `fake` 메서드와 결합될 때 파일 업로드 테스트를 크게 단순화합니다. 예를 들어, 이 두 기능을 결합하여 아바타 업로드 폼을 쉽게 테스트할 수 있습니다:```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('avatars can be uploaded', function () {
    Storage::fake('avatars');

    $file = UploadedFile::fake()->image('avatar.jpg');

    $response = $this->post('/avatar', [
        'avatar' => $file,
    ]);

    Storage::disk('avatars')->assertExists($file->hashName());
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_avatars_can_be_uploaded(): void
    {
        Storage::fake('avatars');

        $file = UploadedFile::fake()->image('avatar.jpg');

        $response = $this->post('/avatar', [
            'avatar' => $file,
        ]);

        Storage::disk('avatars')->assertExists($file->hashName());
    }
}
```



주어진 파일이 존재하지 않음을 주장하고 싶다면, `Storage` 퍼사드에서 제공하는 `assertMissing` 메서드를 사용할 수 있습니다:

```php
Storage::fake('avatars');

// ...

Storage::disk('avatars')->assertMissing('missing.jpg');
```



<a name="fake-file-customization"></a>
#### 가짜 파일 커스터마이징

`UploadedFile` 클래스에서 제공하는 `fake` 방법을 사용하여 파일을 생성할 때, 애플리케이션의 검증 규칙을 더 잘 테스트하기 위해 이미지의 너비, 높이 및 크기(킬로바이트 단위)를 지정할 수 있습니다:

```php
UploadedFile::fake()->image('avatar.jpg', $width, $height)->size(100);
```



이미지를 생성하는 것 외에도, `create` 방법을 사용하여 다른 유형의 파일을 생성할 수 있습니다:

```php
UploadedFile::fake()->create('document.pdf', $sizeInKilobytes);
```



필요한 경우, 메서드에 `$mimeType` 인수를 전달하여 파일이 반환해야 하는 MIME 유형을 명시적으로 정의할 수 있습니다:

```php
UploadedFile::fake()->create(
    'document.pdf', $sizeInKilobytes, 'application/pdf'
);
```



<a name="testing-views"></a>
## 뷰 테스트하기

Laravel은 또한 애플리케이션에 대한 모의 HTTP 요청을 생성하지 않고도 뷰를 렌더링 할 수 있게 해줍니다. 이를 수행하려면 테스트 내에서 `view` 메서드를 호출할 수 있습니다. `view` 메서드는 뷰 이름과 선택적인 데이터 배열을 받습니다. 이 메서드는 `Illuminate\Testing\TestView` 인스턴스를 반환하며, 이 인스턴스를 통해 뷰의 내용을 편리하게 검증할 수 있는 여러 메서드를 제공합니다:```php tab=Pest
<?php

test('a welcome view can be rendered', function () {
    $view = $this->view('welcome', ['name' => 'Taylor']);

    $view->assertSee('Taylor');
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_a_welcome_view_can_be_rendered(): void
    {
        $view = $this->view('welcome', ['name' => 'Taylor']);

        $view->assertSee('Taylor');
    }
}
```



`TestView` 클래스는 다음과 같은 검증(assertion) 메서드를 제공합니다: `assertSee`, `assertSeeInOrder`, `assertSeeText`, `assertSeeTextInOrder`, `assertDontSee`, 그리고 `assertDontSeeText`.

필요하다면, `TestView` 인스턴스를 문자열로 캐스팅하여 원시(raw) 렌더링된 뷰 컨텐츠를 얻을 수 있습니다:

```php
$contents = (string) $this->view('welcome');
```



<a name="sharing-errors"></a>
#### 오류 공유

일부 뷰는 [Laravel에서 제공하는 글로벌 오류 백](/docs/{{version}}/validation#quick-displaying-the-validation-errors)에 공유된 오류에 따라 달라질 수 있습니다. 오류 메시지로 오류 백을 채우려면, `withViewErrors` 메서드를 사용할 수 있습니다:

```php
$view = $this->withViewErrors([
    'name' => ['Please provide a valid name.']
])->view('form');

$view->assertSee('Please provide a valid name.');
```



<a name="rendering-blade-and-components"></a>
### 블레이드와 컴포넌트 렌더링

필요한 경우, `blade` 메서드를 사용하여 원시 [Blade](/docs/{{version}}/blade) 문자열을 평가하고 렌더링할 수 있습니다. `view` 메서드와 마찬가지로, `blade` 메서드는 `Illuminate\Testing\TestView`의 인스턴스를 반환합니다:

```php
$view = $this->blade(
    '<x-component :name="$name" />',
    ['name' => 'Taylor']
);

$view->assertSee('Taylor');
```



`component` 메서드를 사용하여 [Blade 컴포넌트](/docs/{{version}}/blade#components)를 평가하고 렌더링할 수 있습니다. `component` 메서드는 `Illuminate\Testing\TestComponent` 인스턴스를 반환합니다:

```php
$view = $this->component(Profile::class, ['name' => 'Taylor']);

$view->assertSee('Taylor');
```



<a name="caching-routes"></a>
## 라우트 캐싱

테스트가 실행되기 전에 Laravel은 애플리케이션의 새로운 인스턴스를 부트하며, 여기에는 정의된 모든 라우트 수집이 포함됩니다. 애플리케이션에 많은 라우트 파일이 있는 경우, 테스트 케이스에 `Illuminate\Foundation\Testing\WithCachedRoutes` 트레이트를 추가하는 것이 좋습니다. 이 트레이트를 사용하는 테스트에서는 라우트가 한 번만 빌드되어 메모리에 저장되므로, 라우트 수집 과정이 테스트 스위트 전체에 대해 한 번만 실행됩니다:```php tab=Pest
<?php

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;

pest()->use(WithCachedRoutes::class);

test('basic example', function () {
    $this->get(action([UserController::class, 'index']));

    // ...
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Http\Controllers\UserController;
use Illuminate\Foundation\Testing\WithCachedRoutes;
use Tests\TestCase;

class BasicTest extends TestCase
{
    use WithCachedRoutes;

    /**
     * A basic functional test example.
     */
    public function test_basic_example(): void
    {
        $response = $this->get(action([UserController::class, 'index']));

        // ...
    }
}
```

<a name="available-assertions"></a>
## 사용 가능한 어서션

<a name="response-assertions"></a>
### 응답 어서션

Laravel의 `Illuminate\Testing\TestResponse` 클래스는 애플리케이션을 테스트할 때 사용할 수 있는 다양한 커스텀 어서션 메서드를 제공합니다. 이러한 어서션은 `json`, `get`, `post`, `put`, `delete` 테스트 메서드가 반환하는 응답에서 접근할 수 있습니다.

<style>
    .collection-method-list > p {
        columns: 14.4em 2; -moz-columns: 14.4em 2; -webkit-columns: 14.4em 2;
    }

.collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

<div class="collection-method-list" markdown="1">

[assertAccepted](#assert-accepted)
[assertBadRequest](#assert-bad-request)
[assertClientError](#assert-client-error)
[assertConflict](#assert-conflict)
[assertCookie](#assert-cookie)
[assertCookieExpired](#assert-cookie-expired)
[assertCookieNotExpired](#assert-cookie-not-expired)
[assertCookieMissing](#assert-cookie-missing)
[assertCreated](#assert-created)
[assertDontSee](#assert-dont-see)
[assertDontSeeText](#assert-dont-see-text)
[assertDownload](#assert-download)
[assertExactJson](#assert-exact-json)
[assertExactJsonStructure](#assert-exact-json-structure)
[assertFailedDependency](#assert-failed-dependency)
[assertForbidden](#assert-forbidden)
[assertFound](#assert-found)
[assertGone](#assert-gone)
[assertHeader](#assert-header)
[assertHeaderContains](#assert-header-contains)
[assertHeaderMissing](#assert-header-missing)
[assertInternalServerError](#assert-internal-server-error)
[assertJson](#assert-json)
[assertJsonCount](#assert-json-count)
[assertJsonFragment](#assert-json-fragment)
[assertJsonIsArray](#assert-json-is-array)
[assertJsonIsObject](#assert-json-is-object)
[assertJsonMissing](#assert-json-missing)
[assertJsonMissingExact](#assert-json-missing-exact)
[assertJsonMissingValidationErrors](#assert-json-missing-validation-errors)
[assertJsonPath](#assert-json-path)
[assertJsonPaths](#assert-json-paths)
[assertJsonMissingPath](#assert-json-missing-path)
[assertJsonMissingPaths](#assert-json-missing-paths)
[assertJsonStructure](#assert-json-structure)
[assertJsonValidationErrors](#assert-json-validation-errors)
[assertJsonValidationErrorFor](#assert-json-validation-error-for)
[assertLocation](#assert-location)
[assertMethodNotAllowed](#assert-method-not-allowed)
[assertMovedPermanently](#assert-moved-permanently)
[assertContent](#assert-content)
[assertNoContent](#assert-no-content)
[assertStreamed](#assert-streamed)
[assertStreamedContent](#assert-streamed-content)
[assertNotFound](#assert-not-found)
[assertOk](#assert-ok)
[assertPaymentRequired](#assert-payment-required)
[assertPlainCookie](#assert-plain-cookie)
[assertRedirect](#assert-redirect)
[assertRedirectBack](#assert-redirect-back)
[assertRedirectBackWithErrors](#assert-redirect-back-with-errors)
[assertRedirectBackWithoutErrors](#assert-redirect-back-without-errors)
[assertRedirectContains](#assert-redirect-contains)
[assertRedirectToRoute](#assert-redirect-to-route)
[assertRedirectToSignedRoute](#assert-redirect-to-signed-route)
[assertRequestTimeout](#assert-request-timeout)
[assertSee](#assert-see)
[assertSeeInOrder](#assert-see-in-order)
[assertSeeText](#assert-see-text)
[assertSeeTextInOrder](#assert-see-text-in-order)
[assertServerError](#assert-server-error)
[assertServiceUnavailable](#assert-service-unavailable)
[assertSessionHas](#assert-session-has)
[assertSessionHasInput](#assert-session-has-input)
[assertSessionHasAll](#assert-session-has-all)
[assertSessionHasErrors](#assert-session-has-errors)
[assertSessionHasErrorsIn](#assert-session-has-errors-in)
[assertSessionHasNoErrors](#assert-session-has-no-errors)
[assertSessionDoesntHaveErrors](#assert-session-doesnt-have-errors)
[assertSessionMissing](#assert-session-missing)
[assertSessionMissingInput](#assert-session-missing-input)
[assertStatus](#assert-status)
[assertSuccessful](#assert-successful)
[assertTooManyRequests](#assert-too-many-requests)
[assertUnauthorized](#assert-unauthorized)
[assertUnprocessable](#assert-unprocessable)
[assertUnsupportedMediaType](#assert-unsupported-media-type)
[assertValid](#assert-valid)
[assertInvalid](#assert-invalid)
[assertViewHas](#assert-view-has)
[assertViewHasAll](#assert-view-has-all)
[assertViewIs](#assert-view-is)
[assertViewMissing](#assert-view-missing)



</div>

<a name="assert-accepted"></a>
#### assertAccepted

응답이 허용된(202) HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertAccepted();
```



<a name="assert-bad-request"></a>
#### 잘못된 요청(assertBadRequest) 확인

응답이 잘못된 요청(400) HTTP 상태 코드를 가지는지 확인합니다:

```php
$response->assertBadRequest();
```



<a name="assert-client-error"></a>
#### assertClientError

응답이 클라이언트 오류(HTTP 상태 코드 >= 400, < 500)를 가지고 있는지 확인합니다:

```php
$response->assertClientError();
```



<a name="assert-conflict"></a>
#### assertConflict

응답이 충돌(409) HTTP 상태 코드를 가지고 있는지 확인하세요:

```php
$response->assertConflict();
```



<a name="assert-cookie"></a>
#### assertCookie

응답에 주어진 쿠키가 포함되어 있는지 확인하세요:

```php
$response->assertCookie($cookieName, $value = null);
```



<a name="assert-cookie-expired"></a>
#### assertCookieExpired

응답에 지정된 쿠키가 포함되어 있으며 해당 쿠키가 만료되었는지 확인합니다:

```php
$response->assertCookieExpired($cookieName);
```



<a name="assert-cookie-not-expired"></a>
#### assertCookieNotExpired

응답에 지정된 쿠키가 포함되어 있고 만료되지 않았는지 확인합니다:

```php
$response->assertCookieNotExpired($cookieName);
```



<a name="assert-cookie-missing"></a>
#### assertCookieMissing

응답에 지정된 쿠키가 포함되어 있지 않음을 확인합니다:

```php
$response->assertCookieMissing($cookieName);
```



<a name="assert-created"></a>
#### assertCreated

응답이 201 HTTP 상태 코드를 가지고 있는지 확인하세요:

```php
$response->assertCreated();
```



<a name="assert-dont-see"></a>
#### assertDontSee

주어진 문자열이 애플리케이션에서 반환된 응답에 포함되어 있지 않음을 확인합니다. 이 검증은 두 번째 인수로 `false`를 전달하지 않는 한 주어진 문자열을 자동으로 이스케이프합니다.

```php
$response->assertDontSee($value, $escape = true);
```



<a name="assert-dont-see-text"></a>
#### assertDontSeeText

주어진 문자열이 응답 텍스트에 포함되어 있지 않음을 확인합니다. 이 검증은 두 번째 인자로 `false`를 전달하지 않는 한 주어진 문자열을 자동으로 이스케이프 합니다. 이 메서드는 검증을 수행하기 전에 응답 내용을 `strip_tags` PHP 함수에 전달합니다:

```php
$response->assertDontSeeText($value, $escape = true);
```



<a name="assert-download"></a>
#### assertDownload

응답이 "다운로드"인지 확인합니다. 일반적으로 이는 호출된 경로가 반환한 응답이 `Response::download` 응답, `BinaryFileResponse`, 또는 `Storage::download` 응답을 반환했음을 의미합니다:

```php
$response->assertDownload();
```



원하신다면, 다운로드 가능한 파일에 지정된 파일 이름이 할당되었다고 주장할 수 있습니다:

```php
$response->assertDownload('image.jpg');
```



<a name="assert-exact-json"></a>
#### assertExactJson

응답이 주어진 JSON 데이터와 정확히 일치하는지 확인하십시오:

```php
$response->assertExactJson(array $data);
```



<a name="assert-exact-json-structure"></a>
#### assertExactJsonStructure

응답이 주어진 JSON 구조와 정확히 일치하는지 확인합니다:

```php
$response->assertExactJsonStructure(array $data);
```



이 방법은 [assertJsonStructure](#assert-json-structure)의 보다 엄격한 변형입니다. `assertJsonStructure`와 달리, 이 방법은 응답에 예상 JSON 구조에 명시적으로 포함되지 않은 키가 포함되어 있으면 실패합니다.

<a name="assert-failed-dependency"></a>
#### assertFailedDependency

응답이 실패한 종속성(424) HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertFailedDependency();
```



<a name="assert-forbidden"></a>
#### assertForbidden

응답이 금지된(403) HTTP 상태 코드를 가지고 있는지 확인하십시오:

```php
$response->assertForbidden();
```



<a name="assert-found"></a>
#### assertFound

응답이 발견됨(302) HTTP 상태 코드를 가지고 있는지 확인:

```php
$response->assertFound();
```



<a name="assert-gone"></a>
#### assertGone

응답이 gone(410) HTTP 상태 코드를 가지고 있는지 확인하십시오:

```php
$response->assertGone();
```



<a name="assert-header"></a>
#### assertHeader

주어진 헤더와 값이 응답에 존재하는지 확인합니다:

```php
$response->assertHeader($headerName, $value = null);
```



<a name="assert-header-contains"></a>
#### assertHeaderContains

주어진 헤더가 특정 하위 문자열 값을 포함하는지 확인합니다:

```php
$response->assertHeaderContains($headerName, $value);
```



<a name="assert-header-missing"></a>
#### assertHeaderMissing

주어진 헤더가 응답에 존재하지 않음을 확인합니다:

```php
$response->assertHeaderMissing($headerName);
```



<a name="assert-internal-server-error"></a>
#### 내부 서버 오류(assertInternalServerError)

응답에 "내부 서버 오류"(500) HTTP 상태 코드가 있는지 확인합니다:

```php
$response->assertInternalServerError();
```



<a name="assert-json"></a>
#### assertJson

응답에 주어진 JSON 데이터가 포함되어 있는지 확인하십시오:

```php
$response->assertJson(array $data, $strict = false);
```



`assertJson` 방법은 응답을 배열로 변환하여 주어진 배열이 애플리케이션에서 반환된 JSON 응답 내에 존재하는지 확인합니다. 따라서 JSON 응답에 다른 속성이 있어도 주어진 조각이 존재하는 한 이 테스트는 여전히 통과합니다.

<a name="assert-json-count"></a>
#### assertJsonCount

응답 JSON이 지정된 키에 예상 항목 수를 가진 배열을 포함하고 있는지 확인합니다:

```php
$response->assertJsonCount($count, $key = null);
```



<a name="assert-json-fragment"></a>
#### assertJsonFragment

응답에 주어진 JSON 데이터가 어디에든 포함되어 있는지 확인합니다:

```php
Route::get('/users', function () {
    return [
        'users' => [
            [
                'name' => 'Taylor Otwell',
            ],
        ],
    ];
});

$response->assertJsonFragment(['name' => 'Taylor Otwell']);
```



<a name="assert-json-is-array"></a>
#### assertJsonIsArray

응답 JSON이 배열인지 확인합니다:

```php
$response->assertJsonIsArray();
```



<a name="assert-json-is-object"></a>
#### assertJsonIsObject

응답 JSON이 객체인지 확인합니다:

```php
$response->assertJsonIsObject();
```



<a name="assert-json-missing"></a>
#### assertJsonMissing

응답에 주어진 JSON 데이터가 포함되어 있지 않음을 확인하십시오:

```php
$response->assertJsonMissing(array $data);
```



<a name="assert-json-missing-exact"></a>
#### assertJsonMissingExact

응답에 정확한 JSON 데이터가 포함되어 있지 않은지 확인하십시오:

```php
$response->assertJsonMissingExact(array $data);
```



<a name="assert-json-missing-validation-errors"></a>
#### assertJsonMissingValidationErrors

응답에 지정된 키에 대한 JSON 검증 오류가 없음을 확인합니다:

```php
$response->assertJsonMissingValidationErrors($keys);
```



> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는 응답이 JSON으로 반환된 유효성 검사 오류가 없음을 **그리고** 세션 저장소에 오류가 기록되지 않았음을 확인하는 데 사용할 수 있습니다.

<a name="assert-json-path"></a>
#### assertJsonPath

응답이 지정된 경로에 주어진 데이터를 포함하고 있는지 확인합니다:

```php
$response->assertJsonPath($path, $expectedValue);
```



예를 들어, 다음 JSON 응답이 귀하의 애플리케이션에서 반환되는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```



다음과 같이 `user` 객체의 `name` 속성이 주어진 값과 일치하는지 주장할 수 있습니다:

```php
$response->assertJsonPath('user.name', 'Steve Schoger');
```



<a name="assert-json-paths"></a>
#### assertJsonPaths

응답에 지정된 경로에 주어진 데이터가 포함되어 있는지 확인합니다:

```php
$response->assertJsonPaths(array $paths);
```



예를 들어, 응답 내에서 여러 값을 한 번에 주장할 수 있습니다:

```php
$response->assertJsonPaths([
    'user.name' => 'Steve Schoger',
    'user.email' => fn (string $email) => str($email)->endsWith('@laravel.com'),
]);
```



<a name="assert-json-missing-path"></a>
#### assertJsonMissingPath

응답에 지정된 경로가 포함되지 않았음을 확인합니다:

```php
$response->assertJsonMissingPath($path);
```



예를 들어, 다음 JSON 응답이 귀하의 애플리케이션에서 반환되는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```



`user` 객체의 `email` 속성이 포함되어 있지 않다고 단언할 수 있습니다:

```php
$response->assertJsonMissingPath('user.email');
```



<a name="assert-json-missing-paths"></a>
#### assertJsonMissingPaths

응답에 지정된 경로가 포함되지 않았음을 확인합니다:

```php
$response->assertJsonMissingPaths($paths);
```



예를 들어, 응답에서 여러 경로가 누락되었다고 주장할 수 있습니다:

```php
$response->assertJsonMissingPaths([
    'user.email',
    'user.password',
]);
```



<a name="assert-json-structure"></a>
#### assertJsonStructure

응답이 주어진 JSON 구조를 가지고 있는지 확인합니다:

```php
$response->assertJsonStructure(array $structure);
```



예를 들어, 애플리케이션에서 반환된 JSON 응답에 다음과 같은 데이터가 포함되어 있는 경우:

```json
{
    "user": {
        "name": "Steve Schoger"
    }
}
```



다음과 같이 JSON 구조가 예상과 일치한다고 주장할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        'name',
    ]
]);
```



때때로, 애플리케이션에서 반환되는 JSON 응답에는 객체 배열이 포함될 수 있습니다:

```json
{
    "user": [
        {
            "name": "Steve Schoger",
            "age": 55,
            "location": "Earth"
        },
        {
            "name": "Mary Schoger",
            "age": 60,
            "location": "Earth"
        }
    ]
}
```



이 상황에서, 배열에 있는 모든 객체의 구조에 대해 주장하기 위해 `*` 문자를 사용할 수 있습니다:

```php
$response->assertJsonStructure([
    'user' => [
        '*' => [
             'name',
             'age',
             'location'
        ]
    ]
]);
```



<a name="assert-json-validation-errors"></a>
#### assertJsonValidationErrors

주어진 키에 대해 응답에 특정 JSON 검증 오류가 있는지 확인합니다. 이 메서드는 검증 오류가 세션에 플래시되는 대신 JSON 구조로 반환되는 응답을 대상으로 검증할 때 사용해야 합니다:

```php
$response->assertJsonValidationErrors(array $data, $responseKey = 'errors');
```



> [!NOTE]
> 더 일반적인 [assertInvalid](#assert-invalid) 메서드는 응답이 JSON으로 반환된 검증 오류가 있는지 **또는** 오류가 세션 스토리지에 플래시되었는지를 검증하는 데 사용할 수 있습니다.

<a name="assert-json-validation-error-for"></a>
#### assertJsonValidationErrorFor

응답이 주어진 키에 대해 JSON 검증 오류가 있는지 검증합니다:

```php
$response->assertJsonValidationErrorFor(string $key, $responseKey = 'errors');
```



<a name="assert-method-not-allowed"></a>
#### 메서드허용안됨검증

응답이 메서드 허용 안 됨(405) HTTP 상태 코드를 가지고 있는지 검증합니다:

```php
$response->assertMethodNotAllowed();
```



<a name="assert-moved-permanently"></a>
#### assertMovedPermanently

응답이 영구 이동(301) HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertMovedPermanently();
```



<a name="assert-location"></a>
#### assertLocation

응답이 `Location` 헤더에 주어진 URI 값을 가지고 있는지 확인합니다:

```php
$response->assertLocation($uri);
```



<a name="assert-content"></a>
#### assertContent

주어진 문자열이 응답 내용과 일치하는지 확인하십시오:

```php
$response->assertContent($value);
```



<a name="assert-no-content"></a>
#### assertNoContent

응답이 지정된 HTTP 상태 코드를 가지고 있고 내용이 없음을 확인합니다:

```php
$response->assertNoContent($status = 204);
```



<a name="assert-streamed"></a>
#### assertStreamed

응답이 스트리밍된 응답인지 확인합니다:

$response->assertStreamed();

<a name="assert-streamed-content"></a>
#### assertStreamedContent

주어진 문자열이 스트리밍된 응답 내용과 일치하는지 확인합니다:

```php
$response->assertStreamedContent($value);
```



<a name="assert-not-found"></a>
#### assertNotFound

응답이 찾을 수 없음(404) HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertNotFound();
```



<a name="assert-ok"></a>
#### assertOk

응답이 200 HTTP 상태 코드를 가지고 있는지 확인하세요:

```php
$response->assertOk();
```



<a name="assert-payment-required"></a>
#### assertPaymentRequired

응답이 결제가 필요함(402) HTTP 상태 코드를 포함하는지 확인합니다:

```php
$response->assertPaymentRequired();
```



<a name="assert-plain-cookie"></a>
#### assertPlainCookie

응답에 지정된 암호화되지 않은 쿠키가 포함되어 있는지 확인하십시오:

```php
$response->assertPlainCookie($cookieName, $value = null);
```



<a name="assert-redirect"></a>
#### assertRedirect

응답이 주어진 URI로 리디렉션되는지 확인합니다:

```php
$response->assertRedirect($uri = null);
```



<a name="assert-redirect-back"></a>
#### assertRedirectBack

응답이 이전 페이지로 리디렉션되는지 확인:

```php
$response->assertRedirectBack();
```



<a name="assert-redirect-back-with-errors"></a>
#### assertRedirectBackWithErrors

응답이 이전 페이지로 리디렉션되고 [세션에 지정된 오류들이 있는지](#assert-session-has-errors) 확인합니다:

```php
$response->assertRedirectBackWithErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```



<a name="assert-redirect-back-without-errors"></a>
#### assertRedirectBackWithoutErrors

응답이 이전 페이지로 리디렉션되고 세션에 오류 메시지가 없는지 확인합니다:

```php
$response->assertRedirectBackWithoutErrors();
```



<a name="assert-redirect-contains"></a>
#### assertRedirectContains

응답이 주어진 문자열을 포함하는 URI로 리디렉션되는지 여부를 확인합니다:

```php
$response->assertRedirectContains($string);
```



<a name="assert-redirect-to-route"></a>
#### assertRedirectToRoute

응답이 주어진 [이름 있는 경로](/docs/{{version}}/routing#named-routes)로 리디렉션되는지 확인합니다:

```php
$response->assertRedirectToRoute($name, $parameters = []);
```



<a name="assert-redirect-to-signed-route"></a>
#### assertRedirectToSignedRoute

응답이 주어진 [서명된 라우트](/docs/{{version}}/urls#signed-urls)로 리디렉션되는지 확인합니다:

```php
$response->assertRedirectToSignedRoute($name = null, $parameters = []);
```



<a name="assert-request-timeout"></a>
#### assertRequestTimeout

응답이 요청 시간 초과(408) HTTP 상태 코드를 갖는지 확인합니다:

```php
$response->assertRequestTimeout();
```



<a name="assert-see"></a>
#### assertSee

주어진 문자열이 응답 안에 포함되어 있는지 확인합니다. 이 검증은 두 번째 인수로 `false`를 전달하지 않는 한 주어진 문자열을 자동으로 이스케이프합니다:

```php
$response->assertSee($value, $escape = true);
```



<a name="assert-see-in-order"></a>
#### assertSeeInOrder

주어진 문자열들이 응답 내에서 순서대로 포함되어 있는지 확인합니다. 이 검증은 두 번째 인수로 `false`를 전달하지 않는 한 주어진 문자열을 자동으로 이스케이프합니다:

```php
$response->assertSeeInOrder(array $values, $escape = true);
```



<a name="assert-see-text"></a>
#### assertSeeText

주어진 문자열이 응답 텍스트에 포함되어 있는지 확인합니다. 이 검증은 두 번째 인수로 `false`를 전달하지 않는 한 주어진 문자열을 자동으로 이스케이프합니다. 검증이 수행되기 전에 응답 내용은 `strip_tags` PHP 함수에 전달됩니다:

```php
$response->assertSeeText($value, $escape = true);
```



<a name="assert-see-text-in-order"></a>
#### assertSeeTextInOrder

주어진 문자열들이 응답 텍스트 안에서 순서대로 포함되어 있는지 확인합니다. 이 검증은 두 번째 인수로 `false`를 전달하지 않는 한 주어진 문자열들을 자동으로 이스케이프합니다. 검증이 수행되기 전에 응답 내용은 `strip_tags` PHP 함수로 전달됩니다:

```php
$response->assertSeeTextInOrder(array $values, $escape = true);
```



<a name="assert-server-error"></a>
#### assertServerError

응답이 서버 오류(HTTP 상태 코드 500 이상, 600 미만)를 가지는지 확인합니다:

```php
$response->assertServerError();
```



<a name="assert-service-unavailable"></a>
#### assertServiceUnavailable

응답이 "서비스를 사용할 수 없음"(503) HTTP 상태 코드를 가지는지 확인:

```php
$response->assertServiceUnavailable();
```



<a name="assert-session-has"></a>
#### assertSessionHas

세션에 주어진 데이터가 포함되어 있는지 확인하세요:

```php
$response->assertSessionHas($key, $value = null);
```



필요한 경우, 클로저를 `assertSessionHas` 메서드의 두 번째 인수로 제공할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 통과됩니다:

```php
$response->assertSessionHas($key, function (User $value) {
    return $value->name === 'Taylor Otwell';
});
```



<a name="assert-session-has-input"></a>
#### assertSessionHasInput

세션에 [플래시된 입력 배열](/docs/{{version}}/responses#redirecting-with-flashed-session-data)에 주어진 값이 있는지 확인합니다:

```php
$response->assertSessionHasInput($key, $value = null);
```



필요한 경우, 클로저를 `assertSessionHasInput` 메서드의 두 번째 인수로 제공할 수 있습니다. 클로저가 `true`를 반환하면 어설션이 통과됩니다:

```php
use Illuminate\Support\Facades\Crypt;

$response->assertSessionHasInput($key, function (string $value) {
    return Crypt::decryptString($value) === 'secret';
});
```



<a name="assert-session-has-all"></a>
#### assertSessionHasAll

세션이 주어진 키/값 쌍 배열을 포함하고 있는지 확인합니다:

```php
$response->assertSessionHasAll(array $data);
```



예를 들어, 애플리케이션의 세션에 `name` 및 `status` 키가 포함되어 있는 경우, 다음과 같이 두 키가 존재하고 지정된 값을 가지고 있는지 확인할 수 있습니다:

```php
$response->assertSessionHasAll([
    'name' => 'Taylor Otwell',
    'status' => 'active',
]);
```



<a name="assert-session-has-errors"></a>
#### assertSessionHasErrors

세션에 주어진 `$keys`에 대한 오류가 포함되어 있는지 확인합니다. 만약 `$keys`가 연관 배열이라면, 세션이 각 필드(key)에 대해 특정 오류 메시지(value)를 포함하고 있는지 확인합니다. 이 메서드는 JSON 구조로 반환하는 대신 세션에 검증 오류를 플래시하는 라우트를 테스트할 때 사용되어야 합니다:

```php
$response->assertSessionHasErrors(
    array $keys = [], $format = null, $errorBag = 'default'
);
```



예를 들어, `name` 및 `email` 필드에 세션에 표시된 유효성 검사 오류 메시지가 있다고 주장하려면, 다음과 같이 `assertSessionHasErrors` 메서드를 호출할 수 있습니다:

```php
$response->assertSessionHasErrors(['name', 'email']);
```



또는, 특정 필드가 특정 검증 오류 메시지를 가지고 있다고 주장할 수 있습니다:

```php
$response->assertSessionHasErrors([
    'name' => 'The given name was invalid.'
]);
```



> [!NOTE]
> 보다 일반적인 [assertInvalid](#assert-invalid) 메서드는 응답에 JSON으로 반환된 유효성 검사 오류가 있는지 또는 오류가 세션 저장소에 플래시되었는지 확인하는 데 사용할 수 있습니다.

<a name="assert-session-has-errors-in"></a>
#### assertSessionHasErrorsIn

세션에 특정 [error bag](/docs/{{version}}/validation#named-error-bags) 내에서 주어진 `$keys`에 대한 오류가 포함되어 있는지 확인합니다. `$keys`가 연관 배열(associative array)인 경우, 오류 배그 내에서 각 필드(key)에 대해 특정 오류 메시지(value)가 세션에 있는지 확인합니다:

```php
$response->assertSessionHasErrorsIn($errorBag, $keys = [], $format = null);
```



<a name="assert-session-has-no-errors"></a>
#### 세션에 오류가 없는지 확인

세션에 검증 오류가 없는지 확인:

```php
$response->assertSessionHasNoErrors();
```



<a name="assert-session-doesnt-have-errors"></a>
#### assertSessionDoesntHaveErrors

주어진 키에 대해 세션에 검증 오류가 없음을 확인합니다:

```php
$response->assertSessionDoesntHaveErrors($keys = [], $format = null, $errorBag = 'default');
```



> [!NOTE]
> 보다 일반적인 [assertValid](#assert-valid) 메서드는 응답이 JSON으로 반환된 검증 오류가 없음을 **그리고** 세션 저장소에 플래시된 오류가 없음을 확인하는 데 사용할 수 있습니다.

<a name="assert-session-missing"></a>
#### assertSessionMissing

세션에 주어진 키가 포함되어 있지 않음을 확인합니다:

```php
$response->assertSessionMissing($key);
```



<a name="assert-session-missing-input"></a>
#### assertSessionMissingInput

세션에 플래시된 입력 배열에서 주어진 입력 키가 없는지 확인합니다:

```php
$response->assertSessionMissingInput($key);
```



<a name="assert-status"></a>
#### assertStatus

응답이 특정 HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertStatus($code);
```



<a name="assert-successful"></a>
#### 성공 확인

응답이 성공적인(>= 200 및 < 300) HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertSuccessful();
```



<a name="assert-too-many-requests"></a>
#### assertTooManyRequests

응답이 너무 많은 요청(429) HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertTooManyRequests();
```



<a name="assert-unauthorized"></a>
#### assertUnauthorized

응답이 허가되지 않음(401) HTTP 상태 코드를 갖는지 확인하십시오:

```php
$response->assertUnauthorized();
```



<a name="assert-unprocessable"></a>
#### assertUnprocessable

응답이 처리할 수 없는 엔터티(422) HTTP 상태 코드를 가지고 있는지 확인합니다:

```php
$response->assertUnprocessable();
```



<a name="assert-unsupported-media-type"></a>
#### 지원되지 않는 미디어 타입(assertUnsupportedMediaType) 확인

응답이 지원되지 않는 미디어 타입(HTTP 상태 코드 415)을 가지고 있는지 확인합니다:

```php
$response->assertUnsupportedMediaType();
```



<a name="assert-valid"></a>
#### assertValid

주어진 키에 대한 응답에 유효성 검사 오류가 없음을 확인합니다. 이 메서드는 유효성 검사 오류가 JSON 구조로 반환되거나 세션에 플래시된 응답에 대해 확인할 때 사용할 수 있습니다:

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```



<a name="assert-invalid"></a>
#### assertInvalid

주어진 키에 대한 응답에 검증 오류가 있는지 확인합니다. 이 메서드는 검증 오류가 JSON 구조로 반환되거나 검증 오류가 세션에 플래시된 응답에 대해 확인하는 데 사용할 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```



또한 특정 키가 특정 유효성 검사 오류 메시지를 가지고 있다고 주장할 수 있습니다. 이렇게 할 때 전체 메시지를 제공하거나 메시지의 일부분만 제공할 수 있습니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```



주어진 필드가 유효성 검사 오류가 있는 유일한 필드라고 주장하고 싶다면, `assertOnlyInvalid` 방법을 사용할 수 있습니다:

```php
$response->assertOnlyInvalid(['name', 'email']);
```



<a name="assert-view-has"></a>
#### assertViewHas

응답 뷰에 특정 데이터가 포함되어 있는지 확인합니다:

```php
$response->assertViewHas($key, $value = null);
```



`assertViewHas` 메서드의 두 번째 인수로 클로저를 전달하면 특정 뷰 데이터에 대해 검사하고 주장할 수 있습니다:

```php
$response->assertViewHas('user', function (User $user) {
    return $user->name === 'Taylor';
});
```



또한 응답에서 배열 변수로 뷰 데이터를 접근할 수 있어 편리하게 확인할 수 있습니다:```php tab=Pest
expect($response['name'])->toBe('Taylor');
```

```php tab=PHPUnit
$this->assertEquals('Taylor', $response['name']);
```



<a name="assert-view-has-all"></a>
#### assertViewHasAll

응답 뷰에 주어진 데이터 목록이 있는지 확인합니다:

```php
$response->assertViewHasAll(array $data);
```



이 방법은 뷰가 단순히 주어진 키와 일치하는 데이터를 포함하고 있음을 확인하는 데 사용될 수 있습니다:

```php
$response->assertViewHasAll([
    'name',
    'email',
]);
```



또는, 뷰 데이터가 존재하며 특정 값을 가지고 있다고 주장할 수도 있습니다:

```php
$response->assertViewHasAll([
    'name' => 'Taylor Otwell',
    'email' => 'taylor@example.com,',
]);
```



<a name="assert-view-is"></a>
#### assertViewIs

지정된 뷰가 라우트에 의해 반환되었는지 확인하십시오:

```php
$response->assertViewIs($value);
```



<a name="assert-view-missing"></a>
#### assertViewMissing

주어진 데이터 키가 애플리케이션 응답에서 반환된 뷰에 제공되지 않았음을 확인합니다:

```php
$response->assertViewMissing($key);
```



<a name="authentication-assertions"></a>
### 인증 주장

Laravel은 애플리케이션의 기능 테스트 내에서 사용할 수 있는 다양한 인증 관련 주장을 제공합니다. 이러한 메서드는 `get` 및 `post`와 같은 메서드가 반환하는 `Illuminate\Testing\TestResponse` 인스턴스가 아니라, 테스트 클래스 자체에서 호출된다는 점에 유의하세요.

<a name="assert-authenticated"></a>
#### assertAuthenticated

사용자가 인증되었는지 주장합니다:

```php
$this->assertAuthenticated($guard = null);
```



<a name="assert-guest"></a>
#### assertGuest

사용자가 인증되지 않았음을 확인합니다:

```php
$this->assertGuest($guard = null);
```



<a name="assert-authenticated-as"></a>
#### assertAuthenticatedAs

특정 사용자가 인증되었는지 확인합니다:

```php
$this->assertAuthenticatedAs($user, $guard = null);
```



<a name="validation-assertions"></a>
## 검증 주장

라라벨은 요청에서 제공된 데이터가 유효했는지 또는 무효했는지를 확인하는 데 사용할 수 있는 두 가지 주요 검증 관련 주장을 제공합니다.

<a name="validation-assert-valid"></a>
#### assertValid

주어진 키에 대해 응답에 검증 오류가 없음을 주장합니다. 이 메서드는 검증 오류가 JSON 구조로 반환되거나 검증 오류가 세션에 플래시된 응답에 대해 주장하는 데 사용할 수 있습니다:

```php
// Assert that no validation errors are present...
$response->assertValid();

// Assert that the given keys do not have validation errors...
$response->assertValid(['name', 'email']);
```



<a name="validation-assert-invalid"></a>
#### assertInvalid

주어진 키에 대한 응답에 검증 오류가 있는지 확인합니다. 이 메서드는 검증 오류가 JSON 구조로 반환되거나 검증 오류가 세션에 플래시된 응답에 대해 확인하는 데 사용될 수 있습니다:

```php
$response->assertInvalid(['name', 'email']);
```



또한 특정 키가 특정 유효성 검사 오류 메시지를 가지고 있다고 주장할 수 있습니다. 이렇게 할 때 전체 메시지를 제공하거나 메시지의 일부분만 제공할 수 있습니다:

```php
$response->assertInvalid([
    'name' => 'The name field is required.',
    'email' => 'valid email address',
]);
```
{% endraw %}
