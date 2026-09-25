---
layout: docs
title: "Eloquent: Mutators & Casting"
---

{% raw %}
---
layout: docs
title: "Eloquent: Mutators & Casting"
---

# Eloquent: Mutators & Casting

- [Introduction](#introduction)
- [Accessors and Mutators](#accessors-and-mutators)
    - [Defining an Accessor](#defining-an-accessor)
    - [Defining a Mutator](#defining-a-mutator)
- [Attribute Casting](#attribute-casting)
    - [Array and JSON Casting](#array-and-json-casting)
    - [Vector Casting](#vector-casting)
    - [Binary Casting](#binary-casting)
    - [Date Casting](#date-casting)
    - [Enum Casting](#enum-casting)
    - [Encrypted Casting](#encrypted-casting)
    - [Query Time Casting](#query-time-casting)
- [Custom Casts](#custom-casts)
    - [Value Object Casting](#value-object-casting)
    - [Array / JSON Serialization](#array-json-serialization)
    - [Inbound Casting](#inbound-casting)
    - [Cast Parameters](#cast-parameters)
    - [Comparing Cast Values](#comparing-cast-values)
    - [Castables](#castables)

<a name="introduction"></a>
## Introduction

Accessors, mutators, and attribute casting allow you to transform Eloquent attribute values when you retrieve or set them on model instances. For example, you may want to use the [Laravel encrypter](/docs/{{version}}/encryption) to encrypt a value while it is stored in the database, and then automatically decrypt the attribute when you access it on an Eloquent model. Or, you may want to convert a JSON string that is stored in your database to an array when it is accessed via your Eloquent model.

<a name="accessors-and-mutators"></a>
## Accessors and Mutators

<a name="defining-an-accessor"></a>
### Defining an Accessor

An accessor transforms an Eloquent attribute value when it is accessed. To define an accessor, create a protected method on your model to represent the accessible attribute. This method name should correspond to the "camel case" representation of the true underlying model attribute / database column when applicable.

In this example, we'll define an accessor for the `first_name` attribute. The accessor will automatically be called by Eloquent when attempting to retrieve the value of the `first_name` attribute. All attribute accessor / mutator methods must declare a return type-hint of `Illuminate\Database\Eloquent\Casts\Attribute`:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the user's first name.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
        );
    }
}
```



모든 접근자 메서드는 속성이 어떻게 접근되고, 선택적으로 변경될 것인지를 정의하는 `Attribute` 인스턴스를 반환합니다. 이 예제에서는 속성이 어떻게 접근될 것인지만 정의하고 있습니다. 이를 위해 `Attribute` 클래스 생성자에 `get` 인수를 제공합니다.

보시다시피, 컬럼의 원래 값이 접근자에 전달되어 값을 조작하고 반환할 수 있습니다. 접근자의 값을 확인하려면 모델 인스턴스에서 `first_name` 속성에 간단히 접근하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$firstName = $user->first_name;
```



> [!NOTE]
> 이 계산된 값을 모델의 배열/JSON 표현에 추가하고 싶다면, [이를 추가해야 합니다](/docs/{{version}}/eloquent-serialization#appending-values-to-json).

<a name="building-value-objects-from-multiple-attributes"></a>
#### 여러 속성에서 값 객체(Building Value Objects) 만들기

때로는 접근자가 여러 모델 속성을 단일 "값 객체"로 변환해야 할 수도 있습니다. 이렇게 하려면, `get` 클로저가 `$attributes`라는 두 번째 인수를 받을 수 있으며, 이 인수는 클로저에 자동으로 제공되고 모델의 현재 모든 속성을 포함하는 배열을 담게 됩니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    );
}
```



<a name="accessor-caching"></a>
#### 접근자 캐싱

접근자에서 값 객체를 반환할 때, 값 객체에 가해진 모든 변경 사항은 모델이 저장되기 전에 자동으로 모델에 동기화됩니다. 이는 Eloquent가 접근자를 통해 반환된 인스턴스를 유지하여 접근자가 호출될 때마다 동일한 인스턴스를 반환할 수 있기 때문에 가능합니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Line 1 Value';
$user->address->lineTwo = 'Updated Address Line 2 Value';

$user->save();
```



그러나 문자열이나 불리언과 같은 원시 값에 대해 캐싱을 활성화하고 싶은 경우가 있을 수 있습니다. 특히 이러한 값들이 계산적으로 비용이 많이 드는 경우에는 더욱 그렇습니다. 이를 달성하기 위해, 액세서(accessor)를 정의할 때 `shouldCache` 메서드를 호출할 수 있습니다:

```php
protected function hash(): Attribute
{
    return Attribute::make(
        get: fn (string $value) => bcrypt(gzuncompress($value)),
    )->shouldCache();
}
```



속성의 객체 캐싱 동작을 비활성화하려면 속성을 정의할 때 `withoutObjectCaching` 메서드를 호출할 수 있습니다:

```php
/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
    )->withoutObjectCaching();
}
```



<a name="defining-a-mutator"></a>
### 변환기 정의하기

변환기는 Eloquent 속성 값을 설정할 때 변환합니다. 변환기를 정의하려면 속성을 정의할 때 `set` 인수를 제공할 수 있습니다. 이제 `first_name` 속성에 대한 변환기를 정의해 봅시다. 이 변환기는 모델에서 `first_name` 속성의 값을 설정하려고 시도할 때 자동으로 호출됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Interact with the user's first name.
     */
    protected function firstName(): Attribute
    {
        return Attribute::make(
            get: fn (string $value) => ucfirst($value),
            set: fn (string $value) => strtolower($value),
        );
    }
}
```



뮤테이터 클로저는 속성에 설정되는 값을 받아 이 값을 조작하고 조작된 값을 반환할 수 있습니다. 뮤테이터를 사용하려면 Eloquent 모델에서 `first_name` 속성만 설정하면 됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->first_name = 'Sally';
```



이 예제에서는 `set` 콜백이 `Sally` 값과 함께 호출됩니다. 그런 다음 변형자는 `strtolower` 함수를 이름에 적용하고 그 결과 값을 모델의 내부 `$attributes` 배열에 설정합니다.

<a name="mutating-multiple-attributes"></a>
#### 여러 속성 변형하기

때로는 변형자가 기본 모델에 여러 속성을 설정해야 할 수도 있습니다. 이를 위해 `set` 클로저에서 배열을 반환할 수 있습니다. 배열의 각 키는 모델과 연관된 기본 속성/데이터베이스 열에 해당해야 합니다:

```php
use App\Support\Address;
use Illuminate\Database\Eloquent\Casts\Attribute;

/**
 * Interact with the user's address.
 */
protected function address(): Attribute
{
    return Attribute::make(
        get: fn (mixed $value, array $attributes) => new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two'],
        ),
        set: fn (Address $value) => [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ],
    );
}
```



<a name="attribute-casting"></a>
## Attribute Casting

Attribute casting provides functionality similar to accessors and mutators without requiring you to define any additional methods on your model. Instead, your model's `casts` method provides a convenient way of converting attributes to common data types.

The `casts` method should return an array where the key is the name of the attribute being cast and the value is the type you wish to cast the column to. The supported cast types are:

<div class="content-list" markdown="1">

- `array`
- `AsFluent::class`
- `AsStringable::class`
- `AsUri::class`
- `AsVector::class`
- `boolean`
- `collection`
- `date`
- `datetime`
- `immutable_date`
- `immutable_datetime`
- <code>decimal:&lt;precision&gt;</code>
- `double`
- `encrypted`
- `encrypted:array`
- `encrypted:collection`
- `encrypted:object`
- `float`
- `hashed`
- `integer`
- `object`
- `real`
- `string`
- `timestamp`

</div>

To demonstrate attribute casting, let's cast the `is_admin` attribute, which is stored in our database as an integer (`0` or `1`) to a boolean value:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'is_admin' => 'boolean',
        ];
    }
}
```



캐스트를 정의한 후에는, `is_admin` 속성은 데이터베이스에 값이 정수로 저장되어 있더라도 접근할 때 항상 불리언으로 캐스트됩니다:

```php
$user = App\Models\User::find(1);

if ($user->is_admin) {
    // ...
}
```



실행 시간에 새 임시 캐스트를 추가해야 하는 경우, `mergeCasts` 메서드를 사용할 수 있습니다. 이러한 캐스트 정의는 모델에 이미 정의된 캐스트에 추가됩니다:

```php
$user->mergeCasts([
    'is_admin' => 'integer',
    'options' => 'object',
]);
```



> [!WARNING]
> `null` 속성은 캐스팅되지 않습니다. 또한, 관계와 같은 이름을 가진 캐스트(또는 속성)를 정의하거나 모델의 기본 키에 캐스트를 할당해서는 안 됩니다.

<a name="stringable-casting"></a>
#### 문자열로 변환 가능한 캐스팅

모델 속성을 [플루언트 Illuminate\Support\Stringable 객체](/docs/{{version}}/strings#fluent-strings-method-list)로 캐스팅하려면 `Illuminate\Database\Eloquent\Casts\AsStringable` 캐스트 클래스를 사용할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\AsStringable;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'directory' => AsStringable::class,
        ];
    }
}
```



<a name="array-and-json-casting"></a>
### 배열 및 JSON 변환

`array` 변환은 직렬화된 JSON으로 저장된 열을 다룰 때 특히 유용합니다. 예를 들어, 데이터베이스에 `JSON` 또는 `TEXT` 필드 유형이 직렬화된 JSON을 포함하고 있는 경우, 해당 속성에 `array` 변환을 추가하면 Eloquent 모델에서 해당 속성에 접근할 때 자동으로 PHP 배열로 역직렬화됩니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => 'array',
        ];
    }
}
```



캐스트가 정의되면 `options` 속성에 접근할 수 있으며, JSON에서 PHP 배열로 자동으로 역직렬화됩니다. `options` 속성의 값을 설정하면, 주어진 배열이 저장을 위해 JSON으로 자동으로 직렬화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$options = $user->options;

$options['key'] = 'value';

$user->options = $options;

$user->save();
```



JSON 속성의 단일 필드를 더 간결한 문법으로 업데이트하려면, [속성을 대량 할당 가능하도록 설정](/docs/{{version}}/eloquent#mass-assignment-json-columns)하고 `update` 메서드를 호출할 때 `->` 연산자를 사용할 수 있습니다:

```php
$user = User::find(1);

$user->update(['options->key' => 'value']);
```



<a name="json-and-unicode"></a>
#### JSON 및 유니코드

배열 속성을 이스케이프되지 않은 유니코드 문자와 함께 JSON으로 저장하고 싶다면, `json:unicode` 캐스트를 사용할 수 있습니다:

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => 'json:unicode',
    ];
}
```



<a name="array-object-and-collection-casting"></a>
#### 배열 객체 및 컬렉션 캐스팅

표준 `array` 캐스트는 많은 응용 프로그램에 충분하지만, 몇 가지 단점이 있습니다. `array` 캐스트는 원시 타입을 반환하기 때문에 배열의 오프셋을 직접 수정하는 것은 불가능합니다. 예를 들어, 다음 코드는 PHP 오류를 발생시킬 것입니다:

```php
$user = User::find(1);

$user->options['key'] = $value;
```



이를 해결하기 위해, Laravel은 JSON 속성을 [ArrayObject](https://www.php.net/manual/en/class.arrayobject.php) 클래스으로 캐스팅하는 `AsArrayObject` 캐스트를 제공합니다. 이 기능은 Laravel의 [커스텀 캐스트](#custom-casts) 구현을 사용하여 구현되며, 이를 통해 Laravel은 변형된 객체를 지능적으로 캐시하고 변환하여 개별 오프셋이 PHP 오류를 발생시키지 않고 수정될 수 있도록 합니다. `AsArrayObject` 캐스트를 사용하려면 단순히 속성에 할당하면 됩니다:

```php
use Illuminate\Database\Eloquent\Casts\AsArrayObject;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsArrayObject::class,
    ];
}
```



마찬가지로, Laravel은 JSON 속성을 Laravel [Collection](/docs/{{version}}/collections) 인스턴스로 캐스팅하는 `AsCollection` 캐스트를 제공합니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::class,
    ];
}
```



기본적으로, `AsArrayObject` 또는 `AsCollection`으로 캐스팅된 속성에 `null`를 할당하면 데이터베이스에 JSON `null` 값이 저장됩니다. 대신 `null` 값을 네이티브 SQL `NULL` 값으로 저장하고 싶다면, 캐스트를 정의할 때 `nullable` 메서드를 호출할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::nullable(),
    ];
}
```



`nullable` 메서드는 맞춤 컬렉션 클래스와 결합될 수도 있습니다:

```php
'options' => AsCollection::nullable(OptionCollection::class),
```



`AsArrayObject` 캐스트는 동일한 동작을 가진 `nullable` 메서드도 제공합니다.

`AsCollection` 캐스트가 Laravel의 기본 컬렉션 클래스 대신 사용자 정의 컬렉션 클래스를 인스턴스화하기를 원한다면, 캐스트 인수로 컬렉션 클래스 이름을 제공할 수 있습니다:

```php
use App\Collections\OptionCollection;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::using(OptionCollection::class),
    ];
}
```



`of` 방법은 컬렉션 항목을 컬렉션의 [mapInto 메서드](/docs/{{version}}/collections#method-mapinto)를 통해 지정된 클래스에 매핑해야 함을 나타내는 데 사용될 수 있습니다:

```php
use App\ValueObjects\Option;
use Illuminate\Database\Eloquent\Casts\AsCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'options' => AsCollection::of(Option::class)
    ];
}
```



컬렉션을 객체에 매핑할 때, 객체는 인스턴스가 데이터베이스에 JSON으로 직렬화되는 방식을 정의하기 위해 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Support\Arrayable;
use JsonSerializable;

class Option implements Arrayable, JsonSerializable
{
    public string $name;
    public mixed $value;
    public bool $isLocked;

    /**
     * Create a new Option instance.
     */
    public function __construct(array $data)
    {
        $this->name = $data['name'];
        $this->value = $data['value'];
        $this->isLocked = $data['is_locked'];
    }

    /**
     * Get the instance as an array.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function toArray(): array
    {
        return [
            'name' => $this->name,
            'value' => $this->value,
            'is_locked' => $this->isLocked,
        ];
    }

    /**
     * Specify the data which should be serialized to JSON.
     *
     * @return array{name: string, data: string, is_locked: bool}
     */
    public function jsonSerialize(): array
    {
        return $this->toArray();
    }
}
```



