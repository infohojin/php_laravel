---
layout: docs
title: "디렉토리 구조"
---

{% raw %}
# 디렉토리 구조

- [소개](#introduction)
- [루트 디렉토리](#the-root-directory)
- [The `app` Directory](#the-root-app-directory)
- [The `bootstrap` Directory](#the-bootstrap-directory)
- [The `config` Directory](#the-config-directory)
- [The `database` Directory](#the-database-directory)
- [The `public` Directory](#the-public-directory)
- [The `resources` Directory](#the-resources-directory)
- [The `routes` Directory](#the-routes-directory)
- [The `storage` Directory](#the-storage-directory)
- [The `tests` Directory](#the-tests-directory)
- [The `vendor` Directory](#the-vendor-directory)
- [The App Directory](#the-app-directory)
- [The `Broadcasting` Directory](#the-broadcasting-directory)
- [The `Console` Directory](#the-console-directory)
- [The `Events` Directory](#the-events-directory)
- [The `Exceptions` Directory](#the-exceptions-directory)
- [The `Http` Directory](#the-http-directory)
- [The `Jobs` Directory](#the-jobs-directory)
- [The `Listeners` Directory](#the-listeners-directory)
- [The `Mail` Directory](#the-mail-directory)
- [The `Models` Directory](#the-models-directory)
- [The `Notifications` Directory](#the-notifications-directory)
- [The `Policies` Directory](#the-policies-directory)
- [The `Providers` Directory](#the-providers-directory)
- [The `Rules` Directory](#the-rules-directory)

<a name="introduction"></a>
## 소개

기본 Laravel 애플리케이션 구조는 큰 애플리케이션과 작은 애플리케이션 모두에 훌륭한 시작점을 제공하기 위한 것입니다. 하지만 애플리케이션을 원하는 대로 자유롭게 구성할 수 있습니다. Laravel 은 Composer 가 해당 클래스를 자동으로 로드할 수 있는 한， 주어진 클래스의 위치에 거의 제한을 두지 않습니다。

<a name="the-root-directory"></a>
## 루트 디렉토리

<a name="the-root-app-directory"></a>
### 앱 디렉토리

`app` 디렉터리에는 애플리케이션의 핵심 코드가 포함되어 있습니다. 곧 이 디렉터리를 더 자세히 살펴보겠지만， 애플리케이션의 거의 모든 클래스가 이 디렉터리에 있을 것입니다。

<a name="the-bootstrap-directory"></a>
### 부트스트랩 디렉토리

`bootstrap` 디렉토리에는 프레임워크를 부트스트랩하는 `app.php` 파일이 포함되어 있습니다. 이 디렉토리는 또한 경로 및 서비스 캐시 파일과 같은 성능 최적화를 위해 프레임워크에서 생성된 파일을 포함하는 `cache` 디렉토리를 호스트합니다。

<a name="the-config-directory"></a>
### 컨피그 디렉토리

`config` 디렉토리에는 이름에서 알 수 있듯이 애플리케이션의 모든 구성 파일이 포함되어 있습니다. 이러한 모든 파일을 읽고 사용할 수 있는 모든 옵션에 익숙해지는 것이 좋습니다。

<a name="the-database-directory"></a>
### 데이터베이스 디렉토리

`database` 디렉토리에는 데이터베이스 마이그레이션， 모델 팩토리 및 시드가 포함되어 있습니다. 원하는 경우 이 디렉토리를 사용하여 SQLite 데이터베이스를 저장할 수도 있습니다。

<a name="the-public-directory"></a>
### 퍼블릭 디렉터리

`public` 디렉토리에는 `index.php` 파일이 포함되어 있습니다. 이 파일은 애플리케이션에 들어오는 모든 요청의 엔트리 포인트이며 자동 로딩을 구성합니다. 이 디렉토리는 이미지， JavaScript 및 CSS 와 같은 자산도 호스팅합니다。

<a name="the-resources-directory"></a>
### 리소스 디렉토리

`resources` 디렉토리에는 CSS 또는 JavaScript 와 같은 원시， 컴파일되지 않은 자산뿐만 아니라 [views](/docs/{{version}}/views) 가 포함되어 있습니다。

<a name="the-routes-directory"></a>
### 경로 디렉터리

`routes` 디렉토리에는 애플리케이션에 대한 모든 경로 정의가 포함되어 있습니다. 기본적으로 Laravel 에는 `web.php` 및 `console.php` 라는 두 개의 경로 파일이 포함되어 있습니다。

`web.php` 파일에는 Laravel 이 세션 상태， CSRF 보호 및 쿠키 암호화를 제공하는 `web` 미들웨어 그룹에 배치하는 경로가 포함되어 있습니다. 애플리케이션에서 상태 비저장 RESTful API 를 제공하지 않는 경우 모든 경로가 `web.php` 파일에서 정의될 가능성이 높습니다。

`console.php` 파일은 모든 종료 기반 콘솔 명령을 정의할 수 있는 곳입니다. 각 종료는 명령 인스턴스에 바인딩되어 각 명령의 IO 메서드와 상호 작용하는 간단한 접근 방식을 제공합니다. 이 파일은 HTTP 경로를 정의하지 않지만， 애플리케이션에 대한 콘솔 기반 엔트리 포인트 (경로) 를 정의합니다. `console.php` 파일에서 [스케줄](/docs/{{version}}/scheduling) 작업을 수행할 수도 있습니다。

선택적으로 `install:api` 및 `install:broadcasting` Artisan 명령을 통해 API 경로 (`api.php`) 및 브로드캐스트 채널 (`channels.php`) 에 대한 추가 경로 파일을 설치할 수 있습니다。

`api.php` 파일에는 상태 비저장을 의도한 경로가 포함되어 있으므로， 이러한 경로를 통해 애플리케이션에 입력되는 요청은 인증 (via tokens)(/docs/{{version}}/sanctum) 되어야 하며 세션 상태에 액세스할 수 없습니다。

`channels.php` 파일은 애플리케이션이 지원하는 모든 [이벤트 방송](/docs/{{version}}/broadcasting) 채널을 등록할 수 있는 곳입니다。

<a name="the-storage-directory"></a>
### 저장소 디렉토리

`storage` 디렉토리에는 로그， 컴파일된 블레이드 템플릿， 파일 기반 세션， 파일 캐시 및 프레임워크에서 생성한 기타 파일이 포함되어 있습니다. 이 디렉토리는 `app`, `framework` 및 `logs` 디렉토리로 분리됩니다. `app` 디렉토리는 애플리케이션에서 생성한 모든 파일을 저장하는 데 사용될 수 있습니다. `framework` 디렉토리는 프레임워크에서 생성된 파일과 캐시를 저장하는 데 사용됩니다. 마지막으로 `logs` 디렉토리에는 애플리케이션의 로그 파일이 포함되어 있어야 합니다。

`storage/app/public` 디렉토리는 공개적으로 접근할 수 있어야 하는 프로필 아바타와 같은 사용자 생성 파일을 저장하는 데 사용될 수 있습니다. 이 디렉토리를 가리키는 `public/storage` 에서 기호 링크를 생성해야 합니다. `php artisan storage:link` Artisan 명령을 사용하여 링크를 생성할 수 있습니다。

<a name="the-tests-directory"></a>
### 테스트 디렉토리

`tests` 디렉터리에는 자동화된 테스트가 포함되어 있습니다. Example [Pest](https://pestphp.com) 또는 [PHPUnit](https://phpunit.de/) 단위 테스트 및 기능 테스트가 즉시 제공됩니다. 각 테스트 클래스는 `Test` 라는 단어로 접미사가 지정되어야 합니다. `/vendor/bin/pest` 또는 `/vendor/bin/phpunit` 명령을 사용하여 테스트를 실행할 수 있습니다. 또는 테스트 결과를 보다 상세하고 아름답게 표현하려는 경우 `php artisan test` Artisan 명령을 사용하여 테スト를 실행할 수도 있습니다。

<a name="the-vendor-directory"></a>
### 공급업체 디렉토리

`vendor` 디렉토리에는 [Composer](https://getcomposer.org) 종속성이 포함되어 있습니다。

<a name="the-app-directory"></a>
## 앱 디렉토리

애플리케이션의 대부분은 `app` 디렉토리에 저장됩니다. 기본적으로 이 디렉토리는 `App` 아래에 네임스페이스가 있으며 [PSR-4 자동 로딩 표준](https://www.php-fig.org/psr/psr-4/) 을 사용하여 Composer 에 의해 자동 로드됩니다。

기본적으로 `app` 디렉토리에는 `Http`, `Models` 및 `Providers` 디렉토리가 포함되어 있습니다. 그러나 시간이 지남에 따라 make Artisan 명령을 사용하여 클래스를 생성할 때 앱 디렉토리 내에 다양한 다른 디렉토리가 생성됩니다. 예를 들어 `app/Console` 디렉토리는 `make:command` Artisan 명령을 실행하여 명령 클래스를 생성할 때까지 존재하지 않습니다。

`Console` 디렉터리와 `Http` 디렉터리 모두 아래의 해당 섹션에서 추가로 설명되지만， `Console` 디렉터리와 `Http` 디렉터리를 애플리케이션의 핵심에 API 를 제공하는 것으로 생각하세요. HTTP 프로토콜과 CLI 는 모두 애플리케이션과 상호 작용하는 메커니즘이지만， 실제로는 애플리케이션 로직을 포함하지 않습니다. 즉， 애플리케이션에 명령을 내리는 두 가지 방법입니다. `Console` 디렉터리에는 모든 Artisan 명령이 포함되어 있고， `Http` 디렉터리에는 컨트롤러， 미들웨어 및 요청이 포함되어 있습니다。

> [!NOTE]
> `app` 디렉토리의 많은 클래스는 명령을 통해 Artisan 에서 생성할 수 있습니다. 사용 가능한 명령을 검토하려면 터미널에서 `php artisan list make` 명령을 실행하십시오。

<a name="the-broadcasting-directory"></a>
### 방송 디렉토리

`Broadcasting` 디렉토리에는 애플리케이션의 모든 방송 채널 클래스가 포함되어 있습니다. 이러한 클래스는 `make:channel` 명령을 사용하여 생성됩니다. 이 디렉토리는 기본적으로 존재하지 않지만， 첫 번째 채널을 생성할 때 사용자를 위해 생성됩니다. 채널에 대한 자세한 내용은 [이벤트 방송](/docs/{{version}}/broadcasting) 설명서를 참조하십시오。

<a name="the-console-directory"></a>
### 콘솔 디렉토리

`Console` 디렉토리에는 애플리케이션에 대한 모든 사용자 지정 Artisan 명령이 포함되어 있습니다. 이러한 명령은 `make:command` 명령을 사용하여 생성할 수 있습니다。

<a name="the-events-directory"></a>
### 사건 디렉토리

이 디렉토리는 기본적으로 존재하지 않지만 `event:generate` 및 `make:event` Artisan 명령을 통해 사용자를 위해 생성됩니다. `Events` 디렉토리는 이벤트 클래스 (/docs/{{version}}/events) 를 호스팅합니다. 이벤트는 특정 작업이 발생했다는 것을 애플리케이션의 다른 부분에 알리는 데 사용될 수 있으므로 매우 유연하고 분리가 가능합니다。

<a name="the-exceptions-directory"></a>
### 예외 디렉토리

`Exceptions` 디렉토리에는 애플리케이션에 대한 모든 사용자 지정 예외가 포함되어 있습니다. 이러한 예외는 `make:exception` 명령을 사용하여 생성될 수 있습니다。

<a name="the-http-directory"></a>
### Http 디렉토리

`Http` 디렉토리에는 컨트롤러， 미들웨어 및 양식 요청이 포함되어 있습니다. 애플리케이션에 들어오는 요청을 처리하기 위한 거의 모든 로직이 이 디렉토리에 배치됩니다。

<a name="the-jobs-directory"></a>
### 직업 디렉토리

이 디렉토리는 기본적으로 존재하지 않지만 `make:job` Artisan 명령을 실행하면 사용자를 위해 생성됩니다. `Jobs` 디렉토리는 애플리케이션에 대한 [대기열에 배치 가능한 작업](/docs/{{version}}/queues) 을 호스팅합니다. 작업은 애플리케이션에 의해 대기열에 배치되거나 현재 요청 수명 주기 내에서 동기적으로 실행될 수 있습니다. 현재 요청 중에 동기적으로 실행되는 작업은 [명령 패턴](https://en.wikipedia.org/wiki/Command_pattern) 의 구현이므로 때때로 “명령” 이라고 불립니다。

<a name="the-listeners-directory"></a>
### 청취자 디렉토리

이 디렉토리는 기본적으로 존재하지 않지만 `event:generate` 또는 `make:listener` Artisan 명령을 실행하면 사용자를 위해 생성됩니다. `Listeners` 디렉토리에는 사용자의 [이벤트](/docs/{{version}}/events) 를 처리하는 클래스가 포함되어 있습니다. 이벤트 리스너는 이벤트 인스턴스를 수신하고 발생하는 이벤트에 대한 응답으로 로직을 수행합니다. 예를 들어 `UserRegistered` 이벤트는 `SendWelcomeEmail` 리스너에 의해 처리될 수 있습니다。

<a name="the-mail-directory"></a>
### 메일 디렉토리

이 디렉토리는 기본적으로 존재하지 않지만 `make:mail` Artisan 명령을 실행하면 사용자를 위해 생성됩니다. `Mail` 디렉토리에는 애플리케이션에서 전송한 모든 [이메일을 나타내는 클래스](/docs/{{version}}/mail) 가 포함되어 있습니다. Mail 객체를 사용하면 `Mail::send` 메서드를 사용하여 전송할 수 있는 단일하고 간단한 클래스에 이메일 구축의 모든 로직을 캡슐화할 수 있습니다。

<a name="the-models-directory"></a>
### 모델 디렉토리

`Models` 디렉터리에는 모든 [Eloquent model classes](/docs/{{version}}/eloquent) 가 포함되어 있습니다. Laravel 에 포함된 Eloquent ORM 은 데이터베이스 작업을 위한 아름답고 간단한 ActiveRecord 구현을 제공합니다. 각 데이터베이스 테이블에는 해당 테이블과 상호 작용하는 데 사용되는 해당 “모델” 이 있습니다. 모델을 사용하면 테이블에서 데이터를 쿼리하고 테이블에 새 레코드를 삽입할 수 있습니다。

<a name="the-notifications-directory"></a>
### 알림 디렉토리

이 디렉터리는 기본적으로 존재하지 않지만 `make:notification` Artisan 명령을 실행하면 사용자를 위해 생성됩니다. `Notifications` 디렉터리에는 애플리케이션에서 발생하는 이벤트에 대한 간단한 알림과 같이 애플리케이션에서 보내는 모든 “트랜잭션” [알림](/docs/{{version}}/notifications) 이 포함되어 있습니다. Laravel 의 알림 기능은 이메일， Slack, SMS 또는 데이터베이스에 저장된 알림과 같은 다양한 드라이버를 통해 알림을 전송하는 추상화 기능입니다。

<a name="the-policies-directory"></a>
### 정책 디렉토리

이 디렉토리는 기본적으로 존재하지 않지만 `make:policy` Artisan 명령을 실행하면 사용자를 위해 생성됩니다. `Policies` 디렉토리에는 애플리케이션에 대한 [권한 부여 정책 클래스](/docs/{{version}}/authorization) 가 포함되어 있습니다. 정책은 사용자가 리소스에 대해 특정 작업을 수행할 수 있는지 여부를 결정하는 데 사용됩니다。

<a name="the-providers-directory"></a>
### 공급업체 디렉토리

`Providers` 디렉터리에는 애플리케이션의 모든 [서비스 제공자](/docs/{{version}}/providers) 가 포함되어 있습니다. 서비스 제공자는 서비스 컨테이너에서 서비스를 바인딩하거나， 이벤트를 등록하거나， 수신 요청에 대비하기 위해 다른 작업을 수행하여 애플리케이션을 부트스트랩합니다。

새로운 Laravel 애플리케이션에서는 이 디렉토리에 `AppServiceProvider` 가 이미 포함되어 있습니다. 필요에 따라 이 디렉토리에 자체 제공자를 추가할 수 있습니다。

<a name="the-rules-directory"></a>
### 규칙 디렉토리

이 디렉토리는 기본적으로 존재하지 않지만 `make:rule` Artisan 명령을 실행하면 생성됩니다. `Rules` 디렉토리에는 애플리케이션에 대한 사용자 지정 검증 규칙 객체가 포함되어 있습니다. 규칙은 복잡한 검증 로직을 간단한 객체로 캡슐화하는 데 사용됩니다. 자세한 내용은 [검증 문서](/docs/{{version}}/validation) 를 참조하십시오。
{% endraw %}
