---
layout: docs
title: "Broadcasting"
---

{% raw %}
# Broadcasting

- [Introduction](#introduction)
- [Quickstart](#quickstart)
- [Server Side Installation](#server-side-installation)
    - [Reverb](#reverb)
    - [Pusher Channels](#pusher-channels)
    - [Ably](#ably)
    - [Mercure](#mercure)
- [Client Side Installation](#client-side-installation)
    - [Reverb](#client-reverb)
    - [Pusher Channels](#client-pusher-channels)
    - [Ably](#client-ably)
    - [Mercure](#client-mercure)
- [Concept Overview](#concept-overview)
    - [Using an Example Application](#using-example-application)
- [Defining Broadcast Events](#defining-broadcast-events)
    - [Broadcast Name](#broadcast-name)
    - [Broadcast Data](#broadcast-data)
    - [Broadcast Queue](#broadcast-queue)
    - [Broadcast Conditions](#broadcast-conditions)
    - [Broadcasting and Database Transactions](#broadcasting-and-database-transactions)
- [Authorizing Channels](#authorizing-channels)
    - [Defining Authorization Callbacks](#defining-authorization-callbacks)
    - [Defining Channel Classes](#defining-channel-classes)
- [Broadcasting Events](#broadcasting-events)
    - [Only to Others](#only-to-others)
    - [Customizing the Connection](#customizing-the-connection)
    - [Anonymous Events](#anonymous-events)
    - [Rescuing Broadcasts](#rescuing-broadcasts)
- [Receiving Broadcasts](#receiving-broadcasts)
    - [Listening for Events](#listening-for-events)
    - [Leaving a Channel](#leaving-a-channel)
    - [Namespaces](#namespaces)
    - [Using React, Vue, or Svelte](#using-react-or-vue)
- [Presence Channels](#presence-channels)
    - [Authorizing Presence Channels](#authorizing-presence-channels)
    - [Joining Presence Channels](#joining-presence-channels)
    - [Broadcasting to Presence Channels](#broadcasting-to-presence-channels)
- [Model Broadcasting](#model-broadcasting)
    - [Model Broadcasting Conventions](#model-broadcasting-conventions)
    - [Listening for Model Broadcasts](#listening-for-model-broadcasts)
- [Client Events](#client-events)
- [Notifications](#notifications)

<a name="introduction"></a>
## Introduction



In many modern web applications, WebSockets are used to implement realtime, live-updating user interfaces. When some data is updated on the server, a message is typically sent over a WebSocket connection to be handled by the client. WebSockets provide a more efficient alternative to continually polling your application's server for data changes that should be reflected in your UI.

For example, imagine your application is able to export a user's data to a CSV file and email it to them. However, creating this CSV file takes several minutes so you choose to create and mail the CSV within a [queued job](/docs/{{version}}/queues). When the CSV has been created and mailed to the user, we can use event broadcasting to dispatch an `App\Events\UserDataExported` event that is received by our application's JavaScript. Once the event is received, we can display a message to the user that their CSV has been emailed to them without them ever needing to refresh the page.

To assist you in building these types of features, Laravel makes it easy to "broadcast" your server-side Laravel [events](/docs/{{version}}/events) over a WebSocket connection. Broadcasting your Laravel events allows you to share the same event names and data between your server-side Laravel application and your client-side JavaScript application.

The core concepts behind broadcasting are simple: clients connect to named channels on the frontend, while your Laravel application broadcasts events to these channels on the backend. These events can contain any additional data you wish to make available to the frontend.

<a name="supported-drivers"></a>
#### Supported Drivers

By default, Laravel includes four server-side broadcasting drivers for you to choose from: [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), and [Mercure](https://mercure.rocks).

> [!NOTE]
> Before diving into event broadcasting, make sure you have read Laravel's documentation on [events and listeners](/docs/{{version}}/events).

<a name="quickstart"></a>
## Quickstart

By default, broadcasting is not enabled in new Laravel applications. You may enable broadcasting using the `install:broadcasting` Artisan command:

```shell
php artisan install:broadcasting
```

The `install:broadcasting` command will prompt you for which event broadcasting service you would like to use. In addition, it will create the `config/broadcasting.php` configuration file and the `routes/channels.php` file where you may register your application's broadcast authorization routes and callbacks.

Laravel supports several broadcast drivers out of the box: [Laravel Reverb](/docs/{{version}}/reverb), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), [Mercure](https://mercure.rocks), and a `log` driver for local development and debugging. Additionally, a `null` driver is included which allows you to disable broadcasting during testing. A configuration example is included for each of these drivers in the `config/broadcasting.php` configuration file.

All of your application's event broadcasting configuration is stored in the `config/broadcasting.php` configuration file. Don't worry if this file does not exist in your application; it will be created when you run the `install:broadcasting` Artisan command.

<a name="quickstart-next-steps"></a>
#### Next Steps

Once you have enabled event broadcasting, you're ready to learn more about [defining broadcast events](#defining-broadcast-events) and [listening for events](#listening-for-events). If you're using Laravel's React, Vue, or Svelte [starter kits](/docs/{{version}}/starter-kits), you may listen for events using Echo's [useEcho hook](#using-react-or-vue).

> [!NOTE]
> Before broadcasting any events, you should first configure and run a [queue worker](/docs/{{version}}/queues). All event broadcasting is done via queued jobs so that the response time of your application is not seriously affected by events being broadcast.

<a name="server-side-installation"></a>
## Server Side Installation

To get started using Laravel's event broadcasting, we need to do some configuration within the Laravel application as well as install a few packages.

Event broadcasting is accomplished by a server-side broadcasting driver that broadcasts your Laravel events so that Laravel Echo (a JavaScript library) can receive them within the browser client. Don't worry - we'll walk through each part of the installation process step-by-step.

<a name="reverb"></a>
### Reverb



Reverb를 이벤트 브로드캐스터로 사용하면서 Laravel의 브로드캐스팅 기능 지원을 빠르게 활성화하려면 `--reverb` 옵션과 함께 `install:broadcasting` Artisan 명령을 호출하십시오. 이 Artisan 명령은 Reverb에 필요한 Composer 및 NPM 패키지를 설치하고 애플리케이션의 `.env` 파일을 적절한 변수로 업데이트합니다:

```shell
php artisan install:broadcasting --reverb
```



<a name="reverb-manual-installation"></a>
#### 수동 설치

`install:broadcasting` 명령을 실행하면 [Laravel Reverb](/docs/{{version}}/reverb)를 설치하라는 메시지가 표시됩니다. 물론, Composer 패키지 관리자를 사용하여 Reverb를 수동으로 설치할 수도 있습니다:

```shell
composer require laravel/reverb
```



패키지가 설치되면 Reverb의 설치 명령을 실행하여 구성을 게시하고, Reverb에 필요한 환경 변수를 추가하며, 애플리케이션에서 이벤트 브로드캐스팅을 활성화할 수 있습니다:

```shell
php artisan reverb:install
```



자세한 Reverb 설치 및 사용 방법은 [Reverb 문서](/docs/{{version}}/reverb)에서 찾을 수 있습니다.

<a name="pusher-channels"></a>
### Pusher 채널

Pusher를 이벤트 브로드캐스터로 사용하면서 Laravel의 브로드캐스팅 기능을 빠르게 활성화하려면 `install:broadcasting` Artisan 명령을 `--pusher` 옵션과 함께 호출하십시오. 이 Artisan 명령은 Pusher 자격 증명을 입력하도록 요청하고, Pusher PHP 및 JavaScript SDK를 설치하며, 애플리케이션의 `.env` 파일을 적절한 변수로 업데이트합니다.

```shell
php artisan install:broadcasting --pusher
```



<a name="pusher-manual-installation"></a>
#### 수동 설치

Pusher 지원을 수동으로 설치하려면 Composer 패키지 관리자를 사용하여 Pusher Channels PHP SDK를 설치해야 합니다:

```shell
composer require pusher/pusher-php-server
```



다음으로, `config/broadcasting.php` 구성 파일에서 Pusher Channels 자격 증명을 구성해야 합니다. 이 파일에는 이미 예제 Pusher Channels 구성이 포함되어 있어 키, 시크릿 및 애플리케이션 ID를 빠르게 지정할 수 있습니다. 일반적으로 애플리케이션의 `.env` 파일에서 Pusher Channels 자격 증명을 구성해야 합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"
```



`config/broadcasting.php` 파일의 `pusher` 구성은 또한 클러스터와 같이 채널에서 지원되는 추가 `options`를 지정할 수 있습니다.

그런 다음 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `pusher`로 설정합니다:

```ini
BROADCAST_CONNECTION=pusher
```



마지막으로, 클라이언트 측에서 브로드캐스트 이벤트를 수신할 [Laravel Echo](#client-side-installation)를 설치하고 구성할 준비가 되었습니다.

<a name="ably"></a>
### Ably

> [!NOTE]
> 아래 문서는 "Pusher 호환" 모드에서 Ably를 사용하는 방법을 다룹니다. 그러나 Ably 팀은 Ably가 제공하는 고유한 기능을 활용할 수 있는 브로드캐스터와 Echo 클라이언트를 유지 관리하고 권장합니다. Ably에서 유지 관리하는 드라이버 사용에 대한 자세한 내용은 [Ably의 Laravel 브로드캐스터 문서](https://github.com/ably/laravel-broadcaster)를 참조하십시오.

이벤트 브로드캐스터로 [Ably](https://ably.com)를 사용하면서 Laravel의 브로드캐스팅 기능 지원을 빠르게 활성화하려면, `install:broadcasting` Artisan 명령을 `--ably` 옵션과 함께 호출하십시오. 이 Artisan 명령은 Ably 자격 증명을 요청하고, Ably PHP 및 JavaScript SDK를 설치하며, 애플리케이션의 `.env` 파일을 적절한 변수로 업데이트합니다:

```shell
php artisan install:broadcasting --ably
```



**계속하기 전에, Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 기능은 Ably 애플리케이션 설정 대시보드의 "프로토콜 어댑터 설정" 부분에서 활성화할 수 있습니다.**

<a name="ably-manual-installation"></a>
#### 수동 설치

Ably 지원을 수동으로 설치하려면, Composer 패키지 관리자를 사용하여 Ably PHP SDK를 설치해야 합니다:

```shell
composer require ably/ably-php
```



다음으로, `config/broadcasting.php` 구성 파일에서 Ably 자격 증명을 구성해야 합니다. 예제 Ably 구성은 이미 이 파일에 포함되어 있어 키를 빠르게 지정할 수 있습니다. 일반적으로 이 값은 `ABLY_KEY` [환경 변수](/docs/{{version}}/configuration#environment-configuration)를 통해 설정해야 합니다:

```ini
ABLY_KEY=your-ably-key
```



그런 다음 애플리케이션의 `.env` 파일에서 `BROADCAST_CONNECTION` 환경 변수를 `ably`로 설정하세요:

```ini
BROADCAST_CONNECTION=ably
```



마지막으로, 클라이언트 측에서 브로드캐스트 이벤트를 수신할 [Laravel Echo](#client-side-installation)를 설치하고 구성할 준비가 되었습니다.

<a name="mercure"></a>
### Mercure

[Mercure](https://mercure.rocks)는 서버 전송 이벤트를 사용하는 실시간 프로토콜입니다. Mercure 허브를 통해 이벤트를 브로드캐스트하려면 애플리케이션의 `.env` 파일에서 `mercure` 연결을 구성하십시오:

```ini
BROADCAST_CONNECTION=mercure

MERCURE_URL=https://mercure.example.com/.well-known/mercure
MERCURE_PUBLIC_URL=https://mercure.example.com/.well-known/mercure
MERCURE_JWT_SECRET=<your-mercure-jwt-secret>
```



`MERCURE_URL` 값은 Laravel이 업데이트를 게시할 때 사용하는 URL이고, `MERCURE_PUBLIC_URL`은 브라우저 클라이언트가 구독할 때 사용하는 URL입니다. Mercure 허브는 동일한 JWT 비밀키로 구성되어야 합니다.

종단 간 암호화된 개인 채널을 사용하려면 32바이트 `MERCURE_ENCRYPTION_KEY` 환경 변수를 구성하세요:

```ini
MERCURE_ENCRYPTION_KEY=<your-32-byte-encryption-key>
```



<a name="client-side-installation"></a>
## 클라이언트 측 설치

<a name="client-reverb"></a>
### 리버브

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스트 드라이버에서 방송되는 이벤트를 구독하고 청취하는 것을 쉽게 만들어주는 자바스크립트 라이브러리입니다.

`install:broadcasting` Artisan 명령어를 통해 Laravel Reverb를 설치하면, Reverb와 Echo의 스캐폴딩 및 설정이 자동으로 애플리케이션에 주입됩니다. 그러나 Laravel Echo를 수동으로 구성하고 싶다면 아래 지침을 따라 진행할 수 있습니다.

<a name="reverb-client-manual-installation"></a>
#### 수동 설치

애플리케이션 프런트엔드용 Laravel Echo를 수동으로 구성하려면, 먼저 `pusher-js` 패키지를 설치하세요. Reverb는 WebSocket 구독, 채널 및 메시지에 Pusher 프로토콜을 사용하기 때문입니다:

```shell
npm install --save-dev laravel-echo pusher-js
```



Echo가 설치되면, 애플리케이션의 자바스크립트에서 새로운 Echo 인스턴스를 생성할 준비가 된 것입니다. 이를 수행하기에 좋은 위치는 Laravel 프레임워크와 함께 제공되는 `resources/js/app.js` 파일의 하단입니다:```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'reverb',
    key: import.meta.env.VITE_REVERB_APP_KEY,
    wsHost: import.meta.env.VITE_REVERB_HOST,
    wsPort: import.meta.env.VITE_REVERB_PORT ?? 80,
    wssPort: import.meta.env.VITE_REVERB_PORT ?? 443,
    forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    enabledTransports: ['ws', 'wss'],
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "reverb",
    // key: import.meta.env.VITE_REVERB_APP_KEY,
    // wsHost: import.meta.env.VITE_REVERB_HOST,
    // wsPort: import.meta.env.VITE_REVERB_PORT,
    // wssPort: import.meta.env.VITE_REVERB_PORT,
    // forceTLS: (import.meta.env.VITE_REVERB_SCHEME ?? 'https') === 'https',
    // enabledTransports: ['ws', 'wss'],
});
```



다음으로, 애플리케이션의 자산을 컴파일해야 합니다:

```shell
npm run build
```



> [!WARNING]
> Laravel Echo `reverb` 브로드캐스터는 laravel-echo v1.16.0 이상을 필요로 합니다.

<a name="client-pusher-channels"></a>
### Pusher Channels

[Laravel Echo](https://github.com/laravel/echo)는 서버 측 브로드캐스트 드라이버가 브로드캐스트하는 이벤트를 구독하고 듣는 것을 쉽게 해주는 자바스크립트 라이브러리입니다.

`install:broadcasting --pusher` Artisan 명령을 통해 브로드캐스팅 지원을 설치하면 Pusher와 Echo의 기본 설정 및 구성이 애플리케이션에 자동으로 주입됩니다. 그러나 Laravel Echo를 수동으로 구성하고자 하는 경우, 아래 지침을 따라 수동으로 설정할 수 있습니다.

<a name="pusher-client-manual-installation"></a>
#### 수동 설치

애플리케이션의 프런트엔드에서 Laravel Echo를 수동으로 구성하려면 먼저 WebSocket 구독, 채널 및 메시지를 위한 Pusher 프로토콜을 사용하는 `laravel-echo`와 `pusher-js` 패키지를 설치하세요:

```shell
npm install --save-dev laravel-echo pusher-js
```



Echo가 설치되면, 애플리케이션의 `resources/js/app.js` 파일에서 새 Echo 인스턴스를 생성할 준비가 된 것입니다:```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY,
    cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    forceTLS: true
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "pusher",
    // key: import.meta.env.VITE_PUSHER_APP_KEY,
    // cluster: import.meta.env.VITE_PUSHER_APP_CLUSTER,
    // forceTLS: true,
    // wsHost: import.meta.env.VITE_PUSHER_HOST,
    // wsPort: import.meta.env.VITE_PUSHER_PORT,
    // wssPort: import.meta.env.VITE_PUSHER_PORT,
    // enabledTransports: ["ws", "wss"],
});
```



다음으로, 애플리케이션의 `.env` 파일에서 Pusher 환경 변수에 대한 적절한 값을 정의해야 합니다. 이러한 변수가 이미 `.env` 파일에 존재하지 않는 경우, 추가해야 합니다:

```ini
PUSHER_APP_ID="your-pusher-app-id"
PUSHER_APP_KEY="your-pusher-key"
PUSHER_APP_SECRET="your-pusher-secret"
PUSHER_HOST=
PUSHER_PORT=443
PUSHER_SCHEME="https"
PUSHER_APP_CLUSTER="mt1"

VITE_APP_NAME="${APP_NAME}"
VITE_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
VITE_PUSHER_HOST="${PUSHER_HOST}"
VITE_PUSHER_PORT="${PUSHER_PORT}"
VITE_PUSHER_SCHEME="${PUSHER_SCHEME}"
VITE_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"
```



응용 프로그램의 필요에 따라 Echo 구성을 조정한 후에는 응용 프로그램의 자산을 컴파일할 수 있습니다:

```shell
npm run build
```



> [!NOTE]
> 애플리케이션의 JavaScript 자산을 컴파일하는 방법에 대해 더 알아보려면, [Vite](/docs/{{version}}/vite) 문서를 참고하십시오.

<a name="using-an-existing-client-instance"></a>
#### 기존 클라이언트 인스턴스 사용

이미 구성된 Pusher Channels 클라이언트 인스턴스를 Echo에서 사용하고자 하는 경우, `client` 구성 옵션을 통해 Echo에 전달할 수 있습니다:

```js
import Echo from 'laravel-echo';
import Pusher from 'pusher-js';

const options = {
    broadcaster: 'pusher',
    key: import.meta.env.VITE_PUSHER_APP_KEY
}

window.Echo = new Echo({
    ...options,
    client: new Pusher(options.key, options)
});
```



<a name="client-ably"></a>
### Ably

> [!NOTE]
> The documentation below discusses how to use Ably in "Pusher compatibility" mode. However, the Ably team recommends and maintains a broadcaster and Echo client that is able to take advantage of the unique capabilities offered by Ably. For more information on using the Ably maintained drivers, please [consult Ably's Laravel broadcaster documentation](https://github.com/ably/laravel-broadcaster).

[Laravel Echo](https://github.com/laravel/echo) is a JavaScript library that makes it painless to subscribe to channels and listen for events broadcast by your server-side broadcasting driver.

When installing broadcasting support via the `install:broadcasting --ably` Artisan command, Ably and Echo's scaffolding and configuration will be injected into your application automatically. However, if you wish to manually configure Laravel Echo, you may do so by following the instructions below.

<a name="ably-client-manual-installation"></a>
#### Manual Installation

To manually configure Laravel Echo for your application's frontend, first install the `laravel-echo` and `pusher-js` packages which utilize the Pusher protocol for WebSocket subscriptions, channels, and messages:

```shell
npm install --save-dev laravel-echo pusher-js
```



**계속하기 전에, Ably 애플리케이션 설정에서 Pusher 프로토콜 지원을 활성화해야 합니다. 이 기능은 Ably 애플리케이션 설정 대시보드의 '프로토콜 어댑터 설정' 부분에서 활성화할 수 있습니다.**

Echo가 설치되면, 애플리케이션의 `resources/js/app.js` 파일에서 새로운 Echo 인스턴스를 생성할 준비가 완료된 것입니다:```js tab=JavaScript
import Echo from 'laravel-echo';

import Pusher from 'pusher-js';
window.Pusher = Pusher;

window.Echo = new Echo({
    broadcaster: 'pusher',
    key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    wsHost: 'realtime-pusher.ably.io',
    wsPort: 443,
    disableStats: true,
    encrypted: true,
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "ably",
    // key: import.meta.env.VITE_ABLY_PUBLIC_KEY,
    // wsHost: "realtime-pusher.ably.io",
    // wsPort: 443,
    // disableStats: true,
    // encrypted: true,
});
```



귀하께서는 저희 Ably Echo 구성에서 `VITE_ABLY_PUBLIC_KEY` 환경 변수를 참조하는 것을 눈치채셨을 수 있습니다. 이 변수의 값은 귀하의 Ably 공개 키여야 합니다. 공개 키는 `:` 문자 앞에 위치한 Ably 키의 부분입니다.

필요에 따라 Echo 구성을 조정한 후, 애플리케이션의 자산을 컴파일할 수 있습니다:

```shell
npm run dev
```



> [!NOTE]
> 애플리케이션의 JavaScript 자산을 컴파일하는 방법에 대해 자세히 알아보려면 [Vite](/docs/{{version}}/vite) 문서를 참조하십시오.

<a name="client-mercure"></a>
### Mercure

Laravel Echo와 함께 Mercure를 사용하려면 `laravel-echo` 패키지를 설치하십시오:

```shell
npm install --save-dev laravel-echo
```



다음으로, `mercure` 브로드캐스터로 Echo 인스턴스를 생성합니다. `host` 옵션은 현재 오리진에서 기본값으로 `/.well-known/mercure`를 사용합니다:```js tab=JavaScript
import Echo from 'laravel-echo';

window.Echo = new Echo({
    broadcaster: 'mercure',
    host: import.meta.env.VITE_MERCURE_HUB_URL,
});
```

```js tab=React
import { configureEcho } from "@laravel/echo-react";

configureEcho({
    broadcaster: "mercure",
});
```

```js tab=Vue
import { configureEcho } from "@laravel/echo-vue";

configureEcho({
    broadcaster: "mercure",
});
```

```js tab=Svelte
import { configureEcho } from "@laravel/echo-svelte";

configureEcho({
    broadcaster: "mercure",
});
```



`.env` 파일에서 허브 URL을 정의하십시오:

```ini
VITE_MERCURE_HUB_URL="${MERCURE_PUBLIC_URL}"
```



<a name="concept-overview"></a>
## Concept Overview

Laravel's event broadcasting allows you to broadcast your server-side Laravel events to your client-side JavaScript application using a driver-based approach. Currently, Laravel ships with [Laravel Reverb](https://reverb.laravel.com), [Pusher Channels](https://pusher.com/channels), [Ably](https://ably.com), and [Mercure](https://mercure.rocks) drivers. The events may be easily consumed on the client-side using the [Laravel Echo](#client-side-installation) JavaScript package.

Events are broadcast over "channels", which may be specified as public or private. Any visitor to your application may subscribe to a public channel without any authentication or authorization; however, in order to subscribe to a private channel, a user must be authenticated and authorized to listen on that channel.

<a name="using-example-application"></a>
### Using an Example Application

Before diving into each component of event broadcasting, let's take a high level overview using an e-commerce store as an example.

In our application, let's assume we have a page that allows users to view the shipping status for their orders. Let's also assume that an `OrderShipmentStatusUpdated` event is fired when a shipping status update is processed by the application:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```



<a name="the-shouldbroadcast-interface"></a>
#### `ShouldBroadcast` 인터페이스

사용자가 자신의 주문 중 하나를 보고 있을 때, 상태 업데이트를 확인하기 위해 페이지를 새로 고치게 하고 싶지 않습니다. 대신 업데이트가 생성될 때 애플리케이션에 브로드캐스트되길 원합니다. 따라서 `OrderShipmentStatusUpdated` 이벤트를 `ShouldBroadcast` 인터페이스로 표시해야 합니다. 이렇게 하면 이벤트가 발생할 때 Laravel이 해당 이벤트를 브로드캐스트하도록 지시합니다:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    /**
     * The order instance.
     *
     * @var \App\Models\Order
     */
    public $order;
}
```



`ShouldBroadcast` 인터페이스는 우리 이벤트가 `broadcastOn` 메서드를 정의하도록 요구합니다. 이 메서드는 이벤트가 브로드캐스트할 채널을 반환하는 역할을 합니다. 생성된 이벤트 클래스에는 이미 이 메서드의 빈 스텁이 정의되어 있으므로, 우리는 세부 사항만 채우면 됩니다. 우리는 주문을 생성한 사람만 상태 업데이트를 볼 수 있도록 하고 싶으므로, 이벤트를 주문과 연결된 프라이빗 채널에서 브로드캐스트할 것입니다.

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channel the event should broadcast on.
 */
public function broadcastOn(): Channel
{
    return new PrivateChannel('orders.'.$this->order->id);
}
```



이벤트를 여러 채널에서 방송되도록 하려면 대신 `array`를 반환할 수 있습니다:

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PrivateChannel('orders.'.$this->order->id),
        // ...
    ];
}
```



<a name="example-application-authorizing-channels"></a>
#### 채널 승인

사용자가 비공개 채널을 청취하려면 반드시 승인이 필요하다는 것을 기억하세요. 우리는 애플리케이션의 `routes/channels.php` 파일에서 채널 승인 규칙을 정의할 수 있습니다. 이 예제에서는 비공개 `orders.1` 채널을 청취하려는 사용자가 실제로 주문 생성자인지 확인해야 합니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```



`channel` 메서드는 두 개의 인수를 받습니다: 채널의 이름과 사용자가 채널을 청취할 권한이 있는지를 나타내는 `true` 또는 `false`를 반환하는 콜백입니다.

모든 권한 부여 콜백은 현재 인증된 사용자를 첫 번째 인수로 받고, 추가적인 와일드카드 매개변수를 이후 인수로 받습니다. 이 예제에서는 채널 이름의 "ID" 부분이 와일드카드임을 표시하기 위해 `{orderId}` 자리 표시자를 사용하고 있습니다.

<a name="listening-for-event-broadcasts"></a>
#### 이벤트 방송 수신

다음으로, JavaScript 애플리케이션에서 이벤트를 수신하는 것만 남았습니다. 우리는 [Laravel Echo](#client-side-installation)를 사용하여 이를 수행할 수 있습니다. Laravel Echo의 내장 React, Vue 및 Svelte 훅을 사용하면 쉽게 시작할 수 있으며, 기본적으로 모든 이벤트의 공개 속성이 방송 이벤트에 포함됩니다:```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```



<a name="defining-broadcast-events"></a>
## 방송 이벤트 정의하기

주어진 이벤트를 방송해야 한다고 Laravel에 알리려면 이벤트 클래스에서 `Illuminate\Contracts\Broadcasting\ShouldBroadcast` 인터페이스를 구현해야 합니다. 이 인터페이스는 프레임워크에서 생성한 모든 이벤트 클래스에 이미 가져와져 있으므로, 모든 이벤트에 쉽게 추가할 수 있습니다.

`ShouldBroadcast` 인터페이스는 단일 메서드인 `broadcastOn`를 구현해야 합니다. `broadcastOn` 메서드는 이벤트가 방송될 채널 또는 채널 배열을 반환해야 합니다. 채널은 `Channel`, `PrivateChannel`, 또는 `PresenceChannel`의 인스턴스여야 합니다. `Channel`의 인스턴스는 모든 사용자가 구독할 수 있는 공개 채널을 나타내며, `PrivateChannels` 및 `PresenceChannels`는 [채널 인증](#authorizing-channels)이 필요한 비공개 채널을 나타냅니다.

```php
<?php

namespace App\Events;

use App\Models\User;
use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast
{
    use SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Get the channels the event should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel>
     */
    public function broadcastOn(): array
    {
        return [
            new PrivateChannel('user.'.$this->user->id),
        ];
    }
}
```



`ShouldBroadcast` 인터페이스를 구현한 후에는 평소 하던 대로 [이벤트를 발생](/docs/{{version}}/events)시키기만 하면 됩니다. 이벤트가 발생하면, [대기 중인 작업](/docs/{{version}}/queues)이 지정한 브로드캐스트 드라이버를 사용하여 이벤트를 자동으로 브로드캐스트합니다.

<a name="broadcast-name"></a>
### 브로드캐스트 이름

기본적으로 Laravel은 이벤트의 클래스 이름을 사용하여 이벤트를 브로드캐스트합니다. 그러나 이벤트에 `broadcastAs` 메서드를 정의하여 브로드캐스트 이름을 사용자 정의할 수도 있습니다:

```php
/**
 * The event's broadcast name.
 */
public function broadcastAs(): string
{
    return 'server.created';
}
```



`broadcastAs` 방식을 사용하여 방송 이름을 사용자 지정하는 경우, 리스너를 선행 `.` 문자로 등록해야 합니다. 이렇게 하면 Echo가 이벤트에 애플리케이션의 네임스페이스를 붙이지 않도록 지시합니다:

```js
.listen('.server.created', function (e) {
    // ...
});
```



<a name="broadcast-data"></a>
### 방송 데이터

이벤트가 방송될 때, 그 이벤트의 모든 `public` 속성은 자동으로 직렬화되어 이벤트의 페이로드로 방송됩니다. 이를 통해 JavaScript 애플리케이션에서 해당 이벤트의 공개 데이터를 접근할 수 있습니다. 예를 들어, 이벤트가 Eloquent 모델을 포함하는 단일 공개 `$user` 속성을 가지고 있다면, 이벤트의 방송 페이로드는 다음과 같을 것입니다:

```json
{
    "user": {
        "id": 1,
        "name": "Patrick Stewart"
        ...
    }
}
```



그러나 방송 페이로드에 대해 보다 세밀한 제어를 원한다면 이벤트에 `broadcastWith` 메서드를 추가할 수 있습니다. 이 메서드는 이벤트 페이로드로 방송하고자 하는 데이터 배열을 반환해야 합니다:

```php
/**
 * Get the data to broadcast.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(): array
{
    return ['id' => $this->user->id];
}
```



<a name="broadcast-queue"></a>
### 브로드캐스트 큐

기본적으로, 각 브로드캐스트 이벤트는 `queue.php` 구성 파일에 지정된 기본 큐 연결의 기본 큐에 배치됩니다. 이벤트 클래스에서 `Connection` 및 `Queue` 속성을 사용하여 브로드캐스터가 사용하는 큐 연결과 이름을 사용자 지정할 수 있습니다:

```php
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Queue;

#[Connection('redis')]
#[Queue('default')]
class ServerCreated implements ShouldBroadcast
{
    // ...
}
```



또는 이벤트에서 `broadcastQueue` 메서드를 정의하여 대기열 이름을 사용자 지정할 수 있습니다:

```php
/**
 * The name of the queue on which to place the broadcasting job.
 */
public function broadcastQueue(): string
{
    return 'default';
}
```



모든 방송 이벤트가 각 이벤트 클래스를 사용자 지정하지 않고 동일한 큐를 사용하도록 하려면, 대신 [`ShouldBroadcast` 계약을 큐로 라우팅](/docs/{{version}}/queues#queue-routing)할 수 있습니다.

기본 큐 드라이버 대신 `sync` 큐를 사용하여 이벤트를 방송하려면, `ShouldBroadcast` 대신 `ShouldBroadcastNow` 인터페이스를 구현할 수 있습니다:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcastNow;

class OrderShipmentStatusUpdated implements ShouldBroadcastNow
{
    // ...
}
```



<a name="broadcast-conditions"></a>
### 방송 조건

때때로 특정 조건이 참일 때만 이벤트를 방송하고 싶을 수 있습니다. 이벤트 클래스에 `broadcastWhen` 메서드를 추가하여 이러한 조건을 정의할 수 있습니다:

```php
/**
 * Determine if this event should broadcast.
 */
public function broadcastWhen(): bool
{
    return $this->order->value > 100;
}
```



<a name="broadcasting-and-database-transactions"></a>
#### 방송 및 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 방송 이벤트가 발송될 때, 데이터베이스 트랜잭션이 커밋되기 전에 이벤트가 큐에서 처리될 수 있습니다. 이런 경우, 데이터베이스 트랜잭션 동안 모델이나 데이터베이스 레코드에 수행한 업데이트가 아직 데이터베이스에 반영되지 않았을 수 있습니다. 또한, 트랜잭션 내에서 생성된 모델이나 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수 있습니다. 이벤트가 이러한 모델에 의존한다면, 이벤트를 방송하는 작업(job)이 처리될 때 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 구성 옵션이 `false`로 설정되어 있다면, 이벤트 클래스에서 `ShouldDispatchAfterCommit` 인터페이스를 구현하여 특정 방송 이벤트가 모든 열려 있는 데이터베이스 트랜잭션이 커밋된 후에 발송되도록 여전히 지정할 수 있습니다:

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Queue\SerializesModels;

class ServerCreated implements ShouldBroadcast, ShouldDispatchAfterCommit
{
    use SerializesModels;
}
```



> [!NOTE]
> 이러한 문제를 해결하는 방법에 대해 더 알아보려면 [대기열 작업 및 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions)에 대한 문서를 검토하십시오.

<a name="authorizing-channels"></a>
## 채널 권한 부여

개인 채널은 현재 인증된 사용자가 실제로 해당 채널을 수신할 수 있는지 권한을 부여해야 합니다. 이는 채널 이름과 함께 Laravel 애플리케이션에 HTTP 요청을 보내고 사용자가 해당 채널을 수신할 수 있는지 애플리케이션이 판단하도록 함으로써 수행됩니다. [Laravel Echo](#client-side-installation)를 사용할 경우, 개인 채널 구독 권한을 위한 HTTP 요청이 자동으로 수행됩니다.

방송이 설치되면 Laravel은 권한 요청을 처리하기 위해 `/broadcasting/auth` 경로를 자동으로 등록하려고 시도합니다. Laravel이 이러한 경로를 자동으로 등록하지 못하면 애플리케이션의 `/bootstrap/app.php` 파일에서 수동으로 등록할 수 있습니다:

```php
->withRouting(
    web: __DIR__.'/../routes/web.php',
    channels: __DIR__.'/../routes/channels.php',
    health: '/up',
)
```



<a name="defining-authorization-callbacks"></a>
### 권한 부여 콜백 정의

다음으로, 현재 인증된 사용자가 특정 채널을 들을 수 있는지 실제로 결정하는 로직을 정의해야 합니다. 이는 `install:broadcasting` Artisan 명령으로 생성된 `routes/channels.php` 파일에서 수행됩니다. 이 파일에서 `Broadcast::channel` 메서드를 사용하여 채널 권한 부여 콜백을 등록할 수 있습니다:

```php
use App\Models\User;

Broadcast::channel('orders.{orderId}', function (User $user, int $orderId) {
    return $user->id === Order::findOrNew($orderId)->user_id;
});
```



`channel` 메서드는 두 개의 인수를 받습니다: 채널의 이름과 사용자가 해당 채널을 수신할 수 있는 권한이 있는지 여부를 나타내는 `true` 또는 `false`를 반환하는 콜백입니다.

모든 권한 부여 콜백은 현재 인증된 사용자를 첫 번째 인수로 받고, 추가적인 와일드카드 매개변수를 이후 인수로 받습니다. 이 예제에서는 채널 이름의 "ID" 부분이 와일드카드임을 나타내기 위해 `{orderId}` 자리 표시자를 사용하고 있습니다.

`channel:list` Artisan 명령을 사용하여 애플리케이션의 방송 권한 부여 콜백 목록을 확인할 수 있습니다:

```shell
php artisan channel:list
```



<a name="authorization-callback-model-binding"></a>
#### 인증 콜백 모델 바인딩

HTTP 경로와 마찬가지로, 채널 경로도 암묵적 및 명시적 [경로 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 활용할 수 있습니다. 예를 들어, 문자열이나 숫자 주문 ID를 받는 대신 실제 `Order` 모델 인스턴스를 요청할 수 있습니다:

```php
use App\Models\Order;
use App\Models\User;

Broadcast::channel('orders.{order}', function (User $user, Order $order) {
    return $user->id === $order->user_id;
});
```



> [!WARNING]
> HTTP 라우트 모델 바인딩과 달리, 채널 모델 바인딩은 자동 [암시적 모델 바인딩 범위 지정](/docs/{{version}}/routing#implicit-model-binding-scoping)을 지원하지 않습니다. 하지만 대부분의 채널은 단일 모델의 고유한 기본 키를 기반으로 범위를 지정할 수 있기 때문에 이는 거의 문제가 되지 않습니다.

<a name="authorization-callback-authentication"></a>
#### 권한 콜백 인증

프라이빗 및 프레즌스 브로드캐스트 채널은 애플리케이션의 기본 인증 가드를 통해 현재 사용자를 인증합니다. 사용자가 인증되지 않은 경우, 채널 권한이 자동으로 거부되며 권한 콜백은 실행되지 않습니다. 그러나 필요하다면 들어오는 요청을 인증해야 하는 여러 개의 맞춤 가드를 지정할 수 있습니다:

```php
Broadcast::channel('channel', function () {
    // ...
}, ['guards' => ['web', 'admin']]);
```



<a name="defining-channel-classes"></a>
### 채널 클래스 정의

애플리케이션이 여러 채널을 많이 소비하고 있다면, `routes/channels.php` 파일이 커질 수 있습니다. 따라서 채널을 승인하기 위해 클로저를 사용하는 대신, 채널 클래스를 사용할 수 있습니다. 채널 클래스를 생성하려면 `make:channel` Artisan 명령을 사용하세요. 이 명령은 `App/Broadcasting` 디렉토리에 새로운 채널 클래스를 생성할 것입니다.

```shell
php artisan make:channel OrderChannel
```



다음으로, `routes/channels.php` 파일에 채널을 등록하세요:

```php
use App\Broadcasting\OrderChannel;

Broadcast::channel('orders.{order}', OrderChannel::class);
```



마지막으로, 채널 클래스의 `join` 메서드에 채널에 대한 인증 로직을 배치할 수 있습니다. 이 `join` 메서드는 일반적으로 채널 인증 클로저에 배치했을 동일한 로직을 포함하게 됩니다. 또한 채널 모델 바인딩을 활용할 수도 있습니다:

```php
<?php

namespace App\Broadcasting;

use App\Models\Order;
use App\Models\User;

class OrderChannel
{
    /**
     * Create a new channel instance.
     */
    public function __construct() {}

    /**
     * Authenticate the user's access to the channel.
     */
    public function join(User $user, Order $order): array|bool
    {
        return $user->id === $order->user_id;
    }
}
```



> [!NOTE]
> 라라벨의 다른 많은 클래스들처럼, 채널 클래스는 [서비스 컨테이너](/docs/{{version}}/container)에 의해 자동으로 해결됩니다. 따라서, 채널의 생성자에서 필요한 모든 의존성을 타입 힌트로 지정할 수 있습니다.

<a name="broadcasting-events"></a>
## 이벤트 브로드캐스팅

이벤트를 정의하고 `ShouldBroadcast` 인터페이스로 표시한 후에는, 이벤트의 dispatch 메서드를 사용하여 이벤트를 발생시키기만 하면 됩니다. 이벤트 디스패처는 이벤트가 `ShouldBroadcast` 인터페이스로 표시되어 있는지를 확인하고, 브로드캐스팅을 위해 이벤트를 큐에 추가할 것입니다:

```php
use App\Events\OrderShipmentStatusUpdated;

OrderShipmentStatusUpdated::dispatch($order);
```



<a name="only-to-others"></a>
### 다른 사용자에게만

이벤트 브로드캐스팅을 활용하는 애플리케이션을 구축할 때, 현재 사용자를 제외하고 특정 채널의 모든 구독자에게 이벤트를 브로드캐스트해야 할 때가 있습니다. 이는 `broadcast` 헬퍼와 `toOthers` 메서드를 사용하여 달성할 수 있습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->toOthers();
```



`toOthers` 방법을 언제 사용하고 싶은지 더 잘 이해하기 위해, 사용자가 작업 이름을 입력하여 새로운 작업을 생성할 수 있는 작업 목록 애플리케이션을 상상해 봅시다. 작업을 생성하기 위해, 애플리케이션은 작업의 생성을 방송하고 새로운 작업의 JSON 표현을 반환하는 `/task` URL에 요청을 보낼 수 있습니다. JavaScript 애플리케이션이 엔드포인트로부터 응답을 받으면, 다음과 같이 새로운 작업을 직접 자신의 작업 목록에 삽입할 수 있습니다:

```js
axios.post('/task', task)
    .then((response) => {
        this.tasks.push(response.data);
    });
```



However, remember that we also broadcast the task's creation. If your JavaScript application is also listening for this event in order to add tasks to the task list, you will have duplicate tasks in your list: one from the end-point and one from the broadcast. You may solve this by using the `toOthers` method to instruct the broadcaster to not broadcast the event to the current user.

> [!WARNING]
> Your event must use the `Illuminate\Broadcasting\InteractsWithSockets` trait in order to call the `toOthers` method.

<a name="only-to-others-configuration"></a>
#### Configuration

When you initialize a Laravel Echo instance, a socket ID is assigned to the connection. If you are using a global [Axios](https://github.com/axios/axios) instance to make HTTP requests from your JavaScript application, the socket ID will automatically be attached to every outgoing request as an `X-Socket-ID` header. Then, when you call the `toOthers` method, Laravel will extract the socket ID from the header and instruct the broadcaster to not broadcast to any connections with that socket ID.

If you are not using a global Axios instance, you will need to manually configure your JavaScript application to send the `X-Socket-ID` header with all outgoing requests. You may retrieve the socket ID using the `Echo.socketId` method:

```js
var socketId = Echo.socketId();
```



<a name="customizing-the-connection"></a>
### 연결 사용자 정의

애플리케이션이 여러 방송 연결과 상호작용하고 있고 기본 방송자가 아닌 다른 방송자를 사용하여 이벤트를 방송하려는 경우, `via` 메서드를 사용하여 이벤트를 푸시할 연결을 지정할 수 있습니다:

```php
use App\Events\OrderShipmentStatusUpdated;

broadcast(new OrderShipmentStatusUpdated($update))->via('pusher');
```



또는 이벤트의 생성자 내에서 `broadcastVia` 메서드를 호출하여 이벤트의 방송 연결을 지정할 수 있습니다. 그러나 그렇게 하기 전에 이벤트 클래스가 `InteractsWithBroadcasting` 트레이트를 사용하는지 확인해야 합니다:

```php
<?php

namespace App\Events;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\InteractsWithBroadcasting;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Broadcasting\PresenceChannel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Queue\SerializesModels;

class OrderShipmentStatusUpdated implements ShouldBroadcast
{
    use InteractsWithBroadcasting;

    /**
     * Create a new event instance.
     */
    public function __construct()
    {
        $this->broadcastVia('pusher');
    }
}
```



<a name="anonymous-events"></a>
### 익명 이벤트

때때로, 전용 이벤트 클래스를 만들지 않고 애플리케이션의 프론트엔드에 단순한 이벤트를 브로드캐스트하고 싶을 수 있습니다. 이를 위해, `Broadcast` 퍼사드는 "익명 이벤트"를 브로드캐스트할 수 있게 합니다:

```php
Broadcast::on('orders.'.$order->id)->send();
```



위의 예제는 다음 이벤트를 브로드캐스트합니다:

```json
{
    "event": "AnonymousEvent",
    "data": "[]",
    "channel": "orders.1"
}
```



`as` 및 `with` 방법을 사용하여 이벤트의 이름과 데이터를 사용자 정의할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)
    ->as('OrderPlaced')
    ->with($order)
    ->send();
```



위의 예제는 다음과 같은 이벤트를 브로드캐스트할 것입니다:

```json
{
    "event": "OrderPlaced",
    "data": "{ id: 1, total: 100 }",
    "channel": "orders.1"
}
```



익명 이벤트를 개인 채널이나 존재 채널에서 방송하고 싶다면 `private` 및 `presence` 메서드를 사용할 수 있습니다:

```php
Broadcast::private('orders.'.$order->id)->send();
Broadcast::presence('channels.'.$channel->id)->send();
```



`send` 메서드를 사용하여 익명 이벤트를 브로드캐스트하면 이벤트가 처리되기 위해 애플리케이션의 [큐](/docs/{{version}}/queues)로 전송됩니다. 그러나 이벤트를 즉시 브로드캐스트하려면 `sendNow` 메서드를 사용할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)->sendNow();
```



현재 인증된 사용자를 제외한 모든 채널 구독자에게 이벤트를 브로드캐스트하려면, `toOthers` 메서드를 호출할 수 있습니다:

```php
Broadcast::on('orders.'.$order->id)
    ->toOthers()
    ->send();
```



<a name="rescuing-broadcasts"></a>
### 브로드캐스트 복구

애플리케이션의 큐 서버를 사용할 수 없거나 Laravel이 이벤트를 브로드캐스트하는 동안 오류가 발생하면 예외가 발생하며, 일반적으로 최종 사용자는 애플리케이션 오류를 보게 됩니다. 이벤트 브로드캐스트는 종종 애플리케이션의 핵심 기능을 보조하는 역할을 하기 때문에, 이벤트에 `ShouldRescue` 인터페이스를 구현하면 이러한 예외가 사용자 경험을 방해하지 않도록 방지할 수 있습니다.

`ShouldRescue` 인터페이스를 구현한 이벤트는 브로드캐스트 시도 동안 자동으로 Laravel의 [rescue 헬퍼 함수](/docs/{{version}}/helpers#method-rescue)를 활용합니다. 이 헬퍼는 모든 예외를 포착하고, 애플리케이션의 예외 처리기로 보고하여 로그를 기록하며, 사용자의 워크플로를 방해하지 않고 애플리케이션이 정상적으로 계속 실행되도록 합니다.

```php
<?php

namespace App\Events;

use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Contracts\Broadcasting\ShouldRescue;

class ServerCreated implements ShouldBroadcast, ShouldRescue
{
    // ...
}
```



<a name="receiving-broadcasts"></a>
## 방송 수신

<a name="listening-for-events"></a>
### 이벤트 수신 대기

[Laravel Echo를 설치하고 인스턴스화한 후](#client-side-installation), Laravel 애플리케이션에서 방송되는 이벤트 수신을 시작할 준비가 된 것입니다. 먼저, `channel` 메서드를 사용하여 채널 인스턴스를 가져오고, `listen` 메서드를 호출하여 지정된 이벤트를 수신 대기합니다:

```js
Echo.channel(`orders.${this.order.id}`)
    .listen('OrderShipmentStatusUpdated', (e) => {
        console.log(e.order.name);
    });
```



개인 채널에서 이벤트를 듣고 싶다면 대신 `private` 메서드를 사용하십시오. 단일 채널에서 여러 이벤트를 듣기 위해 `listen` 메서드에 대한 호출을 계속 연결할 수 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .listen(/* ... */)
    .listen(/* ... */)
    .listen(/* ... */);
```



<a name="stop-listening-for-events"></a>
#### 이벤트 수신 중지

채널에서 [떠나지 않고](#leaving-a-channel) 특정 이벤트 수신을 중지하고 싶다면, `stopListening` 메서드를 사용할 수 있습니다:

```js
Echo.private(`orders.${this.order.id}`)
    .stopListening('OrderShipmentStatusUpdated');
```



<a name="leaving-a-channel"></a>
### 채널 나가기

채널을 나가려면 Echo 인스턴스에서 `leaveChannel` 메서드를 호출할 수 있습니다:

```js
Echo.leaveChannel(`orders.${this.order.id}`);
```



채널과 그와 관련된 개인 및 존재 채널을 모두 떠나고 싶다면, `leave` 메서드를 호출할 수 있습니다:

```js
Echo.leave(`orders.${this.order.id}`);
```

<a name="namespaces"></a>
### 네임스페이스

위의 예제에서 이벤트 클래스에 대해 전체 `App\Events` 네임스페이스를 지정하지 않은 것을 눈치채셨을 수 있습니다. 이는 Echo가 이벤트가 `App\Events` 네임스페이스에 있다고 자동으로 가정하기 때문입니다. 그러나 Echo를 인스턴스화할 때 `namespace` 구성 옵션을 전달하여 루트 네임스페이스를 설정할 수 있습니다:

```js
window.Echo = new Echo({
    broadcaster: 'pusher',
    // ...
    namespace: 'App.Other.Namespace'
});
```



또는 Echo를 사용하여 이벤트 클래스를 구독할 때 클래스 앞에 `.`를 붙일 수 있습니다. 이렇게 하면 항상 전체 클래스 이름을 지정할 수 있습니다:

```js
Echo.channel('orders')
    .listen('.Namespace\\Event\\Class', (e) => {
        // ...
    });
```



<a name="using-react-or-vue"></a>
### React, Vue 또는 Svelte 사용하기

Laravel Echo에는 이벤트를 듣는 것을 간단하게 해주는 React, Vue, Svelte 훅이 포함되어 있습니다. 시작하려면, 비공개 이벤트를 듣는 데 사용되는 `useEcho` 훅을 호출하세요. `useEcho` 훅은 소비하는 컴포넌트가 언마운트될 때 자동으로 채널을 떠납니다:```js tab=React
import { useEcho } from "@laravel/echo-react";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);
</script>
```



`useEcho`에 이벤트 배열을 제공하여 여러 이벤트를 들을 수 있습니다:

```js
useEcho(
    `orders.${orderId}`,
    ["OrderShipmentStatusUpdated", "OrderShipped"],
    (e) => {
        console.log(e.order);
    },
);
```



브로드캐스트 이벤트 페이로드 데이터의 형식을 지정하여 보다 높은 유형 안전성과 편집 편의성을 제공할 수도 있습니다:

```ts
type OrderData = {
    order: {
        id: number;
        user: {
            id: number;
            name: string;
        };
        created_at: string;
    };
};

useEcho<OrderData>(`orders.${orderId}`, "OrderShipmentStatusUpdated", (e) => {
    console.log(e.order.id);
    console.log(e.order.user.id);
});
```



`useEcho` 훅은 소비하는 컴포넌트가 언마운트될 때 자동으로 채널을 떠나지만, 필요할 경우 반환된 함수를 사용하여 프로그래밍 방식으로 채널 청취를 수동으로 중지하거나 시작할 수 있습니다:```js tab=React
import { useEcho } from "@laravel/echo-react";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

const { leaveChannel, leave, stopListening, listen } = useEcho(
    `orders.${orderId}`,
    "OrderShipmentStatusUpdated",
    (e) => {
        console.log(e.order);
    },
);

// Stop listening without leaving channel...
stopListening();

// Start listening again...
listen();

// Leave channel...
leaveChannel();

// Leave a channel and also its associated private and presence channels...
leave();
</script>
```



<a name="react-vue-connecting-to-public-channels"></a>
#### 공개 채널 연결

공개 채널에 연결하려면 `useEchoPublic` 훅을 사용할 수 있습니다:```js tab=React
import { useEchoPublic } from "@laravel/echo-react";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPublic } from "@laravel/echo-vue";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoPublic } from "@laravel/echo-svelte";

useEchoPublic("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```



<a name="react-vue-connecting-to-presence-channels"></a>
#### 프레즌스 채널에 연결하기

프레즌스 채널에 연결하려면, `useEchoPresence` 훅을 사용할 수 있습니다:```js tab=React
import { useEchoPresence } from "@laravel/echo-react";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoPresence } from "@laravel/echo-vue";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoPresence } from "@laravel/echo-svelte";

useEchoPresence("posts", "PostPublished", (e) => {
    console.log(e.post);
});
</script>
```



<a name="react-vue-connection-status"></a>
#### 연결 상태

`useConnectionStatus` 후크를 사용하여 현재 WebSocket 연결 상태를 가져올 수 있으며, 이 후크는 연결 상태가 변경될 때 자동으로 업데이트되는 반응형 상태를 제공합니다:```js tab=React
import { useConnectionStatus } from "@laravel/echo-react";

function ConnectionIndicator() {
    const status = useConnectionStatus();

    return <div>Connection: {status}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useConnectionStatus } from "@laravel/echo-vue";

const status = useConnectionStatus();
</script>

<template>
    <div>Connection: {{ status }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useConnectionStatus } from "@laravel/echo-svelte";

const status = useConnectionStatus();
</script>

<div>Connection: {status()}</div>
```



가능한 상태 값은 다음과 같습니다:

<div class="content-list" markdown="1">

- `connected` - WebSocket 서버에 성공적으로 연결됨.
- `connecting` - 초기 연결 시도가 진행 중임.
- `reconnecting` - 연결이 끊어진 후 재연결 시도 중임.
- `disconnected` - 연결되지 않았으며 재연결 시도를 하지 않음.
- `failed` - 연결 실패했으며 재시도하지 않음.

</div>

<a name="react-vue-socket-id"></a>
#### 소켓 ID

`useSocketId` 훅을 사용하여 현재 WebSocket 소켓 ID를 가져올 수 있으며, 이 훅은 연결이 새 소켓 ID로 재연결될 때 자동으로 업데이트되는 반응형 값을 제공합니다:```js tab=React
import { useSocketId } from "@laravel/echo-react";

function SocketIndicator() {
    const socketId = useSocketId();

    return <div>Socket ID: {socketId}</div>;
}
```

```vue tab=Vue
<script setup lang="ts">
import { useSocketId } from "@laravel/echo-vue";

const socketId = useSocketId();
</script>

<template>
    <div>Socket ID: {{ socketId }}</div>
</template>
```

```svelte tab=Svelte
<script>
import { useSocketId } from "@laravel/echo-svelte";

const socketId = useSocketId();
</script>

<div>Socket ID: {socketId()}</div>
```



<a name="presence-channels"></a>
## Presence Channels

Presence channels build on the security of private channels while exposing the additional feature of awareness of who is subscribed to the channel. This makes it easy to build powerful, collaborative application features such as notifying users when another user is viewing the same page or listing the inhabitants of a chat room.

<a name="authorizing-presence-channels"></a>
### Authorizing Presence Channels

All presence channels are also private channels; therefore, users must be [authorized to access them](#authorizing-channels). However, when defining authorization callbacks for presence channels, you will not return `true` if the user is authorized to join the channel. Instead, you should return an array of data about the user.

The data returned by the authorization callback will be made available to the presence channel event listeners in your JavaScript application. If the user is not authorized to join the presence channel, you should return `false` or `null`:

```php
use App\Models\User;

Broadcast::channel('chat.{roomId}', function (User $user, int $roomId) {
    if ($user->canJoinRoom($roomId)) {
        return ['id' => $user->id, 'name' => $user->name];
    }
});
```



<a name="joining-presence-channels"></a>
### 프레즌스 채널 참여

프레즌스 채널에 참여하려면 Echo의 `join` 메서드를 사용할 수 있습니다. `join` 메서드는 `PresenceChannel` 구현을 반환하며, `listen` 메서드를 노출하는 것과 함께 `here`, `joining` 및 `leaving` 이벤트를 구독할 수 있습니다.

```js
Echo.join(`chat.${roomId}`)
    .here((users) => {
        // ...
    })
    .joining((user) => {
        console.log(user.name);
    })
    .leaving((user) => {
        console.log(user.name);
    })
    .error((error) => {
        console.error(error);
    });
```



`here` 콜백은 채널에 성공적으로 가입되면 즉시 실행되며, 현재 채널에 가입된 다른 모든 사용자의 정보가 포함된 배열을 받게 됩니다. `joining` 메서드는 새로운 사용자가 채널에 참여할 때 실행되며, `leaving` 메서드는 사용자가 채널을 떠날 때 실행됩니다. `error` 메서드는 인증 엔드포인트가 200이 아닌 HTTP 상태 코드를 반환하거나 반환된 JSON을 파싱하는 데 문제가 있을 경우 실행됩니다.

<a name="broadcasting-to-presence-channels"></a>
### 프레즌스 채널로 브로드캐스팅

프레즌스 채널은 공용 또는 비공개 채널처럼 이벤트를 받을 수 있습니다. 채팅룸의 예를 들어, 우리는 `NewMessage` 이벤트를 채팅룸의 프레즌스 채널로 브로드캐스트하고 싶을 수 있습니다. 그렇게 하려면, 이벤트의 `broadcastOn` 메서드에서 `PresenceChannel`의 인스턴스를 반환하면 됩니다:

```php
/**
 * Get the channels the event should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(): array
{
    return [
        new PresenceChannel('chat.'.$this->message->room_id),
    ];
}
```



다른 이벤트와 마찬가지로, 현재 사용자가 방송을 받지 않도록 제외하려면 `broadcast` 헬퍼와 `toOthers` 메서드를 사용할 수 있습니다:

```php
broadcast(new NewMessage($message));

broadcast(new NewMessage($message))->toOthers();
```



다른 유형의 이벤트에서 일반적인 것처럼, Echo의 `listen` 메서드를 사용하여 프레즌스 채널로 전송된 이벤트를 수신할 수 있습니다:

```js
Echo.join(`chat.${roomId}`)
    .here(/* ... */)
    .joining(/* ... */)
    .leaving(/* ... */)
    .listen('NewMessage', (e) => {
        // ...
    });
```



<a name="model-broadcasting"></a>
## Model Broadcasting

> [!WARNING]
> Before reading the following documentation about model broadcasting, we recommend you become familiar with the general concepts of Laravel's model broadcasting services as well as how to manually create and listen to broadcast events.

It is common to broadcast events when your application's [Eloquent models](/docs/{{version}}/eloquent) are created, updated, or deleted. Of course, this can easily be accomplished by manually [defining custom events for Eloquent model state changes](/docs/{{version}}/eloquent#events) and marking those events with the `ShouldBroadcast` interface.

However, if you are not using these events for any other purposes in your application, it can be cumbersome to create event classes for the sole purpose of broadcasting them. To remedy this, Laravel allows you to indicate that an Eloquent model should automatically broadcast its state changes.

To get started, your Eloquent model should use the `Illuminate\Database\Eloquent\BroadcastsEvents` trait. In addition, the model should define a `broadcastOn` method, which will return an array of channels that the model's events should broadcast on:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\Channel;
use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Database\Eloquent\BroadcastsEvents;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Post extends Model
{
    use BroadcastsEvents, HasFactory;

    /**
     * Get the user that the post belongs to.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Get the channels that model events should broadcast on.
     *
     * @return array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>
     */
    public function broadcastOn(string $event): array
    {
        return [$this, $this->user];
    }
}
```



모델에 이 특성을 포함하고 방송 채널을 정의하면, 모델 인스턴스가 생성, 업데이트, 삭제, 휴지통으로 이동, 또는 복원될 때 이벤트를 자동으로 방송하기 시작합니다.

또한, `broadcastOn` 메서드가 문자열 `$event` 인수를 받는 것을 눈치채셨을 수도 있습니다. 이 인수에는 모델에서 발생한 이벤트 유형이 들어 있으며, 값은 `created`, `updated`, `deleted`, `trashed` 또는 `restored` 중 하나가 됩니다. 이 변수의 값을 확인함으로써, 특정 이벤트에 대해 모델이 어떤 채널(있는 경우)에 방송을 해야 하는지 결정할 수 있습니다.

```php
/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<string, array<int, \Illuminate\Broadcasting\Channel|\Illuminate\Database\Eloquent\Model>>
 */
public function broadcastOn(string $event): array
{
    return match ($event) {
        'deleted' => [],
        default => [$this, $this->user],
    };
}
```



<a name="customizing-model-broadcasting-event-creation"></a>
#### 모델 브로드캐스팅 이벤트 생성 사용자 정의

가끔 Laravel이 기본 모델 브로드캐스팅 이벤트를 생성하는 방식을 사용자 정의하고 싶을 수 있습니다. 이를 위해 Eloquent 모델에 `newBroadcastableEvent` 메서드를 정의할 수 있습니다. 이 메서드는 `Illuminate\Database\Eloquent\BroadcastableModelEventOccurred` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\BroadcastableModelEventOccurred;

/**
 * Create a new broadcastable model event for the model.
 */
protected function newBroadcastableEvent(string $event): BroadcastableModelEventOccurred
{
    return (new BroadcastableModelEventOccurred(
        $this, $event
    ))->dontBroadcastToCurrentUser();
}
```



<a name="model-broadcasting-conventions"></a>
### 모델 방송 규칙

<a name="model-broadcasting-channel-conventions"></a>
#### 채널 규칙

눈치채셨겠지만, 위 모델 예시에서 `broadcastOn` 메서드는 `Channel` 인스턴스를 반환하지 않았습니다. 대신, Eloquent 모델이 직접 반환되었습니다. 만약 모델의 `broadcastOn` 메서드에 의해 Eloquent 모델 인스턴스가 반환되거나 (또는 메서드에서 반환된 배열에 포함되어 있다면), Laravel은 모델의 클래스 이름과 기본 키 식별자를 채널 이름으로 사용하여 자동으로 모델에 대한 비공개 채널 인스턴스를 생성합니다.

따라서, `App\Models\User` 모델이 `id`가 `1`인 경우, `App.Models.User.1`라는 이름을 가진 `Illuminate\Broadcasting\PrivateChannel` 인스턴스로 변환됩니다. 물론, 모델의 `broadcastOn` 메서드에서 Eloquent 모델 인스턴스를 반환하는 것 외에도, 모델의 채널 이름을 완전히 제어하기 위해 완전한 `Channel` 인스턴스를 반환할 수도 있습니다.

```php
use Illuminate\Broadcasting\PrivateChannel;

/**
 * Get the channels that model events should broadcast on.
 *
 * @return array<int, \Illuminate\Broadcasting\Channel>
 */
public function broadcastOn(string $event): array
{
    return [
        new PrivateChannel('user.'.$this->id)
    ];
}
```



모델의 `broadcastOn` 메서드에서 명시적으로 채널 인스턴스를 반환할 계획이라면, 채널의 생성자에 Eloquent 모델 인스턴스를 전달할 수 있습니다. 이렇게 하면 Laravel은 위에서 설명한 모델 채널 규칙을 사용하여 Eloquent 모델을 채널 이름 문자열로 변환합니다:

```php
return [new Channel($this->user)];
```



모델의 채널 이름을 확인해야 하는 경우, 모든 모델 인스턴스에서 `broadcastChannel` 메서드를 호출할 수 있습니다. 예를 들어, 이 메서드는 `1`의 `id`를 가진 `App\Models\User` 모델에 대해 문자열 `App.Models.User.1`를 반환합니다:

```php
$user->broadcastChannel();
```



<a name="model-broadcasting-event-conventions"></a>
#### 이벤트 규칙

모델 브로드캐스트 이벤트는 애플리케이션의 `App\Events` 디렉토리 내의 '실제' 이벤트와 관련이 없기 때문에, 규칙에 따라 이름과 페이로드가 할당됩니다. Laravel의 규칙은 브로드캐스트를 트리거한 모델 이벤트의 이름과 모델 클래스 이름(네임스페이스 제외)을 사용하여 이벤트를 브로드캐스트하는 것입니다.

예를 들어, `App\Models\Post` 모델이 업데이트되면 클라이언트 사이드 애플리케이션으로 다음 페이로드와 함께 `PostUpdated` 이벤트를 브로드캐스트합니다:

```json
{
    "model": {
        "id": 1,
        "title": "My first post"
        ...
    },
    ...
    "socket": "someSocketId"
}
```



`App\Models\User` 모델이 삭제되면 `UserDeleted`라는 이름의 이벤트가 브로드캐스트됩니다.

원하신다면 모델에 `broadcastAs` 및 `broadcastWith` 메서드를 추가하여 맞춤 브로드캐스트 이름과 페이로드를 정의할 수 있습니다. 이 메서드들은 발생 중인 모델 이벤트/작업의 이름을 받아, 각 모델 작업에 대해 이벤트 이름과 페이로드를 맞춤 설정할 수 있게 합니다. 만약 `broadcastAs` 메서드에서 `null`가 반환되면, 라라벨은 이벤트를 브로드캐스트할 때 위에서 논의한 모델 브로드캐스팅 이벤트 이름 규칙을 사용합니다:

```php
/**
 * The model event's broadcast name.
 */
public function broadcastAs(string $event): string|null
{
    return match ($event) {
        'created' => 'post.created',
        default => null,
    };
}

/**
 * Get the data to broadcast for the model.
 *
 * @return array<string, mixed>
 */
public function broadcastWith(string $event): array
{
    return match ($event) {
        'created' => ['title' => $this->title],
        default => ['model' => $this],
    };
}
```



<a name="listening-for-model-broadcasts"></a>
### Listening for Model Broadcasts

Once you have added the `BroadcastsEvents` trait to your model and defined your model's `broadcastOn` method, you are ready to start listening for broadcasted model events within your client-side application. Before getting started, you may wish to consult the complete documentation on [listening for events](#listening-for-events).

First, use the `private` method to retrieve an instance of a channel, then call the `listen` method to listen for a specified event. Typically, the channel name given to the `private` method should correspond to Laravel's [model broadcasting conventions](#model-broadcasting-conventions).

Once you have obtained a channel instance, you may use the `listen` method to listen for a particular event. Since model broadcast events are not associated with an "actual" event within your application's `App\Events` directory, the [event name](#model-broadcasting-event-conventions) must be prefixed with a `.` to indicate it does not belong to a particular namespace. Each model broadcast event has a `model` property which contains all of the broadcastable properties of the model:

```js
Echo.private(`App.Models.User.${this.user.id}`)
    .listen('.UserUpdated', (e) => {
        console.log(e.model);
    });
```



<a name="model-broadcasts-with-react-or-vue"></a>
#### React, Vue 또는 Svelte 사용하기

React, Vue 또는 Svelte를 사용하는 경우, 모델 브로드캐스트를 쉽게 수신하기 위해 Laravel Echo에 포함된 `useEchoModel` 훅을 사용할 수 있습니다:```js tab=React
import { useEchoModel } from "@laravel/echo-react";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoModel } from "@laravel/echo-svelte";

useEchoModel("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model);
});
</script>
```



모델 이벤트 페이로드 데이터의 형태를 지정하여 더 높은 타입 안정성과 편집 편의성을 제공할 수도 있습니다:

```ts
type User = {
    id: number;
    name: string;
    email: string;
};

useEchoModel<User, "App.Models.User">("App.Models.User", userId, ["UserUpdated"], (e) => {
    console.log(e.model.id);
    console.log(e.model.name);
});
```



<a name="client-events"></a>
## 클라이언트 이벤트

> [!NOTE]
> [Pusher Channels](https://pusher.com/channels)를 사용할 때, 클라이언트 이벤트를 전송하려면 [애플리케이션 대시보드](https://dashboard.pusher.com/)의 '앱 설정' 섹션에서 '클라이언트 이벤트' 옵션을 활성화해야 합니다.

때때로 Laravel 애플리케이션에 전혀 요청을 보내지 않고 다른 연결된 클라이언트에게 이벤트를 방송하고 싶을 수 있습니다. 이는 특히 '타이핑' 알림과 같이 특정 화면에서 다른 사용자가 메시지를 입력 중임을 사용자에게 알리고 싶을 때 유용할 수 있습니다.

클라이언트 이벤트를 방송하려면, Echo의 `whisper` 메서드를 사용할 수 있습니다:```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .whisper('typing', {
        name: this.user.name
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().whisper('typing', { name: user.name });
</script>
```



클라이언트 이벤트를 수신하려면 `listenForWhisper` 메서드를 사용할 수 있습니다:```js tab=JavaScript
Echo.private(`chat.${roomId}`)
    .listenForWhisper('typing', (e) => {
        console.log(e.name);
    });
```

```js tab=React
import { useEcho } from "@laravel/echo-react";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEcho } from "@laravel/echo-vue";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEcho } from "@laravel/echo-svelte";

const { channel } = useEcho(`chat.${roomId}`, ['update'], (e) => {
    console.log('Chat event received:', e);
});

channel().listenForWhisper('typing', (e) => {
    console.log(e.name);
});
</script>
```



<a name="notifications"></a>
## 알림

이벤트 브로드캐스팅을 [알림](/docs/{{version}}/notifications)과 결합하면, JavaScript 애플리케이션이 페이지를 새로 고침하지 않고도 발생하는 새로운 알림을 받을 수 있습니다. 시작하기 전에 [브로드캐스트 알림 채널](/docs/{{version}}/notifications#broadcast-notifications) 사용에 대한 문서를 반드시 읽어보세요.

브로드캐스트 채널을 사용하도록 알림을 구성한 후에는 Echo의 `notification` 메서드를 사용하여 브로드캐스트 이벤트를 수신할 수 있습니다. 채널 이름은 알림을 받는 엔티티의 클래스 이름과 일치해야 한다는 점을 기억하세요:```js tab=JavaScript
Echo.private(`App.Models.User.${userId}`)
    .notification((notification) => {
        console.log(notification.type);
    });
```

```js tab=React
import { useEchoModel } from "@laravel/echo-react";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoModel } from "@laravel/echo-vue";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```

```svelte tab=Svelte
<script>
import { useEchoModel } from "@laravel/echo-svelte";

const { channel } = useEchoModel('App.Models.User', userId);

channel().notification((notification) => {
    console.log(notification.type);
});
</script>
```



이 예제에서 `broadcast` 채널을 통해 `App\Models\User` 인스턴스로 전송된 모든 알림은 콜백에서 수신됩니다. `App.Models.User.{id}` 채널에 대한 채널 권한 콜백이 애플리케이션의 `routes/channels.php` 파일에 포함되어 있습니다.

<a name="stop-listening-for-notifications"></a>
#### 알림 수신 중지

[채널을 나가지 않고](#leaving-a-channel) 알림 수신을 중지하려면, `stopListeningForNotification` 메서드를 사용할 수 있습니다:

```js
const callback = (notification) => {
    console.log(notification.type);
}

// Start listening...
Echo.private(`App.Models.User.${userId}`)
    .notification(callback);

// Stop listening (callback must be the same)...
Echo.private(`App.Models.User.${userId}`)
    .stopListeningForNotification(callback);
```
{% endraw %}
