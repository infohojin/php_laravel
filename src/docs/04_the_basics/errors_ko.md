---
layout: docs
title: "오류 처리"
---

{% raw %}
# 오류 처리

- [소개](#introduction)
- [컨피그레이션](#configuration)
- [예외 처리](#handling-exceptions)
- [예외 보고](#reporting-exceptions)
- [예외 로그 수준](#exception-log-levels)
- [유형별 예외 무시](#ignoring-exceptions-by-type)
- [렌더링 예외](#rendering-exceptions)
- 보고 가능 및 렌더링 가능 예외 (#renderable-exceptions)
- [보고된 예외 제한](#throttling-reported-exceptions)
- [HTTP 예외](#http-exceptions)
- [사용자 지정 HTTP 오류 페이지](#custom-http-error-pages)

<a name="introduction"></a>
## 소개

새 Laravel 프로젝트를 시작할 때 오류 및 예외 처리는 이미 구성되어 있습니다. 그러나 언제든지 애플리케이션의 `bootstrap/app.php` 에서 `withExceptions` 메서드를 사용하여 애플리케이션에서 예외를 보고하고 렌더링하는 방법을 관리할 수 있습니다。

`withExceptions` 종료에 제공되는 `$exceptions` 객체는 `Illuminate\Foundation\Configuration\Exceptions` 의 인스턴스이며 애플리케이션에서 예외 처리를 관리하는 역할을 합니다. 이 문서에서는 이 객체에 대해 자세히 살펴봅니다。

<a name="configuration"></a>
## 구성

`config/app.php` 구성 파일의 `debug` 옵션은 실제로 사용자에게 표시되는 오류에 대한 정보의 양을 결정합니다. 기본적으로 이 옵션은 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 존중하도록 설정됩니다。

로컬 개발 중에 `APP_DEBUG` 환경 변수를 `true` 로 설정해야 합니다。

> [!WARNING]
> 프로덕션 환경에서 `APP_DEBUG` 의 값은 항상 `false` 여야 합니다. 프로덕션에서 값을 `true` 로 설정하면 애플리케이션의 최종 사용자에게 민감한 구성 값이 노출될 위험이 있습니다。

<a name="handling-exceptions"></a>
## 예외 처리

<a name="reporting-exceptions"></a>
### 예외 보고

Laravel 에서 예외 보고는 [Laravel Nightwatch](https://nightwatch.laravel.com), [Sentry](https://github.com/getsentry/sentry-laravel) 또는 [Flare](https://flareapp.io) 와 같은 외부 서비스에 예외를 기록하거나 전송하는 데 사용됩니다. 기본적으로 예외는 [logging](/docs/{{version}}/logging) 구성에 따라 기록됩니다. 그러나 원하는 대로 예외를 기록할 수 있습니다。



만약 서로 다른 유형의 예외를 서로 다른 방식으로 보고해야 한다면, 애플리케이션의 `bootstrap/app.php`에서 `report` 예외 메서드를 사용하여 특정 유형의 예외가 보고되어야 할 때 실행되어야 하는 클로저를 등록할 수 있습니다. Laravel은 클로저의 타입 힌트를 검사하여 클로저가 보고하는 예외의 유형을 결정합니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    });
})
```



`report` 메서드를 사용하여 사용자 정의 예외 보고 콜백을 등록하면, Laravel은 여전히 애플리케이션의 기본 로그 구성으로 예외를 기록합니다. 예외가 기본 로그 스택으로 전달되는 것을 중지하려면, 보고 콜백을 정의할 때 `stop` 메서드를 사용하거나 콜백에서 `false`를 반환할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->report(function (InvalidOrderException $e) {
        // ...
    })->stop();

    $exceptions->report(function (InvalidOrderException $e) {
        return false;
    });
})
```



> [!NOTE]
> 특정 예외에 대한 예외 보고를 사용자 정의하려면 [보고 가능한 예외](/docs/{{version}}/errors#renderable-exceptions)를 활용할 수도 있습니다.

<a name="global-log-context"></a>
#### 전역 로그 컨텍스트

사용 가능한 경우, Laravel은 자동으로 현재 사용자의 ID를 모든 예외 로그 메시지에 컨텍스트 데이터로 추가합니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `context` 예외 메서드를 사용하여 자신만의 전역 컨텍스트 데이터를 정의할 수 있습니다. 이 정보는 애플리케이션에서 작성하는 모든 예외 로그 메시지에 포함됩니다:

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->context(fn () => [
        'foo' => 'bar',
    ]);
})
```



<a name="exception-log-context"></a>
#### 예외 로그 컨텍스트

모든 로그 메시지에 컨텍스트를 추가하는 것이 유용할 수 있지만, 때로는 특정 예외에 고유한 컨텍스트를 로그에 포함하고 싶을 때가 있습니다. 애플리케이션의 예외 중 하나에 `context` 메서드를 정의하면, 해당 예외의 로그 항목에 추가되어야 하는 예외와 관련된 데이터를 지정할 수 있습니다:

```php
<?php

namespace App\Exceptions;

use Exception;

class InvalidOrderException extends Exception
{
    // ...

    /**
     * Get the exception's context information.
     *
     * @return array<string, mixed>
     */
    public function context(): array
    {
        return ['order_id' => $this->orderId];
    }
}
```



<a name="the-report-helper"></a>
#### `report` 도우미

때때로 예외를 보고해야 하지만 현재 요청 처리를 계속해야 할 때가 있습니다. `report` 도우미 함수는 사용자에게 오류 페이지를 렌더링하지 않고 예외를 신속하게 보고할 수 있게 해줍니다:

```php
public function isValid(string $value): bool
{
    try {
        // Validate the value...
    } catch (Throwable $e) {
        report($e);

        return false;
    }
}
```



<a name="deduplicating-reported-exceptions"></a>
#### 보고된 예외 중복 제거

애플리케이션 전반에서 `report` 함수를 사용하고 있다면, 동일한 예외가 여러 번 보고되어 로그에 중복 항목이 생성될 수 있습니다.

예외의 단일 인스턴스가 한 번만 보고되도록 하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `dontReportDuplicates` 예외 메서드를 호출할 수 있습니다.

```php
->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportDuplicates();
})
```



이제 `report` 헬퍼가 동일한 예외 인스턴스로 호출되면, 첫 번째 호출만 보고됩니다:

```php
$original = new RuntimeException('Whoops!');

report($original); // reported

try {
    throw $original;
} catch (Throwable $caught) {
    report($caught); // ignored
}

report($original); // ignored
report($caught); // ignored
```



<a name="exception-log-levels"></a>
### 예외 로그 레벨

메시지가 애플리케이션의 [로그](/docs/{{version}}/logging)에 기록될 때, 메시지는 지정된 [로그 레벨](/docs/{{version}}/logging#log-levels)로 기록되며, 이는 기록되는 메시지의 심각도나 중요성을 나타냅니다.

위에서 언급한 바와 같이, `report` 메서드를 사용하여 사용자 정의 예외 보고 콜백을 등록하더라도, Laravel은 여전히 애플리케이션의 기본 로깅 구성을 사용하여 예외를 기록합니다. 그러나 로그 레벨이 메시지가 기록되는 채널에 영향을 줄 수 있기 때문에, 특정 예외가 기록되는 로그 레벨을 구성하고 싶을 수 있습니다.

이를 수행하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `level` 예외 메서드를 사용할 수 있습니다. 이 메서드는 예외 유형을 첫 번째 인수로, 로그 레벨을 두 번째 인수로 받습니다:

```php
use PDOException;
use Psr\Log\LogLevel;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->level(PDOException::class, LogLevel::CRITICAL);
})
```



<a name="ignoring-exceptions-by-type"></a>
### 유형별 예외 무시

애플리케이션을 구축할 때, 보고하고 싶지 않은 예외 유형이 있을 수 있습니다. 이러한 예외를 무시하려면 애플리케이션의 `bootstrap/app.php` 파일에서 `dontReport` 예외 메서드를 사용할 수 있습니다. 이 메서드에 제공된 클래스는 절대로 보고되지 않지만, 여전히 사용자 정의 렌더링 로직을 가질 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReport([
        InvalidOrderException::class,
    ]);
})
```



또는 단순히 `Illuminate\Contracts\Debug\ShouldntReport` 인터페이스로 예외 클래스를 "표시"할 수 있습니다. 이 인터페이스로 예외가 표시되면, Laravel의 예외 처리기에 의해 보고되지 않습니다:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Contracts\Debug\ShouldntReport;

class PodcastProcessingException extends Exception implements ShouldntReport
{
    //
}
```



특정 유형의 예외가 무시되는 시점을 더 세밀하게 제어해야 하는 경우, `dontReportWhen` 메서드에 클로저를 제공할 수 있습니다:

```php
use App\Exceptions\InvalidOrderException;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontReportWhen(function (Throwable $e) {
        return $e instanceof PodcastProcessingException &&
               $e->reason() === 'Subscription expired';
    });
})
```



내부적으로 Laravel은 이미 일부 유형의 오류를 무시합니다. 예를 들어 404 HTTP 오류로 인한 예외, 출처 불일치로 인해 생성된 403 HTTP 응답, 또는 잘못된 CSRF 토큰으로 인해 생성된 419 HTTP 응답 등이 있습니다. 특정 유형의 예외를 Laravel이 더 이상 무시하지 않도록 지시하고 싶다면, 애플리케이션의 `bootstrap/app.php` 파일에서 `stopIgnoring` 예외 메서드를 사용할 수 있습니다:

```php
use Symfony\Component\HttpKernel\Exception\HttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->stopIgnoring(HttpException::class);
})
```



<a name="rendering-exceptions"></a>
### 렌더링 예외

기본적으로 Laravel 예외 처리기는 예외를 HTTP 응답으로 변환합니다. 그러나 특정 유형의 예외에 대해 사용자 정의 렌더링 클로저를 등록할 수 있습니다. 이는 애플리케이션의 `bootstrap/app.php` 파일에서 `render` 예외 메서드를 사용하여 수행할 수 있습니다.

`render` 메서드에 전달된 클로저는 `response` 헬퍼를 통해 생성할 수 있는 `Illuminate\Http\Response` 인스턴스를 반환해야 합니다. Laravel은 클로저의 타입 힌트를 검사하여 클로저가 렌더링하는 예외 유형을 결정합니다:

```php
use App\Exceptions\InvalidOrderException;
use Illuminate\Http\Request;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (InvalidOrderException $e, Request $request) {
        return response()->view('errors.invalid-order', status: 500);
    });
})
```



내장 Laravel 또는 Symfony 예외(예: `NotFoundHttpException`)의 렌더링 동작을 재정의하기 위해 `render` 방법을 사용할 수도 있습니다. `render` 메서드에 제공된 클로저가 값을 반환하지 않으면 Laravel의 기본 예외 렌더링이 사용됩니다:

```php
use Illuminate\Http\Request;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->render(function (NotFoundHttpException $e, Request $request) {
        if ($request->is('api/*')) {
            return response()->json([
                'message' => 'Record not found.'
            ], 404);
        }
    });
})
```



<a name="rendering-exceptions-as-json"></a>
#### 예외를 JSON으로 렌더링하기

예외를 렌더링할 때, Laravel은 요청의 `Accept` 헤더를 기반으로 예외를 HTML 또는 JSON 응답으로 렌더링할지 자동으로 결정합니다. Laravel이 HTML 또는 JSON 예외 응답을 렌더링할지를 결정하는 방식을 사용자 정의하고 싶다면, `shouldRenderJsonWhen` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Http\Request;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->shouldRenderJsonWhen(function (Request $request, Throwable $e) {
        if ($request->is('admin/*')) {
            return true;
        }

        return $request->expectsJson();
    });
})
```



