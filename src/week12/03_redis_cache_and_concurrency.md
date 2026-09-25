---
layout: docs
title: "12주차 03강: Redis 캐시 아키텍처, 캐시 태그(Cache Tags)와 병렬 동시성(Concurrency)"
---

{% raw %}
# 📖 12주차 03강: Redis 캐시 아키텍처, 캐시 태그(Cache Tags)와 병렬 동시성(Concurrency)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 인기 도서 목록을 초고속 인메모리 Redis 캐시에 적재하여 1ms 응답 속도를 달성하고, 캐시 태그(Tags)로 정밀하게 무효화하며, 라라벨 11의 `Concurrency` 파사드로 다중 외부 택배사 배송 조회를 병렬 동시 처리합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 연말 베스트셀러 발표 날 메인 페이지에 동시 접속자가 5,000명이 몰렸는데, 메인 페이지를 열 때마다 `Book::with('authors')->orderByDesc('sales_count')->take(10)` 복잡한 조인 쿼리가 5,000번씩 돌면서 DB CPU 점유율이 99%까지 치솟았어!"  
🐱 **지니**: "도로시, 바로 그럴 때 **Redis 캐시**와 `Cache::remember()`를 쓰는 거란다! 첫 번째 손님이 들어왔을 때 DB에서 뽑은 결과를 초고속 메모리(Redis)에 딱 넣어두면, 나머지 4,999명은 DB를 전혀 건드리지 않고 0.001초 만에 결과를 받아보지!"  
🐶 **토토**: "멍멍! 관리자가 책 가격이나 표지를 수정했을 때만 그 카테고리 캐시만 쏙 골라서 지우고 싶다면 **캐시 태그(Cache Tags)**가 최고야! 그리고 고객 주문 조회 페이지에서 여러 택배사 API를 한꺼번에 찌를 때는 라라벨 11의 **동시성(Concurrency)** 파사드로 3배 빠르게 병렬 조회하자멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **Redis 캐시 저장소 연동:** `config/cache.php` 및 `.env` 캐시 스토어 전환
2. **`Cache::remember()`를 이용한 베스트셀러 고속 서빙:** 1시간 TTL 설정 및 캐시 히트(Hit/Miss) 검증
3. **캐시 태그(Cache Tags):** `Cache::tags(['books', "category:{$id}"])`를 이용한 정밀 무효화
4. **원자적 락(Atomic Locks):** `Cache::lock()`을 활용한 동일 주문 중복 결제 방지
5. **라라벨 11 `Concurrency::run()`:** 외부 3대 택배사(CJ, 한진, 우체국) 배송 추적 병렬 동시 처리

---

## 🛠️ 단계별 실습 절차

### 1단계: Redis 캐시 스토어 설정 (.env)

`.env` 파일에서 캐시 기본 드라이버를 `redis`로 지정합니다.

```env
CACHE_STORE=redis
REDIS_CLIENT=phpredis
REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379
```

> 🐶 **토토의 팁!**  
> "캐시 태그(Cache Tags) 기능은 `file`이나 `database` 드라이버에서는 지원되지 않고, 오직 `redis`나 `memcached` 같은 고급 캐시 저장소에서만 작동한다멍!"

---

### 2단계: 베스트셀러 목록 Redis 캐싱 (`Cache::remember`)

`app/Services/BookRankingService.php`를 작성합니다:

```php
<?php

namespace App\Services;

use App\Models\Book;
use Illuminate\Support\Facades\Cache;

class BookRankingService
{
    /**
     * 주간 종합 베스트셀러 10권 조회 (1시간 동안 캐싱)
     */
    public function getWeeklyBestsellers(): array
    {
        // 'bestsellers:weekly' 키로 캐시가 있으면 반환, 없으면 클로저 실행 후 캐시 저장
        return Cache::tags(['books', 'bestsellers'])->remember('bestsellers:weekly', now()->addHour(), function () {
            // 복잡한 집계 쿼리 실행
            return Book::with(['authors', 'publisher'])
                ->where('is_sold_out', false)
                ->orderByDesc('sales_count')
                ->take(10)
                ->get()
                ->toArray();
        });
    }

    /**
     * 카테고리별 인기 도서 조회 (캐시 태그 다중 적용)
     */
    public function getBestsellersByCategory(int $categoryId): array
    {
        $cacheKey = "category_bestsellers:{$categoryId}";

        return Cache::tags(['books', "category:{$categoryId}"])->remember($cacheKey, now()->addMinutes(30), function () use ($categoryId) {
            return Book::where('category_id', $categoryId)
                ->orderByDesc('sales_count')
                ->take(8)
                ->get()
                ->toArray();
        });
    }
}
```

---

### 3단계: 도서 정보 변경 시 캐시 태그 무효화 (`flush`)

책의 가격이나 제목이 변경되거나 새 도서가 등록되었을 때, 전체 캐시를 날리지 않고 해당 태그의 캐시만 스마트하게 비워줍니다:

`app/Observers/BookObserver.php`:

```php
<?php

namespace App\Observers;

use App\Models\Book;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class BookObserver
{
    public function updated(Book $book): void
    {
        // 1. 해당 도서가 속한 카테고리 태그의 캐시만 정밀 삭제
        Cache::tags(["category:{$book->category_id}"])->flush();

        // 2. 베스트셀러 태그 캐시 삭제
        Cache::tags(['bestsellers'])->flush();

        Log::info("[캐시 무효화] 도서 #{$book->id} 변경으로 카테고리 #{$book->category_id} 및 베스트셀러 캐시가 갱신되었습니다.");
    }
}
```

