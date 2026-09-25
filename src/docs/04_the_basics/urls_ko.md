---
layout: docs
title: "URL 생성"
---

{% raw %}
# URL 생성

- [서론](#introduction)
- [기본기](#the-basics)
    - [URL 생성](#generating-urls)
    - [현재 URL 접근 중](#accessing-the-current-url)
- [명명 경로 URL](#urls-for-named-routes)
    - [서명된 URL](#signed-urls)
- [컨트롤러 동작용 URL](#urls-for-controller-actions)
- [유창한 URI 객체](#fluent-uri-objects)
- [기본 값](#default-values)

<a name="introduction"></a>
## 서론

Laravel은 애플리케이션용 URL 생성을 돕는 여러 헬퍼를 제공합니다. 이 헬퍼들은 주로 템플릿과 API 응답에서 링크를 만들거나, 애플리케이션의 다른 부분으로 리디렉션 응답을 생성할 때 유용합니다.

<a name="the-basics"></a>
## 기본적인 것들

<a name="generating-urls"></a>
### URL 생성

`url` 헬퍼는 애플리케이션의 임의의 URL을 생성하는 데 사용될 수 있습니다. 생성된 URL은 애플리케이션이 현재 처리 중인 요청에서 자동으로 HTTP 또는 HTTP와 호스트 방식을 사용합니다:

```php
$post = App\Models\Post::find(1);

echo url("/posts/{$post->id}");

// http://example.com/posts/1

```

쿼리 문자열 매개변수가 있는 URL을 생성하려면 `query` 메서드를 사용할 수 있습니다:

```php
echo url()->query('/posts', ['search' => 'Laravel']);

// https://example.com/posts?search=Laravel

echo url()->query('/posts?sort=latest', ['search' => 'Laravel']);

// http://example.com/posts?sort=latest&search=Laravel

```

경로에 이미 존재하는 쿼리 문자열 매개변수를 제공하면 기존 값이 덮어쓰여집니다:

```php
echo url()->query('/posts?sort=latest', ['sort' => 'oldest']);

// http://example.com/posts?sort=oldest

```

값의 배열도 쿼리 매개변수로 전달될 수 있습니다. 이러한 값들은 생성된 URL에서 적절히 키가 지정되고 인코딩됩니다:

```php
echo $url = url()->query('/posts', ['columns' => ['title', 'body']]);

// http://example.com/posts?columns%5B0%5D=title&columns%5B1%5D=body

echo urldecode($url);

// http://example.com/posts?columns[0]=title&columns[1]=body

```

<a name="accessing-the-current-url"></a>
### 현재 URL에 접근하기

`url` 도우미에 경로가 제공되지 않으면, `Illuminate\Routing\UrlGenerator` 인스턴스가 반환되어 현재 URL에 대한 정보를 접근할 수 있습니다:

```php
// Get the current URL without the query string...
echo url()->current();

// Get the current URL including the query string...
echo url()->full();

```

이 방법들 각각은 `URL` [파사드](/docs/{{version}}/facades)를 통해서도 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\URL;

echo URL::current();

```

<a name="accessing-the-previous-url"></a>
#### 이전 URL에 접근하기

사용자가 이전에 방문한 URL을 아는 것이 도움이 될 때가 있습니다. `url` 헬퍼의 `previous` 및 `previousPath` 메서드를 통해 이전 URL에 접근할 수 있습니다:

```php
// Get the full URL for the previous request...
echo url()->previous();

// Get the path for the previous request...
echo url()->previousPath();

```

또는, [세션](/docs/{{version}}/session)을 통해 이전 URL에 [유창한 URI](#fluent-uri-objects) 인스턴스로 접근할 수 있습니다:

```php
use Illuminate\Http\Request;

Route::post('/users', function (Request $request) {
    $previousUri = $request->session()->previousUri();

    // ...
});

```

세션을 통해 이전에 방문한 URL의 라우트 이름을 가져오는 것도 가능합니다:

```php
$previousRoute = $request->session()->previousRoute();

```

<a name="urls-for-named-routes"></a>
## 명명된 라우트를 위한 URL

`route` 헬퍼는 [명명된 라우트](/docs/{{version}}/routing#named-routes)에 대한 URL을 생성하는 데 사용할 수 있습니다. 명명된 라우트를 사용하면 라우트에 정의된 실제 URL에 의존하지 않고 URL을 생성할 수 있습니다. 따라서 라우트의 URL이 변경되더라도 `route` 함수를 호출하는 부분을 수정할 필요가 없습니다. 예를 들어, 애플리케이션에 다음과 같이 정의된 라우트가 있다고 가정해 보겠습니다:

```php
Route::get('/post/{post}', function (Post $post) {
    // ...
})->name('post.show');

```

이 경로에 대한 URL을 생성하려면 다음과 같이 `route` 헬퍼를 사용할 수 있습니다:

```php
echo route('post.show', ['post' => 1]);

// http://example.com/post/1

```

물론, `route` 도우미는 여러 매개변수를 가진 경로의 URL을 생성하는 데에도 사용할 수 있습니다:

```php
Route::get('/post/{post}/comment/{comment}', function (Post $post, Comment $comment) {
    // ...
})->name('comment.show');

echo route('comment.show', ['post' => 1, 'comment' => 3]);

// http://example.com/post/1/comment/3

```

라우트의 정의 매개변수에 해당하지 않는 추가 배열 요소는 URL의 쿼리 문자열에 추가됩니다:

```php
echo route('post.show', ['post' => 1, 'search' => 'rocket']);

// http://example.com/post/1?search=rocket

```

<a name="eloquent-models"></a>
#### 엘로퀀트 모델

당신은 종종 [엘로퀀트 모델](/docs/{{version}}/eloquent)의 라우트 키(일반적으로 기본 키)를 사용하여 URL을 생성하게 될 것입니다. 이러한 이유로, 엘로퀀트 모델을 매개변수 값으로 전달할 수 있습니다. `route` 헬퍼는 모델의 라우트 키를 자동으로 추출합니다:

```php
echo route('post.show', ['post' => $post]);

```

<a name="signed-urls"></a>
### 서명된 URL

Laravel은 명명된 라우트에 대해 쉽게 "서명된(signed)" URL을 생성할 수 있도록 해줍니다. 이러한 URL에는 쿼리 문자열에 "서명(signature)" 해시가 추가되어, Laravel이 URL이 생성된 이후로 변경되지 않았는지 확인할 수 있습니다. 서명된 URL은 공개적으로 접근 가능하지만 URL 조작을 방지하기 위한 보호 계층이 필요한 라우트에서 특히 유용합니다.

예를 들어, 고객에게 이메일로 전송되는 공개 "구독 취소(unsubscribe)" 링크를 구현할 때 서명된 URL을 사용할 수 있습니다. 명명된 라우트에 대한 서명된 URL을 생성하려면 `URL` 파사드의 `signedRoute` 메서드를 사용합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::signedRoute('unsubscribe', ['user' => 1]);

```



`signedRoute` 메서드에 `absolute` 인수를 제공하여 서명된 URL 해시에서 도메인을 제외할 수 있습니다:

```php
return URL::signedRoute('unsubscribe', ['user' => 1], absolute: false);

```

지정된 시간 후에 만료되는 임시 서명된 경로 URL을 생성하려면 `temporarySignedRoute` 방법을 사용할 수 있습니다. Laravel이 임시 서명된 경로 URL을 검증할 때, 서명된 URL에 인코딩된 만료 타임스탬프가 경과하지 않았는지 확인합니다:

```php
use Illuminate\Support\Facades\URL;

return URL::temporarySignedRoute(
    'unsubscribe', now()->plus(minutes: 30), ['user' => 1]
);

```

<a name="validating-signed-route-requests"></a>
#### 서명된 경로 요청 검증

들어오는 요청이 유효한 서명을 가지고 있는지 확인하려면, 들어오는 `Illuminate\Http\Request` 인스턴스에서 `hasValidSignature` 메서드를 호출해야 합니다:

```php
use Illuminate\Http\Request;

Route::get('/unsubscribe/{user}', function (Request $request) {
    if (! $request->hasValidSignature()) {
        abort(401);
    }

    // ...
})->name('unsubscribe');

```

때때로 클라이언트 측 페이징을 수행할 때와 같이 애플리케이션의 프론트엔드가 서명된 URL에 데이터를 추가할 수 있도록 허용해야 할 수도 있습니다. 따라서 `hasValidSignatureWhileIgnoring` 메서드를 사용하여 서명된 URL을 검증할 때 무시해야 하는 요청 쿼리 매개변수를 지정할 수 있습니다. 매개변수를 무시하면 누구나 요청의 해당 매개변수를 수정할 수 있다는 점을 기억하세요:

```php
if (! $request->hasValidSignatureWhileIgnoring(['page', 'order'])) {
    abort(401);
}

```

들어오는 요청 인스턴스를 사용하여 서명된 URL을 검증하는 대신, 라우트에 `signed` (`Illuminate\Routing\Middleware\ValidateSignature`) [미들웨어](/docs/{{version}}/middleware)를 할당할 수 있습니다. 들어오는 요청에 유효한 서명이 없으면, 미들웨어는 자동으로 `403` HTTP 응답을 반환합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed');

```

서명된 URL에 URL 해시 내 도메인이 포함되어 있지 않은 경우, 미들웨어에 `relative` 인수를 제공해야 합니다:

```php
Route::post('/unsubscribe/{user}', function (Request $request) {
    // ...
})->name('unsubscribe')->middleware('signed:relative');

```

<a name="responding-to-invalid-signed-routes"></a>
#### 잘못된 서명된 경로에 응답하기

만료된 서명된 URL을 방문하면, 사용자는 `403` HTTP 상태 코드에 대한 일반 오류 페이지를 받게 됩니다. 그러나 애플리케이션의 `bootstrap/app.php` 파일에서 `InvalidSignatureException` 예외에 대한 사용자 정의 "render" 클로저를 정의하여 이 동작을 사용자화할 수 있습니다:

```php
use Illuminate\Routing\Exceptions\InvalidSignatureException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidSignatureException $e) {
        return response()->view('errors.link-expired', status: 403);
    });
})

```

<a name="urls-for-controller-actions"></a>
## 컨트롤러 액션용 URL

`action` 함수는 주어진 컨트롤러 액션에 대한 URL을 생성합니다:

```php
use App\Http\Controllers\HomeController;

$url = action([HomeController::class, 'index']);

```

컨트롤러 메서드가 라우트 매개변수를 허용하면, 함수의 두 번째 인수로 라우트 매개변수의 연관 배열을 전달할 수 있습니다:

```php
$url = action([UserController::class, 'profile'], ['id' => 1]);

```

<a name="fluent-uri-objects"></a>
## 유창한 URI 객체

Laravel의 `Uri` 클래스는 객체를 통해 URI를 생성하고 조작하기 위한 편리하고 유창한 인터페이스를 제공합니다. 이 클래스는 기본 League URI 패키지가 제공하는 기능을 감싸고 Laravel의 라우팅 시스템과 원활하게 통합됩니다.

정적 메서드를 사용하여 `Uri` 인스턴스를 쉽게 생성할 수 있습니다:

```php
use App\Http\Controllers\UserController;
use App\Http\Controllers\InvokableController;
use Illuminate\Support\Uri;

// Generate a URI instance from the given string...
$uri = Uri::of('https://example.com/path');

// Generate URI instances to paths, named routes, or controller actions...
$uri = Uri::to('/dashboard');
$uri = Uri::route('users.show', ['user' => 1]);
$uri = Uri::signedRoute('users.show', ['user' => 1]);
$uri = Uri::temporarySignedRoute('user.index', now()->plus(minutes: 5));
$uri = Uri::action([UserController::class, 'index']);
$uri = Uri::action(InvokableController::class);

// Generate a URI instance from the current request URL...
$uri = $request->uri();

// Generate a URI instance from the previous request URL...
$uri = $request->session()->previousUri();

```

URI 인스턴스를 가지게 되면, 이를 유창하게 수정할 수 있습니다:

```php
$uri = Uri::of('https://example.com')
    ->withScheme('http')
    ->withHost('test.com')
    ->withPort(8000)
    ->withPath('/users')
    ->withQuery(['page' => 2])
    ->withFragment('section-1');

```

유창한 URI 객체로 작업하는 방법에 대한 자세한 정보는 [URI 문서](/docs/{{version}}/helpers#uri)를 참조하세요.

<a name="default-values"></a>
## 기본 값

일부 애플리케이션의 경우 특정 URL 매개변수에 대한 요청 전체 기본 값을 지정하고자 할 수 있습니다. 예를 들어, 많은 경로가 `{locale}` 매개변수를 정의한다고 가정해 보세요:

```php
Route::get('/{locale}/posts', function () {
    // ...
})->name('post.index');

```



`route` 헬퍼를 호출할 때마다 `locale`를 항상 전달하는 것은 번거롭습니다. 따라서 현재 요청 동안 항상 적용될 이 매개변수의 기본값을 정의하기 위해 `URL::defaults` 메서드를 사용할 수 있습니다. 현재 요청에 접근할 수 있도록 이 메서드를 [라우트 미들웨어](/docs/{{version}}/middleware#assigning-middleware-to-routes)에서 호출하는 것이 좋습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\URL;
use Symfony\Component\HttpFoundation\Response;

class SetDefaultLocaleForUrls
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        URL::defaults(['locale' => $request->user()->locale]);

        return $next($request);
    }
}

```



`locale` 매개변수의 기본값이 설정되면, `route` 헬퍼를 통해 URL을 생성할 때 더 이상 해당 값을 전달할 필요가 없습니다.

<a name="url-defaults-middleware-priority"></a>
#### URL 기본값과 미들웨어 우선순위

URL 기본값을 설정하면 Laravel의 암시적 모델 바인딩 처리에 영향을 줄 수 있습니다. 따라서 URL 기본값을 설정하는 [미들웨어의 우선순위를](/docs/{{version}}/middleware#sorting-middleware) Laravel 자체 `SubstituteBindings` 미들웨어보다 먼저 실행되도록 지정해야 합니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `priority` 미들웨어 메서드를 사용하여 수행할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->prependToPriorityList(
        before: \Illuminate\Routing\Middleware\SubstituteBindings::class,
        prepend: \App\Http\Middleware\SetDefaultLocaleForUrls::class,
    );
})

```
{% endraw %}
