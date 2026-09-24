# Laravel 최신 공식 문서 저장소

라라벨(Laravel) 공식 GitHub 문서 저장소([laravel/docs](https://github.com/laravel/docs))의 최신 버전(13.x) 문서를 다운로드하여 [공식 문서 사이트](https://laravel.com/framework/docs)의 그룹 구조에 맞춰 체계적으로 정리한 저장소입니다.

## 파일 및 디렉터리 구성 규칙

1. **언어 표기 규칙**: 원본 영문 마크다운 파일은 `파일명_en.md` 형식으로 저장됩니다. (추후 한글 번역 문서 등을 `파일명_ko.md` 형태로 나란히 확장할 수 있습니다.)
2. **그룹별 디렉터리 분리**: 공식 사이트 사이드바 네비게이션 구조에 맞추어 11개의 주요 그룹별 하위 디렉터리(`src/01_...` ~ `src/11_...`)로 분할하여 배치하였습니다.

## 그룹별 문서 현황 (총 11개 그룹, 103개 문서)

| 순번 | 그룹명 (영문 / 한글) | 디렉터리 | 문서 수 | 주요 포함 내용 |
| :--- | :--- | :--- | :---: | :--- |
| 01 | **Prologue** (서문) | [`src/01_prologue/`](./src/01_prologue/) | 3개 | Release Notes, Upgrade Guide, Contributions |
| 02 | **Getting Started** (시작하기) | [`src/02_getting_started/`](./src/02_getting_started/) | 7개 | Installation, Configuration, AI Agentic Dev, Structure, Frontend, Starter Kits, Deployment |
| 03 | **Architecture Concepts** (아키텍처 개념) | [`src/03_architecture_concepts/`](./src/03_architecture_concepts/) | 4개 | Request Lifecycle, Service Container, Service Providers, Facades |
| 04 | **The Basics** (기본 개념) | [`src/04_the_basics/`](./src/04_the_basics/) | 14개 | Routing, Middleware, CSRF, Controllers, Requests, Responses, Views, Blade, Vite, Sessions 등 |
| 05 | **Digging Deeper** (심화 주제) | [`src/05_digging_deeper/`](./src/05_digging_deeper/) | 22개 | Artisan, Cache, Queues, Mail, Events, Scheduling, HTTP Client, Filesystem 등 |
| 06 | **Security** (보안) | [`src/06_security/`](./src/06_security/) | 6개 | Authentication, Authorization, Verification, Encryption, Hashing, Passwords |
| 07 | **Database** (데이터베이스) | [`src/07_database/`](./src/07_database/) | 7개 | Database Getting Started, Query Builder, Pagination, Migrations, Seeding, Redis, MongoDB |
| 08 | **Eloquent ORM** (Eloquent ORM) | [`src/08_eloquent_orm/`](./src/08_eloquent_orm/) | 7개 | Eloquent Getting Started, Relationships, Collections, Mutators, Resources, Factories |
| 09 | **AI** (인공지능 (AI)) | [`src/09_ai/`](./src/09_ai/) | 3개 | Laravel AI SDK, Model Context Protocol (MCP), Laravel Boost |
| 10 | **Testing** (테스트) | [`src/10_testing/`](./src/10_testing/) | 6개 | Testing Getting Started, HTTP Tests, Console Tests, Browser Tests (Dusk), Database Testing |
| 11 | **Packages** (공식 패키지) | [`src/11_packages/`](./src/11_packages/) | 24개 | Cashier, Dusk, Fortify, Folio, Octane, Passport, Pennant, Reverb, Sail, Sanctum, Scout, Telescope, Valet 등 24종 |

## 상세 목차 및 링크

전체 문서의 세부 링크는 [`src/index.md`](./src/index.md)에서 확인하실 수 있습니다.
