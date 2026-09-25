---
layout: docs
title: "Database: Query Builder"
---

{% raw %}
# Database: Query Builder

- [Introduction](#introduction)
- [Running Database Queries](#running-database-queries)
    - [Chunking Results](#chunking-results)
    - [Streaming Results Lazily](#streaming-results-lazily)
    - [Aggregates](#aggregates)
- [Select Statements](#select-statements)
- [Raw Expressions](#raw-expressions)
- [Joins](#joins)
- [Unions](#unions)
- [Basic Where Clauses](#basic-where-clauses)
    - [Where Clauses](#where-clauses)
    - [Or Where Clauses](#or-where-clauses)
    - [Where Not Clauses](#where-not-clauses)
    - [Where Any / All / None Clauses](#where-any-all-none-clauses)
    - [JSON Where Clauses](#json-where-clauses)
    - [Additional Where Clauses](#additional-where-clauses)
    - [Logical Grouping](#logical-grouping)
- [Advanced Where Clauses](#advanced-where-clauses)
    - [Where Exists Clauses](#where-exists-clauses)
    - [Subquery Where Clauses](#subquery-where-clauses)
    - [Full Text Where Clauses](#full-text-where-clauses)
    - [Vector Similarity Clauses](#vector-similarity-clauses)
- [Ordering, Grouping, Limit and Offset](#ordering-grouping-limit-and-offset)
    - [Ordering](#ordering)
    - [Grouping](#grouping)
    - [Limit and Offset](#limit-and-offset)
- [Conditional Clauses](#conditional-clauses)
- [Insert Statements](#insert-statements)
    - [Upserts](#upserts)
- [Update Statements](#update-statements)
    - [Updating JSON Columns](#updating-json-columns)
    - [Increment and Decrement](#increment-and-decrement)
- [Delete Statements](#delete-statements)
- [Pessimistic Locking](#pessimistic-locking)
- [Reusable Query Components](#reusable-query-components)
- [Debugging](#debugging)

<a name="introduction"></a>
## Introduction

Laravel's database query builder provides a convenient, fluent interface to creating and running database queries. It can be used to perform most database operations in your application and works perfectly with all of Laravel's supported database systems.

The Laravel query builder uses PDO parameter binding to protect your application against SQL injection attacks. There is no need to clean or sanitize strings passed to the query builder as query bindings.

> [!WARNING]
> PDO does not support binding column names. Therefore, you should never allow user input to dictate the column names referenced by your queries, including "order by" columns.

<a name="running-database-queries"></a>
## Running Database Queries



<a name="retrieving-all-rows-from-a-table"></a>
#### 테이블에서 모든 행 가져오기

쿼리를 시작하기 위해 `DB` 퍼사드에서 제공하는 `table` 메서드를 사용할 수 있습니다. `table` 메서드는 지정된 테이블에 대한 유창한 쿼리 빌더 인스턴스를 반환하여, 쿼리에 더 많은 제약 조건을 연결한 다음 `get` 메서드를 사용하여 쿼리의 결과를 최종적으로 가져올 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class UserController extends Controller
{
    /**
     * Show a list of all of the application's users.
     */
    public function index(): View
    {
        $users = DB::table('users')->get();

        return view('user.index', ['users' => $users]);
    }
}
```



`get` 메서드는 쿼리 결과를 포함하는 `Illuminate\Support\Collection` 인스턴스를 반환하며, 각 결과는 PHP `stdClass` 객체의 인스턴스입니다. 객체의 속성으로 열에 접근하여 각 열의 값을 확인할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->get();

foreach ($users as $user) {
    echo $user->name;
}
```



> [!NOTE]
> Laravel 컬렉션은 데이터를 매핑하고 축소하는 데 매우 강력한 다양한 메서드를 제공합니다. Laravel 컬렉션에 대한 자세한 정보는 [컬렉션 문서](/docs/{{version}}/collections)를 확인하세요.

<a name="retrieving-a-single-row-column-from-a-table"></a>
#### 테이블에서 단일 행 / 열 가져오기

데이터베이스 테이블에서 단일 행만 가져와야 하는 경우 `DB` 퍼사드의 `first` 메서드를 사용할 수 있습니다. 이 메서드는 단일 `stdClass` 객체를 반환합니다:

```php
$user = DB::table('users')->where('name', 'John')->first();

return $user->email;
```



데이터베이스 테이블에서 단일 행을 검색하고 싶지만, 일치하는 행이 없으면 `Illuminate\Database\RecordNotFoundException`를 발생시키고 싶다면 `firstOrFail` 메서드를 사용할 수 있습니다. `RecordNotFoundException`를 잡지 않으면, 404 HTTP 응답이 자동으로 클라이언트에 전송됩니다:

```php
$user = DB::table('users')->where('name', 'John')->firstOrFail();
```



전체 행이 필요하지 않은 경우 `value` 메서드를 사용하여 레코드에서 단일 값을 추출할 수 있습니다. 이 메서드는 열의 값을 직접 반환합니다:

```php
$email = DB::table('users')->where('name', 'John')->value('email');
```



`id` 열 값으로 단일 행을 검색하려면, `find` 메서드를 사용하세요:

```php
$user = DB::table('users')->find(3);
```



<a name="retrieving-a-list-of-column-values"></a>
#### 열 값 목록 가져오기

단일 열의 값을 포함하는 `Illuminate\Support\Collection` 인스턴스를 가져오려면 `pluck` 메서드를 사용할 수 있습니다. 이 예제에서는 사용자 제목 모음을 가져옵니다:

```php
use Illuminate\Support\Facades\DB;

$titles = DB::table('users')->pluck('title');

foreach ($titles as $title) {
    echo $title;
}
```



`pluck` 메서드에 두 번째 인수를 제공하여 결과 컬렉션이 키로 사용할 열을 지정할 수 있습니다:

```php
$titles = DB::table('users')->pluck('title', 'name');

foreach ($titles as $name => $title) {
    echo $title;
}
```



<a name="chunking-results"></a>
### 청크 처리 결과

수천 개의 데이터베이스 레코드를 처리해야 하는 경우, `DB` 파사드에서 제공하는 `chunk` 메서드를 사용하는 것을 고려하세요. 이 메서드는 한 번에 작은 청크의 결과를 가져오고 각 청크를 클로저로 전달하여 처리합니다. 예를 들어, `users` 테이블 전체를 한 번에 100개 레코드씩 청크로 가져와 보겠습니다:

```php
use Illuminate\Support\Collection;
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    foreach ($users as $user) {
        // ...
    }
});
```



클로저에서 `false`를 반환하면 추가 청크 처리를 중단할 수 있습니다:

```php
DB::table('users')->orderBy('id')->chunk(100, function (Collection $users) {
    // Process the records...

    return false;
});
```



결과를 청크 처리하면서 데이터베이스 레코드를 업데이트하는 경우, 청크된 결과가 예상치 못한 방식으로 변경될 수 있습니다. 청크 처리 중에 검색된 레코드를 업데이트할 계획이라면, 항상 대신 `chunkById` 방법을 사용하는 것이 가장 좋습니다. 이 방법은 레코드의 기본 키를 기준으로 결과를 자동으로 페이징합니다:

```php
DB::table('users')->where('active', false)
    ->chunkById(100, function (Collection $users) {
        foreach ($users as $user) {
            DB::table('users')
                ->where('id', $user->id)
                ->update(['active' => true]);
        }
    });
```



`chunkById` 및 `lazyById` 메서드가 실행 중인 쿼리에 자체적인 "where" 조건을 추가하기 때문에, 일반적으로 자신의 조건을 클로저 안에서 [논리적으로 그룹화](#logical-grouping)해야 합니다:

```php
DB::table('users')->where(function ($query) {
    $query->where('credits', 1)->orWhere('credits', 2);
})->chunkById(100, function (Collection $users) {
    foreach ($users as $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['credits' => 3]);
    }
});
```



> [!WARNING]
> 청크 콜백 안에서 레코드를 업데이트하거나 삭제할 때, 기본 키나 외래 키에 대한 변경 사항은 청크 쿼리에 영향을 미칠 수 있습니다. 이는 결과적으로 레코드가 청크 처리된 결과에 포함되지 않을 가능성을 초래할 수 있습니다.

<a name="streaming-results-lazily"></a>
### 결과를 느리게 스트리밍하기

`lazy` 메서드는 [chunk 메서드](#chunking-results)와 유사하게 쿼리를 청크 단위로 실행한다는 점에서 비슷하게 작동합니다. 그러나 각 청크를 콜백으로 전달하는 대신, `lazy()` 메서드는 [LazyCollection](/docs/{{version}}/collections#lazy-collections)을 반환하여 결과를 단일 스트림으로 상호작용할 수 있게 합니다:

```php
use Illuminate\Support\Facades\DB;

DB::table('users')->orderBy('id')->lazy()->each(function (object $user) {
    // ...
});
```



다시 말하지만, 가져온 레코드를 순회하면서 업데이트할 계획이라면 대신 `lazyById` 또는 `lazyByIdDesc` 메서드를 사용하는 것이 가장 좋습니다. 이 메서드들은 레코드의 기본 키를 기준으로 결과를 자동으로 페이지 처리합니다:

```php
DB::table('users')->where('active', false)
    ->lazyById()->each(function (object $user) {
        DB::table('users')
            ->where('id', $user->id)
            ->update(['active' => true]);
    });
```



> [!WARNING]
> 레코드를 반복하면서 업데이트하거나 삭제할 때, 기본 키나 외래 키의 변경은 청크 쿼리에 영향을 미칠 수 있습니다. 이는 결과에 일부 레코드가 포함되지 않게 될 가능성이 있습니다.

<a name="aggregates"></a>
### 집계

쿼리 빌더는 `count`, `max`, `min`, `avg`, `sum`와 같은 집계 값을 가져오기 위한 다양한 메서드를 제공합니다. 쿼리를 구성한 후 이러한 메서드 중 어떤 것이든 호출할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')->count();

$price = DB::table('orders')->max('price');
```



물론, 집계 값이 계산되는 방식을 세밀하게 조정하기 위해 이러한 방법들을 다른 절과 결합할 수도 있습니다:

```php
$price = DB::table('orders')
    ->where('finalized', 1)
    ->avg('price');
```



<a name="determining-if-records-exist"></a>
#### 레코드 존재 여부 확인

쿼리의 조건과 일치하는 레코드가 존재하는지 확인하기 위해 `count` 방법을 사용하는 대신, `exists` 및 `doesntExist` 방법을 사용할 수 있습니다:

```php
if (DB::table('orders')->where('finalized', 1)->exists()) {
    // ...
}

if (DB::table('orders')->where('finalized', 1)->doesntExist()) {
    // ...
}
```



<a name="select-statements"></a>
## 선택 구문

<a name="specifying-a-select-clause"></a>
#### 선택 절 지정하기

항상 데이터베이스 테이블의 모든 열을 선택하고 싶지 않을 수 있습니다. `select` 메서드를 사용하면 쿼리에 대한 사용자 정의 '선택' 절을 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->select('name', 'email as user_email')
    ->get();
```



`distinct` 방법을 사용하면 쿼리가 고유한 결과를 반환하도록 강제할 수 있습니다:

```php
$users = DB::table('users')->distinct()->get();
```



이미 쿼리 빌더 인스턴스가 있고 기존 선택 절에 열을 추가하려는 경우, `addSelect` 메서드를 사용할 수 있습니다:

```php
$query = DB::table('users')->select('name');

$users = $query->addSelect('age')->get();
```



<a name="raw-expressions"></a>
## 원시 표현식

때때로 쿼리에 임의의 문자열을 삽입해야 할 때가 있습니다. 원시 문자열 표현식을 만들기 위해, `DB` 퍼사드에서 제공하는 `raw` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->select(DB::raw('count(*) as user_count, status'))
    ->where('status', '<>', 1)
    ->groupBy('status')
    ->get();
```



> [!WARNING]
> 원시 구문은 문자열로 쿼리에 삽입되므로 SQL 인젝션 취약점을 생성하지 않도록 매우 주의해야 합니다.

<a name="raw-methods"></a>
### 원시 메서드

`DB::raw` 메서드를 사용하는 대신, 쿼리의 여러 부분에 원시 표현식을 삽입하기 위해 다음 메서드도 사용할 수 있습니다. **Laravel은 원시 표현식을 사용하는 쿼리가 SQL 인젝션 취약점으로부터 안전하다고 보장할 수 없습니다.**

<a name="selectraw"></a>
#### `selectRaw`

`selectRaw` 메서드는 `addSelect(DB::raw(/* ... */))` 대신 사용할 수 있습니다. 이 메서드는 선택적 배열 바인딩을 두 번째 인자로 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->selectRaw('price * ? as price_with_tax', [1.0825])
    ->get();
```



<a name="whereraw-orwhereraw"></a>
#### `whereRaw / orWhereRaw`

`whereRaw` 및 `orWhereRaw` 메서드는 쿼리에 원시 "where" 절을 주입하는 데 사용할 수 있습니다. 이러한 메서드는 두 번째 인수로 선택적인 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->whereRaw('price > IF(state = "TX", ?, 100)', [200])
    ->get();
```



<a name="havingraw-orhavingraw"></a>
#### `havingRaw / orHavingRaw`

`havingRaw`와 `orHavingRaw` 메서드는 "having" 절의 값으로 원시 문자열을 제공하는 데 사용할 수 있습니다. 이 메서드들은 선택적으로 두 번째 인수로 바인딩 배열을 받을 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('department', DB::raw('SUM(price) as total_sales'))
    ->groupBy('department')
    ->havingRaw('SUM(price) > ?', [2500])
    ->get();
```



<a name="orderbyraw"></a>
#### `orderByRaw`

`orderByRaw` 메서드는 "order by" 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다:

```php
$orders = DB::table('orders')
    ->orderByRaw('updated_at - created_at DESC')
    ->get();
```



<a name="groupbyraw"></a>
#### `groupByRaw`

`groupByRaw` 방법은 `group by` 절의 값으로 원시 문자열을 제공하는 데 사용될 수 있습니다:

```php
$orders = DB::table('orders')
    ->select('city', 'state')
    ->groupByRaw('city, state')
    ->get();
```



<a name="joins"></a>
## 조인

<a name="inner-join-clause"></a>
#### 내부 조인 절

쿼리 빌더는 쿼리에 조인 절을 추가하는 데에도 사용할 수 있습니다. 기본적인 "내부 조인"을 수행하려면, 쿼리 빌더 인스턴스에서 `join` 메서드를 사용할 수 있습니다. `join` 메서드에 전달되는 첫 번째 인자는 조인하려는 테이블의 이름이고, 나머지 인자는 조인을 위한 컬럼 제약 조건을 지정합니다. 한 쿼리에서 여러 테이블을 조인할 수도 있습니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::table('users')
    ->join('contacts', 'users.id', '=', 'contacts.user_id')
    ->join('orders', 'users.id', '=', 'orders.user_id')
    ->select('users.*', 'contacts.phone', 'orders.price')
    ->get();
```



<a name="left-join-right-join-clause"></a>
#### 왼쪽 조인 / 오른쪽 조인 절

"내부 조인" 대신 "왼쪽 조인" 또는 "오른쪽 조인"을 수행하려면 `leftJoin` 또는 `rightJoin` 메서드를 사용하십시오. 이 메서드들은 `join` 메서드와 동일한 시그니처를 갖습니다:

```php
$users = DB::table('users')
    ->leftJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();

$users = DB::table('users')
    ->rightJoin('posts', 'users.id', '=', 'posts.user_id')
    ->get();
```



<a name="cross-join-clause"></a>
#### 크로스 조인 절

"크로스 조인"을 수행하려면 `crossJoin` 방법을 사용할 수 있습니다. 크로스 조인은 첫 번째 테이블과 조인된 테이블 간에 데카르트 곱을 생성합니다:

```php
$sizes = DB::table('sizes')
    ->crossJoin('colors')
    ->get();
```



<a name="advanced-join-clauses"></a>
#### 고급 조인 절

더 고급 조인 절을 지정할 수도 있습니다. 시작하려면 `join` 메서드의 두 번째 인수로 클로저를 전달하세요. 클로저는 "join" 절에 대한 제약을 지정할 수 있는 `Illuminate\Database\Query\JoinClause` 인스턴스를 받게 됩니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')->orOn(/* ... */);
    })
    ->get();
```



조인에서 "where" 절을 사용하고 싶다면 `JoinClause` 인스턴스가 제공하는 `where` 및 `orWhere` 메서드를 사용할 수 있습니다. 두 열을 비교하는 대신, 이 메서드들은 열을 값과 비교할 것입니다:

```php
DB::table('users')
    ->join('contacts', function (JoinClause $join) {
        $join->on('users.id', '=', 'contacts.user_id')
            ->where('contacts.user_id', '>', 5);
    })
    ->get();
```



<a name="subquery-joins"></a>
#### 서브쿼리 조인

쿼리를 서브쿼리에 조인할 때 `joinSub`, `leftJoinSub`, `rightJoinSub` 메서드를 사용할 수 있습니다. 이 메서드 각각은 세 개의 인수를 받습니다: 서브쿼리, 그 서브쿼리의 테이블 별칭, 그리고 관련 열을 정의하는 클로저입니다. 이 예제에서는 각 사용자 레코드에 사용자가 가장 최근에 게시한 블로그 게시물의 `created_at` 타임스탬프도 포함된 사용자 컬렉션을 검색할 것입니다:

```php
$latestPosts = DB::table('posts')
    ->select('user_id', DB::raw('MAX(created_at) as last_post_created_at'))
    ->where('is_published', true)
    ->groupBy('user_id');

$users = DB::table('users')
    ->joinSub($latestPosts, 'latest_posts', function (JoinClause $join) {
        $join->on('users.id', '=', 'latest_posts.user_id');
    })->get();
```



<a name="lateral-joins"></a>
#### 측면 조인 (Lateral Joins)

> [!WARNING]
> 측면 조인은 현재 PostgreSQL, MySQL >= 8.0.14, 및 SQL Server에서 지원됩니다.

서브쿼리를 사용하여 "측면 조인"을 수행하기 위해 `joinLateral` 및 `leftJoinLateral` 메서드를 사용할 수 있습니다. 각 메서드는 두 개의 인수를 받습니다: 서브쿼리와 그 테이블 별칭. 조인 조건은 주어진 서브쿼리의 `where` 절 내에서 지정해야 합니다. 측면 조인은 각 행마다 평가되며 서브쿼리 외부의 열을 참조할 수 있습니다.

이 예제에서는 사용자 컬렉션과 각 사용자의 최근 3개 블로그 게시물을 가져옵니다. 각 사용자는 결과 집합에서 최대 3개의 행을 생성할 수 있습니다: 각 사용자의 최근 블로그 게시물마다 한 행씩. 조인 조건은 현재 사용자 행을 참조하여 서브쿼리 내 `whereColumn` 절로 지정됩니다:

```php
$latestPosts = DB::table('posts')
    ->select('id as post_id', 'title as post_title', 'created_at as post_created_at')
    ->whereColumn('user_id', 'users.id')
    ->orderBy('created_at', 'desc')
    ->limit(3);

$users = DB::table('users')
    ->joinLateral($latestPosts, 'latest_posts')
    ->get();
```



<a name="unions"></a>
## 합집합

쿼리 빌더는 또한 두 개 이상의 쿼리를 함께 "합집합"으로 결합하는 편리한 방법을 제공합니다. 예를 들어, 초기 쿼리를 생성하고 `union` 메서드를 사용하여 다른 쿼리와 합집합을 만들 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

$usersWithoutFirstName = DB::table('users')
    ->whereNull('first_name');

$users = DB::table('users')
    ->whereNull('last_name')
    ->union($usersWithoutFirstName)
    ->get();
```



`union` 메서드 외에도, 쿼리 빌더는 `unionAll` 메서드를 제공합니다. `unionAll` 메서드를 사용하여 결합된 쿼리는 중복 결과가 제거되지 않습니다. `unionAll` 메서드는 `union` 메서드와 동일한 메서드 시그니처를 가집니다.

<a name="basic-where-clauses"></a>
## 기본 Where 절

<a name="where-clauses"></a>
### Where 절

쿼리 빌더의 `where` 메서드를 사용하여 쿼리에 'where' 절을 추가할 수 있습니다. `where` 메서드에 대한 가장 기본적인 호출은 세 개의 인수를 필요로 합니다. 첫 번째 인수는 컬럼의 이름입니다. 두 번째 인수는 연산자로, 데이터베이스가 지원하는 어떤 연산자도 될 수 있습니다. 세 번째 인수는 컬럼의 값과 비교할 값입니다.

예를 들어, 다음 쿼리는 `votes` 컬럼의 값이 `100`와 같고 `age` 컬럼의 값이 `35`보다 큰 사용자들을 검색합니다:

```php
$users = DB::table('users')
    ->where('votes', '=', 100)
    ->where('age', '>', 35)
    ->get();
```



편의를 위해, 특정 값에 대해 열이 `=`인지 확인하고 싶다면, 값을 `where` 메서드의 두 번째 인수로 전달할 수 있습니다. Laravel은 `=` 연산자를 사용하고 싶어한다고 가정합니다:

```php
$users = DB::table('users')->where('votes', 100)->get();
```



여러 열에 대해 빠르게 조회하기 위해 `where` 메서드에 연관 배열을 제공할 수도 있습니다:

```php
$users = DB::table('users')->where([
    'first_name' => 'Jane',
    'last_name' => 'Doe',
])->get();
```



앞서 언급했듯이, 데이터베이스 시스템에서 지원하는 모든 연산자를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>=', 100)
    ->get();

$users = DB::table('users')
    ->where('votes', '<>', 100)
    ->get();

$users = DB::table('users')
    ->where('name', 'like', 'T%')
    ->get();
```



`where` 함수에 조건 배열을 전달할 수도 있습니다. 배열의 각 요소는 일반적으로 `where` 메서드에 전달되는 세 개의 인수를 포함하는 배열이어야 합니다:

```php
$users = DB::table('users')->where([
    ['status', '=', '1'],
    ['subscribed', '<>', '1'],
])->get();
```



> [!WARNING]
> PDO는 컬럼 이름 바인딩을 지원하지 않습니다. 따라서 쿼리에서 참조되는 컬럼 이름, 'order by' 컬럼을 포함하여, 사용자 입력이 컬럼 이름을 결정하도록 절대 허용해서는 안 됩니다.

> [!WARNING]
> MySQL과 MariaDB는 문자열-숫자 비교에서 문자열을 자동으로 정수로 형 변환합니다. 이 과정에서 숫자가 아닌 문자열은 `0`로 변환되며, 이는 예상치 못한 결과를 초래할 수 있습니다. 예를 들어, 테이블에 `secret` 컬럼이 `aaa` 값을 가지고 있고 `User::where('secret', 0)`를 실행하면, 해당 행이 반환됩니다. 이를 방지하려면 쿼리에서 값을 사용하기 전에 모든 값을 적절한 타입으로 형 변환해야 합니다.

<a name="or-where-clauses"></a>
### 또는 Where 절

쿼리 빌더의 `where` 메서드 호출을 연쇄적으로 연결할 때, 'where' 절은 `and` 연산자를 사용하여 함께 결합됩니다. 그러나 `orWhere` 메서드를 사용하여 `or` 연산자를 사용하여 절을 쿼리에 결합할 수도 있습니다. `orWhere` 메서드는 `where` 메서드와 동일한 인수를 받습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere('name', 'John')
    ->get();
```



만약 괄호 안에 '또는(or)' 조건을 그룹화해야 한다면, `orWhere` 메서드의 첫 번째 인자로 클로저를 전달할 수 있습니다:

```php
use Illuminate\Database\Query\Builder;

$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhere(function (Builder $query) {
        $query->where('name', 'Abigail')
            ->where('votes', '>', 50);
        })
    ->get();
```



위의 예제는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where votes > 100 or (name = 'Abigail' and votes > 50)
```



> [!WARNING]
> 전역 스코프가 적용될 때 예상치 못한 동작을 피하기 위해 `orWhere` 호출을 항상 그룹화해야 합니다.

<a name="where-not-clauses"></a>
### Where Not 절

`whereNot` 및 `orWhereNot` 메서드는 주어진 쿼리 제약 조건 그룹을 부정하는 데 사용할 수 있습니다. 예를 들어, 다음 쿼리는 클리어런스 중이거나 가격이 10보다 작은 제품을 제외합니다:

```php
$products = DB::table('products')
    ->whereNot(function (Builder $query) {
        $query->where('clearance', true)
            ->orWhere('price', '<', 10);
        })
    ->get();
```



<a name="where-any-all-none-clauses"></a>
### 어떤 / 모든 / 없는 절

때때로 여러 열에 동일한 쿼리 제약 조건을 적용해야 할 때가 있습니다. 예를 들어, 주어진 목록의 열 중 어느 하나라도 특정 값인 모든 레코드를 검색하고 싶을 수 있습니다. 이는 `whereAny` 방법을 사용하여 수행할 수 있습니다:

```php
$users = DB::table('users')
    ->where('active', true)
    ->whereAny([
        'name',
        'email',
        'phone',
    ], 'like', 'Example%')
    ->get();
```



위의 쿼리는 다음 SQL을 생성합니다:

```sql
SELECT *
FROM users
WHERE active = true AND (
    name LIKE 'Example%' OR
    email LIKE 'Example%' OR
    phone LIKE 'Example%'
)
```



마찬가지로, `whereAll` 방법은 주어진 제약 조건과 모든 지정된 열이 일치하는 레코드를 검색하는 데 사용될 수 있습니다:

```php
$posts = DB::table('posts')
    ->where('published', true)
    ->whereAll([
        'title',
        'content',
    ], 'like', '%Laravel%')
    ->get();
```



위의 쿼리는 다음 SQL을 생성합니다:

```sql
SELECT *
FROM posts
WHERE published = true AND (
    title LIKE '%Laravel%' AND
    content LIKE '%Laravel%'
)
```



`whereNone` 방법은 주어진 열 중 어느 것도 지정된 제약 조건과 일치하지 않는 레코드를 검색하는 데 사용할 수 있습니다:

```php
$albums = DB::table('albums')
    ->where('published', true)
    ->whereNone([
        'title',
        'lyrics',
        'tags',
    ], 'like', '%explicit%')
    ->get();
```



위의 쿼리는 다음 SQL을 생성합니다:

```sql
SELECT *
FROM albums
WHERE published = true AND NOT (
    title LIKE '%explicit%' OR
    lyrics LIKE '%explicit%' OR
    tags LIKE '%explicit%'
)
```



<a name="json-where-clauses"></a>
### JSON 조건절

Laravel은 또한 JSON 열 타입을 지원하는 데이터베이스에서 JSON 열 타입에 대한 쿼리도 지원합니다. 현재 이것에는 MariaDB 10.3+, MySQL 8.0+, PostgreSQL 12.0+, SQL Server 2017+, 및 SQLite 3.39.0+이 포함됩니다. JSON 열을 쿼리하려면 `->` 연산자를 사용하세요:

```php
$users = DB::table('users')
    ->where('preferences->dining->meal', 'salad')
    ->get();

$users = DB::table('users')
    ->whereIn('preferences->dining->meal', ['pasta', 'salad', 'sandwiches'])
    ->get();
```



JSON 배열을 쿼리하기 위해 `whereJsonContains` 및 `whereJsonDoesntContain` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', 'en')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', 'en')
    ->get();
```



애플리케이션이 MariaDB, MySQL 또는 PostgreSQL 데이터베이스를 사용하는 경우, `whereJsonContains` 및 `whereJsonDoesntContain` 메서드에 값 배열을 전달할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContains('options->languages', ['en', 'de'])
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContain('options->languages', ['en', 'de'])
    ->get();
```



또한, JSON 키를 포함하거나 포함하지 않는 결과를 가져오기 위해 `whereJsonContainsKey` 또는 `whereJsonDoesntContainKey` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonContainsKey('preferences->dietary_requirements')
    ->get();

$users = DB::table('users')
    ->whereJsonDoesntContainKey('preferences->dietary_requirements')
    ->get();
```



마지막으로, `whereJsonLength` 방법을 사용하여 JSON 배열을 길이로 조회할 수 있습니다:

```php
$users = DB::table('users')
    ->whereJsonLength('options->languages', 0)
    ->get();

$users = DB::table('users')
    ->whereJsonLength('options->languages', '>', 1)
    ->get();
```



<a name="additional-where-clauses"></a>
### 추가 Where 절

**whereLike / orWhereLike / whereNotLike / orWhereNotLike**

`whereLike` 메서드는 패턴 매칭을 위해 쿼리에 'LIKE' 절을 추가할 수 있게 해줍니다. 이 메서드들은 데이터베이스에 구애받지 않고 문자열 매칭 쿼리를 수행할 수 있는 방법을 제공하며, 대소문자 구분을 켜고 끌 수 있는 기능도 제공합니다. 기본적으로 문자열 매칭은 대소문자를 구분하지 않습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%')
    ->get();
```



`caseSensitive` 인수를 통해 대소문자를 구분하는 검색을 활성화할 수 있습니다:

```php
$users = DB::table('users')
    ->whereLike('name', '%John%', caseSensitive: true)
    ->get();
```



`orWhereLike` 방법을 사용하면 LIKE 조건과 함께 '또는(or)' 절을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereLike('name', '%John%')
    ->get();
```



`whereNotLike` 메서드를 사용하면 쿼리에 "NOT LIKE" 절을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->whereNotLike('name', '%John%')
    ->get();
```



유사하게, `orWhereNotLike`를 사용하여 NOT LIKE 조건과 함께 '또는(or)' 절을 추가할 수 있습니다:

```php
$users = DB::table('users')
    ->where('votes', '>', 100)
    ->orWhereNotLike('name', '%John%')
    ->get();
```



> [!WARNING]
> SQL Server에서는 현재 `whereLike` 대소문자 구분 검색 옵션이 지원되지 않습니다.

**whereIn / whereNotIn / orWhereIn / orWhereNotIn**

`whereIn` 메서드는 주어진 열의 값이 주어진 배열에 포함되어 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereIn('id', [1, 2, 3])
    ->get();
```



`whereNotIn` 메서드는 지정된 열의 값이 주어진 배열에 포함되어 있지 않은지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotIn('id', [1, 2, 3])
    ->get();
```



또한 `whereIn` 메서드의 두 번째 인자로 쿼리 객체를 제공할 수 있습니다:

```php
$activeUsers = DB::table('users')->select('id')->where('is_active', 1);

$comments = DB::table('comments')
    ->whereIn('user_id', $activeUsers)
    ->get();
```



위의 예제는 다음과 같은 SQL을 생성합니다:

```sql
select * from comments where user_id in (
    select id
    from users
    where is_active = 1
)
```



> [!WARNING]
> 쿼리에 대량의 정수 바인딩 배열을 추가하는 경우, `whereIntegerInRaw` 또는 `whereIntegerNotInRaw` 메서드를 사용하여 메모리 사용량을 크게 줄일 수 있습니다.

**whereBetween / orWhereBetween**

`whereBetween` 메서드는 컬럼의 값이 두 값 사이에 있는지 확인합니다:

```php
$users = DB::table('users')
    ->whereBetween('votes', [1, 100])
    ->get();
```



**whereNotBetween / orWhereNotBetween**

`whereNotBetween` 메서드는 컬럼의 값이 두 값 사이에 있지 않은지 확인합니다:

```php
$users = DB::table('users')
    ->whereNotBetween('votes', [1, 100])
    ->get();
```



**whereBetweenColumns / whereNotBetweenColumns / orWhereBetweenColumns / orWhereNotBetweenColumns**

`whereBetweenColumns` 메서드는 한 테이블 행에서 특정 컬럼의 값이 두 컬럼의 두 값 사이에 있는지 확인합니다:

```php
$patients = DB::table('patients')
    ->whereBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```



`whereNotBetweenColumns` 방법은 한 열의 값이 동일한 테이블 행의 두 열 값 사이에 있지 않음을 검증합니다:

```php
$patients = DB::table('patients')
    ->whereNotBetweenColumns('weight', ['minimum_allowed_weight', 'maximum_allowed_weight'])
    ->get();
```



**whereValueBetween / whereValueNotBetween / orWhereValueBetween / orWhereValueNotBetween**

`whereValueBetween` 메서드는 주어진 값이 동일한 테이블 행의 동일한 유형 두 열 값 사이에 있는지 확인합니다:

```php
$products = DB::table('products')
    ->whereValueBetween(100, ['min_price', 'max_price'])
    ->get();
```



`whereValueNotBetween` 방법은 값이 동일한 테이블 행의 두 열 값 밖에 있는지 확인합니다:

```php
$products = DB::table('products')
    ->whereValueNotBetween(100, ['min_price', 'max_price'])
    ->get();
```



**whereNull / whereNotNull / orWhereNull / orWhereNotNull**

`whereNull` 메서드는 주어진 열의 값이 `NULL`인지 확인합니다:

```php
$users = DB::table('users')
    ->whereNull('updated_at')
    ->get();
```



`whereNotNull` 방법은 해당 열의 값이 `NULL`가 아님을 확인합니다:

```php
$users = DB::table('users')
    ->whereNotNull('updated_at')
    ->get();
```



**whereNullSafeEquals / orWhereNullSafeEquals**

`whereNullSafeEquals` 및 `orWhereNullSafeEquals` 메서드는 두 `NULL` 값을 동일하게 취급하면서 열의 값을 주어진 값과 비교하는 데 사용할 수 있습니다:

```php
$lastLoginIp = $request->input('last_login_ip');

$users = DB::table('users')
    ->whereNullSafeEquals('last_login_ip', $lastLoginIp)
    ->get();
```



**whereDate / whereMonth / whereDay / whereYear / whereTime**

`whereDate` 메서드는 열의 값을 날짜와 비교할 때 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereDate('created_at', '2016-12-31')
    ->get();
```



`whereMonth` 방법은 열의 값을 특정 월과 비교하는 데 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereMonth('created_at', '12')
    ->get();
```



`whereDay` 방법은 열의 값을 특정 월의 날짜와 비교하는 데 사용될 수 있습니다:

```php
$users = DB::table('users')
    ->whereDay('created_at', '31')
    ->get();
```



`whereYear` 방법은 열의 값을 특정 연도와 비교하는 데 사용될 수 있습니다:

```php
$users = DB::table('users')
    ->whereYear('created_at', '2016')
    ->get();
```



`whereTime` 방법은 열의 값을 특정 시간과 비교하는 데 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereTime('created_at', '=', '11:20:45')
    ->get();
```



**wherePast / whereFuture / whereToday / whereBeforeToday / whereAfterToday**

`wherePast` 및 `whereFuture` 메서드는 열의 값이 과거인지 미래인지 판단하는 데 사용될 수 있습니다:

```php
$invoices = DB::table('invoices')
    ->wherePast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereFuture('due_at')
    ->get();
```



`whereNowOrPast` 및 `whereNowOrFuture` 방법은 열의 값이 현재 날짜와 시간을 포함하여 과거인지 미래인지를 확인하는 데 사용할 수 있습니다:

```php
$invoices = DB::table('invoices')
    ->whereNowOrPast('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereNowOrFuture('due_at')
    ->get();
```



`whereToday`, `whereBeforeToday`, `whereAfterToday` 메서드는 각각 열의 값이 오늘인지, 오늘 이전인지, 오늘 이후인지 확인하는 데 사용할 수 있습니다:

```php
$invoices = DB::table('invoices')
    ->whereToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereBeforeToday('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereAfterToday('due_at')
    ->get();
```



마찬가지로, `whereTodayOrBefore` 및 `whereTodayOrAfter` 방법은 열의 값이 오늘 이전인지 오늘 이후인지(오늘 날짜 포함)를 확인하는 데 사용할 수 있습니다:

```php
$invoices = DB::table('invoices')
    ->whereTodayOrBefore('due_at')
    ->get();

$invoices = DB::table('invoices')
    ->whereTodayOrAfter('due_at')
    ->get();
```



**whereColumn / orWhereColumn**

`whereColumn` 메소드는 두 열이 같은지 확인하는 데 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('first_name', 'last_name')
    ->get();
```



`whereColumn` 메서드에 비교 연산자를 전달할 수도 있습니다:

```php
$users = DB::table('users')
    ->whereColumn('updated_at', '>', 'created_at')
    ->get();
```



또한 `whereColumn` 메서드에 열 비교 배열을 전달할 수 있습니다. 이러한 조건들은 `and` 연산자를 사용하여 결합됩니다:

```php
$users = DB::table('users')
    ->whereColumn([
        ['first_name', '=', 'last_name'],
        ['updated_at', '>', 'created_at'],
    ])->get();
```



<a name="logical-grouping"></a>
### 논리적 그룹화

때때로 원하는 쿼리의 논리적 그룹화를 달성하기 위해 여러 개의 "where" 절을 괄호로 묶어야 할 때가 있습니다. 실제로 예상치 못한 쿼리 동작을 피하기 위해 `orWhere` 메서드 호출을 항상 괄호로 묶는 것이 일반적으로 좋습니다. 이를 달성하기 위해 `where` 메서드에 클로저를 전달할 수 있습니다:

```php
$users = DB::table('users')
    ->where('name', '=', 'John')
    ->where(function (Builder $query) {
        $query->where('votes', '>', 100)
            ->orWhere('title', '=', 'Admin');
    })
    ->get();
```



보시다시피, 클로저를 `where` 메서드에 전달하면 쿼리 빌더에게 제약 조건 그룹을 시작하도록 지시합니다. 클로저는 쿼리 빌더 인스턴스를 받게 되며, 이를 사용하여 괄호 그룹 안에 포함되어야 할 제약 조건을 설정할 수 있습니다. 위의 예제는 다음과 같은 SQL을 생성합니다:

```sql
select * from users where name = 'John' and (votes > 100 or title = 'Admin')
```



> [!WARNING]
> 글로벌 스코프가 적용될 때 예상치 못한 동작을 피하기 위해 `orWhere` 호출을 항상 그룹화해야 합니다.

<a name="advanced-where-clauses"></a>
## 고급 Where 절

<a name="where-exists-clauses"></a>
### Where Exists 절

`whereExists` 메서드를 사용하면 "where exists" SQL 절을 작성할 수 있습니다. `whereExists` 메서드는 쿼리 빌더 인스턴스를 받는 클로저를 허용하여, "exists" 절 안에 들어갈 쿼리를 정의할 수 있습니다:

```php
$users = DB::table('users')
    ->whereExists(function (Builder $query) {
        $query->select(DB::raw(1))
            ->from('orders')
            ->whereColumn('orders.user_id', 'users.id');
    })
    ->get();
```



또는 클로저 대신 `whereExists` 메서드에 쿼리 객체를 제공할 수 있습니다:

```php
$orders = DB::table('orders')
    ->select(DB::raw(1))
    ->whereColumn('orders.user_id', 'users.id');

$users = DB::table('users')
    ->whereExists($orders)
    ->get();
```



위의 두 예제 모두 다음 SQL을 생성합니다:

```sql
select * from users
where exists (
    select 1
    from orders
    where orders.user_id = users.id
)
```



<a name="subquery-where-clauses"></a>
### 서브쿼리 Where 절

때때로 서브쿼리의 결과를 주어진 값과 비교하는 "where" 절을 구성해야 할 때가 있습니다. 이는 `where` 메서드에 클로저와 값을 전달함으로써 수행할 수 있습니다. 예를 들어, 다음 쿼리는 주어진 유형의 최근 "회원가입"을 가진 모든 사용자를 검색합니다;

```php
use App\Models\User;
use Illuminate\Database\Query\Builder;

$users = User::where(function (Builder $query) {
    $query->select('type')
        ->from('membership')
        ->whereColumn('membership.user_id', 'users.id')
        ->orderByDesc('membership.start_date')
        ->limit(1);
}, 'Pro')->get();
```



또는 열을 하위 쿼리의 결과와 비교하는 "where" 절을 구성해야 할 수도 있습니다. 이는 열, 연산자, 클로저를 `where` 메서드에 전달하여 수행할 수 있습니다. 예를 들어, 다음 쿼리는 금액이 평균보다 작은 모든 수입 기록을 검색합니다;

```php
use App\Models\Income;
use Illuminate\Database\Query\Builder;

$incomes = Income::where('amount', '<', function (Builder $query) {
    $query->selectRaw('avg(i.amount)')->from('incomes as i');
})->get();
```



<a name="full-text-where-clauses"></a>
### 전체 텍스트 WHERE 절

> [!WARNING]
> 전체 텍스트 WHERE 절은 현재 MariaDB, MySQL 및 PostgreSQL에서 지원됩니다.

`whereFullText` 및 `orWhereFullText` 메서드는 [전체 텍스트 인덱스](/docs/{{version}}/migrations#available-index-types)가 있는 열에 대한 쿼리에 전체 텍스트 "WHERE" 절을 추가하는 데 사용할 수 있습니다. 이러한 메서드는 Laravel에 의해 기본 데이터베이스 시스템에 적합한 SQL로 변환됩니다. 예를 들어, MariaDB 또는 MySQL을 사용하는 애플리케이션에서는 `MATCH AGAINST` 절이 생성됩니다:

```php
$users = DB::table('users')
    ->whereFullText('bio', 'web developer')
    ->get();
```



<a name="vector-similarity-clauses"></a>
### 벡터 유사도 조항

> [!NOTE]
> 벡터 유사도 조항은 현재 `pgvector` 확장을 사용하는 PostgreSQL 연결과 MariaDB 11.7 이상에서 지원됩니다. 벡터 열과 인덱스 정의에 대한 정보는 [마이그레이션 문서](/docs/{{version}}/migrations#available-column-types)를 참조하십시오.

`whereVectorSimilarTo` 방법은 주어진 벡터와의 코사인 유사도에 따라 결과를 필터링하고, 결과를 관련성에 따라 정렬합니다. `minSimilarity` 임계값은 `0.0`와 `1.0` 사이의 값이어야 하며, `1.0`는 동일합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)
    ->limit(10)
    ->get();
```



벡터 인수로 일반 문자열이 주어지면 Laravel은 [Laravel AI SDK](/docs/{{version}}/ai-sdk#embeddings)를 사용하여 자동으로 임베딩을 생성합니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', 'Best wineries in Napa Valley')
    ->limit(10)
    ->get();
```



기본적으로 `whereVectorSimilarTo`는 결과를 거리 순으로 정렬하기도 합니다(가장 유사한 것부터). `order` 인수로 `false`를 전달하면 이 정렬을 비활성화할 수 있습니다:

```php
$documents = DB::table('documents')
    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4, order: false)
    ->orderBy('created_at', 'desc')
    ->limit(10)
    ->get();
```



더 많은 제어가 필요하다면, `selectVectorDistance`, `whereVectorDistanceLessThan`, `orderByVectorDistance` 메서드를 독립적으로 사용할 수 있습니다:

```php
$documents = DB::table('documents')
    ->select('*')
    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')
    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)
    ->orderByVectorDistance('embedding', $queryEmbedding)
    ->limit(10)
    ->get();
```



PostgreSQL를 사용할 때 `vector` 열을 생성하기 전에 `pgvector` 확장을 로드해야 합니다:

```php
Schema::ensureVectorExtensionExists();
```



<a name="ordering-grouping-limit-and-offset"></a>
## 정렬, 그룹화, 제한 및 오프셋

<a name="ordering"></a>
### 정렬

<a name="orderby"></a>
#### `orderBy` 메서드

`orderBy` 메서드는 쿼리 결과를 지정된 열을 기준으로 정렬할 수 있게 합니다. `orderBy` 메서드가 받는 첫 번째 인자는 정렬하려는 열이어야 하며, 두 번째 인자는 정렬의 방향을 결정하며 `asc` 또는 `desc` 일 수 있습니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->get();
```



여러 열로 정렬하려면 필요한 만큼 `orderBy`를 여러 번 호출하면 됩니다:

```php
$users = DB::table('users')
    ->orderBy('name', 'desc')
    ->orderBy('email', 'asc')
    ->get();
```



정렬 방향은 선택 사항이며 기본값은 오름차순입니다. 내림차순으로 정렬하려면 `orderBy` 메서드의 두 번째 매개변수를 지정하거나 단순히 `orderByDesc`를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->orderByDesc('verified_at')
    ->get();
```



마지막으로, `->` 연산자를 사용하여 결과를 JSON 열 내의 값으로 정렬할 수 있습니다:

```php
$corporations = DB::table('corporations')
    ->where('country', 'US')
    ->orderBy('location->state')
    ->get();
```



<a name="latest-oldest"></a>
#### `latest` 및 `oldest` 방법

`latest` 및 `oldest` 방법을 사용하면 결과를 날짜별로 쉽게 정렬할 수 있습니다. 기본적으로 결과는 테이블의 `created_at` 열 기준으로 정렬됩니다. 또는 정렬하려는 열 이름을 전달할 수도 있습니다:

```php
$user = DB::table('users')
    ->latest()
    ->first();
```



<a name="random-ordering"></a>
#### 무작위 정렬

`inRandomOrder` 방법은 쿼리 결과를 무작위로 정렬하는 데 사용될 수 있습니다. 예를 들어, 이 방법을 사용하여 무작위 사용자 정보를 가져올 수 있습니다:

```php
$randomUser = DB::table('users')
    ->inRandomOrder()
    ->first();
```



<a name="removing-existing-orderings"></a>
#### 기존 정렬 제거

`reorder` 메서드는 이전에 쿼리에 적용된 모든 "order by" 절을 제거합니다:

```php
$query = DB::table('users')->orderBy('name');

$unorderedUsers = $query->reorder()->get();
```



`reorder` 메서드를 호출할 때 열과 방향을 전달하여 기존의 모든 'order by' 절을 제거하고 쿼리에 완전히 새로운 정렬을 적용할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorder('email', 'desc')->get();
```



편의를 위해, 쿼리 결과를 내림차순으로 재정렬하기 위해 `reorderDesc` 방법을 사용할 수 있습니다:

```php
$query = DB::table('users')->orderBy('name');

$usersOrderedByEmail = $query->reorderDesc('email')->get();
```



<a name="grouping"></a>
### 그룹화

<a name="groupby-having"></a>
#### `groupBy` 및 `having` 메서드

예상할 수 있듯이, `groupBy` 및 `having` 메서드는 쿼리 결과를 그룹화하는 데 사용할 수 있습니다. `having` 메서드의 시그니처는 `where` 메서드와 유사합니다:

```php
$users = DB::table('users')
    ->groupBy('account_id')
    ->having('account_id', '>', 100)
    ->get();
```



주어진 범위 내에서 결과를 필터링하기 위해 `havingBetween` 방법을 사용할 수 있습니다:

```php
$report = DB::table('orders')
    ->selectRaw('count(id) as number_of_orders, customer_id')
    ->groupBy('customer_id')
    ->havingBetween('number_of_orders', [5, 15])
    ->get();
```



여러 열을 기준으로 그룹화하기 위해 `groupBy` 메서드에 여러 인수를 전달할 수 있습니다:

```php
$users = DB::table('users')
    ->groupBy('first_name', 'status')
    ->having('account_id', '>', 100)
    ->get();
```



더 발전된 `having` 구문을 작성하려면 [havingRaw](#raw-methods) 메서드를 참조하세요.

<a name="limit-and-offset"></a>
### 제한 및 오프셋

쿼리에서 반환되는 결과 수를 제한하거나 쿼리에서 특정 수의 결과를 건너뛰려면 `limit` 및 `offset` 메서드를 사용할 수 있습니다:

```php
$users = DB::table('users')
    ->offset(10)
    ->limit(5)
    ->get();
```



<a name="conditional-clauses"></a>
## 조건절

때때로 특정 쿼리 절을 다른 조건에 따라 쿼리에 적용하고 싶을 때가 있습니다. 예를 들어, 들어오는 HTTP 요청에 특정 입력 값이 있는 경우에만 `where` 문을 적용하고 싶을 수 있습니다. 이는 `when` 방법을 사용하여 수행할 수 있습니다:

```php
$role = $request->input('role');

$users = DB::table('users')
    ->when($role, function (Builder $query, string $role) {
        $query->where('role_id', $role);
    })
    ->get();
```



`when` 메서드는 첫 번째 인수가 `true`일 때만 주어진 클로저를 실행합니다. 첫 번째 인수가 `false`인 경우 클로저는 실행되지 않습니다. 따라서 위의 예제에서 `when` 메서드에 주어진 클로저는 들어오는 요청에 `role` 필드가 존재하고 `true`로 평가될 때만 호출됩니다.

`when` 메서드의 세 번째 인수로 다른 클로저를 전달할 수 있습니다. 이 클로저는 첫 번째 인수가 `false`로 평가될 때만 실행됩니다. 이 기능이 어떻게 사용될 수 있는지를 보여주기 위해, 이를 사용하여 쿼리의 기본 정렬 순서를 구성하겠습니다:

```php
$sortByVotes = $request->boolean('sort_by_votes');

$users = DB::table('users')
    ->when($sortByVotes, function (Builder $query, bool $sortByVotes) {
        $query->orderBy('votes');
    }, function (Builder $query) {
        $query->orderBy('name');
    })
    ->get();
```



<a name="insert-statements"></a>
## 삽입 구문

쿼리 빌더는 데이터베이스 테이블에 레코드를 삽입하는 데 사용할 수 있는 `insert` 메서드도 제공합니다. `insert` 메서드는 열 이름과 값의 배열을 받습니다:

```php
DB::table('users')->insert([
    'email' => 'kayla@example.com',
    'votes' => 0
]);
```



여러 배열을 전달하여 한 번에 여러 레코드를 삽입할 수 있습니다. 각 배열은 테이블에 삽입되어야 할 레코드를 나타냅니다:

```php
DB::table('users')->insert([
    ['email' => 'picard@example.com', 'votes' => 0],
    ['email' => 'janeway@example.com', 'votes' => 0],
]);
```



`insertOrIgnore` 메서드는 데이터베이스에 레코드를 삽입하는 동안 오류를 무시합니다. 이 메서드를 사용할 때, 중복 레코드 오류가 무시되며 데이터베이스 엔진에 따라 다른 유형의 오류도 무시될 수 있다는 점을 인지해야 합니다. 예를 들어, `insertOrIgnore`는 [MySQL의 엄격 모드](https://dev.mysql.com/doc/refman/en/sql-mode.html#ignore-effect-on-execution)를 우회합니다:

```php
DB::table('users')->insertOrIgnore([
    ['id' => 1, 'email' => 'sisko@example.com'],
    ['id' => 2, 'email' => 'archer@example.com'],
]);
```



`insertUsing` 방법은 삽입해야 할 데이터를 결정하기 위해 하위 쿼리를 사용하면서 테이블에 새 레코드를 삽입합니다:

```php
DB::table('pruned_users')->insertUsing([
    'id', 'name', 'email', 'email_verified_at'
], DB::table('users')->select(
    'id', 'name', 'email', 'email_verified_at'
)->where('updated_at', '<=', now()->minus(months: 1)));
```



<a name="auto-incrementing-ids"></a>
#### 자동 증가 ID

테이블에 자동 증가 ID가 있는 경우, `insertGetId` 방법을 사용하여 레코드를 삽입한 다음 ID를 가져옵니다:

```php
$id = DB::table('users')->insertGetId(
    ['email' => 'john@example.com', 'votes' => 0]
);
```



> [!WARNING]
> PostgreSQL을 사용할 때 `insertGetId` 메서드는 자동 증가 열의 이름이 `id`라고 예상합니다. 다른 "시퀀스"에서 ID를 가져오고 싶다면 `insertGetId` 메서드의 두 번째 매개변수로 열 이름을 전달할 수 있습니다.

<a name="upserts"></a>
### 업서트

`upsert` 메서드는 존재하지 않는 레코드를 삽입하고 이미 존재하는 레코드를 지정한 새 값으로 업데이트합니다. 메서드의 첫 번째 인수는 삽입하거나 업데이트할 값으로 구성되며, 두 번째 인수는 관련 테이블 내에서 레코드를 고유하게 식별하는 열(들)을 나열합니다. 세 번째이자 마지막 인수는 데이터베이스에 이미 일치하는 레코드가 존재할 경우 업데이트해야 하는 열들의 배열입니다.

```php
DB::table('flights')->upsert(
    [
        ['departure' => 'Oakland', 'destination' => 'San Diego', 'price' => 99],
        ['departure' => 'Chicago', 'destination' => 'New York', 'price' => 150]
    ],
    ['departure', 'destination'],
    ['price']
);
```



위 예제에서 Laravel은 두 개의 레코드를 삽입하려고 시도합니다. 동일한 `departure` 및 `destination` 열 값을 가진 레코드가 이미 존재하면, Laravel은 해당 레코드의 `price` 열을 업데이트합니다.

> [!WARNING]
> SQL Server를 제외한 모든 데이터베이스는 `upsert` 메서드의 두 번째 인수에 있는 열이 "primary" 또는 "unique" 인덱스를 가져야 합니다. 또한 MariaDB 및 MySQL 데이터베이스 드라이버는 `upsert` 메서드의 두 번째 인수를 무시하고 항상 테이블의 "primary" 및 "unique" 인덱스를 사용하여 기존 레코드를 감지합니다.

<a name="update-statements"></a>
## 업데이트 문

데이터베이스에 레코드를 삽입하는 것 외에도, 쿼리 빌더는 `update` 메서드를 사용하여 기존 레코드를 업데이트할 수 있습니다. `update` 메서드는 `insert` 메서드처럼 업데이트할 열과 값 쌍의 배열을 받습니다. `update` 메서드는 영향을 받은 행의 수를 반환합니다. `update` 쿼리는 `where` 절을 사용하여 제한할 수 있습니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['votes' => 1]);
```



<a name="update-or-insert"></a>
#### 업데이트 또는 삽입

때때로 데이터베이스에서 기존 레코드를 업데이트하거나 일치하는 레코드가 없으면 새로 생성해야 할 때가 있습니다. 이 시나리오에서는 `updateOrInsert` 메서드를 사용할 수 있습니다. `updateOrInsert` 메서드는 두 개의 인수를 받습니다: 레코드를 찾기 위한 조건 배열과 업데이트할 열과 값의 쌍을 나타내는 배열입니다.

`updateOrInsert` 메서드는 첫 번째 인수의 열과 값 쌍을 사용하여 일치하는 데이터베이스 레코드를 찾으려고 시도합니다. 레코드가 존재하면 두 번째 인수의 값으로 업데이트됩니다. 레코드를 찾을 수 없으면 두 인수의 속성을 병합하여 새 레코드가 삽입됩니다:

```php
DB::table('users')
    ->updateOrInsert(
        ['email' => 'john@example.com', 'name' => 'John'],
        ['votes' => '2']
    );
```



일치하는 레코드의 존재 여부에 따라 데이터베이스에 업데이트되거나 삽입되는 속성을 사용자 정의하기 위해 `updateOrInsert` 메서드에 클로저를 제공할 수 있습니다:

```php
DB::table('users')->updateOrInsert(
    ['user_id' => $user_id],
    fn ($exists) => $exists ? [
        'name' => $data['name'],
        'email' => $data['email'],
    ] : [
        'name' => $data['name'],
        'email' => $data['email'],
        'marketable' => true,
    ],
);
```



<a name="updating-json-columns"></a>
### JSON 열 업데이트

JSON 열을 업데이트할 때는 JSON 객체의 해당 키를 업데이트하기 위해 `->` 구문을 사용해야 합니다. 이 작업은 MariaDB 10.3+, MySQL 5.7+, PostgreSQL 9.5+에서 지원됩니다:

```php
$affected = DB::table('users')
    ->where('id', 1)
    ->update(['options->enabled' => true]);
```



<a name="increment-and-decrement"></a>
### 증가 및 감소

쿼리 빌더는 또한 특정 열의 값을 증가시키거나 감소시키기 위한 편리한 메서드를 제공합니다. 이 두 메서드 모두 최소한 하나의 인수를 받습니다: 수정할 열. 두 번째 인수는 열이 증가되거나 감소될 양을 지정하기 위해 제공될 수 있습니다:

```php
DB::table('users')->increment('votes');

DB::table('users')->increment('votes', 5);

DB::table('users')->decrement('votes');

DB::table('users')->decrement('votes', 5);
```



필요한 경우 증가 또는 감소 작업 중에 업데이트할 추가 열을 지정할 수도 있습니다:

```php
DB::table('users')->increment('votes', 1, ['name' => 'John']);
```



또한 `incrementEach` 및 `decrementEach` 메서드를 사용하여 여러 열을 한 번에 증가시키거나 감소시킬 수 있습니다:

```php
DB::table('users')->incrementEach([
    'votes' => 5,
    'balance' => 100,
]);
```



<a name="delete-statements"></a>
## 삭제 문

쿼리 빌더의 `delete` 메서드는 테이블에서 레코드를 삭제하는 데 사용할 수 있습니다. `delete` 메서드는 영향을 받은 행의 수를 반환합니다. `delete` 문은 `delete` 메서드를 호출하기 전에 "where" 절을 추가하여 제한할 수 있습니다:

```php
$deleted = DB::table('users')->delete();

$deleted = DB::table('users')->where('votes', '>', 100)->delete();
```



<a name="pessimistic-locking"></a>
## 비관적 잠금

쿼리 빌더에는 `select` 문을 실행할 때 "비관적 잠금"을 달성하는 데 도움이 되는 몇 가지 함수도 포함되어 있습니다. "공유 잠금"으로 문을 실행하려면 `sharedLock` 메서드를 호출할 수 있습니다. 공유 잠금은 트랜잭션이 커밋될 때까지 선택한 행이 수정되는 것을 방지합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->sharedLock()
    ->get();
```



또는 `lockForUpdate` 방법을 사용할 수 있습니다. 'for update' 잠금은 선택된 레코드가 수정되거나 다른 공유 잠금으로 선택되는 것을 방지합니다:

```php
DB::table('users')
    ->where('votes', '>', 100)
    ->lockForUpdate()
    ->get();
```



의무 사항은 아니지만, 비관적 잠금은 [트랜잭션](/docs/{{version}}/database#database-transactions) 내에 감싸는 것이 권장됩니다. 이렇게 하면 전체 작업이 완료될 때까지 데이터베이스에서 가져온 데이터가 변경되지 않은 상태로 유지됩니다. 실패할 경우, 트랜잭션은 모든 변경 사항을 롤백하고 잠금을 자동으로 해제합니다:

```php
DB::transaction(function () {
    $sender = DB::table('users')
        ->lockForUpdate()
        ->find(1);

    $receiver = DB::table('users')
        ->lockForUpdate()
        ->find(2);

    if ($sender->balance < 100) {
        throw new RuntimeException('Balance too low.');
    }

    DB::table('users')
        ->where('id', $sender->id)
        ->update([
            'balance' => $sender->balance - 100
        ]);

    DB::table('users')
        ->where('id', $receiver->id)
        ->update([
            'balance' => $receiver->balance + 100
        ]);
});
```



<a name="reusable-query-components"></a>
## 재사용 가능한 쿼리 구성 요소

애플리케이션 전체에서 반복되는 쿼리 로직이 있는 경우, 쿼리 빌더의 `tap` 및 `pipe` 메서드를 사용하여 로직을 재사용 가능한 객체로 추출할 수 있습니다. 애플리케이션에 다음 두 가지 다른 쿼리가 있다고 가정해 보겠습니다:

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->orderByDesc('price')
    ->get();

// ...

$destination = $request->query('destination');

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) {
        $query->where('destination', $destination);
    })
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```



쿼리들 사이에 공통인 대상 필터링을 재사용 가능한 객체로 추출하고 싶을 수 있습니다:

```php
<?php

namespace App\Scopes;

use Illuminate\Database\Query\Builder;

class DestinationFilter
{
    public function __construct(
        private ?string $destination,
    ) {
        //
    }

    public function __invoke(Builder $query): void
    {
        $query->when($this->destination, function (Builder $query) {
            $query->where('destination', $this->destination);
        });
    }
}
```



그런 다음, 쿼리 빌더의 `tap` 메서드를 사용하여 객체의 로직을 쿼리에 적용할 수 있습니다:

```php
use App\Scopes\DestinationFilter;
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\DB;

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->orderByDesc('price')
    ->get();

// ...

DB::table('flights')
    ->when($destination, function (Builder $query, string $destination) { // [tl! remove]
        $query->where('destination', $destination); // [tl! remove]
    }) // [tl! remove]
    ->tap(new DestinationFilter($destination)) // [tl! add]
    ->where('user', $request->user()->id)
    ->orderBy('destination')
    ->get();
```



<a name="query-pipes"></a>
#### 쿼리 파이프

`tap` 메서드는 항상 쿼리 빌더를 반환합니다. 쿼리를 실행하고 다른 값을 반환하는 객체를 추출하고 싶다면 대신 `pipe` 메서드를 사용할 수 있습니다.

애플리케이션 전체에서 사용되는 공유 [페이지네이션](/docs/{{version}}/pagination) 로직을 포함하는 다음 쿼리 객체를 고려해 보세요. 쿼리 조건을 쿼리에 적용하는 `DestinationFilter`와 달리, `Paginate` 객체는 쿼리를 실행하고 페이지네이터 인스턴스를 반환합니다:

```php
<?php

namespace App\Scopes;

use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Database\Query\Builder;

class Paginate
{
    public function __construct(
        private string $sortBy = 'timestamp',
        private string $sortDirection = 'desc',
        private int $perPage = 25,
    ) {
        //
    }

    public function __invoke(Builder $query): LengthAwarePaginator
    {
        return $query->orderBy($this->sortBy, $this->sortDirection)
            ->paginate($this->perPage, pageName: 'p');
    }
}
```



쿼리 빌더의 `pipe` 메서드를 사용하여, 이 객체를 활용해 공통 페이징 로직을 적용할 수 있습니다:

```php
$flights = DB::table('flights')
    ->tap(new DestinationFilter($destination))
    ->pipe(new Paginate);
```



<a name="debugging"></a>
## 디버깅

쿼리를 구성하는 동안 `dd` 및 `dump` 메서드를 사용하여 현재 쿼리 바인딩 및 SQL을 덤프할 수 있습니다. `dd` 메서드는 디버그 정보를 표시한 후 요청 실행을 중지합니다. `dump` 메서드는 디버그 정보를 표시하지만 요청 실행을 계속 허용합니다:

```php
DB::table('users')->where('votes', '>', 100)->dd();

DB::table('users')->where('votes', '>', 100)->dump();
```



쿼리의 SQL과 모든 매개변수 바인딩이 올바르게 대체된 상태를 덤프하기 위해 쿼리에서 `dumpRawSql` 및 `ddRawSql` 메서드를 호출할 수 있습니다:

```php
DB::table('users')->where('votes', '>', 100)->dumpRawSql();

DB::table('users')->where('votes', '>', 100)->ddRawSql();
```
{% endraw %}
