---
layout: docs
title: "패키지 개발"
---

{% raw %}
# 패키지 개발

- [소개](#introduction)
- [패키지 만들기](#creating-a-package)
- A Note on Facades (#a-note-on-facades)
- [패키지 발견](#package-discovery)
- 서비스 제공자 (#service-providers)
- [리소스](#resources)
- [구성](#configuration)
- Routes(#routes)
- [이주](#migrations)
- 언어 파일 (#language-files)
- [뷰](#views)
- [View Components](#view-components)
- “About” Artisan Command(#about-artisan-command)
- [명령](#commands)
- [최적화 명령](#optimize-commands)
- [재로드 명령](#reload-commands)
- Public Assets(#public-assets)
- [출판 파일 그룹](#publishing-file-groups)

<a name="introduction"></a>
## 소개

패키지는 Laravel 에 기능을 추가하는 주요 방법입니다. 패키지는 [Carbon](https://github.com/briannesbitt/Carbon) 과 같은 날짜로 작업하는 훌륭한 방법에서부터 Spatie’s [Laravel Media Library](https://github.com/spatie/laravel-medialibrary) 와 같은 Eloquent 모델과 파일을 연결할 수 있는 패키지에 이르기까지 모든 것이 될 수 있습니다。

다양한 유형의 패키지가 있습니다. 일부 패키지는 독립형으로， 즉 모든 PHP 프레임워크와 작동합니다. Carbon 과 Pest 가 독립형 패키지의 예입니다. 이러한 패키지 중 하나는 `composer.json` 파일에서 요구함으로써 Laravel 에서 사용할 수 있습니다。

반면， 다른 패키지는 Laravel 과 함께 사용하도록 특별히 설계되었습니다. 이러한 패키지에는 Laravel 애플리케이션을 향상시키도록 특별히 설계된 경로， 컨트롤러， 보기 및 구성이 있을 수 있습니다. 이 가이드는 주로 Laravel 에 특화된 패키지의 개발을 다룹니다。

<a name="creating-a-package"></a>
### 패키지 생성

새로운 Laravel 패키지 구축을 시작하는 가장 쉬운 방법은 공식 [Laravel 패키지 스켈레톤](https://github.com/laravel/package-skeleton) 입니다. 스켈레톤은 Laravel 패키지 구축에 필요한 모든 것을 제공합니다. 여기에는 서비스 제공자， Pest 를 통한 테스트， Larastan 을 통한 정적 분석， Pint 를 통한 코드 형식 지정 및 엔드 투 엔드 패키지 개발을 위한 워크벤치 애플리케이션이 포함됩니다. [Laravel 설치기 CLI](/docs/{{version}}/installation#creating-a-laravel-project) 의 `package` 명령을 사용하여 새 패키지를 생성할 수 있습니다：

```shell
laravel package my-package

```

대화형 구성 스크립트는 패키지의 스켈레톤을 개인화하여 네임스페이스， 서비스 제공자 및 구성 파일， 경로， 보기， 번역， 마이그레이션， 자산， 명령 및 패싯과 같은 필요한 기능만 설정합니다。

<a name="a-note-on-facades"></a>
### 외관에 대한 메모

Laravel 애플리케이션을 작성할 때는 일반적으로 계약이나 패시드를 사용하는지 여부가 중요하지 않습니다. 둘 다 기본적으로 동일한 수준의 테스트 가능성을 제공하기 때문입니다. 그러나 패키지를 작성할 때， 패키지는 일반적으로 Laravel 의 모든 테스트 도우미에 액세스할 수 없습니다. 일반적인 Laravel 애플리케이션 내에 패키지가 설치된 것처럼 패키지 테스트를 작성할 수 있으려면 [Orchestral Testbench](https://github.com/orchestral/testbench) 패키지를 사용할 수 있습니다。

<a name="package-discovery"></a>
## 패키지 발견

Laravel 애플리케이션의 `bootstrap/providers.php` 파일에는 Laravel 에서 로드해야 하는 서비스 제공자 목록이 포함되어 있습니다. 그러나 사용자가 서비스 제공자를 목록에 수동으로 추가하도록 요구하는 대신， 패키지의 `composer.json` 파일의 `extra` 섹션에서 제공자를 정의하여 Laravel 에서 자동으로 로드되도록 할 수 있습니다. 서비스 제공자 외에도 등록하려는 모든 [facades](/docs/{{version}}/facades) 을 나열할 수도 있습니다：

```json
"extra": {
    "laravel": {
        "providers": [
            "Barryvdh\\Debugbar\\ServiceProvider"
        ],
        "aliases": {
            "Debugbar": "Barryvdh\\Debugbar\\Facade"
        }
    }
},

```

패키지가 자동 탐색을 위해 구성되면, Laravel은 설치 시 해당 패키지의 서비스 제공자와 파사드를 자동으로 등록하여 패키지 사용자를 위한 편리한 설치 경험을 제공합니다.

<a name="opting-out-of-package-discovery"></a>
#### 패키지 탐색을 비활성화하기

패키지 사용자인 경우 특정 패키지의 탐색을 비활성화하고 싶다면, 애플리케이션의 `composer.json` 파일의 `extra` 섹션에 패키지 이름을 나열하면 됩니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "barryvdh/laravel-debugbar"
        ]
    }
},

```

애플리케이션의 `dont-discover` 지시문 안에서 `*` 문자를 사용하여 모든 패키지에 대한 패키지 검색을 비활성화할 수 있습니다:

```json
"extra": {
    "laravel": {
        "dont-discover": [
            "*"
        ]
    }
},

```

<a name="service-providers"></a>
## 서비스 제공업체

[서비스 제공자](/docs/{{version}}/providers) 는 패키지와 Laravel 간의 연결 지점입니다. 서비스 제공자는 Laravel 의 [서비스 컨테이너](/docs/{{version}}/container) 에 항목을 바인딩하고 뷰， 구성 및 언어 파일과 같은 패키지 리소스를 로드할 위치를 Laravel 에 알리는 역할을 합니다。

서비스 제공자는 `Illuminate\Support\ServiceProvider` 클래스를 확장하고 `register` 및 `boot` 라는 두 가지 메서드를 포함합니다. 기본 `ServiceProvider` 클래스는 `illuminate/support` Composer 패키지에 있으며， 이를 자체 패키지의 종속성에 추가해야 합니다. 서비스 제공자의 구조와 목적에 대해 자세히 알아보려면 [그들의 문서](/docs/{{version}}/providers) 를 확인하십시오。

<a name="resources"></a>
## 리소스

<a name="configuration"></a>
### 구성

일반적으로 패키지의 구성 파일을 애플리케이션의 `config` 디렉토리에 게시해야 합니다. 이를 통해 패키지의 사용자가 기본 구성 옵션을 쉽게 재정의할 수 있습니다. 구성 파일을 게시하려면 서비스 제공자의 `boot` 메서드에서 `publishes` 메서드를 호출합니다：

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/courier.php' => config_path('courier.php'),
    ]);
}

```

이제 패키지 사용자가 Laravel의 `vendor:publish` 명령을 실행하면, 귀하의 파일이 지정된 배포 위치로 복사됩니다. 구성 파일이 배포되면 그 값은 다른 구성 파일과 같이 접근할 수 있습니다:

```php
$value = config('courier.option');

```

> [!WARNING]
> 구성 파일에서 클로저를 정의해서는 안 됩니다. 사용자가 `config:cache` Artisan 명령을 실행할 때 올바르게 직렬화될 수 없습니다.

<a name="default-package-configuration"></a>
#### 기본 패키지 구성

자신의 패키지 구성 파일을 애플리케이션에서 게시된 사본과 병합할 수도 있습니다. 이렇게 하면 사용자가 구성 파일에서 실제로 재정의하려는 옵션만 정의할 수 있습니다. 구성 파일 값을 병합하려면 서비스 제공자의 `register` 메서드 내에서 `mergeConfigFrom` 메서드를 사용하십시오.

`mergeConfigFrom` 메서드는 첫 번째 인수로 패키지 구성 파일의 경로를, 두 번째 인수로 애플리케이션 구성 파일 사본의 이름을 받습니다:

```php
/**
 * Register any package services.
 */
public function register(): void
{
    $this->mergeConfigFrom(
        __DIR__.'/../config/courier.php', 'courier'
    );
}

```

> [!WARNING]
> 이 메서드는 구성 배열의 첫 번째 수준만 병합합니다. 사용자가 다차원 구성 배열을 부분적으로 정의한 경우, 누락된 옵션은 병합되지 않습니다.

<a name="routes"></a>
### 라우트

패키지에 라우트가 포함된 경우, `loadRoutesFrom` 메서드를 사용하여 이를 불러올 수 있습니다. 이 메서드는 애플리케이션의 라우트가 캐시되었는지 자동으로 판단하며, 라우트가 이미 캐시된 경우 라우트 파일을 불러오지 않습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadRoutesFrom(__DIR__.'/../routes/web.php');
}

```

<a name="migrations"></a>
### 마이그레이션

패키지에 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)이 포함되어 있는 경우, `publishesMigrations` 메서드를 사용하여 주어진 디렉토리나 파일에 마이그레이션이 포함되어 있음을 Laravel에 알릴 수 있습니다. Laravel이 마이그레이션을 게시하면, 파일 이름 내의 타임스탬프가 현재 날짜와 시간으로 자동으로 업데이트됩니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishesMigrations([
        __DIR__.'/../database/migrations' => database_path('migrations'),
    ]);
}

```

<a name="language-files"></a>
### 언어 파일

패키지에 [언어 파일](/docs/{{version}}/localization)이 포함되어 있는 경우, `loadTranslationsFrom` 방법을 사용하여 Laravel에 이를 로드하는 방법을 알릴 수 있습니다. 예를 들어, 패키지 이름이 `courier`인 경우, 서비스 제공자의 `boot` 메서드에 다음을 추가해야 합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');
}

```

패키지 번역 라인은 `package::file.line` 구문 규칙을 사용하여 참조됩니다. 따라서 `messages` 파일에서 `courier` 패키지의 `welcome` 라인을 다음과 같이 불러올 수 있습니다:

```php
echo trans('courier::messages.welcome');

```



`loadJsonTranslationsFrom` 메서드를 사용하여 패키지에 대한 JSON 번역 파일을 등록할 수 있습니다. 이 메서드는 패키지의 JSON 번역 파일이 포함된 디렉토리 경로를 받습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadJsonTranslationsFrom(__DIR__.'/../lang');
}

```

<a name="publishing-language-files"></a>
#### 언어 파일 퍼블리싱

패키지의 언어 파일을 애플리케이션의 `lang/vendor` 디렉토리로 퍼블리시하고 싶다면, 서비스 제공자의 `publishes` 메서드를 사용할 수 있습니다. `publishes` 메서드는 패키지 경로 배열과 원하는 퍼블리시 위치를 받습니다. 예를 들어, `courier` 패키지의 언어 파일을 퍼블리시하려면 다음과 같이 할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadTranslationsFrom(__DIR__.'/../lang', 'courier');

    $this->publishes([
        __DIR__.'/../lang' => $this->app->langPath('vendor/courier'),
    ]);
}

```

이제 사용자가 귀하의 패키지에서 Laravel의 `vendor:publish` Artisan 명령어를 실행하면, 패키지의 언어 파일이 지정된 게시 위치로 게시됩니다.

<a name="views"></a>
### 뷰

Laravel에 패키지의 [뷰](/docs/{{version}}/views)를 등록하려면, Laravel에 뷰가 어디에 있는지 알려야 합니다. 이는 서비스 제공자의 `loadViewsFrom` 메서드를 사용하여 수행할 수 있습니다. `loadViewsFrom` 메서드는 두 개의 인수를 받습니다: 뷰 템플릿의 경로와 패키지 이름입니다. 예를 들어, 패키지 이름이 `courier`인 경우 서비스 제공자의 `boot` 메서드에 다음을 추가하면 됩니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');
}

```

패키지 뷰는 `package::view` 구문 규칙을 사용하여 참조됩니다. 따라서 뷰 경로가 서비스 제공자에 등록되면, 다음과 같이 `courier` 패키지에서 `dashboard` 뷰를 불러올 수 있습니다:

```php
Route::get('/dashboard', function () {
    return view('courier::dashboard');
});

```

<a name="overriding-package-views"></a>
#### 패키지 뷰 재정의

`loadViewsFrom` 메소드를 사용할 때, Laravel은 실제로 뷰를 위한 두 개의 위치를 등록합니다: 애플리케이션의 `resources/views/vendor` 디렉터리와 사용자가 지정한 디렉터리. 예를 들어 `courier` 패키지를 사용하는 경우, Laravel은 먼저 개발자가 `resources/views/vendor/courier` 디렉터리에 뷰의 맞춤 버전을 배치했는지 확인합니다. 그 후 뷰가 맞춤화되지 않았다면, Laravel은 `loadViewsFrom` 호출에서 지정한 패키지 뷰 디렉터리를 검색합니다. 이는 패키지 사용자가 패키지의 뷰를 쉽게 맞춤화하거나 재정의할 수 있게 합니다.

<a name="publishing-views"></a>
#### 뷰 게시

애플리케이션의 `resources/views/vendor` 디렉터리에 뷰를 게시 가능하게 만들고 싶다면, 서비스 제공자의 `publishes` 메소드를 사용할 수 있습니다. `publishes` 메소드는 패키지 뷰 경로와 원하는 게시 위치의 배열을 받습니다:

```php
/**
 * Bootstrap the package services.
 */
public function boot(): void
{
    $this->loadViewsFrom(__DIR__.'/../resources/views', 'courier');

    $this->publishes([
        __DIR__.'/../resources/views' => resource_path('views/vendor/courier'),
    ]);
}

```

이제 사용자가 여러분의 패키지에서 Laravel의 `vendor:publish` Artisan 명령을 실행하면, 패키지의 뷰가 지정된 게시 위치로 복사됩니다.

<a name="view-components"></a>
### 뷰 컴포넌트

Blade 컴포넌트를 사용하는 패키지를 제작하거나 컴포넌트를 비전통적인 디렉토리에 배치하는 경우, Laravel이 컴포넌트를 찾을 수 있도록 컴포넌트 클래스와 HTML 태그 별칭을 수동으로 등록해야 합니다. 일반적으로 패키지 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록하는 것이 좋습니다:

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}

```

컴포넌트가 등록되면, 해당 태그 별칭을 사용하여 렌더링할 수 있습니다:

```blade
<x-package-alert/>

```

<a name="autoloading-package-components"></a>
#### 패키지 구성 요소 자동 로드

또는 관례에 따라 구성 요소 클래스를 자동으로 로드하기 위해 `componentNamespace` 방법을 사용할 수 있습니다. 예를 들어, `Nightshade` 패키지는 `Nightshade\Views\Components` 네임스페이스 내에 있는 `Calendar` 및 `ColorPicker` 구성 요소를 가질 수 있습니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}

```

이를 통해 `package-name::` 구문을 사용하여 공급업체 네임스페이스로 패키지 구성 요소를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />

```

Blade는 이 컴포넌트에 연결된 클래스를 컴포넌트 이름을 파스칼 케이스로 변환하여 자동으로 감지합니다. 하위 디렉토리도 '닷(dot)' 표기법을 사용하여 지원됩니다.

<a name="anonymous-components"></a>
#### 익명 컴포넌트

패키지에 익명 컴포넌트가 포함되어 있는 경우, 패키지의 'views' 디렉토리 내 `components` 디렉토리에 배치해야 합니다([loadViewsFrom 메서드](#views)에서 지정한 대로). 그런 다음, 패키지의 뷰 네임스페이스를 컴포넌트 이름 앞에 붙여 렌더링할 수 있습니다:

```blade
<x-courier::alert />

```

<a name="about-artisan-command"></a>
### "About" Artisan 명령어

Laravel에 내장된 `about` Artisan 명령어는 애플리케이션의 환경 및 구성에 대한 개요를 제공합니다. 패키지는 `AboutCommand` 클래스를 통해 이 명령어의 출력에 추가 정보를 전달할 수 있습니다. 일반적으로 이 정보는 패키지 서비스 제공자의 `boot` 메서드에서 추가될 수 있습니다:

```php
use Illuminate\Foundation\Console\AboutCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    AboutCommand::add('My Package', fn () => ['Version' => '1.0.0']);
}

```

<a name="commands"></a>
## 명령어

패키지의 Artisan 명령어를 Laravel에 등록하려면 `commands` 메서드를 사용할 수 있습니다. 이 메서드는 명령어 클래스 이름의 배열을 기대합니다. 명령어가 등록되면 [Artisan CLI](/docs/{{version}}/artisan)를 사용하여 실행할 수 있습니다:

```php
use Courier\Console\Commands\InstallCommand;
use Courier\Console\Commands\NetworkCommand;

/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->commands([
            InstallCommand::class,
            NetworkCommand::class,
        ]);
    }
}

```

<a name="optimize-commands"></a>
### 명령어 최적화

Laravel의 [optimize 명령어](/docs/{{version}}/deployment#optimization)는 애플리케이션의 구성, 이벤트, 라우트 및 뷰를 캐시합니다. `optimizes` 방법을 사용하면 `optimize` 및 `optimize:clear` 명령어가 실행될 때 호출되어야 하는 패키지 고유의 Artisan 명령어를 등록할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->optimizes(
            optimize: 'package:optimize',
            clear: 'package:clear-optimizations',
        );
    }
}

```

<a name="reload-commands"></a>
### 명령어 재시작

Laravel의 [재시작 명령어](/docs/{{version}}/deployment#reloading-services)는 실행 중인 서비스를 종료하여 시스템 프로세스 모니터가 자동으로 다시 시작할 수 있도록 합니다. `reloads` 방법을 사용하면 `reload` 명령어가 실행될 때 호출되어야 하는 패키지의 자체 Artisan 명령어를 등록할 수 있습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    if ($this->app->runningInConsole()) {
        $this->reloads('package:reload');
    }
}

```

<a name="public-assets"></a>
## 공개 자산

귀하의 패키지에는 JavaScript, CSS 및 이미지와 같은 자산이 있을 수 있습니다. 이러한 자산을 애플리케이션의 `public` 디렉토리에 게시하려면 서비스 제공자의 `publishes` 메서드를 사용하십시오. 이 예제에서는 관련 자산 그룹을 쉽게 게시하는 데 사용할 수 있는 `public` 자산 그룹 태그도 추가합니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../public' => public_path('vendor/courier'),
    ], 'public');
}

```

이제 패키지 사용자가 `vendor:publish` 명령을 실행하면 자산이 지정된 게시 위치로 복사됩니다. 사용자는 패키지가 업데이트될 때마다 자산을 덮어써야 할 필요가 있으므로 `--force` 플래그를 사용할 수 있습니다:

```shell
php artisan vendor:publish --tag=public --force

```

<a name="publishing-file-groups"></a>
## 파일 그룹 게시

패키지 자산과 리소스 그룹을 별도로 게시하고자 할 수 있습니다. 예를 들어, 사용자가 패키지의 자산을 게시하도록 강제하지 않고 패키지의 설정 파일만 게시할 수 있도록 하려는 경우가 있을 수 있습니다. 패키지 서비스 제공자의 `publishes` 메서드를 호출할 때 이들을 "태그"함으로써 이를 수행할 수 있습니다. 예를 들어, 패키지 서비스 제공자의 `boot` 메서드에서 `courier` 패키지에 대해 두 개의 게시 그룹(`courier-config` 및 `courier-migrations`)을 정의하기 위해 태그를 사용하는 방법은 다음과 같습니다:

```php
/**
 * Bootstrap any package services.
 */
public function boot(): void
{
    $this->publishes([
        __DIR__.'/../config/package.php' => config_path('package.php')
    ], 'courier-config');

    $this->publishesMigrations([
        __DIR__.'/../database/migrations/' => database_path('migrations')
    ], 'courier-migrations');
}

```

이제 사용자는 `vendor:publish` 명령을 실행할 때 태그를 참조하여 이러한 그룹을 개별적으로 게시할 수 있습니다:

```shell
php artisan vendor:publish --tag=courier-config

```

사용자는 `--provider` 플래그를 사용하여 패키지 서비스 제공자가 정의한 모든 게시 가능한 파일을 게시할 수도 있습니다:

```shell
php artisan vendor:publish --provider="Your\Package\ServiceProvider"

```
{% endraw %}
