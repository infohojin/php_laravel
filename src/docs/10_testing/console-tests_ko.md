---
layout: docs
title: "콘솔 테스트"
---

{% raw %}
# 콘솔 테스트

- [소개](#introduction)
- [성공 / 실패 기대](#success-failure-expectations)
- [입력 / 출력 기대](#input-output-expectations)
- [콘솔 이벤트](#console-events)

<a name="introduction"></a>
## 소개

HTTP 테스트를 단순화하는 것 외에도, Laravel은 애플리케이션의 [맞춤 콘솔 명령어](/docs/{{version}}/artisan)를 테스트하기 위한 간단한 API를 제공합니다.

<a name="success-failure-expectations"></a>
## 성공 / 실패 기대

시작하려면, Artisan 명령어의 종료 코드에 관한 단언(assertion)을 만드는 방법을 살펴보겠습니다. 이를 위해, 테스트에서 Artisan 명령어를 호출하기 위해 `artisan` 메서드를 사용할 것입니다. 그런 다음, 명령어가 특정 종료 코드로 완료되었는지 단언하기 위해 `assertExitCode` 메서드를 사용할 것입니다:

```

php tab=Pest
test('console command', function () {
    $this->artisan('inspire')->assertExitCode(0);
});

```

```

php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('inspire')->assertExitCode(0);
}

```

다음과 같이 명령이 특정 종료 코드로 종료되지 않았음을 주장하기 위해 `assertNotExitCode` 방법을 사용할 수 있습니다:

```php
$this->artisan('inspire')->assertNotExitCode(1);

```

물론, 모든 터미널 명령어는 일반적으로 성공하면 `0` 상태 코드로 종료되고, 성공하지 못하면 0이 아닌 종료 코드로 종료됩니다. 따라서 편의를 위해, 주어진 명령어가 성공적인 종료 코드로 종료되었는지 여부를 확인하기 위해 `assertSuccessful` 및 `assertFailed` 어설션을 사용할 수 있습니다:

```php
$this->artisan('inspire')->assertSuccessful();

$this->artisan('inspire')->assertFailed();

```

<a name="input-output-expectations"></a>
## 입력 / 출력 기대치

Laravel은 `expectsQuestion` 메서드를 사용하여 콘솔 명령어에 대한 사용자 입력을 쉽게 "모의(mock)"할 수 있게 해줍니다. 또한, `assertExitCode` 및 `expectsOutput` 메서드를 사용하여 콘솔 명령어에서 출력될 것으로 예상되는 종료 코드와 텍스트를 지정할 수 있습니다. 예를 들어, 다음 콘솔 명령어를 고려해 보십시오:

```php
Artisan::command('question', function () {
    $name = $this->ask('What is your name?');

    $language = $this->choice('Which language do you prefer?', [
        'PHP',
        'Ruby',
        'Python',
    ]);

    $this->line('Your name is '.$name.' and you prefer '.$language.'.');
});

```

다음 테스트로 이 명령을 시험해 볼 수 있습니다:

```

php tab=Pest
test('console command', function () {
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
});

```

```

php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('question')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('Which language do you prefer?', 'PHP')
        ->expectsOutput('Your name is Taylor Otwell and you prefer PHP.')
        ->doesntExpectOutput('Your name is Taylor Otwell and you prefer Ruby.')
        ->assertExitCode(0);
}

```

만약 [Laravel Prompts](/docs/{{version}}/prompts)가 제공하는 `search` 또는 `multisearch` 함수를 사용하고 있다면, `expectsSearch` 단정을 사용하여 사용자의 입력, 검색 결과 및 선택을 모의할 수 있습니다:

```

php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
});

```

```

php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsSearch('What is your name?', search: 'Tay', answers: [
            'Taylor Otwell',
            'Taylor Swift',
            'Darian Taylor'
        ], answer: 'Taylor Otwell')
        ->assertExitCode(0);
}

```

콘솔 명령어가 `doesntExpectOutput` 방법을 사용하여 아무 출력도 생성하지 않는다고 단언할 수도 있습니다:

```

php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
});

```

```

php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->doesntExpectOutput()
        ->assertExitCode(0);
}

```



`expectsOutputToContain` 및 `doesntExpectOutputToContain` 메서드는 출력의 일부에 대해 단언을 수행하는 데 사용할 수 있습니다:

```

php tab=Pest
test('console command', function () {
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
});

```

```

php tab=PHPUnit
/**
 * Test a console command.
 */
public function test_console_command(): void
{
    $this->artisan('example')
        ->expectsOutputToContain('Taylor')
        ->assertExitCode(0);
}

```

<a name="confirmation-expectations"></a>
#### 확인 기대치

"예" 또는 "아니오" 형태의 확인을 기대하는 명령을 작성할 때, `expectsConfirmation` 방법을 사용할 수 있습니다:

```php
$this->artisan('module:import')
    ->expectsConfirmation('Do you really wish to run this command?', 'no')
    ->assertExitCode(1);

```

<a name="table-expectations"></a>
#### 테이블 기대사항

명령이 Artisan의 `table` 방법을 사용하여 정보 테이블을 표시하는 경우, 전체 테이블에 대한 출력 기대를 작성하는 것은 번거로울 수 있습니다. 대신 `expectsTable` 방법을 사용할 수 있습니다. 이 방법은 테이블의 헤더를 첫 번째 인수로, 테이블의 데이터를 두 번째 인수로 받습니다:

```php
$this->artisan('users:all')
    ->expectsTable([
        'ID',
        'Email',
    ], [
        [1, 'taylor@example.com'],
        [2, 'abigail@example.com'],
    ]);

```

<a name="console-events"></a>
## 콘솔 이벤트

기본적으로, 애플리케이션의 테스트를 실행하는 동안 `Illuminate\Console\Events\CommandStarting` 및 `Illuminate\Console\Events\CommandFinished` 이벤트는 발생되지 않습니다. 그러나 해당 테스트 클래스에 `Illuminate\Foundation\Testing\WithConsoleEvents` 트레이트를 추가하여 이 이벤트들을 활성화할 수 있습니다:

```

php tab=Pest
<?php

use Illuminate\Foundation\Testing\WithConsoleEvents;

pest()->use(WithConsoleEvents::class);

// ...

```

```

php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\WithConsoleEvents;
use Tests\TestCase;

class ConsoleEventTest extends TestCase
{
    use WithConsoleEvents;

    // ...
}

```
{% endraw %}