<a name="vector-casting"></a>
### 벡터 캐스팅

`Illuminate\Database\Eloquent\Casts\AsVector` 캐스트 클래스를 사용하여 데이터베이스 벡터 열을 PHP 배열로 그리고 PHP 배열에서 캐스팅할 수 있습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsVector;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'embedding' => AsVector::class,
    ];
}
```



속성을 설정할 때, 캐스트는 PHP 배열 또는 Laravel 컬렉션과 같은 `Arrayable` 인스턴스를 허용합니다. 속성을 가져올 때, 캐스트는 부동 소수점 숫자의 배열을 반환합니다.

<a name="binary-casting"></a>
### 이진 캐스팅

Eloquent 모델이 모델의 자동 증가 ID 열 외에 [이진 타입](/docs/{{version}}/migrations#column-method-binary) `uuid` 또는 `ulid` 열을 가지고 있는 경우, `AsBinary` 캐스트를 사용하여 해당 값을 이진 표현으로 자동으로 캐스팅하고 되돌릴 수 있습니다:

```php
use Illuminate\Database\Eloquent\Casts\AsBinary;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'uuid' => AsBinary::uuid(),
        'ulid' => AsBinary::ulid(),
    ];
}
```



모델에서 캐스트가 정의되면 객체 인스턴스나 문자열에 UUID / ULID 속성 값을 설정할 수 있습니다. Eloquent는 자동으로 값을 이진 표현으로 캐스트합니다. 속성 값을 가져올 때는 항상 일반 텍스트 문자열 값을 받게 됩니다:

```php
use Illuminate\Support\Str;

