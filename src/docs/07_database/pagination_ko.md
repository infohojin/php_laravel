---
layout: docs
title: "데이터베이스: 페이지 구성"
---

{% raw %}
# 데이터베이스: 페이지 구성

- [소개](#introduction)
- [기본 사용법](#basic-usage)
- [페이지 넘기기 쿼리 빌더 결과](#paginating-query-builder-results)
- [유창한 결과 페이지 지정](#paginating-eloquent-results)
- [커서 페이지 지정](#cursor-pagination)
- [페이지 매기기 수동 생성](#manually-creating-a-paginator)
- [페이지 구성 URL 사용자 지정](#customizing-pagination-urls)
- [페이지 구성 결과 표시](#displaying-pagination-results)
- [페이지 구성 링크 창 조정](#adjusting-the-pagination-link-window)
- [결과를 JSON 으로 변환](#converting-results-to-json)
- [페이지 구성 뷰 사용자 지정](#customizing-the-pagination-view)
- [부트스트랩 사용](#using-bootstrap)
- [Paginator 및 LengthAwarePaginator 인스턴스 메서드](#paginator-instance-methods)
- [커서 페이지너 인스턴스 방법](#cursor-paginator-instance-methods)

<a name="introduction"></a>
## 소개

다른 프레임워크에서는 페이지 구성이 매우 고통스러울 수 있습니다. Laravel 의 페이지 구성 접근 방식이 신선한 공기를 마시게 해주기를 바랍니다. Laravel 의 페이지 지정기는 [query builder](/docs/{{version}}/queries) 및 [Eloquent ORM](/docs/{{version}}/eloquent) 과 통합되어 구성 없이도 편리하고 사용하기 쉬운 데이터베이스 레코드 페이지 구성을 제공합니다。

기본적으로 페이지 매기기에서 생성된 HTML 은 [Tailwind CSS 프레임워크](https://tailwindcss.com/) 와 호환됩니다. 하지만 Bootstrap 페이지 매기기 지원도 사용할 수 있습니다。

<a name="tailwind"></a>
#### 테일윈드

Tailwind 4.x 와 함께 Laravel 의 기본 Tailwind 페이지 보기를 사용하는 경우， 애플리케이션의 `resources/css/app.css` 파일이 이미 Laravel 의 `@source` 페이지 보기로 올바르게 구성되어 있습니다：

```css
@import 'tailwindcss';

@source '../../vendor/laravel/framework/src/Illuminate/Pagination/resources/views/*.blade.php';
```



<a name="basic-usage"></a>
## 기본 사용법

<a name="paginating-query-builder-results"></a>
### 쿼리 빌더 결과 페이지네이션

아이템을 페이지네이션하는 방법에는 여러 가지가 있습니다. 가장 간단한 방법은 [쿼리 빌더](/docs/{{version}}/queries)나 [Eloquent 쿼리](/docs/{{version}}/eloquent)에서 `paginate` 메서드를 사용하는 것입니다. `paginate` 메서드는 사용자가 보고 있는 현재 페이지를 기준으로 쿼리의 "limit"와 "offset"을 자동으로 설정해 줍니다. 기본적으로 현재 페이지는 HTTP 요청의 `page` 쿼리 문자열 인자 값으로 감지됩니다. 이 값은 Laravel에 의해 자동으로 감지되며, 페이지네이터에서 생성되는 링크에도 자동으로 삽입됩니다.

이 예제에서는 `paginate` 메서드에 전달되는 유일한 인자가 "페이지당" 표시하고자 하는 아이템 수입니다. 이 경우, 페이지당 `15`개의 아이템을 표시하고자 한다고 지정해 봅시다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show all application users.
     */
    public function index(): View
    {
        return view('user.index', [
            'users' => DB::table('users')->paginate(15)
        ]);
    }
}
```



<a name="simple-pagination"></a>
#### 간단한 페이지 매김

`paginate` 메서드는 데이터베이스에서 레코드를 가져오기 전에 쿼리와 일치하는 총 레코드 수를 계산합니다. 이는 페이징 도구가 전체 레코드 페이지 수를 알 수 있도록 하기 위해 수행됩니다. 그러나 애플리케이션 UI에서 전체 페이지 수를 표시할 계획이 없다면 레코드 수 쿼리는 필요하지 않습니다.

따라서 애플리케이션 UI에서 단순히 '다음' 및 '이전' 링크만 표시하면 되는 경우, 단일 효율적인 쿼리를 수행하기 위해 `simplePaginate` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')->simplePaginate(15);
```



<a name="paginating-eloquent-results"></a>
### Eloquent 결과 페이지 나누기

[Eloquent](/docs/{{version}}/eloquent) 쿼리도 페이지를 나눌 수 있습니다. 이 예제에서는 `App\Models\User` 모델을 페이지로 나누고 페이지당 15개의 레코드를 표시할 계획임을 나타냅니다. 보시다시피, 구문은 쿼리 빌더 결과를 페이지로 나누는 것과 거의 동일합니다:

```php
use App\Models\User;

$users = User::paginate(15);
```



물론, `where` 절과 같은 쿼리에 대한 다른 제약 조건을 설정한 후 `paginate` 메서드를 호출할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->paginate(15);
```



Eloquent 모델을 페이지 매김할 때 `simplePaginate` 방법을 사용할 수도 있습니다:

```php
$users = User::where('votes', '>', 100)->simplePaginate(15);
```



마찬가지로, Eloquent 모델을 커서 페이지네이션할 때 `cursorPaginate` 방법을 사용할 수 있습니다:

```php
$users = User::where('votes', '>', 100)->cursorPaginate(15);
```



<a name="multiple-paginator-instances-per-page"></a>
#### 페이지당 여러 페이징 인스턴스

때때로 애플리케이션에서 렌더링된 단일 화면에 두 개의 별도 페이징을 렌더링해야 할 때가 있습니다. 그러나 두 페이징 인스턴스 모두 현재 페이지를 저장하기 위해 `page` 쿼리 문자열 매개변수를 사용하는 경우, 두 페이징이 충돌하게 됩니다. 이 충돌을 해결하려면, 페이징의 현재 페이지를 저장하는 데 사용할 쿼리 문자열 매개변수의 이름을 `paginate`, `simplePaginate`, `cursorPaginate` 메서드에 제공되는 세 번째 인수를 통해 전달할 수 있습니다:

```php
use App\Models\User;

$users = User::where('votes', '>', 100)->paginate(
    $perPage = 15, $columns = ['*'], $pageName = 'users'
);
```



<a name="cursor-pagination"></a>
### 커서 페이지네이션

`paginate`와 `simplePaginate`가 SQL "오프셋(offset)" 절을 사용하여 쿼리를 생성하는 반면, 커서 페이지네이션은 쿼리에 포함된 정렬된 열 값들을 비교하는 "where" 절을 구성하여 작동하며, Laravel의 모든 페이지네이션 방법 중에서 가장 효율적인 데이터베이스 성능을 제공합니다. 이 페이지네이션 방법은 특히 대규모 데이터 집합과 "무한" 스크롤 사용자 인터페이스에 적합합니다.

페이지 번호를 URL의 쿼리 문자열에 포함하는 오프셋 기반 페이지네이션과 달리, 커서 기반 페이지네이션은 쿼리 문자열에 "커서(cursor)" 문자열을 배치합니다. 커서는 다음 페이지네이션 쿼리가 시작되어야 할 위치와 페이지네이션 방향을 포함하는 인코딩된 문자열입니다:

```text
http://localhost/users?cursor=eyJpZCI6MTUsIl9wb2ludHNUb05leHRJdGVtcyI6dHJ1ZX0
```



쿼리 빌더에서 제공하는 `cursorPaginate` 메서드를 통해 커서 기반 페이징 인스턴스를 생성할 수 있습니다. 이 메서드는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다:

```php
$users = DB::table('users')->orderBy('id')->cursorPaginate(15);
```



커서 페이지네이터 인스턴스를 가져온 후에는 일반적으로 `paginate` 및 `simplePaginate` 메서드를 사용할 때와 같이 [페이지네이션 결과를 표시](#displaying-pagination-results)할 수 있습니다. 커서 페이지네이터에서 제공하는 인스턴스 메서드에 대한 자세한 정보는 [커서 페이지네이터 인스턴스 메서드 문서](#cursor-paginator-instance-methods)를 참조하십시오.

> [!WARNING]
> 커서 페이지네이션을 활용하려면 쿼리에 "order by" 절이 포함되어야 합니다. 또한 쿼리에서 정렬되는 열은 페이지네이션하려는 테이블에 속해야 합니다.

<a name="cursor-vs-offset-pagination"></a>
#### 커서 대 오프셋 페이지네이션

오프셋 페이지네이션과 커서 페이지네이션의 차이를 설명하기 위해 몇 가지 SQL 쿼리 예제를 살펴보겠습니다. 다음 두 쿼리는 모두 `users` 테이블에 대해 `id`로 정렬된 "두 번째 페이지"의 결과를 표시합니다:

```sql
# Offset Pagination...
select * from users order by id asc limit 15 offset 15;

# Cursor Pagination...
select * from users where id > 15 order by id asc limit 15;
```

커서 페이징 쿼리는 오프셋 페이징보다 다음과 같은 이점을 제공합니다：

- 대규모 데이터 집합의 경우 “순서” 열이 인덱싱되어 있으면 커서 페이징이 더 나은 성능을 제공합니다. 이는 “offset” 절이 이전에 일치한 모든 데이터를 스캔하기 때문입니다。
- 자주 쓰는 데이터 집합의 경우， 오프셋 페이지 지정은 사용자가 현재 보고 있는 페이지에 최근에 결과가 추가되었거나 삭제된 경우 레코드를 건너뛰거나 중복된 항목을 표시할 수 있습니다。

그러나 커서 페이징에는 다음과 같은 제한이 있습니다：

- `simplePaginate` 와 마찬가지로 커서 페이지 지정은 “다음” 및 “이전” 링크를 표시하는 데만 사용할 수 있으며 페이지 번호가 있는 링크 생성을 지원하지 않습니다。
- 순서는 하나 이상의 고유한 열 또는 고유한 열의 조합을 기반으로 해야 합니다. `null` 값이 있는 열은 지원되지 않습니다。
- “order by” 절의 쿼리 표현식은 별칭이 지정되고 “select” 절에도 추가된 경우에만 지원됩니다。
- 매개변수가 있는 쿼리 표현식은 지원되지 않습니다。

<a name="manually-creating-a-paginator"></a>
### 페이지 매기기 수동 생성

때로는 이미 메모리에 있는 항목의 배열을 전달하여 페이지 인스턴스를 수동으로 생성하고 싶을 수 있습니다. 필요에 따라 `Illuminate\Pagination\Paginator`, `Illuminate\Pagination\LengthAwarePaginator` 또는 `Illuminate\Pagination\CursorPaginator` 인스턴스를 생성하여 이를 수행할 수 있습니다。

`Paginator` 및 `CursorPaginator` 클래스는 결과 세트의 총 항목 수를 알 필요가 없습니다. 하지만 이로 인해 이러한 클래스에는 마지막 페이지의 인덱스를 검색하는 메서드가 없습니다. `LengthAwarePaginator` 는 `Paginator` 와 거의 동일한 인수를 수락합니다. 하지만 결과 세트의 총 항目 수를 계산해야 합니다。

즉， `Paginator` 는 쿼리 빌더의 `simplePaginate` 메서드에 해당하고， `CursorPaginator` 는 `cursorPaginate` 메서드에 해당하며， `LengthAwarePaginator` 는 `paginate` 메서드에 해당합니다。

> [!WARNING]
페이지 편집기 인스턴스를 수동으로 생성할 때는 페이지 편집기에 전달하는 결과 배열을 수동으로 “슬라이스” 해야 합니다. 이 방법을 잘 모르는 경우 [array_slice](https://secure.php.net/manual/en/function.array-slice.php) PHP 함수를 확인하세요。

<a name="customizing-pagination-urls"></a>
### 페이지 구성 URL 사용자 지정



기본적으로, 페이지네이터가 생성하는 링크는 현재 요청의 URI와 일치합니다. 그러나 페이지네이터의 `withPath` 메서드를 사용하면 링크를 생성할 때 페이지네이터가 사용하는 URI를 사용자 정의할 수 있습니다. 예를 들어, 페이지네이터가 `http://example.com/admin/users?page=N`와 같은 링크를 생성하도록 하려면 `withPath` 메서드에 `/admin/users`를 전달해야 합니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->withPath('/admin/users');

    // ...
});
```



<a name="appending-query-string-values"></a>
#### 쿼리 문자열 값 추가하기

`appends` 메서드를 사용하여 페이지 네이션 링크의 쿼리 문자열에 값을 추가할 수 있습니다. 예를 들어, 각 페이지 네이션 링크에 `sort=votes`를 추가하려면 다음과 같이 `appends`를 호출해야 합니다:

```php
use App\Models\User;

Route::get('/users', function () {
    $users = User::paginate(15);

    $users->appends(['sort' => 'votes']);

    // ...
});
```



현재 요청의 쿼리 문자열 값을 모두 페이지 매김 링크에 추가하고 싶다면 `withQueryString` 방법을 사용할 수 있습니다:

```php
$users = User::paginate(15)->withQueryString();
```



<a name="appending-hash-fragments"></a>
#### 해시 조각 추가

페이징 생성기에서 생성된 URL에 '해시 조각'을 추가해야 하는 경우, `fragment` 메서드를 사용할 수 있습니다. 예를 들어, 각 페이지네이션 링크 끝에 `#users`를 추가하려면, 다음과 같이 `fragment` 메서드를 호출해야 합니다:

```php
$users = User::paginate(15)->fragment('users');
```



<a name="displaying-pagination-results"></a>
## 페이지네이션 결과 표시

`paginate` 메서드를 호출하면 `Illuminate\Pagination\LengthAwarePaginator` 인스턴스를 받게 되며, `simplePaginate` 메서드를 호출하면 `Illuminate\Pagination\Paginator` 인스턴스를 반환합니다. 마지막으로, `cursorPaginate` 메서드를 호출하면 `Illuminate\Pagination\CursorPaginator` 인스턴스를 반환합니다.

이 객체들은 결과 세트를 설명하는 여러 메서드를 제공합니다. 이러한 도우미 메서드 외에도, 페이지네이터 인스턴스는 반복자(iterator)이며 배열처럼 반복(loop)할 수 있습니다. 따라서 결과를 가져온 후, 결과를 표시하고 [Blade](/docs/{{version}}/blade)를 사용하여 페이지 링크를 렌더링할 수 있습니다:

```blade
<div class="container">
    @foreach ($users as $user)
        {{ $user->name }}
    @endforeach
</div>

{{ $users->links() }}
```



`links` 메서드는 결과 집합의 나머지 페이지에 대한 링크를 렌더링합니다. 이 링크 각각에는 이미 올바른 `page` 쿼리 문자열 변수가 포함되어 있습니다. `links` 메서드가 생성하는 HTML은 [Tailwind CSS 프레임워크](https://tailwindcss.com)와 호환된다는 점을 기억하세요.

<a name="adjusting-the-pagination-link-window"></a>
### 페이지 네비게이션 링크 창 조정

페이지네이터가 페이지 네비게이션 링크를 표시할 때 현재 페이지 번호와 현재 페이지 전후의 세 페이지에 대한 링크가 표시됩니다. `onEachSide` 메서드를 사용하면 페이지네이터가 생성한 링크의 중간 슬라이딩 창 내에서 현재 페이지 양쪽에 표시되는 추가 링크 수를 제어할 수 있습니다:

```blade
{{ $users->onEachSide(5)->links() }}
```



<a name="converting-results-to-json"></a>
### 결과를 JSON으로 변환하기

Laravel 페이징 클래스는 `Illuminate\Contracts\Support\Jsonable` 인터페이스 계약을 구현하고 `toJson` 메서드를 제공하므로, 페이징 결과를 JSON으로 변환하는 것이 매우 쉽습니다. 또한 라우트나 컨트롤러 액션에서 반환하여 페이징 인스턴스를 JSON으로 변환할 수도 있습니다:

```php
use App\Models\User;

Route::get('/users', function () {
    return User::paginate();
});
```



페이지네이터에서 가져온 JSON에는 `total`, `current_page`, `last_page` 등과 같은 메타 정보가 포함됩니다. 결과 레코드는 JSON 배열의 `data` 키를 통해 사용할 수 있습니다. 다음은 라우트에서 페이지네이터 인스턴스를 반환하여 생성된 JSON의 예입니다:

```json
{
   "total": 50,
   "per_page": 15,
   "current_page": 1,
   "last_page": 4,
   "current_page_url": "http://laravel.app?page=1",
   "first_page_url": "http://laravel.app?page=1",
   "last_page_url": "http://laravel.app?page=4",
   "next_page_url": "http://laravel.app?page=2",
   "prev_page_url": null,
   "path": "http://laravel.app",
   "from": 1,
   "to": 15,
   "data":[
        {
            // Record...
        },
        {
            // Record...
        }
   ]
}
```



<a name="customizing-the-pagination-view"></a>
## 페이지 매김 뷰 사용자 정의

기본적으로 페이지 매김 링크를 표시하기 위해 렌더링되는 뷰는 [Tailwind CSS](https://tailwindcss.com) 프레임워크와 호환됩니다. 그러나 Tailwind를 사용하지 않는 경우, 이러한 링크를 렌더링할 자신만의 뷰를 정의할 수 있습니다. 페이지 네이터 인스턴스에서 `links` 메서드를 호출할 때, 뷰 이름을 메서드의 첫 번째 인수로 전달할 수 있습니다:

```blade
{{ $paginator->links('view.name') }}

<!-- Passing additional data to the view... -->
{{ $paginator->links('view.name', ['foo' => 'bar']) }}
```



하지만 페이지 매김 보기를 사용자 정의하는 가장 쉬운 방법은 `vendor:publish` 명령을 사용하여 이를 `resources/views/vendor` 디렉터리로 내보내는 것입니다:

```shell
php artisan vendor:publish --tag=laravel-pagination
```



이 명령은 애플리케이션의 `resources/views/vendor/pagination` 디렉토리에 뷰를 배치합니다. 이 디렉토리 내의 `tailwind.blade.php` 파일은 기본 페이지 매김 뷰에 해당합니다. 이 파일을 편집하여 페이지 매김 HTML을 수정할 수 있습니다.

다른 파일을 기본 페이지 매김 뷰로 지정하고 싶다면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 페이지네이터의 `defaultView` 및 `defaultSimpleView` 메서드를 호출할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Pagination\Paginator;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Paginator::defaultView('view-name');

        Paginator::defaultSimpleView('view-name');
    }
}
```



<a name="using-bootstrap"></a>
### 부트스트랩 사용

Laravel은 [Bootstrap CSS](https://getbootstrap.com/)를 사용하여 만든 페이징 뷰를 포함합니다. 기본 Tailwind 뷰 대신 이러한 뷰를 사용하려면, `App\Providers\AppServiceProvider` 클래스의 `boot` 메서드 내에서 페이징 처리기의 `useBootstrapFour` 또는 `useBootstrapFive` 메서드를 호출할 수 있습니다:

```php
use Illuminate\Pagination\Paginator;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Paginator::useBootstrapFive();
    Paginator::useBootstrapFour();
}
```

<a name="paginator-instance-methods"></a>
## 페이징 처리기 / LengthAwarePaginator 인스턴스 메소드

각 페이징 처리기 인스턴스는 다음 메소드를 통해 추가적인 페이징 정보를 제공합니다:

<div class="overflow-auto">

| 방법 설명 설명 설명 설명
| —————————————————————————————————————————————————
| `$paginator->count()` 현재 페이지의 항목 수를 확인합니다. 현재 페이지의 항목을 확인합니다. 현재
| `$paginator->currentPage()` 현재 페이지 번호 가져오기. 현재 페이지 번호. 현재 페이지 번호를 가져오기。
| `$paginator->firstItem()`             | 결과에서 첫 번째 항목의 결과 번호를 얻습니다.           
| `$paginator->getOptions()` 페이지 지정기 옵션 가져오기。
| `$paginator->getUrlRange($start, $end)` | 페이지 지정 URL 의 범위를 생성합니다. 페이지 지정 URL 범위를 생성합니다. |
| `$paginator->hasPages()` 페이지 지정 옵션 | 여러 페이지로 나눌 수 있을 만큼 충분한 항목이 있는지 결정합니다. 페이지 지정 옵션
| `$paginator->hasMorePages()`  | 데이터스토어에 더 많은 항목이 있는지 결정합니다.            
| `$paginator->items()` 페이지 페이지 페이지 | 현재 페이지의 항목을 가져옵니다。
| `$paginator->lastItem()`             | 결과에서 마지막 항목의 결과 번호 얻기.           
| `$paginator->lastPage()` 페이지 번호 | 사용 가능한 마지막 페이지의 페이지 번호를 가져옵니다. (`simplePaginate` 를 사용할 때는 사용할 수 없습니다.) . . . . . . . . . . . .
| `$paginator->nextPageUrl()`             | 다음 페이지의 URL 을 가져옵니다.           
| `$paginator->onFirstPage()` 페이지 지정기가 첫 번째 페이지에 있는지 확인합니다. 페이지 지정기 페이지 지정기
| `$paginator->onLastPage()` 페이지 지정기가 마지막 페이지에 있는지 확인합니다. 페이지 지정기 페이지 지정기 페이 지정기 페이 지정기
| `$paginator->perPage()` 페이지당 표시되는 항목 수. 페이지당 표시되는 項目 수. 페이지당 표시될 항목 수。
| `$paginator->previousPageUrl()`  | 이전 페이지의 URL 을 가져옵니다. 페이지 페이지 페이지
| `$paginator->total()` 일치하는 항목의 총 수를 데이터 저장소에서 결정합니다. (`simplePaginate` 를 사용할 때는 사용할 수 없습니다.) |
| `$paginator->url($page)`             | 주어진 페이지 번호의 URL 을 가져옵니다.           
| `$paginator->getPageName()` 페이지를 저장하는 데 사용되는 쿼리 문자열 변수를 가져옵니다. 페이지
| `$paginator->setPageName($name)` | 페이지를 저장하는 데 사용되는 쿼리 문자열 변수를 설정합니다. 페이지 번호 |
| `$paginator->through($callback)` 변환 | 콜백을 사용하여 각 항목을 변환합니다. |

</div>

<a name="cursor-paginator-instance-methods"></a>
## 커서 페이지어 인스턴스 메서드

각 커서 페이지 매기기 인스턴스는 다음 방법을 통해 추가 페이지 매기기 정보를 제공합니다：

<div class="overflow-auto">

| 방법             |           
| —————————————————————————— —————————————————————————————————————————————
| `$paginator->count()`  | 현재 페이지의 항목 수를 가져옵니다.           |
| `$paginator->cursor()`  | 현재 커서 인스턴스를 가져옵니다.             |
| `$paginator->getOptions()` | 페이지 매기기 옵션을 가져옵니다. 페이지 매기기 옵션 가져옵니다。
| `$paginator->hasPages()` | 여러 페이지로 나누기에 충분한 항목이 있는지 확인합니다. |
| `$paginator->hasMorePages()` | 데이터 저장소에 더 많은 항목이 있는지 확인합니다.       |
| `$paginator->getCursorName()` | 커서를 저장하는 데 사용되는 쿼리 문자열 변수를 가져옵니다.  |
| `$paginator->items()`  | 현재 페이지의 항목을 가져옵니다.             |
| `$paginator->nextCursor()` | 다음 항목 집합의 커서 인스턴스를 가져옵니다.  |
| `$paginator->nextPageUrl()` | 다음 페이지의 URL 을 가져옵니다.             |
| `$paginator->onFirstPage()` | 페이지 지정기가 첫 번째 페이지에 있는지 확인합니다. . . . . . . . . . . . .
| `$paginator->onLastPage()` | 페이지 지정기가 마지막 페이지에 있는지 확인합니다.             |
| `$paginator->perPage()`  | 페이지당 표시할 항목 수.             |
| `$paginator->previousCursor()` | 이전 항목 집합의 커서 인스턴스를 가져옵니다.       |
| `$paginator->previousPageUrl()` | 이전 페이지의 URL 을 가져옵니다.            
| `$paginator->setCursorName()` | 커서를 저장하는 데 사용되는 쿼리 문자열 변수를 설정합니다.  |
| `$paginator->url($cursor)` | 주어진 커서 인스턴스의 URL 을 가져옵니다.             |

</div>
{% endraw %}
