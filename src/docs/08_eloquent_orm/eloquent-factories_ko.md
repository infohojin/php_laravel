---
layout: docs
title: "웅변: 공장"
---

{% raw %}
# 웅변: 공장

- [소개](#introduction)
- [모델 정의 공장](#defining-model-factories)
- 생성 모델 팩토리 (#generating-factories)
- [Factory States](#factory-states)
- 팩토리 콜백 (#factory-callbacks)
- 팩토리를 이용한 모델 만들기 (#creating-models-using-factories)
- [모델 생성](#instantiating-models)
- Persisting Models(#persisting-models)
- [시퀀스](#sequences)
- [공장 관계](#factory-relationships)
- Has Many Relationships (#has-many-relationships)
- [속한 관계](#belongs-to-relationships)
- [Many to Many Relationships](#many-to-many-relationships)
- 폴리모프 관계 (#polymorphic-relationships)
- 공장 내 관계 정의 (#defining-relationships-within-factories)
- 기존 관계 모델 재활용 (#recycling-an-existing-model-for-relationships)

<a name="introduction"></a>
## 소개

애플리케이션을 테스트하거나 데이터베이스에 시드할 때 데이터베이스에 몇 개의 레코드를 삽입해야 할 수 있습니다. Laravel 을 사용하면 각 열의 값을 수동으로 지정하는 대신 모델 팩토리를 사용하여 각 Eloquent models(/docs/{{version}}/eloquent) 에 대한 기본 속성 집합을 정의할 수 있습니다。

팩토리를 작성하는 방법의 예를 보려면 애플리케이션의 `database/factories/UserFactory.php` 파일을 살펴보세요. 이 팩토리는 모든 새로운 Laravel 애플리케이션에 포함되어 있으며 다음과 같은 팩토리 정의를 포함합니다：

```php
namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
{
    /**
     * The current password being used by the factory.
     */
    protected static ?string $password;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * Indicate that the model's email address should be unverified.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```



보시다시피, 가장 기본적인 형태에서 팩토리는 Laravel의 기본 팩토리 클래스를 확장하고 `definition` 메서드를 정의하는 클래스입니다. `definition` 메서드는 팩토리를 사용하여 모델을 생성할 때 적용되어야 하는 기본 속성 값 세트를 반환합니다.

`fake` 헬퍼를 통해 팩토리는 [Faker](https://github.com/FakerPHP/Faker) PHP 라이브러리에 접근할 수 있으며, 이를 통해 테스트 및 시딩을 위해 다양한 종류의 랜덤 데이터를 편리하게 생성할 수 있습니다.

> [!NOTE]
> `config/app.php` 구성 파일에서 `faker_locale` 옵션을 업데이트하여 애플리케이션의 Faker 로케일을 변경할 수 있습니다.

<a name="defining-model-factories"></a>
## 모델 팩토리 정의하기

<a name="generating-factories"></a>
### 팩토리 생성

팩토리를 생성하려면 `make:factory` [Artisan 명령어](/docs/{{version}}/artisan)를 실행하세요:

```shell
php artisan make:factory PostFactory
```



새 공장 클래스는 당신의 `database/factories` 디렉토리에 배치될 것입니다.

<a name="factory-and-model-discovery-conventions"></a>
#### 모델 및 공장 발견 규칙

공장을 정의한 후에는 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 모델에 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 공장 인스턴스를 생성할 수 있습니다.

`HasFactory` 트레이트의 `factory` 메서드는 규칙을 사용하여 트레이트가 할당된 모델에 적절한 공장을 결정합니다. 특히, 메서드는 모델 이름과 일치하고 `Factory` 접미사가 붙은 클래스 이름을 가진 공장을 `Database\Factories` 네임스페이스에서 찾습니다. 이러한 규칙이 특정 애플리케이션이나 공장에 적용되지 않는 경우, 모델에 `UseFactory` 속성을 추가하여 모델의 공장을 수동으로 지정할 수 있습니다.

```php
use Illuminate\Database\Eloquent\Attributes\UseFactory;
use Database\Factories\Administration\FlightFactory;

#[UseFactory(FlightFactory::class)]
class Flight extends Model
{
    // ...
}
```



또는 모델에서 `newFactory` 메서드를 덮어써서 모델의 해당 팩토리 인스턴스를 직접 반환할 수 있습니다:

```php
use Database\Factories\Administration\FlightFactory;

/**
 * Create a new factory instance for the model.
 */
protected static function newFactory()
{
    return FlightFactory::new();
}
```



그런 다음 해당 공장에 `UseModel` 속성을 사용하여 모델을 지정합니다:

```php
use App\Administration\Flight;
use Illuminate\Database\Eloquent\Factories\Attributes\UseModel;
use Illuminate\Database\Eloquent\Factories\Factory;

#[UseModel(Flight::class)]
class FlightFactory extends Factory
{
    // ...
}
```



<a name="factory-states"></a>
### 공장 상태

상태 조작 메서드를 사용하면 모델 팩토리에 임의의 조합으로 적용할 수 있는 개별 수정 사항을 정의할 수 있습니다. 예를 들어, `Database\Factories\UserFactory` 공장은 기본 속성 값 중 하나를 수정하는 `suspended` 상태 메서드를 포함할 수 있습니다.

상태 변환 메서드는 일반적으로 Laravel의 기본 공장 클래스에서 제공하는 `state` 메서드를 호출합니다. `state` 메서드는 팩토리에 정의된 원시 속성 배열을 전달받는 클로저를 수락하며, 수정할 속성 배열을 반환해야 합니다:

```php
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    });
}
```



<a name="trashed-state"></a>
#### "삭제됨(Trashed)" 상태

만약 당신의 Eloquent 모델이 [소프트 삭제](/docs/{{version}}/eloquent#soft-deleting)될 수 있다면, 생성된 모델이 이미 "소프트 삭제" 상태여야 함을 나타내기 위해 내장 `trashed` 상태 메서드를 호출할 수 있습니다. `trashed` 상태를 수동으로 정의할 필요는 없으며, 모든 팩토리에서 자동으로 사용할 수 있습니다:

```php
use App\Models\User;

$user = User::factory()->trashed()->create();
```



<a name="factory-callbacks"></a>
### 팩토리 콜백

팩토리 콜백은 `afterMaking`와 `afterCreating` 메서드를 사용하여 등록되며, 모델을 만들거나 생성한 후 추가 작업을 수행할 수 있습니다. 이러한 콜백은 팩토리 클래스에서 `configure` 메서드를 정의하여 등록해야 합니다. 이 메서드는 팩토리가 인스턴스화될 때 Laravel에 의해 자동으로 호출됩니다:

```php
namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class UserFactory extends Factory
{
    /**
     * Configure the model factory.
     */
    public function configure(): static
    {
        return $this->afterMaking(function (User $user) {
            // ...
        })->afterCreating(function (User $user) {
            // ...
        });
    }

    // ...
}
```



특정 상태에 고유한 추가 작업을 수행하기 위해 상태 메서드 내에서 팩토리 콜백을 등록할 수도 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * Indicate that the user is suspended.
 */
public function suspended(): Factory
{
    return $this->state(function (array $attributes) {
        return [
            'account_status' => 'suspended',
        ];
    })->afterMaking(function (User $user) {
        // ...
    })->afterCreating(function (User $user) {
        // ...
    });
}
```



<a name="creating-models-using-factories"></a>
## 팩토리를 사용하여 모델 생성하기

<a name="instantiating-models"></a>
### 모델 인스턴스화하기

팩토리를 정의한 후에는, 모델에 `Illuminate\Database\Eloquent\Factories\HasFactory` 트레이트가 제공하는 정적 `factory` 메서드를 사용하여 해당 모델의 팩토리 인스턴스를 생성할 수 있습니다. 모델을 생성하는 몇 가지 예제를 살펴보겠습니다. 먼저, 모델을 데이터베이스에 저장하지 않고 생성하기 위해 `make` 메서드를 사용할 것입니다:

```php
use App\Models\User;

$user = User::factory()->make();
```



`count` 방법을 사용하여 여러 모델의 컬렉션을 만들 수 있습니다:

```php
$users = User::factory()->count(3)->make();
```



<a name="applying-states"></a>
#### 상태 적용

모델에 [상태](#factory-states)를 적용할 수도 있습니다. 모델에 여러 상태 변환을 적용하고 싶다면, 상태 변환 메서드를 직접 호출하면 됩니다:

```php
$users = User::factory()->count(5)->suspended()->make();
```



<a name="overriding-attributes"></a>
#### 속성 재정의

모델의 일부 기본 값을 재정의하고 싶다면, `make` 메서드에 값 배열을 전달할 수 있습니다. 지정된 속성만 교체되며, 나머지 속성은 팩토리에서 지정한 기본 값으로 그대로 유지됩니다:

```php
$user = User::factory()->make([
    'name' => 'Abigail Otwell',
]);
```



또는 `state` 메서드를 공장 인스턴스에서 직접 호출하여 인라인 상태 변환을 수행할 수 있습니다:

```php
$user = User::factory()->state([
    'name' => 'Abigail Otwell',
])->make();
```



> [!NOTE]
> [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)는 팩토리를 사용하여 모델을 생성할 때 자동으로 비활성화됩니다.

<a name="persisting-models"></a>
### 모델 지속

`create` 메서드는 모델 인스턴스를 생성하고 Eloquent의 `save` 메서드를 사용하여 데이터베이스에 지속합니다:

```php
use App\Models\User;

// Create a single App\Models\User instance...
$user = User::factory()->create();

// Create three App\Models\User instances...
$users = User::factory()->count(3)->create();
```



`create` 메서드에 속성 배열을 전달하여 팩토리의 기본 모델 속성을 재정의할 수 있습니다:

```php
$user = User::factory()->create([
    'name' => 'Abigail',
]);
```



<a name="sequences"></a>
### 시퀀스

때때로 생성된 각 모델에 대해 주어진 모델 속성의 값을 번갈아 가며 설정하고 싶을 수 있습니다. 이는 상태 변환을 시퀀스로 정의하여 달성할 수 있습니다. 예를 들어, 생성된 각 사용자에 대해 `admin` 열의 값을 `Y`과 `N` 사이에서 번갈아 가며 설정하고 싶을 수 있습니다:

```php
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        ['admin' => 'Y'],
        ['admin' => 'N'],
    ))
    ->create();
```



이 예제에서는 다섯 명의 사용자가 `admin` 값으로 `Y`를 가지도록 생성되며, 다섯 명의 사용자가 `admin` 값으로 `N`를 가지도록 생성됩니다.

필요한 경우, 시퀀스 값으로 클로저를 포함할 수 있습니다. 시퀀스가 새 값을 필요로 할 때마다 클로저가 호출됩니다:

```php
use Illuminate\Database\Eloquent\Factories\Sequence;

$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],
    ))
    ->create();
```



시퀀스 클로저 내에서 클로저에 주입된 시퀀스 인스턴스에서 `$index` 속성에 접근할 수 있습니다. `$index` 속성에는 지금까지 시퀀스를 통해 발생한 반복 횟수가 포함되어 있습니다:

```php
$users = User::factory()
    ->count(10)
    ->state(new Sequence(
        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],
    ))
    ->create();
```



편의를 위해, 시퀀스는 내부적으로 단순히 `state` 메서드를 호출하는 `sequence` 방법을 사용하여 적용할 수도 있습니다. `sequence` 메서드는 클로저 또는 시퀀스화된 속성의 배열을 허용합니다:

```php
$users = User::factory()
    ->count(2)
    ->sequence(
        ['name' => 'First User'],
        ['name' => 'Second User'],
    )
    ->create();
```



<a name="factory-relationships"></a>
## 팩토리 관계

<a name="has-many-relationships"></a>
### 다대다 관계

다음으로, Laravel의 플루언트 팩토리 메서드를 사용하여 Eloquent 모델 관계를 구축하는 방법을 살펴보겠습니다. 먼저, 우리 애플리케이션에 `App\Models\User` 모델과 `App\Models\Post` 모델이 있다고 가정해 보겠습니다. 또한 `User` 모델이 `Post`와 `hasMany` 관계를 정의한다고 가정합니다. 우리는 Laravel의 팩토리가 제공하는 `has` 메서드를 사용하여 세 개의 게시물을 가진 사용자를 생성할 수 있습니다. `has` 메서드는 팩토리 인스턴스를 받습니다:

```php
use App\Models\Post;
use App\Models\User;

$user = User::factory()
    ->has(Post::factory()->count(3))
    ->create();
```



관례에 따라 `Post` 모델을 `has` 메서드에 전달할 때, Laravel은 `User` 모델이 관계를 정의하는 `posts` 메서드를 반드시 가져야 한다고 가정합니다. 필요하다면, 조작하고자 하는 관계의 이름을 명시적으로 지정할 수도 있습니다:

```php
$user = User::factory()
    ->has(Post::factory()->count(3), 'posts')
    ->create();
```



물론 관련 모델에 대해 상태 조작을 수행할 수 있습니다. 또한 상태 변경이 상위 모델에 대한 액세스를 필요로 하는 경우 클로저 기반 상태 변환을 전달할 수 있습니다:

```php
$user = User::factory()
    ->has(
        Post::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['user_type' => $user->type];
            })
    )
    ->create();
```



<a name="has-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

편의를 위해, 관계를 구축할 때 Laravel의 매직 팩토리 관계 메서드를 사용할 수 있습니다. 예를 들어, 다음 예제는 관례를 사용하여 관련 모델이 `User` 모델의 `posts` 관계 메서드를 통해 생성되어야 함을 결정합니다:

```php
$user = User::factory()
    ->hasPosts(3)
    ->create();
```



팩토리 관계를 만들기 위해 매직 메소드를 사용할 때, 관련 모델에서 덮어쓸 속성 배열을 전달할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, [
        'published' => false,
    ])
    ->create();
```



여러 속성 배열을 전달하여 각 모델별 상태로 관련 모델을 생성할 수도 있습니다. Laravel은 각 배열을 순서대로 적용합니다:

```php
$user = User::factory()
    ->hasPosts(
        ['title' => 'First Post'],
        ['title' => 'Second Post'],
        ['title' => 'Third Post'],
    )
    ->create();
```



상태 변경이 부모 모델에 대한 접근을 필요로 하는 경우, 클로저 기반 상태 변환을 제공할 수 있습니다:

```php
$user = User::factory()
    ->hasPosts(3, function (array $attributes, User $user) {
        return ['user_type' => $user->type];
    })
    ->create();
```



<a name="belongs-to-relationships"></a>
### 소속 관계

이제 팩토리를 사용하여 "has many" 관계를 구축하는 방법을 살펴보았으니, 관계의 역방향을 살펴보겠습니다. `for` 메서드는 팩토리가 생성한 모델이 속하는 부모 모델을 정의하는 데 사용할 수 있습니다. 예를 들어, 하나의 사용자에 속하는 세 개의 `App\Models\Post` 모델 인스턴스를 생성할 수 있습니다:

```php
use App\Models\Post;
use App\Models\User;

$posts = Post::factory()
    ->count(3)
    ->for(User::factory()->state([
        'name' => 'Jessica Archer',
    ]))
    ->create();
```



만약 생성하려는 모델과 연관되어야 하는 부모 모델 인스턴스가 이미 있다면, 모델 인스턴스를 `for` 메서드에 전달할 수 있습니다:

```php
$user = User::factory()->create();

$posts = Post::factory()
    ->count(3)
    ->for($user)
    ->create();
```



<a name="belongs-to-relationships-using-magic-methods"></a>
#### 매직 메서드 사용

편의를 위해, Laravel의 매직 팩토리 관계 메서드를 사용하여 "belongs to" 관계를 정의할 수 있습니다. 예를 들어, 다음 예제는 관례를 사용하여 세 개의 게시물이 `Post` 모델의 `user` 관계에 속해야 함을 결정합니다:

```php
$posts = Post::factory()
    ->count(3)
    ->forUser([
        'name' => 'Jessica Archer',
    ])
    ->create();
```



<a name="many-to-many-relationships"></a>
### 다대다 관계

[has many 관계](#has-many-relationships)처럼, "다대다" 관계는 `has` 방법을 사용하여 생성할 수 있습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->has(Role::factory()->count(3))
    ->create();
```



<a name="pivot-table-attributes"></a>
#### 피벗 테이블 속성

모델을 연결하는 피벗 / 중간 테이블에 설정해야 하는 속성을 정의해야 하는 경우, `hasAttached` 메서드를 사용할 수 있습니다. 이 메서드는 두 번째 인수로 피벗 테이블 속성 이름과 값의 배열을 받습니다:

```php
use App\Models\Role;
use App\Models\User;

$user = User::factory()
    ->hasAttached(
        Role::factory()->count(3),
        ['active' => true]
    )
    ->create();
```



상태 변경이 관련 모델에 대한 접근을 필요로 하는 경우, 클로저 기반의 상태 변환을 제공할 수 있습니다:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory()
            ->count(3)
            ->state(function (array $attributes, User $user) {
                return ['name' => $user->name.' Role'];
            }),
        ['active' => true]
    )
    ->create();
```



각 관련 모델에 대한 고유한 피벗 데이터를 제공하기 위해 피벗 배열의 배열을 전달할 수도 있습니다:

```php
$user = User::factory()
    ->hasAttached(
        Role::factory(),
        [
            ['active' => true],
            ['active' => false],
        ]
    )
    ->create();
```



이미 생성하려는 모델에 연결하고 싶은 모델 인스턴스가 있는 경우, 모델 인스턴스를 `hasAttached` 메서드에 전달할 수 있습니다. 이 예제에서는 동일한 세 역할이 세 사용자 모두에 연결됩니다:

```php
$roles = Role::factory()->count(3)->create();

$users = User::factory()
    ->count(3)
    ->hasAttached($roles, ['active' => true])
    ->create();
```



<a name="many-to-many-relationships-using-magic-methods"></a>
#### 매직 메서드 사용하기

편의를 위해, Laravel의 매직 팩토리 관계 메서드를 사용하여 다대다 관계를 정의할 수 있습니다. 예를 들어, 다음 예제는 관습을 사용하여 관련 모델이 `User` 모델의 `roles` 관계 메서드를 통해 생성되어야 함을 결정합니다:

```php
$user = User::factory()
    ->hasRoles(1, [
        'name' => 'Editor'
    ])
    ->create();
```



<a name="polymorphic-relationships"></a>
### 다형성 관계

[다형성 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)도 팩토리를 사용하여 생성할 수 있습니다. 다형성 "morph many" 관계는 일반적인 "has many" 관계와 같은 방식으로 생성됩니다. 예를 들어, 만약 `App\Models\Post` 모델이 `App\Models\Comment` 모델과 `morphMany` 관계를 가지고 있다면:

```php
use App\Models\Post;

$post = Post::factory()->hasComments(3)->create();
```



<a name="morph-to-relationships"></a>
#### 관계형 전환

마법 메서드는 `morphTo` 관계를 생성하는 데 사용될 수 없습니다. 대신, `for` 메서드를 직접 사용해야 하며 관계의 이름을 명시적으로 제공해야 합니다. 예를 들어, `Comment` 모델이 `commentable` 메서드를 가지고 있어서 `morphTo` 관계를 정의한다고 가정해 보겠습니다. 이러한 상황에서는 `for` 메서드를 직접 사용하여 단일 게시물에 속하는 세 개의 댓글을 생성할 수 있습니다:

```php
$comments = Comment::factory()->count(3)->for(
    Post::factory(), 'commentable'
)->create();
```



<a name="polymorphic-many-to-many-relationships"></a>
#### 다형성 다대다 관계

다형성 "다대다" (`morphToMany` / `morphedByMany`) 관계는 비다형성 "다대다" 관계를 만드는 것과 똑같이 생성될 수 있습니다:

```php
use App\Models\Tag;
use App\Models\Video;

$video = Video::factory()
    ->hasAttached(
        Tag::factory()->count(3),
        ['public' => true]
    )
    ->create();
```



물론, 마법 같은 `has` 방법을 사용하여 다형적인 '다대다' 관계를 생성할 수도 있습니다:

```php
$video = Video::factory()
    ->hasTags(3, ['public' => true])
    ->create();
```



<a name="defining-relationships-within-factories"></a>
### 공장 내 관계 정의하기

모델 공장에서 관계를 정의하려면 일반적으로 관계의 외래 키에 새 공장 인스턴스를 할당합니다. 이는 일반적으로 `belongsTo` 및 `morphTo` 관계와 같은 '역방향' 관계에 대해 수행됩니다. 예를 들어, 게시물을 생성할 때 새 사용자를 생성하고 싶다면 다음과 같이 할 수 있습니다:

```php
use App\Models\User;

/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```



관계의 열이 그것을 정의하는 팩토리에 따라 달라지는 경우 속성에 클로저를 할당할 수 있습니다. 클로저는 팩토리에서 평가된 속성 배열을 받게 됩니다:

```php
/**
 * Define the model's default state.
 *
 * @return array<string, mixed>
 */
public function definition(): array
{
    return [
        'user_id' => User::factory(),
        'user_type' => function (array $attributes) {
            return User::find($attributes['user_id'])->type;
        },
        'title' => fake()->title(),
        'content' => fake()->paragraph(),
    ];
}
```



<a name="recycling-an-existing-model-for-relationships"></a>
### 관계를 위해 기존 모델 재활용하기

다른 모델과 공통 관계를 공유하는 모델이 있는 경우, `recycle` 방법을 사용하여 공장(factory)에서 생성된 모든 관계에 대해 관련 모델의 단일 인스턴스가 재활용되도록 할 수 있습니다.

예를 들어, 티켓이 항공사와 항공편에 속하고, 항공편 또한 항공사에 속한다고 가정해보겠습니다. 티켓을 생성할 때, 티켓과 항공편 모두에 동일한 항공사를 사용하고 싶을 때가 있을 수 있으므로, 항공사 인스턴스를 `recycle` 방법에 전달할 수 있습니다.

```php
Ticket::factory()
    ->recycle(Airline::factory()->create())
    ->create();
```



`recycle` 방법은 공통 사용자나 팀에 속한 모델이 있는 경우 특히 유용할 수 있습니다.

`recycle` 방법도 기존 모델 모음을 허용합니다. `recycle` 방법에 모음이 제공되면, 팩토리가 해당 유형의 모델이 필요할 때 모음에서 무작위로 모델이 선택됩니다:

```php
Ticket::factory()
    ->recycle($airlines)
    ->create();
```
{% endraw %}
