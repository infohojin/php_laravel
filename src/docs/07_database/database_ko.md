---
layout: docs
title: "데이터베이스: 시작하기"
---

{% raw %}
# 데이터베이스: 시작하기

- [소개](#introduction)
- [컨피그레이션](#configuration)
- 읽기 및 쓰기 연결 (#read-and-write-connections)
- 풀드 PostgreSQL 연결 (#pooled-postgresql-connections)
- [SQL 쿼리 실행](#running-queries)
- 다중 데이터베이스 연결 사용 (#using-multiple-database-connections)
- 쿼리 이벤트 수신 (#listening-for-query-events)
- [누적 쿼리 시간 모니터링](#monitoring-cumulative-query-time)
- [데이터베이스 트랜잭션](#database-transactions)
- [데이터베이스 CLI 에 연결](#connecting-to-the-database-cli)
- 데이터베이스 검사 (#inspecting-your-databases)
- [데이터베이스 모니터링](#monitoring-your-databases)

<a name="introduction"></a>
## 소개

거의 모든 현대적인 웹 애플리케이션은 데이터베이스와 상호 작용합니다. Laravel 은 원시 SQL, 유동적 쿼리 빌더 (/docs/{{version}}/queries), 그리고 Eloquent ORM(/docs/{{version}}/eloquent) 을 사용하여 지원되는 다양한 데이터베이스에서 데이터베이스와의 상호 작용을 매우 간단하게 만듭니다. 현재 Laravel 은 5 개의 데이터베이스에 대한 제 1 자 지원을 제공합니다：

<div class="content-list" markdown="1">

- MariaDB 10.3+ ([Version Policy](https://mariadb.org/about/#maintenance-policy))
- MySQL 5.7+ ([버전 정책](https://en.wikipedia.org/wiki/MySQL#Release_history))
- PostgreSQL 10.0+ (Version Policy)(https://www.postgresql.org/support/versioning/))
- SQLite 3.26.0+
- SQL Server 2017+([Version Policy](https://docs.microsoft.com/en-us/lifecycle/products/?products=sql-server))

</div>

또한 MongoDB 는 공식적으로 MongoDB 에서 유지 관리하는 `mongodb/laravel-mongodb` 패키지를 통해 지원됩니다. 자세한 내용은 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 설명서를 참조하세요。

<a name="configuration"></a>
### 구성

Laravel 의 데이터베이스 서비스에 대한 구성은 애플리케이션의 `config/database.php` 구성 파일에 있습니다. 이 파일에서는 모든 데이터베이스 연결을 정의할 수 있을 뿐만 아니라 기본적으로 사용할 연결을 지정할 수도 있습니다. 이 파일의 대부분의 구성 옵션은 애플리케이션의 환경 변수 값에 의해 결정됩니다. Laravel 이 지원하는 대부분의 데이터베이스 시스템에 대한 예제가 이 파일에 제공됩니다。



기본적으로, Laravel의 샘플 [환경 구성](/docs/{{version}}/configuration#environment-configuration)은 [Laravel Sail](/docs/{{version}}/sail)과 함께 사용할 준비가 되어 있으며, 이는 로컬 컴퓨터에서 Laravel 애플리케이션을 개발하기 위한 Docker 구성입니다. 그러나 로컬 데이터베이스에 맞게 필요에 따라 데이터베이스 구성을 자유롭게 수정할 수 있습니다.

<a name="sqlite-configuration"></a>
#### SQLite 구성

SQLite 데이터베이스는 파일 시스템 내 단일 파일 안에 저장됩니다. 터미널에서 `touch` 명령을 사용하여 새 SQLite 데이터베이스를 생성할 수 있습니다: `touch database/database.sqlite`. 데이터베이스가 생성된 후, 데이터베이스의 절대 경로를 `DB_DATABASE` 환경 변수에 배치하여 환경 변수를 쉽게 구성할 수 있습니다.

```ini
DB_CONNECTION=sqlite
DB_DATABASE=/absolute/path/to/database.sqlite
```



기본적으로 SQLite 연결에는 외래 키 제약 조건이 활성화되어 있습니다. 이를 비활성화하려면 `DB_FOREIGN_KEYS` 환경 변수를 `false`로 설정해야 합니다:

```ini
DB_FOREIGN_KEYS=false
```



> [!NOTE]
[Laravel 설치 프로그램](/docs/{{version}}/installation#creating-a-laravel-project) 을 사용하여 Laravel 애플리케이션을 생성하고 SQLite 를 데이터베이스로 선택하면 Laravel 이 자동으로 `database/database.sqlite` 파일을 생성하고 기본 [데이터베이스 이동](/docs/{{version}}/migrations) 을 실행합니다。

<a name="mssql-configuration"></a>
#### Microsoft SQL Server 구성

Microsoft SQL Server 데이터베이스를 사용하려면 `sqlsrv` 및 `pdo_sqlsrv` PHP 확장 프로그램과 Microsoft SQL ODBC 드라이버와 같이 필요할 수 있는 모든 종속성이 설치되어 있는지 확인해야 합니다。

<a name="configuration-using-urls"></a>
#### URL 을 사용한 구성

일반적으로 데이터베이스 연결은 `host`, `database`, `username`, `password` 등과 같은 여러 구성 값을 사용하여 구성됩니다. 이러한 각 구성 값에는 해당하는 고유한 환경 변수가 있습니다. 즉， 프로덕션 서버에서 데이터베이스 연결 정보를 구성할 때 여러 환경 변수를 관리해야 합니다。

AWS 및 Heroku 와 같은 일부 관리형 데이터베이스 공급자는 데이터베이스에 대한 모든 연결 정보를 단일 문자열로 포함하는 단일 데이터베이스 “URL” 을 제공합니다. 데이터베이스 URL 의 예는 다음과 같을 수 있습니다：

```html
mysql://root:password@127.0.0.1/forge?charset=UTF-8
```



이 URL들은 일반적으로 표준 스키마 규칙을 따릅니다:

```html
driver://username:password@host:port/database?options
```



편의를 위해, Laravel은 여러 구성 옵션으로 데이터베이스를 설정하는 대신 이러한 URL을 지원합니다. `url`(또는 해당 `DB_URL` 환경 변수) 구성 옵션이 있을 경우, 데이터베이스 연결 및 인증 정보를 추출하는 데 사용됩니다.

<a name="read-and-write-connections"></a>
### 읽기 및 쓰기 연결

때때로 SELECT 문에는 하나의 데이터베이스 연결을 사용하고, INSERT, UPDATE, DELETE 문에는 다른 연결을 사용하고 싶을 수 있습니다. Laravel은 이를 매우 쉽게 처리하며, 로우 쿼리, 쿼리 빌더 또는 Eloquent ORM을 사용할 때 항상 적절한 연결이 사용됩니다.

읽기/쓰기 연결이 어떻게 구성되어야 하는지 보려면, 이 예제를 살펴봅시다:

```php
'mysql' => [
    'driver' => 'mysql',
    
    'read' => [
        'host' => [
            '192.168.1.1',
            '196.168.1.2',
        ],
    ],
    'write' => [
        'host' => [
            '192.168.1.3',
        ],
    ],
    'sticky' => true,
    
    'port' => env('DB_PORT', '3306'),
    'database' => env('DB_DATABASE', 'laravel'),
    'username' => env('DB_USERNAME', 'root'),
    'password' => env('DB_PASSWORD', ''),
    'unix_socket' => env('DB_SOCKET', ''),
    'charset' => env('DB_CHARSET', 'utf8mb4'),
    'collation' => env('DB_COLLATION', 'utf8mb4_unicode_ci'),
    'prefix' => '',
    'prefix_indexes' => true,
    'strict' => true,
    'engine' => null,
    'options' => extension_loaded('pdo_mysql') ? array_filter([
        (PHP_VERSION_ID >= 80500 ? \Pdo\Mysql::ATTR_SSL_CA : \PDO::MYSQL_ATTR_SSL_CA) => env('MYSQL_ATTR_SSL_CA'),
    ]) : [],
],
```



구성 배열에 `read`, `write` 및 `sticky` 라는 세 개의 키가 추가되었습니다. `read` 및 `write` 키에는 단일 키인 `host` 를 포함하는 배열 값이 있습니다. `read` 및 `write` 연결에 대한 나머지 데이터베이스 옵션은 주 `mysql` 구성 배열에서 병합됩니다。

주 `mysql` 배열의 값을 재정의하려는 경우에만 `read` 및 `write` 배열에 항목을 배치해야 합니다. 따라서 이 경우 `192.168.1.1` 는 “읽기” 연결에 호스트로 사용되고， `192.168.1.3` 는 “쓰기” 연결에 사용됩니다. 주 `mysql` 배열의 데이터베이스 자격 증명， 접두사， 문자 집합 및 기타 모든 옵션은 두 연결에서 공유됩니다. `host` 구성 배열에 여러 값이 존재하는 경우， 각 요청에 대해 데이터베이스 호스트가 무작위로 선택됩니다。

<a name="the-sticky-option"></a>
#### `sticky` 옵션

`sticky` 옵션은 현재 요청 주기 동안 데이터베이스에 기록된 레코드의 즉시 읽기를 허용하는 데 사용할 수 있는 *optional* 값입니다. `sticky` 옵션이 활성화되어 있고 현재 요청 주기 중에 데이터베이스에 대해 “쓰기” 작업이 수행된 경우， 추가적인 “읽기” 작업은 “쓰기” 연결을 사용합니다. 이렇게 하면 요청 주기 동안 기록된 모든 데이터를 동일한 요청 중에 데이터베이스에서 즉시 다시 읽을 수 있습니다. 이것이 애플리케이션에 대해 원하는 동작인지 여부는 사용자가 결정합니다。

<a name="pooled-postgresql-connections"></a>
### 풀링된 PostgreSQL 연결

많은 관리형 PostgreSQL 공급자는 PgBouncer 또는 연결 프록시와 같은 서비스를 통해 트랜잭션 모드 연결 풀링을 제공합니다. 이러한 풀러는 애플리케이션 쿼리에 이상적이지만， 일부 스키마 작업， 마이그레이션 및 유지 관리 명령에는 직접적인 데이터베이스 연결이 필요합니다。

PostgreSQL 에서 트랜잭션 풀러를 사용하려면 일반적으로 풀링된 연결을 구성하고 `direct` 구성 옵션을 통해 직접 연결 세부 정보를 제공합니다。

```php
'pgsql' => [
    'driver' => 'pgsql',
    // ...
    'pooled' => env('DB_POOLED', false),
    'direct' => array_filter([
        'host' => env('DB_DIRECT_HOST'),
        'port' => env('DB_DIRECT_PORT'),
        'username' => env('DB_DIRECT_USERNAME'),
        'password' => env('DB_DIRECT_PASSWORD'),
        'sslmode' => env('DB_DIRECT_SSLMODE'),
    ]),
],
```



PostgreSQL 연결이 풀링된 상태로 구성되면, Laravel은 풀링된 연결에 대해 자동으로 에뮬레이션된 준비(emulated prepares)를 활성화합니다. 직접 연결(direct connection)은 `direct` 구성에서 명시적으로 정의되지 않은 모든 옵션을 상속하며, 기본적으로 네이티브 준비(native prepares)를 사용합니다.

Laravel은 마이그레이션(migrations), 스키마 덤프(schema dumps) 및 복원(restores), `db:wipe`, `db:show`, `db:table`에 대해 자동으로 직접 연결을 사용합니다. 풀링 모드가 활성화되어 있고 직접 연결이 구성된 경우, `db` 명령도 기본적으로 직접 연결을 사용합니다. 대신 풀링된 연결에 연결하기 위해 `--pooled` 옵션을 전달할 수 있습니다:

```shell
php artisan db --pooled
```



애플리케이션에서 직접 연결을 명시적으로 사용해야 하는 경우, 연결 이름에 `::direct` 접미사를 추가하세요:

```php
DB::connection('pgsql::direct')->statement('create extension if not exists "uuid-ossp"');
```



<a name="running-queries"></a>
## SQL 쿼리 실행

데이터베이스 연결을 설정한 후에는 `DB` 퍼사드를 사용하여 쿼리를 실행할 수 있습니다. `DB` 퍼사드는 각 쿼리 유형에 대한 메서드를 제공합니다: `select`, `update`, `insert`, `delete`, `statement`.

<a name="running-a-select-query"></a>
#### Select 쿼리 실행

기본 SELECT 쿼리를 실행하려면 `DB` 퍼사드에서 `select` 메서드를 사용할 수 있습니다:

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
        $users = DB::select('select * from users where active = ?', [1]);

        return view('user.index', ['users' => $users]);
    }
}
```



`select` 메서드에 전달되는 첫 번째 인수는 SQL 쿼리이고, 두 번째 인수는 쿼리에 바인딩해야 하는 파라미터 바인딩입니다. 일반적으로 이것들은 `where` 절 제약의 값들입니다. 파라미터 바인딩은 SQL 인젝션으로부터 보호를 제공합니다.

`select` 메서드는 항상 `array` 결과를 반환합니다. 배열 내의 각 결과는 데이터베이스의 레코드를 나타내는 PHP `stdClass` 객체가 됩니다:

```php
use Illuminate\Support\Facades\DB;

$users = DB::select('select * from users');

foreach ($users as $user) {
    echo $user->name;
}
```



<a name="selecting-scalar-values"></a>
#### 스칼라 값 선택하기

때때로 데이터베이스 쿼리 결과가 단일 스칼라 값이 될 수 있습니다. 쿼리의 스칼라 결과를 레코드 객체에서 가져와야 하는 대신, Laravel에서는 이 값을 `scalar` 메서드를 사용하여 직접 가져올 수 있습니다:

```php
$burgers = DB::scalar(
    "select count(case when food = 'burger' then 1 end) as burgers from menu"
);
```



<a name="selecting-multiple-result-sets"></a>
#### 여러 결과 집합 선택

응용 프로그램이 여러 결과 집합을 반환하는 저장 프로시저를 호출하는 경우, `selectResultSets` 방법을 사용하여 저장 프로시저가 반환하는 모든 결과 집합을 가져올 수 있습니다:

```php
[$options, $notifications] = DB::selectResultSets(
    "CALL get_user_options_and_notifications(?)", $request->user()->id
);
```



<a name="using-named-bindings"></a>
#### 명명된 바인딩 사용

매개변수 바인딩을 나타내기 위해 `?`를 사용하는 대신, 명명된 바인딩을 사용하여 쿼리를 실행할 수 있습니다:

```php
$results = DB::select('select * from users where id = :id', ['id' => 1]);
```



<a name="running-an-insert-statement"></a>
#### INSERT 문 실행하기

`insert` 문을 실행하려면 `DB` 퍼사드에서 `insert` 메서드를 사용할 수 있습니다. `select`와 마찬가지로, 이 메서드는 SQL 쿼리를 첫 번째 인수로, 바인딩을 두 번째 인수로 받습니다:

```php
use Illuminate\Support\Facades\DB;

DB::insert('insert into users (id, name) values (?, ?)', [1, 'Marc']);
```



<a name="running-an-update-statement"></a>
#### 업데이트 문 실행

`update` 메서드는 데이터베이스의 기존 레코드를 업데이트하는 데 사용되어야 합니다. 문에 의해 영향을 받은 행의 수는 메서드에 의해 반환됩니다:

```php
use Illuminate\Support\Facades\DB;

$affected = DB::update(
    'update users set votes = 100 where name = ?',
    ['Anita']
);
```



<a name="running-a-delete-statement"></a>
#### 삭제 문 실행

`delete` 메서드는 데이터베이스에서 레코드를 삭제하는 데 사용해야 합니다. `update`와 마찬가지로, 영향을 받은 행의 수가 메서드에 의해 반환됩니다:

```php
use Illuminate\Support\Facades\DB;

$deleted = DB::delete('delete from users');
```



<a name="running-a-general-statement"></a>
#### 일반 구문 실행

일부 데이터베이스 구문은 값을 반환하지 않습니다. 이러한 유형의 작업에는 `DB` 파사드에서 `statement` 메서드를 사용할 수 있습니다:

```php
DB::statement('drop table users');
```



<a name="running-an-unprepared-statement"></a>
#### 준비되지 않은 문장 실행

때때로 값들을 바인딩하지 않고 SQL 문을 실행하고 싶을 때가 있습니다. 이를 수행하기 위해 `DB` 퍼사드의 `unprepared` 메서드를 사용할 수 있습니다:

```php
DB::unprepared('update users set votes = 100 where name = "Dries"');
```



> [!WARNING]
> 준비되지 않은 쿼리는 파라미터를 바인딩하지 않기 때문에 SQL 인젝션에 취약할 수 있습니다. 사용자가 제어하는 값을 준비되지 않은 쿼리 안에 절대 포함시키지 않아야 합니다.

<a name="implicit-commits-in-transactions"></a>
#### 암묵적 커밋

트랜잭션 내에서 `DB` 퍼사드의 `statement` 및 `unprepared` 메서드를 사용할 때는 [암묵적 커밋](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)을 일으키는 쿼리를 피하도록 주의해야 합니다. 이러한 쿼리는 데이터베이스 엔진이 전체 트랜잭션을 간접적으로 커밋하게 하여 Laravel이 데이터베이스의 트랜잭션 상태를 인식하지 못하게 합니다. 이러한 쿼리의 예로는 데이터베이스 테이블을 생성하는 것이 있습니다:

```php
DB::unprepared('create table a (col varchar(1) null)');
```



암시적 커밋을 트리거하는 모든 문장 목록은 MySQL 매뉴얼을 참조하십시오([여기](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)).

<a name="using-multiple-database-connections"></a>
### 다중 데이터베이스 연결 사용하기

애플리케이션에서 `config/database.php` 구성 파일에 여러 연결을 정의한 경우, `DB` 퍼사드에서 제공하는 `connection` 메서드를 통해 각 연결에 접근할 수 있습니다. `connection` 메서드에 전달되는 연결 이름은 `config/database.php` 구성 파일에 나열된 연결 중 하나와 일치해야 하며, `config` 헬퍼를 사용하여 런타임에 구성할 수도 있습니다.

```php
use Illuminate\Support\Facades\DB;

$users = DB::connection('sqlite')->select(/* ... */);
```



연결 인스턴스에서 `getPdo` 메서드를 사용하여 연결의 원시 기본 PDO 인스턴스에 접근할 수 있습니다:

```php
$pdo = DB::connection()->getPdo();
```



<a name="listening-for-query-events"></a>
### 쿼리 이벤트 수신

애플리케이션에서 실행된 각 SQL 쿼리에 대해 호출되는 클로저를 지정하려면 `DB` 파사드의 `listen` 메서드를 사용할 수 있습니다. 이 메서드는 쿼리를 로깅하거나 디버깅하는 데 유용할 수 있습니다. 쿼리 리스너 클로저는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 등록할 수 있습니다:

```php
<?php

namespace App\Providers;

use Illuminate\Database\Events\QueryExecuted;
use Illuminate\Support\Facades\DB;
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
        DB::listen(function (QueryExecuted $query) {
            // $query->sql;
            // $query->bindings;
            // $query->time;
            // $query->toRawSql();
        });
    }
}
```



<a name="monitoring-cumulative-query-time"></a>
### 누적 쿼리 시간 모니터링

현대 웹 애플리케이션의 일반적인 성능 병목 현상 중 하나는 데이터베이스 쿼리에 소비되는 시간입니다. 다행히, Laravel은 단일 요청 동안 데이터베이스 쿼리에 너무 많은 시간을 소비할 경우 선택한 클로저나 콜백을 호출할 수 있습니다. 시작하려면, 쿼리 시간 임계값(밀리초 단위)과 클로저를 `whenQueryingForLongerThan` 메서드에 제공하십시오. 이 메서드는 [서비스 프로바이더](/docs/{{version}}/providers)의 `boot` 메서드에서 호출할 수 있습니다.

```php
<?php

namespace App\Providers;

use Illuminate\Database\Connection;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\ServiceProvider;
use Illuminate\Database\Events\QueryExecuted;

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
        DB::whenQueryingForLongerThan(500, function (Connection $connection, QueryExecuted $event) {
            // Notify development team...
        });
    }
}
```



<a name="database-transactions"></a>
## 데이터베이스 트랜잭션

데이터베이스 트랜잭션 내에서 일련의 작업을 실행하기 위해 `DB` 퍼사드에서 제공하는 `transaction` 메서드를 사용할 수 있습니다. 트랜잭션 클로저 내에서 예외가 발생하면 트랜잭션은 자동으로 롤백되며 예외가 다시 던져집니다. 클로저가 성공적으로 실행되면 트랜잭션은 자동으로 커밋됩니다. `transaction` 메서드를 사용할 때 수동으로 롤백하거나 커밋하는 것에 대해 걱정할 필요가 없습니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
});
```



<a name="handling-deadlocks"></a>
#### 교착 상태 처리

`transaction` 메서드는 교착 상태가 발생했을 때 트랜잭션을 재시도할 횟수를 정의하는 선택적 두 번째 인수를 허용합니다. 이러한 시도가 모두 소진되면 예외가 발생합니다:

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    DB::update('update users set votes = 1');

    DB::delete('delete from posts');
}, attempts: 5);
```



<a name="manually-using-transactions"></a>
#### 트랜잭션 수동 사용

트랜잭션을 수동으로 시작하고 롤백과 커밋을 완전히 제어하고 싶다면, `DB` 퍼사드가 제공하는 `beginTransaction` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();
```



`rollBack` 방법을 통해 거래를 롤백할 수 있습니다:

```php
DB::rollBack();
```



마지막으로, `commit` 메서드를 통해 거래를 커밋할 수 있습니다:

```php
DB::commit();
```



> [!NOTE]
> `DB` 페이사드의 트랜잭션 메서드는 [쿼리 빌더](/docs/{{version}}/queries)와 [Eloquent ORM](/docs/{{version}}/eloquent) 모두의 트랜잭션을 제어합니다.

<a name="connecting-to-the-database-cli"></a>
## 데이터베이스 CLI에 연결하기

데이터베이스의 CLI에 연결하려면 `db` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan db
```



필요한 경우, 기본 연결이 아닌 데이터베이스에 연결하기 위해 데이터베이스 연결 이름을 지정할 수 있습니다:

```shell
php artisan db mysql
```



<a name="inspecting-your-databases"></a>
## 데이터베이스 검사하기

`db:show` 및 `db:table` Artisan 명령어를 사용하면 데이터베이스와 관련된 테이블에 대한 유용한 정보를 얻을 수 있습니다. 데이터베이스의 크기, 유형, 열린 연결 수 및 테이블 요약을 포함한 개요를 보려면 `db:show` 명령어를 사용할 수 있습니다:

```shell
php artisan db:show
```



`--database` 옵션을 통해 데이터베이스 연결 이름을 명령에 제공하면 검사할 데이터베이스 연결을 지정할 수 있습니다:

```shell
php artisan db:show --database=pgsql
```



명령어의 출력에 테이블 행 수와 데이터베이스 뷰 세부 정보를 포함하고 싶다면 각각 `--counts`와 `--views` 옵션을 제공할 수 있습니다. 대형 데이터베이스에서는 행 수와 뷰 세부 정보를 가져오는 것이 느릴 수 있습니다:

```shell
php artisan db:show --counts --views
```



또한, 데이터베이스를 검사하기 위해 다음 `Schema` 방법들을 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Schema;

$tables = Schema::getTables();
$views = Schema::getViews();
$columns = Schema::getColumns('users');
$indexes = Schema::getIndexes('users');
$foreignKeys = Schema::getForeignKeys('users');
```



애플리케이션의 기본 연결이 아닌 데이터베이스 연결을 검사하고 싶다면, `connection` 메서드를 사용할 수 있습니다:

```php
$columns = Schema::connection('sqlite')->getColumns('users');
```



<a name="table-overview"></a>
#### 테이블 개요

데이터베이스 내 개별 테이블의 개요를 확인하고 싶다면, `db:table` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 데이터베이스 테이블의 열, 타입, 속성, 키 및 인덱스를 포함한 일반적인 개요를 제공합니다:

```shell
php artisan db:table users
```



<a name="monitoring-your-databases"></a>
## 데이터베이스 모니터링

`db:monitor` Artisan 명령어를 사용하면, 지정된 수 이상의 열린 연결을 관리하는 경우 Laravel이 `Illuminate\Database\Events\DatabaseBusy` 이벤트를 디스패치하도록 지시할 수 있습니다.

시작하려면, `db:monitor` 명령어를 [매분 실행](/docs/{{version}}/scheduling)하도록 예약해야 합니다. 명령어는 이벤트를 디스패치하기 전에 허용할 수 있는 최대 열린 연결 수뿐만 아니라 모니터링하려는 데이터베이스 연결 구성의 이름을 받습니다:

```shell
php artisan db:monitor --databases=mysql,pgsql --max=100
```



이 명령만 스케줄링하는 것으로는 열려 있는 연결 수를 알리는 알림을 트리거하기에 충분하지 않습니다. 명령이 열려 있는 연결 수가 임계값을 초과하는 데이터베이스를 만나면 `DatabaseBusy` 이벤트가 발행됩니다. 이 이벤트를 애플리케이션의 `AppServiceProvider` 내에서 수신하도록 하여 본인 또는 개발 팀에게 알림을 보낼 수 있어야 합니다:

```php
use App\Notifications\DatabaseApproachingMaxConnections;
use Illuminate\Database\Events\DatabaseBusy;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Notification;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Event::listen(function (DatabaseBusy $event) {
        Notification::route('mail', 'dev@example.com')
            ->notify(new DatabaseApproachingMaxConnections(
                $event->connectionName,
                $event->connections
            ));
    });
}
```
{% endraw %}