<a name="customizing-the-exception-response"></a>
#### 예외 응답 사용자 정의

가끔 Laravel의 예외 처리기가 렌더링하는 전체 HTTP 응답을 사용자 정의해야 할 때가 있습니다. 이를 달성하기 위해, `respond` 메서드를 사용하여 응답 사용자 정의 클로저를 등록할 수 있습니다:

```php
use Symfony\Component\HttpFoundation\Response;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->respond(function (Response $response) {
        if ($response->getStatusCode() === 419) {
            return back()->with([
                'message' => 'The page expired, please try again.',
            ]);
        }

        return $response;
    });
})
```



<a name="renderable-exceptions"></a>
### 보고 가능하고 렌더링 가능한 예외

애플리케이션의 `bootstrap/app.php` 파일에서 사용자 정의 보고 및 렌더링 동작을 정의하는 대신, 애플리케이션 예외에서 `report` 및 `render` 메서드를 직접 정의할 수 있습니다. 이러한 메서드가 존재하면 프레임워크에서 자동으로 호출됩니다:

```php
<?php

namespace App\Exceptions;

use Exception;
use Illuminate\Http\Request;
use Illuminate\Http\Response;

class InvalidOrderException extends Exception
{
    /**
     * Report the exception.
     */
    public function report(): void
    {
        // ...
    }

    /**
     * Render the exception as an HTTP response.
     */
    public function render(Request $request): Response
    {
        return response(/* ... */);
    }
}
```



