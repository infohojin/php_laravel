---
layout: docs
title: "01강: 라라벨 13과의 만남 & 지니샵 프로젝트 생성"
---

{% raw %}
# 01강: 라라벨 13과의 만남 & 지니샵 프로젝트 생성

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 라라벨 13의 핵심 가치, 개발 환경(Herd / Sail / Valet) 준비, `laravel new jinyshop` 실행  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [설치 (Installation)](../docs/02_getting_started/installation_ko.md), [Sail](../docs/11_packages/sail_ko.md), [Valet](../docs/11_packages/valet_ko.md), [Homestead](../docs/11_packages/homestead_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리가 만들 **지니샵(JinyShop)**은 수만 권의 컴퓨터, 인문, 과학 도서를 독자들에게 소개하고 판매하는 멋진 온라인 서점이잖아! 첫 코드를 짜기 전에 왜 하필 PHP와 라라벨을 골랐는지 궁금해. 요즘 파이썬이나 노드(Node.js)도 유행하잖아?"

🐱 **지니**: "좋은 질문이야 도로시! 예전의 구식 PHP를 생각하면 오산이란다. 현대의 **PHP 8.2+**는 강력한 타입 시스템과 JIT 컴파일러로 놀랍도록 빠르고 견고해졌지. 그리고 그 정점에 바로 **라라벨(Laravel)**이 있단다. 라라벨은 웹 애플리케이션에 필요한 라우팅, 데이터베이스 ORM, 사용자 인증, 파일 업로드, 비동기 큐, 결제 연동까지 모든 도구가 유기적으로 결합된 **풀스택 마법 상자**거든! 바퀴를 다시 발명할 필요 없이, 오직 서점의 비즈니스 로직에만 집중할 수 있게 해준단다."

🐶 **토토**: "멍멍! Mac 사용자라면 **Laravel Herd**를 쓰면 PHP와 Nginx를 1초 만에 깔 수 있고, 윈도우나 리눅스 환경이라면 Docker 기반의 **Laravel Sail**을 쓰면 된다멍! 망설이지 말고 터미널을 열라멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 현대 PHP 생태계(PHP 8.2 이상, Composer)의 기본 요구 조건을 점검합니다.
2. 개발 환경(Laravel Herd / Sail / Valet) 중 본인의 OS에 맞는 최적의 툴체인을 선택합니다.
3. 라라벨 공식 인스톨러를 사용해 온라인 도서 쇼핑몰 **`jinyshop`** 프로젝트를 생성합니다.
4. 로컬 웹 서버를 실행하여 기본 웰컴 화면 접속을 확인합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] PHP 버전 및 Composer 설치 확인

터미널을 열고 시스템에 설치된 PHP 버전과 Composer가 준비되어 있는지 확인합니다.

```bash
# 1. PHP 버전 확인 (PHP 8.2 이상 필수)
php -v

# 2. Composer 버전 확인
composer -V
```

> **출력 예시:**
> ```text
> PHP 8.3.10 (cli) (built: Aug 15 2024 12:00:00) (NTS)
> Composer version 2.7.7 2024-06-10 15:00:00
> ```

---

### [Step 2] 라라벨 공식 인스톨러 설치

Composer 전역 패키지로 Laravel Installer를 설치하면 `laravel new` 명령어를 자유롭게 쓸 수 있습니다.

```bash
composer global require laravel/installer
```

설치 후 PATH 환경 변수가 올바르게 잡혀 있는지 확인합니다:

```bash
laravel --version
# Laravel Installer 5.x.x
```

---

### [Step 3] 온라인 서점 `jinyshop` 프로젝트 생성

원하는 작업 디렉터리로 이동하여 도서 쇼핑몰 프로젝트 `jinyshop`을 생성합니다.

```bash
# 인터랙티브 옵션으로 생성 (Git, 테스트 프레임워크 선택)
laravel new jinyshop
```

인스톨러 실행 시 나타나는 프롬프트 추천 설정:
- **Starter Kit 선택**: `None` (우리는 14주 동안 기초부터 탄탄하게 직접 만들 것입니다)
- **Testing Framework**: `Pest` 또는 `PHPUnit` (Pest 추천)
- **Database Engine**: `MySQL` 또는 `SQLite` (로컬 빠른 실습에는 SQLite, 실무형에는 MySQL 선택)
- **Git 저장소 초기화**: `Yes`

> 💡 **Composer로 직접 생성하는 대안 명령어:**
> ```bash
> composer create-project laravel/laravel jinyshop
> ```

---

### [Step 4] 프로젝트 디렉터리 진입 및 로컬 서버 가동

생성된 서점 프로젝트 폴더로 이동합니다.

```bash
cd jinyshop
```

라라벨 내장 아티산(Artisan) 웹 서버를 띄웁니다:

```bash
php artisan serve
```

> **터미널 출력:**
> ```text
>    INFO  Server running on [http://127.0.0.1:8000].
> 
>   Press Ctrl+C to stop the server
> ```

웹 브라우저를 열고 `http://127.0.0.1:8000`에 접속합니다. 라라벨 13의 세련된 공식 웰컴 페이지가 표시되면 성공입니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 1) Laravel Sail (도커 컨테이너 환경)
- 로컬 머신에 MySQL이나 Redis를 직접 설치하지 않고, Docker 컨테이너로 격리된 개발 환경을 구축할 수 있습니다.
- `php artisan sail:install` 명령어로 MySQL, Redis, Mailpit(가짜 메일 서버), Meilisearch(도서 검색) 컨테이너를 한 번에 조립할 수 있습니다.
- 실행 명령어: `./vendor/bin/sail up -d`

### 2) Laravel Valet vs Homestead
- **Valet (macOS 전용 초경량 환경)**: 백그라운드에서 Nginx와 DnsMasq를 활용하여 `~/Sites` 아래의 폴더명을 그대로 `http://jinyshop.test` 도메인으로 초고속 매핑해 줍니다. 리소스 소비가 10MB 미만으로 매우 가볍습니다.
- **Homestead (전통적인 가상머신)**: Vagrant + VirtualBox 기반의 올인원 Ubuntu VM 환경입니다. 현재는 Sail이나 Herd에 비해 무거워 레거시 환경 유지보수에 주로 사용됩니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`laravel: command not found` 에러가 나요!**  
>    `composer global config bin-dir --absolute` 명령으로 전역 bin 경로를 확인한 뒤, `~/.zshrc` 또는 `~/.bashrc` 파일 맨 밑에 `export PATH="$PATH:$HOME/.composer/vendor/bin"`을 추가하고 `source ~/.zshrc`를 실행하라멍!
> 
> 2. **포트 8000번이 이미 사용 중이에요!**  
>    `php artisan serve --port=8080` 처럼 다른 포트 번호를 지정해주면 충돌 없이 열린다멍!

---

## 💡 6. 1강 자가진단 과제

1. `jinyshop` 프로젝트 폴더에서 Git 커밋 로그(`git log`)를 확인하고, `Initial commit` 상태인지 확인하세요.
2. 터미널에서 `php artisan --version`을 실행하여 현재 설치된 정확한 라라벨 프레임워크 버전을 확인해 보세요.
3. 로컬 브라우저에서 `http://127.0.0.1:8000`에 접속하여 화면 하단에 표시된 `Laravel v13.x (PHP v8.x)` 정보를 캡처해 두세요.
{% endraw %}