$user->uuid = Str::uuid();

return $user->uuid;

// "6e8cdeed-2f32-40bd-b109-1e4405be2140"
```



<a name="date-casting"></a>
### 날짜 캐스팅

기본적으로 Eloquent는 `created_at`와 `updated_at` 컬럼을 [Carbon](https://github.com/briannesbitt/Carbon) 인스턴스로 캐스팅합니다. Carbon은 PHP `DateTime` 클래스를 확장하며 유용한 메서드를 제공합니다. 모델의 `casts` 메서드 내에 추가 날짜 캐스트를 정의하여 추가 날짜 속성을 캐스팅할 수 있습니다. 일반적으로 날짜는 `datetime` 또는 `immutable_datetime` 캐스트 타입을 사용하여 캐스팅하는 것이 좋습니다.

`date` 또는 `datetime` 캐스트를 정의할 때 날짜 형식을 지정할 수도 있습니다. 이 형식은 [모델이 배열 또는 JSON으로 직렬화될 때](/docs/{{version}}/eloquent-serialization) 사용됩니다.

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'created_at' => 'datetime:Y-m-d',
    ];
}
```



열이 날짜로 캐스팅될 때, 해당 모델 속성 값을 UNIX 타임스탬프, 날짜 문자열(`Y-m-d`), 날짜-시간 문자열, 또는 `DateTime` / `Carbon` 인스턴스로 설정할 수 있습니다. 날짜 값은 올바르게 변환되어 데이터베이스에 저장됩니다.

