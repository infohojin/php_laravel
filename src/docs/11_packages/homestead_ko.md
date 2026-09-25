---
layout: docs
title: "Laravel Homestead"
---

{% raw %}
# Laravel Homestead

- [Introduction](#introduction)
- [Installation and Setup](#installation-and-setup)
    - [First Steps](#first-steps)
    - [Configuring Homestead](#configuring-homestead)
    - [Configuring Nginx Sites](#configuring-nginx-sites)
    - [Configuring Services](#configuring-services)
    - [Launching the Vagrant Box](#launching-the-vagrant-box)
    - [Per Project Installation](#per-project-installation)
    - [Installing Optional Features](#installing-optional-features)
    - [Aliases](#aliases)
- [Updating Homestead](#updating-homestead)
- [Daily Usage](#daily-usage)
    - [Connecting via SSH](#connecting-via-ssh)
    - [Adding Additional Sites](#adding-additional-sites)
    - [Environment Variables](#environment-variables)
    - [Ports](#ports)
    - [PHP Versions](#php-versions)
    - [Connecting to Databases](#connecting-to-databases)
    - [Database Backups](#database-backups)
    - [Configuring Cron Schedules](#configuring-cron-schedules)
    - [Configuring Mailpit](#configuring-mailpit)
    - [Configuring Minio](#configuring-minio)
    - [Laravel Dusk](#laravel-dusk)
    - [Sharing Your Environment](#sharing-your-environment)
- [Debugging and Profiling](#debugging-and-profiling)
    - [Debugging Web Requests With Xdebug](#debugging-web-requests)
    - [Debugging CLI Applications](#debugging-cli-applications)
    - [Profiling Applications With Blackfire](#profiling-applications-with-blackfire)
- [Network Interfaces](#network-interfaces)
- [Extending Homestead](#extending-homestead)
- [Provider Specific Settings](#provider-specific-settings)
    - [VirtualBox](#provider-specific-virtualbox)

<a name="introduction"></a>
## Introduction

> [!WARNING]
> Laravel Homestead is a legacy package that is no longer actively maintained. [Laravel Sail](/docs/{{version}}/sail) may be used as a modern alternative.

Laravel strives to make the entire PHP development experience delightful, including your local development environment. [Laravel Homestead](https://github.com/laravel/homestead) is an official, pre-packaged Vagrant box that provides you a wonderful development environment without requiring you to install PHP, a web server, or any other server software on your local machine.

[Vagrant](https://www.vagrantup.com) provides a simple, elegant way to manage and provision Virtual Machines. Vagrant boxes are completely disposable. If something goes wrong, you can destroy and re-create the box in minutes!

Homestead runs on any Windows, macOS, or Linux system and includes Nginx, PHP, MySQL, PostgreSQL, Redis, Memcached, Node, and all of the other software you need to develop amazing Laravel applications.

> [!WARNING]
> If you are using Windows, you may need to enable hardware virtualization (VT-x). It can usually be enabled via your BIOS. If you are using Hyper-V on a UEFI system you may additionally need to disable Hyper-V in order to access VT-x.

<a name="included-software"></a>
### Included Software

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

<div id="software-list" markdown="1">

- Ubuntu 22.04
- Git
- PHP 8.3
- PHP 8.2
- PHP 8.1
- PHP 8.0
- PHP 7.4
- PHP 7.3
- PHP 7.2
- PHP 7.1
- PHP 7.0
- PHP 5.6
- Nginx
- MySQL 8.0
- lmm
- Sqlite3
- PostgreSQL 15
- Composer
- Docker
- Node (With Yarn, Bower, Grunt, and Gulp)
- Redis
- Memcached
- Beanstalkd
- Mailpit
- avahi
- ngrok
- Xdebug
- XHProf / Tideways / XHGui
- wp-cli

</div>

<a name="optional-software"></a>
### Optional Software

<style>
    #software-list > ul {
        column-count: 2; -moz-column-count: 2; -webkit-column-count: 2;
        column-gap: 5em; -moz-column-gap: 5em; -webkit-column-gap: 5em;
        line-height: 1.9;
    }
</style>

<div id="software-list" markdown="1">

- Apache
- Blackfire
- Cassandra
- Chronograf
- CouchDB
- Crystal & Lucky Framework
- Elasticsearch
- EventStoreDB
- Flyway
- Gearman
- Go
- Grafana
- InfluxDB
- Logstash
- MariaDB
- Meilisearch
- MinIO
- MongoDB
- Neo4j
- Oh My Zsh
- Open Resty
- PM2
- Python
- R
- RabbitMQ
- Rust
- RVM (Ruby Version Manager)
- Solr
- TimescaleDB
- Trader <small>(PHP extension)</small>
- Webdriver & Laravel Dusk Utilities

</div>

<a name="installation-and-setup"></a>
## Installation and Setup

<a name="first-steps"></a>
### First Steps

Before launching your Homestead environment, you must install [Vagrant](https://developer.hashicorp.com/vagrant/downloads) as well as one of the following supported providers:

- [VirtualBox 6.1.x](https://www.virtualbox.org/wiki/Download_Old_Builds_6_1)
- [Parallels](https://www.parallels.com/products/desktop/)



이 모든 소프트웨어 패키지는 모든 인기 운영체제에 사용하기 쉬운 시각적 설치 프로그램을 제공합니다.

Parallels 제공자를 사용하려면 [Parallels Vagrant 플러그인](https://github.com/Parallels/vagrant-parallels)을 설치해야 합니다. 무료입니다.

<a name="installing-homestead"></a>
#### 홈스테드 설치

Homestead 저장소를 호스트 컴퓨터에 복제하여 Homestead를 설치할 수 있습니다. 저장소를 "home" 디렉터리 내 `Homestead` 폴더에 복제하는 것을 고려하세요. Homestead 가상 머신은 모든 Laravel 애플리케이션의 호스트 역할을 합니다. 이 문서에서는 이 디렉터리를 "Homestead 디렉터리"라고 부릅니다:

```shell
git clone https://github.com/laravel/homestead.git ~/Homestead
```



Laravel Homestead 저장소를 클론한 후에는 `release` 브랜치를 체크아웃해야 합니다. 이 브랜치는 항상 Homestead의 최신 안정 버전을 포함하고 있습니다:

```shell
cd ~/Homestead

git checkout release
```



다음으로, Homestead 디렉토리에서 `bash init.sh` 명령을 실행하여 `Homestead.yaml` 구성 파일을 생성합니다. `Homestead.yaml` 파일은 Homestead 설치를 위한 모든 설정을 구성하는 곳입니다. 이 파일은 Homestead 디렉토리에 배치됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```



<a name="configuring-homestead"></a>
### 홈스테드 구성

<a name="setting-your-provider"></a>
#### 공급자 설정

`provider` 키는 `Homestead.yaml` 파일에서 사용할 Vagrant 공급자를 나타냅니다: `virtualbox` 또는 `parallels`:

provider: virtualbox

> [!WARNING]
> Apple Silicon을 사용하는 경우 Parallels 공급자가 필요합니다.

<a name="configuring-shared-folders"></a>
#### 공유 폴더 구성

`folders` 속성은 `Homestead.yaml` 파일에서 홈스테드 환경과 공유하려는 모든 폴더를 나열합니다. 이러한 폴더 내의 파일이 변경되면 로컬 머신과 홈스테드 가상 환경 간에 동기화됩니다. 필요한 만큼 많은 공유 폴더를 구성할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
```



> [!WARNING]
> Windows 사용자는 `~/` 경로 구문을 사용하지 말고 대신 프로젝트에 대한 전체 경로를 사용해야 합니다. 예: `C:\Users\user\Code\project1`.

개별 애플리케이션을 단일 큰 디렉터리에 매핑하는 대신 각 애플리케이션을 자체 폴더 매핑에 항상 매핑해야 합니다. 폴더를 매핑하면 가상 머신이 해당 폴더에 있는 *모든* 파일의 디스크 입출력을 추적해야 합니다. 폴더에 파일이 많으면 성능이 저하될 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
    - map: ~/code/project2
      to: /home/vagrant/project2
```



> [!WARNING]
> Homestead를 사용할 때 `.`(현재 디렉토리)을 마운트해서는 안 됩니다. 이렇게 하면 Vagrant가 현재 폴더를 `/vagrant`에 매핑하지 않아 선택적 기능이 작동하지 않거나 프로비저닝 중 예상치 못한 결과가 발생할 수 있습니다.

[NFS](https://developer.hashicorp.com/vagrant/docs/synced-folders/nfs)를 사용하려면 폴더 매핑에 `type` 옵션을 추가할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "nfs"
```



> [!WARNING]
> Windows에서 NFS를 사용할 때는 [vagrant-winnfsd](https://github.com/winnfsd/vagrant-winnfsd) 플러그인을 설치하는 것을 고려해야 합니다. 이 플러그인은 Homestead 가상 머신 내 파일과 디렉터리에 대한 올바른 사용자/그룹 권한을 유지합니다.

Vagrant의 [동기화 폴더](https://developer.hashicorp.com/vagrant/docs/synced-folders/basic_usage)에서 지원하는 모든 옵션도 `options` 키 아래에 나열하여 전달할 수 있습니다:

```yaml
folders:
    - map: ~/code/project1
      to: /home/vagrant/project1
      type: "rsync"
      options:
          rsync__args: ["--verbose", "--archive", "--delete", "-zz"]
          rsync__exclude: ["node_modules"]
```



<a name="configuring-nginx-sites"></a>
### Nginx 사이트 구성

Nginx에 익숙하지 않으신가요? 문제 없습니다. `Homestead.yaml` 파일의 `sites` 속성을 사용하면 Homestead 환경에서 폴더에 '도메인'을 쉽게 매핑할 수 있습니다. 샘플 사이트 구성은 `Homestead.yaml` 파일에 포함되어 있습니다. 다시 말하지만, 필요에 따라 Homestead 환경에 원하는 만큼의 사이트를 추가할 수 있습니다. Homestead는 작업 중인 모든 Laravel 애플리케이션에 대해 편리한 가상화 환경으로 사용할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
```



If you change the `sites` property after provisioning the Homestead virtual machine, you should execute the `vagrant reload --provision` command in your terminal to update the Nginx configuration on the virtual machine.

> [!WARNING]
> Homestead scripts are built to be as idempotent as possible. However, if you are experiencing issues while provisioning you should destroy and rebuild the machine by executing the `vagrant destroy && vagrant up` command.

<a name="hostname-resolution"></a>
#### Hostname Resolution

Homestead publishes hostnames using `mDNS` for automatic host resolution. If you set `hostname: homestead` in your `Homestead.yaml` file, the host will be available at `homestead.local`. macOS, iOS, and Linux desktop distributions include `mDNS` support by default. If you are using Windows, you must install [Bonjour Print Services for Windows](https://support.apple.com/kb/DL999?viewlocale=en_US&locale=en_US).

Using automatic hostnames works best for [per project installations](#per-project-installation) of Homestead. If you host multiple sites on a single Homestead instance, you may add the "domains" for your web sites to the `hosts` file on your machine. The `hosts` file will redirect requests for your Homestead sites into your Homestead virtual machine. On macOS and Linux, this file is located at `/etc/hosts`. On Windows, it is located at `C:\Windows\System32\drivers\etc\hosts`. The lines you add to this file will look like the following:

```text
192.168.56.56  homestead.test
```



나열된 IP 주소가 `Homestead.yaml` 파일에 설정된 것인지 확인하십시오. `hosts` 파일에 도메인을 추가하고 Vagrant 박스를 실행하면 웹 브라우저를 통해 사이트에 접근할 수 있습니다:

```shell
http://homestead.test
```



<a name="configuring-services"></a>
### 서비스 구성

Homestead는 기본적으로 여러 서비스를 시작합니다. 그러나 프로비저닝 중에 어떤 서비스를 활성화하거나 비활성화할지 사용자 정의할 수 있습니다. 예를 들어, `Homestead.yaml` 파일 내 `services` 옵션을 수정하여 PostgreSQL을 활성화하고 MySQL을 비활성화할 수 있습니다:

```yaml
services:
    - enabled:
        - "postgresql"
    - disabled:
        - "mysql"
```



지정된 서비스는 `enabled` 및 `disabled` 지시문에 있는 순서에 따라 시작되거나 중지됩니다.

<a name="launching-the-vagrant-box"></a>
### Vagrant 박스 시작하기

`Homestead.yaml`를 원하는 대로 편집한 후, Homestead 디렉토리에서 `vagrant up` 명령을 실행하세요. Vagrant는 가상 머신을 부팅하고 공유 폴더와 Nginx 사이트를 자동으로 구성합니다.

머신을 제거하려면 `vagrant destroy` 명령을 사용할 수 있습니다.

<a name="per-project-installation"></a>
### 프로젝트별 설치

Homestead를 전역적으로 설치하고 모든 프로젝트에서 동일한 Homestead 가상 머신을 공유하는 대신, 관리하는 각 프로젝트에 대해 Homestead 인스턴스를 구성할 수 있습니다. 프로젝트별로 Homestead를 설치하는 것은 프로젝트와 함께 `Vagrantfile`를 전송하고, 프로젝트의 저장소를 복제한 후 바로 `vagrant up`할 수 있도록 하려는 경우 유용할 수 있습니다.

Composer 패키지 관리자를 사용하여 프로젝트에 Homestead를 설치할 수 있습니다:

```shell
composer require laravel/homestead --dev
```



Homestead가 설치되면 Homestead의 `make` 명령어를 실행하여 프로젝트용 `Vagrantfile` 및 `Homestead.yaml` 파일을 생성합니다. 이 파일들은 프로젝트의 루트에 배치됩니다. `make` 명령어는 `Homestead.yaml` 파일 내에서 `sites` 및 `folders` 지시어를 자동으로 구성합니다:

```shell
# macOS / Linux...
php vendor/bin/homestead make

# Windows...
vendor\\bin\\homestead make
```



다음으로, 터미널에서 `vagrant up` 명령을 실행하고 브라우저에서 `http://homestead.test`에서 프로젝트에 접근하세요. 자동 [호스트명 해결](#hostname-resolution)을 사용하지 않는 경우, `homestead.test` 또는 원하는 도메인에 대한 `/etc/hosts` 파일 항목을 여전히 추가해야 한다는 점을 기억하세요.

<a name="installing-optional-features"></a>
### 선택적 기능 설치

선택적 소프트웨어는 `Homestead.yaml` 파일 내의 `features` 옵션을 사용하여 설치됩니다. 대부분의 기능은 불리언 값으로 활성화 또는 비활성화할 수 있으며, 일부 기능은 여러 구성 옵션을 허용합니다:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
    - cassandra: true
    - chronograf: true
    - couchdb: true
    - crystal: true
    - dragonflydb: true
    - elasticsearch:
        version: 7.9.0
    - eventstore: true
        version: 21.2.0
    - flyway: true
    - gearman: true
    - golang: true
    - grafana: true
    - influxdb: true
    - logstash: true
    - mariadb: true
    - meilisearch: true
    - minio: true
    - mongodb: true
    - neo4j: true
    - ohmyzsh: true
    - openresty: true
    - pm2: true
    - python: true
    - r-base: true
    - rabbitmq: true
    - rustc: true
    - rvm: true
    - solr: true
    - timescaledb: true
    - trader: true
    - webdriver: true
```



<a name="elasticsearch"></a>
#### Elasticsearch

You may specify a supported version of Elasticsearch, which must be an exact version number (major.minor.patch). The default installation will create a cluster named 'homestead'. You should never give Elasticsearch more than half of the operating system's memory, so make sure your Homestead virtual machine has at least twice the Elasticsearch allocation.

> [!NOTE]
> Check out the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current) to learn how to customize your configuration.

<a name="mariadb"></a>
#### MariaDB

Enabling MariaDB will remove MySQL and install MariaDB. MariaDB typically serves as a drop-in replacement for MySQL, so you should still use the `mysql` database driver in your application's database configuration.

<a name="mongodb"></a>
#### MongoDB

The default MongoDB installation will set the database username to `homestead` and the corresponding password to `secret`.

<a name="neo4j"></a>
#### Neo4j

The default Neo4j installation will set the database username to `homestead` and the corresponding password to `secret`. To access the Neo4j browser, visit `http://homestead.test:7474` via your web browser. The ports `7687` (Bolt), `7474` (HTTP), and `7473` (HTTPS) are ready to serve requests from the Neo4j client.

<a name="aliases"></a>
### Aliases

You may add Bash aliases to your Homestead virtual machine by modifying the `aliases` file within your Homestead directory:

```shell
alias c='clear'
alias ..='cd ..'
```



`aliases` 파일을 업데이트한 후에는 `vagrant reload --provision` 명령을 사용하여 Homestead 가상 머신을 다시 프로비저닝해야 합니다. 이렇게 하면 새 별칭이 머신에서 사용 가능하도록 보장됩니다.

<a name="updating-homestead"></a>
## Homestead 업데이트

Homestead 업데이트를 시작하기 전에, Homestead 디렉토리에서 다음 명령을 실행하여 현재 가상 머신을 제거했는지 확인해야 합니다:

```shell
vagrant destroy
```



다음으로, Homestead 소스 코드를 업데이트해야 합니다. 저장소를 클론했다면, 원래 저장소를 클론한 위치에서 다음 명령어를 실행할 수 있습니다:

```shell
git fetch

git pull origin release
```



이 명령어들은 GitHub 저장소에서 최신 Homestead 코드를 가져오고, 최신 태그를 가져온 다음, 최신 태그된 릴리스를 체크아웃합니다. 최신 안정 릴리스 버전은 Homestead의 [GitHub 릴리스 페이지](https://github.com/laravel/homestead/releases)에서 확인할 수 있습니다.

프로젝트의 `composer.json` 파일을 통해 Homestead를 설치한 경우, `composer.json` 파일에 `"laravel/homestead": "^12"`가 포함되어 있는지 확인하고 종속성을 업데이트해야 합니다:

```shell
composer update
```



다음으로, `vagrant box update` 명령어를 사용하여 Vagrant 박스를 업데이트해야 합니다:

```shell
vagrant box update
```



Vagrant 박스를 업데이트한 후에는 Homestead 디렉토리에서 `bash init.sh` 명령을 실행하여 Homestead의 추가 구성 파일을 업데이트해야 합니다. 기존 `Homestead.yaml`, `after.sh` 및 `aliases` 파일을 덮어쓸지 여부를 묻는 메시지가 표시됩니다:

```shell
# macOS / Linux...
bash init.sh

# Windows...
init.bat
```



마지막으로, 최신 Vagrant 설치를 활용하기 위해 Homestead 가상 머신을 재생성해야 합니다:

```shell
vagrant up
```



<a name="daily-usage"></a>
## 일일 사용

<a name="connecting-via-ssh"></a>
### SSH를 통한 연결

Homestead 디렉토리에서 `vagrant ssh` 터미널 명령어를 실행하여 가상 머신에 SSH로 접속할 수 있습니다.

<a name="adding-additional-sites"></a>
### 추가 사이트 추가

Homestead 환경이 프로비저닝되고 실행되면, 다른 Laravel 프로젝트를 위해 추가 Nginx 사이트를 추가할 수 있습니다. 단일 Homestead 환경에서 원하는 만큼 많은 Laravel 프로젝트를 실행할 수 있습니다. 추가 사이트를 추가하려면, 사이트를 `Homestead.yaml` 파일에 추가하십시오.

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
    - map: another.test
      to: /home/vagrant/project2/public
```



> [!WARNING]
> 사이트를 추가하기 전에 프로젝트 디렉토리에 대한 [폴더 매핑](#configuring-shared-folders)이 구성되어 있는지 확인해야 합니다.

Vagrant가 자동으로 "hosts" 파일을 관리하지 않는 경우, 새 사이트를 해당 파일에 추가해야 할 수도 있습니다. macOS 및 Linux에서는 이 파일이 `/etc/hosts`에 위치해 있습니다. Windows에서는 `C:\Windows\System32\drivers\etc\hosts`에 위치해 있습니다:

```text
192.168.56.56  homestead.test
192.168.56.56  another.test
```



사이트가 추가되면 Homestead 디렉토리에서 `vagrant reload --provision` 터미널 명령을 실행하세요.

<a name="site-types"></a>
#### 사이트 유형

Homestead는 Laravel 기반이 아닌 프로젝트도 쉽게 실행할 수 있는 여러 "유형"의 사이트를 지원합니다. 예를 들어, `statamic` 사이트 유형을 사용하여 Statamic 애플리케이션을 Homestead에 쉽게 추가할 수 있습니다:

```yaml
sites:
    - map: statamic.test
      to: /home/vagrant/my-symfony-project/web
      type: "statamic"
```



사용 가능한 사이트 유형은 다음과 같습니다: `apache`, `apache-proxy`, `apigility`, `expressive`, `laravel`(기본값), `proxy`(nginx용), `silverstripe`, `statamic`, `symfony2`, `symfony4`, `zf`입니다.

<a name="site-parameters"></a>
#### 사이트 매개변수

`params` 사이트 지시문을 통해 사이트에 추가 Nginx `fastcgi_param` 값을 추가할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      params:
          - key: FOO
            value: BAR
```



<a name="environment-variables"></a>
### 환경 변수

`Homestead.yaml` 파일에 추가하여 전역 환경 변수를 정의할 수 있습니다:

```yaml
variables:
    - key: APP_ENV
      value: local
    - key: FOO
      value: bar
```



`Homestead.yaml` 파일을 업데이트한 후에는 반드시 `vagrant reload --provision` 명령을 실행하여 머신을 다시 프로비저닝하십시오. 이렇게 하면 설치된 모든 PHP 버전에 대한 PHP-FPM 구성이 업데이트되고 `vagrant` 사용자 환경도 업데이트됩니다.

<a name="ports"></a>
### 포트

기본적으로 다음 포트가 Homestead 환경으로 전달됩니다:

<div class="content-list" markdown="1">

- **HTTP:** 8000 → 80으로 전달
- **HTTPS:** 44300 → 443으로 전달

</div>

<a name="forwarding-additional-ports"></a>
#### 추가 포트 전달

원하는 경우 `Homestead.yaml` 파일 내에서 `ports` 구성 항목을 정의하여 Vagrant 박스로 추가 포트를 전달할 수 있습니다. `Homestead.yaml` 파일을 업데이트한 후에는 반드시 `vagrant reload --provision` 명령을 실행하여 머신을 다시 프로비저닝하십시오:

```yaml
ports:
    - send: 50000
      to: 5000
    - send: 7777
      to: 777
      protocol: udp
```



아래는 호스트 머신에서 Vagrant 박스로 매핑할 수 있는 추가 Homestead 서비스 포트 목록입니다:

<div class="content-list" markdown="1">

- **SSH:** 2222 &rarr; 22로
- **ngrok UI:** 4040 &rarr; 4040으로
- **MySQL:** 33060 &rarr; 3306으로
- **PostgreSQL:** 54320 &rarr; 5432로
- **MongoDB:** 27017 &rarr; 27017로
- **Mailpit:** 8025 &rarr; 8025로
- **Minio:** 9600 &rarr; 9600으로

</div>

<a name="php-versions"></a>
### PHP 버전

Homestead는 동일한 가상 머신에서 여러 버전의 PHP를 실행하는 것을 지원합니다. 특정 사이트에서 사용할 PHP 버전을 `Homestead.yaml` 파일 내에서 지정할 수 있습니다. 사용 가능한 PHP 버전은 다음과 같습니다: "5.6", "7.0", "7.1", "7.2", "7.3", "7.4", "8.0", "8.1", "8.2", "8.3" (기본값):

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      php: "7.1"
```



[Homestead 가상 머신 내에서](#connecting-via-ssh), CLI를 통해 지원되는 모든 PHP 버전을 사용할 수 있습니다:

```shell
php5.6 artisan list
php7.0 artisan list
php7.1 artisan list
php7.2 artisan list
php7.3 artisan list
php7.4 artisan list
php8.0 artisan list
php8.1 artisan list
php8.2 artisan list
php8.3 artisan list
```



Homestead 가상 머신 내에서 다음 명령을 실행하여 CLI에서 사용되는 PHP의 기본 버전을 변경할 수 있습니다:

```shell
php56
php70
php71
php72
php73
php74
php80
php81
php82
php83
```



<a name="connecting-to-databases"></a>
### Connecting to Databases

A `homestead` database is configured for both MySQL and PostgreSQL out of the box. To connect to your MySQL or PostgreSQL database from your host machine's database client, you should connect to `127.0.0.1` on port `33060` (MySQL) or `54320` (PostgreSQL). The username and password for both databases is `homestead` / `secret`.

> [!WARNING]
> You should only use these non-standard ports when connecting to the databases from your host machine. You will use the default 3306 and 5432 ports in your Laravel application's `database` configuration file since Laravel is running _within_ the virtual machine.

<a name="database-backups"></a>
### Database Backups

Homestead can automatically backup your database when your Homestead virtual machine is destroyed. To utilize this feature, you must be using Vagrant 2.1.0 or greater. Or, if you are using an older version of Vagrant, you must install the `vagrant-triggers` plug-in. To enable automatic database backups, add the following line to your `Homestead.yaml` file:

```yaml
backup: true
```



한 번 구성되면, Homestead는 `vagrant destroy` 명령이 실행될 때 데이터베이스를 `.backup/mysql_backup` 및 `.backup/postgres_backup` 디렉토리로 내보냅니다. 이 디렉토리는 Homestead를 설치한 폴더나 [프로젝트별 설치](#per-project-installation) 방법을 사용하는 경우 프로젝트 루트에서 찾을 수 있습니다.

<a name="configuring-cron-schedules"></a>
### 크론 일정 구성

Laravel은 단일 `schedule:run` Artisan 명령을 매 분 실행하도록 스케줄링하여 [크론 작업을 예약](/docs/{{version}}/scheduling)하는 편리한 방법을 제공합니다. `schedule:run` 명령은 `routes/console.php` 파일에 정의된 작업 일정을 확인하여 실행할 예정인 스케줄된 작업을 결정합니다.

Homestead 사이트에서 `schedule:run` 명령을 실행하려면, 사이트를 정의할 때 `schedule` 옵션을 `true`로 설정할 수 있습니다:

```yaml
sites:
    - map: homestead.test
      to: /home/vagrant/project1/public
      schedule: true
```



사이트용 크론 작업은 Homestead 가상 머신의 `/etc/cron.d` 디렉토리에 정의됩니다.

<a name="configuring-mailpit"></a>
### Mailpit 구성하기

[Mailpit](https://github.com/axllent/mailpit)은 발신 이메일을 가로채 수신자에게 실제로 보내지 않고도 검토할 수 있게 해줍니다. 시작하려면, 애플리케이션의 `.env` 파일을 다음 메일 설정으로 업데이트하십시오:

```ini
MAIL_MAILER=smtp
MAIL_HOST=localhost
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
```



Mailpit이 구성되면 `http://localhost:8025`에서 Mailpit 대시보드에 접근할 수 있습니다.

<a name="configuring-minio"></a>
### Minio 구성

[Minio](https://github.com/minio/minio)는 Amazon S3 호환 API를 가진 오픈 소스 객체 저장 서버입니다. Minio를 설치하려면 [features](#installing-optional-features) 섹션에서 `Homestead.yaml` 파일을 다음 구성 옵션으로 업데이트하십시오:

minio: true

기본적으로 Minio는 포트 9600에서 사용할 수 있습니다. `http://localhost:9600` 방문을 통해 Minio 제어판에 접근할 수 있습니다. 기본 액세스 키는 `homestead`이고, 기본 비밀 키는 `secretkey`입니다. Minio에 접근할 때는 항상 `us-east-1` 지역을 사용해야 합니다.

Minio를 사용하려면 `.env` 파일에 다음 옵션이 있는지 확인하십시오:

```ini
AWS_USE_PATH_STYLE_ENDPOINT=true
AWS_ENDPOINT=http://localhost:9600
AWS_ACCESS_KEY_ID=homestead
AWS_SECRET_ACCESS_KEY=secretkey
AWS_DEFAULT_REGION=us-east-1
```



Minio 기반 'S3' 버킷을 프로비저닝하려면 `Homestead.yaml` 파일에 `buckets` 지시문을 추가하십시오. 버킷을 정의한 후에는 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다:

```yaml
buckets:
    - name: your-bucket
      policy: public
    - name: your-private-bucket
      policy: none
```



지원되는 `policy` 값에는 `none`, `download`, `upload` 및 `public`가 포함됩니다.

<a name="laravel-dusk"></a>
### 라라벨 더스크(Laravel Dusk)

Homestead 내에서 [라라벨 더스크](/docs/{{version}}/dusk) 테스트를 실행하려면 Homestead 구성에서 [웹드라이버 기능](#installing-optional-features)을 활성화해야 합니다:

```yaml
features:
    - webdriver: true
```



`webdriver` 기능을 활성화한 후에는 터미널에서 `vagrant reload --provision` 명령을 실행해야 합니다.

<a name="sharing-your-environment"></a>
### 환경 공유하기

때때로 현재 작업 중인 내용을 동료나 고객과 공유하고 싶을 수 있습니다. Vagrant는 `vagrant share` 명령을 통해 이를 내장 지원하지만, `Homestead.yaml` 파일에 여러 사이트가 구성되어 있으면 작동하지 않습니다.

이 문제를 해결하기 위해, Homestead는 자체 `share` 명령을 포함합니다. 시작하려면, [SSH를 통해 Homestead 가상 머신에 접속](#connecting-via-ssh)한 후 `vagrant ssh`를 사용하여 `share homestead.test` 명령을 실행하십시오. 이 명령은 `Homestead.yaml` 구성 파일에서 `homestead.test` 사이트를 공유합니다. 다른 구성된 사이트 중 어느 것이든 `homestead.test` 대신 사용할 수 있습니다.

```shell
share homestead.test
```



명령을 실행한 후에는 활동 로그와 공유된 사이트에 대한 공개적으로 접근 가능한 URL이 포함된 Ngrok 화면이 나타납니다. 사용자 지정 지역, 하위 도메인 또는 기타 Ngrok 실행 옵션을 지정하려면 `share` 명령어에 추가할 수 있습니다:

```shell
share homestead.test -region=eu -subdomain=laravel
```



If you need to share content over HTTPS rather than HTTP, using the `sshare` command instead of `share` will enable you to do so.

> [!WARNING]
> Remember, Vagrant is inherently insecure and you are exposing your virtual machine to the Internet when running the `share` command.

<a name="debugging-and-profiling"></a>
## Debugging and Profiling

<a name="debugging-web-requests"></a>
### Debugging Web Requests With Xdebug

Homestead includes support for step debugging using [Xdebug](https://xdebug.org). For example, you can access a page in your browser and PHP will connect to your IDE to allow inspection and modification of the running code.

By default, Xdebug is already running and ready to accept connections. If you need to enable Xdebug on the CLI, execute the `sudo phpenmod xdebug` command within your Homestead virtual machine. Next, follow your IDE's instructions to enable debugging. Finally, configure your browser to trigger Xdebug with an extension or [bookmarklet](https://www.jetbrains.com/phpstorm/marklets/).

> [!WARNING]
> Xdebug causes PHP to run significantly slower. To disable Xdebug, run `sudo phpdismod xdebug` within your Homestead virtual machine and restart the FPM service.

<a name="autostarting-xdebug"></a>
#### Autostarting Xdebug

When debugging functional tests that make requests to the web server, it is easier to autostart debugging rather than modifying tests to pass through a custom header or cookie to trigger debugging. To force Xdebug to start automatically, modify the `/etc/php/7.x/fpm/conf.d/20-xdebug.ini` file inside your Homestead virtual machine and add the following configuration:

```ini
; If Homestead.yaml contains a different subnet for the IP address, this address may be different...
xdebug.client_host = 192.168.10.1
xdebug.mode = debug
xdebug.start_with_request = yes
```



<a name="debugging-cli-applications"></a>
### CLI 애플리케이션 디버깅

PHP CLI 애플리케이션을 디버깅하려면 Homestead 가상 머신 안에서 `xphp` 셸 별칭을 사용하세요:

```shell
xphp /path/to/script
```



<a name="profiling-applications-with-blackfire"></a>
### Blackfire로 애플리케이션 프로파일링하기

[Blackfire](https://blackfire.io/docs/introduction)는 웹 요청과 CLI 애플리케이션을 프로파일링하기 위한 서비스입니다. 이 서비스는 콜 그래프와 타임라인에서 프로파일 데이터를 보여주는 대화형 사용자 인터페이스를 제공합니다. 개발, 스테이징, 프로덕션 환경에서 사용할 수 있도록 설계되었으며 최종 사용자에게는 오버헤드가 없습니다. 또한 Blackfire는 코드와 `php.ini` 설정에 대해 성능, 품질, 보안 검사를 제공합니다.

[Blackfire Player](https://blackfire.io/docs/player/index)는 Blackfire와 함께 사용하여 프로파일링 시나리오를 스크립트화할 수 있는 오픈 소스 웹 크롤링, 웹 테스트 및 웹 스크래핑 애플리케이션입니다.

Blackfire를 활성화하려면 Homestead 구성 파일에서 "features" 설정을 사용하십시오:

```yaml
features:
    - blackfire:
        server_id: "server_id"
        server_token: "server_value"
        client_id: "client_id"
        client_token: "client_value"
```



Blackfire 서버 자격 증명과 클라이언트 자격 증명은 [Blackfire 계정이 필요합니다](https://blackfire.io/signup). Blackfire는 CLI 도구와 브라우저 확장을 포함하여 애플리케이션을 프로파일링할 수 있는 다양한 옵션을 제공합니다. 자세한 내용은 [Blackfire 문서를 확인하세요](https://blackfire.io/docs/php/integrations/laravel/index).

<a name="network-interfaces"></a>
## 네트워크 인터페이스

`Homestead.yaml` 파일의 `networks` 속성은 Homestead 가상 머신의 네트워크 인터페이스를 구성합니다. 필요한 만큼 인터페이스를 구성할 수 있습니다:

```yaml
networks:
    - type: "private_network"
      ip: "192.168.10.20"
```



[브리지](https://developer.hashicorp.com/vagrant/docs/networking/public_network) 인터페이스를 활성화하려면, 네트워크에 대해 `bridge` 설정을 구성하고 네트워크 유형을 `public_network`로 변경하십시오:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
```



DHCP을 사용하려면, 구성에서 `ip` 옵션을 제거하면 됩니다:

```yaml
networks:
    - type: "public_network"
      bridge: "en1: Wi-Fi (AirPort)"
```



네트워크가 사용하는 장치를 업데이트하려면 네트워크 구성에 `dev` 옵션을 추가할 수 있습니다. 기본 `dev` 값은 `eth0`입니다:

```yaml
networks:
    - type: "public_network"
      ip: "192.168.10.20"
      bridge: "en1: Wi-Fi (AirPort)"
      dev: "enp2s0"
```



<a name="extending-homestead"></a>
## 홈스테드 확장

홈스테드 디렉토리 루트에 있는 `after.sh` 스크립트를 사용하여 홈스테드를 확장할 수 있습니다. 이 파일 내에서 가상 머신을 적절히 구성하고 사용자화하는 데 필요한 모든 셸 명령을 추가할 수 있습니다.

홈스테드를 사용자화할 때, 우분투는 패키지의 원래 구성 파일을 유지할지 아니면 새 구성 파일로 덮어쓸지 물어볼 수 있습니다. 이를 피하려면 패키지를 설치할 때 다음 명령을 사용하여 홈스테드가 이전에 작성한 구성을 덮어쓰지 않도록 해야 합니다:

```shell
sudo apt-get -y \
    -o Dpkg::Options::="--force-confdef" \
    -o Dpkg::Options::="--force-confold" \
    install package-name
```



<a name="user-customizations"></a>
### 사용자 맞춤 설정

팀과 함께 Homestead를 사용할 때, 개인 개발 스타일에 맞게 Homestead를 조정하고 싶을 수 있습니다. 이를 위해 Homestead 디렉토리의 루트(같은 디렉토리에 `Homestead.yaml` 파일이 있는 위치)에 `user-customizations.sh` 파일을 생성할 수 있습니다. 이 파일 내에서 원하는 모든 맞춤 설정을 할 수 있지만, `user-customizations.sh`는 버전 관리에 포함되지 않아야 합니다.

<a name="provider-specific-settings"></a>
## 공급자 특정 설정

<a name="provider-specific-virtualbox"></a>
### VirtualBox

<a name="natdnshostresolver"></a>
#### `natdnshostresolver`

기본적으로 Homestead는 `natdnshostresolver` 설정을 `on`로 구성합니다. 이렇게 하면 Homestead가 호스트 운영 체제의 DNS 설정을 사용할 수 있습니다. 이 동작을 변경하고 싶다면 `Homestead.yaml` 파일에 다음 구성 옵션을 추가하십시오:

```yaml
provider: virtualbox
natdnshostresolver: 'off'
```
{% endraw %}
