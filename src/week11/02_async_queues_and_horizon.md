---
layout: docs
title: "11주차 02강: 비동기 큐(Queues) 작업 처리와 라라벨 호라이즌(Horizon) 모니터링"
---

{% raw %}
# 📖 11주차 02강: 비동기 큐(Queues) 작업 처리와 라라벨 호라이즌(Horizon) 모니터링

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 대용량 전자책(eBook) 워터마크 삽입 및 영수증 PDF 생성과 같은 무거운 작업을 비동기 큐(Queue) Job으로 분리하고, Redis 기반의 큐 관리 툴인 라라벨 호라이즌(Horizon)으로 실시간 처리량과 실패 작업을 모니터링합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 전자책(eBook)을 구매하면 불법 복제를 막기 위해 모든 페이지 하단에 '구매자: 홍길동 (주문번호 ORD-1234)'이라는 워터마크를 찍어서 PDF를 다운로드할 수 있게 해줘야 해. 그런데 500페이지짜리 책에 워터마크를 찍는 데 무려 15초나 걸려! 손님이 웹 브라우저 타임아웃 504 Gateway Timeout을 보고 주문이 취소된 줄 알았대!"  
🐱 **지니**: "도로시, 바로 그런 CPU 집약적인 무거운 작업이야말로 **비동기 큐(Queues)**의 전담 영역이란다! 손님에게는 '주문 완료! 전자책 워터마크 작업이 준비 중입니다'라고 0.1초 만에 알리고, 백그라운드 큐 워커가 뒤에서 묵묵히 PDF를 구워내는 거지!"  
🐶 **토토**: "멍멍! 큐 작업이 중간에 뻗거나 메모리가 모자라면 어떡하냐고? **라라벨 호라이즌(Laravel Horizon)**을 띄워두면 실시간 처리량, 작업 대기 시간, 실패한 이유와 에러 스택 트레이스까지 예쁜 웹 대시보드에서 다 보여준다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **큐 환경 설정:** `.env`의 `QUEUE_CONNECTION`을 `sync`(동기)에서 `database` 또는 고속 인메모리 `redis`로 전환
2. **전자책 워터마크 생성 Job 제작:** `ShouldQueue`를 구현한 `ProcessBookWatermarkJob` 작성
3. **견고한 큐 제어:** 최대 시도 횟수(`$tries`), 타임아웃(`$timeout`), 지수 백오프(`$backoff`), 실패 콜백(`failed()`)
4. **라라벨 호라이즌(Laravel Horizon) 설치 및 연동:** 실시간 큐 모니터링 대시보드 구축 및 실패 작업 재시도(`queue:retry`)

---

## 🛠️ 단계별 실습 절차

### 1단계: 큐 드라이버 설정 및 마이그레이션

로컬 실습 및 배포 환경에 따라 `database` 드라이버 또는 `redis` 드라이버를 선택합니다.

```env
# .env
QUEUE_CONNECTION=redis
REDIS_CLIENT=phpredis
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

> 💡 **데이터베이스 큐를 사용하고 싶다면?**  
> `QUEUE_CONNECTION=database`로 설정하고 아래 명령어로 큐 테이블 마이그레이션을 생성합니다:  
> `php artisan queue:table`  
> `php artisan queue:failed-table`  
> `php artisan migrate`

---

### 2단계: 전자책 워터마크 생성 Job 클래스 작성

Artisan으로 새로운 잡(Job)을 생성합니다.

```bash
php artisan make:job ProcessBookWatermarkJob
```

생성된 `app/Jobs/ProcessBookWatermarkJob.php`를 다음과 같이 작성합니다:

```php
<?php

namespace App\Jobs;

use App\Models\Book;
use App\Models\User;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use Throwable;

class ProcessBookWatermarkJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    /**
     * 작업 최대 재시도 횟수
     */
    public int $tries = 3;

    /**
     * 작업 최대 허용 실행 시간(초) - 초과 시 실패 처리
     */
    public int $timeout = 120;

    /**
     * 재시도 간격(초) - 지수 백오프 적용 (1회차 5초, 2회차 15초, 3회차 45초)
     */
    public array $backoff = [5, 15, 45];

    /**
     * 새 Job 인스턴스 생성
     */
    public function __construct(
        public User $user,
        public Book $book,
        public string $orderNumber
    ) {
        // 'watermark' 전용 우선순위 큐 지정
        $this->onQueue('watermark');
    }

    /**
     * 백그라운드 워커에 의해 실행되는 작업 본문
     */
    public function handle(): void
    {
        Log::info("[큐 작업 시작] 사용자 '{$this->user->name}'을 위한 '{$this->book->title}' 전자책 워터마크 작업 시작");

        // 1. 원본 PDF 경로 확인
        $sourcePdf = "ebooks/originals/{$this->book->id}.pdf";
        if (!Storage::disk('local')->exists($sourcePdf)) {
            throw new \Exception("도서 ID {$this->book->id}의 원본 PDF 파일을 찾을 수 없습니다.");
        }

        // 2. 가상의 무거운 워터마크 프로세싱 시뮬레이션
        // (실제 실무에서는 setasign/fpdi 라이브러리 등을 사용하여 PDF 각 페이지 하단에 텍스트를 인쇄함)
        sleep(3); // 3초 소요되는 CPU 작업

        $watermarkText = "구매자: {$this->user->name} ({$this->user->email}) | 주문번호: {$this->orderNumber}";
        $outputPdfPath = "ebooks/watermarked/{$this->user->id}_{$this->book->id}.pdf";

        Storage::disk('local')->put($outputPdfPath, "WATERMARKED CONTENT FOR: {$watermarkText}");

        Log::info("[큐 작업 완료] 도서 '{$this->book->title}' 워터마크 PDF 생성 완료: {$outputPdfPath}");
    }

    /**
     * 모든 재시도($tries)가 실패했을 때 호출되는 최종 실패 콜백
     */
    public function failed(?Throwable $exception): void
    {
        Log::critical("[큐 작업 최종 실패] 전자책 워터마크 생성 실패! 긴급 점검 필요", [
            'user_id' => $this->user->id,
            'book_id' => $this->book->id,
            'error' => $exception?->getMessage(),
        ]);

        // 관리자에게 알림 또는 고객 주문 상태를 '워터마크 생성 실패'로 갱신
    }
}
```

---

### 3단계: 컨트롤러에서 지연(Delay) 및 체이닝(Chaining) 디스패치

주문 완료 컨트롤러에서 전자책 구매 건이 있을 때 잡을 큐로 보냅니다:

```php
// 즉시 큐로 디스패치
ProcessBookWatermarkJob::dispatch($user, $book, $order->order_number);

// 10초 뒤에 실행되도록 지연(Delay) 디스패치
ProcessBookWatermarkJob::dispatch($user, $book, $order->order_number)
    ->delay(now()->addSeconds(10));

// 여러 작업 순차 체이닝 (PDF 워터마크 완료 후 -> DRM 암호화 -> 다운로드 링크 발송)
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ProcessBookWatermarkJob($user, $book, $order->order_number),
    new EncryptDrmEbookJob($user, $book),
    new SendEbookDownloadLinkJob($user, $book),
])->dispatch();
```

---

### 4단계: 큐 워커 실행 및 실시간 테스트

개발 환경에서는 Artisan 명령어로 큐 워커를 기동합니다.

```bash
# 기본 큐 및 watermark 큐를 함께 처리하는 워커 실행
php artisan queue:work --queue=high,watermark,default --tries=3
```

> 🐶 **토토의 팁!**  
> "`queue:work`는 코드를 메모리에 한 번 올려두고 계속 실행하기 때문에 PHP 코드를 수정해도 워커에는 반영되지 않는다멍! 코드를 고쳤다면 `Ctrl+C`로 껐다 켜거나 `php artisan queue:restart`를 외치라멍!"

---

### 5단계: 라라벨 호라이즌(Horizon) 설치 및 대시보드 구성

Redis 큐를 사용한다면 라라벨 공식 패키지인 **Horizon**을 통해 화려한 실시간 관제 센터를 얻을 수 있습니다!

```bash
composer require laravel/horizon
php artisan horizon:install
php artisan migrate
```

`config/horizon.php`에서 큐 워커 프로세스 수와 밸런싱 모드를 확인합니다:

```php
'environments' => [
    'local' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['high', 'watermark', 'default'],
            'balance' => 'auto', // 큐 작업량에 따라 워커 수 동적 조절
            'minProcesses' => 1,
            'maxProcesses' => 5,
            'tries' => 3,
        ],
    ],
],
```

호라이즌을 시작합니다:

```bash
php artisan horizon
```

웹 브라우저에서 `http://127.0.0.1:8000/horizon`에 접속하면, 멋진 다크 테마 대시보드가 열립니다:
- **Dashboard:** 현재 큐 상태 (Active Workers, Jobs Per Minute, Wait Time)
- **Batches & Pending Jobs:** 대기 중인 작업 목록
- **Failed Jobs:** 실패한 작업의 Exception 내용과 클릭 한 번으로 재시도(`Retry`)할 수 있는 버튼 제공!

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. 동기(Sync) vs 비동기 큐의 메모리 및 아키텍처

