---
layout: docs
title: "Events"
---

{% raw %}
# Events

- [Introduction](#introduction)
- [Generating Events and Listeners](#generating-events-and-listeners)
- [Registering Events and Listeners](#registering-events-and-listeners)
    - [Event Discovery](#event-discovery)
    - [Manually Registering Events](#manually-registering-events)
    - [Closure Listeners](#closure-listeners)
- [Defining Events](#defining-events)
- [Defining Listeners](#defining-listeners)
- [Queued Event Listeners](#queued-event-listeners)
    - [Manually Interacting With the Queue](#manually-interacting-with-the-queue)
    - [Queued Event Listeners and Database Transactions](#queued-event-listeners-and-database-transactions)
    - [Queued Listener Middleware](#queued-listener-middleware)
    - [Encrypted Queued Listeners](#encrypted-queued-listeners)
    - [Unique Event Listeners](#unique-event-listeners)
        - [Keeping Listeners Unique Until Processing Begins](#keeping-listeners-unique-until-processing-begins)
        - [Unique Listener Locks](#unique-listener-locks)
    - [Debounced Event Listeners](#debounced-event-listeners)
    - [Handling Failed Jobs](#handling-failed-jobs)
- [Dispatching Events](#dispatching-events)
    - [Dispatching Events After Database Transactions](#dispatching-events-after-database-transactions)
    - [Deferring Events](#deferring-events)
- [Event Subscribers](#event-subscribers)
    - [Writing Event Subscribers](#writing-event-subscribers)
    - [Registering Event Subscribers](#registering-event-subscribers)
- [Testing](#testing)
    - [Faking a Subset of Events](#faking-a-subset-of-events)
    - [Scoped Event Fakes](#scoped-event-fakes)

<a name="introduction"></a>
## Introduction

Laravel's events provide a simple observer pattern implementation, allowing you to subscribe and listen for various events that occur within your application. Event classes are typically stored in the `app/Events` directory, while their listeners are stored in `app/Listeners`. Don't worry if you don't see these directories in your application as they will be created for you as you generate events and listeners using Artisan console commands.



이벤트는 애플리케이션의 다양한 측면을 분리하는 훌륭한 방법으로 작용합니다. 하나의 이벤트가 서로 의존하지 않는 여러 리스너를 가질 수 있기 때문입니다. 예를 들어, 주문이 발송될 때마다 사용자에게 슬랙 알림을 보내고 싶을 수 있습니다. 주문 처리 코드를 슬랙 알림 코드와 결합하는 대신, 리스너가 수신하고 슬랙 알림을 전송하는 데 사용할 수 있는 `App\Events\OrderShipped` 이벤트를 발생시킬 수 있습니다.

<a name="generating-events-and-listeners"></a>
## 이벤트 및 리스너 생성

이벤트와 리스너를 빠르게 생성하려면, `make:event`와 `make:listener` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan make:event PodcastProcessed

php artisan make:listener SendPodcastNotification --event=PodcastProcessed
```



편의를 위해, 추가 인수 없이도 `make:event` 및 `make:listener` Artisan 명령어를 호출할 수 있습니다. 이렇게 하면 Laravel이 자동으로 클래스 이름을 묻고, 리스너를 생성할 때는 해당 리스너가 청취할 이벤트를 묻습니다:

```shell
php artisan make:event

php artisan make:listener
```



<a name="registering-events-and-listeners"></a>
## 이벤트 및 리스너 등록

<a name="event-discovery"></a>
### 이벤트 발견

기본적으로 Laravel은 애플리케이션의 `Listeners` 디렉터리를 스캔하여 이벤트 리스너를 자동으로 찾아 등록합니다. Laravel이 `handle` 또는 `__invoke`로 시작하는 리스너 클래스 메서드를 찾으면, Laravel은 해당 메서드의 시그니처에 타입 힌트로 지정된 이벤트에 대한 이벤트 리스너로 그 메서드를 등록합니다:

```php
use App\Events\PodcastProcessed;

class SendPodcastNotification
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }
}
```



PHP의 유니언 타입을 사용하여 여러 이벤트를 들을 수 있습니다:

```php
/**
 * Handle the event.
 */
public function handle(PodcastProcessed|PodcastPublished $event): void
{
    // ...
}
```



리스너를 다른 디렉토리나 여러 디렉토리에 저장할 계획이라면, 애플리케이션의 `bootstrap/app.php` 파일에서 `withEvents` 메서드를 사용하여 Laravel에게 해당 디렉토리를 스캔하도록 지시할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/Orders/Listeners',
])
```



와일드카드로 `*` 문자를 사용하여 여러 유사한 디렉터리에서 리스너를 검색할 수 있습니다:

```php
->withEvents(discover: [
    __DIR__.'/../app/Domain/*/Listeners',
])
```



`event:list` 명령은 애플리케이션에 등록된 모든 리스너를 나열하는 데 사용할 수 있습니다:

```shell
php artisan event:list
```



<a name="event-discovery-in-production"></a>
#### 프로덕션에서 이벤트 발견

애플리케이션의 속도를 높이기 위해, `optimize` 또는 `event:cache` Artisan 명령어를 사용하여 애플리케이션의 모든 리스너 매니페스트를 캐시해야 합니다. 일반적으로 이 명령어는 애플리케이션의 [배포 과정](/docs/{{version}}/deployment#optimization)의 일부로 실행되어야 합니다. 이 매니페스트는 이벤트 등록 과정을 빠르게 하기 위해 프레임워크에서 사용됩니다. `event:clear` 명령어는 이벤트 캐시를 삭제할 때 사용할 수 있습니다.

<a name="dynamic-event-discovery"></a>
#### 동적 이벤트 발견

특정 리스너가 발견될지를 동적으로 제어하려면, 리스너 클래스에서 `ShouldBeDiscovered` 인터페이스를 구현하고 `shouldBeDiscovered` 메서드를 정의하여 boolean 값을 반환할 수 있습니다. 메서드가 `false`를 반환하면, 이벤트 발견 시 해당 리스너는 등록되지 않습니다:

```php
use Illuminate\Contracts\Events\ShouldBeDiscovered;

class SendPodcastNotification implements ShouldBeDiscovered
{
    /**
     * Handle the event.
     */
    public function handle(PodcastProcessed $event): void
    {
        // ...
    }

    /**
     * Determine if the listener should be discovered.
     */
    public static function shouldBeDiscovered(): bool
    {
        return app()->environment('production');
    }
}
```



<a name="manually-registering-events"></a>
### 이벤트 수동 등록

`Event` 퍼사드를 사용하여 애플리케이션의 `AppServiceProvider` 안에 있는 `boot` 메서드 내에서 이벤트와 해당 리스너를 수동으로 등록할 수 있습니다:

```php
use App\Domain\Orders\Events\PodcastProcessed;
use App\Domain\Orders\Listeners\SendPodcastNotification;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(
        PodcastProcessed::class,
        SendPodcastNotification::class,
    );
}
```



`event:list` 명령은 애플리케이션에 등록된 모든 리스너를 나열하는 데 사용할 수 있습니다:

```shell
php artisan event:list
```



<a name="closure-listeners"></a>
### 클로저 리스너

일반적으로 리스너는 클래스 형태로 정의되지만, 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 클로저 기반 이벤트 리스너를 수동으로 등록할 수도 있습니다:

```php
use App\Events\PodcastProcessed;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (PodcastProcessed $event) {
        // ...
    });
}
```



<a name="queueable-anonymous-event-listeners"></a>
#### 큐 가능한 익명 이벤트 리스너

클로저 기반 이벤트 리스너를 등록할 때, 리스너 클로저를 `Illuminate\Events\queueable` 함수로 감싸서 Laravel이 [큐](/docs/{{version}}/queues)를 사용하여 리스너를 실행하도록 지시할 수 있습니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(queueable(function (PodcastProcessed $event) {
        // ...
    }));
}
```



대기열에 있는 작업과 마찬가지로, 대기열 리스너의 실행을 맞춤 설정하기 위해 `onConnection`, `onQueue`, `delay` 메서드를 사용할 수 있습니다:

```php
Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->onConnection('redis')->onQueue('podcasts')->delay(now()->plus(seconds: 10)));
```



익명 대기열 리스너 실패를 처리하고 싶다면, `queueable` 리스너를 정의하는 동안 `catch` 메서드에 클로저를 제공할 수 있습니다. 이 클로저는 이벤트 인스턴스와 리스너 실패를 초래한 `Throwable` 인스턴스를 받게 됩니다:

```php
use App\Events\PodcastProcessed;
use function Illuminate\Events\queueable;
use Illuminate\Support\Facades\Event;
use Throwable;

Event::listen(queueable(function (PodcastProcessed $event) {
    // ...
})->catch(function (PodcastProcessed $event, Throwable $e) {
    // The queued listener failed...
}));
```



<a name="wildcard-event-listeners"></a>
#### 와일드카드 이벤트 리스너

`*` 문자를 와일드카드 매개변수로 사용하여 리스너를 등록할 수도 있으며, 이를 통해 동일한 리스너에서 여러 이벤트를 포착할 수 있습니다. 와일드카드 리스너는 첫 번째 인수로 이벤트 이름을, 두 번째 인수로 전체 이벤트 데이터 배열을 받습니다:

```php
Event::listen('event.*', function (string $eventName, array $data) {
    // ...
});
```



<a name="defining-events"></a>
## 이벤트 정의

이벤트 클래스는 본질적으로 이벤트와 관련된 정보를 담고 있는 데이터 컨테이너입니다. 예를 들어, `App\Events\OrderShipped` 이벤트가 [Eloquent ORM](/docs/{{version}}/eloquent) 객체를 받는다고 가정해 봅시다:

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```



보시다시피, 이 이벤트 클래스에는 로직이 포함되어 있지 않습니다. 구매한 `App\Models\Order` 인스턴스를 담는 컨테이너입니다. 이벤트에서 사용되는 `SerializesModels` 트레이트는 PHP의 `serialize` 함수를 사용해 이벤트 객체를 직렬화할 경우, [큐에 저장된 리스너](#queued-event-listeners) 같은 경우에도 모든 Eloquent 모델을 원활하게 직렬화합니다.

<a name="defining-listeners"></a>
## 리스너 정의

다음으로, 예제 이벤트에 대한 리스너를 살펴보겠습니다. 이벤트 리스너는 `handle` 메서드에서 이벤트 인스턴스를 받습니다. `make:listener` Artisan 명령은 `--event` 옵션과 함께 호출될 때, 적절한 이벤트 클래스를 자동으로 불러오고 `handle` 메서드에서 이벤트를 타입 힌트합니다. `handle` 메서드 내에서, 이벤트에 대응하기 위해 필요한 모든 작업을 수행할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;

class SendShipmentNotification
{
    /**
     * Create the event listener.
     */
    public function __construct() {}

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Access the order using $event->order...
    }
}
```



> [!NOTE]
> Your event listeners may also type-hint any dependencies they need on their constructors. All event listeners are resolved via the Laravel [service container](/docs/{{version}}/container), so dependencies will be injected automatically.

<a name="stopping-the-propagation-of-an-event"></a>
#### Stopping The Propagation Of An Event

Sometimes, you may wish to stop the propagation of an event to other listeners. You may do so by returning `false` from your listener's `handle` method.

<a name="queued-event-listeners"></a>
## Queued Event Listeners

Queueing listeners can be beneficial if your listener is going to perform a slow task such as sending an email or making an HTTP request. Before using queued listeners, make sure to [configure your queue](/docs/{{version}}/queues) and start a queue worker on your server or local development environment.

To specify that a listener should be queued, add the `ShouldQueue` interface to the listener class. Listeners generated by the `make:listener` Artisan commands already have this interface imported into the current namespace so you can use it immediately:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```



그게 전부입니다! 이제 이 리스너가 처리하는 이벤트가 디스패치되면, 리스너는 Laravel의 [큐 시스템](/docs/{{version}}/queues)을 사용하여 이벤트 디스패처에 의해 자동으로 큐에 등록됩니다. 큐에서 리스너가 실행될 때 예외가 발생하지 않으면, 큐에 등록된 작업은 처리 완료 후 자동으로 삭제됩니다.

<a name="customizing-the-queue-connection-queue-name"></a>
#### 큐 연결, 이름 및 지연 시간 커스터마이즈하기

이벤트 리스너의 큐 연결, 큐 이름 또는 큐 지연 시간을 커스터마이즈하고 싶다면, 리스너 클래스에서 `Connection`, `Queue`, `Delay` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Connection;
use Illuminate\Queue\Attributes\Delay;
use Illuminate\Queue\Attributes\Queue;

#[Connection('sqs')]
#[Queue('listeners')]
#[Delay(60)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```

리스너의 큐 연결, 큐 이름 또는 지연 시간을 런타임에 정의하고 싶다면, 리스너에 `viaConnection`, `viaQueue` 또는 `withDelay` 메서드를 정의할 수 있습니다:

```php
/**
 * Get the name of the listener's queue connection.
 */
public function viaConnection(): string
{
    return 'sqs';
}

/**
 * Get the name of the listener's queue.
 */
public function viaQueue(): string
{
    return 'listeners';
}

/**
 * Get the number of seconds before the job should be processed.
 */
public function withDelay(OrderShipped $event): int
{
    return $event->highPriority ? 0 : 60;
}
```



모든 대기 중인 리스너가 각각의 리스너 클래스를 커스터마이즈하지 않고 동일한 큐를 사용하도록 하려면, 대신 [`ShouldQueue` 계약을 큐로 라우팅](/docs/{{version}}/queues#queue-routing)할 수 있습니다.

<a name="conditionally-queueing-listeners"></a>
#### 조건부 리스너 큐잉

때때로, 리스너를 큐에 넣을지 여부를 런타임에만 사용할 수 있는 데이터를 기반으로 결정해야 할 수 있습니다. 이를 달성하기 위해, 리스너에 `shouldQueue` 메서드를 추가하여 해당 리스너를 큐에 넣어야 하는지 여부를 결정할 수 있습니다. `shouldQueue` 메서드가 `false`를 반환하면, 해당 리스너는 큐에 추가되지 않습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use Illuminate\Contracts\Queue\ShouldQueue;

class RewardGiftCard implements ShouldQueue
{
    /**
     * Reward a gift card to the customer.
     */
    public function handle(OrderCreated $event): void
    {
        // ...
    }

    /**
     * Determine whether the listener should be queued.
     */
    public function shouldQueue(OrderCreated $event): bool
    {
        return $event->order->subtotal >= 5000;
    }
}
```



<a name="manually-interacting-with-the-queue"></a>
### 큐를 수동으로 조작하기

리스너의 기본 큐 작업의 `delete` 및 `release` 메서드에 수동으로 접근해야 하는 경우, `Illuminate\Queue\InteractsWithQueue` 트레이트를 사용하여 그렇게 할 수 있습니다. 이 트레이트는 생성된 리스너에 기본적으로 불러오기되며, 이러한 메서드에 대한 접근을 제공합니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        if ($condition) {
            $this->release(30);
        }
    }
}
```



<a name="queued-event-listeners-and-database-transactions"></a>
### 큐에 대기 중인 이벤트 리스너와 데이터베이스 트랜잭션

큐에 대기 중인 리스너가 데이터베이스 트랜잭션 내에서 디스패치될 때, 트랜잭션이 커밋되기 전에 큐에서 처리될 수 있습니다. 이런 경우, 데이터베이스 트랜잭션 중에 모델이나 데이터베이스 레코드에 수행한 모든 업데이트가 데이터베이스에 아직 반영되지 않았을 수 있습니다. 또한, 트랜잭션 내에서 생성된 모델이나 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수 있습니다. 만약 리스너가 이러한 모델에 의존한다면, 큐에 대기 중인 리스너를 디스패치하는 작업이 처리될 때 예상치 못한 오류가 발생할 수 있습니다.

큐 연결의 `after_commit` 구성 옵션이 `false`로 설정된 경우에도, 특정 대기 중인 리스너가 모든 열린 데이터베이스 트랜잭션이 커밋된 후에 디스패치되도록 리스너 클래스에서 `ShouldQueueAfterCommit` 인터페이스를 구현함으로써 이를 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueueAfterCommit;
use Illuminate\Queue\InteractsWithQueue;

class SendShipmentNotification implements ShouldQueueAfterCommit
{
    use InteractsWithQueue;
}
```



> [!NOTE]
> 이러한 문제를 우회하는 방법에 대해 자세히 알아보려면, [대기열 작업 및 데이터베이스 트랜잭션](/docs/{{version}}/queues#jobs-and-database-transactions)에 관한 문서를 검토하십시오.

<a name="queued-listener-middleware"></a>
### 대기열 리스너 미들웨어

대기열 리스너는 또한 [작업 미들웨어](/docs/{{version}}/queues#job-middleware)를 활용할 수 있습니다. 작업 미들웨어를 사용하면 대기열 리스너 실행 주위에 사용자 정의 로직을 감쌀 수 있어, 리스너 자체의 반복 코드를 줄일 수 있습니다. 작업 미들웨어를 생성한 후에는, 리스너의 `middleware` 메서드에서 반환하여 리스너에 첨부할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use App\Jobs\Middleware\RateLimited;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }

    /**
     * Get the middleware the listener should pass through.
     *
     * @return array<int, object>
     */
    public function middleware(OrderShipped $event): array
    {
        return [new RateLimited];
    }
}
```



<a name="encrypted-queued-listeners"></a>
#### 암호화된 대기열 리스너

Laravel은 [암호화](/docs/{{version}}/encryption)를 통해 대기열 리스너 데이터의 프라이버시와 무결성을 보장할 수 있습니다. 시작하려면 리스너 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스가 클래스에 추가되면, Laravel은 리스너를 대기열에 푸시하기 전에 자동으로 암호화합니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class SendShipmentNotification implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```



<a name="unique-event-listeners"></a>
### 고유 이벤트 리스너

> [!WARNING]
> 고유 리스너는 [잠금](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file` 및 `array` 캐시 드라이버는 원자적 잠금(atomic locks)을 지원합니다.

때때로 특정 리스너의 인스턴스가 언제나 큐에 하나만 존재하도록 보장하고 싶을 수 있습니다. 이는 리스너 클래스에서 `ShouldBeUnique` 인터페이스를 구현하여 수행할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }
}
```



위의 예제에서 `AcquireProductKey` 리스너는 고유합니다. 따라서 리스너의 다른 인스턴스가 이미 큐에 있고 처리를 완료하지 않았으면, 리스너는 큐에 추가되지 않습니다. 이렇게 하면 라이선스가 여러 번 연속으로 저장되더라도 각 라이선스에 대해 하나의 제품 키만 획득되도록 보장됩니다.

특정 경우에는 리스너를 고유하게 만드는 특정 "키"를 정의하거나, 일정 시간이 지나면 더 이상 리스너가 고유하지 않도록 타임아웃을 지정하고 싶을 수 있습니다. 이를 달성하기 위해, 리스너 클래스에서 `uniqueId` 및 `uniqueFor` 속성이나 메서드를 정의할 수 있습니다. 이 메서드들은 이벤트 인스턴스를 받아 이벤트 데이터를 사용하여 반환 값을 구성할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    /**
     * The number of seconds after which the listener's unique lock will be released.
     *
     * @var int
     */
    public $uniqueFor = 3600;

    public function __invoke(LicenseSaved $event): void
    {
        // ...
    }

    /**
     * Get the unique ID for the listener.
     */
    public function uniqueId(LicenseSaved $event): string
    {
        return 'listener:'.$event->license->id;
    }
}
```



In the example above, the `AcquireProductKey` listener is unique by license ID. So, any new dispatches of the listener for the same license will be ignored until the existing listener has completed processing. This prevents duplicate product keys from being acquired for the same license. In addition, if the existing listener is not processed within one hour, the unique lock will be released and another listener with the same unique key can be queued.

> [!WARNING]
> If your application dispatches events from multiple web servers or containers, you should ensure that all of your servers are communicating with the same central cache server so that Laravel can accurately determine if a listener is unique.

<a name="keeping-listeners-unique-until-processing-begins"></a>
#### Keeping Listeners Unique Until Processing Begins

By default, unique listeners are "unlocked" after a listener completes processing or fails all of its retry attempts. However, there may be situations where you would like your listener to unlock immediately before it is processed. To accomplish this, your listener should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;
use Illuminate\Contracts\Queue\ShouldQueue;

class AcquireProductKey implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```



<a name="unique-listener-locks"></a>
#### 고유 리스너 잠금

배경에서, `ShouldBeUnique` 리스너가 디스패치될 때, Laravel은 `uniqueId` 키로 [잠금](/docs/{{version}}/cache#atomic-locks)을 획득하려 시도합니다. 만약 잠금이 이미 잡혀 있다면, 리스너는 디스패치되지 않습니다. 이 잠금은 리스너가 처리를 완료하거나 모든 재시도 시도가 실패할 때 해제됩니다. 기본적으로 Laravel은 이 잠금을 얻기 위해 기본 캐시 드라이버를 사용합니다. 그러나 잠금을 획득하기 위해 다른 드라이버를 사용하고 싶다면, 사용해야 할 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\LicenseSaved;
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class AcquireProductKey implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique listener lock.
     */
    public function uniqueVia(LicenseSaved $event): Repository
    {
        return Cache::driver('redis');
    }
}
```



> [!NOTE]
> 리스너의 동시 처리를 제한해야 하는 경우, 대신 [WithoutOverlapping](/docs/{{version}}/queues#preventing-job-overlaps) 작업 미들웨어를 사용하세요.

<a name="debounced-event-listeners"></a>
### 디바운스된 이벤트 리스너

때때로, 짧은 시간 내에 반복적으로 발생하는 이벤트 중 최신 인스턴스만 처리하고 싶을 수 있습니다. 큐에 추가된 리스너에 `DebounceFor` 속성을 추가하여 이를 수행할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\ProductUpdated;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\DebounceFor;

#[DebounceFor(30)]
class UpdateProductSearchIndex implements ShouldQueue
{
    /**
     * Handle the event.
     */
    public function handle(ProductUpdated $event): void
    {
        // Update the product's search index...
    }

    /**
     * Get the debounce ID for the listener.
     */
    public function debounceId(ProductUpdated $event): string
    {
        return (string) $event->product->getKey();
    }
}
```



위의 예제에서 동일한 제품에 대해 `30`초 내에 `ProductUpdated` 이벤트를 반복적으로 전송하면 리스너가 디바운스되어 최신 이벤트만 처리됩니다. 서로 다른 디바운스 ID는 독립적으로 처리됩니다.

자주 전송되는 이벤트가 리스너를 지연시킬 수 있는 최대 시간을 제한하고 싶다면 `DebounceFor` 속성에 `maxWait` 인수를 제공할 수 있습니다:

```php
#[DebounceFor(30, maxWait: 120)]
class UpdateProductSearchIndex implements ShouldQueue
{
    // ...
}
```



리스너에 `debounceVia` 메서드를 정의하여 디바운스 추적에 사용되는 캐시 저장소를 사용자 정의할 수 있습니다. 이 메서드는 이벤트 인스턴스를 받고 캐시 저장소를 반환해야 합니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

public function debounceVia(ProductUpdated $event): Repository
{
    return Cache::driver('redis');
}
```



디바운스 리스너와 유니크 리스너는 상호 배타적입니다. `DebounceFor` 속성을 사용하는 리스너는 `ShouldBeUnique`를 구현해서는 안 됩니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버나 컨테이너에서 이벤트를 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 통신하고 있는지 확인해야 합니다.

<a name="handling-failed-jobs"></a>
### 실패한 작업 처리

때때로 큐에 있는 이벤트 리스너가 실패할 수 있습니다. 큐 리스너가 큐 워커에 정의된 최대 시도 횟수를 초과하면 `failed` 메서드가 리스너에서 호출됩니다. `failed` 메서드는 이벤트 인스턴스와 실패를 발생시킨 `Throwable`를 받습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;
use Throwable;

class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // ...
    }

    /**
     * Handle a job failure.
     */
    public function failed(OrderShipped $event, Throwable $exception): void
    {
        // ...
    }
}
```



<a name="specifying-queued-listener-maximum-attempts"></a>
#### 대기 중인 리스너 최대 시도 횟수 지정

대기 중인 리스너 중 하나가 오류를 겪고 있다면, 아마도 무한히 재시도하게 하고 싶지는 않을 것입니다. 따라서 Laravel은 리스너가 시도될 수 있는 횟수나 기간을 지정할 수 있는 다양한 방법을 제공합니다.

리스너 클래스에서 `Tries` 속성을 사용하여 리스너가 실패로 간주되기 전에 시도될 수 있는 최대 횟수를 지정할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(5)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    // ...
}
```



리스너가 실패하기 전에 시도할 수 있는 횟수를 정의하는 대신, 더 이상 시도를 하지 않아야 하는 시간을 정의할 수 있습니다. 이를 통해 특정 시간 내에 리스너를 원하는 만큼 시도할 수 있습니다. 리스너를 더 이상 시도하지 않아야 할 시간을 정의하려면, 리스너 클래스에 `retryUntil` 메서드를 추가하십시오. 이 메서드는 `DateTimeInterface` 인스턴스를 반환해야 합니다:

```php
use DateTimeInterface;

/**
 * Determine the time at which the listener should timeout.
 */
public function retryUntil(): DateTimeInterface
{
    return now()->plus(minutes: 5);
}
```



만약 `retryUntil`와 `tries`가 모두 정의되어 있다면, Laravel은 `retryUntil` 방식을 우선시합니다.

<a name="specifying-queued-listener-backoff"></a>
#### 대기열 리스너 백오프 지정

예외가 발생한 리스너를 다시 시도하기 전에 Laravel이 몇 초를 기다려야 하는지 구성하고 싶다면, 리스너 클래스에서 `Backoff` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```



리스너의 백오프 시간을 결정하기 위해 더 복잡한 로직이 필요한 경우, 리스너 클래스에 `backoff` 메서드를 정의할 수 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 */
public function backoff(OrderShipped $event): int
{
    return 3;
}
```



`backoff` 메서드에서 백오프 값 배열을 반환함으로써 '지수형' 백오프를 쉽게 구성할 수 있습니다. 이 예제에서 재시도 지연 시간은 첫 번째 재시도에는 1초, 두 번째 재시도에는 5초, 세 번째 재시도에는 10초, 그리고 이후 재시도 시 남은 시도가 있다면 매번 10초가 됩니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the queued listener.
 *
 * @return list<int>
 */
public function backoff(OrderShipped $event): array
{
    return [1, 5, 10];
}
```



<a name="specifying-queued-listener-max-exceptions"></a>
#### 큐 대기 리스너 최대 예외 지정

때때로 큐 대기 리스너를 여러 번 시도할 수 있지만, 주어진 수의 처리되지 않은 예외로 인해 재시도가 트리거될 경우에는 실패하도록 지정하고 싶을 수 있습니다(직접 `release` 메서드에 의해 해제되는 경우와 반대로). 이를 수행하기 위해 리스너 클래스에서 `Tries`와 `MaxExceptions` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\InteractsWithQueue;

#[Tries(25)]
#[MaxExceptions(3)]
class SendShipmentNotification implements ShouldQueue
{
    use InteractsWithQueue;

    /**
     * Handle the event.
     */
    public function handle(OrderShipped $event): void
    {
        // Process the event...
    }
}
```



이 예제에서 리스너는 최대 25번까지 재시도됩니다. 그러나 리스너가 처리하지 못한 예외를 세 번 던지면 리스너는 실패하게 됩니다.

<a name="specifying-queued-listener-timeout"></a>
#### 큐된 리스너 타임아웃 지정

종종 큐된 리스너가 수행될 대략적인 시간을 알고 있습니다. 이러한 이유로 Laravel에서는 "timeout" 값을 지정할 수 있습니다. 리스너가 timeout 값으로 지정된 초보다 더 오래 처리되면, 리스너를 처리 중인 워커는 오류와 함께 종료됩니다. 리스너 클래스에서 `Timeout` 속성을 사용하여 리스너가 실행될 수 있는 최대 시간을 정의할 수 있습니다.

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```



타임아웃 시 리스너를 실패로 표시해야 함을 나타내고 싶다면, 리스너 클래스에서 `FailOnTimeout` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Listeners;

use App\Events\OrderShipped;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class SendShipmentNotification implements ShouldQueue
{
    // ...
}
```



<a name="dispatching-events"></a>
## 이벤트 전송

이벤트를 전송하려면 이벤트에서 정적 `dispatch` 메서드를 호출할 수 있습니다. 이 메서드는 `Illuminate\Foundation\Events\Dispatchable` 트레이트에 의해 이벤트에서 사용할 수 있도록 제공됩니다. `dispatch` 메서드에 전달된 모든 인수는 이벤트의 생성자에 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Events\OrderShipped;
use App\Models\Order;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class OrderShipmentController extends Controller
{
    /**
     * Ship the given order.
     */
    public function store(Request $request): RedirectResponse
    {
        $order = Order::findOrFail($request->order_id);

        // Order shipment logic...

        OrderShipped::dispatch($order);

        return redirect('/orders');
    }
}
```



조건부로 이벤트를 발송하고 싶다면, `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
OrderShipped::dispatchIf($condition, $order);

OrderShipped::dispatchUnless($condition, $order);
```



> [!NOTE]
> 테스트할 때 실제로 이벤트 리스너를 트리거하지 않고 특정 이벤트가 발생했는지 확인하는 것이 도움이 될 수 있습니다. Laravel의 [내장 테스트 도우미](#testing)는 이를 매우 쉽게 만들어 줍니다.

<a name="dispatching-events-after-database-transactions"></a>
### 데이터베이스 트랜잭션 후 이벤트 디스패치

때때로, 활성 데이터베이스 트랜잭션이 커밋된 후에만 Laravel이 이벤트를 디스패치하도록 지시하고 싶을 수 있습니다. 이를 위해 이벤트 클래스에 `ShouldDispatchAfterCommit` 인터페이스를 구현할 수 있습니다.

이 인터페이스는 현재 데이터베이스 트랜잭션이 커밋될 때까지 Laravel이 이벤트를 디스패치하지 않도록 지시합니다. 트랜잭션이 실패하면 이벤트는 폐기됩니다. 이벤트가 디스패치될 때 진행 중인 데이터베이스 트랜잭션이 없다면 이벤트는 즉시 디스패치됩니다.

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Events\ShouldDispatchAfterCommit;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderShipped implements ShouldDispatchAfterCommit
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    /**
     * Create a new event instance.
     */
    public function __construct(
        public Order $order,
    ) {}
}
```



<a name="deferring-events"></a>
### 이벤트 연기

연기된 이벤트를 사용하면 특정 코드 블록이 완료될 때까지 모델 이벤트 전송과 이벤트 리스너 실행을 지연시킬 수 있습니다. 이는 모든 관련 레코드가 이벤트 리스너가 트리거되기 전에 생성되도록 보장해야 할 때 특히 유용합니다.

이벤트를 연기하려면 `Event::defer()` 메서드에 클로저를 제공하세요:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
});
```



클로저 내에서 발생하는 모든 이벤트는 클로저가 실행된 후에 전송됩니다. 이는 이벤트 리스너가 지연 실행 동안 생성된 모든 관련 레코드에 접근할 수 있도록 보장합니다. 클로저 내에서 예외가 발생하면 지연된 이벤트는 전송되지 않습니다.

특정 이벤트만 지연하려면 `defer` 메서드의 두 번째 인수로 이벤트 배열을 전달하면 됩니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Event;

Event::defer(function () {
    $user = User::create(['name' => 'Victoria Otwell']);

    $user->posts()->create(['title' => 'My first post!']);
}, ['eloquent.created: '.User::class]);
```



<a name="event-subscribers"></a>
## 이벤트 구독자

<a name="writing-event-subscribers"></a>
### 이벤트 구독자 작성

이벤트 구독자는 구독자 클래스 자체 내에서 여러 이벤트를 구독할 수 있는 클래스이며, 하나의 클래스 내에서 여러 이벤트 핸들러를 정의할 수 있습니다. 구독자는 이벤트 디스패처 인스턴스를 받는 `subscribe` 메서드를 정의해야 합니다. 주어진 디스패처에서 `listen` 메서드를 호출하여 이벤트 리스너를 등록할 수 있습니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     */
    public function subscribe(Dispatcher $events): void
    {
        $events->listen(
            Login::class,
            [UserEventSubscriber::class, 'handleUserLogin']
        );

        $events->listen(
            Logout::class,
            [UserEventSubscriber::class, 'handleUserLogout']
        );
    }
}
```



이벤트 리스너 메서드가 구독자 자체 내에 정의되어 있는 경우, 구독자의 `subscribe` 메서드에서 이벤트와 메서드 이름의 배열을 반환하는 것이 더 편리할 수 있습니다. Laravel은 이벤트 리스너를 등록할 때 자동으로 구독자의 클래스 이름을 결정합니다:

```php
<?php

namespace App\Listeners;

use Illuminate\Auth\Events\Login;
use Illuminate\Auth\Events\Logout;
use Illuminate\Events\Dispatcher;

class UserEventSubscriber
{
    /**
     * Handle user login events.
     */
    public function handleUserLogin(Login $event): void {}

    /**
     * Handle user logout events.
     */
    public function handleUserLogout(Logout $event): void {}

    /**
     * Register the listeners for the subscriber.
     *
     * @return array<string, string>
     */
    public function subscribe(Dispatcher $events): array
    {
        return [
            Login::class => 'handleUserLogin',
            Logout::class => 'handleUserLogout',
        ];
    }
}
```



<a name="registering-event-subscribers"></a>
### 이벤트 구독자 등록

구독자를 작성한 후, Laravel은 구독자 내의 핸들러 메서드가 Laravel의 [이벤트 발견 규칙](#event-discovery)을 따르면 자동으로 등록합니다. 그렇지 않은 경우에는 `Event` 페사드의 `subscribe` 메서드를 사용하여 구독자를 수동으로 등록할 수 있습니다. 일반적으로 이는 애플리케이션의 `AppServiceProvider` 내 `boot` 메서드에서 수행해야 합니다:

```php
<?php

namespace App\Providers;

use App\Listeners\UserEventSubscriber;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Event::subscribe(UserEventSubscriber::class);
    }
}
```



<a name="testing"></a>
## 테스트

이벤트를 디스패치하는 코드를 테스트할 때, 이벤트의 리스너가 실제로 실행되지 않도록 Laravel에 지시하고 싶을 수 있습니다. 리스너의 코드는 해당 이벤트를 디스패치하는 코드와 별도로 직접 테스트할 수 있기 때문입니다. 물론 리스너 자체를 테스트하려면, 테스트에서 리스너 인스턴스를 생성하고 `handle` 메서드를 직접 호출할 수 있습니다.

`Event` 파사드의 `fake` 메서드를 사용하면 리스너 실행을 방지하고, 테스트 중인 코드를 실행한 후, `assertDispatched`, `assertNotDispatched`, `assertNothingDispatched` 메서드를 사용하여 애플리케이션에서 어떤 이벤트가 디스패치되었는지 단언할 수 있습니다:```php tab=Pest
<?php

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;

test('orders can be shipped', function () {
    Event::fake();

    // Perform order shipping...

    // Assert that an event was dispatched...
    Event::assertDispatched(OrderShipped::class);

    // Assert an event was dispatched twice...
    Event::assertDispatched(OrderShipped::class, 2);

    // Assert an event was dispatched once...
    Event::assertDispatchedOnce(OrderShipped::class);

    // Assert an event was not dispatched...
    Event::assertNotDispatched(OrderFailedToShip::class);

    // Assert that no events were dispatched...
    Event::assertNothingDispatched();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderFailedToShip;
use App\Events\OrderShipped;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order shipping.
     */
    public function test_orders_can_be_shipped(): void
    {
        Event::fake();

        // Perform order shipping...

        // Assert that an event was dispatched...
        Event::assertDispatched(OrderShipped::class);

        // Assert an event was dispatched twice...
        Event::assertDispatched(OrderShipped::class, 2);

        // Assert an event was dispatched once...
        Event::assertDispatchedOnce(OrderShipped::class);

        // Assert an event was not dispatched...
        Event::assertNotDispatched(OrderFailedToShip::class);

        // Assert that no events were dispatched...
        Event::assertNothingDispatched();
    }
}
```



주어진 "진실 테스트"를 통과하는 이벤트가 발생했는지 확인하기 위해 `assertDispatched` 또는 `assertNotDispatched` 메서드에 클로저를 전달할 수 있습니다. 주어진 진실 테스트를 통과하는 이벤트가 하나 이상 발생하면 해당 검증은 성공합니다:

```php
Event::assertDispatched(function (OrderShipped $event) use ($order) {
    return $event->order->id === $order->id;
});
```



만약 단순히 이벤트 리스너가 특정 이벤트를 수신하고 있음을 주장하고 싶다면, `assertListening` 메서드를 사용할 수 있습니다:

```php
Event::assertListening(
    OrderShipped::class,
    SendShipmentNotification::class
);
```



> [!WARNING]
> `Event::fake()`를 호출한 후에는 어떤 이벤트 리스너도 실행되지 않습니다. 따라서 테스트에서 모델의 `creating` 이벤트 동안 UUID를 생성하는 것과 같이 이벤트에 의존하는 모델 팩토리를 사용하는 경우, 팩토리를 사용한 **후에** `Event::fake()`를 호출해야 합니다.

<a name="faking-a-subset-of-events"></a>
### 이벤트의 일부를 가짜로 만들기

특정 이벤트 집합에 대한 이벤트 리스너만 가짜로 만들고 싶다면, `fake` 또는 `fakeFor` 메서드에 해당 이벤트를 전달할 수 있습니다:```php tab=Pest
test('orders can be processed', function () {
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
/**
 * Test order process.
 */
public function test_orders_can_be_processed(): void
{
    Event::fake([
        OrderCreated::class,
    ]);

    $order = Order::factory()->create();

    Event::assertDispatched(OrderCreated::class);

    // Other events are dispatched as normal...
    $order->update([
        // ...
    ]);
}
```



`except` 방법을 사용하여 지정된 이벤트 집합을 제외한 모든 이벤트를 위조할 수 있습니다:

```php
Event::fake()->except([
    OrderCreated::class,
]);
```



<a name="scoped-event-fakes"></a>
### 스코프 이벤트 가짜

테스트의 일부에 대해서만 이벤트 리스너를 가짜로 만들고 싶다면, `fakeFor` 메서드를 사용할 수 있습니다:```php tab=Pest
<?php

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;

test('orders can be processed', function () {
    $order = Event::fakeFor(function () {
        $order = Order::factory()->create();

        Event::assertDispatched(OrderCreated::class);

        return $order;
    });

    // Events are dispatched as normal and observers will run...
    $order->update([
        // ...
    ]);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Events\OrderCreated;
use App\Models\Order;
use Illuminate\Support\Facades\Event;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    /**
     * Test order process.
     */
    public function test_orders_can_be_processed(): void
    {
        $order = Event::fakeFor(function () {
            $order = Order::factory()->create();

            Event::assertDispatched(OrderCreated::class);

            return $order;
        });

        // Events are dispatched as normal and observers will run...
        $order->update([
            // ...
        ]);
    }
}
```
{% endraw %}
