---
layout: docs
title: "01강: 브라우저에서 화면까지 — 라라벨 13 요청 라이프사이클"
---

{% raw %}
# 01강: 브라우저에서 화면까지 — 라라벨 13 요청 라이프사이클

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 독자가 `http://127.0.0.1:8000/books`를 호출했을 때 라라벨 내부에서 일어나는 전체 실행 흐름  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [요청 라이프사이클 (Request Lifecycle)](../docs/03_architecture_concepts/lifecycle_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 브라우저 주소창에 `jinyshop.test/books`를 입력하고 엔터를 치면, 화면에 예쁜 책 표지들이 뜨기 전까지 라라벨 내부에서는 무슨 일이 일어나는 거예요? `public/index.php` 파일 하나밖에 없던데 어떻게 그 많은 기능이 돌아가죠?"

🐱 **지니**: "도로시, 그것이 바로 라라벨의 **요청 라이프사이클(Request Lifecycle)**이란다! 웹 브라우저의 요청은 거대한 오케스트라의 지휘봉과 같단다. `public/index.php`라는 현관문으로 들어온 요청은 오토로더를 거쳐 라라벨 애플리케이션 객체를 깨우고, 수많은 서비스 프로바이더(Service Provider)들이 조명과 음향을 세팅한 뒤, 라우터와 미들웨어라는 문지기를 통과해 알맞은 컨트롤러 방으로 안내되는 거란다!"

🐶 **토토**: "멍멍! 이 라이프사이클을 머릿속에 지도처럼 그려두면, 나중에 에러가 났을 때 '아, 이건 미들웨어에서 걸렸구나!' 혹은 '서비스 프로바이더가 안 켜졌네!' 하고 1초 만에 원인을 찾을 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨의 단일 진입점(Single Entry Point)인 `public/index.php`의 역할을 이해합니다.
2. 부트스트랩 $\rightarrow$ 서비스 프로바이더 $\rightarrow$ 미들웨어 $\rightarrow$ 라우터 $\rightarrow$ 컨트롤러로 이어지는 5단계 요청 여정을 추적합니다.
3. Telescope의 **Requests** 탭과 덤프(`dump()`)를 활용하여 실제 요청 객체가 어떻게 조립되는지 눈으로 확인합니다.

---

## 🗺️ 3. 요청 라이프사이클 5단계 다이어그램

```text
[독자의 브라우저] (GET /books)
       │
       ▼
[1. public/index.php]  ─── Composer 오토로더 로드 & bootstrap/app.php 호출
       │
       ▼
[2. Application 부트스트랩] ─── 환경 설정(.env) 로드, 에러 핸들러 준비
       │
       ▼
[3. 서비스 프로바이더 부트] ─── DB, 캐시, 세션, 이벤트 서비스 등록(register -> boot)
       │
       ▼
[4. 미들웨어 파이프라인]  ─── CSRF 검사, 세션 시작, 유지보수 모드 확인
       │
       ▼
[5. 라우터 & 컨트롤러]   ─── routes/web.php 매핑 ➔ BookController@index ➔ View 응답 반환!
```

---

## 🛠️ 4. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 단일 진입점 `public/index.php` 코드 확인

에디터에서 `public/index.php` 파일을 열어봅니다. 놀랍게도 파일 내용은 30줄 남짓에 불과합니다.

```php
<?php

use Illuminate\Http\Request;

define('LARAVEL_START', microtime(true));

// 1. 유지보수 모드(점검 중) 체크
if (file_exists($maintenance = __DIR__.'/../storage/framework/maintenance.php')) {
    require $maintenance;
}

// 2. Composer 자동 로딩(Autoloader) 등록
require __DIR__.'/../vendor/autoload.php';

// 3. 라라벨 13 앱 부트스트랩 및 요청 핸들링
(require_once __DIR__.'/../bootstrap/app.php')
    ->handleRequest(Request::capture());
```

> **지니의 핵심 해설:**  
> `Request::capture()`는 PHP의 슈퍼 전역 변수(`$_GET`, `$_POST`, `$_SERVER`, `$_COOKIE`)를 깔끔하고 객체 지향적인 `Illuminate\Http\Request` 객체로 포장해주는 순간이란다!

---

### [Step 2] `routes/web.php`에서 라이프사이클 테스트

라라벨이 요청을 받아 응답을 만드는 과정을 확인하기 위해 `routes/web.php`에 도서 목록 테스트 라우트를 추가합니다.

```php
// routes/web.php
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/books', function (Request $request) {
    // 현재 요청의 URL과 클라이언트 IP 확인
    return response()->json([
        'message' => '지니샵 도서 목록 요청 접수 완료!',
        'client_ip' => $request->ip(),
        'requested_url' => $request->fullUrl(),
        'execution_time_ms' => round((microtime(true) - LARAVEL_START) * 1000, 2),
    ]);
});
```

브라우저에서 `http://127.0.0.1:8000/books`에 접속합니다.

> **응답 결과:**
> ```json
> {
>   "message": "지니샵 도서 목록 요청 접수 완료!",
>   "client_ip": "127.0.0.1",
>   "requested_url": "http://127.0.0.1:8000/books",
>   "execution_time_ms": 12.45
> }
> ```
> 단 12ms 만에 전체 라이프사이클을 통과하여 응답을 돌려줍니다!

---

## 🔍 5. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 가장 중요한 부품: 서비스 프로바이더(Service Providers)
- 라라벨 부트스트래핑 과정에서 가장 중요한 주인공은 **서비스 프로바이더**입니다.
- 데이터베이스 쿼리 빌더, 큐 워커, 블레이드 템플릿 컴파일러 등 라라벨의 모든 핵심 코어 기능은 서비스 프로바이더의 `register()`와 `boot()` 메서드를 통해 컨테이너에 등록됩니다.
- 이 원리는 10주차 코어 아키텍처 Deep Dive에서 직접 결제 프로바이더를 제작하며 깊이 파고들게 됩니다!

---

## 🐶 6. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **서점이 리뉴얼 중일 때 손님들에게 점검 화면을 띄우고 싶어요!**  
>    터미널에 `php artisan down --secret="jiny-secret"`을 입력하면 즉시 점검 모드로 전환된다멍!  
>    비밀 키(`http://127.0.0.1:8000/jiny-secret`)를 가진 도로시만 서점에 들어갈 수 있고, 손님들에게는 503 점검 화면이 뜬다멍! 점검이 끝나면 `php artisan up`을 치면 된다멍!

---

## 💡 7. 1강 자가진단 과제

1. `routes/web.php`의 `/books` 라우트에서 `$request->userAgent()`를 추가하여 현재 본인이 사용하는 웹 브라우저 정보가 응답에 올바르게 찍히는지 확인하세요.
2. Telescope 대시보드(`http://127.0.0.1:8000/telescope/requests`)에 들어가 방금 호출한 `/books` 요청의 전체 라이프사이클 처리 시간과 로드된 미들웨어 목록을 확인하세요.
{% endraw %}