| 항목 | 동기 드라이버 (`sync`) | 비동기 큐 (`redis` / `database`) |
| :--- | :--- | :--- |
| **실행 주체** | 사용자의 웹 요청 프로세스 (PHP-FPM) | 별도의 백그라운드 데몬 프로세스 (CLI) |
| **HTTP 응답 시간** | 모든 작업이 끝날 때까지 브라우저 대기 | 작업 큐 적재 즉시(10ms 이내) 200 OK 반환 |
| **서버 부하 분산** | 웹 서버 메모리 고갈 위험 | 별도의 큐 워커 전용 인스턴스/컨테이너로 분리 가능 |
| **장애 복구** | 타임아웃 시 데이터 유실 위험 | `$tries`, `$backoff`, `failed_jobs` 테이블에 보존 |

### 2. 고유 작업 (Unique Jobs)

만약 사용자가 광클하여 똑같은 책에 대한 워터마크 작업이 큐에 10개 쌓이는 것을 막으려면 `ShouldBeUnique` 인터페이스를 구현하면 됩니다:

```php
use Illuminate\Contracts\Queue\ShouldBeUnique;

class ProcessBookWatermarkJob implements ShouldQueue, ShouldBeUnique
{
    // 60초 동안 동일 도서 및 사용자에 대한 중복 큐 진입 방지
    public int $uniqueFor = 60;

    public function uniqueId(): string
    {
        return $this->user->id . '-' . $this->book->id;
    }
}
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **Horizon 대시보드 보안:**  
   운영 환경(`production`)에서는 누구나 호라이즌에 들어와서 큐를 조작하면 안 됩니다! `app/Providers/HorizonServiceProvider.php`의 `gate()` 메소드에서 관리자 계정만 접근할 수 있도록 권한을 걸어주어야 합니다:
   ```php
   protected function gate(): void
   {
       Gate::define('viewHorizon', function ($user) {
           return $user->is_admin;
       });
   }
   ```
2. **실패한 작업 관리 CLI:**  
   터미널에서 실패한 작업을 확인하고 재실행할 때는 다음 명령어를 사용합니다:
   - `php artisan queue:failed` : 실패 목록 조회
   - `php artisan queue:retry all` : 실패한 모든 작업 재시도
   - `php artisan queue:flush` : 실패 기록 삭제

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 큐 작업이 일시적인 네트워크 장애로 실패했을 때, 1회차 10초 뒤, 2회차 30초 뒤, 3회차 60초 뒤에 재시도하도록 설정하는 클래스 프로퍼티는 무엇일까요?
   - 정답: `public array $backoff = [10, 30, 60];`
2. **과제:** 호라이즌 대시보드(`/horizon`)에 접속한 상태에서, 일부러 예외(`throw new Exception('테스트 에러')`)를 발생시키는 테스트 잡을 디스패치해 보세요. 대시보드의 **Failed Jobs** 탭에 에러가 뜨는지 확인하고, 웹 화면의 **Retry** 버튼을 눌러 재시도해 보세요!
{% endraw %}
