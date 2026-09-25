---
layout: docs
title: "Controllers"
---

{% raw %}
# Controllers

- [Introduction](#introduction)
- [Writing Controllers](#writing-controllers)
    - [Basic Controllers](#basic-controllers)
    - [Single Action Controllers](#single-action-controllers)
- [Controller Middleware](#controller-middleware)
    - [Middleware Attributes](#middleware-attributes)
    - [Authorization Attributes](#authorization-attributes)
- [Resource Controllers](#resource-controllers)
    - [Partial Resource Routes](#restful-partial-resource-routes)
    - [Nested Resources](#restful-nested-resources)
    - [Naming Resource Routes](#restful-naming-resource-routes)
    - [Naming Resource Route Parameters](#restful-naming-resource-route-parameters)
    - [Scoping Resource Routes](#restful-scoping-resource-routes)
    - [Localizing Resource URIs](#restful-localizing-resource-uris)
    - [Supplementing Resource Controllers](#restful-supplementing-resource-controllers)
    - [Singleton Resource Controllers](#singleton-resource-controllers)
    - [Middleware and Resource Controllers](#middleware-and-resource-controllers)
- [Dependency Injection and Controllers](#dependency-injection-and-controllers)

<a name="introduction"></a>
## Introduction

Instead of defining all of your request handling logic as closures in your route files, you may wish to organize this behavior using "controller" classes. Controllers can group related request handling logic into a single class. For example, a `UserController` class might handle all incoming requests related to users, including showing, creating, updating, and deleting users. By default, controllers are stored in the `app/Http/Controllers` directory.

<a name="writing-controllers"></a>
## Writing Controllers

<a name="basic-controllers"></a>
### Basic Controllers

To quickly generate a new controller, you may run the `make:controller` Artisan command. By default, all of the controllers for your application are stored in the `app/Http/Controllers` directory:

```shell
php artisan make:controller UserController
```



기본 컨트롤러의 예제를 살펴봅시다. 컨트롤러는 들어오는 HTTP 요청에 응답할 수 있는 임의의 수의 public 메소드를 가질 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): View
    {
        return view('user.profile', [
            'user' => User::findOrFail($id)
        ]);
    }
}
```



컨트롤러 클래스와 메서드를 작성한 후에는 다음과 같이 컨트롤러 메서드로 가는 라우트를 정의할 수 있습니다:

```php
use App\Http\Controllers\UserController;

Route::get('/user/{id}', [UserController::class, 'show']);
```



들어오는 요청이 지정된 라우트 URI와 일치하면, `App\Http\Controllers\UserController` 클래스의 `show` 메서드가 호출되고 라우트 매개변수가 해당 메서드로 전달됩니다.

> [!NOTE]
> 컨트롤러는 기본 클래스를 **상속할 필요가 없습니다**. 그러나 때때로 모든 컨트롤러에서 공유되어야 하는 메서드를 포함하는 기본 컨트롤러 클래스를 상속하는 것이 편리할 수 있습니다.

<a name="single-action-controllers"></a>
### 단일 액션 컨트롤러

컨트롤러 액션이 특히 복잡한 경우, 해당 단일 액션에 전용 컨트롤러 클래스를 만드는 것이 편리할 수 있습니다. 이를 구현하기 위해, 컨트롤러 내에 단일 `__invoke` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

class ProvisionServer extends Controller
{
    /**
     * Provision a new web server.
     */
    public function __invoke()
    {
        // ...
    }
}
```



단일 액션 컨트롤러용 라우트를 등록할 때는 컨트롤러 메서드를 지정할 필요가 없습니다. 대신 라우터에 컨트롤러 이름만 전달하면 됩니다:

```php
use App\Http\Controllers\ProvisionServer;

Route::post('/server', ProvisionServer::class);
```



`make:controller` Artisan 명령어의 `--invokable` 옵션을 사용하여 호출 가능한 컨트롤러를 생성할 수 있습니다:

```shell
php artisan make:controller ProvisionServer --invokable
```



> [!NOTE]
> 컨트롤러 스텁은 [스텁 게시](/docs/{{version}}/artisan#stub-customization)를 사용하여 사용자 정의할 수 있습니다.

<a name="controller-middleware"></a>
## 컨트롤러 미들웨어

[미들웨어](/docs/{{version}}/middleware)는 라우트 파일에서 컨트롤러의 라우트에 할당할 수 있습니다:

```php
Route::get('/profile', [UserController::class, 'show'])->middleware('auth');
```



또는 컨트롤러 클래스 내에서 미들웨어를 지정하는 것이 편리할 수 있습니다. 이렇게 하려면, 컨트롤러가 `HasMiddleware` 인터페이스를 구현해야 하며, 이 인터페이스는 컨트롤러가 정적 `middleware` 메서드를 가져야 한다고 규정합니다. 이 메서드에서 컨트롤러의 액션에 적용될 미들웨어 배열을 반환할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Controllers\HasMiddleware;
use Illuminate\Routing\Controllers\Middleware;

class UserController implements HasMiddleware
{
    /**
     * Get the middleware that should be assigned to the controller.
     */
    public static function middleware(): array
    {
        return [
            'auth',
            new Middleware('log', only: ['index']),
            new Middleware('subscribed', except: ['store']),
        ];
    }

    // ...
}
```



컨트롤러 미들웨어를 클로저로 정의할 수도 있는데, 이는 전체 미들웨어 클래스를 작성하지 않고 인라인 미들웨어를 정의할 수 있는 편리한 방법을 제공합니다:

```php
use Closure;
use Illuminate\Http\Request;

/**
 * Get the middleware that should be assigned to the controller.
 */
public static function middleware(): array
{
    return [
        function (Request $request, Closure $next) {
            return $next($request);
        },
    ];
}
```



<a name="middleware-attributes"></a>
### 미들웨어 속성

PHP 속성을 사용하여 미들웨어를 컨트롤러에 할당할 수도 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
#[Middleware('log', only: ['index'])]
#[Middleware('subscribed', except: ['store'])]
class UserController
{
    // ...
}
```



개별 컨트롤러 메서드에도 미들웨어 속성을 지정할 수 있습니다. 메서드에 할당된 미들웨어는 클래스 수준에 할당된 미들웨어와 병합됩니다:

```php
<?php

namespace App\Http\Controllers;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Routing\Attributes\Controllers\Middleware;

#[Middleware('auth')]
class UserController
{
    #[Middleware('log')]
    #[Middleware('subscribed')]
    public function index()
    {
        // ...
    }

    #[Middleware(static function (Request $request, Closure $next) {
        // ...

        return $next($request);
    })]
    public function store()
    {
        // ...
    }
}
```



컨트롤러 또는 개별 컨트롤러 메서드에서 미들웨어를 제외하려면 `WithoutMiddleware` 속성을 사용하십시오. 클래스 수준 속성을 특정 컨트롤러 메서드로 제한하려면 `only` 및 `except` 인수를 사용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Middleware\EnsureTokenIsValid;
use Illuminate\Routing\Attributes\Controllers\WithoutMiddleware;

#[WithoutMiddleware('subscribed', except: ['index'])]
class UserController
{
    #[WithoutMiddleware(EnsureTokenIsValid::class)]
    public function index()
    {
        // ...
    }

    public function show()
    {
        // ...
    }
}
```



클래스 수준의 `WithoutMiddleware` 속성은 자식 컨트롤러에 상속됩니다. 이 속성은 라우트 미들웨어를 제거할 수만 있으며 [글로벌 미들웨어](/docs/{{version}}/middleware#global-middleware)에는 적용되지 않습니다.

<a name="authorization-attributes"></a>
### 권한 부여 속성

정책을 통해 컨트롤러 액션을 인증하는 경우, `can` 미들웨어의 편리한 단축 옵션으로 `Authorize` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use App\Models\Post;
use Illuminate\Routing\Attributes\Controllers\Authorize;

class CommentController
{
    #[Authorize('create', [Comment::class, 'post'])]
    public function store(Post $post)
    {
        // ...
    }

    #[Authorize('delete', 'comment')]
    public function destroy(Comment $comment)
    {
        // ...
    }
}
```



첫 번째 인수는 허용하려는 권한입니다. 두 번째 인수는 정책에 전달되어야 하는 모델 클래스, 라우트 매개변수 또는 매개변수입니다.

<a name="resource-controllers"></a>
## 리소스 컨트롤러

애플리케이션의 각 Eloquent 모델을 "리소스"로 생각하면, 애플리케이션의 각 리소스에 대해 동일한 작업 집합을 수행하는 것이 일반적입니다. 예를 들어, 애플리케이션에 `Photo` 모델과 `Movie` 모델이 있다고 가정해 봅시다. 사용자가 이러한 리소스를 생성, 읽기, 업데이트 또는 삭제할 가능성이 높습니다.

이러한 일반적인 사용 사례 때문에 Laravel 리소스 라우팅은 컨트롤러에 단일 코드 라인으로 일반적인 생성, 읽기, 업데이트 및 삭제("CRUD") 라우트를 할당합니다. 시작하려면, 이러한 작업을 처리할 컨트롤러를 빠르게 생성하기 위해 `make:controller` Artisan 명령의 `--resource` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --resource
```



이 명령은 `app/Http/Controllers/PhotoController.php`에 컨트롤러를 생성합니다. 컨트롤러는 사용 가능한 각 리소스 작업에 대한 메서드를 포함합니다. 그 다음, 컨트롤러를 가리키는 리소스 라우트를 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class);
```



이 하나의 라우트 선언은 리소스에 대한 다양한 액션을 처리하기 위해 여러 라우트를 생성합니다. 생성된 컨트롤러는 이미 이러한 각 액션에 대한 메서드가 스텁으로 준비되어 있습니다. 애플리케이션의 라우트를 빠르게 확인하고 싶다면 언제든지 `route:list` Artisan 명령을 실행하면 됩니다.

배열을 `resources` 메서드에 전달하여 여러 리소스 컨트롤러를 한 번에 등록할 수도 있습니다:

```php
Route::resources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```



`softDeletableResources` 메서드는 모두 `withTrashed` 메서드를 사용하는 많은 리소스 컨트롤러를 등록합니다:

```php
Route::softDeletableResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```



<a name="actions-handled-by-resource-controllers"></a>
#### Actions Handled by Resource Controllers

<div class="overflow-auto">

| Verb      | URI                    | Action  | Route Name     |
| --------- | ---------------------- | ------- | -------------- |
| GET       | `/photos`              | index   | photos.index   |
| GET       | `/photos/create`       | create  | photos.create  |
| POST      | `/photos`              | store   | photos.store   |
| GET       | `/photos/{photo}`      | show    | photos.show    |
| GET       | `/photos/{photo}/edit` | edit    | photos.edit    |
| PUT/PATCH | `/photos/{photo}`      | update  | photos.update  |
| DELETE    | `/photos/{photo}`      | destroy | photos.destroy |

</div>

<a name="customizing-missing-model-behavior"></a>
#### Customizing Missing Model Behavior

Typically, a 404 HTTP response will be generated if an implicitly bound resource model is not found. However, you may customize this behavior by calling the `missing` method when defining your resource route. The `missing` method accepts a closure that will be invoked if an implicitly bound model cannot be found for any of the resource's routes:

```php
use App\Http\Controllers\PhotoController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Redirect;

Route::resource('photos', PhotoController::class)
    ->missing(function (Request $request) {
        return Redirect::route('photos.index');
    });
```



<a name="soft-deleted-models"></a>
#### 소프트 삭제된 모델

일반적으로, 암묵적 모델 바인딩은 [소프트 삭제됨](/docs/{{version}}/eloquent#soft-deleting) 모델을 가져오지 않으며, 대신 404 HTTP 응답을 반환합니다. 그러나 리소스 라우트를 정의할 때 `withTrashed` 메서드를 호출하여 프레임워크가 소프트 삭제된 모델을 허용하도록 지시할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->withTrashed();
```



인수 없이 `withTrashed`를 호출하면 `show`, `edit` 및 `update` 리소스 경로에 대해 소프트 삭제된 모델이 허용됩니다. `withTrashed` 메서드에 배열을 전달하여 이러한 경로의 하위 집합을 지정할 수 있습니다:

```php
Route::resource('photos', PhotoController::class)->withTrashed(['show']);
```



<a name="specifying-the-resource-model"></a>
#### 리소스 모델 지정하기

[라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 사용하고 있고 리소스 컨트롤러의 메서드가 모델 인스턴스를 타입 힌트하도록 하려면, 컨트롤러를 생성할 때 `--model` 옵션을 사용할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource
```



<a name="generating-form-requests"></a>
#### 폼 요청 생성

리소스 컨트롤러를 생성할 때 `--requests` 옵션을 제공하면 Artisan에게 컨트롤러의 저장 및 업데이트 메서드용 [폼 요청 클래스](/docs/{{version}}/validation#form-request-validation)를 생성하도록 지시할 수 있습니다:

```shell
php artisan make:controller PhotoController --model=Photo --resource --requests
```



<a name="restful-partial-resource-routes"></a>
### 부분 리소스 라우트

리소스 라우트를 선언할 때, 전체 기본 액션 세트 대신 컨트롤러가 처리해야 할 액션의 일부만 지정할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->only([
    'index', 'show'
]);

Route::resource('photos', PhotoController::class)->except([
    'create', 'store', 'update', 'destroy'
]);
```



<a name="api-resource-routes"></a>
#### API 리소스 경로

API에서 사용될 리소스 경로를 선언할 때, 일반적으로 `create` 및 `edit`와 같은 HTML 템플릿을 제공하는 경로는 제외하고자 합니다. 편리하게도, `apiResource` 메서드를 사용하여 이 두 경로를 자동으로 제외할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::apiResource('photos', PhotoController::class);
```



배열을 `apiResources` 메서드에 전달하여 여러 API 리소스 컨트롤러를 한 번에 등록할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;
use App\Http\Controllers\PostController;

Route::apiResources([
    'photos' => PhotoController::class,
    'posts' => PostController::class,
]);
```



`create` 또는 `edit` 메서드를 포함하지 않는 API 리소스 컨트롤러를 빠르게 생성하려면 `make:controller` 명령을 실행할 때 `--api` 스위치를 사용하십시오:

```shell
php artisan make:controller PhotoController --api
```



<a name="restful-nested-resources"></a>
### 중첩 리소스

때때로 중첩된 리소스에 대한 경로를 정의해야 할 때가 있습니다. 예를 들어, 사진 리소스에는 사진에 첨부될 수 있는 여러 댓글이 있을 수 있습니다. 리소스 컨트롤러를 중첩하려면 경로 선언에서 "점(dot)" 표기법을 사용할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class);
```



이 경로는 다음과 같은 URI로 접근할 수 있는 중첩된 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment}
```



<a name="scoping-nested-resources"></a>
#### 중첩 리소스 범위 지정

Laravel의 [암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 중첩 바인딩의 범위를 자동으로 지정하여, 해결된 자식 모델이 부모 모델에 속하는지 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정을 활성화하고, Laravel에게 자식 리소스를 검색할 때 사용할 필드를 지정할 수 있습니다. 이를 달성하는 방법에 대한 자세한 내용은 [리소스 라우트 범위 지정](#restful-scoping-resource-routes) 문서를 참조하십시오.

<a name="shallow-nesting"></a>
#### 얕은 중첩

종종 자식 ID가 이미 고유 식별자이므로 URI 내에서 부모와 자식 ID를 모두 포함할 필요는 없습니다. URI 세그먼트에서 자동 증가하는 기본 키와 같은 고유 식별자를 사용하여 모델을 식별할 때, "얕은 중첩"을 사용할 수 있습니다:

```php
use App\Http\Controllers\CommentController;

Route::resource('photos.comments', CommentController::class)->shallow();
```



이 라우트 정의는 다음 라우트를 정의합니다:

<div class="overflow-auto">

| 동사      | URI                               | 액션  | 라우트 이름             |
| --------- | --------------------------------- | ----- | ---------------------- |
| GET       | `/photos/{photo}/comments`        | index   | photos.comments.index  |
| GET       | `/photos/{photo}/comments/create` | create  | photos.comments.create |
| POST      | `/photos/{photo}/comments`        | store   | photos.comments.store  |
| GET       | `/comments/{comment}`             | show    | comments.show          |
| GET       | `/comments/{comment}/edit`        | edit    | comments.edit          |
| PUT/PATCH | `/comments/{comment}`             | update  | comments.update        |
| DELETE    | `/comments/{comment}`             | destroy | comments.destroy       |

</div>

<a name="restful-naming-resource-routes"></a>
### 리소스 라우트 이름 지정

기본적으로 모든 리소스 컨트롤러 액션에는 라우트 이름이 있으며, 원하는 라우트 이름으로 `names` 배열을 전달하여 이 이름들을 재정의할 수 있습니다:

```php
use App\Http\Controllers\PhotoController;

Route::resource('photos', PhotoController::class)->names([
    'create' => 'photos.build'
]);
```



<a name="restful-naming-resource-route-parameters"></a>
### 리소스 경로 매개변수 이름 지정

기본적으로, `Route::resource`는 리소스 이름의 '단수형'을 기준으로 리소스 경로의 매개변수를 생성합니다. 리소스별로 이를 쉽게 재정의할 수 있으며, `parameters` 메서드를 사용하면 됩니다. `parameters` 메서드에 전달되는 배열은 리소스 이름과 매개변수 이름의 연관 배열이어야 합니다:

```php
use App\Http\Controllers\AdminUserController;

Route::resource('users', AdminUserController::class)->parameters([
    'users' => 'admin_user'
]);
```



위의 예시는 리소스의 `show` 경로에 대해 다음 URI를 생성합니다:

```text
/users/{admin_user}
```



<a name="restful-scoping-resource-routes"></a>
### 리소스 경로 범위 지정

Laravel의 [범위 지정 암시적 모델 바인딩](/docs/{{version}}/routing#implicit-model-binding-scoping) 기능은 중첩된 바인딩을 자동으로 범위 지정할 수 있어, 해결된 자식 모델이 부모 모델에 속하는지 확인할 수 있습니다. 중첩 리소스를 정의할 때 `scoped` 메서드를 사용하면 자동 범위 지정을 활성화하고 자식 리소스를 어떤 필드로 조회할지 Laravel에 지시할 수 있습니다:

```php
use App\Http\Controllers\PhotoCommentController;

Route::resource('photos.comments', PhotoCommentController::class)->scoped([
    'comment' => 'slug',
]);
```



이 경로는 다음과 같은 URI로 액세스할 수 있는 범위가 지정된 중첩 리소스를 등록합니다:

```text
/photos/{photo}/comments/{comment:slug}
```



Laravel에서 사용자 정의 키를 가진 암시적 바인딩을 중첩 경로 매개변수로 사용할 때, Laravel은 부모의 관계 이름을 추측하는 규칙을 사용하여 중첩 모델을 검색하도록 쿼리를 자동으로 범위 지정합니다. 이 경우, `Photo` 모델이 `Comment` 모델을 검색하는 데 사용할 수 있는 `comments`라는 관계(경로 매개변수 이름의 복수형)를 가진 것으로 간주됩니다.

<a name="restful-localizing-resource-uris"></a>
### 자원 URI 지역화

기본적으로 `Route::resource`는 영어 동사와 복수 규칙을 사용하여 자원 URI를 생성합니다. `create` 및 `edit` 동작 동사를 지역화해야 하는 경우, `Route::resourceVerbs` 메서드를 사용할 수 있습니다. 이는 애플리케이션의 `App\Providers\AppServiceProvider` 내에서 `boot` 메서드 시작 부분에서 수행할 수 있습니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Route::resourceVerbs([
        'create' => 'crear',
        'edit' => 'editar',
    ]);
}
```



라라벨의 복수화기는 [여러 다른 언어를 지원하며, 필요에 따라 구성할 수 있습니다](/docs/{{version}}/localization#pluralization-language). 동사와 복수화 언어가 맞춤 설정되면, `Route::resource('publicacion', PublicacionController::class)`와 같은 리소스 라우트 등록은 다음과 같은 URI를 생성합니다:

```text
/publicacion/crear

/publicacion/{publicaciones}/editar
```



<a name="restful-supplementing-resource-controllers"></a>
### 리소스 컨트롤러 보충

리소스 컨트롤러에 기본 리소스 경로 외에 추가 경로를 추가해야 하는 경우, `Route::resource` 메서드를 호출하기 전에 해당 경로를 정의해야 합니다. 그렇지 않으면 `resource` 메서드에 의해 정의된 경로가 의도치 않게 보충 경로보다 우선될 수 있습니다:

```php
use App\Http\Controller\PhotoController;

Route::get('/photos/popular', [PhotoController::class, 'popular']);
Route::resource('photos', PhotoController::class);
```



> [!NOTE]
> 컨트롤러를 집중적으로 유지하는 것을 기억하세요. 일반적인 리소스 액션 집합 외에 메서드가 필요할 경우가 반복된다면, 컨트롤러를 두 개의 더 작은 컨트롤러로 나누는 것을 고려해보세요.

<a name="singleton-resource-controllers"></a>
### 싱글톤 리소스 컨트롤러

때때로, 애플리케이션에는 단일 인스턴스만 가질 수 있는 리소스가 있습니다. 예를 들어, 사용자의 "프로필"은 편집하거나 업데이트할 수 있지만, 사용자는 하나 이상의 "프로필"을 가질 수 없습니다. 마찬가지로, 이미지에는 하나의 "썸네일"이 있을 수 있습니다. 이러한 리소스는 "싱글톤 리소스"라고 하며, 리소스의 인스턴스가 하나만 존재할 수 있음을 의미합니다. 이러한 시나리오에서는 "싱글톤" 리소스 컨트롤러를 등록할 수 있습니다:

```php
use App\Http\Controllers\ProfileController;
use Illuminate\Support\Facades\Route;

Route::singleton('profile', ProfileController::class);
```



위의 싱글톤 리소스 정의는 다음 경로들을 등록합니다. 볼 수 있듯이, 싱글톤 리소스에서는 "생성" 경로가 등록되지 않으며, 등록된 경로는 리소스의 인스턴스가 하나만 존재할 수 있기 때문에 식별자를 허용하지 않습니다:

<div class="overflow-auto">

| 동사      | URI             | 액션  | 경로 이름       |
| --------- | --------------- | ------ | -------------- |
| GET       | `/profile`      | show   | profile.show   |
| GET       | `/profile/edit` | edit   | profile.edit   |
| PUT/PATCH | `/profile`      | update | profile.update |

</div>

싱글톤 리소스는 또한 표준 리소스 안에 중첩될 수 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class);
```



이 예제에서, `photos` 리소스는 모든 [표준 리소스 경로](#actions-handled-by-resource-controllers)를 받게 됩니다; 그러나 `thumbnail` 리소스는 다음과 같은 경로를 가진 싱글톤 리소스가 됩니다:

<div class="overflow-auto">

| 동사      | URI                              | 동작 | 경로 이름              |
| --------- | -------------------------------- | ------ | ----------------------- |
| GET       | `/photos/{photo}/thumbnail`      | show   | photos.thumbnail.show   |
| GET       | `/photos/{photo}/thumbnail/edit` | edit   | photos.thumbnail.edit   |
| PUT/PATCH | `/photos/{photo}/thumbnail`      | update | photos.thumbnail.update |

</div>

<a name="creatable-singleton-resources"></a>
#### 생성 가능한 싱글톤 리소스

때때로, 싱글톤 리소스에 대해 생성 및 저장 경로를 정의하고 싶을 때가 있습니다. 이를 달성하기 위해, 싱글톤 리소스 경로를 등록할 때 `creatable` 메서드를 호출할 수 있습니다:

```php
Route::singleton('photos.thumbnail', ThumbnailController::class)->creatable();
```



이 예제에서는 다음 경로들이 등록됩니다. 볼 수 있듯이, 생성 가능한 싱글톤 리소스에 대해서는 `DELETE` 경로도 등록됩니다:

<div class="overflow-auto">

| 동사      | URI                                | 액션  | 경로 이름                     |
| --------- | ---------------------------------- | ------- | ----------------------------- |
| GET       | `/photos/{photo}/thumbnail/create` | 생성  | photos.thumbnail.create  |
| POST      | `/photos/{photo}/thumbnail`        | 저장   | photos.thumbnail.store   |
| GET       | `/photos/{photo}/thumbnail`        | 표시    | photos.thumbnail.show    |
| GET       | `/photos/{photo}/thumbnail/edit`   | 편집    | photos.thumbnail.edit    |
| PUT/PATCH | `/photos/{photo}/thumbnail`        | 업데이트  | photos.thumbnail.update  |
| DELETE    | `/photos/{photo}/thumbnail`        | 삭제     | photos.thumbnail.destroy |

</div>

싱글톤 리소스에 대해 `DELETE` 경로를 Laravel이 등록하도록 하면서 생성이나 저장 경로는 등록하지 않으려면, `destroyable` 메서드를 사용할 수 있습니다:

```php
Route::singleton(...)->destroyable();
```



<a name="api-singleton-resources"></a>
#### API 싱글톤 리소스

`apiSingleton` 메서드는 API를 통해 조작될 싱글톤 리소스를 등록하는 데 사용할 수 있으며, 따라서 `create` 및 `edit` 경로가 불필요하게 됩니다:

```php
Route::apiSingleton('profile', ProfileController::class);
```



물론, API 싱글톤 리소스는 또한 `creatable`일 수 있으며, 이는 리소스에 대해 `store` 및 `destroy` 경로를 등록합니다:

```php
Route::apiSingleton('photos.thumbnail', ProfileController::class)->creatable();
```

<a name="middleware-and-resource-controllers"></a>
### 미들웨어 및 리소스 컨트롤러

Laravel은 `middleware`, `middlewareFor`, `withoutMiddlewareFor` 메서드를 사용하여 모든 리소스 경로의 메서드, 또는 특정 메서드에만 미들웨어를 할당할 수 있습니다. 이 메서드들은 각 리소스 액션에 적용되는 미들웨어를 세밀하게 제어할 수 있게 합니다.

#### 모든 메서드에 미들웨어 적용하기

리소스 또는 싱글톤 리소스 경로에서 생성된 모든 경로에 미들웨어를 할당하려면 `middleware` 메서드를 사용할 수 있습니다:

```php
Route::resource('users', UserController::class)
    ->middleware(['auth', 'verified']);

Route::singleton('profile', ProfileController::class)
    ->middleware('auth');
```



#### 특정 메서드에 미들웨어 적용

주어진 리소스 컨트롤러의 하나 이상의 특정 메서드에 미들웨어를 할당하려면 `middlewareFor` 메서드를 사용할 수 있습니다:

```php
Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], 'auth');

Route::resource('users', UserController::class)
    ->middlewareFor('show', 'auth')
    ->middlewareFor('update', 'auth');

Route::apiResource('users', UserController::class)
    ->middlewareFor(['show', 'update'], ['auth', 'verified']);
```



`middlewareFor` 방법은 싱글톤 및 API 싱글톤 리소스 컨트롤러와 함께 사용할 수도 있습니다:

```php
Route::singleton('profile', ProfileController::class)
    ->middlewareFor('show', 'auth');

Route::apiSingleton('profile', ProfileController::class)
    ->middlewareFor(['show', 'update'], 'auth');
```



#### 특정 메서드에서 미들웨어 제외하기

리소스 컨트롤러의 특정 메서드에서 미들웨어를 제외하려면 `withoutMiddlewareFor` 메서드를 사용할 수 있습니다:

```php
Route::middleware(['auth', 'verified', 'subscribed'])->group(function () {
    Route::resource('users', UserController::class)
        ->withoutMiddlewareFor('index', ['auth', 'verified'])
        ->withoutMiddlewareFor(['create', 'store'], 'verified')
        ->withoutMiddlewareFor('destroy', 'subscribed');
});
```



<a name="dependency-injection-and-controllers"></a>
## 의존성 주입과 컨트롤러

<a name="constructor-injection"></a>
#### 생성자 주입

Laravel [서비스 컨테이너](/docs/{{version}}/container)는 모든 Laravel 컨트롤러를 해결하는 데 사용됩니다. 그 결과, 컨트롤러의 생성자에서 필요할 수 있는 모든 의존성을 타입 힌트로 지정할 수 있습니다. 선언된 의존성은 자동으로 해결되어 컨트롤러 인스턴스에 주입됩니다:

```php
<?php

namespace App\Http\Controllers;

use App\Repositories\UserRepository;

class UserController extends Controller
{
    /**
     * Create a new controller instance.
     */
    public function __construct(
        protected UserRepository $users,
    ) {}
}
```



<a name="method-injection"></a>
#### 메소드 주입

생성자 주입 외에도 컨트롤러의 메소드에 의존성을 타입 힌트로 줄 수 있습니다. 메소드 주입의 일반적인 사용 사례는 `Illuminate\Http\Request` 인스턴스를 컨트롤러 메소드에 주입하는 것입니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Store a new user.
     */
    public function store(Request $request): RedirectResponse
    {
        $name = $request->name;

        // Store the user...

        return redirect('/users');
    }
}
```



컨트롤러 메서드가 라우트 매개변수에서 입력을 기대하는 경우 다른 의존성 뒤에 라우트 인수를 나열하십시오. 예를 들어, 라우트가 다음과 같이 정의된 경우:

```php
use App\Http\Controllers\UserController;

Route::put('/user/{id}', [UserController::class, 'update']);
```



다음과 같이 컨트롤러 메서드를 정의하여 `Illuminate\Http\Request`를 타입 힌트하고 `id` 매개변수에 접근할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;

class UserController extends Controller
{
    /**
     * Update the given user.
     */
    public function update(Request $request, string $id): RedirectResponse
    {
        // Update the user...

        return redirect('/users');
    }
}
```
{% endraw %}