모델의 모든 날짜에 대한 기본 직렬화 형식을 사용자 정의하려면 모델에 `serializeDate` 메서드를 정의하면 됩니다. 이 메서드는 데이터베이스에 저장될 때 날짜가 형식화되는 방식에는 영향을 주지 않습니다.

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}
```



모델의 날짜를 실제로 데이터베이스에 저장할 때 사용해야 하는 형식을 지정하려면, 모델의 `Table` 속성에서 `dateFormat` 인수를 사용해야 합니다:

```php
use Illuminate\Database\Eloquent\Attributes\Table;

#[Table(dateFormat: 'U')]
class Flight extends Model
{
    // ...
}
```



<a name="date-casting-and-timezones"></a>
#### Date Casting, Serialization, and Timezones

By default, the `date` and `datetime` casts will serialize dates to a UTC ISO-8601 date string (`YYYY-MM-DDTHH:MM:SS.uuuuuuZ`), regardless of the timezone specified in your application's `timezone` configuration option. You are strongly encouraged to always use this serialization format, as well as to store your application's dates in the UTC timezone by not changing your application's `timezone` configuration option from its default `UTC` value. Consistently using the UTC timezone throughout your application will provide the maximum level of interoperability with other date manipulation libraries written in PHP and JavaScript.

If a custom format is applied to the `date` or `datetime` cast, such as `datetime:Y-m-d H:i:s`, the inner timezone of the Carbon instance will be used during date serialization. Typically, this will be the timezone specified in your application's `timezone` configuration option. However, it's important to note that `timestamp` columns such as `created_at` and `updated_at` are exempt from this behavior and are always formatted in UTC, regardless of the application's timezone setting.

<a name="enum-casting"></a>
### Enum Casting

Eloquent also allows you to cast your attribute values to PHP [Enums](https://www.php.net/manual/en/language.enumerations.backed.php). To accomplish this, you may specify the attribute and enum you wish to cast in your model's `casts` method:

```php
use App\Enums\ServerStatus;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'status' => ServerStatus::class,
    ];
}
```



모델에서 캐스트를 정의하면, 지정된 속성은 속성과 상호작용할 때 자동으로 열거형으로 캐스트되고 다시 열거형에서 캐스트됩니다:

```php
if ($server->status == ServerStatus::Provisioned) {
    $server->status = ServerStatus::Ready;

    $server->save();
}
```



<a name="casting-arrays-of-enums"></a>
#### 열거형 배열 캐스팅

때때로 모델이 단일 열 안에 열거형 값 배열을 저장해야 할 때가 있습니다. 이를 달성하기 위해 Laravel에서 제공하는 `AsEnumArrayObject` 또는 `AsEnumCollection` 캐스트를 사용할 수 있습니다:

```php
use App\Enums\ServerStatus;
use Illuminate\Database\Eloquent\Casts\AsEnumCollection;

