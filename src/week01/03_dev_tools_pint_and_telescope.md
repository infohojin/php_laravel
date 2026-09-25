---
layout: docs
title: "03강: 코드 스타일러 Pint & 실시간 디버거 Telescope 세팅"
---

{% raw %}
# 03강: 코드 스타일러 Pint & 실시간 디버거 Telescope 세팅

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** Laravel Pint로 깔끔한 PSR-12 코드 유지, Laravel Telescope로 서점 요청/쿼리/에러 실시간 관측  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Pint (코드 스타일러)](../docs/11_packages/pint_ko.md), [Telescope (디버깅 도구)](../docs/11_packages/telescope_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 여러 사람이 함께 코딩하다 보면 들여쓰기 탭이랑 스페이스가 뒤섞이거나 세미콜론 줄바꿈 스타일이 달라서 코드가 지저분해지잖아요. 그리고 나중에 고객이 주문하다가 에러가 났을 때 어떤 SQL 쿼리가 실패했는지 어떻게 눈으로 볼 수 있어요?"

🐱 **지니**: "도로시가 벌써 실무 팀 개발자의 시각을 갖추었구나! 라라벨에는 완벽한 해결책 두 가지가 기본으로 준비되어 있단다. 첫째는 **Laravel Pint**야. PHP-CS-Fixer를 기반으로 제작된 초고속 코드 스타일러로, 명령어 한 줄이면 모든 코드를 라라벨 공식 표준 스타일로 다듬어주지. 둘째는 바로 **Laravel Telescope(망원경)**란다! 웹 브라우저 화면에서 서버로 들어온 모든 HTTP 요청, 실행된 데이터베이스 쿼리, 로그, 큐 작업까지 엑스레이처럼 훤히 들여다볼 수 있는 최고급 디버깅 도우미란다!"

🐶 **토토**: "멍멍! Telescope는 개발 환경(`local`)에서만 켜야 해! 운영 서버에 아무 보안 장치 없이 열어두면 손님들의 비밀번호나 주문 내역이 노출될 수 있으니 주의하라멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. Laravel Pint를 실행하여 지니샵 프로젝트 전체의 코드 컨벤션을 자동 정렬합니다.
2. 개발 의존성(`--dev`)으로 Laravel Telescope를 설치하고 마이그레이션을 실행합니다.
3. 웹 브라우저에서 `http://127.0.0.1:8000/telescope` 대시보드에 접속합니다.
4. 서점 페이지를 몇 번 새로고침한 뒤 Telescope의 Requests 탭과 Queries 탭에서 데이터가 수집되는 것을 확인합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] Laravel Pint로 코드 컨벤션 자동 교정

Laravel 13 프로젝트에는 Pint가 기본으로 설치되어 있습니다. 프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
# 1. 변경된 파일 코드 스타일 자동 검사 및 교정
./vendor/bin/pint

# 2. 파일 수정 없이 스타일 위반 여부만 테스트 (CI 환경용)
./vendor/bin/pint --test
```

> **터미널 출력 예시:**
> ```text
>   PASS  ............. 15 files
>   Fixed: 0, Total: 15, Time: 0.05s
> ```

만약 들여쓰기나 빈 줄이 어긋난 코드가 있다면 Pint가 즉시 아래처럼 친절하게 고쳐줍니다:
```diff
-   public function index( ) {
+   public function index()
+   {
```

---

### [Step 2] Laravel Telescope 설치 및 설정

Telescope는 로컬 개발 디버깅에 특화된 패키지이므로 `--dev` 플래그를 붙여 설치합니다.

```bash
# 1. 패키지 설치
composer require laravel/telescope --dev

# 2. Telescope 에셋 및 설정 퍼블리싱
php artisan telescope:install
```

이 명령어를 실행하면 다음 파일들이 자동 생성됩니다:
- `config/telescope.php`: 수집할 항목(쿼리, 캐시, 뷰, 메일 등) 설정
- `app/Providers/TelescopeServiceProvider.php`: 접근 권한 및 필터링 규칙

---

### [Step 3] Telescope 관측용 데이터베이스 마이그레이션

Telescope가 수집한 요청과 쿼리 로그를 저장할 테이블들을 생성합니다:

```bash
php artisan migrate
```

> **터미널 출력:**
> ```text
>    INFO  Running migrations.
> 
>   2024_01_01_000000_create_telescope_entries_table ............ 15ms DONE
> ```

---

### [Step 4] Telescope 대시보드 접속 및 실시간 관측 확인

1. 로컬 서버가 켜져 있는지 확인합니다 (`php artisan serve`).
2. 웹 브라우저를 열고 `http://127.0.0.1:8000/telescope` 로 이동합니다.
3. 세련된 어두운 테마의 Telescope 대시보드가 열립니다!

![Telescope Dashboard](https://laravel.com/img/docs/telescope-requests.png)

#### 🔍 Telescope에서 관측할 수 있는 주요 항목:
- **Requests**: 서점 방문자의 HTTP 요청 주소, 상태 코드(200, 404, 500), 응답 시간(ms)
- **Queries**: 도서 목록을 불러올 때 실행된 실제 SQL 쿼리문과 실행 시간
- **Models**: 생성/수정/삭제된 Eloquent 모델 이력
- **Exceptions**: 발생한 에러의 스택 트레이스와 코드 라인 번호
- **Mails**: 고객에게 발송된 주문 확인 이메일 미리보기
- **Logs**: `Log::info()`나 `Log::error()`로 기록된 로그

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### Telescope 권한 제어 (`TelescopeServiceProvider.php`)
운영 서버(Production)에서는 인가된 관리자만 Telescope에 접속할 수 있도록 Gate를 설정해야 합니다:

```php
// app/Providers/TelescopeServiceProvider.php

protected function gate(): void
{
    Gate::define('viewTelescope', function ($user) {
        // 지니샵 관리자 이메일 목록에 포함된 경우에만 대시보드 열람 허용
        return in_array($user->email, [
            'jiny@jinyshop.com',
            'admin@jinyshop.com',
        ]);
    });
}
```

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **Telescope 테이블에 데이터가 너무 많이 쌓여요!**  
>    요청이 많아지면 DB 용량이 커질 수 있다멍! 터미널에서 `php artisan telescope:prune --hours=48`를 실행하면 48시간이 지난 오래된 디버그 로그가 싹 정리된다멍!
> 
> 2. **Pint 규칙을 우리 서점 팀 스타일에 맞추고 싶어요!**  
>    프로젝트 루트에 `pint.json` 파일을 만들고 `{"preset": "laravel"}` 옵션을 주면 커스텀 룰을 지정할 수 있다멍!

---

## 💡 6. 3강 자가진단 과제

1. 임의로 `routes/web.php`에 들여쓰기를 엉망으로 만든 뒤 `./vendor/bin/pint`를 실행하여 자동으로 예쁘게 정렬되는지 확인하세요.
2. 브라우저에서 존재하지 않는 주소(`http://127.0.0.1:8000/books/unknown-999`)에 접속하여 404 에러를 낸 뒤, Telescope의 **Requests** 및 **Views** 탭에서 해당 404 기록이 붉은색으로 찍히는지 확인하세요.
{% endraw %}
