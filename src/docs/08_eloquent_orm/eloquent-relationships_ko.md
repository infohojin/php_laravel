---
layout: docs
title: "Eloquent: 관계"
---

{% raw %}
# Eloquent: 관계

- [Introduction](#introduction)
- [Defining Relationships](#defining-relationships)
    - [One to One / Has One](#one-to-one)
    - [One to Many / Has Many](#one-to-many)
    - [One to Many (Inverse) / Belongs To](#one-to-many-inverse)
    - [Has One of Many](#has-one-of-many)
    - [Has One Through](#has-one-through)
    - [Has Many Through](#has-many-through)
- [Scoped Relationships](#scoped-relationships)
- [Many to Many Relationships](#many-to-many)
    - [Retrieving Intermediate Table Columns](#retrieving-intermediate-table-columns)
    - [Filtering Queries via Intermediate Table Columns](#filtering-queries-via-intermediate-table-columns)
    - [Ordering Queries via Intermediate Table Columns](#ordering-queries-via-intermediate-table-columns)
    - [Defining Custom Intermediate Table Models](#defining-custom-intermediate-table-models)
        - [Automatically Hydrating Pivot Relationships](#automatically-hydrating-pivot-relationships)
- [Polymorphic Relationships](#polymorphic-relationships)
    - [One to One](#one-to-one-polymorphic-relations)
    - [One to Many](#one-to-many-polymorphic-relations)
    - [One of Many](#one-of-many-polymorphic-relations)
    - [Many to Many](#many-to-many-polymorphic-relations)
    - [Custom Polymorphic Types](#custom-polymorphic-types)
- [Dynamic Relationships](#dynamic-relationships)
- [Querying Relations](#querying-relations)
    - [Relationship Methods vs. Dynamic Properties](#relationship-methods-vs-dynamic-properties)
    - [Querying Relationship Existence](#querying-relationship-existence)
    - [Querying Relationship Absence](#querying-relationship-absence)
    - [Querying Morph To Relationships](#querying-morph-to-relationships)
- [Aggregating Related Models](#aggregating-related-models)
    - [Counting Related Models](#counting-related-models)
    - [Other Aggregate Functions](#other-aggregate-functions)
    - [Counting Related Models on Morph To Relationships](#counting-related-models-on-morph-to-relationships)
- [Eager Loading](#eager-loading)
    - [Constraining Eager Loads](#constraining-eager-loads)
    - [Lazy Eager Loading](#lazy-eager-loading)
    - [Automatic Eager Loading](#automatic-eager-loading)
    - [Preventing Lazy Loading](#preventing-lazy-loading)
- [Inserting and Updating Related Models](#inserting-and-updating-related-models)
    - [The `save` Method](#the-save-method)
    - [The `create` Method](#the-create-method)
    - [Belongs To Relationships](#updating-belongs-to-relationships)
    - [Many to Many Relationships](#updating-many-to-many-relationships)
- [Touching Parent Timestamps](#touching-parent-timestamps)



<a name="introduction"></a>
## 소개

데이터베이스 테이블은 종종 서로 관련이 있습니다. 예를 들어, 블로그 게시물은 여러 댓글을 가질 수 있으며, 주문은 주문한 사용자와 관련될 수 있습니다. Eloquent는 이러한 관계를 관리하고 다루는 것을 쉽게 만들어 주며, 다양한 일반적인 관계를 지원합니다:

<div class="content-list" markdown="1">

- [일대일](#one-to-one)
- [일대다](#one-to-many)
- [다대다](#many-to-many)
- [중간을 통한 일대일](#has-one-through)
- [중간을 통한 일대다](#has-many-through)
- [다형 일대일](#one-to-one-polymorphic-relations)
- [다형 일대다](#one-to-many-polymorphic-relations)
- [다형 다대다](#many-to-many-polymorphic-relations)

</div>

<a name="defining-relationships"></a>
## 관계 정의하기

Eloquent 관계는 Eloquent 모델 클래스의 메서드로 정의됩니다. 관계는 또한 강력한 [쿼리 빌더](/docs/{{version}}/queries)로 사용되기 때문에, 관계를 메서드로 정의하면 강력한 메서드 체이닝과 쿼리 기능을 제공합니다. 예를 들어, 우리는 이 `posts` 관계에 추가 쿼리 조건을 체이닝할 수 있습니다:

```php
$user->posts()->where('active', 1)->get();
```



하지만 관계 사용에 대해 너무 깊이 들어가기 전에, Eloquent가 지원하는 각 유형의 관계를 정의하는 방법을 배워봅시다.

<a name="one-to-one"></a>
### 일대일 / Has One

일대일 관계는 매우 기본적인 데이터베이스 관계 유형입니다. 예를 들어, `User` 모델은 하나의 `Phone` 모델과 연관될 수 있습니다. 이 관계를 정의하기 위해, `User` 모델에 `phone` 메서드를 추가합니다. `phone` 메서드는 `hasOne` 메서드를 호출하고 그 결과를 반환해야 합니다. `hasOne` 메서드는 모델의 `Illuminate\Database\Eloquent\Model` 기반 클래스를 통해 모델에서 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

class User extends Model
{
    /**
     * Get the phone associated with the user.
     */
    public function phone(): HasOne
    {
        return $this->hasOne(Phone::class);
    }
}
```



`hasOne` 메서드에 전달된 첫 번째 인수는 관련 모델 클래스의 이름입니다. 관계가 정의되면 Eloquent의 동적 속성을 사용하여 관련 레코드를 가져올 수 있습니다. 동적 속성을 사용하면 관계 메서드를 마치 모델에 정의된 속성처럼 접근할 수 있습니다:

```php
$phone = User::find(1)->phone;
```



Eloquent는 관계의 외래 키를 부모 모델 이름을 기반으로 결정합니다. 이 경우, `Phone` 모델은 자동으로 `user_id` 외래 키를 가진 것으로 간주됩니다. 이 규칙을 재정의하고 싶다면, `hasOne` 메서드에 두 번째 인수를 전달할 수 있습니다:

```php
return $this->hasOne(Phone::class, 'foreign_key');
```



또한, Eloquent는 외래 키가 부모의 기본 키 열과 일치하는 값을 가져야 한다고 가정합니다. 다시 말해, Eloquent는 사용자의 `id` 열의 값을 `Phone` 레코드의 `user_id` 열에서 찾습니다. 관계가 `id` 또는 모델의 기본 키가 아닌 다른 기본 키 값을 사용하도록 하려면, `hasOne` 메서드에 세 번째 인수를 전달할 수 있습니다.

```php
return $this->hasOne(Phone::class, 'foreign_key', 'local_key');
```



<a name="one-to-one-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역을 정의하기

그래서 우리는 우리의 `User` 모델에서 `Phone` 모델에 접근할 수 있습니다. 다음으로, 전화기를 소유한 사용자를 접근할 수 있게 해주는 `Phone` 모델에 관계를 정의해 봅시다. `hasOne` 관계의 역은 `belongsTo` 메서드를 사용하여 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Phone extends Model
{
    /**
     * Get the user that owns the phone.
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```



`user` 메서드를 호출할 때, Eloquent는 `Phone` 모델의 `user_id` 열과 일치하는 `id`를 가진 `User` 모델을 찾으려고 시도합니다.

Eloquent는 관계 메서드의 이름을 확인하고 메서드 이름에 `_id`를 붙여 외래 키 이름을 결정합니다. 따라서 이 경우 Eloquent는 `Phone` 모델이 `user_id` 열을 가지고 있다고 가정합니다. 그러나 `Phone` 모델의 외래 키가 `user_id`가 아닌 경우, `belongsTo` 메서드의 두 번째 인수로 사용자 정의 키 이름을 전달할 수 있습니다:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key');
}
```



부모 모델이 `id`를 기본 키로 사용하지 않거나 다른 열을 사용하여 연결된 모델을 찾으려는 경우, 부모 테이블의 사용자 정의 키를 지정하는 세 번째 인수를 `belongsTo` 메서드에 전달할 수 있습니다:

```php
/**
 * Get the user that owns the phone.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class, 'foreign_key', 'owner_key');
}
```



<a name="one-to-many"></a>
### 일대다 / 다수 소유

일대다 관계는 단일 모델이 하나 이상의 자식 모델의 부모인 관계를 정의할 때 사용됩니다. 예를 들어, 블로그 게시물은 무한한 수의 댓글을 가질 수 있습니다. 다른 모든 Eloquent 관계와 마찬가지로, 일대다 관계는 Eloquent 모델에 메서드를 정의하여 정의됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```



기억하세요, Eloquent는 `Comment` 모델에 대한 적절한 외래 키 열을 자동으로 결정합니다. 관례상, Eloquent는 부모 모델의 '스네이크 케이스' 이름을 가져오고 `_id`를 접미사로 붙입니다. 따라서 이 예제에서 Eloquent는 `Comment` 모델의 외래 키 열이 `post_id`라고 가정합니다.

관계 메서드가 정의되면, `comments` 속성을 통해 관련 댓글의 [컬렉션](/docs/{{version}}/eloquent-collections)에 접근할 수 있습니다. Eloquent가 '동적 관계 속성'을 제공하므로, 관계 메서드를 모델에 속성으로 정의된 것처럼 접근할 수 있다는 점을 기억하세요.

```php
use App\Models\Post;

$comments = Post::find(1)->comments;

foreach ($comments as $comment) {
    // ...
}
```



모든 관계가 또한 쿼리 빌더 역할을 하기 때문에, `comments` 메서드를 호출하고 조건을 계속 연결하여 관계 쿼리에 추가 제약을 추가할 수 있습니다:

```php
$comment = Post::find(1)->comments()
    ->where('title', 'foo')
    ->first();
```



`hasOne` 방법과 마찬가지로, `hasMany` 메서드에 추가 인수를 전달하여 외부 키와 로컬 키를 재정의할 수도 있습니다:

```php
return $this->hasMany(Comment::class, 'foreign_key');

return $this->hasMany(Comment::class, 'foreign_key', 'local_key');
```



<a name="automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 수화

Eloquent eager loading을 사용하더라도, 자식 모델을 반복하면서 자식 모델에서 부모 모델에 접근하려고 하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->post->title;
    }
}
```



위의 예제에서는 "N + 1" 쿼리 문제가 발생했습니다. 이는 모든 `Post` 모델에 대해 댓글이 미리 로드되었음에도 불구하고, Eloquent가 각 자식 `Comment` 모델에 부모 `Post`를 자동으로 채우지 않기 때문입니다.

Eloquent가 부모 모델을 자식 모델에 자동으로 채우도록 하려면, `hasMany` 관계를 정의할 때 `chaperone` 메서드를 호출할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    /**
     * Get the comments for the blog post.
     */
    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class)->chaperone();
    }
}
```



또는 실행 시간에 자동 상위 하이드레이션을 선택하고 싶다면, 관계를 즉시 로드할 때 `chaperone` 모델을 호출할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```



<a name="one-to-many-inverse"></a>
### 일대다 (역방향) / 소속 관계

이제 게시물의 모든 댓글에 접근할 수 있으므로, 댓글이 자신의 부모 게시물에 접근할 수 있도록 관계를 정의해 봅시다. `hasMany` 관계의 역방향을 정의하려면, 자식 모델에서 `belongsTo` 메서드를 호출하는 관계 메서드를 정의하면 됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    /**
     * Get the post that owns the comment.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```



관계가 정의되면 `post` "동적 관계 속성"에 접근하여 댓글의 상위 게시물을 가져올 수 있습니다.

```php
use App\Models\Comment;

$comment = Comment::find(1);

return $comment->post->title;
```



위의 예제에서, Eloquent는 `Comment` 모델의 `post_id` 열과 일치하는 `id`를 가진 `Post` 모델을 찾으려고 시도합니다.

Eloquent는 관계 메서드의 이름을 살펴보고 메서드 이름에 `_`를 붙인 다음 부모 모델의 기본 키 열 이름을 붙임으로써 기본 외래 키 이름을 결정합니다. 따라서 이 예제에서, Eloquent는 `comments` 테이블에서 `Post` 모델의 외래 키가 `post_id`라고 가정합니다.

그러나 관계의 외래 키가 이러한 규칙을 따르지 않는 경우, `belongsTo` 메서드의 두 번째 인수로 사용자 정의 외래 키 이름을 전달할 수 있습니다:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key');
}
```



부모 모델이 `id`를 기본 키로 사용하지 않거나 다른 열을 사용하여 연결된 모델을 찾으려는 경우, 부모 테이블의 사용자 정의 키를 지정하는 세 번째 인수를 `belongsTo` 메서드에 전달할 수 있습니다:

```php
/**
 * Get the post that owns the comment.
 */
public function post(): BelongsTo
{
    return $this->belongsTo(Post::class, 'foreign_key', 'owner_key');
}
```



<a name="default-models"></a>
#### 기본 모델

`belongsTo`, `hasOne`, `hasOneThrough`, 및 `morphOne` 관계를 사용하면, 주어진 관계가 `null`일 때 반환될 기본 모델을 정의할 수 있습니다. 이 패턴은 흔히 [널 객체 패턴](https://en.wikipedia.org/wiki/Null_Object_pattern)이라고 불리며, 코드에서 조건문 검사를 제거하는 데 도움을 줄 수 있습니다. 다음 예제에서, `user` 관계는 `Post` 모델에 사용자가 연결되지 않은 경우 빈 `App\Models\User` 모델을 반환합니다:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault();
}
```



기본 모델에 속성을 채우려면 `withDefault` 메서드에 배열이나 클로저를 전달할 수 있습니다:

```php
/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault([
        'name' => 'Guest Author',
    ]);
}

/**
 * Get the author of the post.
 */
public function user(): BelongsTo
{
    return $this->belongsTo(User::class)->withDefault(function (User $user, Post $post) {
        $user->name = 'Guest Author';
    });
}
```



<a name="querying-belongs-to-relationships"></a>
#### 'belongs to' 관계 쿼리하기

"belongs to" 관계의 자식을 쿼리할 때, 해당 Eloquent 모델을 가져오기 위해 `where` 절을 수동으로 작성할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::where('user_id', $user->id)->get();
```



하지만 주어진 모델에 대해 적절한 관계와 외래 키를 자동으로 결정하는 `whereBelongsTo` 방법을 사용하는 것이 더 편리할 수 있습니다:

```php
$posts = Post::whereBelongsTo($user)->get();
```



`whereBelongsTo` 메서드에 [컬렉션](/docs/{{version}}/eloquent-collections) 인스턴스를 제공할 수도 있습니다. 이렇게 하면 Laravel은 컬렉션 내의 어떤 부모 모델에도 속하는 모델들을 가져오게 됩니다:

```php
$users = User::where('vip', true)->get();

$posts = Post::whereBelongsTo($users)->get();
```



기본적으로 Laravel은 주어진 모델과 관련된 관계를 모델의 클래스 이름을 기반으로 결정합니다. 그러나 `whereBelongsTo` 메서드의 두 번째 인수로 관계 이름을 제공하여 수동으로 지정할 수도 있습니다:

```php
$posts = Post::whereBelongsTo($user, 'author')->get();
```



<a name="has-one-of-many"></a>
### 여러 개 중 하나 가지기

때때로 하나의 모델이 많은 관련 모델을 가질 수 있지만, 관계의 "최신" 또는 "가장 오래된" 관련 모델을 쉽게 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 `Order` 모델과 관련될 수 있지만, 사용자가 주문한 가장 최근 주문과 상호작용하는 편리한 방법을 정의하고자 할 수 있습니다. 이는 `hasOne` 관계 유형과 `ofMany` 메서드를 결합하여 수행할 수 있습니다:

```php
/**
 * Get the user's most recent order.
 */
public function latestOrder(): HasOne
{
    return $this->hasOne(Order::class)->latestOfMany();
}
```



마찬가지로, 관계에서 '가장 오래된' 또는 첫 번째 관련 모델을 가져오는 메서드를 정의할 수도 있습니다:

```php
/**
 * Get the user's oldest order.
 */
public function oldestOrder(): HasOne
{
    return $this->hasOne(Order::class)->oldestOfMany();
}
```



기본적으로 `latestOfMany` 및 `oldestOfMany` 메서드는 모델의 기본 키를 기준으로 최신 또는 가장 오래된 관련 모델을 가져옵니다. 이 기본 키는 정렬 가능해야 합니다. 그러나 때로는 다른 정렬 기준을 사용하여 더 큰 관계에서 단일 모델을 가져오고 싶을 수 있습니다.

예를 들어, `ofMany` 메서드를 사용하면 사용자의 가장 비싼 주문을 가져올 수 있습니다. `ofMany` 메서드는 첫 번째 인수로 정렬 가능한 열을 받고, 관련 모델을 조회할 때 적용할 집계 함수(`min` 또는 `max`)를 지정합니다:

```php
/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->hasOne(Order::class)->ofMany('price', 'max');
}
```



> [!WARNING]
> PostgreSQL은 UUID 열에 대해 `MAX` 함수를 실행하는 것을 지원하지 않기 때문에, 현재 PostgreSQL UUID 열과 함께 다중 중 하나 관계를 사용하는 것은 불가능합니다.

<a name="converting-many-relationships-to-has-one-relationships"></a>
#### "다수형" 관계를 '하나 있음' 관계로 변환하기

종종 `latestOfMany`, `oldestOfMany`, 또는 `ofMany` 메서드를 사용하여 단일 모델을 조회할 때, 동일한 모델에 대해 이미 '다수 있음' 관계가 정의되어 있는 경우가 있습니다. 편의를 위해 Laravel은 관계에서 `one` 메서드를 호출하여 이 관계를 쉽게 '하나 있음' 관계로 변환할 수 있게 합니다:

```php
/**
 * Get the user's orders.
 */
public function orders(): HasMany
{
    return $this->hasMany(Order::class);
}

/**
 * Get the user's largest order.
 */
public function largestOrder(): HasOne
{
    return $this->orders()->one()->ofMany('price', 'max');
}
```



`HasManyThrough` 관계를 `HasOneThrough` 관계로 변환하기 위해 `one` 방법을 사용할 수도 있습니다:

```php
public function latestDeployment(): HasOneThrough
{
    return $this->deployments()->one()->latestOfMany();
}
```



<a name="advanced-has-one-of-many-relationships"></a>
#### 고급에는 여러 관계 중 하나가 있습니다

더 고급 "하나의 많은 관계 중 하나"를 구성하는 것이 가능합니다. 예를 들어, `Product` 모델은 많은 관련 `Price` 모델을 가질 수 있으며, 이러한 모델은 새로운 가격이 게시된 후에도 시스템에 유지될 수 있습니다. 또한, 제품의 새로운 가격 데이터를 `published_at` 열을 통해 미리 게시하여 미래 날짜에 적용되도록 할 수 있습니다.

요약하면, 게시 날짜가 미래가 아닌 최신 게시된 가격을 검색해야 합니다. 또한, 두 가격의 게시 날짜가 동일한 경우, 가장 큰 ID를 가진 가격을 선호합니다. 이를 달성하기 위해, 최신 가격을 결정하는 정렬 가능한 열을 포함하는 배열을 `ofMany` 메서드에 전달해야 합니다. 또한, 두 번째 매개변수로 `ofMany` 메서드에 닫힘(클로저)이 제공됩니다. 이 클로저는 관계 쿼리에 추가 게시 날짜 제약 조건을 추가할 책임이 있습니다:

```php
/**
 * Get the current pricing for the product.
 */
public function currentPricing(): HasOne
{
    return $this->hasOne(Price::class)->ofMany([
        'published_at' => 'max',
        'id' => 'max',
    ], function (Builder $query) {
        $query->where('published_at', '<', now());
    });
}
```



<a name="has-one-through"></a>
### 일대일-중간 관계

"일대일-중간(has-one-through)" 관계는 다른 모델과의 일대일 관계를 정의합니다. 그러나 이 관계는 선언한 모델이 세 번째 모델을 거쳐 다른 모델의 한 인스턴스와 매칭될 수 있음을 나타냅니다.

예를 들어, 차량 수리점 애플리케이션에서 각 `Mechanic` 모델은 하나의 `Car` 모델과 연관될 수 있고, 각 `Car` 모델은 하나의 `Owner` 모델과 연관될 수 있습니다. 정비사와 고객은 데이터베이스 상에서 직접적인 관계가 없지만, 정비사는 `Car` 모델을 통해 고객에 접근할 수 있습니다. 이 관계를 정의하는 데 필요한 테이블을 살펴보겠습니다:

```text
mechanics
    id - integer
    name - string

cars
    id - integer
    model - string
    mechanic_id - integer

owners
    id - integer
    name - string
    car_id - integer
```



이제 관계를 위한 테이블 구조를 검토했으므로, `Mechanic` 모델에서 관계를 정의해 보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOneThrough;

class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(Owner::class, Car::class);
    }
}
```



`hasOneThrough` 메서드에 전달되는 첫 번째 인수는 우리가 접근하고자 하는 최종 모델의 이름이고, 두 번째 인수는 중간 모델의 이름입니다.

또는, 관련된 모든 모델에 이미 관련 관계가 정의되어 있다면, `through` 메서드를 호출하고 해당 관계의 이름을 제공하여 'has-one-through' 관계를 자연스럽게 정의할 수 있습니다. 예를 들어, `Mechanic` 모델이 `cars` 관계를 가지고 있고 `Car` 모델이 `owner` 관계를 가지고 있다면, 다음과 같이 정비사와 소유자를 연결하는 'has-one-through' 관계를 정의할 수 있습니다:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```



<a name="has-one-through-key-conventions"></a>
#### 주요 규칙

관계 쿼리를 수행할 때 일반적인 Eloquent 외래 키 규칙이 사용됩니다. 관계의 키를 사용자 정의하려면 `hasOneThrough` 메서드에 세 번째와 네 번째 인수로 전달할 수 있습니다. 세 번째 인수는 중간 모델의 외래 키 이름입니다. 네 번째 인수는 최종 모델의 외래 키 이름입니다. 다섯 번째 인수는 로컬 키이고, 여섯 번째 인수는 중간 모델의 로컬 키입니다:

```php
class Mechanic extends Model
{
    /**
     * Get the car's owner.
     */
    public function carOwner(): HasOneThrough
    {
        return $this->hasOneThrough(
            Owner::class,
            Car::class,
            'mechanic_id', // Foreign key on the cars table...
            'car_id', // Foreign key on the owners table...
            'id', // Local key on the mechanics table...
            'id' // Local key on the cars table...
        );
    }
}
```



또는 앞서 논의한 것처럼, 관련 모델들 모두에서 이미 관련 관계가 정의되어 있는 경우, `through` 메서드를 호출하고 해당 관계들의 이름을 제공함으로써 'has-one-through' 관계를 유창하게 정의할 수 있습니다. 이 접근 방식은 기존 관계에 이미 정의된 키 관례를 재사용할 수 있는 장점을 제공합니다:

```php
// String based syntax...
return $this->through('cars')->has('owner');

// Dynamic syntax...
return $this->throughCars()->hasOwner();
```



<a name="has-many-through"></a>
### 다대다를 통해 갖기

'다대다를 통해 갖기' 관계는 중간 관계를 통해 먼 관계에 접근할 수 있는 편리한 방법을 제공합니다. 예를 들어, [Laravel Cloud](https://cloud.laravel.com)와 같은 배포 플랫폼을 구축한다고 가정해 봅시다. `Application` 모델은 중간 `Environment` 모델을 통해 여러 `Deployment` 모델에 접근할 수 있습니다. 이 예제를 사용하면 특정 애플리케이션에 대한 모든 배포를 쉽게 모을 수 있습니다. 이 관계를 정의하는 데 필요한 테이블을 살펴봅시다:

```text
applications
    id - integer
    name - string

environments
    id - integer
    application_id - integer
    name - string

deployments
    id - integer
    environment_id - integer
    commit_hash - string
```



이제 관계에 대한 테이블 구조를 검토했으므로, `Application` 모델에서 관계를 정의해 보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasManyThrough;

class Application extends Model
{
    /**
     * Get all of the deployments for the application.
     */
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(Deployment::class, Environment::class);
    }
}
```



`hasManyThrough` 메서드에 전달되는 첫 번째 인수는 우리가 접근하고자 하는 최종 모델의 이름이고, 두 번째 인수는 중간 모델의 이름입니다.

또는, 관련된 모든 모델에 이미 관련 관계가 정의되어 있다면, `through` 메서드를 호출하고 해당 관계의 이름을 제공하여 'has-many-through' 관계를 자연스럽게 정의할 수 있습니다. 예를 들어, `Application` 모델이 `environments` 관계를 가지고 있고 `Environment` 모델이 `deployments` 관계를 가지고 있다면, 애플리케이션과 배포를 연결하는 'has-many-through' 관계를 다음과 같이 정의할 수 있습니다:

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```



`Deployment` 모델의 테이블에는 `application_id` 열이 없지만, `hasManyThrough` 관계를 통해 `$application->deployments`를 사용하여 애플리케이션의 배포에 접근할 수 있습니다. 이러한 모델을 검색하기 위해, Eloquent는 중간 `Environment` 모델의 테이블에 있는 `application_id` 열을 검사합니다. 관련 환경 ID를 찾은 후, 이를 사용하여 `Deployment` 모델의 테이블을 쿼리합니다.

<a name="has-many-through-key-conventions"></a>
#### 주요 규칙

관계의 쿼리를 수행할 때 일반적인 Eloquent 외래 키 규칙이 사용됩니다. 관계의 키를 사용자 지정하려는 경우, `hasManyThrough` 메서드의 세 번째와 네 번째 인수로 전달할 수 있습니다. 세 번째 인수는 중간 모델의 외래 키 이름입니다. 네 번째 인수는 최종 모델의 외래 키 이름입니다. 다섯 번째 인수는 로컬 키이고, 여섯 번째 인수는 중간 모델의 로컬 키입니다.

```php
class Application extends Model
{
    public function deployments(): HasManyThrough
    {
        return $this->hasManyThrough(
            Deployment::class,
            Environment::class,
            'application_id', // Foreign key on the environments table...
            'environment_id', // Foreign key on the deployments table...
            'id', // Local key on the applications table...
            'id' // Local key on the environments table...
        );
    }
}
```



또는 앞서 논의한 것처럼, 관련 모델들 모두에서 관계가 이미 정의되어 있는 경우, `through` 메서드를 호출하고 해당 관계의 이름을 제공하여 'has-many-through' 관계를 자연스럽게 정의할 수 있습니다. 이 접근 방식은 기존 관계에 이미 정의된 키 규칙을 재사용할 수 있다는 장점을 제공합니다.

```php
// String based syntax...
return $this->through('environments')->has('deployments');

// Dynamic syntax...
return $this->throughEnvironments()->hasDeployments();
```



<a name="scoped-relationships"></a>
### 범위가 지정된 관계

관계를 제한하는 추가 메서드를 모델에 추가하는 것은 일반적입니다. 예를 들어, 보다 넓은 `posts` 관계를 추가적인 `where` 제한으로 제한하는 `User` 모델에 `featuredPosts` 메서드를 추가할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get the user's posts.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class)->latest();
    }

    /**
     * Get the user's featured posts.
     */
    public function featuredPosts(): HasMany
    {
        return $this->posts()->where('featured', true);
    }
}
```



그러나 `featuredPosts` 방법을 통해 모델을 생성하려고 시도하면, 그 `featured` 속성은 `true`로 설정되지 않습니다. 관계 메서드를 통해 모델을 생성하고 해당 관계를 통해 생성된 모든 모델에 추가해야 하는 속성을 지정하려면, 관계 쿼리를 작성할 때 `withAttributes` 메서드를 사용할 수 있습니다:

```php
/**
 * Get the user's featured posts.
 */
public function featuredPosts(): HasMany
{
    return $this->posts()->withAttributes(['featured' => true]);
}
```



`withAttributes` 방법은 주어진 속성을 사용하여 쿼리에 `where` 조건을 추가하며, 관계 메서드를 통해 생성된 모든 모델에도 주어진 속성을 추가합니다:

```php
$post = $user->featuredPosts()->create(['title' => 'Featured Post']);

$post->featured; // true
```



쿼리에 `where` 조건을 추가하지 않도록 `withAttributes` 메서드를 지시하려면 `asConditions` 인수를 `false`로 설정할 수 있습니다:

```php
return $this->posts()->withAttributes(['featured' => true], asConditions: false);
```



<a name="many-to-many"></a>
## Many to Many Relationships

Many-to-many relations are slightly more complicated than `hasOne` and `hasMany` relationships. An example of a many-to-many relationship is a user that has many roles and those roles are also shared by other users in the application. For example, a user may be assigned the role of "Author" and "Editor"; however, those roles may also be assigned to other users as well. So, a user has many roles and a role has many users.

<a name="many-to-many-table-structure"></a>
#### Table Structure

To define this relationship, three database tables are needed: `users`, `roles`, and `role_user`. The `role_user` table is derived from the alphabetical order of the related model names and contains `user_id` and `role_id` columns. This table is used as an intermediate table linking the users and roles.

Remember, since a role can belong to many users, we cannot simply place a `user_id` column on the `roles` table. This would mean that a role could only belong to a single user. In order to provide support for roles being assigned to multiple users, the `role_user` table is needed. We can summarize the relationship's table structure like so:

```text
users
    id - integer
    name - string

roles
    id - integer
    name - string

role_user
    user_id - integer
    role_id - integer
```



<a name="many-to-many-model-structure"></a>
#### 모델 구조

다대다 관계는 `belongsToMany` 메서드의 결과를 반환하는 메서드를 작성하여 정의됩니다. `belongsToMany` 메서드는 모든 애플리케이션의 Eloquent 모델에서 사용하는 `Illuminate\Database\Eloquent\Model` 기본 클래스에 의해 제공됩니다. 예를 들어, `User` 모델에서 `roles` 메서드를 정의해 보겠습니다. 이 메서드에 전달되는 첫 번째 인수는 관련된 모델 클래스의 이름입니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class User extends Model
{
    /**
     * The roles that belong to the user.
     */
    public function roles(): BelongsToMany
    {
        return $this->belongsToMany(Role::class);
    }
}
```



관계가 정의되면 `roles` 동적 관계 속성을 사용하여 사용자의 역할에 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    // ...
}
```



모든 관계가 또한 쿼리 빌더 역할을 하기 때문에, `roles` 메서드를 호출하고 조건을 계속 연결하여 관계 쿼리에 추가 제약을 추가할 수 있습니다:

```php
$roles = User::find(1)->roles()->orderBy('name')->get();
```



관계의 중간 테이블 이름을 결정하기 위해, Eloquent는 두 관련 모델 이름을 알파벳 순서로 결합합니다. 그러나 이 규칙을 자유롭게 재정의할 수 있습니다. `belongsToMany` 메서드에 두 번째 인수를 전달하여 그렇게 할 수 있습니다:

```php
return $this->belongsToMany(Role::class, 'role_user');
```



중간 테이블의 이름을 사용자 지정하는 것 외에도, `belongsToMany` 메서드에 추가 인수를 전달하여 테이블의 키 열 이름을 사용자 지정할 수도 있습니다. 세 번째 인수는 관계를 정의하는 모델의 외래 키 이름이며, 네 번째 인수는 연결하려는 모델의 외래 키 이름입니다:

```php
return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
```



<a name="many-to-many-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역 정의

다대다 관계의 '역'을 정의하려면, 관련 모델에 `belongsToMany` 메서드의 결과를 반환하는 메서드를 정의해야 합니다. 사용자 / 역할 예제를 완성하기 위해, `Role` 모델에 `users` 메서드를 정의해 봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class);
    }
}
```



보시다시피, 이 관계는 `App\Models\User` 모델을 참조하는 것을 제외하고는 `User` 모델의 대응 관계와 정확히 동일하게 정의됩니다. `belongsToMany` 메서드를 재사용하고 있기 때문에, 다대다 관계의 "역방향"을 정의할 때 모든 일반적인 테이블 및 키 맞춤 옵션을 사용할 수 있습니다.

<a name="retrieving-intermediate-table-columns"></a>
### 중간 테이블 컬럼 가져오기

이미 배운 것처럼, 다대다 관계를 다루려면 중간 테이블이 필요합니다. Eloquent는 이 테이블과 상호작용할 수 있는 매우 유용한 방법을 제공합니다. 예를 들어, 우리의 `User` 모델이 관련된 많은 `Role` 모델을 가지고 있다고 가정해 봅시다. 이 관계에 접근한 후에, 우리는 모델의 `pivot` 속성을 사용하여 중간 테이블에 접근할 수 있습니다.

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->pivot->created_at;
}
```



각각의 `Role` 모델을 가져올 때마다 자동으로 `pivot` 속성이 할당된다는 점에 유의하십시오. 이 속성은 중간 테이블을 나타내는 모델을 포함합니다.

기본적으로 `pivot` 모델에는 모델 키만 존재합니다. 중간 테이블에 추가 속성이 있는 경우 관계를 정의할 때 이를 지정해야 합니다:

```php
return $this->belongsToMany(Role::class)->withPivot('active', 'created_by');
```



중간 테이블이 Eloquent에 의해 자동으로 유지되는 `created_at` 및 `updated_at` 타임스탬프를 갖기를 원한다면, 관계를 정의할 때 `withTimestamps` 메서드를 호출하세요:

```php
return $this->belongsToMany(Role::class)->withTimestamps();
```



> [!WARNING]
> Eloquent이 자동으로 유지 관리하는 타임스탬프를 활용하는 중간 테이블은 `created_at`와 `updated_at` 타임스탬프 컬럼을 모두 가져야 합니다.

<a name="customizing-the-pivot-attribute-name"></a>
#### `pivot` 속성 이름 사용자 정의

앞서 언급했듯이, 중간 테이블의 속성은 모델에서 `pivot` 속성을 통해 접근할 수 있습니다. 그러나 애플리케이션 내에서의 목적을 더 잘 반영하기 위해 이 속성의 이름을 자유롭게 사용자 정의할 수 있습니다.

예를 들어, 애플리케이션에 팟캐스트를 구독할 수 있는 사용자가 포함되어 있다면, 사용자와 팟캐스트 간 다대다 관계가 있을 가능성이 높습니다. 이 경우 중간 테이블 속성의 이름을 `pivot` 대신 `subscription`로 변경하고 싶을 수 있습니다. 관계를 정의할 때 `as` 메서드를 사용하면 이를 수행할 수 있습니다:

```php
return $this->belongsToMany(Podcast::class)
    ->as('subscription')
    ->withTimestamps();
```



사용자 정의 중간 테이블 속성이 지정되면, 사용자 정의 이름을 사용하여 중간 테이블 데이터에 접근할 수 있습니다:

```php
$users = User::with('podcasts')->get();

foreach ($users->flatMap->podcasts as $podcast) {
    echo $podcast->subscription->created_at;
}
```



<a name="filtering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 컬럼을 통한 쿼리 필터링

관계를 정의할 때 `belongsToMany` 관계 쿼리에서 반환된 결과를 `wherePivot`, `wherePivotIn`, `wherePivotNotIn`, `wherePivotBetween`, `wherePivotNotBetween`, `wherePivotNull`, `wherePivotNotNull` 메서드를 사용하여 필터링할 수도 있습니다:

```php
return $this->belongsToMany(Role::class)
    ->wherePivot('approved', 1);

return $this->belongsToMany(Role::class)
    ->wherePivotIn('priority', [1, 2]);

return $this->belongsToMany(Role::class)
    ->wherePivotNotIn('priority', [1, 2]);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotBetween('created_at', ['2020-01-01 00:00:00', '2020-12-31 00:00:00']);

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNull('expired_at');

return $this->belongsToMany(Podcast::class)
    ->as('subscriptions')
    ->wherePivotNotNull('expired_at');
```



`wherePivot`는 쿼리에 where 절 제약 조건을 추가하지만, 정의된 관계를 통해 새 모델을 생성할 때 지정된 값을 추가하지는 않습니다. 특정 피벗 값으로 관계를 쿼리하고 생성해야 하는 경우, `withPivotValue` 메서드를 사용할 수 있습니다:

```php
return $this->belongsToMany(Role::class)
    ->withPivotValue('approved', 1);
```



<a name="ordering-queries-via-intermediate-table-columns"></a>
### 중간 테이블 열을 통한 쿼리 정렬

`belongsToMany` 관계 쿼리에서 반환된 결과를 `orderByPivot` 및 `orderByPivotDesc` 방법을 사용하여 정렬할 수 있습니다. 다음 예제에서는 사용자의 최신 배지를 모두 가져옵니다:

```php
return $this->belongsToMany(Badge::class)
    ->where('rank', 'gold')
    ->orderByPivotDesc('created_at');
```



<a name="defining-custom-intermediate-table-models"></a>
### 사용자 정의 중간 테이블 모델 정의하기

다대다 관계의 중간 테이블을 나타내는 사용자 정의 모델을 정의하고 싶다면, 관계를 정의할 때 `using` 메서드를 호출할 수 있습니다. 사용자 정의 피벗 모델은 메서드와 캐스트와 같은 피벗 모델에 추가적인 동작을 정의할 수 있는 기회를 제공합니다.

사용자 정의 다대다 피벗 모델은 `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 확장해야 하며, 사용자 정의 다형 다대다 피벗 모델은 `Illuminate\Database\Eloquent\Relations\MorphPivot` 클래스를 확장해야 합니다. 예를 들어, 사용자 정의 `RoleUser` 피벗 모델을 사용하는 `Role` 모델을 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;

class Role extends Model
{
    /**
     * The users that belong to the role.
     */
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)->using(RoleUser::class);
    }
}
```



`RoleUser` 모델을 정의할 때, `Illuminate\Database\Eloquent\Relations\Pivot` 클래스를 확장해야 합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    // ...
}
```



> [!WARNING]
> 피벗 모델은 `SoftDeletes` 트레이트를 사용할 수 없습니다. 피벗 레코드를 소프트 삭제해야 하는 경우 피벗 모델을 실제 Eloquent 모델로 변환하는 것을 고려하세요.

<a name="custom-pivot-models-and-incrementing-ids"></a>
#### 사용자 정의 피벗 모델과 증가하는 ID

사용자 정의 피벗 모델을 사용하는 다대다 관계를 정의했으며, 그 피벗 모델에 자동 증가 기본 키가 있는 경우, 사용자 정의 피벗 모델 클래스가 `Table` 속성을 사용하며 `incrementing`가 `true`로 설정되어 있는지 확인해야 합니다:

```php
use Illuminate\Database\Eloquent\Attributes\Table;
use Illuminate\Database\Eloquent\Relations\Pivot;

#[Table(incrementing: true)]
class RoleUser extends Pivot
{
    // ...
}
```



<a name="automatically-hydrating-pivot-relationships"></a>
#### 피벗 관계 자동 하이드레이션

커스텀 피벗 모델이 선언 모델과 관련 모델에 대한 `belongsTo` 관계를 정의할 때, 각 피벗 모델에서 해당 관계를 자동으로 하이드레이션하기 위해 `chaperone`를 호출할 수 있습니다. 이렇게 하면 피벗을 통해 모델에 접근할 때 추가 쿼리를 피할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\Pivot;

class RoleUser extends Pivot
{
    public function role(): BelongsTo
    {
        return $this->belongsTo(Role::class);
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}

class Role extends Model
{
    public function users(): BelongsToMany
    {
        return $this->belongsToMany(User::class)
            ->using(RoleUser::class)
            ->chaperone();
    }
}
```



Eloquent은 피벗 관계 이름을 추론하려고 시도합니다. 피벗 모델이 비표준 이름을 사용하는 경우, 선언된 관계 이름과 관련 관계 이름을 `chaperone`에 전달하세요:

```php
return $this->belongsToMany(User::class)
    ->using(RoleUser::class)
    ->chaperone(declaring: 'role', related: 'user');
```



<a name="polymorphic-relationships"></a>
## 다형성 관계

다형성 관계는 자식 모델이 단일 연관을 사용하여 여러 유형의 모델에 속할 수 있도록 합니다. 예를 들어, 사용자가 블로그 게시물과 비디오를 공유할 수 있는 애플리케이션을 만든다고 가정해 봅시다. 이런 애플리케이션에서 `Comment` 모델은 `Post` 및 `Video` 모델 모두에 속할 수 있습니다.

<a name="one-to-one-polymorphic-relations"></a>
### 일대일 (다형성)

<a name="one-to-one-polymorphic-table-structure"></a>
#### 테이블 구조

일대일 다형성 관계는 일반적인 일대일 관계와 유사하지만, 자식 모델은 단일 연관을 사용하여 여러 유형의 모델에 속할 수 있습니다. 예를 들어, 블로그 `Post`와 `User`는 `Image` 모델과 다형성 관계를 공유할 수 있습니다. 일대일 다형성 관계를 사용하면 게시물과 사용자와 연결될 수 있는 단일 고유 이미지 테이블을 가질 수 있습니다. 먼저 테이블 구조를 살펴보겠습니다:

```text
posts
    id - integer
    name - string

users
    id - integer
    name - string

images
    id - integer
    url - string
    imageable_type - string
    imageable_id - integer
```



`images` 테이블의 `imageable_id` 및 `imageable_type` 열에 주목하세요. `imageable_id` 열에는 게시물 또는 사용자의 ID 값이 들어 있고, `imageable_type` 열에는 부모 모델의 클래스 이름이 들어 있습니다. `imageable_type` 열은 Eloquent가 `imageable` 관계에 접근할 때 어떤 "타입"의 부모 모델을 반환할지 결정하는 데 사용됩니다. 이 경우, 해당 열에는 `App\Models\Post` 또는 `App\Models\User` 중 하나가 들어갑니다.

<a name="one-to-one-polymorphic-model-structure"></a>
#### 모델 구조

다음으로, 이 관계를 구축하는 데 필요한 모델 정의를 살펴보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Image extends Model
{
    /**
     * Get the parent imageable model (user or post).
     */
    public function imageable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class Post extends Model
{
    /**
     * Get the post's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphOne;

class User extends Model
{
    /**
     * Get the user's image.
     */
    public function image(): MorphOne
    {
        return $this->morphOne(Image::class, 'imageable');
    }
}
```



<a name="one-to-one-polymorphic-retrieving-the-relationship"></a>
#### 관계 가져오기

데이터베이스 테이블과 모델이 정의되면, 모델을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시물의 이미지를 가져오기 위해 `image` 동적 관계 속성에 접근할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

$image = $post->image;
```



다형 모델의 상위 항목은 `morphTo`를 호출하는 메서드의 이름에 접근함으로써 가져올 수 있습니다. 이 경우, 이는 `Image` 모델의 `imageable` 메서드입니다. 따라서 우리는 이 메서드에 동적 관계 속성으로 접근할 것입니다:

```php
use App\Models\Image;

$image = Image::find(1);

$imageable = $image->imageable;
```



`Image` 모델의 `imageable` 관계는 이미지 소유 모델의 유형에 따라 `Post` 또는 `User` 인스턴스를 반환합니다.

<a name="morph-one-to-one-key-conventions"></a>
#### 주요 관례

필요한 경우, 다형성 자식 모델이 사용하는 "id"와 "type" 열의 이름을 지정할 수 있습니다. 지정하는 경우, 항상 관계의 이름을 `morphTo` 메서드의 첫 번째 인수로 전달해야 합니다. 일반적으로 이 값은 메서드 이름과 일치해야 하므로 PHP의 `__FUNCTION__` 상수를 사용할 수 있습니다.

```php
/**
 * Get the model that the image belongs to.
 */
public function imageable(): MorphTo
{
    return $this->morphTo(__FUNCTION__, 'imageable_type', 'imageable_id');
}
```



<a name="one-to-many-polymorphic-relations"></a>
### 일대다 (다형성)

<a name="one-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

일대다 다형성 관계는 일반적인 일대다 관계와 유사합니다. 그러나 자식 모델은 단일 연관을 사용하여 여러 유형의 모델에 속할 수 있습니다. 예를 들어, 애플리케이션 사용자가 게시물과 동영상에 '댓글'을 남길 수 있다고 가정해 보겠습니다. 다형성 관계를 사용하면 단일 `comments` 테이블을 사용하여 게시물과 동영상 모두에 대한 댓글을 포함할 수 있습니다. 먼저, 이 관계를 구축하는 데 필요한 테이블 구조를 살펴보겠습니다:

```text
posts
    id - integer
    title - string
    body - text

videos
    id - integer
    title - string
    url - string

comments
    id - integer
    body - text
    commentable_type - string
    commentable_id - integer
```



<a name="one-to-many-polymorphic-model-structure"></a>
#### 모델 구조

다음으로, 이 관계를 구축하는 데 필요한 모델 정의를 살펴보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class Comment extends Model
{
    /**
     * Get the parent commentable model (post or video).
     */
    public function commentable(): MorphTo
    {
        return $this->morphTo();
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphMany;

class Video extends Model
{
    /**
     * Get all of the video's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable');
    }
}
```



<a name="one-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 가져오기

데이터베이스 테이블과 모델이 정의되면, 모델의 동적 관계 속성을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시물의 모든 댓글에 접근하려면 `comments` 동적 속성을 사용할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->comments as $comment) {
    // ...
}
```



폴리모픽 자식 모델의 부모 역시 `morphTo`를 호출하는 메서드의 이름에 접근하여 가져올 수 있습니다. 이 경우, `Comment` 모델의 `commentable` 메서드입니다. 따라서 댓글의 부모 모델에 접근하기 위해 해당 메서드를 동적 관계 속성으로 접근할 것입니다:

```php
use App\Models\Comment;

$comment = Comment::find(1);

$commentable = $comment->commentable;
```



`Comment` 모델의 `commentable` 관계는 댓글의 부모 모델 유형에 따라 `Post` 또는 `Video` 인스턴스를 반환합니다.

<a name="polymorphic-automatically-hydrating-parent-models-on-children"></a>
#### 자식 모델에서 부모 모델 자동 수화

Eloquent eager loading을 사용하더라도, 자식 모델을 반복하면서 자식 모델에서 부모 모델에 접근하려고 하면 "N + 1" 쿼리 문제가 발생할 수 있습니다:

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->commentable->title;
    }
}
```



위의 예제에서는 "N + 1" 쿼리 문제가 발생했습니다. 이는 모든 `Post` 모델에 대해 댓글이 미리 로드되었음에도 불구하고, Eloquent가 각 자식 `Comment` 모델에 부모 `Post`를 자동으로 채우지 않기 때문입니다.

Eloquent가 부모 모델을 자식 모델에 자동으로 채우도록 하려면, `morphMany` 관계를 정의할 때 `chaperone` 메서드를 호출할 수 있습니다:

```php
class Post extends Model
{
    /**
     * Get all of the post's comments.
     */
    public function comments(): MorphMany
    {
        return $this->morphMany(Comment::class, 'commentable')->chaperone();
    }
}
```



또는 실행 시간에 자동 상위 하이드레이션을 선택하고 싶다면, 관계를 즉시 로드할 때 `chaperone` 모델을 호출할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::with([
    'comments' => fn ($comments) => $comments->chaperone(),
])->get();
```



<a name="one-of-many-polymorphic-relations"></a>
### 다수 중 하나 (다형성)

때때로 한 모델이 여러 관련 모델을 가질 수 있지만, 관계에서 '최신' 또는 '가장 오래된' 관련 모델을 쉽게 가져오고 싶을 때가 있습니다. 예를 들어, `User` 모델이 여러 `Image` 모델과 관련될 수 있지만, 사용자가 업로드한 가장 최근 이미지를 편리하게 다루는 방법을 정의하고 싶을 수 있습니다. 이는 `morphOne` 관계 유형과 `ofMany` 메서드를 결합하여 수행할 수 있습니다:

```php
/**
 * Get the user's most recent image.
 */
public function latestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->latestOfMany();
}
```



마찬가지로, 관계에서 '가장 오래된' 또는 첫 번째 관련 모델을 가져오는 메서드를 정의할 수도 있습니다:

```php
/**
 * Get the user's oldest image.
 */
public function oldestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->oldestOfMany();
}
```



기본적으로, `latestOfMany`와 `oldestOfMany` 메서드는 모델의 기본 키를 기준으로 최신 또는 가장 오래된 관련 모델을 가져옵니다. 기본 키는 정렬 가능해야 합니다. 그러나 때때로 다른 정렬 기준을 사용하여 더 큰 관계에서 단일 모델을 가져오고 싶을 수 있습니다.

예를 들어, `ofMany` 메서드를 사용하면 사용자가 가장 '좋아요'를 많이 받은 이미지를 가져올 수 있습니다. `ofMany` 메서드는 정렬 가능한 열을 첫 번째 인수로 받고, 관련 모델을 쿼리할 때 적용할 집계 함수(`min` 또는 `max`)를 지정합니다:

```php
/**
 * Get the user's most popular image.
 */
public function bestImage(): MorphOne
{
    return $this->morphOne(Image::class, 'imageable')->ofMany('likes', 'max');
}
```



> [!NOTE]
> 보다 발전된 '여러 개 중 하나' 관계를 구성하는 것이 가능합니다. 자세한 정보는 [하나의 '여러 개 중 하나' 문서](#advanced-has-one-of-many-relationships)를 참조하십시오.

<a name="many-to-many-polymorphic-relations"></a>
### 다대다 (다형성)

<a name="many-to-many-polymorphic-table-structure"></a>
#### 테이블 구조

다대다 다형성 관계는 '하나의 다형성' 및 '여러 개 다형성' 관계보다 약간 더 복잡합니다. 예를 들어, `Post` 모델과 `Video` 모델이 `Tag` 모델과 다형성 관계를 공유할 수 있습니다. 이 상황에서 다대다 다형성 관계를 사용하면 앱이 게시물이나 동영상과 연관될 수 있는 고유 태그의 단일 테이블을 가질 수 있습니다. 먼저, 이 관계를 구축하는 데 필요한 테이블 구조를 살펴보겠습니다:

```text
posts
    id - integer
    name - string

videos
    id - integer
    name - string

tags
    id - integer
    name - string

taggables
    tag_id - integer
    taggable_type - string
    taggable_id - integer
```



> [!NOTE]
> 다형 다대다 관계(polymorphic many-to-many relationships)에 들어가기 전에, 일반적인 [다대다 관계](#many-to-many)에 대한 문서를 읽는 것이 도움이 될 수 있습니다.

<a name="many-to-many-polymorphic-model-structure"></a>
#### 모델 구조

다음으로, 모델에서 관계를 정의할 준비가 되었습니다. `Post` 및 `Video` 모델은 모두 기본 Eloquent 모델 클래스에서 제공하는 `morphToMany` 메서드를 호출하는 `tags` 메서드를 포함하게 됩니다.

`morphToMany` 메서드는 관련 모델의 이름과 "관계 이름"을 받습니다. 우리가 중간 테이블 이름과 그 안에 포함된 키에 할당한 이름에 기반하여, 우리는 관계를 "taggable"이라고 부를 것입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Post extends Model
{
    /**
     * Get all of the tags for the post.
     */
    public function tags(): MorphToMany
    {
        return $this->morphToMany(Tag::class, 'taggable');
    }
}
```



<a name="many-to-many-polymorphic-defining-the-inverse-of-the-relationship"></a>
#### 관계의 역함수 정의

다음으로, `Tag` 모델에서, 가능한 각 부모 모델에 대한 메서드를 정의해야 합니다. 따라서 이 예제에서는 `posts` 메서드와 `videos` 메서드를 정의할 것입니다. 이 두 메서드는 모두 `morphedByMany` 메서드의 결과를 반환해야 합니다.

`morphedByMany` 메서드는 관련 모델의 이름과 "관계 이름"을 받아들입니다. 우리가 중간 테이블 이름에 할당한 이름과 그 테이블이 포함하는 키를 기반으로, 우리는 이 관계를 "taggable"로 참조할 것입니다.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphToMany;

class Tag extends Model
{
    /**
     * Get all of the posts that are assigned this tag.
     */
    public function posts(): MorphToMany
    {
        return $this->morphedByMany(Post::class, 'taggable');
    }

    /**
     * Get all of the videos that are assigned this tag.
     */
    public function videos(): MorphToMany
    {
        return $this->morphedByMany(Video::class, 'taggable');
    }
}
```



<a name="many-to-many-polymorphic-retrieving-the-relationship"></a>
#### 관계 가져오기

데이터베이스 테이블과 모델이 정의되면, 모델을 통해 관계에 접근할 수 있습니다. 예를 들어, 게시물의 모든 태그에 접근하려면 `tags` 동적 관계 속성을 사용할 수 있습니다:

```php
use App\Models\Post;

$post = Post::find(1);

foreach ($post->tags as $tag) {
    // ...
}
```



폴리모픽 자식 모델에서 폴리모픽 관계의 부모를 가져오려면 `morphedByMany`에 호출을 수행하는 메서드의 이름에 접근하면 됩니다. 이 경우, `Tag` 모델의 `posts` 또는 `videos` 메서드가 해당됩니다:

```php
use App\Models\Tag;

$tag = Tag::find(1);

foreach ($tag->posts as $post) {
    // ...
}

foreach ($tag->videos as $video) {
    // ...
}
```



<a name="custom-polymorphic-types"></a>
### 사용자 정의 다형성 타입

기본적으로 Laravel은 관련 모델의 "type"을 저장하기 위해 완전한 클래스 이름을 사용합니다. 예를 들어, 위의 일대다 관계 예제에서 `Comment` 모델이 `Post` 또는 `Video` 모델에 속할 수 있는 경우, 기본 `commentable_type`는 각각 `App\Models\Post` 또는 `App\Models\Video`가 됩니다. 그러나 이러한 값을 애플리케이션의 내부 구조와 분리하고 싶을 수 있습니다.

예를 들어, 모델 이름을 "type"으로 사용하는 대신 `post`와 `video`와 같은 간단한 문자열을 사용할 수 있습니다. 이렇게 하면 모델이 이름이 변경되더라도 데이터베이스의 다형성 "type" 열 값이 유효하게 유지됩니다.

```php
use Illuminate\Database\Eloquent\Relations\Relation;

Relation::enforceMorphMap([
    'post' => 'App\Models\Post',
    'video' => 'App\Models\Video',
]);
```



원하신다면 `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드에서 `enforceMorphMap` 메서드를 호출하거나 별도의 서비스 제공자를 생성할 수 있습니다.

모델의 `getMorphClass` 메서드를 사용하여 주어진 모델의 morph 별칭을 런타임에 결정할 수 있습니다. 반대로, `Relation::getMorphedModel` 메서드를 사용하여 morph 별칭과 연결된 완전한 클래스 이름을 결정할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\Relation;

$alias = $post->getMorphClass();

$class = Relation::getMorphedModel($alias);
```



> [!WARNING]
> 기존 애플리케이션에 "morph map"을 추가할 때, 여전히 완전히 제한된 클래스가 포함된 데이터베이스의 모든 변형 가능한 `*_type` 열 값은 해당 "맵" 이름으로 변환되어야 합니다.

<a name="dynamic-relationships"></a>
### 동적 관계

런타임에 Eloquent 모델 간의 관계를 정의하기 위해 `resolveRelationUsing` 메서드를 사용할 수 있습니다. 일반적인 애플리케이션 개발에서는 일반적으로 권장되지 않지만, 때때로 Laravel 패키지를 개발할 때 유용할 수 있습니다.

`resolveRelationUsing` 메서드는 원하는 관계 이름을 첫 번째 인수로 받습니다. 메서드에 전달된 두 번째 인수는 모델 인스턴스를 받아 유효한 Eloquent 관계 정의를 반환하는 클로저여야 합니다. 일반적으로 동적 관계는 [서비스 제공자](/docs/{{version}}/providers)의 boot 메서드 내에서 구성해야 합니다.

```php
use App\Models\Order;
use App\Models\Customer;

Order::resolveRelationUsing('customer', function (Order $orderModel) {
    return $orderModel->belongsTo(Customer::class, 'customer_id');
});
```



> [!WARNING]
> 동적 관계를 정의할 때, 항상 Eloquent 관계 메서드에 명시적인 키 이름 인수를 제공하세요.

<a name="querying-relations"></a>
## 관계 쿼리

모든 Eloquent 관계는 메서드를 통해 정의되므로, 실제로 관련 모델을 로드하기 위해 쿼리를 실행하지 않고도 해당 메서드를 호출하여 관계 인스턴스를 얻을 수 있습니다. 또한 모든 유형의 Eloquent 관계는 [쿼리 빌더](/docs/{{version}}/queries) 역할도 하여, 관계 쿼리를 데이터베이스에 대한 SQL 쿼리를 최종 실행하기 전에 계속해서 제약 조건을 연결(chaining)할 수 있습니다.

예를 들어, 블로그 애플리케이션에서 `User` 모델이 여러 개의 `Post` 모델과 연관되어 있다고 가정해 봅시다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Model
{
    /**
     * Get all of the posts for the user.
     */
    public function posts(): HasMany
    {
        return $this->hasMany(Post::class);
    }
}
```



다음과 같이 `posts` 관계를 조회하고 관계에 추가 제약 조건을 추가할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->posts()->where('active', 1)->get();
```



관계에서 Laravel [쿼리 빌더](/docs/{{version}}/queries)의 모든 메서드를 사용할 수 있으므로, 사용 가능한 모든 메서드에 대해 알아보려면 쿼리 빌더 문서를 꼭 확인하세요.

<a name="chaining-orwhere-clauses-after-relationships"></a>
#### 관계 뒤에 `orWhere` 절 체이닝하기

위 예제에서 보여준 것처럼, 관계를 쿼리할 때 추가 제약 조건을 자유롭게 추가할 수 있습니다. 그러나 관계에 `orWhere` 절을 체이닝할 때는 주의해야 하며, `orWhere` 절은 관계 제약 조건과 동일한 수준에서 논리적으로 그룹화됩니다:

```php
$user->posts()
    ->where('active', 1)
    ->orWhere('votes', '>=', 100)
    ->get();
```



위의 예제는 다음 SQL을 생성합니다. 보시다시피, `or` 절은 쿼리가 100표 이상을 받은 _어떤_ 게시물이라도 반환하도록 지시합니다. 쿼리는 더 이상 특정 사용자에 국한되지 않습니다:

```sql
select *
from posts
where user_id = ? and active = 1 or votes >= 100
```



대부분의 상황에서, 괄호 안의 조건 검사를 그룹화할 때 [논리적 그룹](/docs/{{version}}/queries#logical-grouping)을 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$user->posts()
    ->where(function (Builder $query) {
        return $query->where('active', 1)
            ->orWhere('votes', '>=', 100);
    })
    ->get();
```



위의 예제는 다음과 같은 SQL을 생성합니다. 논리적 그룹화가 제약 조건을 올바르게 그룹화했으며 쿼리가 특정 사용자로 제한되어 있다는 점에 유의하십시오:

```sql
select *
from posts
where user_id = ? and (active = 1 or votes >= 100)
```



<a name="relationship-methods-vs-dynamic-properties"></a>
### 관계 메서드와 동적 속성

Eloquent 관계 쿼리에 추가 제약 조건을 추가할 필요가 없다면, 관계를 속성처럼 접근할 수 있습니다. 예를 들어, 계속해서 우리의 `User`와 `Post` 예제 모델을 사용하면, 사용자의 모든 게시물에 다음과 같이 접근할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

foreach ($user->posts as $post) {
    // ...
}
```



동적 관계 속성은 "지연 로딩(lazy loading)"을 수행합니다. 즉, 실제로 이러한 관계 데이터에 접근할 때만 데이터를 로드합니다. 이로 인해 개발자는 모델을 로드한 후 접근할 것이 확실한 관계를 미리 로드하기 위해 [사전 로딩(eager loading)](#eager-loading)을 자주 사용합니다. 사전 로딩은 모델의 관계를 로드하기 위해 실행해야 하는 SQL 쿼리를 크게 줄여줍니다.

<a name="querying-relationship-existence"></a>
### 관계 존재 여부 쿼리

모델 레코드를 검색할 때, 관계의 존재 여부에 따라 결과를 제한하고 싶을 수 있습니다. 예를 들어, 최소 하나의 댓글을 가진 모든 블로그 게시물을 가져오고 싶다고 가정해봅시다. 이렇게 하려면 관계의 이름을 `has` 및 `orHas` 메서드에 전달할 수 있습니다:

```php
use App\Models\Post;

// Retrieve all posts that have at least one comment...
$posts = Post::has('comments')->get();
```



쿼리를 더욱 맞춤화하기 위해 연산자와 개수 값을 지정할 수도 있습니다:

```php
// Retrieve all posts that have three or more comments...
$posts = Post::has('comments', '>=', 3)->get();
```



중첩된 `has` 문장은 '점(dot)' 표기법을 사용하여 구성할 수 있습니다. 예를 들어, 하나 이상의 이미지를 가진 하나 이상의 댓글이 있는 모든 게시물을 가져올 수 있습니다:

```php
// Retrieve posts that have at least one comment with images...
$posts = Post::has('comments.images')->get();
```



더 많은 성능이 필요하다면 `whereHas`와 `orWhereHas` 방법을 사용하여 `has` 쿼리에 대한 추가 쿼리 제약 조건을 정의할 수 있습니다. 예를 들어, 댓글 내용을 검사하는 것과 같이:

```php
use Illuminate\Database\Eloquent\Builder;

// Retrieve posts with at least one comment containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();

// Retrieve posts with at least ten comments containing words like code%...
$posts = Post::whereHas('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
}, '>=', 10)->get();
```



> [!WARNING]
> Eloquent은 현재 데이터베이스 간 관계 존재 여부를 쿼리하는 것을 지원하지 않습니다. 관계는 동일한 데이터베이스 내에 존재해야 합니다.

<a name="many-to-many-relationship-existence-queries"></a>
#### 다대다 관계 존재 여부 쿼리

`whereAttachedTo` 메서드는 특정 모델이나 모델 컬렉션에 다대다로 연결된 모델을 쿼리할 때 사용할 수 있습니다:

```php
$users = User::whereAttachedTo($role)->get();
```



`whereAttachedTo` 메서드에 [컬렉션](/docs/{{version}}/eloquent-collections) 인스턴스를 제공할 수도 있습니다. 이렇게 하면 Laravel은 컬렉션 내의 모델 중 어느 것과든 연결된 모델을 가져옵니다:

```php
$tags = Tag::whereLike('name', '%laravel%')->get();

$posts = Post::whereAttachedTo($tags)->get();
```



<a name="inline-relationship-existence-queries"></a>
#### 인라인 관계 존재 쿼리

관계 쿼리에 단일의 간단한 where 조건을 첨부하여 관계의 존재 여부를 쿼리하고 싶다면 `whereRelation`, `orWhereRelation`, `whereMorphRelation` 및 `orWhereMorphRelation` 메서드를 사용하는 것이 더 편리할 수 있습니다. 예를 들어, 승인되지 않은 댓글이 있는 모든 게시물을 쿼리할 수 있습니다:

```php
use App\Models\Post;

$posts = Post::whereRelation('comments', 'is_approved', false)->get();
```



물론, 쿼리 빌더의 `where` 메서드 호출처럼, 연산자도 지정할 수 있습니다:

```php
$posts = Post::whereRelation(
    'comments', 'created_at', '>=', now()->minus(hours: 1)
)->get();
```



<a name="querying-relationship-absence"></a>
### 관계 부재 쿼리하기

모델 레코드를 검색할 때, 관계가 없는 경우를 기준으로 결과를 제한하고 싶을 수 있습니다. 예를 들어, 댓글이 전혀 없는 블로그 게시물을 모두 검색하고 싶다고 가정해 보겠습니다. 그렇게 하려면 `doesntHave`와 `orDoesntHave` 메서드에 관계 이름을 전달하면 됩니다:

```php
use App\Models\Post;

$posts = Post::doesntHave('comments')->get();
```



더 많은 성능이 필요하다면 `doesntHave` 쿼리에 추가 쿼리 제약 조건을 추가하기 위해 `whereDoesntHave` 및 `orWhereDoesntHave` 방법을 사용할 수 있습니다. 예를 들어, 댓글의 내용을 검사하는 것과 같이:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments', function (Builder $query) {
    $query->where('content', 'like', 'code%');
})->get();
```



중첩된 관계에 대해 쿼리를 실행하기 위해 "dot" 표기법을 사용할 수 있습니다. 예를 들어, 다음 쿼리는 댓글이 없는 모든 게시물과, 아무 댓글도 금지된 사용자가 작성하지 않은 게시물을 가져옵니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::whereDoesntHave('comments.author', function (Builder $query) {
    $query->where('banned', 1);
})->get();
```



<a name="querying-morph-to-relationships"></a>
### Morph To 관계 쿼리하기

"morph to" 관계의 존재를 쿼리하려면, `whereHasMorph` 및 `whereDoesntHaveMorph` 메서드를 사용할 수 있습니다. 이 메서드들은 첫 번째 인수로 관계의 이름을 받습니다. 다음으로, 쿼리에 포함하고자 하는 관련 모델들의 이름을 인수로 받습니다. 마지막으로, 관계 쿼리를 사용자 정의하는 클로저를 제공할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;
use App\Models\Video;
use Illuminate\Database\Eloquent\Builder;

// Retrieve comments associated to posts or videos with a title like code%...
$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();

// Retrieve comments associated to posts with a title not like code%...
$comments = Comment::whereDoesntHaveMorph(
    'commentable',
    Post::class,
    function (Builder $query) {
        $query->where('title', 'like', 'code%');
    }
)->get();
```



관련 다형 모델의 "type"에 따라 쿼리 제약 조건을 가끔 추가해야 할 수도 있습니다. `whereHasMorph` 메서드에 전달된 클로저는 두 번째 인수로 `$type` 값을 받을 수 있습니다. 이 인수를 통해 작성 중인 쿼리의 "type"을 확인할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph(
    'commentable',
    [Post::class, Video::class],
    function (Builder $query, string $type) {
        $column = $type === Post::class ? 'content' : 'title';

        $query->where($column, 'like', 'code%');
    }
)->get();
```



때때로 'morph to' 관계의 부모의 자식을 조회하고 싶을 때가 있습니다. 주어진 모델에 대한 적절한 morph 타입 매핑을 자동으로 결정하는 `whereMorphedTo` 및 `whereNotMorphedTo` 메서드를 사용하여 이를 달성할 수 있습니다. 이 메서드들은 첫 번째 인수로 `morphTo` 관계의 이름을, 두 번째 인수로 관련된 부모 모델을 받습니다:

```php
$comments = Comment::whereMorphedTo('commentable', $post)
    ->orWhereMorphedTo('commentable', $video)
    ->get();
```



<a name="querying-all-morph-to-related-models"></a>
#### 모든 관련 모델 쿼리하기

가능한 다형성 모델 배열을 전달하는 대신, 와일드카드 값으로 `*`를 제공할 수 있습니다. 이는 Laravel에게 데이터베이스에서 가능한 모든 다형성 유형을 가져오도록 지시합니다. 이 작업을 수행하기 위해 Laravel은 추가 쿼리를 실행합니다:

```php
use Illuminate\Database\Eloquent\Builder;

$comments = Comment::whereHasMorph('commentable', '*', function (Builder $query) {
    $query->where('title', 'like', 'foo%');
})->get();
```



<a name="aggregating-related-models"></a>
## 관련 모델 집계하기

<a name="counting-related-models"></a>
### 관련 모델 수 세기

때때로 실제 모델을 로드하지 않고 특정 관계에 대한 관련 모델의 수를 세고 싶을 때가 있습니다. 이를 위해 `withCount` 메서드를 사용할 수 있습니다. `withCount` 메서드는 결과 모델에 `{relation}_count` 속성을 배치합니다:

```php
use App\Models\Post;

$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count;
}
```



배열을 `withCount` 메서드에 전달함으로써, 여러 관계에 대한 'counts'를 추가하고 쿼리에 추가적인 제약 조건을 넣을 수도 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount(['votes', 'comments' => function (Builder $query) {
    $query->where('content', 'like', 'code%');
}])->get();

echo $posts[0]->votes_count;
echo $posts[0]->comments_count;
```



관계 수 결과에 별칭을 지정하여 같은 관계에 대해 여러 개의 수를 허용할 수도 있습니다:

```php
use Illuminate\Database\Eloquent\Builder;

$posts = Post::withCount([
    'comments',
    'comments as pending_comments_count' => function (Builder $query) {
        $query->where('approved', false);
    },
])->get();

echo $posts[0]->comments_count;
echo $posts[0]->pending_comments_count;
```



<a name="deferred-count-loading"></a>
#### 지연된 카운트 로딩

`loadCount` 방법을 사용하면, 부모 모델이 이미 가져와진 후에도 관계 카운트를 로드할 수 있습니다:

```php
$book = Book::first();

$book->loadCount('genres');
```



카운트 쿼리에 추가적인 쿼리 제약 조건을 설정해야 하는 경우, 계산하려는 관계를 키로 하는 배열을 전달할 수 있습니다. 배열 값은 쿼리 빌더 인스턴스를 받는 클로저여야 합니다:

```php
$book->loadCount(['reviews' => function (Builder $query) {
    $query->where('rating', 5);
}]);
```



<a name="relationship-counting-and-custom-select-statements"></a>
#### 관계 계산 및 사용자 정의 선택문

`withCount`를 `select` 문과 결합하는 경우, `select` 메서드 후에 `withCount`를 호출해야 합니다:

```php
$posts = Post::select(['title', 'body'])
    ->withCount('comments')
    ->get();
```



<a name="other-aggregate-functions"></a>
### 기타 집계 함수

`withCount` 메서드 외에도, Eloquent는 `withMin`, `withMax`, `withAvg`, `withSum`, `withExists` 메서드를 제공합니다. 이 메서드들은 결과 모델에 `{relation}_{function}_{column}` 속성을 추가합니다:

```php
use App\Models\Post;

$posts = Post::withSum('comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->comments_sum_votes;
}
```



집계 함수의 결과를 다른 이름으로 접근하고 싶다면, 자신만의 별칭을 지정할 수 있습니다:

```php
$posts = Post::withSum('comments as total_comments', 'votes')->get();

foreach ($posts as $post) {
    echo $post->total_comments;
}
```



`loadCount` 방법과 마찬가지로, 이러한 방법들의 지연(deferred) 버전도 사용할 수 있습니다. 이러한 추가 집계 연산은 이미 가져온 Eloquent 모델에서도 수행할 수 있습니다:

```php
$post = Post::first();

$post->loadSum('comments', 'votes');
```



이 집계 메서드를 `select` 문과 결합하고 있다면, `select` 메서드 이후에 집계 메서드를 호출하도록 하십시오:

```php
$posts = Post::select(['title', 'body'])
    ->withExists('comments')
    ->get();
```



<a name="counting-related-models-on-morph-to-relationships"></a>
### Counting Related Models on Morph To Relationships

If you would like to eager load a "morph to" relationship, as well as related model counts for the various entities that may be returned by that relationship, you may utilize the `with` method in combination with the `morphTo` relationship's `morphWithCount` method.

In this example, let's assume that `Photo` and `Post` models may create `ActivityFeed` models. We will assume the `ActivityFeed` model defines a "morph to" relationship named `parentable` that allows us to retrieve the parent `Photo` or `Post` model for a given `ActivityFeed` instance. Additionally, let's assume that `Photo` models "have many" `Tag` models and `Post` models "have many" `Comment` models.

Now, let's imagine we want to retrieve `ActivityFeed` instances and eager load the `parentable` parent models for each `ActivityFeed` instance. In addition, we want to retrieve the number of tags that are associated with each parent photo and the number of comments that are associated with each parent post:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::with([
    'parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWithCount([
            Photo::class => ['tags'],
            Post::class => ['comments'],
        ]);
    }])->get();
```



<a name="morph-to-deferred-count-loading"></a>
#### 연기된 개수 로딩

이미 `ActivityFeed` 모델 세트를 가져왔고 이제 활동 피드와 관련된 다양한 `parentable` 모델의 중첩 관계 개수를 로드하고 싶다고 가정해봅시다. 이를 수행하기 위해 `loadMorphCount` 메서드를 사용할 수 있습니다:

```php
$activities = ActivityFeed::with('parentable')->get();

$activities->loadMorphCount('parentable', [
    Photo::class => ['tags'],
    Post::class => ['comments'],
]);
```



<a name="eager-loading"></a>
## 즉시 로딩(Eager Loading)

Eloquent 관계를 속성으로 접근할 때, 관련 모델들은 "지연 로딩(lazy loaded)"됩니다. 이는 실제로 관계 데이터가 속성에 처음 접근할 때까지 로드되지 않는다는 것을 의미합니다. 그러나 Eloquent는 부모 모델을 쿼리할 때 관계를 "즉시 로드(eager load)"할 수 있습니다. 즉시 로딩은 "N + 1" 쿼리 문제를 완화합니다. N + 1 쿼리 문제를 설명하기 위해, `Book` 모델이 `Author` 모델에 "속해 있다(belongs to)"고 가정해 보겠습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }
}
```



이제 모든 책과 그 저자를 찾아봅시다:

```php
use App\Models\Book;

$books = Book::all();

foreach ($books as $book) {
    echo $book->author->name;
}
```



이 루프는 데이터베이스 테이블 내의 모든 책을 가져오기 위해 하나의 쿼리를 실행한 다음, 각 책의 저자를 가져오기 위해 추가로 쿼리를 실행합니다. 따라서 책이 25권 있다면, 위 코드에서는 총 26개의 쿼리가 실행됩니다: 원래 책을 위한 1개의 쿼리와 각 책의 저자를 가져오기 위한 추가 25개의 쿼리입니다.

다행히도, eager loading을 사용하면 이 작업을 단 두 개의 쿼리로 줄일 수 있습니다. 쿼리를 작성할 때 `with` 메서드를 사용하여 어떤 관계를 eager loading할지 지정할 수 있습니다:

```php
$books = Book::with('author')->get();

foreach ($books as $book) {
    echo $book->author->name;
}
```



이 작업을 위해 실행되는 쿼리는 단 두 개뿐입니다 - 하나는 모든 책을 가져오는 쿼리이고, 다른 하나는 모든 책에 대한 모든 저자를 가져오는 쿼리입니다:

```sql
select * from books

select * from authors where id in (1, 2, 3, 4, 5, ...)
```



<a name="eager-loading-multiple-relationships"></a>
#### 여러 관계를 한 번에 eager loading 하기

가끔 여러 다른 관계를 eager load 해야 할 때가 있습니다. 그렇게 하려면, 단순히 관계들의 배열을 `with` 메서드에 전달하면 됩니다:

```php
$books = Book::with(['author', 'publisher'])->get();
```



<a name="nested-eager-loading"></a>
#### 중첩된 즉시 로딩

관계의 관계를 즉시 로딩하려면 "점(dot)" 구문을 사용할 수 있습니다. 예를 들어, 책의 모든 저자와 저자의 모든 개인 연락처를 즉시 로딩해 보겠습니다:

```php
$books = Book::with('author.contacts')->get();
```



또는 `with` 메서드에 중첩 배열을 제공하여 중첩된 eager 로드 관계를 지정할 수 있으며, 이는 여러 중첩 관계를 eager 로드할 때 편리할 수 있습니다:

```php
$books = Book::with([
    'author' => [
        'contacts',
        'publisher',
    ],
])->get();
```



<a name="nested-eager-loading-morphto-relationships"></a>
#### 중첩된 즉시 로딩 `morphTo` 관계

만약 `morphTo` 관계를 즉시 로딩하고 싶고, 그 관계에 의해 반환될 수 있는 다양한 엔티티에 대한 중첩 관계 또한 로딩하고 싶다면, `with` 메서드를 `morphTo` 관계의 `morphWith` 메서드와 함께 사용할 수 있습니다. 이 메서드를 설명하기 위해, 다음 모델을 고려해 봅시다:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```



이 예제에서, `Event`, `Photo`, `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정해 보겠습니다. 또한 `Event` 모델은 `Calendar` 모델에 속하고, `Photo` 모델은 `Tag` 모델과 연관되며, `Post` 모델은 `Author` 모델에 속한다고 가정해 보겠습니다.

이러한 모델 정의와 관계를 사용하면, `ActivityFeed` 모델 인스턴스를 가져오고 모든 `parentable` 모델과 각각의 중첩 관계를 eager load할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$activities = ActivityFeed::query()
    ->with(['parentable' => function (MorphTo $morphTo) {
        $morphTo->morphWith([
            Event::class => ['calendar'],
            Photo::class => ['tags'],
            Post::class => ['author'],
        ]);
    }])->get();
```



<a name="eager-loading-specific-columns"></a>
#### 특정 열에 대한 즉시 로딩

항상 조회하는 관계의 모든 열이 필요하지 않을 수 있습니다. 이러한 이유로 Eloquent는 조회하고자 하는 관계의 열을 지정할 수 있도록 허용합니다:

```php
$books = Book::with('author:id,name,book_id')->get();
```



> [!WARNING]
> 이 기능을 사용할 때는 항상 `id` 열과 관련 외래 키 열들을 가져오고자 하는 열 목록에 포함해야 합니다.

<a name="eager-loading-by-default"></a>
#### 기본적으로 지연 로딩 대신 선행 로딩(Eager Loading)

때때로 모델을 가져올 때 항상 일부 관계를 로드하고 싶을 수 있습니다. 이를 달성하기 위해 모델에 `$with` 속성을 정의할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Book extends Model
{
    /**
     * The relationships that should always be loaded.
     *
     * @var array
     */
    protected $with = ['author'];

    /**
     * Get the author that wrote the book.
     */
    public function author(): BelongsTo
    {
        return $this->belongsTo(Author::class);
    }

    /**
     * Get the genre of the book.
     */
    public function genre(): BelongsTo
    {
        return $this->belongsTo(Genre::class);
    }
}
```



단일 쿼리에 대해 `$with` 속성에서 항목을 제거하려면 `without` 메서드를 사용할 수 있습니다:

```php
$books = Book::without('author')->get();
```



단일 쿼리에 대해 `$with` 속성 내의 모든 항목을 재정의하려면 `withOnly` 메서드를 사용할 수 있습니다:

```php
$books = Book::withOnly('genre')->get();
```



<a name="constraining-eager-loads"></a>
### 적극적 로드 제약하기

때때로 관계를 적극적으로 로드하고 싶지만, 적극적 로드 쿼리에 추가적인 쿼리 조건도 지정하고자 할 수 있습니다. 이는 배열을 `with` 메서드에 전달하여 수행할 수 있으며, 여기서 배열 키는 관계 이름이고 배열 값은 적극적 로드 쿼리에 추가 제약 조건을 더하는 클로저입니다:

```php
use App\Models\User;

$users = User::with(['posts' => function ($query) {
    $query->where('title', 'like', '%code%');
}])->get();
```



이 예제에서 Eloquent는 게시물의 `title` 열에 `code`라는 단어가 포함된 게시물만 미리 로드합니다. 미리 로딩 작업을 추가로 사용자 정의하려면 다른 [쿼리 빌더](/docs/{{version}}/queries) 메서드를 호출할 수 있습니다:

```php
$users = User::with(['posts' => function ($query) {
    $query->orderBy('created_at', 'desc');
}])->get();
```



<a name="constraining-eager-loading-of-morph-to-relationships"></a>
#### `morphTo` 관계의 조기 로딩 제한하기

`morphTo` 관계를 조기 로딩하는 경우, Eloquent는 각 유형의 관련 모델을 가져오기 위해 여러 쿼리를 실행합니다. 이러한 쿼리 각각에 추가 제약 조건을 `MorphTo` 관계의 `constrain` 메서드를 사용하여 추가할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Relations\MorphTo;

$comments = Comment::with(['commentable' => function (MorphTo $morphTo) {
    $morphTo->constrain([
        Post::class => function ($query) {
            $query->whereNull('hidden_at');
        },
        Video::class => function ($query) {
            $query->where('type', 'educational');
        },
    ]);
}])->get();
```



이 예에서, Eloquent는 숨겨지지 않은 게시물과 `type` 값이 'educational'인 비디오만 미리 로드합니다.

<a name="constraining-eager-loads-with-relationship-existence"></a>
#### 관계 존재로 미리 로드 제한하기

때때로 동일한 조건을 기반으로 관계를 로드하는 동안 관계의 존재 여부를 확인해야 할 수도 있습니다. 예를 들어, 주어진 쿼리 조건에 맞는 하위 `Post` 모델을 가진 `User` 모델만 검색하면서, 동시에 일치하는 게시물을 미리 로드하고 싶을 수 있습니다. 이를 `withWhereHas` 메서드를 사용하여 수행할 수 있습니다:

```php
use App\Models\User;

$users = User::withWhereHas('posts', function ($query) {
    $query->where('featured', true);
})->get();
```



<a name="lazy-eager-loading"></a>
### 지연된 적극적 로딩

때때로 부모 모델이 이미 검색된 후에 관계를 적극적으로 로드해야 할 때가 있습니다. 예를 들어, 관련 모델을 로드할지 동적으로 결정해야 하는 경우에 유용할 수 있습니다:

```php
use App\Models\Book;

$books = Book::all();

if ($condition) {
    $books->load('author', 'publisher');
}
```



필요하다면 eager loading 쿼리에 추가적인 쿼리 제약 조건을 설정하기 위해, 로드하려는 관계를 키로 하는 배열을 전달할 수 있습니다. 배열 값은 쿼리 인스턴스를 받는 클로저 인스턴스여야 합니다:

```php
$author->load(['books' => function ($query) {
    $query->orderBy('published_date', 'asc');
}]);
```



관계가 이미 로드되지 않은 경우에만 관계를 로드하려면, `loadMissing` 메서드를 사용하세요:

```php
$book->loadMissing('author');
```



<a name="nested-lazy-eager-loading-morphto"></a>
#### 중첩 지연 및 즉시 로딩 `morphTo`

특정 `morphTo` 관계와, 해당 관계를 통해 반환될 수 있는 다양한 엔티티의 중첩 관계를 즉시 로딩하고 싶다면, `loadMorph` 메서드를 사용할 수 있습니다.

이 메서드는 첫 번째 인수로 `morphTo` 관계의 이름을 받고, 두 번째 인수로 모델/관계 쌍의 배열을 받습니다. 이 메서드를 설명하기 위해, 다음 모델을 고려해 보겠습니다:

```php
<?php

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\MorphTo;

class ActivityFeed extends Model
{
    /**
     * Get the parent of the activity feed record.
     */
    public function parentable(): MorphTo
    {
        return $this->morphTo();
    }
}
```



이 예제에서, `Event`, `Photo`, `Post` 모델이 `ActivityFeed` 모델을 생성할 수 있다고 가정해 보겠습니다. 또한 `Event` 모델은 `Calendar` 모델에 속하고, `Photo` 모델은 `Tag` 모델과 연관되며, `Post` 모델은 `Author` 모델에 속한다고 가정해 보겠습니다.

이러한 모델 정의와 관계를 사용하면, `ActivityFeed` 모델 인스턴스를 가져오고 모든 `parentable` 모델과 각각의 중첩 관계를 eager load 할 수 있습니다:

```php
$activities = ActivityFeed::with('parentable')
    ->get()
    ->loadMorph('parentable', [
        Event::class => ['calendar'],
        Photo::class => ['tags'],
        Post::class => ['author'],
    ]);
```



<a name="automatic-eager-loading"></a>
### 자동 탐욕적 로딩

많은 경우에, Laravel은 당신이 접근하는 관계를 자동으로 탐욕적으로 로드할 수 있습니다. 자동 탐욕적 로딩을 활성화하려면, 애플리케이션의 `AppServiceProvider`에서 `boot` 메서드 내에서 `Model::automaticallyEagerLoadRelationships` 메서드를 호출해야 합니다:

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::automaticallyEagerLoadRelationships();
}
```



이 기능이 활성화되면, Laravel은 이전에 로드되지 않은 관계를 자동으로 로드하려고 시도합니다. 예를 들어, 다음과 같은 시나리오를 고려해 보십시오:

```php
use App\Models\User;

$users = User::all();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        foreach ($post->comments as $comment) {
            echo $comment->content;
        }
    }
}
```



일반적으로 위의 코드는 각 사용자의 게시물을 가져오기 위해 사용자마다 쿼리를 실행하고, 각 게시물의 댓글을 가져오기 위해 게시물마다 쿼리를 실행합니다. 그러나 `automaticallyEagerLoadRelationships` 기능이 활성화되면, 라라벨은 검색된 사용자 중 어느 한 사용자의 게시물에 접근하려 할 때 사용자 컬렉션의 모든 사용자에 대한 게시물을 자동으로 [지연 탐욕 로드](#lazy-eager-loading)합니다. 마찬가지로, 검색된 게시물의 댓글에 접근하려 할 때, 모든 게시물에 대한 댓글이 원래 검색된 모든 게시물에 대해 지연 탐욕 로드됩니다.

자동 탐욕 로딩을 전역적으로 활성화하고 싶지 않은 경우, 여전히 컬렉션에서 `withRelationshipAutoloading` 메서드를 호출하여 단일 Eloquent 컬렉션 인스턴스에 대해 이 기능을 활성화할 수 있습니다:

```php
$users = User::where('vip', true)->get();

return $users->withRelationshipAutoloading();
```



<a name="preventing-lazy-loading"></a>
### 게으른 로딩 방지

앞서 논의한 바와 같이, 관계를 즉시 로딩(eager loading)하는 것은 종종 애플리케이션의 성능에 상당한 이점을 줄 수 있습니다. 따라서 원하신다면, Laravel에 관계의 게으른 로딩(lazy loading)을 항상 방지하도록 지시할 수 있습니다. 이를 달성하기 위해, 기본 Eloquent 모델 클래스가 제공하는 `preventLazyLoading` 메서드를 호출하면 됩니다. 일반적으로, 이 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출해야 합니다.

`preventLazyLoading` 메서드는 선택적인 불리언(boolean) 인수를 받아, 게으른 로딩을 방지할지를 나타냅니다. 예를 들어, 프로덕션 환경에서는 게으른 로딩된 관계가 실수로 코드에 존재하더라도 애플리케이션이 정상적으로 작동하게 하기 위해 비프로덕션 환경에서만 게으른 로딩을 비활성화할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Model;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Model::preventLazyLoading(! $this->app->isProduction());
}
```



지연 로딩을 방지한 후, 애플리케이션이 어떤 Eloquent 관계든 지연 로딩하려고 시도할 때 Eloquent는 `Illuminate\Database\LazyLoadingViolationException` 예외를 발생시킬 것입니다.

`handleLazyLoadingViolationsUsing` 메서드를 사용하여 지연 로딩 위반의 동작을 사용자 정의할 수 있습니다. 예를 들어, 이 메서드를 사용하여 지연 로딩 위반을 예외로 애플리케이션 실행을 중단시키는 대신 로그만 남기도록 지시할 수 있습니다:

```php
Model::handleLazyLoadingViolationUsing(function (Model $model, string $relation) {
    $class = $model::class;

    info("Attempted to lazy load [{$relation}] on model [{$class}].");
});
```



<a name="inserting-and-updating-related-models"></a>
## 관련 모델 삽입 및 업데이트

<a name="the-save-method"></a>
### `save` 메서드

Eloquent는 관계에 새로운 모델을 추가할 수 있는 편리한 메서드를 제공합니다. 예를 들어, 게시물에 새 댓글을 추가해야 할 수도 있습니다. `Comment` 모델에서 `post_id` 속성을 수동으로 설정하는 대신, 관계의 `save` 메서드를 사용하여 댓글을 삽입할 수 있습니다:

```php
use App\Models\Comment;
use App\Models\Post;

$comment = new Comment(['message' => 'A new comment.']);

$post = Post::find(1);

$post->comments()->save($comment);
```



`comments` 관계를 동적 속성으로 액세스하지 않았다는 점에 유의하세요. 대신 관계의 인스턴스를 얻기 위해 `comments` 메서드를 호출했습니다. `save` 메서드는 새로운 `Comment` 모델에 적절한 `post_id` 값을 자동으로 추가합니다.

여러 관련 모델을 저장해야 하는 경우, `saveMany` 메서드를 사용할 수 있습니다:

```php
$post = Post::find(1);

$post->comments()->saveMany([
    new Comment(['message' => 'A new comment.']),
    new Comment(['message' => 'Another new comment.']),
]);
```



`save` 및 `saveMany` 메서드는 주어진 모델 인스턴스를 지속시키지만, 새롭게 지속된 모델을 부모 모델에 이미 로드된 메모리 내 관계에 추가하지는 않습니다. `save` 또는 `saveMany` 메서드를 사용한 후 관계에 접근할 계획이 있다면, 모델과 그 관계를 다시 불러오기 위해 `refresh` 메서드를 사용하는 것이 좋습니다:

```php
$post->comments()->save($comment);

$post->refresh();

// All comments, including the newly saved comment...
$post->comments;
```



<a name="the-push-method"></a>
#### 모델과 관계를 재귀적으로 저장하기

모델과 그와 관련된 모든 관계를 `save`하고 싶다면, `push` 메서드를 사용할 수 있습니다. 이 예제에서 `Post` 모델은 그 모델의 댓글과 댓글 작성자와 함께 저장됩니다:

```php
$post = Post::find(1);

$post->comments[0]->message = 'Message';
$post->comments[0]->author->name = 'Author Name';

$post->push();
```



`pushQuietly` 메서드는 어떤 이벤트도 발생시키지 않고 모델과 관련된 관계를 저장하는 데 사용할 수 있습니다:

```php
$post->pushQuietly();
```



<a name="the-create-method"></a>
### `create` 방법

`save` 및 `saveMany` 방법 외에도 배열 속성을 받아 모델을 생성하고 데이터베이스에 삽입하는 `create` 방법을 사용할 수 있습니다. `save`와 `create`의 차이점은 `save`가 전체 Eloquent 모델 인스턴스를 받는 반면, `create`는 일반 PHP `array`를 받는다는 점입니다. 새로 생성된 모델은 `create` 메서드에 의해 반환됩니다:

```php
use App\Models\Post;

$post = Post::find(1);

$comment = $post->comments()->create([
    'message' => 'A new comment.',
]);
```



여러 관련 모델을 생성하기 위해 `createMany` 방법을 사용할 수 있습니다:

```php
$post = Post::find(1);

$post->comments()->createMany([
    ['message' => 'A new comment.'],
    ['message' => 'Another new comment.'],
]);
```



`createQuietly`와 `createManyQuietly` 메서드는 어떤 이벤트도 발생시키지 않고 모델을 생성하는 데 사용할 수 있습니다:

```php
$user = User::find(1);

$user->posts()->createQuietly([
    'title' => 'Post title.',
]);

$user->posts()->createManyQuietly([
    ['title' => 'First post.'],
    ['title' => 'Second post.'],
]);
```



`findOrNew`, `firstOrNew`, `firstOrCreate` 및 `updateOrCreate` 메서드를 사용하여 [관계에 대한 모델을 생성하고 업데이트](/docs/{{version}}/eloquent#upserts)할 수도 있습니다.

> [!NOTE]
> `create` 메서드를 사용하기 전에, [대량 할당](/docs/{{version}}/eloquent#mass-assignment) 문서를 반드시 검토하세요.

<a name="updating-belongs-to-relationships"></a>
### 소속 관계(Belongs To Relationships)

자식 모델을 새 부모 모델에 할당하려는 경우 `associate` 메서드를 사용할 수 있습니다. 이 예제에서 `User` 모델은 `Account` 모델에 대한 `belongsTo` 관계를 정의합니다. 이 `associate` 메서드는 자식 모델의 외래 키를 설정합니다:

```php
use App\Models\Account;

$account = Account::find(10);

$user->account()->associate($account);

$user->save();
```



자식 모델에서 부모 모델을 제거하려면 `dissociate` 메서드를 사용할 수 있습니다. 이 메서드는 관계의 외래 키를 `null`로 설정합니다:

```php
$user->account()->dissociate();

$user->save();
```



<a name="updating-many-to-many-relationships"></a>
### 다대다 관계

<a name="attaching-detaching"></a>
#### 연결 / 연결 해제

Eloquent는 또한 다대다 관계 작업을 더 편리하게 수행할 수 있는 메서드를 제공합니다. 예를 들어, 사용자가 여러 역할을 가질 수 있고, 역할 또한 여러 사용자를 가질 수 있다고 가정해 보겠습니다. `attach` 메서드를 사용하여 관계의 중간 테이블에 레코드를 삽입하여 사용자가 역할을 연결할 수 있습니다:

```php
use App\Models\User;

$user = User::find(1);

$user->roles()->attach($roleId);
```



모델에 관계를 연결할 때, 중간 테이블에 삽입될 추가 데이터를 배열로 전달할 수도 있습니다:

```php
$user->roles()->attach($roleId, ['expires' => $expires]);
```



때때로 사용자로부터 역할을 제거해야 할 필요가 있을 수 있습니다. 다대다 관계 레코드를 제거하려면 `detach` 메서드를 사용하십시오. `detach` 메서드는 중간 테이블에서 해당 레코드를 삭제하지만, 두 모델은 데이터베이스에 남아 있게 됩니다:

```php
// Detach a single role from the user...
$user->roles()->detach($roleId);

// Detach all roles from the user...
$user->roles()->detach();
```



편의를 위해, `attach`와 `detach`는 ID 배열을 입력으로 받을 수도 있습니다:

```php
$user = User::find(1);

$user->roles()->detach([1, 2, 3]);

$user->roles()->attach([
    1 => ['expires' => $expires],
    2 => ['expires' => $expires],
]);
```



<a name="syncing-associations"></a>
#### 연관 동기화

여러 개 대 여러 개 연관을 구성하려면 `sync` 방법을 사용할 수도 있습니다. `sync` 방법은 중간 테이블에 배치할 ID 배열을 받습니다. 주어진 배열에 없는 ID는 중간 테이블에서 제거됩니다. 따라서 이 작업이 완료된 후에는 주어진 배열에 있는 ID만 중간 테이블에 존재하게 됩니다:

```php
$user->roles()->sync([1, 2, 3]);
```



다음 ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다:

```php
$user->roles()->sync([1 => ['expires' => true], 2, 3]);
```



동기화된 각 모델 ID와 함께 동일한 중간 테이블 값을 삽입하려면, `syncWithPivotValues` 방법을 사용할 수 있습니다:

```php
$user->roles()->syncWithPivotValues([1, 2, 3], ['active' => true]);
```



주어진 배열에 없는 기존 ID를 분리하고 싶지 않다면, `syncWithoutDetaching` 방법을 사용할 수 있습니다:

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```



<a name="toggling-associations"></a>
#### 연관 관계 전환

다대다 관계는 또한 주어진 관련 모델 ID의 첨부 상태를 "전환"하는 `toggle` 메서드를 제공합니다. 주어진 ID가 현재 첨부되어 있으면 분리됩니다. 마찬가지로, 현재 분리되어 있으면 첨부됩니다:

```php
$user->roles()->toggle([1, 2, 3]);
```



다음 ID와 함께 추가 중간 테이블 값을 전달할 수도 있습니다:

```php
$user->roles()->toggle([
    1 => ['expires' => true],
    2 => ['expires' => true],
]);
```



<a name="transactional-pivot-operations"></a>
#### 트랜잭션 피벗 연산

위에서 논의된 각 피벗 연산에는 `OrFail` 버전(`attachOrFail`, `detachOrFail`, `syncOrFail`, `syncWithoutDetachingOrFail`, `toggleOrFail`)이 있으며, 이 버전은 연산을 데이터베이스 트랜잭션 내에서 감싸서 예외가 발생하면 모든 변경 사항이 자동으로 롤백되도록 합니다:

```php
$user->roles()->attachOrFail([1, 2, 3]);

$user->roles()->syncOrFail([1, 2, 3]);
```



<a name="updating-a-record-on-the-intermediate-table"></a>
#### 중간 테이블의 레코드 업데이트하기

관계의 중간 테이블에서 기존 행을 업데이트해야 하는 경우, `updateExistingPivot` 메서드를 사용할 수 있습니다. 이 메서드는 중간 레코드의 외래 키와 업데이트할 속성 배열을 받습니다:

```php
$user = User::find(1);

$user->roles()->updateExistingPivot($roleId, [
    'active' => false,
]);
```



<a name="touching-parent-timestamps"></a>
## 부모 타임스탬프 갱신하기

모델이 다른 모델과 `belongsTo` 또는 `belongsToMany` 관계를 정의할 때, 예를 들어 `Post`에 속하는 `Comment`와 같은 경우, 자식 모델이 업데이트될 때 부모의 타임스탬프를 갱신하는 것이 유용한 경우가 있습니다.

예를 들어, `Comment` 모델이 업데이트될 때, 소유한 `Post`의 `updated_at` 타임스탬프를 자동으로 "터치"하여 현재 날짜와 시간으로 설정하고 싶을 수 있습니다. 이를 수행하려면, 자식 모델에서 관계 이름을 포함하는 `Touches` 속성을 사용하여 자식 모델이 업데이트될 때 해당 관계의 `updated_at` 타임스탬프가 갱신되도록 할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Touches;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

#[Touches(['post'])]
class Comment extends Model
{
    /**
     * Get the post that the comment belongs to.
     */
    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

> [!WARNING]
> 부모 모델의 타임스탬프는 자식 모델이 Eloquent의 `save` 메서드를 사용하여 업데이트될 때만 갱신됩니다.
{% endraw %}
