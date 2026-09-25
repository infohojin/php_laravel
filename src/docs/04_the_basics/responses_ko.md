---
layout: docs
title: "HTTP Responses"
---

{% raw %}
# HTTP Responses

- [Creating Responses](#creating-responses)
    - [Attaching Headers to Responses](#attaching-headers-to-responses)
    - [Attaching Cookies to Responses](#attaching-cookies-to-responses)
    - [Cookies and Encryption](#cookies-and-encryption)
- [Redirects](#redirects)
    - [Redirecting to Named Routes](#redirecting-named-routes)
    - [Redirecting to Controller Actions](#redirecting-controller-actions)
    - [Redirecting to External Domains](#redirecting-external-domains)
    - [Redirecting With Flashed Session Data](#redirecting-with-flashed-session-data)
- [Other Response Types](#other-response-types)
    - [View Responses](#view-responses)
    - [JSON Responses](#json-responses)
    - [File Downloads](#file-downloads)
    - [File Responses](#file-responses)
- [Streamed Responses](#streamed-responses)
    - [Consuming Streamed Responses](#consuming-streamed-responses)
    - [Streamed JSON Responses](#streamed-json-responses)
    - [Event Streams (SSE)](#event-streams)
    - [Streamed Downloads](#streamed-downloads)
- [Response Macros](#response-macros)

<a name="creating-responses"></a>
## Creating Responses

<a name="strings-arrays"></a>
#### Strings and Arrays

All routes and controllers should return a response to be sent back to the user's browser. Laravel provides several different ways to return responses. The most basic response is returning a string from a route or controller. The framework will automatically convert the string into a full HTTP response:

```php
Route::get('/', function () {
    return 'Hello World';
});
```



라우트와 컨트롤러에서 문자열을 반환하는 것 외에도 배열을 반환할 수도 있습니다. 프레임워크는 자동으로 배열을 JSON 응답으로 변환합니다:

```php
Route::get('/', function () {
    return [1, 2, 3];
});
```



> [!NOTE]
> 라우트나 컨트롤러에서 [Eloquent 컬렉션](/docs/{{version}}/eloquent-collections)을 반환할 수도 있다는 것을 알고 계셨나요? 이들은 자동으로 JSON으로 변환됩니다. 한번 시도해보세요!

<a name="response-objects"></a>
#### 응답 객체

일반적으로, 라우트 액션에서 단순 문자열이나 배열만 반환하지는 않습니다. 대신, 전체 `Illuminate\Http\Response` 인스턴스나 [뷰](/docs/{{version}}/views)를 반환하게 됩니다.

전체 `Response` 인스턴스를 반환하면, 응답의 HTTP 상태 코드와 헤더를 사용자 정의할 수 있습니다. `Response` 인스턴스는 `Symfony\Component\HttpFoundation\Response` 클래스로부터 상속되며, HTTP 응답을 구성하기 위한 다양한 메서드를 제공합니다:

```php
Route::get('/home', function () {
    return response('Hello World', 200)
        ->header('Content-Type', 'text/plain');
});
```



<a name="eloquent-models-and-collections"></a>
#### 엘로퀀트 모델과 컬렉션

라우트와 컨트롤러에서 [Eloquent ORM](/docs/{{version}}/eloquent) 모델과 컬렉션을 직접 반환할 수도 있습니다. 이렇게 하면, 라라벨은 모델의 [숨겨진 속성](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json)을 존중하면서 모델과 컬렉션을 자동으로 JSON 응답으로 변환합니다:

```php
use App\Models\User;

Route::get('/user/{user}', function (User $user) {
    return $user;
});
```



<a name="attaching-headers-to-responses"></a>
### 응답에 헤더 첨부하기

대부분의 응답 메서드는 체이닝이 가능하여, 응답 인스턴스를 유창하게 구성할 수 있다는 점을 기억하세요. 예를 들어, 사용자에게 다시 보내기 전에 일련의 헤더를 응답에 추가하기 위해 `header` 메서드를 사용할 수 있습니다:

```php
return response($content)
    ->header('Content-Type', $type)
    ->header('X-Header-One', 'Header Value')
    ->header('X-Header-Two', 'Header Value');
```



또는 `withHeaders` 방법을 사용하여 응답에 추가할 헤더 배열을 지정할 수 있습니다:

```php
return response($content)
    ->withHeaders([
        'Content-Type' => $type,
        'X-Header-One' => 'Header Value',
        'X-Header-Two' => 'Header Value',
    ]);
```



`withoutHeader` 메서드를 사용하여 나가는 응답에서 특정 헤더를 제거할 수 있습니다:

```php
return response($content)->withoutHeader('X-Debug');

return response($content)->withoutHeader(['X-Debug', 'X-Powered-By']);
```



<a name="cache-control-middleware"></a>
#### 캐시 제어 미들웨어

Laravel에는 `cache.headers` 미들웨어가 포함되어 있으며, 이것을 사용하여 그룹 라우트에 대해 `Cache-Control` 헤더를 빠르게 설정할 수 있습니다. 지침은 해당 캐시 제어 지침의 "스네이크 케이스"에 해당하는 형식으로 제공되어야 하며, 세미콜론으로 구분해야 합니다. 목록에 `etag`가 지정되면, 응답 콘텐츠의 MD5 해시가 자동으로 ETag 식별자로 설정됩니다:

```php
Route::middleware('cache.headers:public;max_age=30;s_maxage=300;stale_while_revalidate=600;etag')->group(function () {
    Route::get('/privacy', function () {
        // ...
    });

    Route::get('/terms', function () {
        // ...
    });
});
```



<a name="attaching-cookies-to-responses"></a>
### 응답에 쿠키 첨부하기

`cookie` 메서드를 사용하여 나가는 `Illuminate\Http\Response` 인스턴스에 쿠키를 첨부할 수 있습니다. 이 메서드에는 쿠키의 이름, 값, 그리고 쿠키가 유효하다고 간주될 시간을 분 단위로 전달해야 합니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes
);
```



`cookie` 메서드는 사용 빈도가 낮은 몇 가지 추가 인수도 받습니다. 일반적으로 이러한 인수는 PHP의 기본 [setcookie](https://secure.php.net/manual/en/function.setcookie.php) 메서드에 제공되는 인수와 동일한 목적과 의미를 갖습니다:

```php
return response('Hello World')->cookie(
    'name', 'value', $minutes, $path, $domain, $secure, $httpOnly
);
```



응답과 함께 쿠키가 전송되도록 보장하고 싶지만 아직 해당 응답의 인스턴스를 가지고 있지 않은 경우, `Cookie` 퍼사드를 사용하여 전송될 때 응답에 첨부될 쿠키를 '대기열'에 추가할 수 있습니다. `queue` 메서드는 쿠키 인스턴스를 생성하는 데 필요한 인수를 받습니다. 이러한 쿠키는 브라우저로 전송되기 전에 나가는 응답에 첨부됩니다:

```php
use Illuminate\Support\Facades\Cookie;

Cookie::queue('name', 'value', $minutes);
```



<a name="generating-cookie-instances"></a>
#### 쿠키 인스턴스 생성

나중에 응답 인스턴스에 첨부할 수 있는 `Symfony\Component\HttpFoundation\Cookie` 인스턴스를 생성하려면 글로벌 `cookie` 도우미를 사용할 수 있습니다. 이 쿠키는 응답 인스턴스에 첨부되지 않으면 클라이언트로 반환되지 않습니다:

```php
$cookie = cookie('name', 'value', $minutes);

return response('Hello World')->cookie($cookie);
```



<a name="expiring-cookies-early"></a>
#### 쿠키를 조기 만료시키기

나가는 응답의 `withoutCookie` 또는 `withoutCookies` 메서드를 통해 쿠키를 만료시켜 제거할 수 있습니다:

```php
return response('Hello World')->withoutCookie('name');

return response('Hello World')->withoutCookies([
    'name',
    'email',
    'preferences',
]);
```



아직 발신 응답 인스턴스가 없다면, `Cookie` 퍼사드의 `expire` 메서드를 사용하여 쿠키를 만료시킬 수 있습니다:

```php
Cookie::expire('name');
```



<a name="cookies-and-encryption"></a>
### 쿠키와 암호화

기본적으로 `Illuminate\Cookie\Middleware\EncryptCookies` 미들웨어 덕분에, Laravel에서 생성된 모든 쿠키는 암호화되고 서명되어 클라이언트가 수정하거나 읽을 수 없습니다. 애플리케이션에서 생성된 일부 쿠키에 대한 암호화를 비활성화하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `encryptCookies` 메서드를 사용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->encryptCookies(except: [
        'cookie_name',
    ]);
})
```



> [!NOTE]
> 일반적으로 쿠키 암호화는 절대 비활성화해서는 안 되며, 이는 쿠키가 잠재적인 클라이언트 측 데이터 노출 및 변조에 노출될 수 있습니다.

<a name="redirects"></a>
## 리디렉션

리디렉션 응답은 `Illuminate\Http\RedirectResponse` 클래스의 인스턴스이며, 사용자를 다른 URL로 리디렉션하는 데 필요한 적절한 헤더를 포함합니다. `RedirectResponse` 인스턴스를 생성하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 전역 `redirect` 헬퍼를 사용하는 것입니다:

```php
Route::get('/dashboard', function () {
    return redirect('/home/dashboard');
});
```



때때로 사용자가 제출한 양식이 유효하지 않은 경우와 같이 이전 위치로 사용자를 다시 보내고 싶을 수 있습니다. 전역 `back` 헬퍼 함수를 사용하여 이를 수행할 수 있습니다. 이 기능은 [세션](/docs/{{version}}/session)을 사용하므로, `back` 함수를 호출하는 경로가 `web` 미들웨어 그룹을 사용하고 있는지 확인하십시오:

```php
Route::post('/user/profile', function () {
    // Validate the request...

    return back()->withInput();
});
```



<a name="redirecting-named-routes"></a>
### 명명된 경로로 리디렉션

`redirect` 헬퍼를 매개변수 없이 호출하면 `Illuminate\Routing\Redirector` 인스턴스가 반환되어 `Redirector` 인스턴스의 모든 메서드를 호출할 수 있습니다. 예를 들어, 명명된 경로로 `RedirectResponse`를 생성하려면 `route` 메서드를 사용할 수 있습니다:

```php
return redirect()->route('login');
```



라우트에 매개변수가 있는 경우 `route` 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', ['id' => 1]);
```



<a name="populating-parameters-via-eloquent-models"></a>
#### 엘로퀀트 모델을 통해 매개변수 채우기

엘로퀀트 모델에서 채워지는 "ID" 매개변수가 있는 경로로 리디렉션하는 경우, 모델 자체를 전달할 수 있습니다. ID는 자동으로 추출됩니다:

```php
// For a route with the following URI: /profile/{id}

return redirect()->route('profile', [$user]);
```



라우트 매개변수에 배치되는 값을 사용자 지정하려면 라우트 매개변수 정의(`/profile/{id:slug}`)에서 열을 지정하거나 Eloquent 모델에서 `getRouteKey` 메서드를 재정의할 수 있습니다:

```php
/**
 * Get the value of the model's route key.
 */
public function getRouteKey(): mixed
{
    return $this->slug;
}
```



<a name="redirecting-controller-actions"></a>
### 컨트롤러 액션으로 리디렉션

[컨트롤러 액션](/docs/{{version}}/controllers)으로 리디렉션을 생성할 수도 있습니다. 그렇게 하려면 컨트롤러와 액션 이름을 `action` 메서드에 전달하세요:

```php
use App\Http\Controllers\UserController;

return redirect()->action([UserController::class, 'index']);
```



컨트롤러 경로에 매개변수가 필요한 경우, `action` 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
return redirect()->action(
    [UserController::class, 'profile'], ['id' => 1]
);
```



<a name="redirecting-external-domains"></a>
### 외부 도메인으로 리디렉션

가끔 애플리케이션 외부의 도메인으로 리디렉션해야 할 때가 있습니다. 추가적인 URL 인코딩, 검증 또는 확인 없이 `RedirectResponse`를 생성하는 `away` 메서드를 호출하여 이를 수행할 수 있습니다:

```php
return redirect()->away('https://www.google.com');
```



<a name="redirecting-with-flashed-session-data"></a>
### 플래시된 세션 데이터를 사용하여 리디렉션하기

새 URL로 리디렉션하고 [세션에 데이터를 플래시](/docs/{{version}}/session#flash-data)하는 것은 일반적으로 동시에 수행됩니다. 일반적으로 이는 성공 메시지를 세션에 플래시할 때, 어떤 작업을 성공적으로 수행한 후에 이루어집니다. 편의를 위해, `RedirectResponse` 인스턴스를 생성하고 단일 유창한 메서드 체인에서 데이터를 세션에 플래시할 수 있습니다:

```php
Route::post('/user/profile', function () {
    // ...

    return redirect('/dashboard')->with('status', 'Profile updated!');
});
```



사용자가 리디렉션된 후에는 [session](/docs/{{version}}/session)에서 플래시된 메시지를 표시할 수 있습니다. 예를 들어, [Blade 구문](/docs/{{version}}/blade)을 사용하여:

```blade
@if (session('status'))
    <div class="alert alert-success">
        {{ session('status') }}
    </div>
@endif
```



<a name="redirecting-with-input"></a>
#### 입력과 함께 리디렉션

사용자는 `RedirectResponse` 인스턴스에서 제공하는 `withInput` 메서드를 사용하여 사용자를 새로운 위치로 리디렉션하기 전에 현재 요청의 입력 데이터를 세션에 플래시할 수 있습니다. 이는 일반적으로 사용자가 유효성 검사 오류를 만난 경우에 수행됩니다. 입력 데이터가 세션에 플래시된 후, 다음 요청에서 쉽게 [검색](/docs/{{version}}/requests#retrieving-old-input)하여 폼을 다시 채울 수 있습니다:

```php
return back()->withInput();
```



<a name="other-response-types"></a>
## 다른 응답 유형

`response` 도우미는 다른 유형의 응답 인스턴스를 생성하는 데 사용할 수 있습니다. `response` 도우미가 인수 없이 호출되면 `Illuminate\Contracts\Routing\ResponseFactory` [계약](/docs/{{version}}/contracts)의 구현이 반환됩니다. 이 계약은 응답을 생성하는 데 유용한 여러 메서드를 제공합니다.

<a name="view-responses"></a>
### 뷰 응답

응답의 상태와 헤더를 제어해야 하지만 응답의 내용으로 [뷰](/docs/{{version}}/views)를 반환해야 하는 경우, `view` 메서드를 사용해야 합니다:

```php
return response()
    ->view('hello', $data, 200)
    ->header('Content-Type', $type);
```



물론, 커스텀 HTTP 상태 코드나 커스텀 헤더를 전달할 필요가 없다면, 전역 `view` 헬퍼 함수를 사용할 수 있습니다.

<a name="json-responses"></a>
### JSON 응답

`json` 메서드는 `Content-Type` 헤더를 `application/json`로 자동 설정하고, 주어진 배열을 `json_encode` PHP 함수를 사용하여 JSON으로 변환합니다:

```php
return response()->json([
    'name' => 'Abigail',
    'state' => 'CA',
]);
```



JSONP 응답을 생성하고 싶다면, `withCallback` 메서드와 함께 `json` 메서드를 사용할 수 있습니다:

```php
return response()
    ->json(['name' => 'Abigail', 'state' => 'CA'])
    ->withCallback($request->input('callback'));
```



<a name="file-downloads"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 지정된 경로에 있는 파일을 다운로드하도록 강제하는 응답을 생성하는 데 사용할 수 있습니다. `download` 메서드는 메서드의 두 번째 인수로 파일 이름을 받아, 사용자가 파일을 다운로드할 때 볼 수 있는 파일 이름을 결정합니다. 마지막으로, 세 번째 인수로 HTTP 헤더 배열을 메서드에 전달할 수 있습니다:

```php
return response()->download($pathToFile);

return response()->download($pathToFile, $name, $headers);
```



> [!WARNING]
> 파일 다운로드를 관리하는 Symfony HttpFoundation은 다운로드되는 파일이 ASCII 파일 이름을 가져야 합니다.

<a name="file-responses"></a>
### 파일 응답

`file` 메서드는 다운로드를 시작하는 대신 이미지나 PDF와 같은 파일을 사용자의 브라우저에서 직접 표시하는 데 사용할 수 있습니다. 이 메서드는 파일의 절대 경로를 첫 번째 인수로, 헤더 배열을 두 번째 인수로 받습니다:

```php
return response()->file($pathToFile);

return response()->file($pathToFile, $headers);
```



<a name="streamed-responses"></a>
## 스트리밍 응답

데이터를 생성되는 즉시 클라이언트로 스트리밍하면, 특히 매우 큰 응답의 경우 메모리 사용량을 크게 줄이고 성능을 향상시킬 수 있습니다. 스트리밍된 응답을 사용하면 클라이언트가 서버에서 데이터를 모두 전송하기 전에 데이터를 처리하기 시작할 수 있습니다:

```php
Route::get('/stream', function () {
    return response()->stream(function (): void {
        foreach (['developer', 'admin'] as $string) {
            echo $string;
            ob_flush();
            flush();
            sleep(2); // Simulate delay between chunks...
        }
    }, 200, ['X-Accel-Buffering' => 'no']);
});
```



편의를 위해, `stream` 메서드에 제공한 클로저가 [Generator](https://www.php.net/manual/en/language.generators.overview.php)를 반환하면, Laravel은 생성기가 반환하는 문자열 사이에서 자동으로 출력 버퍼를 플러시하고, Nginx 출력 버퍼링을 비활성화합니다:

```php
Route::post('/chat', function () {
    return response()->stream(function (): Generator {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```



<a name="consuming-streamed-responses"></a>
### 스트리밍된 응답 사용하기

스트리밍된 응답은 Laravel의 `stream` npm 패키지를 사용하여 소비할 수 있으며, 이 패키지는 Laravel 응답 및 이벤트 스트림과 상호작용할 수 있는 편리한 API를 제공합니다. 시작하려면 `@laravel/stream-react`, `@laravel/stream-vue`, 또는 `@laravel/stream-svelte` 패키지를 설치하세요:```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```



그런 다음, `useStream`를 사용하여 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 제공하면, 후크가 Laravel 애플리케이션에서 콘텐츠가 반환될 때 결합된 응답으로 `data`를 자동으로 업데이트합니다:```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, isFetching, isStreaming, send } = useStream("chat");

    const sendMessage = () => {
        send({
            message: `Current timestamp: ${Date.now()}`,
        });
    };

    return (
        <div>
            <div>{data}</div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
            <button onClick={sendMessage}>Send Message</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, isFetching, isStreaming, send } = useStream("chat");

const sendMessage = () => {
    send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
        <button @click="sendMessage">Send Message</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");

const sendMessage = () => {
    stream.send({
        message: `Current timestamp: ${Date.now()}`,
    });
};
</script>

<div>
    <div>{$stream.data}</div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
    <button onclick={sendMessage}>Send Message</button>
</div>
```



`send`를 통해 데이터를 스트림에 다시 보낼 때, 새 데이터를 보내기 전에 스트림에 대한 활성 연결이 취소됩니다. 모든 요청은 JSON `POST` 요청으로 전송됩니다.

> [!WARNING]
> `useStream` 후크가 애플리케이션에 `POST` 요청을 보내므로, 유효한 CSRF 토큰이 필요합니다. CSRF 토큰을 제공하는 가장 쉬운 방법은 [애플리케이션 레이아웃의 head에 메타 태그로 포함시키는 것](/docs/{{version}}/csrf#csrf-x-csrf-token)입니다.

`useStream`에 제공된 두 번째 인수는 스트림 사용 동작을 사용자 정의하는 데 사용할 수 있는 옵션 객체입니다. 이 객체의 기본 값은 아래와 같이 표시됩니다:```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        id: undefined,
        initialInput: undefined,
        headers: undefined,
        csrfToken: undefined,
        onResponse: (response: Response) => void,
        onData: (data: string) => void,
        onCancel: () => void,
        onFinish: () => void,
        onError: (error: Error) => void,
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response: Response) => void,
    onData: (data: string) => void,
    onCancel: () => void,
    onFinish: () => void,
    onError: (error: Error) => void,
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    id: undefined,
    initialInput: undefined,
    headers: undefined,
    csrfToken: undefined,
    onResponse: (response) => {},
    onData: (data) => {},
    onCancel: () => {},
    onFinish: () => {},
    onError: (error) => {},
});
</script>

<div>{$stream.data}</div>
```



`onResponse`은 스트림에서 초기 응답이 성공적으로 완료된 후 트리거되며, 원시 [Response](https://developer.mozilla.org/en-US/docs/Web/API/Response)가 콜백으로 전달됩니다. `onData`은 각 청크가 수신될 때 호출되며, 현재 청크가 콜백으로 전달됩니다. `onFinish`는 스트림이 완료되거나 fetch / read 과정에서 오류가 발생할 때 호출됩니다.

기본적으로 초기화 시 스트림에 요청이 이루어지지 않습니다. `initialInput` 옵션을 사용하여 초기 페이로드를 스트림에 전달할 수 있습니다:```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data } = useStream("chat", {
        initialInput: {
            message: "Introduce yourself.",
        },
    });

    return <div>{data}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data } = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<template>
    <div>{{ data }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat", {
    initialInput: {
        message: "Introduce yourself.",
    },
});
</script>

<div>{$stream.data}</div>
```



스트림을 수동으로 취소하려면, 훅에서 반환된 `cancel` 방법을 사용할 수 있습니다:```tsx tab=React
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, cancel } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <button onClick={cancel}>Cancel</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const { data, cancel } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <button @click="cancel">Cancel</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useStream } from "@laravel/stream-svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <button onclick={() => stream.cancel()}>Cancel</button>
</div>
```



`useStream` 훅을 사용할 때마다 스트림을 식별하기 위해 무작위 `id`가 생성됩니다. 이것은 각 요청과 함께 `X-STREAM-ID` 헤더를 통해 서버로 전송됩니다. 여러 구성 요소에서 동일한 스트림을 사용하는 경우, 자신의 `id`를 제공하여 스트림을 읽고 쓸 수 있습니다:```tsx tab=React
// App.tsx
import { useStream } from "@laravel/stream-react";

function App() {
    const { data, id } = useStream("chat");

    return (
        <div>
            <div>{data}</div>
            <StreamStatus id={id} />
        </div>
    );
}

// StreamStatus.tsx
import { useStream } from "@laravel/stream-react";

function StreamStatus({ id }) {
    const { isFetching, isStreaming } = useStream("chat", { id });

    return (
        <div>
            {isFetching && <div>Connecting...</div>}
            {isStreaming && <div>Generating...</div>}
        </div>
    );
}
```

```vue tab=Vue
<!-- App.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";
import StreamStatus from "./StreamStatus.vue";

const { data, id } = useStream("chat");
</script>

<template>
    <div>
        <div>{{ data }}</div>
        <StreamStatus :id="id" />
    </div>
</template>

<!-- StreamStatus.vue -->
<script setup lang="ts">
import { useStream } from "@laravel/stream-vue";

const props = defineProps<{
    id: string;
}>();

const { isFetching, isStreaming } = useStream("chat", { id: props.id });
</script>

<template>
    <div>
        <div v-if="isFetching">Connecting...</div>
        <div v-if="isStreaming">Generating...</div>
    </div>
</template>
```

```svelte tab=Svelte
<!-- App.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";
import StreamStatus from "./StreamStatus.svelte";

const stream = useStream("chat");
</script>

<div>
    <div>{$stream.data}</div>
    <StreamStatus id={stream.id} />
</div>

<!-- StreamStatus.svelte -->
<script>
import { useStream } from "@laravel/stream-svelte";

let { id } = $props();

const stream = useStream("chat", { id });
</script>

<div>
    {#if $stream.isFetching}
        <div>Connecting...</div>
    {/if}
    {#if $stream.isStreaming}
        <div>Generating...</div>
    {/if}
</div>
```



<a name="streamed-json-responses"></a>
### 스트리밍된 JSON 응답

JSON 데이터를 점진적으로 스트리밍해야 하는 경우, `streamJson` 방법을 사용할 수 있습니다. 이 방법은 브라우저로 점진적으로 전송해야 하며 JavaScript에서 쉽게 파싱할 수 있는 형식의 대규모 데이터셋에 특히 유용합니다:

```php
use App\Models\User;

Route::get('/users.json', function () {
    return response()->streamJson([
        'users' => User::cursor(),
    ]);
});
```



`useJsonStream` 훅은 [useStream 훅](#consuming-streamed-responses)과 동일하지만, 스트리밍이 완료되면 데이터를 JSON으로 파싱하려고 시도합니다:```tsx tab=React
import { useJsonStream } from "@laravel/stream-react";

type User = {
    id: number;
    name: string;
    email: string;
};

function App() {
    const { data, send } = useJsonStream<{ users: User[] }>("users");

    const loadUsers = () => {
        send({
            query: "taylor",
        });
    };

    return (
        <div>
            <ul>
                {data?.users.map((user) => (
                    <li>
                        {user.id}: {user.name}
                    </li>
                ))}
            </ul>
            <button onClick={loadUsers}>Load Users</button>
        </div>
    );
}
```

```vue tab=Vue
<script setup lang="ts">
import { useJsonStream } from "@laravel/stream-vue";

type User = {
    id: number;
    name: string;
    email: string;
};

const { data, send } = useJsonStream<{ users: User[] }>("users");

const loadUsers = () => {
    send({
        query: "taylor",
    });
};
</script>

<template>
    <div>
        <ul>
            <li v-for="user in data?.users" :key="user.id">
                {{ user.id }}: {{ user.name }}
            </li>
        </ul>
        <button @click="loadUsers">Load Users</button>
    </div>
</template>
```

```svelte tab=Svelte
<script>
import { useJsonStream } from "@laravel/stream-svelte";

const stream = useJsonStream("users");

const loadUsers = () => {
    stream.send({
        query: "taylor",
    });
};
</script>

<div>
    <ul>
        {#if $stream.data?.users}
            {#each $stream.data.users as user (user.id)}
                <li>{user.id}: {user.name}</li>
            {/each}
        {/if}
    </ul>
    <button onclick={loadUsers}>Load Users</button>
</div>
```



<a name="event-streams"></a>
### 이벤트 스트림(SSE)

`eventStream` 메서드는 `text/event-stream` 콘텐츠 타입을 사용하여 서버 전송 이벤트(SSE) 스트리밍 응답을 반환하는 데 사용될 수 있습니다. `eventStream` 메서드는 클로저를 받아야 하며, 응답이 사용 가능해지는 대로 스트림에 응답을 [생산](https://www.php.net/manual/en/language.generators.overview.php)해야 합니다:

```php
Route::get('/chat', function () {
    return response()->eventStream(function () {
        $stream = OpenAI::client()->chat()->createStreamed(...);

        foreach ($stream as $response) {
            yield $response->choices[0];
        }
    });
});
```



이벤트의 이름을 사용자 지정하고 싶다면, `StreamedEvent` 클래스의 인스턴스를 생성할 수 있습니다:

```php
use Illuminate\Http\StreamedEvent;

yield new StreamedEvent(
    event: 'update',
    data: $response->choices[0],
);
```



<a name="consuming-event-streams"></a>
#### 이벤트 스트림 소비

Laravel의 `stream` npm 패키지를 사용하여 이벤트 스트림을 소비할 수 있으며, 이 패키지는 Laravel 이벤트 스트림과 상호작용할 수 있는 편리한 API를 제공합니다. 시작하려면 `@laravel/stream-react`, `@laravel/stream-vue` 또는 `@laravel/stream-svelte` 패키지를 설치하십시오:```shell tab=React
npm install @laravel/stream-react
```

```shell tab=Vue
npm install @laravel/stream-vue
```

```shell tab=Svelte
npm install @laravel/stream-svelte
```



그런 다음, `useEventStream`를 사용하여 이벤트 스트림을 소비할 수 있습니다. 스트림 URL을 제공하면, 후크가 Laravel 애플리케이션에서 메시지가 반환될 때 결합된 응답으로 `message`를 자동으로 업데이트합니다:```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/chat");

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat");
</script>

<template>
  <div>{{ message }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat");
</script>

<div>{$eventStream.message}</div>
```



`useEventStream`에 제공되는 두 번째 인수는 스트림 소비 동작을 사용자 지정하는 데 사용할 수 있는 옵션 객체입니다. 이 객체의 기본값은 아래에 나와 있습니다:```jsx tab=React
import { useEventStream } from "@laravel/stream-react";

function App() {
  const { message } = useEventStream("/stream", {
    eventName: "update",
    onMessage: (message) => {
      //
    },
    onError: (error) => {
      //
    },
    onComplete: () => {
      //
    },
    endSignal: "</stream>",
    glue: " ",
  });

  return <div>{message}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useEventStream } from "@laravel/stream-vue";

const { message } = useEventStream("/chat", {
  eventName: "update",
  onMessage: (message) => {
    // ...
  },
  onError: (error) => {
    // ...
  },
  onComplete: () => {
    // ...
  },
  endSignal: "</stream>",
  glue: " ",
});
</script>
```

```svelte tab=Svelte
<script>
import { useEventStream } from "@laravel/stream-svelte";

const eventStream = useEventStream("/chat", {
    eventName: "update",
    onMessage: (event) => {
        //
    },
    onError: (error) => {
        //
    },
    onComplete: () => {
        //
    },
    endSignal: "</stream>",
    glue: " ",
    replace: false,
});
</script>
```



이벤트 스트림은 또한 애플리케이션의 프론트엔드에서 [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) 객체를 통해 수동으로 소비될 수 있습니다. 스트림이 완료되면 `eventStream` 메서드는 이벤트 스트림에 `</stream>` 업데이트를 자동으로 전송합니다:

```js
const source = new EventSource('/chat');

source.addEventListener('update', (event) => {
    if (event.data === '</stream>') {
        source.close();

        return;
    }

    console.log(event.data);
});
```



이벤트 스트림으로 전송되는 최종 이벤트를 사용자 지정하려면 `eventStream` 메서드의 `endStreamWith` 인수에 `StreamedEvent` 인스턴스를 제공할 수 있습니다:

```php
return response()->eventStream(function () {
    // ...
}, endStreamWith: new StreamedEvent(event: 'update', data: '</stream>'));
```



<a name="streamed-downloads"></a>
### 스트리밍 다운로드

때때로 특정 작업의 문자열 응답을 디스크에 내용을 기록하지 않고도 다운로드 가능한 응답으로 만들고 싶을 수 있습니다. 이러한 경우 `streamDownload` 메서드를 사용할 수 있습니다. 이 메서드는 콜백, 파일 이름, 그리고 선택적인 헤더 배열을 인수로 받습니다:

```php
use App\Services\GitHub;

return response()->streamDownload(function () {
    echo GitHub::api('repo')
        ->contents()
        ->readme('laravel', 'laravel')['contents'];
}, 'laravel-readme.md');
```



<a name="response-macros"></a>
## 응답 매크로

여러 경로와 컨트롤러에서 재사용할 수 있는 사용자 정의 응답을 정의하고 싶다면, `Response` 파사드의 `macro` 메서드를 사용할 수 있습니다. 일반적으로 이 메서드는 `boot` 메서드에서 호출해야 하며, 예를 들어 `App\Providers\AppServiceProvider` 서비스 제공자와 같은 애플리케이션의 [서비스 제공자](/docs/{{version}}/providers) 중 하나에서 호출합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Response;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Response::macro('caps', function (string $value) {
            return Response::make(strtoupper($value));
        });
    }
}
```



`macro` 함수는 첫 번째 인수로 이름을 받고 두 번째 인수로 클로저를 받습니다. 매크로의 클로저는 `ResponseFactory` 구현에서 매크로 이름을 호출하거나 `response` 도우미를 호출할 때 실행됩니다:

```php
return response()->caps('foo');
```
{% endraw %}
