---
layout: docs
title: "02강: 라라벨 13 디렉터리 구조 해부 & 도서 서점 환경 설정 (.env)"
---

{% raw %}
# 02강: 라라벨 13 디렉터리 구조 해부 & 도서 서점 환경 설정 (.env)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 라라벨 13의 슬림 아키텍처 디렉터리 구조 정복, `.env` 환경 파일 및 `config/` 설정  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [디렉터리 구조 (Directory Structure)](../docs/02_getting_started/structure_ko.md), [환경 설정 (Configuration)](../docs/02_getting_started/configuration_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! `jinyshop` 폴더를 VS Code 에디터로 열어봤는데, 폴더가 너무 많아서 머리가 어지러워요! `app/`, `bootstrap/`, `config/`, `routes/`, `resources/`... 도대체 우리가 판매할 책 목록과 컨트롤러 코드는 어디에 넣어야 해요?"

🐱 **지니**: "후후, 처음 보면 지도 없는 미로처럼 보이지? 하지만 라라벨 13은 과거 버전보다 폴더 구조가 엄청나게 **슬림(Slim)**해졌단다! 불필요한 보일러플레이트 파일 수십 개가 사라지고, 오직 핵심적인 파일만 남아있지. 책(Book) 모델은 `app/Models/`에, 도서 화면 라우트는 `routes/web.php`에, HTML 화면은 `resources/views/`에 위치한단다. 그리고 서점의 비밀번호와 DB 주소는 `.env`라는 비밀 금고에 적어두는 거지!"

🐶 **토토**: "멍멍! 이전 라라벨 책을 보면 `app/Http/Kernel.php`를 찾으라고 하는데, 라라벨 11~13에서는 그 파일이 사라지고 `bootstrap/app.php`에서 모든 미들웨어와 예외 처리를 한 방에 끝낸다멍! 옛날 책 보고 헷갈리지 말라멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨 13 프로젝트의 주요 디렉터리 역할과 명명 규칙(Convention)을 완벽히 이해합니다.
2. `bootstrap/app.php`가 라라벨의 요청 진입점을 어떻게 관장하는지 확인합니다.
3. `.env` 파일을 열어 **지니샵(JinyShop)**에 맞게 애플리케이션 이름, 시간대, 데이터베이스 설정을 조정합니다.
4. `php artisan config:cache`와 `config:clear`의 차이와 환경 변수 캐싱 원리를 배웁니다.

---

## 📂 3. 라라벨 13 디렉터리 맵 (Directory Map)

```text
jinyshop/
├── app/                        # 🧠 서점의 핵심 비즈니스 로직
│   ├── Http/
│   │   └── Controllers/       # BookController 등 웹 요청 처리자
│   ├── Models/                # Book, Author, Order 등 Eloquent 데이터 모델
│   └── Providers/             # AppServiceProvider 등 시스템 등록소
├── bootstrap/
│   ├── app.php                # 🚀 라라벨 13의 통합 관제소 (라우트, 미들웨어, 예외)
│   └── providers.php          # 로드할 서비스 프로바이더 목록
├── config/                     # ⚙️ 프레임워크 및 서점 전역 설정 파일들
│   ├── app.php, database.php, session.php, filesystems.php ...
├── database/
│   ├── factories/             # BookFactory 등 가짜 도서 데이터 생성 공장
│   ├── migrations/            # books, orders 테이블 생성 스키마
│   └── seeders/               # 초기 카테고리 데이터 적재
├── public/                     # 🌐 웹 브라우저가 직접 접근하는 공개 웹 루트
│   └── index.php              # 모든 HTTP 요청이 맨 처음 도착하는 관문
├── resources/                  # 🎨 화면과 프론트엔드 원본 소스
│   ├── views/                 # Blade 도서 상세 페이지 템플릿
│   ├── css/                   # Tailwind CSS 스타일
│   └── js/                    # Alpine.js / Vue / React 스크립트
├── routes/                     # 🗺️ 서점 URL 길잡이
│   ├── web.php                # 일반 웹 브라우저 라우트 (/books, /cart)
│   └── console.php            # 아티산 스케줄러 및 CLI 명령어
├── storage/                    # 📦 로그, 업로드된 도서 표지 이미지, 세션 파일
│   ├── app/public/books/      # 고객에게 공개 서빙될 책 표지 이미지
│   └── logs/laravel.log       # 시스템 에러 및 결제 감사 로그
└── .env                        # 🔑 로컬 환경 비밀 설정 (Git에 커밋 금지!)
```

---

## 🛠️ 4. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `.env` 서점 환경 변수 커스터마이징

