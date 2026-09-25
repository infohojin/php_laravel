# 📘 지니샵(JinyShop) 도서 쇼핑몰 14주 핸드온 라라벨 마스터 작업 가이드

> **문서 버전:** 1.0.0  
> **프로젝트명:** 지니샵 (`jinyshop` — 온라인 도서 쇼핑몰 / Bookstore E-Commerce)  
> **교육 대상:** 라라벨 초급~중급 개발자 및 모던 풀스택 PHP 학습자  
> **핵심 페르소나:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **기반 교재:** 라라벨 최신 공식 문서 103개 전 주제 (11개 그룹) 100% 매핑  

---

## 📌 1. 프로젝트 개요 & 작업 방향

### 1.1 프로젝트 목표
- **단일 완성형 도서 쇼핑몰 구축**: 단순 기능 나열식 예제가 아니라, 실제로 서비스 가능한 완성도 높은 **도서 전문 쇼핑몰(지니샵, JinyShop)**을 처음부터 끝까지 점진적으로 완성합니다.
- **라라벨 공식 문서 100% 전수 학습**: 공식 문서의 방대한 11개 그룹 103개 세부 주제를 단 하나도 축소하거나 누락하지 않고, 도서 쇼핑몰 개발 흐름에 맞추어 재배치·체화합니다.
- **스토리텔링 기반 협업 학습**: 🐱 지니, 👧 도로시, 🐶 토토의 페르소나 대화(Dialogue)를 통해 "왜 이 기능이 필요한가?"를 먼저 공감하고 코딩에 착수합니다.

---

## 📂 2. 디렉터리 구조 및 체계

```text
php_laravel/
├── README.md                      # 전체 프로젝트 소개 및 14주 로드맵 요약
├── syllabus.md                    # 14주 종합 실습 계획서 (루트)
├── guide.md                       # 본 작업 가이드 문서 (루트)
├── verify_coverage.py             # 공식 문서 103개 전수 포함율 자동 검증 스크립트
└── src/
    ├── index.md                   # 14주 학습 마스터 인덱스 및 종합 내비게이션
    ├── character.md               # 지니, 도로시, 토토 캐릭터 설정 및 대화 작성 가이드
    ├── syllabus.md                # 14주 종합 실습 계획서 (src 내부)
    ├── guide.md                   # 본 작업 가이드 문서 (src 내부)
    ├── docs/                      # 라라벨 최신 공식 문서 (영문/한글 쌍)
    │   ├── index.md               # 공식 문서 전체 색인 목차
    │   ├── 01_prologue/           # releases, upgrade, contributions (_en.md, _ko.md)
    │   ├── 02_getting_started/    # installation, configuration, structure, ai, frontend, ...
    │   ├── 03_architecture_concepts/ # lifecycle, container, providers, facades
    │   ├── 04_the_basics/         # routing, middleware, controllers, requests, responses, views, blade, vite, ...
    │   ├── 05_digging_deeper/     # artisan, cache, events, filesystem, mail, queues, scheduling, ...
    │   ├── 06_security/           # authentication, authorization, passwords, hashing, ...
    │   ├── 07_database/           # database, migrations, queries, pagination, redis, mongodb
    │   ├── 08_eloquent_orm/       # eloquent, relationships, collections, mutators, resources, ...
    │   ├── 09_ai/                 # ai-sdk, mcp, boost
    │   ├── 10_testing/            # testing, http-tests, console-tests, database-testing, mocking, dusk
    │   └── 11_packages/           # breeze, cashier-paddle, dusk, horizon, pulse, sanctum, scout, ...
    ├── week01/ ~ week14/          # 주차별 상세 실습 강의 및 핸드온 가이드
    │   └── index.md               # 주차별 대화, 목표, 도서 쇼핑몰 구현 명세, 공식 문서 링크, 체크리스트
```

---

## 📚 3. 도서 쇼핑몰 (JinyShop) 도메인 모델 & 데이터 설계

본 프로젝트는 실제 상용 서점(교보문고, 알라딘, Yes24 등)의 비즈니스 로직을 모방한 실감 나는 도서 쇼핑몰을 구현합니다.

