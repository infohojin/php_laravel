---
layout: docs
title: "Task Scheduling"
---

{% raw %}
# Task Scheduling

- [Introduction](#introduction)
- [Defining Schedules](#defining-schedules)
    - [Scheduling Artisan Commands](#scheduling-artisan-commands)
    - [Scheduling Queued Jobs](#scheduling-queued-jobs)
    - [Scheduling Shell Commands](#scheduling-shell-commands)
    - [Schedule Frequency Options](#schedule-frequency-options)
    - [Timezones](#timezones)
    - [Preventing Task Overlaps](#preventing-task-overlaps)
    - [Running Tasks on One Server](#running-tasks-on-one-server)
    - [Background Tasks](#background-tasks)
    - [Maintenance Mode](#maintenance-mode)
    - [Pausing Scheduled Tasks](#pausing-scheduled-tasks)
    - [Schedule Groups](#schedule-groups)
- [Running the Scheduler](#running-the-scheduler)
    - [Sub-Minute Scheduled Tasks](#sub-minute-scheduled-tasks)
    - [Running the Scheduler Locally](#running-the-scheduler-locally)
- [Task Output](#task-output)
- [Task Hooks](#task-hooks)
- [Events](#events)

<a name="introduction"></a>
## Introduction

In the past, you may have written a cron configuration entry for each task you needed to schedule on your server. However, this can quickly become a pain because your task schedule is no longer in source control and you must SSH into your server to view your existing cron entries or add additional entries.

Laravel's command scheduler offers a fresh approach to managing scheduled tasks on your server. The scheduler allows you to fluently and expressively define your command schedule within your Laravel application itself. When using the scheduler, only a single cron entry is needed on your server. Your task schedule is typically defined in your application's `routes/console.php` file.

<a name="defining-schedules"></a>
## Defining Schedules

You may define all of your scheduled tasks in your application's `routes/console.php` file. To get started, let's take a look at an example. In this example, we will schedule a closure to be called every day at midnight. Within the closure we will execute a database query to clear a table:

```php
<?php

use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->daily();
```



클로저를 사용한 스케줄링 외에도 [호출 가능한 객체](https://secure.php.net/manual/en/language.oop5.magic.php#object.invoke)를 스케줄링할 수 있습니다. 호출 가능한 객체는 `__invoke` 메서드를 포함하는 간단한 PHP 클래스입니다:

```php
Schedule::call(new DeleteRecentUsers)->daily();
```



`routes/console.php` 파일을 명령 정의용으로만 예약하는 것을 선호하는 경우, 응용 프로그램의 `bootstrap/app.php` 파일에서 `withSchedule` 메서드를 사용하여 예약된 작업을 정의할 수 있습니다. 이 메서드는 스케줄러의 인스턴스를 받는 클로저를 허용합니다:

```php
use Illuminate\Console\Scheduling\Schedule;

->withSchedule(function (Schedule $schedule) {
    $schedule->call(new DeleteRecentUsers)->daily();
})
```



예약된 작업과 다음 실행 예정 시간을 개요로 보려면 `schedule:list` Artisan 명령을 사용할 수 있습니다:

```shell
php artisan schedule:list
```



<a name="scheduling-artisan-commands"></a>
### 아티즌 명령 예약

클로저 예약 외에도 [아티즌 명령](/docs/{{version}}/artisan) 및 시스템 명령을 예약할 수 있습니다. 예를 들어, `command` 메서드를 사용하여 명령의 이름이나 클래스를 사용하여 아티즌 명령을 예약할 수 있습니다.

명령 클래스 이름을 사용하여 아티즌 명령을 예약할 때, 명령이 호출될 때 전달되어야 하는 추가 명령줄 인수를 배열로 전달할 수 있습니다:

```php
use App\Console\Commands\SendEmailsCommand;
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send Taylor --force')->daily();

Schedule::command(SendEmailsCommand::class, ['Taylor', '--force'])->daily();
```



<a name="scheduling-artisan-closure-commands"></a>
#### 아티산 클로저 명령 스케줄링

클로저로 정의된 아티산 명령을 스케줄링하고 싶다면, 명령 정의 후 스케줄링 관련 메서드를 체이닝할 수 있습니다:

```php
Artisan::command('delete:recent-users', function () {
    DB::table('recent_users')->delete();
})->purpose('Delete recent users')->daily();
```



클로저 명령에 인수를 전달해야 하는 경우, `schedule` 메서드에 인수를 제공할 수 있습니다:

```php
Artisan::command('emails:send {user} {--force}', function ($user) {
    // ...
})->purpose('Send emails to the specified user')->schedule(['Taylor', '--force'])->daily();
```



<a name="scheduling-queued-jobs"></a>
### 대기 중인 작업 예약

`job` 메서드는 [대기 중인 작업](/docs/{{version}}/queues)을 예약하는 데 사용할 수 있습니다. 이 메서드는 작업을 대기열에 넣기 위해 클로저를 정의하는 `call` 메서드를 사용하지 않고도 대기 중인 작업을 예약할 수 있는 편리한 방법을 제공합니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

Schedule::job(new Heartbeat)->everyFiveMinutes();
```



선택적으로 두 번째 및 세 번째 인수를 `job` 메서드에 제공할 수 있으며, 이 인수들은 작업을 큐에 넣는 데 사용해야 하는 큐 이름과 큐 연결을 지정합니다:

```php
use App\Jobs\Heartbeat;
use Illuminate\Support\Facades\Schedule;

// Dispatch the job to the "heartbeats" queue on the "sqs" connection...
Schedule::job(new Heartbeat, 'heartbeats', 'sqs')->everyFiveMinutes();
```



<a name="scheduling-shell-commands"></a>
### 셸 명령 스케줄링

`exec` 방법은 운영 체제에 명령을 내리는 데 사용될 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::exec('node /home/forge/script.js')->daily();
```

<a name="schedule-frequency-options"></a>
### 일정 빈도 옵션

우리는 이미 특정 간격으로 작업이 실행되도록 작업을 구성하는 몇 가지 예를 보았습니다. 그러나 작업에 할당할 수 있는 더 많은 작업 일정 빈도가 있습니다:

<div class="overflow-auto">

| Method                             | Description                                              |
| ---------------------------------- | -------------------------------------------------------- |
| `->cron('* * * * *');`             | Run the task on a custom cron schedule.                  |
| `->everySecond();`                 | Run the task every second.                               |
| `->everyTwoSeconds();`             | Run the task every two seconds.                          |
| `->everyFiveSeconds();`            | Run the task every five seconds.                         |
| `->everyTenSeconds();`             | Run the task every ten seconds.                          |
| `->everyFifteenSeconds();`         | Run the task every fifteen seconds.                      |
| `->everyTwentySeconds();`          | Run the task every twenty seconds.                       |
| `->everyThirtySeconds();`          | Run the task every thirty seconds.                       |
| `->everyMinute();`                 | Run the task every minute.                               |
| `->everyTwoMinutes();`             | Run the task every two minutes.                          |
| `->everyThreeMinutes();`           | Run the task every three minutes.                        |
| `->everyFourMinutes();`            | Run the task every four minutes.                         |
| `->everyFiveMinutes();`            | Run the task every five minutes.                         |
| `->everyTenMinutes();`             | Run the task every ten minutes.                          |
| `->everyFifteenMinutes();`         | Run the task every fifteen minutes.                      |
| `->everyThirtyMinutes();`          | Run the task every thirty minutes.                       |
| `->hourly();`                      | Run the task every hour.                                 |
| `->hourlyAt(17);`                  | Run the task every hour at 17 minutes past the hour.     |
| `->everyOddHour($minutes = 0);`    | Run the task every odd hour.                             |
| `->everyTwoHours($minutes = 0);`   | Run the task every two hours.                            |
| `->everyThreeHours($minutes = 0);` | Run the task every three hours.                          |
| `->everyFourHours($minutes = 0);`  | Run the task every four hours.                           |
| `->everySixHours($minutes = 0);`   | Run the task every six hours.                            |
| `->daily();`                       | Run the task every day at midnight.                      |
| `->dailyAt('13:00');`              | Run the task every day at 13:00.                         |
| `->twiceDaily(1, 13);`             | Run the task daily at 1:00 & 13:00.                      |
| `->twiceDailyAt(1, 13, 15);`       | Run the task daily at 1:15 & 13:15.                      |
| `->daysOfMonth([1, 10, 20]);`      | Run the task on specific days of the month.              |
| `->weekly();`                      | Run the task every Sunday at 00:00.                      |
| `->weeklyOn(1, '8:00');`           | Run the task every week on Monday at 8:00.               |
| `->monthly();`                     | Run the task on the first day of every month at 00:00.   |
| `->monthlyOn(4, '15:00');`         | Run the task every month on the 4th at 15:00.            |
| `->twiceMonthly(1, 16, '13:00');`  | Run the task monthly on the 1st and 16th at 13:00.       |
| `->lastDayOfMonth('15:00');`       | Run the task on the last day of the month at 15:00.      |
| `->quarterly();`                   | Run the task on the first day of every quarter at 00:00. |
| `->quarterlyOn(4, '14:00');`       | Run the task every quarter on the 4th at 14:00.          |
| `->yearly();`                      | Run the task on the first day of every year at 00:00.    |
| `->yearlyOn(6, 1, '17:00');`       | Run the task every year on June 1st at 17:00.            |
| `->timezone('America/New_York');`  | Set the timezone for the task.                           |



</div>

이러한 방법들은 추가적인 제약과 결합되어 특정 요일에만 실행되는 더욱 세밀하게 조정된 스케줄을 만들 수 있습니다. 예를 들어, 명령을 매주 월요일에 실행되도록 스케줄할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

// Run once per week on Monday at 1 PM...
Schedule::call(function () {
    // ...
})->weekly()->mondays()->at('13:00');

// Run hourly from 8 AM to 5 PM on weekdays...
Schedule::command('foo')
    ->weekdays()
    ->hourly()
    ->timezone('America/Chicago')
    ->between('8:00', '17:00');
```



A list of additional schedule constraints may be found below:

<div class="overflow-auto">

| Method                                   | Description                                            |
| ---------------------------------------- | ------------------------------------------------------ |
| `->weekdays();`                          | Limit the task to weekdays.                            |
| `->weekends();`                          | Limit the task to weekends.                            |
| `->sundays();`                           | Limit the task to Sunday.                              |
| `->mondays();`                           | Limit the task to Monday.                              |
| `->tuesdays();`                          | Limit the task to Tuesday.                             |
| `->wednesdays();`                        | Limit the task to Wednesday.                           |
| `->thursdays();`                         | Limit the task to Thursday.                            |
| `->fridays();`                           | Limit the task to Friday.                              |
| `->saturdays();`                         | Limit the task to Saturday.                            |
| `->days(array\|mixed);`                  | Limit the task to specific days.                       |
| `->between($startTime, $endTime);`       | Limit the task to run between start and end times.     |
| `->unlessBetween($startTime, $endTime);` | Limit the task to not run between start and end times. |
| `->when(Closure);`                       | Limit the task based on a truth test.                  |
| `->environments($env);`                  | Limit the task to specific environments.               |

</div>

<a name="day-constraints"></a>
#### Day Constraints

The `days` method may be used to limit the execution of a task to specific days of the week. For example, you may schedule a command to run hourly on Sundays and Wednesdays:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->hourly()
    ->days([0, 3]);
```



또는 작업을 실행할 날을 정의할 때 `Illuminate\Console\Scheduling\Schedule` 클래스에서 사용할 수 있는 상수를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades;
use Illuminate\Console\Scheduling\Schedule;

Facades\Schedule::command('emails:send')
    ->hourly()
    ->days([Schedule::SUNDAY, Schedule::WEDNESDAY]);
```



<a name="between-time-constraints"></a>
#### 시간 제약 사이

`between` 방법은 하루 중 시간에 따라 작업 실행을 제한하는 데 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->between('7:00', '22:00');
```



마찬가지로, `unlessBetween` 방법은 일정 기간 동안 작업 실행을 제외하는 데 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->hourly()
    ->unlessBetween('23:00', '4:00');
```



<a name="truth-test-constraints"></a>
#### 진리 테스트 제약 조건

`when` 방법은 주어진 진리 테스트 결과에 따라 작업 실행을 제한하는 데 사용할 수 있습니다. 즉, 주어진 클로저가 `true`를 반환하면, 다른 제약 조건이 작업 실행을 방해하지 않는 한 작업은 실행됩니다:

```php
Schedule::command('emails:send')->daily()->when(function () {
    return true;
});
```



`skip` 방법은 `when`의 역으로 볼 수 있습니다. 만약 `skip` 방법이 `true`를 반환하면, 예약된 작업은 실행되지 않습니다:

```php
Schedule::command('emails:send')->daily()->skip(function () {
    return true;
});
```



연쇄 `when` 메서드를 사용할 때, 예약된 명령은 모든 `when` 조건이 `true`를 반환할 경우에만 실행됩니다.

<a name="environment-constraints"></a>
#### 환경 제약 조건

`environments` 메서드는 지정된 환경(`APP_ENV` [환경 변수](/docs/{{version}}/configuration#environment-configuration)에 의해 정의됨)에서만 작업을 실행하는 데 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->environments(['staging', 'production']);
```



<a name="timezones"></a>
### 시간대

`timezone` 방법을 사용하여 예약된 작업의 시간이 특정 시간대 내에서 해석되도록 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->timezone('America/New_York')
    ->at('2:00');
```



모든 예약된 작업에 동일한 시간대를 반복해서 할당하는 경우, 애플리케이션의 `app` 구성 파일 내에 `schedule_timezone` 옵션을 정의하여 모든 일정에 어떤 시간대를 할당할지 지정할 수 있습니다:

```php
'timezone' => 'UTC',

'schedule_timezone' => 'America/Chicago',
```



> [!WARNING]
> 일부 시간대에서는 일광 절약 시간제를 사용한다는 점을 기억하세요. 일광 절약 시간이 변경될 때는 예약된 작업이 두 번 실행되거나 전혀 실행되지 않을 수 있습니다. 이러한 이유로 가능하면 시간대 예약을 피하는 것이 좋습니다.

<a name="preventing-task-overlaps"></a>
### 작업 겹침 방지

기본적으로, 예약된 작업은 이전 작업 인스턴스가 아직 실행 중이더라도 실행됩니다. 이를 방지하기 위해, 다음의 `withoutOverlapping` 방법을 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')->withoutOverlapping();
```



이 예제에서는 `emails:send` [Artisan 명령어](/docs/{{version}}/artisan)가 이미 실행 중이 아니면 매분 실행됩니다. `withoutOverlapping` 방법은 실행 시간이 크게 달라지는 작업이 있는 경우 특히 유용하며, 특정 작업이 정확히 얼마나 걸릴지 예측할 수 없게 됩니다.

필요한 경우 "중복 방지" 잠금이 만료되기 전에 몇 분이 경과해야 하는지 지정할 수 있습니다. 기본적으로 잠금은 24시간 후에 만료됩니다:

```php
Schedule::command('emails:send')->withoutOverlapping(10);
```



Behind the scenes, the `withoutOverlapping` method utilizes your application's [cache](/docs/{{version}}/cache) to obtain locks. If necessary, you can clear these cache locks using the `schedule:clear-cache` Artisan command. This is typically only necessary if a task becomes stuck due to an unexpected server problem.

<a name="running-tasks-on-one-server"></a>
### Running Tasks on One Server

> [!WARNING]
> To utilize this feature, your application must be using the `database`, `memcached`, `dynamodb`, or `redis` cache driver as your application's default cache driver. In addition, all servers must be communicating with the same central cache server.

If your application's scheduler is running on multiple servers, you may limit a scheduled job to only execute on a single server. For instance, assume you have a scheduled task that generates a new report every Friday night. If the task scheduler is running on three worker servers, the scheduled task will run on all three servers and generate the report three times. Not good!

To indicate that the task should run on only one server, use the `onOneServer` method when defining the scheduled task. The first server to obtain the task will secure an atomic lock on the job to prevent other servers from running the same task at the same time:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('report:generate')
    ->fridays()
    ->at('17:00')
    ->onOneServer();
```



단일 서버 작업에 필요한 원자적 잠금을 얻기 위해 스케줄러가 사용하는 캐시 저장소를 사용자 정의하려면 `useCache` 방법을 사용할 수 있습니다:

```php
Schedule::useCache('database');
```



<a name="naming-unique-jobs"></a>
#### 단일 서버 작업 이름 지정

때때로 동일한 작업을 서로 다른 매개변수로 실행되도록 예약해야 할 수 있으며, 동시에 Laravel이 작업의 각 조합을 단일 서버에서 실행하도록 지시해야 할 때가 있습니다. 이를 달성하기 위해 각 예약 정의에 `name` 메서드를 통해 고유한 이름을 지정할 수 있습니다:

```php
Schedule::job(new CheckUptime('https://laravel.com'))
    ->name('check_uptime:laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();

Schedule::job(new CheckUptime('https://vapor.laravel.com'))
    ->name('check_uptime:vapor.laravel.com')
    ->everyFiveMinutes()
    ->onOneServer();
```



유사하게, 예정된 종료가 하나의 서버에서 실행될 예정이라면 이름이 지정되어야 합니다:

```php
Schedule::call(fn () => User::resetApiRequestCount())
    ->name('reset-api-request-count')
    ->daily()
    ->onOneServer();
```



<a name="background-tasks"></a>
### 백그라운드 작업

기본적으로, 동일한 시간에 예정된 여러 작업은 `schedule` 메서드에서 정의된 순서에 따라 순차적으로 실행됩니다. 장기 실행 작업이 있는 경우, 그로 인해 이후의 작업이 예상보다 훨씬 늦게 시작될 수 있습니다. 모든 작업을 동시에 실행할 수 있도록 백그라운드에서 실행하려면 `runInBackground` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('analytics:report')
    ->daily()
    ->runInBackground();
```



> [!WARNING]
> `runInBackground` 메서드는 `command` 및 `exec` 메서드를 통해 작업을 예약할 때만 사용할 수 있습니다.

<a name="maintenance-mode"></a>
### 유지보수 모드

애플리케이션이 [유지보수 모드](/docs/{{version}}/configuration#maintenance-mode)일 때는 예약된 작업이 실행되지 않습니다. 이는 서버에서 수행 중인 미완료 유지보수에 작업이 영향을 주지 않도록 하기 위함입니다. 그러나 유지보수 모드에서도 작업을 강제로 실행하고 싶다면, 작업을 정의할 때 `evenInMaintenanceMode` 메서드를 호출할 수 있습니다:

```php
Schedule::command('emails:send')->evenInMaintenanceMode();
```



<a name="pausing-scheduled-tasks"></a>
### 예약된 작업 일시 중지

배포된 코드를 변경하지 않고 `schedule:pause` Artisan 명령어를 사용하여 예약된 작업 처리를 일시적으로 중지할 수 있습니다:

```shell
php artisan schedule:pause
```



스케줄러가 일시 중지된 동안에는 예약된 작업이 실행되지 않습니다. `schedule:continue` 명령을 사용하여 예약 작업 처리를 다시 시작할 수 있습니다:

```shell
php artisan schedule:continue
```



작업이 스케줄러가 일시정지된 동안에도 여전히 실행되어야 하는 경우, `evenWhenPaused` 메서드로 표시할 수 있습니다:

```php
Schedule::command('emails:send')->evenWhenPaused();
```



<a name="schedule-groups"></a>
### 스케줄 그룹

유사한 구성을 가진 여러 예약 작업을 정의할 때, 각 작업마다 동일한 설정을 반복하지 않도록 Laravel의 작업 그룹 기능을 사용할 수 있습니다. 작업을 그룹화하면 코드를 단순화하고 관련 작업 간의 일관성을 보장할 수 있습니다.

예약 작업 그룹을 만들려면 원하는 작업 구성 메서드를 호출한 후 `group` 메서드를 호출합니다. `group` 메서드는 지정된 구성을 공유하는 작업을 정의하는 클로저를 인수로 받습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::daily()
    ->onOneServer()
    ->timezone('America/New_York')
    ->group(function () {
        Schedule::command('emails:send --force');
        Schedule::command('emails:prune');
    });
```



<a name="running-the-scheduler"></a>
## 스케줄러 실행하기

이제 예정된 작업을 정의하는 방법을 배웠으니, 실제로 서버에서 이를 실행하는 방법에 대해 이야기해보겠습니다. `schedule:run` Artisan 명령어는 모든 예정된 작업을 평가하고 서버의 현재 시간을 기준으로 실행이 필요한지 판단합니다.

따라서 Laravel의 스케줄러를 사용할 때는, 매 분마다 `schedule:run` 명령어를 실행하도록 서버에 단 하나의 크론(cron) 설정 항목만 추가하면 됩니다. 서버에 크론 항목을 추가하는 방법을 모른다면, 예정된 작업 실행을 관리해주는 [Laravel Cloud](https://cloud.laravel.com)와 같은 관리형 플랫폼을 사용하는 것을 고려해 보세요:

```shell
* * * * * cd /path-to-your-project && php artisan schedule:run >> /dev/null 2>&1
```



<a name="sub-minute-scheduled-tasks"></a>
### 1분 미만 스케줄된 작업

대부분의 운영 체제에서 cron 작업은 최대 1분에 한 번만 실행되도록 제한됩니다. 그러나 Laravel의 스케줄러를 사용하면 작업을 더 짧은 간격으로, 심지어 초당 한 번씩 실행되도록 예약할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::call(function () {
    DB::table('recent_users')->delete();
})->everySecond();
```



애플리케이션 내에서 1분 미만의 작업이 정의되면, `schedule:run` 명령은 즉시 종료되는 대신 현재 분이 끝날 때까지 계속 실행됩니다. 이를 통해 명령은 분 동안 필요한 모든 1분 미만 작업을 호출할 수 있습니다.

예상보다 더 오래 실행되는 1분 미만 작업이 나중의 1분 미만 작업 실행을 지연시킬 수 있으므로, 모든 1분 미만 작업은 실제 작업 처리를 위해 대기 중인 작업이나 백그라운드 명령을 디스패치하는 것이 권장됩니다:

```php
use App\Jobs\DeleteRecentUsers;

Schedule::job(new DeleteRecentUsers)->everyTenSeconds();

Schedule::command('users:delete')->everyTenSeconds()->runInBackground();
```



<a name="interrupting-sub-minute-tasks"></a>
#### 1분 미만 작업 중단

하위 1분 작업이 정의된 경우, `schedule:run` 명령은 호출된 전체 1분 동안 실행되므로, 애플리케이션을 배포할 때 가끔 명령을 중단해야 할 필요가 있습니다. 그렇지 않으면 이미 실행 중인 `schedule:run` 명령의 인스턴스가 현재 1분이 끝날 때까지 이전에 배포된 애플리케이션 코드를 계속 사용할 수 있습니다.

진행 중인 `schedule:run` 호출을 중단하려면, `schedule:interrupt` 명령을 애플리케이션 배포 스크립트에 추가할 수 있습니다. 이 명령은 애플리케이션 배포가 완료된 후에 호출해야 합니다:

```shell
php artisan schedule:interrupt
```



<a name="running-the-scheduler-locally"></a>
### 로컬에서 스케줄러 실행하기

일반적으로 로컬 개발 머신에는 스케줄러 크론 항목을 추가하지 않습니다. 대신 `schedule:work` Artisan 명령어를 사용할 수 있습니다. 이 명령어는 포그라운드에서 실행되며, 명령어를 종료할 때까지 매 분마다 스케줄러를 호출합니다. 1분 미만의 작업이 정의되어 있을 경우, 스케줄러는 해당 작업을 처리하기 위해 각 분 내에서 계속 실행됩니다:

```shell
php artisan schedule:work
```



<a name="task-output"></a>
## 작업 출력

Laravel 스케줄러는 예약된 작업에서 생성된 출력을 처리하기 위한 여러 편리한 방법을 제공합니다. 먼저, `sendOutputTo` 메서드를 사용하여 출력을 나중에 확인할 수 있도록 파일로 보낼 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->sendOutputTo($filePath);
```



출력을 주어진 파일에 추가하고 싶다면, `appendOutputTo` 방법을 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->appendOutputTo($filePath);
```



`emailOutputTo` 방법을 사용하여 출력물을 원하는 이메일 주소로 보낼 수 있습니다. 작업의 출력물을 이메일로 보내기 전에 Laravel의 [이메일 서비스](/docs/{{version}}/mail)를 구성해야 합니다:

```php
Schedule::command('report:generate')
    ->daily()
    ->sendOutputTo($filePath)
    ->emailOutputTo('taylor@example.com');
```



예약된 Artisan 또는 시스템 명령이 0이 아닌 종료 코드로 종료될 경우에만 출력 내용을 이메일로 보내고 싶다면, `emailOutputOnFailure` 방법을 사용하십시오:

```php
Schedule::command('report:generate')
    ->daily()
    ->emailOutputOnFailure('taylor@example.com');
```



> [!WARNING]
> `emailOutputTo`, `emailOutputOnFailure`, `sendOutputTo` 및 `appendOutputTo` 메서드는 `command` 및 `exec` 메서드에만 해당됩니다.

<a name="task-hooks"></a>
## 작업 후크

`before` 및 `after` 메서드를 사용하면 예약된 작업이 실행되기 전과 후에 실행될 코드를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('emails:send')
    ->daily()
    ->before(function () {
        // The task is about to execute...
    })
    ->after(function () {
        // The task has executed...
    });
```



`onSuccess` 및 `onFailure` 메서드는 예약된 작업이 성공하거나 실패할 경우 실행될 코드를 지정할 수 있게 해줍니다. 실패는 예약된 Artisan 또는 시스템 명령이 0이 아닌 종료 코드로 종료되었음을 나타냅니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function () {
        // The task succeeded...
    })
    ->onFailure(function () {
        // The task failed...
    });
```



명령에서 출력이 가능한 경우, 후크 클로저 정의의 `$output` 인수로 `Illuminate\Support\Stringable` 인스턴스를 타입 힌팅하여 `after`, `onSuccess` 또는 `onFailure` 후크에서 접근할 수 있습니다:

```php
use Illuminate\Support\Stringable;

Schedule::command('emails:send')
    ->daily()
    ->onSuccess(function (Stringable $output) {
        // The task succeeded...
    })
    ->onFailure(function (Stringable $output) {
        // The task failed...
    });
```



<a name="pinging-urls"></a>
#### URL 핑(Pinging)하기

`pingBefore`와 `thenPing` 방법을 사용하면, 스케줄러는 작업이 실행되기 전이나 후에 지정된 URL을 자동으로 핑할 수 있습니다. 이 방법은 [Envoyer](https://envoyer.io)와 같은 외부 서비스에 스케줄된 작업이 시작되었거나 실행이 완료되었음을 알리는 데 유용합니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBefore($url)
    ->thenPing($url);
```



`pingOnSuccess` 및 `pingOnFailure` 방법은 작업이 성공하거나 실패한 경우에만 주어진 URL을 핑하는 데 사용할 수 있습니다. 실패는 예약된 Artisan 또는 시스템 명령이 0이 아닌 종료 코드로 종료되었음을 나타냅니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccess($successUrl)
    ->pingOnFailure($failureUrl);
```



`pingBeforeIf`, `thenPingIf`, `pingOnSuccessIf`, 그리고 `pingOnFailureIf` 메서드는 주어진 조건이 `true`인 경우에만 주어진 URL을 핑하는 데 사용할 수 있습니다:

```php
Schedule::command('emails:send')
    ->daily()
    ->pingBeforeIf($condition, $url)
    ->thenPingIf($condition, $url);

Schedule::command('emails:send')
    ->daily()
    ->pingOnSuccessIf($condition, $successUrl)
    ->pingOnFailureIf($condition, $failureUrl);
```

<a name="events"></a>
## 이벤트

Laravel은 스케줄링 과정 동안 다양한 [이벤트](/docs/{{version}}/events)를 발생시킵니다. 다음 이벤트 중 어떤 것이든 [리스너를 정의](/docs/{{version}}/events)할 수 있습니다:

<div class="overflow-auto">

| 이벤트 이름                                                  |
| ----------------------------------------------------------- |
| `Illuminate\Console\Events\ScheduledTaskStarting`           |
| `Illuminate\Console\Events\ScheduledTaskFinished`           |
| `Illuminate\Console\Events\ScheduledBackgroundTaskFinished` |
| `Illuminate\Console\Events\ScheduledTaskSkipped`            |
| `Illuminate\Console\Events\ScheduledTaskFailed`             |

</div>
{% endraw %}
