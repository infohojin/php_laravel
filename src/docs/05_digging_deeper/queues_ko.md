---
layout: docs
title: "큐" 
---

{% raw %}
# 큐

- [Introduction](#introduction)
    - [Connections vs. Queues](#connections-vs-queues)
    - [Driver Notes and Prerequisites](#driver-prerequisites)
- [Creating Jobs](#creating-jobs)
    - [Generating Job Classes](#generating-job-classes)
    - [Class Structure](#class-structure)
    - [Unique Jobs](#unique-jobs)
    - [Debounced Jobs](#debounced-jobs)
    - [Encrypted Jobs](#encrypted-jobs)
- [Job Middleware](#job-middleware)
    - [Rate Limiting](#rate-limiting)
    - [Preventing Job Overlaps](#preventing-job-overlaps)
    - [Throttling Exceptions](#throttling-exceptions)
    - [Releasing Jobs](#releasing-jobs)
    - [Skipping Jobs](#skipping-jobs)
- [Dispatching Jobs](#dispatching-jobs)
    - [Delayed Dispatching](#delayed-dispatching)
    - [Synchronous Dispatching](#synchronous-dispatching)
    - [Bulk Dispatching](#bulk-dispatching)
    - [Preparing Jobs Before Dispatch](#preparing-jobs-before-dispatch)
    - [Jobs & Database Transactions](#jobs-and-database-transactions)
    - [Job Chaining](#job-chaining)
    - [Customizing The Queue and Connection](#customizing-the-queue-and-connection)
    - [Specifying Max Job Attempts / Timeout Values](#max-job-attempts-and-timeout)
    - [SQS FIFO and Fair Queues](#sqs-fifo-and-fair-queues)
    - [Queue Failover](#queue-failover)
    - [Error Handling](#error-handling)
- [Job Batching](#job-batching)
    - [Defining Batchable Jobs](#defining-batchable-jobs)
    - [Dispatching Batches](#dispatching-batches)
    - [Chains and Batches](#chains-and-batches)
    - [Adding Jobs to Batches](#adding-jobs-to-batches)
    - [Inspecting Batches](#inspecting-batches)
    - [Cancelling Batches](#cancelling-batches)
    - [Batch Failures](#batch-failures)
    - [Pruning Batches](#pruning-batches)
    - [Storing Batches in DynamoDB](#storing-batches-in-dynamodb)
- [Queueing Closures](#queueing-closures)
- [Running the Queue Worker](#running-the-queue-worker)
    - [The `queue:work` Command](#the-queue-work-command)
    - [Queue Priorities](#queue-priorities)
    - [Queue Workers and Deployment](#queue-workers-and-deployment)
    - [Reacting to Worker Signals](#reacting-to-worker-signals)
    - [Job Expirations and Timeouts](#job-expirations-and-timeouts)
    - [Pausing and Resuming Queue Workers](#pausing-and-resuming-queue-workers)
- [Supervisor Configuration](#supervisor-configuration)
- [Dealing With Failed Jobs](#dealing-with-failed-jobs)
    - [Cleaning Up After Failed Jobs](#cleaning-up-after-failed-jobs)
    - [Retrying Failed Jobs](#retrying-failed-jobs)
    - [Ignoring Missing Models](#ignoring-missing-models)
    - [Pruning Failed Jobs](#pruning-failed-jobs)
    - [Storing Failed Jobs in DynamoDB](#storing-failed-jobs-in-dynamodb)
    - [Disabling Failed Job Storage](#disabling-failed-job-storage)
    - [Failed Job Events](#failed-job-events)
- [Clearing Jobs From Queues](#clearing-jobs-from-queues)
- [Monitoring Your Queues](#monitoring-your-queues)
- [Testing](#testing)
    - [Faking a Subset of Jobs](#faking-a-subset-of-jobs)
    - [Testing Job Chains](#testing-job-chains)
    - [Testing Job Batches](#testing-job-batches)
    - [Testing Job / Queue Interactions](#testing-job-queue-interactions)
- [Job Events](#job-events)



<a name="introduction"></a>
## Introduction

While building your web application, you may have some tasks, such as parsing and storing an uploaded CSV file, that take too long to perform during a typical web request. Thankfully, Laravel allows you to easily create queued jobs that may be processed in the background. By moving time intensive tasks to a queue, your application can respond to web requests with blazing speed and provide a better user experience to your customers.

Laravel queues provide a unified queueing API across a variety of different queue backends, such as [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), or even a relational database.

Laravel's queue configuration options are stored in your application's `config/queue.php` configuration file. In this file, you will find connection configurations for each of the queue drivers that are included with the framework, including the database, [Amazon SQS](https://aws.amazon.com/sqs/), [Redis](https://redis.io), and [Beanstalkd](https://beanstalkd.github.io/) drivers, as well as a synchronous driver that will execute jobs immediately (for use during development or testing). A `null` queue driver is also included which discards queued jobs.

> [!NOTE]
> Laravel Horizon is a beautiful dashboard and configuration system for your Redis powered queues. Check out the full [Horizon documentation](/docs/{{version}}/horizon) for more information.

<a name="connections-vs-queues"></a>
### Connections vs. Queues

Before getting started with Laravel queues, it is important to understand the distinction between "connections" and "queues". In your `config/queue.php` configuration file, there is a `connections` configuration array. This option defines the connections to backend queue services such as Amazon SQS, Beanstalk, or Redis. However, any given queue connection may have multiple "queues" which may be thought of as different stacks or piles of queued jobs.

Note that each connection configuration example in the `queue` configuration file contains a `queue` attribute. This is the default queue that jobs will be dispatched to when they are sent to a given connection. In other words, if you dispatch a job without explicitly defining which queue it should be dispatched to, the job will be placed on the queue that is defined in the `queue` attribute of the connection configuration:

```php
use App\Jobs\ProcessPodcast;

// This job is sent to the default connection's default queue...
ProcessPodcast::dispatch();

// This job is sent to the default connection's "emails" queue...
ProcessPodcast::dispatch()->onQueue('emails');
```



일부 애플리케이션은 여러 큐에 작업을 푸시할 필요가 없고, 대신 하나의 단순한 큐를 선호할 수 있습니다. 그러나 작업을 여러 큐에 푸시하는 것은 작업 처리 우선순위를 지정하거나 세분화하려는 애플리케이션에 특히 유용할 수 있습니다. Laravel 큐 워커는 처리할 큐를 우선순위에 따라 지정할 수 있기 때문입니다. 예를 들어, 작업을 `high` 큐에 푸시하면 해당 작업에 더 높은 처리 우선순위를 부여하는 워커를 실행할 수 있습니다:

```shell
php artisan queue:work --queue=high,default
```



<a name="driver-prerequisites"></a>
### 드라이버 참고 사항 및 전제 조건

<a name="database"></a>
#### 데이터베이스

`database` 큐 드라이버를 사용하려면 작업을 보관할 데이터베이스 테이블이 필요합니다. 일반적으로 이는 Laravel의 기본 `0001_01_01_000002_create_jobs_table.php` [데이터베이스 마이그레이션](/docs/{{version}}/migrations)에 포함되어 있습니다. 그러나 애플리케이션에 이 마이그레이션이 포함되어 있지 않은 경우, `make:queue-table` Artisan 명령어를 사용하여 생성할 수 있습니다:

```shell
php artisan make:queue-table

php artisan migrate
```



<a name="redis"></a>
#### 레디스 (Redis)

`redis` 큐 드라이버를 사용하려면 `config/database.php` 구성 파일에서 레디스 데이터베이스 연결을 설정해야 합니다.

> [!WARNING]
> `serializer`와 `compression` 레디스 옵션은 `redis` 큐 드라이버에서 지원되지 않습니다.

<a name="redis-cluster"></a>
##### 레디스 클러스터 (Redis Cluster)

Redis 큐 연결이 [Redis 클러스터](https://redis.io/docs/latest/operate/rs/databases/durability-ha/clustering)를 사용하는 경우, 큐 이름에는 [키 해시 태그](https://redis.io/docs/latest/develop/using-commands/keyspace/#hashtags)를 포함해야 합니다. 이는 주어진 큐에 대한 모든 Redis 키가 동일한 해시 슬롯에 배치되도록 보장하기 위해 필요합니다:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', '{default}'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => null,
    'after_commit' => false,
],
```



<a name="blocking"></a>
##### 블로킹

Redis 큐를 사용할 때, `block_for` 구성 옵션을 사용하여 작업이 사용 가능해질 때까지 드라이버가 기다릴 시간을 지정할 수 있으며, 그 후 워커 루프를 반복하고 Redis 데이터베이스를 다시 폴링합니다.

큐 부하에 따라 이 값을 조정하는 것이 새로운 작업을 위해 Redis 데이터베이스를 지속적으로 폴링하는 것보다 더 효율적일 수 있습니다. 예를 들어, 드라이버가 작업이 사용 가능해질 때까지 5초 동안 블록하도록 나타내기 위해 값을 `5`로 설정할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    'connection' => env('REDIS_QUEUE_CONNECTION', 'default'),
    'queue' => env('REDIS_QUEUE', 'default'),
    'retry_after' => env('REDIS_QUEUE_RETRY_AFTER', 90),
    'block_for' => 5,
    'after_commit' => false,
],
```



> [!WARNING]
> `block_for`를 `0`로 설정하면, 작업이 사용 가능해질 때까지 큐 작업자가 무한히 차단됩니다. 이로 인해 `SIGTERM`과 같은 신호도 다음 작업이 처리될 때까지 처리되지 않습니다.

<a name="sqs-overflow-storage"></a>
#### SQS 오버플로우 저장소

Amazon SQS는 큐에 저장되는 메시지 페이로드의 최대 크기를 제한합니다. 만약 이 제한을 초과할 수 있는 페이로드를 가진 작업을 전송해야 한다면, Laravel을 구성하여 초과된 SQS 페이로드를 캐시 저장소에 저장하고 SQS를 통해 포인터를 보내도록 할 수 있습니다. 이 기능을 활성화하려면, SQS 큐 연결 구성에 `overflow` 배열을 추가하십시오:

```php
'sqs' => [
    'driver' => 'sqs',
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'prefix' => env('SQS_PREFIX', 'https://sqs.us-east-1.amazonaws.com/your-account-id'),
    'queue' => env('SQS_QUEUE', 'default'),
    'suffix' => env('SQS_SUFFIX'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'after_commit' => false,
    'overflow' => [
        'enabled' => env('SQS_OVERFLOW_ENABLED', false),
        'store' => env('SQS_OVERFLOW_STORE'),
        'always' => false,
        'delete_after_processing' => true,
        'flush_on_clear' => env('SQS_OVERFLOW_FLUSH_ON_CLEAR', false),
    ],
],
```



When overflow storage is enabled, Laravel will store payloads that are at least 1 MB in the configured cache store. If the `always` option is `true`, every SQS payload will be stored in the cache store regardless of its size. Since queued jobs will need to retrieve their payloads from the cache store when they are processed, you should choose a store that can retain the payloads until your workers process them. By default, stored payloads are deleted after their jobs have been successfully processed and deleted from SQS.

If the `flush_on_clear` option is `true`, the configured overflow cache store will be flushed when the `queue:clear` command clears the SQS queue. Since flushing a cache store may remove all items from that store, you should configure SQS overflow storage to use a dedicated cache store when enabling this option.

<a name="other-driver-prerequisites"></a>
#### Other Driver Prerequisites

The following dependencies are needed for the listed queue drivers. These dependencies may be installed via the Composer package manager:

<div class="content-list" markdown="1">

- Amazon SQS: `aws/aws-sdk-php ~3.0`
- Beanstalkd: `pda/pheanstalk ~5.0`
- Redis: `predis/predis ~3.0` or phpredis PHP extension
- [MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/): `mongodb/laravel-mongodb`

</div>

<a name="creating-jobs"></a>
## Creating Jobs

<a name="generating-job-classes"></a>
### Generating Job Classes

By default, all of the queueable jobs for your application are stored in the `app/Jobs` directory. If the `app/Jobs` directory doesn't exist, it will be created when you run the `make:job` Artisan command:

```shell
php artisan make:job ProcessPodcast
```



생성된 클래스는 `Illuminate\Contracts\Queue\ShouldQueue` 인터페이스를 구현하며, 이는 작업이 비동기적으로 실행되도록 큐에 푸시되어야 함을 Laravel에 알립니다.

> [!NOTE]
> 작업 스텁은 [스텁 퍼블리싱](/docs/{{version}}/artisan#stub-customization)을 사용하여 커스터마이징할 수 있습니다.

<a name="class-structure"></a>
### 클래스 구조

작업 클래스는 매우 단순하며, 일반적으로 큐에서 작업이 처리될 때 호출되는 `handle` 메서드만 포함합니다. 시작하기 위해 예시 작업 클래스를 살펴보겠습니다. 이 예제에서는 팟캐스트 발행 서비스를 관리한다고 가정하고, 업로드된 팟캐스트 파일을 발행하기 전에 처리해야 합니다:

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        // Process uploaded podcast...
    }
}
```



In this example, note that we were able to pass an [Eloquent model](/docs/{{version}}/eloquent) directly into the queued job's constructor. Because of the `Queueable` trait that the job is using, Eloquent models and their loaded relationships will be gracefully serialized and unserialized when the job is processing.

If your queued job accepts an Eloquent model in its constructor, only the identifier for the model will be serialized onto the queue. When the job is actually handled, the queue system will automatically re-retrieve the full model instance and its loaded relationships from the database. This approach to model serialization allows for much smaller job payloads to be sent to your queue driver.

<a name="handle-method-dependency-injection"></a>
#### `handle` Method Dependency Injection

The `handle` method is invoked when the job is processed by the queue. Note that we are able to type-hint dependencies on the `handle` method of the job. The Laravel [service container](/docs/{{version}}/container) automatically injects these dependencies.

If you would like to take total control over how the container injects dependencies into the `handle` method, you may use the container's `bindMethod` method. The `bindMethod` method accepts a callback which receives the job and the container. Within the callback, you are free to invoke the `handle` method however you wish. Typically, you should call this method from the `boot` method of your `App\Providers\AppServiceProvider` [service provider](/docs/{{version}}/providers):

```php
use App\Jobs\ProcessPodcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Foundation\Application;

$this->app->bindMethod([ProcessPodcast::class, 'handle'], function (ProcessPodcast $job, Application $app) {
    return $job->handle($app->make(AudioProcessor::class));
});
```



> [!WARNING]
> Binary data, such as raw image contents, should be passed through the `base64_encode` function before being passed to a queued job. Otherwise, the job may not properly serialize to JSON when being placed on the queue.

<a name="handling-relationships"></a>
#### Queued Relationships

Because all loaded Eloquent model relationships also get serialized when a job is queued, the serialized job string can sometimes become quite large. Furthermore, when a job is deserialized and model relationships are re-retrieved from the database, they will be retrieved in their entirety. Any previous relationship constraints that were applied before the model was serialized during the job queueing process will not be applied when the job is deserialized. Therefore, if you wish to work with a subset of a given relationship, you should re-constrain that relationship within your queued job.

Or, to prevent relations from being serialized, you can call the `withoutRelations` method on the model when setting a property value. This method will return an instance of the model without its loaded relationships:

```php
/**
 * Create a new job instance.
 */
public function __construct(
    Podcast $podcast,
) {
    $this->podcast = $podcast->withoutRelations();
}
```



나머지는 그대로 두고 특정 관계만 제거해야 한다면, `withoutRelation` 방법을 사용할 수 있습니다:

```php
$this->podcast = $podcast->withoutRelation('comments');
```



만약 [PHP 생성자 속성 프로모션](https://www.php.net/manual/en/language.oop5.decon.php#language.oop5.decon.constructor.promotion)을 사용 중이고 Eloquent 모델의 관계가 직렬화되지 않도록 표시하고 싶다면, `WithoutRelations` 속성을 사용할 수 있습니다:

```php
use Illuminate\Queue\Attributes\WithoutRelations;

/**
 * Create a new job instance.
 */
public function __construct(
    #[WithoutRelations]
    public Podcast $podcast,
) {}
```



편의를 위해, 관계 없이 모든 모델을 직렬화하려는 경우, 각 모델에 속성을 적용하는 대신 전체 클래스에 `WithoutRelations` 속성을 적용할 수 있습니다:

```php
<?php

namespace App\Jobs;

use App\Models\DistributionPlatform;
use App\Models\Podcast;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\WithoutRelations;

#[WithoutRelations]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
        public DistributionPlatform $platform,
    ) {}
}
```



작업이 단일 모델 대신 Eloquent 모델의 컬렉션이나 배열을 받으면, 해당 컬렉션 내의 모델들은 작업이 역직렬화되고 실행될 때 관계가 복원되지 않습니다. 이는 많은 수의 모델을 처리하는 작업에서 과도한 리소스 사용을 방지하기 위한 것입니다.

<a name="unique-jobs"></a>
### 고유 작업

> [!WARNING]
> 고유 작업은 [잠금](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file` 및 `array` 캐시 드라이버가 원자적 잠금을 지원합니다.

> [!WARNING]
> 고유 작업 제약 조건은 배치 내의 작업에는 적용되지 않습니다.

때때로 특정 작업의 인스턴스가 어느 시점에서든 큐에 하나만 있도록 보장하고 싶을 수 있습니다. 이 경우 작업 클래스에 `ShouldBeUnique` 인터페이스를 구현하면 됩니다. 이 인터페이스는 클래스에 추가 메서드를 정의할 필요가 없습니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...
}
```



위의 예제에서 `UpdateSearchIndex` 작업은 고유합니다. 따라서 다른 인스턴스의 작업이 이미 대기열에 있으며 처리를 완료하지 않은 경우, 해당 작업은 전송되지 않습니다.

특정 경우에는 작업을 고유하게 만드는 특정 "키"를 정의하거나, 작업이 더 이상 고유하지 않게 되는 제한 시간을 지정하고 싶을 수 있습니다. 이를 달성하기 위해 `UniqueFor` 속성을 사용하고 작업 클래스에서 `uniqueId` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUnique;
use Illuminate\Queue\Attributes\UniqueFor;

#[UniqueFor(3600)]
class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    /**
     * The product instance.
     *
     * @var \App\Models\Product
     */
    public $product;

    /**
     * Get the unique ID for the job.
     */
    public function uniqueId(): string
    {
        return $this->product->id;
    }
}
```

In the example above, the `UpdateSearchIndex` job is unique by a product ID. So, any new dispatches of the job with the same product ID will be ignored until the existing job has completed processing. In addition, if the existing job is not processed within one hour, the unique lock will be released and another job with the same unique key can be dispatched to the queue.

> [!WARNING]
> If your application dispatches jobs from multiple web servers or containers, you should ensure that all of your servers are communicating with the same central cache server so that Laravel can accurately determine if a job is unique.

<a name="keeping-jobs-unique-until-processing-begins"></a>
#### Keeping Jobs Unique Until Processing Begins

By default, unique jobs are "unlocked" after a job completes processing or fails all of its retry attempts. However, there may be situations where you would like your job to unlock immediately before it is processed. To accomplish this, your job should implement the `ShouldBeUniqueUntilProcessing` contract instead of the `ShouldBeUnique` contract:

```php
<?php

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Contracts\Queue\ShouldBeUniqueUntilProcessing;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUniqueUntilProcessing
{
    // ...
}
```



<a name="unique-job-locks"></a>
#### 고유 작업 잠금

백그라운드에서 `ShouldBeUnique` 작업이 디스패치되면, Laravel은 `uniqueId` 키를 사용하여 [잠금](/docs/{{version}}/cache#atomic-locks)을 획득하려 시도합니다. 만약 잠금이 이미 사용 중이라면, 작업은 디스패치되지 않습니다. 이 잠금은 작업 처리가 완료되거나 모든 재시도 시도가 실패하면 해제됩니다. 기본적으로, Laravel은 이 잠금을 얻기 위해 기본 캐시 드라이버를 사용합니다. 그러나 잠금을 획득하기 위해 다른 드라이버를 사용하려는 경우, 사용해야 할 캐시 드라이버를 반환하는 `uniqueVia` 메서드를 정의할 수 있습니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

class UpdateSearchIndex implements ShouldQueue, ShouldBeUnique
{
    // ...

    /**
     * Get the cache driver for the unique job lock.
     */
    public function uniqueVia(): Repository
    {
        return Cache::driver('redis');
    }
}
```



> [!NOTE]
> 작업의 동시 처리를 제한할 필요가 있는 경우, 대신 [WithoutOverlapping](/docs/{{version}}/queues#preventing-job-overlaps) 작업 미들웨어를 사용하세요.

<a name="debounced-jobs"></a>
### 디바운스된 작업

때때로 동일한 작업이 짧은 시간 내에 여러 번 디스패치될 때, 실제로 실행되는 것은 가장 최근의 디스패치만 되도록 하고 싶을 수 있습니다. 이 경우 작업에 `DebounceFor` 속성을 추가하면 됩니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\DebounceFor;

#[DebounceFor(30)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(public int $productId)
    {
    }

    /**
     * Get the debounce ID for the job.
     */
    public function debounceId(): string
    {
        return (string) $this->productId;
    }
}
```



위 예제에서, 동일한 제품에 대해 `30` 초 내에 `UpdateSearchIndex`를 반복적으로 발송하면, 작업이 디바운스되어 최신 발송만 실행됩니다.

자주 재발송되는 작업이 연기될 수 있는 최대 시간을 제한하고 싶다면, `DebounceFor` 속성에 `maxWait` 인수를 제공할 수 있습니다:

```php
#[DebounceFor(30, maxWait: 120)]
class UpdateSearchIndex implements ShouldQueue
{
    use Queueable;

    // ...
}
```



작업에서 `debounceVia` 메서드를 정의하여 디바운스 추적에 사용되는 캐시 저장소를 사용자 정의할 수 있습니다:

```php
use Illuminate\Contracts\Cache\Repository;
use Illuminate\Support\Facades\Cache;

public function debounceVia(): Repository
{
    return Cache::driver('redis');
}
```



만약 디바운스된 작업이 새로운 디스패치에 의해 대체된다면, Laravel은 `Illuminate\Queue\Events\JobDebounced` 이벤트를 디스패치하고 대체된 작업을 큐에서 제거할 것입니다.

> [!WARNING]
> 디바운스된 작업과 고유 작업은 상호 배타적입니다. `DebounceFor` 속성을 사용하는 작업은 `ShouldBeUnique`를 구현해서는 안 됩니다.

> [!WARNING]
> 애플리케이션이 여러 웹 서버나 컨테이너에서 디바운스된 작업을 디스패치하는 경우, 모든 서버가 동일한 중앙 캐시 서버와 통신하고 있는지 확인해야 합니다.

<a name="encrypted-jobs"></a>
### 암호화된 작업

Laravel은 [암호화](/docs/{{version}}/encryption)를 통해 작업 데이터의 프라이버시와 무결성을 보장할 수 있도록 합니다. 시작하려면, 단순히 작업 클래스에 `ShouldBeEncrypted` 인터페이스를 추가하면 됩니다. 이 인터페이스가 클래스에 추가되면, Laravel은 작업을 큐에 넣기 전에 자동으로 암호화합니다:

```php
<?php

use Illuminate\Contracts\Queue\ShouldBeEncrypted;
use Illuminate\Contracts\Queue\ShouldQueue;

class UpdateSearchIndex implements ShouldQueue, ShouldBeEncrypted
{
    // ...
}
```



<a name="job-middleware"></a>
## 작업 미들웨어

작업 미들웨어는 대기열에 있는 작업의 실행 주위에 맞춤 로직을 감쌀 수 있게 해 주어, 작업 자체의 보일러플레이트를 줄입니다. 예를 들어, 다음 `handle` 메서드는 Laravel의 Redis 속도 제한 기능을 활용하여 5초마다 하나의 작업만 처리될 수 있도록 합니다:

```php
use Illuminate\Support\Facades\Redis;

/**
 * Execute the job.
 */
public function handle(): void
{
    Redis::throttle('key')->block(0)->allow(1)->every(5)->then(function () {
        info('Lock obtained...');

        // Handle job...
    }, function () {
        // Could not obtain lock...

        return $this->release(5);
    });
}
```



이 코드는 유효하지만, `handle` 메서드의 구현은 Redis 레이트 제한 로직으로 인해 복잡해져 소음이 발생합니다. 또한, 이 레이트 제한 로직은 레이트 제한을 적용하려는 다른 작업에도 복제되어야 합니다. handle 메서드에서 레이트 제한을 적용하는 대신, 레이트 제한을 처리하는 작업 미들웨어를 정의할 수 있습니다:

```php
<?php

namespace App\Jobs\Middleware;

use Closure;
use Illuminate\Support\Facades\Redis;

class RateLimited
{
    /**
     * Process the queued job.
     *
     * @param  \Closure(object): void  $next
     */
    public function handle(object $job, Closure $next): void
    {
        Redis::throttle('key')
            ->block(0)->allow(1)->every(5)
            ->then(function () use ($job, $next) {
                // Lock obtained...

                $next($job);
            }, function () use ($job) {
                // Could not obtain lock...

                $job->release(5);
            });
    }
}
```



보시다시피, [라우트 미들웨어](/docs/{{version}}/middleware)와 마찬가지로, 작업 미들웨어는 처리 중인 작업과 작업 처리를 계속하기 위해 호출해야 하는 콜백을 받습니다.

`make:job-middleware` Artisan 명령을 사용하여 새 작업 미들웨어 클래스를 생성할 수 있습니다. 작업 미들웨어를 생성한 후에는 작업의 `middleware` 메서드에서 반환하여 작업에 첨부할 수 있습니다. 이 메서드는 `make:job` Artisan 명령으로 생성된 작업에는 존재하지 않으므로, 작업 클래스에 수동으로 추가해야 합니다:

```php
use App\Jobs\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited];
}
```



> [!NOTE]
> 작업 미들웨어는 [큐 가능한 이벤트 리스너들](/docs/{{version}}/events#queued-event-listeners), [메일러블](/docs/{{version}}/mail#queueing-mail), 그리고 [알림](/docs/{{version}}/notifications#queueing-notifications)에도 할당될 수 있습니다.

<a name="rate-limiting"></a>
### 속도 제한

앞서 자체 속도 제한 작업 미들웨어를 작성하는 방법을 보여주었지만, 실제로 Laravel에는 작업을 속도 제한하는 데 사용할 수 있는 속도 제한 미들웨어가 포함되어 있습니다. [라우트 속도 제한기](/docs/{{version}}/routing#defining-rate-limiters)처럼 작업 속도 제한기도 `RateLimiter` 페이사드의 `for` 메서드를 사용하여 정의됩니다.

예를 들어, 사용자가 데이터를 한 시간마다 백업할 수 있도록 허용하면서 프리미엄 고객에게는 이러한 제한을 두지 않기를 원할 수 있습니다. 이를 달성하기 위해 `AppServiceProvider`의 `boot` 메서드에서 `RateLimiter`를 정의할 수 있습니다:

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    RateLimiter::for('backups', function (object $job) {
        return $job->user->vipCustomer()
            ? Limit::none()
            : Limit::perHour(1)->by($job->user->id);
    });
}
```



위의 예제에서는 시간당 제한을 정의했지만, `perMinute` 방법을 사용하여 분 단위의 제한을 쉽게 정의할 수 있습니다. 또한, 원하는 값을 제한의 `by` 방법에 전달할 수 있지만, 이 값은 대부분 고객별로 제한을 구분하는 데 사용됩니다:

```php
return Limit::perMinute(50)->by($job->user->id);
```



한 번 속도 제한을 정의하면 `Illuminate\Queue\Middleware\RateLimited` 미들웨어를 사용하여 해당 속도 제한기를 작업에 연결할 수 있습니다. 작업이 속도 제한을 초과할 때마다, 이 미들웨어는 속도 제한 기간에 따라 적절한 지연 시간을 두고 작업을 큐로 다시 보냅니다:

```php
use Illuminate\Queue\Middleware\RateLimited;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new RateLimited('backups')];
}
```



속도 제한된 작업을 다시 큐에 놓으면 작업의 `attempts` 총 횟수가 여전히 증가합니다. 이에 따라 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 조정할 수 있습니다. 또는 작업을 더 이상 시도하지 않아야 하는 시간을 정의하기 위해 [retryUntil 메서드](#time-based-attempts)를 사용할 수도 있습니다.

`releaseAfter` 메서드를 사용하면, 해제된 작업이 다시 시도되기 전에 경과해야 하는 초 단위 시간도 지정할 수 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->releaseAfter(60)];
}
```



작업이 속도 제한될 때 재시도되기를 원하지 않는 경우, `dontRelease` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new RateLimited('backups'))->dontRelease()];
}
```



<a name="rate-limiting-with-redis"></a>
#### Redis를 사용한 속도 제한

Redis를 사용하는 경우, Redis에 맞게 최적화되어 있으며 기본 속도 제한 미들웨어보다 더 효율적인 `Illuminate\Queue\Middleware\RateLimitedWithRedis` 미들웨어를 사용할 수 있습니다:

```php
use Illuminate\Queue\Middleware\RateLimitedWithRedis;

public function middleware(): array
{
    return [new RateLimitedWithRedis('backups')];
}
```



`connection` 메서드는 미들웨어가 사용할 Redis 연결을 지정하는 데 사용할 수 있습니다:

```php
return [(new RateLimitedWithRedis('backups'))->connection('limiter')];
```



<a name="preventing-job-overlaps"></a>
### 작업 중복 방지

Laravel에는 임의의 키를 기반으로 작업 중복을 방지할 수 있는 `Illuminate\Queue\Middleware\WithoutOverlapping` 미들웨어가 포함되어 있습니다. 이는 큐에 쌓인 작업이 한 번에 하나의 작업만 수정해야 하는 리소스를 수정할 때 유용할 수 있습니다.

예를 들어, 사용자의 신용 점수를 업데이트하는 큐에 쌓인 작업이 있고 동일한 사용자 ID에 대한 신용 점수 업데이트 작업 중복을 방지하고 싶다고 가정해 보겠습니다. 이를 달성하기 위해, 작업의 `middleware` 메서드에서 `WithoutOverlapping` 미들웨어를 반환할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new WithoutOverlapping($this->user->id)];
}
```



중첩 작업을 다시 큐에 넣으면 작업의 전체 시도 횟수가 여전히 증가합니다. 이에 따라 작업 클래스의 `Tries` 및 `MaxExceptions` 속성을 조정하는 것이 좋습니다. 예를 들어, 기본값으로 그대로 둔 `Tries`를 1로 유지하면 중첩된 작업이 나중에 다시 시도되는 것을 방지할 수 있습니다.

동일한 유형의 모든 중첩 작업은 다시 큐에 반환됩니다. 또한 반환된 작업이 다시 시도되기 전에 경과해야 하는 시간을 초 단위로 지정할 수도 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->releaseAfter(60)];
}
```



겹치는 작업을 즉시 삭제하여 재시도되지 않도록 하려면, `dontRelease` 방법을 사용할 수 있습니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->dontRelease()];
}
```



`WithoutOverlapping` 미들웨어는 Laravel의 원자적 잠금 기능을 기반으로 작동합니다. 때때로 작업이 예기치 않게 실패하거나 시간 초과되어 잠금이 해제되지 않을 수 있습니다. 따라서 `expireAfter` 메서드를 사용하여 잠금 만료 시간을 명시적으로 정의할 수 있습니다. 예를 들어, 아래의 예시는 작업이 처리되기 시작한 후 3분 후에 Laravel이 `WithoutOverlapping` 잠금을 해제하도록 지시합니다:

```php
/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new WithoutOverlapping($this->order->id))->expireAfter(180)];
}
```



> [!WARNING]
> `WithoutOverlapping` 미들웨어는 [잠금](/docs/{{version}}/cache#atomic-locks)을 지원하는 캐시 드라이버가 필요합니다. 현재 `memcached`, `redis`, `dynamodb`, `database`, `file` 및 `array` 캐시 드라이버는 원자적 잠금을 지원합니다.

<a name="sharing-lock-keys"></a>
#### 작업 클래스 간 잠금 키 공유

기본적으로 `WithoutOverlapping` 미들웨어는 동일한 클래스의 작업이 겹치는 것만 방지합니다. 따라서 두 개의 서로 다른 작업 클래스가 동일한 잠금 키를 사용할 수 있지만, 겹침이 방지되지는 않습니다. 그러나 `shared` 메서드를 사용하여 키를 작업 클래스 전체에 적용하도록 Laravel에 지시할 수 있습니다:

```php
use Illuminate\Queue\Middleware\WithoutOverlapping;

class ProviderIsDown
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}

class ProviderIsUp
{
    // ...

    public function middleware(): array
    {
        return [
            (new WithoutOverlapping("status:{$this->provider}"))->shared(),
        ];
    }
}
```



<a name="throttling-exceptions"></a>
### 예외 제한

Laravel은 예외를 제한할 수 있는 `Illuminate\Queue\Middleware\ThrottlesExceptions` 미들웨어를 포함하고 있습니다. 작업이 특정 횟수의 예외를 발생시키면, 이후에 작업을 실행하려는 모든 시도는 지정된 시간 간격이 지나기 전까지 지연됩니다. 이 미들웨어는 불안정한 타사 서비스와 상호작용하는 작업에 특히 유용합니다.

예를 들어, 예외를 발생시키기 시작하는 타사 API와 상호작용하는 큐 작업이 있다고 가정해 봅시다. 예외를 제한하려면, 작업의 `middleware` 메서드에서 `ThrottlesExceptions` 미들웨어를 반환하면 됩니다. 일반적으로 이 미들웨어는 [시간 기반 시도](#time-based-attempts)를 구현한 작업과 함께 사용해야 합니다:

```php
use DateTime;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [new ThrottlesExceptions(10, 5 * 60)];
}

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 30);
}
```



미들웨어가 받는 첫 번째 생성자 인수는 작업이 제한되기 전에 발생시킬 수 있는 예외의 수이고, 두 번째 생성자 인수는 작업이 제한된 후 다시 시도되기 전에 경과해야 하는 초(seconds)의 수입니다. 위의 코드 예시에서 작업이 연속으로 10번 예외를 발생시키면, 30분 시간 제한에 따라 제약을 받으며 작업을 다시 시도하기 전에 5분을 기다립니다.

작업이 예외를 발생시키더라도 예외 임계값에 도달하지 않은 경우, 작업은 일반적으로 즉시 재시도됩니다. 그러나 미들웨어를 작업에 첨부할 때 `backoff` 메서드를 호출하여 이러한 작업이 지연될 분(minutes)의 수를 지정할 수 있습니다.

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(5)];
}
```



`backoff` 메서드는 던져진 예외를 받는 클로저도 허용하여 지연 시간을 동적으로 결정할 수 있습니다:

```php
use App\Exceptions\RateLimitedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;
use Throwable;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 5 * 60))->backoff(
        fn (Throwable $throwable) => $throwable instanceof RateLimitedException
            ? $throwable->retryAfterMinutes()
            : 5
    )];
}
```



내부적으로 이 미들웨어는 Laravel의 캐시 시스템을 사용하여 속도 제한을 구현하며, 작업의 클래스 이름이 캐시 "키"로 사용됩니다. 미들웨어를 작업에 연결할 때 `by` 메서드를 호출하여 이 키를 재정의할 수 있습니다. 이는 여러 작업이 동일한 타사 서비스와 상호작용하며 공통의 제한을 공유하도록 하여 단일 공유 제한을 준수하게 하고 싶을 때 유용할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->by('key')];
}
```



기본적으로, 이 미들웨어는 모든 예외를 제한합니다. 이 동작은 미들웨어를 작업에 연결할 때 `when` 메서드를 호출하여 수정할 수 있습니다. 그러면 예외는 `when` 메서드에 제공된 클로저가 `true`를 반환할 경우에만 제한됩니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->when(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```



작업을 다시 큐에 반환하거나 예외를 발생시키는 `when` 방법과 달리, `deleteWhen` 방법은 특정 예외가 발생할 때 작업을 완전히 삭제할 수 있습니다:

```php
use App\Exceptions\CustomerDeletedException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(2, 10 * 60))->deleteWhen(CustomerDeletedException::class)];
}
```



만약 제한된 예외를 귀하의 애플리케이션 예외 처리기에 보고하고 싶다면, 미들웨어를 작업에 연결할 때 `report` 메서드를 호출하면 됩니다. 선택적으로, `report` 메서드에 클로저를 제공할 수 있으며, 예외는 주어진 클로저가 `true`를 반환할 경우에만 보고됩니다:

```php
use Illuminate\Http\Client\HttpClientException;
use Illuminate\Queue\Middleware\ThrottlesExceptions;

/**
 * Get the middleware the job should pass through.
 *
 * @return array<int, object>
 */
public function middleware(): array
{
    return [(new ThrottlesExceptions(10, 10 * 60))->report(
        fn (Throwable $throwable) => $throwable instanceof HttpClientException
    )];
}
```



<a name="throttling-exceptions-with-redis"></a>
#### Redis로 예외 제한 처리

Redis를 사용하는 경우, Redis에 최적화되어 기본 예외 제한 미들웨어보다 더 효율적인 `Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis` 미들웨어를 사용할 수 있습니다:

```php
use Illuminate\Queue\Middleware\ThrottlesExceptionsWithRedis;

public function middleware(): array
{
    return [new ThrottlesExceptionsWithRedis(10, 10 * 60)];
}
```



`connection` 방법은 미들웨어가 사용할 Redis 연결을 지정하는 데 사용될 수 있습니다:

```php
return [(new ThrottlesExceptionsWithRedis(10, 10 * 60))->connection('limiter')];
```



<a name="releasing-jobs"></a>
### 작업 해제

`Release` 미들웨어를 사용하면 작업을 실행하지 않고도 큐로 다시 해제할 수 있습니다. `Release::when` 메서드는 주어진 조건이 `true`로 평가되면 작업을 해제하며, `Release::unless` 메서드는 조건이 `false`로 평가되면 작업을 해제합니다:

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when($condition, releaseAfter: 60),
    ];
}
```



작업을 다시 큐에 반환해도 작업의 총 시도 횟수는 증가합니다. 작업 클래스에서 `Tries` 및 `MaxExceptions` 속성을 적절히 조정하고 싶을 수 있습니다.

또한 더 복잡한 조건 평가를 위해 `Closure`를 `when` 및 `unless` 메서드에 전달할 수도 있습니다:

```php
use Illuminate\Queue\Middleware\Release;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Release::when(function (): bool {
            return ! $this->order->isPaid();
        }, releaseAfter: 60),
    ];
}
```



<a name="skipping-jobs"></a>
### 작업 건너뛰기

`Skip` 미들웨어를 사용하면 작업의 로직을 수정할 필요 없이 작업을 건너뛰거나 삭제하도록 지정할 수 있습니다. `Skip::when` 메서드는 주어진 조건이 `true`로 평가되면 작업을 삭제하고, `Skip::unless` 메서드는 조건이 `false`로 평가되면 작업을 삭제합니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when($condition),
    ];
}
```



더 복잡한 조건 평가를 위해 `Closure`를 `when` 및 `unless` 메서드에 전달할 수도 있습니다:

```php
use Illuminate\Queue\Middleware\Skip;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [
        Skip::when(function (): bool {
            return $this->shouldSkip();
        }),
    ];
}
```



<a name="dispatching-jobs"></a>
## 작업 디스패치

작업 클래스를 작성한 후에는, 작업 자체에서 `dispatch` 메서드를 사용하여 해당 작업을 디스패치할 수 있습니다. `dispatch` 메서드에 전달된 인수는 작업의 생성자에 전달됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast);

        return redirect('/podcasts');
    }
}
```



작업을 조건부로 전송하고 싶다면, `dispatchIf` 및 `dispatchUnless` 메서드를 사용할 수 있습니다:

```php
ProcessPodcast::dispatchIf($accountActive, $podcast);

ProcessPodcast::dispatchUnless($accountSuspended, $podcast);
```



새로운 Laravel 애플리케이션에서는 `database` 연결이 기본 큐로 정의되어 있습니다. 애플리케이션의 `.env` 파일에서 `QUEUE_CONNECTION` 환경 변수를 변경하여 다른 기본 큐 연결을 지정할 수 있습니다.

<a name="delayed-dispatching"></a>
### 지연 디스패치

작업이 큐 워커에 의해 즉시 처리되지 않도록 지정하려면 작업을 디스패치할 때 `delay` 메서드를 사용할 수 있습니다. 예를 들어, 작업이 디스패치된 후 10분이 지나기 전까지 처리되지 않도록 지정해 보겠습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // ...

        ProcessPodcast::dispatch($podcast)
            ->delay(now()->plus(minutes: 10));

        return redirect('/podcasts');
    }
}
```



경우에 따라 작업에는 기본 지연이 설정되어 있을 수 있습니다. 이 지연을 건너뛰고 작업을 즉시 처리하도록 전송해야 하는 경우, `withoutDelay` 방법을 사용할 수 있습니다:

```php
ProcessPodcast::dispatch($podcast)->withoutDelay();
```



> [!WARNING]
> 아마존 SQS 큐 서비스는 최대 지연 시간이 15분입니다.

<a name="synchronous-dispatching"></a>
### 동기식 디스패치

작업을 즉시(동기적으로) 디스패치하려면 `dispatchSync` 메서드를 사용할 수 있습니다. 이 메서드를 사용할 경우, 작업은 큐에 담기지 않고 현재 프로세스 내에서 즉시 실행됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatchSync($podcast);

        return redirect('/podcasts');
    }
}
```



<a name="deferred-dispatching"></a>
#### 지연 디스패치

지연 동기 디스패치를 사용하면, 현재 프로세스 중에 작업을 디스패치할 수 있지만, HTTP 응답이 사용자에게 전송된 후에 처리됩니다. 이를 통해 사용자의 애플리케이션 경험을 느리게 하지 않고도 동기적으로 "대기열" 작업을 처리할 수 있습니다. 동기 작업의 실행을 지연시키려면 작업을 `deferred` 연결에 디스패치하십시오:

```php
RecordDelivery::dispatch($order)->onConnection('deferred');
```



`deferred` 연결은 기본 [페일오버 큐](#queue-failover) 역할도 합니다.

비슷하게, `background` 연결은 HTTP 응답이 사용자에게 전송된 후 작업을 처리합니다. 그러나 작업은 별도로 생성된 PHP 프로세스에서 처리되므로 PHP-FPM / 애플리케이션 워커가 다른 들어오는 HTTP 요청을 처리할 수 있습니다:

```php
RecordDelivery::dispatch($order)->onConnection('background');
```



<a name="bulk-dispatching"></a>
### 대량 디스패치

많은 독립적인 작업을 한 번에 디스패치해야 하고 [배치](#job-batching) 추적이나 콜백이 필요하지 않은 경우, `Bus` 파사드의 `bulk` 메서드를 사용할 수 있습니다. 라라벨은 작업을 구성된 큐 연결 및 큐 이름별로 그룹화하고 각 그룹을 적절한 큐에 대량으로 푸시합니다:

```php
use App\Jobs\ProcessUser;
use Illuminate\Support\Facades\Bus;

Bus::bulk(
    $users->map(fn ($user) => new ProcessUser($user))
);
```



<a name="preparing-jobs-before-dispatch"></a>
### 작업을 디스패치하기 전에 준비하기

작업이 큐에 푸시되기 전에 상태를 준비하거나 점검해야 하는 경우, 작업은 `Illuminate\Contracts\Queue\PreparesForDispatch` 인터페이스를 구현할 수 있습니다. 라라벨은 작업을 디스패치하기 전에 작업의 `prepareForDispatch` 메서드를 호출합니다. 이 메서드가 `false`를 반환하면, 작업은 디스패치되지 않습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\PreparesForDispatch;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Support\Facades\Cache;

class SyncPodcasts implements PreparesForDispatch, ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public array $podcastIds,
    ) {}

    /**
     * Prepare the job before dispatching.
     */
    public function prepareForDispatch(): bool
    {
        return collect($this->podcastIds)
            ->reject(fn (int $id) => Cache::has("podcast-syncing:{$id}"))
            ->isNotEmpty();
    }
}
```



<a name="jobs-and-database-transactions"></a>
### 작업 및 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 작업을 디스패치하는 것이 완전히 괜찮지만, 작업이 실제로 성공적으로 실행될 수 있도록 특별히 주의해야 합니다. 트랜잭션 내에서 작업을 디스패치할 때, 작업이 상위 트랜잭션이 커밋되기 전에 워커에 의해 처리될 가능성이 있습니다. 이렇게 되면, 데이터베이스 트랜잭션 동안 모델이나 데이터베이스 레코드에 수행한 업데이트가 데이터베이스에 아직 반영되지 않았을 수 있습니다. 또한 트랜잭션 내에서 생성된 모델이나 데이터베이스 레코드가 데이터베이스에 존재하지 않을 수도 있습니다.

다행히도, Laravel은 이 문제를 해결할 수 있는 여러 방법을 제공합니다. 먼저, 큐 연결 구성 배열에서 `after_commit` 연결 옵션을 설정할 수 있습니다:

```php
'redis' => [
    'driver' => 'redis',
    // ...
    'after_commit' => true,
],
```



When the `after_commit` option is `true`, you may dispatch jobs within database transactions; however, Laravel will wait until the open parent database transactions have been committed before actually dispatching the job. Of course, if no database transactions are currently open, the job will be dispatched immediately.

If a transaction is rolled back due to an exception that occurs during the transaction, the jobs that were dispatched during that transaction will be discarded.

> [!NOTE]
> Setting the `after_commit` configuration option to `true` will also cause any queued event listeners, mailables, notifications, and broadcast events to be dispatched after all open database transactions have been committed.

<a name="specifying-commit-dispatch-behavior-inline"></a>
#### Specifying Commit Dispatch Behavior Inline

If you do not set the `after_commit` queue connection configuration option to `true`, you may still indicate that a specific job should be dispatched after all open database transactions have been committed. To accomplish this, you may chain the `afterCommit` method onto your dispatch operation:

```php
use App\Jobs\ProcessPodcast;

ProcessPodcast::dispatch($podcast)->afterCommit();
```



마찬가지로, `after_commit` 구성 옵션이 `true`로 설정된 경우, 특정 작업이 대기 중인 데이터베이스 트랜잭션이 커밋되기를 기다리지 않고 즉시 디스패치되어야 함을 나타낼 수 있습니다:

```php
ProcessPodcast::dispatch($podcast)->beforeCommit();
```



<a name="job-chaining"></a>
### 작업 연쇄

작업 연쇄를 사용하면 기본 작업이 성공적으로 실행된 후 순서대로 실행해야 하는 대기 중인 작업 목록을 지정할 수 있습니다. 시퀀스 중 하나의 작업이 실패하면 나머지 작업은 실행되지 않습니다. 대기 중인 작업 체인을 실행하려면 `Bus` 퍼사드에서 제공하는 `chain` 메서드를 사용할 수 있습니다. Laravel의 커맨드 버스는 대기 중인 작업 디스패치가 구축되는 하위 수준 구성 요소입니다:

```php
use App\Jobs\OptimizePodcast;
use App\Jobs\ProcessPodcast;
use App\Jobs\ReleasePodcast;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->dispatch();
```



잡 클래스 인스턴스를 연결하는 것 외에도, 클로저를 연결할 수도 있습니다:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    function () {
        Podcast::update(/* ... */);
    },
])->dispatch();
```



> [!WARNING]
> 작업 내에서 `$this->delete()` 메서드를 사용하여 작업을 삭제해도 연결된 작업이 처리되는 것은 방지되지 않습니다. 체인은 체인 내의 작업이 실패할 경우에만 실행이 중지됩니다.

<a name="chain-connection-queue"></a>
#### 체인 연결 및 큐

연결된 작업에 사용할 연결 및 큐를 지정하려면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 이러한 메서드는 큐에 들어간 작업이 명시적으로 다른 연결/큐로 지정되지 않는 한 사용해야 하는 큐 연결과 큐 이름을 지정합니다:

```php
Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->onConnection('redis')->onQueue('podcasts')->dispatch();
```



<a name="adding-jobs-to-the-chain"></a>
#### 체인에 작업 추가하기

때때로, 체인 내 다른 작업에서 기존 작업 체인에 작업을 앞쪽이나 뒤쪽에 추가해야 할 필요가 있습니다. 이는 `prependToChain`와 `appendToChain` 메서드를 사용하여 수행할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    // Prepend to the current chain, run job immediately after current job...
    $this->prependToChain(new TranscribePodcast);

    // Append to the current chain, run job at end of chain...
    $this->appendToChain(new TranscribePodcast);
}
```



<a name="chain-failures"></a>
#### 체인 실패

작업을 체인할 때, 체인 내의 작업이 실패할 경우 호출될 클로저를 지정하기 위해 `catch` 방법을 사용할 수 있습니다. 주어진 콜백은 작업 실패를 일으킨 `Throwable` 인스턴스를 받게 됩니다:

```php
use Illuminate\Support\Facades\Bus;
use Throwable;

Bus::chain([
    new ProcessPodcast,
    new OptimizePodcast,
    new ReleasePodcast,
])->catch(function (Throwable $e) {
    // A job within the chain has failed...
})->dispatch();
```



> [!WARNING]
> 체인 콜백은 직렬화되어 나중에 Laravel 큐에 의해 실행되므로, 체인 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="customizing-the-queue-and-connection"></a>
### 큐 및 연결 사용자 정의

<a name="dispatching-to-a-particular-queue"></a>
#### 특정 큐에 디스패치하기

잡을 다른 큐로 푸시함으로써, 큐에 넣은 잡을 "분류"하고 다양한 큐에 할당하는 워커 수를 우선순위로 지정할 수도 있습니다. 이는 큐 설정 파일에 정의된 다른 큐 "연결"로 잡을 푸시하는 것이 아니라, 단일 연결 내의 특정 큐에만 푸시한다는 점을 명심하세요. 큐를 지정하려면 잡을 디스패치할 때 `onQueue` 메서드를 사용하십시오:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onQueue('processing');

        return redirect('/podcasts');
    }
}
```



또는 작업의 생성자 내에서 `onQueue` 메서드를 호출하여 작업의 큐를 지정할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct()
    {
        $this->onQueue('processing');
    }
}
```



<a name="dispatching-to-a-particular-connection"></a>
#### 특정 연결로 디스패치하기

애플리케이션이 여러 큐 연결과 상호 작용하는 경우, `onConnection` 메서드를 사용하여 작업을 보낼 연결을 지정할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Jobs\ProcessPodcast;
use App\Models\Podcast;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PodcastController extends Controller
{
    /**
     * Store a new podcast.
     */
    public function store(Request $request): RedirectResponse
    {
        $podcast = Podcast::create(/* ... */);

        // Create podcast...

        ProcessPodcast::dispatch($podcast)->onConnection('sqs');

        return redirect('/podcasts');
    }
}
```



`onConnection`와 `onQueue` 메서드를 연쇄하여 작업의 연결과 큐를 지정할 수 있습니다:

```php
ProcessPodcast::dispatch($podcast)
    ->onConnection('sqs')
    ->onQueue('processing');
```



또는 작업의 생성자 내에서 `onConnection` 메서드를 호출하여 작업의 연결을 지정할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct()
    {
        $this->onConnection('sqs');
    }
}
```



<a name="queue-routing"></a>
#### 큐 라우팅

특정 작업 클래스에 대해 기본 연결과 큐를 정의하려면 `Queue` 퍼사드의 `route` 메서드를 사용할 수 있습니다. 이는 특정 작업이 항상 특정 큐를 사용하도록 보장하고자 할 때, 작업에서 연결이나 큐를 지정할 필요 없이 유용합니다.

특정 작업 클래스를 라우팅하는 것 외에도, `route` 메서드에 인터페이스, 트레이트 또는 부모 클래스도 전달할 수 있습니다. 이렇게 하면, 인터페이스를 구현하거나, 트레이트를 사용하거나, 부모 클래스를 확장하는 모든 작업이 자동으로 설정된 연결과 큐를 사용하게 됩니다.

일반적으로, 서비스 제공자의 `boot` 메서드에서 `route` 메서드를 호출해야 합니다:

```php
use App\Concerns\RequiresVideo;
use App\Jobs\ProcessPodcast;
use App\Jobs\ProcessVideo;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');
    Queue::route(RequiresVideo::class, queue: 'video');
    Queue::route(ShouldBroadcast::class, queue: 'events');
}
```



연결이 큐 없이 지정되면 작업은 기본 큐로 전송됩니다:

```php
Queue::route(ProcessPodcast::class, connection: 'redis');
```



배열을 `route` 메서드에 전달하여 여러 작업 클래스를 한 번에 라우팅할 수도 있습니다:

```php
Queue::route([
    ProcessPodcast::class => ['redis', 'podcasts'], // Connection and queue
    ProcessVideo::class => 'videos', // Queue only (uses default connection)
]);
```



> [!NOTE]
> 큐 라우팅은 여전히 작업별로 개별 작업에 의해 재정의될 수 있습니다.

`forward` 방법을 사용하여 작업을 한 큐에서 다른 큐 및/또는 연결로 전달할 수 있습니다. 이는 개별 작업이나 디스패치 위치를 수정하지 않고 큐 인프라를 변경해야 할 때 유용합니다:

```php
Queue::forward('reports', 'reports.fifo', 'sqs');
Queue::forward('payments', connection: 'sqs');
Queue::forward('updates', 'notifications');
```



배열을 전달하여 여러 대기열을 한 번에 전달할 수도 있습니다:

```php
Queue::forward([
    'reports' => 'reports.fifo',
    'emails' => 'emails.fifo',
], connection: 'sqs');
```



An explicit connection configured on a job takes precedence over a forwarded connection.

<a name="max-job-attempts-and-timeout"></a>
### Specifying Max Job Attempts / Timeout Values

<a name="max-attempts"></a>
#### Max Attempts

Job attempts are a core concept of Laravel's queue system and power many advanced features. While they may seem confusing at first, it's important to understand how they work before modifying the default configuration.

When a job is dispatched, it is pushed onto the queue. A worker then picks it up and attempts to execute it. This is a job attempt.

However, an attempt does not necessarily mean the job's `handle` method was executed. Attempts can also be "consumed" in several ways:

<div class="content-list" markdown="1">

- The job encounters an unhandled exception during execution.
- The job is manually released back to the queue using `$this->release()`.
- Middleware such as `WithoutOverlapping` or `RateLimited` fails to acquire a lock and releases the job.
- The job timed out.
- The job's `handle` method runs and completes without throwing an exception.

</div>

You likely do not want to keep attempting a job indefinitely. Therefore, Laravel provides various ways to specify how many times or for how long a job may be attempted.

> [!NOTE]
> By default, Laravel will only attempt a job once. If your job uses middleware like `WithoutOverlapping` or `RateLimited`, or if you're manually releasing jobs, you will likely need to increase the number of allowed attempts via the `tries` option.

One approach to specifying the maximum number of times a job may be attempted is via the `--tries` switch on the Artisan command line. This will apply to all jobs processed by the worker unless the job being processed specifies the number of times it may be attempted:

```shell
php artisan queue:work --tries=3
```



작업이 최대 시도 횟수를 초과하면 해당 작업은 "실패한" 작업으로 간주됩니다. 실패한 작업 처리에 대한 자세한 내용은 [실패한 작업 문서](#dealing-with-failed-jobs)를 참조하십시오. `queue:work` 명령에 `--tries=0`가 제공되면 작업은 무기한 재시도됩니다.

작업 클래스 자체에서 `Tries` 속성을 사용하여 작업이 시도될 수 있는 최대 횟수를 정의함으로써 보다 세분화된 접근 방식을 취할 수 있습니다. 작업에서 최대 시도 횟수가 지정된 경우 명령줄에서 제공된 `--tries` 값보다 우선합니다.

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Tries;

#[Tries(5)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```



특정 작업의 최대 시도 횟수에 대해 동적으로 제어해야 하는 경우, 작업에 `tries` 메서드를 정의할 수 있습니다:

```php
/**
 * Determine number of times the job may be attempted.
 */
public function tries(): int
{
    return 5;
}
```



<a name="time-based-attempts"></a>
#### 시간 기반 시도

작업이 실패하기 전에 몇 번 시도될 수 있는지를 정의하는 대신, 작업을 더 이상 시도하지 말아야 하는 시간을 정의할 수 있습니다. 이를 통해 주어진 시간 내에 작업을 아무 횟수나 시도할 수 있습니다. 작업을 더 이상 시도하지 말아야 하는 시간을 정의하려면, 작업 클래스에 `retryUntil` 메서드를 추가하십시오. 이 메서드는 `DateTime` 인스턴스를 반환해야 합니다:

```php
use DateTime;

/**
 * Determine the time at which the job should timeout.
 */
public function retryUntil(): DateTime
{
    return now()->plus(minutes: 10);
}
```



만약 `retryUntil`와 `tries`가 모두 정의되어 있으면, Laravel은 `retryUntil` 메서드를 우선시합니다.

> [!NOTE]
> 또한 [대기열 이벤트 리스너](/docs/{{version}}/events#queued-event-listeners)와 [대기열 알림](/docs/{{version}}/notifications#queueing-notifications)에 `Tries` 속성이나 `retryUntil` 메서드를 정의할 수도 있습니다.

<a name="max-exceptions"></a>
#### 최대 예외

때로는 작업이 여러 번 시도될 수 있도록 지정하되, 특정 횟수의 처리되지 않은 예외로 인해 재시도가 발생하면 실패하도록 지정하고 싶을 때가 있습니다(직접 `release` 메서드로 릴리스된 경우와 반대로). 이를 수행하기 위해 작업 클래스에서 `Tries` 및 `MaxExceptions` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\MaxExceptions;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Support\Facades\Redis;

#[Tries(25)]
#[MaxExceptions(3)]
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Redis::throttle('key')->allow(10)->every(60)->then(function () {
            // Lock obtained, process the podcast...
        }, function () {
            // Unable to obtain lock...
            return $this->release(10);
        });
    }
}
```



이 예제에서, 애플리케이션이 Redis 락을 얻지 못하면 작업은 10초 동안 해제되며 최대 25회까지 계속 재시도됩니다. 그러나 작업 중 세 번의 처리되지 않은 예외가 발생하면 작업은 실패합니다.

<a name="stopping-retries-by-exception"></a>
#### 예외로 재시도 중지

때때로 예외는 큐에 있는 작업이 다시 시도되기보다는 즉시 실패해야 함을 나타낼 수 있습니다. 애플리케이션의 `bootstrap/app.php` 파일에서 `dontRetry` 예외 메서드를 사용하여 작업 재시도를 중단해야 하는 예외 유형을 구성할 수 있습니다:

```php
use App\Exceptions\InvalidPodcastSourceException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetry([
        InvalidPodcastSourceException::class,
    ]);
})
```



재시도가 언제 중단되어야 하는지에 대해 더 많은 제어가 필요하다면, `dontRetryWhen` 메서드에 클로저를 제공할 수 있습니다. 클로저가 `true`를 반환하면 작업은 실패로 표시되며 재시도되지 않습니다:

```php
use App\Exceptions\PodcastProcessingException;
use Illuminate\Foundation\Configuration\Exceptions;

->withExceptions(function (Exceptions $exceptions): void {
    $exceptions->dontRetryWhen(function (PodcastProcessingException $e) {
        return $e->reason() === 'Subscription expired';
    });
})
```



<a name="timeout"></a>
#### 타임아웃

종종, 대기 중인 작업이 얼마나 걸릴지 대략 알고 있습니다. 이런 이유로, Laravel은 "timeout" 값을 지정할 수 있게 합니다. 기본적으로 타임아웃 값은 60초입니다. 작업이 타임아웃 값으로 지정된 초보다 더 오래 처리될 경우, 해당 작업을 처리하는 워커는 오류와 함께 종료됩니다. 일반적으로, 워커는 [서버에서 설정된 프로세스 관리자](#supervisor-configuration)에 의해 자동으로 재시작됩니다.

작업이 실행될 수 있는 최대 초 수는 Artisan 명령어 라인에서 `--timeout` 스위치를 사용하여 지정할 수 있습니다:

```shell
php artisan queue:work --timeout=30
```



작업이 지속적으로 시간 초과되어 최대 시도를 초과하면 실패한 것으로 표시됩니다.

작업 클래스의 `Timeout` 속성을 사용하여 작업이 실행될 수 있는 최대 시간을 초 단위로 정의할 수도 있습니다. 작업에 시간 제한이 지정된 경우, 명령줄에 지정된 시간 제한보다 우선합니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Timeout;

#[Timeout(120)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```



때때로 소켓이나 아웃고잉 HTTP 연결과 같은 I/O 차단 프로세스는 지정한 타임아웃을 존중하지 않을 수 있습니다. 따라서 이러한 기능을 사용할 때에는 항상 해당 API를 통해 타임아웃을 지정하도록 시도해야 합니다. 예를 들어 [Guzzle](https://docs.guzzlephp.org)을 사용할 때에는 항상 연결 및 요청 타임아웃 값을 지정해야 합니다.

> [!WARNING]
> 작업 타임아웃을 지정하려면 [PCNTL](https://www.php.net/manual/en/book.pcntl.php) PHP 확장 모듈이 설치되어 있어야 합니다. 또한 작업의 'timeout' 값은 항상 ['retry after'](#job-expiration) 값보다 작아야 합니다. 그렇지 않으면 작업이 실제로 실행을 완료하거나 타임아웃되기 전에 다시 시도될 수 있습니다. `--timeout` 옵션은 `queue:work` 명령이 `--once` 옵션과 함께 호출될 때는 효과가 없습니다.

<a name="failing-on-timeout"></a>
#### 타임아웃 시 실패 처리

타임아웃 시 작업을 [실패](#dealing-with-failed-jobs)로 표시하고 싶다면, 작업 클래스에서 `FailOnTimeout` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\FailOnTimeout;

#[FailOnTimeout]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```



> [!NOTE]
> 기본적으로, 작업이 시간 초과되면 시도 횟수 하나를 소모하고 다시 큐로 반환됩니다(재시도가 허용되는 경우). 그러나 시간 초과 시 작업이 실패하도록 구성하면, 시도 횟수와 관계없이 재시도되지 않습니다.

<a name="sqs-fifo-and-fair-queues"></a>
### SQS FIFO 및 공정 큐

Laravel은 [Amazon SQS FIFO (First-In-First-Out)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fifo-queues.html) 및 [공정](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html) 큐를 지원합니다. FIFO 큐를 사용하면 작업이 전송된 정확한 순서대로 처리되며, 메시지 중복 제거를 통해 정확히 한 번만 처리됨을 보장합니다.

FIFO 큐는 어떤 작업을 병렬로 처리할 수 있을지 결정하기 위해 메시지 그룹 ID가 필요합니다. 동일한 그룹 ID를 가진 작업은 순차적으로 처리되며, 다른 그룹 ID를 가진 메시지는 동시에 처리될 수 있습니다.

Laravel은 작업을 디스패치할 때 메시지 그룹 ID를 지정하기 위해 유창한 `onGroup` 메서드를 제공합니다:

```php
ProcessOrder::dispatch($order)
    ->onGroup("customer-{$order->customer_id}");
```



작업을 SQS FIFO 큐에 메시지 그룹을 지정하지 않고 전송하면, Laravel은 큐 이름을 메시지 그룹 ID로 사용합니다.

SQS FIFO 큐는 정확히 한 번만 처리되도록 메시지 중복 제거를 지원합니다. 작업 클래스에 `deduplicationId` 메서드를 구현하여 사용자 지정 중복 제거 ID를 제공하세요:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessSubscriptionRenewal implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's deduplication ID.
     */
    public function deduplicationId(): string
    {
        return "renewal-{$this->subscription->id}";
    }
}
```



<a name="fair-queues"></a>
#### 공정 큐

표준 SQS 큐를 사용 중인 경우, 메시지 그룹을 설정하면 공정 큐잉이 가능합니다. 즉, 그룹을 할당하면 SQS가 이를 사용하여 테넌트/워크로드 간 공정한 전달을 유지합니다. 추가적인 Laravel 구성은 필요하지 않습니다.

`onGroup`를 디스패치 시점에 호출하는 대신, 작업(Job) 클래스에 `messageGroup` 메서드를 직접 정의할 수도 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ProcessOrder implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return "customer-{$this->order->customer_id}";
    }
}
```



<a name="fifo-listeners-mail-and-notifications"></a>
#### FIFO 리스너, 메일 및 알림

FIFO 큐를 사용할 때, 리스너, 메일 및 알림에서 메시지 그룹을 정의해야 합니다. 또는 이러한 객체의 큐된 인스턴스를 비-FIFO 큐로 전송할 수도 있습니다.

[큐 이벤트 리스너](/docs/{{version}}/events#queued-event-listeners)의 메시지 그룹을 정의하려면, 리스너에서 `messageGroup` 메서드를 정의하십시오. 선택적으로 `deduplicationId` 메서드를 정의할 수도 있습니다:

```php
<?php

namespace App\Listeners;

class SendShipmentNotification
{
    // ...

    /**
     * Get the job's message group.
     */
    public function messageGroup(): string
    {
        return 'shipments';
    }

    /**
     * Get the job's deduplication ID.
     */
    public function deduplicationId(): string
    {
        return "shipment-notification-{$this->shipment->id}";
    }
}
```



FIFO 큐에 대기될 [메일 메시지](/docs/{{version}}/mail)를 보낼 때는 알림을 보낼 때 `onGroup` 메서드를 호출하고 선택적으로 `withDeduplicator` 메서드를 호출해야 합니다:

```php
use App\Mail\InvoicePaid;
use Illuminate\Support\Facades\Mail;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

Mail::to($request->user())->send($invoicePaid);
```



FIFO 큐에 대기열로 추가될 [알림](/docs/{{version}}/notifications)을 보낼 때, 알림을 보낼 때 `onGroup` 메서드를 호출하고 필요에 따라 `withDeduplicator` 메서드를 선택적으로 호출해야 합니다:

```php
use App\Notifications\InvoicePaid;

$invoicePaid = (new InvoicePaid($invoice))
    ->onGroup('invoices')
    ->withDeduplicator(fn () => 'invoices-'.$invoice->id);

$user->notify($invoicePaid);
```



<a name="queue-failover"></a>
### 큐 장애 조치

`failover` 큐 드라이버는 작업을 큐에 푸시할 때 자동 장애 조치 기능을 제공합니다. `failover` 구성의 기본 큐 연결이 어떤 이유로든 실패하면, Laravel은 자동으로 리스트에 지정된 다음 구성된 연결로 작업을 푸시하려고 시도합니다. 이는 큐 안정성이 중요한 프로덕션 환경에서 고가용성을 보장하는 데 특히 유용합니다.

장애 조치 큐 연결을 구성하려면 `failover` 드라이버를 지정하고 시도할 연결 이름의 배열을 제공하십시오. 기본적으로 Laravel은 애플리케이션의 `config/queue.php` 구성 파일에 예제 장애 조치 구성을 포함합니다:

```php
'failover' => [
    'driver' => 'failover',
    'connections' => [
        'redis',
        'database',
        'sync',
    ],
],
```



`failover` 드라이버를 사용하는 연결을 구성한 후에는 페일오버 기능을 사용하려면 애플리케이션의 `.env` 파일에서 페일오버 연결을 기본 큐 연결로 설정해야 합니다:

```ini
QUEUE_CONNECTION=failover
```



다음으로, 장애 조치(connection) 목록에 있는 각 연결마다 최소 한 명의 작업자를 시작하세요:

```shell
php artisan queue:work redis
php artisan queue:work database
```



> [!NOTE]
> You do not need to run a worker for connections using the `sync`, `background`, or `deferred` queue drivers since those drivers process jobs within the current PHP process.

When a queue connection operation fails and failover is activated, Laravel will dispatch the `Illuminate\Queue\Events\QueueFailedOver` event, allowing you to report or log that a queue connection has failed.

> [!NOTE]
> If you use Laravel Horizon, remember that Horizon manages Redis queues only. If your failover list includes `database`, you should run a regular `php artisan queue:work database` process alongside Horizon.

<a name="error-handling"></a>
### Error Handling

If an exception is thrown while the job is being processed, the job will automatically be released back onto the queue so it may be attempted again. The job will continue to be released until it has been attempted the maximum number of times allowed by your application. The maximum number of attempts is defined by the `--tries` switch used on the `queue:work` Artisan command. Alternatively, the maximum number of attempts may be defined on the job class itself. More information on running the queue worker [can be found below](#running-the-queue-worker).

<a name="manually-releasing-a-job"></a>
#### Manually Releasing a Job

Sometimes you may wish to manually release a job back onto the queue so that it can be attempted again at a later time. You may accomplish this by calling the `release` method:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->release();
}
```



기본적으로 `release` 메서드는 작업을 즉시 처리할 수 있도록 큐에 다시 반환합니다. 그러나 `release` 메서드에 정수나 날짜 인스턴스를 전달하여 특정 시간(초)이 경과할 때까지 큐가 작업을 처리할 수 없도록 지시할 수 있습니다:

```php
$this->release(10);

$this->release(now()->plus(seconds: 10));
```



<a name="manually-failing-a-job"></a>
#### 작업 수동 실패 처리

가끔 작업을 수동으로 "실패"로 표시해야 할 때가 있습니다. 이렇게 하려면 `fail` 메서드를 호출할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    // ...

    $this->fail();
}
```



잡을 잡은 예외 때문에 실패한 것으로 표시하고 싶다면, 예외를 `fail` 메서드에 전달할 수 있습니다. 또는 편의를 위해 문자열 오류 메시지를 전달하면, 해당 메시지가 예외로 변환됩니다:

```php
$this->fail($exception);

$this->fail('Something went wrong.');
```



> [!NOTE]
> 실패한 작업에 대한 자세한 정보는 [작업 실패 처리에 대한 문서](#dealing-with-failed-jobs)를 참조하세요.

<a name="fail-jobs-on-exceptions"></a>
#### 특정 예외에서 작업 실패

`FailOnException` [작업 미들웨어](#job-middleware)는 특정 예외가 발생할 때 재시도를 건너뛸 수 있게 해줍니다. 이를 통해 외부 API 오류와 같은 일시적인 예외에서는 재시도할 수 있지만, 사용자의 권한이 철회되는 것과 같은 지속적인 예외에서는 작업을 영구적으로 실패하게 할 수 있습니다:

```php
<?php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Auth\Access\AuthorizationException;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Illuminate\Queue\Attributes\Tries;
use Illuminate\Queue\Middleware\FailOnException;
use Illuminate\Support\Facades\Http;

#[Tries(3)]
class SyncChatHistory implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public User $user,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $this->user->authorize('sync-chat-history');

        $response = Http::throw()->get(
            "https://chat.laravel.test/?user={$this->user->uuid}"
        );

        // ...
    }

    /**
     * Get the middleware the job should pass through.
     */
    public function middleware(): array
    {
        return [
            new FailOnException([AuthorizationException::class])
        ];
    }
}
```



<a name="job-batching"></a>
## 작업 배치

Laravel의 작업 배치 기능을 사용하면 여러 작업을 병렬로 쉽게 실행한 후, 작업 배치가 실행을 완료했을 때 일부 작업을 수행할 수 있습니다.

시작하기 전에, 작업 배치에 대한 메타 정보를 포함할 테이블을 생성할 데이터베이스 마이그레이션을 만들어야 합니다. 예를 들어 완료 비율과 같은 정보를 포함할 수 있습니다. 이 마이그레이션은 `make:queue-batches-table` Artisan 명령을 사용하여 생성할 수 있습니다:

```shell
php artisan make:queue-batches-table

php artisan migrate
```



<a name="defining-batchable-jobs"></a>
### 일괄 처리 가능한 작업 정의

일괄 처리 가능한 작업을 정의하려면 일반적으로 [큐 가능한 작업을 생성](#creating-jobs)하면 됩니다. 그러나 작업 클래스에 `Illuminate\Bus\Batchable` 특성을 추가해야 합니다. 이 특성은 작업이 실행 중인 현재 배치를 가져오는 데 사용할 수 있는 `batch` 메서드에 대한 접근을 제공합니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Bus\Batchable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportCsv implements ShouldQueue
{
    use Batchable, Queueable;

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            // Determine if the batch has been cancelled...

            return;
        }

        // Import a portion of the CSV file...
    }
}
```



<a name="dispatching-batches"></a>
### 배치 전송

작업 배치를 전송하려면 `Bus` 퍼사드의 `batch` 메서드를 사용해야 합니다. 물론, 배치 처리 방식은 주로 완료 콜백과 결합될 때 유용합니다. 따라서 `then`, `catch`, `finally` 메서드를 사용하여 배치에 대한 완료 콜백을 정의할 수 있습니다. 이들 각 콜백은 호출될 때 `Illuminate\Bus\Batch` 인스턴스를 받게 됩니다.

여러 큐 워커를 실행하면, 배치의 작업들은 병렬로 처리됩니다. 따라서 작업 완료 순서는 배치에 추가된 순서와 동일하지 않을 수 있습니다. 순차적으로 작업을 실행하는 방법에 대한 정보는 [작업 체인 및 배치](#chains-and-batches) 문서를 참조하십시오.

이 예제에서는 CSV 파일에서 지정된 행 수를 처리하는 작업 배치를 큐에 넣는 상황을 가정해 보겠습니다:

```php
use App\Jobs\ImportCsv;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;
use Throwable;

$batch = Bus::batch([
    new ImportCsv(1, 100),
    new ImportCsv(101, 200),
    new ImportCsv(201, 300),
    new ImportCsv(301, 400),
    new ImportCsv(401, 500),
])->before(function (Batch $batch) {
    // The batch has been created but no jobs have been added...
})->progress(function (Batch $batch) {
    // A single job has completed successfully...
})->then(function (Batch $batch) {
    // All jobs completed successfully...
})->catch(function (Batch $batch, Throwable $e) {
    // Batch job failure detected...
})->finally(function (Batch $batch) {
    // The batch has finished executing...
})->dispatch();

return $batch->id;
```



배치 ID는 `$batch->id` 속성을 통해 접근할 수 있으며, 배치가 디스패치된 후에는 [Laravel 커맨드 버스](#inspecting-batches)를 통해 배치에 대한 정보를 조회하는 데 사용할 수 있습니다.

> [!WARNING]
> 배치 콜백은 직렬화되어 나중에 Laravel 큐에서 실행되므로, 콜백 내에서 `$this` 변수를 사용하면 안 됩니다. 또한, 배치된 작업은 데이터베이스 트랜잭션 내에 래핑되므로, 암시적 커밋을 트리거하는 데이터베이스 명령문은 작업 내에서 실행해서는 안 됩니다.

<a name="naming-batches"></a>
#### 배치 이름 지정

[Laravel Horizon](/docs/{{version}}/horizon)이나 [Laravel Telescope](/docs/{{version}}/telescope)와 같은 일부 도구는 배치에 이름을 지정하면 배치에 대한 더 사용자 친화적인 디버그 정보를 제공할 수 있습니다. 배치에 임의의 이름을 지정하려면, 배치를 정의할 때 `name` 메서드를 호출하면 됩니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import CSV')->dispatch();
```



<a name="batch-connection-queue"></a>
#### 배치 연결 및 큐

배치 작업에 사용될 연결과 큐를 지정하고자 한다면 `onConnection` 및 `onQueue` 메서드를 사용할 수 있습니다. 모든 배치 작업은 동일한 연결과 큐 내에서 실행되어야 합니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->onConnection('redis')->onQueue('imports')->dispatch();
```



<a name="chains-and-batches"></a>
### 체인과 배치

배치 내에서 [연쇄 작업](#job-chaining) 세트를 배열 안에 연쇄 작업을 배치하여 정의할 수 있습니다. 예를 들어, 두 개의 작업 체인을 병렬로 실행하고 두 작업 체인이 모두 처리 완료되면 콜백을 실행할 수 있습니다:

```php
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

Bus::batch([
    [
        new ReleasePodcast(1),
        new SendPodcastReleaseNotification(1),
    ],
    [
        new ReleasePodcast(2),
        new SendPodcastReleaseNotification(2),
    ],
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->dispatch();
```



반대로, 체인([chain](#job-chaining)) 내에서 배치를 정의하여 배치 작업을 실행할 수 있습니다. 예를 들어, 먼저 여러 팟캐스트를 공개하기 위한 배치 작업을 실행한 다음, 공개 알림을 보내기 위한 배치 작업을 실행할 수 있습니다:

```php
use App\Jobs\FlushPodcastCache;
use App\Jobs\ReleasePodcast;
use App\Jobs\SendPodcastReleaseNotification;
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new FlushPodcastCache,
    Bus::batch([
        new ReleasePodcast(1),
        new ReleasePodcast(2),
    ]),
    Bus::batch([
        new SendPodcastReleaseNotification(1),
        new SendPodcastReleaseNotification(2),
    ]),
])->dispatch();
```



<a name="adding-jobs-to-batches"></a>
### 배치에 작업 추가하기

때때로 배치 작업 내에서 추가 작업을 배치에 추가하는 것이 유용할 수 있습니다. 이 패턴은 웹 요청 중에 디스패치하기에는 너무 오래 걸릴 수 있는 수천 개의 작업을 배치해야 할 때 유용할 수 있습니다. 대신, 초기 '로더' 작업 배치를 디스패치하여 배치를 더 많은 작업으로 채우도록 할 수 있습니다:

```php
$batch = Bus::batch([
    new LoadImportBatch,
    new LoadImportBatch,
    new LoadImportBatch,
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->name('Import Contacts')->dispatch();
```



이 예제에서는 `LoadImportBatch` 작업을 사용하여 배치를 추가 작업으로 채울 것입니다. 이를 달성하기 위해, 우리는 작업의 `batch` 메서드를 통해 접근할 수 있는 배치 인스턴스에서 `add` 메서드를 사용할 수 있습니다:

```php
use App\Jobs\ImportContacts;
use Illuminate\Support\Collection;

/**
 * Execute the job.
 */
public function handle(): void
{
    if ($this->batch()->cancelled()) {
        return;
    }

    $this->batch()->add(Collection::times(1000, function () {
        return new ImportContacts;
    }));
}
```



> [!WARNING]
> 동일한 배치에 속한 작업 내에서만 배치에 작업을 추가할 수 있습니다.

<a name="inspecting-batches"></a>
### 배치 검사

배치 완료 콜백에 제공되는 `Illuminate\Bus\Batch` 인스턴스에는 주어진 작업 배치를 상호작용하고 검사하는 데 도움이 되는 다양한 속성과 메서드가 있습니다:

```php
// The UUID of the batch...
$batch->id;

// The name of the batch (if applicable)...
$batch->name;

// The number of jobs assigned to the batch...
$batch->totalJobs;

// The number of jobs that have not been processed by the queue...
$batch->pendingJobs;

// The number of jobs that have failed...
$batch->failedJobs;

// The number of jobs that have been processed thus far...
$batch->processedJobs();

// The completion percentage of the batch (0-100)...
$batch->progress();

// Indicates if the batch has finished executing...
$batch->finished();

// Cancel the execution of the batch...
$batch->cancel();

// Indicates if the batch has been cancelled...
$batch->cancelled();
```



<a name="returning-batches-from-routes"></a>
#### 경로에서 배치 반환

모든 `Illuminate\Bus\Batch` 인스턴스는 JSON 직렬화가 가능하므로, 애플리케이션의 경로 중 하나에서 직접 반환하여 배치에 대한 정보를 포함한 JSON 페이로드를 가져올 수 있습니다. 여기에는 완료 진행 상황도 포함됩니다. 이를 통해 애플리케이션 UI에서 배치 완료 진행 상황 정보를 편리하게 표시할 수 있습니다.

배치를 ID로 검색하려면 `Bus` 퍼사드의 `findBatch` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Bus;
use Illuminate\Support\Facades\Route;

Route::get('/batch/{batchId}', function (string $batchId) {
    return Bus::findBatch($batchId);
});
```



<a name="cancelling-batches"></a>
### 배치 취소

때때로 특정 배치의 실행을 취소해야 할 때가 있습니다. 이는 `Illuminate\Bus\Batch` 인스턴스에서 `cancel` 메서드를 호출하여 수행할 수 있습니다:

```php
/**
 * Execute the job.
 */
public function handle(): void
{
    if ($this->user->exceedsImportLimit()) {
        $this->batch()->cancel();

        return;
    }

    if ($this->batch()->cancelled()) {
        return;
    }
}
```



이전 예제에서 알 수 있듯이, 배치 작업은 일반적으로 해당 배치가 취소되었는지 여부를 확인한 후 실행을 계속해야 합니다. 그러나 편의를 위해, 대신 `SkipIfBatchCancelled` [미들웨어](#job-middleware)를 작업에 할당할 수 있습니다. 이름에서 알 수 있듯이, 이 미들웨어는 해당 배치가 취소된 경우 Laravel이 작업을 처리하지 않도록 지시합니다:

```php
use Illuminate\Queue\Middleware\SkipIfBatchCancelled;

/**
 * Get the middleware the job should pass through.
 */
public function middleware(): array
{
    return [new SkipIfBatchCancelled];
}
```



<a name="batch-failures"></a>
### 배치 실패

배치 작업이 실패하면, `catch` 콜백(할당된 경우)이 호출됩니다. 이 콜백은 배치 내에서 처음 실패한 작업에 대해서만 호출됩니다.

<a name="allowing-failures"></a>
#### 실패 허용

배치 내 작업이 실패하면, Laravel은 자동으로 해당 배치를 "취소됨"으로 표시합니다. 원한다면, 작업 실패가 배치를 자동으로 취소된 것으로 표시하지 않도록 이 동작을 비활성화할 수 있습니다. 이는 배치를 디스패치하는 동안 `allowFailures` 메소드를 호출하여 수행할 수 있습니다:

```php
$batch = Bus::batch([
    // ...
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->allowFailures()->dispatch();
```



각 작업 실패 시 실행될 `allowFailures` 메서드에 대해 선택적으로 클로저를 제공할 수 있습니다:

```php
$batch = Bus::batch([
    // ...
])->allowFailures(function (Batch $batch, $exception) {
    // Handle individual job failures...
})->dispatch();
```



<a name="retrying-failed-batch-jobs"></a>
#### 실패한 배치 작업 재시도

편의를 위해, Laravel은 주어진 배치의 모든 실패한 작업을 쉽게 재시도할 수 있는 `queue:retry-batch` Artisan 명령어를 제공합니다. 이 명령어는 실패한 작업을 재시도해야 하는 배치의 UUID를 받습니다:

```shell
php artisan queue:retry-batch 32dbc76c-4f82-4749-b610-a639fe0099b5
```



<a name="pruning-batches"></a>
### 배치 가지치기

가지치기 없이 `job_batches` 테이블은 매우 빠르게 레코드를 축적할 수 있습니다. 이를 완화하기 위해, `queue:prune-batches` Artisan 명령을 매일 실행되도록 [예약](/docs/{{version}}/scheduling)해야 합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches')->daily();
```



기본적으로, 완료된 모든 배치는 24시간 이상 지난 경우 제거됩니다. 명령을 호출할 때 `hours` 옵션을 사용하여 배치 데이터를 보관할 기간을 지정할 수 있습니다. 예를 들어, 다음 명령은 48시간 이상 지난 모든 완료된 배치를 삭제합니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48')->daily();
```



때때로, `job_batches` 테이블에는 성공적으로 완료되지 않은 배치의 배치 기록이 쌓일 수 있습니다. 예를 들어, 작업이 실패했지만 해당 작업이 성공적으로 재시도되지 않은 배치가 이에 해당됩니다. `queue:prune-batches` 명령에 `unfinished` 옵션을 사용하여 이러한 완료되지 않은 배치 기록을 정리하도록 지시할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --unfinished=72')->daily();
```



마찬가지로, 귀하의 `job_batches` 테이블도 취소된 배치에 대한 배치 기록을 축적할 수 있습니다. `queue:prune-batches` 명령어를 사용하여 `cancelled` 옵션을 통해 이러한 취소된 배치 기록을 정리하도록 지시할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('queue:prune-batches --hours=48 --cancelled=72')->daily();
```



<a name="storing-batches-in-dynamodb"></a>
### Storing Batches in DynamoDB

Laravel also provides support for storing batch meta information in [DynamoDB](https://aws.amazon.com/dynamodb) instead of a relational database. However, you will need to manually create a DynamoDB table to store all of the batch records.

Typically, this table should be named `job_batches`, but you should name the table based on the value of the `queue.batching.table` configuration value within your application's `queue` configuration file.

<a name="dynamodb-batch-table-configuration"></a>
#### DynamoDB Batch Table Configuration

The `job_batches` table should have a string primary partition key named `application` and a string primary sort key named `id`. The `application` portion of the key will contain your application's name as defined by the `name` configuration value within your application's `app` configuration file. Since the application name is part of the DynamoDB table's key, you can use the same table to store job batches for multiple Laravel applications.

In addition, you may define `ttl` attribute for your table if you would like to take advantage of [automatic batch pruning](#pruning-batches-in-dynamodb).

<a name="dynamodb-configuration"></a>
#### DynamoDB Configuration

Next, install the AWS SDK so that your Laravel application can communicate with Amazon DynamoDB:

```shell
composer require aws/aws-sdk-php
```



그런 다음, `queue.batching.driver` 구성 옵션의 값을 `dynamodb`로 설정하십시오. 또한, `batching` 구성 배열 내에서 `key`, `secret` 및 `region` 구성 옵션을 정의해야 합니다. 이 옵션들은 AWS와 인증하는 데 사용됩니다. `dynamodb` 드라이버를 사용할 때는 `queue.batching.database` 구성 옵션이 필요하지 않습니다:

```php
'batching' => [
    'driver' => env('QUEUE_BATCHING_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
],
```



<a name="pruning-batches-in-dynamodb"></a>
#### DynamoDB에서 배치 가지치기

[job 배치 정보](https://aws.amazon.com/dynamodb)를 저장하기 위해 [DynamoDB](https://aws.amazon.com/dynamodb)를 사용할 때, 관계형 데이터베이스에서 배치를 가지치기 위해 일반적으로 사용하는 가지치기 명령은 작동하지 않습니다. 대신, [DynamoDB의 기본 TTL 기능](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)을 사용하여 오래된 배치 레코드를 자동으로 제거할 수 있습니다.

DynamoDB 테이블을 `ttl` 속성으로 정의한 경우, Laravel이 배치 레코드를 어떻게 가지치기할지 지시하는 구성 매개변수를 정의할 수 있습니다. `queue.batching.ttl_attribute` 구성 값은 TTL을 보유하는 속성의 이름을 정의하며, `queue.batching.ttl` 구성 값은 레코드가 마지막으로 업데이트된 시점을 기준으로 배치 레코드를 DynamoDB 테이블에서 제거할 수 있을 때까지의 초 수를 정의합니다:

```php
'batching' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'job_batches',
    'ttl_attribute' => 'ttl',
    'ttl' => 60 * 60 * 24 * 7, // 7 days...
],
```



<a name="queueing-closures"></a>
## 클로저 큐잉

큐에 작업 클래스를 디스패치하는 대신, 클로저를 디스패치할 수도 있습니다. 이는 현재 요청 주기 외부에서 실행되어야 하는 빠르고 간단한 작업에 적합합니다. 클로저를 큐에 디스패치할 때, 클로저의 코드 내용은 전송 중에 수정될 수 없도록 암호화 서명이 적용됩니다:

```php
use App\Models\Podcast;

$podcast = Podcast::find(1);

dispatch(function () use ($podcast) {
    $podcast->publish();
});
```



큐 보고 대시보드에서 사용되거나 `queue:work` 명령으로 표시될 수 있는 대기 중인 클로저에 이름을 지정하려면, `name` 방법을 사용할 수 있습니다:

```php
dispatch(function () {
    // ...
})->name('Publish Podcast');
```



`catch` 방법을 사용하여, 대기 중인 클로저가 큐에 설정된 [재시도 시도](#max-job-attempts-and-timeout)를 모두 소모한 후에도 완료되지 않을 경우 실행되어야 하는 클로저를 제공할 수 있습니다:

```php
use Throwable;

dispatch(function () use ($podcast) {
    $podcast->publish();
})->catch(function (Throwable $e) {
    // This job has failed...
});
```



> [!WARNING]
> `catch` 콜백은 직렬화되어 나중에 Laravel 큐에 의해 실행되므로, `catch` 콜백 내에서 `$this` 변수를 사용해서는 안 됩니다.

<a name="running-the-queue-worker"></a>
## 큐 워커 실행

<a name="the-queue-work-command"></a>
### `queue:work` 명령어

Laravel에는 큐 워커를 시작하고 큐에 푸시된 새 작업을 처리하는 Artisan 명령어가 포함되어 있습니다. 워커는 `queue:work` Artisan 명령어를 사용하여 실행할 수 있습니다. `queue:work` 명령어가 시작되면 수동으로 중지하거나 터미널을 닫을 때까지 계속 실행됩니다:

```shell
php artisan queue:work
```



> [!NOTE]
> `queue:work` 프로세스를 백그라운드에서 영구적으로 실행 상태로 유지하려면 [Supervisor](#supervisor-configuration)와 같은 프로세스 모니터를 사용하여 큐 작업자가 실행을 멈추지 않도록 해야 합니다.

처리된 작업 ID, 연결 이름 및 큐 이름을 명령 출력에 포함시키고 싶다면 `queue:work` 명령을 호출할 때 `-v` 플래그를 포함할 수 있습니다:

```shell
php artisan queue:work -v
```



기억하세요, 큐 워커(queue workers)는 장기 실행 프로세스이며 부팅된 애플리케이션 상태를 메모리에 저장합니다. 그 결과, 시작된 후에는 코드베이스의 변경 사항을 인식하지 못합니다. 따라서 배포 프로세스 중에는 반드시 [큐 워커를 재시작](#queue-workers-and-deployment)해야 합니다. 또한 애플리케이션에 의해 생성되거나 수정된 모든 정적 상태는 작업 간 자동으로 재설정되지 않는다는 점을 기억하세요.

또는 `queue:listen` 명령을 실행할 수 있습니다. `queue:listen` 명령을 사용할 때 업데이트된 코드를 다시 로드하거나 애플리케이션 상태를 재설정하고 싶을 때 워커를 수동으로 재시작할 필요가 없습니다; 그러나 이 명령은 `queue:work` 명령보다 효율성이 현저히 낮습니다.

```shell
php artisan queue:listen
```



<a name="running-multiple-queue-workers"></a>
#### 여러 큐 워커 실행하기

큐에 여러 워커를 할당하고 작업을 동시에 처리하려면, 단순히 여러 `queue:work` 프로세스를 시작하면 됩니다. 이는 터미널에서 여러 탭을 통해 로컬로 수행할 수 있거나, 프로덕션 환경에서는 프로세스 관리자의 설정을 통해 수행할 수 있습니다. [Supervisor를 사용할 경우](#supervisor-configuration), `numprocs` 설정 값을 사용할 수 있습니다.

<a name="specifying-the-connection-queue"></a>
#### 연결 및 큐 지정하기

워커가 사용할 큐 연결을 지정할 수도 있습니다. `work` 명령어에 전달된 연결 이름은 `config/queue.php` 설정 파일에 정의된 연결 중 하나와 일치해야 합니다:

```shell
php artisan queue:work redis
```



기본적으로 `queue:work` 명령은 특정 연결에서 기본 큐의 작업만 처리합니다. 그러나 특정 연결에서 특정 큐만 처리하도록 큐 작업자를 더욱 맞춤 설정할 수도 있습니다. 예를 들어, 모든 이메일이 `redis` 큐 연결에서 `emails` 큐로 처리되는 경우, 해당 큐만 처리하는 작업자를 시작하려면 다음 명령을 실행할 수 있습니다:

```shell
php artisan queue:work redis --queue=emails
```



<a name="processing-a-specified-number-of-jobs"></a>
#### 지정된 수의 작업 처리

`--once` 옵션은 작업자가 큐에서 단일 작업만 처리하도록 지시하는 데 사용될 수 있습니다:

```shell
php artisan queue:work --once
```



`--max-jobs` 옵션은 작업자가 지정된 수의 작업을 처리한 후 종료하도록 지시하는 데 사용할 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 결합하면 유용할 수 있으며, 작업자가 지정된 수의 작업을 처리한 후 자동으로 재시작되어 축적된 메모리를 해제하게 됩니다:

```shell
php artisan queue:work --max-jobs=1000
```



<a name="processing-all-queued-jobs-then-exiting"></a>
#### 모든 대기 중인 작업을 처리한 후 종료

`--stop-when-empty` 옵션은 작업자를 지시하여 모든 작업을 처리한 후 정상적으로 종료하도록 할 때 사용할 수 있습니다. 이 옵션은 큐가 비워진 후 컨테이너를 종료하려는 경우 Docker 컨테이너 내에서 Laravel 큐를 처리할 때 유용할 수 있습니다:

```shell
php artisan queue:work --stop-when-empty
```



<a name="processing-jobs-for-a-given-number-of-seconds"></a>
#### 주어진 시간(초) 동안 작업 처리하기

`--max-time` 옵션은 워커에게 주어진 시간(초) 동안 작업을 처리한 후 종료하도록 지시하는 데 사용될 수 있습니다. 이 옵션은 [Supervisor](#supervisor-configuration)와 함께 사용하면 유용할 수 있습니다. 이렇게 하면 워커가 일정 시간 동안 작업을 처리한 후 자동으로 다시 시작되어 쌓인 메모리를 해제할 수 있습니다:

```shell
# Process jobs for one hour and then exit...
php artisan queue:work --max-time=3600
```



<a name="worker-sleep-duration"></a>
#### 작업자 대기 시간

큐에 작업이 있는 경우, 작업자는 작업 사이에 지연 없이 계속 작업을 처리합니다. 그러나 `sleep` 옵션은 작업이 없을 때 작업자가 몇 초 동안 "대기"할지를 결정합니다. 물론 대기하는 동안 작업자는 새로운 작업을 처리하지 않습니다:

```shell
php artisan queue:work --sleep=3
```



<a name="maintenance-mode-queues"></a>
#### 유지 관리 모드 및 대기열

애플리케이션이 [유지 관리 모드](/docs/{{version}}/configuration#maintenance-mode)에 있는 동안에는 대기열에 있는 작업이 처리되지 않습니다. 애플리케이션이 유지 관리 모드에서 벗어나면 작업은 정상적으로 처리됩니다.

유지 관리 모드가 활성화되어 있어도 대기열 작업자를 강제로 작업을 처리하게 하려면 `--force` 옵션을 사용할 수 있습니다:

```shell
php artisan queue:work --force
```



<a name="resource-considerations"></a>
#### 자원 고려사항

데몬 큐 작업자는 각 작업을 처리하기 전에 프레임워크를 "재부팅"하지 않습니다. 따라서 각 작업이 완료된 후에는 모든 무거운 자원을 해제해야 합니다. 예를 들어, [GD 라이브러리](https://www.php.net/manual/en/book.image.php)를 사용하여 [이미지 조작](/docs/{{version}}/images)을 수행하는 경우, 이미지 처리 작업이 끝나면 `imagedestroy`로 메모리를 해제해야 합니다.

<a name="queue-priorities"></a>
### 큐 우선순위

때때로 큐 처리 순서를 우선순위로 지정하고 싶을 수 있습니다. 예를 들어, `config/queue.php` 구성 파일에서 `redis` 연결의 기본 `queue`를 `low`로 설정할 수 있습니다. 그러나 가끔 다음과 같이 작업을 `high` 우선순위 큐에 넣고 싶을 수 있습니다:

```php
dispatch((new Job)->onQueue('high'));
```



`work` 명령에 쉼표로 구분된 큐 이름 목록을 전달하여 `low` 큐의 작업을 계속하기 전에 `high` 큐의 모든 작업이 처리되었는지 확인하는 작업자를 시작합니다.

```shell
php artisan queue:work --queue=high,low
```



<a name="queue-workers-and-deployment"></a>
### 큐 워커와 배포

큐 워커는 장기 실행되는 프로세스이기 때문에, 재시작하지 않으면 코드 변경 사항을 감지하지 못합니다. 따라서 큐 워커를 사용하는 애플리케이션을 배포하는 가장 간단한 방법은 배포 과정에서 워커를 재시작하는 것입니다. 다음 `queue:restart` 명령어를 실행하여 모든 워커를 정상적으로 재시작할 수 있습니다:

```shell
php artisan queue:restart
```



This command will instruct all queue workers to gracefully exit after they finish processing their current job so that no existing jobs are lost. Since the queue workers will exit when the `queue:restart` command is executed, you should be running a process manager such as [Supervisor](#supervisor-configuration) to automatically restart the queue workers.

> [!NOTE]
> The queue uses the [cache](/docs/{{version}}/cache) to store restart signals, so you should verify that a cache driver is properly configured for your application before using this feature.

<a name="reacting-to-worker-signals"></a>
### Reacting to Worker Signals

When a queue worker receives a termination signal such as `SIGQUIT`, `SIGTERM`, or `SIGINT` while processing a job, the worker will finish its current job before exiting. However, your job may need to react to the signal before the process is stopped by your server or container orchestrator. For example, a long-running import job may need to stop pulling new records and save its current progress.

To react to worker signals from within a job, implement the `Illuminate\Contracts\Queue\Interruptible` interface and define an `interrupted` method on your job. The signal number received by the worker will be passed to the `interrupted` method:

```php
<?php

namespace App\Jobs;

use App\Models\Import;
use Illuminate\Contracts\Queue\Interruptible;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;

class ImportProducts implements ShouldQueue, Interruptible
{
    use Queueable;

    protected bool $shouldStop = false;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Import $import,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        foreach ($this->import->pendingRows() as $row) {
            if ($this->shouldStop) {
                break;
            }

            // Import the product row...
        }

        $this->import->saveProgress();
    }

    /**
     * Handle a signal received by the queue worker.
     */
    public function interrupted(int $signal): void
    {
        $this->shouldStop = true;
    }
}
```



The `interrupted` method is only invoked when the worker receives a process signal while the job is currently running. It is not a replacement for [timeouts](#worker-timeouts) or the job's [`failed` method](#cleaning-up-after-failed-jobs).

<a name="job-expirations-and-timeouts"></a>
### Job Expirations and Timeouts

<a name="job-expiration"></a>
#### Job Expiration

In your `config/queue.php` configuration file, each queue connection defines a `retry_after` option. This option specifies how many seconds the queue connection should wait before retrying a job that is being processed. For example, if the value of `retry_after` is set to `90`, the job will be released back onto the queue if it has been processing for 90 seconds without being released or deleted. Typically, you should set the `retry_after` value to the maximum number of seconds your jobs should reasonably take to complete processing.

> [!WARNING]
> The only queue connection which does not contain a `retry_after` value is Amazon SQS. SQS will retry the job based on the [Default Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/AboutVT.html) which is managed within the AWS console.

<a name="worker-timeouts"></a>
#### Worker Timeouts

The `queue:work` Artisan command exposes a `--timeout` option. By default, the `--timeout` value is 60 seconds. If a job is processing for longer than the number of seconds specified by the timeout value, the worker processing the job will exit with an error. Typically, the worker will be restarted automatically by a [process manager configured on your server](#supervisor-configuration):

```shell
php artisan queue:work --timeout=60
```



`retry_after` 구성 옵션과 `--timeout` CLI 옵션은 다르지만, 작업이 손실되지 않고 작업이 한 번만 성공적으로 처리되도록 함께 작동합니다.

> [!WARNING]
> `--timeout` 값은 항상 `retry_after` 구성 값보다 최소 몇 초 정도 짧아야 합니다. 이는 중단된 작업을 처리하는 작업자가 작업이 재시도되기 전에 항상 종료되도록 보장합니다. `--timeout` 옵션이 `retry_after` 구성 값보다 길면 작업이 두 번 처리될 수 있습니다.

<a name="pausing-and-resuming-queue-workers"></a>
### 큐 작업자 일시 중지 및 재개

때로는 큐 작업자를 완전히 중지하지 않고 새로운 작업 처리를 일시적으로 방지해야 할 때가 있습니다. 예를 들어 시스템 유지 관리 중에 작업 처리를 일시 중지할 수 있습니다. Laravel은 큐 작업자를 일시 중지하고 재개할 수 있는 `queue:pause` 및 `queue:continue` Artisan 명령어를 제공합니다.

특정 큐를 일시 중지하려면 큐 연결 이름과 큐 이름을 제공하십시오:

```shell
php artisan queue:pause database:default
```



이 예제에서 `database`는 큐 연결 이름이고 `default`는 큐 이름입니다. 큐가 일시 중지되면 해당 큐에서 작업을 처리하는 작업자들은 현재 작업을 끝까지 처리하지만, 큐가 다시 시작될 때까지 새 작업을 가져오지 않습니다.

모든 연결의 모든 큐에서 작업 처리 일시 중지를 하려면 `--all` 옵션을 사용하십시오:

```shell
php artisan queue:pause --all
```



일시 중지된 큐에서 작업 처리를 다시 시작하려면 `queue:continue` 명령을 사용하세요:

```shell
php artisan queue:continue database:default
```



모든 연결의 모든 큐에 대한 작업 처리를 재개하려면 `queue:resume` 명령과 함께 `--all` 옵션을 사용하십시오:

```shell
php artisan queue:resume --all
```



큐를 다시 시작하면 작업자는 해당 큐에서 새로운 작업을 즉시 처리하기 시작합니다. 모든 큐를 다시 시작한다고 해서 개별적으로 일시 중지된 큐가 다시 시작되는 것은 아닙니다. 큐 일시 중지가 작업자 프로세스 자체를 중단시키는 것은 아니며, 단지 지정된 큐에서 작업자가 새로운 작업을 처리하지 못하게 할 뿐입니다.

<a name="worker-restart-and-pause-signals"></a>
#### 작업자 재시작 및 일시 중지 신호

기본적으로, 큐 작업자는 각 작업 반복에서 재시작 및 일시 중지 신호를 위해 캐시 드라이버를 폴링합니다. 이러한 폴링은 `queue:restart` 및 `queue:pause` 명령에 응답하는 데 필수적이지만, 약간의 성능 오버헤드를 발생시킬 수 있습니다.

성능을 최적화해야 하고 이러한 중단 기능이 필요하지 않은 경우, `Queue` 파사드에서 `withoutInterruptionPolling` 메서드를 호출하여 이 폴링을 전역적으로 비활성화할 수 있습니다. 일반적으로 이는 `AppServiceProvider`의 `boot` 메서드에서 수행해야 합니다.

```php
use Illuminate\Support\Facades\Queue;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Queue::withoutInterruptionPolling();
}
```



또는 `Illuminate\Queue\Worker` 클래스에서 정적 `$restartable` 또는 `$pausable` 속성을 설정하여 재시작 또는 폴링 일시 중지를 개별적으로 비활성화할 수 있습니다:

```php
use Illuminate\Queue\Worker;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Worker::$restartable = false;
    Worker::$pausable = false;
}
```



> [!WARNING]
> When interruption polling is disabled, workers will not respond to `queue:restart` or `queue:pause` commands (depending on which features are disabled).

<a name="supervisor-configuration"></a>
## Supervisor Configuration

In production, you need a way to keep your `queue:work` processes running. A `queue:work` process may stop running for a variety of reasons, such as an exceeded worker timeout or the execution of the `queue:restart` command.

For this reason, you need to configure a process monitor that can detect when your `queue:work` processes exit and automatically restart them. In addition, process monitors can allow you to specify how many `queue:work` processes you would like to run concurrently. Supervisor is a process monitor commonly used in Linux environments and we will discuss how to configure it in the following documentation.

<a name="installing-supervisor"></a>
#### Installing Supervisor

Supervisor is a process monitor for the Linux operating system, and will automatically restart your `queue:work` processes if they fail. To install Supervisor on Ubuntu, you may use the following command:

```shell
sudo apt-get install supervisor
```



> [!NOTE]
> 직접 Supervisor를 구성하고 관리하는 것이 부담스럽게 느껴진다면, Laravel 큐 작업자를 실행하기 위한 완전 관리 플랫폼을 제공하는 [Laravel Cloud](https://cloud.laravel.com)를 사용하는 것을 고려해 보세요.

<a name="configuring-supervisor"></a>
#### Supervisor 구성하기

Supervisor 구성 파일은 일반적으로 `/etc/supervisor/conf.d` 디렉토리에 저장됩니다. 이 디렉토리 내에서 Supervisor가 프로세스를 어떻게 모니터링할지를 지시하는 여러 구성 파일을 생성할 수 있습니다. 예를 들어, `queue:work` 프로세스를 시작하고 모니터링하는 `laravel-worker.conf` 파일을 생성해 보겠습니다:

```ini
[program:laravel-worker]
process_name=%(program_name)s_%(process_num)02d
command=php /home/forge/app.com/artisan queue:work --sleep=3 --tries=3 --max-time=3600
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
user=forge
numprocs=8
redirect_stderr=true
stdout_logfile=/home/forge/app.com/worker.log
stopwaitsecs=3600
```



이 예제에서, `numprocs` 지시문은 Supervisor에게 8개의 `queue:work` 프로세스를 실행하고 모두 모니터링하도록 지시하며, 실패할 경우 자동으로 재시작합니다. 원하는 큐 연결 및 작업자 옵션을 반영하도록 구성의 `command` 지시문을 변경해야 합니다.

> [!WARNING]
> `stopwaitsecs` 값이 가장 오래 실행되는 작업에 소요되는 시간(초)보다 큰지 확인해야 합니다. 그렇지 않으면 Supervisor가 작업을 완료하기 전에 종료할 수 있습니다.

<a name="starting-supervisor"></a>
#### Supervisor 시작하기

구성 파일이 생성되면, 다음 명령어를 사용하여 Supervisor 구성을 업데이트하고 프로세스를 시작할 수 있습니다:

```shell
sudo supervisorctl reread

sudo supervisorctl update

sudo supervisorctl start "laravel-worker:*"
```



Supervisor에 대한 자세한 정보는 [Supervisor 문서](http://supervisord.org/index.html)를 참조하세요.

<a name="dealing-with-failed-jobs"></a>
## 실패한 작업 처리

때때로 대기열에 있는 작업이 실패할 수 있습니다. 걱정하지 마세요, 계획대로 항상 진행되는 것은 아닙니다! Laravel은 작업이 시도될 최대 횟수를 [지정할 수 있는 편리한 방법](#max-job-attempts-and-timeout)을 포함하고 있습니다. 비동기 작업이 이 시도 횟수를 초과하면 `failed_jobs` 데이터베이스 테이블에 삽입됩니다. 실패한 [동기식 디스패치 작업](/docs/{{version}}/queues#synchronous-dispatching)은 이 테이블에 저장되지 않고 예외는 즉시 애플리케이션에 의해 처리됩니다.

`failed_jobs` 테이블을 생성하는 마이그레이션은 일반적으로 새로운 Laravel 애플리케이션에 이미 존재합니다. 그러나 애플리케이션에 이 테이블에 대한 마이그레이션이 없는 경우, `make:queue-failed-table` 명령을 사용하여 마이그레이션을 생성할 수 있습니다:

```shell
php artisan make:queue-failed-table

php artisan migrate
```



[큐 작업자](#running-the-queue-worker) 프로세스를 실행할 때, `queue:work` 명령의 `--tries` 스위치를 사용하여 작업을 시도할 최대 횟수를 지정할 수 있습니다. `--tries` 옵션에 대한 값을 지정하지 않으면, 작업은 한 번만 시도되거나 작업 클래스의 `Tries` 속성에 지정된 횟수만큼 시도됩니다:

```shell
php artisan queue:work redis --tries=3
```



`--backoff` 옵션을 사용하여, 예외가 발생한 작업을 재시도하기 전에 Laravel이 대기할 초를 지정할 수 있습니다. 기본적으로 작업은 즉시 큐로 다시 반환되어 다시 시도될 수 있습니다:

```shell
php artisan queue:work redis --tries=3 --backoff=3
```



개별 작업별로 예외가 발생한 작업을 재시도하기 전에 Laravel이 몇 초를 기다려야 하는지 구성하려면, 작업 클래스에서 `Backoff` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Backoff;

#[Backoff(3)]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```



작업의 백오프 시간을 결정하기 위해 더 복잡한 로직이 필요한 경우, 작업 클래스에 `backoff` 메서드를 정의할 수 있습니다:

```php
/**
 * Calculate the number of seconds to wait before retrying the job.
 */
public function backoff(): int
{
    return 3;
}
```



백오프 값을 배열로 정의하여 "지수적" 백오프를 쉽게 구성할 수 있습니다. 이 예제에서는 재시도 지연 시간이 첫 번째 재시도는 1초, 두 번째 재시도는 5초, 세 번째 재시도는 10초이며, 만약 남은 시도가 더 있으면 이후의 모든 재시도는 10초가 됩니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\Backoff;

#[Backoff([1, 5, 10])]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```



<a name="cleaning-up-after-failed-jobs"></a>
### 실패한 작업 후 정리

특정 작업이 실패할 경우, 사용자에게 알림을 보내거나 작업이 부분적으로 완료한 작업을 되돌리고 싶을 수 있습니다. 이를 수행하기 위해, 작업 클래스에 `failed` 메서드를 정의할 수 있습니다. 작업을 실패하게 한 `Throwable` 인스턴스가 `failed` 메서드에 전달됩니다:

```php
<?php

namespace App\Jobs;

use App\Models\Podcast;
use App\Services\AudioProcessor;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Queue\Queueable;
use Throwable;

class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    /**
     * Create a new job instance.
     */
    public function __construct(
        public Podcast $podcast,
    ) {}

    /**
     * Execute the job.
     */
    public function handle(AudioProcessor $processor): void
    {
        // Process uploaded podcast...
    }

    /**
     * Handle a job failure.
     */
    public function failed(?Throwable $exception): void
    {
        // Send user notification of failure, etc...
    }
}
```



> [!WARNING]
> A new instance of the job is instantiated before invoking the `failed` method; therefore, any class property modifications that may have occurred within the `handle` method will be lost.

A failed job is not necessarily one that encountered an unhandled exception. A job may also be considered failed when it has exhausted all of its allowed attempts. These attempts can be consumed in several ways:

<div class="content-list" markdown="1">

- The job timed out.
- The job encounters an unhandled exception during execution.
- The job is released back to the queue either manually or by a middleware.

</div>

If the final attempt fails due to an exception thrown during job execution, that exception will be passed to the job's `failed` method. However, if the job fails because it has reached the maximum number of allowed attempts, the `$exception` will be an instance of `Illuminate\Queue\MaxAttemptsExceededException`. Similarly, if the job fails due to exceeding the configured timeout, the `$exception` will be an instance of `Illuminate\Queue\TimeoutExceededException`.

<a name="retrying-failed-jobs"></a>
### Retrying Failed Jobs

To view all of the failed jobs that have been inserted into your `failed_jobs` database table, you may use the `queue:failed` Artisan command:

```shell
php artisan queue:failed
```



`queue:failed` 명령은 작업 ID, 연결, 큐, 실패 시간 및 작업에 대한 기타 정보를 나열합니다. 작업 ID는 실패한 작업을 다시 시도하는 데 사용할 수 있습니다. 예를 들어, ID가 `ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece`인 실패한 작업을 다시 시도하려면 다음 명령을 실행하십시오:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece
```



필요한 경우, 명령어에 여러 개의 ID를 전달할 수 있습니다:

```shell
php artisan queue:retry ce7bb17c-cdd8-41f0-a8ec-7b4fef4e5ece 91401d2c-0784-4f43-824c-34f94a33c24d
```



특정 큐에 대해 실패한 모든 작업을 다시 시도할 수도 있습니다:

```shell
php artisan queue:retry --queue=name
```



실패한 모든 작업을 다시 시도하려면 `queue:retry` 명령을 실행하고 ID로 `all`를 전달하세요:

```shell
php artisan queue:retry all
```



실패한 작업을 삭제하려면 `queue:forget` 명령을 사용할 수 있습니다:

```shell
php artisan queue:forget 91401d2c-0784-4f43-824c-34f94a33c24d
```



> [!NOTE]
> [Horizon](/docs/{{version}}/horizon)을 사용할 때, 실패한 작업을 삭제하려면 `queue:forget` 명령 대신 `horizon:forget` 명령을 사용해야 합니다.

`failed_jobs` 테이블에서 모든 실패한 작업을 삭제하려면 `queue:flush` 명령을 사용할 수 있습니다:

```shell
php artisan queue:flush
```



`queue:flush` 명령은 실패한 작업이 얼마나 오래되었든 상관없이 큐에서 모든 실패한 작업 기록을 제거합니다. `--hours` 옵션을 사용하면 특정 시간 이상 전에 실패한 작업만 삭제할 수 있습니다:

```shell
php artisan queue:flush --hours=48
```



<a name="ignoring-missing-models"></a>
### 누락된 모델 무시하기

Eloquent 모델을 작업에 주입할 때, 모델은 큐에 배치되기 전에 자동으로 직렬화되며, 작업이 처리될 때 데이터베이스에서 다시 가져옵니다. 그러나 작업이 워커에 의해 처리되기 위해 대기하는 동안 모델이 삭제된 경우, 작업이 `ModelNotFoundException` 오류로 실패할 수 있습니다.

편의를 위해, 작업 클래스에서 `DeleteWhenMissingModels` 속성을 사용하여 누락된 모델이 있는 작업을 자동으로 삭제하도록 선택할 수 있습니다. 이 속성이 존재하면, Laravel은 예외를 발생시키지 않고 조용히 작업을 버립니다:

```php
<?php

namespace App\Jobs;

use Illuminate\Queue\Attributes\DeleteWhenMissingModels;

#[DeleteWhenMissingModels]
class ProcessPodcast implements ShouldQueue
{
    // ...
}
```



<a name="pruning-failed-jobs"></a>
### 실패한 작업 제거

애플리케이션의 `failed_jobs` 테이블에서 레코드를 제거하려면 `queue:prune-failed` Artisan 명령어를 실행하세요:

```shell
php artisan queue:prune-failed
```



기본적으로 24시간 이상된 모든 실패한 작업 기록은 삭제됩니다. 명령어에 `--hours` 옵션을 제공하면, 마지막 N시간 내에 삽입된 실패한 작업 기록만 보존됩니다. 예를 들어, 다음 명령어는 48시간 이상 전에 삽입된 모든 실패한 작업 기록을 삭제합니다:

```shell
php artisan queue:prune-failed --hours=48
```



<a name="storing-failed-jobs-in-dynamodb"></a>
### Storing Failed Jobs in DynamoDB

Laravel also provides support for storing your failed job records in [DynamoDB](https://aws.amazon.com/dynamodb) instead of a relational database table. However, you must manually create a DynamoDB table to store all of the failed job records. Typically, this table should be named `failed_jobs`, but you should name the table based on the value of the `queue.failed.table` configuration value within your application's `queue` configuration file.

The `failed_jobs` table should have a string primary partition key named `application` and a string primary sort key named `uuid`. The `application` portion of the key will contain your application's name as defined by the `name` configuration value within your application's `app` configuration file. Since the application name is part of the DynamoDB table's key, you can use the same table to store failed jobs for multiple Laravel applications.

In addition, ensure that you install the AWS SDK so that your Laravel application can communicate with Amazon DynamoDB:

```shell
composer require aws/aws-sdk-php
```



다음으로, `queue.failed.driver` 구성 옵션의 값을 `dynamodb`로 설정하십시오. 또한, 실패한 작업 구성 배열 내에서 `key`, `secret` 및 `region` 구성 옵션을 정의해야 합니다. 이러한 옵션은 AWS에 인증하는 데 사용됩니다. `dynamodb` 드라이버를 사용할 경우, `queue.failed.database` 구성 옵션은 필요하지 않습니다:

```php
'failed' => [
    'driver' => env('QUEUE_FAILED_DRIVER', 'dynamodb'),
    'key' => env('AWS_ACCESS_KEY_ID'),
    'secret' => env('AWS_SECRET_ACCESS_KEY'),
    'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    'table' => 'failed_jobs',
],
```



<a name="disabling-failed-job-storage"></a>
### 실패한 작업 저장 비활성화

Laravel이 실패한 작업을 저장하지 않고 폐기하도록 지시하려면 `queue.failed.driver` 구성 옵션의 값을 `null`로 설정하면 됩니다. 일반적으로 이는 `QUEUE_FAILED_DRIVER` 환경 변수를 통해 수행할 수 있습니다:

```ini
QUEUE_FAILED_DRIVER=null
```



<a name="failed-job-events"></a>
### 실패한 작업 이벤트

작업이 실패할 때 호출될 이벤트 리스너를 등록하고 싶다면, `Queue` 파사드의 `failing` 메서드를 사용할 수 있습니다. 예를 들어, 우리는 Laravel에 포함된 `AppServiceProvider`의 `boot` 메서드에서 이 이벤트에 클로저를 첨부할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobFailed;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Queue::failing(function (JobFailed $event) {
            // $event->connectionName
            // $event->job
            // $event->exception
        });
    }
}
```



<a name="clearing-jobs-from-queues"></a>
## 큐에서 작업 삭제

> [!NOTE]
> [Horizon](/docs/{{version}}/horizon)을 사용할 때, `queue:clear` 명령 대신 `horizon:clear` 명령을 사용하여 큐에서 작업을 삭제해야 합니다.

기본 연결의 기본 큐에서 모든 작업을 삭제하려면, 다음 `queue:clear` Artisan 명령을 사용할 수 있습니다:

```shell
php artisan queue:clear
```



특정 연결 및 큐에서 작업을 삭제하려면 `connection` 인수와 `queue` 옵션을 제공할 수도 있습니다:

```shell
php artisan queue:clear redis --queue=emails
```



> [!WARNING]
> 큐에서 작업을 삭제하는 것은 SQS, Redis 및 데이터베이스 큐 드라이버에서만 사용할 수 있습니다. 또한, SQS 메시지 삭제 과정은 최대 60초가 걸리므로, 큐를 비운 후 60초 이내에 SQS 큐로 전송된 작업도 삭제될 수 있습니다.

<a name="monitoring-your-queues"></a>
## 큐 모니터링

큐에 갑작스러운 작업이 들어오면 큐가 과부하되어 작업 완료까지 시간이 오래 걸릴 수 있습니다. 원하면, Laravel은 큐 작업 수가 지정된 임계값을 초과할 때 알림을 보낼 수 있습니다.

시작하려면, `queue:monitor` 명령을 [매분 실행](/docs/{{version}}/scheduling)하도록 스케줄링해야 합니다. 이 명령은 모니터링하려는 큐의 이름과 원하는 작업 수 임계값을 인수로 받습니다:

```shell
php artisan queue:monitor redis:default,redis:deployments --max=100
```



이 명령만 예약하는 것으로는 큐가 과부하 상태임을 알리는 알림을 트리거하기에 충분하지 않습니다. 명령이 귀하의 임계값을 초과하는 작업 수를 가진 큐를 만나면 `Illuminate\Queue\Events\QueueBusy` 이벤트가 전송됩니다. 이 이벤트를 애플리케이션의 `AppServiceProvider` 내에서 수신하여 귀하 또는 개발 팀에게 알림을 보낼 수 있습니다:

```php
use App\Notifications\QueueHasLongWaitTime;
use Illuminate\Queue\Events\QueueBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (QueueBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new QueueHasLongWaitTime(
                $event->connectionName,
                $event->queue,
                $event->size
            ));
    });
}
```



<a name="testing"></a>
## 테스트

작업을 전송하는 코드를 테스트할 때, Laravel이 실제로 작업을 실행하지 않도록 지시할 수 있습니다. 왜냐하면 작업의 코드는 전송 코드를 별도로 직접 테스트할 수 있기 때문입니다. 물론, 작업 자체를 테스트하려면 테스트에서 작업 인스턴스를 생성하고 `handle` 메서드를 직접 호출할 수 있습니다.

`Queue` 파사드의 `fake` 메서드를 사용하여 큐 작업이 실제로 큐에 푸시되는 것을 방지할 수 있습니다. `Queue` 파사드의 `fake` 메서드를 호출한 후에는 애플리케이션이 작업을 큐에 푸시하려고 시도했는지 검증할 수 있습니다:```php tab=Pest
<?php

use App\Jobs\AnotherJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;

test('orders can be shipped', function () {
    Queue::fake();

    // Perform order shipping...

    // Assert that no jobs were pushed...
    Queue::assertNothingPushed();

    // Assert a job was pushed to a given queue...
    Queue::assertPushedOn('queue-name', ShipOrder::class);

    // Assert a job was pushed
    Queue::assertPushed(ShipOrder::class);

    // Assert a job was pushed exactly once...
    Queue::assertPushedOnce(ShipOrder::class);

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);

    // Assert a job was not pushed...
    Queue::assertNotPushed(AnotherJob::class);

    // Assert that a closure was pushed to the queue...
    Queue::assertClosurePushed();

    // Assert that a closure was not pushed...
    Queue::assertClosureNotPushed();

    // Assert the total number of jobs that were pushed...
    Queue::assertCount(3);
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use App\Jobs\AnotherJob;
use App\Jobs\ShipOrder;
use Illuminate\Support\Facades\Queue;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_orders_can_be_shipped(): void
    {
        Queue::fake();

        // Perform order shipping...

        // Assert that no jobs were pushed...
        Queue::assertNothingPushed();

        // Assert a job was pushed to a given queue...
        Queue::assertPushedOn('queue-name', ShipOrder::class);

        // Assert a job was pushed
        Queue::assertPushed(ShipOrder::class);

        // Assert a job was pushed exactly once...
        Queue::assertPushedOnce(ShipOrder::class);

        // Assert a job was pushed twice...
        Queue::assertPushedTimes(ShipOrder::class, 2);

        // Assert a job was not pushed...
        Queue::assertNotPushed(AnotherJob::class);

        // Assert that a closure was pushed to the queue...
        Queue::assertClosurePushed();

        // Assert that a closure was not pushed...
        Queue::assertClosureNotPushed();

        // Assert the total number of jobs that were pushed...
        Queue::assertCount(3);
    }
}
```



주어진 '진리 테스트'를 통과하는 작업이 푸시되었음을 주장하기 위해 `assertPushed`, `assertNotPushed`, `assertClosurePushed` 또는 `assertClosureNotPushed` 메서드에 클로저를 전달할 수 있습니다. 주어진 진리 테스트를 통과하는 작업이 최소한 하나라도 푸시되면 주장은 성공하게 됩니다:

```php
use Illuminate\Queue\CallQueuedClosure;

Queue::assertPushed(function (ShipOrder $job) use ($order) {
    return $job->order->id === $order->id;
});

Queue::assertClosurePushed(function (CallQueuedClosure $job) {
    return $job->name === 'validate-order';
});
```



<a name="faking-a-subset-of-jobs"></a>
### 일부 작업 위조하기

다른 작업은 정상적으로 실행되도록 하면서 특정 작업만 위조해야 하는 경우, 위조해야 하는 작업의 클래스 이름을 `fake` 메서드에 전달할 수 있습니다:```php tab=Pest
test('orders can be shipped', function () {
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);
});
```

```php tab=PHPUnit
public function test_orders_can_be_shipped(): void
{
    Queue::fake([
        ShipOrder::class,
    ]);

    // Perform order shipping...

    // Assert a job was pushed twice...
    Queue::assertPushedTimes(ShipOrder::class, 2);
}
```



`except` 방법을 사용하여 지정된 일부 직업을 제외한 모든 직업을 속일 수 있습니다:

```php
Queue::fake()->except([
    ShipOrder::class,
]);
```



<a name="testing-job-chains"></a>
### 작업 체인 테스트

작업 체인을 테스트하려면 `Bus` 퍼사드의 가짜 기능을 활용해야 합니다. `Bus` 퍼사드의 `assertChained` 메서드는 [작업 체인](/docs/{{version}}/queues#job-chaining)이 발송되었는지를 확인하는 데 사용될 수 있습니다. `assertChained` 메서드는 연결된 작업 배열을 첫 번째 인수로 받습니다:

```php
use App\Jobs\RecordShipment;
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertChained([
    ShipOrder::class,
    RecordShipment::class,
    UpdateInventory::class
]);
```



위의 예에서 볼 수 있듯이, 체인된 작업 배열은 작업의 클래스 이름 배열일 수 있습니다. 그러나 실제 작업 인스턴스 배열을 제공할 수도 있습니다. 이렇게 하면 Laravel은 작업 인스턴스가 동일한 클래스에 속하며, 애플리케이션에서 디스패치한 체인된 작업과 동일한 속성 값을 가지도록 보장합니다:

```php
Bus::assertChained([
    new ShipOrder,
    new RecordShipment,
    new UpdateInventory,
]);
```



작업이 일련의 작업 없이 푸시되었음을 주장하기 위해 `assertDispatchedWithoutChain` 방법을 사용할 수 있습니다:

```php
Bus::assertDispatchedWithoutChain(ShipOrder::class);
```



<a name="testing-chain-modifications"></a>
#### 체인 수정 테스트

연결된 작업이 [기존 체인에 작업을 추가하거나 삽입](#adding-jobs-to-the-chain)하는 경우, 작업의 `assertHasChain` 메서드를 사용하여 작업이 예상되는 나머지 작업 체인을 가지고 있는지 확인할 수 있습니다:

```php
$job = new ProcessPodcast;

$job->handle();

$job->assertHasChain([
    new TranscribePodcast,
    new OptimizePodcast,
    new ReleasePodcast,
]);
```



`assertDoesntHaveChain` 방법은 작업의 남은 체인이 비어 있음을 주장하는 데 사용할 수 있습니다:

```php
$job->assertDoesntHaveChain();
```



<a name="testing-chained-batches"></a>
#### 연쇄 배치 테스트

작업 체인에 [작업 배치가 포함된 경우](#chains-and-batches), 체인 검증 내에 `Bus::chainedBatch` 정의를 삽입하여 연쇄 배치가 예상과 일치하는지 확인할 수 있습니다:

```php
use App\Jobs\ShipOrder;
use App\Jobs\UpdateInventory;
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::assertChained([
    new ShipOrder,
    Bus::chainedBatch(function (PendingBatch $batch) {
        return $batch->jobs->count() === 3;
    }),
    new UpdateInventory,
]);
```



<a name="testing-job-batches"></a>
### 작업 배치 테스트

`Bus` 퍼사드의 `assertBatched` 메서드는 [작업 배치](/docs/{{version}}/queues#job-batching)가 전송되었는지 확인하는 데 사용할 수 있습니다. `assertBatched` 메서드에 제공된 클로저는 `Illuminate\Bus\PendingBatch`의 인스턴스를 받으며, 이를 사용하여 배치 내의 작업들을 검사할 수 있습니다:

```php
use Illuminate\Bus\PendingBatch;
use Illuminate\Support\Facades\Bus;

Bus::fake();

// ...

Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->name == 'Import CSV' &&
           $batch->jobs->count() === 10;
});
```



`hasJobs` 메서드는 보류 중인 배치에서 배치에 예상된 작업이 포함되어 있는지 확인하는 데 사용할 수 있습니다. 이 메서드는 작업 인스턴스, 클래스 이름 또는 클로저 배열을 허용합니다:

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        new ProcessCsvRow(row: 1),
        new ProcessCsvRow(row: 2),
        new ProcessCsvRow(row: 3),
    ]);
});
```



클로저를 사용할 때, 클로저는 작업 인스턴스를 받게 됩니다. 예상되는 작업 유형은 클로저의 타입 힌트에서 추론됩니다:

```php
Bus::assertBatched(function (PendingBatch $batch) {
    return $batch->hasJobs([
        fn (ProcessCsvRow $job) => $job->row === 1,
        fn (ProcessCsvRow $job) => $job->row === 2,
        fn (ProcessCsvRow $job) => $job->row === 3,
    ]);
});
```



주어진 배치 수가 발송되었음을 주장하기 위해 `assertBatchCount` 방법을 사용할 수 있습니다:

```php
Bus::assertBatchCount(3);
```



배치가 전송되지 않았음을 주장하기 위해 `assertNothingBatched`를 사용할 수 있습니다:

```php
Bus::assertNothingBatched();
```



<a name="testing-job-batch-interaction"></a>
#### 작업 / 배치 상호작용 테스트

또한, 때때로 개별 작업이 그에 속한 배치와 상호작용하는지 테스트해야 할 수도 있습니다. 예를 들어, 작업이 배치의 추가 처리를 취소했는지 테스트해야 할 수도 있습니다. 이를 수행하려면 `withFakeBatch` 메서드를 통해 작업에 가짜 배치를 할당해야 합니다. `withFakeBatch` 메서드는 작업 인스턴스와 가짜 배치를 포함하는 튜플을 반환합니다:

```php
[$job, $batch] = (new ShipOrder)->withFakeBatch();

$job->handle();

$this->assertTrue($batch->cancelled());
$this->assertEmpty($batch->added);
```



<a name="testing-job-queue-interactions"></a>
### 작업 / 큐 상호작용 테스트

때때로, 큐에 있는 작업이 [자신을 큐로 되돌리는지](#manually-releasing-a-job) 테스트해야 할 필요가 있습니다. 또는 작업이 스스로 삭제되는지 테스트해야 할 수도 있습니다. 이러한 큐 상호작용은 작업을 인스턴스화하고 `withFakeQueueInteractions` 메서드를 호출하여 테스트할 수 있습니다.

작업의 큐 상호작용이 가짜로 설정되면, 작업에서 `handle` 메서드를 호출할 수 있습니다. 작업을 호출한 후에는 다양한 검증 메서드를 사용하여 작업의 큐 상호작용을 확인할 수 있습니다:

```php
use App\Exceptions\CorruptedAudioException;
use App\Jobs\ProcessPodcast;

$job = (new ProcessPodcast)->withFakeQueueInteractions();

$job->handle();

$job->assertReleased(delay: 30);
$job->assertDeleted();
$job->assertNotDeleted();
$job->assertFailed();
$job->assertFailedWith(CorruptedAudioException::class);
$job->assertNotFailed();
```



<a name="job-events"></a>
## 작업 이벤트

`Queue` [퍼사드](/docs/{{version}}/facades)에서 `before` 및 `after` 메서드를 사용하면, 대기열에 있는 작업이 처리되기 전이나 후에 실행될 콜백을 지정할 수 있습니다. 이러한 콜백은 추가 로그를 남기거나 대시보드용 통계를 증가시키는 좋은 기회입니다. 일반적으로 이러한 메서드는 [서비스 제공자](/docs/{{version}}/providers)의 `boot` 메서드에서 호출해야 합니다. 예를 들어, Laravel에 포함된 `AppServiceProvider`를 사용할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Queue;
use Illuminate\Support\ServiceProvider;
use Illuminate\Queue\Events\JobProcessed;
use Illuminate\Queue\Events\JobProcessing;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Queue::before(function (JobProcessing $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });

        Queue::after(function (JobProcessed $event) {
            // $event->connectionName
            // $event->job
            // $event->job->payload()
        });
    }
}
```



`Queue` [facade](/docs/{{version}}/facades)에서 `looping` 방법을 사용하면, 작업자가 큐에서 작업을 가져오기 시도하기 전에 실행될 콜백을 지정할 수 있습니다. 예를 들어, 이전에 실패한 작업으로 인해 열려 있는 트랜잭션을 롤백하기 위해 클로저를 등록할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Queue;

Queue::looping(function () {
    while (DB::transactionLevel() > 0) {
        DB::rollBack();
    }
});
```



Laravel은 큐 작업자가 큐에서 작업을 가져올 수 없을 때 `Illuminate\Queue\Events\WorkerIdle` 이벤트도 발송합니다:

```php
use Illuminate\Queue\Events\WorkerIdle;
use Illuminate\Support\Facades\Event;

Event::listen(function (WorkerIdle $event) {
    // $event->connectionName
    // $event->queue
    // $event->workerOptions
});
```
{% endraw %}
