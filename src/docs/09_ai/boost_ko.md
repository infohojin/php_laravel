---
layout: docs
title: "라라벨 부스트"
---

{% raw %}
# 라라벨 부스트

- [소개](#introduction)
- [설치](#installation)
- 에이전트 설정 (#set-up-your-agents)
- [부스트 리소스 업데이트 유지](#keeping-boost-resources-updated)
- [MCP Server](#mcp-server)
- [사용 가능한 MCP 도구](#available-mcp-tools)
- [MCP 서버 수동 등록](#manually-registering-the-mcp-server)
- [AI 지침](#ai-guidelines)
- [사용 가능한 AI 지침](#available-ai-guidelines)
- [맞춤형 AI 지침 추가](#adding-custom-ai-guidelines)
- 오버라이딩 부스트 AI 가이드라인 (#overriding-boost-ai-guidelines)
- [서드파티 패키지 AI 가이드라인](#third-party-package-ai-guidelines)
- 에이전트 스킬스 (#agent-skills)
- [사용 가능 스킬](#available-skills)
- 커스텀 스킬스 (#custom-skills)
- 오버라이딩 스킬스 (#overriding-skills)
- [제 3 자 패키지 스킬](#third-party-package-skills)
- [Guidelines vs. Skills](#guidelines-vs-skills)
- [프로젝트 규칙](#project-rules)
- [녹음 규칙](#recording-rules)
- [애플리케이션 규칙 추론](#inferring-your-applications-conventions)
- [프로젝트 규칙 비활성화](#disabling-project-rules)
- [문서화 API](#documentation-api)
- [확장 부스트](#extending-boost)
- [기타 IDE/AI 에이전트에 대한 지원 추가](#adding-support-for-other-ides-ai-agents)

<a name="introduction"></a>
## 소개

Laravel Boost 는 AI 에이전트가 Laravel 모범 사례를 준수하는 고품질 Laravel 애플리케이션을 작성하는 데 도움이 되는 필수 지침과 에이전트 기술을 제공하여 AI 지원 개발을 가속화합니다。

Boost 는 또한 내장된 MCP 도구와 17,000 개 이상의 Laravel 특정 정보가 포함된 광범위한 지식 기반을 결합한 강력한 Laravel 에코시스템 문서 API 를 제공합니다. 이 모든 정보는 정확하고 컨텍스트 인식 결과를 위한 임베디드를 사용하는 의미 검색 기능으로 향상됩니다. Boost 는 Claude Code 및 Cursor 와 같은 AI 에이전트에게 이 API 를 사용하여 최신 Laravel 기능과 모범 사례에 대해 알아보도록 지시합니다。

<a name="installation"></a>
## 설치

Laravel Boost 는 Composer 를 통해 설치할 수 있습니다：

```shell
composer require laravel/boost --dev
```



다음으로, MCP 서버와 코딩 가이드라인을 설치하세요:

```shell
php artisan boost:install
```



`boost:install` 명령어는 설치 과정에서 선택한 코딩 에이전트를 위한 관련 에이전트 가이드라인 및 스킬 파일을 생성합니다.

Laravel Boost가 설치되면 Cursor, Claude Code 또는 선택한 AI 에이전트로 코딩을 시작할 준비가 된 것입니다.

> [!NOTE]
> 생성된 MCP 구성 파일(`.mcp.json`), 가이드라인 파일(`CLAUDE.md`, `AGENTS.md`, `junie/` 등), `boost.json` 구성 파일을 애플리케이션의 `.gitignore`에 자유롭게 추가하세요. 이 파일들은 `boost:install` 및 `boost:update` 실행 시 자동으로 재생성됩니다.

<a name="set-up-your-agents"></a>
### 에이전트 설정```text tab=Cursor
1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "/open MCP Settings"
3. Turn the toggle on for `laravel-boost`
```

```text tab=Claude Code
Claude Code support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

claude mcp add -s local -t stdio laravel-boost php artisan boost:mcp
```

```text tab=Codex
Codex support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

codex mcp add laravel-boost -- php "artisan" "boost:mcp"
```

```text tab=Gemini CLI
Gemini CLI support is typically enabled automatically. If you find it isn't, open a shell in the project's directory and run the following command:

gemini mcp add -s project -t stdio laravel-boost php artisan boost:mcp
```

```text tab=GitHub Copilot (VS Code)
1. Open the command palette (`Cmd+Shift+P` or `Ctrl+Shift+P`)
2. Press `enter` on "MCP: List Servers"
3. Arrow to `laravel-boost` and press `enter`
4. Choose "Start server"
```

```text tab=Junie
1. Press `shift` twice to open the command palette
2. Search "MCP Settings" and press `enter`
3. Check the box next to `laravel-boost`
4. Click "Apply" at the bottom right
```



<a name="keeping-boost-resources-updated"></a>
### Boost 리소스 업데이트 유지하기

설치된 Laravel 에코시스템 패키지의 최신 버전을 반영하도록 로컬 Boost 리소스(AI 가이드라인 및 스킬)를 주기적으로 업데이트하고 싶을 수 있습니다. 이를 위해 `boost:update` Artisan 명령어를 사용할 수 있습니다.

```shell
php artisan boost:update
```



이 과정을 Composer의 "post-update-cmd" 스크립트에 추가하여 자동화할 수도 있습니다:

```json
{
  "scripts": {
    "post-update-cmd": [
      "@php artisan boost:update --ansi"
    ]
  }
}
```



기본적으로 `boost:update` 명령어는 애플리케이션 내에 이미 게시된 기존 Boost 리소스만 업데이트합니다. 애플리케이션에서 새로 설치된 패키지를 Boost가 스캔하고 해당 지침과 기술을 게시하도록 하려면 `--discover` 옵션을 사용할 수 있습니다:

```shell
php artisan boost:update --discover
```



<a name="mcp-server"></a>
## MCP 서버

Laravel Boost 는 AI 에이전트가 Laravel 애플리케이션과 상호 작용할 수 있는 도구를 노출하는 MCP(모델 컨텍스트 프로토콜) 서버를 제공합니다. 이러한 도구는 에이전트에게 애플리케이션의 구조를 검사하고， 데이터베이스를 쿼리하며， 코드를 실행하는 등의 기능을 제공합니다。

<a name="available-mcp-tools"></a>
### 사용 가능한 MCP 도구

<div class="overflow-auto">

| 이름             |           
| —————————————————————————————————————————————————
| 애플리케이션 정보 | PHP 및 Laravel 버전， 데이터베이스 엔진， 버전이 있는 에코시스템 패키지 목록， 그리고 Eloquent 모델 읽기 |
| 브라우저 로그 | 브라우저의 로그 및 오류 읽기            
| 데이터베이스 연결 | 기본 연결을 포함하여 사용 가능한 데이터베이스 연결 검사 |
| 데이터베이스 쿼리 | 데이터베이스에 대한 쿼리 실행 |
| 데이터베이스 스키마 | 데이터베이스 스키マ 읽기 데이터베이스 스키마 읽기
| 절대 URL 가져오기 | 에이전트가 유효한 URL 을 생성할 수 있도록 상대 경로 URI 를 절대 URL 로 변환 |
| 마지막 오류 | 애플리케이션의 로그 파일에서 마지막 오류 읽기 |
| 로그 항목 읽기 | 마지막 N 개의 로그 항목 읽기 |
| 기록 규칙 | 내구성 있는 [프로젝트 규칙](#project-rules) 을 `.ai/rules` 에 기록하여 미래 에이전트가 상속할 수 있도록 합니다. |
| 문서 검색 | Laravel 에서 호스팅하는 문서 API 서비스를 쿼리하여 설치된 패키지를 기반으로 문서를 검색 |

</div>

<a name="manually-registering-the-mcp-server"></a>
### MCP 서버 수동 등록

때로는 Laravel Boost MCP 서버를 원하는 편집기에 수동으로 등록해야 할 수 있습니다. 다음 세부 사항을 사용하여 MCP 서버를 등록해야 합니다：

<table>
<tr><td><strong>Command</strong></td><td><code>php</code></td></tr>
<tr><td><strong>Args</strong></td><td><code>artisan 부스트: mcp</code></td></tr>
</table>

JSON 예시：

```json
{
    "mcpServers": {
        "laravel-boost": {
            "command": "php",
            "args": ["artisan", "boost:mcp"]
        }
    }
}
```

<a name="ai-guidelines"></a>
## AI 지침

AI 지침은 사전에 로드된 구성 가능한 지침 파일로， AI 에이전트에게 Laravel 에코시스템 패키지에 대한 필수적인 컨텍스트를 제공합니다. 이러한 지침에는 에이전트가 일관된 고품질 코드를 생성하는 데 도움이 되는 핵심 규약， 모범 사례 및 프레임워크별 패턴이 포함되어 있습니다。

<a name="available-ai-guidelines"></a>
### 사용 가능한 AI 지침

Laravel Boost 에는 다음 패키지 및 프레임워크에 대한 AI 지침이 포함되어 있습니다. `core` 지침은 모든 버전에 적용 가능한 특정 패키지에 대한 일반적이고 일반화된 AI 조언을 제공합니다。

<div class="overflow-auto">

| 패키지 | 지원되는 버전 |
| --------------- | -----------------------|
| Core & Boost | core             |
| Laravel Framework | core, 10.x, 11.x, 12.x, 13.x |
Livewire 코어， 2.x, 3.x, 4.x
| Flux UI 코어 | core, 프리， 프로 |
| 폴리오             Core            |
Herd        core            
| Inertia Laravel | core, 1.x, 2.x, 3.x |
Inertia React core, 1.x, 2.x, 3.x
Inertia Vue core, 1.x, 2.x, 3.x
Inertia Svelte core, 1.x, 2.x, 3.x
| MCP             core          
| Pennant 페넌트 코어 코어 코어 페넌트 페넌트
페스트 코어 코어， 3.x, 4.x 코어
| PHPUnit    core    core            
| Pint             core            |
| Sail             core           
| Tailwind CSS core , 3.x, 4.x |
| Livewire Volt | core             |
| 웨이파인더 코어 | core           |
| 강제 테스트 | 조건부    |

</div>

> ** 참고: ** AI 지침을 최신 상태로 유지하려면 [부스트 리소스 업데이트 유지](#keeping-boost-resources-updated) 섹션을 참조하세요。

<a name="adding-custom-ai-guidelines"></a>
### 맞춤형 AI 지침 추가

자체 사용자 지정 AI 지침으로 Laravel Boost 를 보강하려면 애플리케이션의 `.ai/guidelines/*` 디렉토리에 `.blade.php` 또는 `.md` 파일을 추가합니다. 이러한 파일은 `boost:install` 를 실행할 때 Laravel Boost 의 지침에 자동으로 포함됩니다。

<a name="overriding-boost-ai-guidelines"></a>
### 부스트 AI 지침 재정의

일치하는 파일 경로로 자체 사용자 지정 지침을 생성하여 Boost 의 기본 제공 AI 지침을 재정의할 수 있습니다. 기존 Boost 지침 경로와 일치하는 사용자 지정 가이드라인을 생성하면 Boost 가 기본 제공 가이드라인 대신 사용자 지정 버전을 사용합니다。



예를 들어, Boost의 "Inertia React v2 Form Guidance" 지침을 재정의하려면 `.ai/guidelines/inertia-react/2/forms.blade.php`에 파일을 생성하세요. `boost:install`를 실행하면 Boost는 기본 지침 대신 사용자의 맞춤 지침을 포함합니다.

<a name="third-party-package-ai-guidelines"></a>
### 서드파티 패키지 AI 지침

서드파티 패키지를 관리하며 Boost가 이에 대한 AI 지침을 포함하도록 하고 싶다면 패키지에 `resources/boost/guidelines/core.blade.php` 파일을 추가하면 됩니다. 사용자가 패키지에서 `php artisan boost:install`를 실행하면 Boost가 자동으로 지침을 불러옵니다.

AI 지침은 패키지가 수행하는 기능에 대한 간략한 개요를 제공하고, 필요한 파일 구조나 규칙을 설명하며, 주요 기능을 생성하거나 사용하는 방법(예제 명령어나 코드 스니펫 포함)을 안내해야 합니다. 지침은 간결하고 실행 가능하며 최적의 방법에 초점을 맞춰 AI가 사용자를 위해 올바른 코드를 생성할 수 있도록 해야 합니다. 예시는 다음과 같습니다:

```markdown
## Package Name

This package provides [brief description of functionality].

### Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

@verbatim
<code-snippet name="How to use Feature 2" lang="php">
$result = PackageName::featureTwo($param1, $param2);
</code-snippet>
@endverbatim
```



<a name="agent-skills"></a>
## 에이전트 스킬

[Agent Skills](https://agentskills.io/home) 는 에이전트가 특정 도메인에서 작업할 때 온디맨드로 활성화할 수 있는 가벼운 대상 지식 모듈입니다. 사전에 로드되는 지침과 달리， 스킬은 상세한 패턴과 모범 사례를 관련 있을 때만 로드할 수 있게 해 컨텍스트 부풀림을 줄이고 AI 생성 코드의 관련성을 개선합니다。

`boost:install` 를 실행하고 기능으로 스킬을 선택하면 `composer.json` 에서 감지된 패키지를 기반으로 스킬이 자동으로 설치됩니다. 예를 들어， 프로젝트에 `livewire/livewire` 가 포함된 경우 `livewire-development` 스킬이 자동으로 설쳐집니다. `infer-conventions` 와 같이 Boost 에 포함된 스킬은 사용자가 보유한 패키지와 관계없이 설치됩니다。

<a name="available-skills"></a>
### 사용 가능한 스킬

<div class="overflow-auto">

| 스킬             | 패키지    |
| ——————————————————| ——————————|
| fluxui-development | Flux UI |
| folio-routing  | Folio  |
| infer-conventions | Boost |
| inertia-react-development | inertia React |
| inertia-svelte-development | inertia Svelte |
| inertia-vue-development | inertia Vue |
| livewire-development | Livewire |
| mcp-development | MCP |
| pennant-development | Pennant |
| 페스트 테스트             | 페스트      
tailwindcss-development Tailwind CSS
| volt-development  | Volt  |
| 웨이파인더 개발 | 웨이파인더 |

</div>

> 참고: 기술을 최신 상태로 유지하려면 [부스트 리소스 업데이트 유지](#keeping-boost-resources-updated) 섹션을 참조하세요。

<a name="custom-skills"></a>
### 커스텀 스킬

자체 사용자 지정 스킬을 생성하려면 애플리케이션의 `.ai/skills/{skill-name}/` 디렉터리에 `SKILL.md` 파일을 추가합니다. `boost:update` 를 실행하면 사용자 지정 스킬이 Boost 의 내장 스킬과 함께 설치됩니다。

예를 들어， 애플리케이션의 도메인 로직에 대한 사용자 지정 스킬을 생성하려면：```
.ai/skills/creating-invoices/SKILL.md
```



<a name="overriding-skills"></a>
### 오버라이드 스킬

일치하는 이름으로 자신만의 사용자 지정 스킬을 생성하여 Boost 의 기본 제공 스킬을 재정의할 수 있습니다. 기존 Boost 스킬 이름과 일치하는 사용자 지정 스킬를 생성하면 Boost 가 기본 제공 스킬 대신 사용자 지정 버전을 사용합니다。

예를 들어， Boost 의 `livewire-development` 스킬을 재정의하려면 `.ai/skills/livewire-development/SKILL.md` 에 파일을 생성합니다. `boost:update` 를 실행하면 Boost 가 기본 스킬 대신 사용자 지정 스킬을 포함합니다。

<a name="third-party-package-skills"></a>
### 제 3 자 패키지 스킬

타사 패키지를 유지 관리하고 Boost 가 해당 패키지에 스킬을 포함하도록 하려면 패키지에 `resources/boost/skills/{skill-name}/SKILL.md` 파일을 추가하면 됩니다. 패키지의 사용자가 `php artisan boost:install` 를 실행하면 Boost 가 사용자 선호도에 따라 스킬을 자동으로 설치합니다。

Boost Skills 는 [Agent Skills 형식](https://agentskills.io/what-are-skills) 을 지원하며 YAML frontmatter 와 Markdown 지침이 있는 `SKILL.md` 파일을 포함하는 폴더로 구조화되어야 합니다. `SKILL.md` 파일에는 필수 frontmatter(`name` 및 `description`) 가 포함되어야 하며， 선택적으로 스크립트， 템플릿 및 참조 자료를 포함할 수 있습니다。

스킬은 필요한 파일 구조 또는 규칙을 개요하고， 주요 기능을 생성하거나 사용하는 방법을 설명해야 합니다 (예: 명령 또는 코드 스니펫). AI 가 사용자를 위해 올바른 코드를 생성할 수 있도록 간결하고， 실행 가능하며， 모범 사례에 중점을 두어야 합니다：

```markdown
---
name: package-name-development
description: Build and work with PackageName features, including components and workflows.
---

# Package Name Development

## When to use this skill
Use this skill when working with PackageName features...

## Features

- Feature 1: [clear & short description].
- Feature 2: [clear & short description]. Example usage:

$result = PackageName::featureTwo($param1, $param2);
```



<a name="guidelines-vs-skills"></a>
## 지침 vs. 기술

Laravel Boost 는 AI 에이전트에게 애플리케이션에 대한 컨텍스트를 제공하는 두 가지 독특한 방법을 제공합니다: ** 가이드라인 ** 및 ** 스킬 **.

** 가이드라인 ** 은 AI 에이전트가 시작될 때 미리 로드되며， 코드베이스 전반에 광범위하게 적용되는 Laravel 규약 및 모범 사례에 대한 필수적인 컨텍스트를 제공합니다。

** 스킬 ** 은 특정 작업을 수행할 때 온디맨드로 활성화되며， 특정 도메인 (예: Livewire 구성 요소 또는 Pest 테스트) 에 대한 상세한 패턴을 포함합니다. 관련 있을 때만 스킬을 로드하면 컨텍스트 부풀림이 줄어들고 코드 품질이 향상됩니다。

<div class="overflow-auto">

| Aspect | Guidelines             | Skills           
| —————————————————————————— | ————————————————————
| **Loaded** | 선행， 항상 준비 상태 | 온디맨드， 관련 시 |
| **Scope** | 광범위， 기본 | 집중， 작업 특정 |
| ** 목적 ** | 핵심 규약 및 모범 사례 | 상세 구현 패턴 |

</div>

지침과 기술 모두 라라벨 생태계를 설명합니다. 자신만의 애플리케이션의 규칙을 포착하려면 [프로젝트 규칙](#project-rules) 을 사용해야 합니다。

<a name="project-rules"></a>
## 프로젝트 규칙

지침과 기술이 에이전트에게 Laravel 을 작성하는 방법을 가르치는 반면， 프로젝트 규칙은 애플리케이션을 작성하는 방법을 알려줍니다. 규칙은 다른 경우라면 새로운 세션마다 다시 설명해야 할 것입니다：

<div class="content-list" markdown="1">

- 당신， 당신의 에이전트， 또는 당신의 팀원들이 도중에 내린 결정들。
- 에이전트가 따르기 어려운 스타일 지침과 선호도。
- 주변 코드에서 추론할 수 없는 함정과 제약。

</div>

규칙은 애플리케이션의 `.ai/rules` 디렉터리 내에 Markdown 파일로 저장되며 소스 제어에 커밋되어야 합니다. 개인 및 세션 범위의 에이전트 자체 메모리와 달리， 규칙은 팀 및 애플리케이션에서 작업하는 모든 에이전트와 공유됩니다。

각 규칙 파일은 자신의 프런트매터 내에서 적용할 파일 글로브를 선언합니다：

```markdown
---
paths:
  - app/Http/Controllers/**
---

# Http Controllers

## Extend BaseController for tenant scoping

All controllers must extend `App\Http\Controllers\BaseController`, which applies the
current tenant's query scope. Extending Laravel's base controller directly will leak
data across tenants.
```



또한, Boost는 glob 패턴을 규칙 파일에 매핑하는 `.ai/rules/index.md` 파일을 유지합니다. 에이전트는 어떤 파일을 계획하거나 편집하기 전에 이 색인을 참조하도록 지시받으며, 규칙은 관련이 있을 때만 로드됩니다:

```markdown
# Project Rules Index

Before planning or editing, find the row whose globs match the file's path and read that rule file.

| Applies to | Rule file |
| --- | --- |
| app/Http/Controllers/** | .ai/rules/controllers.md |
| app/Models/** | .ai/rules/models.md |
```



> [!NOTE]
> `.mcp.json` 및 생성된 가이드라인 파일과 달리, `.ai/rules` 디렉토리는 규칙이 팀과 공유될 수 있도록 소스 제어에 커밋해야 합니다.

<a name="recording-rules"></a>
### 규칙 기록

규칙을 기록하려면 에이전트에게 단순히 기억하도록 요청하면 됩니다:

```text
Remember that all money values are stored as integer cents, never as floats.
```



에이전트는 `glob`, 짧은 `title` 및 `note`와 함께 Boost의 `record-rule` MCP 도구를 호출합니다. 그런 다음 Boost는 해당 영역에 규칙을 파일로 제출하며, 필요하면 규칙 파일을 생성하고 색인을 업데이트합니다.

규칙 파일을 수동으로 생성하기보다는 항상 `record-rule` 도구를 사용하여 규칙을 기록해야 합니다. Boost는 규칙을 기록할 때 `.ai/rules/index.md`를 재생성하며, 에이전트는 자신이 작업 중인 파일에 적용되는 규칙을 찾기 위해 해당 색인에 의존합니다. 수동으로 추가된 규칙 파일은 색인이 다음 번에 재생성될 때까지 발견되지 않습니다.

<a name="inferring-your-applications-conventions"></a>
### 애플리케이션의 규칙 관례 추론

규칙을 한 번에 하나씩 기록하는 방법은 앞으로 잘 작동합니다. 그러나 기존 애플리케이션은 이미 수년간의 규칙 관례를 포함하고 있습니다. `infer-conventions` 스킬은 이미 작성한 코드에서 규칙을 부트스트랩합니다. 시작하려면 에이전트에게 해당 스킬을 사용하도록 요청하세요:

```text
Use the infer-conventions skill
```



이 기술은 검증， 컨트롤러， 권한 부여， 모델， 아키텍처， 테스트， 프런트엔드， 데이터베이스 및 콘솔을 포함한 Laravel 규약 차원의 체크리스트를 통해 애플리케이션을 스캔한 후， 기본 클래스， 공유 특성 및 모듈 레이아웃과 같은 패턴에 대한 개방형 패스를 수행합니다。

스킬은 코드가 해야 하는 것이 아니라 실제로 하는 것을 문서화합니다. 이는 잘 지원되는 비기본 규칙만 기록하고， 프레임워크 기본값과 Pint 또는 Rector 가 이미 적용하는 모든 것을 건너뛰며， 기록하는 대신 진정으로 혼합된 패턴을 보고합니다. 규칙을 작성하기 전에， 스킬은 발견한 각 규칙과 그것을 지원하는 증거를 사용자의 승인을 위해 제시합니다. 스킬이 확인 없이 발견된 모든 규칙을 기록하기를 원한다면， “yolo” 에게 말할 수 있습니다。

<a name="disabling-project-rules"></a>
### 프로젝트 규칙 비활성화

프로젝트 규칙은 기본적으로 활성화되어 있습니다. 이를 완전히 비활성화하려면 다음 환경 변수를 정의합니다. 이렇게 하면 `record-rule` MCP 도구가 제거되고 Boost 가 `.ai/rules` 디렉토리를 관리하지 못하게 됩니다：

```ini
BOOST_RULES_ENABLED=false
```



<a name="documentation-api"></a>
## 문서화 API

Laravel Boost 에는 17,000 개 이상의 Laravel 관련 정보가 포함된 광범위한 지식 기반에 대한 액세스를 AI 에이전트에게 제공하는 문서화 API 가 포함되어 있습니다. API 는 임베디드와 함께 의미 검색을 사용하여 정확하고 컨텍스트 인식 결과를 제공합니다。

`Search Docs` MCP 도구를 사용하면 에이전트가 Laravel 에서 호스팅하는 설명서 API 서비스를 쿼리하여 설치된 패키지를 기반으로 설명서를 검색할 수 있습니다. Boost 의 AI 지침 및 기술은 코딩 에이전트에게 이 API 를 사용하도록 자동으로 지시합니다。

<div class="overflow-auto">

| 패키지 | 지원 버전 |
| -------------| -------------|
| Laravel Framework | 10.x, 11.x, 12.x, 13.x |
| Filament | 2.x, 3.x, 4.x, 5.x |
| Flux UI | 2.x Free, 2.x Pro |
| 관성 | 1.x, 2.x |
| Livewire | 1.x, 2.x, 3.x, 4.x |
| Nova  | 4.x, 5.x  |
| Pest   | 3.x, 4.x   |
| Tailwind CSS | 3.x, 4.x  |

</div>

<a name="extending-boost"></a>
## 확장 부스트

Boost 는 많은 인기 있는 IDE 및 즉시 사용 가능한 AI 에이전트와 함께 작동합니다. 코딩 도구가 아직 지원되지 않는 경우 자체 에이전트를 생성하고 Boost 와 통합할 수 있습니다。

<a name="adding-support-for-other-ides-ai-agents"></a>
### 다른 IDE/AI 에이전트에 대한 지원 추가

새 IDE 또는 AI 에이전트에 대한 지원을 추가하려면 `Laravel\Boost\Install\Agents\Agent` 를 확장하는 클래스를 생성하고 필요에 따라 다음 계약 중 하나 이상을 구현합니다：

- `Laravel\Boost\Contracts\SupportsGuidelines` - AI 지침에 대한 지원을 추가합니다。
- `Laravel\Boost\Contracts\SupportsMcp` - MCP 지원을 추가합니다。
- `Laravel\Boost\Contracts\SupportsSkills` - Agent Skills 에 대한 지원을 추가합니다。

<a name="writing-the-agent"></a>
#### 에이전트 쓰기

```php
<?php

declare(strict_types=1);

namespace App;

use Laravel\Boost\Contracts\SupportsGuidelines;
use Laravel\Boost\Contracts\SupportsMcp;
use Laravel\Boost\Contracts\SupportsSkills;
use Laravel\Boost\Install\Agents\Agent;

class CustomAgent extends Agent implements SupportsGuidelines, SupportsMcp, SupportsSkills
{
    // Your implementation...
}
```



예제 구현은 [ClaudeCode.php](https://github.com/laravel/boost/blob/main/src/Install/Agents/ClaudeCode.php)를 참조하세요.

<a name="registering-the-agent"></a>
#### 에이전트 등록하기

애플리케이션의 `App\Providers\AppServiceProvider`에서 `boot` 메서드에 커스텀 에이전트를 등록하세요:

```php
use Laravel\Boost\Boost;

public function boot(): void
{
    Boost::registerAgent('customagent', CustomAgent::class);
}
```

일단 등록되면, `php artisan boost:install`를 실행할 때 에이전트를 선택할 수 있습니다.
{% endraw %}