만약 당신의 예외가 이미 렌더링 가능한 예외(예: 내장 Laravel 또는 Symfony 예외)를 상속한다면, 예외의 `render` 메서드에서 `false`를 반환하여 예외의 기본 HTTP 응답을 렌더링할 수 있습니다:

```php
/**
 * Render the exception as an HTTP response.
 */
public function render(Request $request): Response|bool
{
    if (/** Determine if the exception needs custom rendering */) {

        return response(/* ... */);
    }

    return false;
}
```



예외에 특정 조건이 충족될 때만 필요한 사용자 정의 보고 로직이 포함되어 있는 경우, 때때로 Laravel에게 기본 예외 처리 구성을 사용하여 예외를 보고하도록 지시해야 할 수 있습니다. 이를 수행하려면 예외의 `report` 메서드에서 `false`를 반환할 수 있습니다:

```php
/**
 * Report the exception.
 */
public function report(): bool
{
    if (/** Determine if the exception needs custom reporting */) {

        // ...

        return true;
    }

    return false;
}
```



> [!NOTE]
> `report` 메서드의 필요한 종속성을 타입 힌트로 지정할 수 있으며, 그러면 라라벨의 [서비스 컨테이너](/docs/{{version}}/container)에 의해 메서드에 자동으로 주입됩니다.

