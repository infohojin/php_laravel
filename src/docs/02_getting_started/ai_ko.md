---
layout: docs
title: "AI 지원 개발"
---

{% raw %}
# AI 지원 개발

- [소개](#introduction)
     - [왜 Laravel을 AI 개발에 사용하나요?](#why-laravel-for-ai-development)
 - [라라벨 부스트](#laravel-boost)
     - [설치](#installation)
     - [사용 가능한 도구](#available-tools)
     - [AI 가이드라인](#ai-guidelines)
     - [에이전트 스킬](#agent-skills)
     - [문서 검색](#documentation-search)
     - [에이전트 통합](#agents-integration)

<a name="introduction"></a>
## 소개

Laravel은 AI 지원 및 에이전트 개발을 위한 최고의 프레임워크로 독보적인 위치에 있습니다. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenCode](https://opencode.ai), [Cursor](https://cursor.com) 및 [GitHub Copilot](https://github.com/features/copilot)과 같은 AI 코딩 에이전트의 등장은 개발자가 코드를 작성하는 방식을 변화시켰습니다. 이러한 도구는 전례 없는 속도로 전체 기능을 생성하고, 복잡한 문제를 디버깅하고, 코드를 리팩터링할 수 있습니다. 하지만 그 효과는 코드베이스를 얼마나 잘 이해하는지에 따라 크게 달라집니다.

<a name="why-laravel-for-ai-development"></a>
### AI 개발에 Laravel을 사용하는 이유는 무엇인가요?

Laravel의 독창적인 규칙과 잘 정의된 구조는 AI 지원 개발을 위한 이상적인 프레임워크를 만듭니다. AI 에이전트에 컨트롤러 추가를 요청하면 컨트롤러를 배치할 위치를 정확히 알고 있습니다. 새로운 마이그레이션이 필요할 때 명명 규칙과 파일 위치를 예측할 수 있습니다. 이러한 일관성은 보다 유연한 프레임워크에서 AI 도구를 작동시키지 못하는 추측을 제거합니다.

파일 구성 외에도 Laravel의 표현적인 구문과 포괄적인 문서는 AI 에이전트에게 정확하고 관용적인 코드를 생성하는 데 필요한 컨텍스트를 제공합니다. Eloquent 관계, 양식 요청, 미들웨어와 같은 기능은 에이전트가 안정적으로 이해하고 복제할 수 있는 패턴을 따릅니다. 그 결과는 일반적인 PHP 조각을 엮은 것이 아니라 노련한 Laravel 개발자가 작성한 것처럼 보이는 AI 생성 코드입니다.

<a name="laravel-boost"></a>
## 라라벨 부스트

[Laravel Boost](https://github.com/laravel/boost)는 AI 코딩 에이전트와 Laravel 애플리케이션 간의 격차를 해소합니다. Boost는 AI 에이전트에 애플리케이션의 구조, 데이터베이스, 경로 등에 대한 심층적인 통찰력을 제공하는 15개 이상의 전문 도구를 갖춘 MCP(모델 컨텍스트 프로토콜) 서버입니다. Boost를 설치하면 AI 에이전트가 범용 코드 도우미에서 특정 애플리케이션을 이해하는 Laravel 전문가로 변모합니다.

Boost는 애플리케이션 검사 및 상호 작용을 위한 MCP 도구 모음, Laravel 생태계를 위해 특별히 제작된 구성 가능한 AI 지침, 17,000개 이상의 Laravel 관련 지식이 포함된 강력한 문서 API라는 세 가지 주요 기능을 제공합니다.

<a name="installation"></a>
### 설치

Boost는 PHP 8.1 이상을 실행하는 Laravel 10, 11, 12 및 13 애플리케이션에 설치할 수 있습니다. 시작하려면 Boost를 개발 종속성으로 설치하십시오.

```shell
composer require laravel/boost --dev

```

설치가 완료되면 대화형 설치 프로그램을 실행합니다.

```shell
php artisan boost:install

```

설치 프로그램은 IDE 및 AI 에이전트를 자동으로 감지하므로 프로젝트에 적합한 통합을 선택할 수 있습니다. Boost는 MCP 호환 편집기용 `.mcp.json` 및 AI 컨텍스트용 지침 파일과 같은 필수 구성 파일을 생성합니다.

> [!NOTE]
> 각 개발자가 자신의 환경을 구성하기를 원하는 경우 `.mcp.json`, `CLAUDE.md` 및 `boost.json`와 같이 생성된 구성 파일을 `.gitignore`에 안전하게 추가할 수 있습니다.

<a name="available-tools"></a>
### 사용 가능한 도구

Boost는 Model Context Protocol을 통해 AI 에이전트에 포괄적인 도구 세트를 제공합니다. 이러한 도구를 통해 에이전트는 Laravel 애플리케이션을 깊이 이해하고 상호 작용할 수 있습니다.

<div class="content-list" markdown="1">

- **애플리케이션 내부 검사** - PHP 및 Laravel 버전을 쿼리하고, 설치된 패키지를 나열하고, 애플리케이션의 구성 및 환경 변수를 검사합니다.
- **데이터베이스 도구** - 대화를 종료하지 않고도 데이터베이스 스키마를 검사하고, 읽기 전용 쿼리를 실행하고, 데이터 구조를 이해할 수 있습니다.
- **경로 검사** - 미들웨어, 컨트롤러 및 매개변수와 함께 등록된 모든 경로를 나열합니다.
- **Artisan 명령** - 사용 가능한 Artisan 명령과 해당 인수를 검색하여 에이전트가 작업에 적합한 명령을 제안하고 실행할 수 있도록 합니다.
- **로그 분석** - 애플리케이션의 로그 파일을 읽고 분석하여 문제 디버깅에 도움을 줍니다.
- **브라우저 로그** - Laravel의 프런트엔드 도구를 사용하여 개발할 때 브라우저 콘솔 로그 및 오류에 액세스합니다.
- **Tinker 통합** - Laravel Tinker를 통해 애플리케이션 컨텍스트에서 PHP 코드를 실행하여 에이전트가 가설을 테스트하고 동작을 확인할 수 있도록 합니다.
- **문서 검색** - 설치된 패키지 버전에 맞는 결과로 Laravel 생태계 문서를 검색합니다.

</div>

<a name="ai-guidelines"></a>
### AI 지침

Boost에는 Laravel 생태계를 위해 특별히 제작된 포괄적인 AI 지침 세트가 포함되어 있습니다. 이 지침은 AI 에이전트에게 관용적인 Laravel 코드를 작성하고, 프레임워크 규칙을 따르고, 일반적인 함정을 피하는 방법을 가르칩니다. 지침은 구성 가능하고 버전을 인식하므로 에이전트는 정확한 패키지 버전에 적합한 지침을 받습니다.

Laravel 자체와 Laravel 생태계의 16개 이상의 패키지에 대한 지침이 제공됩니다.

<div class="content-list" markdown="1">

- 라이브와이어(2.x, 3.x, 4.x)
- Inertia.js(React, Svelte 및 Vue 변형)
- Tailwind CSS(3.x 및 4.x)
- 필라멘트(3.x 및 4.x)
- PHPUnit
- 해충 PHP
- 라라벨 파인트
- 그리고 더 많은 것

</div>

`boost:install`를 실행하면 Boost는 애플리케이션이 사용하는 패키지를 자동으로 감지하고 관련 지침을 프로젝트의 AI 컨텍스트 파일에 조합합니다.

<a name="agent-skills"></a>
### 상담원 기술

[에이전트 기술](https://agentskills.io/home)은 에이전트가 특정 도메인에서 작업할 때 필요에 따라 활성화할 수 있는 경량의 대상 지식 모듈입니다. 사전에 로드되는 지침과 달리 기술을 사용하면 관련성이 있는 경우에만 세부 패턴과 모범 사례를 로드할 수 있으므로 컨텍스트 부풀림이 줄어들고 AI 생성 코드의 관련성이 향상됩니다.

Livewire, Inertia, Tailwind CSS, Pest 등과 같은 인기 있는 Laravel 패키지에 대한 기술을 사용할 수 있습니다. `boost:install`를 실행하고 스킬을 기능으로 선택하면 `composer.json`에서 감지된 패키지를 기반으로 스킬이 자동으로 설치됩니다.

<a name="documentation-search"></a>
### 문서 검색

Boost에는 AI 에이전트가 17,000개 이상의 Laravel 생태계 문서에 액세스할 수 있는 강력한 문서 API가 포함되어 있습니다. 일반적인 웹 검색과 달리 이 문서는 정확한 패키지 버전과 일치하도록 색인화, 벡터화 및 필터링됩니다.

에이전트가 기능의 작동 방식을 이해해야 할 경우 Boost의 문서 API를 검색하여 정확한 버전별 정보를 받을 수 있습니다. 이는 이전 프레임워크 버전에서 더 이상 사용되지 않는 메서드나 구문을 제안하는 AI 에이전트의 일반적인 문제를 제거합니다.

<a name="agents-integration"></a>
### 에이전트 통합

Boost는 모델 컨텍스트 프로토콜을 지원하는 인기 있는 IDE 및 AI 도구와 통합됩니다. Cursor, Claude Code, Codex, Gemini CLI, GitHub Copilot 및 Junie에 대한 자세한 설정 지침은 Boost 설명서의 [에이전트 설정](/docs/{{version}}/boost#set-up-your-agents) 섹션을 참조하세요.
{% endraw %}
