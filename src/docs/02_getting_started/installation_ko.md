---
layout: docs
title: "설치"
---

{% raw %}
# 설치

- [Meet Laravel](#meet-laravel)
- [왜 라라벨？](#why-laravel)
- 라라벨 애플리케이션 만들기 (#creating-a-laravel-project)
- [인공지능 사용 시작하기](#getting-started-using-ai)
- [PHP 및 라라벨 설치 프로그램 설치](#installing-php)
- [애플리케이션 만들기](#creating-an-application)
- [초기 구성](#initial-configuration)
- [환경 기반 구성](#environment-based-configuration)
- [데이터베이스 및 이주](#databases-and-migrations)
- [디렉토리 구성](#directory-configuration)
- [Herd 를 사용한 설치](#installation-using-herd)
- [Herd on macOS](#herd-on-macos)
- [Herd on Windows](#herd-on-windows)
- [IDE 지원](#ide-support)
- [Laravel and AI](#laravel-and-ai)
- 라라벨 부스트 설치 (#installing-laravel-boost)
- [다음 단계](#next-steps)
- [Laravel the Full Stack Framework](#laravel-the-fullstack-framework)
- [Laravel the API 백엔드](#laravel-the-api-backend)

<a name="meet-laravel"></a>
## 라라벨 만나기

Laravel 은 표현력 있고 우아한 구문을 갖춘 웹 애플리케이션 프레임워크입니다. 웹 프레임워크는 애플리케이션 생성을 위한 구조와 출발점을 제공하므로， 우리가 세부 사항을 작업하는 동안 여러분은 놀라운 무언가를 만드는 데 집중할 수 있습니다。

Laravel 은 철저한 종속성 주입， 표현력 있는 데이터베이스 추상화 계층， 대기열 및 예약된 작업， 단위 및 통합 테스트 등과 같은 강력한 기능을 제공하면서도 놀라운 개발자 경험을 제공하기 위해 노력합니다。

PHP 웹 프레임워크를 처음 사용하든 수년간의 경험이 있든， Laravel 은 함께 성장할 수 있는 프레임워크입니다. 웹 개발자로서의 첫 번째 단계를 도와드리거나 전문성을 한 단계 더 끌어올릴 수 있도록 도와드리겠습니다. 무엇을 구축할 수 있을지 기대됩니다。

<a name="why-laravel"></a>
### 왜 라라벨인가？

웹 애플리케이션을 구축할 때 사용할 수 있는 다양한 도구와 프레임워크가 있습니다. 그러나 우리는 Laravel 이 현대적인 풀스택 웹 애플리케이션 구축에 가장 적합한 선택이라고 생각합니다。

#### 점진적 프레임워크

우리는 Laravel 을 “진보적” 프레임워크라고 부르는 것을 좋아합니다. 이는 Laravel 이 여러분과 함께 성장한다는 의미입니다. 웹 개발을 처음 시작하는 경우 Laravel 의 방대한 설명서， 가이드 및 [비디오 튜토리얼] 라이브러리 (https://laracasts.com) 를 통해 압도되지 않고 기술을 배울 수 있습니다。

선임 개발자인 경우 Laravel 은 [의존성 주입](/docs/{{version}}/container), [유닛 테스트](/docs/{{version}}/testing), [대기열](/docs/{{version}}/queues), [실시간 이벤트](/docs/{{version}}/broadcasting) 등을 위한 강력한 도구를 제공합니다. Laravel 은 전문 웹 애플리케이션 구축을 위해 미세 조정되어 있으며 엔터프라이즈 워크로드를 처리할 준비가 되어 있습니다。

#### 확장 가능한 프레임워크

Laravel 은 엄청나게 확장 가능합니다. PHP 의 확장 친화적인 특성과 Laravel 의 Redis 와 같은 빠른 분산 캐시 시스템에 대한 기본 지원 덕분에 Laravel 을 사용한 수평 확장은 간단합니다. 실제로 Laravel 애플리케이션은 매월 수억 건의 요청을 처리할 수 있도록 쉽게 확장되었습니다。

극단적인 확장이 필요하십니까？ [Laravel Cloud](https://cloud.laravel.com) 와 같은 플랫폼을 사용하면 Laravel 애플리케이션을 거의 무제한의 규모로 실행할 수 있습니다。

#### 에이전트 준비 프레임워크

Laravel 의 고집스러운 규약과 잘 정의된 구조는 커서 및 클로드 코드와 같은 도구를 사용하는 [AI 보조 개발](/docs/{{version}}/ai) 에 이상적인 프레임워크를 제공합니다. AI 에이전트에게 컨트롤러를 추가하라고 요청하면 컨트롤러를 정확히 어디에 배치해야 하는지 알고 있습니다. 새로운 마이그레이션이 필요할 때는 명명 규약과 파일 위치를 예측할 수 있습니다. 이러한 일관성은 보다 유연한 프레임워크에서 AI 도구를 종종 방해하는 추측을 제거합니다。

파일 구성 외에도 Laravel 의 표현력 있는 구문과 포괄적인 설명서는 AI 에이전트에게 정확하고 표현적인 코드를 생성하는 데 필요한 컨텍스트를 제공합니다. Eloquent 관계， 양식 요청 및 미들웨어와 같은 기능은 에이전트가 안정적으로 이해하고 복제할 수 있는 패턴을 따릅니다. 그 결과 AI 생성 코드는 일반적인 PHP 스니펫에서 조합된 것이 아니라 노련한 Laravel 개발자가 작성한 것처럼 보입니다。

라라벨이 AI 보조 개발에 완벽한 선택인 이유에 대해 자세히 알아보려면 [에이전트 개발] 설명서 (/docs/{{version}}/ai) 를 확인하세요。

#### 커뮤니티 프레임워크

Laravel 은 PHP 에코시스템의 최고 패키지를 결합하여 가장 강력하고 개발자 친화적인 프레임워크를 제공합니다. 또한 전 세계 수천 명의 재능 있는 개발자들이 [프레임워크에 기여했습니다](https://github.com/laravel/framework). 누가 알겠습니까？ 어쩌면 여러분도 Laravel 기여자가 될 수 있을지도 모릅니다。

<a name="creating-a-laravel-project"></a>
## Laravel 애플리케이션 생성

<a name="getting-started-using-ai"></a>
### AI 사용 시작하기



만약 당신이 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 또는 [OpenCode](https://opencode.ai)와 같은 AI 코딩 에이전트를 사용하고 있다면, 프로젝트를 시작하기 전에 에이전트에게 라라벨(Laravel) 전용 플레이북을 제공하는 프롬프트로 시작할 수 있습니다.

아래 프롬프트는 에이전트에게 라라벨 설치 지침을 어디에서 찾을 수 있는지, 무엇을 우선시해야 하는지, 선택을 아직 하지 않았을 때 어떻게 합리적인 기본값을 설정할지 알려줍니다. 시작하려면 이 프롬프트를 에이전트에 붙여 넣으십시오:

```text
I'm building a new Laravel application.

Fetch and follow the instructions from https://laravel.com/for/agents. Treat the returned Markdown as the source of truth for how to install and set up Laravel in this session.
```



에이전트가 지침을 읽은 후에는 단계별로 안내하고 설정이 Laravel의 기본값과 일치하도록 유지해야 합니다.

<a name="installing-php"></a>
### PHP 및 Laravel 설치 프로그램 설치

첫 번째 Laravel 애플리케이션을 만들기 전에 로컬 컴퓨터에 [PHP](https://php.net), [Composer](https://getcomposer.org), [Laravel 설치 프로그램](https://github.com/laravel/installer)이 설치되어 있는지 확인해야 합니다. 또한 애플리케이션의 프런트엔드 자산을 컴파일할 수 있도록 [Node 및 NPM](https://nodejs.org) 또는 [Bun](https://bun.sh/) 중 하나를 설치해야 합니다.

로컬 컴퓨터에 PHP와 Composer가 설치되어 있지 않은 경우, 다음 명령어를 사용하면 macOS, Windows 또는 Linux에서 PHP, Composer 및 Laravel 설치 프로그램을 설치할 수 있습니다:```shell tab=macOS
/bin/bash -c "$(curl -fsSL https://php.new/install/mac/8.5)"
```

```shell tab=Windows PowerShell
# Run as administrator...
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://php.new/install/windows/8.5'))
```

```shell tab=Linux
/bin/bash -c "$(curl -fsSL https://php.new/install/linux/8.5)"
```



위 명령어 중 하나를 실행한 후에는 터미널 세션을 재시작해야 합니다. `php.new`를 통해 PHP, Composer, Laravel 설치 프로그램을 설치한 후 업데이트하려면 터미널에서 해당 명령어를 다시 실행할 수 있습니다.

이미 PHP와 Composer가 설치되어 있는 경우, Composer를 통해 Laravel 설치 프로그램을 설치할 수 있습니다:

```shell
composer global require laravel/installer
```



> [!NOTE]
> 완전한 기능을 갖춘 그래픽 PHP 설치 및 관리 경험을 위해 [Laravel Herd](#installation-using-herd)를 확인하세요.

<a name="creating-an-application"></a>
### 애플리케이션 생성

PHP, Composer, Laravel 인스톨러를 설치한 후에는 새 Laravel 애플리케이션을 생성할 준비가 된 것입니다:

```shell
laravel new example-app
```



애플리케이션이 생성되면 `dev` Composer 스크립트를 사용하여 Laravel의 로컬 개발 서버, 큐 워커 및 Vite 개발 서버를 시작할 수 있습니다:

```shell
cd example-app
npm install && npm run build
composer run dev
```

개발 서버를 시작하면 웹 브라우저에서 [http://localhost:8000](http://localhost:8000) 에서 애플리케이션에 액세스할 수 있습니다. 그런 다음 [라라벨 에코시스템의 다음 단계를 시작하기](#next-steps) 를 시작할 준비가 되었습니다. 물론 [데이터베이스 구성](#databases-and-migrations) 을 수행하고 필요한 마이그레이션을 수행할 수도 있습니다。

> [!NOTE]
> Laravel 애플리케이션을 개발할 때 초기 단계를 원한다면 당사의 [스타터 키트](/docs/{{version}}/starter-kits) 중 하나를 사용하는 것을 고려하세요. Laravel 의 스타터 키트는 새로운 Laravel 애플리케이션을 위한 백엔드 및 프런트엔드 인증 스태프를 제공합니다。

<a name="initial-configuration"></a>
## 초기 구성

Laravel 프레임워크의 모든 구성 파일은 `config` 디렉토리에 저장됩니다. 각 옵션은 문서화되어 있으므로 자유롭게 파일을 검토하고 사용 가능한 옵션에 익숙해지세요。

Laravel 은 기본적으로 추가 구성이 거의 필요하지 않습니다. 자유롭게 개발을 시작할 수 있습니다！ 그러나 `config/app.php` 파일과 해당 설명서를 검토하고 싶을 수 있습니다. 애플리케이션에 따라 변경하고 싶을 수 있는 `url` 및 `locale` 와 같은 여러 옵션이 포함되어 있습니다。

<a name="environment-based-configuration"></a>
### 환경 기반 구성

Laravel 의 많은 구성 옵션 값은 애플리케이션이 로컬 시스템에서 실행되는지 프로덕션 웹 서버에서 실행되는지에 따라 달라질 수 있으므로， 애플리케이션의 루트에 존재하는 `.env` 파일을 사용하여 많은 중요한 구성 값이 정의됩니다。

애플리케이션을 사용하는 각 개발자/서버에 다른 환경 구성이 필요할 수 있으므로 `.env` 파일을 애플리케이션의 소스 제어에 커밋해서는 안 됩니다. 또한 이는 침입자가 소스 제어 저장소에 액세스할 경우 민감한 자격 증명이 노출될 수 있으므로 보안 위험이 될 수 있습니다。

> [!NOTE]
> `.env` 파일 및 환경 기반 구성에 대한 자세한 내용은 전체 [구성 문서](/docs/{{version}}/configuration#environment-configuration) 를 참조하십시오。

<a name="databases-and-migrations"></a>
### 데이터베이스와 마이그레이션

이제 Laravel 애플리케이션을 생성했으니， 데이터베이스에 일부 데이터를 저장하고 싶을 것입니다. 기본적으로 애플리케이션의 `.env` 구성 파일은 Laravel 이 SQLite 데이터베이스와 상호 작용할 것임을 지정합니다。



애플리케이션을 생성하는 동안, Laravel이 당신을 위해 `database/database.sqlite` 파일을 생성하고, 애플리케이션의 데이터베이스 테이블을 생성하기 위해 필요한 마이그레이션을 실행했습니다.

MySQL이나 PostgreSQL과 같은 다른 데이터베이스 드라이버를 사용하고 싶다면, `.env` 구성 파일을 업데이트하여 적절한 데이터베이스를 사용할 수 있습니다. 예를 들어 MySQL을 사용하고 싶다면, `.env` 구성 파일의 `DB_*` 변수를 다음과 같이 업데이트하십시오:

```ini
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=root
DB_PASSWORD=
```



SQLite가 아닌 다른 데이터베이스를 사용하기로 선택한 경우, 데이터베이스를 생성하고 애플리케이션의 [데이터베이스 마이그레이션](/docs/{{version}}/migrations)을 실행해야 합니다:

```shell
php artisan migrate
```



> [!NOTE]
> macOS 또는 Windows 에서 개발 중이고 MySQL, PostgreSQL 또는 Redis 를 로컬로 설치해야 하는 경우 [Herd Pro](https://herd.laravel.com/#plans) 또는 [DBngin](https://dbngin.com/) 사용을 고려하세요。

<a name="directory-configuration"></a>
### 디렉토리 구성

Laravel 은 항상 웹 서버에 대해 구성된 “웹 디렉토리” 의 루트에서 제공되어야 합니다. “웹 디렉토리” 의 하위 디렉토리에서 Laravel 애플리케이션을 제공하려고 시도하지 마십시오. 이를 시도하면 애플리케이션 내에 존재하는 민감한 파일이 노출될 수 있습니다。

<a name="installation-using-herd"></a>
## 가스레인지를 사용한 설치

[Laravel Herd](https://herd.laravel.com) 는 macOS 및 Windows 용 매우 빠른 네이티브 Laravel 및 PHP 개발 환경입니다. Herd 에는 PHP 및 Nginx 를 포함하여 Laravel 개발을 시작하는 데 필요한 모든 것이 포함되어 있습니다。

Herd 를 설치하면 Laravel 로 개발을 시작할 준비가 되었습니다. Herd 에는 `php`, `composer`, `laravel`, `expose`, `node`, `npm` 및 `nvm` 용 명령줄 도구가 포함되어 있습니다。

> [!NOTE]
> [Herd Pro](https://herd.laravel.com/#plans) 는 로컬 MySQL, Postgres 및 Redis 데이터베이스를 생성하고 관리하는 기능， 로컬 메일 보기 및 로그 모니터링과 같은 추가적인 강력한 기능으로 Herd 를 강화합니다。

<a name="herd-on-macos"></a>
### macOS 의 Herd

macOS 에서 개발하는 경우 [Herd 웹사이트](https://herd.laravel.com) 에서 Herd 설치 프로그램을 다운로드할 수 있습니다. 설치 프로그램은 최신 버전의 PHP 를 자동으로 다운로드하고 Mac 을 항상 백그라운드에서 [Nginx](https://www.nginx.com/) 를 실행하도록 구성합니다。

macOS 용 Herd 는 [dnsmasq](https://en.wikipedia.org/wiki/Dnsmasq) 를 사용하여 “주차된” 디렉토리를 지원합니다. 주차된 디렉토리의 모든 Laravel 애플리케이션은 Herd 에서 자동으로 제공됩니다. 기본적으로 Herd 는 `~/Herd` 에 주차된 디렉토리를 생성하며， 디렉토리 이름을 사용하여 `.test` 도메인의 이 디렉토리에 있는 모든 Laravel 앱에 액세스할 수 있습니다。

Herd 를 설치한 후 새로운 Laravel 애플리케이션을 생성하는 가장 빠른 방법은 Herd 와 함께 번들로 제공되는 Laravel CLI 를 사용하는 것입니다：

```shell
cd ~/Herd
laravel new my-app
cd my-app
herd open
```



물론， 시스템 트레이의 Herd 메뉴에서 열 수 있는 Herd 의 UI 를 통해 주차된 디렉터리와 기타 PHP 설정을 항상 관리할 수 있습니다。

Herd 에 대해 자세히 알아보려면 Herd 문서 (https://herd.laravel.com/docs) 를 확인하세요。

<a name="herd-on-windows"></a>
### Windows 의 Herd

Herd 웹사이트 (https://herd.laravel.com/windows) 에서 Herd 용 Windows 설치 프로그램을 다운로드할 수 있습니다. 설치가 완료되면 Herd 를 시작하여 온보딩 프로세스를 완료하고 Herd UI 에 처음으로 액세스할 수 있습니다。

Herd 의 시스템 트레이 아이콘을 왼쪽 클릭하면 Herd UI 에 액세스할 수 있습니다. 오른쪽 클릭하면 매일 필요한 모든 도구에 액세스할 수 있는 빠른 메뉴가 열립니다。

설치 중에 Herd 는 `%USERPROFILE%\Herd` 의 홈 디렉터리에 “주차된” 디렉터리를 생성합니다. 주차된 디렉터리의 모든 Laravel 애플리케이션은 Herd 에서 자동으로 제공되며， 디렉터리 이름을 사용하여 `.test` 도메인의 이 디렉터리에 있는 모든 Laravel 앱에 액세스할 수 있습니다。

Herd 를 설치한 후 새 Laravel 애플리케이션을 생성하는 가장 빠른 방법은 Herd 와 함께 번들로 제공되는 Laravel CLI 를 사용하는 것입니다. 시작하려면 Powershell 을 열고 다음 명령을 실행합니다：

```shell
cd ~\Herd
laravel new my-app
cd my-app
herd open
```



Windows용 [Herd 문서](https://herd.laravel.com/docs/windows)를 확인하여 Herd에 대해 더 배울 수 있습니다.

<a name="ide-support"></a>
## IDE 지원

Laravel 애플리케이션을 개발할 때 원하는 코드 편집기를 자유롭게 사용할 수 있습니다. [Laravel LSP](https://github.com/laravel/lsp)는 코드 완성, 호버 정보, 진단, 문서 링크, 정의로 이동, Laravel 및 Blade 코드에 대한 빠른 수정 등 프레임워크 인식 편집기 지원을 제공합니다.

Laravel LSP를 설치하려면 Composer를 통해 전역으로 설치하세요. Composer의 전역 벤더 bin 디렉토리가 `PATH`에 있는지 확인하세요.

```shell
composer global require laravel/lsp
```

경량 및 확장 가능한 편집기를 찾고 있다면， [VS Code](https://code.visualstudio.com) 또는 [Cursor](https://cursor.com) 와 공식 [Laravel VS Code Extension](https://marketplace.visualstudio.com/items?itemName=laravel.vscode-laravel) 을 결합하여 구문 강조 표시， 스니펫， 아티잔 명령 통합 및 자동 Laravel LSP 지원을 제공합니다. 공식 Laravel 확장은 [Sublime Text](https://github.com/laravel/sublime-extension) 및 [Zed](https://github.com/laravel/zed-extension) 에서도 사용할 수 있습니다. Neovim 및 OpenCode 를 포함한 다른 언어 서버 호환 편집기의 설정 지침은 [Laravel LSP 리포지토리](https://github.com/laravel/lsp) 를 참조하십시오。

Laravel 에 대한 광범위하고 강력한 지원을 위해 JetBrains IDE 인 [PhpStorm](https://www.jetbrains.com/phpstorm/laravel/?utm_source=laravel.com&utm_medium=link&utm_campaign=laravel-2025&utm_content=partner&ref=laravel-2025) 을 살펴보세요. PhpStorm 의 내장된 Laravel 프레임워크 지원에는 Blade 템플릿， Eloquent 모델， 경로， 뷰， 번역 및 구성 요소에 대한 스마트 자동 완성， 그리고 Laravel 프로젝트 전반에 걸친 강력한 코드 생성 및 탐색이 포함됩니다。

클라우드 기반 개발 경험을 원하는 사용자를 위해 [Firebase Studio](https://firebase.studio/) 는 브라우저에서 직접 Laravel 을 사용하여 구축할 수 있는 즉각적인 액세스를 제공합니다. 설정이 필요 없는 Firebase Studio 를 사용하면 어떤 디바이스에서든 Laravel 애플리케이션 구축을 쉽게 시작할 수 있습니다。

<a name="laravel-and-ai"></a>
## 라라벨과 AI

[Laravel Boost](https://github.com/laravel/boost) 는 AI 코딩 에이전트와 Laravel 애플리케이션 간의 격차를 해소하는 강력한 도구입니다. Boost 는 AI 에이전트에 Laravel 특정 컨텍스트， 도구 및 지침을 제공하여 Laravel 규약을 따르는 보다 정확한 버전별 코드를 생성할 수 있도록 합니다。

Laravel 애플리케이션에 Boost 를 설치하면 AI 에이전트가 사용 중인 패키지를 파악하고， 데이터베이스를 쿼리하고， Laravel 설명서를 검색하고， 브라우저 로그를 읽고， 테스트를 생성하고， Tinker 를 통해 코드를 실행하는 등 15 개 이상의 전문 도구에 액세스할 수 있습니다。

또한 Boost 는 AI 에이전트에게 설치된 패키지 버전별로 17,000 개 이상의 벡터화된 Laravel 에코시스템 문서에 대한 액세스 권한을 제공합니다. 이는 에이전트가 프로젝트에서 사용하는 정확한 버전을 대상으로 지침을 제공할 수 있음을 의미합니다。



Boost에는 에이전트가 프레임워크 규칙을 따르고, 적절한 테스트를 작성하며, Laravel 코드를 생성할 때 흔히 발생하는 실수를 피하도록 돕는 Laravel 관리 AI 가이드라인도 포함되어 있습니다.

<a name="installing-laravel-boost"></a>
### Laravel Boost 설치

Boost는 PHP 8.1 이상을 실행하는 Laravel 10, 11, 12, 13 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발 의존성으로 설치하세요:

```shell
composer require laravel/boost --dev
```



설치가 완료되면, 대화형 설치 프로그램을 실행하십시오:

```shell
php artisan boost:install
```

설치 프로그램은 IDE 및 AI 에이전트를 자동으로 감지하므로 프로젝트에 적합한 기능을 선택할 수 있습니다. 부스트는 기존 프로젝트 규칙을 준수하며 기본적으로 독단적인 스타일 규칙을 적용하지 않습니다。

> [!NOTE]
> 부스트에 대해 자세히 알아보려면 [GitHub 의 Laravel Boost 리포지토리](https://github.com/laravel/boost) 를 확인하세요。

<a name="adding-custom-ai-guidelines"></a>
#### 맞춤형 AI 지침 추가

자체 사용자 지정 AI 지침으로 Laravel Boost 를 보강하려면 애플리케이션의 `.ai/guidelines/*` 디렉토리에 `.blade.php` 또는 `.md` 파일을 추가합니다. 이러한 파일은 `boost:install` 를 실행할 때 Laravel Boost 의 지침에 자동으로 포함됩니다。

<a name="next-steps"></a>
## 다음 단계

이제 Laravel 애플리케이션을 만들었으니， 다음에 무엇을 배워야 할지 궁금할 수 있습니다. 먼저， 다음 설명서를 읽어서 Laravel 의 작동 방식에 익숙해지는 것을 강력히 권장합니다：

<div class="content-list" markdown="1">

- [Request Lifecycle](/docs/{{version}}/lifecycle)
- [컨피그레이션](/docs/{{version}}/configuration)
- [디렉토리 구조](/docs/{{version}}/structure)
- Frontend(/docs/{{version}}/frontend)
- 서비스 컨테이너 (/docs/{{version}}/container)
- [Facades](/docs/{{version}}/facades)

</div>

Laravel 을 사용하는 방법도 여정의 다음 단계를 결정합니다. Laravel 을 사용하는 방법은 다양하며， 아래 프레임워크의 두 가지 주요 사용 사례를 살펴보겠습니다。

<a name="laravel-the-fullstack-framework"></a>
### 라라벨 풀 스택 프레임워크

Laravel 은 전체 스택 프레임워크로 사용될 수 있습니다. “전체 스택” 프레임워크란 라라벨을 사용하여 애플리케이션으로 요청을 라우팅하고 Blade templates(/docs/{{version}}/blade) 또는 Inertia(https://inertiajs.com) 와 같은 단일 페이지 애플리케이션 하이브리드 기술을 통해 프론트엔드를 렌더링하는 것을 의미합니다. 이는 Laravel 프레임워크를 사용하는 가장 일반적인 방법이며， 우리 의견으로는 Laravel 을 사용하는 가장 생산적인 방법입니다。

이러한 방식으로 Laravel 을 사용할 계획이라면 [프런트엔드 개발](/docs/{{version}}/frontend), [라우팅](/docs/{{version}}/routing), [뷰](/docs/{{version}}/views) 또는 [엘로퀀트 ORM](/docs/{{version}}/eloquent) 에 대한 설명서를 확인하는 것이 좋습니다. 또한 [Livewire](https://livewire.laravel.com) 및 [Inertia](https://inertiajs.com) 와 같은 커뮤니티 패키지에 대해 알아보는 것도 흥미로울 수 있습니다. 이러한 패키지를 사용하면 단일 페이지 JavaScript 애플리케이션이 제공하는 많은 UI 이점을 누리면서 Laravel 을 전체 스택 프레임워크로 사용할 수 있습니다。

전체 스택 프레임워크로 Laravel 을 사용하고 있다면 [Vite](/docs/{{version}}/vite) 를 사용하여 애플리케이션의 CSS 및 JavaScript 를 컴파일하는 방법을 배우는 것도 강력히 권장합니다。

> [!NOTE]
> 애플리케이션 구축을 빠르게 시작하고 싶다면 공식 애플리케이션 스타터 키트 (/docs/{{version}}/starter-kits) 중 하나를 확인하세요。

<a name="laravel-the-api-backend"></a>
### API 백엔드 라라벨

Laravel 은 JavaScript 단일 페이지 애플리케이션 또는 모바일 애플리케이션의 API 백엔드 역할도 할 수 있습니다. 예를 들어， 애플리케이션 [Next.js](https://nextjs.org) 의 API 백엔드로 Laravel 을 사용할 수 있습니다. 이 맥락에서 Laravel 을 사용하여 애플리케이션에 대한 [authentication](/docs/{{version}}/sanctum) 및 데이터 저장/검색을 제공하는 동시에 대기열， 이메일， 알림 등 Laravel 의 강력한 서비스를 활용할 수 있습니다。

라라벨을 이런 방식으로 사용할 계획이라면 [routing](/docs/{{version}}/routing), [Laravel Sanctum](/docs/{{version}}/sanctum), [Eloquent ORM](/docs/{{version}}/eloquent) 에 대한 설명서를 확인하시기 바랍니다。
{% endraw %}
