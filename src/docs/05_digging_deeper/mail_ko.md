---
layout: docs
title: "Mail"
---

{% raw %}
# Mail

- [Introduction](#introduction)
    - [Configuration](#configuration)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Failover Configuration](#failover-configuration)
    - [Round Robin Configuration](#round-robin-configuration)
- [Generating Mailables](#generating-mailables)
- [Writing Mailables](#writing-mailables)
    - [Configuring the Sender](#configuring-the-sender)
    - [Configuring the View](#configuring-the-view)
    - [View Data](#view-data)
    - [Attachments](#attachments)
    - [Inline Attachments](#inline-attachments)
    - [Attachable Objects](#attachable-objects)
    - [Headers](#headers)
    - [Tags and Metadata](#tags-and-metadata)
    - [Customizing the Symfony Message](#customizing-the-symfony-message)
- [Markdown Mailables](#markdown-mailables)
    - [Generating Markdown Mailables](#generating-markdown-mailables)
    - [Writing Markdown Messages](#writing-markdown-messages)
    - [Customizing the Components](#customizing-the-components)
- [Sending Mail](#sending-mail)
    - [Queueing Mail](#queueing-mail)
- [Rendering Mailables](#rendering-mailables)
    - [Previewing Mailables in the Browser](#previewing-mailables-in-the-browser)
- [Localizing Mailables](#localizing-mailables)
- [Testing](#testing-mailables)
    - [Testing Mailable Content](#testing-mailable-content)
    - [Testing Mailable Sending](#testing-mailable-sending)
- [Mail and Local Development](#mail-and-local-development)
- [Events](#events)
- [Custom Transports](#custom-transports)
    - [Additional Symfony Transports](#additional-symfony-transports)

<a name="introduction"></a>
## Introduction

Sending email doesn't have to be complicated. Laravel provides a clean, simple email API powered by the popular [Symfony Mailer](https://symfony.com/doc/current/mailer.html) component. Laravel and Symfony Mailer provide drivers for sending email via SMTP, Cloudflare, Mailgun, Postmark, Resend, Amazon SES, and `sendmail`, allowing you to quickly get started sending mail through a local or cloud-based service of your choice.

<a name="configuration"></a>
### Configuration



Laravel's email services may be configured via your application's `config/mail.php` configuration file. Each mailer configured within this file may have its own unique configuration and even its own unique "transport", allowing your application to use different email services to send certain email messages. For example, your application might use Postmark to send transactional emails while using Amazon SES to send bulk emails.

Within your `mail` configuration file, you will find a `mailers` configuration array. This array contains a sample configuration entry for each of the major mail drivers / transports supported by Laravel, while the `default` configuration value determines which mailer will be used by default when your application needs to send an email message.

<a name="driver-prerequisites"></a>
### Driver / Transport Prerequisites

The API based drivers such as Mailgun, Postmark, and Resend are often simpler and faster than sending mail via SMTP servers. Whenever possible, we recommend that you use one of these drivers.

<a name="cloudflare-driver"></a>
#### Cloudflare Driver

To use the Cloudflare driver, install Symfony's HTTP Client via Composer:

```shell
composer require symfony/http-client
```



다음으로, 애플리케이션의 `config/mail.php` 구성 파일에서 두 가지를 변경해야 합니다. 먼저, 기본 메일러를 `cloudflare`로 설정하십시오:

```php
'default' => env('MAIL_MAILER', 'cloudflare'),
```



둘째, 다음 구성 배열을 `mailers` 배열에 추가하십시오:

```php
'cloudflare' => [
    'transport' => 'cloudflare',
],
```



애플리케이션의 기본 메일러를 구성한 후, 다음 옵션을 `config/services.php` 구성 파일에 추가하세요:

```php
'cloudflare' => [
    'account_id' => env('CLOUDFLARE_ACCOUNT_ID'),
    'key' => env('CLOUDFLARE_KEY'),
],
```



<a name="mailgun-driver"></a>
#### Mailgun 드라이버

Mailgun 드라이버를 사용하려면 Composer를 통해 Symfony의 Mailgun Mailer 전송을 설치하세요:

```shell
composer require symfony/mailgun-mailer symfony/http-client
```



다음으로, 애플리케이션의 `config/mail.php` 구성 파일에서 두 가지 변경을 해야 합니다. 먼저, 기본 메일러를 `mailgun`로 설정하십시오:

```php
'default' => env('MAIL_MAILER', 'mailgun'),
```



둘째, 다음 구성 배열을 `mailers` 배열에 추가하십시오:

```php
'mailgun' => [
    'transport' => 'mailgun',
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```



애플리케이션의 기본 메일러를 구성한 후, 다음 옵션을 `config/services.php` 구성 파일에 추가하세요:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    'scheme' => 'https',
],
```



미국 [Mailgun 지역](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview#mailgun-regions)을 사용하고 있지 않은 경우, `services` 구성 파일에서 지역의 엔드포인트를 정의할 수 있습니다:

```php
'mailgun' => [
    'domain' => env('MAILGUN_DOMAIN'),
    'secret' => env('MAILGUN_SECRET'),
    'endpoint' => env('MAILGUN_ENDPOINT', 'api.eu.mailgun.net'),
    'scheme' => 'https',
],
```



<a name="postmark-driver"></a>
#### 포스트마크 드라이버

[Postmark](https://postmarkapp.com/) 드라이버를 사용하려면 Composer를 통해 Symfony의 Postmark 메일러 트랜스포트를 설치하세요:

```shell
composer require symfony/postmark-mailer symfony/http-client
```



다음으로, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `postmark`로 설정합니다. 애플리케이션의 기본 메일러를 설정한 후, `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인하십시오:

```php
'postmark' => [
    'key' => env('POSTMARK_API_KEY'),
],
```



특정 메일러가 사용할 Postmark 메시지 스트림을 지정하고 싶다면, 해당 메일러의 구성 배열에 `message_stream_id` 구성 옵션을 추가할 수 있습니다. 이 구성 배열은 애플리케이션의 `config/mail.php` 구성 파일에서 확인할 수 있습니다:

```php
'postmark' => [
    'transport' => 'postmark',
    'message_stream_id' => env('POSTMARK_MESSAGE_STREAM_ID'),
    // 'client' => [
    //     'timeout' => 5,
    // ],
],
```



이렇게 하면 서로 다른 메시지 스트림으로 여러 개의 Postmark 메일러를 설정할 수도 있습니다.

<a name="resend-driver"></a>
#### Resend 드라이버

[Resend](https://resend.com/) 드라이버를 사용하려면, Composer를 통해 Resend의 PHP SDK를 설치하세요:

```shell
composer require resend/resend-php
```



다음으로, 애플리케이션의 `config/mail.php` 설정 파일에서 `default` 옵션을 `resend`로 설정합니다. 애플리케이션의 기본 메일러를 설정한 후, `config/services.php` 설정 파일에 다음 옵션이 포함되어 있는지 확인하십시오:

```php
'resend' => [
    'key' => env('RESEND_API_KEY'),
],
```



<a name="ses-driver"></a>
#### SES 드라이버

Amazon SES 드라이버를 사용하려면 먼저 PHP용 Amazon AWS SDK를 설치해야 합니다. 이 라이브러리는 Composer 패키지 관리자를 통해 설치할 수 있습니다:

```shell
composer require aws/aws-sdk-php
```



다음으로, `config/mail.php` 구성 파일에서 `default` 옵션을 `ses`로 설정하고, `config/services.php` 구성 파일에 다음 옵션들이 포함되어 있는지 확인하십시오:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
],
```



세션 토큰을 통해 AWS [임시 자격 증명](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html)을 사용하려면, 애플리케이션의 SES 구성에 `token` 키를 추가할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'token' => env('AWS_SESSION_TOKEN'),
],
```



SES의 [구독 관리 기능](https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html)과 상호작용하려면, 메일 메시지의 [headers](#headers) 메소드가 반환하는 배열에 `X-Ses-List-Management-Options` 헤더를 포함시킬 수 있습니다:

```php
/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        text: [
            'X-Ses-List-Management-Options' => 'contactListName=MyContactList;topicName=MyTopic',
        ],
    );
}
```



SES [테넌트](https://docs.aws.amazon.com/ses/latest/dg/tenants.html)를 통해 이메일을 보내려면 `headers` 메서드에서 `X-Ses-Tenant-Name` 헤더를 반환할 수 있습니다. Laravel은 메시지를 보낼 때 SES에 헤더 값을 `TenantName` 옵션으로 전달합니다:

```php
public function headers(): Headers
{
    return new Headers(
        text: [
            'X-Ses-Tenant-Name' => 'tenant-id',
        ],
    );
}
```



Laravel이 이메일을 보낼 때 AWS SDK의 `SendEmail` 메서드에 전달해야 하는 [추가 옵션](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-sesv2-2019-09-27.html#sendemail)을 정의하고 싶다면, `ses` 설정 내에 `options` 배열을 정의할 수 있습니다:

```php
'ses' => [
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'options' => [
        'ConfigurationSetName' => 'MyConfigurationSet',
        'EmailTags' => [
            ['Name' => 'foo', 'Value' => 'bar'],
        ],
    ],
],
```



<a name="failover-configuration"></a>
### 장애 조치 구성

때때로, 애플리케이션의 메일을 전송하도록 구성한 외부 서비스가 다운될 수 있습니다. 이러한 경우, 기본 전송 드라이버가 다운될 경우 사용될 하나 이상의 백업 메일 전송 구성을 정의하는 것이 유용할 수 있습니다.

이를 달성하려면, 애플리케이션의 `mail` 구성 파일 내에서 `failover` 전송을 사용하는 메일러를 정의해야 합니다. 애플리케이션 `failover` 메일러의 구성 배열에는, 구성된 메일러가 전송을 위해 선택될 순서를 참조하는 `mailers` 배열이 포함되어야 합니다:

```php
'mailers' => [
    'failover' => [
        'transport' => 'failover',
        'mailers' => [
            'postmark',
            'mailgun',
            'sendmail',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```



`failover` 전송을 사용하는 메일러를 구성한 후에는, 대체 기능을 사용하기 위해 실패 시 전환(failover) 메일러를 애플리케이션의 `.env` 파일에서 기본 메일러로 설정해야 합니다.

```ini
MAIL_MAILER=failover
```



<a name="round-robin-configuration"></a>
### 라운드 로빈 구성

`roundrobin` 전송을 사용하면 여러 메일러에 걸쳐 메일 발송 작업을 분산시킬 수 있습니다. 시작하려면, `roundrobin` 전송을 사용하는 메일러를 애플리케이션의 `mail` 구성 파일 내에 정의하세요. 애플리케이션의 `roundrobin` 메일러에 대한 구성 배열은 어떤 구성된 메일러를 전송에 사용할지 참조하는 `mailers` 배열을 포함해야 합니다:

```php
'mailers' => [
    'roundrobin' => [
        'transport' => 'roundrobin',
        'mailers' => [
            'ses',
            'postmark',
        ],
        'retry_after' => 60,
    ],

    // ...
],
```



라운드 로빈 메일러가 정의되면, 애플리케이션의 `mail` 구성 파일 내에서 `default` 구성 키의 값으로 해당 메일러의 이름을 지정하여 이 메일러를 애플리케이션에서 사용하는 기본 메일러로 설정해야 합니다:

```php
'default' => env('MAIL_MAILER', 'roundrobin'),
```



라운드 로빈 전송은 구성된 메일러 목록에서 무작위로 메일러를 선택한 다음, 이후 이메일마다 다음 사용 가능한 메일러로 전환합니다. *[고가용성](https://en.wikipedia.org/wiki/High_availability)*을 달성하는 데 도움이 되는 `failover` 전송과 달리, `roundrobin` 전송은 *[로드 밸런싱](https://en.wikipedia.org/wiki/Load_balancing_(computing)*을 제공합니다.

<a name="generating-mailables"></a>
## 메일러 생성

Laravel 애플리케이션을 구축할 때, 애플리케이션에서 보내는 각 이메일 유형은 "메일러(mailable)" 클래스에 의해 표현됩니다. 이러한 클래스는 `app/Mail` 디렉토리에 저장됩니다. 애플리케이션에서 이 디렉토리가 보이지 않더라도 걱정하지 마세요. 첫 번째 메일러 클래스를 `make:mail` Artisan 명령을 사용하여 생성할 때 자동으로 생성됩니다.

```shell
php artisan make:mail OrderShipped
```



<a name="writing-mailables"></a>
## 메일 작성하기

메일 클래스를 생성한 후에는 그 내용을 살펴보기 위해 열어봅시다. 메일 클래스 구성은 여러 메서드에서 이루어지며, `envelope`, `content`, `attachments` 메서드를 포함합니다.

`envelope` 메서드는 메시지의 주제와 경우에 따라 수신자를 정의하는 `Illuminate\Mail\Mailables\Envelope` 객체를 반환합니다. `content` 메서드는 메시지 내용을 생성하는 데 사용할 [Blade 템플릿](/docs/{{version}}/blade)을 정의하는 `Illuminate\Mail\Mailables\Content` 객체를 반환합니다.

<a name="configuring-the-sender"></a>
### 발신자 구성

<a name="using-the-envelope"></a>
#### Envelope 사용

먼저, 이메일의 발신자를 구성하는 방법을 살펴봅시다. 즉, 이메일이 누구로부터 발송되는지를 설정하는 것입니다. 발신자를 구성하는 두 가지 방법이 있습니다. 먼저, 메시지의 envelope에서 "from" 주소를 지정할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Address;
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        from: new Address('jeffrey@example.com', 'Jeffrey Way'),
        subject: 'Order Shipped',
    );
}
```



원하신다면 `replyTo` 주소를 지정할 수도 있습니다:

```php
return new Envelope(
    from: new Address('jeffrey@example.com', 'Jeffrey Way'),
    replyTo: [
        new Address('taylor@example.com', 'Taylor Otwell'),
    ],
    subject: 'Order Shipped',
);
```



<a name="using-a-global-from-address"></a>
#### 전역 `from` 주소 사용

그러나 애플리케이션이 모든 이메일에 대해 동일한 "발신자(from)" 주소를 사용하는 경우, 생성하는 각 메일러 클래스에 이를 추가하는 것이 번거로울 수 있습니다. 대신, `config/mail.php` 구성 파일에서 전역 "발신자(from)" 주소를 지정할 수 있습니다. 이 주소는 메일러 클래스 내에서 다른 "발신자(from)" 주소가 지정되지 않은 경우 사용됩니다:

```php
'from' => [
    'address' => env('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name' => env('MAIL_FROM_NAME', 'Example'),
],
```



또한, `config/mail.php` 구성 파일 내에서 전역 "reply_to" 주소를 정의할 수 있습니다:

```php
'reply_to' => [
    'address' => 'example@example.com',
    'name' => 'App Name',
],
```



<a name="configuring-the-view"></a>
### 뷰 구성하기

메일 발송 클래스의 `content` 메서드 내에서 `view`, 즉 이메일 내용을 렌더링할 때 사용할 템플릿을 정의할 수 있습니다. 각 이메일은 일반적으로 [Blade 템플릿](/docs/{{version}}/blade)을 사용하여 내용을 렌더링하므로, 이메일의 HTML을 작성할 때 Blade 템플릿 엔진의 모든 기능과 편리함을 활용할 수 있습니다:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
    );
}
```



> [!NOTE]
> 모든 이메일 템플릿을 보관할 `resources/views/mail` 디렉토리를 만들고 싶을 수도 있지만, `resources/views` 디렉토리 내 어디에든 원하는 위치에 자유롭게 배치할 수 있습니다.

<a name="plain-text-emails"></a>
#### 일반 텍스트 이메일

이메일의 일반 텍스트 버전을 정의하고 싶다면, 메시지의 `Content` 정의를 생성할 때 일반 텍스트 템플릿을 지정할 수 있습니다. `view` 매개변수와 마찬가지로, `text` 매개변수는 이메일 콘텐츠를 렌더링하는 데 사용될 템플릿 이름이어야 합니다. 메시지에 대해 HTML 버전과 일반 텍스트 버전 모두를 자유롭게 정의할 수 있습니다:

```php
/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        view: 'mail.orders.shipped',
        text: 'mail.orders.shipped-text'
    );
}
```



명확성을 위해, `html` 매개변수는 `view` 매개변수의 별칭으로 사용될 수 있습니다:

```php
return new Content(
    html: 'mail.orders.shipped',
    text: 'mail.orders.shipped-text'
);
```



<a name="view-data"></a>
### 데이터 보기

<a name="via-public-properties"></a>
#### 공용 속성을 통해

일반적으로 이메일의 HTML을 렌더링할 때 사용할 수 있는 데이터를 뷰에 전달하고 싶을 것입니다. 데이터를 뷰에서 사용할 수 있도록 만드는 방법에는 두 가지가 있습니다. 먼저, 메일러 클래스에 정의된 모든 공용 속성은 자동으로 뷰에서 사용 가능하게 됩니다. 예를 들어, 메일러 클래스의 생성자에 데이터를 전달하고 해당 데이터를 클래스에 정의된 공용 속성에 설정할 수 있습니다:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        public Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
        );
    }
}
```



데이터가 공개 속성(public property)으로 설정되면 자동으로 뷰에서 사용할 수 있으므로, Blade 템플릿에서 다른 데이터를 접근하듯이 이 데이터를 접근할 수 있습니다:

```blade
<div>
    Price: {{ $order->price }}
</div>
```



<a name="via-the-with-parameter"></a>
#### `with` 매개변수를 통해:

이메일의 데이터를 템플릿으로 보내기 전에 형식을 맞춤 설정하고 싶다면, `Content` 정의의 `with` 매개변수를 통해 데이터를 수동으로 뷰에 전달할 수 있습니다. 일반적으로 데이터는 여전히 메일러 클래스의 생성자를 통해 전달하지만, 이 데이터를 `protected` 또는 `private` 속성에 설정해야 하며, 그래야 데이터가 자동으로 템플릿에 제공되지 않습니다:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct(
        protected Order $order,
    ) {}

    /**
     * Get the message content definition.
     */
    public function content(): Content
    {
        return new Content(
            view: 'mail.orders.shipped',
            with: [
                'orderName' => $this->order->name,
                'orderPrice' => $this->order->price,
            ],
        );
    }
}
```



데이터가 `with` 매개변수를 통해 전달되면, 해당 데이터는 자동으로 뷰에서 사용 가능하게 되므로, Blade 템플릿에서 다른 데이터를 접근하듯이 접근할 수 있습니다:

```blade
<div>
    Price: {{ $orderPrice }}
</div>
```



<a name="attachments"></a>
### 첨부파일

이메일에 첨부파일을 추가하려면 메시지의 `attachments` 메서드가 반환하는 배열에 첨부파일을 추가하면 됩니다. 먼저, `Attachment` 클래스에서 제공하는 `fromPath` 메서드에 파일 경로를 제공하여 첨부파일을 추가할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Attachment;

/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file'),
    ];
}
```



메시지에 파일을 첨부할 때, `as` 및 `withMime` 메서드를 사용하여 첨부 파일의 표시 이름 및/또는 MIME 유형을 지정할 수도 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```



<a name="attaching-files-from-disk"></a>
#### 디스크에서 파일 첨부하기

파일을 [파일 시스템 디스크](/docs/{{version}}/filesystem) 중 하나에 저장한 경우, `fromStorage` 첨부 방법을 사용하여 이메일에 첨부할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}
```



물론, 첨부 파일의 이름과 MIME 유형을 지정할 수도 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```



기본 디스크 외에 다른 저장 디스크를 지정해야 하는 경우 `fromStorageDisk` 방법을 사용할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromStorageDisk('s3', '/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf'),
    ];
}
```



<a name="raw-data-attachments"></a>
#### 원시 데이터 첨부

`fromData` 첨부 방법은 바이트의 원시 문자열을 첨부 파일로 첨부하는 데 사용될 수 있습니다. 예를 들어, 메모리에서 PDF를 생성했는데 이를 디스크에 저장하지 않고 이메일에 첨부하고 싶을 때 이 방법을 사용할 수 있습니다. `fromData` 방법은 첨부 파일에 할당될 이름과 함께 원시 데이터 바이트를 해결하는 클로저를 허용합니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [
        Attachment::fromData(fn () => $this->pdf, 'Report.pdf')
            ->withMime('application/pdf'),
    ];
}
```



<a name="inline-attachments"></a>
### 인라인 첨부 파일

이메일에 인라인 이미지를 삽입하는 것은 일반적으로 번거롭지만, Laravel은 이메일에 이미지를 첨부하는 편리한 방법을 제공합니다. 인라인 이미지를 삽입하려면 이메일 템플릿 내의 `$message` 변수에서 `embed` 메서드를 사용하세요. Laravel은 `$message` 변수를 모든 이메일 템플릿에서 자동으로 사용할 수 있도록 제공하므로 수동으로 전달하는 것에 대해 걱정할 필요가 없습니다:

```blade
<body>
    Here is an image:

    <img src="{{ $message->embed($pathToImage) }}">
</body>
```



> [!WARNING]
> `$message` 변수는 일반 텍스트 메시지 템플릿에서는 사용할 수 없습니다. 일반 텍스트 메시지는 인라인 첨부 파일을 사용하지 않기 때문입니다.

<a name="embedding-raw-data-attachments"></a>
#### 원시 데이터 첨부 파일 삽입

이미 이메일 템플릿에 삽입하려는 원시 이미지 데이터 문자열이 있는 경우, `$message` 변수에서 `embedData` 메서드를 호출할 수 있습니다. `embedData` 메서드를 호출할 때는 삽입할 이미지에 할당할 파일 이름을 제공해야 합니다:

```blade
<body>
    Here is an image from raw data:

    <img src="{{ $message->embedData($data, 'example-image.jpg') }}">
</body>
```



<a name="attachable-objects"></a>
### 첨부 가능한 객체

단순 문자열 경로를 통해 파일을 메시지에 첨부하는 것으로 충분한 경우가 많지만, 많은 경우 애플리케이션 내에서 첨부 가능한 엔티티는 클래스에 의해 표현됩니다. 예를 들어, 애플리케이션이 메시지에 사진을 첨부하는 경우, 애플리케이션에는 해당 사진을 나타내는 `Photo` 모델이 있을 수 있습니다. 그런 경우, `Photo` 모델을 `attach` 메서드에 전달하는 것이 편리하지 않을까요? 첨부 가능한 객체는 바로 그렇게 할 수 있게 해줍니다.

시작하려면, 메시지에 첨부될 객체에 `Illuminate\Contracts\Mail\Attachable` 인터페이스를 구현하세요. 이 인터페이스는 클래스가 `Illuminate\Mail\Attachment` 인스턴스를 반환하는 `toMailAttachment` 메서드를 정의하도록 요구합니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Mail\Attachable;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Mail\Attachment;

class Photo extends Model implements Attachable
{
    /**
     * Get the attachable representation of the model.
     */
    public function toMailAttachment(): Attachment
    {
        return Attachment::fromPath('/path/to/file');
    }
}
```



첨부 가능한 객체를 정의한 후, 이메일 메시지를 작성할 때 `attachments` 메서드에서 해당 객체의 인스턴스를 반환할 수 있습니다:

```php
/**
 * Get the attachments for the message.
 *
 * @return array<int, \Illuminate\Mail\Mailables\Attachment>
 */
public function attachments(): array
{
    return [$this->photo];
}
```



물론 첨부 파일 데이터는 Amazon S3와 같은 원격 파일 저장 서비스에 저장될 수 있습니다. 따라서 Laravel은 애플리케이션의 [파일시스템 디스크](/docs/{{version}}/filesystem)에 저장된 데이터에서 첨부 파일 인스턴스를 생성할 수도 있습니다:

```php
// Create an attachment from a file on your default disk...
return Attachment::fromStorage($this->path);

// Create an attachment from a file on a specific disk...
return Attachment::fromStorageDisk('backblaze', $this->path);
```



또한, 메모리에 있는 데이터를 통해 첨부 파일 인스턴스를 생성할 수 있습니다. 이를 수행하려면 `fromData` 메서드에 클로저를 제공하십시오. 클로저는 첨부 파일을 나타내는 원시 데이터를 반환해야 합니다:

```php
return Attachment::fromData(fn () => $this->content, 'Photo Name');
```



라라벨은 또한 첨부 파일을 사용자 정의하는 데 사용할 수 있는 추가 메서드를 제공합니다. 예를 들어, 파일의 이름과 MIME 유형을 사용자 정의하기 위해 `as` 및 `withMime` 메서드를 사용할 수 있습니다:

```php
return Attachment::fromPath('/path/to/file')
    ->as('Photo Name')
    ->withMime('image/jpeg');
```



<a name="headers"></a>
### 헤더

때때로 발신 메시지에 추가 헤더를 첨부해야 할 때가 있습니다. 예를 들어, 사용자 정의 `Message-Id` 또는 기타 임의의 텍스트 헤더를 설정해야 할 수도 있습니다.

이를 수행하려면, 메일러블에 `headers` 메서드를 정의하십시오. `headers` 메서드는 `Illuminate\Mail\Mailables\Headers` 인스턴스를 반환해야 합니다. 이 클래스는 `messageId`, `references`, 그리고 `text` 매개변수를 받습니다. 물론 특정 메시지에 필요한 매개변수만 제공할 수도 있습니다:

```php
use Illuminate\Mail\Mailables\Headers;

/**
 * Get the message headers.
 */
public function headers(): Headers
{
    return new Headers(
        messageId: 'custom-message-id@example.com',
        references: ['previous-message@example.com'],
        text: [
            'X-Custom-Header' => 'Custom Value',
        ],
    );
}
```



<a name="tags-and-metadata"></a>
### 태그와 메타데이터

Mailgun 및 Postmark와 같은 일부 타사 이메일 제공자는 메시지 "태그"와 "메타데이터"를 지원하며, 이를 통해 애플리케이션에서 보낸 이메일을 그룹화하고 추적할 수 있습니다. `Envelope` 정의를 통해 이메일 메시지에 태그와 메타데이터를 추가할 수 있습니다:

```php
use Illuminate\Mail\Mailables\Envelope;

/**
 * Get the message envelope.
 *
 * @return \Illuminate\Mail\Mailables\Envelope
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        tags: ['shipment'],
        metadata: [
            'order_id' => $this->order->id,
        ],
    );
}
```



애플리케이션이 Mailgun 드라이버를 사용하는 경우, [태그](https://documentation.mailgun.com/docs/mailgun/user-manual/tracking-messages/#tags) 및 [메타데이터](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/#attaching-metadata-to-messages)에 대한 자세한 정보는 Mailgun 문서를 참조할 수 있습니다. 마찬가지로, [태그](https://postmarkapp.com/blog/tags-support-for-smtp) 및 [메타데이터](https://postmarkapp.com/support/article/1125-custom-metadata-faq)에 대한 지원 정보는 Postmark 문서에서도 확인할 수 있습니다.

애플리케이션이 Amazon SES를 사용하여 이메일을 보내는 경우, 메시지에 [SES "태그"](https://docs.aws.amazon.com/ses/latest/APIReference/API_MessageTag.html)를 첨부하려면 `metadata` 방법을 사용해야 합니다.

<a name="customizing-the-symfony-message"></a>
### Symfony 메시지 맞춤화

Laravel의 메일 기능은 Symfony Mailer를 기반으로 합니다. Laravel은 메시지를 보내기 전에 Symfony Message 인스턴스와 함께 호출될 사용자 정의 콜백을 등록할 수 있도록 허용합니다. 이를 통해 메시지가 전송되기 전에 메시지를 깊이 있게 맞춤화할 수 있습니다. 이를 수행하려면 `Envelope` 정의에서 `using` 매개변수를 정의하십시오:

```php
use Illuminate\Mail\Mailables\Envelope;
use Symfony\Component\Mime\Email;

/**
 * Get the message envelope.
 */
public function envelope(): Envelope
{
    return new Envelope(
        subject: 'Order Shipped',
        using: [
            function (Email $message) {
                // ...
            },
        ]
    );
}
```



<a name="markdown-mailables"></a>
## 마크다운 메일

마크다운 메일 메시지를 사용하면 메일러블에서 [메일 알림](/docs/{{version}}/notifications#mail-notifications)의 미리 만들어진 템플릿과 구성 요소를 활용할 수 있습니다. 메시지가 마크다운으로 작성되었기 때문에, Laravel은 메시지에 대해 아름답고 반응형 HTML 템플릿을 렌더링할 수 있으며, 동일한 메시지의 일반 텍스트 버전도 자동으로 생성합니다.

<a name="generating-markdown-mailables"></a>
### 마크다운 메일 생성

해당 마크다운 템플릿과 함께 메일러블을 생성하려면, `make:mail` Artisan 명령의 `--markdown` 옵션을 사용할 수 있습니다:

```shell
php artisan make:mail OrderShipped --markdown=mail.orders.shipped
```



그런 다음, `content` 메서드 내에서 전송 가능한 `Content` 정의를 구성할 때 `view` 매개변수 대신 `markdown` 매개변수를 사용하십시오:

```php
use Illuminate\Mail\Mailables\Content;

/**
 * Get the message content definition.
 */
public function content(): Content
{
    return new Content(
        markdown: 'mail.orders.shipped',
        with: [
            'url' => $this->orderUrl,
        ],
    );
}
```



<a name="writing-markdown-messages"></a>
### 마크다운 메시지 작성

마크다운 메일러블은 블레이드 컴포넌트와 마크다운 구문을 결합하여 사용하며, 이를 통해 라라벨의 사전 제작된 이메일 UI 컴포넌트를 활용하면서 손쉽게 메일 메시지를 구성할 수 있습니다:

```blade
<x-mail::message>
# Order Shipped

Your order has been shipped!

<x-mail::button :url="$url">
View Order
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```



> [!NOTE]
> Markdown 이메일을 작성할 때 과도한 들여쓰기를 사용하지 마세요. Markdown 표준에 따르면, Markdown 파서가 들여쓰기가 된 내용을 코드 블록으로 렌더링합니다.

<a name="button-component"></a>
#### 버튼 컴포넌트

버튼 컴포넌트는 가운데 정렬된 버튼 링크를 렌더링합니다. 이 컴포넌트는 두 가지 인수를 받으며, 하나는 `url`이고 선택 사항인 하나는 `color`입니다. 지원되는 색상은 `primary`, `success`, `error`입니다. 메시지에 원하는 만큼 버튼 컴포넌트를 추가할 수 있습니다:

```blade
<x-mail::button :url="$url" color="success">
View Order
</x-mail::button>
```



<a name="panel-component"></a>
#### 패널 컴포넌트

패널 컴포넌트는 주어진 텍스트 블록을 메시지의 나머지 부분과 약간 다른 배경색을 가진 패널에 렌더링합니다. 이를 통해 특정 텍스트 블록에 주목을 끌 수 있습니다:

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

마크다운 메일 구성 요소를 모두 내 애플리케이션으로 내보내어 사용자 정의할 수 있습니다. 구성 요소를 내보내려면 `vendor:publish` Artisan 명령어를 사용하여 `laravel-mail` 자산 태그를 게시하세요:

```shell
php artisan vendor:publish --tag=laravel-mail
```



This command will publish the Markdown mail components to the `resources/views/vendor/mail` directory. The `mail` directory will contain an `html` and a `text` directory, each containing their respective representations of every available component. You are free to customize these components however you like.

<a name="customizing-the-css"></a>
#### Customizing the CSS

After exporting the components, the `resources/views/vendor/mail/html/themes` directory will contain a `default.css` file. You may customize the CSS in this file and your styles will automatically be converted to inline CSS styles within the HTML representations of your Markdown mail messages.

If you would like to build an entirely new theme for Laravel's Markdown components, you may place a CSS file within the `html/themes` directory. After naming and saving your CSS file, update the `theme` option of your application's `config/mail.php` configuration file to match the name of your new theme.

To customize the theme for an individual mailable, you may set the `$theme` property of the mailable class to the name of the theme that should be used when sending that mailable.

<a name="sending-mail"></a>
## Sending Mail

To send a message, use the `to` method on the `Mail` [facade](/docs/{{version}}/facades). The `to` method accepts an email address, a user instance, or a collection of users. If you pass an object or collection of objects, the mailer will automatically use their `email` and `name` properties when determining the email's recipients, so make sure these attributes are available on your objects. Once you have specified your recipients, you may pass an instance of your mailable class to the `send` method:

```php
<?php

namespace App\Http\Controllers;

use App\Mail\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Ship the order...

        Mail::to($request->user())->send(new OrderShipped($order));

        return redirect('/orders');
    }
}
```



메시지를 보낼 때 단지 '받는 사람'만 지정하는 것으로 제한되지 않습니다. 각자의 메서드를 연결하여 '받는 사람', '참조', '숨은 참조' 수신자를 자유롭게 설정할 수 있습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->send(new OrderShipped($order));
```



<a name="looping-over-recipients"></a>
#### 수신자 반복 처리

때때로, 수신자 배열/이메일 주소 배열을 반복하여 메일 가능한 객체를 여러 수신자에게 보내야 할 때가 있습니다. 그러나 `to` 메서드는 이메일 주소를 메일 가능한 객체의 수신자 목록에 추가하기 때문에, 루프를 반복할 때마다 이전의 모든 수신자에게 또 다른 이메일이 전송됩니다. 그러므로 각 수신자마다 항상 메일 가능한 객체 인스턴스를 새로 생성해야 합니다:

```php
foreach (['taylor@example.com', 'dries@example.com'] as $recipient) {
    Mail::to($recipient)->send(new OrderShipped($order));
}
```



<a name="sending-mail-via-a-specific-mailer"></a>
#### 특정 메일러를 사용하여 메일 보내기

기본적으로 Laravel은 애플리케이션의 `mail` 설정 파일에서 `default` 메일러로 구성된 메일러를 사용하여 이메일을 보냅니다. 그러나 `mailer` 메서드를 사용하여 특정 메일러 구성을 사용하여 메시지를 보낼 수 있습니다:

```php
Mail::mailer('postmark')
    ->to($request->user())
    ->send(new OrderShipped($order));
```



<a name="queueing-mail"></a>
### 메일 큐잉

<a name="queueing-a-mail-message"></a>
#### 메일 메시지 큐잉

이메일 메시지를 보내는 것은 애플리케이션의 응답 시간에 부정적인 영향을 줄 수 있으므로, 많은 개발자가 이메일 메시지를 백그라운드 전송을 위해 큐에 넣는 것을 선택합니다. Laravel은 내장된 [통합 큐 API](/docs/{{version}}/queues)를 사용하여 이를 쉽게 수행할 수 있습니다. 메일 메시지를 큐에 넣으려면, 메시지 수신자를 지정한 후 `Mail` 퍼사드에서 `queue` 메서드를 사용하세요:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue(new OrderShipped($order));
```



이 방법은 작업을 큐에 자동으로 넣어 메시지가 백그라운드에서 전송되도록 처리합니다. 이 기능을 사용하기 전에 [큐를 구성](/docs/{{version}}/queues)해야 합니다.

<a name="delayed-message-queueing"></a>
#### 지연 메시지 큐잉

큐에 있는 이메일 메시지의 전송을 지연하고자 할 경우, `later` 메서드를 사용할 수 있습니다. 이 메서드는 첫 번째 인자로 메시지를 언제 전송할지를 나타내는 `DateTime` 인스턴스를 받습니다:

```php
Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->later(now()->plus(minutes: 10), new OrderShipped($order));
```



<a name="pushing-to-specific-queues"></a>
#### 특정 큐로 푸시하기

`make:mail` 명령을 사용하여 생성된 모든 메일 클래스는 `Illuminate\Bus\Queueable` 트레이트를 사용하므로, 모든 메일 클래스 인스턴스에서 `onQueue` 및 `onConnection` 메서드를 호출할 수 있으며, 이를 통해 메시지의 연결 및 큐 이름을 지정할 수 있습니다:

```php
$message = (new OrderShipped($order))
    ->onConnection('sqs')
    ->onQueue('emails');

Mail::to($request->user())
    ->cc($moreUsers)
    ->bcc($evenMoreUsers)
    ->queue($message);
```



또는, mailable 클래스에서 `Connection` 및 `Queue` 속성을 사용하여 연결과 큐를 지정할 수 있습니다:

```php
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('emails')]
class OrderShipped extends Mailable
{
    // ...
}
```



<a name="queueing-by-default"></a>
#### 기본적으로 큐잉하기

항상 큐에 넣고 싶은 발송 가능한 클래스가 있는 경우, 클래스에서 `ShouldQueue` 계약을 구현할 수 있습니다. 이제, 발송 시 `send` 메서드를 호출하더라도, 해당 계약을 구현했기 때문에 발송 가능한 항목은 여전히 큐에 들어가게 됩니다:

```php
use Illuminate\Contracts\Queue\ShouldQueue;

class OrderShipped extends Mailable implements ShouldQueue
{
    // ...
}
```



<a name="queued-mailables-and-database-transactions"></a>
#### 대기 중인 메일과 데이터베이스 트랜잭션

대기 중인 메일이 데이터베이스 트랜잭션 내에서 발송될 때, 데이터베이스 트랜잭션이 커밋되기 전에 큐에서 처리될 수 있습니다. 이런 경우, 트랜잭션 동안 모델이나 데이터베이스 레코드에 수행한 업데이트가 데이터베이스에 반영되지 않을 수 있습니다. 또한, 트랜잭션 내에서 생성된 모델이나 데이터베이스 레코드는 데이터베이스에 존재하지 않을 수 있습니다. 만약 메일이 이러한 모델에 의존한다면, 대기 중인 메일을 발송하는 작업이 처리될 때 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 설정 옵션이 `false`로 설정된 경우에도, 메일 메시지를 보낼 때 `afterCommit` 메서드를 호출하여 특정 대기 중인 메일이 모든 열린 데이터베이스 트랜잭션이 커밋된 후에 발송되도록 지정할 수 있습니다:

```php
Mail::to($request->user())->send(
    (new OrderShipped($order))->afterCommit()
);
```



또는, 메일 가능 객체의 생성자에서 `afterCommit` 메서드를 호출할 수 있습니다:

```php
<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

class OrderShipped extends Mailable implements ShouldQueue
{
    use Queueable, SerializesModels;

    /**
     * Create a new message instance.
     */
    public function __construct()
    {
        $this->afterCommit();
    }
}
```



> [!NOTE]
> 이러한 문제를 해결하는 방법에 대해 자세히 알아보려면 [대기 중인 작업과 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions)에 관한 문서를 참조하세요.

<a name="queued-email-failures"></a>
#### 대기 중인 이메일 실패

대기 중인 이메일이 실패하면, 정의되어 있는 경우 해당 대기 중인 마일러블 클래스에서 `failed` 메서드가 호출됩니다. 대기 중인 이메일 실패를 일으킨 `Throwable` 인스턴스가 `failed` 메서드에 전달됩니다:

```php
<?php

namespace App\Mail;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;
use Throwable;

class OrderDelayed extends Mailable implements ShouldQueue
{
    use SerializesModels;

    /**
     * Handle a queued email's failure.
     */
    public function failed(Throwable $exception): void
    {
        // ...
    }
}
```



<a name="rendering-mailables"></a>
## 메일 가능 객체 렌더링

때때로 메일을 보내지 않고 메일 가능 객체의 HTML 내용을 캡처하고 싶을 수 있습니다. 이를 수행하려면 메일 가능 객체의 `render` 메서드를 호출할 수 있습니다. 이 메서드는 메일 가능 객체의 평가된 HTML 내용을 문자열로 반환합니다:

```php
use App\Mail\InvoicePaid;
use App\Models\Invoice;

$invoice = Invoice::find(1);

return (new InvoicePaid($invoice))->render();
```



<a name="previewing-mailables-in-the-browser"></a>
### 브라우저에서 메일 가능 항목 미리보기

메일 가능 항목의 템플릿을 디자인할 때, 일반적인 Blade 템플릿처럼 브라우저에서 렌더링된 메일 가능 항목을 빠르게 미리보는 것이 편리합니다. 이러한 이유로, Laravel에서는 라우트 클로저나 컨트롤러에서 메일 가능 항목을 직접 반환할 수 있습니다. 메일 가능 항목이 반환되면, 브라우저에 렌더링되어 표시되므로 실제 이메일 주소로 보내지 않고도 디자인을 빠르게 미리볼 수 있습니다:

```php
Route::get('/mailable', function () {
    $invoice = App\Models\Invoice::find(1);

    return new App\Mail\InvoicePaid($invoice);
});
```



<a name="localizing-mailables"></a>
## 메일러블 로컬라이즈하기

Laravel은 요청의 현재 로케일이 아닌 다른 로케일에서 메일러블을 보낼 수 있으며, 메일이 큐에 들어가더라도 이 로케일을 기억합니다.

이를 달성하기 위해, `Mail` 파사드는 원하는 언어를 설정하는 `locale` 메서드를 제공합니다. 메일러블의 템플릿이 평가될 때 애플리케이션은 이 로케일로 변경되며, 평가가 완료되면 이전 로케일로 다시 돌아갑니다:

```php
Mail::to($request->user())->locale('es')->send(
    new OrderShipped($order)
);
```



<a name="user-preferred-locales"></a>
#### 사용자 선호 지역 설정

때때로, 애플리케이션은 각 사용자의 선호 지역(locale)을 저장합니다. 하나 이상의 모델에서 `HasLocalePreference` 계약을 구현함으로써, Laravel에게 메일을 보낼 때 이 저장된 지역을 사용하도록 지시할 수 있습니다:

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



인터페이스를 구현하면, Laravel은 모델에 메일과 알림을 보낼 때 자동으로 선호하는 로케일을 사용합니다. 따라서 이 인터페이스를 사용할 때는 `locale` 메서드를 호출할 필요가 없습니다:

```php
Mail::to($request->user())->send(new OrderShipped($order));
```



<a name="testing-mailables"></a>
## 테스트

<a name="testing-mailable-content"></a>
### 전송 가능한 콘텐츠 테스트

Laravel은 메일러블(mailable)의 구조를 검사하기 위한 다양한 방법을 제공합니다. 또한, Laravel은 메일러블에 예상한 내용이 포함되어 있는지 테스트하기 위한 몇 가지 편리한 방법을 제공합니다:```php tab=Pest
use App\Mail\InvoicePaid;
use App\Models\User;

test('mailable content', function () {
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
});
```

```php tab=PHPUnit
use App\Mail\InvoicePaid;
use App\Models\User;

public function test_mailable_content(): void
{
    $user = User::factory()->create();

    $mailable = new InvoicePaid($user);

    $mailable->assertFrom('jeffrey@example.com');
    $mailable->assertTo('taylor@example.com');
    $mailable->assertHasCc('abigail@example.com');
    $mailable->assertHasBcc('victoria@example.com');
    $mailable->assertHasReplyTo('tyler@example.com');
    $mailable->assertHasSubject('Invoice Paid');
    $mailable->assertHasTag('example-tag');
    $mailable->assertHasMetadata('key', 'value');

    $mailable->assertSeeInHtml($user->email);
    $mailable->assertDontSeeInHtml('Invoice Not Paid');
    $mailable->assertSeeInOrderInHtml(['Invoice Paid', 'Thanks']);

    $mailable->assertSeeInText($user->email);
    $mailable->assertDontSeeInText('Invoice Not Paid');
    $mailable->assertSeeInOrderInText(['Invoice Paid', 'Thanks']);

    $mailable->assertHasAttachment('/path/to/file');
    $mailable->assertHasAttachment(Attachment::fromPath('/path/to/file'));
    $mailable->assertHasAttachedData($pdfData, 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorage('/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
    $mailable->assertHasAttachmentFromStorageDisk('s3', '/path/to/file', 'name.pdf', ['mime' => 'application/pdf']);
}
```



예상할 수 있듯이, "HTML" 어설션은 전송 가능한 메일의 HTML 버전에 특정 문자열이 포함되어 있는지 확인하고, "text" 어설션은 전송 가능한 메일의 일반 텍스트 버전에 특정 문자열이 포함되어 있는지 확인합니다.

<a name="testing-mailable-sending"></a>
### 전송 가능한 메일 테스트

특정 사용자에게 특정 전송 가능한 메일이 "전송되었다"고 확인하는 테스트와는 별개로, 전송 가능한 메일의 내용을 별도로 테스트할 것을 권장합니다. 일반적으로, 전송 가능한 메일의 내용은 테스트 중인 코드와 관련이 없으며, Laravel이 특정 전송 가능한 메일을 전송하도록 지시했는지만 어설션하는 것으로 충분합니다.

메일이 전송되는 것을 방지하기 위해 `Mail` 페사드의 `fake` 메서드를 사용할 수 있습니다. `Mail` 페사드의 `fake` 메서드를 호출한 후에는, 전송 가능한 메일이 사용자에게 전송되도록 지시되었는지 어설션하고, 메일이 받은 데이터를 검사할 수도 있습니다:```php tab=Pest
<?php

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;

test('orders can be shipped', function () {
    Mail::fake();

    // Perform order shipping...

    // Assert that no mailables were sent...
    Mail::assertNothingSent();

    // Assert that a mailable was sent...
    Mail::assertSent(OrderShipped::class);

    // Assert a mailable was sent twice...
    Mail::assertSent(OrderShipped::class, 2);

    // Assert a mailable was sent to an email address...
    Mail::assertSent(OrderShipped::class, 'example@laravel.com');

    // Assert a mailable was sent to multiple email addresses...
    Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

    // Assert a mailable was not sent...
    Mail::assertNotSent(AnotherMailable::class);

    // Assert a mailable was sent twice...
    Mail::assertSentTimes(OrderShipped::class, 2);

    // Assert that a mailable was sent exactly once...
    Mail::assertSentOnce(OrderShipped::class);

    // Assert 3 total mailables were sent...
    Mail::assertSentCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Mail\OrderShipped;
use Illuminate\Support\Facades\Mail;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Mail::fake();

        // Perform order shipping...

        // Assert that no mailables were sent...
        Mail::assertNothingSent();

        // Assert that a mailable was sent...
        Mail::assertSent(OrderShipped::class);

        // Assert a mailable was sent twice...
        Mail::assertSent(OrderShipped::class, 2);

        // Assert a mailable was sent to an email address...
        Mail::assertSent(OrderShipped::class, 'example@laravel.com');

        // Assert a mailable was sent to multiple email addresses...
        Mail::assertSent(OrderShipped::class, ['example@laravel.com', '...']);

        // Assert a mailable was not sent...
        Mail::assertNotSent(AnotherMailable::class);

        // Assert a mailable was sent twice...
        Mail::assertSentTimes(OrderShipped::class, 2);

        // Assert that a mailable was sent exactly once...
        Mail::assertSentOnce(OrderShipped::class);

        // Assert 3 total mailables were sent...
        Mail::assertSentCount(3);
    }
}
```



메일 발송을 백그라운드에서 대기열에 넣고 있다면, `assertSent` 대신 `assertQueued` 메서드를 사용해야 합니다:

```php
Mail::assertQueued(OrderShipped::class);
Mail::assertQueuedOnce(OrderShipped::class);
Mail::assertNotQueued(OrderShipped::class);
Mail::assertNothingQueued();
Mail::assertQueuedCount(3);
```



`assertOutgoingCount` 메서드를 사용하여 전송되었거나 대기 중인 메일 수를 확인할 수도 있습니다:

```php
Mail::assertOutgoingCount(3);
```



`assertSent`, `assertNotSent`, `assertQueued` 또는 `assertNotQueued` 메서드에 클로저를 전달하여 주어진 "진리 테스트"를 통과하는 메일이 전송되었음을 확인할 수 있습니다. 주어진 진리 테스트를 통과하는 메일이 최소한 하나 이상 전송되었다면, 이 검증은 성공하게 됩니다:

```php
Mail::assertSent(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```



`Mail` 퍼사드의 assertion 메서드를 호출할 때, 제공된 클로저에서 받아들이는 mailable 인스턴스는 mailable을 검사할 수 있는 유용한 메서드를 제공합니다:

```php
Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($user) {
    return $mail->hasTo($user->email) &&
           $mail->hasCc('...') &&
           $mail->hasBcc('...') &&
           $mail->hasReplyTo('...') &&
           $mail->hasFrom('...') &&
           $mail->hasSubject('...') &&
           $mail->hasMetadata('order_id', $mail->order->id);
           $mail->usesMailer('ses');
});
```



메일 가능한 인스턴스에는 메일 가능 항목의 첨부 파일을 확인하는 데 유용한 몇 가지 메서드도 포함되어 있습니다:

```php
use Illuminate\Mail\Mailables\Attachment;

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromPath('/path/to/file')
            ->as('name.pdf')
            ->withMime('application/pdf')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) {
    return $mail->hasAttachment(
        Attachment::fromStorageDisk('s3', '/path/to/file')
    );
});

Mail::assertSent(OrderShipped::class, function (OrderShipped $mail) use ($pdfData) {
    return $mail->hasAttachment(
        Attachment::fromData(fn () => $pdfData, 'name.pdf')
    );
});
```



메일이 전송되지 않았음을 확인하는 방법에는 `assertNotSent`와 `assertNotQueued`의 두 가지 방법이 있다는 것을 눈치채셨을 수 있습니다. 때때로 전송되지 않았거나 큐에 쌓이지 않았음을 확인하고 싶을 수 있습니다. 이를 수행하기 위해 `assertNothingOutgoing`와 `assertNotOutgoing` 방법을 사용할 수 있습니다:

```php
Mail::assertNothingOutgoing();

Mail::assertNotOutgoing(function (OrderShipped $mail) use ($order) {
    return $mail->order->id === $order->id;
});
```



<a name="mail-and-local-development"></a>
## Mail and Local Development

When developing an application that sends email, you probably don't want to actually send emails to live email addresses. Laravel provides several ways to "disable" the actual sending of emails during local development.

<a name="log-driver"></a>
#### Log Driver

Instead of sending your emails, the `log` mail driver will write all email messages to your log files for inspection. Typically, this driver would only be used during local development. For more information on configuring your application per environment, check out the [configuration documentation](/docs/{{version}}/configuration#environment-configuration).

<a name="mailtrap"></a>
#### HELO / Mailtrap / Mailpit

Alternatively, you may use a service like [HELO](https://usehelo.com) or [Mailtrap](https://mailtrap.io) and the `smtp` driver to send your email messages to a "dummy" mailbox where you may view them in a true email client. This approach has the benefit of allowing you to actually inspect the final emails in Mailtrap's message viewer.

If you are using [Laravel Sail](/docs/{{version}}/sail), you may preview your messages using [Mailpit](https://github.com/axllent/mailpit). When Sail is running, you may access the Mailpit interface at: `http://localhost:8025`.

<a name="using-a-global-to-address"></a>
#### Using a Global `to` Address

Finally, you may specify a global "to" address by invoking the `alwaysTo` method offered by the `Mail` facade. Typically, this method should be called from the `boot` method of one of your application's service providers:

```php
use Illuminate\Support\Facades\Mail;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    if ($this->app->environment('local')) {
        Mail::alwaysTo('taylor@example.com');
    }
}
```



`alwaysTo` 방법을 사용할 때, 메일 메시지의 추가적인 "cc" 또는 "bcc" 주소는 삭제됩니다.

<a name="events"></a>
## 이벤트

Laravel은 메일 메시지를 보내는 동안 두 개의 이벤트를 발생시킵니다. `MessageSending` 이벤트는 메시지가 전송되기 전에 발생하며, `MessageSent` 이벤트는 메시지가 전송된 후에 발생합니다. 이러한 이벤트는 메일이 대기열에 저장될 때가 아닌, *전송될 때* 발생한다는 것을 기억하세요. 애플리케이션 내에서 이러한 이벤트에 대한 [이벤트 리스너](/docs/{{version}}/events)를 생성할 수 있습니다.

```php
use Illuminate\Mail\Events\MessageSending;
// use Illuminate\Mail\Events\MessageSent;

class LogMessage
{
    /**
     * Handle the event.
     */
    public function handle(MessageSending $event): void
    {
        // ...
    }
}
```



<a name="custom-transports"></a>
## 맞춤 전송

Laravel에는 다양한 메일 전송 방법이 포함되어 있지만, Laravel이 기본적으로 지원하지 않는 다른 서비스를 통해 이메일을 전송하기 위해 직접 전송 방법을 작성하고 싶을 수 있습니다. 시작하려면 `Symfony\Component\Mailer\Transport\AbstractTransport` 클래스를 확장하는 클래스를 정의하세요. 그런 다음, 전송 방법에서 `doSend` 및 `__toString` 메서드를 구현하세요:

```php
<?php

namespace App\Mail;

use MailchimpTransactional\ApiClient;
use Symfony\Component\Mailer\SentMessage;
use Symfony\Component\Mailer\Transport\AbstractTransport;
use Symfony\Component\Mime\Address;
use Symfony\Component\Mime\MessageConverter;

class MailchimpTransport extends AbstractTransport
{
    /**
     * Create a new Mailchimp transport instance.
     */
    public function __construct(
        protected ApiClient $client,
    ) {
        parent::__construct();
    }

    /**
     * {@inheritDoc}
     */
    protected function doSend(SentMessage $message): void
    {
        $email = MessageConverter::toEmail($message->getOriginalMessage());

        $this->client->messages->send(['message' => [
            'from_email' => $email->getFrom(),
            'to' => collect($email->getTo())->map(function (Address $email) {
                return ['email' => $email->getAddress(), 'type' => 'to'];
            })->all(),
            'subject' => $email->getSubject(),
            'text' => $email->getTextBody(),
        ]]);
    }

    /**
     * Get the string representation of the transport.
     */
    public function __toString(): string
    {
        return 'mailchimp';
    }
}
```



사용자 정의 전송 방식을 정의한 후에는 `Mail` 퍼사드에서 제공하는 `extend` 메서드를 통해 이를 등록할 수 있습니다. 일반적으로 이는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드 내에서 수행해야 합니다. `extend` 메서드에 제공된 클로저에는 `$config` 인수가 전달됩니다. 이 인수에는 애플리케이션의 `config/mail.php` 구성 파일에 정의된 메일러 구성 배열이 포함됩니다:

```php
use App\Mail\MailchimpTransport;
use Illuminate\Support\Facades\Mail;
use MailchimpTransactional\ApiClient;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('mailchimp', function (array $config = []) {
        $client = new ApiClient;

        $client->setApiKey($config['key']);

        return new MailchimpTransport($client);
    });
}
```



맞춤 전송 수단이 정의되고 등록되면, 응용 프로그램의 `config/mail.php` 구성 파일 내에서 새 전송 수단을 사용하는 메일러 정의를 생성할 수 있습니다:

```php
'mailchimp' => [
    'transport' => 'mailchimp',
    'key' => env('MAILCHIMP_API_KEY'),
    // ...
],
```



<a name="additional-symfony-transports"></a>
### 추가 Symfony 전송

Laravel은 Mailgun 및 Postmark와 같은 기존 Symfony에서 유지 관리하는 일부 메일 전송에 대한 지원을 포함합니다. 그러나 추가 Symfony에서 유지 관리하는 전송에 대한 지원으로 Laravel을 확장하고 싶을 수 있습니다. 필요한 Symfony 메일러를 Composer를 통해 설치하고 Laravel에 전송을 등록하여 그렇게 할 수 있습니다. 예를 들어, "Brevo"(이전 "Sendinblue") Symfony 메일러를 설치하고 등록할 수 있습니다:

```shell
composer require symfony/brevo-mailer symfony/http-client
```



Brevo 메일러 패키지가 설치되면, 애플리케이션의 `services` 구성 파일에 Brevo API 자격 증명 항목을 추가할 수 있습니다:

```php
'brevo' => [
    'key' => env('BREVO_API_KEY'),
],
```



다음으로, `Mail` 퍼사드의 `extend` 메서드를 사용하여 라라벨에 트랜스포트를 등록할 수 있습니다. 일반적으로 이는 서비스 프로바이더의 `boot` 메서드 내에서 수행되어야 합니다:

```php
use Illuminate\Support\Facades\Mail;
use Symfony\Component\Mailer\Bridge\Brevo\Transport\BrevoTransportFactory;
use Symfony\Component\Mailer\Transport\Dsn;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Mail::extend('brevo', function () {
        return (new BrevoTransportFactory)->create(
            new Dsn(
                'brevo+api',
                'default',
                config('services.brevo.key')
            )
        );
    });
}
```



운송 수단이 등록되면, 애플리케이션의 `config/mail.php` 구성 파일 내에서 새 운송 수단을 활용하는 메일러 정의를 생성할 수 있습니다:

```php
'brevo' => [
    'transport' => 'brevo',
    // ...
],
```
{% endraw %}
