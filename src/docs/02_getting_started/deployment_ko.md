---
layout: docs
title: "배포"
---

{% raw %}
# 배포

- [소개](#introduction)
- [서버 요구사항](#server-requirements)
- [서버 구성](#server-configuration)
    - [엔진엑스](#nginx)
    - [프랑켄PHP](#frankenphp)
    - [디렉터리 권한](#directory-permissions)
- [최적화](#optimization)
    - [캐싱 구성](#optimizing-configuration-loading)
    - [캐싱 이벤트](#caching-events)
    - [캐싱 경로](#optimizing-route-loading)
    - [캐싱 뷰](#optimizing-view-loading)
- [리로딩 서비스](#reloading-services)
- [디버그 모드](#debug-mode)
- [헬스 루트](#the-health-route)
- [Laravel Cloud 또는 Forge로 배포](#deploying-with-cloud-or-forge)

<a name="introduction"></a>
## 소개

Laravel 애플리케이션을 프로덕션 환경에 배포할 준비가 되면 애플리케이션이 최대한 효율적으로 실행되도록 하기 위해 수행할 수 있는 몇 가지 중요한 작업이 있습니다. 이 문서에서는 Laravel 애플리케이션이 올바르게 배포되었는지 확인하기 위한 몇 가지 훌륭한 시작점을 다룰 것입니다.

<a name="server-requirements"></a>
## 서버 요구 사항

Laravel 프레임워크에는 몇 가지 시스템 요구 사항이 있습니다. 웹 서버에 다음과 같은 최소 PHP 버전 및 확장이 있는지 확인해야 합니다.

<div class="content-list" markdown="1">

- PHP >= 8.3
- Ctype PHP 확장
- cURL PHP 확장
- DOM PHP 확장
- Fileinfo PHP 확장
- 필터 PHP 확장
- 해시 PHP 확장
- Mbstring PHP 확장
- OpenSSL PHP 확장
- PCRE PHP 확장
- PDO PHP 확장
- 세션 PHP 확장
- 토크나이저 PHP 확장
- XML PHP 확장

</div>

<a name="server-configuration"></a>
## 서버 구성

<a name="nginx"></a>
### 엔진엑스

Nginx를 실행하는 서버에 애플리케이션을 배포하는 경우 웹 서버 구성을 위한 시작점으로 다음 구성 파일을 사용할 수 있습니다. 대부분의 경우 이 파일은 서버 구성에 따라 사용자 정의해야 합니다. **서버 관리에 도움이 필요하시면 [Laravel Cloud](https://cloud.laravel.com)와 같은 완전관리형 Laravel 플랫폼 사용을 고려해 보세요.**

아래 구성과 같이 웹 서버가 모든 요청을 애플리케이션의 `public/index.php` 파일로 전달하는지 확인하세요. `index.php` 파일을 프로젝트 루트로 이동하려고 시도해서는 안 됩니다. 프로젝트 루트에서 애플리케이션을 제공하면 많은 민감한 구성 파일이 공개 인터넷에 노출되기 때문입니다.

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com;
    root /srv/example.com/public;

    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-Content-Type-Options "nosniff";

    index index.php;

    charset utf-8;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location = /favicon.ico { access_log off; log_not_found off; }
    location = /robots.txt  { access_log off; log_not_found off; }

    error_page 404 /index.php;

    location ~ ^/index\.php(/|$) {
        fastcgi_pass unix:/var/run/php/php8.3-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $realpath_root$fastcgi_script_name;
        include fastcgi_params;
        fastcgi_buffer_size 32k;
        fastcgi_buffers 8 32k;
        fastcgi_busy_buffers_size 64k;
        fastcgi_hide_header X-Powered-By;
    }

    location ~ /\.(?!well-known).* {
        deny all;
    }
}

```

<a name="frankenphp"></a>
### 프랑켄PHP

[FrankenPHP](https://frankenphp.dev/)는 Laravel 애플리케이션을 제공하는 데에도 사용될 수 있습니다. FrankenPHP는 Go로 작성된 최신 PHP 애플리케이션 서버입니다. FrankenPHP를 사용하여 Laravel PHP 애플리케이션을 제공하려면 `php-server` 명령을 호출하기만 하면 됩니다.

```shell
frankenphp php-server -r public/

```

[Laravel Octane](/docs/{{version}}/octane) 통합, HTTP/3, 최신 압축 또는 Laravel 애플리케이션을 독립 실행형 바이너리로 패키징하는 기능과 같이 FrankenPHP에서 지원하는 보다 강력한 기능을 활용하려면 FrankenPHP의 [Laravel 문서](https://frankenphp.dev/docs/laravel/)를 참조하세요.

<a name="directory-permissions"></a>
### 디렉토리 권한

Laravel은 `bootstrap/cache` 및 `storage` 디렉토리에 작성해야 하므로 웹 서버 프로세스 소유자에게 이러한 디렉토리에 대한 쓰기 권한이 있는지 확인해야 합니다.

<a name="optimization"></a>
## 최적화

애플리케이션을 프로덕션에 배포할 때 구성, 이벤트, 경로 및 보기를 포함하여 캐시해야 하는 다양한 파일이 있습니다. Laravel은 이러한 모든 파일을 캐시하는 편리한 단일 `optimize` Artisan 명령을 제공합니다. 이 명령은 일반적으로 애플리케이션 배포 프로세스의 일부로 호출되어야 합니다.

```shell
php artisan optimize

```

`optimize:clear` 방법은 `optimize` 명령으로 생성된 모든 캐시 파일과 기본 캐시 드라이버의 모든 키를 제거하는 데 사용할 수 있습니다.

```shell
php artisan optimize:clear

```

다음 문서에서는 `optimize` 명령으로 실행되는 각 세부적인 최적화 명령에 대해 설명합니다.

<a name="optimizing-configuration-loading"></a>
### 캐싱 구성

애플리케이션을 프로덕션에 배포할 때 배포 프로세스 중에 `config:cache` Artisan 명령을 실행해야 합니다.

```shell
php artisan config:cache

```

이 명령은 Laravel의 모든 구성 파일을 하나의 캐시된 파일로 결합하여 구성 값을 로드할 때 프레임워크가 파일 시스템으로 이동해야 하는 횟수를 크게 줄입니다.

> [!WARNING]
> 배포 프로세스 중에 `config:cache` 명령을 실행하는 경우 구성 파일 내에서만 `env` 기능을 호출하고 있는지 확인해야 합니다. 구성이 캐시되면 `.env` 파일은 로드되지 않으며 `.env` 변수에 대한 `env` 함수에 대한 모든 호출은 `null`를 반환합니다.

<a name="caching-events"></a>
### 캐싱 이벤트

배포 프로세스 중에 애플리케이션의 자동 검색 이벤트를 리스너 매핑에 캐시해야 합니다. 이는 배포 중에 `event:cache` Artisan 명령을 호출하여 수행할 수 있습니다.

```shell
php artisan event:cache

```

<a name="optimizing-route-loading"></a>
### 캐싱 경로

경로가 많은 대규모 애플리케이션을 구축하는 경우 배포 프로세스 중에 `route:cache` Artisan 명령을 실행하고 있는지 확인해야 합니다.

```shell
php artisan route:cache

```

이 명령은 모든 경로 등록을 캐시된 파일 내의 단일 메서드 호출로 줄여 수백 개의 경로를 등록할 때 경로 등록 성능을 향상시킵니다.

<a name="optimizing-view-loading"></a>
### 캐싱 뷰

애플리케이션을 프로덕션에 배포할 때 배포 프로세스 중에 `view:cache` Artisan 명령을 실행해야 합니다.

```shell
php artisan view:cache

```

이 명령은 요청 시 컴파일되지 않도록 모든 블레이드 보기를 사전 컴파일하여 보기를 반환하는 각 요청의 성능을 향상시킵니다.

<a name="reloading-services"></a>
## 서비스 다시 로드

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com)에 배포할 때 모든 서비스의 정상적인 재로드가 자동으로 처리되므로 `reload` 명령을 사용할 필요가 없습니다.

새 버전의 애플리케이션을 배포한 후 새 코드를 사용하려면 대기열 작업자, Laravel Reverb 또는 Laravel Octane과 같은 장기 실행 서비스를 다시 로드하거나 다시 시작해야 합니다. Laravel은 이러한 서비스를 종료하는 단일 `reload` Artisan 명령을 제공합니다:

```shell
php artisan reload

```

[Laravel Cloud](https://cloud.laravel.com)를 사용하지 않는 경우 다시 로드 가능한 프로세스가 종료되는 시점을 감지하고 자동으로 다시 시작할 수 있는 프로세스 모니터를 수동으로 구성해야 합니다.

<a name="debug-mode"></a>
## 디버그 모드

`config/app.php` 구성 파일의 디버그 옵션은 오류에 대한 정보가 실제로 사용자에게 표시되는 정도를 결정합니다. 기본적으로 이 옵션은 애플리케이션의 `.env` 파일에 저장된 `APP_DEBUG` 환경 변수의 값을 따르도록 설정됩니다.

> [!WARNING]
> **프로덕션 환경에서 이 값은 항상 `false`여야 합니다. 프로덕션 환경에서 `APP_DEBUG` 변수가 `true`로 설정된 경우 민감한 구성 값이 애플리케이션의 최종 사용자에게 노출될 위험이 있습니다.**

<a name="the-health-route"></a>
## 건강 경로

Laravel에는 애플리케이션 상태를 모니터링하는 데 사용할 수 있는 상태 확인 경로가 내장되어 있습니다. 프로덕션에서 이 경로는 가동 시간 모니터, 로드 밸런서 또는 Kubernetes와 같은 오케스트레이션 시스템에 애플리케이션 상태를 보고하는 데 사용될 수 있습니다.

기본적으로 상태 확인 경로는 `/up`에서 제공되며 애플리케이션이 예외 없이 부팅되면 200 HTTP 응답을 반환합니다. 그렇지 않으면 500 HTTP 응답이 반환됩니다. 애플리케이션의 `bootstrap/app` 파일에서 이 경로에 대한 URI를 구성할 수 있습니다.

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    commands: __DIR__.'/../routes/console.php',
    health: '/up', // [tl! remove]
    health: '/status', // [tl! add]
)

```

이 경로에 대한 HTTP 요청이 이루어지면 Laravel은 `Illuminate\Foundation\Events\DiagnosingHealth` 이벤트도 전달하여 애플리케이션과 관련된 추가 상태 확인을 수행할 수 있습니다. 이 이벤트에 대한 [리스너](/docs/{{version}}/events) 내에서 애플리케이션의 데이터베이스 또는 캐시 상태를 확인할 수 있습니다. 애플리케이션에서 문제를 발견하면 리스너에서 예외를 발생시키기만 하면 됩니다.

<a name="deploying-with-cloud-or-forge"></a>
## Laravel Cloud 또는 Forge를 사용하여 배포

<a name="laravel-cloud"></a>
#### 라라벨 클라우드

Laravel에 맞게 조정된 완전 관리형 자동 확장 배포 플랫폼을 원한다면 [Laravel Cloud](https://cloud.laravel.com)를 확인하세요. Laravel Cloud는 관리형 컴퓨팅, 데이터베이스, 캐시 및 객체 스토리지를 제공하는 Laravel을 위한 강력한 배포 플랫폼입니다.

클라우드에서 Laravel 애플리케이션을 실행하고 확장 가능한 단순성에 빠져보세요. Laravel Cloud는 Laravel 제작자에 의해 프레임워크와 원활하게 작동하도록 미세 조정되었으므로 Laravel 애플리케이션을 예전과 똑같이 계속 작성할 수 있습니다.

<a name="laravel-forge"></a>
#### 라라벨 포지

자신의 서버를 관리하고 싶지만 강력한 Laravel 애플리케이션을 실행하는 데 필요한 다양한 서비스를 모두 구성하는 것이 불편하다면 [Laravel Forge](https://forge.laravel.com)는 Laravel 애플리케이션을 위한 VPS 서버 관리 플랫폼입니다.

Laravel Forge는 DigitalOcean, Linode, AWS 등과 같은 다양한 인프라 제공업체에 서버를 생성할 수 있습니다. 또한 Forge는 Nginx, MySQL, Redis, Memcached, Beanstalk 등과 같은 강력한 Laravel 애플리케이션을 구축하는 데 필요한 모든 도구를 설치하고 관리합니다.
{% endraw %}
