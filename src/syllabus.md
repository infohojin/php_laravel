---
layout: docs
title: "지니와 도로시의 라라벨 마스터 클래스: 14주 핸드온 쇼핑몰 프로젝트 (Syllabus)"
---

{% raw %}
# 🛒 지니와 도로시의 라라벨 마스터 클래스: 14주 핸드온 쇼핑몰 프로젝트 (Syllabus)

> **프로젝트명:** 지니샵 (JinyShop / jinyshop) — 현대적인 풀스택 도서 커머스 시스템 (도서, 저자, 출판사, eBook, 서평, 주문)  
> **등장인물:** 🐱 지니(강의자/멘토), 👧 도로시(개발자/학습자), 🐶 토토(개발 보조/길잡이)  
> **캐릭터 가이드 참조:** [`src/character.md`](./src/character.md)  
> **교재/참조:** 라라벨 공식 문서 최신판(13.x) 한국어 번역본 (`php_laravel/src/`)  
> **방식:** 100% 핸드온 실습 + 친근한 협업 대화형 스토리텔링 (하나의 완전한 온라인 도서 쇼핑몰(지니샵)을 구축하며 공식 문서 103개 주제를 체화)  

---

## 👥 주인공 캐릭터 소개 & 학습 페르소나

본 강좌는 지니, 도로시, 토토 세 주인공이 함께 **지니샵(JinyShop)**이라는 실전 쇼핑몰을 기획하고 한 줄 한 줄 코딩해 나가는 친근한 대화형 스토리로 진행됩니다.

| 캐릭터 | 역할 | 페르소나 및 설명 | 대화 아이콘 |
| :---: | :---: | :--- | :---: |
| **지니 (Jiny)** | **강의자 / 시니어 멘토** | 보랏빛 마법사 고양이. 날렵하고 영리하며 상냥한 시니어 시스템 아키텍트입니다. 라라벨의 보이지 않는 내부 원리(서비스 컨테이너, 파사드, 생명주기)와 베스트 프랙티스를 알기 쉽게 짚어줍니다. | 🐱 **지니** |
| **도로시 (Dorothy)** | **개발자 / 학습자** | 초등학교 저학년(8~9세) 치비 SD 체형의 똑똑하고 호기심 많은 주니어 개발자입니다. 초보자의 눈높이에서 궁금한 점을 질문하고, 직접 터미널에 명령어를 치며 지니샵의 기능을 구현해 나갑니다. | 👧 **도로시** |
| **토토 (Toto)** | **보조 / 길잡이** | 도로시의 사랑스러운 반려견이자 개발 보조견입니다. 초보자가 범하기 쉬운 실수, 에러 해결 팁, 유용한 CLI 단축키를 꼬리를 흔들며 멍멍 짚어주는 든든한 가이드입니다. | 🐶 **토토** |

---

## 🌟 강좌의 철학과 특징

1. **단 하나의 완성도 높은 실습 프로젝트 ("JinyShop")**
   - 단편적인 예제가 아닌 도서 카탈로그, 종이책/eBook 옵션 및 재고, 장바구니 세션, 회원/권한, 결제, 비동기 주문 처리, 실시간 배송 알림, 전문 검색, AI 상품 추천, 관리자 백오피스를 갖춘 **완전한 이커머스 시스템**을 구축합니다.

2. **공식 문서의 100% 완전 흡수 (생략이나 축소 없음)**
   - 라라벨 공식 문서(11개 그룹, 103개 세부 주제)의 방대한 내용을 단 하나도 누락하지 않습니다.
   - 지나치게 레퍼런스 중심인 공식 문서를 **쇼핑몰 개발 단계에 맞추어 분리, 병합, 재배치**하여 실무 맥락 속에서 자연스럽게 체화합니다.

3. **지니-도로시-토토의 티키타카 협업 대화 (Dialogue Blocks)**
   - 각 주차마다 개념 도입부에 세 캐릭터의 개발 회의 대화가 수록되어 있어, 딱딱한 기술 용어가 아니라 친근한 대화를 통해 "왜 이 기능이 필요한지"를 먼저 이해하고 코딩에 들어갑니다.

4. **프론트엔드 스토어프론트 & 백엔드 관리자 백오피스 듀얼 트랙(Dual-Track) 동시 개발**
   - 독자가 이용하는 **스토어프론트(Storefront)**와 운영자가 관제하는 **백오피스(Admin Backoffice)**를 14주 동안 병행하여 온전한 상용 엔터프라이즈 아키텍처를 구축합니다.

---

## 📅 주차별 종합 커리큘럼 요약표 (프론트엔드 & 백엔드 관리자 듀얼 트랙)

| 주차 | 단계 | 주제 | 🌐 독자용 프론트엔드 (Storefront) | ⚙️ 운영자용 백엔드 관리자 (Admin Backoffice) | 연계 공식 문서 (`src/`) |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **1주** | 환경 & 킥오프 | **환경 구축 & 프로젝트 킥오프** | 웰컴 페이지 브라우징, Tailwind CSS 폰트 및 UI 토큰 준비 | 관리자 디버깅 도구(Telescope, Pint) 구축, Slim 디렉터리 아키텍처 및 `.env` 설정 | `02_getting_started/installation, configuration, structure, ai`, `11_packages/sail, pint, telescope, valet, homestead` |
| **2주** | 코어 웹 기초 | **생명주기, 라우팅 & 컨트롤러** | 도서 홈(`GET /`), 도서 목록/상세 라우트, HTTP 응답 및 리다이렉트 | 관리자 라우트 그룹 분리(`/admin`), 관리자 베이스 컨트롤러 및 요청 파라미터 캡처 | `03_architecture_concepts/lifecycle`, `04_the_basics/routing, controllers, requests, responses, urls` |
| **3주** | 템플릿 & UI | **블레이드 컴포넌트 & 에셋 번들링** | 서점 공통 레이아웃, 헤더 베스트셀러 배너, 도서 카드(`x-book-card`) 컴포넌트, Vite 번들링 | 관리자 백오피스 전용 레이아웃(`admin.blade.php`), 관리자 사이드바 컴포넌트, CSRF 보안 방어 | `04_the_basics/views, blade, vite, csrf`, `02_getting_started/frontend`, `11_packages/mix, head` |
| **4주** | 데이터베이스 | **데이터베이스 마이그레이션 & 대량 시딩** | 고객에게 노출될 도서, 저자, 출판사, 카테고리 스키마 구조 | 관리자 관점의 1,000권 도서 대량 시딩(`DatabaseSeeder`), Faker 팩토리, 품절/비공개 데이터 분리 | `07_database/database, migrations, seeding`, `08_eloquent_orm/eloquent-factories` |
| **5주** | ORM 기초 | **Eloquent ORM 기초 & 상품 카탈로그** | 도서 카탈로그, 다조건 필터링, 가격 정렬, 페이지네이션, SEO 친화적 슬러그 | 관리자용 도서 재고 목록 쿼리, 소프트 삭제(Soft Deletes)된 절판 도서 복원 및 영구 삭제 | `08_eloquent_orm/eloquent, eloquent-mutators`, `07_database/queries, pagination`, `05_digging_deeper/strings` |
| **6주** | ORM 심화 | **Eloquent 데이터 관계(Relationships) 심화 & N+1 해결** | 도서 상세의 다형성 서평(Reviews) 목록 및 별점, 관련 저자/출판사 도서 표시 | 관리자용 서평 검수/블라인드 처리, 다형성 이미지 첨부 관리, N+1 쿼리 최적화 진단 | `08_eloquent_orm/eloquent-relationships, eloquent-collections`, `05_digging_deeper/collections` |
| **7주** | 입력 & 상태 | **폼 유효성 검사, 세션 상태 관리 & 장바구니** | 장바구니 세션(담기, 수량변경, 삭제), Precognition 실시간 폼 유효성 검사 | 관리자용 장바구니 이탈률 통계 및 MongoDB 하이브리드 사용자 행동/열람 감사 로그 분석 | `04_the_basics/validation, session`, `11_packages/precognition`, `07_database/mongodb` |
| **8주** | 보안 & 인증 | **사용자 인증, 소셜 로그인 & 권한 정책** | 일반 독자 회원가입/로그인, 이메일 인증, 소셜 로그인(구글/카카오), 내 서평 수정 Policy | 관리자 전용 Gate/Policy (`EnsureUserIsAdmin`), 관리자 계정 권한 부여 및 Passport 제휴사 관리 | `06_security/authentication, authorization, verification, passwords, hashing, encryption`, `11_packages/socialite, fortify, passport`, `02_getting_started/starter-kits` |
| **9주** | 파일 & 관리자 | **파일 스토리지, 미들웨어 & 백오피스 관리자 페이지** | 고화질 WebP 도서 표지 및 미리보기 이미지 최적화 서빙, 감성적 404 에러 화면 | 관리자 전용 백오피스 대시보드(`/admin/dashboard`), 신규 도서 등록 CRUD 폼, 표지 파일 업로드(Flysystem), Rate Limiting 및 Monolog 감사 로그 | `05_digging_deeper/filesystem, images, rate-limiting`, `04_the_basics/middleware, errors, logging` |
| **10주** | 아키텍처 | **라라벨 내부 동작 원리 (컨테이너, 프로바이더, 파사드)** | 고객용 주문서 작성 및 토스/스트라이프 PG사 결제 승인 화면 | 관리자용 결제 대행사(PG) 동적 스위칭 바인딩(PaymentServiceProvider), 결제 취소/환불 추적 및 Context 로깅 | `03_architecture_concepts/container, providers, facades`, `05_digging_deeper/contracts, context, helpers, http-client` |
| **11주** | 비동기 & 결제 | **이벤트, 비동기 큐, 알림 시스템 & 주문/결제 연동** | 주문 완료 시 마크다운 영수증 메일 수신, 마이페이지 인앱 알림 뱃지, 북클럽 정기 구독 | 관리자용 고액 주문 발생 시 Slack 실시간 웹훅 경보, Redis 큐 모니터링을 위한 Laravel Horizon 대시보드 | `05_digging_deeper/events, queues, mail, notifications`, `11_packages/billing, cashier-paddle, horizon` |
| **12주** | 자동화 & 실시간 | **아티산 CLI, 스케줄링, 캐시 & 웹소켓 실시간 브로드캐스팅** | 다국어 언어팩(한국어/영어/일본어), 통화 표기 스위처(KRW/USD), 베스트셀러 고속 Redis 캐싱 | 물류 창고 관리자용 대화형 아티산 CLI(`shop:restock`) 재고 입고 도구, 자정 미결제 취소 크론 스케줄러, 실시간 신규 주문 수신 Reverb 웹소켓 토스트 알림 | `05_digging_deeper/artisan, scheduling, cache, broadcasting, concurrency, processes, localization`, `11_packages/prompts, reverb`, `07_database/redis` |
| **13주** | API & AI | **RESTful API, Sanctum 토큰 인증, 검색 & AI 기능 탑재** | 모바일 앱 연동 RESTful API, Sanctum 토큰 인증, 10ms Scout 도서 전문 검색, 봄맞이 기획전 Folio 페이지 | 관리자 도서 등록 시 Laravel AI SDK를 이용한 마케팅 카피 자동 생성, AI 에이전트 연동 재고 조회 MCP 도구, Pennant 신규 결제창 A/B 테스트 피처 플래그 | `08_eloquent_orm/eloquent-resources, eloquent-serialization`, `11_packages/sanctum, scout, pennant, folio`, `09_ai/ai-sdk, mcp, boost`, `05_digging_deeper/search` |
| **14주** | 테스트 & 배포 | **테스트 자동화, 브라우저 E2E, 모니터링 & 프로덕션 배포** | 실제 고객 구매 플로우(장바구니 $\rightarrow$ 결제 $\rightarrow$ 완료) Feature 테스트 및 Dusk 브라우저 E2E 테스트 | 관리자 백오피스 APM 모니터링(Laravel Pulse: 느린 쿼리/요청 관제), Octane 초고속 서빙, Envoy 무중단 배포 스크립트 | `10_testing/testing, http-tests, console-tests, database-testing, mocking, dusk`, `11_packages/pulse, octane, envoy`, `05_digging_deeper/packages`, `02_getting_started/deployment`, `01_prologue/releases, upgrade, contributions` |

