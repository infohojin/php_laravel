---
layout: docs
title: "Eloquent: API Resources"
---

{% raw %}
---
layout: docs
title: "Eloquent: API Resources"
---

# Eloquent: API Resources

- [Introduction](#introduction)
- [Generating Resources](#generating-resources)
- [Concept Overview](#concept-overview)
    - [Resource Collections](#resource-collections)
- [Writing Resources](#writing-resources)
    - [Data Wrapping](#data-wrapping)
    - [Pagination](#pagination)
    - [Conditional Attributes](#conditional-attributes)
    - [Conditional Relationships](#conditional-relationships)
    - [Adding Meta Data](#adding-meta-data)
- [JSON:API Resources](#jsonapi-resources)
    - [Generating JSON:API Resources](#generating-jsonapi-resources)
    - [Defining Attributes](#defining-jsonapi-attributes)
    - [Defining Relationships](#defining-jsonapi-relationships)
    - [Resource Type and ID](#jsonapi-resource-type-and-id)
    - [Sparse Fieldsets and Includes](#jsonapi-sparse-fieldsets-and-includes)
    - [Links and Meta](#jsonapi-links-and-meta)
- [Resource Responses](#resource-responses)

<a name="introduction"></a>
## Introduction

When building an API, you may need a transformation layer that sits between your Eloquent models and the JSON responses that are actually returned to your application's users. For example, you may wish to display certain attributes for a subset of users and not others, or you may wish to always include certain relationships in the JSON representation of your models. Eloquent's resource classes allow you to expressively and easily transform your models and model collections into JSON.

Of course, you may always convert Eloquent models or collections to JSON using their `toJson` methods; however, Eloquent resources provide more granular and robust control over the JSON serialization of your models and their relationships.

<a name="generating-resources"></a>
## Generating Resources

To generate a resource class, you may use the `make:resource` Artisan command. By default, resources will be placed in the `app/Http/Resources` directory of your application. Resources extend the `Illuminate\Http\Resources\Json\JsonResource` class:

```shell
php artisan make:resource UserResource
```



<a name="generating-resource-collections"></a>
#### 리소스 컬렉션

개별 모델을 변환하는 리소스를 생성하는 것 외에도, 모델 컬렉션을 변환하는 역할을 하는 리소스를 생성할 수 있습니다. 이렇게 하면 JSON 응답에 해당 리소스의 전체 컬렉션과 관련된 링크 및 기타 메타 정보를 포함할 수 있습니다.

리소스 컬렉션을 생성하려면, 리소스를 생성할 때 `--collection` 플래그를 사용해야 합니다. 또는 리소스 이름에 `Collection`라는 단어를 포함하면 Laravel에 컬렉션 리소스를 생성해야 한다고 알릴 수 있습니다. 컬렉션 리소스는 `Illuminate\Http\Resources\Json\ResourceCollection` 클래스를 확장합니다:

```shell
php artisan make:resource User --collection

php artisan make:resource UserCollection
```



<a name="concept-overview"></a>
## 개념 개요

> [!NOTE]
> 이것은 리소스와 리소스 컬렉션에 대한 높은 수준의 개요입니다. 리소스가 제공하는 맞춤화와 강력한 기능을 더 깊이 이해하려면 이 문서의 다른 섹션도 읽어보는 것이 좋습니다.

리소스를 작성할 때 사용할 수 있는 모든 옵션을 살펴보기 전에, 먼저 Laravel 내에서 리소스가 어떻게 사용되는지 높은 수준에서 살펴보겠습니다. 리소스 클래스는 JSON 구조로 변환해야 하는 단일 모델을 나타냅니다. 예를 들어, 다음은 간단한 `UserResource` 리소스 클래스입니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```



모든 리소스 클래스는 `toArray` 메서드를 정의하며, 이 메서드는 리소스가 라우트 또는 컨트롤러 메서드의 응답으로 반환될 때 JSON으로 변환되어야 하는 속성 배열을 반환합니다.

`$this` 변수를 통해 모델 속성에 직접 접근할 수 있다는 점에 유의하세요. 이는 리소스 클래스가 편리한 접근을 위해 속성과 메서드 접근을 자동으로 기본 모델로 프록시하기 때문입니다. 리소스가 정의되면 라우트 또는 컨트롤러에서 반환될 수 있습니다. 이 리소스는 생성자를 통해 기본 모델 인스턴스를 받습니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return new UserResource(User::findOrFail($id));
});
```



편의를 위해, 프레임워크 규칙을 사용하여 모델의 기본 리소스를 자동으로 발견하는 `toResource` 메서드를 사용할 수 있습니다:

```php
return User::findOrFail($id)->toResource();
```



`toResource` 메서드를 호출할 때, Laravel은 모델의 이름과 일치하며 선택적으로 `Resource`로 끝나는 리소스를 모델의 네임스페이스와 가장 가까운 `Http\Resources` 네임스페이스 내에서 찾으려고 시도합니다.

리소스 클래스가 이 명명 규칙을 따르지 않거나 다른 네임스페이스에 있는 경우, `UseResource` 속성을 사용하여 모델의 기본 리소스를 지정할 수 있습니다.

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserResource;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResource;

#[UseResource(CustomUserResource::class)]
class User extends Model
{
    // ...
}
```



또는 `toResource` 메서드에 전달하여 리소스 클래스를 지정할 수 있습니다:

```php
return User::findOrFail($id)->toResource(CustomUserResource::class);
```



<a name="resource-collections"></a>
### 리소스 모음

리소스 모음이나 페이지가 나뉜 응답을 반환하는 경우, 라우트나 컨트롤러에서 리소스 인스턴스를 생성할 때 리소스 클래스에서 제공하는 `collection` 메서드를 사용해야 합니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all());
});
```



또는 편의를 위해, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있으며, 이 메서드는 프레임워크 규칙을 사용하여 모델의 기본 리소스 컬렉션을 자동으로 찾습니다:

```php
return User::all()->toResourceCollection();
```



`toResourceCollection` 메서드를 호출할 때, Laravel은 모델의 이름과 일치하며 `Http\Resources` 네임스페이스 내에서 모델의 네임스페이스에 가장 가까운 위치에 `Collection`로 끝나는 리소스 컬렉션을 찾으려고 시도합니다.

만약 리소스 컬렉션 클래스가 이 명명 규칙을 따르지 않거나 다른 네임스페이스에 위치한 경우, `UseResourceCollection` 속성을 사용하여 모델에 대한 기본 리소스 컬렉션을 지정할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Http\Resources\CustomUserCollection;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Attributes\UseResourceCollection;

#[UseResourceCollection(CustomUserCollection::class)]
class User extends Model
{
    // ...
}
```



또는 `toResourceCollection` 메서드에 전달하여 리소스 컬렉션 클래스를 지정할 수 있습니다:

```php
return User::all()->toResourceCollection(CustomUserCollection::class);
```



<a name="custom-resource-collections"></a>
#### 사용자 정의 리소스 컬렉션

기본적으로 리소스 컬렉션은 컬렉션과 함께 반환해야 할 수 있는 사용자 정의 메타 데이터를 추가할 수 없습니다. 리소스 컬렉션 응답을 사용자 정의하려면, 컬렉션을 표현할 전용 리소스를 생성할 수 있습니다:

```shell
php artisan make:resource UserCollection
```



리소스 컬렉션 클래스가 생성되면, 응답과 함께 포함되어야 하는 메타데이터를 쉽게 정의할 수 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<int|string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```



리소스 컬렉션을 정의한 후에는 라우트나 컨트롤러에서 반환될 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```



또는 편의를 위해 Eloquent 컬렉션의 `toResourceCollection` 방법을 사용할 수 있는데, 이 방법은 프레임워크 관습을 사용하여 모델의 기본 자원 컬렉션을 자동으로 발견합니다:

```php
return User::all()->toResourceCollection();
```



`toResourceCollection` 메서드를 호출할 때, Laravel은 모델의 이름과 일치하고 모델의 네임스페이스에서 가장 가까운 `Http\Resources` 네임스페이스 내에 `Collection`가 접미사로 붙은 리소스 컬렉션을 찾으려고 시도합니다.

<a name="preserving-collection-keys"></a>
#### 컬렉션 키 보존

라우트에서 리소스 컬렉션을 반환할 때, Laravel은 컬렉션의 키를 숫자 순서로 재설정합니다. 그러나 리소스 클래스에서 컬렉션의 원래 키를 보존해야 하는지 여부를 나타내는 `PreserveKeys` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Attributes\PreserveKeys;
use Illuminate\Http\Resources\Json\JsonResource;

#[PreserveKeys]
class UserResource extends JsonResource
{
    // ...
}
```



`preserveKeys` 속성이 `true`로 설정되면, 컬렉션이 라우트나 컨트롤러에서 반환될 때 컬렉션 키가 유지됩니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/users', function () {
    return UserResource::collection(User::all()->keyBy->id);
});
```



<a name="customizing-the-underlying-resource-class"></a>
#### 기본 리소스 클래스 사용자 정의

일반적으로, 리소스 컬렉션의 `$this->collection` 속성은 컬렉션의 각 항목을 단일 리소스 클래스에 매핑한 결과로 자동으로 채워집니다. 단일 리소스 클래스는 컬렉션의 클래스 이름에서 클래스 이름의 끝 `Collection` 부분을 제거한 것으로 간주됩니다. 또한, 개인 취향에 따라 단일 리소스 클래스에는 `Resource`가 접미사로 붙을 수도 있고 붙지 않을 수도 있습니다.

예를 들어, `UserCollection`는 주어진 사용자 인스턴스를 `UserResource` 리소스로 매핑하려고 시도합니다. 이 동작을 사용자 정의하려면, 리소스 컬렉션에서 `Collects` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Attributes\Collects;
use Illuminate\Http\Resources\Json\ResourceCollection;

#[Collects(Member::class)]
class UserCollection extends ResourceCollection
{
    // ...
}
```



<a name="writing-resources"></a>
## 작성 자료

> [!NOTE]
> [개념 개요](#concept-overview)를 읽지 않았다면, 이 문서를 진행하기 전에 꼭 읽어보는 것이 강력히 권장됩니다.

자료는 주어진 모델을 배열로 변환하기만 하면 됩니다. 따라서 각 자료에는 모델의 속성을 애플리케이션의 경로나 컨트롤러에서 반환할 수 있는 API 친화적인 배열로 변환하는 `toArray` 메서드가 포함되어 있습니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'email' => $this->email,
            'created_at' => $this->created_at,
            'updated_at' => $this->updated_at,
        ];
    }
}
```



리소스가 정의되면, 경로나 컨트롤러에서 직접 반환될 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toUserResource();
});
```



<a name="relationships"></a>
#### 관계

응답에 관련 리소스를 포함하고 싶다면, 리소스의 `toArray` 메서드가 반환하는 배열에 추가할 수 있습니다. 이 예제에서는 `PostResource` 리소스의 `collection` 메서드를 사용하여 사용자의 블로그 게시물을 리소스 응답에 추가합니다:

```php
use App\Http\Resources\PostResource;
use Illuminate\Http\Request;

/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->posts),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```



> [!NOTE]
> 이미 로드된 경우에만 관계를 포함하고 싶다면, [조건부 관계](#conditional-relationships)에 대한 문서를 참고하세요.

<a name="writing-resource-collections"></a>
#### 리소스 컬렉션

리소스가 단일 모델을 배열로 변환하는 반면, 리소스 컬렉션은 모델 컬렉션을 배열로 변환합니다. 그러나 모든 Eloquent 모델 컬렉션은 즉석에서 "임시" 리소스 컬렉션을 생성하는 `toResourceCollection` 메서드를 제공하므로, 각 모델마다 리소스 컬렉션 클래스를 정의하는 것이 절대적으로 필요한 것은 아닙니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::all()->toResourceCollection();
});
```



그러나 컬렉션과 함께 반환되는 메타 데이터를 사용자 정의해야 하는 경우, 자체 리소스 컬렉션을 정의하는 것이 필요합니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'links' => [
                'self' => 'link-value',
            ],
        ];
    }
}
```



단일 리소스와 마찬가지로, 리소스 컬렉션은 라우트나 컨트롤러에서 직접 반환될 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::all());
});
```



또는 편의를 위해, Eloquent 컬렉션의 `toResourceCollection` 메서드를 사용할 수 있으며, 이 메서드는 프레임워크 규칙을 사용하여 모델의 기본 리소스 컬렉션을 자동으로 발견합니다:

```php
return User::all()->toResourceCollection();
```



`toResourceCollection` 메서드를 호출할 때, Laravel은 모델 이름과 일치하고 모델의 네임스페이스에 가장 가까운 `Http\Resources` 네임스페이스 내에서 `Collection`가 접미사로 붙은 리소스 컬렉션을 찾으려고 시도합니다.

<a name="data-wrapping"></a>
### 데이터 래핑

기본적으로, 리소스 응답이 JSON으로 변환될 때 가장 바깥쪽 리소스는 `data` 키로 래핑됩니다. 예를 들어, 일반적인 리소스 컬렉션 응답은 다음과 같이 보입니다:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ]
}
```



가장 바깥쪽 리소스의 래핑을 비활성화하려면, 기본 `Illuminate\Http\Resources\Json\JsonResource` 클래스에서 `withoutWrapping` 메서드를 호출해야 합니다. 일반적으로 이 메서드는 `AppServiceProvider` 또는 애플리케이션의 모든 요청 시 로드되는 다른 [서비스 제공자](/docs/{{version}}/providers)에서 호출해야 합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\ServiceProvider;

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
        JsonResource::withoutWrapping();
    }
}
```



> [!WARNING]
> `withoutWrapping` 메서드는 최상위 응답에만 영향을 미치며 사용자가 자신의 리소스 컬렉션에 수동으로 추가한 `data` 키를 제거하지 않습니다.

<a name="wrapping-nested-resources"></a>
#### 중첩 리소스 래핑

리소스의 관계가 어떻게 래핑될지는 완전히 자유롭게 결정할 수 있습니다. 모든 리소스 컬렉션을 중첩 여부와 상관없이 `data` 키로 래핑하고 싶다면, 각 리소스에 대해 별도의 리소스 컬렉션 클래스를 정의하고 컬렉션을 `data` 키 내에 반환해야 합니다.

이로 인해 최상위 리소스가 두 개의 `data` 키로 래핑될까 걱정될 수 있습니다. 걱정하지 마세요. Laravel은 리소스가 실수로 두 번 래핑되는 것을 절대 허용하지 않으므로, 변환하는 리소스 컬렉션의 중첩 수준에 대해 신경 쓸 필요가 없습니다.

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class CommentsCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return ['data' => $this->collection];
    }
}
```



<a name="data-wrapping-and-pagination"></a>
#### 데이터 래핑 및 페이지네이션

리소스 응답을 통해 페이지가 나뉜 컬렉션을 반환할 때, Laravel은 `withoutWrapping` 메서드가 호출되었더라도 리소스 데이터를 `data` 키로 래핑합니다. 이는 페이지가 나뉜 응답이 항상 페이지네이터 상태에 대한 정보를 담고 있는 `meta` 및 `links` 키를 포함하기 때문입니다:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ],
    "links":{
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```



<a name="pagination"></a>
### 페이지네이션

Laravel 페이징 객체를 리소스의 `collection` 메서드나 사용자 정의 리소스 컬렉션에 전달할 수 있습니다:

```php
use App\Http\Resources\UserCollection;
use App\Models\User;

Route::get('/users', function () {
    return new UserCollection(User::paginate());
});
```



또는 편의를 위해, 페이징 처리기의 `toResourceCollection` 메서드를 사용할 수 있으며, 이 메서드는 프레임워크 규칙을 사용하여 페이징된 모델의 기본 리소스 컬렉션을 자동으로 발견합니다:

```php
return User::paginate()->toResourceCollection();
```



페이지네이션된 응답은 항상 페이지네이터의 상태에 관한 정보를 담은 `meta` 키와 `links`키를 포함합니다:

```json
{
    "data": [
        {
            "id": 1,
            "name": "Eladio Schroeder Sr.",
            "email": "therese28@example.com"
        },
        {
            "id": 2,
            "name": "Liliana Mayert",
            "email": "evandervort@example.com"
        }
    ],
    "links":{
        "first": "http://example.com/users?page=1",
        "last": "http://example.com/users?page=1",
        "prev": null,
        "next": null
    },
    "meta":{
        "current_page": 1,
        "from": 1,
        "last_page": 1,
        "path": "http://example.com/users",
        "per_page": 15,
        "to": 10,
        "total": 10
    }
}
```



<a name="customizing-the-pagination-information"></a>
#### 페이지네이션 정보 사용자 정의

페이지네이션 응답의 `links` 또는 `meta` 키에 포함된 정보를 사용자 정의하고 싶다면, 리소스에서 `paginationInformation` 메서드를 정의할 수 있습니다. 이 메서드는 `$paginated` 데이터와 `$default` 정보 배열을 받게 되며, 이 배열은 `links` 및 `meta` 키를 포함합니다:

```php
/**
 * Customize the pagination information for the resource.
 *
 * @param  \Illuminate\Http\Request  $request
 * @param  array  $paginated
 * @param  array  $default
 * @return array
 */
public function paginationInformation($request, $paginated, $default)
{
    $default['links']['custom'] = 'https://example.com';

    return $default;
}
```



<a name="conditional-attributes"></a>
### 조건부 속성

때때로 특정 조건이 충족될 경우에만 리소스 응답에 속성을 포함하고 싶을 수 있습니다. 예를 들어, 현재 사용자가 "관리자"인 경우에만 값을 포함하고 싶을 수 있습니다. Laravel은 이러한 상황에서 도움을 주는 다양한 헬퍼 메서드를 제공합니다. `when` 메서드는 조건부로 리소스 응답에 속성을 추가하는 데 사용될 수 있습니다:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'secret' => $this->when($request->user()->isAdmin(), 'secret-value'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```



이 예제에서 `secret` 키는 인증된 사용자의 `isAdmin` 메서드가 `true`를 반환할 경우에만 최종 리소스 응답에 포함됩니다. 만약 메서드가 `false`를 반환하면, `secret` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다. `when` 메서드를 사용하면 배열을 구성할 때 조건문을 사용하지 않고도 리소스를 명확하게 정의할 수 있습니다.

`when` 메서드는 두 번째 인자로 클로저도 허용하며, 주어진 조건이 `true`인 경우에만 최종 값을 계산할 수 있습니다:

```php
'secret' => $this->when($request->user()->isAdmin(), function () {
    return 'secret-value';
}),
```



`whenHas` 방법은 실제로 기본 모델에 속성이 존재하는 경우 해당 속성을 포함하는 데 사용할 수 있습니다:

```php
'name' => $this->whenHas('name'),
```



또한, 속성이 null이 아닌 경우 자원 응답에 속성을 포함하기 위해 `whenNotNull` 방법을 사용할 수 있습니다:

```php
'name' => $this->whenNotNull($this->name),
```



<a name="merging-conditional-attributes"></a>
#### 조건부 속성 병합

때때로 동일한 조건에 따라 리소스 응답에만 포함되어야 하는 여러 속성이 있을 수 있습니다. 이 경우 `mergeWhen` 메서드를 사용하여 주어진 조건이 `true`일 때만 속성을 응답에 포함시킬 수 있습니다:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        $this->mergeWhen($request->user()->isAdmin(), [
            'first-secret' => 'value',
            'second-secret' => 'value',
        ]),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```



Again, if the given condition is `false`, these attributes will be removed from the resource response before it is sent to the client.

> [!WARNING]
> The `mergeWhen` method should not be used within arrays that mix string and numeric keys. Furthermore, it should not be used within arrays with numeric keys that are not ordered sequentially.

<a name="conditional-relationships"></a>
### Conditional Relationships

In addition to conditionally loading attributes, you may conditionally include relationships on your resource responses based on if the relationship has already been loaded on the model. This allows your controller to decide which relationships should be loaded on the model and your resource can easily include them only when they have actually been loaded. Ultimately, this makes it easier to avoid "N+1" query problems within your resources.

The `whenLoaded` method may be used to conditionally load a relationship. In order to avoid unnecessarily loading relationships, this method accepts the name of the relationship instead of the relationship itself:

```php
use App\Http\Resources\PostResource;

/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts' => PostResource::collection($this->whenLoaded('posts')),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```



이 예에서, 관계가 로드되지 않은 경우, `posts` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

<a name="conditional-relationship-counts"></a>
#### 조건부 관계 수

관계를 조건부로 포함하는 것 외에도, 모델에서 관계의 수가 로드되었는지에 따라 리소스 응답에 관계 '수(counts)'를 조건부로 포함할 수 있습니다:

```php
new UserResource($user->loadCount('posts'));
```



`whenCounted` 메서드는 리소스 응답에 관계의 수를 조건부로 포함하는 데 사용할 수 있습니다. 이 메서드는 관계 수가 존재하지 않을 경우 속성을 불필요하게 포함하는 것을 피합니다:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'email' => $this->email,
        'posts_count' => $this->whenCounted('posts'),
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```



이 예제에서, `posts` 관계의 개수가 로드되지 않은 경우, `posts_count` 키는 클라이언트로 전송되기 전에 리소스 응답에서 제거됩니다.

`avg`, `sum`, `min`, `max`와 같은 다른 유형의 집계도 `whenAggregated` 메서드를 사용하여 조건부로 로드될 수 있습니다:

```php
'words_avg' => $this->whenAggregated('posts', 'words', 'avg'),
'words_sum' => $this->whenAggregated('posts', 'words', 'sum'),
'words_min' => $this->whenAggregated('posts', 'words', 'min'),
'words_max' => $this->whenAggregated('posts', 'words', 'max'),
```



<a name="conditional-pivot-information"></a>
#### 조건부 피벗 정보

리소스 응답에 관계 정보를 조건부로 포함하는 것 외에도, `whenPivotLoaded` 메서드를 사용하여 다대다 관계의 중간 테이블 데이터를 조건부로 포함할 수 있습니다. `whenPivotLoaded` 메서드는 첫 번째 인자로 피벗 테이블의 이름을 받습니다. 두 번째 인자는 모델에서 피벗 정보가 이용 가능할 경우 반환할 값을 반환하는 클로저여야 합니다:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoaded('role_user', function () {
            return $this->pivot->expires_at;
        }),
    ];
}
```



만약 당신의 관계가 [사용자 정의 중간 테이블 모델](/docs/{{version}}/eloquent-relationships#defining-custom-intermediate-table-models)을 사용하고 있다면, 중간 테이블 모델의 인스턴스를 첫 번째 인수로 `whenPivotLoaded` 메서드에 전달할 수 있습니다:

```php
'expires_at' => $this->whenPivotLoaded(new Membership, function () {
    return $this->pivot->expires_at;
}),
```



중간 테이블이 `pivot`가 아닌 다른 접근자를 사용하고 있다면, `whenPivotLoadedAs` 방식을 사용할 수 있습니다:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'name' => $this->name,
        'expires_at' => $this->whenPivotLoadedAs('subscription', 'role_user', function () {
            return $this->subscription->expires_at;
        }),
    ];
}
```



<a name="adding-meta-data"></a>
### 메타 데이터 추가

일부 JSON API 표준에서는 리소스 및 리소스 컬렉션 응답에 메타 데이터를 추가해야 합니다. 이는 종종 리소스나 관련 리소스에 대한 `links` 또는 리소스 자체에 대한 메타 데이터를 포함합니다. 리소스에 대한 추가 메타 데이터를 반환해야 하는 경우, `toArray` 메서드에 포함시킵니다. 예를 들어, 리소스 컬렉션을 변환할 때 `links` 정보를 포함할 수 있습니다:

```php
/**
 * Transform the resource into an array.
 *
 * @return array<string, mixed>
 */
public function toArray(Request $request): array
{
    return [
        'data' => $this->collection,
        'links' => [
            'self' => 'link-value',
        ],
    ];
}
```



리소스에서 추가 메타 데이터를 반환할 때, 페이징된 응답을 반환할 때 Laravel이 자동으로 추가하는 `links` 또는 `meta` 키를 실수로 덮어쓸 걱정을 전혀 하지 않아도 됩니다. 정의한 추가 `links`는 페이징을 제공하는 링크와 병합됩니다.

<a name="top-level-meta-data"></a>
#### 최상위 메타 데이터

때때로 리소스가 반환되는 최외곽 리소스일 때만 특정 메타 데이터를 포함하고 싶을 수 있습니다. 일반적으로 이는 응답 전체에 대한 메타 정보를 포함합니다. 이 메타 데이터를 정의하려면 리소스 클래스에 `with` 메서드를 추가하세요. 이 메서드는 리소스가 변환되는 최외곽 리소스일 때만 리소스 응답에 포함될 메타 데이터를 배열로 반환해야 합니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class UserCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return parent::toArray($request);
    }

    /**
     * Get additional data that should be returned with the resource array.
     *
     * @return array<string, mixed>
     */
    public function with(Request $request): array
    {
        return [
            'meta' => [
                'key' => 'value',
            ],
        ];
    }
}
```



<a name="adding-meta-data-when-constructing-resources"></a>
#### 리소스를 구성할 때 메타 데이터 추가

라우트나 컨트롤러에서 리소스 인스턴스를 구성할 때 최상위 데이터를 추가할 수도 있습니다. 모든 리소스에서 사용할 수 있는 `additional` 메서드는 리소스 응답에 추가해야 할 데이터 배열을 받습니다:

```php
return User::all()
    ->load('roles')
    ->toResourceCollection()
    ->additional(['meta' => [
        'key' => 'value',
    ]]);
```



<a name="jsonapi-resources"></a>
## JSON:API 리소스

Laravel은 [JSON:API 사양](https://jsonapi.org/)에 준수하는 응답을 생성하는 `JsonApiResource` 리소스 클래스를 제공합니다. 이 클래스는 표준 `JsonResource` 클래스를 확장하며, 리소스 객체 구조, 관계, 드문 필드셋, 포함, 지연 속성 평가를 자동으로 처리하고, `Content-Type` 헤더를 `application/vnd.api+json`로 설정합니다.

> [!NOTE]
> Laravel의 JSON:API 리소스는 응답의 직렬화를 처리합니다. 또한 필터와 정렬 같은 들어오는 JSON:API 쿼리 매개변수를 파싱해야 하는 경우, [Spatie의 Laravel Query Builder](https://spatie.be/docs/laravel-query-builder)가 훌륭한 보조 패키지입니다.

<a name="generating-jsonapi-resources"></a>
### JSON:API 리소스 생성

JSON:API 리소스를 생성하려면, `--json-api` 플래그를 사용하여 `make:resource` Artisan 명령어를 사용하십시오:

```shell
php artisan make:resource PostResource --json-api
```



생성된 클래스는 `Illuminate\Http\Resources\JsonApi\JsonApiResource`를 확장하고 정의할 `$attributes` 및 `$relationships` 속성을 포함합니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

class PostResource extends JsonApiResource
{
    /**
     * The resource's attributes.
     */
    public $attributes = [
        // ...
    ];

    /**
     * The resource's relationships.
     */
    public $relationships = [
        // ...
    ];
}
```



JSON:API 리소스는 표준 리소스처럼 라우트와 컨트롤러에서 반환될 수 있습니다:

```php
use App\Http\Resources\PostResource;
use App\Models\Post;

Route::get('/api/posts/{post}', function (Post $post) {
    return new PostResource($post);
});
```



또는 편의를 위해 모델의 `toResource` 방법을 사용할 수 있습니다:

```php
Route::get('/api/posts/{post}', function (Post $post) {
    return $post->toResource();
});
```



이것은 JSON:API 준수 응답을 생성합니다:

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World",
            "body": "This is my first post."
        }
    }
}
```



JSON:API 리소스 컬렉션을 반환하려면 `collection` 메서드 또는 `toResourceCollection` 편의 메서드를 사용하세요:

```php
return PostResource::collection(Post::all());

return Post::all()->toResourceCollection();
```



<a name="defining-jsonapi-attributes"></a>
### 속성 정의

JSON:API 리소스에 포함될 속성을 정의하는 방법은 두 가지가 있습니다.

가장 간단한 방법은 리소스에 `$attributes` 속성을 정의하는 것입니다. 속성 이름을 값으로 나열할 수 있으며, 이는 기본 모델에서 직접 읽어옵니다:

```php
public $attributes = [
    'title',
    'body',
    'created_at',
];
```



속성을 계산하는 데 비용이 많이 든다면, 속성이 실제로 응답에서 필요할 때만 평가되도록 `toAttributes`에서 클로저로 반환할 수 있습니다.

또는 리소스의 속성에 대한 완전한 제어를 위해, 리소스에서 `toAttributes` 메서드를 재정의할 수 있습니다:

```php
/**
 * Get the resource's attributes.
 *
 * @return array<string, mixed>
 */
public function toAttributes(Request $request): array
{
    return [
        'title' => $this->title,
        'body' => $this->body,
        'is_published' => fn () => $this->published_at !== null,
        'created_at' => $this->created_at,
        'updated_at' => $this->updated_at,
    ];
}
```



<a name="defining-jsonapi-relationships"></a>
### 관계 정의

JSON:API 리소스는 JSON:API 명세를 따르는 관계 정의를 지원합니다. 관계는 클라이언트가 `include` 쿼리 매개변수를 통해 요청할 때만 직렬화됩니다.

#### `$relationships` 속성

리소스에서 `$relationships` 속성을 통해 리소스의 포함 가능한 관계를 정의할 수 있습니다:

```php
public $relationships = [
    'author',
    'comments',
];
```



관계 이름을 값으로 나열할 때, Laravel은 해당 Eloquent 관계를 해결하고 적절한 리소스 클래스를 자동으로 발견합니다. 리소스 클래스를 명시적으로 지정해야 하는 경우, 관계를 키 / 클래스 쌍으로 정의할 수 있습니다:

```php
use App\Http\Resources\UserResource;

public $relationships = [
    'author' => UserResource::class,
    'comments',
];
```



또는 리소스에서 `toRelationships` 메서드를 재정의할 수 있습니다:

```php
/**
 * Get the resource's relationships.
 */
public function toRelationships(Request $request): array
{
    return [
        'author' => UserResource::class,
        'comments' => fn () => CommentResource::collection(
            $request->user()->is($this->resource)
                ? $this->comments
                : $this->comments->where('is_public', true),
        ),
    ];
}
```



클로저를 사용하면 관계 페이로드에 대한 더 많은 제어가 가능하면서도, 클라이언트가 요청할 때만 관계를 해결할 수 있습니다.

#### 관계 포함

클라이언트는 `include` 쿼리 매개변수를 사용하여 관련 리소스를 요청할 수 있습니다:```
GET /api/posts/1?include=author,comments
```



이것은 `relationships` 키에 리소스 식별자 객체를, 최상위 `included` 배열에 전체 리소스 객체를 포함하는 응답을 생성합니다:

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "relationships": {
            "author": {
                "data": {
                    "id": "1",
                    "type": "users"
                }
            },
            "comments": {
                "data": [
                    {
                        "id": "1",
                        "type": "comments"
                    }
                ]
            }
        }
    },
    "included": [
        {
            "id": "1",
            "type": "users",
            "attributes": {
                "name": "Taylor Otwell"
            }
        },
        {
            "id": "1",
            "type": "comments",
            "attributes": {
                "body": "Great post!"
            }
        }
    ]
}
```



중첩된 관계는 점 표기법을 사용하여 포함될 수 있습니다:```
GET /api/posts/1?include=comments.author
```



<a name="jsonapi-relationship-depth"></a>
#### 관계 깊이

기본적으로, 중첩 관계 포함은 최대 깊이로 제한됩니다. 일반적으로 애플리케이션의 서비스 공급자 중 하나에서 `maxRelationshipDepth` 메서드를 사용하여 이 제한을 사용자 정의할 수 있습니다:

```php
use Illuminate\Http\Resources\JsonApi\JsonApiResource;

JsonApiResource::maxRelationshipDepth(3);
```



<a name="jsonapi-resource-type-and-id"></a>
### 리소스 유형 및 ID

기본적으로, 리소스의 `type`는 리소스 클래스 이름에서 파생됩니다. 예를 들어, `PostResource`는 `posts` 유형을 생성하고 `BlogPostResource`는 `blog-posts`를 생성합니다. 리소스의 `id`는 모델의 기본 키에서 해결됩니다.

이 값을 사용자 정의해야 하는 경우, 리소스에서 `toType` 및 `toId` 메서드를 재정의할 수 있습니다:

```php
/**
 * Get the resource's type.
 */
public function toType(Request $request): string
{
    return 'articles';
}

/**
 * Get the resource's ID.
 */
public function toId(Request $request): string
{
    return (string) $this->uuid;
}
```



이는 리소스의 타입이 클래스 이름과 달라야 하는 경우, 예를 들어 `AuthorResource`가 `User` 모델을 감싸고 타입 `authors`를 출력해야 할 때 특히 유용합니다.

<a name="jsonapi-sparse-fieldsets-and-includes"></a>
### 드문 필드셋(Sparse Fieldsets)과 포함(Include)

JSON:API 리소스는 [드문 필드셋](https://jsonapi.org/format/#fetching-sparse-fieldsets)을 지원하여 클라이언트가 `fields` 쿼리 매개변수를 사용해 각 리소스 타입의 특정 속성만 요청할 수 있습니다:```
GET /api/posts?fields[posts]=title,created_at&fields[users]=name
```



이것은 `posts` 리소스에 대해 `title` 및 `created_at` 속성만 포함하며, `users` 리소스에 대해 `name` 속성만 포함합니다.

<a name="jsonapi-ignoring-query-string"></a>
#### 쿼리 문자열 무시

특정 리소스 응답에 대해 희소 필드셋 필터링을 비활성화하려면 `ignoreFieldsAndIncludesInQueryString` 메서드를 호출할 수 있습니다:

```php
return $post->toResource()
    ->ignoreFieldsAndIncludesInQueryString();
```



<a name="jsonapi-including-previously-loaded-relationships"></a>
#### 이전에 로드된 관계 포함

기본적으로 관계는 `include` 쿼리 매개변수를 통해 요청할 때만 응답에 포함됩니다. 쿼리 문자열에 관계없이 이전에 미리 로드된 모든 관계를 포함하려면 `includePreviouslyLoadedRelationships` 메서드를 호출할 수 있습니다:

```php
return $post->load('author', 'comments')
    ->toResource()
    ->includePreviouslyLoadedRelationships();
```



<a name="jsonapi-links-and-meta"></a>
### 링크 및 메타

리소스에서 `toLinks` 및 `toMeta` 메서드를 재정의하여 JSON:API 리소스 객체에 링크 및 메타 정보를 추가할 수 있습니다:

```php
/**
 * Get the resource's links.
 */
public function toLinks(Request $request): array
{
    return [
        'self' => route('api.posts.show', $this->resource),
    ];
}

/**
 * Get the resource's meta information.
 */
public function toMeta(Request $request): array
{
    return [
        'readable_created_at' => $this->created_at->diffForHumans(),
    ];
}
```



이렇게 하면 응답의 리소스 객체에 `links` 및 `meta` 키가 추가됩니다:

```json
{
    "data": {
        "id": "1",
        "type": "posts",
        "attributes": {
            "title": "Hello World"
        },
        "links": {
            "self": "https://example.com/api/posts/1"
        },
        "meta": {
            "readable_created_at": "2 hours ago"
        }
    }
}
```



<a name="resource-responses"></a>
## 리소스 응답

이미 읽으셨듯이, 리소스는 라우트와 컨트롤러에서 직접 반환될 수 있습니다:

```php
use App\Models\User;

Route::get('/user/{id}', function (string $id) {
    return User::findOrFail($id)->toResource();
});
```



하지만 때때로 클라이언트로 보내기 전에 나가는 HTTP 응답을 사용자 정의해야 할 때가 있습니다. 이를 달성하는 방법은 두 가지가 있습니다. 첫 번째로, 리소스에 `response` 메서드를 연결할 수 있습니다. 이 메서드는 `Illuminate\Http\JsonResponse` 인스턴스를 반환하여 응답의 헤더를 완전히 제어할 수 있게 해줍니다:

```php
use App\Http\Resources\UserResource;
use App\Models\User;

Route::get('/user', function () {
    return User::find(1)
        ->toResource()
        ->response()
        ->header('X-Value', 'True');
});
```



또는 리소스 자체 내에서 `withResponse` 메서드를 정의할 수 있습니다. 이 메서드는 리소스가 응답에서 가장 바깥쪽 리소스로 반환될 때 호출됩니다:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class UserResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
        ];
    }

    /**
     * Customize the outgoing response for the resource.
     */
    public function withResponse(Request $request, JsonResponse $response): void
    {
        $response->header('X-Value', 'True');
    }
}
```
{% endraw %}
