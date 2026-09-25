---
layout: docs
title: "컨텍스트"
---

{% raw %}
# 컨텍스트

- [소개](#introduction)
- [How It Works](#how-it-works)
- 캡처 컨텍스트 (#capturing-context)
- [스택](#stacks)
- 캡처링 컨텍스트 (#retrieving-context)
- [항목 존재 결정](#determining-item-existence)
- [컨텍스트 제거](#removing-context)
- 숨겨진 맥락 (#hidden-context)
- 이벤트 (#events)
- 탈수 (#dehydrating)
- [수분 함유](#hydrated)

<a name="introduction"></a>
## 소개

Laravel 의 “컨텍스트” 기능을 사용하면 애플리케이션 내에서 실행되는 요청， 작업 및 명령 전반에 걸쳐 정보를 캡처， 검색 및 공유할 수 있습니다. 캡처된 이 정보는 애플리케이션에서 작성한 로그에도 포함되므로， 로그 항목이 작성되기 전에 발생한 주변 코드 실행 기록에 대한 심층적인 통찰력을 제공하고 분산 시스템 전체에서 실행 흐름을 추적할 수 있습니다。

<a name="how-it-works"></a>
### 어떻게 작동하는가

Laravel 의 컨텍스트 기능을 이해하는 가장 좋은 방법은 내장된 로깅 기능을 사용하여 작동 중인 모습을 보는 것입니다. 시작하려면 `Context` 패싯을 사용하여 [컨텍스트에 정보 추가](#capturing-context) 를 할 수 있습니다. 이 예에서는 [미들웨어](/docs/{{version}}/middleware) 를 사용하여 수신되는 모든 요청에 대해 요청 URL 과 고유한 추적 ID 를 컨텍스트에 추가합니다：

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;
use Symfony\Component\HttpFoundation\Response;

class AddContext
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): Response
    {
        Context::add('url', $request->url());
        Context::add('trace_id', Str::uuid()->toString());

        return $next($request);
    }
}

```

컨텍스트에 추가된 정보는 요청 전반에 걸쳐 작성된 모든 [로그 항목](/docs/{{version}}/logging)에 자동으로 메타데이터로 첨부됩니다. 컨텍스트를 메타데이터로 첨부하면 개별 로그 항목에 전달되는 정보와 `Context`를 통해 공유되는 정보를 구분할 수 있습니다. 예를 들어, 다음과 같은 로그 항목을 작성한다고 가정해 보겠습니다:

```php
Log::info('User authenticated.', ['auth_id' => Auth::id()]);

```

작성된 로그에는 로그 항목에 전달된 `auth_id`가 포함되지만, 메타데이터로서 컨텍스트의 `url`와 `trace_id`도 포함됩니다:

```text
User authenticated. {"auth_id":27} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}

```

컨텍스트에 추가된 정보는 큐에 배치된 작업에서도 사용할 수 있습니다. 예를 들어, 컨텍스트에 일부 정보를 추가한 후 `ProcessPodcast` 작업을 큐에 배치한다고 가정해 보겠습니다:

```php
// In our middleware...
Context::add('url', $request->url());
Context::add('trace_id', Str::uuid()->toString());

// In our controller...
ProcessPodcast::dispatch($podcast);

```

작업이 배포될 때, 현재 컨텍스트에 저장된 모든 정보가 캡처되어 작업과 공유됩니다. 캡처된 정보는 작업이 실행되는 동안 다시 현재 컨텍스트로 복원됩니다. 따라서 우리의 작업의 handle 메서드가 로그에 기록하는 경우:

```php
class ProcessPodcast implements ShouldQueue
{
    use Queueable;

    // ...

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        Log::info('Processing podcast.', [
            'podcast_id' => $this->podcast->id,
        ]);

        // ...
    }
}

```

결과 로그 항목에는 원래 작업을 실행한 요청 동안 컨텍스트에 추가된 정보가 포함됩니다:

```text
Processing podcast. {"podcast_id":95} {"url":"https://example.com/login","trace_id":"e04e1a11-e75c-4db3-b5b5-cfef4ef56697"}

```

Laravel의 컨텍스트와 관련된 내장 로깅 기능에 초점을 맞췄지만, 다음 문서는 컨텍스트가 HTTP 요청/큐 작업 경계를 넘어 정보를 공유할 수 있는 방법과 로그 항목에 기록되지 않는 [숨겨진 컨텍스트 데이터](#hidden-context)를 추가하는 방법을 보여줄 것입니다.

<a name="capturing-context"></a>
## 컨텍스트 캡처

현재 컨텍스트에 정보를 저장하려면 `Context` 파사드의 `add` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add('key', 'value');

```

여러 항목을 한 번에 추가하려면, 연관 배열을 `add` 메서드에 전달할 수 있습니다:

```php
Context::add([
    'first_key' => 'value',
    'second_key' => 'value',
]);

```



`add` 메서드는 동일한 키를 가진 기존 값을 모두 덮어씁니다. 만약 키가 이미 존재하지 않을 때만 컨텍스트에 정보를 추가하고 싶다면, `addIf` 메서드를 사용할 수 있습니다:

```php
Context::add('key', 'first');

Context::get('key');
// "first"

Context::addIf('key', 'second');

Context::get('key');
// "first"

```

컨텍스트는 또한 주어진 키를 증가시키거나 감소시키는 편리한 방법을 제공합니다. 이 두 가지 방법 모두 최소 하나의 인수를 받습니다: 추적할 키. 두 번째 인수는 키를 증가시키거나 감소시킬 양을 지정하기 위해 제공될 수 있습니다:

```php
Context::increment('records_added');
Context::increment('records_added', 5);

Context::decrement('records_added');
Context::decrement('records_added', 5);

```

<a name="conditional-context"></a>
#### 조건부 컨텍스트

`when` 메서드는 주어진 조건에 따라 컨텍스트에 데이터를 추가하는 데 사용될 수 있습니다. `when` 메서드에 제공된 첫 번째 클로저는 주어진 조건이 `true`로 평가될 경우 호출되며, 두 번째 클로저는 조건이 `false`로 평가될 경우 호출됩니다:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Context;

Context::when(
    Auth::user()->isAdmin(),
    fn ($context) => $context->add('permissions', Auth::user()->permissions),
    fn ($context) => $context->add('permissions', []),
);

```

<a name="scoped-context"></a>
#### 범위 지정된 컨텍스트

`scope` 메서드는 주어진 콜백이 실행되는 동안 컨텍스트를 일시적으로 수정하고, 콜백 실행이 끝나면 컨텍스트를 원래 상태로 복원하는 방법을 제공합니다. 또한, 클로저가 실행되는 동안 컨텍스트에 병합되어야 하는 추가 데이터를 두 번째와 세 번째 인수로 전달할 수 있습니다.

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\Log;

Context::add('trace_id', 'abc-999');
Context::addHidden('user_id', 123);

Context::scope(
    function () {
        Context::add('action', 'adding_friend');

        $userId = Context::getHidden('user_id');

        Log::debug("Adding user [{$userId}] to friends list.");
        // Adding user [987] to friends list.  {"trace_id":"abc-999","user_name":"taylor_otwell","action":"adding_friend"}
    },
    data: ['user_name' => 'taylor_otwell'],
    hidden: ['user_id' => 987],
);

Context::all();
// [
//     'trace_id' => 'abc-999',
// ]

Context::allHidden();
// [
//     'user_id' => 123,
// ]

```

> [!WARNING]
> 스코프 내 클로저 안에서 컨텍스트 내의 객체가 수정되면, 그 변화는 스코프 외부에도 반영됩니다.

<a name="stacks"></a>
### 스택

컨텍스트는 '스택'을 생성할 수 있는 기능을 제공합니다. 스택은 추가된 순서대로 저장되는 데이터 목록입니다. `push` 메서드를 호출하여 스택에 정보를 추가할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::push('breadcrumbs', 'first_value');

Context::push('breadcrumbs', 'second_value', 'third_value');

Context::get('breadcrumbs');
// [
//     'first_value',
//     'second_value',
//     'third_value',
// ]

```

스택은 요청에 대한 역사적 정보를 캡처하는 데 유용할 수 있으며, 예를 들어 애플리케이션 전반에서 발생하는 이벤트를 포함할 수 있습니다. 예를 들어, 쿼리가 실행될 때마다 스택에 푸시하도록 이벤트 리스너를 생성하여 쿼리 SQL과 실행 시간을 튜플로 캡처할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Facades\DB;

// In AppServiceProvider.php...
DB::listen(function ($event) {
    Context::push('queries', [$event->time, $event->sql]);
});

```



`stackContains` 및 `hiddenStackContains` 메서드를 사용하여 값이 스택에 있는지 여부를 확인할 수 있습니다:

```php
if (Context::stackContains('breadcrumbs', 'first_value')) {
    //
}

if (Context::hiddenStackContains('secrets', 'first_value')) {
    //
}

```



`stackContains`와 `hiddenStackContains` 메서드는 두 번째 인수로 클로저를 받기도 하여, 값 비교 연산에 대한 더 많은 제어를 허용합니다:

```php
use Illuminate\Support\Facades\Context;
use Illuminate\Support\Str;

return Context::stackContains('breadcrumbs', function ($value) {
    return Str::startsWith($value, 'query_');
});

```

<a name="retrieving-context"></a>
## 컨텍스트 가져오기

`Context` 파사드의 `get` 메서드를 사용하여 컨텍스트에서 정보를 가져올 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

$value = Context::get('key');

```



`only` 및 `except` 방법은 컨텍스트에서 정보의 일부를 가져오는 데 사용될 수 있습니다:

```php
$data = Context::only(['first_key', 'second_key']);

$data = Context::except(['first_key']);

```



`pull` 방법은 컨텍스트에서 정보를 가져오고 즉시 컨텍스트에서 제거하는 데 사용할 수 있습니다:

```php
$value = Context::pull('key');

```

컨텍스트 데이터가 [스택](#stacks)에 저장되어 있다면, `pop` 메서드를 사용하여 스택에서 항목을 꺼낼 수 있습니다:

```php
Context::push('breadcrumbs', 'first_value', 'second_value');

Context::pop('breadcrumbs');
// second_value

Context::get('breadcrumbs');
// ['first_value']

```



`remember`와 `rememberHidden` 메서드는 요청된 정보가 존재하지 않을 경우 주어진 클로저가 반환한 값으로 컨텍스트 값을 설정하면서 컨텍스트에서 정보를 가져오는 데 사용할 수 있습니다:

```php
$permissions = Context::remember(
    'user-permissions',
    fn () => $user->permissions,
);

```

컨텍스트에 저장된 모든 정보를 가져오려면 `all` 메서드를 호출할 수 있습니다:

```php
$data = Context::all();

```

<a name="determining-item-existence"></a>
### 항목 존재 여부 확인

주어진 키에 대해 컨텍스트에 값이 저장되어 있는지 확인하려면 `has` 및 `missing` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

if (Context::has('key')) {
    // ...
}

if (Context::missing('key')) {
    // ...
}

```



`has` 방법은 저장된 값에 상관없이 `true`를 반환합니다. 따라서 예를 들어 `null` 값을 가진 키도 존재하는 것으로 간주됩니다:

```php
Context::add('key', null);

Context::has('key');
// true

```

<a name="removing-context"></a>
## 컨텍스트 제거

`forget` 메서드는 현재 컨텍스트에서 키와 해당 값을 제거하는 데 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Context;

Context::add(['first_key' => 1, 'second_key' => 2]);

Context::forget('first_key');

Context::all();

// ['second_key' => 2]

```



`forget` 메서드에 배열을 제공하여 여러 키를 한 번에 잊을 수 있습니다:

```php
Context::forget(['first_key', 'second_key']);

```

<a name="hidden-context"></a>
## 숨겨진 컨텍스트

컨텍스트는 "숨겨진" 데이터를 저장할 수 있는 기능을 제공합니다. 이 숨겨진 정보는 로그에 추가되지 않으며, 위에 문서화된 데이터 검색 방법을 통해 접근할 수 없습니다. 컨텍스트는 숨겨진 컨텍스트 정보를 상호작용하기 위한 다른 방법들을 제공합니다:

```php
use Illuminate\Support\Facades\Context;

Context::addHidden('key', 'value');

Context::getHidden('key');
// 'value'

Context::get('key');
// null

```

“숨겨진” 메서드는 위에 문서화된 숨겨지지 않은 메서드의 기능을 그대로 반영합니다:

```php
Context::addHidden(/* ... */);
Context::addHiddenIf(/* ... */);
Context::pushHidden(/* ... */);
Context::getHidden(/* ... */);
Context::pullHidden(/* ... */);
Context::popHidden(/* ... */);
Context::onlyHidden(/* ... */);
Context::exceptHidden(/* ... */);
Context::allHidden(/* ... */);
Context::hasHidden(/* ... */);
Context::missingHidden(/* ... */);
Context::forgetHidden(/* ... */);

```

<a name="events"></a>
## 이벤트

컨텍스트는 컨텍스트의 수분 공급 및 탈수 과정에 참여할 수 있게 해주는 두 가지 이벤트를 전송합니다。

이러한 이벤트를 사용하는 방법을 설명하기 위해， 애플리케이션의 미들웨어에서 수신 HTTP 요청의 `Accept-Language` 헤더를 기반으로 `app.locale` 구성 값을 설정한다고 가정해 보겠습니다. 컨텍스트의 이벤트를 사용하면 요청 중에 이 값을 캡처하고 대기열에서 복원할 수 있으므로， 대기열에 전송된 알림에 올바른 `app.locale` 값이 있는지 확인할 수 있습니다. 다음 설명서에서 설명하는 것처럼 컨텍스트의 이벤트와 [숨겨진](#hidden-context) 데이터를 사용하여 이를 달성할 수 있습니다。

<a name="dehydrating"></a>
### 탈수

작업이 대기열로 전송될 때마다 컨텍스트의 데이터가 “탈수화” 되고 작업의 페이로드와 함께 캡처됩니다. `Context::dehydrating` 메서드를 사용하면 탈수화 프로세스 중에 호출될 종료를 등록할 수 있습니다. 이 종료 내에서 대기열에 있는 작업과 공유될 데이터를 변경할 수 있습니다。

일반적으로 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에 `dehydrating` 콜백을 등록해야 합니다：

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::dehydrating(function (Repository $context) {
        $context->addHidden('locale', Config::get('app.locale'));
    });
}

```

> [!NOTE]
> `dehydrating` 콜백 내에서 `Context` 퍼사드를 사용해서는 안 됩니다. 이는 현재 프로세스의 컨텍스트를 변경할 수 있습니다. 콜백에 전달된 저장소에만 변경을 가하도록 하십시오.

<a name="hydrated"></a>
### 하이드레이션됨

큐에서 대기 중인 작업이 실행되기 시작할 때, 작업과 공유된 모든 컨텍스트는 현재 컨텍스트로 "하이드레이션"됩니다. `Context::hydrated` 메서드를 사용하면 하이드레이션 과정 동안 호출될 클로저를 등록할 수 있습니다.

일반적으로, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 `hydrated` 콜백을 등록해야 합니다:

```php
use Illuminate\Log\Context\Repository;
use Illuminate\Support\Facades\Config;
use Illuminate\Support\Facades\Context;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Context::hydrated(function (Repository $context) {
        if ($context->hasHidden('locale')) {
            Config::set('app.locale', $context->getHidden('locale'));
        }
    });
}

```

> [!NOTE]
> `hydrated` 콜백 내에서 `Context` 퍼사드를 사용해서는 안 되며, 대신 콜백에 전달된 리포지토리에만 변경을 해야 합니다.
{% endraw %}
