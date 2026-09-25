---
layout: docs
title: "Authorization"
---

{% raw %}
# Authorization

- [Introduction](#introduction)
- [Gates](#gates)
    - [Writing Gates](#writing-gates)
    - [Authorizing Actions](#authorizing-actions-via-gates)
    - [Gate Responses](#gate-responses)
    - [Intercepting Gate Checks](#intercepting-gate-checks)
    - [Inline Authorization](#inline-authorization)
- [Creating Policies](#creating-policies)
    - [Generating Policies](#generating-policies)
    - [Registering Policies](#registering-policies)
- [Writing Policies](#writing-policies)
    - [Policy Methods](#policy-methods)
    - [Policy Responses](#policy-responses)
    - [Methods Without Models](#methods-without-models)
    - [Guest Users](#guest-users)
    - [Policy Filters](#policy-filters)
- [Authorizing Actions Using Policies](#authorizing-actions-using-policies)
    - [Via the User Model](#via-the-user-model)
    - [Via the Gate Facade](#via-the-gate-facade)
    - [Via Middleware](#via-middleware)
    - [Via Blade Templates](#via-blade-templates)
    - [Supplying Additional Context](#supplying-additional-context)
- [Authorization & Inertia](#authorization-and-inertia)

<a name="introduction"></a>
## Introduction

In addition to providing built-in [authentication](/docs/{{version}}/authentication) services, Laravel also provides a simple way to authorize user actions against a given resource. For example, even though a user is authenticated, they may not be authorized to update or delete certain Eloquent models or database records managed by your application. Laravel's authorization features provide an easy, organized way of managing these types of authorization checks.

Laravel provides two primary ways of authorizing actions: [gates](#gates) and [policies](#creating-policies). Think of gates and policies like routes and controllers. Gates provide a simple, closure-based approach to authorization while policies, like controllers, group logic around a particular model or resource. In this documentation, we'll explore gates first and then examine policies.

You do not need to choose between exclusively using gates or exclusively using policies when building an application. Most applications will most likely contain some mixture of gates and policies, and that is perfectly fine! Gates are most applicable to actions that are not related to any model or resource, such as viewing an administrator dashboard. In contrast, policies should be used when you wish to authorize an action for a particular model or resource.

<a name="gates"></a>
## Gates



<a name="writing-gates"></a>
### 게이트 작성

> [!WARNING]
> 게이트는 Laravel의 권한 기능 기본을 배우는 훌륭한 방법입니다. 그러나 견고한 Laravel 애플리케이션을 구축할 때는 권한 규칙을 체계적으로 정리하기 위해 [정책](#creating-policies)의 사용을 고려해야 합니다.

게이트는 사용자가 주어진 작업을 수행할 수 있는지 결정하는 단순한 클로저입니다. 일반적으로 게이트는 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 `Gate` 파사드를 사용하여 정의됩니다. 게이트는 항상 첫 번째 인수로 사용자 인스턴스를 받고, 필요에 따라 관련 Eloquent 모델과 같은 추가 인수를 받을 수 있습니다.

이 예제에서는 사용자가 주어진 `App\Models\Post` 모델을 업데이트할 수 있는지 확인하는 게이트를 정의할 것입니다. 게이트는 게시물을 작성한 사용자의 `user_id`와 사용자의 `id`를 비교하여 이를 수행합니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', function (User $user, Post $post) {
        return $user->id === $post->user_id;
    });
}
```



컨트롤러처럼, 게이트 또한 클래스 콜백 배열을 사용하여 정의할 수 있습니다:

```php
use App\Policies\PostPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::define('update-post', [PostPolicy::class, 'update']);
}
```



<a name="authorizing-actions-via-gates"></a>
### 행동 승인하기

게이트를 사용하여 행동을 승인하려면 `Gate` 파사드에서 제공하는 `allows` 또는 `denies` 메서드를 사용해야 합니다. 현재 인증된 사용자를 이러한 메서드에 전달할 필요는 없다는 점에 유의하세요. Laravel은 사용자를 게이트 클로저에 자동으로 전달합니다. 일반적으로 권한이 필요한 행동을 수행하기 전에 애플리케이션 컨트롤러 내에서 게이트 승인 메서드를 호출하는 것이 일반적입니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if (! Gate::allows('update-post', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```



현재 인증된 사용자 이외의 사용자가 특정 작업을 수행할 권한이 있는지 확인하려면, `Gate` 퍼사드에서 `forUser` 메서드를 사용할 수 있습니다:

```php
if (Gate::forUser($user)->allows('update-post', $post)) {
    // The user can update the post...
}

if (Gate::forUser($user)->denies('update-post', $post)) {
    // The user can't update the post...
}
```



`any` 또는 `none` 메서드를 사용하여 한 번에 여러 작업을 승인할 수 있습니다:

```php
if (Gate::any(['update-post', 'delete-post'], $post)) {
    // The user can update or delete the post...
}

if (Gate::none(['update-post', 'delete-post'], $post)) {
    // The user can't update or delete the post...
}
```



<a name="authorizing-or-throwing-exceptions"></a>
#### 예외 승인 또는 발생

사용자가 주어진 행동을 수행할 수 없는 경우 자동으로 `Illuminate\Auth\Access\AuthorizationException`를 발생시키면서 행동을 승인하려면, `Gate` 파사드의 `authorize` 메서드를 사용할 수 있습니다. `AuthorizationException`의 인스턴스는 라라벨에 의해 자동으로 403 HTTP 응답으로 변환됩니다:

```php
Gate::authorize('update-post', $post);

// The action is authorized...
```



<a name="gates-supplying-additional-context"></a>
#### 추가 컨텍스트 제공

능력 인증을 위한 게이트 메서드(`allows`, `denies`, `check`, `any`, `none`, `authorize`, `can`, `cannot`)와 인증 [Blade 지시어](#via-blade-templates)(`@can`, `@cannot`, `@canany`)는 두 번째 인자로 배열을 받을 수 있습니다. 이 배열 요소들은 게이트 클로저에 매개변수로 전달되며, 인증 결정을 내릴 때 추가 컨텍스트로 사용할 수 있습니다:

```php
use App\Models\Category;
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::define('create-post', function (User $user, Category $category, bool $pinned) {
    if (! $user->canPublishToGroup($category->group)) {
        return false;
    } elseif ($pinned && ! $user->canPinPosts()) {
        return false;
    }

    return true;
});

if (Gate::check('create-post', [$category, $pinned])) {
    // The user can create the post...
}
```



<a name="gate-responses"></a>
### 게이트 응답

지금까지 우리는 단순 불리언 값을 반환하는 게이트만 살펴보았습니다. 그러나 때때로 오류 메시지를 포함한 더 자세한 응답을 반환하고 싶을 수 있습니다. 그렇게 하려면 게이트에서 `Illuminate\Auth\Access\Response`를 반환할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::deny('You must be an administrator.');
});
```



심지어 게이트에서 인증 응답을 반환할 때도, `Gate::allows` 메서드는 여전히 단순한 불리언 값을 반환합니다. 그러나 `Gate::inspect` 메서드를 사용하면 게이트가 반환한 전체 인증 응답을 가져올 수 있습니다:

```php
$response = Gate::inspect('edit-settings');

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```



`Gate::authorize` 방법을 사용할 때, 액션이 허가되지 않은 경우 `AuthorizationException`를 발생시키면, 허가 응답에서 제공된 오류 메시지가 HTTP 응답으로 전달됩니다:

```php
Gate::authorize('edit-settings');

// The action is authorized...
```



<a name="customizing-gate-response-status"></a>
#### HTTP 응답 상태 사용자 정의

액션이 Gate를 통해 거부될 때 `403` HTTP 응답이 반환됩니다. 그러나 경우에 따라 대체 HTTP 상태 코드를 반환하는 것이 유용할 수 있습니다. `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용하여 실패한 권한 확인에 대해 반환되는 HTTP 상태 코드를 사용자 정의할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyWithStatus(404);
});
```



웹 애플리케이션에서 `404` 응답을 통해 자원을 숨기는 것이 매우 일반적인 패턴이기 때문에, 편의를 위해 `denyAsNotFound` 방법이 제공됩니다:

```php
use App\Models\User;
use Illuminate\Auth\Access\Response;
use Illuminate\Support\Facades\Gate;

Gate::define('edit-settings', function (User $user) {
    return $user->isAdmin
        ? Response::allow()
        : Response::denyAsNotFound();
});
```



<a name="intercepting-gate-checks"></a>
### 게이트 검사 가로채기

때때로 특정 사용자에게 모든 권한을 부여하고 싶을 수 있습니다. 모든 다른 권한 검사가 수행되기 전에 실행되는 클로저를 정의하려면 `before` 방법을 사용할 수 있습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::before(function (User $user, string $ability) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```



`before` 클로저가 널이 아닌 결과를 반환하면 그 결과가 권한 확인의 결과로 간주됩니다.

다른 모든 권한 확인 후에 실행될 클로저를 정의하기 위해 `after` 메서드를 사용할 수 있습니다:

```php
use App\Models\User;

Gate::after(function (User $user, string $ability, bool|null $result, mixed $arguments) {
    if ($user->isAdministrator()) {
        return true;
    }
});
```



`after` 클로저에 의해 반환된 값은 게이트나 정책이 `null`를 반환하지 않는 한 권한 확인 결과를 덮어쓰지 않습니다.

<a name="inline-authorization"></a>
### 인라인 권한 부여

때때로, 특정 액션에 대해 전용 게이트를 작성하지 않고 현재 인증된 사용자가 그 액션을 수행할 권한이 있는지 확인하고 싶을 수 있습니다. Laravel은 이러한 유형의 "인라인" 권한 부여 확인을 `Gate::allowIf` 및 `Gate::denyIf` 메서드를 통해 수행할 수 있도록 허용합니다. 인라인 권한 부여는 정의된 ["사전" 또는 "사후" 권한 부여 후크](#intercepting-gate-checks)를 실행하지 않습니다:

```php
use App\Models\User;
use Illuminate\Support\Facades\Gate;

Gate::allowIf(fn (User $user) => $user->isAdministrator());

Gate::denyIf(fn (User $user) => $user->banned());
```



행위가 허가되지 않았거나 현재 인증된 사용자가 없는 경우, Laravel은 자동으로 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시킵니다. `AuthorizationException` 인스턴스는 Laravel의 예외 처리기에 의해 자동으로 403 HTTP 응답으로 변환됩니다.

<a name="creating-policies"></a>
## 정책 생성

<a name="generating-policies"></a>
### 정책 생성하기

정책은 특정 모델이나 리소스를 중심으로 권한 부여 로직을 구성하는 클래스입니다. 예를 들어, 애플리케이션이 블로그라면 `App\Models\Post` 모델과 포스트를 생성하거나 업데이트하는 사용자 행동을 권한 부여하기 위한 대응하는 `App\Policies\PostPolicy`가 있을 수 있습니다.

`make:policy` Artisan 명령을 사용하여 정책을 생성할 수 있습니다. 생성된 정책은 `app/Policies` 디렉터리에 배치됩니다. 애플리케이션에 이 디렉터리가 없으면 Laravel이 자동으로 생성합니다.

```shell
php artisan make:policy PostPolicy
```



`make:policy` 명령은 빈 정책 클래스를 생성합니다. 리소스를 보기, 생성, 업데이트 및 삭제와 관련된 예제 정책 메서드가 포함된 클래스를 생성하려면 명령을 실행할 때 `--model` 옵션을 제공할 수 있습니다:

```shell
php artisan make:policy PostPolicy --model=Post
```



<a name="registering-policies"></a>
### 정책 등록

<a name="policy-discovery"></a>
#### 정책 발견

기본적으로, Laravel은 모델과 정책이 표준 Laravel 명명 규칙을 따른다면 자동으로 정책을 발견합니다. 구체적으로, 정책은 모델이 포함된 디렉터리 위 또는 그 위치에 있는 `Policies` 디렉터리에 있어야 합니다. 예를 들어, 모델은 `app/Models` 디렉터리에 위치하고, 정책은 `app/Policies` 디렉터리에 위치할 수 있습니다. 이 경우, Laravel은 `app/Models/Policies` 그리고 `app/Policies`에서 정책을 확인합니다. 또한, 정책 이름은 모델 이름과 일치해야 하며 `Policy` 접미사를 가져야 합니다. 따라서, `User` 모델은 `UserPolicy` 정책 클래스에 해당합니다.

자신만의 정책 발견 논리를 정의하고 싶다면, `Gate::guessPolicyNamesUsing` 메서드를 사용하여 맞춤 정책 발견 콜백을 등록할 수 있습니다. 일반적으로 이 메서드는 애플리케이션의 `AppServiceProvider`의 `boot` 메서드에서 호출되어야 합니다.

```php
use Illuminate\Support\Facades\Gate;

Gate::guessPolicyNamesUsing(function (string $modelClass) {
    // Return the name of the policy class for the given model...
});
```



<a name="manually-registering-policies"></a>
#### 정책 수동 등록

`Gate` 퍼사드를 사용하여 응용 프로그램의 `AppServiceProvider` 내 `boot` 메서드에서 정책과 해당 모델을 수동으로 등록할 수 있습니다:

```php
use App\Models\Order;
use App\Policies\OrderPolicy;
use Illuminate\Support\Facades\Gate;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Gate::policy(Order::class, OrderPolicy::class);
}
```



또는 모델 클래스에 `UsePolicy` 속성을 배치하여 Laravel에 해당 모델의 정책을 알릴 수 있습니다:

```php
<?php

namespace App\Models;

use App\Policies\OrderPolicy;
use Illuminate\Database\Eloquent\Attributes\UsePolicy;
use Illuminate\Database\Eloquent\Model;

#[UsePolicy(OrderPolicy::class)]
class Order extends Model
{
    //
}
```



<a name="writing-policies"></a>
## 정책 작성

<a name="policy-methods"></a>
### 정책 메서드

정책 클래스가 등록되면, 해당 클래스가 허용하는 각 액션에 대해 메서드를 추가할 수 있습니다. 예를 들어, 특정 `PostPolicy`에서 주어진 `App\Models\User`가 주어진 `App\Models\Post` 인스턴스를 업데이트할 수 있는지 결정하는 `update` 메서드를 정의해 보겠습니다.

`update` 메서드는 `User`와 `Post` 인스턴스를 인자로 받으며, 사용자가 주어진 `Post`를 업데이트할 권한이 있는지를 나타내는 `true` 또는 `false`를 반환해야 합니다. 따라서 이 예에서는 사용자의 `id`가 게시물의 `user_id`와 일치하는지 확인할 것입니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(User $user, Post $post): bool
    {
        return $user->id === $post->user_id;
    }
}
```



You may continue to define additional methods on the policy as needed for the various actions it authorizes. For example, you might define `view` or `delete` methods to authorize various `Post` related actions, but remember you are free to give your policy methods any name you like.

If you used the `--model` option when generating your policy via the Artisan console, it will already contain methods for the `viewAny`, `view`, `create`, `update`, `delete`, `restore`, and `forceDelete` actions.

> [!NOTE]
> All policies are resolved via the Laravel [service container](/docs/{{version}}/container), allowing you to type-hint any needed dependencies in the policy's constructor to have them automatically injected.

<a name="policy-responses"></a>
### Policy Responses

So far, we have only examined policy methods that return simple boolean values. However, sometimes you may wish to return a more detailed response, including an error message. To do so, you may return an `Illuminate\Auth\Access\Response` instance from your policy method:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::deny('You do not own this post.');
}
```



정책에서 권한 부여 응답을 반환할 때, `Gate::allows` 메소드는 여전히 단순한 불리언 값을 반환합니다. 그러나 `Gate::inspect` 메소드를 사용하여 게이트에서 반환된 전체 권한 부여 응답을 가져올 수 있습니다:

```php
use Illuminate\Support\Facades\Gate;

$response = Gate::inspect('update', $post);

if ($response->allowed()) {
    // The action is authorized...
} else {
    echo $response->message();
}
```



`Gate::authorize` 방법을 사용할 때, 액션이 허가되지 않은 경우 `AuthorizationException`를 발생시키며, 허가 응답에서 제공된 오류 메시지는 HTTP 응답으로 전달됩니다:

```php
Gate::authorize('update', $post);

// The action is authorized...
```



<a name="customizing-policy-response-status"></a>
#### HTTP 응답 상태 사용자 지정

정책 메서드를 통해 동작이 거부되면 `403` HTTP 응답이 반환됩니다. 그러나 경우에 따라 대체 HTTP 상태 코드를 반환하는 것이 유용할 수 있습니다. `Illuminate\Auth\Access\Response` 클래스의 `denyWithStatus` 정적 생성자를 사용하여 권한 검사 실패 시 반환되는 HTTP 상태 코드를 사용자 지정할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyWithStatus(404);
}
```



웹 애플리케이션에서 `404` 응답을 통해 자원을 숨기는 것이 매우 일반적인 패턴이기 때문에, 편의를 위해 `denyAsNotFound` 방법이 제공됩니다:

```php
use App\Models\Post;
use App\Models\User;
use Illuminate\Auth\Access\Response;

/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post): Response
{
    return $user->id === $post->user_id
        ? Response::allow()
        : Response::denyAsNotFound();
}
```



<a name="methods-without-models"></a>
### 모델 없는 메서드

일부 정책 메서드는 현재 인증된 사용자 인스턴스만 받습니다. 이러한 상황은 `create` 작업을 승인할 때 가장 흔합니다. 예를 들어 블로그를 만들 때 사용자가 게시물을 전혀 만들 수 있는 권한이 있는지 여부를 결정하고 싶을 수 있습니다. 이러한 상황에서는 정책 메서드가 사용자 인스턴스만 받도록 예상해야 합니다:

```php
/**
 * Determine if the given user can create posts.
 */
public function create(User $user): bool
{
    return $user->role == 'writer';
}
```



<a name="guest-users"></a>
### 게스트 사용자

기본적으로, 모든 게이트와 정책은 들어오는 HTTP 요청이 인증된 사용자에 의해 시작되지 않은 경우 자동으로 `false`를 반환합니다. 그러나 사용자 인수 정의에 대해 "optional" 형식 힌트를 선언하거나 `null` 기본값을 제공함으로써 이러한 인가 검사가 게이트와 정책을 통과하도록 허용할 수 있습니다:

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * Determine if the given post can be updated by the user.
     */
    public function update(?User $user, Post $post): bool
    {
        return $user?->id === $post->user_id;
    }
}
```



<a name="policy-filters"></a>
### 정책 필터

특정 사용자에 대해, 주어진 정책 내의 모든 작업을 승인하도록 허용하고자 할 수 있습니다. 이를 수행하기 위해, 정책에 `before` 메서드를 정의하십시오. `before` 메서드는 정책의 다른 어떤 메서드보다 먼저 실행되어, 실제로 의도된 정책 메서드가 호출되기 전에 작업을 승인할 기회를 제공합니다. 이 기능은 애플리케이션 관리자가 모든 작업을 수행하도록 승인하는 데 가장 일반적으로 사용됩니다:

```php
use App\Models\User;

/**
 * Perform pre-authorization checks.
 */
public function before(User $user, string $ability): bool|null
{
    if ($user->isAdministrator()) {
        return true;
    }

    return null;
}
```



특정 유형의 사용자에 대해 모든 승인 검사를 거부하고자 하는 경우, `before` 메서드에서 `false`를 반환할 수 있습니다. `null`가 반환되면, 승인 검사는 정책 메서드로 넘어갑니다.

> [!WARNING]
> 정책 클래스에 확인하려는 권한 이름과 일치하는 이름의 메서드가 포함되어 있지 않으면, 정책 클래스의 `before` 메서드는 호출되지 않습니다.

<a name="authorizing-actions-using-policies"></a>
## 정책을 사용하여 작업 승인

<a name="via-the-user-model"></a>
### 사용자 모델을 통해서

Laravel 애플리케이션에 포함된 `App\Models\User` 모델에는 액션을 승인하는 데 도움이 되는 두 가지 메서드, `can`와 `cannot`가 포함되어 있습니다. `can`와 `cannot` 메서드는 승인하고자 하는 액션의 이름과 관련 모델을 받습니다. 예를 들어, 사용자가 특정 `App\Models\Post` 모델을 업데이트할 수 있는 권한이 있는지 확인해 보겠습니다. 일반적으로 이는 컨트롤러 메서드 내에서 수행됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Update the given post.
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        if ($request->user()->cannot('update', $post)) {
            abort(403);
        }

        // Update the post...

        return redirect('/posts');
    }
}
```



주어진 모델에 대해 [정책이 등록](#registering-policies)되어 있는 경우, `can` 메서드는 자동으로 적절한 정책을 호출하고 불리언 결과를 반환합니다. 모델에 대한 정책이 등록되지 않은 경우, `can` 메서드는 주어진 액션 이름과 일치하는 클로저 기반 Gate를 호출하려 시도합니다.

<a name="user-model-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 액션

일부 액션은 모델 인스턴스가 필요 없는 `create`와 같은 정책 메서드에 해당될 수 있음을 기억하세요. 이러한 상황에서는 `can` 메서드에 클래스 이름을 전달할 수 있습니다. 클래스 이름은 액션을 인가할 때 사용할 정책을 결정하는 데 사용됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class PostController extends Controller
{
    /**
     * Create a post.
     */
    public function store(Request $request): RedirectResponse
    {
        if ($request->user()->cannot('create', Post::class)) {
            abort(403);
        }

        // Create the post...

        return redirect('/posts');
    }
}
```



<a name="via-the-gate-facade"></a>
### `Gate` 퍼사드를 통한 방법

`App\Models\User` 모델에 제공되는 유용한 메서드 외에도, 항상 `Gate` 퍼사드의 `authorize` 메서드를 통해 작업을 승인할 수 있습니다.

`can` 메서드와 마찬가지로, 이 메서드는 승인하려는 작업의 이름과 관련 모델을 받습니다. 만약 작업이 승인되지 않은 경우, `authorize` 메서드는 `Illuminate\Auth\Access\AuthorizationException` 예외를 발생시키며, 라라벨 예외 처리기는 이를 자동으로 403 상태 코드가 포함된 HTTP 응답으로 변환합니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

class PostController extends Controller
{
    /**
     * Update the given blog post.
     *
     * @throws \Illuminate\Auth\Access\AuthorizationException
     */
    public function update(Request $request, Post $post): RedirectResponse
    {
        Gate::authorize('update', $post);

        // The current user can update the blog post...

        return redirect('/posts');
    }
}
```



<a name="controller-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

앞서 논의한 바와 같이, `create`와 같은 일부 정책 메서드는 모델 인스턴스를 필요로 하지 않습니다. 이러한 상황에서는 `authorize` 메서드에 클래스 이름을 전달해야 합니다. 클래스 이름은 작업을 승인할 때 사용할 정책을 결정하는 데 사용됩니다:

```php
use App\Models\Post;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Gate;

/**
 * Create a new blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function create(Request $request): RedirectResponse
{
    Gate::authorize('create', Post::class);

    // The current user can create blog posts...

    return redirect('/posts');
}
```



<a name="via-middleware"></a>
### 미들웨어를 통해

Laravel에는 들어오는 요청이 라우트나 컨트롤러에 도달하기 전에 작업을 승인할 수 있는 미들웨어가 포함되어 있습니다. 기본적으로, `Illuminate\Auth\Middleware\Authorize` 미들웨어는 Laravel에 의해 자동으로 등록된 `can` [미들웨어 별칭](/docs/{{version}}/middleware#middleware-aliases)을 사용하여 라우트에 연결될 수 있습니다. 사용자가 게시물을 업데이트할 수 있는 권한을 부여하기 위해 `can` 미들웨어를 사용하는 예제를 살펴봅시다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->middleware('can:update,post');
```



이 예제에서 우리는 `can` 미들웨어에 두 개의 인수를 전달하고 있습니다. 첫 번째는 권한을 부여하려는 액션의 이름이고, 두 번째는 정책 메서드에 전달하려는 라우트 매개변수입니다. 이 경우 [암묵적 모델 바인딩](/docs/{{version}}/routing#implicit-binding)을 사용하고 있으므로, `App\Models\Post` 모델이 정책 메서드에 전달됩니다. 사용자가 주어진 액션을 수행할 권한이 없으면, 미들웨어가 403 상태 코드의 HTTP 응답을 반환합니다.

편의를 위해, `can` 메서드를 사용하여 `can` 미들웨어를 라우트에 첨부할 수도 있습니다:

```php
use App\Models\Post;

Route::put('/post/{post}', function (Post $post) {
    // The current user may update the post...
})->can('update', 'post');
```



[컨트롤러 미들웨어 속성](/docs/{{version}}/controllers#middleware-attributes)을 사용 중인 경우, `Authorize` 속성을 통해 `can` 미들웨어를 적용할 수 있습니다:

```php
use Illuminate\Routing\Attributes\Controllers\Authorize;

#[Authorize('update', 'post')]
public function update(Post $post)
{
    // The current user may update the post...
}
```



<a name="middleware-actions-that-dont-require-models"></a>
#### 모델이 필요하지 않은 액션

다시 말해, `create`와 같은 일부 정책 메서드는 모델 인스턴스를 필요로 하지 않습니다. 이러한 경우 미들웨어에 클래스 이름을 전달할 수 있습니다. 클래스 이름은 액션을 승인할 때 사용할 정책을 결정하는 데 사용됩니다:

```php
Route::post('/post', function () {
    // The current user may create posts...
})->middleware('can:create,App\Models\Post');
```



문자열 미들웨어 정의 안에 전체 클래스 이름을 지정하는 것은 번거로울 수 있습니다. 이러한 이유로, `can` 방법을 사용하여 `can` 미들웨어를 라우트에 연결할 수 있습니다:

```php
use App\Models\Post;

Route::post('/post', function () {
    // The current user may create posts...
})->can('create', Post::class);
```



<a name="via-blade-templates"></a>
### 블레이드 템플릿을 통해

블레이드 템플릿을 작성할 때, 사용자가 특정 작업을 수행할 권한이 있는 경우에만 페이지의 일부를 표시하고 싶을 수 있습니다. 예를 들어, 사용자가 실제로 게시물을 업데이트할 수 있는 경우에만 블로그 게시물 업데이트 폼을 보여주고 싶을 수 있습니다. 이러한 상황에서는 `@can`와 `@cannot` 지시문을 사용할 수 있습니다:

```blade
@can('update', $post)
    <!-- The current user can update the post... -->
@elsecan('create', App\Models\Post::class)
    <!-- The current user can create new posts... -->
@else
    <!-- ... -->
@endcan

@cannot('update', $post)
    <!-- The current user cannot update the post... -->
@elsecannot('create', App\Models\Post::class)
    <!-- The current user cannot create new posts... -->
@endcannot
```



이 지시문들은 `@if` 및 `@unless` 문을 작성하기 위한 편리한 단축키입니다. 위의 `@can` 및 `@cannot` 문은 다음 문과 동일합니다:

```blade
@if (Auth::user()->can('update', $post))
    <!-- The current user can update the post... -->
@endif

@unless (Auth::user()->can('update', $post))
    <!-- The current user cannot update the post... -->
@endunless
```



사용자가 주어진 작업 배열에서 어떤 작업을 수행할 권한이 있는지도 결정할 수 있습니다. 이를 수행하려면 `@canany` 지시문을 사용하세요:

```blade
@canany(['update', 'view', 'delete'], $post)
    <!-- The current user can update, view, or delete the post... -->
@elsecanany(['create'], \App\Models\Post::class)
    <!-- The current user can create a post... -->
@endcanany
```



<a name="blade-actions-that-dont-require-models"></a>
#### 모델이 필요 없는 작업

다른 대부분의 인증 방법과 마찬가지로, 작업에 모델 인스턴스가 필요하지 않은 경우 `@can` 및 `@cannot` 지시문에 클래스 이름을 전달할 수 있습니다:

```blade
@can('create', App\Models\Post::class)
    <!-- The current user can create posts... -->
@endcan

@cannot('create', App\Models\Post::class)
    <!-- The current user can't create posts... -->
@endcannot
```



<a name="supplying-additional-context"></a>
### 추가 컨텍스트 제공

정책을 사용하여 작업을 승인할 때, 다양한 승인 함수와 헬퍼의 두 번째 인수로 배열을 전달할 수 있습니다. 배열의 첫 번째 요소는 어떤 정책을 호출할지 결정하는 데 사용되며, 나머지 배열 요소들은 정책 메서드에 매개변수로 전달되어 승인 결정을 내릴 때 추가적인 컨텍스트로 사용할 수 있습니다. 예를 들어, 다음의 `PostPolicy` 메서드 정의를 고려해보세요. 여기에는 추가 `$category` 매개변수가 포함되어 있습니다:

```php
/**
 * Determine if the given post can be updated by the user.
 */
public function update(User $user, Post $post, int $category): bool
{
    return $user->id === $post->user_id &&
           $user->canUpdateCategory($category);
}
```



인증된 사용자가 특정 게시물을 업데이트할 수 있는지 확인하려고 할 때, 우리는 다음과 같이 이 정책 메서드를 호출할 수 있습니다:

```php
/**
 * Update the given blog post.
 *
 * @throws \Illuminate\Auth\Access\AuthorizationException
 */
public function update(Request $request, Post $post): RedirectResponse
{
    Gate::authorize('update', [$post, $request->category]);

    // The current user can update the blog post...

    return redirect('/posts');
}
```



<a name="authorization-and-inertia"></a>
## 인증 및 Inertia

인증은 항상 서버에서 처리되어야 하지만, 애플리케이션 UI를 적절히 렌더링하기 위해 프론트엔드 애플리케이션에 인증 데이터를 제공하는 것이 종종 편리할 수 있습니다. Laravel은 Inertia 기반 프론트엔드에 인증 정보를 노출하기 위한 필수 규칙을 정의하지 않습니다.

그러나 Laravel의 Inertia 기반 [스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 사용하고 있다면, 애플리케이션에는 이미 `HandleInertiaRequests` 미들웨어가 포함되어 있습니다. 이 미들웨어의 `share` 메서드 내에서 애플리케이션의 모든 Inertia 페이지에 제공될 공유 데이터를 반환할 수 있습니다. 이 공유 데이터는 사용자에 대한 인증 정보를 정의하기 위한 편리한 위치로 활용될 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use App\Models\Post;
use Illuminate\Http\Request;
use Inertia\Middleware;

class HandleInertiaRequests extends Middleware
{
    // ...

    /**
     * Define the props that are shared by default.
     *
     * @return array<string, mixed>
     */
    public function share(Request $request)
    {
        return [
            ...parent::share($request),
            'auth' => [
                'user' => $request->user(),
                'permissions' => [
                    'post' => [
                        'create' => $request->user()->can('create', Post::class),
                    ],
                ],
            ],
        ];
    }
}
```
{% endraw %}