/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'statuses' => AsEnumCollection::of(ServerStatus::class),
    ];
}
```



<a name="encrypted-casting"></a>
### Encrypted Casting

The `encrypted` cast will encrypt a model's attribute value using Laravel's built-in [encryption](/docs/{{version}}/encryption) features. In addition, the `encrypted:array`, `encrypted:collection`, `encrypted:object`, `AsEncryptedArrayObject`, and `AsEncryptedCollection` casts work like their unencrypted counterparts; however, as you might expect, the underlying value is encrypted when stored in your database.

As the final length of the encrypted text is not predictable and is longer than its plain text counterpart, make sure the associated database column is of `TEXT` type or larger. In addition, since the values are encrypted in the database, you will not be able to query or search encrypted attribute values.

<a name="key-rotation"></a>
#### Key Rotation

As you may know, Laravel encrypts strings using the `key` configuration value specified in your application's `app` configuration file. Typically, this value corresponds to the value of the `APP_KEY` environment variable. If you need to rotate your application's encryption key, you may [gracefully do so](/docs/{{version}}/encryption#gracefully-rotating-encryption-keys).

<a name="query-time-casting"></a>
### Query Time Casting

Sometimes you may need to apply casts while executing a query, such as when selecting a raw value from a table. For example, consider the following query:

```php
use App\Models\Post;
use App\Models\User;

