---
layout: docs
title: "라라벨 세일"
---

{% raw %}
# 라라벨 세일

- [소개](#introduction)
- [설치 및 설정](#installation)
- 리빌딩 세일 이미지 (#rebuilding-sail-images)
- 셸 별칭 구성 (#configuring-a-shell-alias)
- [돛 시작 및 정지](#starting-and-stopping-sail)
- [Executing Commands](#executing-sail-commands)
- [PHP 명령 실행](#executing-php-commands)
- [작곡가 명령 실행](#executing-composer-commands)
- [장인 명령 실행](#executing-artisan-commands)
- [Executing Node / NPM Commands](#executing-node-npm-commands)
- [데이터베이스와 상호작용](#interacting-with-sail-databases)
- [MySQL](#mysql)
- [MongoDB](#mongodb)
- [Redis](#redis)
- [Valkey](#valkey)
- 메일리서치 (#meilisearch)
- 타이페센스 (#typesense)
- 파일 스토리지 (#file-storage)
- 런닝 테스트 (#running-tests)
- 라라벨 더스크 (#laravel-dusk)
- [Previewing Emails](#previewing-emails)
- [컨테이너 CLI](#sail-container-cli)
- [PHP 버전](#sail-php-versions)
- [추가 PHP 확장](#sail-php-extensions)
- [노드 버전](#sail-node-versions)
- [Sharing Your Site](#sharing-your-site)
- [Xdebug 로 디버깅](#debugging-with-xdebug)
- [Xdebug CLI 사용법](#xdebug-cli-usage)
- [Xdebug 브라우저 사용법](#xdebug-browser-usage)
- [커스터마이징](#sail-customization)

<a name="introduction"></a>
## 소개

[Laravel Sail](https://github.com/laravel/sail) 는 Laravel 의 기본 Docker 개발 환경과 상호 작용하기 위한 경량 명령줄 인터페이스입니다. Sail 은 이전 Docker 경험 없이 PHP, MySQL 및 Redis 를 사용하여 Laravel 애플리케이션을 구축하기 위한 훌륭한 출발점을 제공합니다。

Sail 의 핵심은 프로젝트의 루트에 저장된 `compose.yaml` 파일과 `sail` 스크립트입니다. `sail` 스크립트는 `compose.yaml` 파일로 정의된 Docker 컨테이너와 상호 작용하는 편리한 방법을 제공하는 CLI 를 제공합니다。

Laravel Sail 은 macOS, Linux 및 Windows(WSL2(https://docs.microsoft.com/en-us/windows/wsl/about)) 에서 지원됩니다。

<a name="installation"></a>
## 설치 및 설정

Composer 패키지 관리자를 사용하여 Sail 을 설치할 수 있습니다：

```shell
composer require laravel/sail --dev
```



Sail이 설치된 후, `sail:install` Artisan 명령어를 실행할 수 있습니다. 이 명령어는 Sail의 `compose.yaml` 파일을 애플리케이션의 루트에 게시하고, Docker 서비스에 연결하기 위해 필요한 환경 변수로 `.env` 파일을 수정합니다:

```shell
php artisan sail:install
```



마지막으로, Sail을 시작할 수 있습니다. Sail 사용법을 계속 배우려면 이 문서의 나머지 부분을 계속 읽으십시오:

```shell
./vendor/bin/sail up
```



> [!WARNING]
> 만약 리눅스용 Docker Desktop을 사용 중이라면, 다음 명령어를 실행하여 `default` Docker 컨텍스트를 사용해야 합니다: `docker context use default`. 또한 컨테이너 내에서 파일 권한 오류가 발생하면, `SUPERVISOR_PHP_USER` 환경 변수를 `root`로 설정해야 할 수도 있습니다.

<a name="adding-additional-services"></a>
#### 추가 서비스 추가하기

기존 Sail 설치에 추가 서비스를 추가하고 싶다면, 다음 `sail:add` Artisan 명령어를 실행할 수 있습니다:

```shell
php artisan sail:add
```



<a name="using-devcontainers"></a>
#### Devcontainers 사용하기

[Devcontainer](https://code.visualstudio.com/docs/remote/containers) 내에서 개발하고 싶다면, `sail:install` 명령어에 `--devcontainer` 옵션을 제공할 수 있습니다. `sail:install` 명령어에 대해 `--devcontainer` 옵션은 기본 `.devcontainer/devcontainer.json ` 파일을 애플리케이션 루트에 게시하도록 지시합니다:

```shell
php artisan sail:install --devcontainer
```



<a name="rebuilding-sail-images"></a>
### Sail 이미지 재빌드

때때로 Sail 이미지의 모든 패키지와 소프트웨어가 최신 상태인지 확인하기 위해 이미지를 완전히 재빌드하고 싶을 수 있습니다. 다음 `build` 명령을 사용하여 이를 수행할 수 있습니다:

```shell
docker compose down -v

sail build --no-cache

sail up
```



<a name="configuring-a-shell-alias"></a>
### 셸 별칭 구성

기본적으로 Sail 명령은 모든 새로운 Laravel 애플리케이션에 포함된 `vendor/bin/sail` 스크립트를 사용하여 호출됩니다:

```shell
./vendor/bin/sail up
```



하지만 Sail 명령어를 실행하기 위해 `vendor/bin/sail`를 반복해서 입력하는 대신, Sail의 명령어를 더 쉽게 실행할 수 있도록 셸 별칭을 설정하고 싶을 수도 있습니다:

```shell
alias sail='sh $([ -f sail ] && echo sail || echo vendor/bin/sail)'
```



항상 사용할 수 있도록 하려면 홈 디렉토리의 셸 구성 파일(예: `~/.zshrc` 또는 `~/.bashrc`)에 이를 추가한 다음 셸을 재시작할 수 있습니다.

셸 별칭이 구성되면 단순히 `sail`를 입력하여 Sail 명령을 실행할 수 있습니다. 이 문서의 나머지 예제에서는 이미 이 별칭을 구성했다고 가정합니다:

```shell
sail up
```



<a name="starting-and-stopping-sail"></a>
## Sail 시작 및 중지

Laravel Sail의 `compose.yaml` 파일은 Laravel 애플리케이션을 빌드하는 데 함께 작동하는 다양한 Docker 컨테이너를 정의합니다. 이러한 각 컨테이너는 `compose.yaml` 파일의 `services` 구성 내에 있는 항목입니다. `laravel.test` 컨테이너는 애플리케이션을 제공하는 주요 애플리케이션 컨테이너입니다.

Sail을 시작하기 전에, 로컬 컴퓨터에서 다른 웹 서버나 데이터베이스가 실행되고 있지 않은지 확인해야 합니다. 애플리케이션의 `compose.yaml` 파일에 정의된 모든 Docker 컨테이너를 시작하려면, `up` 명령을 실행해야 합니다:

```shell
sail up
```



모든 Docker 컨테이너를 백그라운드에서 시작하려면, Sail을 '분리(detached)' 모드로 시작할 수 있습니다:

```shell
sail up -d
```



애플리케이션의 컨테이너가 시작되면, 웹 브라우저에서 다음 주소로 프로젝트에 접속할 수 있습니다: http://localhost.

모든 컨테이너를 중지하려면, 단순히 Control + C를 눌러 컨테이너 실행을 중지할 수 있습니다. 또는 컨테이너가 백그라운드에서 실행 중이라면, `stop` 명령어를 사용할 수 있습니다:

```shell
sail stop
```



<a name="executing-sail-commands"></a>
## 명령어 실행

Laravel Sail을 사용할 때, 애플리케이션은 Docker 컨테이너 내에서 실행되며 로컬 컴퓨터와는 격리됩니다. 그러나 Sail은 임의의 PHP 명령어, Artisan 명령어, Composer 명령어, Node / NPM 명령어와 같이 애플리케이션에 대해 다양한 명령을 실행할 수 있는 편리한 방법을 제공합니다.

**Laravel 문서를 읽을 때, Sail을 참조하지 않는 Composer, Artisan, Node / NPM 명령어에 대한 언급을 자주 보게 됩니다.** 이러한 예제들은 이러한 도구들이 로컬 컴퓨터에 설치되어 있다고 가정합니다. 로컬 Laravel 개발 환경에서 Sail을 사용하는 경우, 해당 명령어는 Sail을 사용하여 실행해야 합니다:

```shell
# Running Artisan commands locally...
php artisan queue:work

# Running Artisan commands within Laravel Sail...
sail artisan queue:work
```



<a name="executing-php-commands"></a>
### PHP 명령 실행

PHP 명령은 `php` 명령을 사용하여 실행할 수 있습니다. 물론, 이러한 명령은 애플리케이션에 설정된 PHP 버전을 사용하여 실행됩니다. Laravel Sail에서 사용 가능한 PHP 버전에 대해 더 알아보려면 [PHP 버전 문서](#sail-php-versions)를 참조하세요.

```shell
sail php --version

sail php script.php
```



<a name="executing-composer-commands"></a>
### Composer 명령 실행

Composer 명령은 `composer` 명령을 사용하여 실행할 수 있습니다. Laravel Sail의 애플리케이션 컨테이너에는 Composer가 설치되어 있습니다:

```shell
sail composer require laravel/sanctum
```



<a name="executing-artisan-commands"></a>
### Artisan 명령 실행

Laravel Artisan 명령은 `artisan` 명령을 사용하여 실행할 수 있습니다:

```shell
sail artisan queue:work
```



<a name="executing-node-npm-commands"></a>
### 노드 / NPM 명령 실행

노드 명령은 `node` 명령을 사용하여 실행할 수 있으며, NPM 명령은 `npm` 명령을 사용하여 실행할 수 있습니다:

```shell
sail node --version

sail npm run dev
```



원하신다면 NPM 대신 Yarn을 사용할 수 있습니다:

```shell
sail yarn
```

<a name="interacting-with-sail-databases"></a>
## 데이터베이스와의 상호작용

<a name="mysql"></a>
### MySQL

알아차렸을지도 모르겠지만， 애플리케이션의 `compose.yaml` 파일에는 MySQL 컨테이너에 대한 항목이 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/) 을 사용하므로 컨테이너를 중지하고 다시 시작해도 데이터베이스에 저장된 데이터가 유지됩니다。

또한 MySQL 컨테이너가 처음 시작될 때 두 개의 데이터베이스가 생성됩니다. 첫 번째 데이터베이스는 `DB_DATABASE` 환경 변수의 값을 사용하여 이름이 지정되며 로컬 개발용입니다. 두 번째는 `testing` 라는 전용 테스트 데이터베이스로， 테스트가 개발 데이터에 영향을 주지 않도록 보장합니다。

컨테이너를 시작한 후， 애플리케이션의 `.env` 파일 내에서 `DB_HOST` 환경 변수를 `mysql` 로 설정하여 애플리케이션 내의 MySQL 인스턴스에 연결할 수 있습니다。

로컬 시스템에서 애플리케이션의 MySQL 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 와 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 MySQL 데이터베이스는 `localhost` 포트 3306 에서 액세스할 수 있으며 액세스 자격 증명은 `DB_USERNAME` 및 `DB_PASSWORD` 환경 변수의 값에 해당합니다. 또는 `root` 사용자로 연결할 수 있으며， 이 경우 `DB_PASSWORD` 환경 변수의 값을 암호로 사용할 수도 있습니다。

<a name="mongodb"></a>
### MongoDB

Sail 을 설치할 때 [MongoDB](https://www.mongodb.com/) 서비스를 설치하기로 선택한 경우， 애플리케이션의 `compose.yaml` 파일에는 [Search Indexes](https://www.mongodb.com/docs/atlas/atlas-search/) 와 같은 Atlas 기능을 MongoDB 문서 데이터베이스에 제공하는 [MongoDB Atlas Local](https://www.mongodb.com/docs/atlas/cli/current/atlas-cli-local-cloud/) 컨테이너에 대한 항목이 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/) 을 사용하므로 컨테이너를 중지하고 다시 시작해도 데이터베이스에 저장된 데이터가 유지됩니다。



컨테이너를 시작한 후, 애플리케이션의 `.env` 파일 내에서 `MONGODB_URI` 환경 변수를 `mongodb://mongodb:27017`로 설정하여 애플리케이션 내에서 MongoDB 인스턴스에 연결할 수 있습니다. 인증은 기본적으로 비활성화되어 있지만, `mongodb` 컨테이너를 시작하기 전에 `MONGODB_USERNAME` 및 `MONGODB_PASSWORD` 환경 변수를 설정하여 인증을 활성화할 수 있습니다. 그런 다음 연결 문자열에 자격 증명을 추가하십시오:

```ini
MONGODB_USERNAME=user
MONGODB_PASSWORD=laravel
MONGODB_URI=mongodb://${MONGODB_USERNAME}:${MONGODB_PASSWORD}@mongodb:27017
```

MongoDB 를 애플리케이션과 원활하게 통합하려면 [MongoDB 에서 유지 관리하는 공식 패키지](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 를 설치하면 됩니다。

로컬 시스템에서 애플리케이션의 MongoDB 데이터베이스에 연결하려면 [컴퍼스](https://www.mongodb.com/products/tools/compass) 와 같은 그래픽 인터페이스를 사용할 수 있습니다. 기본적으로 MongoDB 데이터베이스는 `localhost` 포트 `27017` 에서 액세스할 수 있습니다。

<a name="redis"></a>
### Redis

애플리케이션의 `compose.yaml` 파일에는 [Redis](https://redis.io) 컨테이너에 대한 항목도 포함되어 있습니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/) 을 사용하므로 컨테이너를 중지하고 다시 시작해도 Redis 인스턴스에 저장된 데이터가 유지됩니다. 컨테이너를 시작한 후 애플리케이션의 `.env` 파일에서 `REDIS_HOST` 환경 변수를 `redis` 로 설정하여 애플리케이션 내 Redis 인스턴스에 연결할 수 있습니다。

로컬 시스템에서 애플리케이션의 Redis 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 와 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 Redis 데이터베이스는 `localhost` 포트 6379 에서 액세스할 수 있습니다。

<a name="valkey"></a>
### 발키

Sail 을 설치할 때 Valkey 서비스를 설치하도록 선택하면 애플리케이션의 `compose.yaml` 파일에 [Valkey](https://valkey.io/) 에 대한 항목이 포함됩니다. 이 컨테이너는 [Docker 볼륨](https://docs.docker.com/storage/volumes/) 을 사용하므로 Valkey 인스턴스에 저장된 데이터는 컨테이너를 중지하고 다시 시작해도 유지됩니다. 애플리케이션의 `.env` 파일 내에서 `REDIS_HOST` 환경 변수를 `valkey` 로 설정하여 애플리케이션에서 이 컨테이너에 연결할 수 있습니다。

로컬 시스템에서 애플리케이션의 Valkey 데이터베이스에 연결하려면 [TablePlus](https://tableplus.com) 와 같은 그래픽 데이터베이스 관리 애플리케이션을 사용할 수 있습니다. 기본적으로 Valkey 데이터베이스는 `localhost` 포트 6379 에서 액세스할 수 있습니다。

<a name="meilisearch"></a>
### 메일리서치

Sail 을 설치할 때 [Meilisearch](https://www.meilisearch.com) 서비스를 설치하기로 선택한 경우， 애플리케이션의 `compose.yaml` 파일에 [Laravel Scout](/docs/{{version}}/scout) 와 통합된 이 강력한 검색 엔진에 대한 항목이 포함됩니다. 컨테이너를 시작한 후， `MEILISEARCH_HOST` 환경 변수를 `http://meilisearch:7700` 로 설정하여 애플리케이션 내의 Meilisearch 인스턴스에 연결할 수 있습니다。



로컬 컴퓨터에서 웹 브라우저를 통해 `http://localhost:7700`로 이동하면 Meilisearch의 웹 기반 관리 패널에 접근할 수 있습니다.

<a name="typesense"></a>
### Typesense

Sail을 설치할 때 [Typesense](https://typesense.org) 서비스를 설치하도록 선택한 경우, 애플리케이션의 `compose.yaml` 파일에는 [Laravel Scout](/docs/{{version}}/scout#typesense)와 네이티브로 통합된 이 초고속 오픈 소스 검색 엔진에 대한 항목이 포함됩니다. 컨테이너를 시작한 후에는 다음 환경 변수를 설정하여 애플리케이션 내에서 Typesense 인스턴스에 연결할 수 있습니다:

```ini
TYPESENSE_HOST=typesense
TYPESENSE_PORT=8108
TYPESENSE_PROTOCOL=http
TYPESENSE_API_KEY=xyz
```



로컬 시스템에서 `http://localhost:8108` 를 통해 Typesense 의 API 에 액세스할 수 있습니다。

<a name="file-storage"></a>
## 파일 저장소

Amazon S3 를 사용하여 프로덕션 환경에서 애플리케이션을 실행하는 동안 파일을 저장할 계획이라면 Sail 을 설치할 때 [RustFS](https://rustfs.com) 서비스를 설치하는 것이 좋습니다. RustFS 는 프로덕션 S3 환경에서 “테스트” 스토리지 버킷을 생성하지 않고 Laravel 의 `s3` 파일 스토리지 드라이버를 사용하여 로컬로 개발하는 데 사용할 수 있는 S3 호환 API 를 제공합니다. Sail 을 설치하는 동안 RustFS 를 설치하도록 선택하면 RustFS 구성 섹션이 애플리케이션의 `compose.yaml` 파일에 추가됩니다。

기본적으로 애플리케이션의 `filesystems` 구성 파일에는 `s3` 디스크에 대한 디스크 구성이 이미 포함되어 있습니다. 이 디스크를 사용하여 Amazon S3 와 상호 작용하는 것 외에도， 해당 구성을 제어하는 관련 환경 변수를 수정하는 것만으로 RustFS 와 같은 S3 호환 파일 스토리지 서비스와 상호 작용할 수 있습니다. 예를 들어， RustFS 를 사용할 때 파일 시스템 환경 변수 구성은 다음과 같이 정의되어야 합니다。

```ini
FILESYSTEM_DISK=s3
AWS_ACCESS_KEY_ID=sail
AWS_SECRET_ACCESS_KEY=password
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=local
AWS_ENDPOINT=http://rustfs:9000
AWS_USE_PATH_STYLE_ENDPOINT=true
```



<a name="running-tests"></a>
## 테스트 실행

Laravel은 기본적으로 훌륭한 테스트 지원을 제공하며, Sail의 `test` 명령어를 사용하여 애플리케이션의 [기능 및 단위 테스트](/docs/{{version}}/testing)를 실행할 수 있습니다. Pest / PHPUnit이 허용하는 모든 CLI 옵션도 `test` 명령어에 전달할 수 있습니다:

```shell
sail test

sail test --group orders
```



Sail `test` 명령은 `test` Artisan 명령을 실행하는 것과 동일합니다:

```shell
sail artisan test
```



기본적으로 Sail은 테스트가 현재 데이터베이스 상태에 영향을 미치지 않도록 전용 `testing` 데이터베이스를 생성합니다. 기본 Laravel 설치에서는 Sail이 테스트를 실행할 때 이 데이터베이스를 사용하도록 `phpunit.xml` 파일도 구성합니다:

```xml
<env name="DB_DATABASE" value="testing"/>
```



<a name="laravel-dusk"></a>
### 라라벨 더스크

[라라벨 더스크](/docs/{{version}}/dusk)는 표현력이 풍부하고 사용하기 쉬운 브라우저 자동화 및 테스트 API를 제공합니다. Sail 덕분에 로컬 컴퓨터에 Selenium이나 다른 도구를 설치하지 않고도 이러한 테스트를 실행할 수 있습니다. 시작하려면 애플리케이션의 `compose.yaml` 파일에서 Selenium 서비스를 주석 해제하세요:

```yaml
selenium:
    image: 'selenium/standalone-chrome'
    extra_hosts:
      - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```



다음으로, 애플리케이션의 `compose.yaml` 파일에 있는 `laravel.test` 서비스가 `selenium`에 대한 `depends_on` 항목을 가지고 있는지 확인하세요:

```yaml
depends_on:
    - mysql
    - redis
    - selenium
```



마지막으로, Sail을 시작하고 `dusk` 명령어를 실행하여 Dusk 테스트 스위트를 실행할 수 있습니다:

```shell
sail dusk
```



<a name="selenium-on-apple-silicon"></a>
#### 애플 실리콘에서의 셀레늄

로컬 머신에 애플 실리콘 칩이 포함되어 있는 경우, `selenium` 서비스는 `selenium/standalone-chromium` 이미지를 사용해야 합니다:

```yaml
selenium:
    image: 'selenium/standalone-chromium'
    extra_hosts:
        - 'host.docker.internal:host-gateway'
    volumes:
        - '/dev/shm:/dev/shm'
    networks:
        - sail
```



<a name="previewing-emails"></a>
## 이메일 미리보기

Laravel Sail의 기본 `compose.yaml` 파일에는 [Mailpit](https://github.com/axllent/mailpit)에 대한 서비스 항목이 포함되어 있습니다. Mailpit은 로컬 개발 중에 애플리케이션에서 전송되는 이메일을 가로채고 브라우저에서 이메일 메시지를 미리볼 수 있는 편리한 웹 인터페이스를 제공합니다. Sail을 사용할 때, Mailpit의 기본 호스트는 `mailpit`이며 포트 1025를 통해 사용할 수 있습니다:

```ini
MAIL_HOST=mailpit
MAIL_PORT=1025
MAIL_ENCRYPTION=null
```



Sail이 실행 중일 때, 다음에서 Mailpit 웹 인터페이스에 접근할 수 있습니다: http://localhost:8025

Sail을 설치할 때 [Mailtrap Local](https://github.com/mailtrap/mailtrap-local) 서비스를 설치하도록 선택했거나, 나중에 `sail:add` Artisan 명령어를 사용하여 추가한 경우, 애플리케이션의 `compose.yaml` 파일에는 대신 이 이메일 캐처에 대한 항목이 포함됩니다. Mailtrap Local의 기본 호스트는 `mailtrap-local`이며 포트 3535를 통해 이용 가능합니다:

```ini
MAIL_HOST=mailtrap-local
MAIL_PORT=3535
```



Sail이 실행 중일 때, 다음에서 Mailtrap 로컬 웹 인터페이스에 접속할 수 있습니다: http://localhost:3550

<a name="sail-container-cli"></a>
## 컨테이너 CLI

때때로 애플리케이션의 컨테이너 안에서 Bash 세션을 시작하고 싶을 수 있습니다. `shell` 명령어를 사용하여 애플리케이션의 컨테이너에 연결할 수 있으며, 이를 통해 컨테이너 내의 파일과 설치된 서비스를 검사하고 임의의 셸 명령을 실행할 수 있습니다:

```shell
sail shell

sail root-shell
```



새 [Laravel Tinker](https://github.com/laravel/tinker) 세션을 시작하려면, 다음 `tinker` 명령을 실행할 수 있습니다:

```shell
sail tinker
```



<a name="sail-php-versions"></a>
## PHP 버전

Sail은 현재 PHP 8.5, 8.4, 8.3, 8.2, 8.1 또는 PHP 8.0을 통해 애플리케이션을 제공하는 것을 지원합니다. Sail에서 기본으로 사용하는 PHP 버전은 현재 PHP 8.5입니다. 애플리케이션을 제공하는 데 사용되는 PHP 버전을 변경하려면 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 컨테이너의 `build` 정의를 업데이트해야 합니다:

```yaml
# PHP 8.5
context: ./vendor/laravel/sail/runtimes/8.5

# PHP 8.4
context: ./vendor/laravel/sail/runtimes/8.4

# PHP 8.3
context: ./vendor/laravel/sail/runtimes/8.3

# PHP 8.2
context: ./vendor/laravel/sail/runtimes/8.2

# PHP 8.1
context: ./vendor/laravel/sail/runtimes/8.1

# PHP 8.0
context: ./vendor/laravel/sail/runtimes/8.0
```



또한, 애플리케이션에서 사용 중인 PHP 버전을 반영하도록 `image` 이름을 업데이트할 수 있습니다. 이 옵션은 애플리케이션의 `compose.yaml` 파일에도 정의되어 있습니다:

```yaml
image: sail-8.2/app
```



응용 프로그램의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다:

```shell
sail build --no-cache

sail up
```



<a name="sail-php-extensions"></a>
### 추가 PHP 확장

Sail의 런타임 이미지에는 일반적인 PHP 확장 세트가 포함되어 있습니다. 애플리케이션에서 추가 확장이 필요한 경우, 애플리케이션의 `compose.yaml` 파일에서 `laravel.test` 서비스에 공백으로 구분된 `PHP_EXTENSIONS` 빌드 인수를 추가하여 이미지를 빌드할 때 설치할 수 있습니다:

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        PHP_EXTENSIONS: 'gmp imagick'
```



응용 프로그램의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다.

<a name="sail-node-versions"></a>
## 노드 버전

Sail은 기본적으로 Node 24를 설치합니다. 이미지를 빌드할 때 설치되는 Node 버전을 변경하려면 응용 프로그램의 `compose.yaml` 파일에서 `laravel.test` 서비스의 `build.args` 정의를 업데이트할 수 있습니다.

```yaml
build:
    args:
        WWWGROUP: '${WWWGROUP}'
        NODE_VERSION: '18'
```



응용 프로그램의 `compose.yaml` 파일을 업데이트한 후에는 컨테이너 이미지를 다시 빌드해야 합니다:

```shell
sail build --no-cache

sail up
```



<a name="sharing-your-site"></a>
## 사이트 공유

때때로 동료에게 사이트를 미리 보여주거나 애플리케이션과의 웹훅 통합을 테스트하기 위해 사이트를 공개적으로 공유해야 할 수도 있습니다. 사이트를 공유하려면 `share` 명령을 사용할 수 있습니다. 이 명령을 실행한 후, 애플리케이션에 접속하는 데 사용할 수 있는 임의의 `laravel-sail.site` URL이 발급됩니다:

```shell
sail share
```



`share` 명령어를 통해 사이트를 공유할 때, 애플리케이션의 `bootstrap/app.php` 파일에서 `trustProxies` 미들웨어 메서드를 사용하여 애플리케이션의 신뢰할 수 있는 프록시를 구성해야 합니다. 그렇지 않으면 `url` 및 `route`와 같은 URL 생성 도우미가 URL 생성 시 사용해야 하는 올바른 HTTP 호스트를 결정할 수 없습니다:

```php
->withMiddleware(function (Middleware $middleware): void {
    $middleware->trustProxies(at: '*');
})
```



공유 사이트의 하위 도메인을 선택하고 싶다면, `share` 명령을 실행할 때 `subdomain` 옵션을 제공할 수 있습니다:

```shell
sail share --subdomain=my-sail-site
```



> [!NOTE]
> `share` 명령어는 [BeyondCode](https://beyondco.de)의 오픈 소스 터널링 서비스인 [Expose](https://github.com/beyondcode/expose)로 구동됩니다.

<a name="debugging-with-xdebug"></a>
## Xdebug로 디버깅하기

Laravel Sail의 Docker 구성에는 PHP용으로 인기 있고 강력한 디버거인 [Xdebug](https://xdebug.org/)에 대한 지원이 포함되어 있습니다. Xdebug를 활성화하려면 [Sail 구성을 게시했는지](#sail-customization) 확인하십시오. 그런 다음 애플리케이션의 `.env` 파일에 다음 변수를 추가하여 Xdebug를 구성합니다:

```ini
SAIL_XDEBUG_MODE=develop,debug,coverage
```



다음으로, 게시된 `php.ini` 파일에 Xdebug가 지정된 모드에서 활성화되도록 다음 구성이 포함되어 있는지 확인하세요:

```ini
[xdebug]
xdebug.mode=${XDEBUG_MODE}
```



`php.ini` 파일을 수정한 후에는 `php.ini` 파일에 대한 변경 사항이 적용되도록 Docker 이미지를 다시 빌드하는 것을 잊지 마세요:

```shell
sail build --no-cache
```



#### 리눅스 호스트 IP 구성

내부적으로, `XDEBUG_CONFIG` 환경 변수는 `client_host=host.docker.internal`로 정의되어 있어 Xdebug가 Mac과 Windows(WSL2)에서 제대로 구성되도록 합니다. 로컬 머신이 리눅스를 실행 중이고 Docker 20.10 이상을 사용하고 있다면, `host.docker.internal`를 사용할 수 있으며 수동 구성이 필요 없습니다.

Docker 버전이 20.10보다 오래된 경우, 리눅스에서는 `host.docker.internal`가 지원되지 않으므로 호스트 IP를 수동으로 정의해야 합니다. 이를 위해 `compose.yaml` 파일에서 사용자 지정 네트워크를 정의하여 컨테이너에 정적 IP를 구성하십시오:

```yaml
networks:
  custom_network:
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  laravel.test:
    networks:
      custom_network:
        ipv4_address: 172.20.0.2
```



정적 IP를 설정한 후, 애플리케이션의 .env 파일 내에서 SAIL_XDEBUG_CONFIG 변수를 정의하세요:

```ini
SAIL_XDEBUG_CONFIG="client_host=172.20.0.2"
```



<a name="xdebug-cli-usage"></a>
### Xdebug CLI 사용법

`sail debug` 명령은 Artisan 명령을 실행할 때 디버깅 세션을 시작하는 데 사용할 수 있습니다:

```shell
# Run an Artisan command without Xdebug...
sail artisan migrate

# Run an Artisan command with Xdebug...
sail debug migrate
```



<a name="xdebug-browser-usage"></a>
### Xdebug 브라우저 사용법

웹 브라우저를 통해 애플리케이션과 상호작용하면서 애플리케이션을 디버그하려면, 웹 브라우저에서 Xdebug 세션을 시작하는 방법에 대한 [Xdebug에서 제공하는 지침](https://xdebug.org/docs/step_debug#web-application)을 따르세요.

PhpStorm을 사용하는 경우, [제로 구성 디버깅](https://www.jetbrains.com/help/phpstorm/zero-configuration-debugging.html)에 관한 JetBrains 문서를 검토하세요.

> [!WARNING]
> Laravel Sail은 애플리케이션을 제공하기 위해 `artisan serve`에 의존합니다. Laravel 버전 8.53.0부터 `artisan serve` 명령은 `XDEBUG_CONFIG` 및 `XDEBUG_MODE` 변수만 허용합니다. 이전 버전의 Laravel(8.52.0 및 이전)은 이러한 변수를 지원하지 않으며 디버그 연결을 허용하지 않습니다.

<a name="sail-customization"></a>
## 사용자 정의

Sail은 단지 Docker이므로 거의 모든 것을 자유롭게 사용자 정의할 수 있습니다. Sail 자체 Dockerfile을 게시하려면 `sail:publish` 명령을 실행할 수 있습니다:

```shell
sail artisan sail:publish
```



이 명령을 실행하면 Laravel Sail에서 사용하는 Dockerfile 및 기타 구성 파일이 애플리케이션 루트 디렉토리의 `docker` 디렉토리에 배치됩니다. Sail 설치를 사용자 지정한 후에는 애플리케이션의 `compose.yaml` 파일에서 애플리케이션 컨테이너의 이미지 이름을 변경하고 싶을 수 있습니다. 그렇게 한 후에는 `build` 명령을 사용하여 애플리케이션의 컨테이너를 다시 빌드하십시오. 단일 머신에서 여러 Laravel 애플리케이션을 개발할 때 특히 애플리케이션 이미지에 고유한 이름을 지정하는 것이 중요합니다.

```shell
sail build --no-cache
```
{% endraw %}
