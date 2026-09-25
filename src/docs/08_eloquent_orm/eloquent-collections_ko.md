---
layout: docs
title: "Eloquent: 컬렉션"
---

{% raw %}
# Eloquent: 컬렉션

- [소개](#introduction)
- [사용 가능한 메서드](#available-methods)
- [사용자 정의 컬렉션](#custom-collections)

<a name="introduction"></a>
## 소개

하나 이상의 모델 결과를 반환하는 모든 Eloquent 메서드는 `Illuminate\Database\Eloquent\Collection` 클래스의 인스턴스를 반환하며, `get` 메서드를 통해 검색되거나 관계를 통해 접근한 결과도 포함됩니다. Eloquent 컬렉션 객체는 Laravel의 [기본 컬렉션](/docs/{{version}}/collections)을 확장하므로 Eloquent 모델의 기본 배열을 유창하게 다루는 데 사용되는 수십 가지 메서드를 자연스럽게 상속받습니다. 이러한 유용한 메서드에 대해 모두 배우려면 Laravel 컬렉션 문서를 반드시 검토하세요!

모든 컬렉션은 반복자(iterator) 역할도 하여 단순 PHP 배열처럼 컬렉션을 반복할 수 있습니다:

```php
use App\Models\User;

$users = User::where('active', 1)->get();

foreach ($users as $user) {
    echo $user->name;
}

```

그러나 앞서 언급했듯이, 컬렉션은 배열보다 훨씬 강력하며 직관적인 인터페이스를 사용하여 연결할 수 있는 다양한 맵/리듀스 연산을 제공합니다. 예를 들어, 모든 비활성 모델을 제거한 후 남은 각 사용자에 대해 이름을 가져올 수 있습니다:

```php
$names = User::all()->reject(function (User $user) {
    return $user->active === false;
})->map(function (User $user) {
    return $user->name;
});

```

<a name="eloquent-collection-conversion"></a>
#### 웅변적 수집 변환

대부분의 Eloquent 컬렉션 메서드는 Eloquent 컬렉션의 새 인스턴스를 반환하지만， `collapse`, `flatten`, `flip`, `keys`, `pluck` 및 `zip` 메서드는 [base collection](/docs/{{version}}/collections) 인스턴스를 반환합니다. 마찬가지로， `map` 작업이 Eloquent 모델을 포함하지 않는 컬렉션을 반환하면 기본 컬렉션 인스턴스로 변환됩니다。

<a name="available-methods"></a>
## 사용 가능한 방법

모든 Eloquent 컬렉션은 기본 [Laravel collection](/docs/{{version}}/collections#available-methods) 오브젝트를 확장합니다. 따라서 기본 컬렉션 클래스가 제공하는 모든 강력한 메서드를 상속합니다。

또한 `Illuminate\Database\Eloquent\Collection` 클래스는 모델 컬렉션을 관리하는 데 도움이 되는 메서드의 상위 집합을 제공합니다. 대부분의 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환하지만， `modelKeys` 와 같은 일부 메서드는 `Illuminate\Support\Collection` 인스턴스를 반환합니다。

<style>
.collection-method-list > p {
columns: 14.4em 1; -moz-columns: 14.4em 1; -webkit-columns: 14.4em
}

.collection-method-list a {
표시: 블록;
오버플로우: 숨겨짐;
텍스트 오버플로우: 타원;
화이트 스페이스: 아무것도 쓰지 않음;
}

.collection-method 코드 {
서체 크기: 14px;
}

.collection-method:not(.first-collection-method) {
마진 - 톱: 50px;
}
</style>

<div class="collection-method-list" markdown="1">

[추가](#method-append)
[내용](#method-contains)
[diff](#method-diff)
[예외](#method-except)
[find](#method-find)
findOrFail(#method-find-or-fail)
[새로운](#method-fresh)
intersect (#method-intersect)
load (#method-load)
loadMissing (#method-loadMissing)
modelKeys (#method-modelKeys)
makeVisible(#method-makeVisible)
makeHidden (#method-makeHidden)
mergeVisible(#method-mergeVisible)
mergeHidden (#method-mergeHidden)
only (#method-only)
partition (#method-partition)
setAppends(#method-setAppends)
setVisible(#method-setVisible)
setHidden(#method-setHidden)
toQuery(#method-toquery)
unique (#method-unique)
[부록 없음](#method-withoutAppends)

</div>

<a name="method-append"></a>
#### `append($attributes)` {collection-method .first-collection-method}



`append` 메서드는 컬렉션의 모든 모델에 대해 속성을 [추가](/docs/{{version}}/eloquent-serialization#appending-values-to-json)해야 함을 나타내는 데 사용될 수 있습니다. 이 메서드는 속성의 배열이나 단일 속성을 받을 수 있습니다:

```php
$users->append('team');

$users->append(['team', 'is_admin']);

```

<a name="method-contains"></a>
#### `contains($key, $operator = null, $value = null)` {.collection-method}

`contains` 메서드는 주어진 모델 인스턴스가 컬렉션에 포함되어 있는지 확인하는 데 사용할 수 있습니다. 이 메서드는 기본 키 또는 모델 인스턴스를 받습니다:

```php
$users->contains(1);

$users->contains(User::find(1));

```

<a name="method-diff"></a>
#### `diff($items)` {.collection-method}

`diff` 메서드는 주어진 컬렉션에 없는 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->diff(User::whereIn('id', [1, 2, 3])->get());

```

<a name="method-except"></a>
#### `except($keys)` {.collection-method}

`except` 메서드는 주어진 기본 키를 가지지 않은 모든 모델을 반환합니다:

```php
$users = $users->except([1, 2, 3]);

```

<a name="method-find"></a>
#### `find($key)` {.collection-method}

`find` 메서드는 주어진 키와 일치하는 기본 키를 가진 모델을 반환합니다. `$key`가 모델 인스턴스인 경우, `find`는 기본 키와 일치하는 모델을 반환하려고 시도합니다. `$key`가 키 배열인 경우, `find`는 주어진 배열에 있는 기본 키를 가진 모든 모델을 반환합니다:

```php
$users = User::all();

$user = $users->find(1);

```

<a name="method-find-or-fail"></a>
#### `findOrFail($key)` {.collection-method}

`findOrFail` 메서드는 주어진 키와 일치하는 기본 키를 가진 모델을 반환하거나, 컬렉션에서 일치하는 모델을 찾을 수 없는 경우 `Illuminate\Database\Eloquent\ModelNotFoundException` 예외를 발생시킵니다:

```php
$users = User::all();

$user = $users->findOrFail(1);

```

<a name="method-fresh"></a>
#### `fresh($with = [])` {.collection-method}

`fresh` 메서드는 컬렉션의 각 모델에 대해 데이터베이스에서 새로운 인스턴스를 가져옵니다. 또한, 지정된 관계가 있으면 이를 즉시 로드합니다:

```php
$users = $users->fresh();

$users = $users->fresh('comments');

```

<a name="method-intersect"></a>
#### `intersect($items)` {.collection-method}

`intersect` 메서드는 주어진 컬렉션에도 존재하는 모든 모델을 반환합니다:

```php
use App\Models\User;

$users = $users->intersect(User::whereIn('id', [1, 2, 3])->get());

```

<a name="method-load"></a>
#### `load($relations)` {.collection-method}

`load` 메서드는 컬렉션의 모든 모델에 대해 지정된 관계를 eager load 합니다:

```php
$users->load(['comments', 'posts']);

$users->load('comments.author');

$users->load(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);

```

<a name="method-loadMissing"></a>
#### `loadMissing($relations)` {.collection-method}

`loadMissing` 메서드는 관계가 이미 로드되지 않은 경우 컬렉션의 모든 모델에 대해 주어진 관계를 eager load 합니다:

```php
$users->loadMissing(['comments', 'posts']);

$users->loadMissing('comments.author');

$users->loadMissing(['comments', 'posts' => fn ($query) => $query->where('active', 1)]);

```

<a name="method-modelKeys"></a>
#### `modelKeys()` {.collection-method}

`modelKeys` 방법은 컬렉션의 모든 모델에 대한 기본 키를 반환합니다:

```php
$users->modelKeys();

// [1, 2, 3, 4, 5]

```

<a name="method-makeVisible"></a>
#### `makeVisible($attributes)` {.collection-method}

`makeVisible` 방법은 컬렉션의 각 모델에서 일반적으로 "숨겨진" 속성을 [보이도록](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json) 합니다:

```php
$users = $users->makeVisible(['address', 'phone_number']);

```

<a name="method-makeHidden"></a>
#### `makeHidden($attributes)` {.collection-method}

`makeHidden` 방법은 컬렉션의 각 모델에서 일반적으로 "보이는" 속성들을 [숨깁니다](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->makeHidden(['address', 'phone_number']);

```

<a name="method-mergeVisible"></a>
#### `mergeVisible($attributes)` {.collection-method}

`mergeVisible` 방법은 기존의 표시된 속성을 유지하면서 [추가 속성을 표시할 수 있습니다](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->mergeVisible(['middle_name']);

```

<a name="method-mergeHidden"></a>
#### `mergeHidden($attributes)` {.collection-method}

`mergeHidden` 방법은 기존의 숨겨진 속성을 유지하면서 [추가 속성을 숨깁니다](/docs/{{version}}/eloquent-serialization#hiding-attributes-from-json):

```php
$users = $users->mergeHidden(['last_login_at']);

```

<a name="method-only"></a>
#### `only($keys)` {.collection-method}

`only` 메서드는 주어진 기본 키를 가진 모든 모델을 반환합니다:

```php
$users = $users->only([1, 2, 3]);

```

<a name="method-partition"></a>
#### `partition` {.collection-method}

`partition` 메서드는 `Illuminate\Database\Eloquent\Collection` 컬렉션 인스턴스를 포함하는 `Illuminate\Support\Collection`의 인스턴스를 반환합니다:

```php
$partition = $users->partition(fn ($user) => $user->age > 18);

dump($partition::class);    // Illuminate\Support\Collection
dump($partition[0]::class); // Illuminate\Database\Eloquent\Collection
dump($partition[1]::class); // Illuminate\Database\Eloquent\Collection

```

<a name="method-setAppends"></a>
#### `setAppends($attributes)` {.collection-method}

`setAppends` 메서드는 컬렉션의 각 모델에 있는 모든 [추가된 속성들](/docs/{{version}}/eloquent-serialization#appending-values-to-json)을 일시적으로 무시합니다:

```php
$users = $users->setAppends(['is_admin']);

```

<a name="method-setVisible"></a>
#### `setVisible($attributes)` {.collection-method}

`setVisible` 방법은 컬렉션의 각 모델에 있는 모든 표시 속성을 [일시적으로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setVisible(['id', 'name']);

```

<a name="method-setHidden"></a>
#### `setHidden($attributes)` {.collection-method}

`setHidden` 방법은 컬렉션의 각 모델에 있는 모든 숨겨진 속성을 [일시적으로 재정의](/docs/{{version}}/eloquent-serialization#temporarily-modifying-attribute-visibility)합니다:

```php
$users = $users->setHidden(['email', 'password', 'remember_token']);

```

<a name="method-toquery"></a>
#### `toQuery()` {.collection-method}

`toQuery` 메서드는 컬렉션 모델의 기본 키에 `whereIn` 제약 조건을 포함하는 Eloquent 쿼리 빌더 인스턴스를 반환합니다:

```php
use App\Models\User;

$users = User::where('status', 'VIP')->get();

$users->toQuery()->update([
    'status' => 'Administrator',
]);

```

<a name="method-unique"></a>
#### `unique($key = null, $strict = false)` {.collection-method}

`unique` 메서드는 컬렉션의 모든 고유 모델을 반환합니다. 컬렉션에 있는 다른 모델과 동일한 기본 키를 가진 모델은 제거됩니다:

```php
$users = $users->unique();

```

<a name="method-withoutAppends"></a>
#### `withoutAppends()` {.collection-method}

`withoutAppends` 메서드는 컬렉션의 각 모델에 있는 모든 [추가된 속성](/docs/{{version}}/eloquent-serialization#appending-values-to-json)을 일시적으로 제거합니다:

```php
$users = $users->withoutAppends();

```

<a name="custom-collections"></a>
## 맞춤 컬렉션

주어진 모델과 상호작용할 때 맞춤 `Collection` 객체를 사용하고 싶다면 모델에 `CollectedBy` 속성을 추가할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Attributes\CollectedBy;
use Illuminate\Database\Eloquent\Model;

#[CollectedBy(UserCollection::class)]
class User extends Model
{
    // ...
}

```

또는 모델에 `newCollection` 메서드를 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Support\UserCollection;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Create a new Eloquent Collection instance.
     *
     * @param  array<int, \Illuminate\Database\Eloquent\Model>  $models
     * @return \Illuminate\Database\Eloquent\Collection<int, \Illuminate\Database\Eloquent\Model>
     */
    public function newCollection(array $models = []): Collection
    {
        $collection = new UserCollection($models);

        if (Model::isAutomaticallyEagerLoadingRelationships()) {
            $collection->withRelationshipAutoloading();
        }

        return $collection;
    }
}

```

`newCollection` 메서드를 정의했거나 모델에 `CollectedBy` 속성을 추가하면, Eloquent가 일반적으로 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환할 때마다 사용자 정의 컬렉션 인스턴스를 받게 됩니다.

애플리케이션의 모든 모델에서 사용자 정의 컬렉션을 사용하고 싶다면, 애플리케이션의 모든 모델이 확장하는 기본 모델 클래스에 `newCollection` 메서드를 정의해야 합니다.
{% endraw %}
