---
layout: docs
title: "알림"
---

{% raw %}
# 알림

- [Introduction](#introduction)
- [Generating Notifications](#generating-notifications)
- [Sending Notifications](#sending-notifications)
    - [Using the Notifiable Trait](#using-the-notifiable-trait)
    - [Using the Notification Facade](#using-the-notification-facade)
    - [Specifying Delivery Channels](#specifying-delivery-channels)
    - [Queueing Notifications](#queueing-notifications)
    - [On-Demand Notifications](#on-demand-notifications)
- [Mail Notifications](#mail-notifications)
    - [Formatting Mail Messages](#formatting-mail-messages)
    - [Customizing the Sender](#customizing-the-sender)
    - [Customizing the Recipient](#customizing-the-recipient)
    - [Customizing the Subject](#customizing-the-subject)
    - [Customizing the Mailer](#customizing-the-mailer)
    - [Customizing the Templates](#customizing-the-templates)
    - [Attachments](#mail-attachments)
    - [Adding Tags and Metadata](#adding-tags-metadata)
    - [Customizing the Symfony Message](#customizing-the-symfony-message)
    - [Using Mailables](#using-mailables)
    - [Previewing Mail Notifications](#previewing-mail-notifications)
- [Markdown Mail Notifications](#markdown-mail-notifications)
    - [Generating the Message](#generating-the-message)
    - [Writing the Message](#writing-the-message)
    - [Customizing the Components](#customizing-the-components)
- [Database Notifications](#database-notifications)
    - [Prerequisites](#database-prerequisites)
    - [Formatting Database Notifications](#formatting-database-notifications)
    - [Accessing the Notifications](#accessing-the-notifications)
    - [Marking Notifications as Read](#marking-notifications-as-read)
- [Broadcast Notifications](#broadcast-notifications)
    - [Prerequisites](#broadcast-prerequisites)
    - [Formatting Broadcast Notifications](#formatting-broadcast-notifications)
    - [Listening for Notifications](#listening-for-notifications)
- [SMS Notifications](#sms-notifications)
    - [Prerequisites](#sms-prerequisites)
    - [Formatting SMS Notifications](#formatting-sms-notifications)
    - [Customizing the "From" Number](#customizing-the-from-number)
    - [Adding a Client Reference](#adding-a-client-reference)
    - [Routing SMS Notifications](#routing-sms-notifications)
- [Slack Notifications](#slack-notifications)
    - [Prerequisites](#slack-prerequisites)
    - [Formatting Slack Notifications](#formatting-slack-notifications)
    - [Slack Interactivity](#slack-interactivity)
    - [Routing Slack Notifications](#routing-slack-notifications)
    - [Notifying External Slack Workspaces](#notifying-external-slack-workspaces)
- [Localizing Notifications](#localizing-notifications)
- [Testing](#testing)
- [Notification Events](#notification-events)
- [Custom Channels](#custom-channels)



<a name="introduction"></a>
## Introduction

In addition to support for [sending email](/docs/{{version}}/mail), Laravel provides support for sending notifications across a variety of delivery channels, including email, SMS (via [Vonage](https://www.vonage.com/communications-apis/), formerly known as Nexmo), and [Slack](https://slack.com). In addition, a variety of [community built notification channels](https://laravel-notification-channels.com/about/#suggesting-a-new-channel) have been created to send notifications over dozens of different channels! Notifications may also be stored in a database so they may be displayed in your web interface.

Typically, notifications should be short, informational messages that notify users of something that occurred in your application. For example, if you are writing a billing application, you might send an "Invoice Paid" notification to your users via the email and SMS channels.

<a name="generating-notifications"></a>
## Generating Notifications

In Laravel, each notification is represented by a single class that is typically stored in the `app/Notifications` directory. Don't worry if you don't see this directory in your application - it will be created for you when you run the `make:notification` Artisan command:

```shell
php artisan make:notification InvoicePaid
```



이 명령은 `app/Notifications` 디렉토리에 새로운 알림 클래스를 생성합니다. 각 알림 클래스에는 `via` 메서드와 메시지를 해당 채널에 맞게 변환하는 `toMail` 또는 `toDatabase`와 같은 가변적인 수의 메시지 생성 메서드가 포함되어 있습니다.

<a name="sending-notifications"></a>
## 알림 보내기

<a name="using-the-notifiable-trait"></a>
### Notifiable 트레이트 사용하기

알림은 두 가지 방법으로 보낼 수 있습니다: `Notifiable` 트레이트의 `notify` 메서드를 사용하거나 `Notification` [퍼사드](/docs/{{version}}/facades)를 사용하는 방법입니다. `Notifiable` 트레이트는 기본적으로 애플리케이션의 `App\Models\User` 모델에 포함되어 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;
}
```



이 트레이트에서 제공하는 `notify` 메서드는 알림 인스턴스를 받도록 예상합니다:

```php
use App\Notifications\InvoicePaid;

$user->notify(new InvoicePaid($invoice));
```



> [!NOTE]
> 기억하세요, `Notifiable` 특성을 여러분의 모델 중 어느 모델에도 사용할 수 있습니다. `User` 모델에만 포함하는 것으로 제한되지 않습니다.

<a name="using-the-notification-facade"></a>
### 알림 퍼사드 사용하기

또는 `Notification` [퍼사드](/docs/{{version}}/facades)를 통해 알림을 보낼 수 있습니다. 이 방법은 사용자 컬렉션과 같은 여러 알림 대상 엔티티에 알림을 보내야 할 때 유용합니다. 퍼사드를 사용하여 알림을 보내려면, 모든 알림 대상 엔티티와 알림 인스턴스를 `send` 메서드에 전달하세요:

```php
use Illuminate\Support\Facades\Notification;

Notification::send($users, new InvoicePaid($invoice));
```



`sendNow` 방법을 사용하여 알림을 즉시 보낼 수도 있습니다. 이 방법은 알림이 `ShouldQueue` 인터페이스를 구현하더라도 알림을 즉시 보냅니다:

```php
Notification::sendNow($developers, new DeploymentCompleted($deployment));
```



<a name="specifying-delivery-channels"></a>
### 알림 채널 지정

모든 알림 클래스에는 알림이 어떤 채널로 전달될지 결정하는 `via` 메서드가 있습니다. 알림은 `mail`, `database`, `broadcast`, `vonage`, `slack` 채널을 통해 전송될 수 있습니다.

> [!NOTE]
> Telegram이나 Pusher 같은 다른 전달 채널을 사용하고 싶다면, 커뮤니티 주도 [Laravel Notification Channels 웹사이트](http://laravel-notification-channels.com)를 확인하세요.

`via` 메서드는 `$notifiable` 인스턴스를 받으며, 이는 알림이 전달될 클래스의 인스턴스가 됩니다. `$notifiable`를 사용하여 알림이 전달될 채널을 결정할 수 있습니다:

```php
/**
 * Get the notification's delivery channels.
 *
 * @return array<int, string>
 */
public function via(object $notifiable): array
{
    return $notifiable->prefers_sms ? ['vonage'] : ['mail', 'database'];
}
```



<a name="queueing-notifications"></a>
### 알림 대기열 관리

> [!WARNING]
> 알림을 대기열에 추가하기 전에, 대기열을 구성하고 [작업자를 시작](/docs/{{version}}/queues#running-the-queue-worker)해야 합니다.

알림 전송에는 시간이 걸릴 수 있습니다. 특히 채널이 알림을 전달하기 위해 외부 API 호출을 해야 하는 경우에는 더욱 그렇습니다. 애플리케이션의 응답 시간을 높이려면, 클래스에 `ShouldQueue` 인터페이스와 `Queueable` 트레이트를 추가하여 알림을 대기열에 추가하도록 하세요. `make:notification` 명령어를 사용하여 생성된 모든 알림에는 이미 인터페이스와 트레이트가 가져오기 되어 있으므로, 바로 알림 클래스에 추가할 수 있습니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    // ...
}
```



`ShouldQueue` 인터페이스가 알림에 추가되면, 일반적으로 알림을 보낼 수 있습니다. Laravel은 클래스에서 `ShouldQueue` 인터페이스를 감지하고 자동으로 알림 전송을 대기열에 추가합니다:

```php
$user->notify(new InvoicePaid($invoice));
```



알림을 큐에 넣을 때, 각 수신자와 채널 조합마다 큐에 들어갈 작업이 생성됩니다. 예를 들어, 알림에 수신자가 3명이고 채널이 2개인 경우, 6개의 작업이 큐에 전송됩니다.

<a name="delaying-notifications"></a>
#### 알림 지연

알림 전달을 지연하고 싶다면, 알림 인스턴스를 생성할 때 `delay` 메서드를 체인으로 연결할 수 있습니다:

```php
$delay = now()->plus(minutes: 10);

$user->notify((new InvoicePaid($invoice))->delay($delay));
```



특정 채널의 지연량을 지정하기 위해 배열을 `delay` 메서드에 전달할 수 있습니다:

```php
$user->notify((new InvoicePaid($invoice))->delay([
    'mail' => now()->plus(minutes: 5),
    'sms' => now()->plus(minutes: 10),
]));
```



또는 알림 클래스 자체에 `withDelay` 메서드를 정의할 수 있습니다. `withDelay` 메서드는 채널 이름과 지연 값을 배열로 반환해야 합니다:

```php
/**
 * Determine the notification's delivery delay.
 *
 * @return array<string, \Illuminate\Support\Carbon>
 */
public function withDelay(object $notifiable): array
{
    return [
        'mail' => now()->plus(minutes: 5),
        'sms' => now()->plus(minutes: 10),
    ];
}
```



<a name="customizing-the-notification-queue-connection"></a>
#### 알림 큐 연결 사용자 정의

기본적으로, 대기 중인 알림은 애플리케이션의 기본 큐 연결을 사용하여 큐에 저장됩니다. 특정 알림에 대해 다른 연결을 사용하고 싶다면, 알림 생성자의 생성자에서 `onConnection` 메서드를 호출할 수 있습니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->onConnection('redis');
    }
}
```



또는 알림에서 지원하는 각 알림 채널에 사용될 특정 큐 연결을 지정하고 싶다면, 알림에서 `viaConnections` 메서드를 정의할 수 있습니다. 이 메서드는 채널 이름/큐 연결 이름 쌍의 배열을 반환해야 합니다:

```php
/**
 * Determine which connections should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaConnections(): array
{
    return [
        'mail' => 'redis',
        'database' => 'sync',
    ];
}
```



<a name="customizing-notification-channel-queues"></a>
#### 알림 채널 큐 사용자 지정

알림에서 지원하는 각 알림 채널에 대해 사용해야 하는 특정 큐를 지정하려는 경우, 알림에서 `viaQueues` 메서드를 정의할 수 있습니다. 이 메서드는 채널 이름 / 큐 이름 쌍의 배열을 반환해야 합니다:

```php
/**
 * Determine which queues should be used for each notification channel.
 *
 * @return array<string, string>
 */
public function viaQueues(): array
{
    return [
        'mail' => 'mail-queue',
        'slack' => 'slack-queue',
    ];
}
```



<a name="customizing-queued-notification-job-properties"></a>
#### 대기 중인 알림 작업 속성 사용자 지정

알림 클래스에서 큐 속성을 정의하여 기본 대기 중인 작업의 동작을 사용자 지정할 수 있습니다. 이러한 속성은 알림을 전송하는 대기 중인 작업이 상속하게 됩니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;
use Illuminate\Queue\Attributes\FailOnTimeout;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Timeout;
use Illuminate\Queue\Attributes\Tries;

#[Tries(5)]
#[Timeout(120)]
#[MaxExceptions(3)]
#[FailOnTimeout]
class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    // ...
}
```



대기 중인 알림 데이터의 [암호화](/docs/{{version}}/encryption)를 통해 개인정보 보호와 무결성을 보장하려면, 알림 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하십시오:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue, ShouldBeEncrypted
{
    use Queueable;

    // ...
}
```



알림 클래스에서 이러한 속성을 직접 정의하는 것 외에도, 대기 중인 알림 작업에 대한 재시도 전략과 재시도 시간 초과를 지정하기 위해 `backoff` 및 `retryUntil` 메서드를 정의할 수도 있습니다:

```php
use DateTime;

/**
 * Calculate the number of seconds to wait before retrying the notification.
 */
public function backoff(): int
{
    return 3;
}

/**
 * Determine the time at which the notification should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 5);
}
```



> [!NOTE]
> 이러한 작업 속성과 메서드에 대한 자세한 정보를 보려면 [대기 중인 작업](/docs/{{version}}/queues#max-job-attempts-and-timeout) 문서를 참조하십시오.

<a name="queued-notification-middleware"></a>
#### 대기 중인 알림 미들웨어

대기 중인 알림은 [대기 중인 작업과 마찬가지로](/docs/{{version}}/queues#job-middleware) 미들웨어를 정의할 수 있습니다. 시작하려면 알림 클래스에 `middleware` 메서드를 정의하십시오. `middleware` 메서드는 `$notifiable` 및 `$channel` 변수를 받으며, 이를 통해 알림의 목적지에 따라 반환될 미들웨어를 사용자 정의할 수 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the notification job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(object $notifiable, string $channel)
{
    return match ($channel) {
        'mail' => [new RateLimited('postmark')],
        'slack' => [new RateLimited('slack')],
        default => [],
    };
}
```



<a name="queued-notifications-and-database-transactions"></a>
#### 대기 중인 알림과 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 대기 중인 알림이 전송될 때, 알림이 트랜잭션이 커밋되기 전에 큐에 의해 처리될 수 있습니다. 이 경우, 데이터베이스 트랜잭션 동안 모델이나 데이터베이스 레코드에 적용한 업데이트가 아직 데이터베이스에 반영되지 않을 수 있습니다. 또한, 트랜잭션 내에서 생성된 모델이나 데이터베이스 레코드는 데이터베이스에 존재하지 않을 수 있습니다. 알림이 이러한 모델에 의존하는 경우, 대기 중인 알림을 전송하는 작업을 처리할 때 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 구성 옵션이 `false`로 설정되어 있는 경우에도, 알림을 전송할 때 `afterCommit` 메서드를 호출하여 특정 대기 중인 알림이 모든 열린 데이터베이스 트랜잭션이 커밋된 후에 전송되도록 지정할 수 있습니다:

```php
use App\Notifications\InvoicePaid;

$user->notify((new InvoicePaid($invoice))->afterCommit());
```



또는 알림의 생성자에서 `afterCommit` 메서드를 호출할 수 있습니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new notification instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```



> [!NOTE]
> 이러한 문제를 우회하여 작업하는 방법에 대해 자세히 알아보려면 [대기열 작업 및 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions) 관련 문서를 검토하세요.

<a name="determining-if-the-queued-notification-should-be-sent"></a>
#### 대기열 알림을 전송할지 결정하기

대기열 알림이 백그라운드 처리용 대기열에 배치된 후, 일반적으로 대기열 작업자가 이를 수락하고 의도된 수신자에게 전송합니다.

그러나 대기열 작업자가 처리 중인 후에 대기열 알림을 전송할지 최종적으로 결정하고 싶다면, 알림 클래스에 `shouldSend` 메서드를 정의할 수 있습니다. 이 메서드가 `false`를 반환하면, 알림은 전송되지 않습니다:

```php
/**
 * Determine if the notification should be sent.
 */
public function shouldSend(object $notifiable, string $channel): bool
{
    return $this->invoice->isPaid();
}
```



<a name="after-sending-notifications"></a>
#### 알림 전송 후

알림이 전송된 후 코드를 실행하고 싶다면, 알림 클래스에 `afterSending` 메서드를 정의할 수 있습니다. 이 메서드는 알림을 받을 엔티티, 채널 이름, 그리고 채널로부터의 응답을 전달받습니다:

```php
/**
 * Handle the notification after it has been sent.
 */
public function afterSending(object $notifiable, string $channel, mixed $response): void
{
    // ...
}
```



<a name="on-demand-notifications"></a>
### 주문형 알림

때때로 애플리케이션의 "사용자"로 저장되지 않은 사람에게 알림을 보내야 할 때가 있습니다. `Notification` 퍼사드의 `route` 메서드를 사용하여 알림을 보내기 전에 임시 알림 라우팅 정보를 지정할 수 있습니다:

```php
use Illuminate\Broadcasting\Channel;
use Illuminate\Support\Facades\Notification;

Notification::route('mail', 'taylor@example.com')
    ->route('vonage', '5555555555')
    ->route('slack', '#slack-channel')
    ->route('broadcast', [new Channel('channel-name')])
    ->notify(new InvoicePaid($invoice));
```



`mail` 경로로 온디맨드 알림을 보낼 때 수신자의 이름을 제공하고 싶다면, 배열의 첫 번째 요소에서 이메일 주소를 키로 하고 이름을 값으로 포함하는 배열을 제공할 수 있습니다:

```php
Notification::route('mail', [
    'barrett@example.com' => 'Barrett Blair',
])->notify(new InvoicePaid($invoice));
```



`routes` 방법을 사용하면 여러 알림 채널에 대해 한 번에 임시 라우팅 정보를 제공할 수 있습니다:

```php
Notification::routes([
    'mail' => ['barrett@example.com' => 'Barrett Blair'],
    'vonage' => '5555555555',
])->notify(new InvoicePaid($invoice));
```



<a name="mail-notifications"></a>
## 메일 알림

<a name="formatting-mail-messages"></a>
### 메일 메시지 형식 지정

알림이 이메일로 전송되는 것을 지원하는 경우, 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받으며 `Illuminate\Notifications\Messages\MailMessage` 인스턴스를 반환해야 합니다.

`MailMessage` 클래스에는 트랜잭션 이메일 메시지를 작성하는 데 도움이 되는 몇 가지 간단한 메서드가 포함되어 있습니다. 메일 메시지에는 텍스트 줄과 "실행 유도(Call to Action)"가 포함될 수 있습니다. `toMail` 메서드의 예제를 살펴보겠습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
        ->greeting('Hello!')
        ->line('One of your invoices has been paid!')
        ->lineIf($this->amount > 0, "Amount paid: {$this->amount}")
        ->action('View Invoice', $url)
        ->line('Thank you for using our application!');
}
```



> [!NOTE]
> Note we are using `$this->invoice->id` in our `toMail` method. You may pass any data your notification needs to generate its message into the notification's constructor.

In this example, we register a greeting, a line of text, a call to action, and then another line of text. These methods provided by the `MailMessage` object make it simple and fast to format small transactional emails. The mail channel will then translate the message components into a beautiful, responsive HTML email template with a plain-text counterpart. Here is an example of an email generated by the `mail` channel:

<img src="https://laravel.com/img/docs/notification-example-2.png">

> [!NOTE]
> When sending mail notifications, be sure to set the `name` configuration option in your `config/app.php` configuration file. This value will be used in the header and footer of your mail notification messages.

<a name="error-messages"></a>
#### Error Messages

Some notifications inform users of errors, such as a failed invoice payment. You may indicate that a mail message is regarding an error by calling the `error` method when building your message. When using the `error` method on a mail message, the call to action button will be red instead of black:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->error()
        ->subject('Invoice Payment Failed')
        ->line('...');
}
```



<a name="other-mail-notification-formatting-options"></a>
#### 다른 메일 알림 서식 옵션

알림 클래스에서 텍스트의 "줄"을 정의하는 대신, `view` 메서드를 사용하여 알림 이메일을 렌더링하는 데 사용할 사용자 지정 템플릿을 지정할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        'mail.invoice.paid', ['invoice' => $this->invoice]
    );
}
```



`view` 메서드에 전달되는 배열의 두 번째 요소로 보기 이름을 전달하여 메일 메시지에 대한 일반 텍스트 보기를 지정할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->view(
        ['mail.invoice.paid', 'mail.invoice.paid-text'],
        ['invoice' => $this->invoice]
    );
}
```



또는 메시지가 일반 텍스트 보기만 있는 경우, `text` 방법을 사용할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)->text(
        'mail.invoice.paid-text', ['invoice' => $this->invoice]
    );
}
```



<a name="customizing-the-sender"></a>
### 발신자 맞춤 설정

기본적으로 이메일의 발신자 / 보내는 주소는 `config/mail.php` 구성 파일에 정의되어 있습니다. 그러나 특정 알림에 대해 `from` 메서드를 사용하여 보내는 주소를 지정할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->from('barrett@example.com', 'Barrett Blair')
        ->line('...');
}
```



<a name="customizing-the-recipient"></a>
### 수신자 맞춤 설정

`mail` 채널을 통해 알림을 보낼 때, 알림 시스템은 자동으로 알림을 받을 수 있는 엔티티에서 `email` 속성을 찾습니다. 알림을 전달하는 데 사용되는 이메일 주소를 사용자 정의하려면 알림을 받을 수 있는 엔티티에 `routeNotificationForMail` 메서드를 정의하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the mail channel.
     *
     * @return  array<string, string>|string
     */
    public function routeNotificationForMail(Notification $notification): array|string
    {
        // Return email address only...
        return $this->email_address;

        // Return email address and name...
        return [$this->email_address => $this->name];
    }
}
```



<a name="customizing-the-subject"></a>
### 제목 맞춤 설정

기본적으로 이메일의 제목은 알림 클래스 이름을 "Title Case" 형식으로 변환한 것입니다. 따라서 알림 클래스 이름이 `InvoicePaid`인 경우, 이메일의 제목은 `Invoice Paid`가 됩니다. 메시지에 대해 다른 제목을 지정하고 싶다면 메시지를 작성할 때 `subject` 메서드를 호출하면 됩니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->subject('Notification Subject')
        ->line('...');
}
```



<a name="customizing-the-mailer"></a>
### 메일러 커스터마이징

기본적으로 이메일 알림은 `config/mail.php` 설정 파일에 정의된 기본 메일러를 사용하여 전송됩니다. 그러나 메시지를 작성할 때 `mailer` 메서드를 호출하여 런타임에 다른 메일러를 지정할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->mailer('postmark')
        ->line('...');
}
```



<a name="customizing-the-templates"></a>
### 템플릿 커스터마이징

메일 알림에 사용되는 HTML 및 일반 텍스트 템플릿은 알림 패키지의 리소스를 게시하여 수정할 수 있습니다. 이 명령을 실행한 후, 메일 알림 템플릿은 `resources/views/vendor/notifications` 디렉터리에 위치하게 됩니다:

```shell
php artisan vendor:publish --tag=laravel-notifications
```



<a name="mail-attachments"></a>
### 첨부 파일

이메일 알림에 첨부 파일을 추가하려면 메시지를 작성하는 동안 `attach` 방법을 사용하세요. `attach` 방법은 파일의 절대 경로를 첫 번째 인수로 받습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file');
}
```



> [!NOTE]
> 알림 메일 메시지에서 제공되는 `attach` 메서드는 [첨부 가능한 객체](/docs/{{version}}/mail#attachable-objects)도 수락합니다. 자세한 내용은 포괄적인 [첨부 객체 문서](/docs/{{version}}/mail#attachable-objects)를 참조하십시오.

메시지에 파일을 첨부할 때, `attach` 메서드의 두 번째 인수로 `array`를 전달하여 표시 이름 및/또는 MIME 유형을 지정할 수도 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attach('/path/to/file', [
            'as' => 'name.pdf',
            'mime' => 'application/pdf',
        ]);
}
```



필요한 경우, `attachMany` 방법을 사용하여 메시지에 여러 파일을 첨부할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attachMany([
            '/path/to/forge.svg',
            '/path/to/vapor.svg' => [
                'as' => 'Logo.svg',
                'mime' => 'image/svg+xml',
            ],
        ]);
}
```



특정 [파일시스템 디스크](/docs/{{version}}/filesystem)에 존재하는 파일을 첨부하기 위해 `attachFromStorageDisk` 방법을 사용할 수 있습니다. 이 방법은 디스크 이름과 해당 디스크의 파일 경로를 받습니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email)
        ->attachFromStorageDisk('s3', '/path/to/file', 'invoice.pdf', [
            'mime' => 'application/pdf',
        ]);
}
```



<a name="raw-data-attachments"></a>
#### 원시 데이터 첨부파일

`attachData` 메서드는 바이트의 원시 문자열을 첨부파일로 첨부할 때 사용할 수 있습니다. `attachData` 메서드를 호출할 때는 첨부파일에 할당할 파일 이름을 제공해야 합니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Hello!')
        ->attachData($this->pdf, 'name.pdf', [
            'mime' => 'application/pdf',
        ]);
}
```



<a name="adding-tags-metadata"></a>
### 태그 및 메타데이터 추가

Mailgun 및 Postmark와 같은 일부 타사 이메일 제공업체는 메시지 "태그" 및 "메타데이터"를 지원하며, 이를 사용하여 애플리케이션에서 보낸 이메일을 그룹화하고 추적할 수 있습니다. `tag` 및 `metadata` 메서드를 통해 이메일 메시지에 태그와 메타데이터를 추가할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->greeting('Comment Upvoted!')
        ->tag('upvote')
        ->metadata('comment_id', $this->comment->id);
}
```



응용 프로그램이 Mailgun 드라이버를 사용하는 경우, [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 대한 추가 정보는 Mailgun 문서를 참조할 수 있습니다. 마찬가지로, Postmark 문서도 [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)에 대한 지원 정보를 확인하는 데 참고할 수 있습니다.

응용 프로그램이 Amazon SES를 사용하여 이메일을 보내는 경우, 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부하려면 `metadata` 방법을 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 맞춤 설정

`MailMessage` 클래스의 `withSymfonyMessage` 메서드는 메시지를 보내기 전에 Symfony 메시지 인스턴스와 함께 호출될 클로저를 등록할 수 있게 해줍니다. 이를 통해 메시지가 전달되기 전에 메시지를 깊이 있게 맞춤 설정할 수 있는 기회를 제공합니다.

```php
use Symfony\Component\Mime\Email;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->withSymfonyMessage(function (Email $message) {
            $message->getHeaders()->addTextHeader(
                'Custom-Header', 'Header Value'
            );
        });
}
```



<a name="using-mailables"></a>
### 메일러블 사용하기

필요한 경우, 알림의 `toMail` 메서드에서 전체 [메일러블 객체](/docs/{{version}}/mail)를 반환할 수 있습니다. `MailMessage` 대신 `Mailable`를 반환할 경우, 메일러블 객체의 `to` 메서드를 사용하여 메시지 수신자를 지정해야 합니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    return (new InvoicePaidMailable($this->invoice))
        ->to($notifiable->email);
}
```



<a name="mailables-and-on-demand-notifications"></a>
#### 메일 및 주문형 알림

[주문형 알림](#on-demand-notifications)을 보내는 경우, `toMail` 메서드에 제공된 `$notifiable` 인스턴스는 `Illuminate\Notifications\AnonymousNotifiable`의 인스턴스가 되며, 이 인스턴스는 주문형 알림이 전송될 이메일 주소를 가져오는 데 사용할 수 있는 `routeNotificationFor` 메서드를 제공합니다:

```php
use App\Mail\InvoicePaid as InvoicePaidMailable;
use Illuminate\Notifications\AnonymousNotifiable;
use Illuminate\Mail\Mailable;

/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): Mailable
{
    $address = $notifiable instanceof AnonymousNotifiable
        ? $notifiable->routeNotificationFor('mail')
        : $notifiable->email;

    return (new InvoicePaidMailable($this->invoice))
        ->to($address);
}
```



<a name="previewing-mail-notifications"></a>
### 메일 알림 미리보기

메일 알림 템플릿을 설계할 때, 일반적인 Blade 템플릿처럼 브라우저에서 렌더링된 메일 메시지를 빠르게 미리보는 것이 편리합니다. 이러한 이유로 Laravel은 라우트 클로저나 컨트롤러에서 메일 알림으로 생성된 메일 메시지를 직접 반환할 수 있도록 허용합니다. `MailMessage`가 반환되면, 브라우저에서 렌더링되어 표시되며 실제 이메일 주소로 보내지 않아도 디자인을 빠르게 미리 볼 수 있습니다:

```php
use App\Models\Invoice;
use App\Notifications\InvoicePaid;

Route::get('/notification', function () {
    $invoice = Invoice::find(1);

    return (new InvoicePaid($invoice))
        ->toMail($invoice->user);
});
```



<a name="markdown-mail-notifications"></a>
## 마크다운 메일 알림

마크다운 메일 알림을 사용하면, 사전 제작된 메일 알림 템플릿을 활용하면서 더 길고 맞춤화된 메시지를 작성할 자유를 얻을 수 있습니다. 메시지가 마크다운으로 작성되기 때문에, Laravel은 메시지에 대해 아름답고 반응형 HTML 템플릿을 렌더링할 수 있으며 동시에 일반 텍스트 버전도 자동으로 생성할 수 있습니다.

<a name="generating-the-message"></a>
### 메시지 생성

해당 마크다운 템플릿과 함께 알림을 생성하려면, `make:notification` Artisan 명령어의 `--markdown` 옵션을 사용할 수 있습니다:

```shell
php artisan make:notification InvoicePaid --markdown=mail.invoice.paid
```



다른 모든 메일 알림과 마찬가지로, Markdown 템플릿을 사용하는 알림은 알림 클래스에 `toMail` 메서드를 정의해야 합니다. 그러나 알림을 구성하기 위해 `line` 및 `action` 메서드를 사용하는 대신, 사용해야 할 Markdown 템플릿의 이름을 지정하기 위해 `markdown` 메서드를 사용하십시오. 템플릿에서 사용할 수 있도록 하려는 데이터 배열은 메서드의 두 번째 인수로 전달할 수 있습니다:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    $url = url('/invoice/'.$this->invoice->id);

    return (new MailMessage)
        ->subject('Invoice Paid')
        ->markdown('mail.invoice.paid', ['url' => $url]);
}
```



<a name="writing-the-message"></a>
### 메시지 작성

Markdown 메일 알림은 Blade 컴포넌트와 Markdown 문법의 조합을 사용하여, Laravel의 사전 제작된 알림 컴포넌트를 활용하면서 쉽게 알림을 구성할 수 있습니다:

```blade
<x-mail::message>
# Invoice Paid

Your invoice has been paid!

<x-mail::button :url="$url">
View Invoice
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```



> [!NOTE]
> Markdown 이메일을 작성할 때 과도한 들여쓰기를 사용하지 마세요. Markdown 표준에 따르면, Markdown 파서가 들여쓰기가 된 내용을 코드 블록으로 렌더링합니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 두 가지 인수를 받으며, 하나는 `url`이고 선택 사항인 하나는 `color`입니다. 지원되는 색상은 `primary`, `green`, `red`입니다. 알림에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="green">
View Invoice
</x-mail::button>
```



<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 알림의 나머지 부분과 약간 다른 배경색을 가진 패널에 렌더링합니다. 이를 통해 특정 텍스트 블록에 주목을 끌 수 있습니다:

```blade
<x-mail::panel>
This is the panel content.
</x-mail::panel>
```



<a name="table-component"></a>
#### 테이블 컴포넌트

테이블 컴포넌트를 사용하면 Markdown 테이블을 HTML 테이블로 변환할 수 있습니다. 이 컴포넌트는 Markdown 테이블을 내용으로 받아들입니다. 테이블 열 정렬은 기본 Markdown 테이블 정렬 구문을 사용하여 지원됩니다:

```blade
<x-mail::table>
| Laravel       | Table         | Example       |
| ------------- | :-----------: | ------------: |
| Col 2 is      | Centered      | $10           |
| Col 3 is      | Right-Aligned | $20           |
</x-mail::table>
```



<a name="customizing-the-components"></a>
### 구성 요소 사용자 정의

마크다운 알림 구성 요소를 모두 내 애플리케이션으로 내보내어 사용자 정의할 수 있습니다. 구성 요소를 내보내려면 `vendor:publish` Artisan 명령어를 사용하여 `laravel-mail` 자산 태그를 게시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```



This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like.

<a name="customizing-the-css"></a>
#### Customizing the CSS

After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be in-lined within the HTML representations of your Markdown notifications.

If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of the `mail` configuration file to match the name of your new theme.

To customize the theme for an individual notification, you may call the `theme` method while building the notification's mail message. The `theme` method accepts the name of the theme that should be used when sending the notification:

```php
/**
 * Get the mail representation of the notification.
 */
public function toMail(object $notifiable): MailMessage
{
    return (new MailMessage)
        ->theme('invoice')
        ->subject('Invoice Paid')
        ->markdown('mail.invoice.paid', ['url' => $url]);
}
```



<a name="database-notifications"></a>
## 데이터베이스 알림

<a name="database-prerequisites"></a>
### 전제 조건

`database` 알림 채널은 데이터베이스 테이블에 알림 정보를 저장합니다. 이 테이블에는 알림 유형과 알림을 설명하는 JSON 데이터 구조와 같은 정보가 포함됩니다.

이 테이블을 쿼리하여 애플리케이션의 사용자 인터페이스에 알림을 표시할 수 있습니다. 그러나 그렇게 하기 전에 알림을 보관할 데이터베이스 테이블을 생성해야 합니다. 적절한 테이블 스키마를 가진 [마이그레이션](/docs/{{version}}/migrations)을 생성하려면 `make:notifications-table` 명령을 사용할 수 있습니다:

```shell
php artisan make:notifications-table

php artisan migrate
```



> [!NOTE]
> 알림 가능한 모델이 [UUID 또는 ULID 기본 키](/docs/{{version}}/eloquent#uuid-and-ulid-keys)를 사용하고 있는 경우, 알림 테이블 마이그레이션에서 `morphs` 메서드를 [uuidMorphs](/docs/{{version}}/migrations#column-method-uuidMorphs) 또는 [ulidMorphs](/docs/{{version}}/migrations#column-method-ulidMorphs)로 교체해야 합니다.

<a name="formatting-database-notifications"></a>
### 데이터베이스 알림 포맷팅

알림이 데이터베이스 테이블에 저장되는 것을 지원하는 경우, 알림 클래스에 `toDatabase` 또는 `toArray` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 수신하며 일반 PHP 배열을 반환해야 합니다. 반환된 배열은 JSON으로 인코딩되어 `data` 열에 `notifications` 테이블에 저장됩니다. `toArray` 메서드의 예제를 살펴보겠습니다:

```php
/**
 * Get the array representation of the notification.
 *
 * @return array<string, mixed>
 */
public function toArray(object $notifiable): array
{
    return [
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ];
}
```



알림이 애플리케이션의 데이터베이스에 저장되면 `type` 열은 기본적으로 알림의 클래스 이름으로 설정되고, `read_at` 열은 `null`가 됩니다. 그러나 알림 클래스에서 `databaseType` 및 `initialDatabaseReadAtValue` 메서드를 정의하여 이 동작을 커스터마이즈할 수 있습니다:

```php
use Illuminate\Support\Carbon;

/**
 * Get the notification's database type.
 */
public function databaseType(object $notifiable): string
{
    return 'invoice-paid';
}

/**
 * Get the initial value for the "read_at" column.
 */
public function initialDatabaseReadAtValue(): ?Carbon
{
    return null;
}
```



<a name="todatabase-vs-toarray"></a>
#### `toDatabase` 대 `toArray`

`toArray` 메서드는 `broadcast` 채널에서도 사용되어 어떤 데이터를 JavaScript 기반 프런트엔드에 브로드캐스트할지 결정합니다. `database`와 `broadcast` 채널에 대해 두 가지 다른 배열 표현을 사용하고 싶다면, `toArray` 메서드 대신 `toDatabase` 메서드를 정의해야 합니다.

<a name="accessing-the-notifications"></a>
### 알림에 접근하기

알림이 데이터베이스에 저장되면, 알림 가능한 엔티티에서 이를 편리하게 접근할 방법이 필요합니다. Laravel의 기본 `App\Models\User` 모델에 포함된 `Illuminate\Notifications\Notifiable` 트레이트에는 엔티티에 대한 알림을 반환하는 `notifications` [Eloquent 관계](/docs/{{version}}/eloquent-relationships)가 포함되어 있습니다. 알림을 가져오려면, 다른 Eloquent 관계처럼 이 메서드에 접근할 수 있습니다. 기본적으로 알림은 `created_at` 타임스탬프 기준으로 정렬되며, 가장 최근 알림이 컬렉션의 시작 부분에 위치합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->notifications as $notification) {
    echo $notification->type;
}
```



읽지 않은 알림만 가져오고 싶다면 `unreadNotifications` 관계를 사용할 수 있습니다. 다시 말하지만, 이러한 알림은 `created_at` 타임스탬프에 따라 정렬되며, 가장 최근 알림이 컬렉션의 시작 부분에 위치합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    echo $notification->type;
}
```



읽은 알림만 가져오고 싶다면, `readNotifications` 관계를 사용할 수 있습니다:

```php
$user = App\Models\User::find(1);

foreach ($user->readNotifications as $notification) {
    echo $notification->type;
}
```



> [!NOTE]
> JavaScript 클라이언트에서 알림에 접근하려면, 알림이 가능한 엔티티(예: 현재 사용자)에 대한 알림을 반환하는 애플리케이션용 알림 컨트롤러를 정의해야 합니다. 그런 다음 JavaScript 클라이언트에서 해당 컨트롤러의 URL로 HTTP 요청을 보낼 수 있습니다.

<a name="marking-notifications-as-read"></a>
### 알림 읽음 표시

일반적으로 사용자가 알림을 확인했을 때 해당 알림을 "읽음"으로 표시하고 싶을 것입니다. `Illuminate\Notifications\Notifiable` 트레이트는 `markAsRead` 메서드를 제공하며, 이는 알림 데이터베이스 레코드의 `read_at` 컬럼을 업데이트합니다:

```php
$user = App\Models\User::find(1);

foreach ($user->unreadNotifications as $notification) {
    $notification->markAsRead();
}
```



그러나 각 알림을 순회하는 대신, 알림 컬렉션에서 `markAsRead` 메서드를 직접 사용할 수 있습니다:

```php
$user->unreadNotifications->markAsRead();
```



데이터베이스에서 알림을 가져오지 않고 모든 알림을 읽음으로 표시하려면 일괄 업데이트 쿼리를 사용할 수도 있습니다:

```php
$user = App\Models\User::find(1);

$user->unreadNotifications()->update(['read_at' => now()]);
```



알림을 완전히 테이블에서 제거하려면 `delete`할 수 있습니다:

```php
$user->notifications()->delete();
```



<a name="broadcast-notifications"></a>
## Broadcast Notifications

<a name="broadcast-prerequisites"></a>
### Prerequisites

Before broadcasting notifications, you should configure and be familiar with Laravel's [event broadcasting](/docs/{{version}}/broadcasting) services. Event broadcasting provides a way to react to server-side Laravel events from your JavaScript powered frontend.

<a name="formatting-broadcast-notifications"></a>
### Formatting Broadcast Notifications

The `broadcast` channel broadcasts notifications using Laravel's [event broadcasting](/docs/{{version}}/broadcasting) services, allowing your JavaScript powered frontend to catch notifications in realtime. If a notification supports broadcasting, you can define a `toBroadcast` method on the notification class. This method will receive a `$notifiable` entity and should return a `BroadcastMessage` instance. If the `toBroadcast` method does not exist, the `toArray` method will be used to gather the data that should be broadcast. The returned data will be encoded as JSON and broadcast to your JavaScript powered frontend. Let's take a look at an example `toBroadcast` method:

```php
use Illuminate\Notifications\Messages\BroadcastMessage;

/**
 * Get the broadcastable representation of the notification.
 */
public function toBroadcast(object $notifiable): BroadcastMessage
{
    return new BroadcastMessage([
        'invoice_id' => $this->invoice->id,
        'amount' => $this->invoice->amount,
    ]);
}
```



<a name="broadcast-queue-configuration"></a>
#### 방송 큐 구성

모든 방송 알림은 방송을 위해 큐에 저장됩니다. 방송 작업을 큐에 저장하는 데 사용되는 큐 연결 또는 큐 이름을 구성하려면 `BroadcastMessage`의 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다:

```php
return (new BroadcastMessage($data))
    ->onConnection('sqs')
    ->onQueue('broadcasts');
```



<a name="customizing-the-notification-type"></a>
#### 알림 유형 맞춤 설정

지정한 데이터 외에도, 모든 방송 알림에는 알림의 전체 클래스 이름을 포함하는 `type` 필드가 있습니다. 알림 `type`를 맞춤 설정하려는 경우, 알림 클래스에 `broadcastType` 메서드를 정의할 수 있습니다:

```php
/**
 * Get the type of the notification being broadcast.
 */
public function broadcastType(): string
{
    return 'broadcast.message';
}
```



<a name="listening-for-notifications"></a>
### 알림 수신 대기

알림은 `{notifiable}.{id}` 관례를 사용하여 포맷된 비공개 채널에서 방송됩니다. 따라서 ID가 `1`인 `App\Models\User` 인스턴스로 알림을 보내는 경우, 알림은 `App.Models.User.1` 비공개 채널에서 방송됩니다. [Laravel Echo](/docs/{{version}}/broadcasting#client-side-installation)를 사용할 때, `notification` 메서드를 사용하여 채널에서 쉽게 알림을 수신할 수 있습니다:

```js
Echo.private('App.Models.User.' + userId)
    .notification((notification) => {
        console.log(notification.type);
    });
```



<a name="using-react-or-vue"></a>
#### React, Vue 또는 Svelte 사용하기

Laravel Echo에는 알림을 듣기 쉽게 해주는 React, Vue 및 Svelte 훅이 포함되어 있습니다. 시작하려면 `useEchoNotification` 훅을 호출하세요. 이 훅은 알림을 듣는 데 사용됩니다. `useEchoNotification` 훅은 소비 컴포넌트가 언마운트될 때 자동으로 채널을 떠나게 합니다:```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
</script>
```

```svelte tab=Svelte
<script>
import { useEchoNotification } from "@laravel/echo-svelte";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
);
</script>
```



기본적으로 훅은 모든 알림을 수신합니다. 수신하고자 하는 알림 유형을 지정하려면 `useEchoNotification`에 문자열 또는 유형 배열을 제공하면 됩니다:```js tab=React
import { useEchoNotification } from "@laravel/echo-react";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```

```vue tab=Vue
<script setup lang="ts">
import { useEchoNotification } from "@laravel/echo-vue";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
</script>
```

```svelte tab=Svelte
<script>
import { useEchoNotification } from "@laravel/echo-svelte";

useEchoNotification(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
</script>
```



알림 페이로드 데이터의 형식을 지정하여 더 높은 타입 안전성과 편집 편의성을 제공할 수도 있습니다:

```ts
type InvoicePaidNotification = {
    invoice_id: number;
    created_at: string;
};

useEchoNotification<InvoicePaidNotification>(
    `App.Models.User.${userId}`,
    (notification) => {
        console.log(notification.invoice_id);
        console.log(notification.created_at);
        console.log(notification.type);
    },
    'App.Notifications.InvoicePaid',
);
```



<a name="customizing-the-notification-channel"></a>
#### 알림 채널 사용자 정의

엔티티의 방송 알림이 전송되는 채널을 사용자 정의하고 싶다면, 알림 가능 엔티티에서 `receivesBroadcastNotificationsOn` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Broadcasting\PrivateChannel;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The channels the user receives notification broadcasts on.
     */
    public function receivesBroadcastNotificationsOn(): string
    {
        return 'users.'.$this->id;
    }
}
```



<a name="sms-notifications"></a>
## SMS 알림

<a name="sms-prerequisites"></a>
### 전제 조건

Laravel에서 SMS 알림을 보내는 기능은 [Vonage](https://www.vonage.com/)(이전 이름: Nexmo)를 통해 제공됩니다. Vonage를 통해 알림을 보내기 전에 `laravel/vonage-notification-channel`와 `guzzlehttp/guzzle` 패키지를 설치해야 합니다:

```shell
composer require laravel/vonage-notification-channel guzzlehttp/guzzle
```



패키지에는 [설정 파일](https://github.com/laravel/vonage-notification-channel/blob/3.x/config/vonage.php)이 포함되어 있습니다. 그러나 이 설정 파일을 자신의 애플리케이션으로 내보낼 필요는 없습니다. 단순히 `VONAGE_KEY` 및 `VONAGE_SECRET` 환경 변수를 사용하여 Vonage 공개 키와 비밀 키를 정의할 수 있습니다.

키를 정의한 후에는 SMS 메시지가 기본적으로 발송될 전화번호를 정의하는 `VONAGE_SMS_FROM` 환경 변수를 설정해야 합니다. 이 전화번호는 Vonage 제어판에서 생성할 수 있습니다:

```ini
VONAGE_SMS_FROM=15556666666
```



<a name="formatting-sms-notifications"></a>
### SMS 알림 형식 지정

알림이 SMS로 전송될 수 있는 경우, 알림 클래스에서 `toVonage` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔터티를 받아 `Illuminate\Notifications\Messages\VonageMessage` 인스턴스를 반환해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content');
}
```



<a name="unicode-content"></a>
#### 유니코드 내용

만약 SMS 메시지에 유니코드 문자가 포함될 경우, `VonageMessage` 인스턴스를 생성할 때 `unicode` 메서드를 호출해야 합니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your unicode message')
        ->unicode();
}
```



<a name="customizing-the-from-number"></a>
### "발신자" 번호 사용자 지정

`VONAGE_SMS_FROM` 환경 변수에 지정된 전화번호와 다른 전화번호에서 알림을 보내고 싶다면, `VonageMessage` 인스턴스에서 `from` 메서드를 호출할 수 있습니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->content('Your SMS message content')
        ->from('15554443333');
}
```



<a name="adding-a-client-reference"></a>
### 클라이언트 참조 추가

사용자, 팀 또는 클라이언트별 비용을 추적하려면 알림에 "클라이언트 참조"를 추가할 수 있습니다. Vonage는 이 클라이언트 참조를 사용하여 보고서를 생성할 수 있으므로 특정 고객의 SMS 사용량을 더 잘 이해할 수 있습니다. 클라이언트 참조는 최대 40자의 임의 문자열일 수 있습니다:

```php
use Illuminate\Notifications\Messages\VonageMessage;

/**
 * Get the Vonage / SMS representation of the notification.
 */
public function toVonage(object $notifiable): VonageMessage
{
    return (new VonageMessage)
        ->clientReference((string) $notifiable->id)
        ->content('Your SMS message content');
}
```



<a name="routing-sms-notifications"></a>
### SMS 알림 라우팅

Vonage 알림을 올바른 전화번호로 라우팅하려면, 알림 가능 엔티티에 `routeNotificationForVonage` 메서드를 정의하세요:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Vonage channel.
     */
    public function routeNotificationForVonage(Notification $notification): string
    {
        return $this->phone_number;
    }
}
```



<a name="slack-notifications"></a>
## 슬랙 알림

<a name="slack-prerequisites"></a>
### 전제 조건

슬랙 알림을 보내기 전에, Composer를 통해 슬랙 알림 채널을 설치해야 합니다:

```shell
composer require laravel/slack-notification-channel
```



또한, Slack 작업 공간을 위해 [Slack 앱](https://api.slack.com/apps?new_app=1)을 생성해야 합니다.

앱이 생성된 동일한 Slack 작업 공간으로 알림만 보내야 하는 경우, 앱에 `chat:write`, `chat:write.public`, `chat:write.customize` 권한 범위가 있는지 확인해야 합니다. 이러한 권한 범위는 Slack 내의 "OAuth & 권한" 앱 관리 탭에서 추가할 수 있습니다.

다음으로, 앱의 "봇 사용자 OAuth 토큰"을 복사하여 애플리케이션의 `services.php` 구성 파일 내 `slack` 구성 배열에 배치하세요. 이 토큰은 Slack의 "OAuth & 권한" 탭에서 확인할 수 있습니다:

```php
'slack' => [
    'notifications' => [
        'bot_user_oauth_token' => env('SLACK_BOT_USER_OAUTH_TOKEN'),
        'channel' => env('SLACK_BOT_USER_DEFAULT_CHANNEL'),
    ],
],
```



<a name="slack-app-distribution"></a>
#### 앱 배포

애플리케이션이 사용자의 소유인 외부 Slack 작업 공간으로 알림을 보낼 경우, 앱을 Slack을 통해 "배포"해야 합니다. 앱 배포는 Slack 내 애플리케이션의 "배포 관리" 탭에서 관리할 수 있습니다. 앱이 배포되면, [Socialite](/docs/{{version}}/socialite)를 사용하여 애플리케이션 사용자를 대신해 [Slack 봇 토큰을 얻을 수 있습니다](/docs/{{version}}/socialite#slack-bot-scopes).

<a name="formatting-slack-notifications"></a>
### Slack 알림 형식 지정

알림이 Slack 메시지로 전송될 수 있는 경우, 알림 클래스에 `toSlack` 메서드를 정의해야 합니다. 이 메서드는 `$notifiable` 엔티티를 받으며 `Illuminate\Notifications\Slack\SlackMessage` 인스턴스를 반환해야 합니다. [Slack의 Block Kit API](https://api.slack.com/block-kit)를 사용하여 풍부한 알림을 구성할 수 있습니다. 다음 예시는 [Slack의 Block Kit 빌더](https://app.slack.com/block-kit-builder/T01KWS6K23Z#%7B%22blocks%22:%5B%7B%22type%22:%22header%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Invoice%20Paid%22%7D%7D,%7B%22type%22:%22context%22,%22elements%22:%5B%7B%22type%22:%22plain_text%22,%22text%22:%22Customer%20%231234%22%7D%5D%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22An%20invoice%20has%20been%20paid.%22%7D,%22fields%22:%5B%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20No:*%5Cn1000%22%7D,%7B%22type%22:%22mrkdwn%22,%22text%22:%22*Invoice%20Recipient:*%5Cntaylor@laravel.com%22%7D%5D%7D,%7B%22type%22:%22divider%22%7D,%7B%22type%22:%22section%22,%22text%22:%7B%22type%22:%22plain_text%22,%22text%22:%22Congratulations!%22%7D%7D%5D%7D)에서 미리 볼 수 있습니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
            $block->field("*Invoice No:*\n1000")->markdown();
            $block->field("*Invoice Recipient:*\ntaylor@laravel.com")->markdown();
        })
        ->dividerBlock()
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('Congratulations!');
        });
}
```



<a name="using-slacks-block-kit-builder-template"></a>
#### 슬랙의 블록 킷 빌더 템플릿 사용하기

블록 킷 메시지를 구성하기 위해 유창한 메시지 빌더 메서드를 사용하는 대신, 슬랙의 블록 킷 빌더에서 생성된 원시 JSON 페이로드를 `usingBlockKitTemplate` 메서드에 제공할 수 있습니다:

```php
use Illuminate\Notifications\Slack\SlackMessage;
use Illuminate\Support\Str;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    $template = <<<JSON
        {
          "blocks": [
            {
              "type": "header",
              "text": {
                "type": "plain_text",
                "text": "Team Announcement"
              }
            },
            {
              "type": "section",
              "text": {
                "type": "plain_text",
                "text": "We are hiring!"
              }
            }
          ]
        }
    JSON;

    return (new SlackMessage)
        ->usingBlockKitTemplate($template);
}
```



<a name="slack-interactivity"></a>
### 슬랙 인터랙티비티

슬랙의 Block Kit 알림 시스템은 [사용자 상호작용 처리](https://api.slack.com/interactivity/handling) 기능을 제공합니다. 이러한 기능을 사용하려면, 슬랙 앱에서 "Interactivity"가 활성화되어 있어야 하며, 애플리케이션에서 제공하는 URL을 가리키는 "Request URL"이 설정되어야 합니다. 이러한 설정은 슬랙 내 앱 관리 탭의 "Interactivity & Shortcuts"에서 관리할 수 있습니다.

다음 예제는 `actionsBlock` 방법을 활용하며, 슬랙은 버튼을 클릭한 Slack 사용자, 클릭된 버튼의 ID 등을 포함한 페이로드와 함께 `POST` 요청을 당신의 "Request URL"로 전송합니다. 그런 다음 애플리케이션은 페이로드를 기반으로 어떤 동작을 취할지 결정할 수 있습니다. 또한 [요청이 슬랙에서 이루어진 것인지 확인](https://api.slack.com/authentication/verifying-requests-from-slack)해야 합니다.

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
             // ID defaults to "button_acknowledge_invoice"...
            $block->button('Acknowledge Invoice')->primary();

            // Manually configure the ID...
            $block->button('Deny')->danger()->id('deny_invoice');
        });
}
```



<a name="slack-confirmation-modals"></a>
#### 확인 모달

사용자가 작업이 수행되기 전에 확인을 요구하도록 하려면, 버튼을 정의할 때 `confirm` 메서드를 호출할 수 있습니다. `confirm` 메서드는 메시지와 `ConfirmObject` 인스턴스를 받는 클로저를 받습니다:

```php
use Illuminate\Notifications\Slack\BlockKit\Blocks\ActionsBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\ContextBlock;
use Illuminate\Notifications\Slack\BlockKit\Blocks\SectionBlock;
use Illuminate\Notifications\Slack\BlockKit\Composites\ConfirmObject;
use Illuminate\Notifications\Slack\SlackMessage;

/**
 * Get the Slack representation of the notification.
 */
public function toSlack(object $notifiable): SlackMessage
{
    return (new SlackMessage)
        ->text('One of your invoices has been paid!')
        ->headerBlock('Invoice Paid')
        ->contextBlock(function (ContextBlock $block) {
            $block->text('Customer #1234');
        })
        ->sectionBlock(function (SectionBlock $block) {
            $block->text('An invoice has been paid.');
        })
        ->actionsBlock(function (ActionsBlock $block) {
            $block->button('Acknowledge Invoice')
                ->primary()
                ->confirm(
                    'Acknowledge the payment and send a thank you email?',
                    function (ConfirmObject $dialog) {
                        $dialog->confirm('Yes');
                        $dialog->deny('No');
                    }
                );
        });
}
```



<a name="inspecting-slack-blocks"></a>
#### 슬랙 블록 검사하기

작성 중인 블록을 빠르게 검사하고 싶다면 `SlackMessage` 인스턴스에서 `dd` 메서드를 호출할 수 있습니다. `dd` 메서드는 URL을 생성하여 슬랙의 [Block Kit Builder](https://app.slack.com/block-kit-builder/)에 덤프하며, 브라우저에서 페이로드와 알림의 미리보기를 표시합니다. `dd` 메서드에 `true`를 전달하여 원시 페이로드를 덤프할 수도 있습니다:

```php
return (new SlackMessage)
    ->text('One of your invoices has been paid!')
    ->headerBlock('Invoice Paid')
    ->dd();
```



<a name="routing-slack-notifications"></a>
### Slack 알림 라우팅

적절한 Slack 팀과 채널로 Slack 알림을 전달하려면, 알림 가능한 모델에 `routeNotificationForSlack` 메서드를 정의하세요. 이 메서드는 세 가지 값 중 하나를 반환할 수 있습니다:

- `null` - 알림 자체에 구성된 채널로 라우팅을 연기합니다. 알림 내에서 채널을 구성하려면 `to` 메서드를 `SlackMessage` 생성 시 사용할 수 있습니다.
- 알림을 보낼 Slack 채널을 지정하는 문자열, 예: `#support-channel`.
- `SlackRoute` 인스턴스, OAuth 토큰과 채널 이름을 지정할 수 있음, 예: `SlackRoute::make($this->slack_channel, $this->slack_token)`. 이 메서드는 외부 워크스페이스에 알림을 보낼 때 사용해야 합니다.

예를 들어, `routeNotificationForSlack` 메서드에서 `#support-channel`를 반환하면, 애플리케이션의 `services.php` 구성 파일에 있는 Bot User OAuth 토큰과 연결된 워크스페이스의 `#support-channel` 채널로 알림이 전송됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return '#support-channel';
    }
}
```



<a name="notifying-external-slack-workspaces"></a>
### 외부 Slack 워크스페이스에 알림 보내기

> [!NOTE]
> 외부 Slack 워크스페이스에 알림을 보내기 전에, 귀하의 Slack 앱은 [배포](#slack-app-distribution)되어 있어야 합니다.

물론, 애플리케이션 사용자가 소유한 Slack 워크스페이스로 알림을 보내고 싶은 경우가 많습니다. 이를 위해 먼저 사용자의 Slack OAuth 토큰을 얻어야 합니다. 다행히도, [Laravel Socialite](/docs/{{version}}/socialite)에는 Slack 드라이버가 포함되어 있어 애플리케이션 사용자를 쉽게 Slack으로 인증하고 [봇 토큰을 얻을 수](/docs/{{version}}/socialite#slack-bot-scopes) 있습니다.

봇 토큰을 얻어 애플리케이션 데이터베이스에 저장한 후에는, `SlackRoute::make` 방법을 사용하여 알림을 사용자의 워크스페이스로 전달할 수 있습니다. 또한, 애플리케이션은 사용자가 알림을 보낼 채널을 지정할 수 있는 기회를 제공해야 할 것입니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Illuminate\Notifications\Notification;
use Illuminate\Notifications\Slack\SlackRoute;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * Route notifications for the Slack channel.
     */
    public function routeNotificationForSlack(Notification $notification): mixed
    {
        return SlackRoute::make($this->slack_channel, $this->slack_token);
    }
}
```



<a name="localizing-notifications"></a>
## 알림 현지화

Laravel은 HTTP 요청의 현재 로케일이 아닌 다른 로케일로 알림을 보낼 수 있으며, 알림이 큐에 들어가더라도 이 로케일을 기억합니다.

이를 수행하기 위해, `Illuminate\Notifications\Notification` 클래스는 원하는 언어를 설정할 수 있는 `locale` 메서드를 제공합니다. 알림이 평가되는 동안 애플리케이션은 이 로케일로 변경되며, 평가가 완료되면 이전 로케일로 돌아갑니다:

```php
$user->notify((new InvoicePaid($invoice))->locale('es'));
```



여러 신고 항목의 현지화는 `Notification` 퍼사드를 통해서도 달성될 수 있습니다:

```php
Notification::locale('es')->send(
    $users, new InvoicePaid($invoice)
);
```



<a name="user-preferred-locales"></a>
#### 사용자가 선호하는 로케일

때때로 애플리케이션은 각 사용자가 선호하는 로케일을 저장합니다. notifiable 모델에서 `HasLocalePreference` 계약을 구현하면, 알림을 보낼 때 Laravel이 이 저장된 로케일을 사용하도록 지시할 수 있습니다:

```php
use Illuminate\Contracts\Translation\HasLocalePreference;

class User extends Model implements HasLocalePreference
{
    /**
     * Get the user's preferred locale.
     */
    public function preferredLocale(): string
    {
        return $this->locale;
    }
}
```



인터페이스를 구현하면, Laravel은 모델에 알림과 메일을 보낼 때 자동으로 선호하는 로케일을 사용합니다. 따라서 이 인터페이스를 사용할 때는 `locale` 메서드를 호출할 필요가 없습니다:

```php
$user->notify(new InvoicePaid($invoice));
```



<a name="testing"></a>
## 테스트

알림이 전송되지 않도록 하려면 `Notification` 퍼사드의 `fake` 메서드를 사용할 수 있습니다. 일반적으로 알림 전송은 실제로 테스트 중인 코드와 관련이 없습니다. 대부분의 경우, Laravel이 특정 알림을 전송하도록 지시되었는지만 단순히 확인하는 것으로 충분합니다.

`Notification` 퍼사드의 `fake` 메서드를 호출한 후에는, 알림이 사용자에게 전송되도록 지시되었는지 확인하고, 알림이 받은 데이터를 검사할 수도 있습니다:```php tab=Pest
<?php

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;

test('orders can be shipped', function () {
    Notification::fake();

    // Perform order shipping...

    // Assert that no notifications were sent...
    Notification::assertNothingSent();

    // Assert a notification was sent to the given users...
    Notification::assertSentTo(
        [$user], OrderShipped::class
    );

    // Assert a notification was not sent...
    Notification::assertNotSentTo(
        [$user], AnotherNotification::class
    );

    // Assert a notification was sent twice...
    Notification::assertSentTimes(WeeklyReminder::class, 2);

    // Assert that a notification was sent to a user exactly once...
    Notification::assertSentToOnce($user, OrderShipped::class);

    // Assert that a given number of notifications were sent...
    Notification::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Notifications\OrderShipped;
use Illuminate\Support\Facades\Notification;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Notification::fake();

        // Perform order shipping...

        // Assert that no notifications were sent...
        Notification::assertNothingSent();

        // Assert a notification was sent to the given users...
        Notification::assertSentTo(
            [$user], OrderShipped::class
        );

        // Assert a notification was not sent...
        Notification::assertNotSentTo(
            [$user], AnotherNotification::class
        );

        // Assert a notification was sent twice...
        Notification::assertSentTimes(WeeklyReminder::class, 2);

        // Assert that a notification was sent to a user exactly once...
        Notification::assertSentToOnce($user, OrderShipped::class);

        // Assert that a given number of notifications were sent...
        Notification::assertCount(3);
    }
}
```



주어진 "진실 테스트"를 통과하는 알림이 전송되었는지 확인하기 위해 `assertSentTo` 또는 `assertNotSentTo` 메서드에 클로저를 전달할 수 있습니다. 만약 주어진 진실 테스트를 통과하는 알림이 적어도 하나 전송되었다면, 해당 어설션은 성공하게 됩니다:

```php
Notification::assertSentTo(
    $user,
    function (OrderShipped $notification, array $channels) use ($order) {
        return $notification->order->id === $order->id;
    }
);
```



<a name="testing-on-demand-notifications"></a>
#### 주문형 알림

테스트 중인 코드가 [주문형 알림](#on-demand-notifications)을 전송하는 경우, `assertSentOnDemand` 방법을 통해 주문형 알림이 전송되었는지 테스트할 수 있습니다:

```php
Notification::assertSentOnDemand(OrderShipped::class);
Notification::assertSentOnDemandOnce(OrderShipped::class);
```



`assertSentOnDemand` 메서드의 두 번째 인수로 클로저를 전달하면 주문형 알림이 올바른 '경로' 주소로 전송되었는지 확인할 수 있습니다:

```php
Notification::assertSentOnDemand(
    OrderShipped::class,
    function (OrderShipped $notification, array $channels, object $notifiable) use ($user) {
        return $notifiable->routes['mail'] === $user->email;
    }
);
```



<a name="notification-events"></a>
## 알림 이벤트

<a name="notification-sending-event"></a>
#### 알림 전송 이벤트

알림이 전송될 때, `Illuminate\Notifications\Events\NotificationSending` 이벤트가 알림 시스템에 의해 발송됩니다. 이 이벤트에는 "알림 가능" 엔터티와 알림 인스턴스 자체가 포함됩니다. 애플리케이션 내에서 이 이벤트에 대한 [이벤트 리스너](/docs/{{version}}/events)를 생성할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSending;

class CheckNotificationStatus
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSending $event): void
    {
        // ...
    }
}
```



`NotificationSending` 이벤트에 대한 이벤트 수신기가 `handle` 메서드에서 `false`를 반환하면 알림이 전송되지 않습니다:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): bool
{
    return false;
}
```



이벤트 리스너 내에서 이벤트의 `notifiable`, `notification`, `channel` 속성에 접근하여 알림 수신자 또는 알림 자체에 대해 더 자세히 알 수 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSending $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
}
```



<a name="notification-sent-event"></a>
#### 알림 전송 이벤트

알림이 전송되면, `Illuminate\Notifications\Events\NotificationSent` [이벤트](/docs/{{version}}/events)가 알림 시스템에 의해 발송됩니다. 이는 "알림 대상" 엔티티와 알림 인스턴스 자체를 포함합니다. 애플리케이션 내에서 이 이벤트에 대한 [이벤트 리스너](/docs/{{version}}/events)를 생성할 수 있습니다:

```php
use Illuminate\Notifications\Events\NotificationSent;

class LogNotification
{
    /**
     * Handle the event.
     */
    public function handle(NotificationSent $event): void
    {
        // ...
    }
}
```



이벤트 리스너 내에서 이벤트의 `notifiable`, `notification`, `channel` 및 `response` 속성에 접근하여 알림 수신자 또는 알림 자체에 대해 더 자세히 알아볼 수 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(NotificationSent $event): void
{
    // $event->channel
    // $event->notifiable
    // $event->notification
    // $event->response
}
```



<a name="custom-channels"></a>
## 사용자 정의 채널

Laravel은 몇 가지 알림 채널을 기본 제공하지만, 다른 채널을 통해 알림을 전달하기 위해 직접 드라이버를 작성할 수도 있습니다. Laravel은 이를 쉽게 만들어 줍니다. 시작하려면 `send` 메서드를 포함하는 클래스를 정의하세요. 이 메서드는 두 개의 인자를 받아야 합니다: `$notifiable`와 `$notification`.

`send` 메서드 내에서, 채널이 이해할 수 있는 메시지 객체를 가져오기 위해 알림에 메서드를 호출한 후 알림을 `$notifiable` 인스턴스로 원하는 방식으로 보낼 수 있습니다:

```php
<?php

namespace App\Notifications;

use Illuminate\Notifications\Notification;

class VoiceChannel
{
    /**
     * Send the given notification.
     */
    public function send(object $notifiable, Notification $notification): void
    {
        $message = $notification->toVoice($notifiable);

        // Send notification to the $notifiable instance...
    }
}
```



알림 채널 클래스가 정의되면, 알림의 `via` 메서드에서 클래스 이름을 반환할 수 있습니다. 이 예제에서, 알림의 `toVoice` 메서드는 음성 메시지를 나타내기 위해 선택한 객체를 반환할 수 있습니다. 예를 들어, 이러한 메시지를 나타내기 위해 자신의 `VoiceMessage` 클래스를 정의할 수 있습니다:

```php
<?php

namespace App\Notifications;

use App\Notifications\Messages\VoiceMessage;
use App\Notifications\VoiceChannel;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Notification;

class InvoicePaid extends Notification
{
    use Queueable;

    /**
     * Get the notification channels.
     */
    public function via(object $notifiable): string
    {
        return VoiceChannel::class;
    }

    /**
     * Get the voice representation of the notification.
     */
    public function toVoice(object $notifiable): VoiceMessage
    {
        // ...
    }
}
```
{% endraw %}
