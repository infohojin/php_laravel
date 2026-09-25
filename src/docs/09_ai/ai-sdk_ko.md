---
layout: docs
title: "Laravel AI SDK"
---

{% raw %}
# Laravel AI SDK

- [Introduction](#introduction)
- [Installation](#installation)
    - [Configuration](#configuration)
    - [Custom Base URLs](#custom-base-urls)
    - [OpenAI-Compatible Providers](#openai-compatible-providers)
    - [Provider Support](#provider-support)
- [Agents](#agents)
    - [Prompting](#prompting)
    - [Conversation Context](#conversation-context)
    - [Structured Output](#structured-output)
    - [Attachments](#attachments)
    - [Streaming](#streaming)
    - [Broadcasting](#broadcasting)
    - [Queueing](#queueing)
    - [Tools](#tools)
    - [Deferred Tool Loading](#deferred-tool-loading)
    - [File Storage Tools](#file-storage-tools)
    - [MCP Tools](#mcp-tools)
    - [Provider Tools](#provider-tools)
    - [Sub-Agents](#sub-agents)
    - [Middleware](#middleware)
    - [Anonymous Agents](#anonymous-agents)
    - [Agent Configuration](#agent-configuration)
    - [Provider Options](#provider-options)
    - [Prompt Caching](#prompt-caching)
- [Human Tool Approval](#human-tool-approval)
    - [Complete Approval Flow](#complete-approval-flow)
- [Images](#images)
- [Audio (TTS)](#audio)
- [Transcription (STT)](#transcription)
- [Text Summarization](#text-summarization)
- [Embeddings](#embeddings)
    - [Multimodal Embeddings](#multimodal-embeddings)
    - [Querying Embeddings](#querying-embeddings)
    - [Caching Embeddings](#caching-embeddings)
- [Reranking](#reranking)
- [Classification](#classification)
- [Files](#files)
- [Vector Stores](#vector-stores)
    - [Adding Files to Stores](#adding-files-to-stores)
- [Usage](#usage)
- [Failover](#failover)
- [Testing](#testing)
    - [Agents](#testing-agents)
    - [Images](#testing-images)
    - [Audio](#testing-audio)
    - [Transcriptions](#testing-transcriptions)
    - [Embeddings](#testing-embeddings)
    - [Reranking](#testing-reranking)
    - [Classification](#testing-classification)
    - [Files](#testing-files)
    - [Vector Stores](#testing-vector-stores)
- [Events](#events)

<a name="introduction"></a>
## Introduction

The [Laravel AI SDK](https://github.com/laravel/ai) provides a unified, expressive API for interacting with AI providers such as OpenAI, Anthropic, Gemini, and more. With the AI SDK, you can build intelligent agents with tools and structured output, generate images, synthesize and transcribe audio, create vector embeddings, and much more — all using a consistent, Laravel-friendly interface.



<a name="installation"></a>
## 설치

Composer를 통해 Laravel AI SDK를 설치할 수 있습니다:

```shell
composer require laravel/ai
```



다음으로, `vendor:publish` Artisan 명령어를 사용하여 AI SDK 구성 및 마이그레이션 파일을 게시해야 합니다:

```shell
php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```



마지막으로, 애플리케이션의 데이터베이스 마이그레이션을 실행해야 합니다. 이는 AI SDK가 대화 저장소를 구동하는 데 사용하는 `agent_conversations`와 `agent_conversation_messages` 테이블을 생성합니다:

```shell
php artisan migrate
```



<a name="configuration"></a>
### 구성

애플리케이션의 `config/ai.php` 구성 파일이나 애플리케이션의 `.env` 파일에서 환경 변수로 AI 공급자 자격 증명을 정의할 수 있습니다:

```ini
ANTHROPIC_API_KEY=
AZURE_OPENAI_API_KEY=
COHERE_API_KEY=
DEEPSEEK_API_KEY=
ELEVENLABS_API_KEY=
GEMINI_API_KEY=
GROQ_API_KEY=
MISTRAL_API_KEY=
OLLAMA_API_KEY=
OPENAI_API_KEY=
OPENAI_COMPATIBLE_API_KEY=
OPENAI_COMPATIBLE_URL=
OPENROUTER_API_KEY=
JINA_API_KEY=
TYPESAFE_API_KEY=
VOYAGEAI_API_KEY=
XAI_API_KEY=
```



텍스트, 이미지, 오디오, 전사 및 임베딩에 사용되는 기본 모델은 애플리케이션의 `config/ai.php` 구성 파일에서도 설정할 수 있습니다.

<a name="custom-base-urls"></a>
### 사용자 정의 기본 URL

기본적으로 Laravel AI SDK는 각 제공자의 공개 API 엔드포인트에 직접 연결합니다. 그러나 요청을 다른 엔드포인트를 통해 라우팅해야 할 수도 있습니다. 예를 들어, API 키 관리를 중앙 집중화하거나 속도 제한을 구현하거나 트래픽을 기업 게이트웨이를 통해 라우팅할 때 프록시 서비스를 사용하는 경우가 있습니다.

공급자 구성에 `url` 매개변수를 추가하여 사용자 정의 기본 URL을 구성할 수 있습니다:

```php
'providers' => [
    'openai' => [
        'driver' => 'openai',
        'key' => env('OPENAI_API_KEY'),
        'url' => env('OPENAI_URL'),
    ],

    'anthropic' => [
        'driver' => 'anthropic',
        'key' => env('ANTHROPIC_API_KEY'),
        'url' => env('ANTHROPIC_BASE_URL'),
    ],
],
```



프록시 서비스(예: LiteLLM 또는 Azure OpenAI Gateway)를 통해 요청을 라우팅하거나 대체 엔드포인트를 사용할 때 유용합니다.

다음 제공업체에 대해 사용자 지정 기본 URL이 지원됩니다: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI 및 OpenRouter.

<a name="openai-compatible-providers"></a>
### OpenAI 호환 제공업체

LM Studio, vLLM, Together, Fireworks 또는 로컬 게이트웨이와 같은 OpenAI 호환 API를 사용하는 경우, `openai-compatible` 제공업체를 구성할 수 있습니다. `url` 옵션은 필수이며, `key` 옵션은 선택 사항으로 존재할 경우 Bearer 토큰으로 전송됩니다:

```php
'providers' => [
    'local' => [
        'driver' => 'openai-compatible',
        'url' => env('LOCAL_AI_URL'),
        'key' => env('LOCAL_AI_API_KEY'),
    ],
],
```



한 번 구성되면, 다른 공급자처럼 이름이 지정된 공급자를 사용할 수 있습니다:

```php
agent()->prompt('What is Laravel?', provider: 'local', model: 'local-model');
```



프로바이더에 대해 기본 텍스트 모델을 구성할 수도 있으므로 모델을 명시적으로 전달할 필요가 없습니다:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'text' => [
            'default' => env('LOCAL_AI_MODEL'),
        ],
    ],
],
```



구성에서 `headers` 배열을 정의하여 공급자의 모든 나가는 요청에 사용자 지정 HTTP 헤더를 추가할 수 있습니다. 이는 엔드포인트가 베어러 토큰 외에 추가 식별 또는 인증 헤더를 필요로 할 때 유용합니다:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'headers' => [
        'X-Tenant-Id' => env('LOCAL_AI_TENANT_ID'),
    ],
],
```



OpenAI 호환 공급자는 텍스트 생성, 스트리밍, 도구, 구조화된 출력, 이미지 첨부, 임베딩 및 전사 기능을 지원합니다. 엔드포인트에 추가 요청 본문 필드가 필요한 경우 [공급자 옵션](#provider-options)을 사용하여 제공하세요.

<a name="openai-compatible-embeddings"></a>
#### OpenAI 호환 임베딩

임의의 엔드포인트에는 알려진 모델이 없으므로, OpenAI 호환 공급자와 함께 `embeddings()`를 사용하기 위해 기본 임베딩 모델을 구성해야 합니다. 고정 차원 값을 설정할 수도 있으며, 생략하면 `dimensions` 매개변수 없이 요청이 전송되고 모델의 기본 차원이 사용됩니다.

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'embeddings' => [
            'default' => 'text-embedding-qwen3-embedding-0.6b',
            'dimensions' => 1024, // optional
        ],
    ],
],
```



<a name="openai-compatible-transcriptions"></a>
#### OpenAI 호환 전사

마찬가지로, OpenAI 호환 공급자를 사용하여 `Transcription`를 사용하도록 기본 전사 모델을 구성해야 합니다. 오디오 파일은 표준 멀티파트 요청으로 엔드포인트의 `/audio/transcriptions` 경로에 업로드됩니다:

```php
'local' => [
    'driver' => 'openai-compatible',
    'url' => env('LOCAL_AI_URL'),
    'key' => env('LOCAL_AI_API_KEY'),
    'models' => [
        'transcription' => [
            'default' => 'whisper-1',
        ],
    ],
],
```



> [!NOTE]
> OpenAI-compatible and Groq providers do not support diarization. Invoking the `diarize` method when using these providers will throw an exception.

<a name="provider-support"></a>
### Provider Support

The AI SDK supports a variety of providers across its features. The following table summarizes which providers are available for each feature:

<div class="overflow-auto">

| Feature | Providers |
|---|---|
| Text | OpenAI, OpenAI Compatible, Anthropic, Gemini, Azure, Bedrock, Groq, xAI, DeepSeek, Mistral, Ollama, OpenRouter |
| Images | OpenAI, Gemini, xAI, Azure, Bedrock, OpenRouter |
| TTS | OpenAI, ElevenLabs, Gemini, Mistral, OpenRouter |
| STT | OpenAI, OpenAI Compatible, ElevenLabs, Groq, Mistral, Gemini, OpenRouter |
| Embeddings | OpenAI, OpenAI Compatible, Gemini, Azure, Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter |
| Reranking | Cohere, Jina, VoyageAI, Bedrock, OpenRouter |
| Classification | TypeSafe, OpenRouter |
| Files | OpenAI, Anthropic, Gemini, Azure, OpenRouter |

</div>

The `Laravel\Ai\Enums\Lab` enum may be used to reference providers throughout your code instead of using plain strings:

```php
use Laravel\Ai\Enums\Lab;

Lab::Anthropic;
Lab::OpenAI;
Lab::OpenAiCompatible;
Lab::Gemini;
// ...
```



<a name="agents"></a>
## 에이전트

에이전트는 Laravel AI SDK에서 AI 제공자와 상호작용하기 위한 기본 구성 요소입니다. 각 에이전트는 대규모 언어 모델과 상호작용하는 데 필요한 지침, 대화 맥락, 도구 및 출력 스키마를 캡슐화하는 전용 PHP 클래스입니다. 에이전트를 전문화된 보조자 — 판매 코치, 문서 분석기, 지원 봇 —로 생각할 수 있으며, 애플리케이션 전반에서 필요할 때마다 구성하고 프롬프트를 보낼 수 있습니다.

`make:agent` Artisan 명령어를 통해 에이전트를 생성할 수 있습니다:

```shell
php artisan make:agent SalesCoach

php artisan make:agent SalesCoach --structured
```



생성된 에이전트 클래스 내에서 시스템 프롬프트/지침, 메시지 컨텍스트, 사용 가능한 도구 및 출력 스키마(해당되는 경우)를 정의할 수 있습니다:

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Tools\RetrievePreviousTranscripts;
use App\Models\History;
use App\Models\User;
use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Messages\Message;
use Laravel\Ai\Promptable;
use Stringable;

class SalesCoach implements Agent, Conversational, HasTools, HasStructuredOutput
{
    use Promptable;

    public function __construct(public User $user) {}

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): Stringable|string
    {
        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';
    }

    /**
     * Get the list of messages comprising the conversation so far.
     */
    public function messages(): iterable
    {
        return History::where('user_id', $this->user->id)
            ->latest()
            ->limit(50)
            ->get()
            ->reverse()
            ->map(function ($message) {
                return new Message($message->role, $message->content);
            })->all();
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RetrievePreviousTranscripts,
        ];
    }

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'feedback' => $schema->string()->required(),
            'score' => $schema->integer()->min(1)->max(10)->required(),
        ];
    }
}
```



<a name="prompting"></a>
### 프롬프트 작성

에이전트를 프롬프트하기 위해 먼저 `make` 메서드나 표준 인스턴스를 사용하여 인스턴스를 생성한 다음, `prompt`를 호출하세요:

```php
$response = (new SalesCoach)
    ->prompt('Analyze this sales transcript...');

return (string) $response;
```



`make` 메서드는 컨테이너에서 에이전트를 분리하여 자동 의존성 주입을 가능하게 합니다. 또한 에이전트의 생성자에 인수를 전달할 수도 있습니다:

```php
$agent = SalesCoach::make(user: $user);
```



`prompt` 메서드에 추가 인수를 전달하면 프롬프트를 실행할 때 기본 제공자, 모델 또는 HTTP 시간 제한을 재정의할 수 있습니다:

```php
$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 120,
);
```



<a name="raw-http-responses"></a>
#### 원시 HTTP 응답

텍스트 생성 에이전트에서 반환되는 모든 응답은 기본 제공자의 API 호출에서 온 원시 HTTP 응답을 `raw` 속성을 통해 노출합니다. 이를 통해 AI SDK의 일반 응답에 포함되지 않은 제공자별 정보에 접근할 수 있습니다 - 속도 제한 헤더, 요청 ID, 또는 기타 정확한 페이로드 필드:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

$response->raw; // Illuminate\Http\Client\Response|null

$response->raw->header('X-RateLimit-Remaining-Requests');
$response->raw->json('id');
```



툴 호출 루프에서 각 단계는 자신의 요청에 대한 원시 응답을 유지합니다:

```php
foreach ($response->steps as $step) {
    $step->raw?->header('X-RateLimit-Remaining-Requests');
}
```



> **참고:** `raw` 속성은 스트리밍 응답 시, Bedrock 공급자(AWS SDK를 통해 API 호출을 수행하며 HTTP 클라이언트를 사용하지 않음)를 사용할 때, 그리고 명시적으로 `withRawResponse`를 통해 제공되지 않은 가짜 응답에서 `null`입니다.

<a name="conversation-context"></a>
### 대화 맥락

에이전트가 `Conversational` 인터페이스를 구현하는 경우, 해당되는 경우 이전 대화 맥락을 반환하기 위해 `messages` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the list of messages comprising the conversation so far.
 */
public function messages(): iterable
{
    return $this->user->history()
        ->latest()
        ->limit(50)
        ->get()
        ->reverse()
        ->map(fn ($message) => new Message(
            $message->role, $message->content,
        ))->all();
}
```



에이전트가 `Conversational` 인터페이스를 구현하지 않는 경우, 단일 실행에 대한 대화 기록을 제공하기 위해 `withMessages` 메서드를 사용할 수 있습니다. 예를 들어, 애플리케이션의 프론트엔드에서 게시한 기록과 같은 경우입니다:

```php
use Laravel\Ai\Messages\Message;

$response = (new SalesCoach)
    ->withMessages([
        new Message('user', 'Analyze this sales transcript...'),
        new Message('assistant', 'The rep never asked for the close.'),
    ])
    ->prompt('What should they say next time?');
```



`Conversational` 인터페이스를 구현하는 에이전트는 자신의 히스토리를 로드하므로, 두 가지 접근 방식을 결합하면 `LogicException`가 발생합니다.

<a name="remembering-conversations"></a>
#### 대화 기억하기

> **경고:** `RemembersConversations` 트레이트를 사용하기 전에, `vendor:publish` Artisan 명령어를 사용하여 AI SDK 마이그레이션을 배포하고 실행해야 합니다. 이 마이그레이션은 대화를 저장하기 위한 필요한 데이터베이스 테이블을 생성합니다.

Laravel이 자동으로 에이전트의 대화 히스토리를 저장하고 불러오게 하고 싶다면, `RemembersConversations` 트레이트를 사용할 수 있습니다. 이 트레이트는 `Conversational` 인터페이스를 수동으로 구현하지 않고도 대화 메시지를 데이터베이스에 간단히 저장할 수 있는 방법을 제공합니다.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Concerns\RemembersConversations;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\Conversational;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, Conversational
{
    use Promptable, RemembersConversations;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You are a sales coach...';
    }
}
```



`RemembersConversations` 트레이트를 사용할 때, 에이전트 클래스에 `messages` 메서드를 수동으로 정의하지 마세요. `messages` 메서드가 존재하면, 해당 메서드가 트레이트의 구현보다 우선하며 대화 기록이 데이터베이스에서 로드되지 않습니다.

사용자를 위한 새로운 대화를 시작하려면, 프롬프트를 호출하기 전에 `forUser` 메서드를 호출하세요:

```php
$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

$conversationId = $response->conversationId;
```



대화 ID는 응답에 반환되며 나중에 참조할 수 있도록 저장할 수 있습니다. Eloquent를 사용하여 사용자의 모든 대화를 가져오려면 사용자 모델에 `HasConversations` 트레이트를 추가할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Ai\Concerns\HasConversations;

class User extends Authenticatable
{
    use HasConversations;
}
```



특성이 모델에 추가되면 `conversations` 관계를 통해 사용자의 대화를 가져오고 조회할 수 있습니다:

```php
$conversations = $user->conversations()
    ->latest('updated_at')
    ->paginate(20);
```



기존 대화를 계속하려면 `continue` 방법을 사용하세요:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $user)
    ->prompt('Tell me more about that.');
```



`continueOrStart` 방법은 주어진 대화를 계속 진행하는 데 사용되거나, 주어진 ID가 `null`인 경우 새로운 대화를 시작하는 데 사용될 수 있습니다:

```php
$response = (new SalesCoach)
    ->continueOrStart($conversationId, as: $user)
    ->prompt('Hello!');
```



`RemembersConversations` 특성을 사용할 때, 이전 메시지는 자동으로 불러와져 프롬프트 시 대화 맥락에 포함됩니다. 새로운 메시지(사용자 및 어시스턴트 모두)는 각 상호작용 후 자동으로 저장됩니다. 각 응답에는 저장된 대화 및 메시지의 ID도 포함됩니다:

```php
$response->conversationId;
$response->userMessageId;
$response->assistantMessageId;
```



<a name="conversation-participants"></a>
#### 대화 참여자

사용자가 가장 일반적인 대화 참여자이긴 하지만, 대화는 어떤 Eloquent 모델에도 속할 수 있습니다. 다른 유형의 모델에 대한 대화를 시작하려면 `forParticipant` 방법을 사용하십시오:

```php
$response = (new SalesCoach)
    ->forParticipant($team)
    ->prompt('Review our latest sales results.');
```



참가자의 형태소 클래스와 기본 키는 대화와 함께 저장됩니다. 따라서 `User` ID `1`와 `Team` ID `1`처럼 동일한 기본 키를 가진 서로 다른 유형의 모델은 별도의 대화 기록을 가집니다. `forUser` 메서드는 `forParticipant`의 별칭입니다.

`continueLastConversation` 메서드를 사용하여 참가자의 가장 최근 대화를 에이전트와 계속할 수 있습니다. 대화는 에이전트를 기준으로 범위가 지정되므로, 에이전트가 참여한 대화만 계속됩니다:

```php
$response = (new SalesCoach)
    ->continueLastConversation($team)
    ->prompt('Tell me more about that.');
```



특정 대화를 계속할 때, 참가자를 `continue` 방법에 전달하세요:

```php
$response = (new SalesCoach)
    ->continue($conversationId, as: $team)
    ->prompt('Tell me more about that.');
```



`HasConversations` 트레이트는 대화에 참여하는 모든 Eloquent 모델에 추가될 수 있습니다. 그 결과 생성된 `conversations` 관계는 해당 모델의 타입과 기본 키에 맞춰 범위가 지정된 다형 관계입니다. 또한 대화를 소유한 참여자에게 반대 관계를 통해 접근할 수도 있습니다:

```php
$conversations = $team->conversations;

$participant = $conversation->participant;
```



응용 프로그램이 여러 참가자 모델 유형을 사용하는 경우, 저장된 참가자 유형이 모델 클래스 이름과 결합되지 않도록 [Eloquent morph map](/docs/{{version}}/eloquent-relationships#custom-polymorphic-types)을 정의하는 것을 고려해야 합니다.

> [!WARNING]
> `continue` 및 `continueOrStart` 메서드는 지정된 참가자가 대화를 소유하고 있는지 확인하지 않습니다. 응용 프로그램은 대화를 계속 진행하기 전에 해당 대화에 대한 접근 권한을 확인해야 합니다.

<a name="inspecting-stored-conversations"></a>
#### 저장된 대화 검사하기

사용자에게 대화를 표시할 때, 메시지 ID, 타임스탬프, 도구 호출과 같은 세부 정보가 필요할 때가 많습니다. 대화를 직접 AI SDK의 테이블에서 조회하지 않고 저장된 메시지를 읽기 위해 서비스 컨테이너에서 대화 저장소를 해결할 수 있습니다:

```php
use Laravel\Ai\Contracts\ConversationStore;

$store = app(ConversationStore::class);
```



메시지는 커서를 사용하여 최신 순으로 페이지가 나뉘며, 각 메시지의 ID, 타임스탬프, 사용량, 메타데이터 및 첨부 파일을 포함하는 `StoredMessage` 인스턴스로 반환됩니다:

```php
$messages = $store->paginateConversationMessages($conversationId, perPage: 25);

foreach ($messages as $message) {
    $message->id;
    $message->role;
    $message->content;
    $message->createdAt;
    $message->usage;
    $message->status;
}
```



각 턴은 사용자 프롬프트와 어시스턴트의 응답으로 구성되며, 단계 목록으로 저장됩니다. 단계는 공급자에게 보내는 단일 요청이므로, 모델이 도구를 호출하는 턴에는 여러 단계가 포함될 수 있습니다. 각 도구 결과는 그것을 생성한 도구 호출에 기록됩니다. `toolCalls`, `providerToolCalls`, `toolResults` 메서드는 이러한 단계를 순서대로 펼치므로, 직접 탐색할 필요가 없습니다:

```php
$message->steps;

$message->toolCalls();
$message->providerToolCalls();
$message->toolResults();
```



도구 호출은 실행된 후 `result`를 포함합니다. `result`가 없고 `approval_reason`를 포함하는 도구 호출은 여전히 [도구 승인](#human-tool-approval)을 기다리고 있습니다.

`status` 속성에는 `Laravel\Ai\Enums\MessageStatus` 인스턴스가 포함됩니다. 도중에 실패한 턴은 이미 완료된 단계와 함께 `Failed`로 저장되므로, 실패 이전에 실행된 도구 호출은 기록에 남아 있습니다. 대화가 계속될 때, 결과가 기록되지 않은 모든 도구 호출은 모델에 중단된 것으로 표시되어 보내집니다. 이는 Laravel이 도구 호출이 실행되었는지 여부를 판단할 수 없기 때문입니다.

애플리케이션 프런트엔드에서 제공된 ID를 통해 대화를 계속하기 전에, 해당 참가자에 대해 대화가 저장되었는지 확인해야 합니다:

```php
abort_unless($store->conversationBelongsTo(
    $conversationId, $user->getMorphClass(), $user->getKey()
), 403);
```



가장 최근의 턴이 [도구 승인](#human-tool-approval)을 기다리며 일시 중지된 경우, 실행을 재개하지 않고 페이지를 새로 고친 후 보류 중인 도구 호출을 렌더링할 수 있습니다:

```php
foreach ($store->pendingApprovalsFor($conversationId) as $approval) {
    // $approval->id, $approval->tool, $approval->arguments, $approval->reason...
}
```



이 메서드들은 `PaginatesConversations`, `VerifiesConversationOwnership`, `ResolvesPendingApprovals` 계약에 의해 정의됩니다. 포함된 데이터베이스 스토어는 세 가지 모두를 구현하며, 커스텀 스토어는 필요한 계약만 구현할 수 있습니다.

<a name="structured-output"></a>
### 구조화된 출력

에이전트가 구조화된 출력을 반환하도록 하려면, `HasStructuredOutput` 인터페이스를 구현해야 하며, 이는 에이전트가 `schema` 메서드를 정의해야 함을 요구합니다:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
        ];
    }
}
```



구조화된 출력을 반환하는 에이전트를 프롬프트할 때, 반환된 `StructuredAgentResponse`에 배열처럼 접근할 수 있습니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

return $response['score'];
```



<a name="structured-output-nested-objects"></a>
#### 중첩된 객체

중첩된 구조화된 출력을 정의하려면, 클로저와 함께 `object` 방법을 사용하세요:

```php
<?php

namespace App\Ai\Agents;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasStructuredOutput;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasStructuredOutput
{
    use Promptable;

    // ...

    /**
     * Get the agent's structured output schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'score' => $schema->integer()->required(),
            'metadata' => $schema->object(fn ($schema) => [
                'confidence' => $schema->string()->enum(['low', 'medium', 'high'])->required(),
                'language' => $schema->string()->required(),
            ])->required(),
        ];
    }
}
```



<a name="structured-output-arrays-of-objects"></a>
#### 객체 배열

에이전트가 구조화된 항목 목록을 반환해야 하는 경우, `array`와 `object` 방법을 결합하십시오:

```php
public function schema(JsonSchema $schema): array
{
    return [
        'feedback' => $schema->array()
            ->items(
                $schema->object(fn ($schema) => [
                    'comment' => $schema->string()->required(),
                    'score' => $schema->integer()->required(),
                ])
            )
            ->required(),
    ];
}
```



값이 여러 스키마 중 하나와 일치할 수 있는 경우, `anyOf` 방법을 사용하십시오:

```php
public function schema(JsonSchema $schema): array
{
    return [
        'content' => $schema->anyOf([
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['article'])->required(),
                'title' => $schema->string()->required(),
            ]),
            $schema->object(fn ($schema) => [
                'type' => $schema->string()->enum(['image'])->required(),
                'url' => $schema->string()->required(),
            ]),
        ])->required(),
    ];
}
```



<a name="attachments"></a>
### 첨부 파일

프롬프트 작성 시 모델이 이미지 및 문서를 검사할 수 있도록 첨부 파일을 함께 전달할 수도 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromStorage('transcript.pdf'), // Attach a document from a filesystem disk...
        Files\Document::fromPath('/home/laravel/transcript.md'), // Attach a document from a local path...
        $request->file('transcript'), // Attach an uploaded file...
    ]
);
```



마찬가지로, `Laravel\Ai\Files\Image` 클래스는 프롬프트에 이미지를 첨부하는 데 사용할 수 있습니다:

```php
use App\Ai\Agents\ImageAnalyzer;
use Laravel\Ai\Files;

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Files\Image::fromStorage('photo.jpg'), // Attach an image from a filesystem disk...
        Files\Image::fromPath('/home/laravel/photo.jpg'), // Attach an image from a local path...
        $request->file('photo'), // Attach an uploaded file...
    ]
);
```



<a name="streaming"></a>
### 스트리밍

`stream` 메서드를 호출하여 에이전트의 응답을 스트리밍할 수 있습니다. 반환된 `StreamableAgentResponse`는 라우트에서 반환되어 클라이언트에게 스트리밍 응답(SSE)을 자동으로 보낼 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)->stream('Analyze this sales transcript...');
});
```



`then` 메서드는 전체 응답이 클라이언트로 스트리밍된 후 호출될 클로저를 제공하는 데 사용될 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Responses\StreamedAgentResponse;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->then(function (StreamedAgentResponse $response) {
            // $response->text, $response->events, $response->usage...
        });
});
```



또는 스트리밍된 이벤트를 수동으로 반복할 수 있습니다:

```php
$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    // ...
}
```



응답에는 모델의 추론과 모델이 인용한 모든 출처도 포함됩니다. 둘 다 `RemembersConversations` 속성을 사용할 때 어시스턴트 메시지와 함께 저장됩니다:

```php
use Laravel\Ai\Responses\StreamedAgentResponse;

(new SalesCoach)
    ->stream('Analyze this sales transcript...')
    ->then(function (StreamedAgentResponse $response) {
        $response->reasoning; // '' unless the model returned reasoning text...
        $response->meta->citations;
    });
```



추론은 `prompt` 메서드가 반환하는 응답에서도 사용할 수 있습니다.

<a name="streaming-using-the-vercel-ai-sdk-protocol"></a>
<a name="stream-protocols"></a>
#### 스트림 프로토콜

기본적으로 스트리밍된 응답은 AI SDK 자체 이벤트 형식을 사용합니다. 그러나 자신만의 채팅 인터페이스를 구축하는 대신 기존 채팅 인터페이스와 에이전트를 연결할 수 있는 프론트엔드 스트리밍 프로토콜을 사용할 수도 있습니다.

스트리밍 가능한 응답에서 `usingVercelDataProtocol` 메서드를 호출하여 [Vercel AI SDK 스트림 프로토콜](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol)을 사용해 이벤트를 스트리밍할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;

Route::get('/coach', function () {
    return (new SalesCoach)
        ->stream('Analyze this sales transcript...')
        ->usingVercelDataProtocol();
});
```



애플리케이션의 프런트엔드가 자체적으로 메시지 ID를 할당하는 경우 메시지 ID를 전달할 수 있습니다:

```php
->usingVercelDataProtocol($request->string('messageId'));
```



또는 `usingAgentUserInteractionProtocol` 방법을 사용하여 [에이전트 사용자 상호작용(AG-UI) 프로토콜](https://docs.ag-ui.com)을 통해 스트리밍할 수 있습니다:

```php
Route::post('/coach', function (Request $request) {
    return (new SalesCoach)
        ->forUser($request->user())
        ->stream($request->string('prompt'))
        ->usingAgentUserInteractionProtocol();
});
```



`threadId` 및 `runId` 인수는 선택 사항이며 기본값은 대화 ID와 호출 ID입니다:

```php
->usingAgentUserInteractionProtocol(
    threadId: $request->input('threadId'),
    runId: $request->input('runId'),
);
```



AI SDK가 구현하지 않은 프로토콜을 사용하려면, 자신의 `Laravel\Ai\Streaming\Protocols\StreamProtocol` 구현을 `usingProtocol` 메서드에 전달할 수 있습니다:

```php
use App\Ai\Protocols\CustomProtocol;

return (new SalesCoach)
    ->stream('Analyze this sales transcript...')
    ->usingProtocol(new CustomProtocol);
```



<a name="chat-requests"></a>
<a name="frontend-integration"></a>
#### 프런트엔드 통합

Vercel의 `useChat` 또는 CopilotKit과 같은 라이브러리로 구축된 채팅 인터페이스는 이미 메시지, 도구 호출 및 승인 프롬프트를 렌더링하므로 애플리케이션은 그들이 보내는 요청만 처리하면 됩니다. 각 요청에는 대화 기록, 최신 사용자 메시지 및 도구 승인 응답이 포함됩니다.

`Vercel::chat` 및 `AgentUserInteraction::chat` 메서드는 이러한 요청을 에이전트의 `stream` 메서드에 직접 전달할 수 있는 객체로 변환합니다:

```php
use Laravel\Ai\Vercel\Vercel;

Route::post('/chat', function (Request $request) {
    $chat = Vercel::chat($request);

    return (new SupportAgent)
        ->withMessages($chat->history())
        ->stream($chat)
        ->usingProtocol($chat->protocol());
});
```



요청에 [승인 결정](#human-tool-approval)이 포함된 경우, 에이전트는 해당 결정을 다시 사용합니다. 그렇지 않으면, 에이전트는 요청의 최신 사용자 메시지와 첨부파일을 기반으로 프롬프트가 제공됩니다. `protocol` 메서드는 클라이언트가 사용하는 프로토콜을 반환합니다.

> [!NOTE]
> `Conversational` 인터페이스를 구현하는 에이전트는 자체 기록을 로드하므로, `withMessages` 메서드는 생략될 수 있습니다.

`AgentUserInteraction::chat` 메서드는 AG-UI 클라이언트에 동일한 API를 제공하며, 요청의 스레드 및 실행 ID도 포함됩니다:

```php
use Laravel\Ai\AgentUserInteraction\AgentUserInteraction;

$chat = AgentUserInteraction::chat($request);

$chat->threadId();
$chat->runId();
```



저장된 메시지를 클라이언트가 기대하는 형식으로 다시 변환하여, 페이지를 다시 로드한 후와 같이 이전 대화를 클라이언트가 표시할 수 있도록 할 수도 있습니다:

```php
$messages = $conversation->messages()->oldest()->get();

return ['messages' => Vercel::toUiMessages($messages)];
```



`AgentUserInteraction::toClientState` 메서드는 보류 중인 승인 인터럽트를 반환하는 것 외에도 AG-UI 클라이언트에 대해 동일한 변환을 수행합니다:

```php
return AgentUserInteraction::toClientState($messages);
```



<a name="broadcasting"></a>
### 방송

스트리밍된 이벤트를 몇 가지 다른 방법으로 방송할 수 있습니다. 먼저, 스트리밍된 이벤트에서 단순히 `broadcast` 또는 `broadcastNow` 메서드를 호출하면 됩니다:

```php
use App\Ai\Agents\SalesCoach;
use Illuminate\Broadcasting\Channel;

$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

foreach ($stream as $event) {
    $event->broadcast(new Channel('channel-name'));
}
```



또는 에이전트의 `broadcastOnQueue` 메서드를 호출하여 에이전트 작업을 대기열에 추가하고 사용 가능한 대로 스트리밍된 이벤트를 브로드캐스트할 수 있습니다:

```php
(new SalesCoach)->broadcastOnQueue(
    'Analyze this sales transcript...',
    new Channel('channel-name'),
);
```



<a name="skipping-oversized-events"></a>
#### 과도하게 큰 이벤트 건너뛰기

일부 방송 플랫폼은 WebSocket 메시지를 약 10KB로 제한합니다. 대용량 스트림 이벤트(예: 큰 툴 결과)는 이 제한을 초과하여 방송이 실패할 수 있습니다. `WithoutBroadcasting` 속성을 사용하여 특정 이벤트 유형을 방송에서 제외할 수 있습니다:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\WithoutBroadcasting;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;
use Laravel\Ai\Streaming\Events\ToolCall;
use Laravel\Ai\Streaming\Events\ToolResult;

#[WithoutBroadcasting(ToolCall::class, ToolResult::class)]
class SearchAgent implements Agent, HasTools
{
    use Promptable;

    // ...
}
```



제외된 이벤트는 절대 방송되지 않지만, 여전히 `agent_conversation_messages` 테이블에 저장되므로 스트림이 완료된 후 프런트엔드에서 전체 도구 데이터를 로드할 수 있습니다. 이는 큐 방식(`broadcastOnQueue`)과 동기 방식(`broadcast` / `broadcastNow`) 방송 모두에 적용됩니다.

<a name="queueing"></a>
### 큐잉

에이전트의 `queue` 메서드를 사용하면 에이전트를 프롬프트할 수 있지만, 응답을 백그라운드에서 처리하도록 하여 애플리케이션이 빠르고 반응성 있게 느껴지도록 할 수 있습니다. `then` 및 `catch` 메서드는 응답이 가능할 때 또는 예외가 발생할 때 호출될 클로저를 등록하는 데 사용할 수 있습니다.

```php
use Illuminate\Http\Request;
use Laravel\Ai\Responses\AgentResponse;
use Throwable;

Route::post('/coach', function (Request $request) {
    (new SalesCoach)
        ->queue($request->input('transcript'))
        ->then(function (AgentResponse $response) {
            // ...
        })
        ->catch(function (Throwable $e) {
            // ...
        });

    return back();
});
```



<a name="tools"></a>
### 도구

도구는 에이전트가 프롬프트에 응답하는 동안 활용할 수 있는 추가 기능을 제공하기 위해 사용될 수 있습니다. 도구는 `make:tool` Artisan 명령을 사용하여 생성할 수 있습니다:

```shell
php artisan make:tool RandomNumberGenerator
```



생성된 도구는 애플리케이션의 `app/Ai/Tools` 디렉토리에 배치됩니다. 각 도구는 에이전트가 도구를 사용해야 할 때 호출되는 `handle` 메서드를 포함하고 있습니다:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class RandomNumberGenerator implements Tool
{
    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'This tool may be used to generate cryptographically secure random numbers.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        return (string) random_int($request['min'], $request['max']);
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'min' => $schema->integer()->min(0)->required(),
            'max' => $schema->integer()->required(),
        ];
    }
}
```



도구를 정의한 후에는 해당 도구를 모든 에이전트의 `tools` 메서드에서 반환할 수 있습니다:

```php
use App\Ai\Tools\RandomNumberGenerator;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        new RandomNumberGenerator,
    ];
}
```



<a name="runtime-tool-overrides"></a>
#### 런타임 도구 재정의

`withTools` 메서드는 에이전트 인스턴스에 의해 선언된 도구를 교체하는 데 사용될 수 있습니다. 이는 테넌트별 또는 기능 플래그가 적용된 도구 세트에 유용합니다:

```php
$response = (new SupportAgent)
    ->withTools([new LookupOrder])
    ->prompt('Where is order 12345?');
```



에이전트가 선언한 도구를 받는 클로저를 전달할 수도 있으며, 이를 통해 도구를 추가하거나 필터링할 수 있습니다:

```php
$response = (new SupportAgent)
    ->withTools(fn (array $tools) => [...$tools, new LookupOrder])
    ->prompt('Where is order 12345?');
```



<a name="validating-tool-arguments"></a>
#### 도구 인수 검증

귀하의 도구 스키마가 모델이 제공할 수 있는 인수를 제한하지만, 요청의 `validate` 메서드를 사용하여 들어오는 인수를 검증할 수 있습니다:

```php
public function handle(Request $request): Stringable|string
{
    $validated = $request->validate([
        'city' => 'required|string',
        'days' => 'required|integer|max:7',
    ]);

    return $this->forecast($validated['city'], $validated['days']);
}
```



검증이 실패하면, 검증 메시지가 도구의 결과로 모델에 반환되어 모델이 인수를 수정하고 도구를 다시 호출할 수 있습니다.

<a name="repairing-tool-calls"></a>
#### 도구 호출 수정

`RepairToolCalls` 속성을 사용하여 모델이 알 수 없는 로컬 도구를 호출할 때 에이전트가 복구할 수 있도록 합니다. Laravel은 사용 가능한 로컬 도구의 이름과 함께 실패한 호출을 모델에 반환하여 호출을 수정할 수 있게 합니다:

```php
use Laravel\Ai\Attributes\RepairToolCalls;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;

#[RepairToolCalls]
class SupportAgent implements Agent, HasTools
{
    use Promptable;

    // ...
}
```



Laravel이 최대 단계를 자동으로 계산할 때, 이 속성은 수리된 호출에 대해 한 단계를 추가합니다. 명시적인 `MaxSteps` 제한은 변경되지 않습니다.

<a name="similarity-search"></a>
#### 유사도 검색

`SimilaritySearch` 도구를 사용하면 에이전트가 데이터베이스에 저장된 벡터 임베딩을 사용하여 주어진 쿼리와 유사한 문서를 검색할 수 있습니다. 이는 에이전트가 애플리케이션의 데이터를 검색할 수 있도록 할 때 검색 보강 생성(RAG)에 유용합니다.

가장 간단한 유사도 검색 도구 생성 방법은 벡터 임베딩이 있는 Eloquent 모델과 함께 `usingModel` 메서드를 사용하는 것입니다:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        SimilaritySearch::usingModel(Document::class, 'embedding'),
    ];
}
```



첫 번째 인수는 Eloquent 모델 클래스이고, 두 번째 인수는 벡터 임베딩을 포함하는 열입니다.

또한 `0.0`와 `1.0` 사이의 최소 유사성 임계값과 쿼리를 사용자화할 수 있는 클로저를 제공할 수도 있습니다:

```php
SimilaritySearch::usingModel(
    model: Document::class,
    column: 'embedding',
    minSimilarity: 0.7,
    limit: 10,
    query: fn ($query) => $query->where('published', true),
),
```



더 많은 제어를 위해, 검색 결과를 반환하는 커스텀 클로저를 사용하여 유사도 검색 도구를 만들 수 있습니다:

```php
use App\Models\Document;
use Laravel\Ai\Tools\SimilaritySearch;

public function tools(): iterable
{
    return [
        new SimilaritySearch(using: function (string $query) {
            return Document::query()
                ->where('user_id', $this->user->id)
                ->whereVectorSimilarTo('embedding', $query)
                ->limit(10)
                ->get();
        }),
    ];
}
```



`withDescription` 방법을 사용하여 도구의 설명을 사용자 정의할 수 있습니다:

```php
SimilaritySearch::usingModel(Document::class, 'embedding')
    ->withDescription('Search the knowledge base for relevant articles.'),
```



<a name="deferred-tool-loading"></a>
### 도구 지연 로딩

기본적으로, 에이전트가 제공하는 모든 도구는 각 요청과 함께 공급자에게 전송됩니다. 에이전트가 많은 수의 도구를 제공하는 경우, 이는 토큰을 소모하고 모델의 도구 선택 정확도를 낮출 수 있습니다. OpenAI 또는 Anthropic과 함께 `ToolSearch` 공급자 도구를 사용하면 도구 정의를 지연시켜 필요할 때만 공급자가 이를 로드하도록 할 수 있습니다:

```php
use App\Ai\Tools\RefundOrder;
use App\Ai\Tools\SearchInvoices;
use App\Ai\Tools\Weather;
use Laravel\Ai\Providers\Tools\ToolSearch;

public function tools(): iterable
{
    return [
        new Weather,
        new ToolSearch(tools: [
            new SearchInvoices,
            new RefundOrder,
        ]),
    ];
}
```



포장된 도구는 어떤 수정도 필요하지 않습니다. 공급자는 프롬프트와 관련될 때 해당 도구를 검색하고 로드하며, 이후 에이전트는 다른 도구처럼 이를 호출할 수 있습니다.

Anthropic을 사용할 때, `strategy` 인수를 사용하여 공급자가 연기된 도구를 어떻게 검색할지 결정할 수 있습니다. 지원되는 전략은 `regex`(기본값)과 `bm25`입니다:

```php
new ToolSearch(tools: [new SearchInvoices], strategy: 'bm25'),
```



Anthropic을 사용할 때, 추가적인 공급자별 옵션은 `withProviderOptions` 방법을 사용하여 검색 도구에 전달될 수 있습니다:

```php
(new ToolSearch(tools: [new SearchInvoices]))
    ->withProviderOptions(['cache_control' => ['type' => 'ephemeral']]),
```



> [!WARNING]
> 도구 검색을 지원하지 않는 제공자는 보류된 도구를 조용히 무시하는 대신 예외를 던집니다. 또한, Anthropic은 `ToolSearch` 래퍼 외부에서 적어도 하나의 도구가 제공되도록 요구합니다.

<a name="file-storage-tools"></a>
### 파일 스토리지 도구

`FileStorage` 도구 팩토리를 사용하면 에이전트가 Laravel [파일시스템 디스크](/docs/{{version}}/filesystem)에 접근할 수 있도록 할 수 있습니다. `all` 메서드는 에이전트가 지정된 디스크에서 파일을 나열, 읽기, 검사, URL 생성, 작성, 삭제 및 복사할 수 있는 도구를 반환합니다:

```php
use Laravel\Ai\Tools\FileStorage;

public function tools(): iterable
{
    return FileStorage::all('local');
}
```



에이전트가 파일만 검사할 수 있어야 한다면, `readOnly` 방법을 사용하세요:

```php
return FileStorage::readOnly('local');
```



이 메서드들은 `Illuminate\Support\Collection`를 반환하며, 에이전트에게 제공되는 도구를 추가로 필터링할 수 있게 합니다:

```php
use Laravel\Ai\Tools\Filesystem\DeleteFile;

return FileStorage::all('s3')
    ->reject(fn ($tool) => $tool instanceof DeleteFile);
```



<a name="mcp-tools"></a>
### MCP 도구

애플리케이션이 [Laravel MCP](/docs/{{version}}/mcp)를 사용하는 경우, 에이전트에게 [Model Context Protocol](https://modelcontextprotocol.io) 서버에서 제공하는 도구를 제공할 수 있습니다. [Laravel MCP 클라이언트](/docs/{{version}}/mcp#client)를 사용하면 원격 또는 로컬 MCP 서버에 연결하고 그 도구를 에이전트에게 직접 전달할 수 있습니다.

> [!NOTE]
> MCP 도구를 사용하려면 애플리케이션에 [Laravel MCP](/docs/{{version}}/mcp) 패키지가 설치되어 있어야 합니다.

MCP 클라이언트의 `tools` 메서드가 컬렉션을 반환하므로, `...` 연산자를 사용하여 에이전트의 `tools` 배열로 펼치세요:

```php
use App\Ai\Tools\RandomNumberGenerator;
use Laravel\Mcp\Client;

/**
 * Get the tools available to the agent.
 *
 * @return Tool[]
 */
public function tools(): iterable
{
    return [
        ...Client::web('https://mcp.example.com')
            ->withToken($token)
            ->tools(),

        new RandomNumberGenerator,
    ];
}
```



AI SDK는 각 MCP 도구를 자동으로 래핑하여 에이전트가 다른 도구처럼 호출할 수 있도록 합니다. 또한 [명명된 MCP 클라이언트](/docs/{{version}}/mcp#named-clients)를 사용할 수도 있습니다:

```php
use Laravel\Mcp\Facades\Mcp;

public function tools(): iterable
{
    return [
        ...Mcp::client('github')->tools(),
    ];
}
```



또는 [로컬 MCP 서버](/docs/{{version}}/mcp#client-connecting)에 연결하세요:

```php
use Laravel\Mcp\Client;

public function tools(): iterable
{
    return [
        ...Client::local('php', ['artisan', 'mcp:start'])->tools(),
    ];
}
```



MCP 클라이언트 생성 및 인증(베어러 토큰 및 OAuth 포함)에 대한 자세한 내용은 [MCP 클라이언트 문서](/docs/{{version}}/mcp#client)를 참조하십시오.

<a name="provider-tools"></a>
### 제공자 도구

제공자 도구는 AI 제공자가 기본적으로 구현한 특별한 도구로, 웹 검색, URL 가져오기, 파일 검색 등의 기능을 제공합니다. 일반 도구와 달리 제공자 도구는 귀하의 애플리케이션이 아닌 제공자가 직접 실행합니다.

제공자 도구는 에이전트의 `tools` 메서드를 통해 반환될 수 있습니다.

<a name="web-search"></a>
#### 웹 검색

`WebSearch` 제공자 도구를 사용하면 에이전트가 실시간 정보 검색을 위해 웹을 검색할 수 있습니다. 이는 최신 이벤트, 최근 데이터 또는 모델의 학습 기준 이후 변경될 수 있는 주제에 대한 질문에 답하는 데 유용합니다.

**지원 제공자:** Anthropic, OpenAI, Azure, Gemini, xAI, OpenRouter

```php
use Laravel\Ai\Providers\Tools\WebSearch;

public function tools(): iterable
{
    return [
        new WebSearch,
    ];
}
```



웹 검색 도구를 구성하여 검색 횟수를 제한하거나 특정 도메인으로 결과를 제한할 수 있습니다:

```php
(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```



사용자 위치를 기반으로 검색 결과를 정제하려면 `location` 방법을 사용하세요:

```php
(new WebSearch)->location(
    city: 'New York',
    region: 'NY',
    country: 'US'
);
```



<a name="web-fetch"></a>
#### 웹 가져오기

`WebFetch` 제공자 도구를 사용하면 에이전트가 웹 페이지의 내용을 가져오고 읽을 수 있습니다. 이는 에이전트가 특정 URL을 분석하거나 알려진 웹 페이지에서 자세한 정보를 가져와야 할 때 유용합니다.

**지원 제공자:** Anthropic, Gemini, OpenRouter

```php
use Laravel\Ai\Providers\Tools\WebFetch;

public function tools(): iterable
{
    return [
        new WebFetch,
    ];
}
```



웹 가져오기 도구를 구성하여 가져오기 횟수를 제한하거나 특정 도메인으로 제한할 수 있습니다:

```php
(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```



<a name="file-search"></a>
#### 파일 검색

`FileSearch` 제공 도구는 에이전트가 [벡터 저장소](#vector-stores)에 저장된 [파일](#files)을 검색할 수 있도록 합니다. 이를 통해 사용자가 업로드한 문서에서 관련 정보를 검색할 수 있어 검색 증강 생성(RAG)을 가능하게 합니다.

**지원되는 제공자:** OpenAI, Gemini, xAI

```php
use Laravel\Ai\Providers\Tools\FileSearch;

public function tools(): iterable
{
    return [
        new FileSearch(stores: ['store_id']),
    ];
}
```



여러 벡터 저장소에서 검색하기 위해 여러 벡터 저장소 ID를 제공할 수 있습니다:

```php
new FileSearch(stores: ['store_1', 'store_2']);
```



파일에 [메타데이터](#adding-files-to-stores)가 있는 경우 `where` 인수를 제공하여 검색 결과를 필터링할 수 있습니다. 단순한 동등 필터의 경우 배열을 전달하십시오:

```php
new FileSearch(stores: ['store_id'], where: [
    'author' => 'Taylor Otwell',
    'year' => 2026,
]);
```



더 복잡한 필터의 경우, `FileSearchQuery` 인스턴스를 받는 클로저를 전달할 수 있습니다:

```php
use Laravel\Ai\Providers\Tools\FileSearchQuery;

new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>
    $query->where('author', 'Taylor Otwell')
        ->whereNot('status', 'draft')
        ->whereIn('category', ['news', 'updates'])
);
```



<a name="code-execution"></a>
#### 코드 실행

`CodeExecution` 제공자 도구는 에이전트가 AI 제공자가 호스팅하는 샌드박스에서 코드를 실행할 수 있도록 합니다. 이는 계산 수행 및 데이터 분석에 유용합니다.

**지원되는 제공자:** Anthropic, OpenAI, Azure, Gemini, xAI

```php
use Laravel\Ai\Providers\Tools\CodeExecution;

public function tools(): iterable
{
    return [new CodeExecution];
}
```



OpenAI 또는 Azure를 사용할 때, 제공자 옵션을 통해 [저장된 파일](#files)을 샌드박스에서 사용할 수 있습니다:

```php
(new CodeExecution)->withProviderOptions([
    'container' => ['type' => 'auto', 'file_ids' => ['file_123']],
]);
```



<a name="sub-agents"></a>
### 하위 에이전트

에이전트는 다른 에이전트의 `tools` 메서드에서 반환될 수도 있습니다. 에이전트가 도구로 반환되면, 상위 에이전트는 특정 작업을 하위 에이전트에게 위임하고 원래 프롬프트에 답변할 때 하위 에이전트의 응답을 사용할 수 있습니다. 이는 범용 에이전트가 자체 지침, 도구, 모델 구성 또는 제공자 선호도를 가진 전문화된 에이전트에 접근해야 할 때 유용합니다.

예를 들어, 고객 지원 에이전트는 환불 자격 질문을 전문 환불 에이전트에게 위임할 수 있습니다:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasTools;
use Laravel\Ai\Promptable;

class CustomerSupportAgent implements Agent, HasTools
{
    use Promptable;

    /**
     * Get the instructions that the agent should follow.
     */
    public function instructions(): string
    {
        return 'You help customers with account, order, and billing questions. Delegate refund policy questions to the refunds specialist.';
    }

    /**
     * Get the tools available to the agent.
     *
     * @return Tool[]
     */
    public function tools(): iterable
    {
        return [
            new RefundsAgent,
        ];
    }
}
```



하위 에이전트가 상위 에이전트에 노출되는 방식을 사용자 정의하려면, 하위 에이전트에서 `CanActAsTool` 인터페이스를 구현하고 도구용 이름과 설명을 정의하세요:

```php
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Contracts\CanActAsTool;
use Laravel\Ai\Enums\Lab;

#[Provider(Lab::Anthropic)]
class RefundsAgent implements Agent, CanActAsTool, HasTools
{
    /**
     * Get the agent's tool name.
     */
    public function name(): string
    {
        return 'refunds_specialist';
    }

    /**
     * Get the agent's tool description.
     */
    public function description(): string
    {
        return 'Determine whether an order is eligible for a refund and explain the next step.';
    }

    // ...
}
```



서브 에이전트가 `CanActAsTool`를 구현하지 않으면, Laravel은 에이전트 클래스의 기본 이름을 도구 이름으로 사용하고, 부모 에이전트에게 명확하고 독립적인 작업 설명을 전달하도록 요청하는 일반적인 설명을 사용합니다. 각 서브 에이전트 호출은 독립적으로 실행되며, 부모 에이전트의 대화 기록을 받지 않습니다.

부모 에이전트가 [스트리밍](#streaming) 중일 때, 그 서브 에이전트들도 스트리밍됩니다. 부모 에이전트는 서브 에이전트가 지금까지 생성한 텍스트를 포함한 `ToolResult` 이벤트를 내보냅니다. 이 이벤트들은 예비로 표시되며, 도구 호출의 최종 결과가 뒤따르므로 이벤트를 수동으로 반복 처리할 때는 이를 건너뛸 수 있습니다:

```php
use Laravel\Ai\Streaming\Events\ToolResult;

foreach ($stream as $event) {
    if ($event instanceof ToolResult && $event->preliminary) {
        continue;
    }

    // ...
}
```



`text`, `usage`, `toolResults`와 같은 응답 값은 사전 이벤트를 무시합니다. [Vercel 프로토콜](#stream-protocols)은 이를 네이티브 스트리밍 도구 출력으로 렌더링하므로 `useChat`는 어떤 사용자 정의 코드 없이 진행 상황을 표시하며, AG-UI 프로토콜은 이를 활동 스냅샷으로 보고합니다. 완료된 응답의 텍스트, 추론, 인용 및 사용에는 하위 에이전트의 내용이 포함됩니다.

<a name="middleware"></a>
### 미들웨어

에이전트는 미들웨어를 지원하여 각 생성 단계를 공급자에게 보내기 전에 가로채고 수정할 수 있습니다. 미들웨어는 각 단계마다 한 번 호출되므로, 세 단계가 걸리는 실행은 세 번 호출됩니다. 미들웨어는 `make:agent-middleware` Artisan 명령을 사용하여 생성할 수 있습니다:

```shell
php artisan make:agent-middleware LogPrompts
```



생성된 미들웨어는 애플리케이션의 `app/Ai/Middleware` 디렉토리에 배치됩니다. 에이전트에 미들웨어를 추가하려면 `HasMiddleware` 인터페이스를 구현하고 미들웨어 클래스 배열을 반환하는 `middleware` 메서드를 정의하세요:

```php
<?php

namespace App\Ai\Agents;

use App\Ai\Middleware\LogPrompts;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasMiddleware;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasMiddleware
{
    use Promptable;

    // ...

    /**
     * Get the agent's middleware.
     */
    public function middleware(): array
    {
        return [
            new LogPrompts,
        ];
    }
}
```



각 미들웨어 클래스는 `PendingStep`와 `Closure`를 받는 `handle` 메서드를 정의해야 하며, 이 메서드는 단계를 다음 미들웨어로 전달합니다:

```php
<?php

namespace App\Ai\Middleware;

use Closure;
use Illuminate\Support\Facades\Log;
use Laravel\Ai\PendingStep;

class LogPrompts
{
    /**
     * Handle the pending generation step.
     */
    public function handle(PendingStep $step, Closure $next)
    {
        Log::info('Prompting agent', ['model' => $step->model]);

        return $next($step);
    }
}
```



곧 전송될 `provider`, `model`, `instructions`, `messages`, `tools` 외에도, 이 단계에서는 이미 완료된 단계들, 그들의 총 사용량, 그리고 실행 진행 상황을 보여줍니다:

```php
$step->steps;
$step->usage;

$step->number;
$step->isFirstStep();
$step->isFinalStep;
```



`withModel`, `withInstructions`, `withMessages`, `withTools`, `onlyTools`, `withoutTools`, `withToolChoice`, `withMaxTokens`, `withProviderOptions` 메서드는 각각 그 단계의 복사본을 반환합니다. 예를 들어, 에이전트가 도구를 사용한 후 비용이 많이 드는 도구를 제거할 수 있습니다:

```php
public function handle(PendingStep $step, Closure $next)
{
    if (! $step->isFirstStep()) {
        $step = $step->withoutTools('SearchDocumentation');
    }

    return $next($step);
}
```



또는 대화 중간 부분을 요약하여 컨텍스트 창 내에서 긴 도구 호출 루프를 유지할 수 있습니다:

```php
use App\Ai\Agents\Summarizer;
use Laravel\Ai\Messages\UserMessage;

public function handle(PendingStep $step, Closure $next)
{
    if (count($step->messages) > 40) {
        $summary = (new Summarizer)->prompt(
            collect(array_slice($step->messages, 1, -10))->map->content->implode("\n"),
        )->text;

        $step = $step->withMessages([
            $step->messages[0],
            new UserMessage("Summary of the conversation so far: {$summary}"),
            ...array_slice($step->messages, -10),
        ]);
    }

    return $next($step);
}
```



`withMessages` 메서드로 전달된 메시지는 현재 단계에 전송되는 내용만 변경합니다. 이후 단계와 저장된 대화는 전체 요약되지 않은 기록을 계속 사용합니다.

모델이 단계를 완료하고 도구 호출이 실행되기 전에 코드를 실행하려면 `then` 메서드를 사용할 수 있습니다. 이는 동기 응답과 스트리밍 응답 모두에 적용됩니다:

```php
use Laravel\Ai\Gateway\StepResponse;

public function handle(PendingStep $step, Closure $next)
{
    return $next($step)->then(function (StepResponse $response) {
        Log::info('Agent responded', ['text' => $response->text]);
    });
}
```



미들웨어는 캐시된 응답을 제공할 때와 같이 모델을 호출하지 않고 단계를 처리하기 위해 `$next`의 결과 또는 자체 `StepResponse`를 반환해야 합니다. 다른 값을 반환하면 `LogicException`가 발생합니다.

<a name="anonymous-agents"></a>
### 익명 에이전트

때때로 전용 에이전트 클래스를 만들지 않고 모델과 빠르게 상호작용하고 싶을 수 있습니다. `agent` 함수를 사용하여 임시 익명 에이전트를 만들 수 있습니다:

```php
use function Laravel\Ai\{agent};

$response = agent(
    instructions: 'You are an expert at software development.',
    messages: [],
    tools: [],
)->prompt('Tell me about Laravel');
```



익명 에이전트는 구조화된 출력도 생성할 수 있습니다:

```php
use Illuminate\Contracts\JsonSchema\JsonSchema;

use function Laravel\Ai\{agent};

$response = agent(
    schema: fn (JsonSchema $schema) => [
        'number' => $schema->integer()->required(),
    ],
)->prompt('Generate a random number less than 100');
```



<a name="agent-configuration"></a>
### 에이전트 구성

PHP 속성을 사용하여 에이전트의 텍스트 생성 옵션을 구성할 수 있습니다. 다음 속성을 사용할 수 있습니다:

- `MaxSteps`: 에이전트가 도구를 사용할 때 수행할 수 있는 최대 단계 수.
- `MaxTokens`: 모델이 생성할 수 있는 최대 토큰 수.
- `Model`: 에이전트가 사용해야 하는 모델.
- `Provider`: 에이전트에 사용할 AI 제공자(또는 장애 조치용 제공자).
- `Temperature`: 생성에 사용할 샘플링 온도(0.0에서 1.0).
- `Timeout`: 에이전트 요청에 대한 HTTP 타임아웃(초 단위, 기본값: 60).
- `TopP`: 생성에 사용할 핵심 샘플링 확률(0.0에서 1.0).
- `UseCheapestModel`: 비용 최적화를 위해 제공자의 가장 저렴한 텍스트 모델 사용.
- `UseSmartestModel`: 복잡한 작업을 위해 제공자의 가장 강력한 텍스트 모델 사용.

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Attributes\MaxSteps;
use Laravel\Ai\Attributes\MaxTokens;
use Laravel\Ai\Attributes\Model;
use Laravel\Ai\Attributes\Provider;
use Laravel\Ai\Attributes\Temperature;
use Laravel\Ai\Attributes\Timeout;
use Laravel\Ai\Attributes\TopP;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

#[Provider(Lab::Anthropic)]
#[Model('claude-sonnet-5')]
#[MaxSteps(10)]
#[MaxTokens(4096)]
#[Temperature(0.7)]
#[Timeout(120)]
#[TopP(0.9)]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```



`UseCheapestModel` 및 `UseSmartestModel` 속성은 모델 이름을 지정하지 않고도 주어진 제공업체에 대해 가장 비용 효율적이거나 가장 성능이 뛰어난 모델을 자동으로 선택할 수 있게 합니다. 이는 다양한 제공업체에 걸쳐 비용 또는 성능을 최적화하려는 경우에 유용합니다:

```php
use Laravel\Ai\Attributes\UseCheapestModel;
use Laravel\Ai\Attributes\UseSmartestModel;
use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Promptable;

#[UseCheapestModel]
class SimpleSummarizer implements Agent
{
    use Promptable;

    // Will use the cheapest model (e.g., Haiku)...
}

#[UseSmartestModel]
class ComplexReasoner implements Agent
{
    use Promptable;

    // Will use the most capable model (e.g., Opus)...
}
```



> [!NOTE]
> `UseCheapestModel`와 `UseSmartestModel`가 선택한 기본 모델은 공급자가 새 모델을 출시함에 따라 Laravel AI SDK의 릴리스 간에 변경될 수 있습니다. 모델을 전환하면 동작 변화, 더 이상 사용되지 않는 매개변수, 그리고 상당한 비용 차이가 발생할 수 있습니다. 안정적이고 예측 가능한 모델과 가격이 필요하다면 `Model` 속성을 사용하여 모델을 명시적으로 지정하십시오.

<a name="provider-options"></a>
### 공급자 옵션

에이전트가 공급자별 옵션(예: OpenAI 추론 노력 또는 페널티 설정)을 전달해야 하는 경우, `HasProviderOptions` 계약을 구현하고 `providerOptions` 메서드를 정의하십시오:

```php
<?php

namespace App\Ai\Agents;

use Laravel\Ai\Contracts\Agent;
use Laravel\Ai\Contracts\HasProviderOptions;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Promptable;

class SalesCoach implements Agent, HasProviderOptions
{
    use Promptable;

    // ...

    /**
     * Get provider-specific generation options.
     */
    public function providerOptions(Lab|string $provider): array
    {
        return match ($provider) {
            Lab::OpenAI => [
                'reasoning' => ['effort' => 'low'],
                'frequency_penalty' => 0.5,
                'presence_penalty' => 0.3,
            ],
            Lab::Anthropic => [
                'thinking' => ['budget_tokens' => 1024],
                'cache_control' => ['type' => 'ephemeral'],
            ],
            default => [],
        };
    }
}
```



`providerOptions` 메서드는 현재 사용 중인 공급자(`Lab` 열거형 또는 문자열)를 받으며, 공급자마다 다른 옵션을 반환할 수 있게 해줍니다. 이는 특히 [페일오버](#failover)를 사용할 때 유용하며, 각 백업 공급자는 자신의 구성 설정을 받을 수 있습니다.

위의 Anthropic 예제는 또한 `cache_control`를 통해 [프롬프트 캐싱](#prompt-caching)을 가능하게 합니다.

[이미지](#images), [오디오](#audio), [전사](#transcription), [임베딩](#embeddings), 그리고 [재순위](#reranking) 빌더 또한 공급자 옵션을 받을 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')
    ->withProviderOptions(['speed' => 1.25])
    ->generate();
```



배열 대신 클로저를 전달할 수도 있으며, 이 클로저는 현재 사용 중인 프로바이더를 받게 됩니다.

#### 사용자 정의 HTTP 헤더

애플리케이션의 `config/ai.php` 구성 파일 내 프로바이더에 대해 설정된 헤더는 해당 프로바이더가 수행하는 모든 요청과 함께 전송됩니다. AI 게이트웨이에서 사용하는 메타데이터처럼 요청별로 헤더를 보내려면, 이미지, 오디오, 전사, 임베딩, 재순위 빌더 및 [파일 업로드](#files)에서 사용할 수 있는 `withHeaders` 메서드를 사용할 수 있습니다.

```php
use Laravel\Ai\Embeddings;

$embeddings = Embeddings::for($chunks)
    ->withHeaders(['cf-aig-metadata' => json_encode(['team' => $team->id])])
    ->withProviderOptions(['dimensions' => 1024])
    ->generate();
```



헤더는 현재 사용 중인 제공자를 받는 클로저로도 제공될 수 있습니다. 헤더는 요청 본문에 포함되지 않으며 [임베딩 캐시 키](#caching-embeddings)에 영향을 주지 않습니다.

<a name="prompt-caching"></a>
### 프롬프트 캐싱

대부분의 제공자는 반복되는 프롬프트 접두사를 자동으로 캐시하고 캐시된 부분에 대해 할인된 요금을 청구합니다. OpenAI, Gemini, Groq, DeepSeek 및 xAI는 별도의 설정이 필요 없으며, 응답의 사용량을 통해 절감액을 확인할 수 있습니다:

```php
$response->usage->cacheReadInputTokens;
$response->usage->cacheWriteInputTokens;
```



이 두 개의 수치 모두 입력 토큰 총계의 하위 집합이며, 이에 대해서는 [사용 문서](#usage)에서 자세히 다룹니다.

`anthropic` 및 `bedrock` 제공자는 요청이 있을 때만 캐시합니다. `CacheInstructions` 및 `CacheToolDefinitions` 속성은 에이전트의 지침과 도구 정의 끝에 캐시 중단점을 설정하므로, 모든 대화가 다시 작성하지 않고 해당 접두사를 캐시에서 읽습니다:

```php
use Laravel\Ai\Attributes\CacheInstructions;
use Laravel\Ai\Attributes\CacheToolDefinitions;

#[CacheInstructions]
#[CacheToolDefinitions]
class SalesCoach implements Agent
{
    use Promptable;

    // ...
}
```



요청마다 현재 날짜를 포함하는 등 지침이 매번 변경되는 경우, `CacheToolDefinitions`만 사용하십시오. 요청마다 변경되는 접두사를 캐시하면 매번 새로운 캐시 항목이 생성되므로, 이를 캐시에 쓰는 비용을 지불하지만 재사용은 하지 않게 됩니다.

이러한 속성을 지원하지 않는 공급자는 이를 무시하므로, 에이전트는 [failover](#failover)를 사용하면서 안전하게 선언할 수 있습니다.

캐시된 접두사는 기본적으로 5분 동안 유지됩니다. TTL을 속성에 전달하면 Anthropic은 최대 한 시간까지 이를 유지할 수 있습니다.

```php
#[CacheInstructions('1h')]
#[CacheToolDefinitions('1h')]
```



Alternatively, Anthropic's automatic caching may be enabled via a top-level `cache_control` [provider option](#provider-options). This places a single breakpoint after the last block of the request, so the breakpoint advances as the conversation grows and each turn reads the previous turns from the cache. Both mechanisms may be combined.

> [!WARNING]
> Because providers build prompts in the order tools, instructions, and messages, caching instructions for an hour also requires caching tool definitions for an hour. Mixing the two throws an `InvalidArgumentException`.

<a name="human-tool-approval"></a>
## Human Tool Approval

> [!WARNING]
> Tool approval requires the paused turn's history to be available when the run is resumed. You should either use a `Conversational` agent, such as one using the `RemembersConversations` trait, or provide the history from your application's frontend using the [`withMessages` method](#conversation-context). Agents that do neither will throw an `ApprovalNotResumableException` when a tool pauses.

Tools that perform sensitive or irreversible actions may require human approval before they are executed. To make a tool approvable, implement the `Approvable` contract and use the `InteractsWithApprovals` trait. Approvable tools require approval by default:

```php
<?php

namespace App\Ai\Tools;

use Illuminate\Contracts\JsonSchema\JsonSchema;
use Illuminate\Support\Facades\Storage;
use Laravel\Ai\Concerns\InteractsWithApprovals;
use Laravel\Ai\Contracts\Approvable;
use Laravel\Ai\Contracts\Tool;
use Laravel\Ai\Tools\Request;
use Stringable;

class DeleteFile implements Approvable, Tool
{
    use InteractsWithApprovals;

    /**
     * Get the description of the tool's purpose.
     */
    public function description(): Stringable|string
    {
        return 'Delete a file from storage.';
    }

    /**
     * Execute the tool.
     */
    public function handle(Request $request): Stringable|string
    {
        Storage::delete($request['path']);

        return "Deleted [{$request['path']}].";
    }

    /**
     * Get the tool's schema definition.
     */
    public function schema(JsonSchema $schema): array
    {
        return [
            'path' => $schema->string()->required(),
        ];
    }
}
```



도구 호출의 인수를 기반으로 승인이 필요한지 여부를 결정하려면 도구에 `needsApproval` 메서드를 정의하십시오. 이 메서드는 불리언 값 또는 승인 요청의 이유를 포함하는 `Approval` 인스턴스를 반환할 수 있습니다:

```php
use Laravel\Ai\Approvals\Approval;

/**
 * Determine whether the tool needs approval for the given request.
 */
protected function needsApproval(Request $request): Approval|bool
{
    return str_starts_with($request['path'], 'temporary/')
        ? false
        : Approval::required('This will permanently delete a file.');
}
```



에이전트의 `tools` 메서드에서 도구를 반납할 때 도구의 승인 요구 사항을 무시할 수 있습니다:

```php
public function tools(): iterable
{
    return [
        (new SendNotification)->withoutApproval(),
        (new DeleteFile)->requireApproval('Deletion review required.'),
    ];
}
```



승인 가능한 도구가 호출되면, 에이전트는 실행하기 전에 잠시 멈춥니다. 각 도구 호출의 ID, 도구 이름, 인수 및 승인 사유가 포함된 응답의 보류 중인 승인을 확인할 수 있습니다:

```php
$response = (new FileAssistant)
    ->forUser($user)
    ->prompt('Delete the old invoice.');

if ($response->hasPendingApprovals()) {
    foreach ($response->pendingApprovals as $approval) {
        // $approval->id
        // $approval->tool
        // $approval->arguments
        // $approval->reason
    }
}
```



에이전트를 재개하려면 대화를 계속하고 각 보류 중인 도구 호출에 대한 결정을 포함하는 `Decisions` 인스턴스를 제공하십시오. 결정은 호출을 승인하거나, 거부하거나, 실행 전에 인수를 편집할 수 있습니다:

```php
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt(Decisions::from([
        'call_abc' => Decision::approve(),
        'call_ghi' => Decision::reject('The invoice must be retained.'),
    ]));
```



> [!IMPORTANT]
> 일시 중지된 턴은 이를 일시 중지한 참가자가 아니라 해당 대화와 보류 중인 도구 호출에 의해 매칭됩니다. 따라서 애플리케이션은 [전체 승인 흐름](#complete-approval-flow)에서 보여준 것처럼 대화를 재개하기 전에 접근을 승인하거나, 대화 저장소의 `conversationBelongsTo` 메서드를 사용하여 접근을 확인해야 합니다.

불리언 값 `true`와 `false`는 승인과 거부를 축약하여 나타내는 데 사용할 수 있습니다. 모든 보류 중인 도구 호출은 반드시 결정이 내려져야 합니다. 알 수 없거나 누락되었거나 이전에 처리된 도구 호출 ID는 `ApprovalMismatchException` 예외를 발생시킬 수 있습니다. 명시적인 결정이 없는 호출의 기본값은 `approveRemaining` 또는 `rejectRemaining` 메서드를 사용하여 제공할 수 있습니다:

```php
$decisions = Decisions::from([
    'call_abc' => true,
])->rejectRemaining('Not approved.');

$response = (new FileAssistant)
    ->continue($conversationId, as: $user)
    ->prompt($decisions);
```



`Decision::reject('Not approved.')`와 같은 결과가 있는 거부는 모델에 반환되어 모델이 계속 응답할 수 있도록 합니다. 결과가 없는 거부는 거부를 기록한 후 생성 루프를 중단합니다.

도구 승인은 `prompt`, `stream`, `queue`, `broadcast`, `broadcastNow` 및 `broadcastOnQueue` 메서드에서 지원됩니다.

스트리밍 및 방송 중에는 중지가 `tool_approval_request` 이벤트로 표시됩니다. [Vercel AI SDK 스트림 프로토콜](#stream-protocols)을 사용할 때, 승인 요청 및 결과는 프로토콜의 기본 도구 승인 부분을 사용하여 전송되며, 에이전트 사용자 상호작용 프로토콜은 이를 인터럽트로 보고합니다.

두 프로토콜 중 하나를 사용하는 클라이언트는 대화의 나머지 부분과 함께 결정을 게시하므로 [채팅 요청](#frontend-integration)을 에이전트에 직접 전달할 수 있습니다:

```php
$chat = Vercel::chat($request);

return (new FileAssistant)
    ->continue($conversationId, as: $request->user())
    ->stream($chat)
    ->usingProtocol($chat->protocol());
```



일시 중지된 턴이 재개될 때, 재개된 단계는 해당 턴에 병합되며, 따라서 각 턴은 단일 어시스턴트 메시지로 저장됩니다. 응답의 `assistantMessageId`에는 일시 중지된 메시지의 ID가 포함되며, 해당 메시지의 사용량에는 일시 중지와 재개가 모두 포함됩니다.

대기 중인 에이전트의 경우, 생성된 응답은 `then` 콜백으로 전달되며, Laravel은 또한 `ToolApprovalRequested` 이벤트를 디스패치합니다.

Laravel은 모델에게 계속 진행하도록 요청하기 전에 승인된 도구의 결과를 저장합니다. 이후 생성이 실패하면, 승인은 이미 해결된 상태입니다. 동일한 승인 결정을 다시 제출하지 말고 일반 텍스트 프롬프트로 대화를 계속하세요.

<a name="complete-approval-flow"></a>
### 완전한 승인 흐름

다음 라우트는 새로운 텍스트 프롬프트 또는 채팅 화면에서의 승인 결정을 받아들이는 완전한 승인 흐름을 보여줍니다. 이 예시는 애플리케이션의 `User` 모델이 `HasConversations` 트레이트를 사용한다고 가정합니다:

```php
use App\Ai\Agents\FileAssistant;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\Facades\Route;
use Illuminate\Validation\Rule;
use Laravel\Ai\Approvals\Decision;
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Models\Conversation;

Route::post('/chat/{conversation}', function (Request $request, Conversation $conversation) {
    Gate::authorize('view', $conversation);

    $validated = $request->validate([
        'message' => ['nullable', 'string', 'required_without:decisions', 'prohibits:decisions'],
        'decisions' => ['nullable', 'array', 'required_without:message', 'prohibits:message'],
        'decisions.*.action' => ['required_with:decisions', Rule::in(['approve', 'reject'])],
        'decisions.*.result' => ['nullable', 'string'],
    ]);

    $prompt = isset($validated['decisions'])
        ? Decisions::from(collect($validated['decisions'])->map(
            fn (array $decision) => match ($decision['action']) {
                'approve' => Decision::approve(),
                'reject' => Decision::reject($decision['result'] ?? null),
            }
        )->all())
        : $validated['message'];

    $response = (new FileAssistant)
        ->continue($conversation->id, as: $request->user())
        ->prompt($prompt);

    return [
        'conversation_id' => $response->conversationId,
        'status' => $response->hasPendingApprovals() ? 'awaiting_approval' : 'complete',
        'message' => $response->text,
        'approvals' => $response->pendingApprovals,
    ];
})->middleware('auth');
```



응답 상태가 `awaiting_approval`일 때, 채팅 화면은 대기 중인 승인 항목을 렌더링하고 각 결정의 키로 툴 호출 ID를 사용하여 사용자의 선택을 동일한 엔드포인트로 제출해야 합니다. 그렇지 않으면 화면은 일반 `message` 값을 제출할 수 있습니다:

```json
{
    "decisions": {
        "call_abc": {
            "action": "approve"
        },
        "call_def": {
            "action": "reject",
            "result": "The invoice must be retained."
        }
    }
}
```



<a name="images"></a>
## 이미지

`Laravel\Ai\Image` 클래스는 `openai`, `gemini` 또는 `xai` 공급자를 사용하여 이미지를 생성하는 데 사용될 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')->generate();

$rawContent = (string) $image;
```



`square`, `portrait`, `landscape` 방법은 이미지의 종횡비를 제어하는 데 사용할 수 있으며, `quality` 방법은 최종 이미지 품질(`high`, `medium`, `low`)에 대해 모델을 안내하는 데 사용할 수 있습니다. `timeout` 방법은 초 단위로 HTTP 타임아웃을 지정하는 데 사용할 수 있습니다:

```php
use Laravel\Ai\Image;

$image = Image::of('A donut sitting on the kitchen counter')
    ->quality('high')
    ->landscape()
    ->timeout(120)
    ->generate();
```



`attachments` 방법을 사용하여 참고 이미지를 첨부할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Image;

$image = Image::of('Update this photo of me to be in the style of an impressionist painting.')
    ->attachments([
        Files\Image::fromStorage('photo.jpg'),
        // Files\Image::fromPath('/home/laravel/photo.jpg'),
        // Files\Image::fromUrl('https://example.com/photo.jpg'),
        // $request->file('photo'),
    ])
    ->landscape()
    ->generate();
```



일부 제공자는 하나의 요청에서 여러 이미지를 생성할 수 있습니다. OpenAI, Azure 및 xAI는 `n` [제공자 옵션](#provider-options)을 허용하며, 응답에는 반환된 모든 이미지가 포함됩니다:

```php
$response = Image::of('A donut sitting on the kitchen counter')
    ->withProviderOptions(['n' => 4])
    ->generate();

count($response);           // 4
$response->images;          // A collection of generated images...
$response->firstImage();    // The first generated image...
```



생성된 이미지는 애플리케이션의 `config/filesystems.php` 구성 파일에 설정된 기본 디스크에 쉽게 저장될 수 있습니다:

```php
$image = Image::of('A donut sitting on the kitchen counter');

$path = $image->store();
$path = $image->storeAs('image.jpg');
$path = $image->storePublicly();
$path = $image->storePubliclyAs('image.jpg');
```



이미지 생성도 대기열에 추가될 수 있습니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Responses\ImageResponse;

Image::of('A donut sitting on the kitchen counter')
    ->portrait()
    ->queue()
    ->then(function (ImageResponse $image) {
        $path = $image->store();

        // ...
    });
```



<a name="audio"></a>
## 오디오

`Laravel\Ai\Audio` 클래스는 주어진 텍스트로부터 오디오를 생성하는 데 사용될 수 있습니다:

```php
use Laravel\Ai\Audio;

$audio = Audio::of('I love coding with Laravel.')->generate();

$rawContent = (string) $audio;
```



Laravel의 `Stringable` 클래스를 통해 사용할 수 있는 `toAudio` 방법을 사용하여 문자열에서 오디오를 생성할 수도 있습니다:

```php
use Illuminate\Support\Str;

$audio = Str::of('I love coding with Laravel.')->toAudio();
```



생성된 오디오의 음성을 결정하기 위해 `male`, `female`, 및 `voice` 방법을 사용할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->generate();

$audio = Audio::of('I love coding with Laravel.')
    ->voice('voice-id-or-name')
    ->generate();
```



마찬가지로, `instructions` 방법은 생성된 오디오가 어떻게 들려야 하는지 모델에 동적으로 가르치는 데 사용할 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')
    ->female()
    ->instructions('Said like a pirate')
    ->generate();
```



생성된 오디오는 애플리케이션의 `config/filesystems.php` 구성 파일에 설정된 기본 디스크에 쉽게 저장될 수 있습니다:

```php
$audio = Audio::of('I love coding with Laravel.')->generate();

$path = $audio->store();
$path = $audio->storeAs('audio.mp3');
$path = $audio->storePublicly();
$path = $audio->storePubliclyAs('audio.mp3');
```



오디오 생성도 대기열에 추가될 수 있습니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Responses\AudioResponse;

Audio::of('I love coding with Laravel.')
    ->queue()
    ->then(function (AudioResponse $audio) {
        $path = $audio->store();

        // ...
    });
```



<a name="transcription"></a>
## 전사

`Laravel\Ai\Transcription` 클래스는 주어진 오디오의 전사를 생성하는 데 사용할 수 있습니다:

```php
use Laravel\Ai\Transcription;

$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();
$transcript = Transcription::fromStorage('audio.mp3')->generate();
$transcript = Transcription::fromUpload($request->file('audio'))->generate();

return (string) $transcript;
```



`diarize` 방법은 원시 텍스트 기록 외에 화자 분리 기록도 포함된 응답을 원할 경우 사용할 수 있으며, 이를 통해 화자별로 구분된 기록에 접근할 수 있습니다:

```php
$transcript = Transcription::fromStorage('audio.mp3')
    ->diarize()
    ->generate();
```



전사 생성도 대기열에 추가될 수 있습니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Responses\TranscriptionResponse;

Transcription::fromStorage('audio.mp3')
    ->queue()
    ->then(function (TranscriptionResponse $transcript) {
        // ...
    });
```



<a name="text-summarization"></a>
## 텍스트 요약

Laravel의 `Stringable` 클래스를 통해 사용할 수 있는 `summarize` 방법을 사용하여 텍스트를 요약할 수 있습니다. 기본적으로 요약은 세 문장을 넘지 않으며 구성된 제공자의 가장 저렴한 텍스트 모델을 사용하여 생성됩니다:

```php
use Illuminate\Support\Str;

$summary = Str::of($article)->summarize();
```



요약을 생성하는 데 사용되는 최대 문장 수, 제공자, 모델 및 시간 초과를 지정할 수 있습니다. `Str` 클래스는 또한 해당 메서드의 정적 버전을 제공합니다:

```php
use Laravel\Ai\Enums\Lab;

$summary = Str::of($article)->summarize(
    sentences: 4,
    provider: Lab::Anthropic,
    model: 'claude-sonnet-5',
    timeout: 30,
);

$summary = Str::summarize($article, sentences: 4);
```



<a name="embeddings"></a>
## 임베딩

Laravel의 `Stringable` 클래스를 통해 사용할 수 있는 새로운 `toEmbeddings` 방법을 사용하여 주어진 문자열의 벡터 임베딩을 쉽게 생성할 수 있습니다:

```php
use Illuminate\Support\Str;

$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```



또는 `Embeddings` 클래스를 사용하여 여러 입력에 대한 임베딩을 한 번에 생성할 수 있습니다:

```php
use Laravel\Ai\Embeddings;

$response = Embeddings::for([
    'Napa Valley has great wine.',
    'Laravel is a PHP framework.',
])->generate();

$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```



임베딩의 차원과 제공자를 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->dimensions(1536)
    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```



<a name="multimodal-embeddings"></a>
### 멀티모달 임베딩

문자열 외에도, `Embeddings::for` 방법은 이미지, 오디오, 문서, 비디오 입력을 허용하여 비텍스트 콘텐츠에 대한 임베딩을 생성할 수 있습니다. Gemini는 이미지, 오디오, 문서, 비디오 임베딩을 지원하며, VoyageAI는 이미지와 비디오 임베딩을 지원합니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

$response = Embeddings::for([
    'A vineyard at sunset.',
    Image::fromStorage('vineyard.jpg'),
    Video::fromPath('/home/laravel/tour.mp4'),
])->generate(Lab::Gemini);
```



멀티모달 입력은 첨부 파일에 사용되는 동일한 [파일 클래스](#attachments)를 사용합니다. 이러한 파일은 로컬 경로, 파일 시스템 디스크, 원격 URL 또는 Base64로 인코딩된 콘텐츠에서 생성될 수 있습니다. 이미지, 문서 및 비디오는 업로드된 파일에서 생성할 수 있으며, 문서는 원시 문자열 콘텐츠에서 생성할 수도 있습니다:

```php
use Laravel\Ai\Files\Audio;
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;
use Laravel\Ai\Files\Video;

Image::fromPath('/home/laravel/photo.jpg');
Image::fromStorage('photo.jpg');
Image::fromUpload($request->file('photo'));

Audio::fromPath('/home/laravel/clip.mp3');
Audio::fromStorage('clip.mp3');
Audio::fromUpload($request->file('clip.mp3'));

Video::fromPath('/home/laravel/video.mp4');
Video::fromStorage('video.mp4');
Video::fromUpload($request->file('video'));

Document::fromUrl('https://example.com/report.pdf');
Document::fromString('Laravel is a PHP framework.', 'text/plain');
Document::fromUpload($request->file('report'));
```



> [!NOTE]
> VoyageAI는 단일 요청에서 원격 URL 미디어와 Base64로 인코딩된 미디어를 혼합하는 것을 허용하지 않습니다. 로컬, 저장된 파일, 업로드된 파일은 Base64로 인코딩된 콘텐츠로 전송되며, 텍스트 입력은 어느 미디어 소스와도 결합될 수 있습니다. 사용 가능한 멀티모달 모델과 입력을 확인하려면 제공자의 문서를 참조하세요.

<a name="querying-embeddings"></a>
### 임베딩 조회

임베딩을 생성한 후, 일반적으로 나중에 조회할 수 있도록 데이터베이스의 `vector` 컬럼에 저장합니다. Laravel은 `pgvector` 확장을 통해 PostgreSQL 및 MariaDB에서 벡터 컬럼을 네이티브로 지원합니다. 시작하려면 마이그레이션에서 `vector` 컬럼을 정의하고 차원 수를 지정하세요:

```php
Schema::ensureVectorExtensionExists();

Schema::create('documents', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->vector('embedding', dimensions: 1536);
    $table->timestamps();
});
```



유사도 검색 속도를 높이기 위해 벡터 인덱스를 추가할 수도 있습니다. 벡터 열에서 `index`를 호출하면, Laravel은 자동으로 코사인 거리를 사용하는 HNSW 인덱스를 생성합니다:

```php
$table->vector('embedding', dimensions: 1536)->index();
```



당신의 Eloquent 모델에서, `AsVector` 캐스트를 사용하여 벡터 컬럼을 캐스트해야 합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsVector;

protected function casts(): array
{
    return [
        'embedding' => AsVector::class,
    ];
}
```



유사한 레코드를 조회하려면 `whereVectorSimilarTo` 메서드를 사용하십시오. 이 메서드는 최소 코사인 유사도(`1.0`가 동일한 경우 `0.0`와 `1.0` 사이)로 결과를 필터링하고, 유사도 순으로 결과를 정렬합니다:

```php
use App\Models\Document;

$documents = Document::query()
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```



`$queryEmbedding`는 부동 소수점 배열이거나 일반 문자열일 수 있습니다. 문자열이 주어지면 Laravel이 자동으로 해당 문자열에 대한 임베딩을 생성합니다:

```php
$documents = Document::query()
    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')
    ->limit(10)
    ->get();
```



더 많은 제어가 필요하다면, `whereVectorDistanceLessThan`, `selectVectorDistance`, `orderByVectorDistance` 메서드를 독립적으로 사용할 수 있습니다:

```php
$documents = Document::query()
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```



에이전트에게 도구로서 유사도 검색을 수행할 수 있는 기능을 부여하고 싶다면, [유사도 검색](#similarity-search) 도구 문서를 확인하세요.

> [!NOTE]
> 백터 쿼리는 현재 `pgvector` 확장을 사용하는 PostgreSQL 연결과 MariaDB 11.7 이상에서 지원됩니다.

<a name="caching-embeddings"></a>
### 임베딩 캐싱

임베딩 생성을 캐시하여 동일한 입력에 대한 불필요한 API 호출을 피할 수 있습니다. 캐싱을 활성화하려면 `ai.caching.embeddings.cache` 구성 옵션을 `true`로 설정하세요:

```php
'caching' => [
    'embeddings' => [
        'cache' => true,
        'store' => env('CACHE_STORE', 'database'),
        'individually' => true,
        // ...
    ],
],
```



캐싱이 활성화되면 임베딩이 30일 동안 캐시됩니다. 캐시 키는 제공자, 모델, 차원 및 입력 콘텐츠를 기준으로 하여 동일한 요청은 캐시된 결과를 반환하고, 다른 구성은 새로운 임베딩을 생성하도록 보장합니다.

기본적으로 각 입력의 임베딩은 자체 키로 캐시되므로, 입력 집합이나 순서가 변경되더라도 이전에 본 입력에 대한 나중 요청은 캐시를 사용할 수 있습니다. 대신 전체 입력 집합을 하나의 키 아래에 캐시하려면 `ai.caching.embeddings.individually` 설정 옵션을 `false`로 설정하십시오.

글로벌 캐싱이 비활성화되어 있어도 `cache` 메서드를 사용하여 특정 요청에 대해 캐싱을 활성화할 수도 있습니다.

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache()
    ->generate();
```



초 단위로 사용자 지정 캐시 지속 시간을 지정할 수 있습니다:

```php
$response = Embeddings::for(['Napa Valley has great wine.'])
    ->cache(seconds: 3600) // Cache for 1 hour
    ->generate();
```



`toEmbeddings` Stringable 메서드는 `cache` 인수도 허용합니다:

```php
// Cache with default duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

// Cache for a specific duration...
$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```



<a name="reranking"></a>
## 재정렬

재정렬은 주어진 쿼리에 대한 관련성을 기준으로 문서 목록의 순서를 다시 지정할 수 있게 합니다. 이는 의미적 이해를 사용하여 검색 결과를 개선하는 데 유용합니다.

`Laravel\Ai\Reranking` 클래스는 문서를 재정렬하는 데 사용할 수 있습니다:

```php
use Laravel\Ai\Reranking;

$response = Reranking::of([
    'Django is a Python web framework.',
    'Laravel is a PHP web application framework.',
    'React is a JavaScript library for building user interfaces.',
])->rerank('PHP frameworks');

// Access the top result...
$response->first()->document; // "Laravel is a PHP web application framework."
$response->first()->score;    // 0.95
$response->first()->index;    // 1 (original position)
```



`limit` 메서드는 반환되는 결과 수를 제한하는 데 사용될 수 있으며, `timeout` 메서드는 초 단위로 HTTP 타임아웃을 지정하는 데 사용될 수 있으며, 기본값은 30입니다:

```php
$response = Reranking::of($documents)
    ->limit(5)
    ->timeout(60)
    ->rerank('search query');
```



<a name="reranking-collections"></a>
### 컬렉션 재정렬

편의를 위해, Laravel 컬렉션은 `rerank` 매크로를 사용하여 재정렬할 수 있습니다. 첫 번째 인수는 재정렬에 사용할 필드를 지정하고, 두 번째 인수는 쿼리입니다:

```php
// Rerank by a single field...
$posts = Post::all()
    ->rerank('body', 'Laravel tutorials');

// Rerank by multiple fields (sent as JSON)...
$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

// Rerank using a closure to build the document...
$reranked = $posts->rerank(
    fn ($post) => $post->title.': '.$post->body,
    'Laravel tutorials'
);
```



결과 수를 제한하고 공급자를 지정할 수도 있습니다:

```php
$reranked = $posts->rerank(
    by: 'content',
    query: 'Laravel tutorials',
    limit: 10,
    provider: Lab::Cohere,
    timeout: 60,
);
```



<a name="classification"></a>
## 분류

> [!WARNING]
> 분류는 현재 실험적이며, AI SDK의 향후 소규모 릴리즈에서 API가 변경될 수 있습니다.

분류를 사용하면 주어진 문자열이나 데이터 배열에 대해 고정된 질문 세트를 묻고, 자유 형식 텍스트 대신 확률을 기반으로 한 유형화된 답변을 각 질문에 대해 받을 수 있습니다. 이는 답변을 임계값과 비교하거나 테스트에서 이에 대한 주장을 해야 하는 라우팅, 검열 및 점수 매기기에 유용합니다.

`Laravel\Ai\Classification` 클래스는 콘텐츠를 분류하는 데 사용할 수 있습니다. 각 질문에는 키가 부여되며, 해당 키를 사용하여 응답에서 해당 답변을 가져올 수 있습니다:

```php
use Laravel\Ai\Classification;
use Laravel\Ai\Classification\Boolean;
use Laravel\Ai\Classification\Choice;
use Laravel\Ai\Classification\Score;

$result = Classification::of($supportRequest)
    ->questions([
        'urgent' => new Boolean('Does this request need an immediate response?', [
            'true' => 'Explicitly time-sensitive',
            'false' => 'No urgency expressed',
        ]),
        'department' => new Choice('Which team should handle this request?', [
            'billing' => 'Payments, invoices, and refunds',
            'technical' => 'Bugs, outages, and integrations',
            'sales' => 'Pricing, plans, and upgrades',
        ]),
        'frustration' => new Score('How frustrated is the customer?', [
            'Calm',
            'Frustrated',
            'Very angry',
        ]),
    ])
    ->classify();
```



`Boolean` 질문은 답이 '참'일 확률을 반환합니다. `isTrue` 방법은 해당 확률이 기본값이 `0.5`인 주어진 임계값을 충족하는지 여부를 결정하는 데 사용할 수 있습니다:

```php
$result['urgent']->probability;             // 0.94
$result['urgent']->isTrue(threshold: 0.8);  // true
```



`Choice` 질문은 각 옵션과 각 옵션의 확률 중 하나를 반환합니다. `confidence` 속성은 공급자가 전체 확률 세트에 대해 얼마나 확신하는지를 나타내며, 측정할 수 없는 경우 `null`가 됩니다:

```php
$result['department']->choice;                      // 'technical'
$result['department']->probabilityOf('technical');  // 0.87
$result['department']->probabilities;               // ['billing' => 0.08, 'technical' => 0.87, 'sales' => 0.05]
$result['department']->confidence;                  // 0.82
```



`Score` 질문은 제공된 순서 수준에서 위치를 반환합니다. `score` 속성은 확률 가중치가 적용되며 두 수준 사이에 위치할 수 있는 반면, `level` 및 `label` 방법은 가장 가능성이 높은 수준을 설명합니다:

```php
$result['frustration']->score;          // 1.24, the probability-weighted level
$result['frustration']->level();        // 1, the most probable level
$result['frustration']->label();        // 'Frustrated'
$result['frustration']->normalized();   // 0.62, the score as a fraction of the highest level
$result['frustration']->probabilities;  // [0.12, 0.52, 0.36]
```



`Boolean` 질문에 주어진 기준, `Choice` 질문에 주어진 옵션 설명, `Score` 질문에 주어진 수준은 하나의 문장으로 충분하지 않을 경우 각각 배열일 수 있습니다. `Choice` 질문에는 최소 두 개의 옵션이 필요하며, `Score` 질문에는 최소 두 개의 수준이 필요합니다.

응답은 반복되거나, 계산되거나, 배열로 접근될 수 있습니다. 또한, `answer` 메서드는 단일 답변을 가져오는 데 사용될 수 있으며, `collect` 메서드는 모든 답변을 [collection](/docs/{{version}}/collections)으로 반환합니다:

```php
$result->answer('urgent');
$result->collect();

$result->usage;
$result->meta->provider;
```



단일 예 또는 아니오 결정의 경우, 전체 응답 대신 불리언을 반환하는 Laravel의 `Stringable` 클래스를 통해 사용할 수 있는 `decide` 방법을 사용할 수 있습니다. '예'와 '아니오'가 의미하는 바를 설명하고, 답변이 도달해야 하는 확률을 지정할 수 있으며, 기본값은 `0.5`입니다:

```php
use Illuminate\Support\Str;

if (Str::of($message)->decide('Is this spam?')) {
    // ...
}

$spam = Str::of($message)->decide('Is this spam?', criteria: [
    'true' => 'Unsolicited bulk mail.',
    'false' => 'A genuine message from a customer.',
], threshold: 0.9);
```



기본적으로 분류는 [TypeSafe](https://typesafe.ai)에 의해 수행됩니다. 애플리케이션의 `config/ai.php` 구성 파일 내 `default_for_classification` 옵션을 사용하여 이를 변경할 수 있습니다. 분류할 때 공급자와 모델을 지정할 수도 있습니다:

```php
use Laravel\Ai\Enums\Lab;

$result = Classification::of($supportRequest)
    ->questions($questions)
    ->classify(Lab::OpenRouter, 'model-name');
```



`timeout` 메서드는 기본값이 30초인 HTTP 타임아웃을 초 단위로 지정하는 데 사용할 수 있습니다. [제공자 옵션](#provider-options) 및 사용자 정의 헤더도 제공할 수 있습니다:

```php
$result = Classification::of($supportRequest)
    ->questions($questions)
    ->timeout(60)
    ->withProviderOptions(['temperature' => 0])
    ->classify();
```



<a name="files"></a>
## 파일

`Laravel\Ai\Files` 클래스 또는 개별 파일 클래스는 나중에 대화에서 사용하기 위해 AI 제공업체와 파일을 저장하는 데 사용할 수 있습니다. 이는 큰 문서나 여러 번 참조해야 하는 파일을 다시 업로드하지 않고 사용하려는 경우에 유용합니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Files\Image;

// Store a file from a local path...
$response = Document::fromPath('/home/laravel/document.pdf')->put();
$response = Image::fromPath('/home/laravel/photo.jpg')->put();

// Store a file that is stored on a filesystem disk...
$response = Document::fromStorage('document.pdf', disk: 'local')->put();
$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

// Store a file that is stored on a remote URL...
$response = Document::fromUrl('https://example.com/document.pdf')->put();
$response = Image::fromUrl('https://example.com/photo.jpg')->put();

return $response->id;
```



원시 콘텐츠나 업로드된 파일도 저장할 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

// Store raw content...
$stored = Document::fromString('Hello, World!', 'text/plain')->put();

// Store an uploaded file...
$stored = Document::fromUpload($request->file('document'))->put();
```



파일이 저장되면, 파일을 다시 업로드하지 않고도 에이전트를 통해 텍스트를 생성할 때 해당 파일을 참조할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Files;

$response = (new SalesCoach)->prompt(
    'Analyze the attached sales transcript...',
    attachments: [
        Files\Document::fromId('file-id') // Attach a stored document...
    ]
);
```



이전에 저장된 파일을 검색하려면 파일 인스턴스에서 `get` 메서드를 사용하십시오:

```php
use Laravel\Ai\Files\Document;

$file = Document::fromId('file-id')->get();

$file->id;
$file->mimeType();
```



프로바이더에서 파일을 삭제하려면 `delete` 방법을 사용하세요:

```php
Document::fromId('file-id')->delete();
```



기본적으로 `Files` 클래스는 애플리케이션의 `config/ai.php` 구성 파일에 설정된 기본 AI 공급자를 사용합니다. 대부분의 작업에서는 `provider` 인수를 사용하여 다른 공급자를 지정할 수 있습니다:

```php
$response = Document::fromPath(
    '/home/laravel/document.pdf'
)->put(provider: Lab::Anthropic);
```



`withProviderOptions` 방법을 사용하여 공급자별 업로드 옵션을 전달할 수 있습니다. 예를 들어, OpenAI의 파일 `purpose`를 설정할 수 있습니다:

```php
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/knowledge.txt')
    ->withProviderOptions(['purpose' => 'assistants'])
    ->put();
```



공급자별로 옵션을 범위 지정하려면, 현재 공급자를 받는 클로저를 전달하세요:

```php
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Files\Document;

$response = Document::fromPath('/home/laravel/training.jsonl')
    ->withProviderOptions(fn (Lab|string $provider) => match ($provider) {
        Lab::OpenAI => ['purpose' => 'fine-tune'],
        default => [],
    })
    ->put();
```



<a name="using-stored-files-in-conversations"></a>
### 대화에서 저장된 파일 사용하기

파일이 제공자에게 저장되면, `Document` 또는 `Image` 클래스에서 `fromId` 메서드를 사용하여 에이전트 대화에서 참조할 수 있습니다:

```php
use App\Ai\Agents\DocumentAnalyzer;
use Laravel\Ai\Files;
use Laravel\Ai\Files\Document;

$stored = Document::fromPath('/path/to/report.pdf')->put();

$response = (new DocumentAnalyzer)->prompt(
    'Summarize this document.',
    attachments: [
        Document::fromId($stored->id),
    ],
);
```



마찬가지로, 저장된 이미지는 `Image` 클래스를 사용하여 참조될 수 있습니다:

```php
use Laravel\Ai\Files;
use Laravel\Ai\Files\Image;

$stored = Image::fromPath('/path/to/photo.jpg')->put();

$response = (new ImageAnalyzer)->prompt(
    'What is in this image?',
    attachments: [
        Image::fromId($stored->id),
    ],
);
```



<a name="vector-stores"></a>
## 벡터 저장소

벡터 저장소를 사용하면 검색 가능한 파일 컬렉션을 만들어 검색 강화 생성(RAG)에 사용할 수 있습니다. `Laravel\Ai\Stores` 클래스는 벡터 저장소를 생성, 검색 및 삭제하는 메서드를 제공합니다:

```php
use Laravel\Ai\Stores;

// Create a new vector store...
$store = Stores::create('Knowledge Base');

// Create a store with additional options...
$store = Stores::create(
    name: 'Knowledge Base',
    description: 'Documentation and reference materials.',
    expiresWhenIdleFor: days(30),
);

return $store->id;
```



기존 벡터 저장소를 ID로 검색하려면 `get` 방법을 사용하세요:

```php
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

$store->id;
$store->name;
$store->fileCounts;
$store->ready;
```



벡터 스토어를 삭제하려면 `Stores` 클래스나 스토어 인스턴스에서 `delete` 메서드를 사용하세요:

```php
use Laravel\Ai\Stores;

// Delete by ID...
Stores::delete('store_id');

// Or delete via a store instance...
$store = Stores::get('store_id');

$store->delete();
```



<a name="adding-files-to-stores"></a>
### 스토어에 파일 추가하기

벡터 스토어를 갖게 되면, `add` 메서드를 사용하여 [파일](#files)을 추가할 수 있습니다. 스토어에 추가된 파일은 [파일 검색 제공 도구](#file-search)를 사용하여 의미 기반 검색을 위해 자동으로 인덱싱됩니다:

```php
use Laravel\Ai\Files\Document;
use Laravel\Ai\Stores;

$store = Stores::get('store_id');

// Add a file that has already been stored with the provider...
$document = $store->add('file_id');
$document = $store->add(Document::fromId('file_id'));

// Or, store and add a file in one step...
$document = $store->add(Document::fromPath('/path/to/document.pdf'));
$document = $store->add(Document::fromStorage('manual.pdf'));
$document = $store->add($request->file('document'));

$document->id;
$document->fileId;
```



> **참고:** 일반적으로 이전에 저장된 파일을 벡터 스토어에 추가할 때 반환되는 문서 ID는 파일에 이전에 할당된 ID와 일치하지만, 일부 벡터 스토리지 제공자는 새로운, 다른 "문서 ID"를 반환할 수 있습니다. 따라서 향후 참조를 위해 항상 두 ID를 데이터베이스에 저장하는 것이 권장됩니다.

파일을 Gemini 스토어에 추가할 때, Laravel은 호출이 반환되면 문서를 검색할 수 있도록 가져오기가 완료될 때까지 기다립니다. 가져오기가 실패하거나 5분 이상 소요되면 `Laravel\Ai\Exceptions\AiException`가 발생하므로, [큐에 등록된 작업](/docs/{{version}}/queues)에서 Gemini 파일을 추가하는 것이 좋을 수 있습니다.

파일을 스토어에 추가할 때 메타데이터를 첨부할 수 있습니다. 이 메타데이터는 나중에 [파일 검색 제공 도구](#file-search)를 사용할 때 검색 결과를 필터링하는 데 사용될 수 있습니다:

```php
$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [
    'author' => 'Taylor Otwell',
    'department' => 'Engineering',
    'year' => 2026,
]);
```



스토어에서 파일을 제거하려면 `remove` 방법을 사용하십시오:

```php
$store->remove('file_id');
```



벡터 스토어에서 파일을 제거해도 제공자의 [파일 스토리지](#files)에서는 삭제되지 않습니다. 벡터 스토어에서 파일을 제거하고 파일 스토리지에서 영구적으로 삭제하려면 `deleteFile` 인수를 사용하세요:

```php
$store->remove('file_abc123', deleteFile: true);
```



<a name="usage"></a>
## 사용법

모든 응답에는 공급자가 보고한 토큰 수를 포함하는 `usage` 속성이 포함되어 있습니다. 입력 및 출력 수는 총합이므로, 캐시된 토큰이나 추론 토큰으로 계산된 토큰도 속한 총합에 포함됩니다:

```php
$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

$response->usage->inputTokens;
$response->usage->outputTokens;
$response->usage->totalTokens();
```



텍스트 생성은 이러한 합계를 더 세분화하는 `Laravel\Ai\Responses\Data\TextUsage` 인스턴스를 반환합니다. 공급자가 이를 보고하지 않을 경우 이러한 값 각각은 `0`가 아닌 `null`가 됩니다:

```php
$response->usage->cacheReadInputTokens; // Subset of the input tokens read from a prompt cache...
$response->usage->cacheWriteInputTokens; // Subset of the input tokens written to a prompt cache...
$response->usage->reasoningTokens; // Subset of the output tokens spent on reasoning...

$response->usage->uncachedInputTokens(); // Input tokens that were neither read from nor written to the cache...
```



캐시 읽기, 캐시 쓰기 및 캐시되지 않은 입력은 서로 다른 요율로 청구되므로, 입력 합계만 사용하는 대신 이 세 가지 수치를 별도로 가격을 매겨야 합니다.

나머지 기능들은 각 기능에 특정된 수치를 포함한 사용량 객체를 반환합니다:

<div class="overflow-auto">

| 기능 | 사용량 객체 | 추가 항목 |
|---|---|---|
| 텍스트, 분류 | `TextUsage` | 캐시 읽기, 캐시 쓰기, 및 추론 토큰 |
| 이미지 | `ImageUsage` | `imageInputTokens` 및 `imageOutputTokens` |
| 전사 | `TranscriptionUsage` | `audioSeconds`, 전사된 오디오의 길이 |
| 재순위 | `RerankingUsage` | `searchUnits`, 일부 제공업체는 토큰 대신 청구함 |
| 오디오, 임베딩 | `Usage` | |

</div>

모든 제공업체가 모든 수치를 보고하지는 않으며, 제공업체가 보고하지 않은 수치는 `null`가 됩니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Transcription;

Image::of('A donut sitting on the kitchen counter')->generate()->usage->imageOutputTokens;

Transcription::fromPath('/home/laravel/meeting.mp3')->generate()->usage->audioSeconds;
```



<a name="failover"></a>
## 장애 조치

다른 미디어를 프롬프트하거나 생성할 때, 주 제공업체에서 서비스 중단이나 속도 제한이 발생하면 백업 제공업체/모델로 자동 장애 조치를 수행할 수 있도록 제공업체/모델 배열을 제공할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Enums\Lab;
use Laravel\Ai\Image;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [Lab::OpenAI, Lab::Anthropic],
);

$image = Image::of('A donut sitting on the kitchen counter')
    ->generate(provider: [Lab::Gemini, Lab::xAI]);
```



장애 조치(Failover)는 `FailoverableException`가 발생할 때만 발생합니다 — 예를 들어 속도 제한(`RateLimitedException`), 과부하 또는 서비스 불가 제공자(`ProviderOverloadedException`), 또는 충분하지 않은 크레딧(`InsufficientCreditsException`) 등이 있습니다. 검증 오류나 잘못된 요청 오류와 같은 일반적인 오류는 장애 조치를 트리거하지 않습니다.

`[Lab::OpenAI, Lab::Anthropic]`와 같이 단순한 제공자 목록을 전달하면 각 제공자는 기본 모델을 사용합니다. 장애 조치 체인에서 각 제공자에 대해 특정 모델을 지정하려면 PHP 배열 키로 `Lab` 열거형의 `value`를 사용하여 제공자를 키로 하는 연관 배열을 전달하십시오(열거형 케이스는 PHP 배열 키로 직접 사용할 수 없습니다):

```php
use Laravel\Ai\Enums\Lab;

$response = (new SalesCoach)->prompt(
    'Analyze this sales transcript...',
    provider: [
        Lab::Gemini->value => 'gemini-3-flash-preview',
        Lab::DeepSeek->value => 'deepseek-v4-pro',
    ],
);
```



<a name="testing"></a>
## 테스트

큐에 대기 중인 이미지, 오디오, 전사 또는 임베딩 생성을 가짜로 실행할 때, 큐에 등록된 모든 `then` 콜백이 가짜 응답과 함께 호출되어 콜백 내에 포함된 로직을 테스트할 수 있습니다. 이러한 콜백이 호출되지 않기를 원한다면, `Queue::fake()`를 사용하여 큐를 가짜로 실행할 수도 있습니다.

<a name="testing-agents"></a>
### 에이전트

테스트 중 에이전트의 응답을 가짜로 만들려면 에이전트 클래스에서 `fake` 메서드를 호출하세요. 선택적으로 응답 배열이나 클로저를 제공할 수 있습니다:

```php
use App\Ai\Agents\SalesCoach;
use Laravel\Ai\Prompts\AgentPrompt;

// Automatically generate a fixed response for every prompt...
SalesCoach::fake();

// Provide a list of prompt responses...
SalesCoach::fake([
    'First response',
    'Second response',
]);

// Dynamically handle prompt responses based on the incoming prompt...
SalesCoach::fake(function (AgentPrompt $prompt) {
    return 'Response for: '.$prompt->prompt;
});
```



구조화된 출력을 반환하는 에이전트를 가장할 때, 응답으로 배열을 제공할 수 있습니다. 에이전트는 주어진 데이터를 포함하는 구조화된 응답을 반환할 것입니다:

```php
SalesCoach::fake([
    ['score' => 87],
]);
```



도구 승인 대기 중인 응답을 가장할 수도 있습니다:

```php
use Laravel\Ai\Approvals\PendingApproval;
use Laravel\Ai\Responses\AgentResponse;

FileAssistant::fake([
    AgentResponse::fakeWithPendingApprovals([
        new PendingApproval(
            id: 'call_abc',
            tool: 'DeleteFile',
            arguments: ['path' => 'invoice.pdf'],
            reason: 'This will permanently delete a file.',
        ),
    ]),
]);

$response = (new FileAssistant)->prompt('Delete the invoice.');

$response->hasPendingApprovals(); // true
```



또한, 추론을 포함한 응답을 가장할 수 있습니다. 이 가짜는 추론 이벤트를 발생시키므로, 추론도 스트리밍 실행에서 보고됩니다:

```php
use Laravel\Ai\Responses\AgentResponse;

SalesCoach::fake([
    AgentResponse::fakeWithReasoning('They asked about pricing.', 'Plans start at $10.'),
]);

$response = (new SalesCoach)->stream('What does it cost?');

foreach ($response as $event) {
    // ...
}

$response->reasoning; // 'They asked about pricing.'
```



> **참고:** `Agent::fake()`가 구조화된 출력을 반환하는 에이전트에서 호출되고 가짜 출력이 명시적으로 제공되지 않은 경우, Laravel은 에이전트의 정의된 출력 스키마와 일치하는 가짜 데이터를 자동으로 생성합니다.

에이전트에 프롬프트를 보낸 후, 수신된 프롬프트에 대해 단언할 수 있습니다:

```php
use Laravel\Ai\Prompts\AgentPrompt;

SalesCoach::assertPrompted('Analyze this...');

SalesCoach::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertPromptedTimes(3);

SalesCoach::assertNotPrompted('Missing prompt');

SalesCoach::assertNeverPrompted();
```



승인 지속을 주장할 때, 프롬프트의 승인 결정을 확인할 수 있습니다:

```php
use Laravel\Ai\Approvals\Decisions;
use Laravel\Ai\Prompts\AgentPrompt;

FileAssistant::fake();

(new FileAssistant)->prompt(Decisions::from([
    'call_abc' => true,
]));

FileAssistant::assertPrompted(function (AgentPrompt $prompt) {
    return $prompt->hasApprovalDecisions()
        && $prompt->approvalDecisions->get('call_abc')->isApproved();
});
```



대기 중인 에이전트 호출의 경우, 대기 확인 메서드를 사용하세요:

```php
use Laravel\Ai\QueuedAgentPrompt;

SalesCoach::assertQueued('Analyze this...');

SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {
    return $prompt->contains('Analyze');
});

SalesCoach::assertNotQueued('Missing prompt');

SalesCoach::assertNeverQueued();
```



모든 에이전트 호출에 해당하는 가짜 응답이 있도록 보장하기 위해, `preventStrayPrompts`를 사용할 수 있습니다. 만약 정의된 가짜 응답 없이 에이전트가 호출되면, 예외가 발생할 것입니다:

```php
SalesCoach::fake()->preventStrayPrompts();
```



<a name="testing-images"></a>
### 이미지

이미지 생성은 `Image` 클래스에서 `fake` 메서드를 호출하여 조작될 수 있습니다. 이미지가 조작되면, 기록된 이미지 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다:

```php
use Laravel\Ai\Image;
use Laravel\Ai\Prompts\ImagePrompt;
use Laravel\Ai\Prompts\QueuedImagePrompt;

// Automatically generate a fixed response for every prompt...
Image::fake();

// Provide a list of prompt responses...
Image::fake([
    base64_encode($firstImage),
    base64_encode($secondImage),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Image::fake(function (ImagePrompt $prompt) {
    return base64_encode('...');
});
```



이미지를 생성한 후에는 받은 프롬프트에 대해 주장할 수 있습니다:

```php
Image::assertGenerated(function (ImagePrompt $prompt) {
    return $prompt->contains('sunset') && $prompt->isLandscape();
});

Image::assertNotGenerated('Missing prompt');

Image::assertNothingGenerated();
```



대기 중인 이미지 생성을 위해서는 대기 중인 어설션 메서드를 사용하세요:

```php
Image::assertQueued(
    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')
);

Image::assertNotQueued('Missing prompt');

Image::assertNothingQueued();
```



모든 이미지 생성에 해당하는 가짜 응답이 있도록 하려면 `preventStrayImages`를 사용할 수 있습니다. 정의된 가짜 응답 없이 이미지가 생성되면 예외가 발생합니다:

```php
Image::fake()->preventStrayImages();
```



<a name="testing-audio"></a>
### 오디오

오디오 생성을 `Audio` 클래스의 `fake` 메서드를 호출하여 조작할 수 있습니다. 오디오가 조작되면, 기록된 오디오 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다:

```php
use Laravel\Ai\Audio;
use Laravel\Ai\Prompts\AudioPrompt;
use Laravel\Ai\Prompts\QueuedAudioPrompt;

// Automatically generate a fixed response for every prompt...
Audio::fake();

// Provide a list of prompt responses...
Audio::fake([
    base64_encode($firstAudio),
    base64_encode($secondAudio),
]);

// Dynamically handle prompt responses based on the incoming prompt...
Audio::fake(function (AudioPrompt $prompt) {
    return base64_encode('...');
});
```



오디오를 생성한 후에, 받은 프롬프트에 대해 주장할 수 있습니다:

```php
Audio::assertGenerated(function (AudioPrompt $prompt) {
    return $prompt->contains('Hello') && $prompt->isFemale();
});

Audio::assertNotGenerated('Missing prompt');

Audio::assertNothingGenerated();
```



대기 중인 오디오 생성의 경우, 대기 중인 단언 메서드를 사용하세요:

```php
Audio::assertQueued(
    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')
);

Audio::assertNotQueued('Missing prompt');

Audio::assertNothingQueued();
```



모든 오디오 생성에 해당하는 가짜 응답이 있도록 하려면 `preventStrayAudio`를 사용할 수 있습니다. 정의된 가짜 응답 없이 오디오가 생성되면 예외가 발생합니다:

```php
Audio::fake()->preventStrayAudio();
```



<a name="testing-transcriptions"></a>
### 전사

전사 생성을 위조하려면 `Transcription` 클래스에서 `fake` 메서드를 호출하면 됩니다. 전사가 위조되면, 기록된 전사 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다:

```php
use Laravel\Ai\Transcription;
use Laravel\Ai\Prompts\TranscriptionPrompt;
use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

// Automatically generate a fixed response for every prompt...
Transcription::fake();

// Provide a list of prompt responses...
Transcription::fake([
    'First transcription text.',
    'Second transcription text.',
]);

// Dynamically handle prompt responses based on the incoming prompt...
Transcription::fake(function (TranscriptionPrompt $prompt) {
    return 'Transcribed text...';
});
```



전사본을 생성한 후에는 수신된 프롬프트에 대해 주장할 수 있습니다:

```php
Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {
    return $prompt->language === 'en' && $prompt->isDiarized();
});

Transcription::assertNotGenerated(
    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingGenerated();
```



대기 중인 전사 생성의 경우, 대기 중인 단언 메서드를 사용하세요:

```php
Transcription::assertQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()
);

Transcription::assertNotQueued(
    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'
);

Transcription::assertNothingQueued();
```



모든 전사 생성물이 해당하는 가짜 응답을 갖도록 보장하기 위해 `preventStrayTranscriptions`를 사용할 수 있습니다. 정의된 가짜 응답 없이 전사가 생성되면 예외가 발생합니다:

```php
Transcription::fake()->preventStrayTranscriptions();
```



<a name="testing-embeddings"></a>
### 임베딩

임베딩 생성을 `Embeddings` 클래스의 `fake` 메서드를 호출하여 위조할 수 있습니다. 임베딩이 위조되면, 기록된 임베딩 생성 프롬프트에 대해 다양한 검증을 수행할 수 있습니다:

```php
use Laravel\Ai\Embeddings;
use Laravel\Ai\Prompts\EmbeddingsPrompt;
use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

// Automatically generate fake embeddings of the proper dimensions for every prompt...
Embeddings::fake();

// Provide a list of prompt responses...
Embeddings::fake([
    [$firstEmbeddingVector],
    [$secondEmbeddingVector],
]);

// Dynamically handle prompt responses based on the incoming prompt...
Embeddings::fake(function (EmbeddingsPrompt $prompt) {
    return array_map(
        fn () => Embeddings::fakeEmbedding($prompt->dimensions),
        $prompt->inputs
    );
});
```



임베딩을 생성한 후에는 받은 프롬프트에 대해 주장할 수 있습니다:

```php
Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;
});

Embeddings::assertNotGenerated(
    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingGenerated();
```



대기 중인 임베딩 생성을 위해, 대기된 어설션 메서드를 사용하세요:

```php
Embeddings::assertQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')
);

Embeddings::assertNotQueued(
    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')
);

Embeddings::assertNothingQueued();
```



모든 임베딩 생성에 해당하는 가짜 응답이 있도록 하려면 `preventStrayEmbeddings`를 사용할 수 있습니다. 임베딩이 정의된 가짜 응답 없이 생성되면 예외가 발생합니다:

```php
Embeddings::fake()->preventStrayEmbeddings();
```



<a name="testing-reranking"></a>
### 재정렬

재정렬 작업은 `Reranking` 클래스에서 `fake` 메서드를 호출하여 가장할 수 있습니다:

```php
use Laravel\Ai\Reranking;
use Laravel\Ai\Prompts\RerankingPrompt;
use Laravel\Ai\Responses\Data\RankedDocument;

// Automatically generate a fake reranked responses...
Reranking::fake();

// Provide custom responses...
Reranking::fake([
    [
        new RankedDocument(index: 0, document: 'First', score: 0.95),
        new RankedDocument(index: 1, document: 'Second', score: 0.80),
    ],
]);
```



재정렬 후에 수행된 작업에 대해 주장할 수 있습니다:

```php
Reranking::assertReranked(function (RerankingPrompt $prompt) {
    return $prompt->contains('Laravel') && $prompt->limit === 5;
});

Reranking::assertNotReranked(
    fn (RerankingPrompt $prompt) => $prompt->contains('Django')
);

Reranking::assertNothingReranked();
```



<a name="testing-classification"></a>
### 분류

분류는 `Classification` 클래스에서 `fake` 메서드를 호출하여 위조될 수 있습니다. 맞춤 응답이 제공되지 않으면, Laravel은 각 질문의 형식에 맞는 답변을 자동으로 생성합니다:

```php
use Laravel\Ai\Classification;
use Laravel\Ai\Prompts\ClassificationPrompt;
use Laravel\Ai\Responses\Data\BooleanAnswer;
use Laravel\Ai\Responses\Data\ChoiceAnswer;

// Automatically generate fake answers...
Classification::fake();

// Provide answers for specific questions...
Classification::fake([
    [
        'urgent' => new BooleanAnswer(0.94),
        'department' => new ChoiceAnswer('technical', [
            'billing' => 0.08,
            'technical' => 0.87,
            'sales' => 0.05,
        ], confidence: 0.82),
    ],
]);

// Build answers from the prompt...
Classification::fake(fn (ClassificationPrompt $prompt) => [
    'urgent' => new BooleanAnswer($prompt->contains('ASAP') ? 1.0 : 0.0),
]);
```



가짜 응답에서 생략된 질문도 여전히 생성된 답변을 받게 되므로, 테스트에서는 단지 그 답변에 대해 단언하는 것만 제공하면 됩니다.

분류한 후에는 수행된 작업에 대해 단언을 할 수 있습니다:

```php
Classification::assertClassified(function (ClassificationPrompt $prompt) {
    return $prompt->contains('refund') && $prompt->asks('department');
});

Classification::assertNotClassified(
    fn (ClassificationPrompt $prompt) => $prompt->asks('sentiment')
);

Classification::assertNothingClassified();
```



<a name="testing-files"></a>
### 파일

파일 작업은 `Files` 클래스에서 `fake` 메서드를 호출하여 가장할 수 있습니다:

```php
use Laravel\Ai\Files;

Files::fake();
```



파일 작업이 조작되면 발생한 업로드 및 삭제에 대해 단언할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

// Store files...
Document::fromString('Hello, Laravel!', mimeType: 'text/plain')
    ->as('hello.txt')
    ->put();

// Make assertions...
Files::assertStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, Laravel!' &&
        $file->mimeType() === 'text/plain'
);

Files::assertNotStored(fn (StorableFile $file) =>
    (string) $file === 'Hello, World!'
);

Files::assertNothingStored();
```



파일 삭제에 대해 단언하려면 파일 ID를 전달할 수 있습니다:

```php
Files::assertDeleted('file-id');
Files::assertNotDeleted('file-id');
Files::assertNothingDeleted();
```



<a name="testing-vector-stores"></a>
### 벡터 저장소

벡터 저장소 작업은 `Stores` 클래스에서 `fake` 메서드를 호출하여 가장할 수 있습니다. 저장소를 가장하면 [파일 작업](#files)도 자동으로 가장됩니다:

```php
use Laravel\Ai\Stores;

Stores::fake();
```



스토어 작업이 조작된 후에는 생성되거나 삭제된 스토어에 대해 단언할 수 있습니다:

```php
use Laravel\Ai\Stores;

// Create store...
$store = Stores::create('Knowledge Base');

// Make assertions...
Stores::assertCreated('Knowledge Base');

Stores::assertCreated(fn (string $name, ?string $description) =>
    $name === 'Knowledge Base'
);

Stores::assertNotCreated('Other Store');

Stores::assertNothingCreated();
```



스토어 삭제에 대해 주장하기 위해, 스토어 ID를 제공할 수 있습니다:

```php
Stores::assertDeleted('store_id');
Stores::assertNotDeleted('other_store_id');
Stores::assertNothingDeleted();
```



스토어에서 파일이 추가되거나 제거되었음을 주장하려면, 주어진 `Store` 인스턴스에서 제공하는 단언 메서드를 사용하세요:

```php
Stores::fake();

$store = Stores::get('store_id');

// Add / remove files...
$store->add('added_id');
$store->remove('removed_id');

// Make assertions...
$store->assertAdded('added_id');
$store->assertRemoved('removed_id');

$store->assertNotAdded('other_file_id');
$store->assertNotRemoved('other_file_id');
```



파일이 제공자의 [파일 스토리지](#files)에 저장되고 동일한 요청에서 벡터 스토어에 추가된 경우, 파일의 제공자 ID를 모를 수 있습니다. 이 경우, 추가된 파일의 내용을 확인하기 위해 `assertAdded` 메서드에 클로저를 전달할 수 있습니다:

```php
use Laravel\Ai\Contracts\Files\StorableFile;
use Laravel\Ai\Files\Document;

$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');
$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

<a name="events"></a>
## 이벤트

Laravel AI SDK는 다음을 포함한 다양한 [이벤트](/docs/{{version}}/events)를 발생시킵니다:

- `AddingFileToStore`
- `AgentFailed`
- `AgentFailedOver`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
- `Classified`
- `Classifying`
- `CreatingStore`
- `EmbeddingsGenerated`
- `FileAddedToStore`
- `FileDeleted`
- `FileRemovedFromStore`
- `FileStored`
- `GeneratingAudio`
- `GeneratingEmbeddings`
- `GeneratingImage`
- `GeneratingTranscription`
- `ImageGenerated`
- `InvokingTool`
- `PromptingAgent`
- `ProviderFailedOver`
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StartingStep`
- `StepCompleted`
- `StepFailed`
- `StoreCreated`
- `StoreDeleted`
- `StoringFile`
- `StreamingAgent`
- `ToolApprovalRequested`
- `ToolApprovalResolved`
- `ToolFailed`
- `ToolInvoked`
- `TranscriptionGenerated`

이러한 이벤트 중 어느 것이든 청취하여 AI SDK 사용 정보를 기록하거나 저장할 수 있습니다.
{% endraw %}
