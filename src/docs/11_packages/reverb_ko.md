---
layout: docs
title: "라라벨 리버브"
---

{% raw %}
# 라라벨 리버브

- [소개](#introduction)
- [설치](#installation)
- [설정](#configuration)
    - [애플리케이션 자격 증명](#application-credentials)
    - [허용된 출처](#allowed-origins)
    - [추가 애플리케이션](#additional-applications)
    - [SSL](#ssl)
- [서버 실행](#running-server)
    - [디버깅](#debugging)
    - [재시작](#restarting)
- [모니터링](#monitoring)
- [프로덕션에서 리버브 실행](#production)
    - [열린 파일](#open-files)
    - [이벤트 루프](#event-loop)
    - [웹 서버](#web-server)
    - [포트](#ports)
    - [프로세스 관리](#process-management)
    - [스케일링](#scaling)
- [이벤트](#events)

<a name="introduction"></a>
## 소개

[라라벨 리버브](https://github.com/laravel/reverb)는 라라벨 애플리케이션에 초고속 및 확장 가능한 실시간 웹소켓 통신을 직접 제공하고, 라라벨의 기존 [이벤트 브로드캐스팅 도구](/docs/{{version}}/broadcasting)와 원활하게 통합됩니다.

<a name="installation"></a>
## 설치

다음 `install:broadcasting` Artisan 명령어를 사용하여 리버브를 설치할 수 있습니다:

```shell
php artisan install:broadcasting

```

<a name="configuration"></a>
## 구성

무대 뒤에서, `install:broadcasting` Artisan 명령은 `reverb:install` 명령을 실행하며, 이는 합리적인 기본 구성 옵션 세트와 함께 Reverb를 설치합니다. 구성 변경을 원하시면 Reverb의 환경 변수를 업데이트하거나 `config/reverb.php` 구성 파일을 업데이트하여 변경할 수 있습니다.

<a name="application-credentials"></a>
### 애플리케이션 자격 증명

Reverb와 연결을 설정하기 위해 클라이언트와 서버 간에 Reverb "애플리케이션" 자격 증명 세트를 교환해야 합니다. 이러한 자격 증명은 서버에서 구성되며 클라이언트의 요청을 검증하는 데 사용됩니다. 다음 환경 변수를 사용하여 이러한 자격 증명을 정의할 수 있습니다:

```ini
REVERB_APP_ID=my-app-id
REVERB_APP_KEY=my-app-key
REVERB_APP_SECRET=my-app-secret

```

<a name="allowed-origins"></a>
### 허용된 출처

클라이언트 요청이 발생할 수 있는 출처를 정의하려면 `config/reverb.php` 구성 파일의 `apps` 섹션 내 `allowed_origins` 구성 값을 업데이트하면 됩니다. 허용된 출처에 나열되지 않은 출처에서 오는 모든 요청은 거부됩니다. `*`를 사용하여 모든 출처를 허용할 수도 있습니다:

```php
'apps' => [
    [
        'app_id' => 'my-app-id',
        'allowed_origins' => ['laravel.com'],
        // ...
    ]
]

```

<a name="additional-applications"></a>
### 추가 응용 프로그램

일반적으로 Reverb는 설치된 애플리케이션을 위해 WebSocket 서버를 제공합니다. 그러나 단일 Reverb 설치로 여러 애플리케이션을 제공하는 것도 가능합니다.

예를 들어, Reverb를 통해 여러 애플리케이션에 WebSocket 연결을 제공하는 단일 Laravel 애플리케이션을 유지하고자 할 수 있습니다. 이는 애플리케이션의 `config/reverb.php` 구성 파일에 여러 `apps`를 정의하여 달성할 수 있습니다:

```php
'apps' => [
    [
        'app_id' => 'my-app-one',
        // ...
    ],
    [
        'app_id' => 'my-app-two',
        // ...
    ],
],

```

<a name="ssl"></a>
### SSL

대부분의 경우, 보안 WebSocket 연결은 요청이 Reverb 서버로 프록시되기 전에 상위 웹 서버(Nginx 등)에 의해 처리됩니다.

그러나 로컬 개발 중과 같이 경우에 따라 Reverb 서버가 보안 연결을 직접 처리하는 것이 유용할 수 있습니다. [Laravel Herd](https://herd.laravel.com)의 보안 사이트 기능을 사용하거나 [Laravel Valet](/docs/{{version}}/valet)을 사용하며 애플리케이션에 대해 [secure 명령어](/docs/{{version}}/valet#securing-sites)를 실행한 경우, 사이트에 대해 생성된 Herd / Valet 인증서를 사용하여 Reverb 연결을 보안할 수 있습니다. 이를 위해, `REVERB_HOST` 환경 변수를 사이트 호스트 이름으로 설정하거나 Reverb 서버를 시작할 때 hostname 옵션을 명시적으로 전달하십시오.

```shell
php artisan reverb:start --host="0.0.0.0" --port=8080 --hostname="laravel.test"

```

Herd와 Valet 도메인이 `localhost`로 해석되므로, 위 명령을 실행하면 Reverb 서버에 `wss://laravel.test:8080`에서 안전한 WebSocket 프로토콜(`wss`)을 통해 접근할 수 있습니다.

또한 애플리케이션의 `config/reverb.php` 구성 파일에서 `tls` 옵션을 정의하여 인증서를 수동으로 선택할 수도 있습니다. `tls` 옵션 배열 내에서 [PHP의 SSL 컨텍스트 옵션](https://www.php.net/manual/en/context.ssl.php)에서 지원하는 모든 옵션을 제공할 수 있습니다.

```php
'options' => [
    'tls' => [
        'local_cert' => '/path/to/cert.pem'
    ],
],

```

<a name="running-server"></a>
## 서버 실행

Reverb 서버는 `reverb:start` Artisan 명령어를 사용하여 시작할 수 있습니다:

```shell
php artisan reverb:start

```

기본적으로 Reverb 서버는 `0.0.0.0:8080`에서 시작되며, 모든 네트워크 인터페이스에서 접근할 수 있습니다.

서버를 시작할 때 `--host` 및 `--port` 옵션을 통해 사용자 지정 호스트나 포트를 지정해야 하는 경우 다음과 같이 할 수 있습니다:

```shell
php artisan reverb:start --host=127.0.0.1 --port=9000

```

또는 애플리케이션의 `.env` 구성 파일에서 `REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT` 환경 변수를 정의할 수 있습니다.

`REVERB_SERVER_HOST` 및 `REVERB_SERVER_PORT` 환경 변수는 `REVERB_HOST` 및 `REVERB_PORT`와 혼동하지 않아야 합니다. 전자는 Reverb 서버 자체를 실행할 호스트와 포트를 지정하는 반면, 후자는 Laravel에게 브로드캐스트 메시지를 보낼 위치를 지시합니다. 예를 들어, 운영 환경에서는 공개 Reverb 호스트 이름의 요청을 `443` 포트에서 `0.0.0.0:8080`에서 작동 중인 Reverb 서버로 라우팅할 수 있습니다. 이 시나리오에서 환경 변수는 다음과 같이 정의됩니다:

```ini
REVERB_SERVER_HOST=0.0.0.0
REVERB_SERVER_PORT=8080

REVERB_HOST=ws.laravel.com
REVERB_PORT=443

```

<a name="debugging"></a>
### 디버깅

성능을 향상시키기 위해, Reverb는 기본적으로 디버그 정보를 출력하지 않습니다. Reverb 서버를 통해 흐르는 데이터 스트림을 보고 싶다면, `reverb:start` 명령어에 `--debug` 옵션을 제공할 수 있습니다:

```shell
php artisan reverb:start --debug

```

<a name="restarting"></a>
### 재시작

Reverb는 장기간 실행되는 프로세스이므로, `reverb:restart` Artisan 명령을 통해 서버를 재시작하지 않으면 코드 변경 사항이 반영되지 않습니다.

`reverb:restart` 명령은 서버를 중지하기 전에 모든 연결이 정상적으로 종료되도록 합니다. Supervisor와 같은 프로세스 관리자를 사용하여 Reverb를 실행하는 경우, 모든 연결이 종료된 후 프로세스 관리자가 서버를 자동으로 재시작합니다:

```shell
php artisan reverb:restart

```

<a name="monitoring"></a>
## 모니터링

리버브는 [Laravel Pulse](/docs/{{version}}/pulse)와의 통합을 통해 모니터링할 수 있습니다. 리버브의 Pulse 통합을 활성화하면 서버에서 처리되는 연결 수와 메시지를 추적할 수 있습니다.

통합을 활성화하려면 먼저 [Pulse를 설치](/docs/{{version}}/pulse#installation)했는지 확인해야 합니다. 그런 다음, 리버브의 어떤 레코더든 애플리케이션의 `config/pulse.php` 구성 파일에 추가합니다:

```php
use Laravel\Reverb\Pulse\Recorders\ReverbConnections;
use Laravel\Reverb\Pulse\Recorders\ReverbMessages;

'recorders' => [
    ReverbConnections::class => [
        'sample_rate' => 1,
    ],

    ReverbMessages::class => [
        'sample_rate' => 1,
    ],

    // ...
],

```

다음으로, 각 레코더에 대한 Pulse 카드를 당신의 [Pulse 대시보드](/docs/{{version}}/pulse#dashboard-customization)에 추가하세요:

```blade
<x-pulse>
    <livewire:reverb.connections cols="full" />
    <livewire:reverb.messages cols="full" />
    ...
</x-pulse>

```

연결 활동은 주기적으로 새로운 업데이트를 폴링하여 기록됩니다. Pulse 대시보드에서 이 정보가 올바르게 렌더링되도록 하려면 Reverb 서버에서 `pulse:check` 데몬을 실행해야 합니다. Reverb 를 [수평 확장](#scaling) 구성에서 실행하는 경우 서버 중 하나에서만 이 데몬을 실행해야 합ニ다。

<a name="production"></a>
## 프로덕션에서의 실행 리버브

WebSocket 서버의 장기 실행 특성으로 인해 Reverb 서버가 서버에서 사용 가능한 리소스에 대한 최적의 연결 수를 효과적으로 처리할 수 있도록 서버 및 호스팅 환경을 최적화해야 할 수 있습니다。

> [!NOTE]
> [Laravel Cloud](https://cloud.laravel.com) 는 Laravel Reverb 클러스터로 구동되는 완전관리형 WebSocket 인프라를 제공하므로， 인프라를 관리하지 않고도 Reverb 지원 애플리케이션을 확장하고 배포할 수 있습니다。

<a name="open-files"></a>
### 파일 열기

각 WebSocket 연결은 클라이언트 또는 서버가 연결을 끊을 때까지 메모리에 보관됩니다. Unix 및 Unix 와 유사한 환경에서는 각 연결이 파일로 표시됩니다. 그러나 운영 체제 및 애플리케이션 수준에서 허용되는 열린 파일의 수에는 종종 제한이 있습니다。

<a name="operating-system"></a>
#### 운영체제

Unix 기반 운영 체제에서는 `ulimit` 명령을 사용하여 허용되는 열린 파일 수를 결정할 수 있습니다：

```shell
ulimit -n

```

이 명령은 서로 다른 사용자에게 허용된 열린 파일 한도를 표시합니다. `/etc/security/limits.conf` 파일을 편집하여 이러한 값을 업데이트할 수 있습니다. 예를 들어, `forge` 사용자의 최대 열린 파일 수를 10,000으로 업데이트하면 다음과 같이 나타납니다:

```ini
# /etc/security/limits.conf
forge        soft  nofile  10000
forge        hard  nofile  10000

```

<a name="event-loop"></a>
### 이벤트 루프

속으로, Reverb는 서버에서 WebSocket 연결을 관리하기 위해 ReactPHP 이벤트 루프를 사용합니다. 기본적으로 이 이벤트 루프는 추가 확장이 필요 없는 `stream_select`에 의해 구동됩니다. 그러나 `stream_select`는 일반적으로 열 수 있는 파일이 1,024개로 제한됩니다. 따라서 1,000개 이상의 동시 연결을 처리할 계획이라면 동일한 제한을 받지 않는 대체 이벤트 루프를 사용해야 합니다.

Reverb는 사용 가능할 때 자동으로 `ext-uv` 구동 루프로 전환됩니다. 이 PHP 확장은 PECL을 통해 설치할 수 있습니다:

```shell
pecl install uv

```

<a name="web-server"></a>
### 웹 서버

대부분의 경우, Reverb는 서버에서 외부에 노출되지 않은 포트에서 실행됩니다. 따라서 Reverb로 트래픽을 라우팅하기 위해서는 리버스 프록시를 설정해야 합니다. Reverb가 호스트 `0.0.0.0`와 포트 `8080`에서 실행 중이고, 서버가 Nginx 웹 서버를 이용하고 있다고 가정하면, 다음 Nginx 사이트 설정을 사용하여 Reverb 서버에 대한 리버스 프록시를 정의할 수 있습니다:

```nginx
server {
    ...

    location / {
        proxy_http_version 1.1;
        proxy_set_header Host $http_host;
        proxy_set_header Scheme $scheme;
        proxy_set_header SERVER_PORT $server_port;
        proxy_set_header REMOTE_ADDR $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";

        proxy_pass http://0.0.0.0:8080;
    }

    ...
}

```

> [!WARNING]
> Reverb는 `/app`에서 WebSocket 연결을 수신하고 `/apps`에서 API 요청을 처리합니다. Reverb 요청을 처리하는 웹 서버가 이 두 URI를 모두 제공할 수 있는지 확인해야 합니다. 서버 관리를 위해 [Laravel Forge](https://forge.laravel.com)를 사용하는 경우 기본적으로 Reverb 서버가 올바르게 구성됩니다.

일반적으로 웹 서버는 서버 과부하를 방지하기 위해 허용되는 연결 수를 제한하도록 구성됩니다. Nginx 웹 서버에서 허용 연결 수를 10,000으로 늘리려면 `nginx.conf` 파일의 `worker_rlimit_nofile` 및 `worker_connections` 값을 업데이트해야 합니다:

```nginx
user forge;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
worker_rlimit_nofile 10000;

events {
  worker_connections 10000;
  multi_accept on;
}

```

위의 구성은 프로세스당 최대 10,000개의 Nginx 워커가 생성될 수 있도록 허용합니다. 또한, 이 구성은 Nginx의 열 수 있는 파일 제한을 10,000으로 설정합니다.

<a name="ports"></a>
### 포트

유닉스 기반 운영 체제는 일반적으로 서버에서 열 수 있는 포트 수를 제한합니다. 다음 명령을 통해 현재 허용된 범위를 확인할 수 있습니다:

```shell
cat /proc/sys/net/ipv4/ip_local_port_range
# 32768	60999

```

위 출력은 서버가 최대 28,231 (60,999 - 32,768)개의 연결을 처리할 수 있음을 보여줍니다. 각 연결에는 사용 가능한 포트가 필요하기 때문입니다. 허용된 연결 수를 늘리기 위해 [수평 확장](#scaling)을 권장하지만, 서버의 `/etc/sysctl.conf` 구성 파일에서 허용된 포트 범위를 업데이트하여 사용 가능한 열린 포트 수를 늘릴 수 있습니다.

<a name="process-management"></a>
### 프로세스 관리

대부분의 경우 Reverb 서버가 지속적으로 실행되도록 Supervisor와 같은 프로세스 관리자를 사용하는 것이 좋습니다. Reverb를 실행하기 위해 Supervisor를 사용하는 경우, Reverb 서버에 대한 연결을 처리하는 데 필요한 파일을 Supervisor가 열 수 있도록 서버의 `supervisor.conf` 파일의 `minfds` 설정을 업데이트해야 합니다.

```ini
[supervisord]
...
minfds=10000

```

<a name="scaling"></a>
### 확장

단일 서버가 허용하는 것보다 더 많은 연결을 처리해야 하는 경우, Reverb 서버를 수평으로 확장할 수 있습니다. Redis의 발행/구독 기능을 활용하여 Reverb는 여러 서버에 걸쳐 연결을 관리할 수 있습니다. 애플리케이션의 Reverb 서버 중 하나가 메시지를 수신하면, 해당 서버는 Redis를 사용하여 들어오는 메시지를 다른 모든 서버에 발행합니다.

수평 확장을 활성화하려면, 애플리케이션의 `.env` 구성 파일에서 `REVERB_SCALING_ENABLED` 환경 변수를 `true`로 설정해야 합니다:

```env
REVERB_SCALING_ENABLED=true

```

다음으로， 모든 Reverb 서버가 통신할 전용 중앙 Redis 서버가 있어야 합니다. Reverb 는 [애플리케이션에 대해 구성된 기본 Redis 연결](/docs/{{version}}/redis#configuration) 을 사용하여 모든 Reverb 서버에 메시지를 게시합니다。

Reverb 의 확장 옵션을 활성화하고 Redis 서버를 구성한 후에는 Redis 서버와 통신할 수 있는 여러 서버에서 `reverb:start` 명령을 간단히 호출할 수 있습니다. 이러한 Reverb 서버는 서버 간에 수신 요청을 균등하게 분산하는 로드 밸런서 뒤에 배치되어야 합니다。

<a name="events"></a>
## 이벤트

리버브는 연결 및 메시지 처리의 수명 주기 동안 내부 이벤트를 전송합니다. 연결이 관리되거나 메시지가 교환될 때 [이러한 이벤트 듣기](/docs/{{version}}/events) 를 수행할 수 있습니다。

다음 이벤트는 Reverb 에 의해 전송됩니다：

#### `Laravel\Reverb\Events\ChannelCreated`

채널이 생성될 때 전송됩니다. 이는 일반적으로 첫 번째 연결이 특정 채널을 구독할 때 발생합니다. 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 수신합니다。

#### `Laravel\Reverb\Events\ChannelRemoved`

채널이 제거될 때 전송됩니다. 이는 일반적으로 마지막 연결이 채널에서 구독을 취소할 때 발생합니다. 이 이벤트는 `Laravel\Reverb\Protocols\Pusher\Channel` 인스턴스를 수신합니다。

#### `Laravel\Reverb\Events\ConnectionPruned`

서버에서 오래된 연결을 다듬을 때 전송됩니다. 이 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스를 수신합니다。

#### `Laravel\Reverb\Events\MessageReceived`

클라이언트 연결에서 메시지가 수신될 때 전송됩니다. 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원시 문자열 `$message` 를 수신합니다。

#### `Laravel\Reverb\Events\MessageSent`

클라이언트 연결에 메시지가 전송될 때 전송됩니다. 이벤트는 `Laravel\Reverb\Contracts\Connection` 인스턴스와 원시 문자열 `$message` 를 수신합니다。
{% endraw %}
