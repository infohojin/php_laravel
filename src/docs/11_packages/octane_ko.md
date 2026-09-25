---
layout: docs
title: "Laravel Octane"
---

{% raw %}
# Laravel Octane

- [Introduction](#introduction)
- [Installation](#installation)
- [Server Prerequisites](#server-prerequisites)
    - [FrankenPHP](#frankenphp)
    - [RoadRunner](#roadrunner)
    - [Swoole](#swoole)
- [Serving Your Application](#serving-your-application)
    - [Serving Your Application via HTTPS](#serving-your-application-via-https)
    - [Serving Your Application via Nginx](#serving-your-application-via-nginx)
    - [Watching for File Changes](#watching-for-file-changes)
    - [Specifying the Worker Count](#specifying-the-worker-count)
    - [Specifying the Max Request Count](#specifying-the-max-request-count)
    - [Specifying the Max Execution Time](#specifying-the-max-execution-time)
    - [Reloading the Workers](#reloading-the-workers)
    - [Stopping the Server](#stopping-the-server)
- [Dependency Injection and Octane](#dependency-injection-and-octane)
    - [Container Injection](#container-injection)
    - [Request Injection](#request-injection)
    - [Configuration Repository Injection](#configuration-repository-injection)
- [Managing Memory Leaks](#managing-memory-leaks)
- [Concurrent Tasks](#concurrent-tasks)
- [Ticks and Intervals](#ticks-and-intervals)
- [The Octane Cache](#the-octane-cache)
    - [Cache Intervals](#cache-intervals)
- [Tables](#tables)

<a name="introduction"></a>
## Introduction

[Laravel Octane](https://github.com/laravel/octane) supercharges your application's performance by serving your application using high-powered application servers, including [FrankenPHP](https://frankenphp.dev/), [Open Swoole](https://openswoole.com/), [Swoole](https://github.com/swoole/swoole-src), and [RoadRunner](https://roadrunner.dev). Octane boots your application once, keeps it in memory, and then feeds it requests at supersonic speeds.

<a name="installation"></a>
## Installation

Octane may be installed via the Composer package manager:

```shell
composer require laravel/octane
```



Octane을 설치한 후에는 `octane:install` Artisan 명령을 실행할 수 있으며, 이는 Octane의 설정 파일을 애플리케이션에 설치합니다:

```shell
php artisan octane:install
```



<a name="server-prerequisites"></a>
## 서버 전제 조건

<a name="frankenphp"></a>
### 프랑켄PHP

[프랑켄PHP](https://frankenphp.dev)는 Go로 작성된 PHP 애플리케이션 서버로, 조기 힌트, 브로틀리(Brotli), Z표준(Zstandard) 압축과 같은 최신 웹 기능을 지원합니다. Octane을 설치하고 서버로 프랑켄PHP를 선택하면 Octane이 자동으로 프랑켄PHP 바이너리를 다운로드하고 설치합니다.

<a name="frankenphp-via-laravel-sail"></a>
#### Laravel Sail을 통한 프랑켄PHP

애플리케이션을 [Laravel Sail](/docs/{{version}}/sail)로 개발할 계획이라면 Octane과 프랑켄PHP를 설치하기 위해 다음 명령어를 실행해야 합니다:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane
```



다음으로, FrankenPHP 바이너리를 설치하기 위해 `octane:install` Artisan 명령을 사용해야 합니다:

```shell
./vendor/bin/sail artisan octane:install --server=frankenphp
```



마지막으로, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 환경 변수에는 Sail이 PHP 개발 서버 대신 Octane을 사용하여 애플리케이션을 제공할 때 사용할 명령어가 포함됩니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=frankenphp --host=0.0.0.0 --admin-port=2019 --port='${APP_PORT:-80}'" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```



HTTPS, HTTP/2 및 HTTP/3를 활성화하려면 대신 다음과 같은 수정을 적용하세요:

```yaml
services:
  laravel.test:
    ports:
        - '${APP_PORT:-80}:80'
        - '${VITE_PORT:-5173}:${VITE_PORT:-5173}'
        - '443:443' # [tl! add]
        - '443:443/udp' # [tl! add]
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --host=localhost --port=443 --admin-port=2019 --https" # [tl! add]
      XDG_CONFIG_HOME:  /var/www/html/config # [tl! add]
      XDG_DATA_HOME:  /var/www/html/data # [tl! add]
```



일반적으로, `https://127.0.0.1`를 사용하는 것은 추가 설정이 필요하고 [권장되지 않기](https://frankenphp.dev/docs/known-issues/#using-https127001-with-docker) 때문에, `https://localhost`를 통해 FrankenPHP Sail 애플리케이션에 접근하는 것이 좋습니다.

<a name="frankenphp-via-docker"></a>
#### Docker를 통한 FrankenPHP

FrankenPHP의 공식 Docker 이미지를 사용하면 성능이 향상되고, FrankenPHP의 정적 설치에는 포함되지 않은 추가 확장 기능을 사용할 수 있습니다. 또한, 공식 Docker 이미지는 Windows와 같이 FrankenPHP가 기본적으로 지원하지 않는 플랫폼에서도 실행을 지원합니다. FrankenPHP의 공식 Docker 이미지는 로컬 개발과 프로덕션 환경 모두에 적합합니다.

FrankenPHP 기반 Laravel 애플리케이션을 컨테이너화하는 시작점으로 아래 Dockerfile을 사용할 수 있습니다:

```dockerfile
FROM dunglas/frankenphp

RUN install-php-extensions \
    pcntl
    # Add other PHP extensions here...

COPY . /app

ENTRYPOINT ["php", "artisan", "octane:frankenphp"]
```



그런 다음 개발 중에는 다음 Docker Compose 파일을 사용하여 애플리케이션을 실행할 수 있습니다:

```yaml
# compose.yaml
services:
  frankenphp:
    build:
      context: .
    entrypoint: php artisan octane:frankenphp --workers=1 --max-requests=1
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```



`php artisan octane:start` 명령어에 `--log-level` 옵션이 명시적으로 전달되면, Octane은 FrankenPHP의 기본 로거를 사용하며, 별도로 구성되지 않는 한 구조화된 JSON 로그를 생성합니다.

FrankenPHP를 Docker와 함께 실행하는 방법에 대한 자세한 정보는 [공식 FrankenPHP 문서](https://frankenphp.dev/docs/docker/)를 참조할 수 있습니다.

<a name="frankenphp-caddyfile"></a>
#### 맞춤형 Caddyfile 구성

FrankenPHP를 사용할 때, Octane을 시작할 때 `--caddyfile` 옵션을 사용하여 맞춤형 Caddyfile을 지정할 수 있습니다:

```shell
php artisan octane:start --server=frankenphp --caddyfile=/path/to/your/Caddyfile
```



이렇게 하면 사용자 지정 미들웨어 추가, 고급 라우팅 구성 또는 사용자 지정 지시문 설정과 같은 기본 설정을 넘어 FrankenPHP의 구성을 사용자화할 수 있습니다. Caddyfile 구문 및 구성 옵션에 대한 자세한 내용은 [공식 Caddy 문서](https://caddyserver.com/docs/caddyfile)를 참조할 수 있습니다.

<a name="roadrunner"></a>
### 로드러너

[로드러너](https://roadrunner.dev)는 Go를 사용하여 빌드된 RoadRunner 바이너리에 의해 구동됩니다. RoadRunner 기반 Octane 서버를 처음 시작하면 Octane이 RoadRunner 바이너리를 다운로드하고 설치할 것인지 제안합니다.

<a name="roadrunner-via-laravel-sail"></a>
#### Laravel Sail을 통한 로드러너

[Laravel Sail](/docs/{{version}}/sail)을 사용하여 애플리케이션을 개발할 계획이라면 Octane과 RoadRunner를 설치하기 위해 다음 명령어를 실행해야 합니다:

```shell
./vendor/bin/sail up

./vendor/bin/sail composer require laravel/octane spiral/roadrunner-cli spiral/roadrunner-http
```



다음으로, Sail 셸을 시작하고 `rr` 실행 파일을 사용하여 RoadRunner 바이너리의 최신 Linux 기반 빌드를 가져와야 합니다:

```shell
./vendor/bin/sail shell

# Within the Sail shell...
./vendor/bin/rr get-binary
```



그런 다음, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가합니다. 이 환경 변수에는 Sail이 PHP 개발 서버 대신 Octane을 사용하여 애플리케이션을 제공할 때 사용할 명령어가 포함됩니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=roadrunner --host=0.0.0.0 --rpc-port=6001 --port='${APP_PORT:-80}'" # [tl! add]
```



마지막으로, `rr` 바이너리가 실행 가능하도록 하고 Sail 이미지를 빌드하세요:

```shell
chmod +x ./rr

./vendor/bin/sail build --no-cache
```



<a name="swoole"></a>
### Swoole

Laravel Octane 애플리케이션을 제공하기 위해 Swoole 애플리케이션 서버를 사용하려는 경우, 반드시 Swoole PHP 확장 기능을 설치해야 합니다. 일반적으로 이는 PECL을 통해 수행할 수 있습니다:

```shell
pecl install swoole
```



<a name="openswoole"></a>
#### 오픈 스울

Laravel Octane 애플리케이션을 서비스하기 위해 Open Swoole 애플리케이션 서버를 사용하려면 Open Swoole PHP 확장 프로그램을 설치해야 합니다. 일반적으로 이는 PECL을 통해 수행할 수 있습니다:

```shell
pecl install openswoole
```



Open Swoole과 함께 Laravel Octane을 사용하면 동시 작업, 틱(ticks), 인터벌(interval)과 같은 Swoole이 제공하는 동일한 기능을 활용할 수 있습니다.

#### Laravel Sail을 통한 Swoole

> Sail을 통해 Octane 애플리케이션을 제공하기 전에, 최신 버전의 Laravel Sail이 설치되어 있는지 확인하고 애플리케이션 루트 디렉토리에서 `./vendor/bin/sail build --no-cache`를 실행하세요.

또는 [Laravel Sail](/docs/{{version}}/sail)을 사용하여 Swoole 기반 Octane 애플리케이션을 개발할 수 있습니다. Laravel에 대한 공식 Docker 기반 개발 환경인 Laravel Sail은 기본적으로 Swoole 확장 기능을 포함하고 있습니다. 그러나 Sail에서 사용하는 `docker-compose.yml` 파일은 여전히 조정해야 합니다.

시작하려면, 애플리케이션의 `docker-compose.yml` 파일에서 `laravel.test` 서비스 정의에 `SUPERVISOR_PHP_COMMAND` 환경 변수를 추가하세요. 이 환경 변수에는 Sail이 PHP 개발 서버 대신 Octane을 사용하여 애플리케이션을 제공할 때 사용할 명령이 포함됩니다:

```yaml
services:
  laravel.test:
    environment:
      SUPERVISOR_PHP_COMMAND: "/usr/bin/php -d variables_order=EGPCS /var/www/html/artisan octane:start --server=swoole --host=0.0.0.0 --port='${APP_PORT:-80}'" # [tl! add]
```



마지막으로, Sail 이미지를 빌드하세요:

```shell
./vendor/bin/sail build --no-cache
```



<a name="swoole-configuration"></a>
#### Swoole 구성

Swoole은 필요에 따라 `octane` 구성 파일에 추가할 수 있는 몇 가지 추가 구성 옵션을 지원합니다. 이 옵션들은 거의 수정할 필요가 없기 때문에 기본 구성 파일에는 포함되어 있지 않습니다:

```php
'swoole' => [
    'options' => [
        'log_file' => storage_path('logs/swoole_http.log'),
        'package_max_length' => 10 * 1024 * 1024,
    ],
],
```



<a name="serving-your-application"></a>
## 애플리케이션 제공

Octane 서버는 `octane:start` Artisan 명령어를 통해 시작할 수 있습니다. 기본적으로 이 명령어는 애플리케이션의 `octane` 구성 파일의 `server` 구성 옵션에 지정된 서버를 사용합니다:

```shell
php artisan octane:start
```



기본적으로 Octane은 포트 8000에서 서버를 시작하므로 웹 브라우저를 통해 `http://localhost:8000`에서 애플리케이션에 접속할 수 있습니다.

<a name="keeping-octane-running-in-production"></a>
#### 프로덕션 환경에서 Octane 실행 유지하기

Octane 애플리케이션을 프로덕션에 배포하는 경우, Octane 서버가 계속 실행되도록 Supervisor와 같은 프로세스 모니터를 사용하는 것이 좋습니다. Octane용 샘플 Supervisor 구성 파일은 다음과 같을 수 있습니다:

```ini
[program:octane]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/example.com/artisan octane:start --server=frankenphp --host=127.0.0.1 --port=8000
autostart=true
autorestart=true
user=forge
redirect_stderr=true
stdout_logfile=/home/forge/example.com/storage/logs/octane.log
stopwaitsecs=3600
```



<a name="serving-your-application-via-https"></a>
### HTTPS를 통해 애플리케이션 제공하기

기본적으로, Octane을 통해 실행되는 애플리케이션은 `http://`로 시작하는 링크를 생성합니다. 애플리케이션의 `config/octane.php` 설정 파일 내에서 사용되는 `OCTANE_HTTPS` 환경 변수는 애플리케이션을 HTTPS로 제공할 때 `true`로 설정할 수 있습니다. 이 설정 값이 `true`로 설정되면, Octane은 Laravel에 모든 생성된 링크에 `https://`를 접두사로 붙이도록 지시합니다:

```php
'https' => env('OCTANE_HTTPS', false),
```



<a name="serving-your-application-via-nginx"></a>
### Nginx를 통한 애플리케이션 제공

> [!NOTE]
> 서버 구성을 직접 관리할 준비가 되어 있지 않거나 강력한 Laravel Octane 애플리케이션을 실행하는 데 필요한 다양한 서비스를 구성하는 것이 부담된다면, 완전 관리형 Laravel Octane 지원을 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 확인해 보세요.

운영 환경에서는 Octane 애플리케이션을 Nginx 또는 Apache와 같은 전통적인 웹 서버 뒤에서 제공하는 것이 좋습니다. 이렇게 하면 웹 서버가 이미지나 스타일시트와 같은 정적 자산을 제공하고 SSL 인증서 종료를 관리할 수 있습니다.

아래 Nginx 구성 예제에서는 Nginx가 사이트의 정적 자산을 제공하고 포트 8000에서 실행 중인 Octane 서버로 요청을 프록시합니다:

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}

server {
    listen 80;
    listen [::]:80;
    server_name domain.com;
    server_tokens off;
    root /home/forge/domain.com/public;

    index index.php;

    charset utf-8;

    location /index.php {
        try_files /not_exists @octane;
    }

    location / {
        try_files $uri $uri/ @octane;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    access_log off;
    error_log  /var/log/nginx/domain.com-error.log error;

    error_page 404 /index.php;

    location @octane {
        set $suffix "";

        if ($uri = /index.php) {
            set $suffix ?$query_string;
        }

        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;

        proxy_pass http://127.0.0.1:8000$suffix;
    }
}
```



<a name="watching-for-file-changes"></a>
### 파일 변경 사항 감지

Octane 서버가 시작될 때 애플리케이션이 한 번 메모리에 로드되므로, 애플리케이션 파일에 대한 변경 사항은 브라우저를 새로 고침해도 반영되지 않습니다. 예를 들어, `routes/web.php` 파일에 추가된 라우트 정의는 서버를 재시작하기 전까지 반영되지 않습니다. 편의를 위해, 애플리케이션 내 파일 변경 시 Octane이 자동으로 서버를 재시작하도록 `--watch` 플래그를 사용할 수 있습니다:

```shell
php artisan octane:start --watch
```



이 기능을 사용하기 전에 로컬 개발 환경에 [Node](https://nodejs.org)가 설치되어 있는지 확인해야 합니다. 또한 프로젝트에 [Chokidar](https://github.com/paulmillr/chokidar) 파일 감시 라이브러리를 설치해야 합니다:

```shell
npm install --save-dev chokidar
```



애플리케이션의 `config/octane.php` 구성 파일 내 `watch` 구성 옵션을 사용하여 감시해야 하는 디렉토리와 파일을 구성할 수 있습니다.

<a name="specifying-the-worker-count"></a>
### 작업자 수 지정

기본적으로 Octane은 머신에서 제공하는 각 CPU 코어마다 애플리케이션 요청 작업자를 시작합니다. 이러한 작업자는 애플리케이션에 들어오는 HTTP 요청을 처리하는 데 사용됩니다. `octane:start` 명령을 호출할 때 `--workers` 옵션을 사용하여 시작할 작업자 수를 수동으로 지정할 수 있습니다:

```shell
php artisan octane:start --workers=4
```



Swoole 애플리케이션 서버를 사용 중인 경우, 시작할 ['task workers'](#concurrent-tasks)의 수를 지정할 수도 있습니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```



<a name="specifying-the-max-request-count"></a>
### 최대 요청 수 지정

스트레인 메모리 누수를 방지하기 위해, Octane은 각 워커가 500개의 요청을 처리하면 해당 워커를 원활하게 재시작합니다. 이 숫자를 조정하려면, `--max-requests` 옵션을 사용할 수 있습니다:

```shell
php artisan octane:start --max-requests=250
```



<a name="specifying-the-max-execution-time"></a>
### 최대 실행 시간 지정

기본적으로 Laravel Octane은 애플리케이션의 `config/octane.php` 구성 파일에 있는 `max_execution_time` 옵션을 통해 들어오는 요청에 대해 최대 실행 시간을 30초로 설정합니다:

```php
'max_execution_time' => 30,
```



이 설정은 들어오는 요청이 종료되기 전에 실행될 수 있는 최대 초 수를 정의합니다. 이 값을 `0`로 설정하면 실행 시간 제한이 완전히 비활성화됩니다. 이 구성 옵션은 파일 업로드, 데이터 처리 또는 외부 서비스에 대한 API 호출과 같이 장시간 실행되는 요청을 처리하는 애플리케이션에 특히 유용합니다.

> [!WARNING]
> `max_execution_time` 구성을 수정한 경우 변경 사항을 적용하려면 Octane 서버를 재시작해야 합니다.

<a name="reloading-the-workers"></a>
### 작업자 재로드

`octane:reload` 명령을 사용하여 Octane 서버의 애플리케이션 작업자를 정상적으로 재시작할 수 있습니다. 일반적으로 이는 새로 배포된 코드가 메모리에 로드되고 이후 요청에 사용되도록 배포 후에 수행해야 합니다.

```shell
php artisan octane:reload
```



<a name="stopping-the-server"></a>
### 서버 중지

`octane:stop` Artisan 명령어를 사용하여 Octane 서버를 중지할 수 있습니다:

```shell
php artisan octane:stop
```



<a name="checking-the-server-status"></a>
#### 서버 상태 확인

`octane:status` Artisan 명령어를 사용하여 Octane 서버의 현재 상태를 확인할 수 있습니다:

```shell
php artisan octane:status
```



<a name="dependency-injection-and-octane"></a>
## Dependency Injection and Octane

Since Octane boots your application once and keeps it in memory while serving requests, there are a few caveats you should consider while building your application. For example, the `register` and `boot` methods of your application's service providers will only be executed once when the request worker initially boots. On subsequent requests, the same application instance will be reused.

In light of this, you should take special care when injecting the application service container or request into any object's constructor. By doing so, that object may have a stale version of the container or request on subsequent requests.

Octane will automatically handle resetting any first-party framework state between requests. However, Octane does not always know how to reset the global state created by your application. Therefore, you should be aware of how to build your application in a way that is Octane friendly. Below, we will discuss the most common situations that may cause problems while using Octane.

<a name="container-injection"></a>
### Container Injection

In general, you should avoid injecting the application service container or HTTP request instance into the constructors of other objects. For example, the following binding injects the entire application service container into an object that is bound as a singleton:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app);
    });
}
```



이 예제에서, 애플리케이션 부트 과정 중에 `Service` 인스턴스가 해결되면, 컨테이너가 서비스에 주입되고 그 동일한 컨테이너가 이후 요청에서 `Service` 인스턴스에 의해 보관됩니다. 이는 특정 애플리케이션에서는 문제가 되지 않을 수 있지만, 부트 사이클 이후나 이후 요청에 의해 추가된 바인딩이 컨테이너에 예상치 못하게 누락되는 상황을 초래할 수 있습니다.

우회 방법으로는, 바인딩을 싱글톤으로 등록하는 것을 중지하거나, 항상 현재 컨테이너 인스턴스를 해결하는 컨테이너 해결 클로저를 서비스에 주입할 수 있습니다:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app);
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance());
});
```



글로벌 `app` 헬퍼와 `Container::getInstance()` 메서드는 항상 애플리케이션 컨테이너의 최신 버전을 반환합니다.

<a name="request-injection"></a>
### 요청 주입

일반적으로 다른 객체의 생성자에 애플리케이션 서비스 컨테이너나 HTTP 요청 인스턴스를 주입하는 것은 피해야 합니다. 예를 들어, 다음 바인딩은 전체 요청 인스턴스를 싱글톤으로 바인딩된 객체에 주입합니다:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app['request']);
    });
}
```



이 예제에서 `Service` 인스턴스가 애플리케이션 부팅 과정에서 해결되면, HTTP 요청이 서비스에 주입되고 이후 요청에서 동일한 요청이 `Service` 인스턴스에 의해 유지됩니다. 따라서 모든 헤더, 입력 및 쿼리 문자열 데이터뿐만 아니라 다른 모든 요청 데이터가 잘못될 것입니다.

우회 방법으로는 바인딩을 싱글톤으로 등록하는 것을 중단하거나, 항상 현재 요청 인스턴스를 해결하는 요청 해결자 클로저를 서비스에 주입할 수도 있습니다. 또는 가장 권장되는 방법은 단순히 객체가 필요로 하는 특정 요청 정보를 실행 시간에 객체의 메서드 중 하나에 전달하는 것입니다:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app['request']);
});

$this->app->singleton(Service::class, function (Application $app) {
    return new Service(fn () => $app['request']);
});

// Or...

$service->method($request->input('name'));
```



글로벌 `request` 헬퍼는 항상 애플리케이션이 현재 처리 중인 요청을 반환하므로 애플리케이션 내에서 사용하기에 안전합니다.

> [!WARNING]
> 컨트롤러 메서드와 라우트 클로저에서 `Illuminate\Http\Request` 인스턴스를 타입 힌트로 사용하는 것은 허용됩니다.

<a name="configuration-repository-injection"></a>
### 구성 저장소 주입

일반적으로, 구성 저장소 인스턴스를 다른 객체의 생성자에 주입하는 것은 피해야 합니다. 예를 들어, 다음 바인딩은 구성 저장소를 싱글톤으로 바인딩된 객체에 주입합니다:

```php
use App\Service;
use Illuminate\Contracts\Foundation\Application;

/**
 * Register any application services.
 */
public function register(): void
{
    $this->app->singleton(Service::class, function (Application $app) {
        return new Service($app->make('config'));
    });
}
```



이 예제에서, 요청 간에 구성 값이 변경되면, 그 서비스는 원래 리포지토리 인스턴스에 의존하고 있기 때문에 새로운 값에 접근할 수 없습니다.

임시 해결책으로, 바인딩을 싱글톤으로 등록하는 것을 중단하거나, 클래스에 구성 리포지토리 해결자 클로저를 주입할 수 있습니다:

```php
use App\Service;
use Illuminate\Container\Container;
use Illuminate\Contracts\Foundation\Application;

$this->app->bind(Service::class, function (Application $app) {
    return new Service($app->make('config'));
});

$this->app->singleton(Service::class, function () {
    return new Service(fn () => Container::getInstance()->make('config'));
});
```



글로벌 `config`는 항상 구성 저장소의 최신 버전을 반환하므로 애플리케이션 내에서 안전하게 사용할 수 있습니다.

<a name="managing-memory-leaks"></a>
### 메모리 누수 관리

기억하세요, Octane은 요청 간에 애플리케이션을 메모리에 유지합니다; 따라서 정적으로 유지되는 배열에 데이터를 추가하면 메모리 누수가 발생합니다. 예를 들어, 다음 컨트롤러는 각 요청이 정적 `$data` 배열에 데이터를 계속 추가하므로 메모리 누수가 발생합니다:

```php
use App\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

/**
 * Handle an incoming request.
 */
public function index(Request $request): array
{
    Service::$data[] = Str::random(10);

    return [
        // ...
    ];
}
```



응용 프로그램을 개발하는 동안 이러한 유형의 메모리 누수를 생성하지 않도록 특별히 주의해야 합니다. 로컬 개발 중에 응용 프로그램의 메모리 사용량을 모니터링하여 새로운 메모리 누수가 발생하지 않도록 하는 것이 권장됩니다.

<a name="concurrent-tasks"></a>
## 동시 작업

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때 경량 백그라운드 작업을 통해 작업을 동시에 실행할 수 있습니다. 이는 Octane의 `concurrently` 메서드를 사용하여 수행할 수 있습니다. 이 메서드는 PHP 배열 구조 분해와 결합하여 각 작업의 결과를 가져올 수 있습니다:

```php
use App\Models\User;
use App\Models\Server;
use Laravel\Octane\Facades\Octane;

[$users, $servers] = Octane::concurrently([
    fn () => User::all(),
    fn () => Server::all(),
]);
```



Octane에서 처리되는 동시 작업은 Swoole의 '작업 워커(task workers)'를 사용하며, 들어오는 요청과 완전히 다른 프로세스 내에서 실행됩니다. 동시 작업을 처리할 수 있는 워커 수는 `octane:start` 명령의 `--task-workers` 지시문에 의해 결정됩니다:

```shell
php artisan octane:start --workers=4 --task-workers=6
```



`concurrently` 메서드를 호출할 때, Swoole의 작업 시스템에서 부과하는 제한으로 인해 1024개 이상의 작업을 제공하지 않아야 합니다.

<a name="ticks-and-intervals"></a>
## 틱과 간격

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 지정된 초마다 실행될 "틱" 작업을 등록할 수 있습니다. `tick` 메서드를 통해 틱 콜백을 등록할 수 있습니다. `tick` 메서드에 제공되는 첫 번째 인자는 틱커의 이름을 나타내는 문자열이어야 합니다. 두 번째 인자는 지정된 간격마다 호출될 호출 가능한 함수여야 합니다.

이 예제에서는 10초마다 호출될 클로저를 등록할 것입니다. 일반적으로 `tick` 메서드는 애플리케이션의 서비스 제공자 중 하나의 `boot` 메서드 내에서 호출해야 합니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10);
```



`immediate` 방법을 사용하면 Octane 서버가 처음 부팅될 때와 이후 매 N초마다 Octane에 즉시 틱 콜백을 호출하도록 지시할 수 있습니다:

```php
Octane::tick('simple-ticker', fn () => ray('Ticking...'))
    ->seconds(10)
    ->immediate();
```



<a name="the-octane-cache"></a>
## 옥테인 캐시

> [!WARNING]
> 이 기능을 사용하려면 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때 옥테인 캐시 드라이버를 활용할 수 있으며, 이 드라이버는 초당 최대 200만 번의 읽기 및 쓰기 속도를 제공합니다. 따라서 캐싱 계층에서 극도의 읽기/쓰기 속도가 필요한 애플리케이션에 이 캐시 드라이버는 훌륭한 선택입니다.

이 캐시 드라이버는 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)에 의해 구동됩니다. 캐시에 저장된 모든 데이터는 서버의 모든 워커에서 사용할 수 있습니다. 그러나 서버가 재시작되면 캐시된 데이터는 삭제됩니다.

```php
Cache::store('octane')->put('framework', 'Laravel', 30);
```



> [!NOTE]
> Octane 캐시에 허용되는 최대 항목 수는 애플리케이션의 `octane` 구성 파일에서 정의할 수 있습니다.

<a name="cache-intervals"></a>
### 캐시 간격

Laravel의 캐시 시스템이 제공하는 일반적인 방법 외에도, Octane 캐시 드라이버는 간격 기반 캐시를 제공합니다. 이러한 캐시는 지정된 간격마다 자동으로 새로고침되며, 애플리케이션의 서비스 제공자 중 하나의 `boot` 메서드 내에 등록되어야 합니다. 예를 들어, 다음 캐시는 5초마다 새로고침됩니다:

```php
use Illuminate\Support\Str;

Cache::store('octane')->interval('random', function () {
    return Str::random(10);
}, seconds: 5);
```



<a name="tables"></a>
## 테이블

> [!WARNING]
> 이 기능은 [Swoole](#swoole)이 필요합니다.

Swoole을 사용할 때, 임의의 [Swoole 테이블](https://www.swoole.co.uk/docs/modules/swoole-table)을 정의하고 상호작용할 수 있습니다. Swoole 테이블은 매우 높은 성능 처리를 제공하며, 이 테이블의 데이터는 서버의 모든 워커가 접근할 수 있습니다. 그러나 서버가 재시작되면 이 데이터는 사라집니다.

테이블은 애플리케이션의 `octane` 설정 파일의 `tables` 구성 배열 내에서 정의해야 합니다. 최대 1000개의 행을 허용하는 예제 테이블이 이미 설정되어 있습니다. 문자열 컬럼의 최대 크기는 아래와 같이 컬럼 타입 뒤에 컬럼 크기를 지정하여 구성할 수 있습니다:

```php
'tables' => [
    'example:1000' => [
        'name' => 'string:1000',
        'votes' => 'int',
    ],
],
```



테이블에 접근하려면 `Octane::table` 메서드를 사용할 수 있습니다:

```php
use Laravel\Octane\Facades\Octane;

Octane::table('example')->set('uuid', [
    'name' => 'Nuno Maduro',
    'votes' => 1000,
]);

return Octane::table('example')->get('uuid');
```

> [!WARNING]
> Swoole 테이블에서 지원하는 열 유형은 `string`, `int` 및 `float`입니다.
{% endraw %}
