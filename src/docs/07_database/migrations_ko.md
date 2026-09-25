---
layout: docs
title: "Database: Migrations"
---

{% raw %}
---
layout: docs
title: "Database: Migrations"
---

# Database: Migrations

- [Introduction](#introduction)
- [Generating Migrations](#generating-migrations)
    - [Squashing Migrations](#squashing-migrations)
- [Migration Structure](#migration-structure)
- [Running Migrations](#running-migrations)
    - [Rolling Back Migrations](#rolling-back-migrations)
- [Tables](#tables)
    - [Creating Tables](#creating-tables)
    - [Updating Tables](#updating-tables)
    - [Renaming / Dropping Tables](#renaming-and-dropping-tables)
- [Columns](#columns)
    - [Creating Columns](#creating-columns)
    - [Available Column Types](#available-column-types)
    - [Column Modifiers](#column-modifiers)
    - [Modifying Columns](#modifying-columns)
    - [Renaming Columns](#renaming-columns)
    - [Dropping Columns](#dropping-columns)
- [Indexes](#indexes)
    - [Creating Indexes](#creating-indexes)
    - [Renaming Indexes](#renaming-indexes)
    - [Dropping Indexes](#dropping-indexes)
    - [Foreign Key Constraints](#foreign-key-constraints)
- [Events](#events)

<a name="introduction"></a>
## Introduction

Migrations are like version control for your database, allowing your team to define and share the application's database schema definition. If you have ever had to tell a teammate to manually add a column to their local database schema after pulling in your changes from source control, you've faced the problem that database migrations solve.

The Laravel `Schema` [facade](/docs/{{version}}/facades) provides database agnostic support for creating and manipulating tables across all of Laravel's supported database systems. Typically, migrations will use this facade to create and modify database tables and columns.

<a name="generating-migrations"></a>
## Generating Migrations

You may use the `make:migration` [Artisan command](/docs/{{version}}/artisan) to generate a database migration. The new migration will be placed in your `database/migrations` directory. Each migration filename contains a timestamp that allows Laravel to determine the order of the migrations:

```shell
php artisan make:migration create_flights_table
```



Laravel will use the name of the migration to attempt to guess the name of the table and whether or not the migration will be creating a new table. If Laravel is able to determine the table name from the migration name, Laravel will pre-fill the generated migration file with the specified table. Otherwise, you may simply specify the table in the migration file manually.

If you would like to specify a custom path for the generated migration, you may use the `--path` option when executing the `make:migration` command. The given path should be relative to your application's base path.

> [!NOTE]
> Migration stubs may be customized using [stub publishing](/docs/{{version}}/artisan#stub-customization).

<a name="squashing-migrations"></a>
### Squashing Migrations

As you build your application, you may accumulate more and more migrations over time. This can lead to your `database/migrations` directory becoming bloated with potentially hundreds of migrations. If you would like, you may "squash" your migrations into a single SQL file. To get started, execute the `schema:dump` command:

```shell
php artisan schema:dump

# Dump the current database schema and prune all existing migrations...
php artisan schema:dump --prune
```



이 명령을 실행하면 Laravel은 애플리케이션의 `database/schema` 디렉토리에 "스키마" 파일을 작성합니다. 스키마 파일의 이름은 데이터베이스 연결에 해당합니다. 이제 데이터베이스를 마이그레이션하려고 시도했는데 다른 마이그레이션이 실행되지 않았다면, Laravel은 먼저 사용 중인 데이터베이스 연결의 스키마 파일에 있는 SQL 문을 실행합니다. 스키마 파일의 SQL 문을 실행한 후, Laravel은 스키마 덤프에 포함되지 않은 나머지 마이그레이션을 실행합니다.

애플리케이션의 테스트가 일반적으로 로컬 개발 중 사용하는 것과 다른 데이터베이스 연결을 사용하는 경우, 테스트가 데이터베이스를 구성할 수 있도록 해당 데이터베이스 연결을 사용하여 스키마 파일을 덤프했는지 확인해야 합니다. 일반적으로 로컬 개발 중 사용하는 데이터베이스 연결을 덤프한 후에 이를 수행할 수도 있습니다:

```shell
php artisan schema:dump
php artisan schema:dump --database=testing --prune
```



귀하는 팀의 다른 신규 개발자가 애플리케이션의 초기 데이터베이스 구조를 빠르게 생성할 수 있도록 데이터베이스 스키마 파일을 소스 관리에 커밋해야 합니다.

> [!WARNING]
> 마이그레이션 스쿼싱은 MariaDB, MySQL, PostgreSQL 및 SQLite 데이터베이스에서만 사용 가능하며 데이터베이스의 명령줄 클라이언트를 이용합니다.

<a name="migration-structure"></a>
## 마이그레이션 구조

마이그레이션 클래스는 두 개의 메서드를 포함합니다: `up` 및 `down`. `up` 메서드는 데이터베이스에 새로운 테이블, 컬럼 또는 인덱스를 추가하는 데 사용되며, `down` 메서드는 `up` 메서드에서 수행된 작업을 되돌려야 합니다.

이 두 메서드 내에서 Laravel 스키마 빌더를 사용하여 테이블을 표현적으로 생성하고 수정할 수 있습니다. `Schema` 빌더에서 사용할 수 있는 모든 메서드에 대해 알아보려면 [문서](#creating-tables)를 참조하세요. 예를 들어, 다음 마이그레이션은 `flights` 테이블을 생성합니다:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('airline');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::drop('flights');
    }
};
```



<a name="setting-the-migration-connection"></a>
#### 마이그레이션 연결 설정

마이그레이션이 애플리케이션의 기본 데이터베이스 연결이 아닌 다른 데이터베이스 연결과 상호 작용할 경우, 마이그레이션의 `$connection` 속성을 설정해야 합니다:

```php
/**
 * The database connection that should be used by the migration.
 *
 * @var string
 */
protected $connection = 'pgsql';

/**
 * Run the migrations.
 */
public function up(): void
{
    // ...
}
```



<a name="skipping-migrations"></a>
#### 마이그레이션 건너뛰기

때때로 마이그레이션은 아직 활성화되지 않은 기능을 지원하기 위해 만들어질 수 있으며, 이 경우 마이그레이션을 아직 실행하고 싶지 않을 수 있습니다. 이 경우 마이그레이션에 `shouldRun` 메서드를 정의할 수 있습니다. `shouldRun` 메서드가 `false`를 반환하면, 마이그레이션은 건너뛰게 됩니다:

```php
use App\Models\Flight;
use Laravel\Pennant\Feature;

/**
 * Determine if this migration should run.
 */
public function shouldRun(): bool
{
    return Feature::active(Flight::class);
}
```



<a name="running-migrations"></a>
## 마이그레이션 실행

모든 대기 중인 마이그레이션을 실행하려면, `migrate` Artisan 명령을 실행하세요:

```shell
php artisan migrate
```



이미 실행된 마이그레이션과 아직 대기 중인 마이그레이션을 확인하고 싶다면 `migrate:status` Artisan 명령어를 사용할 수 있습니다:

```shell
php artisan migrate:status
```



`migrate` 명령어에 `--step` 옵션을 제공하면, 명령어는 각 마이그레이션을 자체 배치로 실행하므로 나중에 `migrate:rollback` 명령어를 사용하여 개별 마이그레이션을 롤백할 수 있습니다:

```shell
php artisan migrate --step
```



마이그레이션으로 실행될 SQL 문을 실제로 실행하지 않고 보고 싶다면, `migrate` 명령에 `--pretend` 플래그를 제공할 수 있습니다:

```shell
php artisan migrate --pretend
```



<a name="isolating-migration-execution"></a>
#### 마이그레이션 실행 격리

여러 서버에 애플리케이션을 배포하고 배포 과정의 일부로 마이그레이션을 실행하는 경우, 두 서버가 동시에 데이터베이스를 마이그레이션 하려고 하지 않도록 하는 것이 좋습니다. 이를 방지하기 위해, `migrate` 명령을 호출할 때 `isolated` 옵션을 사용할 수 있습니다.

`isolated` 옵션이 제공되면, Laravel은 마이그레이션을 실행하기 전에 애플리케이션의 캐시 드라이버를 사용하여 원자적 잠금을 획득합니다. 이 잠금이 유지되는 동안 다른 모든 `migrate` 명령 실행 시도는 실행되지 않지만, 명령은 여전히 성공적인 종료 상태 코드로 종료됩니다:

```shell
php artisan migrate --isolated
```



> [!WARNING]
> 이 기능을 사용하려면, 애플리케이션이 `memcached`, `redis`, `dynamodb`, `database`, `file` 또는 `array` 캐시 드라이버 중 하나를 기본 캐시 드라이버로 사용하고 있어야 합니다. 또한, 모든 서버는 동일한 중앙 캐시 서버와 통신하고 있어야 합니다.

<a name="forcing-migrations-to-run-in-production"></a>
#### 운영 환경에서 마이그레이션 실행 강제하기

일부 마이그레이션 작업은 파괴적일 수 있으며, 이는 데이터 손실을 초래할 수 있음을 의미합니다. 이러한 명령을 운영 데이터베이스에 실행하는 것을 방지하기 위해, 명령 실행 전에 확인을 요청받게 됩니다. 프롬프트 없이 명령을 강제로 실행하려면, `--force` 플래그를 사용하십시오:

```shell
php artisan migrate --force
```



<a name="rolling-back-migrations"></a>
### 마이그레이션 되돌리기

최신 마이그레이션 작업을 되돌리려면 `rollback` Artisan 명령을 사용할 수 있습니다. 이 명령은 마지막 "배치"의 마이그레이션을 되돌리며, 여기에는 여러 마이그레이션 파일이 포함될 수 있습니다:

```shell
php artisan migrate:rollback
```



`rollback` 명령에 `step` 옵션을 제공하여 제한된 수의 마이그레이션을 롤백할 수 있습니다. 예를 들어, 다음 명령은 마지막 다섯 개의 마이그레이션을 롤백합니다:

```shell
php artisan migrate:rollback --step=5
```



특정 "배치"의 마이그레이션은 `rollback` 명령에 `batch` 옵션을 제공하여 되돌릴 수 있으며, 여기서 `batch` 옵션은 애플리케이션의 `migrations` 데이터베이스 테이블 내의 배치 값에 해당합니다. 예를 들어, 다음 명령은 세 번째 배치의 모든 마이그레이션을 되돌립니다:

```shell
php artisan migrate:rollback --batch=3
```



마이그레이션이 실제로 실행되지 않고 수행될 SQL 문을 보고 싶다면, `migrate:rollback` 명령에 `--pretend` 플래그를 제공할 수 있습니다:

```shell
php artisan migrate:rollback --pretend
```



`migrate:reset` 명령은 애플리케이션의 모든 마이그레이션을 롤백합니다:

```shell
php artisan migrate:reset
```



<a name="roll-back-migrate-using-a-single-command"></a>
#### 하나의 명령으로 롤백하고 마이그레이션하기

`migrate:refresh` 명령은 모든 마이그레이션을 롤백한 후 `migrate` 명령을 실행합니다. 이 명령은 전체 데이터베이스를 효과적으로 재생성합니다:

```shell
php artisan migrate:refresh

# Refresh the database and run all database seeds...
php artisan migrate:refresh --seed
```



`refresh` 명령에 `step` 옵션을 제공하여 제한된 수의 마이그레이션을 롤백하고 다시 마이그레이션할 수 있습니다. 예를 들어, 다음 명령은 마지막 다섯 개의 마이그레이션을 롤백하고 다시 마이그레이션합니다:

```shell
php artisan migrate:refresh --step=5
```



<a name="drop-all-tables-migrate"></a>
#### 모든 테이블 삭제 및 마이그레이션

`migrate:fresh` 명령은 데이터베이스의 모든 테이블을 삭제한 후 `migrate` 명령을 실행합니다:

```shell
php artisan migrate:fresh

php artisan migrate:fresh --seed
```



기본적으로 `migrate:fresh` 명령은 기본 데이터베이스 연결에서만 테이블을 삭제합니다. 그러나 `--database` 옵션을 사용하여 마이그레이션할 데이터베이스 연결을 지정할 수 있습니다. 데이터베이스 연결 이름은 애플리케이션의 `database` [설정 파일](/docs/{{version}}/configuration)에 정의된 연결과 일치해야 합니다.

```shell
php artisan migrate:fresh --database=admin
```



> [!WARNING]
> `migrate:fresh` 명령어는 접두사와 상관없이 모든 데이터베이스 테이블을 삭제합니다. 이 명령어는 다른 애플리케이션과 공유되는 데이터베이스에서 개발할 때 주의해서 사용해야 합니다.

<a name="tables"></a>
## 테이블

<a name="creating-tables"></a>
### 테이블 생성

새 데이터베이스 테이블을 생성하려면 `Schema` 파사드에서 `create` 메서드를 사용합니다. `create` 메서드는 두 개의 인수를 받습니다: 첫 번째는 테이블 이름이고, 두 번째는 새 테이블을 정의하는 데 사용할 수 있는 `Blueprint` 객체를 받는 클로저입니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email');
    $table->timestamps();
});
```



테이블을 생성할 때, 스키마 빌더의 [컬럼 메서드](#creating-columns)를 사용하여 테이블의 컬럼을 정의할 수 있습니다.

<a name="determining-table-column-existence"></a>
#### 테이블 / 컬럼 존재 여부 확인

`hasTable`, `hasColumn`, `hasIndex` 메서드를 사용하여 테이블, 컬럼 또는 인덱스의 존재 여부를 확인할 수 있습니다:

```php
if (Schema::hasTable('users')) {
    // The "users" table exists...
}

if (Schema::hasColumn('users', 'email')) {
    // The "users" table exists and has an "email" column...
}

if (Schema::hasIndex('users', ['email'], 'unique')) {
    // The "users" table exists and has a unique index on the "email" column...
}
```



<a name="database-connection-table-options"></a>
#### 데이터베이스 연결 및 테이블 옵션

응용 프로그램의 기본 연결이 아닌 데이터베이스 연결에서 스키마 작업을 수행하려면 `connection` 메서드를 사용하세요:

```php
Schema::connection('sqlite')->create('users', function (Blueprint $table) {
    $table->id();
});
```



또한, 테이블 생성의 다른 측면을 정의하기 위해 몇 가지 다른 속성과 메서드를 사용할 수 있습니다. `engine` 속성은 MariaDB 또는 MySQL을 사용할 때 테이블의 저장 엔진을 지정하는 데 사용할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->engine('InnoDB');

    // ...
});
```



MariaDB 또는 MySQL을 사용할 때 생성된 테이블에 대한 문자 집합과 정렬 규칙을 지정하기 위해 `charset` 및 `collation` 속성을 사용할 수 있습니다:

```php
Schema::create('users', function (Blueprint $table) {
    $table->charset('utf8mb4');
    $table->collation('utf8mb4_unicode_ci');

    // ...
});
```



`temporary` 방법은 테이블이 '임시'임을 나타내는 데 사용할 수 있습니다. 임시 테이블은 현재 연결의 데이터베이스 세션에서만 볼 수 있으며, 연결이 종료되면 자동으로 삭제됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->temporary();

    // ...
});
```



데이터베이스 테이블에 "코멘트"를 추가하고 싶다면, 테이블 인스턴스에서 `comment` 메소드를 호출할 수 있습니다. 테이블 코멘트는 현재 MariaDB, MySQL, PostgreSQL에서만 지원됩니다:

```php
Schema::create('calculations', function (Blueprint $table) {
    $table->comment('Business calculations');

    // ...
});
```



<a name="updating-tables"></a>
### 테이블 업데이트

`Schema` 퍼사드의 `table` 메서드는 기존 테이블을 업데이트하는 데 사용할 수 있습니다. `create` 메서드와 마찬가지로 `table` 메서드는 두 개의 인수를 받습니다: 테이블 이름과 `Blueprint` 인스턴스를 받는 클로저로, 이를 사용하여 테이블에 열이나 인덱스를 추가할 수 있습니다.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```



<a name="renaming-and-dropping-tables"></a>
### 테이블 이름 변경 / 삭제

기존 데이터베이스 테이블의 이름을 변경하려면, `rename` 방법을 사용하십시오:

```php
use Illuminate\Support\Facades\Schema;

Schema::rename($from, $to);
```



기존 테이블을 삭제하려면 `drop` 또는 `dropIfExists` 방법을 사용할 수 있습니다:

```php
Schema::drop('users');

Schema::dropIfExists('users');
```



<a name="renaming-tables-with-foreign-keys"></a>
#### 외래 키가 있는 테이블 이름 변경

테이블 이름을 변경하기 전에, 마이그레이션 파일에서 외래 키 제약 조건이 자동으로 Laravel이 규칙에 따라 이름을 지정하도록 두는 대신 명시적인 이름을 가지고 있는지 확인해야 합니다. 그렇지 않으면 외래 키 제약 조건 이름은 이전 테이블 이름을 참조하게 됩니다.

<a name="columns"></a>
## 컬럼

<a name="creating-columns"></a>
### 컬럼 생성

`Schema` 퍼사드의 `table` 메서드는 기존 테이블을 업데이트하는 데 사용할 수 있습니다. `create` 메서드와 마찬가지로, `table` 메서드는 두 개의 인수를 받습니다: 테이블 이름과, 테이블에 컬럼을 추가하는 데 사용할 수 있는 `Illuminate\Database\Schema\Blueprint` 인스턴스를 받는 클로저.

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->integer('votes');
});
```

<a name="available-column-types"></a>
### Available Column Types

The schema builder blueprint offers a variety of methods that correspond to the different types of columns you can add to your database tables. Each of the available methods are listed in the table below:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

.collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

.collection-method code {
        font-size: 14px;
    }

.collection-method:not(.first-collection-method) {
        margin-top: 50px;
    }
</style>

<a name="booleans-method-list"></a>
#### Boolean Types

<div class="collection-method-list" markdown="1">

[boolean](#column-method-boolean)

</div>

<a name="strings-and-texts-method-list"></a>
#### String & Text Types

<div class="collection-method-list" markdown="1">

[char](#column-method-char)
[longText](#column-method-longText)
[mediumText](#column-method-mediumText)
[string](#column-method-string)
[text](#column-method-text)
[tinyText](#column-method-tinyText)

</div>

<a name="numbers--method-list"></a>
#### Numeric Types

<div class="collection-method-list" markdown="1">

[bigIncrements](#column-method-bigIncrements)
[bigInteger](#column-method-bigInteger)
[decimal](#column-method-decimal)
[double](#column-method-double)
[float](#column-method-float)
[id](#column-method-id)
[increments](#column-method-increments)
[integer](#column-method-integer)
[mediumIncrements](#column-method-mediumIncrements)
[mediumInteger](#column-method-mediumInteger)
[smallIncrements](#column-method-smallIncrements)
[smallInteger](#column-method-smallInteger)
[tinyIncrements](#column-method-tinyIncrements)
[tinyInteger](#column-method-tinyInteger)
[unsignedBigInteger](#column-method-unsignedBigInteger)
[unsignedInteger](#column-method-unsignedInteger)
[unsignedMediumInteger](#column-method-unsignedMediumInteger)
[unsignedSmallInteger](#column-method-unsignedSmallInteger)
[unsignedTinyInteger](#column-method-unsignedTinyInteger)

</div>

<a name="dates-and-times-method-list"></a>
#### Date & Time Types

<div class="collection-method-list" markdown="1">



[dateTime](#column-method-dateTime)
[dateTimeTz](#column-method-dateTimeTz)
[date](#column-method-date)
[time](#column-method-time)
[timeTz](#column-method-timeTz)
[timestamp](#column-method-timestamp)
[timestamps](#column-method-timestamps)
[timestampsTz](#column-method-timestampsTz)
[softDeletes](#column-method-softDeletes)
[softDeletesTz](#column-method-softDeletesTz)
[year](#column-method-year)

</div>

<a name="binaries-method-list"></a>
#### Binary Types

<div class="collection-method-list" markdown="1">

[binary](#column-method-binary)

</div>

<a name="object-and-jsons-method-list"></a>
#### Object & Json Types

<div class="collection-method-list" markdown="1">

[json](#column-method-json)
[jsonb](#column-method-jsonb)

</div>

<a name="uuids-and-ulids-method-list"></a>
#### UUID & ULID Types

<div class="collection-method-list" markdown="1">

[ulid](#column-method-ulid)
[ulidMorphs](#column-method-ulidMorphs)
[uuid](#column-method-uuid)
[uuidMorphs](#column-method-uuidMorphs)
[nullableUlidMorphs](#column-method-nullableUlidMorphs)
[nullableUuidMorphs](#column-method-nullableUuidMorphs)

</div>

<a name="spatials-method-list"></a>
#### Spatial Types

<div class="collection-method-list" markdown="1">

[geography](#column-method-geography)
[geometry](#column-method-geometry)

</div>

<a name="relationship-method-list"></a>
#### Relationship Types

<div class="collection-method-list" markdown="1">

[foreignId](#column-method-foreignId)
[foreignIdFor](#column-method-foreignIdFor)
[foreignUlid](#column-method-foreignUlid)
[foreignUuid](#column-method-foreignUuid)
[foreignUuidFor](#column-method-foreignUuidFor)
[morphs](#column-method-morphs)
[nullableMorphs](#column-method-nullableMorphs)

</div>

<a name="specifics-method-list"></a>
#### Specialty Types

<div class="collection-method-list" markdown="1">

[enum](#column-method-enum)
[set](#column-method-set)
[macAddress](#column-method-macAddress)
[ipAddress](#column-method-ipAddress)
[rememberToken](#column-method-rememberToken)
[vector](#column-method-vector)

</div>

<a name="column-method-bigIncrements"></a>
#### `bigIncrements()` {.collection-method .first-collection-method}

The `bigIncrements` method creates an auto-incrementing `UNSIGNED BIGINT` (primary key) equivalent column:

```php
$table->bigIncrements('id');
```



<a name="column-method-bigInteger"></a>
#### `bigInteger()` {.collection-method}

`bigInteger` 방법은 `BIGINT`에 해당하는 열을 생성합니다:

```php
$table->bigInteger('votes');
```



<a name="column-method-binary"></a>
#### `binary()` {.collection-method}

`binary` 방법은 `BLOB`에 해당하는 열을 생성합니다:

```php
$table->binary('photo');
```



MySQL, MariaDB 또는 SQL Server를 사용할 때 `length` 및 `fixed` 인수를 전달하여 `VARBINARY` 또는 `BINARY`에 해당하는 열을 만들 수 있습니다:

```php
$table->binary('data', length: 16); // VARBINARY(16)

$table->binary('data', length: 16, fixed: true); // BINARY(16)
```



<a name="column-method-boolean"></a>
#### `boolean()` {.collection-method}

`boolean` 방법은 `BOOLEAN`에 해당하는 열을 생성합니다:

```php
$table->boolean('confirmed');
```



<a name="column-method-char"></a>
#### `char()` {.collection-method}

`char` 방법은 지정된 길이의 `CHAR`에 해당하는 열을 생성합니다:

```php
$table->char('name', length: 100);
```



<a name="column-method-dateTimeTz"></a>
#### `dateTimeTz()` {.collection-method}

`dateTimeTz` 방법은 선택적인 소수 초 정밀도로 `DATETIME`(시간대 포함) 동등 열을 생성합니다:

```php
$table->dateTimeTz('created_at', precision: 0);
```



<a name="column-method-dateTime"></a>
#### `dateTime()` {.collection-method}

`dateTime` 메서드는 선택적 소수 초 정밀도를 가진 `DATETIME`와 동일한 컬럼을 생성합니다:

```php
$table->dateTime('created_at', precision: 0);
```



<a name="column-method-date"></a>
#### `date()` {.collection-method}

`date` 방법은 `DATE`에 해당하는 열을 생성합니다:

```php
$table->date('created_at');
```



<a name="column-method-decimal"></a>
#### `decimal()` {.collection-method}

`decimal` 방법은 주어진 정밀도(전체 자릿수)와 스케일(소수 자릿수)로 `DECIMAL`에 해당하는 열을 생성합니다:

```php
$table->decimal('amount', total: 8, places: 2);
```



<a name="column-method-double"></a>
#### `double()` {.collection-method}

`double` 방법은 `DOUBLE`에 해당하는 열을 생성합니다:

```php
$table->double('amount');
```



<a name="column-method-enum"></a>
#### `enum()` {.collection-method}

`enum` 방법은 주어진 유효 값으로 `ENUM`에 해당하는 열을 생성합니다:

```php
$table->enum('difficulty', ['easy', 'hard']);
```



물론, 허용된 값들의 배열을 수동으로 정의하는 대신 `Enum::cases()` 방법을 사용할 수 있습니다:

```php
use App\Enums\Difficulty;

$table->enum('difficulty', Difficulty::cases());
```



<a name="column-method-float"></a>
#### `float()` {.collection-method}

`float` 방법은 주어진 정밀도로 `FLOAT`에 해당하는 열을 생성합니다:

```php
$table->float('amount', precision: 53);
```



<a name="column-method-foreignId"></a>
#### `foreignId()` {.collection-method}

`foreignId` 방법은 `UNSIGNED BIGINT`에 해당하는 열을 생성합니다:

```php
$table->foreignId('user_id');
```



<a name="column-method-foreignIdFor"></a>
#### `foreignIdFor()` {.collection-method}

`foreignIdFor` 메서드는 주어진 모델 클래스에 대해 `{column}_id`에 해당하는 열을 추가합니다. 열 유형은 모델 키 유형에 따라 `UNSIGNED BIGINT`, `CHAR(36)` 또는 `CHAR(26)`이 됩니다:

```php
$table->foreignIdFor(User::class);
```



<a name="column-method-foreignUlid"></a>
#### `foreignUlid()` {.collection-method}

`foreignUlid` 방법은 `ULID`에 해당하는 열을 생성합니다:

```php
$table->foreignUlid('user_id');
```



<a name="column-method-foreignUuid"></a>
#### `foreignUuid()` {.collection-method}

`foreignUuid` 방법은 `UUID`에 해당하는 열을 생성합니다:

```php
$table->foreignUuid('user_id');
```



<a name="column-method-foreignUuidFor"></a>
#### `foreignUuidFor()` {.collection-method}

`foreignUuidFor` 메서드는 주어진 모델 클래스에 `{column}_id` UUID에 해당하는 컬럼을 추가합니다:

```php
$table->foreignUuidFor(User::class);
```



<a name="column-method-geography"></a>
#### `geography()` {.collection-method}

`geography` 방법은 주어진 공간 유형과 SRID(공간 참조 시스템 식별자)를 가진 `GEOGRAPHY`에 해당하는 열을 생성합니다:

```php
$table->geography('coordinates', subtype: 'point', srid: 4326);
```



> [!NOTE]
> 공간 유형에 대한 지원은 사용 중인 데이터베이스 드라이버에 따라 다릅니다. 데이터베이스의 문서를 참조하십시오. 애플리케이션이 PostgreSQL 데이터베이스를 사용 중인 경우, `geography` 메서드를 사용하기 전에 [PostGIS](https://postgis.net) 확장 기능을 설치해야 합니다.

<a name="column-method-geometry"></a>
#### `geometry()` {.collection-method}

`geometry` 메서드는 지정된 공간 유형과 SRID(Spatial Reference System Identifier)를 사용하여 `GEOMETRY`에 해당하는 열을 생성합니다:

```php
$table->geometry('positions', subtype: 'point', srid: 0);
```



> [!NOTE]
> 공간 타입 지원은 데이터베이스 드라이버에 따라 다릅니다. 데이터베이스 문서를 참조하시기 바랍니다. 애플리케이션이 PostgreSQL 데이터베이스를 사용 중이라면, `geometry` 메서드를 사용하기 전에 반드시 [PostGIS](https://postgis.net) 확장을 설치해야 합니다.

<a name="column-method-id"></a>
#### `id()` {.collection-method}

`id` 메서드는 `bigIncrements` 메서드의 별칭입니다. 기본적으로 이 메서드는 `id` 컬럼을 생성하지만, 다른 이름을 컬럼에 지정하고 싶다면 컬럼 이름을 전달할 수 있습니다:

```php
$table->id();
```



<a name="column-method-increments"></a>
#### `increments()` {.collection-method}

`increments` 메서드는 기본 키로서 자동 증가하는 `UNSIGNED INTEGER` 동등 열을 생성합니다:

```php
$table->increments('id');
```



<a name="column-method-integer"></a>
#### `integer()` {.collection-method}

`integer` 방법은 `INTEGER`에 해당하는 열을 생성합니다:

```php
$table->integer('votes');
```



<a name="column-method-ipAddress"></a>
#### `ipAddress()` {.collection-method}

`ipAddress` 방법은 `VARCHAR`에 해당하는 열을 생성합니다:

```php
$table->ipAddress('visitor');
```



PostgreSQL을 사용할 때 `INET` 열이 생성됩니다.

<a name="column-method-json"></a>
#### `json()` {.collection-method}

`json` 메서드는 `JSON`와 동등한 열을 생성합니다:

```php
$table->json('options');
```



SQLite를 사용할 때 `TEXT` 열이 생성됩니다.

<a name="column-method-jsonb"></a>
#### `jsonb()` {.collection-method}

`jsonb` 메서드는 `JSONB`와 동등한 열을 생성합니다:

```php
$table->jsonb('options');
```



SQLite를 사용할 때 `TEXT` 열이 생성됩니다.

<a name="column-method-longText"></a>
#### `longText()` {.collection-method}

`longText` 메서드는 `LONGTEXT`와 동등한 열을 생성합니다:

```php
$table->longText('description');
```



MySQL 또는 MariaDB를 사용할 때 열에 `binary` 문자 집합을 적용하여 `LONGBLOB`에 해당하는 열을 생성할 수 있습니다:

```php
$table->longText('data')->charset('binary'); // LONGBLOB
```



<a name="column-method-macAddress"></a>
#### `macAddress()` {.collection-method}

`macAddress` 방법은 MAC 주소를 저장하도록 설계된 열을 생성합니다. PostgreSQL과 같은 일부 데이터베이스 시스템은 이 유형의 데이터를 위한 전용 열 타입을 제공합니다. 다른 데이터베이스 시스템은 문자열에 해당하는 열을 사용합니다:

```php
$table->macAddress('device');
```



<a name="column-method-mediumIncrements"></a>
#### `mediumIncrements()` {.collection-method}

`mediumIncrements` 메서드는 기본 키로서 자동 증가하는 `UNSIGNED MEDIUMINT` 동등 열을 생성합니다:

```php
$table->mediumIncrements('id');
```



<a name="column-method-mediumInteger"></a>
#### `mediumInteger()` {.collection-method}

`mediumInteger` 방법은 `MEDIUMINT`에 해당하는 열을 생성합니다:

```php
$table->mediumInteger('votes');
```



<a name="column-method-mediumText"></a>
#### `mediumText()` {.collection-method}

`mediumText` 방법은 `MEDIUMTEXT`에 해당하는 열을 생성합니다:

```php
$table->mediumText('description');
```



MySQL 또는 MariaDB를 사용할 때 열에 `binary` 문자 세트를 적용하여 `MEDIUMBLOB`에 해당하는 열을 만들 수 있습니다:

```php
$table->mediumText('data')->charset('binary'); // MEDIUMBLOB
```



<a name="column-method-morphs"></a>
#### `morphs()` {.collection-method}

`morphs` 메서드는 `{column}_type` `VARCHAR` 동등 컬럼과 `{column}_id` 동등 컬럼을 추가하는 편리한 메서드입니다. `{column}_id`의 컬럼 유형은 모델 키 유형에 따라 `UNSIGNED BIGINT`, `CHAR(36)` 또는 `CHAR(26)`가 됩니다.

이 메서드는 다형성 [Eloquent 관계](/docs/{{version}}/eloquent-relationships)를 정의할 때 필요한 컬럼을 정의하는 데 사용하도록 설계되었습니다. 다음 예제에서는 `taggable_type`와 `taggable_id` 컬럼이 생성됩니다:

```php
$table->morphs('taggable');
```



<a name="column-method-nullableMorphs"></a>
#### `nullableMorphs()` {.collection-method}

이 방법은 [morphs](#column-method-morphs) 방법과 유사하지만, 생성되는 열은 "nullable":" 입니다.

```php
$table->nullableMorphs('taggable');
```



<a name="column-method-nullableUlidMorphs"></a>
#### `nullableUlidMorphs()` {.collection-method}

이 방법은 [ulidMorphs](#column-method-ulidMorphs) 방법과 유사합니다; 그러나 생성되는 열은 "nullable":"입니다

```php
$table->nullableUlidMorphs('taggable');
```



<a name="column-method-nullableUuidMorphs"></a>
#### `nullableUuidMorphs()` {.collection-method}

이 방법은 [uuidMorphs](#column-method-uuidMorphs) 방법과 유사하지만, 생성되는 열은 "nullable":" 입니다.

```php
$table->nullableUuidMorphs('taggable');
```



<a name="column-method-rememberToken"></a>
#### `rememberToken()` {.collection-method}

`rememberToken` 방법은 현재 "로그인 상태 유지" [인증 토큰](/docs/{{version}}/authentication#remembering-users)을 저장하도록 의도된, nullable하고 `VARCHAR(100)`에 해당하는 열을 생성합니다:

```php
$table->rememberToken();
```



<a name="column-method-set"></a>
#### `set()` {.collection-method}

`set` 방법은 주어진 유효 값 목록으로 `SET`에 해당하는 열을 생성합니다:

```php
$table->set('flavors', ['strawberry', 'vanilla']);
```



<a name="column-method-smallIncrements"></a>
#### `smallIncrements()` {.collection-method}

`smallIncrements` 메서드는 기본 키로서 자동 증가하는 `UNSIGNED SMALLINT` 동등 열을 생성합니다:

```php
$table->smallIncrements('id');
```



<a name="column-method-smallInteger"></a>
#### `smallInteger()` {.collection-method}

`smallInteger` 방법은 `SMALLINT`에 해당하는 열을 생성합니다:

```php
$table->smallInteger('votes');
```



<a name="column-method-softDeletesTz"></a>
#### `softDeletesTz()` {.collection-method}

`softDeletesTz` 메서드는 선택적 소수점 이하 초 정밀도를 가진 nullable `deleted_at` `TIMESTAMP`(시간대 포함) 동등 컬럼을 추가합니다. 이 컬럼은 Eloquent의 'soft delete' 기능에 필요한 `deleted_at` 타임스탬프를 저장하도록 설계되었습니다:

```php
$table->softDeletesTz('deleted_at', precision: 0);
```



<a name="column-method-softDeletes"></a>
#### `softDeletes()` {.collection-method}

`softDeletes` 방법은 선택적 소수 초 정밀도를 가진 null 허용 `deleted_at` `TIMESTAMP` 동등 열을 추가합니다. 이 열은 Eloquent의 "soft delete" 기능에 필요한 `deleted_at` 타임스탬프를 저장하기 위해 사용됩니다:

```php
$table->softDeletes('deleted_at', precision: 0);
```



<a name="column-method-string"></a>
#### `string()` {.collection-method}

`string` 방법은 주어진 길이의 `VARCHAR` 등가 열을 생성합니다:

```php
$table->string('name', length: 100);
```



<a name="column-method-text"></a>
#### `text()` {.collection-method}

`text` 방법은 `TEXT`에 해당하는 열을 생성합니다:

```php
$table->text('description');
```



MySQL 또는 MariaDB를 사용할 때 열에 `binary` 문자 세트를 적용하여 `BLOB`에 해당하는 열을 만들 수 있습니다:

```php
$table->text('data')->charset('binary'); // BLOB
```



<a name="column-method-timeTz"></a>
#### `timeTz()` {.collection-method}

`timeTz` 방법은 선택적인 소수 초 정밀도로 `TIME`(시간대 포함) 동등 열을 생성합니다:

```php
$table->timeTz('sunrise', precision: 0);
```



<a name="column-method-time"></a>
#### `time()` {.collection-method}

`time` 메서드는 선택적 소수 초 정밀도를 가진 `TIME`와 동일한 컬럼을 생성합니다:

```php
$table->time('sunrise', precision: 0);
```



<a name="column-method-timestampTz"></a>
#### `timestampTz()` {.collection-method}

`timestampTz` 방법은 선택적인 소수 초 정밀도로 `TIMESTAMP`(시간대 포함) 동등 열을 생성합니다:

```php
$table->timestampTz('added_at', precision: 0);
```



<a name="column-method-timestamp"></a>
#### `timestamp()` {.collection-method}

`timestamp` 메서드는 선택적 소수 초 정밀도를 가진 `TIMESTAMP`와 동일한 컬럼을 생성합니다:

```php
$table->timestamp('added_at', precision: 0);
```



<a name="column-method-timestampsTz"></a>
#### `timestampsTz()` {.collection-method}

`timestampsTz` 방법은 선택적 소수 초 정밀도로 `created_at` 및 `updated_at` `TIMESTAMP`(시간대 포함) 동등 컬럼을 생성합니다:

```php
$table->timestampsTz(precision: 0);
```



<a name="column-method-timestamps"></a>
#### `timestamps()` {.collection-method}

`timestamps` 방법은 선택적인 소수점 이하 초 정밀도로 `created_at` 및 `updated_at` `TIMESTAMP` 동등한 열을 생성합니다:

```php
$table->timestamps(precision: 0);
```



<a name="column-method-tinyIncrements"></a>
#### `tinyIncrements()` {.collection-method}

`tinyIncrements` 메서드는 기본 키로서 자동 증가하는 `UNSIGNED TINYINT` 동등 열을 생성합니다:

```php
$table->tinyIncrements('id');
```



<a name="column-method-tinyInteger"></a>
#### `tinyInteger()` {.collection-method}

`tinyInteger` 방법은 `TINYINT`에 해당하는 열을 생성합니다:

```php
$table->tinyInteger('votes');
```



<a name="column-method-tinyText"></a>
#### `tinyText()` {.collection-method}

`tinyText` 방법은 `TINYTEXT`에 해당하는 열을 생성합니다:

```php
$table->tinyText('notes');
```



MySQL 또는 MariaDB를 사용할 때 열에 `binary` 문자 세트를 적용하여 `TINYBLOB`에 해당하는 열을 생성할 수 있습니다:

```php
$table->tinyText('data')->charset('binary'); // TINYBLOB
```



<a name="column-method-unsignedBigInteger"></a>
#### `unsignedBigInteger()` {.collection-method}

`unsignedBigInteger` 방법은 `UNSIGNED BIGINT`에 해당하는 열을 생성합니다:

```php
$table->unsignedBigInteger('votes');
```



<a name="column-method-unsignedInteger"></a>
#### `unsignedInteger()` {.collection-method}

`unsignedInteger` 방법은 `UNSIGNED INTEGER`에 해당하는 열을 생성합니다:

```php
$table->unsignedInteger('votes');
```



<a name="column-method-unsignedMediumInteger"></a>
#### `unsignedMediumInteger()` {.collection-method}

`unsignedMediumInteger` 방법은 `UNSIGNED MEDIUMINT`에 해당하는 열을 생성합니다:

```php
$table->unsignedMediumInteger('votes');
```



<a name="column-method-unsignedSmallInteger"></a>
#### `unsignedSmallInteger()` {.collection-method}

`unsignedSmallInteger` 방법은 `UNSIGNED SMALLINT`에 해당하는 열을 생성합니다:

```php
$table->unsignedSmallInteger('votes');
```



<a name="column-method-unsignedTinyInteger"></a>
#### `unsignedTinyInteger()` {.collection-method}

`unsignedTinyInteger` 방법은 `UNSIGNED TINYINT`에 해당하는 열을 생성합니다:

```php
$table->unsignedTinyInteger('votes');
```



<a name="column-method-ulidMorphs"></a>
#### `ulidMorphs()` {.collection-method}

`ulidMorphs` 메서드는 `{column}_type` `VARCHAR`에 해당하는 컬럼을 추가하고, `{column}_id` `CHAR(26)`에 해당하는 컬럼을 추가하는 편의 메서드입니다.

이 메서드는 ULID 식별자를 사용하는 다형성 [Eloquent 관계](/docs/{{version}}/eloquent-relationships)에 필요한 컬럼을 정의할 때 사용하도록 설계되었습니다. 다음 예제에서는 `taggable_type`와 `taggable_id` 컬럼이 생성됩니다:

```php
$table->ulidMorphs('taggable');
```



<a name="column-method-uuidMorphs"></a>
#### `uuidMorphs()` {.collection-method}

`uuidMorphs` 메서드는 `{column}_type` `VARCHAR`에 해당하는 컬럼을 추가하고, `{column}_id` `CHAR(36)`에 해당하는 컬럼을 추가하는 편의 메서드입니다.

이 메서드는 UUID 식별자를 사용하는 [다형 Eloquent 관계](/docs/{{version}}/eloquent-relationships#polymorphic-relationships)에 필요한 컬럼을 정의할 때 사용하도록 되어 있습니다. 다음 예제에서는 `taggable_type` 및 `taggable_id` 컬럼이 생성됩니다:

```php
$table->uuidMorphs('taggable');
```



<a name="column-method-ulid"></a>
#### `ulid()` {.collection-method}

`ulid` 방법은 `ULID`에 해당하는 열을 생성합니다:

```php
$table->ulid('id');
```



<a name="column-method-uuid"></a>
#### `uuid()` {.collection-method}

`uuid` 방법은 `UUID`에 해당하는 열을 생성합니다:

```php
$table->uuid('id');
```



<a name="column-method-vector"></a>
#### `vector()` {.collection-method}

`vector` 방법은 `vector`에 해당하는 열을 생성합니다:

```php
$table->vector('embedding', dimensions: 1536);
```



벡터 열은 `pgvector` 확장을 사용하는 PostgreSQL 연결과 MariaDB 11.7 이상에서 지원됩니다. PostgreSQL을 사용할 때는 `vector` 열을 생성하기 전에 `pgvector`가 로드되어야 합니다:

```php
Schema::ensureVectorExtensionExists();
```



[벡터 유사성 쿼리](/docs/{{version}}/queries#vector-similarity-clauses)를 가속화하려면 열에 벡터 인덱스를 추가할 수 있습니다. `vector` 열에서 `index` 메서드를 호출하면 코사인 거리를 사용하여 벡터 인덱스를 생성합니다:

```php
$table->vector('embedding', dimensions: 1536)->index();
```



<a name="column-method-year"></a>
#### `year()` {.collection-method}

`year` 방법은 `YEAR`에 해당하는 열을 생성합니다:

```php
$table->year('birth_year');
```



<a name="column-modifiers"></a>
### 열 수정자

위에 나열된 열 유형 외에도 데이터베이스 테이블에 열을 추가할 때 사용할 수 있는 여러 열 "수정자"가 있습니다. 예를 들어, 열을 "널 허용(nullable)"로 만들려면 `nullable` 방법을 사용할 수 있습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->nullable();
});
```

다음 표에는 사용 가능한 모든 열 수정자가 포함되어 있습니다. 이 목록에는 [인덱스 수정자](#creating-indexes)는 포함되어 있지 않습니다:

<div class="overflow-auto">

| Modifier                            | Description                                                                                    |
| ----------------------------------- | ---------------------------------------------------------------------------------------------- |
| `->after('column')`                 | Place the column "after" another column (MariaDB / MySQL).                                     |
| `->autoIncrement()`                 | Set `INTEGER` columns as auto-incrementing (primary key).                                      |
| `->charset('utf8mb4')`              | Specify a character set for the column (MariaDB / MySQL).                                      |
| `->collation('utf8mb4_unicode_ci')` | Specify a collation for the column.                                                            |
| `->comment('my comment')`           | Add a comment to a column (MariaDB / MySQL / PostgreSQL).                                      |
| `->default($value)`                 | Specify a "default" value for the column.                                                      |
| `->first()`                         | Place the column "first" in the table (MariaDB / MySQL).                                       |
| `->from($integer)`                  | Set the starting value of an auto-incrementing field (MariaDB / MySQL / PostgreSQL).           |
| `->instant()`                       | Add or modify the column using an instant operation (MySQL).                                   |
| `->invisible()`                     | Make the column "invisible" to `SELECT *` queries (MariaDB / MySQL).                           |
| `->lock($mode)`                     | Specify a lock mode for the column operation (MySQL).                                          |
| `->nullable($value = true)`         | Allow `NULL` values to be inserted into the column.                                            |
| `->storedAs($expression)`           | Create a stored generated column (MariaDB / MySQL / PostgreSQL / SQLite).                      |
| `->unsigned()`                      | Set `INTEGER` columns as `UNSIGNED` (MariaDB / MySQL).                                         |
| `->using($expression)`              | Specify a casting expression when changing the column type (PostgreSQL).                       |
| `->useCurrent()`                    | Set `TIMESTAMP` columns to use `CURRENT_TIMESTAMP` as default value.                           |
| `->useCurrentOnUpdate()`            | Set `TIMESTAMP` columns to use `CURRENT_TIMESTAMP` when a record is updated (MariaDB / MySQL). |
| `->virtualAs($expression)`          | Create a virtual generated column (MariaDB / MySQL / SQLite).                                  |
| `->generatedAs($expression)`        | Create an identity column with specified sequence options (PostgreSQL).                        |
| `->always()`                        | Defines the precedence of sequence values over input for an identity column (PostgreSQL).      |



</div>

<a name="default-expressions"></a>
#### 기본 표현식

`default` 수정자는 값 또는 `Illuminate\Database\Query\Expression` 인스턴스를 허용합니다. `Expression` 인스턴스를 사용하면 Laravel이 값을 따옴표로 감싸지 않으며 데이터베이스 특정 함수를 사용할 수 있습니다. 이것이 특히 유용한 경우는 JSON 열에 기본 값을 할당해야 할 때입니다:

```php
<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Query\Expression;
use Illuminate\Database\Migrations\Migration;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('flights', function (Blueprint $table) {
            $table->id();
            $table->json('movies')->default(new Expression('(JSON_ARRAY())'));
            $table->timestamps();
        });
    }
};
```



> [!WARNING]
> 기본 표현식 지원 여부는 데이터베이스 드라이버, 데이터베이스 버전 및 필드 유형에 따라 다릅니다. 데이터베이스 문서를 참조하세요.

<a name="column-order"></a>
#### 열 순서

MariaDB 또는 MySQL 데이터베이스를 사용할 때는 스키마의 기존 열 뒤에 열을 추가하기 위해 `after` 방법을 사용할 수 있습니다:

```php
$table->after('password', function (Blueprint $table) {
    $table->string('address_line1');
    $table->string('address_line2');
    $table->string('city');
});
```



<a name="instant-column-operations"></a>
#### 즉시 열 작업

MySQL을 사용할 때, 열 정의에 `instant` 수식어를 연결하여 해당 열이 MySQL의 "즉시" 알고리즘을 사용하여 추가되거나 수정되어야 함을 나타낼 수 있습니다. 이 알고리즘은 전체 테이블 재구성이 필요 없이 특정 스키마 변경을 수행할 수 있게 하여 테이블 크기에 관계없이 거의 즉시 변경이 이루어지도록 합니다:

```php
$table->string('name')->nullable()->instant();
```



즉시 열 추가는 테이블의 끝에만 열을 추가할 수 있으므로 `instant` 수정자는 `after` 또는 `first` 수정자와 결합할 수 없습니다. 또한, 알고리즘은 모든 열 유형이나 연산을 지원하지 않습니다. 요청된 연산이 호환되지 않는 경우 MySQL은 오류를 발생시킵니다.

어떤 연산이 즉시 열 수정과 호환되는지 확인하려면 [MySQL 문서](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)를 참조하십시오.

<a name="ddl-locking"></a>
#### DDL 잠금

MySQL을 사용할 때 열, 인덱스 또는 외래 키 정의에 `lock` 수정자를 연결하여 스키마 작업 중 테이블 잠금을 제어할 수 있습니다. MySQL은 여러 잠금 모드를 지원합니다: `none`는 동시 읽기 및 쓰기를 허용하고, `shared`는 동시 읽기는 허용하지만 쓰기는 차단하며, `exclusive`는 모든 동시 접근을 차단하고, `default`는 MySQL이 가장 적절한 모드를 선택하도록 합니다:

```php
$table->string('name')->lock('none');

$table->index('email')->lock('shared');
```



요청된 잠금 모드가 작업과 호환되지 않으면 MySQL은 오류를 발생시킵니다. `lock` 수정자는 `instant` 수정자와 결합하여 스키마 변경을 더욱 최적화할 수 있습니다:

```php
$table->string('name')->instant()->lock('none');
```



<a name="modifying-columns"></a>
### 열 수정

`change` 메서드를 사용하면 기존 열의 유형과 속성을 수정할 수 있습니다. 예를 들어, `string` 열의 크기를 늘리고 싶을 수 있습니다. `change` 메서드가 실제로 어떻게 작동하는지 보기 위해, `name` 열의 크기를 25에서 50으로 늘려 보겠습니다. 이를 달성하려면 단순히 열의 새로운 상태를 정의한 다음 `change` 메서드를 호출하면 됩니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->string('name', 50)->change();
});
```



열을 수정할 때는 열 정의에서 유지하고자 하는 모든 수정자를 명시적으로 포함해야 합니다 - 누락된 속성은 모두 제거됩니다. 예를 들어, `unsigned`, `default`, `comment` 속성을 유지하려면 열을 변경할 때 각 수정자를 명시적으로 호출해야 합니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->integer('votes')->unsigned()->default(1)->comment('my comment')->change();
});
```



`change` 방법은 열의 인덱스를 변경하지 않습니다. 따라서 열을 수정할 때 인덱스 조정자를 사용하여 인덱스를 명시적으로 추가하거나 제거할 수 있습니다:

```php
// Add an index...
$table->bigIncrements('id')->primary()->change();

// Drop an index...
$table->char('postal_code', 10)->unique(false)->change();
```



<a name="postgresql-column-modifications"></a>
#### PostgreSQL 열 수정

PostgreSQL에서 열의 유형을 변경할 때 기존 값을 변환하는 데 사용되는 표현식을 지정하려면 `using` 수정자를 사용할 수 있습니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->date('birthday')->using('birthday::date')->change();
});
```



<a name="renaming-columns"></a>
### 열 이름 바꾸기

열 이름을 바꾸려면, 스키마 빌더에서 제공하는 `renameColumn` 방법을 사용할 수 있습니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->renameColumn('from', 'to');
});
```



<a name="dropping-columns"></a>
### 열 삭제

열을 삭제하려면 스키마 빌더에서 `dropColumn` 메서드를 사용할 수 있습니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn('votes');
});
```



`dropColumn` 메서드에 열 이름 배열을 전달하여 테이블에서 여러 열을 제거할 수 있습니다:

```php
Schema::table('users', function (Blueprint $table) {
    $table->dropColumn(['votes', 'avatar', 'location']);
});
```



<a name="available-command-aliases"></a>
#### Available Command Aliases

Laravel provides several convenient methods related to dropping common types of columns. Each of these methods is described in the table below:

<div class="overflow-auto">

| Command                             | Description                                           |
| ----------------------------------- | ----------------------------------------------------- |
| `$table->dropMorphs('morphable');`  | Drop the `morphable_type` and `morphable_id` columns. |
| `$table->dropRememberToken();`      | Drop the `remember_token` column.                     |
| `$table->dropSoftDeletes();`        | Drop the `deleted_at` column.                         |
| `$table->dropSoftDeletesTz();`      | Alias of `dropSoftDeletes()` method.                  |
| `$table->dropTimestamps();`         | Drop the `created_at` and `updated_at` columns.       |
| `$table->dropTimestampsTz();`       | Alias of `dropTimestamps()` method.                   |

</div>

<a name="indexes"></a>
## Indexes

<a name="creating-indexes"></a>
### Creating Indexes

The Laravel schema builder supports several types of indexes. The following example creates a new `email` column and specifies that its values should be unique. To create the index, we can chain the `unique` method onto the column definition:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('users', function (Blueprint $table) {
    $table->string('email')->unique();
});
```



또는 열을 정의한 후에 인덱스를 생성할 수 있습니다. 이렇게 하려면 스키마 빌더 블루프린트에서 `unique` 메서드를 호출해야 합니다. 이 메서드는 고유 인덱스를 받을 열의 이름을 인수로 받습니다:

```php
$table->unique('email');
```



여러 열의 배열을 인덱스 메서드에 전달하여 복합(또는 합성) 인덱스를 만들 수도 있습니다:

```php
$table->index(['account_id', 'created_at']);
```



인덱스를 생성할 때, Laravel은 테이블, 컬럼 이름 및 인덱스 유형에 따라 자동으로 인덱스 이름을 생성하지만, 메서드에 두 번째 인수를 전달하여 직접 인덱스 이름을 지정할 수 있습니다:

```php
$table->unique('email', 'unique_email');
```



<a name="available-index-types"></a>
#### Available Index Types

Laravel's schema builder blueprint class provides methods for creating each type of index supported by Laravel. Each index method accepts an optional second argument to specify the name of the index. If omitted, the name will be derived from the names of the table and column(s) used for the index, as well as the index type. Each of the available index methods is described in the table below:

<div class="overflow-auto">

| Command                                          | Description                                                    |
| ------------------------------------------------ | -------------------------------------------------------------- |
| `$table->primary('id');`                         | Adds a primary key.                                            |
| `$table->primary(['id', 'parent_id']);`          | Adds composite keys.                                           |
| `$table->unique('email');`                       | Adds a unique index.                                           |
| `$table->index('state');`                        | Adds an index.                                                 |
| `$table->fullText('body');`                      | Adds a full text index (MariaDB / MySQL / PostgreSQL).         |
| `$table->fullText('body')->language('english');` | Adds a full text index of the specified language (PostgreSQL). |
| `$table->spatialIndex('location');`              | Adds a spatial index (except SQLite).                          |
| `$table->vectorIndex('embedding');`              | Adds a vector index (MariaDB / PostgreSQL).                    |

</div>

<a name="online-index-creation"></a>
#### Online Index Creation

By default, creating an index on a large table can lock the table and block reads or writes while the index is being built. When using PostgreSQL or SQL Server, you may chain the `online` method onto an index definition to create the index without locking the table, allowing your application to continue reading and writing data during index creation:

```php
$table->string('email')->unique()->online();
```



PostgreSQL을 사용할 때, 이는 인덱스 생성 문에 `CONCURRENTLY` 옵션을 추가합니다. SQL Server를 사용할 때, 이는 `WITH (online = on)` 옵션을 추가합니다.

MySQL을 사용할 때, 인덱스나 외래 키 정의에 `inplace` 수정자를 체인하여 해당 작업이 `INPLACE` 알고리즘을 사용하도록 지정할 수 있습니다:

```php
$table->index('email')->inplace();

$table->foreign('user_id')->references('id')->on('users')->inplace();
```



`inplace` 수정자는 작업 중 테이블 잠금을 제어하기 위해 `lock` 수정자와 결합될 수 있습니다:

```php
$table->index('email')->inplace()->lock('none');
```



외래 키 작업에 `inplace` 수식어를 사용할 때는 외래 키 검사를 비활성화해야 합니다.

어떤 작업이 `INPLACE` 알고리즘과 잠금 모드를 지원하는지 확인하려면 [MySQL 문서](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-operations.html)를 참조하십시오.

<a name="renaming-indexes"></a>
### 인덱스 이름 변경

인덱스 이름을 변경하려면 스키마 빌더 청사진에서 제공하는 `renameIndex` 메서드를 사용할 수 있습니다. 이 메서드는 현재 인덱스 이름을 첫 번째 인수로 받고, 원하는 이름을 두 번째 인수로 받습니다:

```php
$table->renameIndex('from', 'to');
```



<a name="dropping-indexes"></a>
### Dropping Indexes

To drop an index, you must specify the index's name. By default, Laravel automatically assigns an index name based on the table name, the name of the indexed column, and the index type. Here are some examples:

<div class="overflow-auto">

| Command                                                       | Description                                                 |
| ------------------------------------------------------------- | ----------------------------------------------------------- |
| `$table->dropPrimary('users_id_primary');`                    | Drop a primary key from the "users" table.                  |
| `$table->dropUnique('users_email_unique');`                   | Drop a unique index from the "users" table.                 |
| `$table->dropIndex('geo_state_index');`                       | Drop a basic index from the "geo" table.                    |
| `$table->dropFullText('posts_body_fulltext');`                | Drop a full text index from the "posts" table.              |
| `$table->dropSpatialIndex('geo_location_spatialindex');`      | Drop a spatial index from the "geo" table  (except SQLite). |
| `$table->dropVectorIndex('documents_embedding_vectorindex');` | Drop a vector index from the "documents" table.             |

</div>

If you pass an array of columns into a method that drops indexes, the conventional index name will be generated based on the table name, columns, and index type:

```php
Schema::table('geo', function (Blueprint $table) {
    $table->dropIndex(['state']); // Drops index 'geo_state_index'
});
```



<a name="foreign-key-constraints"></a>
### 외래 키 제약 조건

Laravel은 또한 데이터베이스 수준에서 참조 무결성을 강제하기 위해 사용되는 외래 키 제약 조건 생성을 지원합니다. 예를 들어, `users` 테이블의 `id` 열을 참조하는 `posts` 테이블에 `user_id` 열을 정의해 보겠습니다:

```php
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

Schema::table('posts', function (Blueprint $table) {
    $table->unsignedBigInteger('user_id');

    $table->foreign('user_id')->references('id')->on('users');
});
```



이 구문은 다소 장황하기 때문에 Laravel은 개발자 경험을 향상시키기 위해 관례를 사용하는 추가적이고 더 간결한 메서드를 제공합니다. `foreignId` 메서드를 사용하여 열을 생성할 때, 위의 예제는 다음과 같이 다시 작성할 수 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained();
});
```



`foreignId` 메서드는 `UNSIGNED BIGINT`에 해당하는 열을 생성하는 반면, `constrained` 메서드는 표와 참조되는 열을 결정하기 위해 규칙을 사용합니다. 만약 테이블 이름이 Laravel의 규칙과 일치하지 않는 경우, `constrained` 메서드에 수동으로 제공할 수 있습니다. 또한 생성된 인덱스에 할당될 이름을 지정할 수도 있습니다:

```php
Schema::table('posts', function (Blueprint $table) {
    $table->foreignId('user_id')->constrained(
        table: 'users', indexName: 'posts_user_id'
    );
});
```



제약 조건의 "on delete" 및 "on update" 속성에 대해 원하는 동작을 지정할 수도 있습니다:

```php
$table->foreignId('user_id')
    ->constrained()
    ->onUpdate('cascade')
    ->onDelete('cascade');
```



이러한 동작에 대해서는 대안적이고 표현적인 문법도 제공됩니다:

<div class="overflow-auto">

| 메서드                        | 설명                                               |
| ----------------------------- | ------------------------------------------------- |
| `$table->cascadeOnUpdate();`  | 업데이트가 연쇄적으로 적용되어야 합니다.                  |
| `$table->restrictOnUpdate();` | 업데이트가 제한되어야 합니다.                            |
| `$table->nullOnUpdate();`     | 업데이트가 외래 키 값을 null로 설정해야 합니다.         |
| `$table->noActionOnUpdate();` | 업데이트에 대해 아무 동작도 수행하지 않습니다.             |
| `$table->cascadeOnDelete();`  | 삭제가 연쇄적으로 적용되어야 합니다.                    |
| `$table->restrictOnDelete();` | 삭제가 제한되어야 합니다.                               |
| `$table->nullOnDelete();`     | 삭제가 외래 키 값을 null로 설정해야 합니다.              |
| `$table->noActionOnDelete();` | 자식 레코드가 존재하면 삭제를 방지합니다.                 |

</div>

추가 [열 수정자](#column-modifiers)는 `constrained` 메서드를 호출하기 전에 반드시 호출해야 합니다:

```php
$table->foreignId('user_id')
    ->nullable()
    ->constrained();
```



<a name="dropping-foreign-keys"></a>
#### 외래 키 삭제

외래 키를 삭제하려면 `dropForeign` 메서드를 사용하여 삭제할 외래 키 제약 조건의 이름을 인수로 전달할 수 있습니다. 외래 키 제약 조건은 인덱스와 동일한 명명 규칙을 사용합니다. 다시 말해, 외래 키 제약 조건 이름은 테이블 이름과 제약 조건에 있는 열 이름을 기반으로 하며, 그 뒤에 "_foreign" 접미사가 붙습니다:

```php
$table->dropForeign('posts_user_id_foreign');
```



또는 외래 키를 포함하는 열 이름을 담고 있는 배열을 `dropForeign` 메서드에 전달할 수 있습니다. 이 배열은 Laravel의 제약 조건 명명 규칙을 사용하여 외래 키 제약 조건 이름으로 변환됩니다:

```php
$table->dropForeign(['user_id']);
```



<a name="toggling-foreign-key-constraints"></a>
#### 외래 키 제약 조건 전환

다음 방법을 사용하여 마이그레이션 내에서 외래 키 제약 조건을 활성화하거나 비활성화할 수 있습니다:

```php
Schema::enableForeignKeyConstraints();

Schema::disableForeignKeyConstraints();

Schema::withoutForeignKeyConstraints(function () {
    // Constraints disabled within this closure...
});
```

> [!WARNING]
> SQLite disables foreign key constraints by default. When using SQLite, make sure to [enable foreign key support](/docs/{{version}}/database#configuration) in your database configuration before attempting to create them in your migrations.

<a name="events"></a>
## Events

For convenience, each migration operation will dispatch an [event](/docs/{{version}}/events). All of the following events extend the base `Illuminate\Database\Events\MigrationEvent` class:

<div class="overflow-auto">

| Class                                            | Description                                      |
| ------------------------------------------------ | ------------------------------------------------ |
| `Illuminate\Database\Events\DatabaseRefreshed`   | The `migrate:refresh` command has finished.      |
| `Illuminate\Database\Events\MigrationsStarted`   | A batch of migrations is about to be executed.   |
| `Illuminate\Database\Events\MigrationsEnded`     | A batch of migrations has finished.              |
| `Illuminate\Database\Events\MigrationStarted`    | A single migration is about to be executed.      |
| `Illuminate\Database\Events\MigrationEnded`      | A single migration has finished.                 |
| `Illuminate\Database\Events\NoPendingMigrations` | A migration command found no pending migrations. |
| `Illuminate\Database\Events\SchemaDumped`        | A database schema dump has finished.             |
| `Illuminate\Database\Events\SchemaLoaded`        | An existing database schema dump has loaded.     |

</div>
{% endraw %}
