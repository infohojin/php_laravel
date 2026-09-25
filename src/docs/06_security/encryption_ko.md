---
layout: docs
title: "암호화"
---

{% raw %}
# 암호화

- [소개](#introduction)
- [컨피그레이션](#configuration)
- [우아하게 회전하는 암호화 키](#gracefully-rotating-encryption-keys)
- 암호화기 사용하기 (#using-the-encrypter)

<a name="introduction"></a>
## 소개

Laravel 의 암호화 서비스는 AES-256 및 AES-128 암호화를 사용하여 OpenSSL 을 통해 텍스트를 암호화하고 복호화하기 위한 간단하고 편리한 인터페이스를 제공합니다. Laravel 의 모든 암호화된 값은 MAC(메시지 인증 코드) 을 사용하여 서명되므로， 일단 암호화되면 기본 값을 수정하거나 변조할 수 없습니다。

<a name="configuration"></a>
## 구성

Laravel 의 암호화기를 사용하기 전에 `config/app.php` 구성 파일에서 `key` 구성 옵션을 설정해야 합니다. 이 구성 값은 `APP_KEY` 환경 변수에 의해 구동됩니다. `key:generate` 명령은 PHP 의 보안 무작위 바이트 생성기를 사용하여 애플리케이션에 대한 암호화적으로 안전한 키를 구축하므로 `php artisan key:generate` 명령을 사용하여 이 변수의 값을 생성해야 합니다. 일반적으로 `APP_KEY` 환경 변수의 값은 [Laravel 의 설치](/docs/{{version}}/installation) 중에 사용자를 위해 생성됩니다。

<a name="gracefully-rotating-encryption-keys"></a>
### 우아하게 회전하는 암호화 키

애플리케이션의 암호화 키를 변경하면 인증된 모든 사용자 세션이 애플리케이션에서 로그아웃됩니다. 이는 세션 쿠키를 포함한 모든 쿠키가 Laravel 에 의해 암호화되기 때문입니다. 또한 이전 암호화 키로 암호화된 데이터는 더 이상 복호화할 수 없습니다。

이 문제를 완화하기 위해 Laravel 을 사용하면 애플리케이션의 `APP_PREVIOUS_KEYS` 환경 변수에 이전 암호화 키를 나열할 수 있습니다. 이 변수에는 이전 모든 암호화 키의 쉼표로 구분된 목록이 포함될 수 있습니다：

```ini
APP_KEY="base64:J63qRTDLub5NuZvP+kb8YIorGS6qFYHKVo6u7179stY="
APP_PREVIOUS_KEYS="base64:2nLsGFGzyoae2ax3EF2Lyq/hH6QghBGLIq5uL+Gp8/w="

```

이 환경 변수를 설정하면, Laravel은 값을 암호화할 때 항상 "현재" 암호화 키를 사용합니다. 그러나 값을 복호화할 때, Laravel은 먼저 현재 키를 시도하고, 현재 키로 복호화가 실패하면, 이전의 모든 키를 순차적으로 시도하여 그 중 하나를 사용해 값을 복호화할 수 있습니다.

이러한 원활한 복호화 방식은 암호화 키가 변경되더라도 사용자가 애플리케이션을 중단 없이 계속 사용할 수 있도록 합니다.

<a name="using-the-encrypter"></a>
## Encrypter 사용하기

<a name="encrypting-a-value"></a>
#### 값 암호화하기

`encryptString` 메서드를 `Crypt` 파사드를 통해 사용하여 값을 암호화할 수 있습니다. 모든 암호화된 값은 OpenSSL과 AES-256-CBC 암호를 사용하여 암호화됩니다. 또한 모든 암호화된 값은 메시지 인증 코드(MAC)로 서명됩니다. 통합된 메시지 인증 코드는 악의적인 사용자가 변조한 값을 복호화하지 못하도록 방지합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Crypt;

class DigitalOceanTokenController extends Controller
{
    /**
     * Store a DigitalOcean API token for the user.
     */
    public function store(Request $request): RedirectResponse
    {
        $request->user()->fill([
            'token' => Crypt::encryptString($request->token),
        ])->save();

        return redirect('/secrets');
    }
}

```

<a name="decrypting-a-value"></a>
#### 값 복호화

`Crypt` 퍼사드가 제공하는 `decryptString` 방법을 사용하여 값을 복호화할 수 있습니다. 메시지 인증 코드가 잘못된 경우와 같이 값이 제대로 복호화될 수 없으면 `Illuminate\Contracts\Encryption\DecryptException`가 발생합니다:

```php
use Illuminate\Contracts\Encryption\DecryptException;
use Illuminate\Support\Facades\Crypt;

try {
    $decrypted = Crypt::decryptString($encryptedValue);
} catch (DecryptException $e) {
    // ...
}

```
{% endraw %}