$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->get();
```



이 쿼리의 결과에 대한 `last_posted_at` 속성은 단순한 문자열이 될 것입니다. 쿼리를 실행할 때 이 속성에 `datetime` 형 변환을 적용할 수 있다면 좋을 것입니다. 다행히도, 우리는 `withCasts` 메서드를 사용하여 이것을 수행할 수 있습니다:

```php
$users = User::select([
    'users.*',
    'last_posted_at' => Post::selectRaw('MAX(created_at)')
        ->whereColumn('user_id', 'users.id')
])->withCasts([
    'last_posted_at' => 'datetime'
])->get();
```



<a name="custom-casts"></a>
## 사용자 정의 캐스트

Laravel에는 다양한 내장된 유용한 캐스트 유형이 있지만, 때때로 사용자 정의 캐스트 유형을 정의해야 할 수도 있습니다. 캐스트를 생성하려면 `make:cast` Artisan 명령을 실행하십시오. 새 캐스트 클래스는 `app/Casts` 디렉터리에 배치됩니다:

```shell
php artisan make:cast AsJson
```



모든 사용자 정의 캐스트 클래스는 `CastsAttributes` 인터페이스를 구현합니다. 이 인터페이스를 구현하는 클래스는 `get` 및 `set` 메서드를 정의해야 합니다. `get` 메서드는 데이터베이스의 원시 값을 캐스트 값으로 변환하는 역할을 하며, `set` 메서드는 캐스트 값을 데이터베이스에 저장할 수 있는 원시 값으로 변환해야 합니다. 예를 들어, 내장 `json` 캐스트 유형을 사용자 정의 캐스트 유형으로 다시 구현해 보겠습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;

class AsJson implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, mixed>
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        return json_decode($value, true);
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
        return json_encode($value);
    }
}
```



사용자 정의 캐스트 유형을 정의한 후에는 클래스 이름을 사용하여 모델 속성에 이를 연결할 수 있습니다:

```php
<?php

namespace App\Models;

use App\Casts\AsJson;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'options' => AsJson::class,
        ];
    }
}
```



<a name="value-object-casting"></a>
### 값 객체 캐스팅

값을 원시 타입으로만 캐스팅하는 데 제한되지 않습니다. 값들을 객체로도 캐스팅할 수 있습니다. 값을 객체로 캐스팅하는 커스텀 캐스트를 정의하는 것은 원시 타입으로 캐스팅하는 것과 매우 유사합니다. 단, 값 객체가 여러 데이터베이스 컬럼을 포함하는 경우, `set` 메서드는 모델에 저장 가능한 원시 값을 설정하는 데 사용될 키/값 쌍의 배열을 반환해야 합니다. 값 객체가 단일 컬럼에만 영향을 미치는 경우, 단순히 저장 가능한 값을 반환하면 됩니다.

예시로, 여러 모델 값을 단일 `Address` 값 객체로 캐스팅하는 커스텀 캐스트 클래스를 정의해 보겠습니다. `Address` 값 객체에는 두 개의 공개 속성: `lineOne`와 `lineTwo`가 있다고 가정합니다:

```php
<?php

namespace App\Casts;

use App\ValueObjects\Address;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;
use Illuminate\Database\Eloquent\Model;
use InvalidArgumentException;

class AsAddress implements CastsAttributes
{
    /**
     * Cast the given value.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function get(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): Address {
        return new Address(
            $attributes['address_line_one'],
            $attributes['address_line_two']
        );
    }

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     * @return array<string, string>
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): array {
        if (! $value instanceof Address) {
            throw new InvalidArgumentException('The given value is not an Address instance.');
        }

        return [
            'address_line_one' => $value->lineOne,
            'address_line_two' => $value->lineTwo,
        ];
    }
}
```



