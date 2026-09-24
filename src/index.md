# Laravel 공식 문서 (Official Documentation - 13.x)

> 원본 저장소: [laravel/docs (GitHub)](https://github.com/laravel/docs)  
> 공식 웹사이트: [laravel.com/framework/docs](https://laravel.com/framework/docs)  
> 브랜치: `13.x` (최신 안정/개발 버전)  
> 파일 명명 규칙: 원본 영문 문서는 `파일명_en.md` 형식으로 저장되어 있습니다.

## 문서 그룹 목록 (Documentation Groups)

### Prologue (서문) - `src/01_prologue/`

- [Release Notes (릴리스 노트)](./01_prologue/releases_en.md)
- [Upgrade Guide (업그레이드 가이드)](./01_prologue/upgrade_en.md)
- [Contribution Guide (기여 가이드)](./01_prologue/contributions_en.md)

### Getting Started (시작하기) - `src/02_getting_started/`

- [Installation (설치)](./02_getting_started/installation_en.md)
- [Configuration (설정)](./02_getting_started/configuration_en.md)
- [Agentic Development (에이전트 개발)](./02_getting_started/ai_en.md)
- [Directory Structure (디렉터리 구조)](./02_getting_started/structure_en.md)
- [Frontend (프론트엔드)](./02_getting_started/frontend_en.md)
- [Starter Kits (스타터 키트)](./02_getting_started/starter-kits_en.md)
- [Deployment (배포)](./02_getting_started/deployment_en.md)

### Architecture Concepts (아키텍처 개념) - `src/03_architecture_concepts/`

- [Request Lifecycle (요청 라이프사이클)](./03_architecture_concepts/lifecycle_en.md)
- [Service Container (서비스 컨테이너)](./03_architecture_concepts/container_en.md)
- [Service Providers (서비스 프로바이더)](./03_architecture_concepts/providers_en.md)
- [Facades (파사드)](./03_architecture_concepts/facades_en.md)

### The Basics (기본 개념) - `src/04_the_basics/`

- [Routing (라우팅)](./04_the_basics/routing_en.md)
- [Middleware (미들웨어)](./04_the_basics/middleware_en.md)
- [CSRF Protection (CSRF 보호)](./04_the_basics/csrf_en.md)
- [Controllers (컨트롤러)](./04_the_basics/controllers_en.md)
- [Requests (요청)](./04_the_basics/requests_en.md)
- [Responses (응답)](./04_the_basics/responses_en.md)
- [Views (뷰)](./04_the_basics/views_en.md)
- [Blade Templates (블레이드 템플릿)](./04_the_basics/blade_en.md)
- [Asset Bundling (에셋 번들링 (Vite))](./04_the_basics/vite_en.md)
- [URL Generation (URL 생성)](./04_the_basics/urls_en.md)
- [Session (세션)](./04_the_basics/session_en.md)
- [Validation (유효성 검사)](./04_the_basics/validation_en.md)
- [Error Handling (에러 핸들링)](./04_the_basics/errors_en.md)
- [Logging (로깅)](./04_the_basics/logging_en.md)

### Digging Deeper (심화 주제) - `src/05_digging_deeper/`

- [Artisan Console (아티산 콘솔)](./05_digging_deeper/artisan_en.md)
- [Broadcasting (브로드캐스팅)](./05_digging_deeper/broadcasting_en.md)
- [Cache (캐시)](./05_digging_deeper/cache_en.md)
- [Collections (컬렉션)](./05_digging_deeper/collections_en.md)
- [Concurrency (동시성)](./05_digging_deeper/concurrency_en.md)
- [Context (컨텍스트)](./05_digging_deeper/context_en.md)
- [Contracts (컨트랙트)](./05_digging_deeper/contracts_en.md)
- [Events (이벤트)](./05_digging_deeper/events_en.md)
- [File Storage (파일 스토리지)](./05_digging_deeper/filesystem_en.md)
- [Helpers (헬퍼)](./05_digging_deeper/helpers_en.md)
- [HTTP Client (HTTP 클라이언트)](./05_digging_deeper/http-client_en.md)
- [Images (이미지)](./05_digging_deeper/images_en.md)
- [Localization (다국어 지원)](./05_digging_deeper/localization_en.md)
- [Mail (메일)](./05_digging_deeper/mail_en.md)
- [Notifications (알림)](./05_digging_deeper/notifications_en.md)
- [Package Development (패키지 개발)](./05_digging_deeper/packages_en.md)
- [Processes (프로세스 실행)](./05_digging_deeper/processes_en.md)
- [Queues (큐)](./05_digging_deeper/queues_en.md)
- [Rate Limiting (속도 제한)](./05_digging_deeper/rate-limiting_en.md)
- [Search (검색)](./05_digging_deeper/search_en.md)
- [Strings (문자열)](./05_digging_deeper/strings_en.md)
- [Task Scheduling (작업 스케줄링)](./05_digging_deeper/scheduling_en.md)

### Security (보안) - `src/06_security/`

- [Authentication (인증)](./06_security/authentication_en.md)
- [Authorization (인가)](./06_security/authorization_en.md)
- [Email Verification (이메일 인증)](./06_security/verification_en.md)
- [Encryption (암호화)](./06_security/encryption_en.md)
- [Hashing (해싱)](./06_security/hashing_en.md)
- [Password Reset (비밀번호 재설정)](./06_security/passwords_en.md)

### Database (데이터베이스) - `src/07_database/`

- [Getting Started (데이터베이스 시작하기)](./07_database/database_en.md)
- [Query Builder (쿼리 빌더)](./07_database/queries_en.md)
- [Pagination (페이지네이션)](./07_database/pagination_en.md)
- [Migrations (마이그레이션)](./07_database/migrations_en.md)
- [Seeding (시딩)](./07_database/seeding_en.md)
- [Redis (레디스)](./07_database/redis_en.md)
- [MongoDB (몽고DB)](./07_database/mongodb_en.md)

### Eloquent ORM (Eloquent ORM) - `src/08_eloquent_orm/`

- [Getting Started (Eloquent 시작하기)](./08_eloquent_orm/eloquent_en.md)
- [Relationships (관계 정의)](./08_eloquent_orm/eloquent-relationships_en.md)
- [Collections (Eloquent 컬렉션)](./08_eloquent_orm/eloquent-collections_en.md)
- [Mutators / Casts (뮤테이터 및 캐스트)](./08_eloquent_orm/eloquent-mutators_en.md)
- [API Resources (API 리소스)](./08_eloquent_orm/eloquent-resources_en.md)
- [Serialization (직렬화)](./08_eloquent_orm/eloquent-serialization_en.md)
- [Factories (팩토리)](./08_eloquent_orm/eloquent-factories_en.md)

### AI (인공지능 (AI)) - `src/09_ai/`

- [AI SDK (라라벨 AI SDK)](./09_ai/ai-sdk_en.md)
- [MCP (모델 컨텍스트 프로토콜 (MCP))](./09_ai/mcp_en.md)
- [Boost (라라벨 Boost)](./09_ai/boost_en.md)

### Testing (테스트) - `src/10_testing/`

- [Getting Started (테스트 시작하기)](./10_testing/testing_en.md)
- [HTTP Tests (HTTP 테스트)](./10_testing/http-tests_en.md)
- [Console Tests (콘솔 테스트)](./10_testing/console-tests_en.md)
- [Browser Tests (브라우저 테스트 (Dusk))](./10_testing/dusk_en.md)
- [Database (데이터베이스 테스트)](./10_testing/database-testing_en.md)
- [Mocking (모킹)](./10_testing/mocking_en.md)

### Packages (공식 패키지) - `src/11_packages/`

- [Cashier (Stripe) (캐셔 (스트라이프 결제))](./11_packages/billing_en.md)
- [Cashier (Paddle) (캐셔 (패들 결제))](./11_packages/cashier-paddle_en.md)
- [Dusk (더스크 (브라우저 자동화 테스트))](./11_packages/dusk_en.md)
- [Envoy (엔보이 (배포 자동화))](./11_packages/envoy_en.md)
- [Fortify (포티파이 (인증 백엔드))](./11_packages/fortify_en.md)
- [Folio (폴리오 (페이지 기반 라우팅))](./11_packages/folio_en.md)
- [Head (헤드 (SPA 메타 태그 제어))](./11_packages/head_en.md)
- [Homestead (홈스테드 (Vagrant 환경))](./11_packages/homestead_en.md)
- [Horizon (호라이즌 (Redis 큐 모니터링))](./11_packages/horizon_en.md)
- [Mix (믹스 (레거시 웹팩 빌드))](./11_packages/mix_en.md)
- [Octane (옥탄 (고성능 앱 서빙))](./11_packages/octane_en.md)
- [Passport (패스포트 (OAuth2 서버))](./11_packages/passport_en.md)
- [Pennant (페넌트 (피처 플래그 관리))](./11_packages/pennant_en.md)
- [Pint (핀트 (PHP 코드 스타일러))](./11_packages/pint_en.md)
- [Precognition (프리코그니션 (실시간 유효성 검사))](./11_packages/precognition_en.md)
- [Prompts (프롬프트 (대화형 CLI 입력))](./11_packages/prompts_en.md)
- [Pulse (펄스 (애플리케이션 상태 모니터링))](./11_packages/pulse_en.md)
- [Reverb (리버브 (웹소켓 서버))](./11_packages/reverb_en.md)
- [Sail (세일 (Docker 개발 환경))](./11_packages/sail_en.md)
- [Sanctum (생텀 (경량 API 토큰 인증))](./11_packages/sanctum_en.md)
- [Scout (스카우트 (전문 검색 엔진))](./11_packages/scout_en.md)
- [Socialite (소셜라이트 (소셜 OAuth 로그인))](./11_packages/socialite_en.md)
- [Telescope (텔레스코프 (디버그 어시스턴트))](./11_packages/telescope_en.md)
- [Valet (발렛 (macOS 경량 개발 환경))](./11_packages/valet_en.md)

## 기타 기본 파일

- [Documentation ToC (documentation_en.md)](./documentation_en.md)
- [License (license_en.md)](./license_en.md)
- [Readme (readme_en.md)](./readme_en.md)
