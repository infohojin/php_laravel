---
layout: docs
title: "14주차 03강: 라라벨 펄스(Pulse) 실시간 APM 모니터링 & 옥탄(Octane) 초고속 메모리 상주 서빙"
---

{% raw %}
# 📖 14주차 03강: 라라벨 펄스(Pulse) 실시간 APM 모니터링 & 옥탄(Octane) 초고속 메모리 상주 서빙

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 대규모 트래픽 발생 시 서버 병목(느린 쿼리, 느린 API, 큐 지연)을 실시간으로 추적하는 라라벨 펄스(Pulse)를 구축하고, FrankenPHP/Swoole 기반의 메모리 상주 엔진인 라라벨 옥탄(Octane)을 연동하여 초당 10,000건 이상의 고속 서빙을 달성합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 지니샵 오픈 이벤트로 '선착순 1,000명 신간 도서 100원 특가'를 진행하기로 했는데, 순간 동시 접속자가 3만 명이 몰리면 우리 서버가 버틸 수 있을까? 그리고 어떤 쿼리나 외부 API가 서버를 느리게 만드는지 어떻게 실시간으로 알아내지?"  
🐱 **지니**: "도로시, 바로 그럴 때 무료 오픈소스 공식 APM인 **라라벨 펄스(Laravel Pulse)**와 초고속 메모리 상주 엔진인 **라라벨 옥탄(Laravel Octane)**의 최강 콤비가 출동할 차례란다! 펄스로 서버의 맥박(느린 쿼리, 큐 적체, 외부 PG사 응답 시간)을 실시간 감시하고, 옥탄으로 PHP 프레임워크 부팅 오버헤드를 0으로 만들어 10배 빠른 처리량을 뽑아내는 거지!"  
🐶 **토토**: "멍멍! 옥탄 환경에서는 PHP 프로세스가 죽지 않고 메모리에 계속 살아있기 때문에 정적 변수나 싱글톤에 이전 손님의 데이터가 남지 않도록 상태 초기화 규칙을 꼭 지켜야 한다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **라라벨 펄스(Pulse) 설치 및 실시간 APM 대시보드 구축:** `/pulse`
2. **5대 핵심 성능 병목 관제:**
   - Servers (서버 CPU/메모리)
   - Slow Requests (1초 이상 소요된 느린 엔드포인트)
   - Slow Queries (풀 테이블 스캔 유발 쿼리)
   - Slow Jobs (큐 작업 지연)
   - Slow Outgoing Requests (토스/스트라이프 외부 통신 지연)
3. **라라벨 옥탄(Octane) 설치 및 아키텍처 이해:** FrankenPHP / Swoole 엔진 연동
4. **옥탄 환경에서의 메모리 누수 방지 및 상태 리셋(Resetting State) 패턴 체득**

---

## 🛠️ 단계별 실습 절차

### 1단계: Laravel Pulse 설치 및 데이터베이스 구성

Pulse 패키지를 설치하고 전용 마이그레이션을 실행합니다:

```bash
composer require laravel/pulse
php artisan pulse:install
php artisan migrate
```

> 💡 **Pulse 데이터베이스 권장사항:**  
> 트래픽이 많은 상용 서비스에서는 메인 비즈니스 DB에 부하를 주지 않도록 `config/pulse.php`에서 별도의 모니터링 전용 MySQL/PostgreSQL 커넥션(`DB_PULSE_CONNECTION`)을 지정하는 것이 좋습니다!

---

### 2단계: Pulse 관제 대시보드 확인 및 권한 통제

웹 브라우저에서 `http://127.0.0.1:8000/pulse`로 접속하면, 현대적인 실시간 APM 대시보드가 열립니다:

- **서버 지표:** 현재 서버의 CPU 부하율 및 메모리 사용량 그래프
- **느린 쿼리(Slow Queries):** 실행 시간이 긴 SQL 문과 호출된 파일/라인 번호 표시
- **느린 웹 요청(Slow Requests):** 사용자가 겪은 1,000ms 이상의 느린 URL 목록
- **외부 요청(Slow Outgoing Requests):** 외부 PG사 통신에 소요된 평균 왕복 시간
- **사용자별 작업량(User Usage):** 가장 많은 요청을 보낸 독자 계정

`app/Providers/PulseServiceProvider.php`에서 관리자만 대시보드에 접근하도록 보호합니다:

```php
protected function gate(): void
{
    Gate::define('viewPulse', function ($user) {
        return $user->is_admin;
    });
}
```