값 객체로 캐스팅할 때, 값 객체에 대해 이루어진 모든 변경 사항은 모델이 저장되기 전에 자동으로 모델에 동기화됩니다:

```php
use App\Models\User;

$user = User::find(1);

$user->address->lineOne = 'Updated Address Value';

$user->save();
```



> [!NOTE]
> JSON이나 배열로 변환할 Eloquent 모델이 값 객체를 포함하고 있다면, 값 객체에 `Illuminate\Contracts\Support\Arrayable`와 `JsonSerializable` 인터페이스를 구현해야 합니다.

<a name="value-object-caching"></a>
#### 값 객체 캐싱

값 객체로 캐스팅된 속성이 해결되면, Eloquent에 의해 캐싱됩니다. 따라서 속성에 다시 접근하면 동일한 객체 인스턴스가 반환됩니다.

사용자 정의 캐스트 클래스의 객체 캐싱 동작을 비활성화하고 싶다면, 사용자 정의 캐스트 클래스에 public `withoutObjectCaching` 속성을 선언할 수 있습니다:

```php
class AsAddress implements CastsAttributes
{
    public bool $withoutObjectCaching = true;

    // ...
}
```



<a name="array-json-serialization"></a>
### 배열 / JSON 직렬화

Eloquent 모델을 배열 또는 JSON으로 변환할 때 `toArray` 및 `toJson` 메서드를 사용하면, 커스텀 캐스트 값 객체도 일반적으로 직렬화됩니다. 단, 해당 객체가 `Illuminate\Contracts\Support\Arrayable` 및 `JsonSerializable` 인터페이스를 구현해야 합니다. 그러나 서드파티 라이브러리에서 제공되는 값 객체를 사용할 경우, 이러한 인터페이스를 객체에 추가할 수 없을 수도 있습니다.

따라서, 커스텀 캐스트 클래스가 값 객체의 직렬화를 담당하도록 지정할 수 있습니다. 이를 위해 커스텀 캐스트 클래스는 `Illuminate\Contracts\Database\Eloquent\SerializesCastableAttributes` 인터페이스를 구현해야 합니다. 이 인터페이스는 클래스가 `serialize` 메서드를 포함해야 하며, 해당 메서드는 값 객체의 직렬화된 형태를 반환해야 한다고 명시합니다:

```php
/**
 * Get the serialized representation of the value.
 *
 * @param  array<string, mixed>  $attributes
 */
public function serialize(
    Model $model,
    string $key,
    mixed $value,
    array $attributes,
): string {
    return (string) $value;
}
```



<a name="inbound-casting"></a>
### 인바운드 캐스팅

가끔 모델에 설정되는 값만 변환하고 모델에서 속성을 가져올 때는 아무 작업도 수행하지 않는 커스텀 캐스트 클래스를 작성해야 할 경우가 있습니다.

인바운드 전용 커스텀 캐스트는 `CastsInboundAttributes` 인터페이스를 구현해야 하며, 이 인터페이스는 `set` 메서드 정의만 요구합니다. `make:cast` Artisan 명령은 `--inbound` 옵션과 함께 호출하여 인바운드 전용 캐스트 클래스를 생성할 수 있습니다:

```shell
php artisan make:cast AsHash --inbound
```



순수 입력 전용 캐스트의 고전적인 예는 '해싱' 캐스트입니다. 예를 들어, 특정 알고리즘을 통해 입력 값을 해싱하는 캐스트를 정의할 수 있습니다:

```php
<?php

namespace App\Casts;

use Illuminate\Contracts\Database\Eloquent\CastsInboundAttributes;
use Illuminate\Database\Eloquent\Model;

class AsHash implements CastsInboundAttributes
{
    /**
     * Create a new cast class instance.
     */
    public function __construct(
        protected string|null $algorithm = null,
    ) {}

    /**
     * Prepare the given value for storage.
     *
     * @param  array<string, mixed>  $attributes
     */
    public function set(
        Model $model,
        string $key,
        mixed $value,
        array $attributes,
    ): string {
        return is_null($this->algorithm)
            ? bcrypt($value)
            : hash($this->algorithm, $value);
    }
}
```



<a name="cast-parameters"></a>
### 캐스트 매개변수

