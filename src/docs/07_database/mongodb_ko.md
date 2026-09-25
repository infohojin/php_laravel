---
layout: docs
title: "MongoDB"
---

{% raw %}
# MongoDB

- [인트로듀션](#introduction)
- [설치](#installation)
- [MongoDB 드라이버](#mongodb-driver)
- [MongoDB 서버 시작](#starting-a-mongodb-server)
- [Install the Laravel MongoDB Package](#install-the-laravel-mongodb-package)
- [구성](#configuration)
- [기능](#features)

<a name="introduction"></a>
## 소개

[MongoDB](https://www.mongodb.com/resources/products/fundamentals/why-use-mongodb) 는 가장 인기 있는 NoSQL 문서 지향 데이터베이스 중 하나로， 높은 쓰기 로드 (분석 또는 IoT 에 유용) 와 높은 가용성 (자동 장애 조치를 통해 복제본 세트를 쉽게 설정) 에 사용됩니다. 또한 수평 확장성을 위해 데이터베이스를 쉽게 샤딩할 수 있으며， 집계， 텍스트 검색 또는 지리공간 쿼리를 수행하기 위한 강력한 쿼리 언어를 갖추고 있습니다。

SQL 데이터베이스와 같이 행이나 열로 구성된 테이블에 데이터를 저장하는 대신， MongoDB 데이터베이스의 각 레코드는 데이터의 이진 표현인 BSON 으로 설명된 문서입니다. 그런 다음 애플리케이션은 이 정보를 JSON 형식으로 검색할 수 있습니다. 이는 문서， 어레이， 내장된 문서 및 이진 데이터를 포함하여 다양한 데이터 유형을 지원합니다。

MongoDB 를 Laravel 과 함께 사용하기 전에 Composer 를 통해 `mongodb/laravel-mongodb` 패키지를 설치하고 사용하는 것이 좋습니다. `laravel-mongodb` 패키지는 MongoDB 에서 공식적으로 유지 관리하며， MongoDB 는 PHP 를 통해 MongoDB 드라이버를 통해 기본적으로 지원되지만 [Laravel MongoDB](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/) 패키지는 Eloquent 및 기타 Laravel 기능과의 더욱 풍부한 통합을 제공합니다：

```shell
composer require mongodb/laravel-mongodb

```

<a name="installation"></a>
## 설치

<a name="mongodb-driver"></a>
### MongoDB 드라이버

MongoDB 데이터베이스에 연결하려면 `mongodb` PHP 확장이 필요합니다. [Laravel Herd](https://herd.laravel.com)를 사용하여 로컬에서 개발하거나 `php.new`를 통해 PHP를 설치한 경우 이미 이 확장이 시스템에 설치되어 있습니다. 그러나 확장을 수동으로 설치해야 하는 경우 PECL을 통해 설치할 수 있습니다:

```shell
pecl install mongodb

```

또는 공식 PHP 확장 설치 프로그램인 [PIE](https://github.com/php/pie)를 사용하여 확장을 설치할 수 있습니다:

```shell
pie install mongodb/mongodb-extension

```

MongoDB PHP 확장 설치에 대한 자세한 정보는 [MongoDB PHP 확장 설치 지침](https://www.php.net/manual/en/mongodb.installation.php)을 참조하세요.

<a name="starting-a-mongodb-server"></a>
### MongoDB 서버 시작하기

MongoDB Community Server는 로컬에서 MongoDB를 실행하는 데 사용할 수 있으며, Windows, macOS, Linux에서 설치하거나 Docker 컨테이너로도 사용할 수 있습니다. MongoDB 설치 방법을 배우려면 [공식 MongoDB Community 설치 가이드](https://docs.mongodb.com/manual/administration/install-community/)를 참조하십시오.

MongoDB 서버에 대한 연결 문자열은 `.env` 파일에서 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb://localhost:27017"
MONGODB_DATABASE="laravel_app"

```

클라우드에서 MongoDB를 호스팅하려면 [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)를 사용하는 것을 고려하세요.
애플리케이션에서 로컬로 MongoDB Atlas 클러스터에 접속하려면 클러스터의 네트워크 설정에서 [자신의 IP 주소를 프로젝트의 IP 접근 목록에 추가](https://www.mongodb.com/docs/atlas/security/add-ip-address-to-list/)해야 합니다.

MongoDB Atlas의 연결 문자열은 `.env` 파일에도 설정할 수 있습니다:

```ini
MONGODB_URI="mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority"
MONGODB_DATABASE="laravel_app"

```

<a name="install-the-laravel-mongodb-package"></a>
### 라라벨 MongoDB 패키지 설치

마지막으로, Composer를 사용하여 라라벨 MongoDB 패키지를 설치합니다:

```shell
composer require mongodb/laravel-mongodb

```

> [!NOTE]
> 이 패키지의 설치는 `mongodb` PHP 확장이 설치되지 않은 경우 실패합니다. PHP 구성은 CLI와 웹 서버 간에 다를 수 있으므로, 두 구성 모두에서 확장이 활성화되어 있는지 확인하십시오.

<a name="configuration"></a>
## 구성

애플리케이션의 `config/database.php` 구성 파일을 통해 MongoDB 연결을 구성할 수 있습니다. 이 파일 내에 `mongodb` 드라이버를 사용하는 `mongodb` 연결을 추가하십시오:

```php
'connections' => [
    'mongodb' => [
        'driver' => 'mongodb',
        'dsn' => env('MONGODB_URI', 'mongodb://localhost:27017'),
        'database' => env('MONGODB_DATABASE', 'laravel_app'),
    ],
],

```

<a name="features"></a>
## 기능

구성이 완료되면 애플리케이션에서 `mongodb` 패키지와 데이터베이스 연결을 사용하여 다양하고 강력한 기능을 활용할 수 있습니다：

- [Using Eloquent](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/eloquent-models/), 모델을 MongoDB 컬렉션에 저장할 수 있습니다. 표준 Eloquent 기능 외에도 Laravel MongoDB 패키지는 내장된 관계와 같은 추가 기능을 제공합니다. 또한 이 패키지는 원시 쿼리 및 집계 파이프라인과 같은 작업을 수행하는 데 사용할 수 있는 MongoDB 드라이버에 대한 직접 액세스를 제공합니다。
- [복잡한 쿼리 작성](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/query-builder/) 쿼리 빌더를 사용합니다。
- [유사성 / 벡터 검색](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/fundamentals/vector-search/) 은 벡터 내장 및 `vectorSearch` Eloquent 메서드를 사용합니다。
- `mongodb` [캐시 드라이버](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/cache/) 는 TTL 인덱스와 같은 MongoDB 기능을 사용하여 만료된 캐시 항목을 자동으로 지우도록 최적화되어 있습니다。
- `mongodb` 대기열 드라이버를 사용하는 [대기열 작업 배포 및 처리](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/queues/).
- [GridFS 에 파일 저장](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/filesystems/), [GridFS Adapter for Flysystem](https://flysystem.thephpleague.com/docs/adapter/gridfs/) 를 통해。
- `mongodb` Scout 엔진을 사용하는 [전체 텍스트 검색](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/scout/).
- 데이터베이스 연결 또는 Eloquent 를 사용하는 대부분의 타사 패키지는 MongoDB 와 함께 사용할 수 있습니다。

MongoDB 및 Laravel 사용 방법을 계속 배우려면 MongoDB 의 [빠른 시작 안내서](https://www.mongodb.com/docs/drivers/php/laravel-mongodb/current/quick-start/) 를 참조하세요。
{% endraw %}
