---
layout: docs
title: "Laravel Scout"
---

{% raw %}
# Laravel Scout

- [Introduction](#introduction)
- [Installation](#installation)
    - [Queueing](#queueing)
- [Driver Prerequisites](#driver-prerequisites)
    - [Algolia](#algolia)
    - [Meilisearch](#meilisearch)
    - [Typesense](#typesense)
    - [Turbopuffer](#turbopuffer)
- [Configuration](#configuration)
    - [Configuring Searchable Data](#configuring-searchable-data)
- [Database / Collection Engines](#database-and-collection-engines)
    - [Database Engine](#database-engine)
    - [Collection Engine](#collection-engine)
- [Third-Party Engine Configuration](#third-party-engine-configuration)
    - [Configuring Model Indexes](#configuring-model-indexes)
    - [Algolia](#algolia-configuration)
    - [Meilisearch](#meilisearch-configuration)
    - [Typesense](#typesense-configuration)
    - [Turbopuffer](#turbopuffer-configuration)
- [Third-Party Engine Indexing](#indexing)
    - [Batch Import](#batch-import)
    - [Adding Records](#adding-records)
    - [Updating Records](#updating-records)
    - [Removing Records](#removing-records)
    - [Pausing Indexing](#pausing-indexing)
    - [Conditionally Searchable Model Instances](#conditionally-searchable-model-instances)
- [Searching](#searching)
    - [Where Clauses](#where-clauses)
    - [Semantic Search](#semantic-search)
    - [Pagination](#pagination)
    - [Soft Deleting](#soft-deleting)
    - [Customizing Engine Searches](#customizing-engine-searches)
- [Custom Engines](#custom-engines)

<a name="introduction"></a>
## Introduction

[Laravel Scout](https://github.com/laravel/scout) provides a simple, driver-based solution for adding full-text search to your [Eloquent models](/docs/{{version}}/eloquent). Using model observers, Scout will automatically keep your search indexes in sync with your Eloquent records.

Scout ships with a built-in `database` engine that uses MySQL / PostgreSQL full-text indexes and `LIKE` clauses to search your existing database — no external service required. For most applications, this is all you need. For an overview of all search options available in Laravel, consult the [search documentation](/docs/{{version}}/search).



Scout는 또한 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com), [Typesense](https://typesense.org), 그리고 [Turbopuffer](https://turbopuffer.com)에 대한 드라이버를 포함하고 있어, 오타 허용, 계층형 필터링, 벡터 검색, 또는 대규모 지리 검색 같은 기능이 필요할 때 사용할 수 있습니다. 로컬 개발을 위한 "컬렉션" 드라이버도 제공되며, [사용자 정의 엔진](#custom-engines)을 작성할 수도 있습니다.

<a name="installation"></a>
## 설치

먼저, Composer 패키지 관리자를 통해 Scout를 설치합니다:

```shell
composer require laravel/scout
```



Scout를 설치한 후, `vendor:publish` Artisan 명령어를 사용하여 Scout 구성 파일을 게시해야 합니다. 이 명령어는 `scout.php` 구성 파일을 애플리케이션의 `config` 디렉터리에 게시합니다:

```shell
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```



마지막으로, 검색 가능하게 만들고 싶은 모델에 `Laravel\Scout\Searchable` 트레이트를 추가하세요. 이 트레이트는 모델 옵저버를 등록하여 모델이 검색 드라이버와 자동으로 동기화되도록 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;
}
```



<a name="queueing"></a>
### 큐잉

`database` 또는 `collection` 엔진이 아닌 엔진을 사용할 경우, 라이브러리를 사용하기 전에 [큐 드라이버](/docs/{{version}}/queues)를 구성하는 것을 강력히 고려해야 합니다. 큐 워커를 실행하면 Scout이 모델 정보를 검색 인덱스로 동기화하는 모든 작업을 큐에 넣을 수 있어, 애플리케이션 웹 인터페이스의 응답 시간을 훨씬 개선할 수 있습니다.

큐 드라이버를 구성한 후에는 `config/scout.php` 구성 파일에서 `queue` 옵션의 값을 `true`로 설정하십시오:

```php
'queue' => true,
```



`queue` 옵션이 `false`로 설정되어 있더라도, Algolia나 Meilisearch와 같은 일부 Scout 드라이버는 항상 레코드를 비동기적으로 인덱싱한다는 점을 기억하는 것이 중요합니다. 다시 말해, 인덱스 작업이 Laravel 애플리케이션 내에서 완료되었더라도 검색 엔진 자체가 새로운 업데이트된 레코드를 즉시 반영하지 않을 수 있습니다.

Scout 작업에서 사용할 연결과 큐를 지정하려면, `queue` 설정 옵션을 배열로 정의할 수 있습니다:

```php
'queue' => [
    'connection' => 'redis',
    'queue' => 'scout'
],
```



물론, Scout 작업이 사용하는 연결과 큐를 사용자 지정하는 경우, 해당 연결과 큐에서 작업을 처리하기 위해 큐 워커를 실행해야 합니다:

```shell
php artisan queue:work redis --queue=scout
```



<a name="unique-jobs"></a>
#### 유일한 작업

쓰기 중심의 애플리케이션에서는 Scout가 동일한 모델 레코드에 대해 중복 작업을 대기열에 추가하지 않도록 하길 원할 수 있습니다. 일반적으로 서비스 제공자의 `boot` 메서드 내에서 `MakeSearchableUniquely` 및 `RemoveFromSearchUniquely` 작업 클래스를 등록하여 유일한 인덱싱 작업을 선택할 수 있습니다:

```php
use Laravel\Scout\Jobs\MakeSearchableUniquely;
use Laravel\Scout\Jobs\RemoveFromSearchUniquely;
use Laravel\Scout\Scout;

Scout::makeSearchableUsing(MakeSearchableUniquely::class);
Scout::removeFromSearchUsing(RemoveFromSearchUniquely::class);
```



이 작업들은 Laravel의 [고유 작업 잠금](/docs/{{version}}/queues#unique-jobs)을 사용하여 동일한 검색 가능한 모델 레코드에 대해 이미 일치하는 작업이 큐에 있는 동안 중복된 큐 인덱싱 작업이 디스패치되지 않도록 합니다.

<a name="driver-prerequisites"></a>
## 드라이버 전제 조건

<a name="algolia"></a>
### Algolia

Algolia 드라이버를 사용할 때는 Algolia `id` 및 `secret` 자격 증명을 `config/scout.php` 구성 파일에 설정해야 합니다. 자격 증명이 설정되면 Composer 패키지 관리자를 통해 Algolia PHP SDK도 설치해야 합니다:

```shell
composer require algolia/algoliasearch-client-php
```



<a name="meilisearch"></a>
### Meilisearch

[Meilisearch](https://www.meilisearch.com)는 빠르고 오픈 소스 검색 엔진입니다. 로컬 컴퓨터에 Meilisearch를 설치하는 방법을 확실히 모른다면, Laravel의 공식 지원 Docker 개발 환경인 [Laravel Sail](/docs/{{version}}/sail#meilisearch)을 사용할 수 있습니다.

Meilisearch 드라이버를 사용할 때는 Composer 패키지 관리자를 통해 Meilisearch PHP SDK를 설치해야 합니다:

```shell
composer require meilisearch/meilisearch-php http-interop/http-factory-guzzle
```



그런 다음, 애플리케이션의 `.env` 파일 내에서 `SCOUT_DRIVER` 환경 변수와 Meilisearch `host` 및 `key` 자격 증명을 설정하십시오:

```ini
SCOUT_DRIVER=meilisearch
MEILISEARCH_HOST=http://127.0.0.1:7700
MEILISEARCH_KEY=masterKey
```



Meilisearch에 대한 자세한 정보는 [Meilisearch 문서](https://docs.meilisearch.com/learn/getting_started/quick_start.html)를 참조하십시오.

또한, Meilisearch 바이너리 버전과 호환되는 `meilisearch/meilisearch-php` 버전을 설치했는지 확인하려면 [바이너리 호환성에 관한 Meilisearch 문서](https://github.com/meilisearch/meilisearch-php#-compatibility-with-meilisearch)를 검토하십시오.

> [!WARNING]
> Meilisearch를 사용하는 애플리케이션에서 Scout를 업그레이드할 때, 항상 Meilisearch 서비스 자체의 [추가적인 Breaking Changes](https://github.com/meilisearch/Meilisearch/releases)를 검토해야 합니다.

<a name="typesense"></a>
### Typesense

[Typesense](https://typesense.org)는 매우 빠른 오픈 소스 검색 엔진으로, 키워드 검색, 의미 검색, 지리 검색, 벡터 검색을 지원합니다.

Typesense를 [셀프 호스팅](https://typesense.org/docs/guide/install-typesense.html#option-2-local-machine-self-hosting)하거나 [Typesense Cloud](https://cloud.typesense.org)를 사용할 수 있습니다.

Scout와 함께 Typesense를 사용하려면 Composer 패키지 관리자를 통해 Typesense PHP SDK를 설치하십시오:

```shell
composer require typesense/typesense-php
```



그런 다음, 애플리케이션의 .env 파일 내에서 `SCOUT_DRIVER` 환경 변수와 Typesense 호스트 및 API 키 자격 증명을 설정하세요:

```ini
SCOUT_DRIVER=typesense
TYPESENSE_API_KEY=masterKey
TYPESENSE_HOST=localhost
```



만약 [Laravel Sail](/docs/{{version}}/sail)을 사용하고 있다면, Docker 컨테이너 이름과 일치하도록 `TYPESENSE_HOST` 환경 변수를 조정해야 할 수도 있습니다. 또한 선택적으로 설치의 포트, 경로 및 프로토콜을 지정할 수 있습니다:

```ini
TYPESENSE_PORT=8108
TYPESENSE_PATH=
TYPESENSE_PROTOCOL=http
```



Typesense 컬렉션에 대한 추가 설정 및 스키마 정의는 애플리케이션의 `config/scout.php` 구성 파일에서 찾을 수 있습니다. Typesense에 대한 자세한 정보는 [Typesense 문서](https://typesense.org/docs/guide/#quick-start)를 참조하십시오.

<a name="turbopuffer"></a>
### 터보퍼퍼(Turbopuffer)

[Turbopuffer](https://turbopuffer.com)는 전체 텍스트, 의미 기반 및 하이브리드 검색을 지원하는 검색 엔진입니다. Turbopuffer 드라이버를 사용하려면 `SCOUT_DRIVER` 환경 변수를 설정하고 Turbopuffer API 키를 제공하십시오:

```ini
SCOUT_DRIVER=turbopuffer
TURBOPUFFER_API_KEY=tpuf_...
TURBOPUFFER_REGION=gcp-us-central1
```



`TURBOPUFFER_REGION` 환경 변수는 선택 사항이며 기본값은 `gcp-us-central1`입니다.

<a name="configuration"></a>
## 구성

<a name="configuring-searchable-data"></a>
### 검색 가능한 데이터 구성

기본적으로 주어진 모델의 전체 `toArray` 형태가 검색 인덱스에 저장됩니다. 검색 인덱스로 동기화되는 데이터를 맞춤 설정하려면 모델에서 `toSearchableArray` 메서드를 재정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the indexable data array for the model.
     *
     * @return array<string, mixed>
     */
    public function toSearchableArray(): array
    {
        $array = $this->toArray();

        // Customize the data array...

        return $array;
    }
}
```



<a name="configuring-search-engines-per-model"></a>
#### 모델 엔진 구성

검색할 때, Scout는 일반적으로 애플리케이션의 `scout` 구성 파일에 지정된 기본 검색 엔진을 사용합니다. 그러나 특정 모델의 검색 엔진은 모델에서 `searchableUsing` 메서드를 재정의하여 변경할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Engines\Engine;
use Laravel\Scout\Scout;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the engine used to index the model.
     */
    public function searchableUsing(): Engine
    {
        return Scout::engine('meilisearch');
    }
}
```



<a name="database-and-collection-engines"></a>
## 데이터베이스 / 컬렉션 엔진

<a name="database-engine"></a>
### 데이터베이스 엔진

> [!WARNING]
> 현재 데이터베이스 엔진은 MySQL과 PostgreSQL을 지원하며, 두 데이터베이스 모두 빠른 전체 텍스트 컬럼 인덱싱을 제공합니다.

`database` 엔진은 MySQL / PostgreSQL 전체 텍스트 인덱스와 `LIKE` 절을 사용하여 기존 데이터베이스를 직접 검색합니다. 많은 응용 프로그램에서 이는 검색을 추가하는 가장 간단하고 실용적인 방법으로, 외부 서비스나 추가 인프라가 필요하지 않습니다.

데이터베이스 엔진을 사용하려면, `SCOUT_DRIVER` 환경 변수를 `database`로 설정하세요:

```ini
SCOUT_DRIVER=database
```



한 번 구성하면 [검색 가능한 데이터를 정의](#configuring-searchable-data)하고 모델에 대해 [검색 쿼리를 실행](#searching)할 수 있습니다. 서드파티 엔진과 달리, 데이터베이스 엔진은 별도의 인덱싱 단계가 필요하지 않으며 — 데이터베이스 테이블을 직접 검색합니다.

<a name="database-semantic-and-hybrid-search"></a>
#### 의미 기반 검색 및 하이브리드 검색

데이터베이스 엔진은 PostgreSQL에서 `pgvector` 확장을 사용할 때 의미 기반 검색과 하이브리드 검색을 지원합니다. 시작하려면, 모델의 테이블에 null 허용 벡터 컬럼과 전문 검색(full-text) 인덱스를 추가하십시오. 벡터 컬럼은 Scout가 모델이 저장된 후 임베딩을 저장하기 때문에 null 허용이어야 합니다:

```php
Schema::ensureVectorExtensionExists();

Schema::table('articles', function (Blueprint $table) {
    // ...

    $table->vector('embedding', dimensions: 1536)->nullable();
    $table->vectorIndex('embedding');
    $table->fullText(['title', 'body']);
});
```



다음으로, 모델에서 `toSearchableEmbedding` 메서드를 정의합니다. 이 메서드는 Scout가 임베딩해야 할 소스 텍스트나 미리 계산된 임베딩 배열을 반환할 수 있습니다. Scout는 기본적으로 임베딩을 `embedding` 열에 저장하며, 다른 열을 사용하려면 모델에서 `searchableEmbeddingColumn` 메서드를 정의하십시오.

#### 데이터베이스 검색 전략 사용자 정의

기본적으로 데이터베이스 엔진은 [검색 가능하도록 구성한](#configuring-searchable-data) 모든 모델 속성에 대해 `LIKE` 쿼리를 실행합니다. 그러나 특정 열에 대해 더 효율적인 검색 전략을 지정할 수 있습니다. `SearchUsingFullText` 속성은 해당 열에 대해 데이터베이스의 전체 텍스트 인덱스를 사용하고, `SearchUsingPrefix`는 문자열의 시작 부분(`example%`)만 일치시키며 전체 문자열(`%example%`) 내 검색 대신 사용합니다.

이 동작을 정의하려면 모델의 `toSearchableArray` 메서드에 PHP 속성을 지정하십시오. 속성이 없는 열은 계속 기본 `LIKE` 전략을 사용합니다.

```php
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;

/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
#[SearchUsingPrefix(['id', 'email'])]
#[SearchUsingFullText(['bio'])]
public function toSearchableArray(): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'bio' => $this->bio,
    ];
}
```



> [!WARNING]
> 컬럼이 전체 텍스트 쿼리 제약 조건을 사용하도록 지정하기 전에, 해당 컬럼에 [전체 텍스트 인덱스](/docs/{{version}}/migrations#available-index-types)가 할당되어 있는지 확인하십시오.

<a name="collection-engine"></a>
### 컬렉션 엔진

"컬렉션" 엔진은 빠른 프로토타입, 매우 작은 데이터셋(수백 개 레코드) 또는 테스트 실행을 위해 설계되었습니다. 데이터베이스에서 가능한 모든 레코드를 가져오고 Laravel의 `Str::is` 헬퍼를 사용하여 PHP에서 필터링하므로, 인덱싱이나 데이터베이스 특정 기능이 필요하지 않습니다. 사소한 사용 사례를 넘어서는 경우에는 대신 [데이터베이스 엔진](#database-engine)을 사용하는 것이 좋습니다.

컬렉션 엔진을 사용하려면 `SCOUT_DRIVER` 환경 변수의 값을 단순히 `collection`로 설정하거나, 애플리케이션의 `scout` 구성 파일에서 `collection` 드라이버를 직접 지정하면 됩니다:

```ini
SCOUT_DRIVER=collection
```



Once you have specified the collection driver as your preferred driver, you may start [executing search queries](#searching) against your models. Search engine indexing, such as the indexing needed to seed Algolia, Meilisearch, or Typesense indexes, is unnecessary when using the collection engine.

#### Differences From Database Engine

While the database engine uses full-text indexes and `LIKE` clauses to find matching records efficiently, the collection engine pulls all records and filters them in PHP. The collection engine is the most portable option as it works across all relational databases supported by Laravel (including SQLite and SQL Server); however, it is significantly less efficient than the database engine and should not be used with large datasets.

<a name="third-party-engine-configuration"></a>
## Third-Party Engine Configuration

The following configuration options are only relevant when using a third-party search engine such as Algolia, Meilisearch, or Typesense. If you are using the [database engine](#database-engine), you may skip this section.

<a name="configuring-model-indexes"></a>
### Configuring Model Indexes

When using a third-party engine, each Eloquent model is synced with a given search "index", which contains all of the searchable records for that model. By default, each model will be persisted to an index matching the model's typical "table" name. Typically, this is the plural form of the model name; however, you are free to customize the model's index by overriding the `searchableAs` method on the model:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Post extends Model
{
    use Searchable;

    /**
     * Get the name of the index associated with the model.
     */
    public function searchableAs(): string
    {
        return 'posts_index';
    }
}
```



> [!NOTE]
> `searchableAs` 메서드는 데이터베이스 엔진을 사용할 때 효과가 없으며, 데이터베이스 엔진은 항상 모델의 데이터베이스 테이블을 직접 검색합니다.

<a name="configuring-the-model-id"></a>
#### 모델 ID 구성

기본적으로 Scout는 모델의 기본 키를 검색 인덱스에 저장되는 모델의 고유 ID/키로 사용합니다. 서드파티 엔진을 사용할 때 이 동작을 사용자 정의해야 하는 경우, 모델에서 `getScoutKey`와 `getScoutKeyName` 메서드를 재정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class User extends Model
{
    use Searchable;

    /**
     * Get the value used to index the model.
     */
    public function getScoutKey(): mixed
    {
        return $this->email;
    }

    /**
     * Get the key name used to index the model.
     */
    public function getScoutKeyName(): mixed
    {
        return 'email';
    }
}
```



> [!NOTE]
> 데이터베이스 엔진을 사용할 때 `getScoutKey` 및 `getScoutKeyName` 메서드는 효과가 없으며, 데이터베이스 엔진은 항상 모델의 기본 키를 사용합니다.

<a name="algolia-configuration"></a>
### Algolia

<a name="algolia-index-settings"></a>
#### 인덱스 설정

때때로 Algolia 인덱스에서 추가 설정을 구성하고 싶을 수 있습니다. 이러한 설정은 Algolia UI를 통해 관리할 수 있지만, 애플리케이션의 `config/scout.php` 설정 파일에서 직접 인덱스 구성의 원하는 상태를 관리하는 것이 더 효율적일 때도 있습니다.

이 접근 방식은 애플리케이션의 자동화된 배포 파이프라인을 통해 설정을 배포할 수 있게 하여 수동 구성을 피하고 여러 환경에서 일관성을 보장합니다. 필터링 가능한 속성, 순위, 페이싱 또는 [그 밖의 지원되는 설정](https://www.algolia.com/doc/rest-api/search/#tag/Indices/operation/setSettings)을 구성할 수 있습니다.

시작하려면, 애플리케이션의 `config/scout.php` 설정 파일에서 각 인덱스에 대한 설정을 추가하십시오:

```php
use App\Models\User;
use App\Models\Flight;

'algolia' => [
    'id' => env('ALGOLIA_APP_ID', ''),
    'secret' => env('ALGOLIA_SECRET', ''),
    'index-settings' => [
        User::class => [
            'searchableAttributes' => ['id', 'name', 'email'],
            'attributesForFaceting'=> ['filterOnly(email)'],
            // Other settings fields...
        ],
        Flight::class => [
            'searchableAttributes'=> ['id', 'destination'],
        ],
    ],
],
```



주어진 인덱스의 기반 모델이 소프트 삭제 가능하고 `index-settings` 배열에 포함되어 있는 경우, Scout는 해당 인덱스에서 소프트 삭제된 모델에 대한 페이싱 지원을 자동으로 포함합니다. 소프트 삭제 가능한 모델 인덱스에 대해 정의할 다른 페이싱 속성이 없다면, 단순히 해당 모델에 대해 `index-settings` 배열에 빈 항목을 추가하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```



애플리케이션의 인덱스 설정을 구성한 후에는 `scout:sync-index-settings` Artisan 명령을 실행해야 합니다. 이 명령은 현재 구성된 인덱스 설정을 Algolia에 알립니다. 편의를 위해, 이 명령을 배포 프로세스의 일부로 만들고 싶을 수도 있습니다:

```shell
php artisan scout:sync-index-settings
```



<a name="algolia-identifying-users"></a>
#### 사용자 식별

Scout는 Algolia를 사용할 때 사용자를 자동으로 식별할 수 있도록 합니다. 인증된 사용자를 검색 작업과 연결하면 Algolia 대시보드에서 검색 분석을 볼 때 유용할 수 있습니다. 애플리케이션의 `.env` 파일에서 `SCOUT_IDENTIFY` 환경 변수를 `true`로 정의하여 사용자 식별을 활성화할 수 있습니다:

```ini
SCOUT_IDENTIFY=true
```



이 기능을 활성화하면 요청의 IP 주소와 인증된 사용자의 주요 식별자가 Algolia로 전달되어, 사용자가 수행하는 모든 검색 요청에 이 데이터가 연결됩니다.

<a name="meilisearch-configuration"></a>
### Meilisearch

<a name="meilisearch-index-settings"></a>
#### 인덱스 설정

Meilisearch는 필터링 가능한 속성, 정렬 가능한 속성 및 [기타 지원되는 설정 필드](https://docs.meilisearch.com/reference/api/settings.html)와 같은 인덱스 검색 설정을 미리 정의해야 합니다.

필터링 가능한 속성은 Scout의 `where` 메서드를 호출할 때 필터링할 계획이 있는 속성이며, 정렬 가능한 속성은 Scout의 `orderBy` 메서드를 호출할 때 정렬할 계획이 있는 속성입니다. 인덱스 설정을 정의하려면 애플리케이션의 `scout` 설정 파일에서 `meilisearch` 구성 항목의 `index-settings` 부분을 조정하세요:

```php
use App\Models\User;
use App\Models\Flight;

'meilisearch' => [
    'host' => env('MEILISEARCH_HOST', 'http://localhost:7700'),
    'key' => env('MEILISEARCH_KEY', null),
    'index-settings' => [
        User::class => [
            'filterableAttributes'=> ['id', 'name', 'email'],
            'sortableAttributes' => ['created_at'],
            // Other settings fields...
        ],
        Flight::class => [
            'filterableAttributes'=> ['id', 'destination'],
            'sortableAttributes' => ['updated_at'],
        ],
    ],
],
```



주어진 인덱스의 기반 모델이 소프트 삭제 가능하고 `index-settings` 배열에 포함되어 있는 경우, Scout는 해당 인덱스에서 소프트 삭제된 모델에 대한 필터링 지원을 자동으로 포함합니다. 소프트 삭제 가능 모델 인덱스에 대해 정의할 다른 필터 가능하거나 정렬 가능한 속성이 없는 경우, 해당 모델에 대해 `index-settings` 배열에 빈 항목을 추가하기만 하면 됩니다:

```php
'index-settings' => [
    Flight::class => []
],
```



애플리케이션의 인덱스 설정을 구성한 후에는 `scout:sync-index-settings` Artisan 명령을 실행해야 합니다. 이 명령은 현재 구성된 인덱스 설정을 Meilisearch에 알립니다. 편의를 위해 이 명령을 배포 과정에 포함시키는 것을 고려할 수 있습니다:

```shell
php artisan scout:sync-index-settings
```



<a name="meilisearch-semantic-and-hybrid-search"></a>
#### 의미 기반 및 하이브리드 검색

Meilisearch에서 의미 기반 또는 하이브리드 검색을 사용하려면, 검색 가능한 각 모델에 대해 인덱스 설정과 임베딩 설정에서 임베더를 구성하세요:

```php
'meilisearch' => [
    // ...
    'index-settings' => [
        Article::class => [
            'embedders' => [
                'default' => [
                    'source' => 'userProvided',
                    'dimensions' => 1536,
                ],
            ],
        ],
    ],
    'model-settings' => [
        Article::class => [
            'embedding' => [
                'embedder' => 'default',
                'dimensions' => 1536,
            ],
        ],
    ],
],
```



모델의 `toSearchableEmbedding` 메서드는 소스 텍스트를 반환할 수 있으며, Scout는 이를 [Laravel AI SDK](/docs/{{version}}/ai-sdk)를 사용해 임베딩하거나, 미리 계산된 임베딩 배열을 사용할 수 있습니다. 구성 업데이트 후에는 `scout:sync-index-settings` 명령을 실행하십시오.

또는 embedding `driver`를 `meilisearch`로 설정하여 Meilisearch의 기본 임베딩을 사용할 수도 있습니다. 이 모드에서는 Meilisearch가 구성된 임베더를 사용하여 문서 및 쿼리 임베딩을 생성하므로 `dimensions` 옵션과 `toSearchableEmbedding` 메서드는 필요하지 않습니다.

```php
'meilisearch' => [
    'index-settings' => [
        Article::class => [
            'embedders' => [
                'default' => [
                    'source' => 'openAi',
                    'apiKey' => env('OPENAI_API_KEY'),
                    'model' => 'text-embedding-3-small',
                    'documentTemplate' => 'An article titled {{ doc.title }}: {{ doc.body }}',
                ],
            ],
        ],
    ],
    'model-settings' => [
        Article::class => [
            'embedding' => [
                'embedder' => 'default',
                'driver' => 'meilisearch',
            ],
        ],
    ],
],
```



네이티브 임베딩을 사용할 때, Scout는 인덱싱된 문서에 벡터를 생성하거나 추가하지 않습니다. `vector` 검색 옵션을 사용하여 미리 계산된 쿼리 벡터를 제공할 수 있습니다.

<a name="meilisearch-data-types"></a>
#### 검색 가능한 데이터 유형

Meilisearch는 올바른 유형의 데이터에서만 필터 연산(`>`, `<` 등)을 수행합니다. 검색 가능한 데이터를 맞춤 설정할 때, 숫자 값을 올바른 유형으로 캐스팅했는지 확인해야 합니다:

```php
public function toSearchableArray()
{
    return [
        'id' => (int) $this->id,
        'name' => $this->name,
        'price' => (float) $this->price,
    ];
}
```



<a name="typesense-configuration"></a>
### Typesense

<a name="typesense-searchable-data"></a>
#### 검색 가능한 데이터 준비

Typesense를 사용할 때, 검색 가능한 모델은 모델의 기본 키를 문자열로, 생성일을 UNIX 타임스탬프로 변환하는 `toSearchableArray` 메서드를 정의해야 합니다:

```php
/**
 * Get the indexable data array for the model.
 *
 * @return array<string, mixed>
 */
public function toSearchableArray(): array
{
    return array_merge($this->toArray(),[
        'id' => (string) $this->id,
        'created_at' => $this->created_at->timestamp,
    ]);
}
```



애플리케이션의 `config/scout.php` 파일에서 Typesense 컬렉션 스키마를 정의해야 합니다. 컬렉션 스키마는 Typesense를 통해 검색 가능한 각 필드의 데이터 유형을 설명합니다. 모든 사용 가능한 스키마 옵션에 대한 자세한 내용은 [Typesense 문서](https://typesense.org/docs/latest/api/collections.html#schema-parameters)를 참조하시기 바랍니다.

Typesense 컬렉션의 스키마를 정의한 후에 변경해야 하는 경우, 기존 인덱스 데이터를 모두 삭제하고 스키마를 재생성하는 `scout:flush`와 `scout:import`를 실행할 수 있습니다. 또는 인덱스된 데이터를 제거하지 않고 Typesense API를 사용하여 컬렉션 스키마를 수정할 수도 있습니다.

검색 가능한 모델이 소프트 삭제 가능하다면, 애플리케이션의 `config/scout.php` 구성 파일 내 모델에 해당하는 Typesense 스키마에서 `__soft_deleted` 필드를 정의해야 합니다:

```php
User::class => [
    'collection-schema' => [
        'fields' => [
            // ...
            [
                'name' => '__soft_deleted',
                'type' => 'int32',
                'optional' => true,
            ],
        ],
    ],
],
```



<a name="typesense-embeddings"></a>
#### 임베딩

의미 기반 및 하이브리드 검색을 활성화하려면 모델의 Typesense 구성에서 `embedding` 설정과 벡터 필드를 정의하십시오. 기본적으로 Scout는 임베딩을 생성하기 위해 [Laravel AI SDK](/docs/{{version}}/ai-sdk)를 사용합니다:

```php
use App\Models\Article;

'model-settings' => [
    Article::class => [
        'collection-schema' => [
            'fields' => [
                ['name' => 'title', 'type' => 'string'],
                ['name' => 'embedding', 'type' => 'float[]', 'num_dim' => 1536],
            ],
        ],
        'search-parameters' => ['query_by' => 'title'],
        'embedding' => [
            'attribute' => 'embedding',
            'dimensions' => 1536,
        ],
    ],
],
```



귀하의 모델 `toSearchableEmbedding` 메서드는 Scout가 임베드해야 할 원본 텍스트 또는 미리 계산된 임베딩 배열을 반환해야 합니다:

```php
public function toSearchableEmbedding(): string|array
{
    return $this->title.' '.$this->body;
}
```



<a name="typesense-dynamic-search-parameters"></a>
#### 동적 검색 매개변수

Typesense는 `options` 방법을 통해 검색 작업을 수행할 때 [검색 매개변수](https://typesense.org/docs/latest/api/search.html#search-parameters)를 동적으로 수정할 수 있습니다:

```php
use App\Models\Todo;

Todo::search('Groceries')->options([
    'query_by' => 'title, description'
])->get();
```



<a name="turbopuffer-configuration"></a>
### 터보퍼퍼

터보퍼퍼는 각 모델에 대한 스키마와 검색 가능한 속성이 필요합니다. 이를 `scout` 구성 파일 내의 `turbopuffer` 구성의 `model-settings` 배열에 정의하세요:

```php
use App\Models\Article;

'turbopuffer' => [
    // ...
    'model-settings' => [
        Article::class => [
            'searchable-attributes' => [
                'title' => 3,
                'body' => 1,
            ],
            'schema' => [
                'title' => ['type' => 'string', 'full_text_search' => true],
                'body' => ['type' => 'string', 'full_text_search' => true],
                'status' => ['type' => 'string'],
            ],
        ],
    ],
],
```



`searchable-attributes`에 할당된 숫자 값은 상대적인 BM25 가중치입니다. 위 예제에서 기사 제목의 일치 항목은 본문 내 일치 항목의 점수보다 세 배의 기여를 합니다.

시맨틱 및 하이브리드 검색을 활성화하려면 모델 구성에 `embedding` 설정과 벡터 스키마를 추가하십시오:

```php
'turbopuffer' => [
    // ...
    'model-settings' => [
        Article::class => [
            'searchable-attributes' => [
                'title' => 3,
                'body' => 1,
            ],
            'embedding' => [
                'attribute' => 'embedding',
                'dimensions' => 1536,
            ],
            'schema' => [
                'title' => ['type' => 'string', 'full_text_search' => true],
                'body' => ['type' => 'string', 'full_text_search' => true],
                'embedding' => ['type' => '[1536]f32', 'ann' => true],
            ],
        ],
    ],
],
```



귀하의 모델 `toSearchableEmbedding` 메서드는 Scout가 임베드해야 할 원문 텍스트 또는 미리 계산된 임베딩 배열을 반환해야 합니다. Scout는 [Laravel AI SDK](/docs/{{version}}/ai-sdk)를 사용하여 원문 텍스트 임베딩을 생성합니다.

또는 Laravel AI SDK를 설치하거나 `toSearchableEmbedding` 메서드를 정의하지 않고 Turbopuffer의 기본 임베딩을 사용할 수 있습니다. 임베딩 드라이버를 `turbopuffer`로 설정하고 검색 가능한 소스 속성에 `embed` 스키마를 구성하세요:

```php
'embedding' => [
    'driver' => 'turbopuffer',
    'attribute' => 'embedding_text',
],

'schema' => [
    // ...
    'embedding_text' => [
        'type' => 'string',
        'embed' => [
            'model' => 'voyage/voyage-4',
            'dimensions' => 1024,
            'attribute' => 'embedding',
        ],
    ],
],
```



모델의 `toSearchableArray` 출력에 source 속성을 포함해야 합니다.

<a name="indexing"></a>
## 서드파티 엔진 인덱싱

> [!NOTE]
> 이 섹션에서 설명하는 인덱싱 기능은 주로 서드파티 엔진(Algolia, Meilisearch, Typesense, Turbopuffer)을 사용할 때 관련이 있습니다. 데이터베이스 엔진은 데이터베이스 테이블을 직접 검색하므로 수동 인덱스 관리가 필요하지 않습니다.

<a name="batch-import"></a>
### 일괄 가져오기

Scout를 기존 프로젝트에 설치하는 경우, 이미 인덱스로 가져와야 하는 데이터베이스 레코드가 있을 수 있습니다. Scout는 모든 기존 레코드를 검색 인덱스로 가져오는 데 사용할 수 있는 `scout:import` Artisan 명령을 제공합니다:

```shell
php artisan scout:import "App\Models\Post"
```



`scout:queue-import` 명령은 [대기 중인 작업](/docs/{{version}}/queues)을 사용하여 기존 모든 기록을 가져오는 데 사용할 수 있습니다:

```shell
php artisan scout:queue-import "App\Models\Post" --chunk=500
```



`flush` 명령은 모델의 모든 레코드를 검색 색인에서 제거하는 데 사용할 수 있습니다:

```shell
php artisan scout:flush "App\Models\Post"
```



<a name="modifying-the-import-query"></a>
#### 가져오기 쿼리 수정하기

일괄 가져오기를 위해 모든 모델을 가져오는 데 사용되는 쿼리를 수정하고 싶다면, 모델에 `makeAllSearchableUsing` 메서드를 정의할 수 있습니다. 모델을 가져오기 전에 필요한 즉시 로딩 관계(eager relationship loading)를 추가하기에 좋은 위치입니다:

```php
use Illuminate\Database\Eloquent\Builder;

/**
 * Modify the query used to retrieve models when making all of the models searchable.
 */
protected function makeAllSearchableUsing(Builder $query): Builder
{
    return $query->with('author');
}
```



> [!WARNING]
> `makeAllSearchableUsing` 방법은 모델을 배치로 가져오기 위해 큐를 사용할 때 적용되지 않을 수 있습니다. 모델 컬렉션이 작업으로 처리될 때 관계는 [복원되지](/docs/{{version}}/queues#handling-relationships) 않습니다.

<a name="adding-records"></a>
### 레코드 추가

모델에 `Laravel\Scout\Searchable` 특성을 추가한 후에는 `save` 또는 `create` 모델 인스턴스를 수행하기만 하면 자동으로 검색 색인에 추가됩니다. Scout을 [큐 사용](#queueing)으로 구성한 경우 이 작업은 큐 작업자가 백그라운드에서 수행합니다:

```php
use App\Models\Order;

$order = new Order;

// ...

$order->save();
```



<a name="adding-records-via-query"></a>
#### 쿼리를 통해 레코드 추가하기

Eloquent 쿼리를 통해 검색 인덱스에 모델 컬렉션을 추가하고 싶다면, Eloquent 쿼리에 `searchable` 메서드를 연결하면 됩니다. `searchable` 메서드는 쿼리의 [결과를 청크 처리](/docs/{{version}}/eloquent#chunking-results)하고 레코드를 검색 인덱스에 추가합니다. 다시 말하지만, Scout를 큐 사용으로 구성한 경우, 모든 청크는 백그라운드에서 큐 작업자에 의해 가져와집니다:

```php
use App\Models\Order;

Order::where('price', '>', 100)->searchable();
```



Eloquent 관계 인스턴스에서 `searchable` 메서드를 호출할 수도 있습니다:

```php
$user->orders()->searchable();
```



또는, 이미 메모리에 Eloquent 모델 컬렉션이 있는 경우, 컬렉션 인스턴스에서 `searchable` 메서드를 호출하여 모델 인스턴스들을 해당 인덱스에 추가할 수 있습니다:

```php
$orders->searchable();
```



> [!NOTE]
> `searchable` 방법은 "업서트(upsert)" 연산으로 간주될 수 있습니다. 즉, 모델 레코드가 이미 인덱스에 있으면 업데이트됩니다. 검색 인덱스에 존재하지 않으면 인덱스에 추가됩니다.

<a name="updating-records"></a>
### 레코드 업데이트

검색 가능한 모델을 업데이트하려면, 모델 인스턴스의 속성을 업데이트하고 `save` 모델을 데이터베이스에 저장하기만 하면 됩니다. Scout은 변경 사항을 자동으로 검색 인덱스에 반영합니다:

```php
use App\Models\Order;

$order = Order::find(1);

// Update the order...

$order->save();
```



Eloquent 쿼리 인스턴스에서 `searchable` 메서드를 호출하여 모델 컬렉션을 업데이트할 수도 있습니다. 모델이 검색 인덱스에 존재하지 않는 경우, 새로 생성됩니다:

```php
Order::where('price', '>', 100)->searchable();
```



관계에 있는 모든 모델의 검색 인덱스 레코드를 업데이트하려면, 관계 인스턴스에서 `searchable`를 호출할 수 있습니다:

```php
$user->orders()->searchable();
```



또는, 이미 메모리에 Eloquent 모델 컬렉션이 있는 경우, 컬렉션 인스턴스에서 `searchable` 메서드를 호출하여 해당 인덱스에 있는 모델 인스턴스를 업데이트할 수 있습니다:

```php
$orders->searchable();
```



<a name="modifying-records-before-importing"></a>
#### 가져오기 전에 레코드 수정하기

때때로 검색 가능하게 만들기 전에 모델 컬렉션을 준비해야 할 때가 있습니다. 예를 들어, 관계 데이터를 검색 인덱스에 효율적으로 추가할 수 있도록 관계를 미리 로드(eager load)하고 싶을 수 있습니다. 이를 달성하려면, 해당 모델에 `makeSearchableUsing` 메서드를 정의하십시오:

```php
use Illuminate\Database\Eloquent\Collection;

/**
 * Modify the collection of models being made searchable.
 */
public function makeSearchableUsing(Collection $models): Collection
{
    return $models->load('author');
}
```



<a name="conditionally-updating-the-search-index"></a>
#### 검색 인덱스 조건부 업데이트

기본적으로 Scout는 어떤 속성이 수정되었는지와 상관없이 업데이트된 모델을 다시 인덱싱합니다. 이 동작을 사용자 정의하고 싶다면 모델에 `searchIndexShouldBeUpdated` 메서드를 정의할 수 있습니다:

```php
/**
 * Determine if the search index should be updated.
 */
public function searchIndexShouldBeUpdated(): bool
{
    return $this->wasRecentlyCreated || $this->wasChanged(['title', 'body']);
}
```



<a name="removing-records"></a>
### 레코드 제거

인덱스에서 레코드를 제거하려면 데이터베이스에서 모델을 단순히 `delete`하면 됩니다. 이것은 [소프트 삭제된](/docs/{{version}}/eloquent#soft-deleting) 모델을 사용하는 경우에도 수행할 수 있습니다:

```php
use App\Models\Order;

$order = Order::find(1);

$order->delete();
```



레코드를 삭제하기 전에 모델을 가져오고 싶지 않다면, Eloquent 쿼리 인스턴스에서 `unsearchable` 메서드를 사용할 수 있습니다:

```php
Order::where('price', '>', 100)->unsearchable();
```



관계에 있는 모든 모델의 검색 인덱스 레코드를 제거하려면, 관계 인스턴스에서 `unsearchable`를 호출할 수 있습니다:

```php
$user->orders()->unsearchable();
```



또는, 이미 메모리에 Eloquent 모델 컬렉션이 있는 경우, 컬렉션 인스턴스에서 `unsearchable` 메서드를 호출하여 해당 모델 인스턴스를 해당 인덱스에서 제거할 수 있습니다:

```php
$orders->unsearchable();
```



모든 모델 레코드를 해당 인덱스에서 제거하려면, `removeAllFromSearch` 메서드를 호출할 수 있습니다:

```php
Order::removeAllFromSearch();
```



<a name="pausing-indexing"></a>
### 인덱싱 일시 중지

때때로 모델 데이터를 검색 인덱스와 동기화하지 않고 모델에 대한 일괄 Eloquent 작업을 수행해야 할 수도 있습니다. 이때 `withoutSyncingToSearch` 메서드를 사용할 수 있습니다. 이 메서드는 즉시 실행되는 단일 클로저를 받습니다. 클로저 내에서 발생하는 모든 모델 작업은 모델의 인덱스와 동기화되지 않습니다:

```php
use App\Models\Order;

Order::withoutSyncingToSearch(function () {
    // Perform model actions...
});
```



<a name="conditionally-searchable-model-instances"></a>
### 조건부 검색 가능한 모델 인스턴스

때때로 특정 조건에서만 모델을 검색 가능하게 만들고 싶을 수 있습니다. 예를 들어, `App\Models\Post` 모델이 "draft"와 "published"의 두 가지 상태 중 하나일 수 있다고 가정해 봅시다. 이 경우, "published" 상태의 게시물만 검색 가능하도록 허용하고 싶을 수 있습니다. 이를 달성하기 위해 모델에 `shouldBeSearchable` 메서드를 정의할 수 있습니다:

```php
/**
 * Determine if the model should be searchable.
 */
public function shouldBeSearchable(): bool
{
    return $this->isPublished();
}
```



`shouldBeSearchable` 메소드는 `save` 및 `create` 메소드, 쿼리 또는 관계를 통해 모델을 조작할 때만 적용됩니다. `searchable` 메소드를 사용하여 모델이나 컬렉션을 직접 검색 가능하게 하면 `shouldBeSearchable` 메소드의 결과가 무시됩니다.

> [!WARNING]
> Scout의 "database" 엔진을 사용할 때는 `shouldBeSearchable` 메소드를 적용할 수 없습니다. 데이터베이스 엔진을 사용할 때 유사한 동작을 달성하려면 대신 [where 절](#where-clauses)을 사용해야 합니다.

<a name="searching"></a>
## 검색

`search` 메소드를 사용하여 모델 검색을 시작할 수 있습니다. search 메소드는 모델을 검색하는 데 사용될 단일 문자열을 받습니다. 그 다음 search 쿼리에 `get` 메소드를 체인하여 주어진 검색 쿼리에 일치하는 Eloquent 모델을 검색해야 합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->get();
```



Scout 검색이 Eloquent 모델의 컬렉션을 반환하기 때문에, 결과를 라우트나 컨트롤러에서 직접 반환해도 자동으로 JSON으로 변환됩니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/search', function (Request $request) {
    return Order::search($request->search)->get();
});
```



Eloquent 모델로 변환되기 전에 원시 검색 결과를 받고 싶다면, `raw` 메서드를 사용할 수 있습니다:

```php
$orders = Order::search('Star Trek')->raw();
```



<a name="semantic-search"></a>
### 의미 기반 검색

데이터베이스, Meilisearch, Typesense 및 Turbopuffer 엔진은 쿼리의 의미를 기반으로 레코드를 일치시키는 의미 기반 검색을 지원합니다. Scout가 임베딩을 생성할 때, 의미 기반 검색 및 하이브리드 검색에는 [Laravel AI SDK](/docs/{{version}}/ai-sdk)가 필요합니다. [Typesense의 네이티브 임베딩](#typesense-embeddings), [Turbopuffer의 네이티브 임베딩](#turbopuffer-configuration), 그리고 미리 계산된 쿼리 벡터는 Laravel AI SDK가 필요하지 않습니다.

선택한 엔진에 대한 임베딩 구성을 완료한 후, 검색 쿼리에 대해 `semantic` 메서드를 호출합니다:

```php
$articles = Article::search('staying cool in the summer')
    ->semantic()
    ->get();
```



선택한 엔진에서 지원되는 경우 최소 유사성 임계값을 제공할 수 있습니다:

```php
$articles = Article::search('renewable energy storage')
    ->semantic(minSimilarity: 0.6)
    ->get();
```



전체 텍스트 검색과 의미 검색을 결합하려면 `hybrid` 방법을 사용하세요. 첫 두 인수는 텍스트 결과와 의미 결과의 상대적 가중치를 제어합니다:

```php
$articles = Article::search('renewable energy storage')
    ->hybrid(textWeight: 1, semanticWeight: 2)
    ->get();
```



<a name="custom-indexes"></a>
#### 맞춤 인덱스

타사 검색 엔진을 사용할 때 검색 쿼리는 일반적으로 모델의 [searchableAs](#configuring-model-indexes) 메서드에 의해 지정된 인덱스에서 수행됩니다. 그러나 대신 검색할 맞춤 인덱스를 지정하려면 `within` 메서드를 사용할 수 있습니다:

```php
$orders = Order::search('Star Trek')
    ->within('tv_shows_popularity_desc')
    ->get();
```



<a name="where-clauses"></a>
### Where 절

Scout는 검색 쿼리에 "where" 절을 추가할 수 있습니다. 예를 들어, 기본 동등성 검사는 소유자 ID로 검색 쿼리의 범위를 지정할 때 유용합니다:

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->where('user_id', 1)->get();
```



또한 더 고급 쿼리를 작성하기 위해 `=`, `!=`, `<`, `>`, `>=`, `<=` 비교 연산자를 사용할 수 있습니다:

```php
Order::search('Star Trek')
  ->where('status', '=', 'completed')
  ->where('is_refunded', '!=', true)
  ->where('total_price', '>', 100)
  ->where('shipping_cost', '<', 20)
  ->where('discount_percent', '>=', 10)
  ->where('item_count', '<=', 5)
  ->get();
```



또한, `whereIn` 방법은 주어진 열의 값이 주어진 배열에 포함되어 있는지 확인하는 데 사용될 수 있습니다:

```php
$orders = Order::search('Star Trek')->whereIn(
    'status', ['open', 'paid']
)->get();
```



`whereNotIn` 메서드는 지정된 열의 값이 주어진 배열에 포함되어 있지 않은지 확인합니다:

```php
$orders = Order::search('Star Trek')->whereNotIn(
    'status', ['closed']
)->get();
```



> [!WARNING]
> 애플리케이션이 Meilisearch를 사용하는 경우, Scout의 "where" 절을 사용하기 전에 애플리케이션의 [필터 가능 속성](#meilisearch-index-settings)을 구성해야 합니다.

<a name="customizing-the-eloquent-results-query"></a>
#### Eloquent 결과 쿼리 사용자 정의

Scout가 애플리케이션의 검색 엔진에서 일치하는 Eloquent 모델 목록을 가져온 후, Eloquent를 사용하여 기본 키로 모든 일치하는 모델을 검색합니다. `query` 메소드를 호출하여 이 쿼리를 사용자 정의할 수 있습니다. `query` 메소드는 Eloquent 쿼리 빌더 인스턴스를 인수로 받는 클로저를 허용합니다:

```php
use App\Models\Order;
use Illuminate\Database\Eloquent\Builder;

$orders = Order::search('Star Trek')
    ->query(fn (Builder $query) => $query->with('invoices'))
    ->get();
```



서드파티 엔진을 사용할 때, 관련 모델을 검색 엔진에서 이미 가져온 후에 이 콜백이 호출되므로 결과를 "필터링"하는 데 사용해서는 안 됩니다 — 대신 [Scout where 절](#where-clauses)을 사용하세요. 그러나 데이터베이스 엔진을 사용할 경우, `query` 메소드의 제약 조건이 데이터베이스 쿼리에 직접 적용되므로 필터링에도 사용할 수 있습니다.

<a name="pagination"></a>
### 페이지네이션

모델 컬렉션을 가져오는 것 외에도, `paginate` 메서드를 사용하여 검색 결과를 페이지별로 나눌 수 있습니다. 이 메서드는 [전통적인 Eloquent 쿼리를 페이지네이션 했을 때](/docs/{{version}}/pagination)와 마찬가지로 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 반환합니다.

```php
use App\Models\Order;

$orders = Order::search('Star Trek')->paginate();
```



`paginate` 메서드에 첫 번째 인수로 수량을 전달하여 페이지당 검색할 모델 수를 지정할 수 있습니다:

```php
$orders = Order::search('Star Trek')->paginate(15);
```



데이터베이스 엔진을 사용할 때 `simplePaginate` 방법을 사용할 수도 있습니다. 전체 일치 레코드 수를 가져와 페이지 번호를 표시할 수 있는 `paginate`와 달리, `simplePaginate`는 현재 페이지를 넘어 더 많은 결과가 있는지 여부만 확인하므로, 이전 및 다음 링크만 필요할 때 대용량 데이터셋에서 더 효율적입니다:

```php
$orders = Order::search('Star Trek')->simplePaginate(15);
```



결과를 가져온 후에는, 전통적인 Eloquent 쿼리를 페이징한 것처럼 [Blade](/docs/{{version}}/blade)를 사용하여 결과를 표시하고 페이지 링크를 렌더링할 수 있습니다:

```html
<div class="container">
    @foreach ($orders as $order)
        {{ $order->price }}
    @endforeach
</div>

{{ $orders->links() }}
```



물론, 페이지네이션 결과를 JSON으로 가져오고 싶다면, 라우트나 컨트롤러에서 페이징 인스턴스를 직접 반환할 수 있습니다:

```php
use App\Models\Order;
use Illuminate\Http\Request;

Route::get('/orders', function (Request $request) {
    return Order::search($request->input('query'))->paginate(15);
});
```



> [!WARNING]
> 검색 엔진은 여러분의 Eloquent 모델의 글로벌 스코프 정의를 인식하지 못하므로, Scout 페이지네이션을 사용하는 애플리케이션에서는 글로벌 스코프를 사용하지 않아야 합니다. 또는 Scout를 통해 검색할 때 글로벌 스코프의 제약 조건을 다시 만들어야 합니다.

<a name="soft-deleting"></a>
### 소프트 삭제

인덱싱된 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)되고 소프트 삭제된 모델을 검색해야 하는 경우, `config/scout.php` 구성 파일의 `soft_delete` 옵션을 `true`로 설정하세요:

```php
'soft_delete' => true,
```



이 구성 옵션이 `true`일 때, Scout는 검색 인덱스에서 소프트 삭제된 모델을 제거하지 않습니다. 대신, 인덱스된 레코드에 숨겨진 `__soft_deleted` 속성을 설정합니다. 그런 다음, 검색할 때 소프트 삭제된 레코드를 가져오기 위해 `withTrashed` 또는 `onlyTrashed` 메서드를 사용할 수 있습니다:

```php
use App\Models\Order;

// Include trashed records when retrieving results...
$orders = Order::search('Star Trek')->withTrashed()->get();

// Only include trashed records when retrieving results...
$orders = Order::search('Star Trek')->onlyTrashed()->get();
```



> [!NOTE]
> 소프트 삭제된 모델이 `forceDelete`를 사용하여 영구적으로 삭제되면 Scout는 검색 색인에서 자동으로 이를 제거합니다.

<a name="customizing-engine-searches"></a>
### 엔진 검색 사용자 정의

엔진의 검색 동작을 고급으로 사용자 정의해야 하는 경우 `search` 메서드의 두 번째 인수로 클로저를 전달할 수 있습니다. 예를 들어, 이 콜백을 사용하여 검색 쿼리가 Algolia에 전달되기 전에 검색 옵션에 지리 위치 데이터를 추가할 수 있습니다:

```php
use Algolia\AlgoliaSearch\SearchIndex;
use App\Models\Order;

Order::search(
    'Star Trek',
    function (SearchIndex $algolia, string $query, array $options) {
        $options['body']['query']['bool']['filter']['geo_distance'] = [
            'distance' => '1000km',
            'location' => ['lat' => 36, 'lon' => 111],
        ];

        return $algolia->search($query, $options);
    }
)->get();
```



<a name="custom-engines"></a>
## 맞춤 엔진

<a name="writing-the-engine"></a>
#### 엔진 작성

내장된 Scout 검색 엔진 중 하나가 필요에 맞지 않다면, 직접 맞춤 엔진을 작성하고 Scout에 등록할 수 있습니다. 엔진은 `Laravel\Scout\Engines\Engine` 추상 클래스를 확장해야 합니다. 이 추상 클래스에는 맞춤 엔진이 구현해야 하는 여덟 가지 메서드가 포함되어 있습니다:

```php
use Laravel\Scout\Builder;

abstract public function update($models);
abstract public function delete($models);
abstract public function search(Builder $builder);
abstract public function paginate(Builder $builder, $perPage, $page);
abstract public function mapIds($results);
abstract public function map(Builder $builder, $results, $model);
abstract public function getTotalCount($results);
abstract public function flush($model);
```



이러한 메서드의 구현을 `Laravel\Scout\Engines\AlgoliaEngine` 클래스에서 검토하는 것이 도움이 될 수 있습니다. 이 클래스는 각 메서드를 자신의 엔진에서 구현하는 방법을 배우는 데 좋은 출발점을 제공합니다.

<a name="registering-the-engine"></a>
#### 엔진 등록

맞춤형 엔진을 작성한 후에는 Scout의 엔진 매니저에서 `extend` 메서드를 사용하여 Scout에 등록할 수 있습니다. Scout의 엔진 매니저는 Laravel 서비스 컨테이너에서 해결할 수 있습니다. `App\Providers\AppServiceProvider` 클래스나 애플리케이션에서 사용되는 다른 서비스 제공자의 `boot` 메서드에서 `extend` 메서드를 호출해야 합니다.

```php
use App\ScoutExtensions\MySqlSearchEngine;
use Laravel\Scout\EngineManager;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    resolve(EngineManager::class)->extend('mysql', function () {
        return new MySqlSearchEngine;
    });
}
```



엔진이 등록되면, 애플리케이션의 `config/scout.php` 구성 파일에서 기본 Scout `driver`로 지정할 수 있습니다:

```php
'driver' => 'mysql',
```
{% endraw %}