### 3.1 주요 취급 상품 및 카테고리
1. **국내외 도서 (Paperback / Hardcover)**:
   - IT/컴퓨터 (프로그래밍, 인공지능, 클라우드, 데이터베이스)
   - 경제/경영 (경영전략, 재테크, 스타트업)
   - 인문/사회 (철학, 역사, 심리학)
   - 소설/문학 (SF, 추리, 에세이)
2. **전자책 (eBook)**:
   - PDF / EPUB 다운로드 형식 (구매자 대상 서명된 임시 URL 제공)

### 3.2 핵심 데이터베이스 ERD 구조
- **`books` (도서 테이블)**:
  - `id`, `isbn` (고유 ISBN-13 식별자), `title` (도서명), `slug` (URL 친화적 슬러그)
  - `author_id` (저자 FK), `publisher_id` (출판사 FK), `category_id` (카테고리 FK)
  - `price` (정가), `sale_price` (할인가), `stock_quantity` (실물 재고 수량)
  - `format` (종이책 `paperback`, 전자책 `ebook`)
  - `ebook_file_path` (전자책 암호화 저장 경로)
  - `page_count` (쪽수), `published_at` (출간일), `description` (책 소개), `toc` (목차)
  - `status` (`draft`, `published`, `out_of_stock`, `discontinued`)
  - `timestamps`, `softDeletes` (품절/절판 보존용 소프트 삭제)
- **`authors` (저자 테이블)**:
  - `id`, `name`, `email`, `bio`, `profile_photo_url`, `timestamps`
- **`publishers` (출판사 테이블)**:
  - `id`, `name`, `code`, `contact_email`, `website_url`, `timestamps`
- **`categories` (도서 분류 테이블)**:
  - `id`, `parent_id` (계층형 카테고리), `name`, `slug`, `order_num`
- **`reviews` (서평/평점 다형성 테이블 - MorphMany)**:
  - `id`, `user_id`, `reviewable_type` (`App\Models\Book`), `reviewable_id`, `rating` (1~5점), `content`
- **`images` (도서 표지 및 미리보기 이미지 다형성 테이블)**:
  - `id`, `imageable_type`, `imageable_id`, `path`, `type` (`cover`, `preview`), `sort_order`
- **`cart_items` (장바구니 테이블)**:
  - `id`, `user_id` (또는 `session_id`), `book_id`, `quantity`, `timestamps`
- **`orders` & `order_items` (주문 및 주문 도서 상세)**:
  - `order_number` (고유 주문번호), `user_id`, `total_amount`, `discount_amount`, `final_amount`
  - `payment_method`, `payment_status` (`pending`, `paid`, `failed`, `refunded`)
  - `shipping_address`, `recipient_name`, `recipient_phone`, `shipping_status`
- **`ebook_downloads` (전자책 다운로드 이력)**:
  - `id`, `order_item_id`, `user_id`, `download_token`, `expires_at`, `downloaded_at`

### 3.3 듀얼 트랙(Dual-Track) 아키텍처 설계

지니샵은 **독자용 프론트엔드 스토어프론트(Storefront)**와 **운영자용 백엔드 관리자(Admin Backoffice)**가 독립되면서도 일관성 있는 비즈니스 로직을 공유하도록 설계됩니다:

| 구분 | 🌐 고객/독자용 프론트엔드 (Storefront) | ⚙️ 운영자용 백엔드 관리자 (Admin Backoffice) |
| :--- | :--- | :--- |
| **접속 대상** | 일반 독자, 회원/비회원 구매자, 모바일 앱 | 서점 대표, 서적 MD, 물류 창고 관리자, CS 상담원 |
| **기본 URL 경로** | `/` (루트), `/books`, `/cart`, `/checkout`, `/mypage` | `/admin`, `/admin/dashboard`, `/admin/books`, `/admin/orders` |
| **UI/UX 테마** | 감성적 북스토어 UI, 배너, 반응형 모바일 최적화 (Tailwind) | 정보 집약형 그리드/테이블, 데이터 시각화 차트, 관리자 사이드바 |
| **보안 & 인가** | 세션 인증, 이메일 인증, 본인 리소스 Policy | 관리자 전용 미들웨어(`EnsureUserIsAdmin`), `Gate::define('admin')` |
| **주요 기능** | 도서 탐색, 실시간 검색, 장바구니, 결제 승인, 서평 작성 | 도서 CRUD, 표지 업로드/리사이징, 재고 CLI, 주문 상태 관리, APM 모니터링 |

---

