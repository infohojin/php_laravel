---
layout: docs
title: "HTTP Requests"
---

{% raw %}
---
layout: docs
title: "HTTP Requests"
---

# HTTP Requests

- [Introduction](#introduction)
- [Interacting With The Request](#interacting-with-the-request)
    - [Accessing the Request](#accessing-the-request)
    - [Request Path, Host, and Method](#request-path-and-method)
    - [Request Headers](#request-headers)
    - [Request IP Address](#request-ip-address)
    - [Content Negotiation](#content-negotiation)
    - [PSR-7 Requests](#psr7-requests)
- [Input](#input)
    - [Retrieving Input](#retrieving-input)
    - [Input Presence](#input-presence)
    - [Merging Additional Input](#merging-additional-input)
    - [Old Input](#old-input)
    - [Cookies](#cookies)
    - [Input Trimming and Normalization](#input-trimming-and-normalization)
- [Files](#files)
    - [Retrieving Uploaded Files](#retrieving-uploaded-files)
    - [Storing Uploaded Files](#storing-uploaded-files)
- [Configuring Trusted Proxies](#configuring-trusted-proxies)
- [Configuring Trusted Hosts](#configuring-trusted-hosts)

<a name="introduction"></a>
## Introduction

Laravel's `Illuminate\Http\Request` class provides an object-oriented way to interact with the current HTTP request being handled by your application as well as retrieve the input, cookies, and files that were submitted with the request.

<a name="interacting-with-the-request"></a>
## Interacting With The Request

<a name="accessing-the-request"></a>
### Accessing the Request

To obtain an instance of the current HTTP request via dependency injection, you should type-hint the `Illuminate\Http\Request` class on your route closure or controller method. The incoming request instance will automatically be injected by the Laravel [service container](/docs/{{version}}/container):

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->input('name');

        // Store the user...

        return redirect('/users');
    }
}
```



앞서 언급한 것처럼, 라우트 클로저에서 `Illuminate\Http\Request` 클래스에 타입 힌트를 지정할 수도 있습니다. 클로저가 실행될 때 서비스 컨테이너가 들어오는 요청을 자동으로 주입합니다:

```php
use Illuminate\Http\Request;

Route::get('/', function (Request $request) {
    // ...
});
```



<a name="dependency-injection-route-parameters"></a>
#### 의존성 주입 및 경로 매개변수

컨트롤러 메서드가 경로 매개변수로부터 입력을 기대하는 경우, 다른 의존성 뒤에 경로 매개변수를 나열해야 합니다. 예를 들어, 경로가 다음과 같이 정의되어 있다면:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```



컨트롤러 메서드를 다음과 같이 정의하여 `Illuminate\Http\Request`를 타입 힌트하고 `id` 경로 매개변수에 액세스할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the specified user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```



<a name="request-path-and-method"></a>
### 요청 경로, 호스트 및 메서드

`Illuminate\Http\Request` 인스턴스는 들어오는 HTTP 요청을 검사하기 위한 다양한 메서드를 제공하며 `Symfony\Component\HttpFoundation\Request` 클래스를 확장합니다. 아래에서는 가장 중요한 몇 가지 메서드에 대해 논의하겠습니다.

<a name="retrieving-the-request-path"></a>
#### 요청 경로 가져오기

`path` 메서드는 요청의 경로 정보를 반환합니다. 따라서 들어오는 요청이 `http://example.com/foo/bar`를 대상으로 하는 경우, `path` 메서드는 `foo/bar`를 반환합니다:

```php
$uri = $request->path();
```



<a name="inspecting-the-request-path"></a>
#### 요청 경로 / 라우트 검사

`is` 메서드는 들어오는 요청 경로가 주어진 패턴과 일치하는지 확인할 수 있게 해줍니다. 이 메서드를 사용할 때 `*` 문자를 와일드카드로 사용할 수 있습니다:

```php
if ($request->is('admin/*')) {
    // ...
}
```



`routeIs` 방법을 사용하면 들어오는 요청이 [명명된 라우트](/docs/{{version}}/routing#named-routes)와 일치하는지 확인할 수 있습니다:

```php
if ($request->routeIs('admin.*')) {
    // ...
}
```



<a name="retrieving-the-request-url"></a>
#### 요청 URL 가져오기

들어오는 요청의 전체 URL을 가져오려면 `url` 또는 `fullUrl` 메서드를 사용할 수 있습니다. `url` 메서드는 쿼리 문자열 없이 URL을 반환하며, `fullUrl` 메서드는 쿼리 문자열을 포함합니다:

```php
$url = $request->url();

$urlWithQueryString = $request->fullUrl();
```



현재 URL에 쿼리 문자열 데이터를 추가하고 싶다면 `fullUrlWithQuery` 메서드를 호출할 수 있습니다. 이 메서드는 주어진 쿼리 문자열 변수 배열을 현재 쿼리 문자열과 병합합니다:

```php
$request->fullUrlWithQuery(['type' => 'phone']);
```



현재 URL에서 특정 쿼리 문자열 매개변수 없이 가져오고 싶다면, `fullUrlWithoutQuery` 메서드를 사용할 수 있습니다:

```php
$request->fullUrlWithoutQuery(['type']);
```



<a name="retrieving-the-request-host"></a>
#### 요청 호스트 가져오기

`host`, `httpHost`, `schemeAndHttpHost` 메서드를 통해 들어오는 요청의 "호스트"를 가져올 수 있습니다:

```php
// http://localhost:8000
$request->host(); // localhost
$request->httpHost(); // localhost:8000
$request->schemeAndHttpHost(); // http://localhost:8000
```



<a name="retrieving-the-request-method"></a>
#### 요청 방식 가져오기

`method` 메서드는 요청의 HTTP 동사를 반환합니다. `isMethod` 메서드를 사용하여 HTTP 동사가 주어진 문자열과 일치하는지 확인할 수 있습니다:

```php
$method = $request->method();

if ($request->isMethod('post')) {
    // ...
}
```



<a name="request-headers"></a>
### 요청 헤더

`Illuminate\Http\Request` 인스턴스에서 `header` 메서드를 사용하여 요청 헤더를 가져올 수 있습니다. 요청에 헤더가 없으면 `null`가 반환됩니다. 그러나 `header` 메서드는 요청에 헤더가 없을 경우 반환될 선택적 두 번째 인수를 허용합니다:

```php
$value = $request->header('X-Header-Name');

$value = $request->header('X-Header-Name', 'default');
```



`hasHeader` 메서드는 요청에 특정 헤더가 포함되어 있는지 확인하는 데 사용할 수 있습니다:

```php
if ($request->hasHeader('X-Header-Name')) {
    // ...
}
```



편의를 위해 `Authorization` 헤더에서 베어러 토큰을 가져오기 위해 `bearerToken` 메소드를 사용할 수 있습니다. 해당 헤더가 없으면 빈 문자열이 반환됩니다:

```php
$token = $request->bearerToken();
```



<a name="request-ip-address"></a>
### 요청 IP 주소

`ip` 방법은 애플리케이션에 요청을 보낸 클라이언트의 IP 주소를 가져오는 데 사용될 수 있습니다:

```php
$ipAddress = $request->ip();
```



프록시를 통해 전달된 모든 클라이언트 IP 주소를 포함한 IP 주소 배열을 가져오고 싶다면, `ips` 메서드를 사용할 수 있습니다. "원본" 클라이언트 IP 주소는 배열의 끝에 위치하게 됩니다:

```php
$ipAddresses = $request->ips();
```



일반적으로 IP 주소는 신뢰할 수 없는, 사용자 제어 입력으로 간주해야 하며 정보 제공 목적으로만 사용해야 합니다.

<a name="content-negotiation"></a>
### 콘텐츠 협상

Laravel은 `Accept` 헤더를 통해 들어오는 요청의 요청된 콘텐츠 유형을 검사하는 여러 방법을 제공합니다. 먼저, `getAcceptableContentTypes` 메서드는 요청에서 허용하는 모든 콘텐츠 유형을 포함하는 배열을 반환합니다:

```php
$contentTypes = $request->getAcceptableContentTypes();
```



`accepts` 메서드는 콘텐츠 타입 배열을 받고 요청에서 어떤 콘텐츠 타입도 허용되면 `true`를 반환합니다. 그렇지 않으면 `false`가 반환됩니다:

```php
if ($request->accepts(['text/html', 'application/json'])) {
    // ...
}
```



주어진 콘텐츠 유형 배열 중 요청에서 가장 선호하는 콘텐츠 유형을 결정하기 위해 `prefers` 방법을 사용할 수 있습니다. 제공된 콘텐츠 유형 중 어느 것도 요청에서 허용되지 않는 경우, `null`가 반환됩니다:

```php
$preferred = $request->prefers(['text/html', 'application/json']);
```



많은 애플리케이션이 HTML 또는 JSON만 제공하기 때문에, 들어오는 요청이 JSON 응답을 기대하는지 빠르게 확인하려면 `expectsJson` 방법을 사용할 수 있습니다:

```php
if ($request->expectsJson()) {
    // ...
}
```



요청이 특히 Markdown을 선호하는지 또는 Markdown을 다른 콘텐츠 유형 중 하나로 수용할 수 있는지 확인해야 하는 경우, 예를 들어 AI 에이전트나 Markdown 응답을 사용하는 다른 클라이언트를 제공할 때, `wantsMarkdown` 및 `acceptsMarkdown` 메서드를 사용할 수 있습니다:

```php
if ($request->wantsMarkdown()) {
    // The client's most preferred content type is text/markdown...
}

if ($request->acceptsMarkdown()) {
    // The client accepts Markdown responses...
}
```



<a name="psr7-requests"></a>
### PSR-7 요청

[PSR-7 표준](https://www.php-fig.org/psr/psr-7/)은 요청과 응답을 포함한 HTTP 메시지에 대한 인터페이스를 명시합니다. Laravel 요청 대신 PSR-7 요청 인스턴스를 얻고자 한다면, 먼저 몇 가지 라이브러리를 설치해야 합니다. Laravel은 일반적인 Laravel 요청과 응답을 PSR-7 호환 구현으로 변환하기 위해 *Symfony HTTP 메시지 브리지* 컴포넌트를 사용합니다:

```shell
composer require symfony/psr-http-message-bridge
composer require nyholm/psr7
```



이 라이브러리들을 설치한 후에는 라우트 클로저나 컨트롤러 메서드에서 요청 인터페이스를 타입 힌트로 지정하여 PSR-7 요청을 얻을 수 있습니다:

```php
use Psr\Http\Message\ServerRequestInterface;

Route::get('/', function (ServerRequestInterface $request) {
    // ...
});
```



> [!NOTE]
> 라우트나 컨트롤러에서 PSR-7 응답 인스턴스를 반환하면, 이는 자동으로 Laravel 응답 인스턴스로 다시 변환되어 프레임워크에 의해 표시됩니다.

<a name="input"></a>
## 입력

<a name="retrieving-input"></a>
### 입력 가져오기

<a name="retrieving-all-input-data"></a>
#### 모든 입력 데이터 가져오기

모든 들어오는 요청의 입력 데이터를 `array`로 `all` 메서드를 사용하여 가져올 수 있습니다. 이 메서드는 들어오는 요청이 HTML 폼에서 온 것이든 XHR 요청이든 관계없이 사용할 수 있습니다:

```php
$input = $request->all();
```



`collect` 방법을 사용하면 모든 들어오는 요청의 입력 데이터를 [컬렉션](/docs/{{version}}/collections)으로 가져올 수 있습니다:

```php
$input = $request->collect();
```



`collect` 메서드는 또한 들어오는 요청의 입력 일부를 컬렉션으로 가져올 수 있도록 합니다:

```php
$request->collect('users')->each(function (string $user) {
    // ...
});
```



<a name="retrieving-an-input-value"></a>
#### 입력 값 가져오기

몇 가지 간단한 방법을 사용하여 요청에 어떤 HTTP 동사가 사용되었는지 걱정하지 않고 `Illuminate\Http\Request` 인스턴스에서 모든 사용자 입력에 접근할 수 있습니다. HTTP 동사에 관계없이 `input` 메서드를 사용하여 사용자 입력을 가져올 수 있습니다:

```php
$name = $request->input('name');
```



`input` 메서드의 두 번째 인수로 기본 값을 전달할 수 있습니다. 요청된 입력 값이 요청에 없으면 이 값이 반환됩니다:

```php
$name = $request->input('name', 'Sally');
```



배열 입력을 포함하는 양식을 다룰 때, 배열에 접근하기 위해 '점(dot)' 표기법을 사용하세요:

```php
$name = $request->input('products.0.name');

$names = $request->input('products.*.name');
```



인수 없이 `input` 메서드를 호출하여 모든 입력 값을 연관 배열로 가져올 수 있습니다:

```php
$input = $request->input();
```



<a name="retrieving-input-from-the-query-string"></a>
#### 쿼리 문자열에서 입력 가져오기

`input` 메서드가 전체 요청 페이로드(쿼리 문자열 포함)에서 값을 가져오는 반면, `query` 메서드는 쿼리 문자열에서만 값을 가져옵니다:

```php
$name = $request->query('name');
```



요청된 쿼리 문자열 값 데이터가 존재하지 않으면, 이 메서드의 두 번째 인자가 반환됩니다:

```php
$name = $request->query('name', 'Helen');
```



모든 쿼리 문자열 값을 연관 배열로 가져오기 위해 인수 없이 `query` 메서드를 호출할 수 있습니다:

```php
$query = $request->query();
```



<a name="retrieving-json-input-values"></a>
#### JSON 입력 값 가져오기

애플리케이션에 JSON 요청을 보낼 때, 요청의 `Content-Type` 헤더가 `application/json`로 올바르게 설정되어 있는 한 `input` 메서드를 통해 JSON 데이터를 액세스할 수 있습니다. JSON 배열/객체 내에 중첩된 값을 가져오기 위해 'dot' 문법을 사용할 수도 있습니다:

```php
$name = $request->input('user.name');
```



<a name="retrieving-stringable-input-values"></a>
#### 문자열로 변환 가능한 입력 값 가져오기

요청의 입력 데이터를 원시 `string`로 가져오는 대신, `string` 메서드를 사용하여 요청 데이터를 [Illuminate\Support\Stringable](/docs/{{version}}/strings) 인스턴스로 가져올 수 있습니다:

```php
$name = $request->string('name')->trim();
```



<a name="retrieving-integer-input-values"></a>
#### 정수 입력 값 가져오기

입력 값을 정수로 가져오려면 `integer` 방법을 사용할 수 있습니다. 이 방법은 입력 값을 정수로 캐스트하려고 시도합니다. 입력이 없거나 캐스트에 실패하면 지정한 기본 값을 반환합니다. 이는 페이지 매김이나 기타 숫자 입력에 특히 유용합니다:

```php
$perPage = $request->integer('per_page');
```



<a name="retrieving-boolean-input-values"></a>
#### 불리언 입력 값 가져오기

체크박스와 같은 HTML 요소를 다룰 때, 애플리케이션은 실제로 문자열인 "참(truthy)" 값을 받을 수 있습니다. 예를 들어, "true" 또는 "on"과 같은 값입니다. 편의를 위해, 이러한 값을 불리언으로 가져오기 위해 `boolean` 메서드를 사용할 수 있습니다. `boolean` 메서드는 1, "1", true, "true", "on", "yes"에 대해 `true`를 반환합니다. 그 외 모든 값은 `false`를 반환합니다:

```php
$archived = $request->boolean('archived');
```



<a name="retrieving-array-input-values"></a>
#### 배열 입력 값 가져오기

배열을 포함한 입력 값은 `array` 방법을 사용하여 가져올 수 있습니다. 이 방법은 입력 값을 항상 배열로 변환합니다. 요청에 지정된 이름의 입력 값이 포함되어 있지 않으면 빈 배열이 반환됩니다:

```php
$versions = $request->array('versions');
```



<a name="retrieving-date-input-values"></a>
#### 날짜 입력 값 가져오기

편의를 위해, 날짜/시간을 포함하는 입력 값은 `date` 메서드를 사용하여 Carbon 인스턴스로 가져올 수 있습니다. 요청에 지정된 이름의 입력 값이 포함되지 않은 경우 `null`가 반환됩니다:

```php
$birthday = $request->date('birthday');
```



`date` 메서드가 받는 두 번째와 세 번째 인수는 각각 날짜의 형식과 시간대를 지정하는 데 사용될 수 있습니다:

```php
$elapsed = $request->date('elapsed', '!H:i', 'Europe/Madrid');
```



입력 값이 존재하지만 형식이 올바르지 않은 경우 `InvalidArgumentException`가 발생하므로, `date` 메서드를 호출하기 전에 입력 값을 검증하는 것이 좋습니다.

<a name="retrieving-interval-input-values"></a>
#### 간격 입력 값 가져오기

기간을 포함하는 입력 값은 `interval` 메서드를 사용하여 `CarbonInterval` 인스턴스로 가져올 수 있습니다. 요청에 지정된 이름의 입력 값이 포함되어 있지 않은 경우, `null`가 반환됩니다:

```php
$duration = $request->interval('duration');
```



입력 값이 숫자인 경우 두 번째 인수로 단위를 제공할 수 있습니다. 단위는 `second`, `minute` 또는 `day`와 같은 문자열이거나 `Carbon\Unit` 열거형 인스턴스일 수 있습니다:

```php
use Carbon\Unit;

$timeout = $request->interval('timeout', 'second');

$delay = $request->interval('delay', Unit::Minute);
```



입력 값이 존재하지만 형식이 잘못된 경우 `InvalidArgumentException`가 발생하므로, `interval` 메서드를 호출하기 전에 입력 값을 검증하는 것이 권장됩니다.

<a name="retrieving-enum-input-values"></a>
#### Enum 입력 값 가져오기

[PHP 열거형](https://www.php.net/manual/en/language.types.enumerations.php)에 해당하는 입력 값은 요청에서 가져올 수도 있습니다. 요청에 지정된 이름의 입력 값이 없거나 열거형이 입력 값과 일치하는 기준 값을 가지고 있지 않은 경우 `null`가 반환됩니다. `enum` 메서드는 첫 번째 인수로 입력 값의 이름을, 두 번째 인수로 열거형 클래스를 받습니다:

```php
use App\Enums\Status;

$status = $request->enum('status', Status::class);
```



값이 없거나 잘못된 경우 반환될 기본값을 제공할 수도 있습니다:

```php
$status = $request->enum('status', Status::class, Status::Pending);
```



입력 값이 PHP 열거형에 해당하는 값들의 배열인 경우, `enums` 메서드를 사용하여 열거형 인스턴스로 값들의 배열을 가져올 수 있습니다:

```php
use App\Enums\Product;

$products = $request->enums('products', Product::class);
```



<a name="retrieving-input-via-dynamic-properties"></a>
#### 동적 속성을 통한 입력 가져오기

`Illuminate\Http\Request` 인스턴스의 동적 속성을 사용하여 사용자 입력에 접근할 수도 있습니다. 예를 들어, 애플리케이션의 폼 중 하나에 `name` 필드가 포함되어 있다면, 다음과 같이 필드의 값을 가져올 수 있습니다:

```php
$name = $request->name;
```



동적 속성을 사용할 때, Laravel은 먼저 요청 페이로드에서 해당 매개변수의 값을 찾습니다. 값이 없으면 Laravel은 일치하는 라우트의 매개변수에서 필드를 검색합니다.

<a name="retrieving-a-portion-of-the-input-data"></a>
#### 입력 데이터의 일부 가져오기

입력 데이터의 일부만 가져와야 하는 경우, `only` 및 `except` 메서드를 사용할 수 있습니다. 이 두 메서드는 단일 `array` 또는 동적 인수 목록을 받습니다:

```php
$input = $request->only(['username', 'password']);

$input = $request->only('username', 'password');

$input = $request->except(['credit_card']);

$input = $request->except('credit_card');
```



> [!WARNING]
> `only` 메서드는 요청한 모든 키/값 쌍을 반환합니다; 그러나 요청에 존재하지 않는 키/값 쌍은 반환하지 않습니다.

<a name="input-presence"></a>
### 입력 존재 여부

요청에 값이 존재하는지 확인하려면 `has` 메서드를 사용할 수 있습니다. `has` 메서드는 요청에 값이 존재하면 `true`를 반환합니다:

```php
if ($request->has('name')) {
    // ...
}
```



배열이 주어지면, `has` 메서드는 지정된 모든 값이 존재하는지 여부를 판단합니다:

```php
if ($request->has(['name', 'email'])) {
    // ...
}
```



`hasAny` 메서드는 지정된 값 중 하나라도 존재하면 `true`를 반환합니다:

```php
if ($request->hasAny(['name', 'email'])) {
    // ...
}
```



`whenHas` 메서드는 요청에 값이 있는 경우 지정된 클로저를 실행합니다:

```php
$request->whenHas('name', function (string $input) {
    // ...
});
```



지정된 값이 요청에 없을 경우 실행될 두 번째 클로저를 `whenHas` 메서드에 전달할 수 있습니다:

```php
$request->whenHas('name', function (string $input) {
    // The "name" value is present...
}, function () {
    // The "name" value is not present...
});
```



값이 요청에 존재하며 빈 문자열이 아닌지 확인하려면 `filled` 메서드를 사용할 수 있습니다:

```php
if ($request->filled('name')) {
    // ...
}
```



값이 요청에서 누락되었는지 또는 빈 문자열인지 확인하려면 `isNotFilled` 방법을 사용할 수 있습니다:

```php
if ($request->isNotFilled('name')) {
    // ...
}
```



배열이 주어지면 `isNotFilled` 메서드는 지정된 값들이 모두 없거나 비어 있는지 여부를 확인합니다:

```php
if ($request->isNotFilled(['name', 'email'])) {
    // ...
}
```



`anyFilled` 메서드는 지정된 값 중 하나라도 빈 문자열이 아니면 `true`를 반환합니다:

```php
if ($request->anyFilled(['name', 'email'])) {
    // ...
}
```



`whenFilled` 메서드는 요청에 값이 존재하고 빈 문자열이 아닐 경우 주어진 클로저를 실행합니다:

```php
$request->whenFilled('name', function (string $input) {
    // ...
});
```



지정된 값이 'filled'가 아닌 경우 실행될 두 번째 클로저를 `whenFilled` 메서드에 전달할 수 있습니다:

```php
$request->whenFilled('name', function (string $input) {
    // The "name" value is filled...
}, function () {
    // The "name" value is not filled...
});
```



주어진 키가 요청에 없는지 확인하려면, `missing` 및 `whenMissing` 메서드를 사용할 수 있습니다:

```php
if ($request->missing('name')) {
    // ...
}

$request->whenMissing('name', function () {
    // The "name" value is missing...
}, function () {
    // The "name" value is present...
});
```



<a name="merging-additional-input"></a>
### 추가 입력 병합

때때로 요청의 기존 입력 데이터에 추가 입력을 수동으로 병합해야 할 수도 있습니다. 이를 달성하기 위해 `merge` 방법을 사용할 수 있습니다. 주어진 입력 키가 요청에 이미 존재하는 경우, `merge` 방법을 통해 제공된 데이터로 덮어쓰게 됩니다:

```php
$request->merge(['votes' => 0]);
```



`mergeIfMissing` 방법은 해당 키가 요청의 입력 데이터 내에 이미 존재하지 않는 경우 입력을 요청에 병합하는 데 사용될 수 있습니다:

```php
$request->mergeIfMissing(['votes' => 0]);
```



<a name="old-input"></a>
### 이전 입력

Laravel은 다음 요청 동안 이전 요청의 입력을 유지할 수 있게 해줍니다. 이 기능은 특히 유효성 검사 오류를 감지한 후 양식을 다시 채울 때 유용합니다. 그러나 Laravel에 포함된 [유효성 검사 기능](/docs/{{version}}/validation)을 사용하는 경우, Laravel의 일부 내장 유효성 검사 기능이 자동으로 이러한 세션 입력 플래시를 호출하기 때문에 이러한 세션 입력 플래시 메서드를 직접 사용할 필요가 없을 수도 있습니다.

<a name="flashing-input-to-the-session"></a>
#### 세션에 입력 플래시하기

`Illuminate\Http\Request` 클래스의 `flash` 메서드는 현재 입력을 [세션](/docs/{{version}}/session)에 플래시하여 사용자가 애플리케이션에 다음번 요청을 할 때 사용할 수 있도록 합니다:

```php
$request->flash();
```



또한 `flashOnly` 및 `flashExcept` 메서드를 사용하여 요청 데이터의 일부를 세션에 플래시할 수 있습니다. 이러한 메서드는 비밀번호와 같은 민감한 정보를 세션에 저장하지 않도록 하는 데 유용합니다:

```php
$request->flashOnly(['username', 'email']);

$request->flashExcept('password');
```



<a name="flashing-input-then-redirecting"></a>
#### 입력을 플래시한 후 리디렉션

세션에 입력을 자주 플래시한 후 이전 페이지로 리디렉션하고 싶을 때, `withInput` 메서드를 사용하여 입력 플래싱을 리디렉션에 쉽게 연결할 수 있습니다:

```php
return redirect('/form')->withInput();

return redirect()->route('user.create')->withInput();

return redirect('/form')->withInput(
    $request->except('password')
);
```



<a name="retrieving-old-input"></a>
#### 이전 입력 가져오기

이전 요청에서 플래시된 입력을 가져오려면 `Illuminate\Http\Request`의 인스턴스에서 `old` 메서드를 호출하십시오. `old` 메서드는 이전에 플래시된 입력 데이터를 [세션](/docs/{{version}}/session)에서 가져옵니다:

```php
$username = $request->old('username');
```



Laravel은 또한 전역 `old` 헬퍼를 제공합니다. [Blade 템플릿](/docs/{{version}}/blade) 내에서 이전 입력을 표시하는 경우, 폼을 다시 채우기 위해 `old` 헬퍼를 사용하는 것이 더 편리합니다. 주어진 필드에 대한 이전 입력이 없으면 `null`가 반환됩니다:

```blade
<input type="text" name="username" value="{{ old('username') }}">
```



<a name="cookies"></a>
### 쿠키

<a name="retrieving-cookies-from-requests"></a>
#### 요청에서 쿠키 가져오기

Laravel 프레임워크에서 생성된 모든 쿠키는 암호화되고 인증 코드로 서명되므로, 클라이언트가 변경한 경우 유효하지 않은 것으로 간주됩니다. 요청에서 쿠키 값을 가져오려면 `Illuminate\Http\Request` 인스턴스에서 `cookie` 메서드를 사용하세요:

```php
$value = $request->cookie('name');
```



<a name="input-trimming-and-normalization"></a>
## 입력 트리밍 및 정규화

기본적으로, Laravel은 애플리케이션의 전역 미들웨어 스택에 `Illuminate\Foundation\Http\Middleware\TrimStrings` 및 `Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull` 미들웨어를 포함합니다. 이 미들웨어는 모든 들어오는 문자열 필드를 자동으로 트리밍하며, 빈 문자열 필드를 `null`로 변환합니다. 이를 통해 라우트나 컨트롤러에서 이러한 정규화 문제를 걱정할 필요가 없습니다.

#### 입력 정규화 비활성화

이 동작을 모든 요청에 대해 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `$middleware->remove` 메서드를 호출하여 미들웨어 스택에서 두 미들웨어를 제거할 수 있습니다:

```php
use Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull;
use Illuminate\Foundation\Http\Middleware\TrimStrings;

->withMiddleware(function (Middleware $middleware): void {
    $middleware->remove([
        ConvertEmptyStringsToNull::class,
        TrimStrings::class,
    ]);
})
```



응용 프로그램의 일부 요청에 대해 문자열 다듬기 및 빈 문자열 변환을 비활성화하고자 하는 경우, 응용 프로그램의 `bootstrap/app.php` 파일 내에서 `trimStrings` 및 `convertEmptyStringsToNull` 미들웨어 메서드를 사용할 수 있습니다. 두 메서드 모두 클로저 배열을 받아들이며, 입력 정규화를 건너뛰어야 하는지 여부를 표시하기 위해 `true` 또는 `false`를 반환해야 합니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->convertEmptyStringsToNull(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);

    $middleware->trimStrings(except: [
        fn (Request $request) => $request->is('admin/*'),
    ]);
})
```



<a name="files"></a>
## 파일

<a name="retrieving-uploaded-files"></a>
### 업로드된 파일 가져오기

`Illuminate\Http\Request` 인스턴스에서 업로드된 파일을 `file` 메서드를 사용하거나 동적 속성을 사용하여 가져올 수 있습니다. `file` 메서드는 PHP `SplFileInfo` 클래스를 확장하고 파일과 상호작용하기 위한 다양한 메서드를 제공하는 `Illuminate\Http\UploadedFile` 클래스의 인스턴스를 반환합니다:

```php
$file = $request->file('photo');

$file = $request->photo;
```



`hasFile` 메서드를 사용하여 요청에 파일이 있는지 확인할 수 있습니다:

```php
if ($request->hasFile('photo')) {
    // ...
}
```



업로드된 파일이 저장하기 전에 조작이 필요한 이미지인 경우, `image` 메서드를 사용하여 `Illuminate\Image\Image` 인스턴스를 가져오거나, 파일이 없는 경우 `null`를 사용할 수 있습니다:

```php
$image = $request->image('photo');
```



이미지 조작에 대한 더 많은 정보는 완전한 [이미지 조작 문서](/docs/{{version}}/images)를 참조하십시오.

<a name="validating-successful-uploads"></a>
#### 업로드 성공 확인

파일이 존재하는지 확인하는 것 외에도 `isValid` 방식을 통해 파일 업로드에 문제가 없었는지 확인할 수 있습니다:

```php
if ($request->file('photo')->isValid()) {
    // ...
}
```



<a name="file-paths-extensions"></a>
#### 파일 경로 및 확장자

`UploadedFile` 클래스는 파일의 전체 경로와 확장자에 접근하기 위한 메서드도 포함하고 있습니다. `extension` 메서드는 파일의 내용을 기반으로 확장자를 추측하려고 시도합니다. 이 확장자는 클라이언트가 제공한 확장자와 다를 수 있습니다:

```php
$path = $request->photo->path();

$extension = $request->photo->extension();
```



<a name="other-file-methods"></a>
#### Other File Methods

There are a variety of other methods available on `UploadedFile` instances. Check out the [API documentation for the class](https://github.com/symfony/symfony/blob/6.0/src/Symfony/Component/HttpFoundation/File/UploadedFile.php) for more information regarding these methods.

<a name="storing-uploaded-files"></a>
### Storing Uploaded Files

To store an uploaded file, you will typically use one of your configured [filesystems](/docs/{{version}}/filesystem). The `UploadedFile` class has a `store` method that will move an uploaded file to one of your disks, which may be a location on your local filesystem or a cloud storage location like Amazon S3.

The `store` method accepts the path where the file should be stored relative to the filesystem's configured root directory. This path should not contain a filename, since a unique ID will automatically be generated to serve as the filename.

The `store` method also accepts an optional second argument for the name of the disk that should be used to store the file. The method will return the path of the file relative to the disk's root:

```php
$path = $request->photo->store('images');

$path = $request->photo->store('images', 's3');
```



파일 이름이 자동으로 생성되지 않도록 하려면 경로, 파일 이름 및 디스크 이름을 인수로 받는 `storeAs` 메서드를 사용할 수 있습니다:

```php
$path = $request->photo->storeAs('images', 'filename.jpg');

$path = $request->photo->storeAs('images', 'filename.jpg', 's3');
```



> [!NOTE]
> Laravel에서 파일 저장에 대한 자세한 정보를 보려면 전체 [파일 저장 문서](/docs/{{version}}/filesystem)를 확인하세요.

<a name="configuring-trusted-proxies"></a>
## 신뢰할 수 있는 프록시 구성

TLS/SSL 인증서를 종료하는 로드 밸런서 뒤에서 애플리케이션을 실행할 때, `url` 헬퍼를 사용할 때 애플리케이션이 때때로 HTTPS 링크를 생성하지 않는 것을 알 수 있습니다. 일반적으로 이는 로드 밸런서에서 포트 80으로 트래픽이 전달되고 있어 애플리케이션이 안전한 링크를 생성해야 하는지 모를 때 발생합니다.

이를 해결하려면, Laravel 애플리케이션에 포함된 `Illuminate\Http\Middleware\TrustProxies` 미들웨어를 활성화할 수 있으며, 이를 통해 애플리케이션에서 신뢰할 수 있는 로드 밸런서 또는 프록시를 빠르게 사용자 지정할 수 있습니다. 신뢰할 수 있는 프록시는 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용하여 지정해야 합니다.

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: [
        '192.168.1.1',
        '10.0.0.0/8',
    ]);
})
```



신뢰할 수 있는 프록시를 구성하는 것 외에도, 신뢰해야 하는 프록시 헤더도 구성할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(headers: Request::HEADER_X_FORWARDED_FOR |
        Request::HEADER_X_FORWARDED_HOST |
        Request::HEADER_X_FORWARDED_PORT |
        Request::HEADER_X_FORWARDED_PROTO |
        Request::HEADER_X_FORWARDED_AWS_ELB
    );
})
```



> [!NOTE]
> AWS Elastic Load Balancing을 사용하는 경우, `headers` 값은 `Request::HEADER_X_FORWARDED_AWS_ELB`이어야 합니다. 로드 밸런서가 [RFC 7239](https://www.rfc-editor.org/rfc/rfc7239#section-4)에서 정의된 표준 `Forwarded` 헤더를 사용하는 경우, `headers` 값은 `Request::HEADER_FORWARDED`이어야 합니다. `headers` 값에 사용할 수 있는 상수에 대한 자세한 내용은 Symfony의 [프록시 신뢰](https://symfony.com/doc/current/deployment/proxies.html) 문서를 확인하십시오.

<a name="trusting-all-proxies"></a>
#### 모든 프록시 신뢰하기

Amazon AWS 또는 다른 "클라우드" 로드 밸런서 제공자를 사용 중인 경우, 실제 로드 밸런서의 IP 주소를 알지 못할 수 있습니다. 이 경우, 모든 프록시를 신뢰하기 위해 `*`를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```



<a name="configuring-trusted-hosts"></a>
## Configuring Trusted Hosts

By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request.

Typically, you should configure your web server, such as Nginx or Apache, to only send requests to your application that match a given hostname. However, if you do not have the ability to customize your web server directly and need to instruct Laravel to only respond to certain hostnames, you may do so by enabling the `Illuminate\Http\Middleware\TrustHosts` middleware for your application.

To enable the `TrustHosts` middleware, you should invoke the `trustHosts` middleware method in your application's `bootstrap/app.php` file. Using the `at` argument of this method, you may specify the hostnames that your application should respond to. The hostname string is treated as a regular expression. Incoming requests with other `Host` headers will be rejected:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$']);
})
```



기본적으로 애플리케이션 URL의 하위 도메인에서 오는 요청도 자동으로 신뢰됩니다. 이 동작을 비활성화하려면 `subdomains` 인수를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: ['^laravel\.test$'], subdomains: false);
})
```



신뢰할 수 있는 호스트를 확인하기 위해 애플리케이션의 구성 파일이나 데이터베이스에 접근해야 하는 경우, `at` 인자에 클로저를 제공할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustHosts(at: fn () => config('app.trusted_hosts'));
})
```
{% endraw %}
