---
layout: docs
title: "릴리스 노트"
---

{% raw %}
# 릴리스 노트

- [버전 관리 체계](#versioning-scheme)
- [지원 정책](#support-policy)
- [라라벨 13](#laravel-13)

<a name="versioning-scheme"></a>
## 버전 관리 체계

Laravel과 기타 자사 패키지는 [Semantic Versioning](https://semver.org)을 따릅니다. 주요 프레임워크 릴리스는 매년(~Q1) 릴리스되는 반면, 마이너 및 패치 릴리스는 매주 릴리스될 수 있습니다. 마이너 및 패치 릴리스에는 **절대로** 주요 변경 사항이 포함되어서는 안 됩니다.

애플리케이션이나 패키지에서 Laravel 프레임워크나 해당 구성 요소를 참조할 때 Laravel의 주요 릴리스에는 주요 변경 사항이 포함되어 있으므로 항상 `^13.0`와 같은 버전 제약 조건을 사용해야 합니다. 그러나 우리는 항상 하루 이내에 새로운 주요 릴리스로 업데이트할 수 있도록 노력하고 있습니다.

<a name="named-arguments"></a>
#### 명명된 인수

[명명된 인수](https://www.php.net/manual/en/functions.arguments.php#functions.named-arguments)는 Laravel의 이전 버전과의 호환성 지침에 포함되지 않습니다. Laravel 코드베이스를 개선하기 위해 필요한 경우 함수 인수의 이름을 바꿀 수 있습니다. 따라서 Laravel 메서드를 호출할 때 명명된 인수를 사용할 때는 매개변수 이름이 미래에 변경될 수 있다는 점을 이해하고 주의 깊게 수행해야 합니다.

<a name="support-policy"></a>
## 지원 정책

모든 Laravel 릴리스에는 버그 수정이 18개월 동안 제공되고 보안 수정은 2년 동안 제공됩니다. 모든 추가 라이브러리의 경우 최신 주요 릴리스에만 버그 수정이 적용됩니다. 또한 [Laravel에서 지원하는](/docs/{{version}}/database#introduction) 데이터베이스 버전을 검토하세요.

<div class="overflow-auto">

| 버전 | PHP (*) | 출시 | 버그 수정 종료일 | 보안 수정 종료일 |
| ------- |-----------| ------------------- | ------------------- | -------------------- |
| 10 | 8.1 - 8.3 | 2023년 2월 14일 | 2024년 8월 6일 | 2025년 2월 4일 |
| 11 | 8.2 - 8.4 | 2024년 3월 12일 | 2025년 9월 3일 | 2026년 3월 12일 |
| 12 | 8.2 - 8.5 | 2025년 2월 24일 | 2026년 8월 13일 | 2027년 2월 24일 |
| 13 | 8.3 - 8.5 | 2026년 3월 17일 | 2027년 3분기 | 2028년 3월 17일 |

</div>

<div class="version-colors">
    <div class="end-of-life">
        <div class="color-box"></div>
        <div>End of life</div>
    </div>
    <div class="security-fixes">
        <div class="color-box"></div>
        <div>Security fixes only</div>
    </div>
</div>

(*) 지원되는 PHP 버전

<a name="laravel-13"></a>
## 라라벨 13

Laravel 13은 AI 기반 워크플로, 더 강력한 기본값, 더 표현력이 풍부한 개발자 API에 중점을 두고 Laravel의 연간 릴리스 흐름을 이어갑니다. 이 릴리스에는 자사 AI 기본 요소, JSON:API 리소스, 의미 체계/벡터 검색 기능, 대기열, 캐시 및 보안 전반에 걸친 점진적인 개선 사항이 포함되어 있습니다.

<a name="minimal-breaking-changes"></a>
### 최소한의 주요 변경 사항

이번 릴리스 주기 동안 우리의 초점은 주요 변경 사항을 최소화하는 것이었습니다. 대신, 우리는 기존 애플리케이션을 손상시키지 않는 지속적인 삶의 질 개선을 일년 내내 제공하는 데 전념해 왔습니다.

따라서 Laravel 13 릴리스는 노력 측면에서 상대적으로 사소한 업그레이드이면서도 여전히 상당한 새로운 기능을 제공합니다. 이를 고려하여 대부분의 Laravel 애플리케이션은 애플리케이션 코드를 많이 변경하지 않고도 Laravel 13으로 업그레이드할 수 있습니다.

<a name="php-8"></a>
### PHP 8.3

Laravel 13.x에는 최소 PHP 버전 8.3이 필요합니다.

<a name="ai-sdk"></a>
### 라라벨 AI SDK

Laravel 13은 텍스트 생성, 도구 호출 에이전트, 임베딩, 오디오, 이미지 및 벡터 저장소 통합을 위한 통합 API를 제공하는 자사 [Laravel AI SDK](https://laravel.com/ai)를 도입합니다.

AI SDK를 사용하면 일관적인 Laravel 기본 개발자 경험을 유지하면서 공급자에 구애받지 않는 AI 기능을 구축할 수 있습니다.

예를 들어 기본 상담원은 한 번의 통화로 메시지를 받을 수 있습니다.

```php
use App\Ai\Agents\SalesCoach;

$response = SalesCoach::make()->prompt('Analyze this sales transcript...');

return (string) $response;

```

Laravel AI SDK는 이미지, 오디오 및 임베딩도 생성할 수 있습니다.

시각적 생성 사용 사례의 경우 SDK는 일반 언어 프롬프트에서 이미지를 생성하기 위한 깔끔한 API를 제공합니다.

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;

```

음성 경험의 경우 보조자, 내레이션 및 접근성 기능을 위해 텍스트에서 자연스러운 오디오를 합성할 수 있습니다.

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;

```

의미론적 검색 및 검색 워크플로를 위해 문자열에서 직접 임베딩을 생성할 수 있습니다.

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();

```

<a name="json-api"></a>
### JSON:API 리소스

이제 Laravel에는 자사 [JSON:API 리소스](/docs/{{version}}/eloquent-resources#jsonapi-resources)가 포함되어 있어 JSON:API 사양을 준수하는 응답을 간단하게 반환할 수 있습니다.

JSON:API 리소스는 리소스 개체 직렬화, 관계 포함, 희소 필드 집합, 링크 및 JSON:API 호환 응답 헤더를 처리합니다.

<a name="request-forgery-protection"></a>
### 위조방지요청

보안을 위해 Laravel의 [요청 위조 방지](/docs/{{version}}/csrf#preventing-csrf-requests) 미들웨어는 토큰 기반 CSRF 보호와의 호환성을 유지하면서 원본 인식 요청 확인을 추가하여 `PreventRequestForgery`로 향상되고 공식화되었습니다.

<a name="queue-routing"></a>
### 대기열 라우팅

Laravel 13은 `Queue::route(...)`를 통해 [클래스별 대기열 라우팅](/docs/{{version}}/queues#queue-routing)을 추가하여 중앙 위치에서 특정 작업에 대한 기본 대기열/연결 라우팅 규칙을 정의할 수 있도록 합니다.

```php
Queue::route(ProcessPodcast::class, connection: 'redis', queue: 'podcasts');

```

<a name="php-attributes"></a>
### 확장된 PHP 속성

Laravel 13은 프레임워크 전반에 걸쳐 자사 PHP 속성 지원을 계속 확장하여 일반적인 구성 및 동작 문제를 보다 선언적으로 만들고 클래스 및 메서드와 함께 배치합니다.

주목할만한 추가 사항에는 [`#[Middleware]`](/docs/{{version}}/controllers#controller-middleware) 및 [`#[Authorize]`](/docs/{{version}}/controllers#authorization-attributes)와 같은 컨트롤러 및 인증 속성과 [`#[Tries]`](/docs/{{version}}/queues#max-job-attempts-and-timeout)와 같은 대기열 기반 작업 제어가 포함됩니다. [`#[Backoff]`](/docs/{{version}}/queues#dealing-with-failed-jobs), [`#[Timeout]`](/docs/{{version}}/queues#max-job-attempts-and-timeout) 및 [`#[FailOnTimeout]`](/docs/{{version}}/queues#failing-on-timeout).

예를 들어, 이제 컨트롤러 미들웨어 및 정책 검사를 클래스 및 메서드에서 직접 선언할 수 있습니다.

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class CommentController
{
    #[Middleware('subscribed')]
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }
}

```

또한 Eloquent, 이벤트, 알림, 검증, 테스트 및 리소스 직렬화 API 전반에 걸쳐 추가 속성이 도입되어 프레임워크의 더 많은 영역에서 일관된 속성 우선 옵션을 제공합니다.

<a name="cache-touch"></a>
### 캐시 TTL 확장

Laravel에는 이제 [`Cache::touch(...)`](/docs/{{version}}/cache)가 포함되어 있어 해당 값을 검색하고 다시 저장하지 않고도 기존 캐시 항목의 TTL을 확장할 수 있습니다.

<a name="semantic-search"></a>
### 의미/벡터 검색

Laravel 13은 [검색](/docs/{{version}}/search#semantic-vector-search), [쿼리](/docs/{{version}}/queries#vector-similarity-clauses) 및 [AI SDK](/docs/{{version}}/ai-sdk#embeddings)에 걸쳐 문서화된 기본 벡터 쿼리 지원, 임베딩 워크플로 및 관련 API를 통해 의미론적 검색 스토리를 심화합니다.

이러한 기능을 사용하면 문자열에서 직접 생성된 임베딩에 대한 유사성 검색을 포함하여 PostgreSQL + `pgvector`를 사용하여 AI 기반 검색 환경을 간단하게 구축할 수 있습니다.

예를 들어 쿼리 빌더에서 직접 의미 유사성 검색을 실행할 수 있습니다.

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();

```
{% endraw %}
