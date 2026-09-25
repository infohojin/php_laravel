---
layout: docs
title: "데이터베이스: 시딩"
---

{% raw %}
# 데이터베이스: 시딩

- [소개](#introduction)
- [시더 작성하기](#writing-seeders)
    - [모델 팩토리 사용](#using-model-factories)
    - [추가 시더 호출](#calling-additional-seeders)
    - [모델 이벤트 음소거](#muting-model-events)
- [시더 실행하기](#running-seeders)

<a name="introduction"></a>
## 소개

Laravel은 시드 클래스를 사용하여 데이터베이스를 데이터로 채우는 기능을 포함합니다. 모든 시드 클래스는 `database/seeders` 디렉터리에 저장됩니다. 기본적으로, `DatabaseSeeder` 클래스가 정의되어 있습니다. 이 클래스에서 다른 시드 클래스를 실행하기 위해 `call` 메서드를 사용할 수 있으며, 이를 통해 시딩 순서를 제어할 수 있습니다.

> [!NOTE]
> [대량 할당 보호](/docs/{{version}}/eloquent#mass-assignment)는 데이터베이스 시딩 중 자동으로 비활성화됩니다.

<a name="writing-seeders"></a>
## 시더 작성하기

시더를 생성하려면 `make:seeder` [아티즌 명령어](/docs/{{version}}/artisan)를 실행하세요. 프레임워크에서 생성된 모든 시더는 `database/seeders` 디렉터리에 배치됩니다:

```shell
php artisan make:seeder UserSeeder

```

시더 클래스는 기본적으로 하나의 메서드만 포함합니다: `run`. 이 메서드는 `db:seed` [Artisan 명령](/docs/{{version}}/artisan)이 실행될 때 호출됩니다. `run` 메서드 내에서는 데이터베이스에 데이터를 원하는 방식으로 삽입할 수 있습니다. 데이터를 수동으로 삽입하기 위해 [쿼리 빌더](/docs/{{version}}/queries)를 사용할 수도 있고, [Eloquent 모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용할 수도 있습니다.

예를 들어, 기본 `DatabaseSeeder` 클래스를 수정하고 `run` 메서드에 데이터베이스 삽입 구문을 추가해 보겠습니다:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        DB::table('users')->insert([
            'name' => Str::random(10),
            'email' => Str::random(10).'@example.com',
            'password' => Hash::make('password'),
        ]);
    }
}

```

> [!NOTE]
> `run` 메서드 시그니처 안에서 필요한 의존성을 타입 힌트로 지정할 수 있습니다. Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 해결됩니다.

<a name="using-model-factories"></a>
### 모델 팩토리 사용

물론, 각 모델 시드를 위해 속성을 수동으로 지정하는 것은 번거롭습니다. 대신 [모델 팩토리](/docs/{{version}}/eloquent-factories)를 사용하면 대량의 데이터베이스 레코드를 편리하게 생성할 수 있습니다. 먼저 [모델 팩토리 문서](/docs/{{version}}/eloquent-factories)를 검토하여 팩토리를 정의하는 방법을 배우십시오.

예를 들어, 각 사용자마다 하나의 관련 게시물을 가진 50명의 사용자를 생성해 보겠습니다:

```php
use App\Models\User;

/**
 * Run the database seeders.
 */
public function run(): void
{
    User::factory()
        ->count(50)
        ->hasPosts(1)
        ->create();
}

```

<a name="calling-additional-seeders"></a>
### 추가 시더 호출

`DatabaseSeeder` 클래스 내에서, `call` 메서드를 사용하여 추가 시더 클래스를 실행할 수 있습니다. `call` 메서드를 사용하면 데이터베이스 시딩을 여러 파일로 나누어 단일 시더 클래스가 너무 커지지 않도록 할 수 있습니다. `call` 메서드는 실행되어야 하는 시더 클래스 배열을 받아들입니다:

```php
/**
 * Run the database seeders.
 */
public function run(): void
{
    $this->call([
        UserSeeder::class,
        PostSeeder::class,
        CommentSeeder::class,
    ]);
}

```

<a name="muting-model-events"></a>
### 모델 이벤트 음소거

시드를 실행하는 동안 모델이 이벤트를 전송하지 못하게 하고 싶을 수 있습니다. 이는 `WithoutModelEvents` 트레이트를 사용하여 달성할 수 있습니다. 사용 시, `WithoutModelEvents` 트레이트는 `call` 메서드를 통해 추가 시드 클래스가 실행되더라도 모델 이벤트가 전송되지 않도록 보장합니다:

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;

class DatabaseSeeder extends Seeder
{
    use WithoutModelEvents;

    /**
     * Run the database seeders.
     */
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
        ]);
    }
}

```

<a name="running-seeders"></a>
## 시더 실행하기

데이터베이스를 시드하기 위해 `db:seed` Artisan 명령어를 실행할 수 있습니다. 기본적으로 `db:seed` 명령어는 `Database\Seeders\DatabaseSeeder` 클래스를 실행하며, 이 클래스는 다른 시더 클래스를 호출할 수 있습니다. 그러나 특정 시더 클래스를 개별적으로 실행하려면 `--class` 옵션을 사용할 수 있습니다:

```shell
php artisan db:seed

php artisan db:seed --class=UserSeeder

```

또한 `--seed` 옵션과 함께 `migrate:fresh` 명령을 사용하여 데이터베이스를 시드할 수 있으며, 이 명령은 모든 테이블을 삭제하고 모든 마이그레이션을 다시 실행합니다. 이 명령은 데이터베이스를 완전히 재구성할 때 유용합니다. `--seeder` 옵션은 실행할 특정 시더를 지정하는 데 사용할 수 있습니다:

```shell
php artisan migrate:fresh --seed

php artisan migrate:fresh --seed --seeder=UserSeeder

```

<a name="forcing-seeding-production"></a>
#### 프로덕션에서 시더 실행 강제하기

일부 시딩 작업은 데이터를 변경하거나 손실시킬 수 있습니다. 프로덕션 데이터베이스에서 시딩 명령을 실행하는 것을 방지하기 위해, `production` 환경에서 시더가 실행되기 전에 확인을 요청받게 됩니다. 확인 없이 시더를 실행하도록 강제하려면 `--force` 플래그를 사용하세요:

```shell
php artisan db:seed --force

```
{% endraw %}
