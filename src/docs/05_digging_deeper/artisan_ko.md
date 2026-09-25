---
layout: docs
title: "Artisan Console"
---

{% raw %}
---
layout: docs
title: "Artisan Console"
---

# Artisan Console

- [Introduction](#introduction)
    - [Tinker (REPL)](#tinker)
- [Writing Commands](#writing-commands)
    - [Generating Commands](#generating-commands)
    - [Command Structure](#command-structure)
    - [Closure Commands](#closure-commands)
    - [Isolatable Commands](#isolatable-commands)
- [Defining Input Expectations](#defining-input-expectations)
    - [Arguments](#arguments)
    - [Options](#options)
    - [Input Arrays](#input-arrays)
    - [Input Descriptions](#input-descriptions)
    - [Prompting for Missing Input](#prompting-for-missing-input)
- [Command I/O](#command-io)
    - [Retrieving Input](#retrieving-input)
    - [Prompting for Input](#prompting-for-input)
    - [Writing Output](#writing-output)
- [Registering Commands](#registering-commands)
- [Programmatically Executing Commands](#programmatically-executing-commands)
    - [Calling Commands From Other Commands](#calling-commands-from-other-commands)
- [Signal Handling](#signal-handling)
- [The Dev Command](#the-dev-command)
    - [Customizing Dev Processes](#customizing-dev-processes)
    - [Filtering Dev Processes](#filtering-dev-processes)
- [Stub Customization](#stub-customization)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Artisan is the command line interface included with Laravel. Artisan exists at the root of your application as the `artisan` script and provides a number of helpful commands you can use while building your application. To view a list of all available Artisan commands, you may use the `list` command:

```shell
php artisan list
```



모든 명령에는 명령의 사용 가능한 인수와 옵션을 표시하고 설명하는 "도움말" 화면도 포함됩니다. 도움말 화면을 보려면 명령 이름 앞에 `help`:를 붙이십시오.

```shell
php artisan help migrate
```



<a name="laravel-sail"></a>
#### 라라벨 세일(Laravel Sail)

로컬 개발 환경으로 [라라벨 세일(Laravel Sail)](/docs/{{version}}/sail)을 사용하고 있다면, Artisan 명령어를 실행할 때 `sail` 명령어를 사용해야 합니다. 세일은 애플리케이션의 도커 컨테이너 내에서 Artisan 명령어를 실행합니다:

```shell
./vendor/bin/sail artisan list
```



<a name="tinker"></a>
### 틴커 (REPL)

[Laravel Tinker](https://github.com/laravel/tinker)는 [PsySH](https://github.com/bobthecow/psysh) 패키지로 구동되는 Laravel 프레임워크용 강력한 REPL입니다.

<a name="installation"></a>
#### 설치

모든 Laravel 애플리케이션에는 기본적으로 Tinker가 포함되어 있습니다. 그러나 애플리케이션에서 Tinker를 이전에 제거한 경우 Composer를 사용하여 Tinker를 설치할 수 있습니다:

```shell
composer require laravel/tinker
```



> [!NOTE]
> Laravel 애플리케이션과 상호작용할 때 핫 리로딩, 다중 라인 코드 편집, 자동 완성 기능을 찾고 계신가요? [Tinkerwell](https://tinkerwell.app)를 확인해 보세요!

<a name="usage"></a>
#### 사용법

Tinker를 사용하면 Eloquent 모델, 작업, 이벤트 등 전체 Laravel 애플리케이션과 명령줄에서 상호작용할 수 있습니다. Tinker 환경에 들어가려면 `tinker` Artisan 명령어를 실행하세요:

```shell
php artisan tinker
```



`vendor:publish` 명령어를 사용하여 Tinker의 구성 파일을 게시할 수 있습니다:

```shell
php artisan vendor:publish --provider="Laravel\Tinker\TinkerServiceProvider"
```



> [!WARNING]
> `Dispatchable` 클래스의 `dispatch` 헬퍼 함수와 `dispatch` 메서드는 작업을 큐에 배치하기 위해 가비지 수집에 의존합니다. 따라서 Tinker를 사용할 때는 작업을 디스패치하기 위해 `Bus::dispatch` 또는 `Queue::push`를 사용해야 합니다.

<a name="command-allow-list"></a>
#### 명령 허용 목록

Tinker는 셸 내에서 실행이 허용되는 Artisan 명령을 결정하기 위해 "허용" 목록을 사용합니다. 기본적으로, `clear-compiled`, `down`, `env`, `inspire`, `migrate`, `migrate:install`, `up`, `optimize` 명령을 실행할 수 있습니다. 더 많은 명령을 허용하고 싶다면 `tinker.php` 구성 파일의 `commands` 배열에 추가할 수 있습니다.

```php
'commands' => [
    // App\Console\Commands\ExampleCommand::class,
],
```



<a name="classes-that-should-not-be-aliased"></a>
#### 별칭을 사용해서는 안 되는 클래스

일반적으로 Tinker는 사용자가 Tinker와 상호작용할 때 클래스에 자동으로 별칭을 지정합니다. 그러나 일부 클래스는 절대 별칭을 사용하지 않기를 원할 수 있습니다. 이것은 `tinker.php` 구성 파일의 `dont_alias` 배열에 클래스를 나열하여 달성할 수 있습니다:

```php
'dont_alias' => [
    App\Models\User::class,
],
```



<a name="writing-commands"></a>
## 명령어 작성

Artisan과 함께 제공되는 명령어 외에도, 자신만의 커스텀 명령어를 만들 수 있습니다. 명령어는 일반적으로 `app/Console/Commands` 디렉터리에 저장되지만, Laravel에게 [다른 디렉터리에서도 Artisan 명령어를 스캔하도록](#registering-commands) 지시하는 한 원하는 저장 위치를 자유롭게 선택할 수 있습니다.

<a name="generating-commands"></a>
### 명령어 생성

새 명령어를 만들기 위해 `make:command` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 `app/Console/Commands` 디렉터리에 새로운 명령어 클래스를 생성합니다. 애플리케이션에 이 디렉터리가 존재하지 않아도 걱정하지 마세요 - `make:command` Artisan 명령어를 처음 실행할 때 생성됩니다.

```shell
php artisan make:command SendEmails
```



<a name="command-structure"></a>
### 명령 구조

명령을 생성한 후, `Signature` 및 `Description` 속성을 사용하여 명령의 시그니처와 설명을 정의해야 합니다. `Signature` 속성을 사용하면 [명령의 입력 기대 사항](#defining-input-expectations)도 정의할 수 있습니다. `handle` 메서드는 명령이 실행될 때 호출됩니다. 이 메서드에 명령 로직을 작성할 수 있습니다.

예시 명령을 살펴보겠습니다. 명령의 `handle` 메서드를 통해 필요한 모든 의존성을 요청할 수 있다는 점에 유의하세요. Laravel [서비스 컨테이너](/docs/{{version}}/container)가 이 메서드의 시그니처에서 타입 힌트가 지정된 모든 의존성을 자동으로 주입합니다:

```php
<?php

namespace App\Console\Commands;

use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Console\Attributes\Description;
use Illuminate\Console\Attributes\Signature;
use Illuminate\Console\Command;

#[Signature('mail:send {user}')]
#[Description('Send a marketing email to a user')]
class SendEmails extends Command
{
    /**
     * Execute the console command.
     */
    public function handle(DripEmailer $drip): void
    {
        $drip->send(User::find($this->argument('user')));
    }
}
```



> [!NOTE]
> 코드 재사용성을 높이기 위해, 콘솔 명령어를 가볍게 유지하고 실제 작업 수행은 애플리케이션 서비스에 맡기는 것이 좋은 습관입니다. 위 예제에서는 이메일 전송의 "핵심 작업"을 수행하도록 서비스 클래스를 주입하는 것을 주목하십시오.

<a name="exit-codes"></a>
#### 종료 코드

`handle` 메서드에서 아무것도 반환하지 않고 명령이 성공적으로 실행되면, 명령은 성공을 나타내는 `0` 종료 코드와 함께 종료됩니다. 그러나 `handle` 메서드는 선택적으로 정수를 반환하여 명령의 종료 코드를 수동으로 지정할 수 있습니다:

```php
$this->error('Something went wrong.');

return 1;
```



명령 내의 어떤 방법에서도 명령을 '실패'시키고 싶다면 `fail` 방법을 사용할 수 있습니다. `fail` 방법은 명령의 실행을 즉시 종료하고 `1` 종료 코드를 반환합니다:

```php
$this->fail('Something went wrong.');
```



<a name="closure-commands"></a>
### 클로저 명령어

클로저 기반 명령어는 콘솔 명령어를 클래스로 정의하는 것에 대한 대안을 제공합니다. 라우트 클로저가 컨트롤러의 대안인 것과 같은 방식으로, 명령 클로저를 명령 클래스의 대안으로 생각할 수 있습니다.

`routes/console.php` 파일은 HTTP 라우트를 정의하지 않지만, 애플리케이션에 대한 콘솔 기반 진입점(라우트)을 정의합니다. 이 파일 내에서 `Artisan::command` 메서드를 사용하여 모든 클로저 기반 콘솔 명령어를 정의할 수 있습니다. `command` 메서드는 두 개의 인수를 받습니다: [명령 서명](#defining-input-expectations)과 명령의 인수 및 옵션을 받는 클로저:

```php
Artisan::command('mail:send {user}', function (string $user) {
    $this->info("Sending email to: {$user}!");
});
```



클로저는 기본 명령 인스턴스에 바인딩되므로, 전체 명령 클래스에서 일반적으로 접근할 수 있는 모든 헬퍼 메서드에 완전히 접근할 수 있습니다.

<a name="type-hinting-dependencies"></a>
#### 타입 힌트 의존성

명령어의 인수와 옵션을 받는 것 외에도, 명령 클로저는 [서비스 컨테이너](/docs/{{version}}/container)에서 해결하고 싶은 추가 의존성을 타입 힌트로 지정할 수도 있습니다:

```php
use App\Models\User;
use App\Support\DripEmailer;
use Illuminate\Support\Facades\Artisan;

Artisan::command('mail:send {user}', function (DripEmailer $drip, string $user) {
    $drip->send(User::find($user));
});
```



<a name="closure-command-descriptions"></a>
#### 클로저 명령 설명

클로저 기반 명령을 정의할 때, `purpose` 방법을 사용하여 명령에 설명을 추가할 수 있습니다. 이 설명은 `php artisan list` 또는 `php artisan help` 명령을 실행할 때 표시됩니다:

```php
Artisan::command('mail:send {user}', function (string $user) {
    // ...
})->purpose('Send a marketing email to a user');
```



<a name="isolatable-commands"></a>
### 고립 가능한 명령어

> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션이 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 캐시 드라이버를 애플리케이션의 기본 캐시 드라이버로 사용해야 합니다. 또한, 모든 서버가 동일한 중앙 캐시 서버와 통신하고 있어야 합니다.

가끔 한 번에 하나의 명령어 인스턴스만 실행되도록 보장하고 싶을 때가 있습니다. 이를 달성하기 위해, 명령어 클래스에 `Illuminate\Contracts\Console\Isolatable` 인터페이스를 구현할 수 있습니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\Isolatable;

class SendEmails extends Command implements Isolatable
{
    // ...
}
```



명령을 `Isolatable`로 표시하면, Laravel은 명령의 옵션에서 명시적으로 정의하지 않아도 해당 명령에 `--isolated` 옵션을 자동으로 사용할 수 있게 합니다. 해당 옵션으로 명령이 호출되면, Laravel은 다른 인스턴스가 이미 실행 중인지 확인합니다. Laravel은 애플리케이션의 기본 캐시 드라이버를 사용하여 원자적 잠금을 시도함으로써 이를 수행합니다. 만약 명령의 다른 인스턴스가 실행 중이라면, 명령은 실행되지 않지만 여전히 성공적인 종료 상태 코드로 종료됩니다:

```shell
php artisan mail:send 1 --isolated
```



명령을 실행할 수 없을 경우 반환할 종료 상태 코드를 지정하고 싶다면, `isolated` 옵션을 통해 원하는 상태 코드를 제공할 수 있습니다:

```shell
php artisan mail:send 1 --isolated=12
```



<a name="lock-id"></a>
#### 잠금 ID

기본적으로 Laravel은 애플리케이션 캐시에서 원자적 잠금을 획득하는 데 사용되는 문자열 키를 생성하기 위해 명령어의 이름을 사용합니다. 그러나 Artisan 명령어 클래스에 `isolatableId` 메서드를 정의하여 이 키를 사용자 정의할 수 있으며, 이를 통해 명령어의 인수나 옵션을 키에 통합할 수 있습니다:

```php
/**
 * Get the isolatable ID for the command.
 */
public function isolatableId(): string
{
    return $this->argument('user');
}
```



<a name="lock-expiration-time"></a>
#### 잠금 만료 시간

기본적으로 격리 잠금은 명령이 완료되면 만료됩니다. 또는 명령이 중단되어 완료할 수 없는 경우, 잠금은 1시간 후에 만료됩니다. 그러나 명령에 `isolationLockExpiresAt` 메서드를 정의하여 잠금 만료 시간을 조정할 수 있습니다:

```php
use DateTimeInterface;
use DateInterval;

/**
 * Determine when an isolation lock expires for the command.
 */
public function isolationLockExpiresAt(): DateTimeInterface|DateInterval
{
    return now()->plus(minutes: 5);
}
```



<a name="defining-input-expectations"></a>
## 입력 기대치 정의

콘솔 명령을 작성할 때, 사용자로부터 인수를 통해 입력을 받는 것이 일반적입니다. Laravel은 명령에서 `signature` 속성을 사용하여 사용자가 제공할 것으로 예상되는 입력을 정의하는 것을 매우 편리하게 만듭니다. `signature` 속성을 사용하면 명령에 대한 이름, 인수 및 옵션을 단일하고 표현력 있는 라우트와 같은 문법으로 정의할 수 있습니다.

<a name="arguments"></a>
### 인수

사용자가 제공하는 모든 인수와 옵션은 중괄호로 감싸집니다. 다음 예제에서 명령은 하나의 필수 인수를 정의합니다: `user`:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user}';
```



인수를 선택사항으로 만들거나 인수의 기본값을 정의할 수도 있습니다:

```php
// Optional argument...
'mail:send {user?}'

// Optional argument with default value...
'mail:send {user=foo}'
```



<a name="options"></a>
### 옵션

옵션은 인수와 마찬가지로 또 다른 형태의 사용자 입력입니다. 옵션은 명령줄을 통해 제공될 때 두 개의 하이픈(`--`)으로 시작합니다. 옵션에는 값을 받는 것과 받지 않는 두 가지 유형이 있습니다. 값을 받지 않는 옵션은 불리언 "스위치" 역할을 합니다. 이러한 유형의 옵션 예제를 살펴보겠습니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue}';
```



이 예제에서는 Artisan 명령을 호출할 때 `--queue` 스위치를 지정할 수 있습니다. `--queue` 스위치가 전달되면 옵션의 값은 `true`가 됩니다. 그렇지 않으면 값은 `false`가 됩니다:

```shell
php artisan mail:send 1 --queue
```



<a name="options-with-values"></a>
#### 값이 있는 옵션

다음으로 값이 필요한 옵션을 살펴보겠습니다. 사용자가 옵션에 대해 값을 지정해야 하는 경우, 옵션 이름에 `=` 기호를 붙여야 합니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send {user} {--queue=}';
```



이 예제에서 사용자는 다음과 같이 옵션에 대한 값을 전달할 수 있습니다. 명령을 호출할 때 옵션이 지정되지 않으면 해당 값은 `null`가 됩니다:

```shell
php artisan mail:send 1 --queue=default
```



옵션 이름 뒤에 기본값을 지정하여 옵션에 기본값을 할당할 수 있습니다. 사용자가 옵션 값을 전달하지 않으면 기본값이 사용됩니다:

```php
'mail:send {user} {--queue=default}'
```



<a name="option-shortcuts"></a>
#### 옵션 단축키

옵션을 정의할 때 단축키를 지정하려면 옵션 이름 앞에 단축키를 명시하고 `|` 문자를 구분 기호로 사용하여 단축키와 전체 옵션 이름을 구분할 수 있습니다:

```php
'mail:send {user} {--Q|queue=}'
```



터미널에서 명령을 호출할 때, 옵션 단축키는 단일 하이픈으로 시작해야 하며 옵션의 값을 지정할 때 `=` 문자가 포함되어서는 안 됩니다:

```shell
php artisan mail:send 1 -Qdefault
```



<a name="input-arrays"></a>
### 입력 배열

여러 입력 값을 예상하는 인수나 옵션을 정의하고 싶다면 `*` 문자를 사용할 수 있습니다. 먼저, 이러한 인수를 지정하는 예제를 살펴보겠습니다:

```php
'mail:send {user*}'
```



이 명령을 실행할 때 `user` 인수를 명령줄에 순서대로 전달할 수 있습니다. 예를 들어, 다음 명령은 `user`의 값을 `1`와 `2`를 값으로 가지는 배열로 설정합니다:

```shell
php artisan mail:send 1 2
```



이 `*` 문자는 선택적인 인수 정의와 결합하여 인수가 0개 이상 있는 경우를 허용할 수 있습니다:

```php
'mail:send {user?*}'
```



<a name="option-arrays"></a>
#### 옵션 배열

여러 입력 값을 기대하는 옵션을 정의할 때, 명령에 전달된 각 옵션 값은 옵션 이름으로 접두사가 붙어야 합니다:

```php
'mail:send {--id=*}'
```



이러한 명령은 여러 개의 `--id` 인수를 전달하여 호출할 수 있습니다:

```shell
php artisan mail:send --id=1 --id=2
```



<a name="input-descriptions"></a>
### 입력 설명

인수 이름과 설명을 콜론으로 구분하여 입력 인수와 옵션에 대한 설명을 지정할 수 있습니다. 명령을 정의하는 데 약간의 여유 공간이 필요하다면 정의를 여러 줄에 걸쳐 나누어 작성해도 됩니다:

```php
/**
 * The name and signature of the console command.
 *
 * @var string
 */
protected $signature = 'mail:send
                        {user : The ID of the user}
                        {--queue : Whether the job should be queued}';
```



<a name="prompting-for-missing-input"></a>
### 누락된 입력 요청

명령어에 필수 인수가 포함된 경우, 사용자가 제공하지 않으면 오류 메시지가 표시됩니다. 또는 `PromptsForMissingInput` 인터페이스를 구현하여 필수 인수가 누락되었을 때 자동으로 사용자에게 요청하도록 명령어를 구성할 수도 있습니다:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Contracts\Console\PromptsForMissingInput;

class SendEmails extends Command implements PromptsForMissingInput
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'mail:send {user}';

    // ...
}
```



만약 Laravel이 사용자로부터 필수 인수를 수집해야 한다면, 인수 이름이나 설명을 사용하여 질문을 지능적으로 표현함으로써 자동으로 사용자에게 해당 인수를 요청합니다. 필수 인수를 수집하기 위해 사용되는 질문을 사용자 정의하고 싶다면, 인수 이름을 키로 하는 질문 배열을 반환하는 `promptForMissingArgumentsUsing` 메서드를 구현할 수 있습니다:

```php
/**
 * Prompt for missing input arguments using the returned questions.
 *
 * @return array<string, string>
 */
protected function promptForMissingArgumentsUsing(): array
{
    return [
        'user' => 'Which user ID should receive the mail?',
    ];
}
```



질문과 플레이스홀더를 포함하는 튜플을 사용하여 플레이스홀더 텍스트를 제공할 수도 있습니다:

```php
return [
    'user' => ['Which user ID should receive the mail?', 'E.g. 123'],
];
```



프롬프트를 완전히 제어하고 싶다면, 사용자를 프롬프트하도록 하고 그들의 답변을 반환하는 클로저를 제공할 수 있습니다:

```php
use App\Models\User;
use function Laravel\Prompts\search;

// ...

return [
    'user' => fn () => search(
        label: 'Search for a user:',
        placeholder: 'E.g. Taylor Otwell',
        options: fn ($value) => strlen($value) > 0
            ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
            : []
    ),
];
```



> [!NOTE]
포괄적인 [Laravel 프롬프트](/docs/{{version}}/prompts) 문서에는 사용 가능한 프롬프트와 그 사용법에 대한 추가 정보가 포함되어 있습니다.

사용자에게 [옵션](#options)을 선택하거나 입력하도록 요청하고 싶다면, 명령어의 `handle` 메서드에 프롬프트를 포함할 수 있습니다. 그러나 사용자가 누락된 인수에 대해 자동으로 프롬프트되었을 때만 사용자에게 요청하고자 한다면, `afterPromptingForMissingArguments` 메서드를 구현할 수 있습니다:

```php
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use function Laravel\Prompts\confirm;

// ...

/**
 * Perform actions after the user was prompted for missing arguments.
 */
protected function afterPromptingForMissingArguments(InputInterface $input, OutputInterface $output): void
{
    $input->setOption('queue', confirm(
        label: 'Would you like to queue the mail?',
        default: $this->option('queue')
    ));
}
```



<a name="command-io"></a>
## 명령 I/O

<a name="retrieving-input"></a>
### 입력 가져오기

명령이 실행되는 동안, 명령에서 허용하는 인수와 옵션의 값을 확인해야 할 수 있습니다. 이를 위해 `argument` 및 `option` 메서드를 사용할 수 있습니다. 인수나 옵션이 존재하지 않는 경우, `null`가 반환됩니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $userId = $this->argument('user');
}
```



모든 인수를 `array`로 가져와야 하는 경우, `arguments` 메서드를 호출하십시오:

```php
$arguments = $this->arguments();
```



옵션은 `option` 메소드를 사용하여 인수만큼 쉽게 검색할 수 있습니다. 모든 옵션을 배열로 가져오려면 `options` 메소드를 호출하십시오:

```php
// Retrieve a specific option...
$queueName = $this->option('queue');

// Retrieve all options as an array...
$options = $this->options();
```



`input` 방법을 사용하여 명령의 인수와 옵션을 `Illuminate\Console\CommandInput` 인스턴스로 가져올 수 있으며, 이 인스턴스는 HTTP 요청 및 기타 데이터 컨테이너에서 사용할 수 있는 동일한 타입 액세서를 제공합니다:

```php
use App\Enums\ReportType;

/**
 * Execute the console command.
 */
public function handle(): void
{
    $input = $this->input()->date('from');

    // ...
}
```



`input` 방법은 인수 또는 옵션에서 단일 입력 값을 가져오는 데에도 사용할 수 있습니다:

```php
$queue = $this->input('queue', 'default');
```



<a name="prompting-for-input"></a>
### 입력 요청하기

> [!NOTE]
> [Laravel Prompts](/docs/{{version}}/prompts)는 브라우저와 유사한 기능(플레이스홀더 텍스트와 검증 포함)을 갖춘 명령어 기반 애플리케이션에 아름답고 사용자 친화적인 폼을 추가하기 위한 PHP 패키지입니다.

출력을 표시하는 것 외에도, 명령어 실행 중에 사용자가 입력을 제공하도록 요청할 수도 있습니다. `ask` 메서드는 주어진 질문을 사용자에게 표시하고, 입력을 받아, 그 사용자의 입력을 다시 명령어로 반환합니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $name = $this->ask('What is your name?');

    // ...
}
```



`ask` 메서드는 또한 사용자가 입력을 제공하지 않을 경우 반환되어야 하는 기본 값을 지정하는 선택적 두 번째 인수를 허용합니다:

```php
$name = $this->ask('What is your name?', 'Taylor');
```



`secret` 방법은 `ask`와 유사하지만, 사용자가 콘솔에 입력할 때 자신의 입력이 보이지 않습니다. 이 방법은 비밀번호와 같은 민감한 정보를 요청할 때 유용합니다:

```php
$password = $this->secret('What is the password?');
```



<a name="asking-for-confirmation"></a>
#### 확인 요청

사용자에게 간단한 "예 또는 아니오" 확인을 요청해야 하는 경우, `confirm` 방법을 사용할 수 있습니다. 기본적으로 이 방법은 `false`를 반환합니다. 그러나 사용자가 프롬프트에 대해 `y` 또는 `yes`를 입력하면, 이 방법은 `true`를 반환합니다.

```php
if ($this->confirm('Do you wish to continue?')) {
    // ...
}
```



필요한 경우, 확인 프롬프트가 기본적으로 `true`를 반환하도록 지정하려면 `confirm` 메서드에 `true`를 두 번째 인수로 전달할 수 있습니다:

```php
if ($this->confirm('Do you wish to continue?', true)) {
    // ...
}
```



<a name="auto-completion"></a>
#### 자동 완성

`anticipate` 방법은 가능한 선택에 대한 자동 완성을 제공하는 데 사용할 수 있습니다. 사용자는 자동 완성 힌트에 상관없이 여전히 어떤 답변이든 제공할 수 있습니다:

```php
$name = $this->anticipate('What is your name?', ['Taylor', 'Dayle']);
```



또는 `anticipate` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 사용자가 입력 문자를 입력할 때마다 클로저가 호출됩니다. 클로저는 지금까지 사용자의 입력을 포함하는 문자열 매개변수를 받아야 하며, 자동 완성을 위한 옵션 배열을 반환해야 합니다:

```php
use App\Models\Address;

$name = $this->anticipate('What is your address?', function (string $input) {
    return Address::whereLike('name', "{$input}%")
        ->limit(5)
        ->pluck('name')
        ->all();
});
```



<a name="multiple-choice-questions"></a>
#### 다지선다형 질문

질문을 할 때 사용자에게 미리 정의된 선택지를 제공해야 하는 경우, `choice` 방법을 사용할 수 있습니다. 옵션이 선택되지 않은 경우 반환할 기본값의 배열 인덱스를 세 번째 인수로 전달하여 설정할 수 있습니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex
);
```



또한, `choice` 메서드는 유효한 응답을 선택하기 위한 최대 시도 횟수와 여러 선택이 허용되는지 여부를 결정하기 위해 선택적인 네 번째 및 다섯 번째 인수를 허용합니다:

```php
$name = $this->choice(
    'What is your name?',
    ['Taylor', 'Dayle'],
    $defaultIndex,
    $maxAttempts = null,
    $allowMultipleSelections = false
);
```



<a name="writing-output"></a>
### 출력 작성

출력을 콘솔로 보내려면 `line`, `newLine`, `info`, `comment`, `question`, `warn`, `alert` 및 `error` 메서드를 사용할 수 있습니다. 이들 각각의 메서드는 해당 목적에 맞는 ANSI 색상을 사용할 것입니다. 예를 들어, 사용자에게 일반 정보를 표시해 봅시다. 일반적으로 `info` 메서드는 콘솔에 초록색 텍스트로 표시됩니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    // ...

    $this->info('The command was successful!');
}
```



오류 메시지를 표시하려면 `error` 메서드를 사용하세요. 오류 메시지 텍스트는 일반적으로 빨간색으로 표시됩니다:

```php
$this->error('Something went wrong!');
```



일반 색상이 없는 텍스트를 표시하려면 `line` 방법을 사용할 수 있습니다:

```php
$this->line('Display this on the screen');
```



빈 줄을 표시하기 위해 `newLine` 방법을 사용할 수 있습니다:

```php
// Write a single blank line...
$this->newLine();

// Write three blank lines...
$this->newLine(3);
```



<a name="tables"></a>
#### 테이블

`table` 메서드는 여러 행/열의 데이터를 올바르게 형식화하는 것을 쉽게 만들어 줍니다. 필요한 것은 테이블의 열 이름과 데이터를 제공하는 것뿐이며, Laravel이 자동으로 테이블에 적절한 너비와 높이를 계산해 줍니다:

```php
use App\Models\User;

$this->table(
    ['Name', 'Email'],
    User::all(['name', 'email'])->toArray()
);
```



<a name="progress-bars"></a>
#### 진행 표시줄

오래 걸리는 작업의 경우, 작업이 얼마나 완료되었는지 사용자에게 알려주는 진행 표시줄을 보여주는 것이 도움이 될 수 있습니다. `withProgressBar` 방법을 사용하면 Laravel은 진행 표시줄을 표시하고 주어진 반복 가능한 값에 대해 각 반복마다 진행 상황을 갱신합니다:

```php
use App\Models\User;

$users = $this->withProgressBar(User::all(), function (User $user) {
    $this->performTask($user);
});
```



때때로 진행률 표시줄을 어떻게 진행시킬지에 대해 더 많은 수동 제어가 필요할 수 있습니다. 먼저 프로세스가 반복할 전체 단계 수를 정의합니다. 그런 다음 각 항목을 처리한 후 진행률 표시줄을 진행시킵니다:

```php
$users = App\Models\User::all();

$bar = $this->output->createProgressBar(count($users));

$bar->start();

foreach ($users as $user) {
    $this->performTask($user);

    $bar->advance();
}

$bar->finish();
```



> [!NOTE]
> 보다 고급 옵션은 [Symfony 진행 표시줄 컴포넌트 문서](https://symfony.com/doc/current/components/console/helpers/progressbar.html)를 확인하세요.

<a name="registering-commands"></a>
## 명령어 등록

기본적으로 Laravel은 `app/Console/Commands` 디렉토리 내의 모든 명령어를 자동으로 등록합니다. 그러나 애플리케이션의 `bootstrap/app.php` 파일에서 `withCommands` 메서드를 사용하여 Laravel이 다른 디렉토리에서 Artisan 명령어를 검색하도록 지시할 수 있습니다:

```php
->withCommands([
    __DIR__.'/../app/Domain/Orders/Commands',
])
```



필요한 경우, `withCommands` 메서드에 명령어의 클래스 이름을 제공하여 명령어를 수동으로 등록할 수도 있습니다:

```php
use App\Domain\Orders\Commands\SendEmails;

->withCommands([
    SendEmails::class,
])
```



아티산트(Artisan)가 부팅되면, 애플리케이션의 모든 명령어는 [서비스 컨테이너](/docs/{{version}}/container)에 의해 해결되고 Artisan에 등록됩니다.

<a name="programmatically-executing-commands"></a>
## 프로그램을 통해 명령어 실행

때때로 CLI 외부에서 Artisan 명령어를 실행하고자 할 수 있습니다. 예를 들어, 라우트나 컨트롤러에서 Artisan 명령어를 실행하고 싶을 수도 있습니다. 이를 위해 `Artisan` 파사드에서 `call` 메서드를 사용할 수 있습니다. `call` 메서드는 첫 번째 인수로 명령어의 시그니처 이름이나 클래스 이름을, 두 번째 인수로 명령어 매개변수 배열을 받습니다. 종료 코드는 반환됩니다.

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    $exitCode = Artisan::call('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```



또는 전체 Artisan 명령어를 문자열로 `call` 메서드에 전달할 수 있습니다:

```php
Artisan::call('mail:send 1 --queue=default');
```



<a name="passing-array-values"></a>
#### 배열 값 전달

명령이 배열을 허용하는 옵션을 정의하는 경우, 해당 옵션에 값의 배열을 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/mail', function () {
    $exitCode = Artisan::call('mail:send', [
        '--id' => [5, 13]
    ]);
});
```



<a name="passing-boolean-values"></a>
#### 불리언 값 전달

문자열 값을 허용하지 않는 옵션의 값을 지정해야 하는 경우, 예를 들어 `migrate:refresh` 명령어의 `--force` 플래그와 같은 경우, 옵션의 값으로 `true` 또는 `false`를 전달해야 합니다:

```php
$exitCode = Artisan::call('migrate:refresh', [
    '--force' => true,
]);
```



<a name="queueing-artisan-commands"></a>
#### Artisan 명령 대기열에 추가하기

`Artisan` 퍼사드에서 `queue` 메서드를 사용하여 Artisan 명령을 대기열에 추가하여 [큐 작업자](/docs/{{version}}/queues)가 백그라운드에서 처리하도록 할 수 있습니다. 이 메서드를 사용하기 전에 큐를 설정하고 큐 리스너를 실행 중인지 확인하세요:

```php
use Illuminate\Support\Facades\Artisan;
use Illuminate\Support\Facades\Route;

Route::post('/user/{user}/mail', function (string $user) {
    Artisan::queue('mail:send', [
        'user' => $user, '--queue' => 'default'
    ]);

    // ...
});
```



`onConnection` 및 `onQueue` 방법을 사용하여 Artisan 명령을 전송할 연결 또는 큐를 지정할 수 있습니다:

```php
Artisan::queue('mail:send', [
    'user' => 1, '--queue' => 'default'
])->onConnection('redis')->onQueue('commands');
```



<a name="calling-commands-from-other-commands"></a>
### 다른 명령어에서 명령어 호출하기

가끔 기존 Artisan 명령어에서 다른 명령어를 호출하고 싶을 때가 있습니다. 이때 `call` 메서드를 사용할 수 있습니다. 이 `call` 메서드는 명령어 이름과 명령어 인수/옵션 배열을 받습니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->call('mail:send', [
        'user' => 1, '--queue' => 'default'
    ]);

    // ...
}
```



다른 콘솔 명령을 호출하고 그 출력물을 모두 숨기고 싶다면 `callSilently` 메서드를 사용할 수 있습니다. `callSilently` 메서드는 `call` 메서드와 동일한 시그니처를 가지고 있습니다:

```php
$this->callSilently('mail:send', [
    'user' => 1, '--queue' => 'default'
]);
```



<a name="signal-handling"></a>
## 신호 처리

알다시피 운영 체제는 실행 중인 프로세스에 신호를 보낼 수 있습니다. 예를 들어, `SIGTERM` 신호는 운영 체제가 프로그램에 정상적으로 종료하라고 요청하는 방법입니다. Artisan 콘솔 명령에서 신호를 수신하고 신호가 발생할 때 코드를 실행하려면, `trap` 메서드를 사용할 수 있습니다:

```php
/**
 * Execute the console command.
 */
public function handle(): void
{
    $this->trap(SIGTERM, fn () => $this->shouldKeepRunning = false);

    while ($this->shouldKeepRunning) {
        // ...
    }
}
```



여러 신호를 동시에 듣기 위해, `trap` 메서드에 신호 배열을 제공할 수 있습니다:

```php
$this->trap([SIGTERM, SIGQUIT], function (int $signal) {
    $this->shouldKeepRunning = false;

    dump($signal); // SIGTERM / SIGQUIT
});
```



<a name="the-dev-command"></a>
## 개발 명령어

`dev` Artisan 명령어는 단일 터미널 창에서 로컬 개발에 필요한 모든 프로세스를 시작합니다. 기본적으로 PHP 개발 서버, 큐 작업자, [Pail](/docs/{{version}}/logging#tailing-log-messages-using-pail)을 통한 로그 추적, Vite 자산 컴파일을 동시에 실행합니다:

```shell
php artisan dev
```



Under the hood, the `dev` command uses the `@laravel/multiplex` npm package to manage the processes, giving each process its own tab with searchable, scrollable output. Each process is labeled and color-coded so you can easily distinguish between them. If a process crashes, it will be restarted automatically, and when you quit, all of the output is written back to your terminal so nothing is lost.

> [!NOTE]
> The `dev` command requires Node 22.13 or later. On Windows, it falls back to the `concurrently` npm package and the tabbed interface is not available.

The default processes are:

| Name | Command |
| --- | --- |
| `server` | `php artisan serve --host=localhost` |
| `queue` | `php artisan queue:listen --tries=1 --timeout=0` |
| `logs` | `php artisan pail --timeout=0` |
| `vite` | `npm run dev` |

> [!NOTE]
> The `vite` process automatically detects your Node package manager (npm, pnpm, Yarn, or Bun) and uses the appropriate run command.

<a name="customizing-dev-processes"></a>
### Customizing Dev Processes

You may customize the processes that the `dev` command runs by using the `DevCommands` class, typically within the `boot` method of your application's `AppServiceProvider`. The `register` method accepts a command string and an optional name:

```php
use Illuminate\Foundation\DevCommands;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    DevCommands::register('some-command --flag', 'my-process');
}
```



아티즌 명령을 등록할 때 명령어에 자동으로 접두사 `php artisan`를 붙이는 `artisan` 메서드를 사용할 수 있습니다:

```php
DevCommands::artisan('horizon', 'horizon');
```



마찬가지로, `node` 방법은 명령어 앞에 감지된 패키지 관리자의 실행 명령어를 붙이고(e.g. `npm run`), `nodeExec` 방법은 명령어 앞에 패키지 관리자의 exec 명령어를 붙입니다(e.g. `npx`):

```php
DevCommands::node('storybook', 'storybook');

DevCommands::nodeExec('tailwindcss -i resources/css/app.css -o public/css/app.css --watch', 'tailwind');
```



기본 프로세스와 동일한 이름으로 프로세스를 등록하면, 해당 프로세스가 기본 프로세스를 대체하게 됩니다. 예를 들어, 서버 프로세스를 다른 포트를 사용하도록 사용자 지정할 수 있습니다:

```php
DevCommands::artisan('serve --host=localhost --port=9000', 'server');
```



터미널에서 프로세스 라벨의 색상을 사용자 정의할 수도 있습니다. 사용 가능한 색상 방법은 `blue`, `purple`, `pink`, `orange`, `green`, `yellow`입니다. 또한 `color` 메서드에 사용자 정의 16진수 색상을 전달할 수도 있습니다:

```php
DevCommands::register('my-command', 'my-process')->green();

DevCommands::register('my-command', 'my-process')->color('#ff6347');
```



등록된 모든 개발 프로세스를 시작하지 않고 보려면 `dev:list` 명령어를 사용하세요:

```shell
php artisan dev:list
```



<a name="restarting-failed-processes"></a>
#### 실패한 프로세스 재시작

프로세스가 충돌하면, Laravel은 짧은 지연 후 최대 다섯 번까지 프로세스를 재시작한 뒤 실패로 표시합니다. 시작한 지 1초 이내에 종료된 프로세스는 처음부터 성공적으로 시작되지 않았을 가능성이 높기 때문에 재시작되지 않습니다. `r`로 프로세스를 수동으로 재시작하면 카운터가 초기화됩니다.

단일 실행에 대해 이 동작을 비활성화하려면 `--no-restart` 옵션을 사용할 수 있습니다:

```shell
php artisan dev --no-restart
```



또는 `disableAutoRestart` 방법을 사용하여 애플리케이션 전체에 대해 비활성화할 수 있습니다:

```php
DevCommands::disableAutoRestart();
```



<a name="filtering-dev-processes"></a>
### 개발 프로세스 필터링

`dev` 명령어가 호출될 때 특정 프로세스만 실행하도록 `only` 방법을 사용하여 지시할 수 있습니다. 마찬가지로 `except` 방법을 사용하여 특정 프로세스를 제외할 수도 있습니다:

```php
// Only run the server and vite processes...
DevCommands::only('server', 'vite');

// Run all processes except the queue worker...
DevCommands::except('queue');
```



`withoutVendorCommands` 및 `withoutDefaultCommands` 메서드를 사용하여 패키지에서 등록한 명령어나 Laravel의 기본 명령어를 제외할 수 있습니다:

```php
DevCommands::withoutVendorCommands();

DevCommands::withoutDefaultCommands();
```



<a name="stub-customization"></a>
## 스텁 커스터마이징

Artisan 콘솔의 `make` 명령어는 컨트롤러, 잡, 마이그레이션, 테스트 등 다양한 클래스를 생성하는 데 사용됩니다. 이러한 클래스들은 입력한 값에 따라 채워지는 "스텁" 파일을 사용하여 생성됩니다. 그러나 Artisan이 생성한 파일에 작은 변경을 하고 싶을 수 있습니다. 이를 위해 `stub:publish` 명령어를 사용하여 가장 일반적인 스텁을 애플리케이션에 게시하고 이를 커스터마이즈할 수 있습니다:

```shell
php artisan stub:publish
```

게시된 스텁은 애플리케이션 루트의 `stubs` 디렉토리 내에 위치하게 됩니다. 이 스텁에 가한 모든 변경 사항은 Artisan의 `make` 명령어를 사용하여 해당 클래스들을 생성할 때 반영됩니다.

<a name="events"></a>
## 이벤트

Artisan은 명령을 실행할 때 세 가지 이벤트를 발생시킵니다: `Illuminate\Console\Events\ArtisanStarting`, `Illuminate\Console\Events\CommandStarting`, 그리고 `Illuminate\Console\Events\CommandFinished`. `ArtisanStarting` 이벤트는 Artisan이 실행되기 시작할 때 즉시 발생합니다. 다음으로, `CommandStarting` 이벤트는 명령이 실행되기 직전에 발생합니다. 마지막으로, `CommandFinished` 이벤트는 명령 실행이 완료되면 발생합니다.
{% endraw %}