<a name="throttling-reported-exceptions"></a>
### 보고된 예외 제한

애플리케이션에서 매우 많은 수의 예외가 보고되는 경우, 실제로 로깅되거나 외부 오류 추적 서비스로 전송되는 예외 수를 제한하고 싶을 수 있습니다.

예외의 무작위 샘플 비율을 적용하려면, 애플리케이션의 `bootstrap/app.php` 파일에서 `throttle` 예외 메서드를 사용할 수 있습니다. `throttle` 메서드는 `Lottery` 인스턴스를 반환해야 하는 클로저를 받습니다:

```php
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return Lottery::odds(1, 1000);
    });
})
```



예외 유형에 따라 조건부로 샘플링하는 것도 가능합니다. 특정 예외 클래스의 인스턴스만 샘플링하고 싶다면, 해당 클래스에 대해서만 `Lottery` 인스턴스를 반환할 수 있습니다:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof ApiMonitoringException) {
            return Lottery::odds(1, 1000);
        }
    });
})
```



또한 `Lottery` 대신 `Limit` 인스턴스를 반환하여 기록되거나 외부 오류 추적 서비스로 전송된 예외의 속도를 제한할 수 있습니다. 이는 예를 들어 애플리케이션에서 사용하는 타사 서비스가 다운되었을 때와 같이 예외가 갑자기 몰려 로그를 뒤덮는 것을 방지하려는 경우에 유용합니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300);
        }
    });
})
```



