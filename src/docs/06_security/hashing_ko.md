---
layout: docs
title: "해싱"
---

{% raw %}
# 해싱

- [소개](#introduction)
- [컨피그레이션](#configuration)
- 기본 사용법 (#basic-usage)
- 해싱 비밀번호 (#hashing-passwords)
- 패스워드가 해시와 일치하는지 확인 (#verifying-that-a-password-matches-a-hash)
- [암호를 다시 해시해야 하는지 결정](#determining-if-a-password-needs-to-be-rehashed)
- [해시 알고리즘 확인](#hash-algorithm-verification)

<a name="introduction"></a>
## 소개

Laravel `Hash` [facade](/docs/{{version}}/facades) 는 사용자 암호를 저장하기 위한 안전한 Bcrypt 및 Argon2 해시를 제공합니다. [Laravel 애플리케이션 스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 사용하는 경우 기본적으로 Bcrypt 가 등록 및 인증에 사용됩니다。

Bcrypt 는 “작업 요소” 가 조정 가능하기 때문에 비밀번호 해싱에 좋은 선택입니다. 즉， 하드웨어 성능이 증가함에 따라 해시를 생성하는 데 걸리는 시간을 늘릴 수 있습니다. 비밀번호를 해시할 때는 느리게 하는 것이 좋습니다. 알고리즘이 비밀번호를 해시하는 데 걸리는 시간이 길수록， 악성 사용자가 애플리케이션에 대한 무차별 공격에 사용될 수 있는 모든 가능한 문자열 해시 값의 “무지개 테이블” 을 생성하는 데 걸리는

<a name="configuration"></a>
## 구성

기본적으로 Laravel 은 데이터를 해싱할 때 `bcrypt` 해싱 드라이버를 사용합니다. 그러나 [argon](https://en.wikipedia.org/wiki/Argon2) 및 [argon2id](https://en.wikipedia.org/wiki/Argon2) 를 포함한 다른 여러 해싱 드라이버가 지원됩니다。

`HASH_DRIVER` 환경 변수를 사용하여 애플리케이션의 해시 드라이버를 지정할 수 있습니다. 그러나 Laravel 의 모든 해시 드라이버 옵션을 사용자 지정하려면 `config:publish` Artisan 명령을 사용하여 전체 `hashing` 구성 파일을 게시해야 합니다：

```shell
php artisan config:publish hashing

```

<a name="basic-usage"></a>
## 기본 사용법

<a name="hashing-passwords"></a>
### 비밀번호 해싱

`Hash` 퍼사드에서 `make` 메서드를 호출하여 비밀번호를 해싱할 수 있습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    /**
     * Update the password for the user.
     */
    public function update(Request $request): RedirectResponse
    {
        // Validate the new password length...

        $request->user()->fill([
            'password' => Hash::make($request->newPassword)
        ])->save();

        return redirect('/profile');
    }
}

```

<a name="adjusting-the-bcrypt-work-factor"></a>
#### Bcrypt 작업 계수 조정

Bcrypt 알고리즘을 사용하는 경우, `make` 메서드를 사용하면 `rounds` 옵션을 통해 알고리즘의 작업 계수를 관리할 수 있습니다. 그러나 Laravel이 관리하는 기본 작업 계수도 대부분의 애플리케이션에는 적합합니다:

```php
$hashed = Hash::make('password', [
    'rounds' => 12,
]);

```

<a name="adjusting-the-argon2-work-factor"></a>
#### 아르곤2 작업 계수 조정

Argon2 알고리즘을 사용하는 경우, `make` 메서드를 통해 `memory`, `time` 및 `threads` 옵션을 사용하여 알고리즘의 작업 계수를 관리할 수 있습니다. 그러나 Laravel에서 관리하는 기본값은 대부분의 애플리케이션에 적합합니다:

```php
$hashed = Hash::make('password', [
    'memory' => 1024,
    'time' => 2,
    'threads' => 2,
]);

```

> [!NOTE]
> 이러한 옵션에 대한 자세한 내용은 [Argon 해싱에 관한 공식 PHP 문서](https://secure.php.net/manual/en/function.password-hash.php)를 참조하세요.

<a name="verifying-that-a-password-matches-a-hash"></a>
### 비밀번호가 해시와 일치하는지 확인하기

`check` 메서드는 `Hash` 퍼사드에서 제공하며, 주어진 일반 텍스트 문자열이 주어진 해시와 일치하는지 확인할 수 있습니다:

```php
if (Hash::check('plain-text', $hashedPassword)) {
    // The passwords match...
}

```

<a name="determining-if-a-password-needs-to-be-rehashed"></a>
### 비밀번호를 다시 해시해야 하는지 확인하기

`Hash` 퍼사드가 제공하는 `needsRehash` 메서드를 사용하면 비밀번호가 해시된 이후 해시기에서 사용된 작업 계수가 변경되었는지 확인할 수 있습니다. 일부 애플리케이션에서는 애플리케이션의 인증 과정 중에 이 확인을 수행하기로 선택합니다:

```php
if (Hash::needsRehash($hashed)) {
    $hashed = Hash::make('plain-text');
}

```

<a name="hash-algorithm-verification"></a>
## 해시 알고리즘 검증

해시 알고리즘 조작을 방지하기 위해, Laravel의 `Hash::check` 메서드는 먼저 주어진 해시가 애플리케이션에서 선택한 해싱 알고리즘을 사용하여 생성되었는지 검증합니다. 알고리즘이 다를 경우, `RuntimeException` 예외가 발생합니다.

대부분의 애플리케이션에서는 해싱 알고리즘이 변경되지 않는 것이 기대되며, 다른 알고리즘 사용은 악의적 공격의 신호일 수 있으므로 이는 예상 동작입니다. 그러나 애플리케이션에서 여러 해싱 알고리즘을 지원해야 하는 경우, 예를 들어 한 알고리즘에서 다른 알고리즘으로 마이그레이션할 때, `HASH_VERIFY` 환경 변수를 `false`로 설정하여 해시 알고리즘 검증을 비활성화할 수 있습니다.

```ini
HASH_VERIFY=false

```
{% endraw %}
