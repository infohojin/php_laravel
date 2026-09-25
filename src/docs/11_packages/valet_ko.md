---
layout: docs
title: "라라벨 발렛"
---

{% raw %}
# 라라벨 발렛

- [소개](#introduction)
- [설치](#installation)
- 업그레이딩 발렛 (#upgrading-valet)
- 서빙 사이트 (#serving-sites)
- The “Park” Command(#the-park-command)
- The “Link” Command(#the-link-command)
- [TLS 로 사이트 보호](#securing-sites)
- 기본 사이트 서비스 (#serving-a-default-site)
- [Per-Site PHP Versions](#per-site-php-versions)
- [Sharing Sites](#sharing-sites)
- 로컬 네트워크에서 사이트 공유 (#sharing-sites-on-your-local-network)
- [사이트 특정 환경 변수](#site-specific-environment-variables)
- [프록시 서비스](#proxying-services)
- 커스텀 발렛 드라이버 (#custom-valet-drivers)
- [로컬 드라이버](#local-drivers)
- [기타 발렛 명령](#other-valet-commands)
- [발렛 디렉터리 및 파일](#valet-directories-and-files)
- 디스크 액세스 (#disk-access)

<a name="introduction"></a>
## 소개

> [!NOTE]
> macOS 또는 Windows 에서 Laravel 애플리케이션을 개발하는 더욱 쉬운 방법을 찾고 계신가요？ [Laravel Herd](https://herd.laravel.com) 를 확인해 보세요. Herd 에는 Valet, PHP, Composer 를 포함하여 Laravel 개발을 시작하는 데 필요한 모든 것이 포함되어 있습니다。

[Laravel Valet](https://github.com/laravel/valet) 는 macOS 미니멀리스트를 위한 개발 환경입니다. Laravel Valet 는 시스템이 시작될 때 항상 백그라운드에서 [Nginx](https://www.nginx.com/) 를 실행하도록 Mac 을 구성합니다. 그런 다음 [DnsMasq](https://en.wikipedia.org/wiki/Dnsmasq) 를 사용하여 `*.test` 도메인의 모든 요청을 프록시하여 로컬 시스템에 설치된 사이트를 가리킵니다。

즉， Valet 는 약 7MB 의 RAM 을 사용하는 매우 빠른 Laravel 개발 환경입니다. Valet 는 [Sail](/docs/{{version}}/sail) 또는 [Homestead](/docs/{{version}}/homestead) 의 완전한 대체품은 아니지만， 유연한 기본 사항을 원하거나， 극도의 속도를 선호하거나， 제한된 양의 RAM 이 있는 머신에서 작업하는 경우 훌륭한 대안을 제공합니다。

상자 밖에서 제공되는 Valet 지원에는 다음이 포함되지만 이에 국한되지 않습니다：

<style>
#종업원 지원 > ul {
column-count: 3; -moz-column-count: 3; -webkit-column-count: 3;
줄 높이: 1.9;
}
</style>

<div id="valet-support" markdown="1">



- [Laravel](https://laravel.com)
- [Bedrock](https://roots.io/bedrock/)
- [CakePHP 3](https://cakephp.org)
- [ConcreteCMS](https://www.concretecms.com/)
- [Contao](https://contao.org/en/)
- [Craft](https://craftcms.com)
- [Drupal](https://www.drupal.org/)
- [ExpressionEngine](https://www.expressionengine.com/)
- [Jigsaw](https://jigsaw.tighten.co)
- [Joomla](https://www.joomla.org/)
- [Katana](https://github.com/themsaid/katana)
- [Kirby](https://getkirby.com/)
- [Magento](https://magento.com/)
- [OctoberCMS](https://octobercms.com/)
- [Sculpin](https://sculpin.io/)
- [Slim](https://www.slimframework.com)
- [Statamic](https://statamic.com)
- 정적 HTML
- [Symfony](https://symfony.com)
- [WordPress](https://wordpress.org)
- [Zend](https://framework.zend.com)

</div>

그러나, 당신은 자신의 [맞춤 드라이버](#custom-valet-drivers)로 Valet를 확장할 수 있습니다.

<a name="installation"></a>
## 설치

> [!WARNING]
> Valet는 macOS와 [Homebrew](https://brew.sh/)가 필요합니다. 설치 전에 Apache나 Nginx와 같은 다른 프로그램들이 로컬 머신의 포트 80을 사용하고 있지 않은지 확인해야 합니다.

시작하려면 먼저 `update` 명령어를 사용하여 Homebrew가 최신 상태인지 확인해야 합니다:

```shell
brew update
```



다음으로, Homebrew를 사용하여 PHP를 설치해야 합니다:

```shell
brew install php
```



PHP를 설치한 후에는 [Composer 패키지 관리자](https://getcomposer.org)를 설치할 준비가 된 것입니다. 또한 `$HOME/.composer/vendor/bin` 디렉토리가 시스템의 "PATH"에 있는지 확인해야 합니다. Composer가 설치된 후에는 Laravel Valet를 글로벌 Composer 패키지로 설치할 수 있습니다:

```shell
composer global require laravel/valet
```



마지막으로, Valet의 `install` 명령을 실행할 수 있습니다. 이 명령은 Valet과 DnsMasq를 구성하고 설치합니다. 또한 Valet가 의존하는 데몬들이 시스템 시작 시 실행되도록 구성됩니다:

```shell
valet install
```



Valet가 설치되면 터미널에서 `*.test` 도메인 중 하나에 `ping foobar.test`와 같은 명령어를 사용하여 핑을 시도해 보세요. Valet가 올바르게 설치되어 있다면 `127.0.0.1`에서 이 도메인이 응답하는 것을 볼 수 있습니다.

Valet는 컴퓨터가 부팅될 때마다 필요한 서비스를 자동으로 시작합니다.

<a name="php-versions"></a>
#### PHP 버전

> [!NOTE]
> 글로벌 PHP 버전을 변경하는 대신, `isolate` [명령어](#per-site-php-versions)를 통해 사이트별 PHP 버전을 사용하도록 Valet를 지시할 수 있습니다.

Valet는 `valet use php@version` 명령어를 사용하여 PHP 버전을 전환할 수 있습니다. Valet는 지정한 PHP 버전이 이미 설치되어 있지 않다면 Homebrew를 통해 설치할 것입니다:

```shell
valet use php@8.2

valet use php
```



프로젝트 루트에 `.valetrc` 파일을 생성할 수도 있습니다. `.valetrc` 파일에는 사이트가 사용할 PHP 버전을 포함해야 합니다:

```shell
php=php@8.2
```

이 파일이 생성되면 `valet use` 명령을 실행하기만 하면 됩니다. 이 명령은 파일을 읽어서 사이트에서 선호하는 PHP 버전을 결정합니다。

> [!WARNING]
> Valet 는 여러 PHP 버전이 설치되어 있더라도 한 번에 하나의 PHP 버전만 제공합니다。

<a name="database"></a>
#### 데이터베이스

애플리케이션에 데이터베이스가 필요한 경우 MySQL, PostgreSQL 및 Redis 를 포함하는 무료 올인원 데이터베이스 관리 도구인 [DBngin](https://dbngin.com) 을 확인하세요. DBngin 을 설치한 후 `root` 사용자 이름과 비밀번호로 사용되는 빈 문자열을 사용하여 `127.0.0.1` 에서 데이터베이스에 연결할 수 있습니다。

<a name="resetting-your-installation"></a>
#### 설치 재설정

Valet 설치를 제대로 실행하는 데 문제가 있는 경우 `composer global require laravel/valet` 명령을 실행한 다음 `valet install` 를 실행하면 설치가 재설정되고 다양한 문제를 해결할 수 있습니다. 드문 경우에는 `valet uninstall --force` 를 실행한 다음 `valet install` 를 실행하여 Valet 를 “하드 재설정” 해야 할 수 있습니다。

<a name="upgrading-valet"></a>
### 업그레이드 하인

터미널에서 `composer global require laravel/valet` 명령을 실행하여 Valet 설치를 업데이트할 수 있습니다. 업그레이드 후에는 필요한 경우 Valet 가 구성 파일을 추가로 업그레이드할 수 있도록 `valet install` 명령을 실행하는 것이 좋습니다。

<a name="upgrading-to-valet-4"></a>
#### 종자 4 로 업그레이드

Valet 3 에서 Valet 4 로 업그레이드하는 경우 Valet 설치를 올바르게 업그레이드하려면 다음 단계를 따르세요：

<div class="content-list" markdown="1">

- 사이트의 PHP 버전을 사용자 지정하기 위해 `.valetphprc` 파일을 추가한 경우， 각 `.valetphprc` 파일의 이름을 `.valetrc` 로 변경합니다. 그런 다음， `php=` 를 `.valetrc` 파일의 기존 콘텐츠에 추가합니다。
- 사용자 지정 드라이버를 업데이트하여 새 드라이버 시스템의 네임스페이스， 확장， 유형 힌트 및 반환 유형 힌트와 일치시킵니다. 예를 들어 Valet 의 [SampleValetDriver](https://github.com/laravel/valet/blob/d7787c025e60abc24a5195dc7d4c5c6f2d984339/cli/stubs/SampleValetDriver.php) 를 참조할 수 있습니다。
- PHP 7.1 - 7.4 를 사용하여 사이트를 서비스하는 경우， 홈브루를 사용하여 8.0 이상의 PHP 버전을 설치해야 합니다. 이 버전이 주 링크된 버전이 아니더라도 Valet 가 이 버전을 사용하여 일부 스크립트를 실행하기 때문입니다。

</div>

<a name="serving-sites"></a>
## 서비스 사이트



Valet이 설치되면, Laravel 애플리케이션을 제공할 준비가 된 것입니다. Valet은 애플리케이션을 제공하는 데 도움이 되는 두 가지 명령어를 제공합니다: `park` 및 `link`.

<a name="the-park-command"></a>
### `park` 명령어

`park` 명령어는 애플리케이션이 포함된 디렉토리를 컴퓨터에 등록합니다. 디렉토리가 Valet로 "주차(park)"되면, 해당 디렉토리 내의 모든 디렉토리는 웹 브라우저에서 `http://<directory-name>.test`를 통해 접근할 수 있습니다:

```shell
cd ~/Sites

valet park
```



그게 전부입니다. 이제 'parked' 디렉토리 내에서 생성하는 모든 애플리케이션은 `http://<directory-name>.test` 규칙을 사용하여 자동으로 제공됩니다. 따라서, 당신의 parked 디렉토리에 'laravel'이라는 디렉토리가 포함되어 있다면, 해당 디렉토리 내의 애플리케이션은 `http://laravel.test`에서 접근할 수 있습니다. 추가로, Valet는 와일드카드 하위 도메인(`http://foo.laravel.test`)을 사용하여 사이트에 접근할 수 있게 자동으로 허용합니다.

<a name="the-link-command"></a>
### `link` 명령어

`link` 명령어는 또한 당신의 Laravel 애플리케이션을 제공하는 데 사용할 수 있습니다. 이 명령어는 디렉토리 전체가 아닌 단일 사이트를 제공하고 싶을 때 유용합니다:

```shell
cd ~/Sites/laravel

valet link
```



한 번 애플리케이션이 `link` 명령어를 사용하여 Valet에 연결되면, 해당 디렉터리 이름을 사용하여 애플리케이션에 접근할 수 있습니다. 따라서 위 예제에서 연결된 사이트는 `http://laravel.test`에서 접근할 수 있습니다. 또한, Valet는 와일드카드 하위 도메인(`http://foo.laravel.test`)을 사용하여 사이트에 접근할 수 있도록 자동으로 허용합니다.

애플리케이션을 다른 호스트 이름에서 제공하고 싶다면, `link` 명령어에 호스트 이름을 전달할 수 있습니다. 예를 들어, 다음 명령어를 실행하여 애플리케이션을 `http://application.test`에서 사용할 수 있도록 할 수 있습니다:

```shell
cd ~/Sites/laravel

valet link application
```



물론, `link` 명령을 사용하여 서브도메인에서도 애플리케이션을 제공할 수 있습니다:

```shell
valet link api.application
```



모든 연결된 디렉터리 목록을 표시하려면 `links` 명령을 실행할 수 있습니다:

```shell
valet links
```



`unlink` 명령은 사이트의 심볼릭 링크를 삭제하는 데 사용할 수 있습니다:

```shell
cd ~/Sites/laravel

valet unlink
```



<a name="securing-sites"></a>
### TLS로 사이트 보안하기

기본적으로 Valet은 사이트를 HTTP를 통해 제공합니다. 그러나 HTTP/2를 사용하는 암호화된 TLS를 통해 사이트를 제공하고 싶다면, `secure` 명령어를 사용할 수 있습니다. 예를 들어, 사이트가 `laravel.test` 도메인에서 Valet에 의해 제공되고 있다면, 다음 명령어를 실행하여 사이트를 보안해야 합니다:

```shell
valet secure laravel
```



사이트를 '보안 해제'하고 트래픽을 일반 HTTP를 통해 다시 제공하려면 `unsecure` 명령을 사용하십시오. `secure` 명령과 마찬가지로 이 명령은 보안 해제하려는 호스트 이름을 받습니다:

```shell
valet unsecure laravel
```



<a name="serving-a-default-site"></a>
### 기본 사이트 제공

때때로, 알 수 없는 `test` 도메인을 방문할 때 `404` 대신 Valet가 "기본" 사이트를 제공하도록 구성하고 싶을 수 있습니다. 이를 달성하기 위해, 기본 사이트로 제공되어야 하는 사이트의 경로를 포함하는 `default` 옵션을 `~/.config/valet/config.json` 구성 파일에 추가할 수 있습니다:

"default": "/Users/Sally/Sites/example-site",

<a name="per-site-php-versions"></a>
### 사이트별 PHP 버전

기본적으로, Valet는 사이트를 제공하기 위해 전역 PHP 설치를 사용합니다. 그러나 여러 사이트에서 다양한 PHP 버전을 지원해야 하는 경우, `isolate` 명령을 사용하여 특정 사이트가 사용할 PHP 버전을 지정할 수 있습니다. `isolate` 명령은 현재 작업 디렉토리에 있는 사이트에 대해 지정된 PHP 버전을 사용하도록 Valet를 구성합니다:

```shell
cd ~/Sites/example-site

valet isolate php@8.0
```



사이트 이름이 해당 사이트를 포함하는 디렉토리 이름과 일치하지 않는 경우, `--site` 옵션을 사용하여 사이트 이름을 지정할 수 있습니다:

```shell
valet isolate php@8.0 --site="site-name"
```



편의를 위해, 사이트에 설정된 PHP 버전에 따라 적절한 PHP CLI 또는 도구에 대한 호출을 대리하기 위해 `valet php`, `composer`, `which-php` 명령어를 사용할 수 있습니다:

```shell
valet php
valet composer
valet which-php
```



모든 격리된 사이트와 해당 사이트의 PHP 버전을 표시하려면 `isolated` 명령을 실행할 수 있습니다:

```shell
valet isolated
```



사이트를 Valet에 전역적으로 설치된 PHP 버전으로 되돌리려면, 사이트의 루트 디렉토리에서 `unisolate` 명령어를 실행할 수 있습니다:

```shell
valet unisolate
```



<a name="sharing-sites"></a>
## 사이트 공유

Valet에는 로컬 사이트를 전 세계와 공유할 수 있는 명령어가 포함되어 있어, 모바일 기기에서 사이트를 테스트하거나 팀원 및 클라이언트와 공유하는 쉬운 방법을 제공합니다.

기본적으로 Valet는 ngrok 또는 Expose를 통해 사이트를 공유하는 것을 지원합니다. 사이트를 공유하기 전에 `share-tool` 명령을 사용하여 Valet 구성을 업데이트하고, `ngrok`, `expose` 또는 `cloudflared`를 지정해야 합니다:

```shell
valet share-tool ngrok
```



도구를 선택하고 Homebrew(ngrok 및 cloudflared용) 또는 Composer(Expose용)를 통해 설치하지 않은 경우, Valet가 자동으로 설치하도록 안내합니다. 물론, 두 도구 모두 사이트를 공유하기 시작하기 전에 ngrok 또는 Expose 계정을 인증해야 합니다.

사이트를 공유하려면 터미널에서 사이트의 디렉토리로 이동한 다음 Valet의 `share` 명령을 실행하세요. 공개적으로 접근 가능한 URL이 클립보드에 복사되며, 이를 브라우저에 바로 붙여 넣거나 팀과 공유할 수 있습니다:

```shell
cd ~/Sites/laravel

valet share
```



사이트 공유를 중지하려면, `Control + C`를 누를 수 있습니다.

> [!WARNING]
> 사용자 지정 DNS 서버(`1.1.1.1`와 같은)를 사용하는 경우, ngrok 공유가 올바르게 작동하지 않을 수 있습니다. 만약 이 문제가 귀하의 컴퓨터에서 발생한다면, Mac의 시스템 설정을 열고, 네트워크 설정으로 들어가, 고급 설정을 열고, DNS 탭으로 이동하여 `127.0.0.1`를 첫 번째 DNS 서버로 추가하십시오.

<a name="sharing-sites-via-ngrok"></a>
#### Ngrok을 통한 사이트 공유

ngrok을 사용하여 사이트를 공유하려면 [ngrok 계정 생성](https://dashboard.ngrok.com/signup)과 [인증 토큰 설정](https://dashboard.ngrok.com/get-started/your-authtoken)이 필요합니다. 인증 토큰을 받으면, 해당 토큰으로 Valet 구성을 업데이트할 수 있습니다:

```shell
valet set-ngrok-token YOUR_TOKEN_HERE
```



> [!NOTE]
> `valet share --region=eu` 와 같은 추가 ngrok 매개변수를 share 명령에 전달할 수 있습니다. 자세한 내용은 [ngrok 문서](https://ngrok.com/docs) 를 참조하십시오。

<a name="sharing-sites-via-expose"></a>
#### Expose 를 통한 사이트 공유

Expose 를 사용하여 사이트를 공유하려면 [Expose 계정 생성](https://expose.dev/register) 및 [인증 토큰을 통해 Expose 로 인증](https://expose.dev/docs/getting-started/getting-your-token) 이 필요합니다。

지원되는 추가 명령줄 매개변수에 대한 정보는 [Expose documentation](https://expose.dev/docs) 를 참조하십시오。

<a name="sharing-sites-on-your-local-network"></a>
### 로컬 네트워크에서 사이트 공유

Valet 는 기본적으로 수신 트래픽을 내부 `127.0.0.1` 인터페이스로 제한하여 개발 머신이 인터넷의 보안 위험에 노출되지 않도록 합니다。

로컬 네트워크의 다른 디바이스가 시스템의 IP 주소 (예: `192.168.1.10/application.test`) 를 통해 시스템의 Valet 사이트에 액세스할 수 있도록 허용하려면， 해당 사이트에 대한 적절한 Nginx 구성 파일을 수동으로 편집하여 `listen` 지침의 제한을 제거해야 합니다. 포트 80 및 443 의 `listen` 지침에서 `127.0.0.1:` 접두사를 제거해야 합니다。

프로젝트에서 `valet secure` 를 실행하지 않은 경우 `/usr/local/etc/nginx/valet/valet.conf` 파일을 편집하여 모든 비 HTTPS 사이트에 대한 네트워크 액세스를 열 수 있습니다. 그러나 HTTPS 를 통해 프로젝트 사이트를 제공하는 경우 (사이트에 대해 `valet secure` 를 실행한 경우) `~/.config/valet/Nginx/app-name.test` 파일을 편집해야 합니다。

Nginx 구성을 업데이트한 후 `valet restart` 명령을 실행하여 구성 변경 사항을 적용합니다。

<a name="site-specific-environment-variables"></a>
## 사이트별 환경 변수

다른 프레임워크를 사용하는 일부 애플리케이션은 서버 환경 변수에 의존할 수 있지만 프로젝트 내에서 해당 변수를 구성할 방법을 제공하지 않습니다. Valet 을 사용하면 프로젝트의 루트 내에 `.valet-env.php` 파일을 추가하여 사이트별 환경 변수를 구성할 수 있습니다. 이 파일은 배열에 지정된 각 사이트에 대해 글로벌 `$_SERVER` 배열에 추가될 사이트/환경 변수 쌍의 배열을 반환해야 합니다：

```php
<?php

return [
    // Set $_SERVER['key'] to "value" for the laravel.test site...
    'laravel' => [
        'key' => 'value',
    ],

    // Set $_SERVER['key'] to "value" for all sites...
    '*' => [
        'key' => 'value',
    ],
];
```



<a name="proxying-services"></a>
## 프록시 서비스

때때로 Valet 도메인을 로컬 머신의 다른 서비스로 프록시하고 싶을 수 있습니다. 예를 들어, 가끔 Valet을 실행하면서 Docker에서 별도의 사이트를 실행해야 할 수도 있습니다. 하지만 Valet과 Docker는 동시에 포트 80에 바인드할 수 없습니다.

이 문제를 해결하기 위해 `proxy` 명령어를 사용하여 프록시를 생성할 수 있습니다. 예를 들어, 모든 트래픽을 `http://elasticsearch.test`에서 `http://127.0.0.1:9200`로 프록시할 수 있습니다:

```shell
# Proxy over HTTP...
valet proxy elasticsearch http://127.0.0.1:9200

# Proxy over TLS + HTTP/2...
valet proxy elasticsearch http://127.0.0.1:9200 --secure
```



`unproxy` 명령을 사용하여 프록시를 제거할 수 있습니다:

```shell
valet unproxy elasticsearch
```



프록시된 모든 사이트 구성을 나열하려면 `proxies` 명령어를 사용할 수 있습니다:

```shell
valet proxies
```



<a name="custom-valet-drivers"></a>
## 사용자 지정 밸릿 드라이버

Valet 에서 기본적으로 지원되지 않는 프레임워크 또는 CMS 에서 실행되는 PHP 애플리케이션에 서비스를 제공하기 위해 자체 Valet “드라이버” 를 작성할 수 있습니다. Valet 을 설치하면 `SampleValetDriver.php` 파일이 포함된 `~/.config/valet/Drivers` 디렉토리가 생성됩니다. 이 파일에는 사용자 지정 드라이버를 작성하는 방법을 보여주는 샘플 드라이버 구현이 포함되어 있습니다. 드라이버를 작성하려면 `serves`, `isStaticFile` 및 `frontControllerPath` 의 세 가지 방법만 구현해야 합니다。

세 가지 메서드 모두 `$sitePath`, `$siteName` 및 `$uri` 값을 인수로 받습니다. `$sitePath` 는 `/Users/Lisa/Sites/my-project` 와 같이 시스템에서 제공되는 사이트에 대한 완전한 정규화된 경로입니다. `$siteName` 는 도메인의 “호스트”/“사이트 이름” 부분 (`my-project`) 입니다. `$uri` 는 수신 요청 URI(`/foo/bar`) 입니다。

사용자 지정 Valet 드라이버를 완료한 후 `FrameworkValetDriver.php` 명명 규칙을 사용하여 `~/.config/valet/Drivers` 디렉토리에 배치합니다. 예를 들어 WordPress 용 사용자 지정 Valet 드라인을 작성하는 경우 파일 이름은 `WordPressValetDriver.php` 여야 합니다。

사용자 지정 Valet 드라이버가 구현해야 하는 각 메서드의 샘플 구현을 살펴보겠습니다。

<a name="the-serves-method"></a>
#### `serves` 방법

드라이버가 수신 요청을 처리해야 하는 경우 `serves` 메서드는 `true` 를 반환해야 합니다. 그렇지 않으면 메서드는 `false` 를 반환해야 합니다。 따라서 이 메서드 내에서 주어진 `$sitePath` 에 서비스하려는 유형의 프로젝트가 포함되어 있는지 확인해야 합니다。

예를 들어， `WordPressValetDriver` 를 작성한다고 가정해 보겠습니다. 우리의 `serves` 메서드는 다음과 같이 보일 수 있습니다：

```php
/**
 * Determine if the driver serves the request.
 */
public function serves(string $sitePath, string $siteName, string $uri): bool
{
    return is_dir($sitePath.'/wp-admin');
}
```



<a name="the-isstaticfile-method"></a>
#### `isStaticFile` 방법

`isStaticFile`은 들어오는 요청이 이미지나 스타일시트와 같은 "정적" 파일을 위한 것인지 확인해야 합니다. 파일이 정적이면, 이 메서드는 디스크의 정적 파일에 대한 전체 경로를 반환해야 합니다. 들어오는 요청이 정적 파일을 위한 것이 아니면, 메서드는 `false`를 반환해야 합니다.

```php
/**
 * Determine if the incoming request is for a static file.
 *
 * @return string|false
 */
public function isStaticFile(string $sitePath, string $siteName, string $uri)
{
    if (file_exists($staticFilePath = $sitePath.'/public/'.$uri)) {
        return $staticFilePath;
    }

    return false;
}
```



> [!WARNING]
> `serves` 메서드가 들어오는 요청에 대해 `true`를 반환하고 요청 URI가 `/`가 아닌 경우에만 `isStaticFile` 메서드가 호출됩니다.

<a name="the-frontcontrollerpath-method"></a>
#### `frontControllerPath` 메서드

`frontControllerPath` 메서드는 일반적으로 "index.php" 파일 또는 이에 상응하는 애플리케이션의 "프론트 컨트롤러"에 대한 전체 경로를 반환해야 합니다:

```php
/**
 * Get the fully resolved path to the application's front controller.
 */
public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
{
    return $sitePath.'/public/index.php';
}
```



<a name="local-drivers"></a>
### 로컬 드라이버

단일 애플리케이션에 대해 사용자 지정 Valet 드라이버를 정의하려면 애플리케이션 루트 디렉토리에 `LocalValetDriver.php` 파일을 생성하세요. 사용자 지정 드라이버는 기본 `ValetDriver` 클래스를 확장하거나 `LaravelValetDriver`와 같은 기존 애플리케이션 특정 드라이버를 확장할 수 있습니다:

```php
use Valet\Drivers\LaravelValetDriver;

class LocalValetDriver extends LaravelValetDriver
{
    /**
     * Determine if the driver serves the request.
     */
    public function serves(string $sitePath, string $siteName, string $uri): bool
    {
        return true;
    }

    /**
     * Get the fully resolved path to the application's front controller.
     */
    public function frontControllerPath(string $sitePath, string $siteName, string $uri): string
    {
        return $sitePath.'/public_html/index.php';
    }
}
```

<a name="other-valet-commands"></a>
## 기타 발렛 명령

<div class="overflow-auto">

| 명령 | 설명 |
| --- | --- |
| `valet list` | 모든 Valet 명령 목록을 표시합니다. |
| `valet diagnose` | Valet 디버깅을 지원하기 위한 출력 진단. |
| `valet directory-listing` | 디렉토리 나열 동작을 결정합니다. 기본값은 “꺼짐” 으로， 디렉토리에 대해 404 페이지를 렌더링합니다. |
`valet forget` “주차된” 디렉토리에서 이 명령을 실행하여 주차된 디렉토리 목록에서 제거합니다。
| `valet log` | Valet 의 서비스에서 작성된 로그 목록을 봅니다. |
`valet paths` 모든 “주차된” 경로를 봅니다。
| `valet restart` | Valet 데몬을 재시작합니다. |
| `valet start` | Valet 데몬을 시작합니다. |
| `valet stop` | Valet 데몬을 중지합니다. |
| `valet trust` | Brew 및 Valet 용 sudoers 파일을 추가하여 Valet 명령을 암호 입력 메시지 없이 실행할 수 있습니다. |
| `valet uninstall` | Valet 제거: 수동 제거 지침을 표시합니다. `--force` 옵션을 통해 Valet 의 모든 리소스를 공격적으로 삭제합니다. |

</div>

<a name="valet-directories-and-files"></a>
## 종업원 디렉터리 및 파일

Valet 환경의 문제를 해결할 때 다음 디렉터리 및 파일 정보가 유용할 수 있습니다：

#### `~/.config/valet`

Valet 의 모든 구성을 포함합니다. 이 디렉토리의 백업을 유지하고 싶을 수 있습니다。

#### `~/.config/valet/dnsmasq.d/`

이 디렉토리에는 DNSMasq 의 구성이 포함되어 있습니다。

#### `~/.config/valet/Drivers/`

이 디렉토리에는 Valet 의 드라이버가 포함되어 있습니다. 드라이버는 특정 프레임워크/CMS 가 제공되는 방식을 결정합니다。

#### `~/.config/valet/Nginx/`

이 디렉토리에는 Valet 의 모든 Nginx 사이트 구성이 포함되어 있습니다. 이러한 파일은 `install` 및 `secure` 명령을 실행할 때 재구축됩니다。

#### `~/.config/valet/Sites/`

이 디렉토리에는 여러분의 [연결된 프로젝트] 에 대한 모든 상징적 링크가 포함되어 있습니다 (#the-link-command).

#### `~/.config/valet/config.json`

이 파일은 Valet 의 마스터 구성 파일입니다。

#### `~/.config/valet/valet.sock`

이 파일은 Valet 의 Nginx 설치에서 사용하는 PHP-FPM 소켓입니다. 이는 PHP 가 올바르게 실행되는 경우에만 존재합니다。

#### `~/.config/valet/Log/fpm-php.www.log`

이 파일은 PHP 오류에 대한 사용자 로그입니다。

#### `~/.config/valet/Log/nginx-error.log`

이 파일은 Nginx 오류에 대한 사용자 로그입니다。

#### `/usr/local/var/log/php-fpm.log`

이 파일은 PHP-FPM 오류에 대한 시스템 로그입니다。

#### `/usr/local/var/log/nginx`

이 디렉토리에는 Nginx 액세스 및 오류 로그가 포함되어 있습니다。

#### `/usr/local/etc/php/X.X/conf.d`

이 디렉토리에는 다양한 PHP 구성 설정에 대한 `*.ini` 파일이 포함되어 있습니다。

#### `/usr/local/etc/php/X.X/php-fpm.d/valet-fpm.conf`

이 파일은 PHP-FPM 풀 구성 파일입니다。

#### `~/.composer/vendor/laravel/valet/cli/stubs/secure.valet.conf`

이 파일은 사이트에 대한 SSL 인증서를 구축하는 데 사용되는 기본 Nginx 구성입니다。

<a name="disk-access"></a>
### 디스크 접근

macOS 10.14 부터 [일부 파일 및 디렉토리에 대한 접근은 기본적으로 제한됩니다](https://manuals.info.apple.com/MANUALS/1000/MA1902/en_US/apple-platform-security-guide.pdf). 이러한 제한 사항에는 데스크탑， 문서 및 다운로드 디렉토리가 포함됩니다. 또한 네트워크 볼륨 및 제거 가능한 볼륨에 대한 접근이 제한됩니다. 따라서 Valet 는 사이트 폴더를 이러한 보호된 위치 외부에 위치시킬 것을 권장합니다。

그러나 이러한 위치 중 하나에서 사이트를 제공하려면 Nginx 에 “전체 디스크 액세스” 를 부여해야 합니다. 그렇지 않으면 Nginx 에서 서버 오류 또는 기타 예측할 수 없는 동작이 발생할 수 있습니다. 특히 정적 자산을 제공할 때 그렇습니다. 일반적으로 macOS 는 이러한 위치에 대한 Nginx 의 전체 액세스를 자동으로 요청합니다. 또는 `System Preferences` > `Security & Privacy` > `Privacy` 를 통해 `Full Disk Access` 를 선택하여 수동으로 이를 수행할 수 있습니다. 다음으로， 주 창 패널에서 모든 `nginx` 항목을 활성화합니다。
{% endraw %}