기본적으로, 제한은 예외의 클래스를 속도 제한 키로 사용합니다. `Limit`에서 `by` 메서드를 사용하여 자체 키를 지정하여 이를 사용자 정의할 수 있습니다:

```php
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        if ($e instanceof BroadcastException) {
            return Limit::perMinute(300)->by($e->getMessage());
        }
    });
})
```



물론, 서로 다른 예외에 대해 `Lottery`와 `Limit` 인스턴스의 혼합을 반환할 수 있습니다:

```php
use App\Exceptions\ApiMonitoringException;
use Illuminate\Broadcasting\BroadcastException;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Lottery;
use Throwable;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->throttle(function (Throwable $e) {
        return match (true) {
            $e instanceof BroadcastException => Limit::perMinute(300),
            $e instanceof ApiMonitoringException => Lottery::odds(1, 1000),
            default => Limit::none(),
        };
    });
})
```



<a name="http-exceptions"></a>
## HTTP 예외

일부 예외는 서버의 HTTP 오류 코드를 설명합니다. 예를 들어, 이는 "페이지를 찾을 수 없음" 오류(404), "권한 없음" 오류(401), 또는 개발자가 생성한 500 오류일 수 있습니다. 애플리케이션 어디에서나 이러한 응답을 생성하려면 `abort` 헬퍼를 사용할 수 있습니다:

```php
abort(404);
```



<a name="custom-http-error-pages"></a>
### 맞춤형 HTTP 오류 페이지

Laravel은 다양한 HTTP 상태 코드에 대해 맞춤형 오류 페이지를 쉽게 표시할 수 있게 해줍니다. 예를 들어, 404 HTTP 상태 코드에 대한 오류 페이지를 맞춤화하려면 `resources/views/errors/404.blade.php` 뷰 템플릿을 생성하면 됩니다. 이 뷰는 애플리케이션에서 발생하는 모든 404 오류에 대해 렌더링됩니다. 이 디렉토리 내의 뷰는 대응하는 HTTP 상태 코드와 일치하도록 이름을 지어야 합니다. `abort` 함수에 의해 발생된 `Symfony\Component\HttpKernel\Exception\HttpException` 인스턴스는 `$exception` 변수로 뷰에 전달됩니다:

```blade
<h2>{{ $exception->getMessage() }}</h2>
```



`vendor:publish` Artisan 명령어를 사용하여 Laravel의 기본 오류 페이지 템플릿을 게시할 수 있습니다. 템플릿이 게시된 후에는 원하는 대로 사용자 정의할 수 있습니다:

```shell
php artisan vendor:publish --tag=laravel-errors
```

<a name="fallback-http-error-pages"></a>
#### 대체(폴백) HTTP 오류 페이지

특정 HTTP 상태 코드 시리즈에 대해 "대체(폴백)" 오류 페이지를 정의할 수도 있습니다. 특정 HTTP 상태 코드에 해당하는 페이지가 없을 경우 이 페이지가 렌더링됩니다. 이를 달성하려면 애플리케이션의 `resources/views/errors` 디렉터리에 `4xx.blade.php` 템플릿과 `5xx.blade.php` 템플릿을 정의하십시오.

대체 오류 페이지를 정의할 때, Laravel이 이러한 상태 코드에 대해 내부적으로 전용 페이지를 가지고 있기 때문에, 대체 페이지는 `404`, `500`, `503` 오류 응답에는 영향을 미치지 않습니다. 이러한 상태 코드에 대해 렌더링되는 페이지를 사용자 정의하려면, 각 코드별로 개별적으로 사용자 정의 오류 페이지를 정의해야 합니다.
{% endraw %}
