---
layout: docs
title: "과정"
---

{% raw %}
# 과정

- [소개](#introduction)
- [소환 과정](#invoking-processes)
- 프로세스 옵션 (#process-options)
- 프로세스 출력 (#process-output)
- [파이프라인](#process-pipelines)
- [비동기 프로세스](#asynchronous-processes)
- [프로세스 ID 및 신호](#process-ids-and-signals)
- [비동기 프로세스 출력](#asynchronous-process-output)
- [비동기 프로세스 시간 초과](#asynchronous-process-timeouts)
- [동시 프로세스](#concurrent-processes)
- [명명 풀 프로세스](#naming-pool-processes)
- [풀 프로세스 ID 및 신호](#pool-process-ids-and-signals)
- 테스팅 (#testing)
- [Faking Processes](#faking-processes)
- [Faking Specific Processes](#faking-specific-processes)
- [Faking Process Sequences](#faking-process-sequences)
- [Faking Asynchronous Process Lifecycle](#faking-asynchronous-process-lifecycles)
- [사용 가능한 주장](#available-assertions)
- [방황 프로세스 방지](#preventing-stray-processes)

<a name="introduction"></a>
## 소개

Laravel 은 [Symphony Process 구성 요소](https://symfony.com/doc/current/components/process.html) 를 중심으로 표현력 있고 최소한의 API 를 제공하므로 Laravel 애플리케이션에서 외부 프로세스를 편리하게 호출할 수 있습니다. Laravel 의 프로세스 기능은 가장 일반적인 사용 사례와 훌륭한 개발자 경험에 중점을 둡니다。

<a name="invoking-processes"></a>
## 호출 프로세스

프로세스를 호출하려면 `Process` 패싯에서 제공하는 `run` 및 `start` 메서드를 사용할 수 있습니다. `run` 메서드는 프로세스를 호출하고 프로세스 실행이 완료될 때까지 기다리는 반면， `start` 메서드는 비동기식 프로세스 실행에 사용됩니다. 이 설명서에서는 두 가지 접근 방식을 모두 검토합니다. 먼저 기본적인 동기식 프로세스를 호출하는 방법과 그 결과를 검사하는 방법을 살펴보겠습니다：

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

return $result->output();
```



물론, `run` 메서드가 반환하는 `Illuminate\Contracts\Process\ProcessResult` 인스턴스는 프로세스 결과를 검사하는 데 사용할 수 있는 다양한 유용한 메서드를 제공합니다:

```php
$result = Process::run('ls -la');

$result->command();
$result->successful();
$result->failed();
$result->output();
$result->errorOutput();
$result->exitCode();
```



<a name="throwing-exceptions"></a>
#### 예외 던지기

프로세스 결과를 가지고 있고 종료 코드가 0보다 큰 경우(즉, 실패를 나타내는 경우) `Illuminate\Process\Exceptions\ProcessFailedException` 인스턴스를 던지고 싶다면 `throw` 및 `throwIf` 메서드를 사용할 수 있습니다. 프로세스가 실패하지 않았다면 `ProcessResult` 인스턴스가 반환됩니다:

```php
$result = Process::run('ls -la')->throw();

$result = Process::run('ls -la')->throwIf($condition);
```



<a name="process-options"></a>
### 프로세스 옵션

물론, 프로세스를 호출하기 전에 프로세스의 동작을 사용자 정의해야 할 수도 있습니다. 다행히도, Laravel은 작업 디렉토리, 타임아웃, 환경 변수와 같은 다양한 프로세스 기능을 조정할 수 있도록 허용합니다.

<a name="working-directory-path"></a>
#### 작업 디렉토리 경로

프로세스의 작업 디렉토리를 지정하려면 `path` 메서드를 사용할 수 있습니다. 이 메서드가 호출되지 않으면, 프로세스는 현재 실행 중인 PHP 스크립트의 작업 디렉토리를 상속받습니다:

```php
$result = Process::path(__DIR__)->run('ls -la');
```



<a name="input"></a>
#### 입력

`input` 방법을 사용하여 프로세스의 "표준 입력"을 통해 입력을 제공할 수 있습니다:

```php
$result = Process::input('Hello World')->run('cat');
```



<a name="timeouts"></a>
#### 타임아웃

기본적으로, 프로세스는 60초 이상 실행된 후 `Illuminate\Process\Exceptions\ProcessTimedOutException`의 인스턴스를 던집니다. 그러나 `timeout` 메서드를 통해 이 동작을 사용자 정의할 수 있습니다:

```php
$result = Process::timeout(120)->run('bash import.sh');
```



`timeout` 및 `idleTimeout` 방법은 `CarbonInterval` 인스턴스도 허용합니다:

```php
use function Illuminate\Support\minutes;

$result = Process::timeout(minutes(2))->run('bash import.sh');
```



또는, 프로세스 시간 초과를 완전히 비활성화하고 싶다면, `forever` 메서드를 호출할 수 있습니다:

```php
$result = Process::forever()->run('bash import.sh');
```



`idleTimeout` 방법은 프로세스가 아무 출력도 반환하지 않고 실행될 수 있는 최대 초 수를 지정하는 데 사용할 수 있습니다:

```php
$result = Process::timeout(60)->idleTimeout(30)->run('bash import.sh');
```



<a name="environment-variables"></a>
#### 환경 변수

환경 변수는 `env` 방식을 통해 프로세스에 제공될 수 있습니다. 호출된 프로세스는 또한 시스템에 의해 정의된 모든 환경 변수를 상속받습니다:

```php
$result = Process::forever()
    ->env(['IMPORT_PATH' => __DIR__])
    ->run('bash import.sh');
```



호출된 프로세스에서 상속된 환경 변수를 제거하려면 해당 환경 변수에 `false` 값을 제공할 수 있습니다:

```php
$result = Process::forever()
    ->env(['LOAD_PATH' => false])
    ->run('bash import.sh');
```



<a name="tty-mode"></a>
#### TTY 모드

`tty` 메서드는 프로세스에 대해 TTY 모드를 활성화하는 데 사용할 수 있습니다. TTY 모드는 프로세스의 입력과 출력을 프로그램의 입력과 출력에 연결하여, 프로세스가 Vim이나 Nano와 같은 편집기를 프로세스로 열 수 있도록 합니다:

```php
Process::forever()->tty()->run('vim');
```



> [!WARNING]
> TTY 모드는 Windows에서 지원되지 않습니다.

<a name="process-output"></a>
### 프로세스 출력

앞서 논의한 바와 같이, 프로세스 출력은 프로세스 결과에서 `output`(stdout) 및 `errorOutput`(stderr) 메서드를 사용하여 접근할 수 있습니다:

```php
use Illuminate\Support\Facades\Process;

$result = Process::run('ls -la');

echo $result->output();
echo $result->errorOutput();
```



그러나 `run` 메서드의 두 번째 인수로 클로저를 전달하여 출력을 실시간으로 수집할 수도 있습니다. 클로저는 두 개의 인수를 받습니다: 출력의 "타입"(`stdout` 또는 `stderr`)과 출력 문자열 자체:

```php
$result = Process::run('ls -la', function (string $type, string $output) {
    echo $output;
});
```



Laravel은 또한 `seeInOutput` 및 `seeInErrorOutput` 메서드를 제공하며, 이는 주어진 문자열이 프로세스의 출력에 포함되었는지 여부를 편리하게 확인할 수 있는 방법을 제공합니다:

```php
if (Process::run('ls -la')->seeInOutput('laravel')) {
    // ...
}
```



<a name="disabling-process-output"></a>
#### 프로세스 출력 비활성화

프로세스가 관심 없는 상당한 양의 출력을 생성하고 있다면, 출력 검색을 완전히 비활성화하여 메모리를 절약할 수 있습니다. 이를 수행하려면 프로세스를 구성할 때 `quietly` 메서드를 호출하십시오:

```php
use Illuminate\Support\Facades\Process;

$result = Process::quietly()->run('bash import.sh');
```



<a name="process-pipelines"></a>
### 파이프라인

때때로 한 프로세스의 출력을 다른 프로세스의 입력으로 만들고 싶을 때가 있습니다. 이는 종종 프로세스의 출력을 다른 프로세스로 '파이핑'한다고 합니다. `Process` 퍼사드가 제공하는 `pipe` 메서드는 이를 쉽게 수행할 수 있게 해줍니다. `pipe` 메서드는 파이프된 프로세스를 동기식으로 실행하고 파이프라인의 마지막 프로세스 결과를 반환합니다:

```php
use Illuminate\Process\Pipe;
use Illuminate\Support\Facades\Process;

$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
});

if ($result->successful()) {
    // ...
}
```



파이프라인을 구성하는 개별 프로세스를 사용자 정의할 필요가 없다면 `pipe` 메서드에 명령 문자열 배열을 전달하기만 하면 됩니다:

```php
$result = Process::pipe([
    'cat example.txt',
    'grep -i "laravel"',
]);
```



프로세스 출력은 `pipe` 메서드의 두 번째 인수로 클로저를 전달하여 실시간으로 수집할 수 있습니다. 클로저는 두 개의 인수를 받습니다: 출력의 "유형"(`stdout` 또는 `stderr`)과 출력 문자열 자체:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->command('cat example.txt');
    $pipe->command('grep -i "laravel"');
}, function (string $type, string $output) {
    echo $output;
});
```



Laravel은 또한 `as` 메서드를 통해 파이프라인 내 각 프로세스에 문자열 키를 할당할 수 있습니다. 이 키는 `pipe` 메서드에 제공된 출력 클로저에도 전달되어, 출력이 어떤 프로세스에 속하는지 결정할 수 있습니다:

```php
$result = Process::pipe(function (Pipe $pipe) {
    $pipe->as('first')->command('cat example.txt');
    $pipe->as('second')->command('grep -i "laravel"');
}, function (string $type, string $output, string $key) {
    // ...
});
```



<a name="asynchronous-processes"></a>
## 비동기 프로세스

`run` 메서드는 프로세스를 동기적으로 호출하는 반면, `start` 메서드는 프로세스를 비동기적으로 호출하는 데 사용할 수 있습니다. 이를 통해 프로세스가 백그라운드에서 실행되는 동안 애플리케이션이 다른 작업을 계속 수행할 수 있습니다. 프로세스가 호출된 후에는 `running` 메서드를 이용하여 프로세스가 아직 실행 중인지 확인할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    // ...
}

$result = $process->wait();
```



아시다시피, 프로세스 실행이 끝날 때까지 기다리고 `ProcessResult` 인스턴스를 가져오기 위해 `wait` 메서드를 호출할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

// ...

$result = $process->wait();
```



<a name="process-ids-and-signals"></a>
### 프로세스 ID 및 신호

`id` 메서드는 실행 중인 프로세스의 운영 체제에서 할당한 프로세스 ID를 가져오는 데 사용할 수 있습니다:

```php
$process = Process::start('bash import.sh');

return $process->id();
```



실행 중인 프로세스에 '신호'를 보내기 위해 `signal` 방법을 사용할 수 있습니다. 미리 정의된 신호 상수 목록은 [PHP 문서](https://www.php.net/manual/en/pcntl.constants.php)에서 찾을 수 있습니다:

```php
$process->signal(SIGUSR2);
```



<a name="asynchronous-process-output"></a>
### 비동기 프로세스 출력

비동기 프로세스가 실행되는 동안, `output` 및 `errorOutput` 메서드를 사용하여 현재 출력 전체에 접근할 수 있습니다. 그러나 `latestOutput` 및 `latestErrorOutput`를 사용하면 마지막으로 출력을 가져온 이후 발생한 프로세스의 출력을 접근할 수 있습니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    echo $process->latestOutput();
    echo $process->latestErrorOutput();

    sleep(1);
}
```



`run` 방식과 마찬가지로, `start` 메서드에 클로저를 두 번째 인수로 전달함으로써 비동기 프로세스에서 실시간으로 출력도 수집할 수 있습니다. 클로저는 두 개의 인수를 받게 됩니다: 출력의 "형식"(`stdout` 또는 `stderr`)과 출력 문자열 자체:

```php
$process = Process::start('bash import.sh', function (string $type, string $output) {
    echo $output;
});

$result = $process->wait();
```



프로세스가 완료될 때까지 기다리는 대신, 프로세스의 출력에 따라 기다림을 중지하기 위해 `waitUntil` 방법을 사용할 수 있습니다. `waitUntil` 방법에 주어진 클로저가 `true`를 반환하면 Laravel은 프로세스가 완료될 때까지 기다리는 것을 중단합니다:

```php
$process = Process::start('bash import.sh');

$process->waitUntil(function (string $type, string $output) {
    return $output === 'Ready...';
});
```



<a name="asynchronous-process-timeouts"></a>
### 비동기 프로세스 타임아웃

비동기 프로세스가 실행되는 동안, `ensureNotTimedOut` 메서드를 사용하여 프로세스가 타임아웃되지 않았는지 확인할 수 있습니다. 이 메서드는 프로세스가 타임아웃된 경우 [타임아웃 예외](#timeouts)를 발생시킵니다:

```php
$process = Process::timeout(120)->start('bash import.sh');

while ($process->running()) {
    $process->ensureNotTimedOut();

    // ...

    sleep(1);
}
```



<a name="concurrent-processes"></a>
## 동시 프로세스

Laravel은 또한 동시 비동기 프로세스 풀을 쉽게 관리할 수 있게 해주므로, 많은 작업을 동시에 쉽게 실행할 수 있습니다. 시작하려면 `pool` 메서드를 호출하세요. 이 메서드는 `Illuminate\Process\Pool`의 인스턴스를 받는 클로저를 인수로 받습니다.

이 클로저 내에서 풀에 속하는 프로세스를 정의할 수 있습니다. `start` 메서드를 통해 프로세스 풀이 시작되면 `running` 메서드를 통해 실행 중인 프로세스의 [컬렉션](/docs/{{version}}/collections)에 접근할 수 있습니다.

```php
use Illuminate\Process\Pool;
use Illuminate\Support\Facades\Process;

$pool = Process::pool(function (Pool $pool) {
    $pool->path(__DIR__)->command('bash import-1.sh');
    $pool->path(__DIR__)->command('bash import-2.sh');
    $pool->path(__DIR__)->command('bash import-3.sh');
})->start(function (string $type, string $output, int $key) {
    // ...
});

while ($pool->running()->isNotEmpty()) {
    // ...
}

$results = $pool->wait();
```



보시다시피, 모든 풀 프로세스가 실행을 종료하고 `wait` 메서드를 통해 결과를 해결할 때까지 기다릴 수 있습니다. `wait` 메서드는 배열 접근이 가능한 객체를 반환하며, 이를 통해 풀에 있는 각 프로세스의 `ProcessResult` 인스턴스에 그 키로 접근할 수 있습니다:

```php
$results = $pool->wait();

echo $results[0]->output();
```



또는 편의를 위해 `concurrently` 방법을 사용하여 비동기 프로세스 풀을 시작하고 즉시 그 결과를 기다릴 수 있습니다. 이는 PHP의 배열 구조 분해 기능과 결합할 때 특히 표현력이 풍부한 구문을 제공할 수 있습니다:

```php
[$first, $second, $third] = Process::concurrently(function (Pool $pool) {
    $pool->path(__DIR__)->command('ls -la');
    $pool->path(app_path())->command('ls -la');
    $pool->path(storage_path())->command('ls -la');
});

echo $first->output();
```



<a name="naming-pool-processes"></a>
### 프로세스 풀 명명

숫자 키를 통해 프로세스 풀 결과에 접근하는 것은 매우 표현력이 떨어집니다; 따라서 Laravel은 `as` 메서드를 통해 풀 내 각 프로세스에 문자열 키를 할당하도록 허용합니다. 이 키는 또한 `start` 메서드에 제공된 클로저로 전달되어 출력이 어느 프로세스에 속하는지 확인할 수 있습니다:

```php
$pool = Process::pool(function (Pool $pool) {
    $pool->as('first')->command('bash import-1.sh');
    $pool->as('second')->command('bash import-2.sh');
    $pool->as('third')->command('bash import-3.sh');
})->start(function (string $type, string $output, string $key) {
    // ...
});

$results = $pool->wait();

return $results['first']->output();
```



<a name="pool-process-ids-and-signals"></a>
### 풀 프로세스 ID 및 시그널

프로세스 풀의 `running` 메서드는 풀 내에서 호출된 모든 프로세스의 컬렉션을 제공하므로, 기본 풀 프로세스 ID에 쉽게 접근할 수 있습니다:

```php
$processIds = $pool->running()->each->id();
```



편의를 위해, 프로세스 풀의 모든 프로세스에 신호를 보내기 위해 프로세스 풀에서 `signal` 메서드를 호출할 수 있습니다:

```php
$pool->signal(SIGUSR2);
```



<a name="testing"></a>
## 테스트

많은 Laravel 서비스는 테스트를 쉽게 그리고 표현력 있게 작성할 수 있도록 도와주는 기능을 제공하며, Laravel의 프로세스 서비스도 예외가 아닙니다. `Process` 페이사드의 `fake` 메서드를 사용하면 프로세스가 호출될 때 Laravel이 스텁 또는 더미 결과를 반환하도록 지시할 수 있습니다.

<a name="faking-processes"></a>
### 프로세스 가짜 만들기

Laravel의 프로세스 가짜 기능을 탐색하기 위해, 프로세스를 호출하는 라우트를 상상해 봅시다:

```php
use Illuminate\Support\Facades\Process;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    Process::run('bash import.sh');

    return 'Import complete!';
});
```



이 경로를 테스트할 때, 우리는 `Process` 퍼사드에서 인자를 주지 않고 `fake` 메서드를 호출함으로써 호출된 모든 프로세스에 대해 Laravel이 가짜의 성공적인 처리 결과를 반환하도록 지시할 수 있습니다. 또한, 특정 프로세스가 "실행됨"을 [확인](#available-assertions)할 수도 있습니다.```php tab=Pest
<?php

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;

test('process is invoked', function () {
    Process::fake();

    $response = $this->get('/import');

    // Simple process assertion...
    Process::assertRan('bash import.sh');

    // Or, inspecting the process configuration...
    Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
        return $process->command === 'bash import.sh' &&
               $process->timeout === 60;
    });
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Contracts\Process\ProcessResult;
use Illuminate\Process\PendingProcess;
use Illuminate\Support\Facades\Process;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_process_is_invoked(): void
    {
        Process::fake();

        $response = $this->get('/import');

        // Simple process assertion...
        Process::assertRan('bash import.sh');

        // Or, inspecting the process configuration...
        Process::assertRan(function (PendingProcess $process, ProcessResult $result) {
            return $process->command === 'bash import.sh' &&
                   $process->timeout === 60;
        });
    }
}
```



논의된 바와 같이, `Process` 퍼사드에서 `fake` 메서드를 호출하면 Laravel이 출력 없이 항상 성공적인 프로세스 결과를 반환하도록 지시합니다. 그러나 `Process` 퍼사드의 `result` 메서드를 사용하여 가짜 프로세스의 출력과 종료 코드를 쉽게 지정할 수 있습니다:

```php
Process::fake([
    '*' => Process::result(
        output: 'Test output',
        errorOutput: 'Test error output',
        exitCode: 1,
    ),
]);
```



<a name="faking-specific-processes"></a>
### 특정 프로세스 가장하기

이전 예제에서 보셨겠지만, `Process` 퍼사드는 `fake` 메서드에 배열을 전달하여 프로세스별로 서로 다른 가짜 결과를 지정할 수 있게 합니다.

배열의 키는 가장하고자 하는 명령 패턴과 그에 연관된 결과를 나타내야 합니다. `*` 문자는 와일드카드 문자로 사용될 수 있습니다. 가장되지 않은 프로세스 명령은 실제로 호출됩니다. 이러한 명령에 대한 스텁/가짜 결과를 구성하려면 `Process` 퍼사드의 `result` 메서드를 사용하실 수 있습니다:

```php
Process::fake([
    'cat *' => Process::result(
        output: 'Test "cat" output',
    ),
    'ls *' => Process::result(
        output: 'Test "ls" output',
    ),
]);
```



위조된 프로세스의 종료 코드나 오류 출력을 사용자 지정할 필요가 없다면, 단순한 문자열로 가짜 프로세스 결과를 지정하는 것이 더 편리할 수 있습니다:

```php
Process::fake([
    'cat *' => 'Test "cat" output',
    'ls *' => 'Test "ls" output',
]);
```



<a name="faking-process-sequences"></a>
### 프로세스 시퀀스 속이기

테스트 중인 코드가 동일한 명령으로 여러 프로세스를 호출하는 경우, 각 프로세스 호출에 서로 다른 가짜 프로세스 결과를 할당하고 싶을 수 있습니다. 이는 `Process` 패사드의 `sequence` 메서드를 통해 달성할 수 있습니다:

```php
Process::fake([
    'ls *' => Process::sequence()
        ->push(Process::result('First invocation'))
        ->push(Process::result('Second invocation')),
]);
```



<a name="faking-asynchronous-process-lifecycles"></a>
### 비동기 프로세스 수명 주기 흉내 내기

지금까지 우리는 주로 `run` 메서드를 사용하여 동기적으로 호출되는 프로세스를 흉내 내는 방법에 대해 논의했습니다. 그러나 `start`를 통해 호출되는 비동기 프로세스와 상호작용하는 코드를 테스트하려는 경우, 가짜 프로세스를 설명하는 보다 정교한 접근 방식이 필요할 수 있습니다.

예를 들어, 비동기 프로세스와 상호작용하는 다음 경로를 상상해 봅시다:

```php
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Route;

Route::get('/import', function () {
    $process = Process::start('bash import.sh');

    while ($process->running()) {
        Log::info($process->latestOutput());
        Log::info($process->latestErrorOutput());
    }

    return 'Done';
});
```



이 과정을 제대로 위조하려면 `running` 메서드가 `true`를 몇 번 반환해야 하는지 설명할 수 있어야 합니다. 또한 순서대로 반환되어야 하는 여러 출력 라인을 지정하고 싶을 수도 있습니다. 이를 달성하기 위해 `Process` 퍼사드의 `describe` 메서드를 사용할 수 있습니다:

```php
Process::fake([
    'bash import.sh' => Process::describe()
        ->output('First line of standard output')
        ->errorOutput('First line of error output')
        ->output('Second line of standard output')
        ->exitCode(0)
        ->iterations(3),
]);
```



위의 예제를 살펴봅시다. `output` 및 `errorOutput` 메서드를 사용하여 순서대로 반환될 여러 줄의 출력을 지정할 수 있습니다. `exitCode` 메서드는 가짜 프로세스의 최종 종료 코드를 지정하는 데 사용될 수 있습니다. 마지막으로, `iterations` 메서드는 `running` 메서드가 `true`를 몇 번 반환해야 하는지를 지정하는 데 사용할 수 있습니다.

<a name="available-assertions"></a>
### 사용 가능한 Assertions

[이전 토론](#faking-processes)에서 언급했듯이, Laravel은 기능 테스트를 위해 여러 프로세스 Assertions를 제공합니다. 아래에서 각 Assertions를 논의하겠습니다.

<a name="assert-process-ran"></a>
#### assertRan

주어진 프로세스가 호출되었는지 Assertions 합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRan('ls -la');
```



프로세스를 배열 인수로 호출한 경우, 동일한 배열을 검증(assertion)에 전달할 수 있습니다:

```php
Process::assertRan(['php', 'artisan', 'migrate']);
```



`assertRanTimes` 및 `assertDidntRun` 메서드 또한 배열 명령을 허용합니다.

`assertRan` 메서드는 클로저도 허용하며, 이 클로저는 프로세스 인스턴스와 프로세스 결과를 받아 프로세스의 구성 옵션을 확인할 수 있습니다. 이 클로저가 `true`을 반환하면, 어설션은 "통과"하게 됩니다.

```php
Process::assertRan(fn ($process, $result) =>
    $process->command === 'ls -la' &&
    $process->path === __DIR__ &&
    $process->timeout === 60
);
```



`assertRan` 클로저에 전달된 `$process`는 `Illuminate\Process\PendingProcess`의 인스턴스인 반면, `$result`는 `Illuminate\Contracts\Process\ProcessResult`의 인스턴스입니다.

<a name="assert-process-didnt-run"></a>
#### assertDidntRun

주어진 프로세스가 호출되지 않았음을 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertDidntRun('ls -la');
```



`assertRan` 방법과 마찬가지로, `assertDidntRun` 방법도 클로저를 받으며, 이 클로저는 프로세스 인스턴스와 프로세스 결과를 받아 프로세스에 설정된 옵션을 검사할 수 있게 합니다. 이 클로저가 `true`를 반환하면, 검증은 "실패"하게 됩니다:

```php
Process::assertDidntRun(fn (PendingProcess $process, ProcessResult $result) =>
    $process->command === 'ls -la'
);
```



<a name="assert-process-ran-times"></a>
#### assertRanTimes

주어진 프로세스가 지정된 횟수만큼 호출되었는지 확인합니다:

```php
use Illuminate\Support\Facades\Process;

Process::assertRanTimes('ls -la', times: 3);
```



`assertRanTimes` 메서드도 클로저를 받으며, 이 클로저는 `PendingProcess`와 `ProcessResult`의 인스턴스를 받아 프로세스의 구성 옵션을 검사할 수 있습니다. 이 클로저가 `true`를 반환하고 프로세스가 지정된 횟수만큼 호출되었다면, 어설션은 "통과"하게 됩니다.

```php
Process::assertRanTimes(function (PendingProcess $process, ProcessResult $result) {
    return $process->command === 'ls -la';
}, times: 3);
```



<a name="assert-processes-ran-in-order"></a>
#### assertRanInOrder

프로세스가 지정된 순서대로 호출되었는지 확인하십시오:

```php
Process::assertRanInOrder([
    'git fetch',
    'composer install',
]);
```



`assertRanInOrder` 메서드는 다른 프로세스 어서션처럼 명령 문자열, 명령 인수 배열 또는 클로저를 받을 수 있습니다.

<a name="preventing-stray-processes"></a>
### 떠돌이 프로세스 방지

개별 테스트나 전체 테스트 스위트에서 호출된 모든 프로세스가 가짜로 처리되었는지 확인하고 싶다면 `preventStrayProcesses` 메서드를 호출할 수 있습니다. 이 메서드를 호출한 후에는 해당 가짜 결과가 없는 모든 프로세스가 실제 프로세스를 시작하는 대신 예외를 발생시킵니다:

```php
use Illuminate\Support\Facades\Process;

Process::preventStrayProcesses();

Process::fake([
    'ls *' => 'Test output...',
]);

// Fake response is returned...
Process::run('ls -la');

// An exception is thrown...
Process::run('bash import.sh');
```
{% endraw %}