## 🗓️ 4. 14주 핸드온 개발 로드맵 요약 (프론트엔드 & 백엔드 관리자 듀얼 트랙)

| 주차 | 단계 | 주제 | 🌐 독자용 프론트엔드 (Storefront) | ⚙️ 운영자용 백엔드 관리자 (Admin Backoffice) | 공식 문서 연계 (`src/docs/`) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **01주** | 환경 & 킥오프 | 환경 구축 & 프로젝트 킥오프 | 웰컴 페이지 브라우징, Tailwind CSS 폰트 및 UI 토큰 준비 | 관리자 디버깅 도구(Telescope, Pint) 구축, Slim 디렉터리 아키텍처 및 `.env` 설정 | `02_getting_started/installation, configuration, structure, ai`, `11_packages/sail, pint, telescope, valet, homestead` |
| **02주** | 코어 웹 기초 | 생명주기, 라우팅 & 컨트롤러 | 도서 홈(`GET /`), 도서 목록/상세 라우트, HTTP 응답 및 리다이렉트 | 관리자 라우트 그룹 분리(`/admin`), 관리자 베이스 컨트롤러 및 요청 파라미터 캡처 | `03_architecture_concepts/lifecycle`, `04_the_basics/routing, controllers, requests, responses, urls` |
| **03주** | 템플릿 & UI | 블레이드 컴포넌트 & 에셋 번들링 | 서점 공통 레이아웃, 헤더 베스트셀러 배너, 도서 카드(`x-book-card`) 컴포넌트, Vite 번들링 | 관리자 백오피스 전용 레이아웃(`admin.blade.php`), 관리자 사이드바 컴포넌트, CSRF 보안 방어 | `04_the_basics/views, blade, vite, csrf`, `02_getting_started/frontend`, `11_packages/mix, head` |
| **04주** | 데이터베이스 | 마이그레이션 & 대량 시딩 | 고객에게 노출될 도서, 저자, 출판사, 카테고리 스키마 구조 | 관리자 관점의 1,000권 도서 대량 시딩(`DatabaseSeeder`), Faker 팩토리, 품절/비공개 데이터 분리 | `07_database/database, migrations, seeding`, `08_eloquent_orm/eloquent-factories` |
| **05주** | ORM 기초 | Eloquent ORM & 도서 카탈로그 | 도서 카탈로그, 다조건 필터링, 가격 정렬, 페이지네이션, SEO 친화적 슬러그 | 관리자용 도서 재고 목록 쿼리, 소프트 삭제(Soft Deletes)된 절판 도서 복원 및 영구 삭제 | `08_eloquent_orm/eloquent, eloquent-mutators`, `07_database/queries, pagination`, `05_digging_deeper/strings` |
| **06주** | ORM 심화 | 데이터 관계(Relationships) 심화 | 도서 상세의 다형성 서평(Reviews) 목록 및 별점, 관련 저자/출판사 도서 표시 | 관리자용 서평 검수/블라인드 처리, 다형성 이미지 첨부 관리, N+1 쿼리 최적화 진단 | `08_eloquent_orm/eloquent-relationships, eloquent-collections`, `05_digging_deeper/collections` |
| **07주** | 입력 & 상태 | 폼 유효성 검사, 세션 & 장바구니 | 장바구니 세션(담기, 수량변경, 삭제), Precognition 실시간 폼 유효성 검사 | 관리자용 장바구니 이탈률 통계 및 MongoDB 하이브리드 사용자 행동/열람 감사 로그 분석 | `04_the_basics/validation, session`, `11_packages/precognition`, `07_database/mongodb` |
| **08주** | 보안 & 인증 | 사용자 인증 & 권한 정책 | 일반 독자 회원가입/로그인, 이메일 인증, 소셜 로그인(구글/카카오), 내 서평 수정 Policy | 관리자 전용 Gate/Policy (`EnsureUserIsAdmin`), 관리자 계정 권한 부여 및 Passport 제휴사 관리 | `06_security/authentication, authorization, verification, passwords, hashing, encryption`, `11_packages/socialite, fortify, passport`, `02_getting_started/starter-kits` |
| **09주** | 파일 & 관리자 | 파일 스토리지 & 백오피스 관리자 | 고화질 WebP 도서 표지 및 미리보기 이미지 최적화 서빙, 감성적 404 에러 화면 | 관리자 전용 백오피스 대시보드(`/admin/dashboard`), 신규 도서 등록 CRUD 폼, 표지 파일 업로드(Flysystem), Rate Limiting 및 Monolog 감사 로그 | `05_digging_deeper/filesystem, images, rate-limiting`, `04_the_basics/middleware, errors, logging` |
| **10주** | 아키텍처 | 서비스 컨테이너, 프로바이더 & 파사드 | 고객용 주문서 작성 및 토스/스트라이프 PG사 결제 승인 화면 | 관리자용 결제 대행사(PG) 동적 스위칭 바인딩(PaymentServiceProvider), 결제 취소/환불 추적 및 Context 로깅 | `03_architecture_concepts/container, providers, facades`, `05_digging_deeper/contracts, context, helpers, http-client` |
| **11주** | 비동기 & 결제 | 이벤트, 비동기 큐, 메일 & 결제 | 주문 완료 시 마크다운 영수증 메일 수신, 마이페이지 인앱 알림 뱃지, 북클럽 정기 구독 | 관리자용 고액 주문 발생 시 Slack 실시간 웹훅 경보, Redis 큐 모니터링을 위한 Laravel Horizon 대시보드 | `05_digging_deeper/events, queues, mail, notifications`, `11_packages/billing, cashier-paddle, horizon` |
| **12주** | 자동화 & 실시간 | 아티산, 스케줄링 & 실시간 소켓 | 다국어 언어팩(한국어/영어/일본어), 통화 표기 스위처(KRW/USD), 베스트셀러 고속 Redis 캐싱 | 물류 창고 관리자용 대화형 아티산 CLI(`shop:restock`) 재고 입고 도구, 자정 미결제 취소 크론 스케줄러, 실시간 신규 주문 수신 Reverb 웹소켓 토스트 알림 | `05_digging_deeper/artisan, scheduling, cache, broadcasting, concurrency, processes, localization`, `11_packages/prompts, reverb`, `07_database/redis` |
| **13주** | API & AI | RESTful API, 토큰 인증, 검색 & AI | 모바일 앱 연동 RESTful API, Sanctum 토큰 인증, 10ms Scout 도서 전문 검색, 봄맞이 기획전 Folio 페이지 | 관리자 도서 등록 시 Laravel AI SDK를 이용한 마케팅 카피 자동 생성, AI 에이전트 연동 재고 조회 MCP 도구, Pennant 신규 결제창 A/B 테스트 피처 플래그 | `08_eloquent_orm/eloquent-resources, eloquent-serialization`, `11_packages/sanctum, scout, pennant, folio`, `09_ai/ai-sdk, mcp, boost`, `05_digging_deeper/search` |
| **14주** | 테스트 & 배포 | 테스트 자동화, E2E & 프로덕션 배포 | 실제 고객 구매 플로우(장바구니 $\rightarrow$ 결제 $\rightarrow$ 완료) Feature 테스트 및 Dusk 브라우저 E2E 테스트 | 관리자 백오피스 APM 모니터링(Laravel Pulse: 느린 쿼리/요청 관제), Octane 초고속 서빙, Envoy 무중단 배포 스크립트 | `10_testing/testing, http-tests, console-tests, database-testing, mocking, dusk`, `11_packages/pulse, octane, envoy`, `05_digging_deeper/packages`, `02_getting_started/deployment`, `01_prologue/releases, upgrade, contributions` |

