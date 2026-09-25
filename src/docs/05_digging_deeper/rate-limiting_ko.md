---
layout: docs
title: "속도 제한"
---

{% raw %}
# 속도 제한

- [소개](#introduction)
    - [캐시 구성](#cache-configuration)
- [기본 사용법](#basic-usage)
    - [시도 수 수동 증가](#manually-incrementing-attempts)
    - [시도 수 초기화](#clearing-attempts)

<a name="introduction"></a>
## 소개

Laravel은 사용하기 간단한 속도 제한 추상화를 포함하고 있으며, 애플리케이션의 [캐시](cache)와 함께 특정 시간 동안 모든 동작을 쉽게 제한할 수 있는 방법을 제공합니다.

> [!NOTE]
> 들어오는 HTTP 요청의 속도 제한에 관심이 있다면, [속도 제한 미들웨어 문서](/docs/{{version}}/routing#rate-limiting)를 참조하세요.

<a name="cache-configuration"></a>
### 캐시 구성

일반적으로 속도 제한기는 애플리케이션의 `cache` 구성 파일 내 `default` 키로 정의된 기본 애플리케이션 캐시를 사용합니다. 그러나 애플리케이션의 `cache` 구성 파일에 `limiter` 키를 정의하여 속도 제한기가 사용할 캐시 드라이버를 지정할 수 있습니다:

```php
'default' => env('CACHE_STORE', 'database'),

'limiter' => 'redis', // [tl! add]

```

<a name="basic-usage"></a>
## 기본 사용법

`Illuminate\Support\Facades\RateLimiter` 페이스북을 사용하면 레이트 리미터와 상호작용할 수 있습니다. 레이트 리미터가 제공하는 가장 간단한 메서드는 `attempt` 메서드로, 주어진 콜백을 지정된 초 동안 제한합니다.

`attempt` 메서드는 콜백에 사용할 수 있는 남은 시도가 없을 때 `false`를 반환합니다. 그렇지 않으면 `attempt` 메서드는 콜백의 결과 또는 `true`를 반환합니다. `attempt` 메서드가 받는 첫 번째 인수는 레이트 리미터 "키"로, 제한하려는 동작을 나타내는 원하는 문자열을 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perMinute = 5,
    function() {
        // Send message...
    }
);

if (! $executed) {
    return 'Too many messages sent!';
}

```

필요하다면 `attempt` 메서드에 네 번째 인수를 제공할 수 있으며, 이는 '감쇠율' 또는 사용 가능한 시도가 초기화될 때까지의 초 수입니다. 예를 들어, 위의 예제를 수정하여 2분마다 다섯 번의 시도를 허용할 수 있습니다:

```php
$executed = RateLimiter::attempt(
    'send-message:'.$user->id,
    $perTwoMinutes = 5,
    function() {
        // Send message...
    },
    $decayRate = 120,
);

```

<a name="manually-incrementing-attempts"></a>
### 수동으로 시도 횟수 증가시키기

속도 제한기(rate limiter)를 수동으로 조작하고 싶다면, 다양한 다른 방법들이 있습니다. 예를 들어, `tooManyAttempts` 메서드를 호출하여 특정 속도 제한기 키가 1분당 허용된 최대 시도 횟수를 초과했는지 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    return 'Too many attempts!';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...

```

많은 동시 요청을 받을 수 있는 엔드포인트의 속도 제한을 설정할 때, `tooManyAttempts`와 `increment`를 개별 작업으로 사용하는 대신 `increment` 메서드가 반환하는 값을 확인하는 것이 좋습니다. `redis`, `memcached` 또는 `database` 캐시 스토어를 사용할 경우, 이 값은 원자적으로 증가하여 각 동시 요청이 고유한 카운트를 받도록 보장됩니다:

```php
use Illuminate\Support\Facades\RateLimiter;

$perMinute = 5;

if (RateLimiter::increment('send-message:'.$user->id) > $perMinute) {
    return 'Too many attempts!';
}

// Send message...

```

또는 `remaining` 방법을 사용하여 특정 키에 남아 있는 시도 횟수를 가져올 수 있습니다. 특정 키에 남은 재시도가 있는 경우, `increment` 방법을 호출하여 총 시도 횟수를 증가시킬 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::remaining('send-message:'.$user->id, $perMinute = 5)) {
    RateLimiter::increment('send-message:'.$user->id);

    // Send message...
}

```

주어진 속도 제한 키의 값을 1보다 더 많이 증가시키고 싶다면, `increment` 메서드에 원하는 수량을 제공할 수 있습니다:

```php
RateLimiter::increment('send-message:'.$user->id, amount: 5);

```

<a name="determining-limiter-availability"></a>
#### 제한기 사용 가능 여부 확인

키에 더 이상 시도가 남아 있지 않은 경우, `availableIn` 방법은 더 많은 시도를 할 수 있을 때까지 남은 초를 반환합니다:

```php
use Illuminate\Support\Facades\RateLimiter;

if (RateLimiter::tooManyAttempts('send-message:'.$user->id, $perMinute = 5)) {
    $seconds = RateLimiter::availableIn('send-message:'.$user->id);

    return 'You may try again in '.$seconds.' seconds.';
}

RateLimiter::increment('send-message:'.$user->id);

// Send message...

```

<a name="clearing-attempts"></a>
### 시도 횟수 초기화

`clear` 방법을 사용하여 특정 속도 제한 키에 대한 시도 횟수를 재설정할 수 있습니다. 예를 들어, 특정 메시지가 수신자에 의해 읽힐 때 시도 횟수를 재설정할 수 있습니다:

```php
use App\Models\Message;
use Illuminate\Support\Facades\RateLimiter;

/**
 * Mark the message as read.
 */
public function read(Message $message): Message
{
    $message->markAsRead();

    RateLimiter::clear('send-message:'.$message->user_id);

    return $message;
}

```
{% endraw %}
