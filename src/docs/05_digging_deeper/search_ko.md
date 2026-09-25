---
layout: docs
title: "검색"
---

{% raw %}
# 검색

- [인트로듀션](#introduction)
- [풀텍스트 검색](#introduction-full-text-search)
- [Semantic / Vector Search](#introduction-semantic-vector-search)
- [순위](#introduction-reranking)
- [스카우트 검색 엔진](#introduction-scout-search-engines)
- 전체 텍스트 검색 (#full-text-search)
- [전체 텍스트 인덱스 추가](#adding-full-text-indexes)
- [전체 텍스트 쿼리 실행](#running-full-text-queries)
- 의미 및 벡터 검색 (#semantic-vector-search)
- [임베디드 생성](#generating-embeddings)
- [저장 및 인덱싱 벡터](#storing-and-indexing-vectors)
- 유사성 쿼리 (#querying-by-similarity)
- [순위 결과](#reranking-results)
- 라라벨 스카우트 (#laravel-scout)
- 데이터베이스 엔진 (#database-engine)
- [서드파티 엔진](#third-party-engines)
- [기술 결합](#combining-techniques)

<a name="introduction"></a>
## 소개

거의 모든 애플리케이션에는 검색이 필요합니다. 사용자가 관련 기사를 찾기 위해 지식 기반을 검색하든， 제품 카탈로그를 탐색하든， 문서 집합에 대해 자연어로 질문하든， Laravel 은 이러한 각 시나리오를 처리할 수 있는 기본 제공 도구를 제공하며， 종종 이를 위해 외부 서비스가 필요하지 않습니다。

대부분의 애플리케이션에서 Laravel 이 제공하는 내장된 데이터베이스 기반 옵션으로 충분합니다. 외부 검색 서비스는 오타 허용， 단면 필터링 또는 대규모 지리 검색과 같은 기능이 필요한 경우에만 필요합니다。

<a name="introduction-full-text-search"></a>
#### 전체 텍스트 검색

키워드 관련성 순위 (검색어와 얼마나 잘 일치하는지에 따라 데이터베이스가 점수를 매기고 결과를 정렬하는 순위) 가 필요한 경우， Laravel 의 `whereFullText` 쿼리 빌더 메서드는 MariaDB, MySQL 및 PostgreSQL 의 기본 전체 텍스트 인덱스를 활용합니다. 전체 텍스트 검색은 단어 경계와 어원을 이해하므로 “running” 을 검색하면 “run” 이 포함된 레코드와 일치할 수 있습니다. 외부 서비스는 필요하지 않습니다。

<a name="introduction-semantic-vector-search"></a>
#### 의미론 / 벡터 검색



정확한 키워드가 아닌 *meaning* 로 결과와 일치하는 AI 기반 의미 검색의 경우， `whereVectorSimilarTo` 쿼리 빌더 메서드는 `pgvector` 확장 또는 MariaDB 와 함께 PostgreSQL 에 저장된 벡터 임베디드를 사용합니다. 예를 들어， “Napa Valley 최고의 와이너리” 를 검색하면 단어가 겹치지 않더라도 “Top Vineyards to Visit” 라는 제목의 문서가 표시될 수 있습니다. 벡터 검색을 사용하려면 `pgvector` 확장 또는 MariaDB 11.7 이상과 [Laravel AI SDK](/docs/{{version}}/ai-sdk) 가 있는 PostgreSQL 이 필요합니다。

<a name="introduction-reranking"></a>
#### 순위

Laravel 의 [AI SDK](/docs/{{version}}/ai-sdk) 는 AI 모델을 사용하여 쿼리에 대한 의미론적 관련성에 따라 모든 결과 집합을 재정렬하는 재순위 지정 기능을 제공합니다. 재순위 지정은 전체 텍스트 검색과 같은 빠른 초기 검색 단계 이후의 두 번째 단계로서 특히 강력하며， 속도와 의미론적 정확도를 모두 제공합니다。

<a name="introduction-scout-search-engines"></a>
#### 라라벨 스카우트 검색

Eloquent 모델과 검색 인덱스를 자동으로 동기화하는 `Searchable` 특성을 원하는 애플리케이션의 경우， [Laravel Scout](/docs/{{version}}/scout) 는 Algolia, Meilisearch, Typesense 및 Turbobuffer 와 같은 타사 서비스를 위한 내장된 데이터베이스 엔진과 드라이버를 모두 제공합니다。

<a name="full-text-search"></a>
## 전체 텍스트 검색

`LIKE` 쿼리는 간단한 하위 문자열 일치에는 잘 작동하지만 언어를 이해하지 못합니다. “running” 을 검색하는 `LIKE` 는 “run” 이 포함된 레코드를 찾지 못하며， 결과는 관련성별로 순위가 지정되지 않습니다. 데이터베이스에서 찾은 순서에 따라 반환됩니다. 전체 텍스트 검색은 단어 경계， 스템 및 관련성 점수를 이해하는 전문화된 인덱스를 사용하여 이러한 두 가지 문제를 모두 해결하므로， 데이터베이스에서 가장 관련성이 높은 결과를 먼저 반환할 수 있습니다。

빠른 전체 텍스트 검색은 MariaDB, MySQL 및 PostgreSQL 에 내장되어 있으므로 외부 검색 서비스가 필요하지 않습니다. 검색하려는 열에 전체 텍스트 인덱스를 추가한 다음 `whereFullText` 쿼리 빌더 메서드를 사용하여 해당 열을 검색하기만 하면 됩니다。

> [!WARNING]
> 전체 텍스트 검색은 현재 MariaDB, MySQL 및 PostgreSQL 에서 지원됩니다。

<a name="adding-full-text-indexes"></a>
### 전체 텍스트 인덱스 추가

전체 텍스트 검색을 사용하려면 먼저 검색하려는 열에 전체 텍스트 인덱스를 추가합니다. 인덱스를 단일 열에 추가하거나 열 배열을 전달하여 여러 필드에서 동시에 검색하는 복합 인덱스를 생성할 수 있습니다：

```php
Schema::create('articles', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('body');
    $table->timestamps();

    $table->fullText(['title', 'body']);
});

```

PostgreSQL에서는 색인에 대해 언어 구성을 지정할 수 있으며, 이는 단어가 어떻게 어간 처리되는지를 제어합니다:

```php
$table->fullText('body')->language('english');

```

인덱스 생성에 대한 자세한 정보는 [마이그레이션 문서](/docs/{{version}}/migrations#available-index-types)를 참고하십시오.

<a name="running-full-text-queries"></a>
### 전체 텍스트 쿼리 실행

인덱스가 설정되면 `whereFullText` 쿼리 빌더 메서드를 사용하여 검색할 수 있습니다. Laravel은 데이터베이스 드라이버에 맞는 적절한 SQL을 생성합니다 — 예를 들어 MariaDB와 MySQL에서는 `MATCH(...) AGAINST(...)`, PostgreSQL에서는 `to_tsvector(...) @@ plainto_tsquery(...)`:

```php
$articles = Article::whereFullText('body', 'web developer')->get();

```

MariaDB와 MySQL을 사용할 때 결과는 자동으로 관련성 점수에 따라 정렬됩니다. PostgreSQL에서는 `whereFullText`가 일치하는 레코드를 필터링하지만 관련성에 따라 정렬하지는 않습니다 — PostgreSQL에서 자동 관련성 정렬이 필요하다면, 이를 처리해주는 [Scout의 데이터베이스 엔진](#database-engine)을 사용하는 것을 고려해 보세요.

여러 열에 걸쳐 복합 전체 텍스트 인덱스를 생성한 경우, 동일한 열 배열을 `whereFullText`에 전달하여 모든 열을 대상으로 검색할 수 있습니다:

```php
$articles = Article::whereFullText(
    ['title', 'body'], 'web developer'
)->get();

```



`orWhereFullText` 메서드를 사용하여 전체 텍스트 검색 절을 “또는” 조건으로 추가할 수 있습니다. 자세한 내용은 [query builder documentation](/docs/{{version}}/queries#full-text-where-clauses) 를 참조하십시오。

<a name="semantic-vector-search"></a>
## 의미론 / 벡터 검색

전체 텍스트 검색은 일치하는 키워드에 의존합니다 - 쿼리의 단어가 데이터에 (어떤 형태로든) 나타나야 합니다. 의미론적 검색은 근본적으로 다른 접근 방식을 취합니다: AI 생성 벡터 임베디드를 사용하여 텍스트의 * 의미 * 를 숫자 배열로 표현한 다음， 쿼리와 가장 유사한 의미를 가진 결과를 찾습니다. 예를 들어， “나파 밸리 최고의 와이너리” 를 검색하면 단어가 전혀 겹치지 않더라도 “방문할 만한 최고의 포도밭” 이라는 제목의 기사가 표시될 수 있습니다。

벡터 검색의 기본 워크플로는 다음과 같습니다: 각 콘텐츠 조각에 대한 임베디드 (숫자 배열) 를 생성하고 데이터와 함께 저장한 다음， 검색 시 사용자 쿼리에 대한 임베디드를 생성하고 벡터 공간에서 가장 가까운 저장된 임베디드를 찾습니다。

> [!NOTE]
> 벡터 검색에는 [Laravel AI SDK](/docs/{{version}}/ai-sdk) 가 필요하며 PostgreSQL(`pgvector` 확장 프로그램 필요), MariaDB 11.7 이상 및 MongoDB([Laravel MongoDB 패키지](https://laravel.com/docs/13.x/mongodb) 가 필요) 에서 지원됩니다. [Laravel Cloud](https://laravel.com/cloud) 의 모든 Postgres 데이터베이스에는 이미 `pgvector` 가 설치되어 있습니다。

<a name="generating-embeddings"></a>
### 임베디드 생성

임베딩은 텍스트 조각의 의미론적 의미를 나타내는 고차원 숫자 배열 (일반적으로 수백 또는 수천 개의 숫자) 입니다. Laravel 의 `Stringable` 클래스에서 사용할 수 있는 `toEmbeddings` 메서드를 사용하여 문자열에 대한 임베딩을 생성할 수 있습니다：

```php
use Illuminate\Support\Str;

$embedding = Str::of('Napa Valley has great wine.')->toEmbeddings();

```

여러 입력에 대한 임베딩을 한 번에 생성하려면 — 임베딩 제공자에게 단일 API 호출만 필요하기 때문에 하나씩 생성하는 것보다 효율적입니다 — `Embeddings` 클래스를 사용하세요:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]

```

임베딩 제공자 구성, 차원 사용자 지정 및 캐싱에 대한 자세한 내용은 [AI SDK 문서](/docs/{{version}}/ai-sdk#embeddings)를 참조하세요.

<a name="storing-and-indexing-vectors"></a>
### 벡터 저장 및 인덱싱

벡터 임베딩을 저장하려면 마이그레이션에서 `vector` 열을 정의하고 임베딩 제공자의 출력과 일치하는 차원 수를 지정하세요(예: OpenAI의 `text-embedding-3-small` 모델의 경우 1536). 또한 HNSW(계층적 탐색 가능한 소형 세계) 인덱스를 생성하기 위해 열에서 `index`를 호출해야 하며, 이는 대규모 데이터 세트에서 유사성 검색 속도를 크게 향상시킵니다.

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536)->index();
    $table->timestamps();
});

```



`Schema::ensureVectorExtensionExists` 방법은 테이블을 생성하기 전에 PostgreSQL 데이터베이스에서 `pgvector` 확장이 활성화되어 있는지 확인합니다.

Eloquent 모델에서는 `AsVector` 캐스트를 사용하여 Laravel이 PHP 배열과 데이터베이스 벡터 형식 간의 변환을 자동으로 처리하도록 합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsVector;

protected function casts(): array
{
    return [
        'embedding' => AsVector::class,
    ];
}

```

벡터 컬럼과 인덱스에 대한 자세한 내용은 [마이그레이션 문서](/docs/{{version}}/migrations#available-column-types)를 참조하세요.

<a name="querying-by-similarity"></a>
### 유사도 기반 쿼리

콘텐츠에 대한 임베딩을 저장한 후에는 `whereVectorSimilarTo` 방법을 사용하여 유사한 레코드를 검색할 수 있습니다. 이 방법은 주어진 임베딩을 저장된 벡터와 코사인 유사도를 사용하여 비교하고, `minSimilarity` 임계값 이하인 결과를 필터링하며, 가장 유사한 레코드가 먼저 오도록 자동으로 결과를 관련성 순으로 정렬합니다. 임계값은 `0.0`와 `1.0` 사이의 값이어야 하며, `1.0`는 벡터가 동일함을 의미합니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();

```

편의를 위해, 임베딩 배열 대신 일반 문자열이 제공되면 Laravel은 구성된 임베딩 제공자를 사용하여 자동으로 임베딩을 생성합니다. 이는 사용자의 검색 쿼리를 먼저 임베딩으로 수동 변환하지 않고 직접 전달할 수 있음을 의미합니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();

```

벡터 쿼리에 대한 낮은 수준의 제어를 위해 `whereVectorDistanceLessThan`, `selectVectorDistance` 및 `orderByVectorDistance` 메서드도 사용할 수 있습니다. 이러한 메서드를 사용하면 유사성 점수 대신 거리 값으로 직접 작업하거나， 결과에서 계산된 거리를 열로 선택하거나， 순서를 수동으로 제어할 수 있습니다. 자세한 내용은 [쿼리 빌더 문서](/docs/{{version}}/queries#vector-similarity-clauses) 및 [AI SDK 문서](/docs/{{version}}/ai-sdk#querying-embeddings) 를 참조하십시오。

<a name="reranking-results"></a>
## 순위 결과

재정렬은 AI 모델이 각 결과가 주어진 쿼리와 의미론적으로 얼마나 관련이 있는지에 따라 결과 집합을 재정렬하는 기술입니다. 사전 계산 및 임베디드 저장이 필요한 벡터 검색과 달리， 재정렬은 모든 텍스트 모음에서 작동합니다. 원시 콘텐츠와 쿼리를 입력으로 받고 관련성별로 정렬된 항목을 반환합니다。

재정렬은 빠른 초기 검색 단계 후의 두 번째 단계로서 특히 강력합니다. 예를 들어， 전체 텍스트 검색을 사용하여 수천 개의 레코드를 상위 50 개 후보로 빠르게 좁힌 다음， 재정렬을 사용하여 가장 관련성 높은 결과를 상위에 배치할 수 있습니다. 이 “검색 후 재정렬” 패턴은 속도와 의미론적 정확도를 모두 제공합니다。

`Reranking` 클래스를 사용하여 문자열 배열의 순위를 재정렬할 수 있습니다：

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

$response->first()->document; // "Laravel is a PHP web application framework."

```

Laravel 컬렉션에는 필드 이름(또는 클로저)과 쿼리를 받는 `rerank` 매크로도 있어 Eloquent 결과를 쉽게 재정렬할 수 있습니다:

```php
$articles = Article::all()
    ->rerank('body', 'Laravel tutorials');

```

재순위 제공자 구성 및 사용 가능한 옵션에 대한 자세한 내용은 [AI SDK 문서](/docs/{{version}}/ai-sdk#reranking) 를 참조하십시오。

<a name="laravel-scout"></a>
## 라라벨 스카우트

위에서 설명한 검색 기술은 모두 코드에서 직접 호출하는 쿼리 빌더 메서드입니다. [Laravel Scout](/docs/{{version}}/scout) 는 다른 접근 방식을 취합니다. 이는 Eloquent 모델에 추가하는 `Searchable` 특성을 제공하며， 레코드가 생성， 업데이트 및 삭제될 때 Scout 가 자동으로 검색 인덱스를 동기화합니다. 이는 인덱스 업데이트를 수동으로 관리하지 않고도 모델을 항상 검색할 수 있게 하려는 경우에 특히 편리합니다。

<a name="database-engine"></a>
### 데이터베이스 엔진

Scout 의 내장된 데이터베이스 엔진은 기존 데이터베이스에 대해 전체 텍스트 및 `LIKE` 검색을 수행합니다. 외부 서비스나 추가 인프라가 필요하지 않습니다. 모델에 `Searchable` 특성을 추가하고 검색 가능하게 하려는 열을 반환하는 `toSearchableArray` 메서드를 정의하기만 하면 됩니다。

PHP 속성을 사용하여 각 열의 검색 전략을 제어할 수 있습니다. `SearchUsingFullText` 는 데이터베이스의 전체 텍스트 인덱스를 사용하고， `SearchUsingPrefix` 는 문자열의 시작부터만 일치시키며 (`example%`), 속성이 없는 모든 열은 양쪽에 와일드카드가 있는 기본 `LIKE` 전략을 사용합니다 (`%example%`):

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Attributes\SearchUsingFullText;
use Laravel\Scout\Attributes\SearchUsingPrefix;
use Laravel\Scout\Searchable;

class Article extends Model
{
    use Searchable;

    #[SearchUsingPrefix(['id'])]
    #[SearchUsingFullText(['title', 'body'])]
    public function toSearchableArray(): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'body' => $this->body,
        ];
    }
}

```

> [!WARNING]
> 열이 전체 텍스트 쿼리 제약 조건을 사용하도록 지정하기 전에, 해당 열에 [전체 텍스트 인덱스](/docs/{{version}}/migrations#available-index-types)가 할당되어 있는지 확인하십시오.

트레이트가 추가되면, Scout의 `search` 메서드를 사용하여 모델을 검색할 수 있습니다. Scout의 데이터베이스 엔진은 PostgreSQL에서도 결과를 자동으로 관련성 순으로 정렬합니다:

```php
$articles = Article::search('Laravel')->get();

```

데이터베이스 엔진은 검색 요구 사항이 중간 수준이고 외부 서비스를 배포하지 않고 Scout 의 자동 인덱스 동기화의 편의성을 원할 때 훌륭한 선택입니다. 필터링， 페이지 구성 및 소프트 삭제 레코드 처리를 포함하여 가장 일반적인 검색 사용 사례를 잘 처리합니다. 자세한 내용은 [Scout 문서](/docs/{{version}}/scout#database-engine) 를 참조하세요。

<a name="third-party-engines"></a>
### 제 3 자 엔진

Scout 는 또한 [Algolia](https://www.algolia.com/), [Meilisearch](https://www.meilisearch.com) 및 [Typesense](https://typesense.org) 와 같은 타사 검색 엔진을 지원합니다. 이러한 전용 검색 서비스는 오타 허용， 단면 필터링， 지리적 검색 및 사용자 지정 순위 지정 규칙과 같은 고급 기능을 제공합니다. 이러한 기능은 매우 큰 규모에서 또는 매우 정교한 맞춤형 검색 경험이 필요할 때 중요해집니다。

Scout 는 모든 드라이버에서 통합 API 를 제공하므로， 나중에 데이터베이스 엔진에서 타사 엔진으로 전환하는 데는 최소한의 코드 변경만 필요합니다. 애플리케이션의 요구 사항이 데이터베이스가 제공할 수 있는 것을 초과하는 경우에만 데이터베이스 엔진으로 시작하여 타사 서비스로 마이그레이션할 수 있습니다。

타사 엔진 구성에 대한 자세한 내용은 [Scout 문서](/docs/{{version}}/scout) 를 참조하십시오。

> [!NOTE]
> 많은 애플리케이션에는 외부 검색 엔진이 필요하지 않습니다. 이 페이지에서 설명하는 내장 기술은 대다수의 사용 사례를 다룹니다。

<a name="combining-techniques"></a>
## 결합 기법

이 페이지에서 설명하는 검색 기법들은 서로 배타적이지 않습니다. 이들을 결합하면 종종 최고의 결과를 얻을 수 있습니다. 다음은 이러한 도구들이 함께 작동하는 방식을 보여주는 두 가지 일반적인 패턴입니다。

** 전체 텍스트 검색 + 순위 조정 **

전체 텍스트 검색을 사용하여 대규모 데이터 집합을 후보자 집합으로 빠르게 좁힌 다음， 재순위를 적용하여 해당 후보자들을 의미론적 관련성별로 정렬합니다. 이를 통해 AI 기반 관련성 점수 부여의 정확성과 함께 데이터베이스 네이티브 전체 텍스트 검색의 속도를 얻을 수 있습니다：

```php
$articles = Article::query()
    ->whereFullText('body', $request->input('query'))
    ->limit(50)
    ->get()
    ->rerank('body', $request->input('query'), limit: 10);

```

**벡터 검색 + 전통적 필터**

벡터 유사성을 표준 `where` 조항과 결합하여 의미 기반 검색을 특정 레코드 하위 집합으로 제한합니다. 이는 의미 기반 검색을 원하지만 소유권, 카테고리 또는 기타 속성에 따라 결과를 제한해야 할 때 유용합니다:

```php
$documents = Document::query()
    ->where('team_id', $user->team_id)
    ->whereVectorSimilarTo('embedding', $request->input('query'))
    ->limit(10)
    ->get();

```
{% endraw %}