---

## 🎭 5. 캐릭터 가이드 & 대화 블록 작성 원칙

각 주차별 강의(`weekXX/index.md`) 및 실습 예제 작성 시 반드시 지켜야 할 캐릭터 가이드라인입니다.

1. **🐱 지니 (Jiny - 시니어 멘토)**:
   - **어조**: 부드럽고 친절한 존댓말, 명쾌하고 원리 중심의 설명.
   - **주요 대사 특징**: "이 부분은 라라벨의 서비스 컨테이너가 내부적으로 처리해 준단다.", "왜 컨트롤러를 얇게 유지해야 하는지 살펴볼까?"
2. **👧 도로시 (Dorothy - 주니어 개발자)**:
   - **어조**: 밝고 활기차며 호기심 가득한 말투, 초보자가 겪는 현실적인 고민과 질문.
   - **주요 대사 특징**: "지니! 도서 카테고리가 100개 넘게 늘어나면 데이터베이스 쿼리가 너무 느려지지 않을까?", "장바구니 세션은 브라우저를 닫아도 유지되나요?"
3. **🐶 토토 (Toto - 보조견 & 에러 방지 가이드)**:
   - **어조**: 멍멍! 활기차고 충성스러운 말투, CLI 명령어 팁 및 트러블슈팅 안내.
   - **주요 대사 특징**: "멍멍! 마이그레이션 할 때 `php artisan migrate:status`로 먼저 확인하라멍!", "`.env` 파일을 수정했다면 `php artisan config:clear`는 필수다멍!"