프로젝트 루트의 `.env` 파일을 텍스트 에디터로 엽니다. 서점의 기본 정보와 한국 표준시(KST) 설정을 반영합니다.

```ini
# 1. 서점 애플리케이션 명칭 및 로컬 URL
APP_NAME="JinyShop"
APP_ENV=local
APP_KEY=base64:... # artisan key:generate로 생성된 고유 키
APP_DEBUG=true
APP_TIMEZONE=Asia/Seoul
APP_URL=http://127.0.0.1:8000

# 2. 로케일 설정 (다국어 및 날짜 표시용)
APP_LOCALE=ko
APP_FALLBACK_LOCALE=en
APP_FAKER_LOCALE=ko_KR

# 3. 데이터베이스 연결 (기본 SQLite 또는 MySQL 선택)
DB_CONNECTION=sqlite
# MySQL을 사용하는 경우:
# DB_CONNECTION=mysql
# DB_HOST=127.0.0.1
# DB_PORT=3306
# DB_DATABASE=jinyshop
# DB_USERNAME=root
# DB_PASSWORD=secret
```

> ⚠️ **주의:** `.env` 파일은 데이터베이스 비밀번호나 결제 API 키 등 민감 정보가 포함되므로 절대로 깃 저장소에 커밋하지 않습니다. (`.gitignore`에 기본 포함되어 있습니다.)

---

### [Step 2] `bootstrap/app.php` 라라벨 13 통합 관제탑 확인

라라벨 13에서는 과거의 복잡했던 설정들이 `bootstrap/app.php` 단 하나의 플루언트(Fluent) 체이닝 코드로 통합되었습니다.

```php
<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up', // 서버 헬스체크 엔드포인트
    )
    ->withMiddleware(function (Middleware $middleware) {
        // 향후 관리자 전용 미들웨어나 장바구니 미들웨어를 여기에 등록합니다
    })
    ->withExceptions(function (Exceptions $exceptions) {
        // 결제 실패나 품절 도서 예외 처리를 여기에 등록합니다
    })->create();
```

---

### [Step 3] 아티산으로 환경 설정 조회 & 테스트

터미널에서 방금 변경한 환경 변수가 라라벨 프레임워크에 정상적으로 인식되는지 확인합니다.

```bash
# 1. 현재 앱 환경 상태 확인
php artisan env

# 2. config 헬퍼를 통한 애플리케이션 이름 출력 테스트
php artisan tinker --execute="echo config('app.name');"
# 출력: JinyShop

# 3. 시간대 출력 테스트
php artisan tinker --execute="echo config('app.timezone');"
# 출력: Asia/Seoul
```

---

## 🔍 5. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 환경 설정 캐싱 메커니즘 (`config:cache`)
- 로컬 개발 환경에서는 `.env` 파일을 수정하면 즉시 반영되지만, 실제 운영(Production) 서버에서는 요청마다 수십 개의 설정 파일을 읽으면 디스크 I/O 병목이 발생합니다.
- 따라서 운영 환경에서는 반드시 다음 명령을 실행하여 모든 설정을 단일 PHP 파일로 병합 캐싱해야 합니다:
  ```bash
  php artisan config:cache
  ```
- **치명적 주의사항**: `config:cache`가 실행된 이후에는 코드 내부에서 `env('APP_NAME')`을 직접 호출하면 `null`을 반환합니다! 반드시 `config('app.name')`처럼 `config()` 헬퍼를 통해 읽어야 합니다.

---

## 🐶 6. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`.env` 파일을 수정했는데 반영이 안 돼요!**  
>    이전에 실수로 `config:cache`를 실행했기 때문일 가능성이 99%다멍! 터미널에 `php artisan config:clear`를 입력하여 캐시를 지우면 즉시 새 값이 반영된다멍!
> 
> 2. **`No application encryption key has been specified.` 에러가 나요!**  
>    `.env` 파일의 `APP_KEY`가 비어 있어서 생기는 에러다멍. `php artisan key:generate`를 실행하면 32바이트 AES 암호화 키가 자동으로 쏙 채워진다멍!

---

## 💡 7. 2강 자가진단 과제

1. `.env` 파일의 `APP_NAME`을 `"JinyShop (지니의 온라인 서점)"`으로 바꾸고, 브라우저 타이틀이나 tinker에서 올바르게 출력되는지 확인해 보세요.
2. `routes/web.php` 파일을 열어 기본 `/` 라우트 클로저에서 `config('app.timezone')` 값을 `dd()`(Dump and Die) 함수로 화면에 찍어보세요.
{% endraw %}
