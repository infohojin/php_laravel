---
layout: docs
title: "구성"
---

{% raw %}
# 구성

- [소개](#introduction)
- [환경설정](#environment-configuration)
    - [환경변수 종류](#environment-variable-types)
    - [환경 구성 불러오기](#retrieving-environment-configuration)
    - [현재 환경 파악](#determining-the-current-environment)
    - [환경 파일 암호화](#encrypting-environment-files)
- [구성 값 접근](#accessing-configuration-values)
- [구성 캐싱](#configuration-caching)
- [구성 게시](#configuration-publishing)
- [디버그 모드](#debug-mode)
- [유지관리 모드](#maintenance-mode)

<a name="introduction"></a>
## 소개

Laravel 프레임워크의 모든 구성 파일은 `config` 디렉터리에 저장됩니다. 각 옵션은 문서화되어 있으므로 자유롭게 파일을 살펴보고 사용 가능한 옵션에 익숙해지세요.

이러한 구성 파일을 사용하면 데이터베이스 연결 정보, 메일 서버 정보는 물론 애플리케이션 URL 및 암호화 키와 같은 다양한 기타 핵심 구성 값을 구성할 수 있습니다.

<a name="the-about-command"></a>
#### `about` 명령

Laravel은 `about` Artisan 명령을 통해 애플리케이션의 구성, 드라이버 및 환경에 대한 개요를 표시할 수 있습니다.

```shell
php artisan about

```

애플리케이션 개요 출력의 특정 섹션에만 관심이 있는 경우 `--only` 옵션을 사용하여 해당 섹션을 필터링할 수 있습니다.

```shell
php artisan about --only=environment

```

또는 특정 구성 파일의 값을 자세히 살펴보려면 `config:show` Artisan 명령을 사용할 수 있습니다.

```shell
php artisan config:show database

```

<a name="environment-configuration"></a>
## 환경 구성

애플리케이션이 실행되는 환경에 따라 다른 구성 값을 갖는 것이 도움이 되는 경우가 많습니다. 예를 들어 프로덕션 서버에서 사용하는 것과 다른 캐시 드라이버를 로컬에서 사용하려고 할 수 있습니다.

이를 쉽게 만들기 위해 Laravel은 [DotEnv](https://github.com/vlucas/phpdotenv) PHP 라이브러리를 활용합니다. Laravel을 새로 설치하면 애플리케이션의 루트 디렉터리에 많은 공통 환경 변수를 정의하는 `.env.example` 파일이 포함됩니다. Laravel 설치 과정에서 이 파일은 자동으로 `.env`에 복사됩니다.

Laravel의 기본 `.env` 파일에는 애플리케이션이 로컬에서 실행되는지 아니면 프로덕션 웹 서버에서 실행되는지에 따라 다를 수 있는 몇 가지 일반적인 구성 값이 포함되어 있습니다. 그런 다음 Laravel의 `env` 기능을 사용하여 `config` 디렉터리 내의 구성 파일에서 이러한 값을 읽습니다.

팀과 함께 개발하는 경우 애플리케이션에 `.env.example` 파일을 계속 포함하고 업데이트할 수 있습니다. 예제 구성 파일에 자리 표시자 값을 입력하면 팀의 다른 개발자가 애플리케이션을 실행하는 데 필요한 환경 변수를 명확하게 확인할 수 있습니다.

> [!NOTE]
> `.env` 파일의 모든 변수는 서버 수준 또는 시스템 수준 환경 변수와 같은 외부 환경 변수로 재정의될 수 있습니다.

<a name="environment-file-security"></a>
#### 환경 파일 보안

귀하의 애플리케이션을 사용하는 각 개발자/서버는 서로 다른 환경 구성을 요구할 수 있으므로 `.env` 파일을 애플리케이션의 소스 제어에 커밋해서는 안 됩니다. 또한 침입자가 소스 제어 저장소에 대한 액세스 권한을 얻는 경우 민감한 자격 증명이 노출되므로 보안 위험이 될 수 있습니다.

그러나 Laravel에 내장된 [환경 암호화](#encrypting-environment-files)를 사용하여 환경 파일을 암호화하는 것이 가능합니다. 암호화된 환경 파일은 소스 제어에 안전하게 배치될 수 있습니다.

<a name="additional-environment-files"></a>
#### 추가 환경 파일

애플리케이션의 환경 변수를 로드하기 전에 Laravel은 `APP_ENV` 환경 변수가 외부에서 제공되었는지 또는 `--env` CLI 인수가 지정되었는지 확인합니다. 그렇다면 Laravel은 `.env.[APP_ENV]` 파일이 존재하는 경우 해당 파일을 로드하려고 시도합니다. 존재하지 않는 경우 기본 `.env` 파일이 로드됩니다.

<a name="environment-variable-types"></a>
### 환경 변수 유형

`.env` 파일의 모든 변수는 일반적으로 문자열로 구문 분석되므로 `env()` 함수에서 더 넓은 범위의 유형을 반환할 수 있도록 일부 예약된 값이 생성되었습니다.

<div class="overflow-auto">

| `.env` 값 | `env()` 값 |
| ------------ | ------------- |
| 사실 | (부울) 참 |
| (사실) | (부울) 참 |
| 거짓 | (부울) 거짓 |
| (거짓) | (부울) 거짓 |
| 비어 있음 | (문자열) '' |
| (비어 있음) | (문자열) '' |
| null | (널) 널 |
| (널) | (널) 널 |

</div>

공백이 포함된 값으로 환경 변수를 정의해야 하는 경우 값을 큰따옴표로 묶어서 정의할 수 있습니다.

```ini
APP_NAME="My Application"

```

<a name="retrieving-environment-configuration"></a>
### 환경 구성 검색 중

`.env` 파일에 나열된 모든 변수는 애플리케이션이 요청을 받으면 `$_ENV` PHP 슈퍼 전역에 로드됩니다. 그러나 `env` 함수를 사용하여 구성 파일의 이러한 변수에서 값을 검색할 수 있습니다. 실제로 Laravel 구성 파일을 검토하면 많은 옵션이 이미 이 기능을 사용하고 있음을 알 수 있습니다.

```php
'debug' => (bool) env('APP_DEBUG', false),

```

`env` 함수에 전달된 두 번째 값은 "기본값"입니다. 해당 키에 대한 환경 변수가 없으면 이 값이 반환됩니다.

<a name="determining-the-current-environment"></a>
### 현재 환경 결정

현재 애플리케이션 환경은 `.env` 파일의 `APP_ENV` 변수를 통해 결정됩니다. `App` [facade](/docs/{{version}}/facades)에서 `environment` 메서드를 통해 이 값에 액세스할 수 있습니다.

```php
use Illuminate\Support\Facades\App;

$environment = App::environment();

```

또한 환경이 주어진 값과 일치하는지 확인하기 위해 `environment` 메서드에 인수를 전달할 수도 있습니다. 환경이 주어진 값 중 하나와 일치하면 메소드는 `true`를 반환합니다.

```php
if (App::environment('local')) {
    // The environment is local
}

if (App::environment(['local', 'staging'])) {
    // The environment is either local OR staging...
}

```

> [!NOTE]
> 현재 애플리케이션 환경 감지는 서버 수준 `APP_ENV` 환경 변수를 정의하여 재정의할 수 있습니다.

<a name="encrypting-environment-files"></a>
### 환경 파일 암호화

암호화되지 않은 환경 파일은 소스 제어에 저장하면 안 됩니다. 그러나 Laravel을 사용하면 환경 파일을 암호화하여 애플리케이션의 나머지 부분과 함께 소스 제어에 안전하게 추가할 수 있습니다.

<a name="encryption"></a>
#### 암호화

환경 파일을 암호화하려면 `env:encrypt` 명령을 사용할 수 있습니다.

```shell
php artisan env:encrypt

```

`env:encrypt` 명령을 실행하면 `.env` 파일이 암호화되고 암호화된 내용이 `.env.encrypted` 파일에 저장됩니다. 암호 해독 키는 명령 출력에 표시되며 보안 암호 관리자에 저장되어야 합니다. 자신만의 암호화 키를 제공하려면 다음 명령을 호출할 때 `--key` 옵션을 사용할 수 있습니다.

```shell
php artisan env:encrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF

```

> [!NOTE]
> 제공된 키 길이는 사용 중인 암호화 암호에 필요한 키 길이와 일치해야 합니다. 기본적으로 Laravel은 32자 키가 필요한 `AES-256-CBC` 암호를 사용합니다. 명령을 호출할 때 `--cipher` 옵션을 전달하면 Laravel의 [암호화기](/docs/{{version}}/encryption)가 지원하는 모든 암호를 자유롭게 사용할 수 있습니다.

애플리케이션에 `.env` 및 `.env.staging`와 같은 여러 환경 파일이 있는 경우 `--env` 옵션을 통해 환경 이름을 제공하여 암호화해야 하는 환경 파일을 지정할 수 있습니다.

```shell
php artisan env:encrypt --env=staging

```

<a name="readable-variable-names"></a>
#### 읽을 수 있는 변수 이름

환경 파일을 암호화할 때 `--readable` 옵션을 사용하여 해당 값을 암호화하는 동안 표시되는 변수 이름을 유지할 수 있습니다.

```shell
php artisan env:encrypt --readable

```

그러면 다음 형식의 암호화된 파일이 생성됩니다.

```ini
APP_NAME=eyJpdiI6...
APP_ENV=eyJpdiI6...
APP_KEY=eyJpdiI6...
APP_DEBUG=eyJpdiI6...
APP_URL=eyJpdiI6...

```

읽을 수 있는 형식을 사용하면 민감한 데이터를 노출하지 않고도 어떤 환경 변수가 존재하는지 확인할 수 있습니다. 또한 파일을 해독하지 않고도 어떤 변수가 추가, 제거 또는 이름이 변경되었는지 확인할 수 있으므로 풀 요청 검토가 훨씬 쉬워집니다.

환경 파일을 복호화할 때 Laravel은 어떤 형식이 사용되었는지 자동으로 감지하므로 `env:decrypt` 명령에 추가 옵션이 필요하지 않습니다.

> [!NOTE]
> `--readable` 옵션을 사용할 경우 원본 환경 파일의 설명과 빈 줄은 암호화된 출력에 포함되지 않습니다.

<a name="updating-readable-environment-files"></a>
#### 읽기 가능한 환경 파일 업데이트 중

읽을 수 있는 암호화된 환경 파일을 업데이트할 때 Laravel은 변경되지 않은 값을 유지하고 소스 환경 파일에 더 이상 존재하지 않는 변수를 제거합니다.

```shell
php artisan env:encrypt --readable --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF

```

암호화된 파일이 없으면 생성됩니다. 기존 파일을 업데이트할 때 해당 파일을 생성하는 데 사용한 것과 동일한 암호화 키와 암호를 제공하세요. 파일을 해독할 수 없으면 덮어쓰지 않고 명령이 실패합니다.

모든 값을 다시 암호화하려면 `--force` 옵션을 사용하세요. 이를 통해 암호화 키를 변경하거나 유효하지 않은 암호화된 파일을 교체할 수 있습니다.

```shell
php artisan env:encrypt --readable --force --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF

```

<a name="decryption"></a>
#### 암호 해독

환경 파일의 암호를 해독하려면 `env:decrypt` 명령을 사용할 수 있습니다. 이 명령에는 Laravel이 `LARAVEL_ENV_ENCRYPTION_KEY` 환경 변수에서 검색할 암호 해독 키가 필요합니다.

```shell
php artisan env:decrypt

```

Or, the key may be provided directly to the command via the `--key` option:

```shell
php artisan env:decrypt --key=3UVsEgGVK36XN82KKeyLFMhvosbZN1aF

```

When the `env:decrypt` command is invoked, Laravel will decrypt the contents of the `.env.encrypted` file and place the decrypted contents in the `.env` file.

The `--cipher` option may be provided to the `env:decrypt` command in order to use a custom encryption cipher:

```shell
php artisan env:decrypt --key=qUWuNRdfuImXcKxZ --cipher=AES-128-CBC

```

If your application has multiple environment files, such as `.env` and `.env.staging`, you may specify the environment file that should be decrypted by providing the environment name via the `--env` option:

```shell
php artisan env:decrypt --env=staging

```

In order to overwrite an existing environment file, you may provide the `--force` option to the `env:decrypt` command:

```shell
php artisan env:decrypt --force

```

<a name="accessing-configuration-values"></a>
## Accessing Configuration Values

You may easily access your configuration values using the `Config` facade or global `config` function from anywhere in your application. The configuration values may be accessed using "dot" syntax, which includes the name of the file and option you wish to access. A default value may also be specified and will be returned if the configuration option does not exist:

```php
use Illuminate\Support\Facades\Config;

$value = Config::get('app.timezone');

$value = config('app.timezone');

// Retrieve a default value if the configuration value does not exist...
$value = config('app.timezone', 'Asia/Seoul');

```

To set configuration values at runtime, you may invoke the `Config` facade's `set` method or pass an array to the `config` function:

```php
Config::set('app.timezone', 'America/Chicago');

config(['app.timezone' => 'America/Chicago']);

```

To assist with static analysis, the `Config` facade also provides typed configuration retrieval methods. If the retrieved configuration value does not match the expected type, an exception will be thrown:

```php
Config::string('config-key');
Config::integer('config-key');
Config::float('config-key');
Config::boolean('config-key');
Config::array('config-key');
Config::collection('config-key');

```

<a name="configuration-caching"></a>
## Configuration Caching

To give your application a speed boost, you should cache all of your configuration files into a single file using the `config:cache` Artisan command. This will combine all of the configuration options for your application into a single file which can be quickly loaded by the framework.

You should typically run the `php artisan config:cache` command as part of your production deployment process. The command should not be run during local development as configuration options will frequently need to be changed during the course of your application's development.

Once the configuration has been cached, your application's `.env` file will not be loaded by the framework during requests or Artisan commands; therefore, the `env` function will only return external, system level environment variables.

For this reason, you should ensure you are only calling the `env` function from within your application's configuration (`config`) files. You can see many examples of this by examining Laravel's default configuration files. Configuration values may be accessed from anywhere in your application using the `config` function [described above](#accessing-configuration-values).

The `config:clear` command may be used to purge the cached configuration:

```shell
php artisan config:clear

```

> [!WARNING]
> If you execute the `config:cache` command during your deployment process, you should be sure that you are only calling the `env` function from within your configuration files. Once the configuration has been cached, the `.env` file will not be loaded; therefore, the `env` function will only return external, system level environment variables.

<a name="configuration-publishing"></a>
## Configuration Publishing

Most of Laravel's configuration files are already published in your application's `config` directory; however, certain configuration files like `cors.php` and `view.php` are not published by default, as most applications will never need to modify them.

However, you may use the `config:publish` Artisan command to publish any configuration files that are not published by default:

```shell
php artisan config:publish

php artisan config:publish --all

```

<a name="debug-mode"></a>
## Debug Mode

The `debug` option in your `config/app.php` configuration file determines how much information about an error is actually displayed to the user. By default, this option is set to respect the value of the `APP_DEBUG` environment variable, which is stored in your `.env` file.

> [!WARNING]
> For local development, you should set the `APP_DEBUG` environment variable to `true`. **In your production environment, this value should always be `false`. If the variable is set to `true` in production, you risk exposing sensitive configuration values to your application's end users.**

<a name="maintenance-mode"></a>
## Maintenance Mode

When your application is in maintenance mode, a custom view will be displayed for all requests into your application. This makes it easy to "disable" your application while it is updating or when you are performing maintenance. A maintenance mode check is included in the default middleware stack for your application. If the application is in maintenance mode, a `Symfony\Component\HttpKernel\Exception\HttpException` instance will be thrown with a status code of 503.

To enable maintenance mode, execute the `down` Artisan command:

```shell
php artisan down

```

If you would like the `Refresh` HTTP header to be sent with all maintenance mode responses, you may provide the `refresh` option when invoking the `down` command. The `Refresh` header will instruct the browser to automatically refresh the page after the specified number of seconds:

```shell
php artisan down --refresh=15

```

You may also provide a `retry` option to the `down` command, which will be set as the `Retry-After` HTTP header's value, although browsers generally ignore this header:

```shell
php artisan down --retry=60

```

<a name="bypassing-maintenance-mode"></a>
#### Bypassing Maintenance Mode

To allow maintenance mode to be bypassed using a secret token, you may use the `secret` option to specify a maintenance mode bypass token:

```shell
php artisan down --secret="1630542a-246b-4b66-afa1-dd72a4c43515"

```

After placing the application in maintenance mode, you may navigate to the application URL matching this token and Laravel will issue a maintenance mode bypass cookie to your browser:

```shell
https://example.com/1630542a-246b-4b66-afa1-dd72a4c43515

```

If you would like Laravel to generate the secret token for you, you may use the `with-secret` option. The secret will be displayed to you once the application is in maintenance mode:

```shell
php artisan down --with-secret

```

When accessing this hidden route, you will then be redirected to the `/` route of the application. Once the cookie has been issued to your browser, you will be able to browse the application normally as if it was not in maintenance mode.

> [!NOTE]
> Your maintenance mode secret should typically consist of alpha-numeric characters and, optionally, dashes. You should avoid using characters that have special meaning in URLs such as `?` or `&`.

<a name="maintenance-mode-on-multiple-servers"></a>
#### Maintenance Mode on Multiple Servers

By default, Laravel determines if your application is in maintenance mode using a file-based system. This means to activate maintenance mode, the `php artisan down` command has to be executed on each server hosting your application.

Alternatively, Laravel offers a cache-based method for handling maintenance mode. This method requires running the `php artisan down` command on just one server. To use this approach, modify the maintenance mode variables in your application's `.env` file. You should select a cache `store` that is accessible by all of your servers. This ensures the maintenance mode status is consistently maintained across every server:

```ini
APP_MAINTENANCE_DRIVER=cache
APP_MAINTENANCE_STORE=database

```

<a name="pre-rendering-the-maintenance-mode-view"></a>
#### Pre-Rendering the Maintenance Mode View

If you utilize the `php artisan down` command during deployment, your users may still occasionally encounter errors if they access the application while your Composer dependencies or other infrastructure components are updating. This occurs because a significant part of the Laravel framework must boot in order to determine your application is in maintenance mode and render the maintenance mode view using the templating engine.

For this reason, Laravel allows you to pre-render a maintenance mode view that will be returned at the very beginning of the request cycle. This view is rendered before any of your application's dependencies have loaded. You may pre-render a template of your choice using the `down` command's `render` option:

```shell
php artisan down --render="errors::503"

```

<a name="redirecting-maintenance-mode-requests"></a>
#### Redirecting Maintenance Mode Requests

While in maintenance mode, Laravel will display the maintenance mode view for all application URLs the user attempts to access. If you wish, you may instruct Laravel to redirect all requests to a specific URL. This may be accomplished using the `redirect` option. For example, you may wish to redirect all requests to the `/` URI:

```shell
php artisan down --redirect=/

```

<a name="disabling-maintenance-mode"></a>
#### Disabling Maintenance Mode

To disable maintenance mode, use the `up` command:

```shell
php artisan up

```

> [!NOTE]
> You may customize the default maintenance mode template by defining your own template at `resources/views/errors/503.blade.php`.

<a name="maintenance-mode-queues"></a>
#### Maintenance Mode and Queues

While your application is in maintenance mode, no [queued jobs](/docs/{{version}}/queues) will be handled. The jobs will continue to be handled as normal once the application is out of maintenance mode.

<a name="alternatives-to-maintenance-mode"></a>
#### Alternatives to Maintenance Mode

Since maintenance mode requires your application to have several seconds of downtime, consider running your applications on a fully-managed platform like [Laravel Cloud](https://cloud.laravel.com) to accomplish zero-downtime deployment with Laravel.
{% endraw %}
