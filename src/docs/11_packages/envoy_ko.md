---
layout: docs
title: "Laravel Envoy"
---

{% raw %}
# Laravel Envoy

- [소개](#introduction)
- [설치](#installation)
- [작업 작성](#writing-tasks)
    - [작업 정의](#defining-tasks)
    - [다중 서버](#multiple-servers)
    - [설정](#setup)
    - [변수](#variables)
    - [스토리](#stories)
    - [후크](#completion-hooks)
- [작업 실행](#running-tasks)
    - [작업 실행 확인](#confirming-task-execution)
- [알림](#notifications)
    - [Slack](#slack)
    - [Discord](#discord)
    - [Telegram](#telegram)
    - [Microsoft Teams](#microsoft-teams)

<a name="introduction"></a>
## 소개

[Laravel Envoy](https://github.com/laravel/envoy)는 원격 서버에서 실행하는 일반적인 작업을 수행하기 위한 도구입니다. [Blade](/docs/{{version}}/blade) 스타일 문법을 사용하여 배포, Artisan 명령어 등 작업을 쉽게 설정할 수 있습니다. 현재 Envoy는 Mac과 Linux 운영체제만 지원합니다. 그러나 [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10)를 사용하면 Windows에서도 지원이 가능합니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 사용하여 프로젝트에 Envoy를 설치합니다:

```shell
composer require laravel/envoy --dev

```

Envoy가 설치되면 Envoy 바이너리는 애플리케이션의 `vendor/bin` 디렉토리에서 사용할 수 있습니다:

```shell
php vendor/bin/envoy

```

<a name="writing-tasks"></a>
## 작성 작업

<a name="defining-tasks"></a>
### 작업 정의

작업은 Envoy의 기본 구성 요소입니다. 작업은 작업이 호출될 때 원격 서버에서 실행되어야 하는 셸 명령을 정의합니다. 예를 들어, 애플리케이션의 모든 큐 작업 서버에서 `php artisan queue:restart` 명령을 실행하는 작업을 정의할 수 있습니다.

모든 Envoy 작업은 애플리케이션 루트에 있는 `Envoy.blade.php` 파일에 정의되어야 합니다. 시작하는 데 도움이 되는 예시는 다음과 같습니다:

```blade
@servers(['web' => ['user@192.168.1.1'], 'workers' => ['user@192.168.1.2']])

@task('restart-queues', ['on' => 'workers'])
    cd /home/user/example.com
    php artisan queue:restart
@endtask

```

보시다시피, 파일 상단에 `@servers` 배열이 정의되어 있어 작업 선언의 `on` 옵션을 통해 이러한 서버를 참조할 수 있습니다. `@servers` 선언은 항상 한 줄에 작성되어야 합니다. `@task` 선언 내에는 작업이 호출될 때 서버에서 실행되어야 하는 셸 명령을 배치해야 합니다.

<a name="local-tasks"></a>
#### 로컬 작업

서버의 IP 주소를 `127.0.0.1`로 지정하여 스크립트를 로컬 컴퓨터에서 실행하도록 강제할 수 있습니다.

```blade
@servers(['localhost' => '127.0.0.1'])

```

<a name="importing-envoy-tasks"></a>
#### 엔보이 작업 가져오기

`@import` 지시문을 사용하면 다른 엔보이 파일을 가져와서 그들의 이야기와 작업을 자신의 파일에 추가할 수 있습니다. 파일을 가져온 후에는 마치 자신의 엔보이 파일에 정의된 것처럼 그 안에 포함된 작업을 실행할 수 있습니다:

```blade
@import('vendor/package/Envoy.blade.php')

```

<a name="multiple-servers"></a>
### 다중 서버

Envoy를 사용하면 여러 서버에 걸쳐 작업을 쉽게 실행할 수 있습니다. 먼저, 추가 서버를 `@servers` 선언에 추가하십시오. 각 서버에는 고유한 이름을 지정해야 합니다. 추가 서버를 정의한 후에는 작업의 `on` 배열에 각 서버를 나열할 수 있습니다:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2']])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask

```

<a name="parallel-execution"></a>
#### 병렬 실행

기본적으로, 작업은 각 서버에서 순차적으로 실행됩니다. 다시 말해, 작업은 첫 번째 서버에서 실행을 마친 후 두 번째 서버에서 실행을 진행합니다. 작업을 여러 서버에서 병렬로 실행하고 싶다면, 작업 선언에 `parallel` 옵션을 추가하십시오:

```blade
@servers(['web-1' => '192.168.1.1', 'web-2' => '192.168.1.2'])

@task('deploy', ['on' => ['web-1', 'web-2'], 'parallel' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate --force
@endtask

```

<a name="setup"></a>
### 설정

때때로, Envoy 작업을 실행하기 전에 임의의 PHP 코드를 실행해야 할 때가 있습니다. `@setup` 지시어를 사용하여 작업을 실행하기 전에 실행되어야 하는 PHP 코드 블록을 정의할 수 있습니다:

```blade
@setup
    $now = new DateTime;
@endsetup

```

작업이 실행되기 전에 다른 PHP 파일들을 포함해야 하는 경우, `Envoy.blade.php` 파일 상단에 `@include` 지시어를 사용할 수 있습니다:

```blade
@include('vendor/autoload.php')

@task('restart-queues')
    # ...
@endtask

```

<a name="variables"></a>
### 변수

필요한 경우, Envoy 작업을 호출할 때 명령줄에서 인수를 지정하여 전달할 수 있습니다:

```shell
php vendor/bin/envoy run deploy --branch=master

```

Blade의 "echo" 문법을 사용하여 작업 내 옵션에 접근할 수 있습니다. 또한 작업 내에서 Blade `if` 문장과 루프를 정의할 수도 있습니다. 예를 들어, `git pull` 명령을 실행하기 전에 `$branch` 변수가 존재하는지 확인해 보겠습니다:

```blade
@servers(['web' => ['user@192.168.1.1']])

@task('deploy', ['on' => 'web'])
    cd /home/user/example.com

    @if ($branch)
        git pull origin {{ $branch }}
    @endif

    php artisan migrate --force
@endtask

```

<a name="stories"></a>
### 스토리

스토리는 여러 작업을 하나의 편리한 이름으로 그룹화합니다. 예를 들어, `deploy` 스토리는 정의 내에서 작업 이름을 나열하여 `update-code` 및 `install-dependencies` 작업을 실행할 수 있습니다:

```blade
@servers(['web' => ['user@192.168.1.1']])

@story('deploy')
    update-code
    install-dependencies
@endstory

@task('update-code')
    cd /home/user/example.com
    git pull origin master
@endtask

@task('install-dependencies')
    cd /home/user/example.com
    composer install
@endtask

```

이야기가 작성되면, 작업을 호출하는 것과 같은 방식으로 이야기를 호출할 수 있습니다:

```shell
php vendor/bin/envoy run deploy

```

<a name="completion-hooks"></a>
### 훅(Hooks)

작업과 스토리가 실행될 때, 여러 훅이 실행됩니다. Envoy에서 지원하는 훅 타입은 `@before`, `@after`, `@error`, `@success`, `@finished`입니다. 이 훅 안의 모든 코드는 PHP로 해석되며, 작업이 상호작용하는 원격 서버가 아니라 로컬에서 실행됩니다.

이 훅들 각각을 원하는 만큼 정의할 수 있습니다. 훅은 Envoy 스크립트에 나타나는 순서대로 실행됩니다.

<a name="hook-before"></a>
#### `@before`

각 작업 실행 전에, Envoy 스크립트에 등록된 모든 `@before` 훅이 실행됩니다. `@before` 훅은 실행될 작업의 이름을 받습니다:

```blade
@before
    if ($task === 'deploy') {
        // ...
    }
@endbefore

```

<a name="completion-after"></a>
#### `@after`

각 작업 실행 후, Envoy 스크립트에 등록된 모든 `@after` 훅이 실행됩니다. `@after` 훅은 실행된 작업의 이름을 받습니다:

```blade
@after
    if ($task === 'deploy') {
        // ...
    }
@endafter

```

<a name="completion-error"></a>
#### `@error`

모든 작업 실패(종료 상태 코드가 `0`보다 큰 경우) 후에, Envoy 스크립트에 등록된 모든 `@error` 훅이 실행됩니다. `@error` 훅은 실행된 작업의 이름을 받습니다:

```blade
@error
    if ($task === 'deploy') {
        // ...
    }
@enderror

```

<a name="completion-success"></a>
#### `@success`

모든 작업이 오류 없이 실행되면, Envoy 스크립트에 등록된 모든 `@success` 훅이 실행됩니다:

```blade
@success
    // ...
@endsuccess

```

<a name="completion-finished"></a>
#### `@finished`

모든 작업이 실행된 후(종료 상태에 관계없이) 모든 `@finished` 훅이 실행됩니다. `@finished` 훅은 완료된 작업의 상태 코드를 받으며, 이는 `null`이거나 `0`보다 크거나 같은 `integer`일 수 있습니다:

```blade
@finished
    if ($exitCode > 0) {
        // There were errors in one of the tasks...
    }
@endfinished

```

<a name="running-tasks"></a>
## 실행 중인 작업

애플리케이션의 `Envoy.blade.php` 파일에 정의된 작업이나 스토리를 실행하려면 Envoy의 `run` 명령을 실행하고, 실행하려는 작업이나 스토리의 이름을 전달하세요. Envoy는 작업을 실행하고 작업이 진행되는 동안 원격 서버의 출력을 표시합니다:

```shell
php vendor/bin/envoy run deploy

```

<a name="confirming-task-execution"></a>
### 작업 실행 확인

서버에서 특정 작업을 실행하기 전에 확인을 받도록 하고 싶다면, 작업 선언에 `confirm` 지시어를 추가해야 합니다. 이 옵션은 파괴적인 작업에 특히 유용합니다:

```blade
@task('deploy', ['on' => 'web', 'confirm' => true])
    cd /home/user/example.com
    git pull origin {{ $branch }}
    php artisan migrate
@endtask

```

<a name="notifications"></a>
## 알림

<a name="slack"></a>
### 슬랙

Envoy는 각 작업이 실행된 후 [Slack](https://slack.com)으로 알림을 보내는 것을 지원합니다. `@slack` 지시문은 Slack 훅 URL과 채널 / 사용자 이름을 받습니다. Slack 제어판에서 "Incoming WebHooks" 통합을 생성하여 웹훅 URL을 가져올 수 있습니다.

`@slack` 지시문에 첫 번째 인수로 전체 웹훅 URL을 전달해야 합니다. `@slack` 지시문에 두 번째 인수로 채널 이름(`#channel`) 또는 사용자 이름(`@user`)을 전달해야 합니다:

```blade
@finished
    @slack('webhook-url', '#bots')
@endfinished

```

기본적으로 Envoy 알림은 실행된 작업을 설명하는 메시지를 알림 채널에 전송합니다. 그러나 `@slack` 지시문에 세 번째 인수를 전달하여 이 메시지를 사용자 지정 메시지로 덮어쓸 수 있습니다:

```blade
@finished
    @slack('webhook-url', '#bots', 'Hello, Slack.')
@endfinished

```

<a name="discord"></a>
### 디스코드

Envoy는 각 작업이 실행된 후 [디스코드](https://discord.com)로 알림을 보내는 것도 지원합니다. `@discord` 지시어는 디스코드 훅 URL과 메시지를 받습니다. 서버 설정에서 “웹훅”을 생성하고 웹훅이 게시할 채널을 선택하여 웹훅 URL을 가져올 수 있습니다. 전체 웹훅 URL을 `@discord` 지시어에 전달해야 합니다:

```blade
@finished
    @discord('discord-webhook-url')
@endfinished

```

<a name="telegram"></a>
### 텔레그램

Envoy는 각 작업이 실행된 후 [텔레그램](https://telegram.org)으로 알림을 보내는 것도 지원합니다. `@telegram` 지시어는 텔레그램 봇 ID와 채팅 ID를 받아들입니다. [BotFather](https://t.me/botfather)를 사용하여 새 봇을 생성하면 봇 ID를 가져올 수 있습니다. [@username_to_id_bot](https://t.me/username_to_id_bot)를 사용하여 유효한 채팅 ID를 가져올 수 있습니다. `@telegram` 지시어에 전체 봇 ID와 채팅 ID를 전달해야 합니다.

```blade
@finished
    @telegram('bot-id','chat-id')
@endfinished

```

<a name="microsoft-teams"></a>
### 마이크로소프트 팀즈

Envoy는 각 작업이 실행된 후 [마이크로소프트 팀즈](https://www.microsoft.com/en-us/microsoft-teams)로 알림을 보내는 것도 지원합니다. `@microsoftTeams` 지시는 Teams Webhook(필수), 메시지, 테마 색상(성공, 정보, 경고, 오류), 옵션 배열을 받습니다. 새 [수신 웹후크](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)를 생성하여 Teams Webhook을 가져올 수 있습니다. Teams API에는 제목, 요약, 섹션과 같이 메시지 박스를 사용자 정의할 수 있는 다른 많은 속성이 있습니다. 자세한 정보는 [마이크로소프트 팀즈 문서](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL#example-of-connector-message)에서 확인할 수 있습니다. 전체 Webhook URL을 `@microsoftTeams` 지시어에 전달해야 합니다:

```blade
@finished
    @microsoftTeams('webhook-url')
@endfinished

```
{% endraw %}
