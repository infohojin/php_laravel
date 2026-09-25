---
layout: docs
title: "Laravel Folio"
---

{% raw %}
# Laravel Folio

- [소개](#introduction)
- [설치](#installation)
    - [페이지 경로 / URI](#page-paths-uris)
    - [서브도메인 라우팅](#subdomain-routing)
- [라우트 생성](#creating-routes)
    - [중첩 라우트](#nested-routes)
    - [인덱스 라우트](#index-routes)
- [라우트 매개변수](#route-parameters)
- [라우트 모델 바인딩](#route-model-binding)
    - [소프트 삭제된 모델](#soft-deleted-models)
- [렌더 훅](#render-hooks)
- [명명된 라우트](#named-routes)
- [미들웨어](#middleware)
- [라우트 캐싱](#route-caching)

<a name="introduction"></a>
## 소개

[Laravel Folio](https://github.com/laravel/folio)는 라라벨 애플리케이션에서 라우팅을 단순화하도록 설계된 강력한 페이지 기반 라우터입니다. Laravel Folio를 사용하면 라우트를 생성하는 것이 애플리케이션의 `resources/views/pages` 디렉토리 안에 Blade 템플릿을 만드는 것만큼이나 간단해집니다.

예를 들어, `/greeting` URL에서 접근 가능한 페이지를 생성하려면 애플리케이션의 `resources/views/pages` 디렉토리 안에 `greeting.blade.php` 파일을 생성하면 됩니다:

```blade
<div>
    Hello World
</div>

```

<a name="installation"></a>
## 설치

시작하려면 Composer 패키지 관리자를 사용하여 프로젝트에 Folio를 설치하세요:

```shell
composer require laravel/folio

```

Folio를 설치한 후, `folio:install` Artisan 명령어를 실행할 수 있으며, 이는 Folio의 서비스 제공자를 애플리케이션에 설치합니다. 이 서비스 제공자는 Folio가 경로/페이지를 검색할 디렉토리를 등록합니다:

```shell
php artisan folio:install

```

<a name="page-paths-uris"></a>
### 페이지 경로 / URI

기본적으로 Folio는 애플리케이션의 `resources/views/pages` 디렉토리에서 페이지를 제공합니다. 그러나 Folio 서비스 제공자의 `boot` 메서드에서 이러한 디렉토리를 사용자 정의할 수 있습니다.

예를 들어, 때로는 동일한 Laravel 애플리케이션에서 여러 Folio 경로를 지정하는 것이 편리할 수 있습니다. 애플리케이션의 "admin" 영역에 대한 별도의 Folio 페이지 디렉토리를 가지고, 나머지 애플리케이션 페이지에는 다른 디렉토리를 사용할 수 있습니다.

`Folio::path` 및 `Folio::uri` 메서드를 사용하여 이를 수행할 수 있습니다. `path` 메서드는 Folio가 들어오는 HTTP 요청을 라우팅할 때 페이지를 검색할 디렉토리를 등록하며, `uri` 메서드는 해당 페이지 디렉토리의 "기본 URI"를 지정합니다:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages/guest'))->uri('/');

Folio::path(resource_path('views/pages/admin'))
    ->uri('/admin')
    ->middleware([
        '*' => [
            'auth',
            'verified',

            // ...
        ],
    ]);

```

<a name="subdomain-routing"></a>
### 서브도메인 라우팅

들어오는 요청의 서브도메인을 기반으로 페이지로 라우팅할 수도 있습니다. 예를 들어, `admin.example.com`에서 오는 요청을 나머지 Folio 페이지와 다른 페이지 디렉토리로 라우팅하고 싶을 수 있습니다. 이는 `Folio::path` 메서드를 호출한 후 `domain` 메서드를 호출하여 수행할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::domain('admin.example.com')
    ->path(resource_path('views/pages/admin'));

```



`domain` 방법은 또한 도메인 또는 하위 도메인의 일부를 매개변수로 캡처할 수 있게 해줍니다. 이러한 매개변수는 페이지 템플릿에 주입됩니다:

```php
use Laravel\Folio\Folio;

Folio::domain('{account}.example.com')
    ->path(resource_path('views/pages/admin'));

```

<a name="creating-routes"></a>
## 라우트 생성

Folio가 마운트된 디렉토리에 Blade 템플릿을 배치하여 Folio 라우트를 생성할 수 있습니다. 기본적으로 Folio는 `resources/views/pages` 디렉토리를 마운트하지만, Folio 서비스 제공자의 `boot` 메서드에서 이러한 디렉토리를 사용자 정의할 수 있습니다.

Blade 템플릿이 Folio가 마운트된 디렉토리에 배치되면, 브라우저를 통해 즉시 접근할 수 있습니다. 예를 들어, `pages/schedule.blade.php`에 배치된 페이지는 브라우저에서 `http://example.com/schedule`로 접근할 수 있습니다.

모든 Folio 페이지 / 라우트 목록을 빠르게 확인하려면, `folio:list` Artisan 명령을 실행할 수 있습니다:

```shell
php artisan folio:list

```

<a name="nested-routes"></a>
### 중첩 경로

Folio의 디렉토리 중 하나 안에 하나 이상의 디렉토리를 생성하여 중첩 경로를 만들 수 있습니다. 예를 들어, `/user/profile`를 통해 접근 가능한 페이지를 만들려면 `pages/user` 디렉토리 안에 `profile.blade.php` 템플릿을 생성하십시오:

```shell
php artisan folio:page user/profile

# pages/user/profile.blade.php → /user/profile

```

<a name="index-routes"></a>
### 인덱스 경로

때때로, 특정 페이지를 디렉토리의 "인덱스"로 만들고 싶을 때가 있습니다. Folio 디렉토리 내에 `index.blade.php` 템플릿을 배치하면, 해당 디렉토리의 루트로의 요청은 그 페이지로 라우팅됩니다:

```shell
php artisan folio:page index
# pages/index.blade.php → /

php artisan folio:page users/index
# pages/users/index.blade.php → /users

```

<a name="route-parameters"></a>
## 경로 매개변수

종종 들어오는 요청의 URL 세그먼트를 페이지에 삽입하여 이를 활용해야 할 때가 있습니다. 예를 들어, 표시되는 사용자의 프로필 "ID"에 접근해야 할 수 있습니다. 이를 수행하기 위해 페이지 파일 이름의 세그먼트를 대괄호로 감쌀 수 있습니다:

```shell
php artisan folio:page "users/[id]"

# pages/users/[id].blade.php → /users/1

```

캡처된 세그먼트는 Blade 템플릿 내에서 변수로 접근할 수 있습니다:

```html
<div>
    User {{ $id }}
</div>

```

여러 세그먼트를 캡처하려면 캡슐화된 세그먼트 앞에 세 개의 점 `...`:를 붙일 수 있습니다.

```shell
php artisan folio:page "users/[...ids]"

# pages/users/[...ids].blade.php → /users/1/2/3

```

여러 구간을 캡처할 때, 캡처된 구간들은 배열로 페이지에 주입됩니다:

```html
<ul>
    @foreach ($ids as $id)
        <li>User {{ $id }}</li>
    @endforeach
</ul>

```

<a name="route-model-binding"></a>
## 라우트 모델 바인딩

페이지 템플릿 파일 이름의 와일드카드 세그먼트가 애플리케이션의 Eloquent 모델 중 하나와 일치하면, Folio는 Laravel의 라우트 모델 바인딩 기능을 자동으로 활용하여 해결된 모델 인스턴스를 페이지에 주입하려고 시도합니다:

```shell
php artisan folio:page "users/[User]"

# pages/users/[User].blade.php → /users/1

```

캡처된 모델은 Blade 템플릿 내에서 변수로 접근할 수 있습니다. 모델의 변수 이름은 '카멜 케이스'로 변환됩니다.

```html
<div>
    User {{ $user->id }}
</div>

```

#### 키 커스터마이징

가끔 바인딩된 Eloquent 모델을 `id`이 아닌 다른 컬럼을 사용하여 해결하고 싶을 때가 있습니다. 이를 위해 페이지 파일 이름에 컬럼을 지정할 수 있습니다. 예를 들어, 파일 이름이 `[Post:slug].blade.php`인 페이지는 `id` 컬럼 대신 `slug` 컬럼을 통해 바인딩된 모델을 해결하려고 시도합니다.

Windows에서는 모델 이름과 키를 구분하기 위해 `-`를 사용해야 합니다: `[Post-slug].blade.php`.

#### 모델 위치

기본적으로 Folio는 애플리케이션의 `app/Models` 디렉터리 내에서 모델을 검색합니다. 그러나 필요하다면 템플릿 파일 이름에 완전한 클래스 이름을 지정할 수도 있습니다:

```shell
php artisan folio:page "users/[.App.Models.User]"

# pages/users/[.App.Models.User].blade.php → /users/1

```

<a name="soft-deleted-models"></a>
### 소프트 삭제된 모델

기본적으로 소프트 삭제된 모델은 암시적 모델 바인딩을 해결할 때 검색되지 않습니다. 그러나 원하신다면, 페이지 템플릿 내에서 `withTrashed` 함수를 호출하여 Folio가 소프트 삭제된 모델을 검색하도록 할 수 있습니다:

```php
<?php

use function Laravel\Folio\{withTrashed};

withTrashed();

?>

<div>
    User {{ $user->id }}
</div>

```

<a name="render-hooks"></a>
## 렌더 훅

기본적으로 Folio는 들어오는 요청에 대한 응답으로 페이지의 Blade 템플릿 내용을 반환합니다. 그러나 페이지 템플릿 내에서 `render` 함수를 호출하여 응답을 사용자 정의할 수 있습니다.

`render` 함수는 클로저를 허용하며, 이 클로저는 Folio에 의해 렌더링되는 `View` 인스턴스를 받게 되어, 뷰에 추가 데이터를 추가하거나 전체 응답을 사용자 정의할 수 있습니다. `View` 인스턴스를 받는 것 외에도, 추가적인 라우트 매개변수나 모델 바인딩도 `render` 클로저에 제공됩니다.

```php
<?php

use App\Models\Post;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

use function Laravel\Folio\render;

render(function (View $view, Post $post) {
    if (! Auth::user()->can('view', $post)) {
        return response('Unauthorized', 403);
    }

    return $view->with('photos', $post->author->photos);
}); ?>

<div>
    {{ $post->content }}
</div>

<div>
    This author has also taken {{ count($photos) }} photos.
</div>

```

<a name="named-routes"></a>
## 명명된 경로

`name` 함수를 사용하여 특정 페이지 경로에 대한 이름을 지정할 수 있습니다:

```php
<?php

use function Laravel\Folio\name;

name('users.index');

```

라라벨(Laravel)의 이름이 지정된 라우트와 마찬가지로, 이름이 지정된 Folio 페이지에 대한 URL을 생성하기 위해 `route` 함수를 사용할 수 있습니다:

```blade
<a href="{{ route('users.index') }}">
    All Users
</a>

```

페이지에 매개변수가 있는 경우, 해당 값을 `route` 함수에 단순히 전달할 수 있습니다:

```php
route('users.show', ['user' => $user]);

```

<a name="middleware"></a>
## 미들웨어

페이지 템플릿 내에서 `middleware` 함수를 호출하여 특정 페이지에 미들웨어를 적용할 수 있습니다:

```php
<?php

use function Laravel\Folio\{middleware};

middleware(['auth', 'verified']);

?>

<div>
    Dashboard
</div>

```

또는 미들웨어를 페이지 그룹에 할당하려면, `Folio::path` 메서드를 호출한 후 `middleware` 메서드를 체인할 수 있습니다.

미들웨어를 적용할 페이지를 지정하려면, 미들웨어 배열을 적용할 페이지의 해당 URL 패턴으로 키를 지정할 수 있습니다. 와일드카드 문자로 `*` 문자를 사용할 수 있습니다:

```php
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        // ...
    ],
]);

```

미들웨어 배열에 클로저를 포함하여 인라인 익명 미들웨어를 정의할 수 있습니다:

```php
use Closure;
use Illuminate\Http\Request;
use Laravel\Folio\Folio;

Folio::path(resource_path('views/pages'))->middleware([
    'admin/*' => [
        'auth',
        'verified',

        function (Request $request, Closure $next) {
            // ...

            return $next($request);
        },
    ],
]);

```

<a name="route-caching"></a>
## 라우트 캐싱

Folio를 사용할 때는 항상 [Laravel의 라우트 캐싱 기능](/docs/{{version}}/routing#route-caching)을 활용해야 합니다. Folio는 Folio 페이지 정의와 라우트 이름이 최대 성능을 위해 올바르게 캐시되도록 `route:cache` Artisan 명령어를 수신합니다.
{% endraw %}
