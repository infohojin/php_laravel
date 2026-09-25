---
layout: docs
title: "현지화"
---

{% raw %}
# 현지화

- [소개](#introduction)
- [언어 파일 발행](#publishing-the-language-files)
- 컨피그레이션 더 로컬 (#configuring-the-locale)
- [복수화 언어](#pluralization-language)
- 번역 문자열 정의 (#defining-translation-strings)
- 짧은 키 사용 (#using-short-keys)
- 번역 문자열을 키로 사용하기 (#using-translation-strings-as-keys)
- [번역 문자열 검색](#retrieving-translation-strings)
- [번역 문자열의 매개변수 대체](#replacing-parameters-in-translation-strings)
- [복수화](#pluralization)
- [오버라이딩 패키지 언어 파일](#overriding-package-language-files)

<a name="introduction"></a>
## 소개

> [!NOTE]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel 의 언어 파일을 사용자 지정하려면 `lang:publish` Artisan 명령을 통해 게시할 수 있습니다。

Laravel 의 현지화 기능은 다양한 언어로 문자열을 검색하는 편리한 방법을 제공하므로， 애플리케이션 내에서 여러 언어를 쉽게 지원할 수 있습니다。

Laravel 은 번역 문자열을 관리하는 두 가지 방법을 제공합니다. 첫째， 언어 문자열은 애플리케이션의 `lang` 디렉토리 내의 파일에 저장될 수 있습니다. 이 디렉토리 내에는 애플리케이션이 지원하는 각 언어에 대한 하위 디렉토리가 있을 수 있습니다. 이는 Laravel 이 검증 오류 메시지와 같은 내장된 Laravel 기능에 대한 번역 문자열을 관리할 때 사용하는 접근 방식입니

```text
/lang
    /en
        messages.php
    /es
        messages.php

```

또는 번역 문자열이 `lang` 디렉토리에 배치된 JSON 파일 내에 정의될 수 있습니다. 이 접근 방식을 사용할 때, 애플리케이션이 지원하는 각 언어는 이 디렉토리 내에 해당 JSON 파일을 가지게 됩니다. 이 접근 방식은 번역할 문자열이 많은 애플리케이션에 권장됩니다:

```text
/lang
    en.json
    es.json

```

우리는 이 문서 내에서 번역 문자열을 관리하는 각 접근 방식을 논의할 것입니다.

<a name="publishing-the-language-files"></a>
### 언어 파일 게시

기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하거나 직접 만들고자 한다면, `lang:publish` Artisan 명령어를 통해 `lang` 디렉터리를 스캐폴딩해야 합니다. `lang:publish` 명령어는 애플리케이션 내에 `lang` 디렉터리를 생성하고 Laravel에서 사용하는 기본 언어 파일 세트를 게시할 것입니다:

```shell
php artisan lang:publish

```

<a name="configuring-the-locale"></a>
### 로케일 설정

애플리케이션의 기본 언어는 `config/app.php` 구성 파일의 `locale` 구성 옵션에 저장되어 있으며, 일반적으로 `APP_LOCALE` 환경 변수를 사용하여 설정됩니다. 애플리케이션의 필요에 맞게 이 값을 자유롭게 수정할 수 있습니다.

기본 언어에 해당 번역 문자열이 없는 경우 사용될 "대체 언어(fallback language)"도 설정할 수 있습니다. 기본 언어와 마찬가지로, 대체 언어는 `config/app.php` 구성 파일에서 설정되며, 값은 일반적으로 `APP_FALLBACK_LOCALE` 환경 변수를 사용하여 설정됩니다.

`App` 퍼사드가 제공하는 `setLocale` 메서드를 사용하여 단일 HTTP 요청에 대한 기본 언어를 런타임에 수정할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

Route::get('/greeting/{locale}', function (string $locale) {
    if (! in_array($locale, ['en', 'es', 'fr'])) {
        abort(400);
    }

    App::setLocale($locale);

    // ...
});

```

<a name="determining-the-current-locale"></a>
#### 현재 로케일 결정

현재 로케일을 결정하거나 로케일이 주어진 값인지 확인하려면 `App` 페이사드에서 `currentLocale` 및 `isLocale` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\App;

$locale = App::currentLocale();

if (App::isLocale('en')) {
    // ...
}

```

<a name="pluralization-language"></a>
### 복수형 언어

<style>
.code-list-no-flex-break code {
    display: contents !important;
}
</style>

<div class="code-list-no-flex-break">

Laravel의 "pluralizer"는 Eloquent 및 프레임워크의 다른 부분에서 단수 문자열을 복수 문자열로 변환할 때 사용되며, 영어가 아닌 다른 언어를 사용하도록 지시할 수 있습니다. 이는 애플리케이션 서비스 제공자의 `boot` 메서드 내에서 `useLanguage` 메서드를 호출하여 수행할 수 있습니다. 현재 pluralizer에서 지원하는 언어는 다음과 같습니다: `french`, `norwegian-bokmal`, `portuguese`, `spanish` 및 `turkish`:

</div>

```php
use Illuminate\Support\Pluralizer;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Pluralizer::useLanguage('spanish');

    // ...
}

```

> [!WARNING]
> 만약 복수형 변환기의 언어를 사용자 정의한다면, Eloquent 모델의 [테이블 이름](/docs/{{version}}/eloquent#table-names)을 명시적으로 정의해야 합니다.

<a name="defining-translation-strings"></a>
## 번역 문자열 정의하기

<a name="using-short-keys"></a>
### 짧은 키 사용하기

일반적으로 번역 문자열은 `lang` 디렉토리 내의 파일에 저장됩니다. 이 디렉토리 안에는 애플리케이션에서 지원하는 각 언어별 하위 디렉토리가 있어야 합니다. 이것이 Laravel이 유효성 검사 오류 메시지와 같은 내장 Laravel 기능의 번역 문자열을 관리하는 방식입니다:

```text
/lang
    /en
        messages.php
    /es
        messages.php

```

모든 언어 파일은 키가 지정된 문자열의 배열을 반환합니다. 예를 들어:

```php
<?php

// lang/en/messages.php

return [
    'welcome' => 'Welcome to our application!',
];

```

> [!WARNING]
> 영역별로 다른 언어의 경우, 언어 디렉토리 이름은 ISO 15897에 따라 지정해야 합니다. 예를 들어 영국 영어에는 "en-gb" 대신 "en_GB"를 사용해야 합니다.

<a name="using-translation-strings-as-keys"></a>
### 번역 문자열을 키로 사용하기

번역할 문자열이 많은 애플리케이션에서는 모든 문자열을 "짧은 키"로 정의하면 뷰에서 키를 참조할 때 혼란스러울 수 있으며, 애플리케이션에서 지원하는 모든 번역 문자열에 대해 지속적으로 키를 만들어야 하는 번거로움이 있습니다.

이러한 이유로 Laravel은 문자열의 "기본" 번역을 키로 사용하여 번역 문자열을 정의할 수 있는 기능도 제공합니다. 번역 문자열을 키로 사용하는 언어 파일은 `lang` 디렉토리에 JSON 파일로 저장됩니다. 예를 들어 애플리케이션에 스페인어 번역이 있는 경우, `lang/es.json` 파일을 만들어야 합니다:

```json
{
    "I love programming.": "Me encanta programar."
}

```

#### 키 / 파일 충돌

다른 번역 파일 이름과 충돌하는 번역 문자열 키를 정의하지 마십시오. 예를 들어, `nl/action.php` 파일이 존재하지만 `nl.json` 파일이 존재하지 않는 경우에 "NL" 로케일에 대해 `__('Action')`를 번역하면, 번역기는 `nl/action.php`의 전체 내용을 반환하게 됩니다.

<a name="retrieving-translation-strings"></a>
## 번역 문자열 가져오기

`__` 헬퍼 함수를 사용하여 언어 파일에서 번역 문자열을 가져올 수 있습니다. 번역 문자열을 정의할 때 "짧은 키"를 사용하는 경우, `__` 함수에 키가 포함된 파일과 키 자체를 "dot" 구문을 사용하여 전달해야 합니다. 예를 들어, `lang/en/messages.php` 언어 파일에서 `welcome` 번역 문자열을 가져오겠습니다:

```php
echo __('messages.welcome');

```

지정된 번역 문자열이 존재하지 않는 경우, `__` 함수는 번역 문자열 키를 반환합니다. 따라서 위의 예를 사용하면, 번역 문자열이 존재하지 않는 경우 `__` 함수는 `messages.welcome`를 반환합니다.

[기본 번역 문자열을 번역 키로 사용하는 경우](#using-translation-strings-as-keys), 문자열의 기본 번역을 `__` 함수에 전달해야 합니다;

```php
echo __('I love programming.');

```

다시 말하지만, 번역 문자열이 존재하지 않는 경우, `__` 함수는 제공된 번역 문자열 키를 반환합니다.

[Blade 템플릿 엔진](/docs/{{version}}/blade)을 사용하는 경우, `{{ }}` 에코 구문을 사용하여 번역 문자열을 표시할 수 있습니다:

```blade
{{ __('messages.welcome') }}

```

<a name="replacing-parameters-in-translation-strings"></a>
### 번역 문자열에서 매개변수 교체하기

원하면 번역 문자열에 자리 표시자를 정의할 수 있습니다. 모든 자리 표시자는 `:`로 시작합니다. 예를 들어, 자리 표시자 이름이 포함된 환영 메시지를 정의할 수 있습니다:

```php
'welcome' => 'Welcome, :name',

```

번역 문자열을 가져올 때 자리 표시자를 교체하려면 `__` 함수의 두 번째 인수로 교체 배열을 전달할 수 있습니다:

```php
echo __('messages.welcome', ['name' => 'dayle']);

```

플레이스홀더가 모두 대문자로 되어 있거나, 첫 글자만 대문자일 경우, 번역된 값도 이에 맞춰 대문자로 표시됩니다:

```php
'welcome' => 'Welcome, :NAME', // Welcome, DAYLE
'goodbye' => 'Goodbye, :Name', // Goodbye, Dayle

```

<a name="object-replacement-formatting"></a>
#### 객체 대체 포맷팅

번역 자리 표시자로 객체를 제공하려고 시도하면, 객체의 `__toString` 메서드가 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 그러나 때때로, 예를 들어 상호작용 중인 클래스가 서드파티 라이브러리에 속하는 경우와 같이 주어진 클래스의 `__toString` 메서드를 제어할 수 없을 때가 있습니다.

이러한 경우, Laravel은 해당 유형의 객체에 대한 사용자 정의 포맷팅 핸들러를 등록할 수 있게 해줍니다. 이를 수행하기 위해 번역기의 `stringable` 메서드를 호출해야 합니다. `stringable` 메서드는 클로저를 허용하며, 이 클로저는 포맷팅을 담당하는 객체의 유형을 타입 힌트로 지정해야 합니다. 일반적으로 `stringable` 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출되어야 합니다.

```php
use Illuminate\Support\Facades\Lang;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Lang::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}

```

<a name="pluralization"></a>
### 복수형

복수형은 복잡한 문제입니다. 언어마다 복수형에 대한 다양한 복잡한 규칙이 있지만, Laravel은 사용자가 정의한 복수형 규칙에 따라 문자열을 다르게 번역하는 데 도움을 줄 수 있습니다. `|` 문자를 사용하여 문자열의 단수형과 복수형을 구분할 수 있습니다:

```php
'apples' => 'There is one apple|There are many apples',

```

물론, [번역 문자열을 키로 사용할 때](#using-translation-strings-as-keys) 복수형도 지원됩니다:

```json
{
    "There is one apple|There are many apples": "Hay una manzana|Hay muchas manzanas"
}

```

여러 값의 범위에 대한 번역 문자열을 지정하는 더 복잡한 복수형 규칙을 만들 수도 있습니다:

```php
'apples' => '{0} There are none|[1,19] There are some|[20,*] There are many',

```

복수형 옵션이 있는 번역 문자열을 정의한 후에는 `trans_choice` 함수를 사용하여 주어진 "count"에 대한 줄을 가져올 수 있습니다. 이 예제에서는 count가 1보다 크므로 번역 문자열의 복수형이 반환됩니다:

```php
echo trans_choice('messages.apples', 10);

```

복수화 문자열에서도 플레이스홀더 속성을 정의할 수 있습니다. 이러한 플레이스홀더는 배열을 `trans_choice` 함수의 세 번째 인수로 전달하여 대체할 수 있습니다:

```php
'minutes_ago' => '{1} :value minute ago|[2,*] :value minutes ago',

echo trans_choice('time.minutes_ago', 5, ['value' => 5]);

```



`trans_choice` 함수에 전달된 정수 값을 표시하고 싶다면, 내장 `:count` 자리 표시자를 사용할 수 있습니다:

```php
'apples' => '{0} There are none|{1} There is one|[2,*] There are :count',

```

<a name="overriding-package-language-files"></a>
## 패키지 언어 파일 재정의

일부 패키지는 자체 언어 파일과 함께 제공될 수 있습니다. 이러한 문구를 수정하기 위해 패키지의 핵심 파일을 변경하는 대신, `lang/vendor/{package}/{locale}` 디렉터리에 파일을 배치하여 재정의할 수 있습니다.

예를 들어, `skyrim/hearthfire`라는 패키지의 `messages.php`에서 영어 번역 문자열을 재정의해야 하는 경우, 언어 파일을 다음 위치에 배치해야 합니다: `lang/vendor/hearthfire/en/messages.php`. 이 파일 내에서는 재정의하려는 번역 문자열만 정의해야 합니다. 재정의하지 않은 번역 문자열은 패키지의 원래 언어 파일에서 계속 로드됩니다.
{% endraw %}
