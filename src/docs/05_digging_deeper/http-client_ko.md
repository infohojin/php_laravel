---
layout: docs
title: "HTTP Client"
---

{% raw %}
---
layout: docs
title: "HTTP Client"
---

# HTTP Client

- [Introduction](#introduction)
- [Making Requests](#making-requests)
    - [Request Data](#request-data)
    - [Headers](#headers)
    - [Authentication](#authentication)
    - [Timeout](#timeout)
    - [Retries](#retries)
    - [Error Handling](#error-handling)
    - [Guzzle Middleware](#guzzle-middleware)
    - [Guzzle Options](#guzzle-options)
- [Concurrent Requests](#concurrent-requests)
    - [Request Pooling](#request-pooling)
    - [Request Batching](#request-batching)
- [Macros](#macros)
- [Testing](#testing)
    - [Faking Responses](#faking-responses)
    - [Inspecting Requests](#inspecting-requests)
    - [Preventing Stray Requests](#preventing-stray-requests)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Laravel provides an expressive, minimal API around the [Guzzle HTTP client](http://docs.guzzlephp.org/en/stable/), allowing you to quickly make outgoing HTTP requests to communicate with other web applications. Laravel's wrapper around Guzzle is focused on its most common use cases and a wonderful developer experience.

<a name="making-requests"></a>
## Making Requests

To make requests, you may use the `head`, `get`, `post`, `put`, `patch`, and `delete` methods provided by the `Http` facade. First, let's examine how to make a basic `GET` request to another URL:

```php
use Illuminate\Support\Facades\Http;

$response = Http::get('http://example.com');
```



`get` 메서드는 `Illuminate\Http\Client\Response`의 인스턴스를 반환하며, 이 인스턴스는 응답을 검사하는 데 사용할 수 있는 다양한 메서드를 제공합니다:

```php
$response->body() : string;
$response->json($key = null, $default = null, $flags = null) : mixed;
$response->object() : object;
$response->collect($key = null) : Illuminate\Support\Collection;
$response->resource() : resource;
$response->status() : int;
$response->successful() : bool;
$response->redirect(): bool;
$response->failed() : bool;
$response->clientError() : bool;
$response->header($header) : string;
$response->headers() : array;
```



`Illuminate\Http\Client\Response` 객체는 또한 PHP `ArrayAccess` 인터페이스를 구현하여 응답에서 JSON 응답 데이터를 직접 액세스할 수 있습니다:

```php
return Http::get('http://example.com/users/1')['name'];
```



위에 나열된 응답 방법 외에도, 응답이 특정 상태 코드를 갖는지 확인하기 위해 다음과 같은 방법을 사용할 수 있습니다:

```php
$response->ok() : bool;                  // 200 OK
$response->created() : bool;             // 201 Created
$response->accepted() : bool;            // 202 Accepted
$response->noContent() : bool;           // 204 No Content
$response->movedPermanently() : bool;    // 301 Moved Permanently
$response->found() : bool;               // 302 Found
$response->badRequest() : bool;          // 400 Bad Request
$response->unauthorized() : bool;        // 401 Unauthorized
$response->paymentRequired() : bool;     // 402 Payment Required
$response->forbidden() : bool;           // 403 Forbidden
$response->notFound() : bool;            // 404 Not Found
$response->requestTimeout() : bool;      // 408 Request Timeout
$response->conflict() : bool;            // 409 Conflict
$response->unprocessableEntity() : bool; // 422 Unprocessable Entity
$response->tooManyRequests() : bool;     // 429 Too Many Requests
$response->serverError() : bool;         // 500 Internal Server Error
```



<a name="uri-templates"></a>
#### URI 템플릿

HTTP 클라이언트는 [URI 템플릿 명세](https://www.rfc-editor.org/rfc/rfc6570)를 사용하여 요청 URL을 구성할 수도 있습니다. URI 템플릿으로 확장할 수 있는 URL 매개변수를 정의하려면 `withUrlParameters` 메서드를 사용할 수 있습니다:

```php
Http::withUrlParameters([
    'endpoint' => 'https://laravel.com',
    'page' => 'docs',
    'version' => '13.x',
    'topic' => 'validation',
])->get('{+endpoint}/{page}/{version}/{topic}');
```



<a name="dumping-requests"></a>
#### 요청 덤프

보내기 전에 나가는 요청 인스턴스를 덤프하고 스크립트 실행을 종료하고 싶다면, 요청 정의의 시작 부분에 `dd` 메서드를 추가할 수 있습니다:

```php
return Http::dd()->get('http://example.com');
```



<a name="request-data"></a>
### 요청 데이터

물론, `POST`, `PUT` 및 `PATCH` 요청을 할 때 추가 데이터를 함께 보내는 것이 일반적이므로, 이러한 메서드는 두 번째 인수로 데이터 배열을 받습니다. 기본적으로 데이터는 `application/json` 콘텐츠 유형을 사용하여 전송됩니다:

```php
use Illuminate\Support\Facades\Http;

$response = Http::post('http://example.com/users', [
    'name' => 'Steve',
    'role' => 'Network Administrator',
]);
```



<a name="get-request-query-parameters"></a>
#### GET 요청 쿼리 매개변수

`GET` 요청을 할 때, 쿼리 문자열을 URL에 직접 추가하거나 `get` 메서드의 두 번째 인수로 키/값 쌍의 배열을 전달할 수 있습니다:

```php
$response = Http::get('http://example.com/users', [
    'name' => 'Taylor',
    'page' => 1,
]);
```



또는 `withQueryParameters` 방법을 사용할 수 있습니다:

```php
Http::retry(3, 100)->withQueryParameters([
    'name' => 'Taylor',
    'page' => 1,
])->get('http://example.com/users');
```



<a name="sending-form-url-encoded-requests"></a>
#### 폼 URL 인코딩 요청 보내기

`application/x-www-form-urlencoded` 콘텐츠 유형을 사용하여 데이터를 보내고 싶다면, 요청을 하기 전에 `asForm` 메서드를 호출해야 합니다:

```php
$response = Http::asForm()->post('http://example.com/users', [
    'name' => 'Sara',
    'role' => 'Privacy Consultant',
]);
```



<a name="sending-a-raw-request-body"></a>
#### 원시 요청 본문 보내기

요청을 할 때 원시 요청 본문을 제공하고 싶다면 `withBody` 메서드를 사용할 수 있습니다. 콘텐츠 유형은 메서드의 두 번째 인수를 통해 제공할 수 있습니다:

```php
$response = Http::withBody(
    base64_encode($photo), 'image/jpeg'
)->post('http://example.com/photo');
```



<a name="multi-part-requests"></a>
#### 다중 파트 요청

파일을 다중 파트 요청으로 보내고 싶다면, 요청을 만들기 전에 `attach` 메서드를 호출해야 합니다. 이 메서드는 파일의 이름과 내용을 받습니다. 필요하다면 세 번째 인자를 제공할 수 있으며, 이는 파일의 파일명으로 간주되며, 네 번째 인자는 파일과 관련된 헤더를 제공하는 데 사용할 수 있습니다:

```php
$response = Http::attach(
    'attachment', file_get_contents('photo.jpg'), 'photo.jpg', ['Content-Type' => 'image/jpeg']
)->post('http://example.com/attachments');
```



파일의 원시 내용을 전달하는 대신, 스트림 리소스를 전달할 수 있습니다:

```php
$photo = fopen('photo.jpg', 'r');

$response = Http::attach(
    'attachment', $photo, 'photo.jpg'
)->post('http://example.com/attachments');
```



<a name="headers"></a>
### 헤더

요청에 헤더는 `withHeaders` 메서드를 사용하여 추가할 수 있습니다. 이 `withHeaders` 메서드는 키 / 값 쌍의 배열을 받습니다:

```php
$response = Http::withHeaders([
    'X-First' => 'foo',
    'X-Second' => 'bar'
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```



요청에 대한 응답으로 애플리케이션이 예상하는 콘텐츠 유형을 지정하기 위해 `accept` 방식을 사용할 수 있습니다:

```php
$response = Http::accept('application/json')->get('http://example.com/users');
```



편의를 위해, 요청에 대한 응답에서 애플리케이션이 `application/json` 콘텐츠 유형을 예상함을 빠르게 지정하기 위해 `acceptJson` 방법을 사용할 수 있습니다:

```php
$response = Http::acceptJson()->get('http://example.com/users');
```



`withHeaders` 방식은 새 헤더를 요청의 기존 헤더에 병합합니다. 필요하다면 `replaceHeaders` 방식을 사용하여 모든 헤더를 완전히 교체할 수 있습니다:

```php
$response = Http::withHeaders([
    'X-Original' => 'foo',
])->replaceHeaders([
    'X-Replacement' => 'bar',
])->post('http://example.com/users', [
    'name' => 'Taylor',
]);
```



<a name="authentication"></a>
### 인증

`withBasicAuth` 및 `withDigestAuth` 메서드를 사용하여 각각 기본 인증 및 다이제스트 인증 자격 증명을 지정할 수 있습니다:

```php
// Basic authentication...
$response = Http::withBasicAuth('taylor@laravel.com', 'secret')->post(/* ... */);

// Digest authentication...
$response = Http::withDigestAuth('taylor@laravel.com', 'secret')->post(/* ... */);
```



<a name="bearer-tokens"></a>
#### 베어러 토큰

요청의 `Authorization` 헤더에 베어러 토큰을 빠르게 추가하려면, `withToken` 방법을 사용할 수 있습니다:

```php
$response = Http::withToken('token')->post(/* ... */);
```



<a name="timeout"></a>
### 타임아웃

`timeout` 메서드는 응답을 기다릴 최대 시간을 초 단위로 지정하는 데 사용될 수 있습니다. 기본적으로 HTTP 클라이언트는 30초 후에 타임아웃됩니다:

```php
$response = Http::timeout(3)->get(/* ... */);
```



주어진 타임아웃을 초과하면 `Illuminate\Http\Client\ConnectionException`의 인스턴스가 던져집니다.

`connectTimeout` 메서드를 사용하여 서버에 연결을 시도하는 동안 기다릴 최대 시간을 초 단위로 지정할 수 있습니다. 기본값은 10초입니다:

```php
$response = Http::connectTimeout(3)->get(/* ... */);
```



<a name="retries"></a>
### 재시도

클라이언트 또는 서버 오류가 발생할 경우 HTTP 클라이언트가 요청을 자동으로 재시도하도록 하려면 `retry` 메서드를 사용할 수 있습니다. `retry` 메서드는 요청을 시도해야 하는 최대 횟수와 Laravel이 시도 사이에 기다려야 하는 밀리초 수를 허용합니다:

```php
$response = Http::retry(3, 100)->post(/* ... */);
```



시도 간에 대기할 밀리초 수를 수동으로 계산하고 싶다면 `retry` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다:

```php
use Exception;

$response = Http::retry(3, function (int $attempt, Exception $exception) {
    return $attempt * 100;
})->post(/* ... */);
```



편의를 위해, `retry` 메서드의 첫 번째 인수로 배열을 제공할 수도 있습니다. 이 배열은 이후 시도 사이에 얼마나 많은 밀리초 동안 대기할지 결정하는 데 사용됩니다:

```php
$response = Http::retry([100, 200])->post(/* ... */);
```



필요한 경우, `retry` 메서드에 세 번째 인수를 전달할 수 있습니다. 세 번째 인수는 재시도를 실제로 시도할지 결정하는 호출 가능한 객체여야 합니다. 예를 들어, 초기 요청이 `ConnectionException`를 만났을 경우에만 요청을 재시도하도록 하고 싶을 수 있습니다:

```php
use Illuminate\Http\Client\PendingRequest;
use Throwable;

$response = Http::retry(3, 100, function (Throwable $exception, PendingRequest $request) {
    return $exception instanceof ConnectionException;
})->post(/* ... */);
```



요청 시도가 실패하면, 새로운 시도가 이루어지기 전에 요청을 변경하고 싶을 수 있습니다. 이는 `retry` 메서드에 제공한 호출 가능 객체에 제공된 request 인수를 수정함으로써 달성할 수 있습니다. 예를 들어, 첫 번째 시도가 인증 오류를 반환한 경우 새로운 인증 토큰으로 요청을 재시도하고 싶을 수 있습니다:

```php
use Illuminate\Http\Client\PendingRequest;
use Illuminate\Http\Client\RequestException;
use Throwable;

$response = Http::withToken($this->getToken())->retry(2, 0, function (Throwable $exception, PendingRequest $request) {
    if (! $exception instanceof RequestException || $exception->response->status() !== 401) {
        return false;
    }

    $request->withToken($this->getNewToken());

    return true;
})->post(/* ... */);
```



모든 요청이 실패하면 `Illuminate\Http\Client\RequestException`의 인스턴스가 발생합니다. 이 동작을 비활성화하려면 `throw` 인수를 `false` 값과 함께 제공할 수 있습니다. 비활성화하면 모든 재시도가 시도된 후 클라이언트가 받은 마지막 응답이 반환됩니다:

```php
$response = Http::retry(3, 100, throw: false)->post(/* ... */);
```



> [!WARNING]
> 모든 요청이 연결 문제로 실패하는 경우, `throw` 인수가 `false`로 설정되어 있어도 `Illuminate\Http\Client\ConnectionException`가 여전히 발생합니다.

<a name="error-handling"></a>
### 오류 처리

Guzzle의 기본 동작과 달리, Laravel의 HTTP 클라이언트 래퍼는 클라이언트 또는 서버 오류(`400` 및 `500` 수준 서버 응답) 발생 시 예외를 던지지 않습니다. 이러한 오류 중 하나가 반환되었는지 여부는 `successful`, `clientError` 또는 `serverError` 메서드를 사용하여 확인할 수 있습니다:

```php
// Determine if the status code is >= 200 and < 300...
$response->successful();

// Determine if the status code is >= 400...
$response->failed();

// Determine if the response has a 400 level status code...
$response->clientError();

// Determine if the response has a 500 level status code...
$response->serverError();

// Immediately execute the given callback if there was a client or server error...
$response->onError(callable $callback);
```



<a name="throwing-exceptions"></a>
#### 예외 던지기

응답 인스턴스가 있고 응답 상태 코드가 클라이언트 또는 서버 오류를 나타내는 경우 `Illuminate\Http\Client\RequestException` 인스턴스를 던지고 싶다면, `throw` 또는 `throwIf` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\Response;

$response = Http::post(/* ... */);

// Throw an exception if a client or server error occurred...
$response->throw();

// Throw an exception if an error occurred and the given condition is true...
$response->throwIf($condition);

// Throw an exception if an error occurred and the given closure resolves to true...
$response->throwIf(fn (Response $response) => true);

// Throw an exception if an error occurred and the given condition is false...
$response->throwUnless($condition);

// Throw an exception if an error occurred and the given closure resolves to false...
$response->throwUnless(fn (Response $response) => false);

// Throw an exception if the response has a specific status code...
$response->throwIfStatus(403);

// Throw an exception unless the response has a specific status code...
$response->throwUnlessStatus(200);

// Throw an exception if a server error occurred (status >500)...
$response->throwIfServerError();

// Throw an exception if a client error occurred (status >400 and <500)...
$response->throwIfClientError();

return $response['user']['id'];
```



`Illuminate\Http\Client\RequestException` 인스턴스에는 반환된 응답을 검사할 수 있는 공개 `$response` 속성이 있습니다.

`throw` 메서드는 오류가 발생하지 않은 경우 응답 인스턴스를 반환하므로, 다른 작업을 `throw` 메서드에 연결할 수 있습니다:

```php
return Http::post(/* ... */)->throw()->json();
```



예외가 발생하기 전에 추가적인 로직을 수행하고 싶다면 `throw` 메서드에 클로저를 전달할 수 있습니다. 클로저가 호출된 후 예외는 자동으로 발생하므로 클로저 내에서 예외를 다시 던질 필요가 없습니다:

```php
use Illuminate\Http\Client\Response;
use Illuminate\Http\Client\RequestException;

return Http::post(/* ... */)->throw(function (Response $response, RequestException $e) {
    // ...
})->json();
```



기본적으로 `RequestException` 메시지는 기록되거나 보고될 때 120자로 잘립니다. 이 동작을 사용자 정의하거나 비활성화하려면, `bootstrap/app.php` 파일에서 애플리케이션의 등록된 동작을 구성할 때 `truncateAt` 및 `dontTruncate` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Client\RequestException;

->registered(function (): void {
    // Truncate request exception messages to 240 characters...
    RequestException::truncateAt(240);

    // Disable request exception message truncation...
    RequestException::dontTruncate();
})
```



또는 `truncateExceptionsAt` 메서드를 사용하여 요청별로 예외 잘림 동작을 사용자 지정할 수 있습니다:

```php
return Http::truncateExceptionsAt(240)->post(/* ... */);
```



<a name="guzzle-middleware"></a>
### Guzzle 미들웨어

Laravel의 HTTP 클라이언트는 Guzzle로 구동되기 때문에, [Guzzle 미들웨어](https://docs.guzzlephp.org/en/stable/handlers-and-middleware.html)를 이용하여 나가는 요청을 조작하거나 들어오는 응답을 검사할 수 있습니다. 나가는 요청을 조작하려면, `withRequestMiddleware` 메서드를 통해 Guzzle 미들웨어를 등록하세요:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\RequestInterface;

$response = Http::withRequestMiddleware(
    function (RequestInterface $request) {
        return $request->withHeader('X-Example', 'Value');
    }
)->get('http://example.com');
```



마찬가지로, `withResponseMiddleware` 메서드를 통해 미들웨어를 등록하여 들어오는 HTTP 응답을 검사할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;
use Psr\Http\Message\ResponseInterface;

$response = Http::withResponseMiddleware(
    function (ResponseInterface $response) {
        $header = $response->getHeader('X-Example');

        // ...

        return $response;
    }
)->get('http://example.com');
```



<a name="global-middleware"></a>
#### 글로벌 미들웨어

때때로, 모든 나가는 요청과 들어오는 응답에 적용되는 미들웨어를 등록하고 싶을 때가 있습니다. 이를 달성하기 위해 `globalRequestMiddleware`와 `globalResponseMiddleware` 메서드를 사용할 수 있습니다. 일반적으로, 이러한 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출되어야 합니다:

```php
use Illuminate\Support\Facades\Http;

Http::globalRequestMiddleware(fn ($request) => $request->withHeader(
    'User-Agent', 'Example Application/1.0'
));

Http::globalResponseMiddleware(fn ($response) => $response->withHeader(
    'X-Finished-At', now()->toDateTimeString()
));
```



<a name="guzzle-options"></a>
### Guzzle 옵션

`withOptions` 메서드를 사용하여 발신 요청에 대한 추가 [Guzzle 요청 옵션](http://docs.guzzlephp.org/en/stable/request-options.html)을 지정할 수 있습니다. `withOptions` 메서드는 키/값 쌍 배열을 받습니다:

```php
$response = Http::withOptions([
    'debug' => true,
])->get('http://example.com/users');
```



<a name="global-options"></a>
#### 전역 옵션

모든 발신 요청에 대한 기본 옵션을 구성하려면 `globalOptions` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출되어야 합니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::globalOptions([
        'allow_redirects' => false,
    ]);
}
```



<a name="concurrent-requests"></a>
## 동시 요청

때때로 여러 HTTP 요청을 동시에 보내고 싶을 때가 있습니다. 다시 말해, 요청을 순차적으로 보내는 대신 여러 요청을 동시에 발송하고자 할 때가 있습니다. 이는 느린 HTTP API와 상호작용할 때 상당한 성능 향상을 가져올 수 있습니다.

<a name="request-pooling"></a>
### 요청 풀링

다행히도, 이는 `pool` 메서드를 사용하여 달성할 수 있습니다. `pool` 메서드는 `Illuminate\Http\Client\Pool` 인스턴스를 받는 클로저를 허용하여, 요청을 쉽게 요청 풀에 추가하고 발송할 수 있습니다:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->get('http://localhost/first'),
    $pool->get('http://localhost/second'),
    $pool->get('http://localhost/third'),
]);

return $responses[0]->ok() &&
       $responses[1]->ok() &&
       $responses[2]->ok();
```



보시다시피, 각 응답 인스턴스는 풀에 추가된 순서에 따라 접근할 수 있습니다. 원하신다면, `as` 방식을 사용하여 요청에 이름을 지정할 수 있으며, 이를 통해 이름으로 해당 응답에 접근할 수 있습니다:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$responses = Http::pool(fn (Pool $pool) => [
    $pool->as('first')->get('http://localhost/first'),
    $pool->as('second')->get('http://localhost/second'),
    $pool->as('third')->get('http://localhost/third'),
]);

return $responses['first']->ok();
```



요청 풀의 최대 동시성은 `pool` 메서드에 `concurrency` 인수를 제공하여 제어할 수 있습니다. 이 값은 요청 풀을 처리하는 동안 동시에 진행 중일 수 있는 HTTP 요청의 최대 수를 결정합니다:

```php
$responses = Http::pool(fn (Pool $pool) => [
    // ...
], concurrency: 5);
```



풀링된 요청이 연결 수준에서 실패하면(예: 타임아웃 또는 DNS 실패), `$responses` 배열의 해당 항목은 `Response` 인스턴스 대신 `Illuminate\Http\Client\ConnectionException` 인스턴스가 됩니다:

```php
foreach ($responses as $response) {
    if ($response instanceof Throwable) {
        // The request failed to connect...
    } elseif ($response->failed()) {
        // The request connected but received an error response...
    }
}
```



<a name="customizing-concurrent-requests"></a>
#### 동시 요청 사용자 정의

`pool` 메서드는 `withHeaders` 또는 `middleware` 메서드와 같은 다른 HTTP 클라이언트 메서드와 체인할 수 없습니다. 풀링된 요청에 사용자 정의 헤더나 미들웨어를 적용하려면, 풀의 각 요청에서 해당 옵션을 구성해야 합니다:

```php
use Illuminate\Http\Client\Pool;
use Illuminate\Support\Facades\Http;

$headers = [
    'X-Example' => 'example',
];

$responses = Http::pool(fn (Pool $pool) => [
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
    $pool->withHeaders($headers)->get('http://laravel.test/test'),
]);
```



<a name="request-batching"></a>
### 요청 배치

Laravel에서 동시 요청을 처리하는 또 다른 방법은 `batch` 메서드를 사용하는 것입니다. `pool` 메서드와 마찬가지로, 이 메서드는 `Illuminate\Http\Client\Batch` 인스턴스를 받는 클로저를 수락하며, 덕분에 요청을 쉽게 요청 풀에 추가하여 전송할 수 있지만, 완료 콜백을 정의할 수도 있습니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Http\Client\ConnectionException;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Client\Response;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->before(function (Batch $batch) {
    // The batch has been created but no requests have been initialized...
})->progress(function (Batch $batch, int|string $key, Response $response) {
    // An individual request has completed successfully...
})->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->catch(function (Batch $batch, int|string $key, Response|RequestException|ConnectionException $response) {
    // Batch request failure detected...
})->finally(function (Batch $batch, array $results) {
    // The batch has finished executing...
})->send();
```



`pool` 방법처럼, `as` 방법을 사용하여 요청의 이름을 지정할 수 있습니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    $batch->as('first')->get('http://localhost/first'),
    $batch->as('second')->get('http://localhost/second'),
    $batch->as('third')->get('http://localhost/third'),
])->send();
```



`send` 메서드를 호출하여 `batch`를 시작한 후에는 여기에 새로운 요청을 추가할 수 없습니다. 시도할 경우 `Illuminate\Http\Client\BatchInProgressException` 예외가 발생합니다.

요청 배치의 최대 동시 실행 수는 `concurrency` 메서드를 통해 제어할 수 있습니다. 이 값은 요청 배치를 처리하는 동안 동시에 진행 중일 수 있는 최대 HTTP 요청 수를 결정합니다:

```php
$responses = Http::batch(fn (Batch $batch) => [
    // ...
])->concurrency(5)->send();
```



<a name="inspecting-batches"></a>
#### 배치 검사

배치 완료 콜백에 제공되는 `Illuminate\Http\Client\Batch` 인스턴스에는 주어진 요청 배치를 상호작용하고 검사하는 데 도움이 되는 다양한 속성과 메서드가 있습니다:

```php
// The number of requests assigned to the batch...
$batch->totalRequests;

// The number of requests that have not been processed yet...
$batch->pendingRequests;

// The number of requests that have failed...
$batch->failedRequests;

// The number of requests that have been processed thus far...
$batch->processedRequests();

// Indicates if the batch has finished executing...
$batch->finished();

// Indicates if the batch has request failures...
$batch->hasFailures();
```

<a name="deferring-batches"></a>
#### 배치 연기

`defer` 메서드가 호출되면, 요청 배치는 즉시 실행되지 않습니다. 대신, Laravel은 현재 애플리케이션 요청의 HTTP 응답이 사용자에게 전송된 후 배치를 실행하여 애플리케이션이 빠르고 반응성이 좋게 느껴지도록 합니다:

```php
use Illuminate\Http\Client\Batch;
use Illuminate\Support\Facades\Http;

$responses = Http::batch(fn (Batch $batch) => [
    $batch->get('http://localhost/first'),
    $batch->get('http://localhost/second'),
    $batch->get('http://localhost/third'),
])->then(function (Batch $batch, array $results) {
    // All requests completed successfully...
})->defer();
```



<a name="macros"></a>
## 매크로

라라벨 HTTP 클라이언트는 "매크로"를 정의할 수 있게 해주며, 이는 애플리케이션 전반에서 서비스와 상호작용할 때 일반적인 요청 경로와 헤더를 구성하는 유창하고 표현력 있는 메커니즘으로 사용할 수 있습니다. 시작하려면 애플리케이션의 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 매크로를 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Http::macro('github', function () {
        return Http::withHeaders([
            'X-Example' => 'example',
        ])->baseUrl('https://github.com');
    });
}
```



매크로를 구성한 후에는 애플리케이션 어디에서나 매크로를 호출하여 지정된 구성으로 대기 중인 요청을 생성할 수 있습니다:

```php
$response = Http::github()->get('/');
```



<a name="testing"></a>
## 테스트

많은 Laravel 서비스는 테스트를 쉽고 표현력 있게 작성할 수 있도록 기능을 제공하며, Laravel의 HTTP 클라이언트도 예외가 아닙니다. `Http` 퍼사드의 `fake` 메서드는 요청이 이루어질 때 HTTP 클라이언트가 스텁 / 더미 응답을 반환하도록 지시할 수 있게 합니다.

<a name="faking-responses"></a>
### 응답 가짜 처리하기

예를 들어, 모든 요청에 대해 빈 `200` 상태 코드 응답을 반환하도록 HTTP 클라이언트에 지시하려면, `fake` 메서드를 인자 없이 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\Http;

Http::fake();

$response = Http::post(/* ... */);
```



<a name="faking-specific-urls"></a>
#### 특정 URL 위조하기

또는, `fake` 메서드에 배열을 전달할 수 있습니다. 배열의 키는 위조하고자 하는 URL 패턴과 해당 패턴에 연결된 응답을 나타내야 합니다. `*` 문자는 와일드카드 문자로 사용할 수 있습니다. 이러한 엔드포인트에 대한 스텁/위조 응답을 생성하기 위해 `Http` 퍼사드의 `response` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, $headers),

    // Stub a string response for Google endpoints...
    'google.com/*' => Http::response('Hello World', 200, $headers),
]);
```



위조되지 않은 URL에 대한 모든 요청은 실제로 실행됩니다. 모든 일치하지 않는 URL을 스텁 처리할 대체 URL 패턴을 지정하려면 단일 `*` 문자를 사용할 수 있습니다:

```php
Http::fake([
    // Stub a JSON response for GitHub endpoints...
    'github.com/*' => Http::response(['foo' => 'bar'], 200, ['Headers']),

    // Stub a string response for all other endpoints...
    '*' => Http::response('Hello World', 200, ['Headers']),
]);
```



편의를 위해, 문자열, 배열 또는 정수를 응답으로 제공하면 간단한 문자열, JSON, 및 빈 응답이 생성될 수 있습니다:

```php
Http::fake([
    'google.com/*' => 'Hello World',
    'github.com/*' => ['foo' => 'bar'],
    'chatgpt.com/*' => 200,
]);
```



<a name="faking-connection-exceptions"></a>
#### 예외 시뮬레이션

때때로 HTTP 클라이언트가 요청을 시도할 때 `Illuminate\Http\Client\ConnectionException`를 만나면 애플리케이션의 동작을 테스트해야 할 수도 있습니다. HTTP 클라이언트가 `failedConnection` 메서드를 사용하여 연결 예외를 발생시키도록 지시할 수 있습니다:

```php
Http::fake([
    'github.com/*' => Http::failedConnection(),
]);
```



`Illuminate\Http\Client\RequestException`가 발생할 경우 애플리케이션의 동작을 테스트하기 위해, `failedRequest` 메서드를 사용할 수 있습니다:

```php
$this->mock(GithubService::class)
    ->shouldReceive('getUser')
    ->andThrow(
        Http::failedRequest(['code' => 'not_found'], 404)
    );
```



<a name="faking-response-sequences"></a>
#### 응답 시퀀스 위조

때때로 단일 URL이 특정 순서로 일련의 가짜 응답을 반환해야 할 경우가 있습니다. `Http::sequence` 방법을 사용하여 응답을 생성함으로써 이를 수행할 수 있습니다:

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->pushStatus(404),
]);
```



응답 시퀀스의 모든 응답이 소비되면, 추가적인 요청은 응답 시퀀스가 예외를 발생시키게 됩니다. 시퀀스가 비어 있을 때 반환될 기본 응답을 지정하고 싶다면, `whenEmpty` 메서드를 사용할 수 있습니다:

```php
Http::fake([
    // Stub a series of responses for GitHub endpoints...
    'github.com/*' => Http::sequence()
        ->push('Hello World', 200)
        ->push(['foo' => 'bar'], 200)
        ->whenEmpty(Http::response()),
]);
```



만약 일련의 응답을 가장하고 싶지만, 가장해야 할 특정 URL 패턴을 지정할 필요가 없다면, `Http::fakeSequence` 방법을 사용할 수 있습니다:

```php
Http::fakeSequence()
    ->push('Hello World', 200)
    ->whenEmpty(Http::response());
```



<a name="fake-callback"></a>
#### 가짜 콜백

특정 엔드포인트에 대해 어떤 응답을 반환할지 결정하는 더 복잡한 로직이 필요한 경우, `fake` 메서드에 클로저를 전달할 수 있습니다. 이 클로저는 `Illuminate\Http\Client\Request`의 인스턴스를 받으며, 응답 인스턴스를 반환해야 합니다. 클로저 내에서 어떤 유형의 응답을 반환할지 결정하기 위해 필요한 모든 로직을 수행할 수 있습니다:

```php
use Illuminate\Http\Client\Request;

Http::fake(function (Request $request) {
    return Http::response('Hello World', 200);
});
```



<a name="inspecting-requests"></a>
### 요청 검사

응답을 위조할 때, 클라이언트가 수신하는 요청을 가끔 검사하여 애플리케이션이 올바른 데이터나 헤더를 보내고 있는지 확인하고 싶을 수 있습니다. 이는 `Http::fake`를 호출한 후 `Http::assertSent` 메서드를 호출하여 수행할 수 있습니다.

`assertSent` 메서드는 `Illuminate\Http\Client\Request` 인스턴스를 수신하고 요청이 기대치와 일치하는지 나타내는 boolean 값을 반환해야 하는 클로저를 허용합니다. 테스트가 통과하려면, 주어진 기대치와 일치하는 적어도 하나의 요청이 발행되어야 합니다:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::withHeaders([
    'X-First' => 'foo',
])->post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertSent(function (Request $request) {
    return $request->hasHeader('X-First', 'foo') &&
           $request->url() == 'http://example.com/users' &&
           $request['name'] == 'Taylor' &&
           $request['role'] == 'Developer';
});
```



필요한 경우, 특정 요청이 `assertNotSent` 방법을 사용하여 전송되지 않았다고 단언할 수 있습니다:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Support\Facades\Http;

Http::fake();

Http::post('http://example.com/users', [
    'name' => 'Taylor',
    'role' => 'Developer',
]);

Http::assertNotSent(function (Request $request) {
    return $request->url() === 'http://example.com/posts';
});
```



테스트 동안 얼마나 많은 요청이 '전송'되었는지 확인하기 위해 `assertSentCount` 방법을 사용할 수 있습니다:

```php
Http::fake();

Http::assertSentCount(5);
```



또는 테스트 중에 요청이 전송되지 않았음을 주장하기 위해 `assertNothingSent` 방법을 사용할 수 있습니다:

```php
Http::fake();

Http::assertNothingSent();
```



<a name="recording-requests-and-responses"></a>
#### 요청 / 응답 기록

모든 요청과 해당 응답을 수집하기 위해 `recorded` 방법을 사용할 수 있습니다. `recorded` 방법은 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response`의 인스턴스를 포함하는 배열 모음을 반환합니다:

```php
Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded();

[$request, $response] = $recorded[0];
```



또한, `recorded` 메서드는 `Illuminate\Http\Client\Request`와 `Illuminate\Http\Client\Response`의 인스턴스를 받게 될 클로저를 허용하며, 이를 사용하여 요청/응답 쌍을 기대에 맞게 필터링할 수 있습니다:

```php
use Illuminate\Http\Client\Request;
use Illuminate\Http\Client\Response;

Http::fake([
    'https://laravel.com' => Http::response(status: 500),
    'https://nova.laravel.com/' => Http::response(),
]);

Http::get('https://laravel.com');
Http::get('https://nova.laravel.com/');

$recorded = Http::recorded(function (Request $request, Response $response) {
    return $request->url() !== 'https://laravel.com' &&
           $response->successful();
});
```



<a name="preventing-stray-requests"></a>
### 잘못된 요청 방지

개별 테스트 또는 전체 테스트 스위트에서 HTTP 클라이언트를 통해 전송된 모든 요청이 조작되었는지 확인하려면 `preventStrayRequests` 메서드를 호출할 수 있습니다. 이 메서드를 호출한 후에는 해당하는 가짜 응답이 없는 요청은 실제 HTTP 요청을 만드는 대신 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::fake([
    'github.com/*' => Http::response('ok'),
]);

// An "ok" response is returned...
Http::get('https://github.com/laravel/framework');

// An exception is thrown...
Http::get('https://laravel.com');
```



때때로, 특정 요청이 실행되도록 허용하면서 대부분의 원치 않는 요청을 차단하고 싶을 수 있습니다. 이를 달성하기 위해, `allowStrayRequests` 메서드에 URL 패턴 배열을 전달할 수 있습니다. 주어진 패턴 중 하나와 일치하는 요청은 허용되며, 나머지 모든 요청은 계속해서 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades\Http;

Http::preventStrayRequests();

Http::allowStrayRequests([
    'http://127.0.0.1:5000/*',
]);

// This request is executed...
Http::get('http://127.0.0.1:5000/generate');

// An exception is thrown...
Http::get('https://laravel.com');
```



<a name="events"></a>
## 이벤트

Laravel은 HTTP 요청을 보내는 과정에서 세 가지 이벤트를 발생시킵니다. `RequestSending` 이벤트는 요청이 전송되기 전에 발생하며, `ResponseReceived` 이벤트는 특정 요청에 대한 응답을 받은 후에 발생합니다. `ConnectionFailed` 이벤트는 특정 요청에 대해 응답을 받지 못한 경우 발생합니다.

`RequestSending` 및 `ConnectionFailed` 이벤트는 모두 `Illuminate\Http\Client\Request` 인스턴스를 검사하는 데 사용할 수 있는 공개 `$request` 속성을 포함합니다. 마찬가지로, `ResponseReceived` 이벤트는 `Illuminate\Http\Client\Response` 인스턴스를 검사하는 데 사용할 수 있는 `$request` 속성과 `$response` 속성을 포함합니다. 애플리케이션 내에서 이러한 이벤트에 대한 [이벤트 리스너](/docs/{{version}}/events)를 생성할 수 있습니다:

```php
use Illuminate\Http\Client\Events\RequestSending;

class LogRequest
{
    /**
     * Handle the event.
     */
    public function handle(RequestSending $event): void
    {
        // $event->request ...
    }
}
```
{% endraw %}
