---
layout: docs
title: "로깅"
---

{% raw %}
# 로깅

- [소개](#introduction)
- [컨피그레이션](#configuration)
- [사용 가능한 채널 드라이버](#available-channel-drivers)
- 채널 전제 조건 (#channel-prerequisites)
- Logging Deprecation Warnings (#logging-deprecation-warnings)
- 빌딩 로그 스택 (#building-log-stacks)
- [로그 메시지 쓰기](#writing-log-messages)
- 컨텍스트 정보 (#contextual-information)
- [특정 채널로 쓰기](#writing-to-specific-channels)
- 모놀로그 채널 커스터마이징 (#monolog-channel-customization)
- 커스터마이징 모놀로그 포 채널 (#customizing-monolog-for-channels)
- 모놀로그 핸들러 채널 만들기 (#creating-monolog-handler-channels)
- 공장을 통한 맞춤형 채널 생성 (#creating-custom-channels-via-factories)
- 페일을 사용한 테일링 로그 메시지 (#tailing-log-messages-using-pail)
- [설치](#pail-installation)
- 사용 (#pail-usage)
- [필터링 로그](#pail-filtering-logs)

<a name="introduction"></a>
## 소개

애플리케이션 내에서 발생하는 일에 대해 더 많이 알아보는 데 도움이 되도록 Laravel 은 파일， 시스템 오류 로그， 심지어 Slack 에 메시지를 기록하여 전체 팀에 알릴 수 있는 강력한 로깅 서비스를 제공합니다。

Laravel 로깅은 “채널” 을 기반으로 합니다. 각 채널은 로그 정보를 쓰는 특정 방식을 나타냅니다. 예를 들어， `single` 채널은 로그 파일을 단일 로그 파일에 쓰는 반면， `slack` 채널은 로그 메시지를 Slack 으로 보냅니다. 로그 메시지는 심각도에 따라 여러 채널에 쓰일 수 있습니다。

Laravel 은 다양한 강력한 로그 핸들러를 지원하는 [Monolog](https://github.com/Seldaek/monolog) 라이브러리를 활용합니다. Laravel 은 이러한 핸들러를 쉽게 구성할 수 있도록 하여， 애플리케이션의 로그 처리를 사용자 지정하기 위해 이를 혼합하고 일치시킬 수 있습니다。

<a name="configuration"></a>
## 구성

애플리케이션의 로깅 동작을 제어하는 모든 구성 옵션은 `config/logging.php` 구성 파일에 저장되어 있습니다. 이 파일을 사용하면 애플리케이션의 로그 채널을 구성할 수 있으므로， 사용 가능한 각 채널과 해당 옵션을 반드시 검토하십시오. 아래에서 몇 가지 일반적인 옵션을 검토합니다。

기본적으로 Laravel 은 메시지를 로깅할 때 `stack` 채널을 사용합니다. `stack` 채널은 여러 로그 채널을 단일 채널로 집계하는 데 사용됩니다. 스택 구축에 대한 자세한 내용은 [아래 문서](#building-log-stacks) 를 참조하십시오。



<a name="available-channel-drivers"></a>
### 사용 가능한 채널 드라이버

각 로그 채널은 “드라이버” 로 구동됩니다. 드라이버는 로그 메시지가 실제로 기록되는 방식과 위치를 결정합니다. 다음 로그 채널 드라이버는 모든 Laravel 애플리케이션에서 사용할 수 있습니다. 이러한 드라이버 대부분에 대한 항목은 애플리케이션의 `config/logging.php` 구성 파일에 이미 존재하므로， 이 파일을 검토하여 내용에 익숙해지십시오：

<div class="overflow-auto">

| 이름 | 설명 설명 설명 설명 | 설명 | 설명 | 설명
| —————————————————————————— ——————————————————————
| `custom` | 채널을 생성하기 위해 지정된 공장을 호출하는 드라이버입니다. |
| `daily` | 매일 회전하는 `RotatingFileHandler` 기반 모놀로그 드라이버. |
| `monthly` | 매월 회전하는 `RotatingFileHandler` 기반 Monolog 드라이버. |
| `errorlog` | `ErrorLogHandler` 기반 Monolog 드라이버.             |
| `monolog` | 지원되는 모놀로그 핸들러를 사용할 수 있는 모놀로그 공장 드라이버. |
| `papertrail` | `SyslogUdpHandler` 기반 모놀로그 드라이버.             |
| `single` | 단일 파일 또는 경로 기반 로거 채널 (`StreamHandler`). .  .
| `slack` | `SlackWebhookHandler` 기반 모놀로그 드라이버.             |
| `stack` | “멀티채널” 채널 생성을 용이하게 하는 래퍼입니다. .  .  .
| `syslog` | `SyslogHandler` 기반 모놀로그 드라이버. . . . . . . . . . . . .

</div>

> [!NOTE]
> `monolog` 및 `custom` 드라이버에 대해 자세히 알아보려면 [고급 채널 사용자 지정](#monolog-channel-customization) 설명서를 확인하세요。

<a name="configuring-the-channel-name"></a>
#### 채널 이름 구성

기본적으로 Monolog 는 `production` 또는 `local` 와 같이 현재 환경과 일치하는 “채널 이름” 으로 인스턴스화됩니다. 이 값을 변경하려면 채널 구성에 `name` 옵션을 추가할 수 있습니다：

```php
'stack' => [
    'driver' => 'stack',
    'name' => 'channel-name',
    'channels' => ['single', 'slack'],
],
```

<a name="channel-prerequisites"></a>
### 채널 사전 요구사항

<a name="configuring-the-single-daily-and-monthly-channels"></a>
#### 단일， 일일 및 월간 채널 구성

`single`, `daily` 및 `monthly` 채널에는 `bubble`, `permission` 및 `locking` 라는 세 가지 선택적 구성 옵션이 있습니다。

<div class="overflow-auto">

| 이름 | 설명 | 설명 | 기본 |
| ————————————————————————————————————————————————— ——————————————————————|——————————————————————
| `bubble` | 처리 후 메시지가 다른 채널로 버블해야 하는지 여부를 나타냅니다. | `true` |
| `locking` | 로그 파일에 쓰기 전에 로그 파일을 잠그려고 시도합니다.           | `false` |
| `permission` | 로그 파일의 권한. . . . . . . . . . . . .  . . . . . . . . . . . | `0644` |

</div>

또한 `daily` 및 `monthly` 채널의 보존 정책은 `max_files` 구성 옵션을 통해 구성할 수 있습니다. `LOG_DAILY_DAYS` 환경 변수를 사용하여 `daily` 채널의 보존을 구성할 수도 있습니다。

<a name="configuring-the-papertrail-channel"></a>
#### Papertrail 채널 구성

`papertrail` 채널에는 `host` 및 `port` 구성 옵션이 필요합니다. 이러한 옵션은 `PAPERTRAIL_URL` 및 `PAPERTRAIL_PORT` 환경 변수를 통해 정의할 수 있습니다. 이러한 값은 [Papertrail](https://help.papertrailapp.com/kb/configuration/configuring-centralized-logging-from-php-apps/#send-events-from-php-app) 에서 얻을 수 있습니다。

<a name="configuring-the-slack-channel"></a>
#### Slack 채널 구성

`slack` 채널에는 `url` 구성 옵션이 필요합니다. 이 값은 `LOG_SLACK_WEBHOOK_URL` 환경 변수를 통해 정의할 수 있습니다. 이 URL 은 Slack 팀에 대해 구성한 [수신 웹훅](https://slack.com/apps/A0F7XDUAZ-incoming-webhooks) 의 URL 과 일치해야 합니다。

기본적으로 Slack 은 `critical` 수준 이상의 로그만 수신합니다. 그러나 `LOG_LEVEL` 환경 변수를 사용하거나 Slack 로그 채널의 구성 배열 내에서 `level` 구성 옵션을 수정하여 이를 조정할 수 있습니다。

<a name="logging-deprecation-warnings"></a>
### 저하 경고 로깅



PHP, Laravel 및 기타 라이브러리는 종종 일부 기능이 더 이상 사용되지 않으며 향후 버전에서 제거될 것임을 사용자에게 알립니다. 이러한 사용 중단 경고를 기록하려면 `LOG_DEPRECATIONS_CHANNEL` 환경 변수를 사용하여 선호하는 `deprecations` 로그 채널을 지정하거나 애플리케이션의 `config/logging.php` 구성 파일 내에서 지정할 수 있습니다:

```php
'deprecations' => [
    'channel' => env('LOG_DEPRECATIONS_CHANNEL', 'null'),
    'trace' => env('LOG_DEPRECATIONS_TRACE', false),
],

'channels' => [
    // ...
]
```



또는 `deprecations`라는 로그 채널을 정의할 수 있습니다. 이 이름을 가진 로그 채널이 존재하면, 항상 이를 사용하여 더 이상 사용되지 않는 항목을 기록합니다:

```php
'channels' => [
    'deprecations' => [
        'driver' => 'single',
        'path' => storage_path('logs/php-deprecation-warnings.log'),
    ],
],
```



<a name="building-log-stacks"></a>
## 로그 스택 빌딩

앞서 언급했듯이, `stack` 드라이버는 편의를 위해 여러 채널을 단일 로그 채널로 결합할 수 있습니다. 로그 스택을 사용하는 방법을 설명하기 위해, 실제 애플리케이션에서 볼 수 있는 구성 예제를 살펴보겠습니다:

```php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['syslog', 'slack'], // [tl! add]
        'ignore_exceptions' => false,
    ],

    'syslog' => [
        'driver' => 'syslog',
        'level' => env('LOG_LEVEL', 'debug'),
        'facility' => env('LOG_SYSLOG_FACILITY', LOG_USER),
        'replace_placeholders' => true,
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => env('LOG_SLACK_USERNAME', 'Laravel Log'),
        'emoji' => env('LOG_SLACK_EMOJI', ':boom:'),
        'level' => env('LOG_LEVEL', 'critical'),
        'replace_placeholders' => true,
    ],
],
```



이 구성 설정을 분석해 봅시다. 먼저, 우리의 `stack` 채널이 `channels` 옵션을 통해 두 개의 다른 채널, `syslog`와 `slack`를 집계한다는 점에 주목하세요. 따라서 메시지를 기록할 때, 이 두 채널 모두 메시지를 기록할 기회를 갖게 됩니다. 하지만 아래에서 볼 수 있듯이, 채널이 실제로 메시지를 기록할지는 메시지의 심각도 / '레벨'에 의해 결정될 수 있습니다.

<a name="log-levels"></a>
#### 로그 레벨

위 예제에서 `syslog`와 `slack` 채널 구성에 존재하는 `level` 구성 옵션에 유의하세요. 이 옵션은 채널이 메시지를 기록하기 위해 메시지가 가져야 하는 최소 '레벨'을 결정합니다. 라라벨(Laravel)의 로깅 서비스를 지원하는 Monolog은 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에 정의된 모든 로그 레벨을 제공합니다. 심각도 순으로, 이 로그 레벨은 **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug** 순입니다.

이제 `debug` 메서드를 사용하여 메시지를 기록한다고 상상해 보세요:

```php
Log::debug('An informational message.');
```



우리의 구성에 따라, `syslog` 채널은 메시지를 시스템 로그에 기록할 것입니다; 그러나 오류 메시지가 `critical` 이상이 아니므로 Slack으로 전송되지는 않습니다. 그러나 `emergency` 메시지를 기록하면, `emergency` 레벨이 두 채널의 최소 레벨 기준 이상이므로 시스템 로그와 Slack 모두로 전송됩니다:

```php
Log::emergency('The system is down!');
```



<a name="writing-log-messages"></a>
## 로그 메시지 작성

`Log` [파사드](/docs/{{version}}/facades)를 사용하여 로그에 정보를 기록할 수 있습니다. 앞서 언급했듯이, 로거는 [RFC 5424 명세](https://tools.ietf.org/html/rfc5424)에서 정의한 여덟 가지 로깅 레벨을 제공합니다: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**:

```php
use Illuminate\Support\Facades\Log;

Log::emergency($message);
Log::alert($message);
Log::critical($message);
Log::error($message);
Log::warning($message);
Log::notice($message);
Log::info($message);
Log::debug($message);
```



해당 수준에 대한 메시지를 기록하기 위해 이 메서드 중 어느 것이든 호출할 수 있습니다. 기본적으로 메시지는 `logging` 구성 파일에 의해 설정된 기본 로그 채널에 기록됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Log;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for the given user.
     */
    public function show(string $id): View
    {
        Log::info('Showing the user profile for user: {id}', ['id' => $id]);

        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```



<a name="contextual-information"></a>
### 상황 정보

로그 메서드에 컨텍스트 데이터를 배열로 전달할 수 있습니다. 이 컨텍스트 데이터는 로그 메시지와 함께 형식이 지정되어 표시됩니다:

```php
use Illuminate\Support\Facades\Log;

Log::info('User {id} failed to login.', ['id' => $user->id]);
```



가끔 특정 채널의 모든 이후 로그 항목에 포함되어야 하는 일부 컨텍스트 정보를 지정하고 싶을 때가 있습니다. 예를 들어, 애플리케이션에 들어오는 각 요청과 관련된 요청 ID를 로그에 기록하고 싶을 수 있습니다. 이를 수행하려면 `Log` 퍼사드의 `withContext` 메서드를 호출할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::withContext([
            'request-id' => $requestId
        ]);

        $response = $next($request);

        $response->headers->set('Request-Id', $requestId);

        return $response;
    }
}
```



모든 로깅 채널에 걸쳐 컨텍스트 정보를 공유하고 싶다면, `Log::shareContext()` 메서드를 호출할 수 있습니다. 이 메서드는 생성된 모든 채널과 이후에 생성되는 채널에 컨텍스트 정보를 제공할 것입니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AssignRequestId
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        $requestId = (string) Str::uuid();

        Log::shareContext([
            'request-id' => $requestId
        ]);

        // ...
    }
}
```



> [!NOTE]
> 큐에 작업을 처리하는 동안 로그 컨텍스트를 공유해야 하는 경우, [작업 미들웨어](/docs/{{version}}/queues#job-middleware)를 활용할 수 있습니다.

<a name="writing-to-specific-channels"></a>
### 특정 채널에 쓰기

가끔 애플리케이션의 기본 채널이 아닌 다른 채널에 메시지를 기록하고자 할 때가 있습니다. 구성 파일에 정의된 모든 채널에 접근하고 로그를 기록하기 위해 `Log` 파사드에서 `channel` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::channel('slack')->info('Something happened!');
```



여러 채널로 구성된 온디맨드 로깅 스택을 생성하고자 한다면, `stack` 방법을 사용할 수 있습니다:

```php
Log::stack(['single', 'slack'])->info('Something happened!');
```



<a name="on-demand-channels"></a>
#### 주문형 채널

애플리케이션의 `logging` 구성 파일에 해당 구성이 없더라도 실행 시 구성을 제공하여 주문형 채널을 만드는 것도 가능합니다. 이를 달성하기 위해 구성 배열을 `Log` 퍼사드의 `build` 메서드에 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
])->info('Something happened!');
```



온디맨드 로깅 스택에 온디맨드 채널을 포함하고자 할 수도 있습니다. 이는 온디맨드 채널 인스턴스를 `stack` 메서드에 전달되는 배열에 포함시켜서 달성할 수 있습니다:

```php
use Illuminate\Support\Facades\Log;

$channel = Log::build([
  'driver' => 'single',
  'path' => storage_path('logs/custom.log'),
]);

Log::stack(['slack', $channel])->info('Something happened!');
```



<a name="monolog-channel-customization"></a>
## 모놀로그 채널 사용자화

<a name="customizing-monolog-for-channels"></a>
### 채널용 모놀로그 사용자화

때때로 기존 채널에 대해 모놀로그가 구성되는 방식을 완전히 제어해야 할 수 있습니다. 예를 들어, Laravel의 내장 `single` 채널에 대해 사용자 정의 모놀로그 `FormatterInterface` 구현을 구성하고 싶을 수 있습니다.

시작하려면 채널 구성에서 `tap` 배열을 정의하십시오. `tap` 배열에는 생성된 후 모놀로그 인스턴스를 사용자화(또는 "탭"할) 기회를 가져야 하는 클래스 목록이 포함되어야 합니다. 이러한 클래스가 배치되어야 하는 특정 위치는 없으므로 애플리케이션 내에 이러한 클래스를 포함할 디렉토리를 자유롭게 생성할 수 있습니다:

```php
'single' => [
    'driver' => 'single',
    'tap' => [App\Logging\CustomizeFormatter::class],
    'path' => storage_path('logs/laravel.log'),
    'level' => env('LOG_LEVEL', 'debug'),
    'replace_placeholders' => true,
],
```



채널에서 `tap` 옵션을 구성하면 Monolog 인스턴스를 사용자 정의할 클래스를 정의할 준비가 된 것입니다. 이 클래스에는 단일 메서드만 필요합니다: `__invoke`, 이 메서드는 `Illuminate\Log\Logger` 인스턴스를 받습니다. `Illuminate\Log\Logger` 인스턴스는 모든 메서드 호출을 기본 Monolog 인스턴스로 프록시합니다:

```php
<?php

namespace App\Logging;

use Illuminate\Log\Logger;
use Monolog\Formatter\LineFormatter;

class CustomizeFormatter
{
    /**
     * Customize the given logger instance.
     */
    public function __invoke(Logger $logger): void
    {
        foreach ($logger->getHandlers() as $handler) {
            $handler->setFormatter(new LineFormatter(
                '[%datetime%] %channel%.%level_name%: %message% %context% %extra%'
            ));
        }
    }
}
```



> [!NOTE]
> 모든 "tap" 클래스는 [서비스 컨테이너](/docs/{{version}}/container)에 의해 해결되므로, 해당 클래스가 요구하는 모든 생성자 의존성은 자동으로 주입됩니다.

<a name="creating-monolog-handler-channels"></a>
### Monolog 핸들러 채널 생성하기

Monolog에는 다양한 [사용 가능한 핸들러](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Handler)가 있으며, Laravel은 각 핸들러에 대한 내장 채널을 제공하지 않습니다. 경우에 따라, 특정 Monolog 핸들러의 인스턴스로만 구성된 맞춤형 채널을 생성하고 싶을 수 있습니다. 이러한 핸들러는 해당하는 Laravel 로그 드라이버가 존재하지 않을 수 있습니다. 이러한 채널은 `monolog` 드라이버를 사용하여 쉽게 생성할 수 있습니다.

`monolog` 드라이버를 사용할 때, `handler` 구성 옵션은 어떤 핸들러가 인스턴스화될지를 지정하는 데 사용됩니다. 선택적으로, 핸들러가 필요로 하는 생성자 매개변수는 `handler_with` 구성 옵션을 사용하여 지정할 수 있습니다:

```php
'logentries' => [
    'driver'  => 'monolog',
    'handler' => Monolog\Handler\SyslogUdpHandler::class,
    'handler_with' => [
        'host' => 'my.logentries.internal.datahubhost.company.com',
        'port' => '10000',
    ],
],
```



<a name="monolog-formatters"></a>
#### 모놀로그 포매터

`monolog` 드라이버를 사용할 때, Monolog `LineFormatter`가 기본 포매터로 사용됩니다. 그러나 `formatter` 및 `formatter_with` 구성 옵션을 사용하여 핸들러에 전달되는 포매터 유형을 사용자 정의할 수 있습니다:

```php
'browser' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\BrowserConsoleHandler::class,
    'formatter' => Monolog\Formatter\HtmlFormatter::class,
    'formatter_with' => [
        'dateFormat' => 'Y-m-d',
    ],
],
```



자체 포매터를 제공할 수 있는 Monolog 핸들러를 사용 중인 경우, `formatter` 구성 옵션의 값을 `default`로 설정할 수 있습니다:

```php
'newrelic' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\NewRelicHandler::class,
    'formatter' => 'default',
],
```



<a name="monolog-processors"></a>
#### 모놀로그 프로세서

모놀로그는 메시지를 기록하기 전에 처리할 수도 있습니다. 직접 프로세서를 만들거나 [모놀로그에서 제공하는 기존 프로세서](https://github.com/Seldaek/monolog/tree/main/src/Monolog/Processor)를 사용할 수 있습니다.

`monolog` 드라이버의 프로세서를 커스터마이즈하고 싶다면, 채널 구성에 `processors` 구성 값을 추가하세요:

```php
'memory' => [
    'driver' => 'monolog',
    'handler' => Monolog\Handler\StreamHandler::class,
    'handler_with' => [
        'stream' => 'php://stderr',
    ],
    'processors' => [
        // Simple syntax...
        Monolog\Processor\MemoryUsageProcessor::class,

        // With options...
        [
            'processor' => Monolog\Processor\PsrLogMessageProcessor::class,
            'with' => ['removeUsedContextFields' => true],
        ],
    ],
],
```



<a name="creating-custom-channels-via-factories"></a>
### 팩토리를 통한 커스텀 채널 생성

Monolog의 인스턴스화 및 구성을 완전히 제어할 수 있는 완전히 맞춤형 채널을 정의하고자 하는 경우, `config/logging.php` 구성 파일에 `custom` 드라이버 유형을 지정할 수 있습니다. 구성에는 Monolog 인스턴스를 생성하기 위해 호출될 팩토리 클래스의 이름을 포함하는 `via` 옵션을 포함해야 합니다:

```php
'channels' => [
    'example-custom-channel' => [
        'driver' => 'custom',
        'via' => App\Logging\CreateCustomLogger::class,
    ],
],
```



`custom` 드라이버 채널을 구성한 후에는 Monolog 인스턴스를 생성할 클래스를 정의할 준비가 된 것입니다. 이 클래스는 Monolog 로거 인스턴스를 반환해야 하는 단일 `__invoke` 메서드만 필요합니다. 이 메서드는 채널 구성 배열을 유일한 인수로 받게 됩니다:

```php
<?php

namespace App\Logging;

use Monolog\Logger;

class CreateCustomLogger
{
    /**
     * Create a custom Monolog instance.
     */
    public function __invoke(array $config): Logger
    {
        return new Logger(/* ... */);
    }
}
```



<a name="tailing-log-messages-using-pail"></a>
## Pail을 사용하여 로그 메시지 실시간 확인

종종 애플리케이션의 로그를 실시간으로 확인해야 할 때가 있습니다. 예를 들어, 문제를 디버그하거나 특정 유형의 오류를 모니터링할 때입니다.

Laravel Pail은 명령줄에서 직접 Laravel 애플리케이션의 로그 파일을 쉽게 탐색할 수 있게 해주는 패키지입니다. 표준 `tail` 명령과 달리, Pail은 [Laravel Nightwatch](https://nightwatch.laravel.com), Sentry, Flare를 포함한 모든 로그 드라이버와 함께 작동하도록 설계되었습니다. 또한, Pail은 필요한 정보를 빠르게 찾을 수 있도록 도와주는 유용한 필터 세트를 제공합니다.

<img src="https://laravel.com/img/docs/pail-example.png">

<a name="pail-installation"></a>
### 설치

> [!WARNING]
> Laravel Pail은 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장이 필요합니다.

시작하려면 Composer 패키지 관리자를 사용하여 프로젝트에 Pail을 설치하세요:

```shell
composer require --dev laravel/pail
```



<a name="pail-usage"></a>
### 사용법

로그를 실시간으로 확인하려면 `pail` 명령어를 실행하세요:

```shell
php artisan pail
```



출력의 자세한 정도를 높이고 잘림(...)을 방지하려면, `-v` 옵션을 사용하세요:

```shell
php artisan pail -v
```



최대 상세 정보를 위해 예외 스택 추적을 표시하려면 `-vv` 옵션을 사용하세요:

```shell
php artisan pail -vv
```



로그 추적을 중지하려면 언제든지 `Ctrl+C`를 누르세요.

<a name="pail-filtering-logs"></a>
### 로그 필터링

<a name="pail-filtering-logs-filter-option"></a>
#### `--filter`

로그를 유형, 파일, 메시지 및 스택 추적 내용별로 필터링하려면 `--filter` 옵션을 사용할 수 있습니다:

```shell
php artisan pail --filter="QueryException"
```



<a name="pail-filtering-logs-message-option"></a>
#### `--message`

로그를 메시지로만 필터링하려면 `--message` 옵션을 사용할 수 있습니다:

```shell
php artisan pail --message="User created"
```



<a name="pail-filtering-logs-level-option"></a>
#### `--level`

`--level` 옵션은 [로그 수준](#log-levels)별로 로그를 필터링하는 데 사용할 수 있습니다:

```shell
php artisan pail --level=error
```



<a name="pail-filtering-logs-user-option"></a>
#### `--user`

특정 사용자가 인증된 동안 기록된 로그만 표시하려면 `--user` 옵션에 사용자의 ID를 제공할 수 있습니다:

```shell
php artisan pail --user=1
```
{% endraw %}