---

## 🔍 6. 품질 관리 & 공식 문서 전수 검증 절차

본 강의 자료를 수정하거나 확장할 때, 공식 문서 내용이 누락되지 않도록 다음 검증 절차를 필히 수행해야 합니다.

1. **검증 스크립트 실행**:
   ```bash
   python3 verify_coverage.py
   ```
2. **검증 기준**:
   - `총 공식 문서 주제 수`: 103개
   - `실습 계획 매핑 문서 수`: 103개
   - `공식 문서 커버리지`: **100.0%**
   - 0개라도 누락이 발생하면 `verify_coverage.py`가 에러 코드를 반환하므로 반드시 `syllabus.md` 및 해당 주차 가이드에 매핑을 보완해야 합니다.
3. **상대 링크 정합성 확인**:
   - `src/syllabus.md` 에서는 공식 문서 참조 시 `./docs/그룹명/문서명_ko.md` 경로를 사용합니다.
   - `src/weekXX/index.md` 에서는 `../docs/그룹명/문서명_ko.md` 경로를 사용합니다.
   - 루트 `syllabus.md` 에서는 `./src/docs/그룹명/문서명_ko.md` 경로를 사용합니다.

---

## 🚀 7. 향후 작업 진행 가이드

1. **주차별 상세 실습 코드 확장**:
   - 각 `src/week01/` ~ `src/week14/`의 `index.md`를 바탕으로 단계별 소스 코드 스니펫(`BookController.php`, `Book.php`, `book-card.blade.php` 등)과 단계별 실습 튜토리얼을 지속 보강합니다.
2. **공식 문서와 실습 가이드의 상호 링크**:
   - `src/docs/` 내의 한글 번역본 각 문서 상단에 관련 주차 실습 링크(`예: 본 문서는 5주차 도서 카탈로그 구현에서 실습합니다`)를 추가하여 역방향 탐색성을 극대화합니다.

---

## 🌐 8. 지킬(Jekyll) 웹사이트 실행 및 빌드 환경

이 웹사이트는 **Ruby**와 **Jekyll**을 사용하여 정적 웹 문서로 빌드됩니다. 로컬 환경에서 강의 노트를 실시간으로 확인하고 편집하려면 아래 절차를 진행하세요.

> [!IMPORTANT]
> 모든 터미널 명령어는 반드시 **`php_laravel` 프로젝트 루트 폴더**(`/Users/hojin9/dev/jinysite/php_laravel`)에서 실행해야 합니다.  
> 상위 폴더에서 실행 시 `Could not locate Gemfile` 오류가 발생합니다.

### 8.1. 필수 도구 설치

#### macOS 환경
```bash
# 1. Homebrew로 최신 Ruby 설치
brew install ruby

# 2. 터미널 환경설정에 Ruby 경로 추가 (~/.zshrc)
echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 3. 프로젝트 루트로 이동 후 의존성 Gem 설치
cd php_laravel
gem install bundler jekyll
bundle install
```

