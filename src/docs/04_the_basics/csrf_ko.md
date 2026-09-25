---
layout: docs
title: "CSRF 보호"
---

{% raw %}
# CSRF 보호

- [소개](#csrf-introduction)
- [CSRF 요청 방지](#preventing-csrf-requests)
- [오리진 확인](#origin-verification)
- [Excluding URIs](#csrf-excluding-uris)
- [X-CSRF-Token](#csrf-x-csrf-token)
- [X-XSRF-Token](#csrf-x-xsrf-token)

<a name="csrf-introduction"></a>
## 소개

크로스 사이트 요청 위조는 인증된 사용자를 대신하여 무단 명령을 실행하는 악성 공격의 한 유형입니다. 다행히도 Laravel 을 사용하면 크로스 사이트 요청 포저리 (https://en.wikipedia.org/wiki/Cross-site_request_forgery)(CSRF) 공격으로부터 애플리케이션을 쉽게 보호할 수 있습니다。

<a name="csrf-explanation"></a>
#### 취약성에 대한 설명

크로스 사이트 요청 위조에 익숙하지 않은 경우， 이 취약점을 악용할 수 있는 방법의 예를 논의해 보겠습니다. 애플리케이션에 인증된 사용자의 이메일 주소를 변경하기 위한 `POST` 요청을 수락하는 `/user/email` 경로가 있다고 가정해 보겠습니다. 가장 가능성이 높은 경우， 이 경로는 사용자가 사용을 시작하려는 이메일 주소를 포함하는 `email` 입력 필드를 기대합니다。

CSRF 보호가 없으면 악성 웹사이트가 애플리케이션의 `/user/email` 경로를 가리키는 HTML 양식을 생성하고 악성 사용자의 자체 이메일 주소를 제출할 수 있습니다：

```blade
<form action="https://your-application.com/user/email" method="POST">
    <input type="email" value="malicious-email@example.com">
</form>

<script>
    document.forms[0].submit();
</script>

```

악성 웹사이트가 페이지가 로드될 때 자동으로 양식을 제출하면， 악성 사용자는 의심하지 않는 애플리케이션 사용자를 유인하여 웹사이트를 방문하게 하기만 하면 됩니다. 그러면 해당 사용자의 이메일 주소가 애플리케이션에서 변경됩니다。

이러한 취약성을 방지하려면 악성 애플리케이션이 액세스할 수 없는 비밀 세션 값에 대한 모든 수신 `POST`, `PUT`, `PATCH` 또는 `DELETE` 요청을 검사해야 합니다。

<a name="preventing-csrf-requests"></a>
## CSRF 요청 방지

`web` 미들웨어 그룹에 기본적으로 포함된 `Illuminate\Foundation\Http\Middleware\PreventRequestForgery`(/docs/{{version}}/middleware) 는 2 계층 접근 방식을 사용하여 교차 사이트 요청 위조로부터 애플리케이션을 보호합니다。

먼저， 미들웨어는 브라우저의 `Sec-Fetch-Site` 헤더를 확인합니다. 최신 브라우저는 각 요청에 대해 이 헤더를 자동으로 설정하여 요청이 동일한 출처， 동일한 사이트 또는 교차 사이트 출처에서 발생했는지 표시합니다. 헤더가 요청이 동일한 출처에서 발생했음을 나타내는 경우， 토큰 확인 없이 요청이 즉시 허용됩니다。

출처 확인이 통과되지 않는 경우 - 예를 들어， 요청이 `Sec-Fetch-Site` 헤더를 보내지 않는 이전 브라우저에서 오거나 연결이 안전하지 않기 때문에 - 미들웨어는 기존 CSRF 토큰 검증으로 되돌아갑니다。

Laravel 은 애플리케이션에서 관리하는 각 활성 [사용자 세션](/docs/{{version}}/session) 에 대해 CSRF “토큰” 을 자동으로 생성합니다. 이 토큰은 인증된 사용자가 실제로 애플리케이션에 요청을 하는 사람인지 확인하는 데 사용됩니다. 이 토큰은 사용자 세션에 저장되고 세션이 재생성될 때마다 변경되므로 악성 애플리케이션은 이에 액세스할 수 없습니다。

현재 세션의 CSRF 토큰은 요청의 세션 또는 `csrf_token` 헬퍼 함수를 통해 액세스할 수 있습니다：

```php
use Illuminate\Http\Request;

Route::get('/token', function (Request $request) {
    $token = $request->session()->token();

    $token = csrf_token();

    // ...
});

```

애플리케이션에서 "POST", "PUT", "PATCH" 또는 "DELETE" HTML 폼을 정의할 때마다, CSRF 보호 미들웨어가 요청을 검증할 수 있도록 폼에 숨겨진 CSRF `_token` 필드를 포함해야 합니다. 편의를 위해 `@csrf` Blade 지시문을 사용하여 숨겨진 토큰 입력 필드를 생성할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    <!-- Equivalent to... -->
    <input type="hidden" name="_token" value="{{ csrf_token() }}" />
</form>

```

<a name="csrf-tokens-and-spas"></a>
#### CSRF 토큰 & SPA

만약 Laravel을 API 백엔드로 사용하는 SPA를 구축하고 있다면, API 인증 및 CSRF 취약점 보호에 대한 정보는 [Laravel Sanctum 문서](/docs/{{version}}/sanctum)를 참조해야 합니다.

<a name="origin-verification"></a>
### 오리진 검증

앞서 논의한 것처럼, Laravel의 요청 위조 미들웨어는 먼저 요청이 동일한 오리진인지 확인하기 위해 `Sec-Fetch-Site` 헤더를 검사합니다. 기본적으로 이 검증을 통과하지 못하면, 미들웨어는 CSRF 토큰 검증으로 대체됩니다.

하지만 오리진 검증만 사용하고 CSRF 토큰 검증을 완전히 비활성화하고 싶은 경우, 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드를 사용하면 됩니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(originOnly: true);
})

```

원본 전용 모드를 사용할 때, 원본 검증에 실패한 요청은 일반적으로 CSRF 토큰 불일치와 관련된 `419` 응답 대신 `403` HTTP 응답을 받게 됩니다.

> [!WARNING]
> `Sec-Fetch-Site` 헤더는 브라우저가 보안(HTTPS) 연결을 통해서만 전송합니다. 애플리케이션이 HTTPS를 통해 제공되지 않는 경우, 원본 검증을 사용할 수 없으며 미들웨어는 CSRF 토큰 검증으로 대체됩니다.

애플리케이션이 하위 도메인에서의 요청을 허용해야 하는 경우(예: `dashboard.example.com`가 `example.com`의 요청을 허용), 동일 출처 요청에 추가하여 동일 사이트 요청을 허용할 수 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(allowSameSite: true);
})

```

<a name="csrf-excluding-uris"></a>
### CSRF 보호에서 URI 제외하기

때때로 특정 URI를 CSRF 보호에서 제외하고자 할 때가 있습니다. 예를 들어, [Stripe](https://stripe.com)를 사용하여 결제를 처리하고 웹훅 시스템을 이용하는 경우, Stripe가 어떤 CSRF 토큰을 보낼지 모르기 때문에 Stripe 웹훅 핸들러 경로를 CSRF 보호에서 제외해야 합니다.

일반적으로 이러한 종류의 경로는 Laravel이 `routes/web.php` 파일의 모든 경로에 적용하는 `web` 미들웨어 그룹 외부에 두는 것이 좋습니다. 그러나 특정 경로를 제외하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `preventRequestForgery` 메서드에 해당 경로의 URI를 제공할 수도 있습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->preventRequestForgery(except: [
        'stripe/*',
        'http://example.com/foo/bar',
        'http://example.com/foo/*',
    ]);
})

```

> [!NOTE]
> 편의를 위해 [테스트 실행](/docs/{{version}}/testing) 시 모든 경로에 대해 CSRF 미들웨어가 자동으로 비활성화됩니다.

<a name="csrf-x-csrf-token"></a>
## X-CSRF-TOKEN

CSRF 토큰을 POST 매개변수로 확인하는 것 외에도, `PreventRequestForgery` 미들웨어는 `X-CSRF-TOKEN` 요청 헤더도 확인합니다. 예를 들어, 토큰을 HTML `meta` 태그에 저장할 수 있습니다:

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">

```

그런 다음, jQuery와 같은 라이브러리에 모든 요청 헤더에 토큰을 자동으로 추가하도록 지시할 수 있습니다. 이는 레거시 자바스크립트 기술을 사용하는 AJAX 기반 애플리케이션에 간단하고 편리한 CSRF 보호를 제공합니다:

```js
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});

```

<a name="csrf-x-xsrf-token"></a>
## X-XSRF-TOKEN

Laravel는 현재 CSRF 토큰을 암호화된 `XSRF-TOKEN` 쿠키에 저장하며, 이 쿠키는 프레임워크가 생성한 각 응답과 함께 포함됩니다. 쿠키 값을 사용하여 `X-XSRF-TOKEN` 요청 헤더를 설정할 수 있습니다.

이 쿠키는 주로 개발자 편의를 위해 전송되며, Angular 및 Axios와 같은 일부 JavaScript 프레임워크와 라이브러리는 동일 출처 요청에서 자동으로 쿠키 값을 `X-XSRF-TOKEN` 헤더에 설정합니다.
{% endraw %}