모델에 커스텀 캐스트를 첨부할 때, 캐스트 매개변수는 클래스 이름과 `:` 문자를 사용하여 구분하고 여러 매개변수는 쉼표로 구분하여 지정할 수 있습니다. 매개변수는 캐스트 클래스의 생성자로 전달됩니다:

```php
/**
 * Get the attributes that should be cast.
 *
 * @return array<string, string>
 */
protected function casts(): array
{
    return [
        'secret' => AsHash::class.':sha256',
    ];
}
```



<a name="comparing-cast-values"></a>
### 캐스트 값 비교

두 개의 주어진 캐스트 값을 비교하여 변경되었는지 여부를 결정하는 방법을 정의하고 싶다면, 사용자 정의 캐스트 클래스가 `Illuminate\Contracts\Database\Eloquent\ComparesCastableAttributes` 인터페이스를 구현할 수 있습니다. 이를 통해 Eloquent가 변경되었다고 간주하는 값을 세밀하게 제어할 수 있으며, 모델이 업데이트될 때 데이터베이스에 저장되는 값을 조절할 수 있습니다.

이 인터페이스는 클래스가 `compare` 메서드를 포함해야 하며, 주어진 값이 동일하다고 간주되면 `true`를 반환해야 한다고 명시합니다:

```php
/**
 * Determine if the given values are equal.
 *
 * @param  \Illuminate\Database\Eloquent\Model  $model
 * @param  string  $key
 * @param  mixed  $firstValue
 * @param  mixed  $secondValue
 * @return bool
 */
public function compare(
    Model $model,
    string $key,
    mixed $firstValue,
    mixed $secondValue
): bool {
    return $firstValue === $secondValue;
}
```



<a name="castables"></a>
### 캐스터블

응용 프로그램의 값 객체가 고유한 커스텀 캐스트 클래스를 정의하도록 허용하고 싶을 수 있습니다. 커스텀 캐스트 클래스를 모델에 첨부하는 대신, `Illuminate\Contracts\Database\Eloquent\Castable` 인터페이스를 구현하는 값 객체 클래스를 첨부할 수 있습니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class,
    ];
}
```



`Castable` 인터페이스를 구현하는 객체는 `Castable` 클래스와의 변환을 담당하는 사용자 정의 캐스터 클래스의 클래스 이름을 반환하는 `castUsing` 메서드를 정의해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use App\Casts\AsAddress;

class Address implements Castable
{
    /**
     * Get the name of the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): string
    {
        return AsAddress::class;
    }
}
```



`Castable` 클래스를 사용할 때, 여전히 `casts` 메서드 정의에 인수를 제공할 수 있습니다. 인수는 `castUsing` 메서드로 전달됩니다:

```php
use App\ValueObjects\Address;

protected function casts(): array
{
    return [
        'address' => Address::class.':argument',
    ];
}
```



<a name="anonymous-cast-classes"></a>
#### 캐스터블 및 익명 캐스트 클래스

"캐스터블(castables)"을 PHP의 [익명 클래스](https://www.php.net/manual/en/language.oop5.anonymous.php)와 결합하면, 하나의 캐스터블 객체로 값 객체와 그 캐스팅 로직을 정의할 수 있습니다. 이를 달성하려면, 값 객체의 `castUsing` 메서드에서 익명 클래스를 반환해야 합니다. 익명 클래스는 `CastsAttributes` 인터페이스를 구현해야 합니다:

```php
<?php

namespace App\ValueObjects;

use Illuminate\Contracts\Database\Eloquent\Castable;
use Illuminate\Contracts\Database\Eloquent\CastsAttributes;

class Address implements Castable
{
    // ...

    /**
     * Get the caster class to use when casting from / to this cast target.
     *
     * @param  array<string, mixed>  $arguments
     */
    public static function castUsing(array $arguments): CastsAttributes
    {
        return new class implements CastsAttributes
        {
            public function get(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): Address {
                return new Address(
                    $attributes['address_line_one'],
                    $attributes['address_line_two']
                );
            }

            public function set(
                Model $model,
                string $key,
                mixed $value,
                array $attributes,
            ): array {
                return [
                    'address_line_one' => $value->lineOne,
                    'address_line_two' => $value->lineTwo,
                ];
            }
        };
    }
}
```
{% endraw %}