#### Windows 환경
1. **Ruby 및 Devkit 설치**:
   - [RubyInstaller 공식 사이트](https://rubyinstaller.org/downloads/)에서 **`Ruby+Devkit 3.3.x (x64)`** 다운로드 및 설치
   - 또는 Windows 터미널(PowerShell)에서 `winget`으로 설치:
     ```powershell
     winget install RubyInstallerTeam.RubyWithDevKit.3.3
     ```
2. **PowerShell 스크립트 실행 권한 설정**:
   - 처음 실행 시 스크립트 보안 정책 에러가 발생할 수 있으므로 권한을 부여합니다:
     ```powershell
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```
3. **의존성 Gem 설치**:
   ```powershell
   cd php_laravel
   gem install bundler jekyll
   bundle install
   ```

#### Linux (Ubuntu/Debian) 환경
```bash
sudo apt update
sudo apt install -y ruby-full build-essential zlib1g-dev
gem install bundler jekyll
bundle install
```

---

### 8.2. 지킬 환경 설정 (_config.yml) 상세

```yaml
title: Laravel 13.x & JinyShop Hand-on Tutorial
email: hojin9@gmail.com
description: >-
  라라벨 13.x 공식 문서 100% 한글화 및 14주 완성 지니샵(JinyShop) 도서 쇼핑몰 핸드온 튜토리얼
baseurl: ""
url: "https://laravel.jiny.dev"

# 빌드 입출력 디렉터리 분리
source: src
destination: docs

# Pretty Permalinks: folder/index.html 구조
permalink: pretty

# 마크다운 파서 및 하이라이팅
markdown: kramdown
highlighter: rouge
kramdown:
  input: GFM
  syntax_highlighter: rouge
  math_engine: mathjax
```

> [!TIP]
> **라라벨 Blade 문법과의 충돌 방지:**  
> 라라벨 Blade의 `{{ $var }}` 문법은 Liquid 템플릿 태그와 형식이 같으므로, 모든 마크다운 파일의 본문은 `{% raw %}`와 `{% endraw %}`로 감싸져 안전하게 컴파일됩니다.

---

### 8.3. 로컬 서버 실행 및 관리

```bash
# 1. 개발용 실시간 핫리로드(LiveReload) 서버 실행 (파일 수정 시 자동 반영)
bundle exec jekyll serve --livereload

# 2. 백그라운드 데몬으로 서버 실행
bundle exec jekyll serve --detach --port 4000

# 3. 사이트 정적 빌드 (결과물은 docs/ 폴더에 생성)
bundle exec jekyll build

# 4. 실행 중인 지킬 서버 확인
lsof -i :4000

# 5. 백그라운드 지킬 서버 종료
pkill -f jekyll
# 또는 포트 기준 종료:
kill $(lsof -t -i:4000)
```

- **로컬 접속 주소**: [http://localhost:4000](http://localhost:4000) (또는 `http://127.0.0.1:4000`)
- **소스 디렉토리**: `src/` (14주 강좌 마크다운, 라라벨 공식 문서, 레이아웃 및 디자인 에셋)
- **출력 디렉토리**: `docs/` (GitHub Pages 배포 타깃)

---

### 8.4. 웹사이트 배포 (GitHub Pages)

1. 수정한 내용을 커밋 후 `main` 브랜치에 푸시합니다:
   ```bash
   git add .
   git commit -m "docs: 14주 핸드온 및 지킬 정적 사이트 업데이트"
   git push origin main
   ```
2. GitHub 저장소 **Settings ➔ Pages** 설정:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` 브랜치의 `/docs` 디렉토리 선택
3. 사용자 지정 도메인: `laravel.jiny.dev` (`src/CNAME` 자동 연동)

---

## 9. 자주 발생하는 문제 해결 (Troubleshooting FAQ)

| 증상 | 원인 | 해결 방법 |
| :--- | :--- | :--- |
| `Could not locate Gemfile` | 터미널 작업 위치가 상위 폴더인 경우 | `cd /Users/hojin9/dev/jinysite/php_laravel` 로 프로젝트 루트 이동 후 실행 |
| `Liquid Exception: Unknown tag ...` | 라라벨 Blade `{{ ... }}` 문법 충돌 | 본문 시작에 `{% raw %}`, 끝에 `{% endraw %}` 태그 추가 |
| `Port 4000 is already in use` | 이전 지킬 프로세스가 포트를 점유 중인 경우 | `pkill -f jekyll` 또는 `kill $(lsof -t -i:4000)` 실행 후 재시작 |
| `PowerShell 스크립트 실행 불가 (PSSecurityException)` | Windows 실행 정책 제한 | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 실행 후 터미널 재시작 |
| `Faraday v2.0+` 경고 메시지 출력 | Faraday 미들웨어 알림 (무시 가능) | 사이트 빌드/실행에는 영향 없음. 필요 시 `gem install faraday-retry` |
| `Conflict: ... index.html and index.md` | 동일 출력 경로 중복 충돌 | 프론트매터에 고유 `permalink` 부여 (예: `permalink: /roadmap/`) |