---

### 3단계: Laravel Octane 설치 및 고성능 서빙

PHP-FPM은 매 요청마다 라라벨 프레임워크 전체를 부팅하고 종료하지만, **Octane**은 프레임워크를 메모리에 상주시켜 부팅 시간을 0ms로 단축합니다!

```bash
composer require laravel/octane
php artisan octane:install --server=frankenphp
```

옥탄 서버를 시작합니다:

```bash
php artisan octane:start --workers=4 --port=8000
```

> ⚡ **벤치마크 성능 향상:**  
> - 전통적인 PHP-FPM: 약 800 ~ 1,200 req/s  
> - Laravel Octane (FrankenPHP / Swoole): **초당 8,000 ~ 15,000 req/s** (10배 이상 폭증!)  

---

### 4단계: 옥탄(Octane) 상태 오염 및 메모리 누수 방지

옥탄 환경에서는 PHP 스크립트가 죽지 않고 계속 돌기 때문에, 요청 간 싱글톤 상태나 정적(Static) 프로퍼티가 다음 요청자에게 노출될 위험이 있습니다!

`config/octane.php`의 `listeners` 항목에 요청 종료 시 상태를 초기화할 리스너를 등록합니다:

```php
'flush' => [
    App\Services\CartSessionService::class, // 요청 종료 시 인메모리 캐시 초기화
],
```

코드 작성 시 주의 패턴:

```php
// ❌ 위험: 이전 사용자의 장바구니 데이터가 다음 사용자에게 노출됨!
class BadCartService {
    public static array $currentItems = [];
}

// ✅ 안전: 서비스 컨테이너의 Request 바인딩 또는 Octane의 clean 리스너 활용
class SafeCartService {
    public function getItems(Request $request): array {
        return $request->session()->get('cart', []);
    }
}
```

---

### 5단계: 옥탄 병렬 동시 작업 (`Octane::concurrently`)

동시에 여러 쿼리를 멀티스레드로 처리하여 응답 속도를 극대화합니다:

```php
use Laravel\Octane\Facades\Octane;

[$bestsellers, $recentReviews, $promotions] = Octane::concurrently([
    fn () => Book::bestsellers()->take(5)->get(),
    fn () => Review::with('user')->latest()->take(5)->get(),
    fn () => PromotionBanner::active()->get(),
]);
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. Pulse의 Recorder 아키텍처

Pulse는 애플리케이션의 성능을 모니터링하기 위해 백그라운드에서 가벼운 **Recorder**들을 가동합니다:
- `RequestsRecorder` : 1초 이상 지연 요청 샘플링
- `SlowQueriesRecorder` : 500ms 이상 슬로우 쿼리 감지
- `JobsRecorder` : 큐 대기 시간 및 실행 시간 기록
- `OutgoingRequestsRecorder` : `Http` 파사드를 거치는 외부 API 벤치마크

### 2. Octane 워커 수와 Max Requests

워커가 무한히 메모리를 먹어 OOM(Out of Memory)이 발생하는 것을 막기 위해, 일정 요청 수(예: 1,000회)마다 워커를 우아하게 자동 재시작(Graceful Restart)하도록 설정합니다:

```bash
php artisan octane:start --max-requests=1000
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **Octane 코드 갱신 감지 (`--watch`):**  
   옥탄은 코드를 메모리에 올려두므로 PHP 파일을 수정해도 바로 반영되지 않습니다! 개발 환경에서는 Node의 Chokidar를 연동한 자동 리로드 플래그를 사용하세요:
   ```bash
   php artisan octane:start --watch
   ```
2. **Pulse 데이터 용량 관리:**  
   수집된 메트릭 데이터가 DB에 무한정 쌓이지 않도록 주기적으로 `php artisan pulse:clear` 또는 `pulse:check` 배치를 돌려 7일 이상 지난 오래된 통계를 자동 정리해야 합니다.

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 라라벨 Octane 환경에서 여러 개의 독립된 작업을 여러 워커 프로세스에서 병렬로 동시 실행하여 그 결과를 튜플로 반환받는 파사드 메소드는 무엇일까요?
   - 정답: `Octane::concurrently([...])`
2. **과제:** 지니샵 메인 페이지에 의도적으로 1.5초가 걸리는 슬로우 쿼리를 하나 심어놓고, `/pulse` 대시보드의 **Slow Queries** 섹션에 해당 쿼리가 정확히 감지되어 카운팅되는지 확인해 보세요!
{% endraw %}