---

### 4단계: 원자적 락(Atomic Lock)을 활용한 중복 결제 방지

고객이 '결제하기' 버튼을 초당 5번 연속으로 눌렀을 때, 첫 번째 요청만 통과시키고 나머지는 차단하는 원자적 락입니다:

```php
use Illuminate\Support\Facades\Cache;

public function processPayment(Request $request, int $orderId)
{
    // 'lock:order:123' 락을 최대 10초 동안 획득 시도
    $lock = Cache::lock("lock:order:{$orderId}", 10);

    if (!$lock->get()) {
        return response()->json([
            'message' => '현재 결제 처리가 이미 진행 중입니다. 잠시만 기다려 주세요.'
        ], 429);
    }

    try {
        // 결제 PG사 통신 및 주문 완료 처리
        $this->chargeCard($orderId);

        return response()->json(['status' => 'success']);
    } finally {
        // 처리가 끝나면 안전하게 락 해제
        $lock->release();
    }
}
```

---

### 5단계: 라라벨 11 병렬 동시성(`Concurrency::run`) 배송 추적

고객의 마이페이지에서 주문한 도서들의 배송 상태를 외부 3개 택배사(CJ, 한진, 우체국)에 각각 조회해야 한다면, 순차적으로 1초씩 걸려 총 3초가 걸리던 작업을 **동시에 병렬 실행**하여 1초 만에 끝낼 수 있습니다!

`app/Http/Controllers/OrderTrackingController.php`:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\Concurrency;
use Illuminate\Support\Facades\Http;
use Illuminate\Http\JsonResponse;

class OrderTrackingController extends Controller
{
    public function trackAllCarriers(string $trackingNumber): JsonResponse
    {
        $startTime = microtime(true);

        // 라라벨 11 Concurrency 파사드로 3개의 외부 HTTP 조회를 병렬 실행!
        [$cjStatus, $hanjinStatus, $postStatus] = Concurrency::run([
            fn () => $this->fetchCarrierStatus('CJ대한통운', 'https://api.mock.test/cj/' . $trackingNumber),
            fn () => $this->fetchCarrierStatus('한진택배', 'https://api.mock.test/hanjin/' . $trackingNumber),
            fn () => $this->fetchCarrierStatus('우체국택배', 'https://api.mock.test/epost/' . $trackingNumber),
        ]);

        $elapsed = round(microtime(true) - $startTime, 2);

        return response()->json([
            'elapsed_seconds' => $elapsed,
            'carriers' => [
                'CJ' => $cjStatus,
                'Hanjin' => $hanjinStatus,
                'Epost' => $postStatus,
            ],
        ]);
    }

    private function fetchCarrierStatus(string $name, string $url): array
    {
        // 1초 슬립 시뮬레이션
        usleep(1000000); 

        return [
            'carrier' => $name,
            'status' => '배송 중 (간선 상차 완료)',
            'updated_at' => now()->toDateTimeString(),
        ];
    }
}
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. Redis 캐시 아키텍처와 원자성 (Atomicity)

Redis는 단일 스레드 이벤트 루프 모델로 동작하기 때문에 `Cache::increment()`, `Cache::decrement()`, `Cache::lock()` 같은 연산이 100% 원자적으로 수행됩니다. 즉, 수천 대의 웹 서버가 동시에 같은 키를 건드려도 Race Condition(경합 상태)이 발생하지 않습니다.

### 2. 스웜프 방지 (Cache Stampede Prevention)

캐시 유효기간이 끝나는 순간 1,000명의 사용자가 동시에 DB에 몰려 서버가 폭발하는 현상(Cache Stampede)을 막기 위해 라라벨은 락 기반 자동 갱신을 지원합니다:

```php
// flexible 캐시 (신선한 캐시 5분, 만료 후 백그라운드 갱신 허용 유예 10분)
Cache::flexible('bestsellers', [300, 600], function () {
    return Book::topSales()->get();
});
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **캐시 키 이름 짓기 네임스페이스 규칙:**  
   캐시 키가 `bestseller`처럼 너무 짧으면 다른 패키지나 모듈과 충돌할 수 있습니다. `도메인:엔티티:조건` (예: `shop:books:bestseller:week25`) 형식으로 일관성 있게 설계하세요!
2. **Concurrency 실행 드라이버 확인:**  
   `Concurrency::run()`은 기본적으로 프로세스 포크(Fork) 드라이버를 사용합니다. CLI 환경이나 Swoole/Octane 환경에서 안전하게 작동하는지 `config/concurrency.php` 설정을 확인하세요!

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** Redis 캐시에서 특정 태그가 붙은 모든 캐시 항목만 골라서 즉시 삭제하는 메소드는 무엇일까요?
   - 정답: `Cache::tags(['태그명'])->flush()`
2. **과제:** 책의 상세 페이지 조회수(`view_count`)를 매번 DB `UPDATE` 치지 않고, Redis `Cache::increment("books:{$id}:views")`로 초고속 카운팅한 뒤 자정에 DB로 일괄 반영하는 배치 로직을 구상해 보세요!
{% endraw %}
