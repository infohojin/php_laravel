---
layout: docs
title: "웅변적: 직렬화"
---

{% raw %}
# 웅변적: 직렬화

- [소개](#introduction)
- [모델 및 컬렉션 직렬화](#serializing-models-and-collections)
- [Serializing to Arrays](#serializing-to-arrays)
- [Serializing to JSON](#serializing-to-json)
- [Hiding Attributes From JSON](#hiding-attributes-from-json)
- [Appending Values to JSON](#appending-values-to-json)
- [Date Serialization](#date-serialization)

<a name="introduction"></a>
## 소개

Laravel 을 사용하여 API 를 구축할 때는 모델과 관계를 배열이나 JSON 으로 변환해야 할 때가 많습니다. Eloquent 에는 이러한 변환을 수행하는 편리한 방법뿐만 아니라 모델의 직렬화된 표현에 포함되는 속성을 제어하는 방법도 포함되어 있습니다。

> [!NOTE]
> 더욱 강력한 방식으로 Eloquent 모델 및 컬렉션 JSON 직렬화를 처리하려면 [Eloquent API 리소스] 설명서 (/docs/{{version}}/eloquent-resources) 를 확인하세요。

<a name="serializing-models-and-collections"></a>
## 모델 및 컬렉션 직렬화

<a name="serializing-to-arrays"></a>
### 배열로 직렬화

모델과 그 로드된 [relationships](/docs/{{version}}/eloquent-relationships) 를 배열로 변환하려면 `toArray` 메서드를 사용해야 합니다. 이 메서드는 재귀적이므로 모든 속성과 모든 관계 (관계의 관계 포함) 가 배열로 변환됩니다：

```php
use App\Models\User;

$user = User::with('roles')->first();

return $user->toArray();

```



`attributesToArray` 메서드는 모델의 속성을 배열로 변환하는 데 사용할 수 있지만, 관계는 변환할 수 없습니다:

```php
$user = User::first();

return $user->attributesToArray();

```

컬렉션 인스턴스에서 `toArray` 메서드를 호출하여 전체 [컬렉션](/docs/{{version}}/eloquent-collections)의 모델을 배열로 변환할 수도 있습니다:

```php
$users = User::all();

return $users->toArray();

```

<a name="serializing-to-json"></a>
### JSON으로 직렬화하기

모델을 JSON으로 변환하려면 `toJson` 메서드를 사용해야 합니다. `toArray`와 마찬가지로 `toJson` 메서드는 재귀적이므로 모든 속성과 관계가 JSON으로 변환됩니다. 또한 [PHP에서 지원하는](https://secure.php.net/manual/en/function.json-encode.php) JSON 인코딩 옵션을 지정할 수도 있습니다:

```php
use App\Models\User;

$user = User::find(1);

return $user->toJson();

return $user->toJson(JSON_PRETTY_PRINT);

```

또는 모델이나 컬렉션을 문자열로 캐스팅할 수 있으며, 이 경우 모델이나 컬렉션에서 `toJson` 메서드가 자동으로 호출됩니다:

```php
return (string) User::find(1);

```

모델과 컬렉션은 문자열로 변환될 때 JSON으로 변환되므로, 애플리케이션의 라우트나 컨트롤러에서 Eloquent 객체를 직접 반환할 수 있습니다. 라라벨은 라우트나 컨트롤러에서 반환될 때 Eloquent 모델과 컬렉션을 자동으로 JSON으로 직렬화합니다:

```php
Route::get('/users', function () {
    return User::all();
});

```

<a name="relationships"></a>
#### 관계

Eloquent 모델이 JSON으로 변환될 때, 로드된 관계는 자동으로 JSON 객체의 속성으로 포함됩니다. 또한, Eloquent 관계 메서드는 "카멜 케이스" 메서드 이름을 사용하여 정의되지만, 관계의 JSON 속성은 "스네이크 케이스"가 됩니다.

<a name="hiding-attributes-from-json"></a>
## JSON에서 속성 숨기기

때때로 모델의 배열 또는 JSON 표현에 포함될 속성(예: 비밀번호)을 제한하고 싶을 수 있습니다. 이를 위해 모델에서 `Hidden` 속성을 사용할 수 있습니다. `Hidden` 속성에 나열된 속성은 모델의 직렬화된 표현에 포함되지 않습니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Hidden;
use Illuminate\Database\Eloquent\Model;

#[Hidden(['password'])]
class User extends Model
{
    // ...
}

```

> [!NOTE]
> 관계를 숨기려면 관계의 메서드 이름을 Eloquent 모델의 `Hidden` 속성에 추가하십시오.

또는 `Visible` 속성을 사용하여 모델의 배열 및 JSON 표현에 포함되어야 하는 속성의 "허용 목록"을 정의할 수 있습니다. `Visible` 속성에 없는 모든 속성은 모델이 배열 또는 JSON으로 변환될 때 숨겨집니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Visible;
use Illuminate\Database\Eloquent\Model;

#[Visible(['first_name', 'last_name'])]
class User extends Model
{
    // ...
}

```

<a name="temporarily-modifying-attribute-visibility"></a>
#### 속성 가시성 일시 수정

특정 모델 인스턴스에서 일반적으로 숨겨져 있는 일부 속성을 보이게 하고 싶다면, `makeVisible` 또는 `mergeVisible` 메서드를 사용할 수 있습니다. `makeVisible` 메서드는 모델 인스턴스를 반환합니다:

```php
return $user->makeVisible('attribute')->toArray();

return $user->mergeVisible(['name', 'email'])->toArray();

```

마찬가지로, 일반적으로 보이는 몇 가지 속성을 숨기고 싶다면 `makeHidden` 또는 `mergeHidden` 방법을 사용할 수 있습니다:

```php
return $user->makeHidden('attribute')->toArray();

return $user->mergeHidden(['name', 'email'])->toArray();

```

모든 보이거나 숨겨진 속성을 일시적으로 재정의하려는 경우, 각각 `setVisible` 및 `setHidden` 메서드를 사용할 수 있습니다:

```php
return $user->setVisible(['id', 'name'])->toArray();

return $user->setHidden(['email', 'password', 'remember_token'])->toArray();

```

<a name="appending-values-to-json"></a>
## JSON에 값 추가하기

때때로 모델을 배열이나 JSON으로 변환할 때, 데이터베이스에 해당 열이 없는 속성을 추가하고 싶을 수 있습니다. 이를 위해 먼저 값에 대한 [접근자](/docs/{{version}}/eloquent-mutators)를 정의하십시오:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * Determine if the user is an administrator.
     */
    protected function isAdmin(): Attribute
    {
        return new Attribute(
            get: fn () => 'yes',
        );
    }
}

```

엑세서가 항상 모델의 배열 및 JSON 표현에 추가되기를 원한다면 모델에 `Appends` 속성을 사용할 수 있습니다. 엑세서의 PHP 메서드가 'camel case'로 정의되어 있어도 속성 이름은 일반적으로 'snake case' 직렬화된 표현을 사용하여 참조된다는 점에 유의하세요.

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Attributes\Appends;
use Illuminate\Database\Eloquent\Model;

#[Appends(['is_admin'])]
class User extends Model
{
    // ...
}

```

속성이 `appends` 목록에 추가되면 모델의 배열과 JSON 표현 모두에 포함됩니다. `appends` 배열의 속성은 모델에서 구성된 `visible` 및 `hidden` 설정도 준수합니다.

<a name="appending-at-run-time"></a>
#### 실행 시 추가

실행 시 모델 인스턴스에 추가 속성을 추가하도록 `append` 또는 `mergeAppends` 메서드를 사용하여 지시할 수 있습니다. 또는 `setAppends` 메서드를 사용하여 주어진 모델 인스턴스에 대해 추가된 속성 배열 전체를 재정의할 수 있습니다:

```php
return $user->append('is_admin')->toArray();

return $user->mergeAppends(['is_admin', 'status'])->toArray();

return $user->setAppends(['is_admin'])->toArray();

```

마찬가지로, 모델에서 모든 추가된 속성을 제거하고 싶다면 `withoutAppends` 메서드를 사용할 수 있습니다:

```php
return $user->withoutAppends()->toArray();

```

<a name="date-serialization"></a>
## 날짜 직렬화

<a name="customizing-the-default-date-format"></a>
#### 기본 날짜 형식 사용자 정의

기본 직렬화 형식을 `serializeDate` 메서드를 재정의하여 사용자 정의할 수 있습니다. 이 메서드는 데이터베이스에 저장될 때 날짜가 형식화되는 방식에는 영향을 미치지 않습니다:

```php
/**
 * Prepare a date for array / JSON serialization.
 */
protected function serializeDate(DateTimeInterface $date): string
{
    return $date->format('Y-m-d');
}

```

<a name="customizing-the-date-format-per-attribute"></a>
#### 속성별 날짜 형식 사용자 정의

모델의 [캐스트 선언](/docs/{{version}}/eloquent-mutators#attribute-casting)에서 날짜 형식을 지정하여 개별 Eloquent 날짜 속성의 직렬화 형식을 사용자 정의할 수 있습니다:

```php
protected function casts(): array
{
    return [
        'birthday' => 'date:Y-m-d',
        'joined_at' => 'datetime:Y-m-d H:00',
    ];
}

```
{% endraw %}
