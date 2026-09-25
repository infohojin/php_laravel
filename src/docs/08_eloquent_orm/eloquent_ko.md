---
layout: docs
title: "Eloquent: Getting Started"
---

{% raw %}
# Eloquent: Getting Started

- [Introduction](#introduction)
- [Generating Model Classes](#generating-model-classes)
- [Eloquent Model Conventions](#eloquent-model-conventions)
    - [Table Names](#table-names)
    - [Primary Keys](#primary-keys)
    - [UUID and ULID Keys](#uuid-and-ulid-keys)
    - [Timestamps](#timestamps)
    - [Database Connections](#database-connections)
    - [Default Attribute Values](#default-attribute-values)
    - [Refreshing Attributes After Writes](#refreshing-attributes-after-writes)
    - [Configuring Eloquent Strictness](#configuring-eloquent-strictness)
- [Retrieving Models](#retrieving-models)
    - [Collections](#collections)
    - [Chunking Results](#chunking-results)
    - [Chunking Using Lazy Collections](#chunking-using-lazy-collections)
    - [Cursors](#cursors)
    - [Advanced Subqueries](#advanced-subqueries)
- [Retrieving Single Models / Aggregates](#retrieving-single-models)
    - [Retrieving or Creating Models](#retrieving-or-creating-models)
    - [Retrieving Aggregates](#retrieving-aggregates)
- [Inserting and Updating Models](#inserting-and-updating-models)
    - [Inserts](#inserts)
    - [Updates](#updates)
    - [Mass Assignment](#mass-assignment)
    - [Upserts](#upserts)
- [Deleting Models](#deleting-models)
    - [Soft Deleting](#soft-deleting)
    - [Querying Soft Deleted Models](#querying-soft-deleted-models)
- [Pruning Models](#pruning-models)
- [Replicating Models](#replicating-models)
- [Query Scopes](#query-scopes)
    - [Global Scopes](#global-scopes)
    - [Local Scopes](#local-scopes)
    - [Pending Attributes](#pending-attributes)
- [Comparing Models](#comparing-models)
- [Events](#events)
    - [Using Closures](#events-using-closures)
    - [Observers](#observers)
    - [Muting Events](#muting-events)

<a name="introduction"></a>
## Introduction

Laravel includes Eloquent, an object-relational mapper (ORM) that makes it enjoyable to interact with your database. When using Eloquent, each database table has a corresponding "Model" that is used to interact with that table. In addition to retrieving records from the database table, Eloquent models allow you to insert, update, and delete records from the table as well.



> [!NOTE]
> 시작하기 전에 애플리케이션의 `config/database.php` 구성 파일에서 데이터베이스 연결을 설정했는지 확인하세요. 데이터베이스 구성에 대한 자세한 내용은 [데이터베이스 구성 문서](/docs/{{version}}/database#configuration)를 참조하세요.

<a name="generating-model-classes"></a>
## 모델 클래스 생성

시작하려면 Eloquent 모델을 하나 만들어 봅시다. 모델은 일반적으로 `app\Models` 디렉터리에 위치하며 `Illuminate\Database\Eloquent\Model` 클래스를 상속합니다. 새로운 모델을 생성하려면 `make:model` [Artisan 명령](/docs/{{version}}/artisan)을 사용할 수 있습니다:

```shell
php artisan make:model Flight
```



모델을 생성할 때 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 생성하고 싶다면, `--migration` 또는 `-m` 옵션을 사용할 수 있습니다:

```shell
php artisan make:model Flight --migration
```



모델을 생성할 때 팩토리, 시더, 정책, 컨트롤러, 폼 요청과 같은 다양한 유형의 클래스를 생성할 수 있습니다. 또한 이러한 옵션을 조합하여 한 번에 여러 클래스를 생성할 수도 있습니다:

```shell
# Generate a model and a FlightFactory class...
php artisan make:model Flight --factory
php artisan make:model Flight -f

# Generate a model and a FlightSeeder class...
php artisan make:model Flight --seed
php artisan make:model Flight -s

# Generate a model and a FlightController class...
php artisan make:model Flight --controller
php artisan make:model Flight -c

# Generate a model, FlightController resource class, and form request classes...
php artisan make:model Flight --controller --resource --requests
php artisan make:model Flight -crR

# Generate a model and a FlightPolicy class...
php artisan make:model Flight --policy

# Generate a model and a migration, factory, seeder, and controller...
php artisan make:model Flight -mfsc

# Shortcut to generate a model, migration, factory, seeder, policy, controller, and form requests...
php artisan make:model Flight --all
php artisan make:model Flight -a

# Generate a pivot model...
php artisan make:model Member --pivot
php artisan make:model Member -p
```



<a name="inspecting-models"></a>
#### 모델 검사하기

때때로 모델의 코드를 대충 훑어보는 것만으로는 모델이 제공하는 모든 속성과 관계를 파악하기 어려울 수 있습니다. 대신, 모든 모델의 속성과 관계를 편리하게 개요로 제공하는 `model:show` Artisan 명령어를 사용해 보세요:

```shell
php artisan model:show Flight
```



<a name="eloquent-model-conventions"></a>
## 엘로퀀트 모델 규칙

`make:model` 명령어로 생성된 모델은 `app/Models` 디렉토리에 위치하게 됩니다. 기본 모델 클래스를 살펴보고 엘로퀀트의 주요 규칙 중 일부를 논의해 봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    // ...
}
```



<a name="table-names"></a>
### 테이블 이름

위의 예제를 잠깐 살펴본 후, 우리는 Eloquent에게 어떤 데이터베이스 테이블이 우리의 `Flight` 모델에 해당하는지 알려주지 않았다는 것을 눈치챘을 수 있습니다. 관례상, 클래스의 "스네이크 케이스" 복수형 이름이 다른 이름이 명시적으로 지정되지 않는 한 테이블 이름으로 사용됩니다. 따라서 이 경우, Eloquent는 `Flight` 모델이 `flights` 테이블에 레코드를 저장한다고 가정하며, `AirTrafficController` 모델은 `air_traffic_controllers` 테이블에 레코드를 저장합니다.

모델에 해당하는 데이터베이스 테이블이 이 관례에 맞지 않는 경우, `Table` 속성을 사용하여 모델의 테이블 이름을 수동으로 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table('my_flights')]
class Flight extends Model
{
    // ...
}
```



<a name="primary-keys"></a>
### 기본 키

Eloquent는 또한 각 모델의 해당 데이터베이스 테이블이 `id`라는 이름의 기본 키 열을 가지고 있다고 가정합니다. 필요한 경우 `Table` 속성의 `key` 인수를 사용하여 모델의 기본 키로 사용되는 다른 열을 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'flight_id')]
class Flight extends Model
{
    // ...
}
```



또한, Eloquent는 기본 키가 증가하는 정수 값이라고 가정하므로 Eloquent는 기본 키를 자동으로 정수로 변환합니다. 증가하지 않거나 숫자가 아닌 기본 키를 사용하려는 경우, `Table` 속성에 `keyType` 및 `incrementing` 인수를 지정해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(key: 'uuid', keyType: 'string', incrementing: false)]
class Flight extends Model
{
    // ...
}
```



자동 증가 ID만 비활성화해야 하는 경우, `WithoutIncrementing` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutIncrementing;
use Illuminate\Database\Eloquent\Model;

#[WithoutIncrementing]
class Flight extends Model
{
    // ...
}
```



<a name="composite-primary-keys"></a>
#### "합성" 기본 키

Eloquent는 각 모델이 고유하게 식별할 수 있는 "ID"를 최소한 하나 이상 가져야 하며, 이는 기본 키로 사용될 수 있습니다. Eloquent 모델은 "합성" 기본 키를 지원하지 않습니다. 그러나 테이블의 고유하게 식별되는 기본 키 외에도 데이터베이스 테이블에 추가적인 다중 컬럼 고유 인덱스를 자유롭게 추가할 수 있습니다.

<a name="uuid-and-ulid-keys"></a>
### UUID 및 ULID 키

Eloquent 모델의 기본 키로 자동 증가 정수를 사용하는 대신, UUID를 사용할 수 있습니다. UUID는 36자 길이의 전 세계적으로 고유한 영숫자 식별자입니다.

모델이 자동 증가 정수 키 대신 UUID 키를 사용하도록 하려면 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUuids` 트레이트를 사용할 수 있습니다. 물론, 해당 모델에 [UUID에 상응하는 기본 키 컬럼](/docs/{{version}}/migrations#column-method-uuid)이 있는지 확인해야 합니다:

```php
use Illuminate\Database\Eloquent\Concerns\HasUuids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUuids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Europe']);

$article->id; // "018f2b5c-6a7f-7b12-9d6f-2f8a4e0c9c11"
```



기본적으로, `HasUuids` 트레잇은 모델에 대해 [UUIDv7](/docs/{{version}}/strings#method-str-uuid7) 식별자를 생성합니다. 이러한 UUID는 사전식으로 정렬할 수 있기 때문에 인덱스된 데이터베이스 저장에 더 효율적입니다.

특정 모델에 대한 UUID 생성 과정을 재정의하려면 모델에 `newUniqueId` 메서드를 정의할 수 있습니다. 또한 모델에 `uniqueIds` 메서드를 정의하여 UUID를 받을 컬럼을 지정할 수 있습니다:

```php
use Ramsey\Uuid\Uuid;

/**
 * Generate a new UUID for the model.
 */
public function newUniqueId(): string
{
    return (string) Uuid::uuid4();
}

/**
 * Get the columns that should receive a unique identifier.
 *
 * @return array<int, string>
 */
public function uniqueIds(): array
{
    return ['id', 'discount_code'];
}
```



원하신다면 UUID 대신 ‘ULID’를 사용할 수 있습니다. ULID는 UUID와 유사하지만 길이가 26자에 불과합니다. 정렬된 UUID와 마찬가지로, ULID는 효율적인 데이터베이스 인덱싱을 위해 사전식으로 정렬이 가능합니다. ULID를 사용하려면 모델에서 `Illuminate\Database\Eloquent\Concerns\HasUlids` 특성을 사용해야 합니다. 또한 모델에 [ULID에 해당하는 기본 키 열](/docs/{{version}}/migrations#column-method-ulid)이 있는지 확인해야 합니다.

```php
use Illuminate\Database\Eloquent\Concerns\HasUlids;
use Illuminate\Database\Eloquent\Model;

class Article extends Model
{
    use HasUlids;

    // ...
}

$article = Article::create(['title' => 'Traveling to Asia']);

$article->id; // "01gd4d3tgrrfqeda94gdbtdk5c"
```



<a name="timestamps"></a>
### 타임스탬프

기본적으로, Eloquent는 모델의 해당 데이터베이스 테이블에 `created_at` 및 `updated_at` 열이 존재할 것으로 예상합니다. 모델이 생성되거나 업데이트될 때 Eloquent는 자동으로 이 열들의 값을 설정합니다. Eloquent가 이러한 열들을 자동으로 관리하지 않기를 원하면, 모델의 `Table` 속성에서 `timestamps`를 `false`로 설정할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(timestamps: false)]
class Flight extends Model
{
    // ...
}
```



만약 타임스탬프만 비활성화할 필요가 있다면, `WithoutTimestamps` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\WithoutTimestamps;
use Illuminate\Database\Eloquent\Model;

#[WithoutTimestamps]
class Flight extends Model
{
    // ...
}
```



모델의 타임스탬프 형식을 사용자 정의해야 하는 경우 `Table` 속성에서 `dateFormat` 인수를 사용할 수 있습니다. 이것은 모델이 배열이나 JSON으로 직렬화될 때의 형식뿐만 아니라 데이터베이스에 날짜 속성이 저장되는 방식을 결정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Model;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```



날짜 형식만 정의해야 하는 경우, `DateFormat` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\DateFormat;
use Illuminate\Database\Eloquent\Model;

#[DateFormat('U')]
class Flight extends Model
{
    // ...
}
```



타임스탬프를 저장하는 데 사용되는 열의 이름을 사용자 지정해야 하는 경우, 모델에서 `CREATED_AT` 및 `UPDATED_AT` 상수를 정의할 수 있습니다:

```php
<?php

class Flight extends Model
{
    /**
     * The name of the "created at" column.
     *
     * @var string|null
     */
    public const CREATED_AT = 'creation_date';

    /**
     * The name of the "updated at" column.
     *
     * @var string|null
     */
    public const UPDATED_AT = 'updated_date';
}
```



모델의 `updated_at` 타임스탬프가 변경되지 않은 상태로 모델 작업을 수행하고 싶다면, `withoutTimestamps` 메서드에 제공된 클로저 내에서 모델을 조작할 수 있습니다:

```php
Model::withoutTimestamps(fn () => $post->increment('reads'));
```



<a name="database-connections"></a>
### 데이터베이스 연결

기본적으로 모든 Eloquent 모델은 애플리케이션에 구성된 기본 데이터베이스 연결을 사용합니다. 특정 모델과 상호작용할 때 사용해야 하는 다른 연결을 지정하고 싶다면, `Connection` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Connection;
use Illuminate\Database\Eloquent\Model;

#[Connection('mysql')]
class Flight extends Model
{
    // ...
}
```



<a name="default-attribute-values"></a>
### 기본 속성 값

기본적으로 새로 생성된 모델 인스턴스는 어떤 속성 값도 포함하지 않습니다. 모델의 일부 속성에 대한 기본값을 정의하고 싶다면, 모델에 `$attributes` 속성을 정의할 수 있습니다. `$attributes` 배열에 배치된 속성 값은 데이터베이스에서 방금 읽어온 것처럼 원시의 "저장 가능한" 형식이어야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Flight extends Model
{
    /**
     * The model's default values for attributes.
     *
     * @var array<string, mixed>
     */
    protected $attributes = [
        'options' => '[]',
        'delayed' => false,
    ];
}
```



<a name="refreshing-attributes-after-writes"></a>
### 쓰기 후 속성 새로 고침

데이터베이스에 생성된 열이 포함되어 있는 경우, 모델이 삽입되거나 업데이트된 후 특정 속성을 새로 고치도록 Eloquent를 구성할 수 있습니다. 이렇게 하려면 모델에 `Refreshes` 속성을 정의하세요:

```php
use Illuminate\Database\Eloquent\Attributes\Refreshes;

#[Refreshes('name')]
class User extends Model
{
    // ...
}
```



여러 속성을 배열로 지정할 수 있습니다:

```php
#[Refreshes(['name', 'slug'])]
```



모델이 작성된 후에는 구성된 속성들이 데이터베이스에서 새로 고쳐집니다.

<a name="configuring-eloquent-strictness"></a>
### Eloquent 엄격성 구성

Laravel은 다양한 상황에서 Eloquent의 동작과 "엄격성"을 구성할 수 있는 여러 가지 방법을 제공합니다.

먼저, `preventLazyLoading` 메서드는 선택적인 불리언 인수를 받아 지연 로딩(lazy loading)을 방지할지 여부를 나타냅니다. 예를 들어, 비생산 환경에서만 지연 로딩을 비활성화하고자 할 수 있으며, 이는 프로덕션 환경에서도 지연 로딩된 관계가 실수로 존재하더라도 정상적으로 작동하게 합니다. 일반적으로, 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출되어야 합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```



또한 `preventSilentlyDiscardingAttributes` 메서드를 호출하여 Laravel에게 채울 수 없는 속성을 채우려고 할 때 예외를 발생시키도록 지시할 수 있습니다. 이는 모델의 `fillable` 배열에 추가되지 않은 속성을 설정하려고 시도할 때 로컬 개발 중 예상치 못한 오류를 방지하는 데 도움이 될 수 있습니다:

```php
Model::preventSilentlyDiscardingAttributes(! $this->app->isProduction());
```



<a name="retrieving-models"></a>
## 모델 가져오기

모델과 [연관된 데이터베이스 테이블](/docs/{{version}}/migrations#generating-migrations)을 생성하면 데이터베이스에서 데이터를 가져올 준비가 된 것입니다. 각 Eloquent 모델을 모델과 연관된 데이터베이스 테이블을 유연하게 쿼리할 수 있는 강력한 [쿼리 빌더](/docs/{{version}}/queries)로 생각할 수 있습니다. 모델의 `all` 메서드는 모델과 연관된 데이터베이스 테이블의 모든 레코드를 가져옵니다:

```php
use App\Models\Flight;

foreach (Flight::all() as $flight) {
    echo $flight->name;
}
```



<a name="building-queries"></a>
#### 쿼리 작성

Eloquent `all` 메서드는 모델의 테이블에 있는 모든 결과를 반환합니다. 그러나 각 Eloquent 모델이 [쿼리 빌더](/docs/{{version}}/queries) 역할을 하기 때문에, 쿼리에 추가적인 제약 조건을 추가한 후 `get` 메서드를 호출하여 결과를 가져올 수 있습니다:

```php
$flights = Flight::where('active', 1)
    ->orderBy('name')
    ->limit(10)
    ->get();
```



> [!NOTE]
> Eloquent 모델은 쿼리 빌더이므로, Laravel의 [쿼리 빌더](/docs/{{version}}/queries)가 제공하는 모든 메서드를 검토해야 합니다. Eloquent 쿼리를 작성할 때 이러한 메서드 중 어느 것이든 사용할 수 있습니다.

<a name="refreshing-models"></a>
#### 모델 새로 고침

이미 데이터베이스에서 가져온 Eloquent 모델 인스턴스가 있는 경우, `fresh` 및 `refresh` 메서드를 사용하여 모델을 "새로 고침"할 수 있습니다. `fresh` 메서드는 모델을 데이터베이스에서 다시 가져옵니다. 기존 모델 인스턴스에는 영향을 주지 않습니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$freshFlight = $flight->fresh();
```



`refresh` 방법은 데이터베이스의 새로운 데이터를 사용하여 기존 모델을 다시 수화할 것입니다. 또한, 로드된 모든 관계도 새로 고쳐질 것입니다:

```php
$flight = Flight::where('number', 'FR 900')->first();

$flight->number = 'FR 456';

$flight->refresh();

$flight->number; // "FR 900"
```



트랜잭션 내에서 모델을 새로 고치고 비관적 잠금을 획득해야 하는 경우, `refreshForUpdate` 메서드를 사용할 수 있습니다. 이 메서드는 `FOR UPDATE` 잠금을 사용하여 모델을 다시 로드합니다:

```php
DB::transaction(function () use ($flight) {
    $flight->refreshForUpdate();

    // Update the locked model...
});
```



<a name="collections"></a>
### 컬렉션

지금까지 본 것처럼, `all`와 `get` 같은 Eloquent 메서드는 데이터베이스에서 여러 레코드를 가져옵니다. 그러나 이러한 메서드는 일반 PHP 배열을 반환하지 않습니다. 대신 `Illuminate\Database\Eloquent\Collection`의 인스턴스를 반환합니다.

Eloquent `Collection` 클래스는 Laravel의 기본 `Illuminate\Support\Collection` 클래스를 확장하며, 이는 데이터 컬렉션과 상호작용하기 위한 [다양한 유용한 메서드](/docs/{{version}}/collections#available-methods)를 제공합니다. 예를 들어, `reject` 메서드는 호출된 클로저의 결과를 기반으로 컬렉션에서 모델을 제거하는 데 사용할 수 있습니다:

```php
$flights = Flight::where('destination', 'Paris')->get();

$flights = $flights->reject(function (Flight $flight) {
    return $flight->cancelled;
});
```



라라벨의 기본 컬렉션 클래스에서 제공하는 메서드 외에도, 엘로퀀트 컬렉션 클래스는 [엘로퀀트 모델 컬렉션과 상호작용하기 위해 특별히 제공되는 몇 가지 추가 메서드](/docs/{{version}}/eloquent-collections#available-methods)를 제공합니다.

라라벨의 모든 컬렉션이 PHP의 반복 가능한 인터페이스를 구현하므로, 컬렉션을 배열처럼 반복할 수 있습니다:

```php
foreach ($flights as $flight) {
    echo $flight->name;
}
```



<a name="chunking-results"></a>
### 청크 결과

수만 개의 Eloquent 레코드를 `all` 또는 `get` 메서드를 통해 로드하려고 하면 애플리케이션의 메모리가 부족할 수 있습니다. 이러한 메서드 대신 `chunk` 메서드를 사용하면 많은 수의 모델을 보다 효율적으로 처리할 수 있습니다.

`chunk` 메서드는 Eloquent 모델의 일부를 검색하고 이를 클로저로 전달하여 처리합니다. 한 번에 현재 청크의 Eloquent 모델만 검색되므로, `chunk` 메서드는 많은 수의 모델을 작업할 때 메모리 사용량을 크게 줄여줍니다:

```php
use App\Models\Flight;
use Illuminate\Database\Eloquent\Collection;

Flight::chunk(200, function (Collection $flights) {
    foreach ($flights as $flight) {
        // ...
    }
});
```



`chunk` 메서드에 전달된 첫 번째 인수는 '청크'당 수신하고자 하는 레코드 수입니다. 두 번째 인수로 전달된 클로저는 데이터베이스에서 가져온 각 청크에 대해 호출됩니다. 클로저에 전달된 각 레코드 청크를 가져오기 위해 데이터베이스 쿼리가 실행됩니다.

만약 `chunk` 메서드의 결과를 반복하면서 업데이트할 열을 기준으로 필터링하고자 한다면, `chunkById` 메서드를 사용해야 합니다. 이러한 시나리오에서 `chunk` 메서드를 사용하면 예상치 못한 일관성 없는 결과가 발생할 수 있습니다. 내부적으로, `chunkById` 메서드는 항상 이전 청크에서 마지막 모델보다 큰 `id` 열을 가진 모델을 가져옵니다.

```php
Flight::where('departed', true)
    ->chunkById(200, function (Collection $flights) {
        $flights->each->update(['departed' => false]);
    }, column: 'id');
```



`chunkById` 및 `lazyById` 메서드가 실행 중인 쿼리에 자체적인 "where" 조건을 추가하기 때문에, 일반적으로 자신의 조건을 클로저 안에서 [논리적으로 그룹화](/docs/{{version}}/queries#logical-grouping)해야 합니다:

```php
Flight::where(function ($query) {
    $query->where('delayed', true)->orWhere('cancelled', true);
})->chunkById(200, function (Collection $flights) {
    $flights->each->update([
        'departed' => false,
        'cancelled' => true
    ]);
}, column: 'id');
```



<a name="chunking-using-lazy-collections"></a>
### 느린 컬렉션(Lazy Collections)을 사용한 청킹

`lazy` 메서드는 내부적으로 쿼리를 청크 단위로 실행한다는 점에서 [`chunk` 메서드](#chunking-results)와 유사하게 작동합니다. 그러나 각 청크를 그대로 콜백으로 전달하는 대신, `lazy` 메서드는 평탄화된 [LazyCollection](/docs/{{version}}/collections#lazy-collections) 형태의 Eloquent 모델을 반환하므로 결과를 단일 스트림처럼 다룰 수 있습니다:

```php
use App\Models\Flight;

foreach (Flight::lazy() as $flight) {
    // ...
}
```



결과를 반복하면서 업데이트할 열을 기준으로 `lazy` 메서드의 결과를 필터링하고 있다면, `lazyById` 메서드를 사용해야 합니다. 내부적으로 `lazyById` 메서드는 항상 이전 청크의 마지막 모델보다 큰 `id` 열을 가진 모델을 가져옵니다:

```php
Flight::where('departed', true)
    ->lazyById(200, column: 'id')
    ->each->update(['departed' => false]);
```



`lazyByIdDesc` 방법을 사용하여 `id`의 내림차순에 따라 결과를 필터링할 수 있습니다.

<a name="cursors"></a>
### 커서

`lazy` 방법과 유사하게, `cursor` 방법은 수만 개의 Eloquent 모델 레코드를 반복 처리할 때 애플리케이션의 메모리 사용량을 크게 줄이는 데 사용할 수 있습니다.

`cursor` 방법은 단일 데이터베이스 쿼리만 실행하지만, 개별 Eloquent 모델은 실제로 반복될 때까지 초기화되지 않습니다. 따라서 커서를 반복하는 동안 언제나 단 하나의 Eloquent 모델만 메모리에 유지됩니다.

> [!WARNING]
> `cursor` 방법은 한 번에 단 하나의 Eloquent 모델만 메모리에 유지하기 때문에 관계를 eager load할 수 없습니다. 관계를 eager load해야 한다면 대신 [`lazy` 방법](#chunking-using-lazy-collections)을 사용하는 것을 고려하세요.

내부적으로, `cursor` 방법은 PHP [제너레이터](https://www.php.net/manual/en/language.generators.overview.php)를 사용하여 이 기능을 구현합니다:

```php
use App\Models\Flight;

foreach (Flight::where('destination', 'Zurich')->cursor() as $flight) {
    // ...
}
```



`cursor`는 `Illuminate\Support\LazyCollection` 인스턴스를 반환합니다. [지연 컬렉션](/docs/{{version}}/collections#lazy-collections)을 사용하면 일반적인 Laravel 컬렉션에서 사용할 수 있는 많은 컬렉션 메서드를 한 번에 하나의 모델만 메모리에 로드하면서 사용할 수 있습니다:

```php
use App\Models\User;

$users = User::cursor()->filter(function (User $user) {
    return $user->id > 500;
});

foreach ($users as $user) {
    echo $user->id;
}
```



Although the `cursor` method uses far less memory than a regular query (by only holding a single Eloquent model in memory at a time), it will still eventually run out of memory. This is [due to PHP's PDO driver internally caching all raw query results in its buffer](https://www.php.net/manual/en/mysqlinfo.concepts.buffering.php). If you're dealing with a very large number of Eloquent records, consider using [the `lazy` method](#chunking-using-lazy-collections) instead.

<a name="advanced-subqueries"></a>
### Advanced Subqueries

<a name="subquery-selects"></a>
#### Subquery Selects

Eloquent also offers advanced subquery support, which allows you to pull information from related tables in a single query. For example, let's imagine that we have a table of flight `destinations` and a table of `flights` to destinations. The `flights` table contains an `arrived_at` column which indicates when the flight arrived at the destination.

Using the subquery functionality available to the query builder's `select` and `addSelect` methods, we can select all of the `destinations` and the name of the flight that most recently arrived at that destination using a single query:

```php
use App\Models\Destination;
use App\Models\Flight;

return Destination::addSelect(['last_flight' => Flight::select('name')
    ->whereColumn('destination_id', 'destinations.id')
    ->orderByDesc('arrived_at')
    ->limit(1)
])->get();
```



<a name="subquery-ordering"></a>
#### 서브쿼리 정렬

또한, 쿼리 빌더의 `orderBy` 기능은 서브쿼리를 지원합니다. 계속해서 항공편 예제를 사용하면, 이 기능을 사용하여 마지막 항공편이 해당 목적지에 도착한 시점을 기준으로 모든 목적지를 정렬할 수 있습니다. 다시 말하지만, 이는 단일 데이터베이스 쿼리를 실행하는 동안 수행할 수 있습니다:

```php
return Destination::orderByDesc(
    Flight::select('arrived_at')
        ->whereColumn('destination_id', 'destinations.id')
        ->orderByDesc('arrived_at')
        ->limit(1)
)->get();
```



<a name="retrieving-single-models"></a>
## 단일 모델 / 집계 가져오기

주어진 쿼리와 일치하는 모든 레코드를 가져오는 것 외에도, `find`, `first` 또는 `firstWhere` 메서드를 사용하여 단일 레코드를 가져올 수도 있습니다. 모델 컬렉션을 반환하는 대신, 이러한 메서드는 단일 모델 인스턴스를 반환합니다:

```php
use App\Models\Flight;

// Retrieve a model by its primary key...
$flight = Flight::find(1);

// Retrieve the first model matching the query constraints...
$flight = Flight::where('active', 1)->first();

// Alternative to retrieving the first model matching the query constraints...
$flight = Flight::firstWhere('active', 1);
```



때때로 결과가 없을 경우 다른 작업을 수행하고 싶을 수도 있습니다. `findOr`와 `firstOr` 메서드는 단일 모델 인스턴스를 반환하거나, 결과가 없을 경우 주어진 클로저를 실행합니다. 클로저가 반환하는 값은 메서드의 결과로 간주됩니다:

```php
$flight = Flight::findOr(1, function () {
    // ...
});

$flight = Flight::where('legs', '>', 3)->firstOr(function () {
    // ...
});
```



<a name="not-found-exceptions"></a>
#### 찾을 수 없음 예외

때때로 모델을 찾을 수 없을 경우 예외를 발생시키고 싶을 때가 있습니다. 이는 특히 라우트나 컨트롤러에서 유용합니다. `findOrFail` 및 `firstOrFail` 메서드는 쿼리의 첫 번째 결과를 가져옵니다. 그러나 결과가 없으면 `Illuminate\Database\Eloquent\ModelNotFoundException`가 발생합니다:

```php
$flight = Flight::findOrFail(1);

$flight = Flight::where('legs', '>', 3)->firstOrFail();
```



`ModelNotFoundException`가 잡히지 않으면 클라이언트에게 자동으로 404 HTTP 응답이 전송됩니다:

```php
use App\Models\Flight;

Route::get('/api/flights/{id}', function (string $id) {
    return Flight::findOrFail($id);
});
```



<a name="retrieving-or-creating-models"></a>
### 모델 검색 또는 생성

`firstOrCreate` 메서드는 주어진 열/값 쌍을 사용하여 데이터베이스에서 레코드를 찾으려고 시도합니다. 데이터베이스에서 모델을 찾을 수 없는 경우, 첫 번째 배열 인수와 선택적 두 번째 배열 인수를 병합한 속성으로 레코드가 삽입됩니다.

`firstOrNew` 메서드는 `firstOrCreate`와 마찬가지로 주어진 속성과 일치하는 레코드를 데이터베이스에서 찾으려고 시도합니다. 그러나 모델을 찾을 수 없는 경우, 새 모델 인스턴스가 반환됩니다. `firstOrNew`에 의해 반환된 모델은 아직 데이터베이스에 저장되지 않았음을 유의하세요. 이를 저장하려면 `save` 메서드를 수동으로 호출해야 합니다:

```php
use App\Models\Flight;

// Retrieve flight by name or create it if it doesn't exist...
$flight = Flight::firstOrCreate([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or create it with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrCreate(
    ['name' => 'London to Paris'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);

// Retrieve flight by name or instantiate a new Flight instance...
$flight = Flight::firstOrNew([
    'name' => 'London to Paris'
]);

// Retrieve flight by name or instantiate with the name, delayed, and arrival_time attributes...
$flight = Flight::firstOrNew(
    ['name' => 'Tokyo to Sydney'],
    ['delayed' => 1, 'arrival_time' => '11:30']
);
```



<a name="retrieving-aggregates"></a>
### 집계 가져오기

Eloquent 모델과 상호작용할 때, Laravel [쿼리 빌더](/docs/{{version}}/queries)에서 제공하는 `count`, `sum`, `max` 및 기타 [집계 메서드](/docs/{{version}}/queries#aggregates)를 사용할 수도 있습니다. 예상할 수 있듯이 이러한 메서드는 Eloquent 모델 인스턴스 대신 스칼라 값을 반환합니다:

```php
$count = Flight::where('active', 1)->count();

$max = Flight::where('active', 1)->max('price');
```



<a name="inserting-and-updating-models"></a>
## 모델 삽입 및 업데이트

<a name="inserts"></a>
### 삽입

물론, Eloquent를 사용할 때 우리는 단순히 데이터베이스에서 모델을 가져오는 것만이 필요하지 않습니다. 또한 새로운 레코드를 삽입해야 합니다. 다행히도 Eloquent는 이를 간단하게 만들어 줍니다. 데이터베이스에 새 레코드를 삽입하려면, 새로운 모델 인스턴스를 생성하고 모델에 속성을 설정해야 합니다. 그런 다음 모델 인스턴스에서 `save` 메서드를 호출하세요:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Flight;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class FlightController extends Controller
{
    /**
     * Store a new flight in the database.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate the request...

        $flight = new Flight;

        $flight->name = $request->name;

        $flight->save();

        return redirect('/flights');
    }
}
```



이 예제에서는 들어오는 HTTP 요청의 `name` 필드를 `App\Models\Flight` 모델 인스턴스의 `name` 속성에 할당합니다. `save` 메서드를 호출하면 데이터베이스에 레코드가 삽입됩니다. 모델의 `created_at` 및 `updated_at` 타임스탬프는 `save` 메서드가 호출될 때 자동으로 설정되므로 수동으로 설정할 필요가 없습니다.

모델을 데이터베이스 트랜잭션 내에서 저장하려면 `saveOrFail` 메서드를 사용할 수 있습니다. 저장 중에 예외가 발생하면 트랜잭션은 자동으로 롤백됩니다:

```php
$flight->saveOrFail();
```



또는 단일 PHP 문장을 사용하여 새 모델을 '저장'하기 위해 `create` 메서드를 사용할 수 있습니다. 삽입된 모델 인스턴스는 `create` 메서드에 의해 반환됩니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```



하지만 `create` 메서드를 사용하기 전에, 모델 클래스에서 `Fillable` 또는 `Guarded` 속성 중 하나를 지정해야 합니다. 이러한 속성은 모든 Eloquent 모델이 기본적으로 대량 할당 취약성으로부터 보호되기 때문에 필요합니다. 대량 할당에 대해 더 알고 싶다면, [대량 할당 문서](#mass-assignment)를 참조하십시오.

<a name="updates"></a>
### 업데이트

`save` 메서드는 데이터베이스에 이미 존재하는 모델을 업데이트할 때도 사용할 수 있습니다. 모델을 업데이트하려면, 먼저 모델을 조회하고 업데이트하려는 속성을 설정해야 합니다. 그런 다음, 모델의 `save` 메서드를 호출해야 합니다. 다시 말하지만, `updated_at` 타임스탬프는 자동으로 업데이트되므로 수동으로 값을 설정할 필요가 없습니다.

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->name = 'Paris to London';

$flight->save();
```



데이터베이스 트랜잭션 내에서 모델을 업데이트하고 싶다면, `updateOrFail` 메서드를 사용할 수 있습니다. 업데이트 중 예외가 발생하면 트랜잭션은 자동으로 롤백됩니다:

```php
$flight->updateOrFail(['name' => 'Paris to London']);
```



가끔씩, 기존 모델을 업데이트하거나 일치하는 모델이 존재하지 않는 경우 새 모델을 생성해야 할 수도 있습니다. `firstOrCreate` 방법과 마찬가지로, `updateOrCreate` 방법은 모델을 유지하므로 `save` 방법을 수동으로 호출할 필요가 없습니다.

아래 예제에서, `departure` 위치가 `Oakland`이고 `destination` 위치가 `San Diego`인 항공편이 존재하면 해당 항공편의 `price` 및 `discounted` 열이 업데이트됩니다. 만약 그런 항공편이 존재하지 않으면, 첫 번째 인수 배열과 두 번째 인수 배열을 병합한 결과 속성을 가진 새 항공편이 생성됩니다.

```php
$flight = Flight::updateOrCreate(
    ['departure' => 'Oakland', 'destination' => 'San Diego'],
    ['price' => 99, 'discounted' => 1]
);
```



`firstOrCreate` 또는 `updateOrCreate`와 같은 방법을 사용할 때, 새로운 모델이 생성되었는지 아니면 기존 모델이 업데이트되었는지 알지 못할 수 있습니다. `wasRecentlyCreated` 속성은 모델이 현재 수명 주기 동안 생성되었는지를 나타냅니다:

```php
$flight = Flight::updateOrCreate(
    // ...
);

if ($flight->wasRecentlyCreated) {
    // New flight record was inserted...
}
```



<a name="mass-updates"></a>
#### 대량 업데이트

업데이트는 주어진 쿼리와 일치하는 모델에 대해서도 수행될 수 있습니다. 이 예제에서는 `active`인 모든 항공편 중 `destination`가 `San Diego`인 항공편이 지연으로 표시됩니다:

```php
Flight::where('active', 1)
    ->where('destination', 'San Diego')
    ->update(['delayed' => 1]);
```



The `update` method expects an array of column and value pairs representing the columns that should be updated. The `update` method returns the number of affected rows.

> [!WARNING]
> When issuing a mass update via Eloquent, the `saving`, `saved`, `updating`, and `updated` model events will not be fired for the updated models. This is because the models are never actually retrieved when issuing a mass update.

<a name="examining-attribute-changes"></a>
#### Examining Attribute Changes

Eloquent provides the `isDirty`, `isClean`, and `wasChanged` methods to examine the internal state of your model and determine how its attributes have changed from when the model was originally retrieved.

The `isDirty` method determines if any of the model's attributes have been changed since the model was retrieved. You may pass a specific attribute name or an array of attributes to the `isDirty` method to determine if any of the attributes are "dirty". The `isClean` method will determine if an attribute has remained unchanged since the model was retrieved. This method also accepts an optional attribute argument:

```php
use App\Models\User;

$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->isDirty(); // true
$user->isDirty('title'); // true
$user->isDirty('first_name'); // false
$user->isDirty(['first_name', 'title']); // true

$user->isClean(); // false
$user->isClean('title'); // false
$user->isClean('first_name'); // true
$user->isClean(['first_name', 'title']); // false

$user->save();

$user->isDirty(); // false
$user->isClean(); // true
```



`wasChanged` 메서드는 현재 요청 주기 내에서 모델이 마지막으로 저장될 때 어떤 속성이 변경되었는지 확인합니다. 필요하다면 특정 속성이 변경되었는지 확인하기 위해 속성 이름을 전달할 수 있습니다:

```php
$user = User::create([
    'first_name' => 'Taylor',
    'last_name' => 'Otwell',
    'title' => 'Developer',
]);

$user->title = 'Painter';

$user->save();

$user->wasChanged(); // true
$user->wasChanged('title'); // true
$user->wasChanged(['title', 'slug']); // true
$user->wasChanged('first_name'); // false
$user->wasChanged(['first_name', 'title']); // true
```



`getOriginal` 메서드는 가져온 이후 모델에 어떤 변경이 있더라도 모델의 원래 속성을 포함하는 배열을 반환합니다. 필요한 경우 특정 속성의 원래 값을 얻기 위해 특정 속성 이름을 전달할 수 있습니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->name = 'Jack';
$user->name; // Jack

$user->getOriginal('name'); // John
$user->getOriginal(); // Array of original attributes...
```



`getChanges` 메서드는 모델이 마지막으로 저장될 때 변경된 속성을 포함하는 배열을 반환하는 반면, `getPrevious` 메서드는 모델이 마지막으로 저장되기 전에 원래 속성 값을 포함하는 배열을 반환합니다:

```php
$user = User::find(1);

$user->name; // John
$user->email; // john@example.com

$user->update([
    'name' => 'Jack',
    'email' => 'jack@example.com',
]);

$user->getChanges();

/*
    [
        'name' => 'Jack',
        'email' => 'jack@example.com',
    ]
*/

$user->getPrevious();

/*
    [
        'name' => 'John',
        'email' => 'john@example.com',
    ]
*/
```



<a name="mass-assignment"></a>
### 대량 할당

단일 PHP 구문을 사용하여 새로운 모델을 "저장"하기 위해 `create` 메서드를 사용할 수 있습니다. 삽입된 모델 인스턴스는 메서드에 의해 반환됩니다:

```php
use App\Models\Flight;

$flight = Flight::create([
    'name' => 'London to Paris',
]);
```



그러나 `create` 메서드를 사용하기 전에 모델 클래스에 `Fillable` 또는 `Guarded` 속성 중 하나를 지정해야 합니다. 이 속성들은 모든 Eloquent 모델이 기본적으로 대량 할당 취약점으로부터 보호되기 때문에 필요합니다.

대량 할당 취약점은 사용자가 예상치 못한 HTTP 요청 필드를 전달하고 해당 필드가 데이터베이스의 예상치 못한 열을 변경할 때 발생합니다. 예를 들어, 악의적인 사용자가 HTTP 요청을 통해 `is_admin` 매개변수를 보내면, 이 매개변수가 모델의 `create` 메서드로 전달되어 사용자가 자신을 관리자로 승격시킬 수 있습니다.

따라서 시작하려면 어떤 모델 속성을 대량 할당 가능하게 만들지 정의해야 합니다. 이는 모델에서 `Fillable` 속성을 사용하여 할 수 있습니다. 예를 들어, `Flight` 모델의 `name` 속성을 대량 할당 가능하게 만들어 보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Fillable;
use Illuminate\Database\Eloquent\Model;

#[Fillable(['name'])]
class Flight extends Model
{
    // ...
}
```



한번 대량 할당이 가능한 속성을 지정하면, `create` 메서드를 사용하여 데이터베이스에 새 레코드를 삽입할 수 있습니다. `create` 메서드는 새로 생성된 모델 인스턴스를 반환합니다:

```php
$flight = Flight::create(['name' => 'London to Paris']);
```



이미 모델 인스턴스가 있는 경우, `fill` 메서드를 사용하여 속성 배열로 그것을 채울 수 있습니다:

```php
$flight->fill(['name' => 'Amsterdam to Frankfurt']);
```



<a name="mass-assignment-json-columns"></a>
#### 대량 할당 및 JSON 컬럼

JSON 컬럼을 할당할 때, 각 컬럼의 대량 할당 가능한 키는 모델의 `Fillable` 속성에 지정되어야 합니다. 보안상, Laravel은 `Guarded` 속성을 사용할 때 중첩된 JSON 속성을 업데이트하는 것을 지원하지 않습니다:

```php
use Illuminate\Database\Eloquent\Attributes\Fillable;

#[Fillable(['options->enabled'])]
class Flight extends Model
{
    // ...
}
```



<a name="allowing-mass-assignment"></a>
#### 대량 할당 허용

모든 속성을 대량 할당 가능하게 만들고자 한다면, 모델에서 `Unguarded` 속성을 사용할 수 있습니다. 모델의 보호를 해제하기로 선택한 경우, Eloquent의 `fill`, `create`, `update` 메서드에 전달되는 배열을 항상 직접 작성하도록 특별히 주의해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Unguarded;
use Illuminate\Database\Eloquent\Model;

#[Unguarded]
class Flight extends Model
{
    // ...
}
```



<a name="mass-assignment-exceptions"></a>
#### 대량 할당 예외

기본적으로, `Fillable` 속성에 포함되지 않은 속성은 대량 할당 작업을 수행할 때 조용히 무시됩니다. 운영 환경에서는 이것이 예상되는 동작이지만, 로컬 개발 중에는 모델 변경 사항이 적용되지 않는 이유에 대해 혼란을 초래할 수 있습니다.

원하는 경우, fill할 수 없는 속성을 채우려고 할 때 Laravel이 예외를 발생시키도록 `preventSilentlyDiscardingAttributes` 메서드를 호출하여 지시할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 호출되어야 합니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventSilentlyDiscardingAttributes($this->app->isLocal());
}
```



<a name="upserts"></a>
### 업서트

Eloquent의 `upsert` 메서드는 단일 원자적 연산으로 레코드를 업데이트하거나 생성할 때 사용할 수 있습니다. 이 메서드의 첫 번째 인수는 삽입하거나 업데이트할 값을 포함하며, 두 번째 인수는 연관된 테이블 내에서 레코드를 고유하게 식별하는 열을 나열합니다. 세 번째이자 마지막 인수는 데이터베이스에 일치하는 레코드가 이미 존재할 경우 업데이트해야 하는 열의 배열입니다. `upsert` 메서드는 모델에 타임스탬프가 활성화되어 있으면 `created_at` 및 `updated_at` 타임스탬프를 자동으로 설정합니다:

```php
Flight::upsert([
    ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
    ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
], uniqueBy: ['departure', 'destination'], update: ['price']);
```



> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드의 두 번째 인수에 있는 열이 'primary' 또는 'unique' 인덱스를 가져야 합니다. 또한, MariaDB와 MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하며, 항상 테이블의 'primary' 및 'unique' 인덱스를 사용하여 기존 레코드를 감지합니다.

<a name="deleting-models"></a>
## 모델 삭제

모델을 삭제하려면 모델 인스턴스에서 `delete` 메서드를 호출할 수 있습니다:

```php
use App\Models\Flight;

$flight = Flight::find(1);

$flight->delete();
```



데이터베이스 트랜잭션 내에서 모델을 삭제하고 싶다면, `deleteOrFail` 메서드를 사용할 수 있습니다. 삭제 중 예외가 발생하면 트랜잭션은 자동으로 롤백됩니다:

```php
$flight->deleteOrFail();
```



<a name="deleting-an-existing-model-by-its-primary-key"></a>
#### 기본 키로 기존 모델 삭제하기

위의 예제에서는 `delete` 메서드를 호출하기 전에 데이터베이스에서 모델을 가져오고 있습니다. 그러나 모델의 기본 키를 알고 있는 경우, `destroy` 메서드를 호출하여 모델을 명시적으로 가져오지 않고도 모델을 삭제할 수 있습니다. `destroy` 메서드는 단일 기본 키를 받는 것 외에도, 여러 개의 기본 키, 기본 키 배열, 또는 기본 키 [컬렉션](/docs/{{version}}/collections)을 받을 수 있습니다:

```php
Flight::destroy(1);

Flight::destroy(1, 2, 3);

Flight::destroy([1, 2, 3]);

Flight::destroy(collect([1, 2, 3]));
```



만약 [소프트 삭제 모델](#soft-deleting)을 사용하고 있다면, `forceDestroy` 메서드를 통해 모델을 영구 삭제할 수 있습니다:

```php
Flight::forceDestroy(1);
```



> [!WARNING]
> `destroy` 메서드는 각 모델을 개별적으로 로드하고 `delete` 메서드를 호출하여 각 모델에 대해 `deleting` 및 `deleted` 이벤트가 올바르게 전달되도록 합니다.

<a name="deleting-models-using-queries"></a>
#### 쿼리를 사용하여 모델 삭제하기

물론, 쿼리의 조건에 맞는 모든 모델을 삭제하기 위해 Eloquent 쿼리를 작성할 수 있습니다. 이 예제에서는 비활성으로 표시된 모든 항공편을 삭제합니다. 대량 업데이트와 마찬가지로, 대량 삭제는 삭제된 모델에 대한 모델 이벤트를 전달하지 않습니다:

```php
$deleted = Flight::where('active', 0)->delete();
```



테이블의 모든 모델을 삭제하려면 조건을 추가하지 않고 쿼리를 실행해야 합니다:

```php
$deleted = Flight::query()->delete();
```



> [!WARNING]
> Eloquent를 통해 대량 삭제 문을 실행할 때, 삭제된 모델에 대해 `deleting` 및 `deleted` 모델 이벤트는 발생하지 않습니다. 이는 삭제 문을 실행할 때 모델이 실제로 검색되지 않기 때문입니다.

<a name="soft-deleting"></a>
### 소프트 삭제

데이터베이스에서 실제로 레코드를 제거하는 것 외에도, Eloquent는 모델을 "소프트 삭제"할 수도 있습니다. 모델이 소프트 삭제되면, 데이터베이스에서 실제로 제거되지 않습니다. 대신 모델에 `deleted_at` 속성이 설정되어 모델이 "삭제"된 날짜와 시간이 표시됩니다. 모델에 소프트 삭제를 활성화하려면 모델에 `Illuminate\Database\Eloquent\SoftDeletes` 트레이트를 추가하십시오:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Flight extends Model
{
    use SoftDeletes;
}
```



> [!NOTE]
> `SoftDeletes` 특성은 `deleted_at` 속성을 `DateTime` / `Carbon` 인스턴스로 자동으로 변환해 줍니다.

또한 `deleted_at` 열을 데이터베이스 테이블에 추가해야 합니다. Laravel [스키마 빌더](/docs/{{version}}/migrations)에는 이 열을 생성하기 위한 도우미 메서드가 포함되어 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('flights', function (Blueprint $table) {
    $table->softDeletes();
});

Schema::table('flights', function (Blueprint $table) {
    $table->dropSoftDeletes();
});
```



이제 모델에서 `delete` 메서드를 호출하면 `deleted_at` 열이 현재 날짜와 시간으로 설정됩니다. 그러나 모델의 데이터베이스 레코드는 테이블에 남아 있습니다. 소프트 삭제를 사용하는 모델을 쿼리할 때, 소프트 삭제된 모델은 모든 쿼리 결과에서 자동으로 제외됩니다.

주어진 모델 인스턴스가 소프트 삭제되었는지 확인하려면 `trashed` 메서드를 사용할 수 있습니다:

```php
if ($flight->trashed()) {
    // ...
}
```



<a name="restoring-soft-deleted-models"></a>
#### 소프트 삭제된 모델 복원하기

때때로 소프트 삭제된 모델을 '삭제 취소'하고 싶을 때가 있습니다. 소프트 삭제된 모델을 복원하려면 모델 인스턴스에서 `restore` 메서드를 호출하면 됩니다. `restore` 메서드는 모델의 `deleted_at` 열을 `null`로 설정합니다:

```php
$flight->restore();
```



여러 모델을 복원하기 위해 쿼리에서 `restore` 방법을 사용할 수도 있습니다. 다시 말하지만, 다른 '대량' 작업과 마찬가지로, 복원된 모델에 대해서는 어떤 모델 이벤트도 발생하지 않습니다:

```php
Flight::withTrashed()
    ->where('airline_id', 1)
    ->restore();
```



`restore` 방법은 [관계](/docs/{{version}}/eloquent-relationships) 쿼리를 작성할 때도 사용할 수 있습니다:

```php
$flight->history()->restore();
```



<a name="permanently-deleting-models"></a>
#### 모델 영구 삭제

가끔 데이터베이스에서 모델을 완전히 제거해야 할 때가 있습니다. `forceDelete` 메서드를 사용하여 데이터베이스 테이블에서 소프트 삭제된 모델을 영구적으로 제거할 수 있습니다:

```php
$flight->forceDelete();
```



Eloquent 관계 쿼리를 작성할 때 `forceDelete` 방법을 사용할 수도 있습니다:

```php
$flight->history()->forceDelete();
```



<a name="querying-soft-deleted-models"></a>
### 소프트 삭제된 모델 쿼리하기

<a name="including-soft-deleted-models"></a>
#### 소프트 삭제된 모델 포함하기

위에서 언급한 것처럼 소프트 삭제된 모델은 쿼리 결과에서 자동으로 제외됩니다. 그러나 쿼리에서 `withTrashed` 메서드를 호출하여 소프트 삭제된 모델을 쿼리 결과에 포함시킬 수 있습니다:

```php
use App\Models\Flight;

$flights = Flight::withTrashed()
    ->where('account_id', 1)
    ->get();
```



`withTrashed` 메서드는 [관계](/docs/{{version}}/eloquent-relationships) 쿼리를 작성할 때도 호출될 수 있습니다:

```php
$flight->history()->withTrashed()->get();
```



<a name="retrieving-only-soft-deleted-models"></a>
#### 소프트 삭제된 모델만 검색하기

`onlyTrashed` 메서드는 **오직** 소프트 삭제된 모델만 검색합니다:

```php
$flights = Flight::onlyTrashed()
    ->where('airline_id', 1)
    ->get();
```



<a name="pruning-models"></a>
## 모델 가지치기

때때로 더 이상 필요하지 않은 모델을 주기적으로 삭제하고 싶을 때가 있습니다. 이를 달성하기 위해 주기적으로 가지치기하고 싶은 모델에 `Illuminate\Database\Eloquent\Prunable` 또는 `Illuminate\Database\Eloquent\MassPrunable` 트레이트를 추가할 수 있습니다. 모델에 트레이트 중 하나를 추가한 후, 더 이상 필요하지 않은 모델을 해결하는 Eloquent 쿼리 빌더를 반환하는 `prunable` 메서드를 구현하세요:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Prunable;

class Flight extends Model
{
    use Prunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```



모델을 `Prunable`로 표시할 때, 모델에 `pruning` 메서드를 정의할 수도 있습니다. 이 메서드는 모델이 삭제되기 전에 호출됩니다. 이 메서드는 모델이 데이터베이스에서 영구적으로 제거되기 전에 저장된 파일과 같은 모델과 관련된 추가 리소스를 삭제하는 데 유용할 수 있습니다:

```php
/**
 * Prepare the model for pruning.
 */
protected function pruning(): void
{
    // ...
}
```



가지치기 가능한 모델을 구성한 후에는 애플리케이션의 `routes/console.php` 파일에서 `model:prune` Artisan 명령을 예약해야 합니다. 이 명령을 실행할 적절한 간격을 자유롭게 선택할 수 있습니다:

```php
use Illuminate\Support\Facades\Schedule;

Schedule::command('model:prune')->daily();
```



백그라운드에서 `model:prune` 명령어는 애플리케이션의 `app/Models` 디렉터리 내에서 "Prunable" 모델을 자동으로 감지합니다. 모델이 다른 위치에 있는 경우 `--model` 옵션을 사용하여 모델 클래스 이름을 지정할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--model' => [Address::class, Flight::class],
])->daily();
```



모든 다른 감지된 모델을 가지치기하면서 특정 모델을 가지치기에서 제외하고자 하는 경우, `--except` 옵션을 사용할 수 있습니다:

```php
Schedule::command('model:prune', [
    '--except' => [Address::class, Flight::class],
])->daily();
```



`prunable` 쿼리는 `--pretend` 옵션과 함께 `model:prune` 명령을 실행하여 테스트할 수 있습니다. 시뮬레이션할 때는 `model:prune` 명령이 명령이 실제로 실행될 경우 몇 개의 레코드가 제거될 것인지 단순히 보고할 것입니다:

```shell
php artisan model:prune --pretend
```



> [!WARNING]
> 모델을 소프트 삭제하면(prunable 쿼리에 일치하는 경우) 영구적으로 삭제됩니다(`forceDelete`).

<a name="mass-pruning"></a>
#### 대량 제거

모델이 `Illuminate\Database\Eloquent\MassPrunable` 특성으로 표시되면, 모델은 대량 삭제 쿼리를 사용하여 데이터베이스에서 삭제됩니다. 따라서 `pruning` 메서드는 호출되지 않으며, `deleting` 및 `deleted` 모델 이벤트도 발생하지 않습니다. 이는 삭제 전에 모델이 실제로 검색되지 않기 때문에, 제거 과정이 훨씬 효율적이기 때문입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\MassPrunable;

class Flight extends Model
{
    use MassPrunable;

    /**
     * Get the prunable model query.
     */
    public function prunable(): Builder
    {
        return static::where('created_at', '<=', now()->minus(months: 1));
    }
}
```



<a name="replicating-models"></a>
## 모델 복제

`replicate` 방법을 사용하여 기존 모델 인스턴스의 저장되지 않은 복사본을 만들 수 있습니다. 이 방법은 많은 속성을 공유하는 모델 인스턴스가 있을 때 특히 유용합니다:

```php
use App\Models\Address;

$shipping = Address::create([
    'type' => 'shipping',
    'line_1' => '123 Example Street',
    'city' => 'Victorville',
    'state' => 'CA',
    'postcode' => '90001',
]);

$billing = $shipping->replicate()->fill([
    'type' => 'billing'
]);

$billing->save();
```



하나 이상의 속성이 새로운 모델로 복제되지 않도록 제외하려면, 배열을 `replicate` 메서드에 전달할 수 있습니다:

```php
$flight = Flight::create([
    'destination' => 'LAX',
    'origin' => 'LHR',
    'last_flown' => '2020-03-04 11:00:00',
    'last_pilot_id' => 747,
]);

$flight = $flight->replicate([
    'last_flown',
    'last_pilot_id'
]);
```



<a name="query-scopes"></a>
## 쿼리 스코프

<a name="global-scopes"></a>
### 전역 스코프

전역 스코프는 주어진 모델의 모든 쿼리에 제약 조건을 추가할 수 있게 해줍니다. Laravel 자체의 [소프트 삭제](#soft-deleting) 기능은 전역 스코프를 활용하여 데이터베이스에서 "삭제되지 않은" 모델만 검색합니다. 자체 전역 스코프를 작성하면 주어진 모델의 모든 쿼리가 특정 제약 조건을 받도록 하는 편리하고 쉬운 방법을 제공할 수 있습니다.

<a name="generating-scopes"></a>
#### 스코프 생성

새 전역 스코프를 생성하려면 `make:scope` Artisan 명령을 호출할 수 있으며, 생성된 스코프는 애플리케이션의 `app/Models/Scopes` 디렉토리에 배치됩니다.

```shell
php artisan make:scope AncientScope
```



<a name="writing-global-scopes"></a>
#### 전역 스코프 작성

전역 스코프를 작성하는 것은 간단합니다. 먼저, `make:scope` 명령어를 사용하여 `Illuminate\Database\Eloquent\Scope` 인터페이스를 구현하는 클래스를 생성합니다. `Scope` 인터페이스는 `apply`라는 하나의 메서드를 구현하도록 요구합니다. `apply` 메서드는 필요에 따라 쿼리에 `where` 제약조건이나 기타 유형의 절을 추가할 수 있습니다:

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class AncientScope implements Scope
{
    /**
     * Apply the scope to a given Eloquent query builder.
     */
    public function apply(Builder $builder, Model $model): void
    {
        $builder->where('created_at', '<', now()->minus(years: 2000));
    }
}
```



> [!NOTE]
> 쿼리의 선택 절(select clause)에 열을 추가하는 글로벌 범위를 사용하는 경우, `select` 대신 `addSelect` 메서드를 사용해야 합니다. 이렇게 하면 쿼리의 기존 선택 절이 의도치 않게 대체되는 것을 방지할 수 있습니다.

<a name="applying-global-scopes"></a>
#### 글로벌 범위 적용하기

모델에 글로벌 범위를 할당하려면, 단순히 모델에 `ScopedBy` 속성을 추가하면 됩니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Attributes\ScopedBy;

#[ScopedBy([AncientScope::class])]
class User extends Model
{
    //
}
```



또는 모델의 `booted` 메서드를 오버라이드하여 글로벌 스코프를 수동으로 등록하고 모델의 `addGlobalScope` 메서드를 호출할 수 있습니다. `addGlobalScope` 메서드는 스코프의 인스턴스를 유일한 인자로 받습니다:

```php
<?php

namespace App\Models;

use App\Models\Scopes\AncientScope;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new AncientScope);
    }
}
```



위 예제에서 범위를 `App\Models\User` 모델에 추가한 후, `User::all()` 메서드를 호출하면 다음 SQL 쿼리가 실행됩니다:

```sql
select * from `users` where `created_at` < 0021-02-18 00:00:00
```



<a name="anonymous-global-scopes"></a>
#### 익명 글로벌 스코프

엘로퀀트(Eloquent)는 또한 클로저를 사용하여 글로벌 스코프를 정의할 수 있게 해주며, 이는 별도의 클래스를 필요로 하지 않는 간단한 스코프에 특히 유용합니다. 클로저를 사용하여 글로벌 스코프를 정의할 때, `addGlobalScope` 메서드의 첫 번째 인자로 직접 선택한 스코프 이름을 제공해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope('ancient', function (Builder $builder) {
            $builder->where('created_at', '<', now()->minus(years: 2000));
        });
    }
}
```



<a name="removing-global-scopes"></a>
#### 전역 스코프 제거

주어진 쿼리에 대한 전역 스코프를 제거하고 싶다면, `withoutGlobalScope` 메서드를 사용할 수 있습니다. 이 메서드는 전역 스코프의 클래스 이름을 유일한 인수로 받습니다:

```php
User::withoutGlobalScope(AncientScope::class)->get();
```



또는 클로저를 사용하여 전역 범위를 정의했다면, 전역 범위에 할당한 문자열 이름을 전달해야 합니다:

```php
User::withoutGlobalScope('ancient')->get();
```



쿼리의 여러 글로벌 스코프 또는 모든 글로벌 스코프를 제거하고 싶다면, `withoutGlobalScopes` 및 `withoutGlobalScopesExcept` 메서드를 사용할 수 있습니다:

```php
// Remove all of the global scopes...
User::withoutGlobalScopes()->get();

// Remove some of the global scopes...
User::withoutGlobalScopes([
    FirstScope::class, SecondScope::class
])->get();

// Remove all global scopes except the given ones...
User::withoutGlobalScopesExcept([
    SecondScope::class,
])->get();
```



<a name="local-scopes"></a>
### 로컬 스코프

로컬 스코프를 사용하면 애플리케이션 전반에서 쉽게 재사용할 수 있는 공통 쿼리 제약 조건 집합을 정의할 수 있습니다. 예를 들어, '인기 있는' 것으로 간주되는 모든 사용자를 자주 검색해야 할 수 있습니다. 스코프를 정의하려면 Eloquent 메서드에 `Scope` 속성을 추가하세요.

스코프는 항상 동일한 쿼리 빌더 인스턴스를 반환하거나 `void`를 반환해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include popular users.
     */
    #[Scope]
    protected function popular(Builder $query): void
    {
        $query->where('votes', '>', 100);
    }

    /**
     * Scope a query to only include active users.
     */
    #[Scope]
    protected function active(Builder $query): void
    {
        $query->where('active', 1);
    }
}
```



<a name="utilizing-a-local-scope"></a>
#### 로컬 스코프 활용

스코프가 정의되면 모델을 쿼리할 때 스코프 메서드를 호출할 수 있습니다. 다양한 스코프 호출을 체인으로 연결할 수도 있습니다:

```php
use App\Models\User;

$users = User::popular()->active()->orderBy('created_at')->get();
```



여러 Eloquent 모델 범위를 `or` 쿼리 연산자를 통해 결합하려면 올바른 [논리적 그룹화](/docs/{{version}}/queries#logical-grouping)를 달성하기 위해 클로저를 사용해야 할 수 있습니다:

```php
$users = User::popular()->orWhere(function (Builder $query) {
    $query->active();
})->get();
```



그러나 이것이 번거로울 수 있기 때문에, Laravel은 클로저를 사용하지 않고도 스코프를 유창하게 연결할 수 있는 "상위 계층" `orWhere` 메서드를 제공합니다:

```php
$users = User::popular()->orWhere->active()->get();
```



<a name="dynamic-scopes"></a>
#### 동적 스코프

가끔 파라미터를 받는 스코프를 정의하고 싶을 때가 있습니다. 시작하려면 스코프 메서드 시그니처에 추가 파라미터를 추가하면 됩니다. 스코프 파라미터는 `$query` 파라미터 뒤에 정의해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Scope a query to only include users of a given type.
     */
    #[Scope]
    protected function ofType(Builder $query, string $type): void
    {
        $query->where('type', $type);
    }
}
```



예상되는 인수들이 스코프 메서드의 서명에 추가되면, 스코프를 호출할 때 인수를 전달할 수 있습니다:

```php
$users = User::ofType('admin')->get();
```



속성(scope)이 지정된 메서드는 `protected`이어야 합니다. 모델 클래스 내에서 속성이 지정된 스코프를 호출할 때는 `static::query()->ofType('admin')`와 같은 쿼리 빌더 인스턴스를 통해 스코프를 호출하여 호출이 Eloquent의 스코프 처리 과정을 거치도록 하십시오.

<a name="pending-attributes"></a>
### 보류 중인 속성

스코프를 제한하는 데 사용된 속성과 동일한 속성을 가진 모델을 생성하기 위해 스코프를 사용하려는 경우 스코프 쿼리를 작성할 때 `withAttributes` 메서드를 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Scope;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * Scope the query to only include drafts.
     */
    #[Scope]
    protected function draft(Builder $query): void
    {
        $query->withAttributes([
            'hidden' => true,
        ]);
    }
}
```



`withAttributes` 메서드는 주어진 속성을 사용하여 쿼리에 `where` 조건을 추가하며, 스코프를 통해 생성된 모든 모델에도 주어진 속성을 추가합니다:

```php
$draft = Post::draft()->create(['title' => 'In Progress']);

$draft->hidden; // true
```



쿼리에 `where` 조건을 추가하지 않도록 `withAttributes` 메서드를 지시하려면 `asConditions` 인수를 `false`로 설정할 수 있습니다:

```php
$query->withAttributes([
    'hidden' => true,
], asConditions: false);
```



<a name="comparing-models"></a>
## 모델 비교

때때로 두 모델이 "같은" 것인지 아닌지를 확인해야 할 때가 있습니다. `is` 및 `isNot` 방법은 두 모델이 동일한 기본 키, 테이블 및 데이터베이스 연결을 가지고 있는지 여부를 빠르게 확인하는 데 사용할 수 있습니다:

```php
if ($post->is($anotherPost)) {
    // ...
}

if ($post->isNot($anotherPost)) {
    // ...
}
```



`belongsTo`, `hasOne`, `morphTo` 및 `morphOne` [관계](/docs/{{version}}/eloquent-relationships)를 사용할 때 `is` 및 `isNot` 메서드도 사용할 수 있습니다. 이 메서드는 해당 모델을 가져오기 위한 쿼리를 실행하지 않고 관련 모델을 비교하고자 할 때 특히 유용합니다:

```php
if ($post->author()->is($user)) {
    // ...
}
```



<a name="events"></a>
## Events

> [!NOTE]
> Want to broadcast your Eloquent events directly to your client-side application? Check out Laravel's [model event broadcasting](/docs/{{version}}/broadcasting#model-broadcasting).

Eloquent models dispatch several events, allowing you to hook into the following moments in a model's lifecycle: `retrieved`, `creating`, `created`, `updating`, `updated`, `saving`, `saved`, `deleting`, `deleted`, `trashed`, `forceDeleting`, `forceDeleted`, `restoring`, `restored`, and `replicating`.

The `retrieved` event will dispatch when an existing model is retrieved from the database. When a new model is saved for the first time, the `creating` and `created` events will dispatch. The `updating` / `updated` events will dispatch when an existing model is modified and the `save` method is called. The `saving` / `saved` events will dispatch when a model is created or updated - even if the model's attributes have not been changed. Event names ending with `-ing` are dispatched before any changes to the model are persisted, while events ending with `-ed` are dispatched after the changes to the model are persisted.

To start listening to model events, define a `$dispatchesEvents` property on your Eloquent model. This property maps various points of the Eloquent model's lifecycle to your own [event classes](/docs/{{version}}/events). Each model event class should expect to receive an instance of the affected model via its constructor:

```php
<?php

namespace App\Models;

use App\Events\UserDeleted;
use App\Events\UserSaved;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The event map for the model.
     *
     * @var array<string, string>
     */
    protected $dispatchesEvents = [
        'saved' => UserSaved::class,
        'deleted' => UserDeleted::class,
    ];
}
```



Eloquent 이벤트를 정의하고 매핑한 후에는 [이벤트 리스너](/docs/{{version}}/events#defining-listeners)를 사용하여 이벤트를 처리할 수 있습니다.

> [!WARNING]
> Eloquent를 통해 대량 업데이트 또는 삭제 쿼리를 실행할 때, `saved`, `updated`, `deleting` 및 `deleted` 모델 이벤트는 영향을 받는 모델에 대해 발생하지 않습니다. 이는 대량 업데이트나 삭제를 수행할 때 모델이 실제로 가져와지지 않기 때문입니다.

<a name="events-using-closures"></a>
### 클로저 사용

사용자 정의 이벤트 클래스를 사용하는 대신, 다양한 모델 이벤트가 발생할 때 실행되는 클로저를 등록할 수 있습니다. 일반적으로 이러한 클로저는 모델의 `booted` 메서드에서 등록해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::created(function (User $user) {
            // ...
        });
    }
}
```



필요한 경우, 모델 이벤트를 등록할 때 [큐 가능한 익명 이벤트 리스너](/docs/{{version}}/events#queueable-anonymous-event-listeners)를 활용할 수 있습니다. 이는 Laravel에게 모델 이벤트 리스너를 애플리케이션의 [큐](/docs/{{version}}/queues)를 사용하여 백그라운드에서 실행하도록 지시합니다:

```php
use function Illuminate\Events\queueable;

static::created(queueable(function (User $user) {
    // ...
}));
```



<a name="observers"></a>
### 옵저버

<a name="defining-observers"></a>
#### 옵저버 정의하기

특정 모델에서 많은 이벤트를 감지하려는 경우, 옵저버를 사용하여 모든 리스너를 하나의 클래스로 그룹화할 수 있습니다. 옵저버 클래스에는 리스닝하려는 Eloquent 이벤트를 반영하는 메서드 이름이 있습니다. 각 메서드는 영향을 받은 모델을 유일한 인수로 받습니다. `make:observer` Artisan 명령어는 새 옵저버 클래스를 만드는 가장 쉬운 방법입니다:

```shell
php artisan make:observer UserObserver --model=User
```



이 명령은 새 관찰자를 `app/Observers` 디렉토리에 배치합니다. 이 디렉토리가 존재하지 않으면 Artisan이 대신 생성합니다. 새 관찰자는 다음과 같이 보일 것입니다:

```php
<?php

namespace App\Observers;

use App\Models\User;

class UserObserver
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "updated" event.
     */
    public function updated(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "deleted" event.
     */
    public function deleted(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "restored" event.
     */
    public function restored(User $user): void
    {
        // ...
    }

    /**
     * Handle the User "forceDeleted" event.
     */
    public function forceDeleted(User $user): void
    {
        // ...
    }
}
```



옵저버를 등록하려면 해당 모델에 `ObservedBy` 속성을 지정할 수 있습니다:

```php
use App\Observers\UserObserver;
use Illuminate\Database\Eloquent\Attributes\ObservedBy;

#[ObservedBy([UserObserver::class])]
class User extends Authenticatable
{
    //
}
```



또는, 관찰하려는 모델에서 `observe` 메서드를 호출하여 관찰자를 수동으로 등록할 수 있습니다. 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드에서 관찰자를 등록할 수 있습니다:

```php
use App\Models\User;
use App\Observers\UserObserver;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    User::observe(UserObserver::class);
}
```



> [!NOTE]
> 관찰자가 `saving` 및 `retrieved`와 같은 추가 이벤트를 수신할 수 있습니다. 이러한 이벤트는 [events](#events) 문서에 설명되어 있습니다.

<a name="observers-and-database-transactions"></a>
#### 관찰자와 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 모델이 생성될 때, 관찰자가 데이터베이스 트랜잭션이 커밋된 후에만 이벤트 핸들러를 실행하도록 지시하고 싶을 수 있습니다. 이는 관찰자에서 `ShouldHandleEventsAfterCommit` 인터페이스를 구현하여 달성할 수 있습니다. 데이터베이스 트랜잭션이 진행 중이 아닌 경우, 이벤트 핸들러는 즉시 실행됩니다:

```php
<?php

namespace App\Observers;

use App\Models\User;
use Illuminate\Contracts\Events\ShouldHandleEventsAfterCommit;

class UserObserver implements ShouldHandleEventsAfterCommit
{
    /**
     * Handle the User "created" event.
     */
    public function created(User $user): void
    {
        // ...
    }
}
```



<a name="muting-events"></a>
### 이벤트 음소거

가끔 모델에서 발생하는 모든 이벤트를 일시적으로 "음소거"해야 할 필요가 있습니다. 이를 위해 `withoutEvents` 메서드를 사용할 수 있습니다. `withoutEvents` 메서드는 클로저를 유일한 인수로 받습니다. 이 클로저 내에서 실행되는 모든 코드는 모델 이벤트를 발송하지 않으며, 클로저가 반환하는 값은 `withoutEvents` 메서드에 의해 반환됩니다:

```php
use App\Models\User;

$user = User::withoutEvents(function () {
    User::findOrFail(1)->delete();

    return User::find(2);
});
```



<a name="saving-a-single-model-without-events"></a>
#### 이벤트 없이 단일 모델 저장하기

때때로 어떤 모델을 이벤트를 발생시키지 않고 "저장"하고 싶을 수 있습니다. 이것은 `saveQuietly` 메서드를 사용하여 수행할 수 있습니다:

```php
$user = User::findOrFail(1);

$user->name = 'Victoria Faith';

$user->saveQuietly();
```



이벤트를 발생시키지 않고도 주어진 모델을 '업데이트', '삭제', '소프트 삭제', '복원', '복제'할 수 있습니다:

```php
$user->deleteQuietly();
$user->forceDeleteQuietly();
$user->restoreQuietly();
```
{% endraw %}