---

## 📖 14주 상세 강의 및 실습 계획서

---

### [01주차] 라라벨과의 첫 만남 & 개발 환경 구축 (JinyShop 프로젝트 킥오프)

> 📖 **주차별 상세 실습 가이드:** [week01 실습 바로가기](./week01/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 우리가 직접 멋진 쇼핑몰 **'지니샵(JinyShop)'**을 만들기로 했잖아! 그런데 PHP로 웹 서비스를 만들 때 왜 다들 라라벨을 추천하는 거야?"  
> 🐱 **지니**: "좋은 질문이야 도로시! 과거에는 데이터베이스 연결부터 라우팅, 보안까지 수천 줄의 코드를 직접 짜야 했단다. 하지만 라라벨은 현대적인 아키텍처와 '개발자의 행복'을 최우선으로 둔 우아한 문법을 제공해주지. 마치 요술 램프에서 마법 도구가 쏟아져 나오는 것과 같단다!"  
> 🐶 **토토**: "멍멍! 도커가 편하면 Sail을 쓰고, Mac에서는 Herd나 Valet을 쓰면 1초 만에 로컬 서버가 열린다멍! `.env` 파일 설정도 잊지 말자멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 앞으로 14주 동안 개발할 대형 쇼핑몰 **"지니샵(JinyShop)"**의 아키텍처와 비즈니스 요구사항을 이해합니다.
- 현대적인 라라벨 개발 환경(Herd / Sail Docker / Valet / Homestead)을 비교하고, 프로젝트를 성공적으로 생성합니다.
- 코드 품질 검사 도구(Pint), 디버깅 툴(Telescope), AI 코딩 도우미(Boost)를 초기 세팅합니다.

#### 2. 핵심 학습 개념
- PHP 8.2+ 생태계와 라라벨의 설계 철학
- 프로젝트 생성: Composer와 `laravel new jinyshop` 인스톨러 사용법
- 라라벨의 디렉터리 구조 완전 정복 (`app/`, `bootstrap/`, `config/`, `routes/`, `resources/`, `storage/`)
- 환경 설정 시스템: `.env` 파일과 `config/` 캐싱 메커니즘
- 로컬 개발 환경 옵션 비교: Herd, Docker 기반 Sail, macOS 초경량 Valet, 가상머신 Homestead
- 최신 라라벨의 AI 지원: Agentic Development 및 Laravel Boost 활용법

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [설치 (Installation)](./docs/02_getting_started/installation_ko.md)
- [환경 설정 (Configuration)](./docs/02_getting_started/configuration_ko.md)
- [디렉터리 구조 (Directory Structure)](./docs/02_getting_started/structure_ko.md)
- [에이전트 개발 (Agentic Development)](./docs/02_getting_started/ai_ko.md)
- [Sail (도커 환경)](./docs/11_packages/sail_ko.md)
- [Pint (코드 스타일러)](./docs/11_packages/pint_ko.md)
- [Telescope (디버깅 어시스턴트)](./docs/11_packages/telescope_ko.md)
- [Valet (macOS 가상 호스트)](./docs/11_packages/valet_ko.md)
- [Homestead (Vagrant 가상 머신)](./docs/11_packages/homestead_ko.md)

#### 4. 핸드온 실습 과제
1. `laravel new jinyshop` 명령어로 최신 라라벨 프로젝트 생성
2. Git 저장소 초기화 및 기본 커밋
3. `.env` 파일의 `APP_NAME="JinyShop"`, `APP_TIMEZONE="Asia/Seoul"` 등 로컬 환경 설정
4. Laravel Telescope 및 Pint 설치 후 로컬 대시보드 접속 확인

---

### [02주차] 요청 라이프사이클 & 라우팅과 컨트롤러 아키텍처

> 📖 **주차별 상세 실습 가이드:** [week02 실습 바로가기](./week02/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 고객이 브라우저 주소창에 `jinyshop.test/products`라고 입력하고 엔터를 치면, 화면이 나오기 전까지 라라벨 내부에서 어떤 모험이 일어나는 거야?"  
> 🐱 **지니**: "도로시, 그것이 바로 **요청 라이프사이클(Request Lifecycle)**이란다! `public/index.php`라는 현관문으로 들어온 요청은 오토로더를 거쳐 서비스 프로바이더들에 의해 기초 체력이 다져지고, 라우터와 미들웨어라는 검문소를 지나 알맞은 컨트롤러 방으로 안내된단다."  
> 🐶 **토토**: "멍멍! 라우트 이름(Named Routes)을 `route('products.show', $id)`처럼 지어두면 나중에 URL 주소가 바뀌어도 링크가 깨지지 않는다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 브라우저 요청이 라라벨 내부에서 처리되는 전체 라이프사이클을 이해합니다.
- JinyShop 쇼핑몰의 메인 홈, 회사 소개, 고객센터, 상품 목록 조회를 위한 기본 라우트와 컨트롤러 체계를 구성합니다.

#### 2. 핵심 학습 개념
- **HTTP 요청 라이프사이클**: `public/index.php` $
ightarrow$ 부트스트랩 $
ightarrow$ 서비스 프로바이더 $
ightarrow$ 라우터 $
ightarrow$ 미들웨어 $
ightarrow$ 컨트롤러
- 라우팅 기본: GET, POST, PUT, DELETE 메서드와 라우트 파라미터(`{id}`) 및 정규식 제약조건
- 명명된 라우트(Named Routes)와 URL 생성 헬퍼(`route('products.show', $id)`)
- 라우트 그룹: 공통 프리픽스, 미들웨어 그룹 지정
- 컨트롤러 패턴: 기본 컨트롤러, 리소스 컨트롤러(`--resource`), 단일 액션(Invokable) 컨트롤러
- `Request` 객체로부터 쿼리스트링, 입력값, 헤더 정보 안전하게 추출하기
- `Response`의 다양한 형태: 뷰 반환, JSON 응답, 리다이렉트(`redirect()->route(...)`), 파일 다운로드
- 보안 강화를 위한 임시 서명된 URL(Signed URLs) 생성

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [요청 라이프사이클 (Request Lifecycle)](./docs/03_architecture_concepts/lifecycle_ko.md)
- [라우팅 (Routing)](./docs/04_the_basics/routing_ko.md)
- [컨트롤러 (Controllers)](./docs/04_the_basics/controllers_ko.md)
- [요청 (Requests)](./docs/04_the_basics/requests_ko.md)
- [응답 (Responses)](./docs/04_the_basics/responses_ko.md)
- [URL 생성 (URL Generation)](./docs/04_the_basics/urls_ko.md)

#### 4. 핸드온 실습 과제
1. `HomeController` 및 `ProductController` 생성
2. 쇼핑몰 메인 페이지(`/`), 상품 목록(`/products`), 상품 상세(`/products/{slug}`) 라우트 정의
3. 주문 영수증 조회를 위한 유효기간 30분짜리 Signed URL 생성 및 검증 테스트

---

### [03주차] 블레이드 템플릿 엔진 & 프론트엔드 에셋 번들링 (JinyShop UI/UX)

> 📖 **주차별 상세 실습 가이드:** [week03 실습 바로가기](./week03/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 쇼핑몰의 수많은 페이지마다 상단 네비게이션 바랑 푸터 디자인을 매번 복사해서 붙여넣어야 해? 너무 번거로운데..."  
> 🐱 **지니**: "후후, 그럴 필요 전혀 없단다! 라라벨의 **Blade 템플릿 엔진**에는 `<x-layouts.app>` 같은 컴포넌트 마법 상자가 있거든. 슬롯(Slot) 구멍에 본문 내용만 쏙 집어넣으면 전체 레이아웃이 완성된단다!"  
> 🐶 **토토**: "멍멍! 폼 태그 안에 `@csrf`를 안 넣으면 419 에러가 나니까 꼭 챙겨야 해! Vite 개발 서버를 켜두면 CSS 고칠 때마다 브라우저가 알아서 새로고침 된다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 현대적인 쇼핑몰의 반응형 인터페이스(상단 바, 상품 그리드, 카테고리 메뉴, 푸터)를 구축합니다.
- 슬롯 기반 Blade 컴포넌트 아키텍처를 완성하고, Vite를 통해 Tailwind CSS를 번들링합니다.
- SNS 공유 시 예쁜 미리보기가 뜨도록 OpenGraph `<head>` 메타 태그를 제어합니다.

#### 2. 핵심 학습 개념
- Blade 템플릿의 컴파일 원리와 캐싱 메커니즘
- 기본 지시어: `@if`, `@foreach`, `@forelse`, `@empty`, `@auth`, `@guest`
- 보안 필수 지시어: `@csrf` (CSRF 공격 방어 토큰), `@method('PUT')` (HTTP 메서드 스푸핑)
- 컴포넌트와 슬롯(Slots): `<x-layouts.app>`, `<x-product-card>`, `<x-button>`, `<x-badge>` 제작
- 뷰 컴포저(View Composer): 모든 화면에 쇼핑몰 카테고리 목록을 자동 주입하는 패턴
- Vite 에셋 번들링: CSS/JS 빌드, 에셋 캐시 버스팅, 레거시 Webpack(Laravel Mix)과의 차이점
- Head 패키지: 페이지별 동적 `<head>` 메타 태그 및 SEO 최적화

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [뷰 (Views)](./docs/04_the_basics/views_ko.md)
- [블레이드 템플릿 (Blade Templates)](./docs/04_the_basics/blade_ko.md)
- [에셋 번들링 (Vite)](./docs/04_the_basics/vite_ko.md)
- [CSRF 보호 (CSRF Protection)](./docs/04_the_basics/csrf_ko.md)
- [프론트엔드 (Frontend)](./docs/02_getting_started/frontend_ko.md)
- [Mix (레거시 번들러)](./docs/11_packages/mix_ko.md)
- [Head (SPA 메타 태그 제어)](./docs/11_packages/head_ko.md)

#### 4. 핸드온 실습 과제
1. `<x-layouts.app>` 마스터 레이아웃 컴포넌트 작성 (반응형 내비게이션 바, 푸터 포함)
2. 재사용 가능한 `<x-product-card>` 컴포넌트 제작 (상품 이미지, 배지, 가격, 장바구니 버튼)
3. 쇼핑몰 홈 화면에 '인기 상품 슬라이더' 및 '신상품 그리드' 뷰 구현

---

### [04주차] 데이터베이스 마이그레이션과 시딩 (데이터 모델링)

> 📖 **주차별 상세 실습 가이드:** [week04 실습 바로가기](./week04/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 우리 지니샵에 상품 종류가 수천 개는 될 텐데, DB 테이블을 만들다가 컬럼을 깜빡하면 어떻게 해? DB를 통째로 지우고 다시 만들어야 하나?"  
> 🐱 **지니**: "걱정 마렴 도로시! 라라벨에는 **마이그레이션(Migration)**이라는 데이터베이스 전용 타임머신이 있단다. 코드 형태로 테이블 변경 이력을 기록하기 때문에 언제든 뒤로 롤백하거나 최신 상태로 되돌릴 수 있지."  
> 🐶 **토토**: "멍멍! 게다가 Faker 팩토리와 시더(Seeder)를 실행하면, 눈 깜짝할 사이에 1,000개의 알록달록한 한국어 가짜 상품 데이터가 촤르륵 채워진다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 지니샵에 필요한 핵심 데이터베이스 구조(카테고리, 상품, 옵션, 사용자)를 체계적으로 설계합니다.
- 마이그레이션 파일로 스키마 버전 관리를 수행하고, Faker 모델 팩토리로 1,000건의 테스트 데이터를 자동 생성합니다.

#### 2. 핵심 학습 개념
- 라라벨 데이터베이스 연결 설정: MySQL/PostgreSQL/SQLite
- 스키마 빌더(Schema Builder): 테이블 생성, 컬럼 타입(문자, 정수, 소수, JSON, 불리언)
- 외래키 제약조건(`foreignId()->constrained()->cascadeOnDelete()`)과 복합 인덱스
- 마이그레이션 라이프사이클: `up()`, `down()`, 롤백(`migrate:rollback`), 재생성(`migrate:fresh`)
- 모델 팩토리(Model Factories): Faker 한국어 로케일을 활용한 실감 나는 가짜 데이터 정의
- 시더(Database Seeder): 카테고리 계층 구조 생성 및 대량 시딩 전략
- 데이터베이스 트랜잭션 기초: `DB::transaction()`의 원자성(ACID) 보장

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [데이터베이스 시작하기 (Database)](./docs/07_database/database_ko.md)
- [마이그레이션 (Migrations)](./docs/07_database/migrations_ko.md)
- [시딩 (Seeding)](./docs/07_database/seeding_ko.md)
- [Eloquent 팩토리 (Eloquent Factories)](./docs/08_eloquent_orm/eloquent-factories_ko.md)

#### 4. 핸드온 실습 과제
1. `categories`, `products`, `product_images`, `users` 마이그레이션 작성
2. `CategoryFactory` 및 `ProductFactory`를 통해 실감 나는 전자제품/패션 상품 데이터 정의
3. `php artisan migrate:fresh --seed`로 한 번에 완벽한 초기 쇼핑몰 데이터베이스 구축

---

### [05주차] Eloquent ORM 기초 & 상품 카탈로그 및 페이징

> 📖 **주차별 상세 실습 가이드:** [week05 실습 바로가기](./week05/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 데이터베이스에서 상품을 가져올 때 길고 복잡한 `SELECT * FROM products WHERE...` SQL 문을 직접 쓰지 않고도 `Product::where('is_active', true)->get()`처럼 쓸 수 있다니 마법 같아!"  
> 🐱 **지니**: "그게 바로 라라벨이 자랑하는 **Eloquent Active Record 패턴**이란다! 데이터베이스 테이블 한 행이 PHP 객체 하나와 일대일로 연결되어, 메서드 체이닝만으로 정렬과 검색, 수정, 저장을 자유자재로 다룰 수 있지."  
> 🐶 **토토**: "멍멍! 상품을 실수로 삭제해도 `SoftDeletes`를 켜두면 복구할 수 있어! 그리고 상품 이름을 영어 URL 슬러그로 바꿀 땐 `Str::slug()`를 쓰면 된다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- Eloquent Active Record 패턴을 마스터하여 상품 카탈로그의 조회, 정렬, 필터링, 페이징을 구현합니다.
- 상품의 고유 URL 슬러그(`Str::slug`) 생성 및 품절/삭제 상품을 보존하는 소프트 삭제(Soft Deletes)를 적용합니다.

#### 2. 핵심 학습 개념
- Eloquent 모델 규칙: 테이블명 복수형 규약, 기본키, 타임스탬프(`created_at`, `updated_at`)
- 대량 할당(Mass Assignment) 보안: `$fillable`과 `$guarded`의 철저한 이해
- CRUD 작업: `create()`, `update()`, `delete()`, `firstOrCreate()`, `findOrFail()`
- 쿼리 스코프(Query Scopes): 비즈니스 조건 캡슐화 (`scopeActive()`, `scopePriceBetween()`)
- 소프트 삭제(Soft Deletes): `SoftDeletes` 트레이트, `trashed()`, `restore()`, `forceDelete()`
- 접근자(Accessors)와 뮤테이터(Mutators): 속성 자동 가공 (가격 원화 포맷팅 `15,000원`)
- 속성 캐스팅(Attribute Casting): `casts()` 메서드로 JSON 배열 및 Enum 자동 변환
- 문자열 조작: `Str::slug()`, Stringable Fluent 인터페이스
- 대용량 데이터 페이징: `paginate()` vs 모바일 무한 스크롤용 `cursorPaginate()`

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [Eloquent 시작하기 (Eloquent)](./docs/08_eloquent_orm/eloquent_ko.md)
- [쿼리 빌더 (Queries)](./docs/07_database/queries_ko.md)
- [페이지네이션 (Pagination)](./docs/07_database/pagination_ko.md)
- [뮤테이터와 캐스트 (Mutators & Casts)](./docs/08_eloquent_orm/eloquent-mutators_ko.md)
- [문자열 조작 (Strings)](./docs/05_digging_deeper/strings_ko.md)

#### 4. 핸드온 실습 과제
1. `Product` 모델에 접근자/캐스트 작성 (가격 포맷, 상품 배지 상태)
2. 카테고리 선택 및 가격대 필터가 동작하는 상품 목록 페이지 완성
3. 데스크톱용 번호 페이지네이션과 모바일용 무한 스크롤(Cursor Pagination) 적용

---

### [06주차] Eloquent 데이터 관계(Relationships) 심화 & N+1 해결

> 📖 **주차별 상세 실습 가이드:** [week06 실습 바로가기](./week06/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니, 큰일 났어! 상품 목록 화면에 카테고리 이름과 이미지들을 같이 띄웠더니, Telescope에서 SQL 쿼리가 100개 넘게 터져 나와서 페이지가 엄청 느려졌어!"  
> 🐱 **지니**: "하하, 도로시가 웹 개발자들의 영원한 숙적인 **'N+1 쿼리 폭발 문제'**를 만났구나! 루프를 돌면서 매번 연관 데이터를 따로 질의하기 때문이란다. 이럴 땐 마법 주문 `with(['category', 'images'])`를 써서 **즉시 로딩(Eager Loading)**을 해주면 쿼리 2개로 압축할 수 있단다!"  
> 🐶 **토토**: "멍멍! 회원은 여러 주문을 하고, 주문은 여러 상품을 담으니 N:M 피벗(Pivot) 관계가 필요해! 대량 데이터 계산할 땐 `LazyCollection`을 써야 메모리가 안 터진다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 회원-주문, 카테고리-상품, 주문-상품(피벗), 상품/리뷰 다형성 이미지를 Eloquent 관계로 구현합니다.
- 서비스 장애의 주범인 N+1 쿼리 문제를 진단하고 즉시 로딩(Eager Loading)으로 극적인 성능 최적화를 달성합니다.

#### 2. 핵심 학습 개념
- **1:1 관계**: `hasOne` / `belongsTo` (회원 - 프로필)
- **1:N 관계**: `hasMany` / `belongsTo` (카테고리 - 상품, 회원 - 주문)
- **N:M 관계와 피벗 테이블(Pivot Table)**: `belongsToMany` (주문 - 상품, 수량 및 주문 당시 단가 속성)
- **원격 1:N (Has Many Through)**: 브랜드(Brand) - 상품(Product) - 리뷰(Review)
- **다형성 관계 (Polymorphic Relations)**: `morphMany` (상품에도 달리고, 리뷰에도 달리는 이미지)
- **N+1 문제의 정체와 해결**: Lazy Loading vs Eager Loading (`with(['category', 'images'])`)
- 조건부 Eager Loading 및 카운트 조회 (`withCount('reviews')`)
- Eloquent Collections의 풍부한 함수형 메서드 (`map`, `filter`, `groupBy`, `sortBy`)
- 대용량 데이터 처리를 위한 제너레이터 기반 지연 컬렉션(`LazyCollection::cursor()`)

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [Eloquent 관계 (Eloquent Relationships)](./docs/08_eloquent_orm/eloquent-relationships_ko.md)
- [Eloquent 컬렉션 (Eloquent Collections)](./docs/08_eloquent_orm/eloquent-collections_ko.md)
- [컬렉션 심화 (Collections)](./docs/05_digging_deeper/collections_ko.md)

#### 4. 핸드온 실습 과제
1. `Order` $\leftrightarrow$ `Product` 간 피벗 테이블(`order_items`)을 만들고 추가 속성(수량, 주문 당시 단가) 매핑
2. 상품 상세 페이지에서 상품, 카테고리, 다형성 이미지, 리뷰 목록을 N+1 없이 2개의 쿼리로 최적화 조회
3. 쇼핑몰 월간 정산 스크립트를 `LazyCollection`으로 작성하여 대량 데이터 메모리 10MB 이하 유지 확인

---

### [07주차] 폼 유효성 검사, 세션 상태 관리 & 장바구니 시스템

> 📖 **주차별 상세 실습 가이드:** [week07 실습 바로가기](./week07/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 고객이 상품 수량에 음수나 문자를 적어 보내면 어쩌지? 그리고 로그인하지 않은 손님이 담은 장바구니 물건들은 어디에 보관해야 안전할까?"  
> 🐱 **지니**: "도로시, 절대로 사용자의 입력을 믿어선 안 된단다! 라라벨의 **Form Request**를 사용하면 컨트롤러에 도달하기 전에 모든 악의적인 입력을 철저히 차단할 수 있지. 그리고 비회원 손님의 장바구니는 암호화된 **세션(Session)** 마법 상자에 안전하게 보관하면 된단다!"  
> 🐶 **토토**: "멍멍! Precognition을 쓰면 폼을 제출하기 전에도 타이핑하는 즉시 실시간으로 에러를 띄워줄 수 있어! 비정형 장바구니 로그는 MongoDB에 쏙쏙 담아두자멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 사용자의 잘못된 입력을 안전하게 방어하는 Form Request 유효성 검사 체계를 구축합니다.
- 비회원도 물건을 담아둘 수 있는 세션 기반 장바구니 시스템을 구현합니다.
- Precognition 기반 실시간 검증 피드백 및 NoSQL(MongoDB) 하이브리드 연동을 학습합니다.

#### 2. 핵심 학습 개념
- 유효성 검사 기본: 컨트롤러 내 `$request->validate()`
- 주요 검증 규칙: `required`, `numeric`, `min`, `max`, `exists`, `unique`
- 에러 표시와 이전 입력값 복원: `@error` 지시어와 `old('quantity')` 헬퍼
- **Form Request 클래스**: 비즈니스 검증 로직 분리 (`StoreCartItemRequest`)
- 커스텀 검증 룰(Custom Validation Rule): "남은 재고보다 많은 수량을 주문할 수 없음"
- 세션(Session)의 작동 원리: 쿠키와 세션 ID, 파일/데이터베이스/Redis 드라이버
- 세션 메서드: `put()`, `get()`, `forget()`, `flash()` (1회성 알림 메시지)
- 라라벨 프리코그니션(Precognition): SPA나 프론트엔드 변경 없이 실시간 백엔드 검증 응답
- NoSQL 데이터베이스(MongoDB) 연동: 비정형 상품 로그 및 장바구니 클릭스트림 수집

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [유효성 검사 (Validation)](./docs/04_the_basics/validation_ko.md)
- [세션 (Session)](./docs/04_the_basics/session_ko.md)
- [Precognition (실시간 유효성 검사)](./docs/11_packages/precognition_ko.md)
- [MongoDB (몽고DB 연동)](./docs/07_database/mongodb_ko.md)

#### 4. 핸드온 실습 과제
1. `CartService`를 제작하여 세션 기반 장바구니 추가, 수량 변경, 항목 삭제 구현
2. `AddToCartRequest` Form Request 클래스로 재고 수량 초과 검증
3. 주문서 작성 폼에서 주소, 전화번호 입력 시 Precognition을 이용한 실시간 에러 피드백 적용

---

### [08주차] 사용자 인증, 소셜 로그인 & 권한 정책 (Security & Auth)

> 📖 **주차별 상세 실습 가이드:** [week08 실습 바로가기](./week08/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 고객들이 아이디랑 비밀번호를 입력하고 가입하는 인증 과정은 직접 테이블 만들고 세션 쿠키 구워서 만들어야 해? 그리고 다른 사람의 주문서를 훔쳐보는 나쁜 손님은 어떻게 막지?"  
> 🐱 **지니**: "라라벨에는 **Breeze / Fortify**라는 튼튼한 성벽이 준비되어 있단다! 비밀번호는 안전하게 Bcrypt로 해싱되고, 이메일 소유권도 자동으로 인증하지. 남의 주문서를 훔쳐보는 행위는 **Policy(정책)**라는 문지기를 세워 403 Forbidden으로 단칼에 튕겨내면 된단다!"  
> 🐶 **토토**: "멍멍! 구글이나 카카오 로그인 버튼 하나 달아주면 손님들이 너무 편해해! Socialite 패키지를 쓰면 5분 만에 연동된다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 안전한 회원가입, 이메일 인증, 로그인, 비밀번호 찾기 프로세스를 구축합니다.
- 복잡한 가입 절차 없이 편리하게 가입할 수 있도록 구글/카카오 소셜 로그인을 연동합니다.
- 일반 고객과 쇼핑몰 관리자(Admin)를 분리하고, 본인의 주문 내역만 열람/수정할 수 있도록 접근을 통제합니다.

#### 2. 핵심 학습 개념
- 라라벨 인증 아키텍처: 가드(Guards, 웹 세션/API 토큰)와 프로바이더(Providers, 유저 저장소)
- `Auth` 파사드와 인증 헬퍼: `Auth::check()`, `Auth::user()`, `Auth::attempt()`
- 스타터 키트(Laravel Breeze) 및 헤드리스 인증 패키지(Laravel Fortify)의 동작 메커니즘
- 비밀번호 암호화: Bcrypt / Argon2 해싱과 `Hash::make()`, `Hash::check()`
- 이메일 인증: `MustVerifyEmail` 인터페이스와 인증 링크 검증
- 비밀번호 재설정 브로커: 토큰 생성, 만료 시간, 재설정 알림
- **인가(Authorization)**: 게이트(Gates)를 이용한 간단한 클로저 권한 검사
- **정책(Policies)**: 모델별 인가 규칙 (`OrderPolicy` - "자신의 주문만 취소 가능")
- Blade 지시어에서의 권한 체크: `@can('cancel', $order)`
- **Socialite 패키지**: OAuth2 프로토콜을 이용한 소셜 로그인 연동
- **Passport 패키지**: B2B 제휴사용 정식 OAuth2 인증 서버 비교

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [인증 (Authentication)](./docs/06_security/authentication_ko.md)
- [인가 (Authorization)](./docs/06_security/authorization_ko.md)
- [이메일 인증 (Email Verification)](./docs/06_security/verification_ko.md)
- [비밀번호 재설정 (Password Reset)](./docs/06_security/passwords_ko.md)
- [해싱 (Hashing)](./docs/06_security/hashing_ko.md)
- [암호화 (Encryption)](./docs/06_security/encryption_ko.md)
- [스타터 키트 (Starter Kits)](./docs/02_getting_started/starter-kits_ko.md)
- [Fortify (인증 백엔드)](./docs/11_packages/fortify_ko.md)
- [Socialite (소셜 로그인)](./docs/11_packages/socialite_ko.md)
- [Passport (OAuth2 서버)](./docs/11_packages/passport_ko.md)

#### 4. 핸드온 실습 과제
1. 라라벨 인증 플로우 세팅 (회원가입, 로그인, 로그아웃, 비밀번호 재설정)
2. `OrderPolicy` 작성: 다른 사람의 주문 조회 및 주문 취소 시도 원천 차단 (403 Forbidden)
3. Socialite를 활용한 Google 소셜 로그인 연동 및 신규 회원 자동 등록 처리

---

### [09주차] 파일 스토리지, 미들웨어 & 백오피스 관리자 페이지

> 📖 **주차별 상세 실습 가이드:** [week09 실습 바로가기](./week09/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 쇼핑몰 관리자가 상품을 새로 등록할 때 사진을 여러 장 올릴 수 있어야 해. 그런데 고화질 사진을 그대로 올리니까 페이지 용량이 너무 커지고 서버가 버벅거려!"  
> 🐱 **지니**: "도로시, 라라벨의 **Flysystem 파일 스토리지**와 **Images 패키지**를 조합할 차례란다! 업로드된 이미지를 800px 너비로 자동 리사이징하고 최신 WebP 포맷으로 압축하면 용량을 90% 줄일 수 있지. 그리고 관리자 페이지는 미들웨어 성벽 뒤에 숨겨두어야 한단다."  
> 🐶 **토토**: "멍멍! 봇들이 결제 버튼을 1초에 백 번 누르지 못하게 Rate Limiting 속도 제한도 꼭 걸어야 해! 이상 징후는 Slack 채널로 삐뽀삐뽀 로깅하자멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 관리자가 상품을 등록하고 수정할 수 있는 전용 백오피스(어드민 대시보드)를 구축합니다.
- 상품 대표/상세 이미지를 안전하게 업로드하고, 크기별 썸네일을 자동 생성하며 WebP로 최적화합니다.
- 일반 사용자의 접근을 차단하는 커스텀 미들웨어, 악의적 트래픽 방어(Rate Limiting), 시스템 감사 로깅을 구성합니다.

#### 2. 핵심 학습 개념
- 라라벨 파일 스토리지(Flysystem): `local`, `public`, `s3` 디스크 추상화
- 파일 업로드 처리: 파일 검증(확장자, 용량, MIME 타입), `$file->store('products', 'public')`
- 심볼릭 링크: `php artisan storage:link`의 동작 원리와 파일 공개 서빙
- 이미지 조작(Images): 이미지 크기 조정, 크롭, WebP 압축을 통한 최적화
- **미들웨어 심화**:
  - 관리자 전용 미들웨어 작성 (`EnsureUserIsAdmin`)
  - 미들웨어 파라미터 전달 (`role:admin`)
  - 글로벌 미들웨어 vs 라우트 미들웨어 vs 미들웨어 그룹
- **속도 제한 (Rate Limiting)**: 결제 및 장바구니 요청에 대한 Throttling 제어
- 에러 핸들링: 커스텀 예외 렌더링, 404/500 에러 페이지 커스터마이징
- 로깅 시스템(Logging): 단일 채널, 일별 로테이션(`daily`), Slack/Discord 웹훅 긴급 에러 알림

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [파일 스토리지 (File Storage)](./docs/05_digging_deeper/filesystem_ko.md)
- [이미지 처리 (Images)](./docs/05_digging_deeper/images_ko.md)
- [미들웨어 (Middleware)](./docs/04_the_basics/middleware_ko.md)
- [에러 핸들링 (Error Handling)](./docs/04_the_basics/errors_ko.md)
- [로깅 (Logging)](./docs/04_the_basics/logging_ko.md)
- [속도 제한 (Rate Limiting)](./docs/05_digging_deeper/rate-limiting_ko.md)

#### 4. 핸드온 실습 과제
1. `/admin` 경로로 시작하는 관리자 전용 라우트 그룹 및 `EnsureUserIsAdmin` 미들웨어 구현
2. 관리자 상품 등록 폼: 멀티 이미지 업로드 및 가로 800px 썸네일 변환 저장
3. 분당 10회 이상 비정상 결제 시도 시 Rate Limiting 차단 및 `Log::warning()`으로 감사 로그 기록

---

### [10주차] 라라벨 코어 아키텍처 Deep Dive (컨테이너, 프로바이더, 파사드)

> 📖 **주차별 상세 실습 가이드:** [week10 실습 바로가기](./week10/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 라라벨 코드를 볼 때마다 너무 신기해. `Payment::charge()`처럼 클래스를 `new`로 생성하지도 않았는데 어떻게 메서드가 실행되는 거야? 그리고 결제 회사를 토스페이에서 스트라이프로 바꾸려면 코드를 다 뜯어고쳐야 해?"  
> 🐱 **지니**: "후후, 이제 드디어 라라벨의 가장 깊은 심장부를 열어볼 때가 되었구나! **서비스 컨테이너(Service Container)**가 객체의 탄생과 의존성을 자동으로 해결해주고, **파사드(Facade)**는 그 뒤에 있는 진짜 인스턴스로 연결해주는 마법의 통로란다. 인터페이스(Contract)를 세워두면 단 한 줄의 코드 수정으로 결제사를 바꿀 수 있지!"  
> 🐶 **토토**: "멍멍! 외부 PG사와 통신할 때는 라라벨 내장 `Http::timeout(5)->retry(3)` HTTP 클라이언트를 쓰면 네트워크 장애도 끄떡없다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 초보자가 가장 마법처럼 느끼는 3대 핵심 아키텍처(서비스 컨테이너, 프로바이더, 파사드)의 내부 원리를 완벽히 이해합니다.
- JinyShop 결제 시스템을 다양한 PG사(토스페이, 카카오페이, 스트라이프)로 자유롭게 교체할 수 있도록 객체지향 인터페이스(Contract)와 의존성 주입(DI)으로 설계합니다.

#### 2. 핵심 학습 개념
- 제어의 역전(IoC)과 **서비스 컨테이너(Service Container)**의 본질
- 바인딩 방식: 단순 바인딩(`bind`), 싱글톤(`singleton`), 인스턴스 바인딩, 컨텍스추얼 바인딩
- 자동 의존성 주입(Auto-wiring): 리플렉션(Reflection)을 통한 의존성 자동 해결
- **서비스 프로바이더(Service Providers)**:
  - `register()` 메서드: 서비스 등록만 수행 (순수 바인딩)
  - `boot()` 메서드: 모든 서비스가 등록된 후 초기화 작업 수행
- **파사드(Facades)**: 정적 호출 문법 뒤에 숨겨진 컨테이너 해결 구조 (`getFacadeAccessor()`)
- **컨트랙트(Contracts)**: 결제 게이트웨이 인터페이스 추상화
- **HTTP 클라이언트 (HTTP Client)**: Guzzle 기반 외부 PG사 REST API 통신, 재시도 및 타임아웃
- 컨텍스트(Context) 헬퍼와 글로벌 헬퍼 함수 작성법

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [서비스 컨테이너 (Service Container)](./docs/03_architecture_concepts/container_ko.md)
- [서비스 프로바이더 (Service Providers)](./docs/03_architecture_concepts/providers_ko.md)
- [파사드 (Facades)](./docs/03_architecture_concepts/facades_ko.md)
- [컨트랙트 (Contracts)](./docs/05_digging_deeper/contracts_ko.md)
- [컨텍스트 (Context)](./docs/05_digging_deeper/context_ko.md)
- [헬퍼 (Helpers)](./docs/05_digging_deeper/helpers_ko.md)
- [HTTP 클라이언트 (HTTP Client)](./docs/05_digging_deeper/http-client_ko.md)

#### 4. 핸드온 실습 과제
1. `PaymentGatewayContract` 인터페이스 정의 및 `TossPaymentGateway`, `MockPaymentGateway` 구현
2. `PaymentServiceProvider`를 제작하여 설정값에 따라 알맞은 결제 구현체 자동 바인딩
3. `Payment` 파사드를 생성하여 컨트롤러에서 한 줄로 우아하게 결제 호출 처리

---

### [11주차] 비동기 큐, 이벤트, 알림 시스템 & 주문/결제 프로세스

> 📖 **주차별 상세 실습 가이드:** [week11 실습 바로가기](./week11/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 고객이 '주문하기' 버튼을 눌렀는데 화면이 5초 동안 뱅글뱅글 돌면서 멈춰 있어! 결제 승인받고, 주문서 이메일 보내고, 재고 깎고, 관리자 슬랙 알림 보내는 걸 한꺼번에 하려니까 손님이 화를 낼 것 같아!"  
> 🐱 **지니**: "바로 그럴 때 **이벤트(Event)**와 **비동기 큐(Queue)** 마법을 쓰는 거란다! 주문 컨트롤러는 `OrderPlaced` 이벤트만 빵 터뜨리고 0.1초 만에 고객에게 '주문 완료!' 화면을 보여주는 거지. 메일 발송과 슬랙 알림은 백그라운드 큐 워커들이 뒤에서 묵묵히 처리한단다!"  
> 🐶 **토토**: "멍멍! 라라벨 Horizon 대시보드를 켜두면 지금 큐에서 몇 건의 메일이 발송 중이고 실패한 작업은 없는지 실시간 그래프로 한눈에 볼 수 있다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 주문 완료 시 동기적으로 실행되던 무거운 후속 작업들을 **이벤트 기반 아키텍처**와 **비동기 큐(Queue)**로 분리합니다.
- 주문 확인 메일과 슬랙 관리자 알림을 비동기로 발송하고, Laravel Horizon을 통해 큐 상태를 모니터링합니다.
- 라라벨 캐셔(Cashier)를 이용한 정기 결제 및 글로벌 결제 흐름을 체득합니다.

#### 2. 핵심 학습 개념
- 동기 vs 비동기 처리의 응답 속도 차이
- **이벤트 시스템**:
  - `OrderPlaced` 이벤트 생성
  - 다중 독립 리스너: `DeductProductStock`, `SendOrderInvoiceEmail`, `NotifyAdminViaSlack`
- **비동기 큐(Queues)**:
  - 큐 드라이버: Database, Redis, SQS
  - 작업(Job) 클래스와 `ShouldQueue` 인터페이스
  - 작업 딜레이, 재시도 횟수(`$tries`), 타임아웃, 지수 백오프(Exponential Backoff)
  - 실패한 작업(Failed Jobs) 추적 및 재실행(`queue:retry`)
- **라라벨 호라이즌(Laravel Horizon)**: Redis 기반 대기열의 실시간 웹 모니터링 대시보드
- **메일(Mail)**: Mailable 클래스, Markdown 메일 템플릿, 첨부 파일(주문서 PDF)
- **알림(Notifications)**: 다채널(Mail, Database, Slack) 단일 API 전송
- **결제 패키지 (Cashier)**: Stripe / Paddle 결제 및 웹훅 처리

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [이벤트 (Events)](./docs/05_digging_deeper/events_ko.md)
- [큐 (Queues)](./docs/05_digging_deeper/queues_ko.md)
- [메일 (Mail)](./docs/05_digging_deeper/mail_ko.md)
- [알림 (Notifications)](./docs/05_digging_deeper/notifications_ko.md)
- [Cashier Stripe (결제)](./docs/11_packages/billing_ko.md)
- [Cashier Paddle (결제)](./docs/11_packages/cashier-paddle_ko.md)
- [Horizon (Redis 큐 모니터링)](./docs/11_packages/horizon_ko.md)

#### 4. 핸드온 실습 과제
1. 주문 결제 완료 시 `OrderPlaced` 이벤트 디스패치
2. 구매자에게 주문 내역을 안내하는 예쁜 Markdown Mailable 작성 및 백그라운드 큐 발송
3. 고객의 웹 대시보드 종(Bell) 아이콘에 '결제 완료' 인앱 데이터베이스 알림 표시

---

### [12주차] 아티산 CLI 도구, 작업 스케줄링, 캐시 & 웹소켓 실시간 알림

> 📖 **주차별 상세 실습 가이드:** [week12 실습 바로가기](./week12/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 매일 밤 12시마다 미결제 주문을 취소하고 품절된 상품 목록을 뽑아야 하는데, 내가 자다 깨서 수동으로 쿼리를 돌릴 순 없잖아? 그리고 인기 상품 페이지에 접속자가 몰리면 DB가 뻗지 않을까?"  
> 🐱 **지니**: "도로시, 라라벨 **스케줄러(Scheduler)**에 크론 한 줄만 등록해두면 밤마다 알아서 배치가 돈단다! 그리고 인기 상품은 **Redis 캐시**에 담아두면 DB를 거치지 않고 0.001초 만에 응답하지. 여기에 **Reverb 웹소켓**을 붙이면 신규 주문이 들어올 때 관리자 화면에 즉시 팝업이 뜬단다!"  
> 🐶 **토토**: "멍멍! 터미널에서 재고 채울 때는 Laravel Prompts를 쓰면 화살표 키로 메뉴 고르는 멋진 대화형 CLI가 만들어진다멍! 글로벌 손님을 위해 다국어 언어팩도 세팅하자멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 매일 자정 미결제 주문을 자동 취소하고 품절 상품을 관리자에게 보고하는 백그라운드 자동화 배치를 구축합니다.
- Redis 캐싱을 도입하여 수만 명의 동시 접속자에게도 10ms 이하로 인기 상품을 서빙합니다.
- 라라벨 리버브(Reverb) 웹소켓을 연동하여 신규 주문 발생 시 관리자 화면에 새로고침 없이 실시간 알림을 띄웁니다.

#### 2. 핵심 학습 개념
- **커스텀 아티산 커맨드(Artisan Console)**: `php artisan shop:daily-report` 명령 제작
- **대화형 CLI (Laravel Prompts)**: 텍스트 입력, 셀렉트 박스, 멀티 셀렉트, 스피너 지원
- **작업 스케줄링(Task Scheduling)**:
  - 크론(Cron) 단 하나로 모든 라라벨 스케줄 관리
  - 빈도 설정: `dailyAt('00:00')`, `hourly()`, `weekdays()`
  - 중복 실행 방지(`withoutOverlapping()`), 백그라운드 실행(`runInBackground()`)
- **캐시(Cache) 시스템**:
  - Redis 캐시 드라이버 및 `Cache::remember()` 고속 캐싱
  - 캐시 태그(Cache Tags)를 이용한 카테고리/상품 캐시 일괄 무효화
- **동시성(Concurrency)과 프로세스(Processes)**: 외부 CLI 명령어 비동기 실행
- **웹소켓과 브로드캐스팅(Broadcasting)**:
  - 라라벨 공식 초고속 웹소켓 서버 **Laravel Reverb**
  - `ShouldBroadcast` 인터페이스로 프론트엔드(Echo)에 실시간 주문 알림 전송
- **다국어 지원 (Localization)**: 한국어/영어/일본어 언어팩 및 통화 포맷 변환

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [아티산 콘솔 (Artisan Console)](./docs/05_digging_deeper/artisan_ko.md)
- [프롬프트 (Prompts)](./docs/11_packages/prompts_ko.md)
- [작업 스케줄링 (Scheduling)](./docs/05_digging_deeper/scheduling_ko.md)
- [캐시 (Cache)](./docs/05_digging_deeper/cache_ko.md)
- [Redis (레디스)](./docs/07_database/redis_ko.md)
- [브로드캐스팅 (Broadcasting)](./docs/05_digging_deeper/broadcasting_ko.md)
- [Reverb (웹소켓 서버)](./docs/11_packages/reverb_ko.md)
- [동시성 (Concurrency)](./docs/05_digging_deeper/concurrency_ko.md)
- [프로세스 (Processes)](./docs/05_digging_deeper/processes_ko.md)
- [다국어 지원 (Localization)](./docs/05_digging_deeper/localization_ko.md)

#### 4. 핸드온 실습 과제
1. 관리자가 터미널에서 대화형으로 재고를 추가하는 `shop:restock` 커맨드 제작 (Prompts 적용)
2. 베스트셀러 상품 목록을 Redis에 1시간 동안 캐싱하고, 상품 수정 시 캐시 태그로 자동 삭제
3. Reverb 웹소켓 서버를 띄우고, 신규 주문 발생 시 관리자 화면에 '새 주문 도착!' 실시간 토스트 알림 표시

---

### [13주차] RESTful API, Sanctum 토큰 인증, 검색 & AI 기능 탑재

> 📖 **주차별 상세 실습 가이드:** [week13 실습 바로가기](./week13/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니! 우리 지니샵을 모바일 앱에서도 쓸 수 있게 API를 열어주고 싶어. 그리고 상품이 너무 많아서 검색이 느린데 빠른 검색 엔진을 붙일 수 있을까? 참, 요즘 유행하는 AI로 상품 설명도 자동으로 쓰고 싶어!"  
> 🐱 **지니**: "도로시의 꿈이 정말 크구나! 라라벨은 **Sanctum**으로 모바일 토큰 인증을 1초 만에 끝내고, **API Resource**로 예쁜 JSON을 빚어준단다. 검색은 **Laravel Scout**으로 10ms 만에 찾아내고, 최신 **Laravel AI SDK**와 **MCP**를 연결하면 AI가 매력적인 상품 홍보글까지 척척 써준단다!"  
> 🐶 **토토**: "멍멍! Pennant 피처 플래그로 신규 결제 화면 A/B 테스트도 하고, Folio로 이벤트 랜딩 페이지도 번개처럼 만들자멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 모바일 앱 연동을 위한 규격화된 RESTful JSON API를 설계하고, Laravel Sanctum 토큰 인증을 적용합니다.
- Laravel Scout를 이용해 상품명/설명 전문 검색(Full-text Search) 엔진을 구축합니다.
- **최신 라라벨 AI 기능**: Laravel AI SDK와 MCP를 결합하여, 상품 키워드 입력 시 AI가 상세 설명을 자동 생성하는 스마트 커머스를 완성합니다.

#### 2. 핵심 학습 개념
- RESTful API 설계 원칙과 HTTP 상태 코드
- **API 리소스 (API Resources & Collections)**: 모델 to JSON 표준 변환, 관계 포함(`whenLoaded`), 숨김 속성
- **라라벨 생텀(Laravel Sanctum)**: SPA 쿠키 인증 및 모바일 API 토큰 발급, 토큰별 권한(Abilities)
- **라라벨 스카우트(Laravel Scout)**:
  - 모델에 `Searchable` 트레이트 적용
  - Meilisearch / 데이터베이스 풀텍스트 인덱스 연동 및 형태소 가중치 검색
- **라라벨 AI 생태계**:
  - **Laravel AI SDK**: LLM 프로바이더 연동, 스트리밍 응답, Tool Calling
  - **Model Context Protocol (MCP)**: AI 에이전트에게 쇼핑몰 DB/주문 조회 도구 제공
  - **Laravel Boost**: 프로젝트 전용 AI 벡터 문서 컨텍스트 연동
- 보너스 생태계: **Pennant** (A/B 테스트 피처 플래그), **Folio** (파일 기반 라우팅)

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [API 리소스 (Eloquent Resources)](./docs/08_eloquent_orm/eloquent-resources_ko.md)
- [직렬화 (Serialization)](./docs/08_eloquent_orm/eloquent-serialization_ko.md)
- [Sanctum (API 토큰 인증)](./docs/11_packages/sanctum_ko.md)
- [Scout (전문 검색)](./docs/11_packages/scout_ko.md)
- [검색 (Search)](./docs/05_digging_deeper/search_ko.md)
- [AI SDK (라라벨 인공지능 SDK)](./docs/09_ai/ai-sdk_ko.md)
- [MCP (모델 컨텍스트 프로토콜)](./docs/09_ai/mcp_ko.md)
- [Boost (라라벨 부스트)](./docs/09_ai/boost_ko.md)
- [Pennant (피처 플래그)](./docs/11_packages/pennant_ko.md)
- [Folio (페이지 기반 라우팅)](./docs/11_packages/folio_ko.md)

#### 4. 핸드온 실습 과제
1. `GET /api/v1/products` 및 `POST /api/v1/orders` 엔드포인트 구현 (Sanctum 인증 및 `ProductResource` 반환)
2. `Product` 모델에 Scout 검색을 붙여 상품명/설명 대상 10ms 실시간 검색창 구현
3. 관리자 상품 등록 페이지에 "AI 상세설명 생성" 버튼을 추가하여, 핵심 키워드 입력 시 Laravel AI SDK가 고품질 상품 홍보글을 자동 생성하도록 연동

---

### [14주차] 테스트 자동화, 브라우저 E2E, 모니터링 & 프로덕션 배포

> 📖 **주차별 상세 실습 가이드:** [week14 실습 바로가기](./week14/index.md)


#### 💬 지니 & 도로시 & 토토의 개발 회의
> 👧 **도로시**: "지니, 토토! 14주 동안 우리가 만든 **지니샵(JinyShop)**이 드디어 완성되었어! 그런데 고객들에게 정식 오픈하기 전에, 결제나 주문 과정에 숨겨진 버그가 없는지 어떻게 완벽하게 확신할 수 있을까?"  
> 🐱 **지니**: "도로시, 진정한 프로 개발자는 **자동화 테스트**로 말한단다! PHPUnit/Pest로 수백 개의 결제 시나리오를 1초 만에 검증하고, **Laravel Dusk**로 실제 브라우저가 장바구니부터 결제까지 자동으로 클릭하며 시험하도록 할 수 있지. 그리고 **Laravel Pulse**로 서버 건강을 지켜보며 **Envoy**로 무중단 배포를 쏘아 올리는 거란다!"  
> 🐶 **토토**: "멍멍! 모든 테스트 창에 영롱한 초록색 불(PASS)이 들어왔다멍! 지니샵 그랜드 오픈 성공이다멍!"

#### 1. 학습 목표 및 쇼핑몰 시나리오
- 지니샵의 모든 비즈니스 로직(장바구니, 쿠폰, 결제)을 보장하는 단위/기능 테스트 스위트를 완성합니다.
- 사용자가 실제 브라우저에서 구매를 완료하는 전 과정을 Laravel Dusk로 자동 검증(E2E)합니다.
- Laravel Pulse로 실시간 성능 모니터링을 구성하고, Envoy를 통해 무중단 프로덕션 배포를 수행합니다.

#### 2. 핵심 학습 개념
- 테스트 주도 개발(TDD)과 Pest / PHPUnit 환경 격리 (인메모리 SQLite DB)
- `RefreshDatabase` 트레이트를 통한 테스트 간 데이터 자동 리셋
- **HTTP 기능 테스트(Feature Tests)**: 엔드포인트 응답, 세션 및 인증 모의(`actingAs($user)`)
- **모킹(Mocking)**: 외부 결제 API, 메일 발송(`Mail::fake()`), 큐 작업(`Queue::fake()`) 가짜 객체 처리
- **라라벨 더스크(Laravel Dusk)**: 헤드리스 크롬을 이용한 실제 브라우저 클릭/입력/스크린샷 E2E 테스트
- **성능 최적화 & 모니터링**:
  - **Laravel Pulse**: 느린 쿼리, 느린 HTTP 엔드포인트 실시간 APM 추적
  - **Laravel Octane**: Swoole / RoadRunner를 이용한 메모리 상주형 고성능 초당 만건 서빙
- **패키지 개발 (Package Development)**: 쇼핑몰 공통 결제 모듈을 독립적인 라라벨 패키지로 분리
- **배포 및 운영**:
  - 배포 체크리스트: `config:cache`, `route:cache`, `view:cache`
  - 배포 자동화 도구: Laravel Envoy 무중단 배포 스크립트
  - 릴리스 노트와 상위 버전 업그레이드 가이드
  - 오픈소스 라라벨 프레임워크 기여하기

#### 3. 연계 공식 문서 (`php_laravel/src/`)
- [테스트 시작하기 (Testing)](./10_testing/testing_ko.md)
- [HTTP 테스트 (HTTP Tests)](./10_testing/http-tests_ko.md)
- [콘솔 테스트 (Console Tests)](./10_testing/console-tests_ko.md)
- [데이터베이스 테스트 (Database Testing)](./10_testing/database-testing_ko.md)
- [모킹 (Mocking)](./10_testing/mocking_ko.md)
- [Dusk (브라우저 테스트)](./10_testing/dusk_ko.md)
- [Pulse (애플리케이션 상태 모니터링)](./docs/11_packages/pulse_ko.md)
- [Octane (고성능 앱 서빙)](./docs/11_packages/octane_ko.md)
- [Envoy (배포 자동화)](./docs/11_packages/envoy_ko.md)
- [패키지 개발 (Package Development)](./docs/05_digging_deeper/packages_ko.md)
- [배포 가이드 (Deployment)](./docs/02_getting_started/deployment_ko.md)
- [릴리스 노트 & 업그레이드 가이드 (Releases & Upgrade)](./docs/01_prologue/releases_ko.md)
- [기여 가이드 (Contributions)](./docs/01_prologue/contributions_ko.md)

#### 4. 핸드온 실습 과제
1. 쇼핑몰 핵심 비즈니스 로직(장바구니 담기 $
ightarrow$ 할인 쿠폰 적용 $
ightarrow$ 결제) Feature Test 작성
2. 결제 외부 통신을 `Http::fake()`로 모킹하여 결제 실패 시나리오 테스트
3. Dusk를 실행하여 실제 브라우저에서 회원가입부터 상품 구매까지 자동으로 테스트가 패스되는 녹색 창 확인
4. 프로덕션 최적화 커맨드 캐싱 실행 및 Envoy 무중단 배포 스크립트 작성으로 지니샵 런칭 완료!

---

## 🛠️ JinyShop 실습 프로젝트 아키텍처 및 폴더 구조

14주 과정을 완주하면 여러분의 쇼핑몰 프로젝트는 다음과 같은 견고한 엔터프라이즈 구조를 갖추게 됩니다:

```text
jinyshop/
├── app/
│   ├── Enums/                  # 주문 상태, 결제 수단 Enum
│   ├── Events/                 # OrderPlaced, ProductSoldOut 등
│   ├── Http/
│   │   ├── Controllers/        # 웹 및 API 컨트롤러
│   │   │   ├── Admin/          # 백오피스 관리자 컨트롤러
│   │   │   └── Api/V1/         # 모바일 연동 RESTful 컨트롤러
│   │   ├── Middleware/         # EnsureUserIsAdmin, CheckCartNotEmpty 등
│   │   ├── Requests/           # StoreOrderRequest, ProductFilterRequest 등
│   │   └── Resources/          # ProductResource, OrderResource 등
│   ├── Jobs/                   # SendOrderInvoiceMail, ProcessPaymentJob 등
│   ├── Listeners/              # SendOrderNotification, DeductStockListener 등
│   ├── Models/                 # User, Product, Category, Order, CartItem 등
│   ├── Notifications/          # OrderCompletedNotification, LowStockNotification 등
│   ├── Policies/               # OrderPolicy, ProductPolicy 등
│   └── Services/               # CartService, TossPaymentService 등 (DI 추상화)
├── database/
│   ├── factories/              # 현실적인 한국어 더미 데이터 팩토리
│   ├── migrations/             # 체계적인 스키마 마이그레이션 파일들
│   └── seeders/                # 카테고리, 초기 관리자, 대량 상품 시더
├── resources/
│   ├── views/                  # 컴포넌트 기반 Blade 화면
│   │   ├── components/         # <x-layouts.app>, <x-product-card> 등
│   │   ├── shop/               # 상품 카탈로그, 상세, 장바구니, 주문서
│   │   └── admin/              # 관리자 대시보드 화면
│   └── js/ & css/              # Vite 번들링 Tailwind CSS & Alpine.js
├── routes/
│   ├── web.php                 # 쇼핑몰 웹 라우트
│   ├── api.php                 # 모바일 토큰 API 라우트
│   └── console.php             # 스케줄러 및 아티산 커맨드 정의
└── tests/
    ├── Feature/                # 주문, 결제, 장바구니 통합 기능 테스트
    ├── Unit/                   # 가격 계산기, 쿠폰 로직 단위 테스트
    └── Browser/                # Dusk 브라우저 E2E 자동화 테스트
```

---

## 📊 라라벨 공식 문서 전수 매핑 및 검증표 (Full Traceability Matrix - 103개 전수 매핑)

> **검증 방법 안내:**
> 본 커리큘럼이 라라벨 공식 문서를 100% 완전하게 포함하고 있음을 증명하기 위해, 공식 저장소의 11개 그룹 총 103개 세부 주제 문서를 1:1로 전수 추적 매핑한 표입니다.
> 터미널에서 `python3 verify_coverage.py` 명령을 실행하시면 실시간으로 **커버리지 100.0% (103/103 매핑 완료)** 검증 결과를 직접 확인하실 수 있습니다.

| 순번 | 공식 그룹 | 문서명 (한글 / 영문) | 실습 주차 | JinyShop 쇼핑몰에서의 구체적 역할 및 구현 시나리오 | 상태 |
| :---: | :--- | :--- | :---: | :--- | :---: |
| 001 | `01_prologue` | [릴리스 노트 (Release Notes)](./src/01_prologue/releases_ko.md) | **14주차** | 라라벨 버전 관리 정책 및 JinyShop의 향후 릴리스 지원 주기 확인 | `100%` |
| 002 | `01_prologue` | [업그레이드 가이드 (Upgrade Guide)](./src/01_prologue/upgrade_ko.md) | **14주차** | 기존 JinyShop 시스템의 상위 라라벨 버전 무중단 마이그레이션 전략 | `100%` |
| 003 | `01_prologue` | [기여 가이드 (Contributions)](./src/01_prologue/contributions_ko.md) | **14주차** | 라라벨 오픈소스 프레임워크 생태계 기여 절차 및 규칙 체득 | `100%` |
| 004 | `02_getting_started` | [설치 (Installation)](./src/02_getting_started/installation_ko.md) | **1주차** | Composer / Herd 기반 최신 라라벨 JinyShop 프로젝트 생성 | `100%` |
| 005 | `02_getting_started` | [설정 (Configuration)](./src/02_getting_started/configuration_ko.md) | **1주차** | .env 환경 변수 격리, config/ 캐싱 메커니즘 구축 | `100%` |
| 006 | `02_getting_started` | [에이전트 개발 (Agentic Development)](./src/02_getting_started/ai_ko.md) | **1주차** | Agentic AI 코딩 도우미 및 Laravel Boost 연동 개발 환경 | `100%` |
| 007 | `02_getting_started` | [디렉터리 구조 (Directory Structure)](./src/02_getting_started/structure_ko.md) | **1주차** | 라라벨 13의 현대적 디렉터리 구성 및 모듈별 역할 정립 | `100%` |
| 008 | `02_getting_started` | [프론트엔드 (Frontend)](./src/02_getting_started/frontend_ko.md) | **3주차** | Tailwind CSS 및 모던 프론트엔드 도구 체계 연동 | `100%` |
| 009 | `02_getting_started` | [스타터 키트 (Starter Kits)](./src/02_getting_started/starter-kits_ko.md) | **8주차** | Breeze / Jetstream 인증 스타터 키트 구조 분석 및 커스터마이징 | `100%` |
| 010 | `02_getting_started` | [배포 (Deployment)](./src/02_getting_started/deployment_ko.md) | **14주차** | 운영 서버 배포 체크리스트 (config/route/view 캐시 및 환경 튜닝) | `100%` |
| 011 | `03_architecture_concepts` | [요청 라이프사이클 (Request Lifecycle)](./src/03_architecture_concepts/lifecycle_ko.md) | **2주차** | HTTP 요청부터 서비스 프로바이더, 미들웨어 거쳐 응답까지의 흐름 | `100%` |
| 012 | `03_architecture_concepts` | [서비스 컨테이너 (Service Container)](./src/03_architecture_concepts/container_ko.md) | **10주차** | IoC 컨테이너 원리, 자동 의존성 주입(Auto-wiring) 및 싱글톤 바인딩 | `100%` |
| 013 | `03_architecture_concepts` | [서비스 프로바이더 (Service Providers)](./src/03_architecture_concepts/providers_ko.md) | **10주차** | register() vs boot() 라이프사이클 및 커스텀 결제 프로바이더 작성 | `100%` |
| 014 | `03_architecture_concepts` | [파사드 (Facades)](./src/03_architecture_concepts/facades_ko.md) | **10주차** | 파사드 뒤의 동적 인스턴스 해결 원리 및 실시간 파사드 활용 | `100%` |
| 015 | `04_the_basics` | [라우팅 (Routing)](./src/04_the_basics/routing_ko.md) | **2주차** | JinyShop 쇼핑몰 URL 매핑, 파라미터 제약조건, 라우트 그룹 및 폴백 | `100%` |
| 016 | `04_the_basics` | [미들웨어 (Middleware)](./src/04_the_basics/middleware_ko.md) | **9주차** | 관리자 전용 접근 제어 미들웨어 및 IP 기반 요청 필터링 | `100%` |
| 017 | `04_the_basics` | [CSRF 보호 (CSRF Protection)](./src/04_the_basics/csrf_ko.md) | **3주차** | 주문서 작성 및 장바구니 폼 전송 시 @csrf 토큰 검증 | `100%` |
| 018 | `04_the_basics` | [컨트롤러 (Controllers)](./src/04_the_basics/controllers_ko.md) | **2주차** | ProductController 리소스 컨트롤러 및 단일 책임 Invokable 컨트롤러 | `100%` |
| 019 | `04_the_basics` | [요청 (Requests)](./src/04_the_basics/requests_ko.md) | **2주차** | 고객 입력값, 필터 조건, 요청 헤더 및 첨부파일 안전 추출 | `100%` |
| 020 | `04_the_basics` | [응답 (Responses)](./src/04_the_basics/responses_ko.md) | **2주차** | View 렌더링, JSON 응답, 파일 다운로드(영수증 PDF), 리다이렉트 | `100%` |
| 021 | `04_the_basics` | [뷰 (Views)](./src/04_the_basics/views_ko.md) | **3주차** | 블레이드 뷰 렌더링 및 뷰 컴포저를 통한 전역 카테고리 주입 | `100%` |
| 022 | `04_the_basics` | [블레이드 템플릿 (Blade)](./src/04_the_basics/blade_ko.md) | **3주차** | 슬롯 기반 레이아웃 컴포넌트(<x-layouts.app>, <x-product-card>) | `100%` |
| 023 | `04_the_basics` | [에셋 번들링 (Vite)](./src/04_the_basics/vite_ko.md) | **3주차** | Vite를 이용한 Tailwind CSS 및 Alpine.js 핫 리로딩 번들링 | `100%` |
| 024 | `04_the_basics` | [URL 생성 (URLs)](./src/04_the_basics/urls_ko.md) | **2주차** | 명명된 라우트 URL 및 임시 주문 조회를 위한 서명된 URL(Signed URLs) | `100%` |
| 025 | `04_the_basics` | [세션 (Session)](./src/04_the_basics/session_ko.md) | **7주차** | 비회원 장바구니 세션 구현 및 1회성 플래시 메시지 | `100%` |
| 026 | `04_the_basics` | [유효성 검사 (Validation)](./src/04_the_basics/validation_ko.md) | **7주차** | 주문/결제 폼 유효성 검사 및 StoreOrderRequest Form Request 분리 | `100%` |
| 027 | `04_the_basics` | [에러 핸들링 (Errors)](./src/04_the_basics/errors_ko.md) | **9주차** | 커스텀 결제 예외 렌더링 및 404/500 에러 페이지 커스터마이징 | `100%` |
| 028 | `04_the_basics` | [로깅 (Logging)](./src/04_the_basics/logging_ko.md) | **9주차** | Monolog 채널 설정, 일별 로테이션, Slack 이상 결제 긴급 알림 | `100%` |
| 029 | `05_digging_deeper` | [아티산 콘솔 (Artisan)](./src/05_digging_deeper/artisan_ko.md) | **12주차** | 관리자용 일별 정산 및 재고 보충 커스텀 CLI 명령어 제작 | `100%` |
| 030 | `05_digging_deeper` | [브로드캐스팅 (Broadcasting)](./src/05_digging_deeper/broadcasting_ko.md) | **12주차** | 주문 접수 및 재고 품절 시 관리자 화면 실시간 브로드캐스팅 | `100%` |
| 031 | `05_digging_deeper` | [캐시 (Cache)](./src/05_digging_deeper/cache_ko.md) | **12주차** | Redis 캐싱, 캐시 태그(Cache Tags)를 이용한 카테고리 캐시 무효화 | `100%` |
| 032 | `05_digging_deeper` | [컬렉션 (Collections)](./src/05_digging_deeper/collections_ko.md) | **6주차** | 컬렉션 함수형 체이닝 및 OOM 방지를 위한 LazyCollection 지연 처리 | `100%` |
| 033 | `05_digging_deeper` | [동시성 (Concurrency)](./src/05_digging_deeper/concurrency_ko.md) | **12주차** | 다중 외부 택배사 배송 상태 조회 병렬(Parallel) 동시 처리 | `100%` |
| 034 | `05_digging_deeper` | [컨텍스트 (Context)](./src/05_digging_deeper/context_ko.md) | **10주차** | 요청별 고유 Trace-ID 및 고객 쇼핑 메타데이터 컨텍스트 추적 | `100%` |
| 035 | `05_digging_deeper` | [컨트랙트 (Contracts)](./src/05_digging_deeper/contracts_ko.md) | **10주차** | PaymentGatewayContract 인터페이스 추상화 및 다중 PG사 교체 설계 | `100%` |
| 036 | `05_digging_deeper` | [이벤트 (Events)](./src/05_digging_deeper/events_ko.md) | **11주차** | OrderPlaced 이벤트 발행을 통한 주문 완료 후속 도메인 로직 분리 | `100%` |
| 037 | `05_digging_deeper` | [파일 스토리지 (Filesystem)](./src/05_digging_deeper/filesystem_ko.md) | **9주차** | Flysystem 기반 상품 이미지 업로드 및 S3/Public 스토리지 서빙 | `100%` |
| 038 | `05_digging_deeper` | [헬퍼 (Helpers)](./src/05_digging_deeper/helpers_ko.md) | **10주차** | 라라벨 내장 헬퍼 함수 활용 및 전역 통화 포맷 커스텀 헬퍼 작성 | `100%` |
| 039 | `05_digging_deeper` | [HTTP 클라이언트 (HTTP Client)](./src/05_digging_deeper/http-client_ko.md) | **10주차** | 외부 토스/스트라이프 PG 결제 API 통신 및 재시도/타임아웃 핸들링 | `100%` |
| 040 | `05_digging_deeper` | [이미지 (Images)](./src/05_digging_deeper/images_ko.md) | **9주차** | 상품 대표/상세 이미지 리사이징, 썸네일 생성 및 WebP 최적화 | `100%` |
| 041 | `05_digging_deeper` | [다국어 지원 (Localization)](./src/05_digging_deeper/localization_ko.md) | **12주차** | 한국어/영어/일본어 다국어 언어팩 및 지역별 통화(KRW/USD) 표기 | `100%` |
| 042 | `05_digging_deeper` | [메일 (Mail)](./src/05_digging_deeper/mail_ko.md) | **11주차** | Mailable 마크다운 주문 확인서 메일 템플릿 제작 및 큐 발송 | `100%` |
| 043 | `05_digging_deeper` | [알림 (Notifications)](./src/05_digging_deeper/notifications_ko.md) | **11주차** | 다채널 알림(이메일, 웹 인앱 알림, 슬랙 웹훅) 동시 발송 | `100%` |
| 044 | `05_digging_deeper` | [패키지 개발 (Packages)](./src/05_digging_deeper/packages_ko.md) | **14주차** | JinyShop 공통 결제/쿠폰 모듈을 독립적인 라라벨 패키지로 분리 | `100%` |
| 045 | `05_digging_deeper` | [프로세스 실행 (Processes)](./src/05_digging_deeper/processes_ko.md) | **12주차** | 서버 썸네일 변환 CLI 및 외부 유틸리티 비동기 프로세스 제어 | `100%` |
| 046 | `05_digging_deeper` | [큐 (Queues)](./src/05_digging_deeper/queues_ko.md) | **11주차** | Redis 기반 비동기 큐 작업, 워커 실행, 재시도 및 실패한 잡(Failed Jobs) 처리 | `100%` |
| 047 | `05_digging_deeper` | [속도 제한 (Rate Limiting)](./src/05_digging_deeper/rate-limiting_ko.md) | **9주차** | 결제 시도 및 장바구니 담기 요청에 대한 Rate Limiting Throttling 적용 | `100%` |
| 048 | `05_digging_deeper` | [검색 (Search)](./src/05_digging_deeper/search_ko.md) | **13주차** | 전문 검색(Full-text Search) 엔진 아키텍처 및 인덱싱 전략 | `100%` |
| 049 | `05_digging_deeper` | [문자열 (Strings)](./src/05_digging_deeper/strings_ko.md) | **5주차** | 상품명 기반 SEO 친화적 슬러그(Slug) 자동 생성 및 Str 유틸리티 | `100%` |
| 050 | `05_digging_deeper` | [작업 스케줄링 (Scheduling)](./src/05_digging_deeper/scheduling_ko.md) | **12주차** | 매일 밤 미결제 주문 자동 취소 및 품절 상품 통계 크론 배치 | `100%` |
| 051 | `06_security` | [인증 (Authentication)](./src/06_security/authentication_ko.md) | **8주차** | 가드와 유저 프로바이더 기반 세션 인증 시스템 구축 | `100%` |
| 052 | `06_security` | [인가 (Authorization)](./src/06_security/authorization_ko.md) | **8주차** | 게이트(Gates) 및 정책(OrderPolicy)을 이용한 주문 취소/조회 권한 통제 | `100%` |
| 053 | `06_security` | [이메일 인증 (Verification)](./src/06_security/verification_ko.md) | **8주차** | 신규 가입 고객 이메일 소유권 검증(MustVerifyEmail) 플로우 | `100%` |
| 054 | `06_security` | [암호화 (Encryption)](./src/06_security/encryption_ko.md) | **8주차** | 민감한 고객 배송지 정보 및 API 키 양방향 암호화 보관 | `100%` |
| 055 | `06_security` | [해싱 (Hashing)](./src/06_security/hashing_ko.md) | **8주차** | Bcrypt / Argon2 기반 고객 비밀번호 단방향 안전 해싱 | `100%` |
| 056 | `06_security` | [비밀번호 재설정 (Passwords)](./src/06_security/passwords_ko.md) | **8주차** | 비밀번호 재설정 토큰 발급 및 안전한 비밀번호 변경 이메일 링크 | `100%` |
| 057 | `07_database` | [데이터베이스 시작하기 (Database)](./src/07_database/database_ko.md) | **4주차** | DB 연결 풀 설정, 원시 쿼리 및 DB::transaction() 원자성 보장 | `100%` |
| 058 | `07_database` | [쿼리 빌더 (Queries)](./src/07_database/queries_ko.md) | **5주차** | 상품 필터링, 조인, 집계 함수(평균 평점, 총 판매량) 고속 쿼리 | `100%` |
| 059 | `07_database` | [페이지네이션 (Pagination)](./src/07_database/pagination_ko.md) | **5주차** | 번호 기반 LengthAwarePaginator 및 모바일 무한 스크롤 CursorPagination | `100%` |
| 060 | `07_database` | [마이그레이션 (Migrations)](./src/07_database/migrations_ko.md) | **4주차** | 테이블 스키마 버전 관리, 외래키 제약조건 및 복합 인덱스 설계 | `100%` |
| 061 | `07_database` | [시딩 (Seeding)](./src/07_database/seeding_ko.md) | **4주차** | JinyShop 초기 카테고리 계층 구조 및 테스트용 대량 데이터 자동 적재 | `100%` |
| 062 | `07_database` | [레디스 (Redis)](./src/07_database/redis_ko.md) | **12주차** | 고성능 캐시, 세션, 비동기 큐 백엔드로서의 Redis 클러스터 연동 | `100%` |
| 063 | `07_database` | [MongoDB (몽고DB)](./src/07_database/mongodb_ko.md) | **7주차** | NoSQL 하이브리드 연동: 상품 비정형 클릭스트림 및 감사 로그 수집 | `100%` |
| 064 | `08_eloquent_orm` | [Eloquent 시작하기 (Eloquent)](./src/08_eloquent_orm/eloquent_ko.md) | **5주차** | Active Record 모델링, 대량 할당 보호, 소프트 삭제(Soft Deletes) | `100%` |
| 065 | `08_eloquent_orm` | [관계 정의 (Relationships)](./src/08_eloquent_orm/eloquent-relationships_ko.md) | **6주차** | 1:1, 1:N, N:M 피벗, 다형성(Morph) 관계 및 Eager Loading N+1 해결 | `100%` |
| 066 | `08_eloquent_orm` | [Eloquent 컬렉션 (Collections)](./src/08_eloquent_orm/eloquent-collections_ko.md) | **6주차** | Eloquent 모델 컬렉션 전용 커스텀 메서드 및 데이터 가공 | `100%` |
| 067 | `08_eloquent_orm` | [뮤테이터 / 캐스트 (Mutators & Casts)](./src/08_eloquent_orm/eloquent-mutators_ko.md) | **5주차** | 가격 원화 표기 접근자 및 상품 옵션 JSON 속성 자동 캐스팅 | `100%` |
| 068 | `08_eloquent_orm` | [API 리소스 (API Resources)](./src/08_eloquent_orm/eloquent-resources_ko.md) | **13주차** | 모바일 앱 연동을 위한 규격화된 JsonResource 응답 변환 | `100%` |
| 069 | `08_eloquent_orm` | [직렬화 (Serialization)](./src/08_eloquent_orm/eloquent-serialization_ko.md) | **13주차** | 모델 to JSON 변환 시 민감 속성 숨김($hidden) 및 가상 속성 추가($appends) | `100%` |
| 070 | `08_eloquent_orm` | [팩토리 (Factories)](./src/08_eloquent_orm/eloquent-factories_ko.md) | **4주차** | Faker 한국어 로케일을 활용한 실감 나는 상품/회원 팩토리 정의 | `100%` |
| 071 | `09_ai` | [AI SDK (라라벨 인공지능 SDK)](./src/09_ai/ai-sdk_ko.md) | **13주차** | 라라벨 공식 AI SDK 연동: 상품명 입력 시 상세 마케팅 홍보글 자동 생성 | `100%` |
| 072 | `09_ai` | [MCP (모델 컨텍스트 프로토콜)](./src/09_ai/mcp_ko.md) | **13주차** | Model Context Protocol을 이용해 AI에게 JinyShop 재고/주문 조회 도구 제공 | `100%` |
| 073 | `09_ai` | [라라벨 Boost (부스트)](./src/09_ai/boost_ko.md) | **13주차** | AI 코딩 에이전트와 라라벨 프로젝트 간 최신 버전 컨텍스트 동기화 | `100%` |
| 074 | `10_testing` | [테스트 시작하기 (Testing)](./src/10_testing/testing_ko.md) | **14주차** | Pest / PHPUnit 테스트 프레임워크 환경 및 인메모리 SQLite DB 구성 | `100%` |
| 075 | `10_testing` | [HTTP 테스트 (HTTP Tests)](./src/10_testing/http-tests_ko.md) | **14주차** | 장바구니 담기, 주문 생성, 결제 엔드포인트 기능 테스트(Feature Tests) | `100%` |
| 076 | `10_testing` | [콘솔 테스트 (Console Tests)](./src/10_testing/console-tests_ko.md) | **14주차** | 일별 정산 아티산 커맨드의 입출력 및 상태 코드 자동 검증 | `100%` |
| 077 | `10_testing` | [브라우저 테스트 (Dusk)](./src/10_testing/dusk_ko.md) | **14주차** | 헤드리스 크롬 기반 실제 브라우저 상품 구매 E2E 시나리오 테스트 | `100%` |
| 078 | `10_testing` | [데이터베이스 테스트 (Database Testing)](./src/10_testing/database-testing_ko.md) | **14주차** | RefreshDatabase 트레이트를 활용한 테스트 데이터 격리 및 팩토리 검증 | `100%` |
| 079 | `10_testing` | [모킹 (Mocking)](./src/10_testing/mocking_ko.md) | **14주차** | 외부 PG사 결제 API, 메일 발송, 비동기 큐 작업 가짜(Mock) 처리 | `100%` |
| 080 | `11_packages` | [캐셔 (Stripe)](./src/11_packages/billing_ko.md) | **11주차** | 라라벨 캐셔(Cashier)를 이용한 정기 배송 구독 및 신용카드 단건 결제 | `100%` |
| 081 | `11_packages` | [캐셔 (Paddle)](./src/11_packages/cashier-paddle_ko.md) | **11주차** | 해외 고객을 위한 글로벌 결제 및 세금 계산 자동화 연동 | `100%` |
| 082 | `11_packages` | [Dusk 패키지](./src/11_packages/dusk_ko.md) | **14주차** | Laravel Dusk 패키지 설치, 드라이버 설정 및 화면 캡처 디버깅 | `100%` |
| 083 | `11_packages` | [엔보이 (Envoy)](./src/11_packages/envoy_ko.md) | **14주차** | 블레이드 문법 스타일의 원격 서버 SSH 무중단 배포 스크립트 작성 | `100%` |
| 084 | `11_packages` | [포티파이 (Fortify)](./src/11_packages/fortify_ko.md) | **8주차** | 프론트엔드에 구애받지 않는 헤드리스 2단계 인증(2FA) 백엔드 구성 | `100%` |
| 085 | `11_packages` | [폴리오 (Folio)](./src/11_packages/folio_ko.md) | **13주차** | 이벤트 기획전 및 프로모션 랜딩 페이지를 위한 파일 기반 고속 라우팅 | `100%` |
| 086 | `11_packages` | [헤드 (Head)](./src/11_packages/head_ko.md) | **3주차** | 상품 상세 페이지 소셜 공유(OpenGraph) 및 동적 <head> 태그 제어 | `100%` |
| 087 | `11_packages` | [홈스테드 (Homestead)](./src/11_packages/homestead_ko.md) | **1주차** | Vagrant/가상머신 기반의 전통적 개발 환경과 모던 Sail 비교 | `100%` |
| 088 | `11_packages` | [호라이즌 (Horizon)](./src/11_packages/horizon_ko.md) | **11주차** | 대용량 Redis 큐 작업의 실시간 처리량, 대기시간, 실패 작업 대시보드 | `100%` |
| 089 | `11_packages` | [믹스 (Mix)](./src/11_packages/mix_ko.md) | **3주차** | 레거시 웹팩(Webpack) 기반 빌드 도구와 차세대 Vite의 아키텍처 비교 | `100%` |
| 090 | `11_packages` | [옥탄 (Octane)](./src/11_packages/octane_ko.md) | **14주차** | Swoole/RoadRunner 엔진을 이용한 메모리 상주형 고성능 초당 만건 서빙 | `100%` |
| 091 | `11_packages` | [패스포트 (Passport)](./src/11_packages/passport_ko.md) | **8주차** | B2B 제휴사 전용 OAuth2 인증 서버 구축 (Sanctum과의 차이 분석) | `100%` |
| 092 | `11_packages` | [페넌트 (Pennant)](./src/11_packages/pennant_ko.md) | **13주차** | 신규 결제 UI A/B 테스트 및 카나리 배포를 위한 피처 플래그 관리 | `100%` |
| 093 | `11_packages` | [핀트 (Pint)](./src/11_packages/pint_ko.md) | **1주차** | PHP CS Fixer 기반 자동 코드 스타일 교정 및 CI 코드 컨벤션 유지 | `100%` |
| 094 | `11_packages` | [프리코그니션 (Precognition)](./src/11_packages/precognition_ko.md) | **7주차** | 주문서 작성 시 프론트엔드와 실시간 반응하는 실시간 폼 유효성 검사 | `100%` |
| 095 | `11_packages` | [프롬프트 (Prompts)](./src/11_packages/prompts_ko.md) | **12주차** | 아티산 CLI에서 셀렉트, 스피너, 유효성 검사를 지원하는 고급 대화형 입력 | `100%` |
| 096 | `11_packages` | [펄스 (Pulse)](./src/11_packages/pulse_ko.md) | **14주차** | 느린 쿼리, 느린 HTTP 엔드포인트, 큐 작업 지연을 추적하는 실시간 APM | `100%` |
| 097 | `11_packages` | [리버브 (Reverb)](./src/11_packages/reverb_ko.md) | **12주차** | 라라벨 공식 고성능 웹소켓 서버를 통한 신규 주문 및 품절 실시간 알림 | `100%` |
| 098 | `11_packages` | [세일 (Sail)](./src/11_packages/sail_ko.md) | **1주차** | Docker 기반 MySQL, Redis, Mailpit 올인원 로컬 개발 컨테이너 환경 | `100%` |
| 099 | `11_packages` | [생텀 (Sanctum)](./src/11_packages/sanctum_ko.md) | **13주차** | 모바일 쇼핑몰 앱 연동을 위한 경량 API 토큰 발급 및 SPA 세션 인증 | `100%` |
| 100 | `11_packages` | [스카우트 (Scout)](./src/11_packages/scout_ko.md) | **13주차** | 상품명/설명 전문 검색(Full-text Search) 엔진 연동 및 10ms 고속 검색 | `100%` |
| 101 | `11_packages` | [소셜라이트 (Socialite)](./src/11_packages/socialite_ko.md) | **8주차** | 구글, 카카오 등 간편 소셜 로그인 및 회원 자동 동기화 | `100%` |
| 102 | `11_packages` | [텔레스코프 (Telescope)](./src/11_packages/telescope_ko.md) | **1주차** | 로컬 요청, 쿼리, 메일, 덤프를 실시간 디버깅하는 필수 어시스턴트 | `100%` |
| 103 | `11_packages` | [발렛 (Valet)](./src/11_packages/valet_ko.md) | **1주차** | macOS 환경에서 Nginx 기반으로 *.test 도메인을 자동 서빙하는 초경량 환경 | `100%` |

### 🔍 공식 문서 100% 전수 포함 여부 검증 3대 방법

1. **위의 '전수 추적 매핑표(Full Traceability Matrix)' 확인**: 103개 공식 주제가 단 하나도 빠짐없이 1주차~14주차 중 어디에서 어떤 역할로 구현되는지 명시되어 있습니다.
2. **자동화 검증 스크립트 실행 (`verify_coverage.py`)**:
   - 프로젝트 루트에서 다음 명령어를 실행합니다:
     ```bash
     python3 verify_coverage.py
     ```
   - 스크립트가 `src/` 디렉터리의 실제 마크다운 파일(103개)과 `syllabus.md`를 크로스체크하여 `100.0% Coverage`를 수학적으로 검증합니다.
3. **주차별 상세 계획서의 '연계 공식 문서' 링크 클릭**: 각 주차마다 배정된 공식 문서 한글 번역본(`*_ko.md`) 링크가 모두 정상 연결되어 원본 내용과 바로 대조할 수 있습니다.
{% endraw %}
