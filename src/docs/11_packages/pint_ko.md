---
layout: docs
title: "라라벨 핀트"
---

{% raw %}
# 라라벨 핀트

- [인트로듀션](#introduction)
- [설치](#installation)
- [Running Pint](#running-pint)
- 구성 핀트 (#configuring-pint)
- [프리셋](#presets)
- [규칙](#rules)
- [파일/폴더 제외](#excluding-files-or-folders)
- 지속적 통합 (#continuous-integration)
- [GitHub Actions](#running-tests-on-github-actions)

<a name="introduction"></a>
## 소개

[Laravel Pint](https://github.com/laravel/pint) 는 미니멀리스트를 위한 고집스러운 PHP 코드 스타일 수정기입니다. Pint 는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer) 위에 구축되어 코드 스타일이 깨끗하고 일관되게 유지되도록 간소화합니다。

Pint 는 모든 새로운 Laravel 애플리케이션과 함께 자동으로 설치되므로 즉시 사용을 시작할 수 있습니다. 기본적으로 Pint 는 어떤 구성도 필요하지 않으며 Laravel 의 독단적인 코딩 스타일을 따라 코드의 코드 스타일 문제를 해결합니다。

<a name="installation"></a>
## 설치

Pint 는 Laravel 프레임워크의 최근 릴리스에 포함되어 있으므로 일반적으로 설치가 필요하지 않습니다. 그러나 이전 애플리케이션의 경우 Composer 를 통해 Laravel Pint 를 설치할 수 있습니다：

```shell
composer require laravel/pint --dev

```

<a name="running-pint"></a>
## Pint 실행하기

프로젝트의 `vendor/bin` 디렉터리에 있는 `pint` 바이너리를 호출하여 Pint에게 코드 스타일 문제를 수정하도록 지시할 수 있습니다:

```shell
./vendor/bin/pint

```

성능 향상을 위해 Pint를 병렬 모드(실험적)로 실행하고 싶다면 `--parallel` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --parallel

```

병렬 모드는 또한 `--max-processes` 옵션을 통해 실행할 최대 프로세스 수를 지정할 수 있습니다. 이 옵션이 제공되지 않으면 Pint는 머신의 사용 가능한 모든 코어를 사용합니다:

```shell
./vendor/bin/pint --parallel --max-processes=4

```

특정 파일이나 디렉토리에서 Pint를 실행할 수도 있습니다:

```shell
./vendor/bin/pint app/Models

./vendor/bin/pint app/Models/User.php

```

기본적으로 Pint는 Blade 템플릿을 포맷하지 않습니다. `.blade.php` 파일도 포맷하려는 경우, 현재 실행에서 `pint.json` 파일을 수정하지 않고 [`Pint/laravel_blade`](#laravel-blade) 규칙을 활성화하는 `--blade` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --blade

```

Pint은 업데이트하는 모든 파일의 상세 목록을 표시합니다. Pint를 호출할 때 `-v` 옵션을 제공하면 Pint의 변경 사항에 대한 더 많은 세부 정보를 확인할 수 있습니다:

```shell
./vendor/bin/pint -v

```

Pint이 실제로 파일을 변경하지 않고 코드 스타일 오류만 검사하도록 하려면 `--test` 옵션을 사용할 수 있습니다. 코드 스타일 오류가 발견되면 Pint는 0이 아닌 종료 코드를 반환합니다:

```shell
./vendor/bin/pint --test

```

Git에 따라 제공된 브랜치와 다른 파일만 Pint가 수정하도록 하려면 `--diff=[branch]` 옵션을 사용할 수 있습니다. 이는 새로운 파일이나 수정된 파일만 검사하여 시간을 절약할 수 있으므로 CI 환경(예: GitHub Actions)에서 효과적으로 사용할 수 있습니다:

```shell
./vendor/bin/pint --diff=main

```

Git에 따라 커밋되지 않은 변경 사항이 있는 파일만 Pint가 수정하도록 하려면 `--dirty` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --dirty

```

코드 스타일 오류가 있는 파일을 Pint가 수정하도록 하면서, 수정된 오류가 있을 경우 비영(zero가 아닌) 종료 코드를 반환하게 하고 싶다면, `--repair` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --repair

```

<a name="configuring-pint"></a>
## Pint 설정

앞서 언급했듯이, Pint는 별도의 설정이 필요하지 않습니다. 그러나 프리셋, 규칙 또는 검사할 폴더를 사용자 정의하려면 프로젝트의 루트 디렉터리에 `pint.json` 파일을 생성하면 됩니다:

```json
{
    "preset": "laravel"
}

```

또한 특정 디렉터리에서 `pint.json`를 사용하려는 경우, Pint를 호출할 때 `--config` 옵션을 제공할 수 있습니다:

```shell
./vendor/bin/pint --config vendor/my-company/coding-style/pint.json

```

<a name="presets"></a>
### 프리셋

프리셋은 코드의 스타일 문제를 해결하는 데 사용할 수 있는 규칙 집합을 정의합니다. 기본적으로 Pint는 `laravel` 프리셋을 사용하며, 이는 Laravel의 의견이 반영된 코딩 스타일을 따라 문제를 해결합니다. 그러나 Pint에 `--preset` 옵션을 제공하여 다른 프리셋을 지정할 수도 있습니다:

```shell
./vendor/bin/pint --preset psr12

```

원하신다면, 프로젝트의 `pint.json` 파일에서 프리셋을 설정할 수도 있습니다:

```json
{
    "preset": "psr12"
}

```

Pint가 현재 지원하는 프리셋은 다음과 같습니다: `laravel`, `per`, `psr12`, `symfony`, 그리고 `empty`.

<a name="rules"></a>
### 규칙

규칙은 Pint가 코드 스타일 문제를 수정할 때 사용할 스타일 지침입니다. 위에서 언급했듯이, 프리셋은 대부분의 PHP 프로젝트에 적합하도록 미리 정의된 규칙 그룹이므로 일반적으로 포함된 개별 규칙에 대해 신경 쓸 필요가 없습니다.

하지만 원하신다면, `pint.json` 파일에서 특정 규칙을 활성화하거나 비활성화할 수 있으며, `empty` 프리셋을 사용하고 규칙을 처음부터 정의할 수도 있습니다:

```json
{
    "preset": "laravel",
    "rules": {
        "simplified_null_return": true,
        "array_indentation": false,
        "new_with_parentheses": {
            "anonymous_class": true,
            "named_class": true
        }
    }
}

```

Pint는 [PHP CS Fixer](https://github.com/FriendsOfPHP/PHP-CS-Fixer)를 기반으로 구축되었습니다. 따라서 프로젝트의 코드 스타일 문제를 수정하기 위해 PHP CS Fixer의 규칙을 사용할 수 있습니다: [PHP CS Fixer Configurator](https://mlocati.github.io/php-cs-fixer-configurator).

<a name="custom-rules"></a>
#### 사용자 정의 규칙

PHP CS Fixer 규칙 외에도, Pint는 `Pint/` 접두사가 붙은 사용자 정의 규칙을 제공합니다. 이러한 규칙은 기본적으로 활성화되어 있지 않지만, `pint.json` 파일에서 활성화할 수 있습니다.

<a name="laravel-blade"></a>
##### `Pint/laravel_blade`

이 규칙은 Blade 템플릿을 포맷하여 `.blade.php` 파일에 일관된 들여쓰기, 공백 및 속성 포맷팅을 적용합니다. 기본적으로 Pint는 Blade 파일을 포맷하지 않으므로, 이 규칙을 적용하려면 `pint.json` 파일에서 활성화해야 합니다.

```json
{
    "preset": "laravel",
    "rules": {
        "Pint/laravel_blade": true
    }
}

```

활성화되면 Pint는 실행될 때마다 PHP 파일뿐만 아니라 Blade 템플릿도 포맷합니다:

```shell
./vendor/bin/pint

```

또는 `pint.json` 파일을 수정하지 않고 단일 실행에 대해 이 규칙을 활성화하려면 `--blade` 옵션을 사용할 수 있습니다:

```shell
./vendor/bin/pint --blade

```

이 규칙은 내부적으로 [Prettier](https://prettier.io)와 함께 `prettier-plugin-blade` 및 `prettier-plugin-tailwindcss` 플러그인을 사용하므로, [Node.js](https://nodejs.org)가 귀하의 컴퓨터에 설치되어 있어야 합니다. 이 규칙이 활성화된 상태에서 처음으로 Pint를 실행하면, Pint는 누락된 Prettier 의존성을 감지하고 설치하라는 메시지를 표시합니다.

> [!NOTE]
> 이 규칙은 일반적으로 자체 포맷팅을 사용하는 파일, 예를 들어 [Laravel Boost](https://github.com/laravel/boost) 지침과 `resources/views/emails` 및 `resources/views/mail` 디렉토리에 위치한 이메일 뷰를 자동으로 건너뜁니다.

<a name="phpdoc-type-annotations-only"></a>
##### `Pint/phpdoc_type_annotations_only`

이 규칙은 코드에서 모든 주석과 문서 블록 글을 제거하고, `@param`, `@return`, `@var`, `@phpstan-type` 등과 같은 `@` 주석이 포함된 줄만 유지합니다:

```php
/**
 * Get the posts for the user. [tl! remove]
 * [tl! remove]
 * @return HasMany<Post, $this>
 */
public function posts(): HasMany

```



`@` 주석이 없는 한 줄 주석과 블록 주석은 완전히 제거됩니다. 특정 주석을 유지하려면 `@note`, `@warning` 또는 `@todo`로 접두사를 붙일 수 있습니다:

```php
// @note This comment will be preserved.

```

이 규칙을 활성화하려면 `pint.json` 파일에 추가하세요:

```json
{
    "preset": "laravel",
    "rules": {
        "Pint/phpdoc_type_annotations_only": true
    }
}

```

> [!NOTE]
> 이 규칙은 `config` 디렉토리의 파일을 자동으로 건너뜁니다. 구성 파일은 일반적으로 문서화를 위해 주석에 의존하기 때문입니다.

<a name="excluding-files-or-folders"></a>
### 파일 / 폴더 제외하기

기본적으로 Pint는 `vendor` 디렉토리에 있는 파일을 제외하고 프로젝트의 모든 `.php` 파일을 검사합니다. 더 많은 폴더를 제외하려면 `exclude` 구성 옵션을 사용하면 됩니다:

```json
{
    "exclude": [
        "my-specific/folder"
    ]
}

```

주어진 이름 패턴을 포함하는 모든 파일을 제외하려면 `notName` 구성 옵션을 사용하여 그렇게 할 수 있습니다:

```json
{
    "notName": [
        "*-my-file.php"
    ]
}

```

파일의 정확한 경로를 제공하여 파일을 제외하려는 경우, `notPath` 구성 옵션을 사용하여 그렇게 할 수 있습니다:

```json
{
    "notPath": [
        "path/to/excluded-file.php"
    ]
}

```

<a name="continuous-integration"></a>
## 지속적 통합

<a name="running-tests-on-github-actions"></a>
### GitHub 액션

Laravel Pint로 프로젝트의 린팅을 자동화하려면, 새로운 코드가 GitHub에 푸시될 때 Pint를 실행하도록 [GitHub Actions](https://github.com/features/actions)를 설정할 수 있습니다. 먼저, GitHub에서 **설정 > 액션 > 일반 > 워크플로 권한**으로 이동하여 워크플로에 "읽기 및 쓰기 권한"을 부여했는지 확인하세요. 그런 다음, 다음 내용을 가진 `.github/workflows/lint.yml` 파일을 생성합니다:

```yaml
name: Fix Code Style

on: [push]

jobs:
  lint:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: true
      matrix:
        php: [8.4]

    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: ${{ matrix.php }}
          tools: pint

      - name: Run Pint
        run: pint

      - name: Commit linted files
        uses: stefanzweifel/git-auto-commit-action@v6

```
{% endraw %}
