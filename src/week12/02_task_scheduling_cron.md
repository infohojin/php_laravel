---
layout: docs
title: "12주차 02강: 작업 스케줄링(Task Scheduling)과 자정 배치 자동화"
---

{% raw %}
# 📖 12주차 02강: 작업 스케줄링(Task Scheduling)과 자정 배치 자동화

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 리눅스 서버에 단 하나의 크론(Cron)만 등록해 두고, 라라벨 스케줄러(`routes/console.php`)를 통해 매일 자정 24시간 미결제 주문 자동 취소 및 품절 임박 도서 통계 배치를 안정적으로 자동화합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객들이 무통장 입금으로 도서를 주문해두고 입금을 안 해서 책 50권이 일주일째 '주문 대기' 상태로 묶여 있어! 다른 손님들이 책을 못 사고 있대. 매일 밤 12시에 내가 야근하면서 24시간 지난 주문을 하나씩 찾아서 취소 버튼을 눌러야 해?"  
🐱 **지니**: "도로시, 잠은 푹 자야지! 라라벨의 **작업 스케줄러(Task Scheduling)**가 있잖니! 리눅스 크론탭에 `php artisan schedule:run` 딱 한 줄만 심어두면, 매일 자정(`dailyAt('00:00')`)에 24시간 지난 미결제 주문을 찾아 일괄 취소하고 묶였던 재고를 자동으로 서고에 복구해 준단다!"  
🐶 **토토**: "멍멍! 이전 작업이 안 끝났는데 다음 작업이 또 돌아 중복 취소되는 대참사를 막으려면 `withoutOverlapping()` 한 줄을 꼭 달아야 안전하다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **미결제 주문 자동 취소 커맨드 제작:** `CancelUnpaidOrdersCommand` (`shop:cancel-unpaid-orders`)
2. **라라벨 11 스케줄 정의:** `routes/console.php`에 스케줄 규칙 등록
3. **스케줄 보호 옵션 적용:**
   - 중복 실행 방지: `withoutOverlapping(60)`
   - 백그라운드 병렬 실행: `runInBackground()`
   - 로그 파일 보관: `appendOutputTo()`
   - 단일 서버 실행: `onOneServer()` (다중 웹서버 환경)
4. **로컬 스케줄러 테스트 및 검증:** `php artisan schedule:list`, `php artisan schedule:work`, `php artisan schedule:test`

---

## 🛠️ 단계별 실습 절차

### 1단계: 24시간 미결제 주문 자동 취소 커맨드 작성

24시간 동안 입금되지 않은 `pending` 상태의 주문을 취소하고 책 재고를 복원하는 커맨드를 생성합니다.

```bash
php artisan make:command CancelUnpaidOrdersCommand
```

`app/Console/Commands/CancelUnpaidOrdersCommand.php`:

```php
<?php

namespace App\Console\Commands;

use App\Models\Order;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class CancelUnpaidOrdersCommand extends Command
{
    protected $signature = 'shop:cancel-unpaid-orders {--hours=24 : 미결제 경과 기준 시간}';
    protected $description = '지정된 시간 동안 결제되지 않은 주문을 자동 취소하고 도서 재고를 복원합니다.';

    public function handle(): int
    {
        $hours = (int) $this->option('hours');
        $cutoffTime = now()->subHours($hours);

        $this->info("{$hours}시간 이상 미결제 상태인 주문 취소 배치를 시작합니다. (기준 시각: {$cutoffTime->toDateTimeString()})");

        // 24시간 지난 pending 주문 조회
        $unpaidOrders = Order::where('status', 'pending')
            ->where('created_at', '<=', $cutoffTime)
            ->with('items.book')
            ->get();

        if ($unpaidOrders->isEmpty()) {
            $this->info('취소 대상 미결제 주문이 없습니다.');
            return self::SUCCESS;
        }

        $cancelledCount = 0;

        foreach ($unpaidOrders as $order) {
            DB::transaction(function () use ($order, &$cancelledCount) {
                // 1. 주문 상세 품목별 재고 복원
                foreach ($order->items as $item) {
                    $item->book->increment('stock', $item->quantity);
                    if ($item->book->is_sold_out && $item->book->stock > 0) {
                        $item->book->update(['is_sold_out' => false]);
                    }
                }

                // 2. 주문 상태를 'cancelled'로 변경
                $order->update([
                    'status' => 'cancelled',
                    'cancelled_at' => now(),
                    'cancel_reason' => '입금 기한(24시간) 만료에 따른 시스템 자동 취소',
                ]);

                $cancelledCount++;
            });

            Log::info("[스케줄러] 미결제 주문 자동 취소 완료: 주문번호 #{$order->order_number}");
        }

        $this->info("총 {$cancelledCount}건의 미결제 주문이 성공적으로 취소되고 재고가 복구되었습니다.");
        return self::SUCCESS;
    }
}
```

---

### 2단계: 라라벨 11 스케줄러 등록 (`routes/console.php`)

라라벨 11에서는 콘솔 스케줄을 `routes/console.php` 파일에 직접 등록합니다!

`routes/console.php`를 열고 다음과 같이 스케줄을 구성합니다:

```php
<?php

use Illuminate\Support\Facades\Schedule;
use App\Console\Commands\CancelUnpaidOrdersCommand;
use App\Models\Book;
use Illuminate\Support\Facades\Log;

/*
|--------------------------------------------------------------------------
| Console Task Scheduling
|--------------------------------------------------------------------------
*/

// 1. 매일 자정(00:00) 24시간 미결제 주문 자동 취소
Schedule::command(CancelUnpaidOrdersCommand::class, ['--hours' => 24])
    ->dailyAt('00:00')
    ->withoutOverlapping(60) // 최대 60분 락
    ->runInBackground()      // 다음 작업 지연 방지
    ->appendOutputTo(storage_path('logs/scheduler-orders.log'))
    ->onSuccess(function () {
        Log::info('[스케줄러] 자정 미결제 주문 취소 배치가 성공적으로 완료되었습니다.');
    })
    ->onFailure(function () {
        Log::critical('[스케줄러 긴급] 자정 미결제 주문 취소 배치가 실패했습니다!');
    });

// 2. 매일 아침 09:00 품절 임박(재고 3권 이하) 도서 점검 인라인 클로저
Schedule::call(function () {
    $lowStockBooks = Book::where('stock', '<=', 3)->where('is_sold_out', false)->get();
    if ($lowStockBooks->isNotEmpty()) {
        Log::warning("[재고 경보] 품절 임박 도서가 {$lowStockBooks->count()}종 있습니다. 발주 검토가 필요합니다.");
    }
})->dailyAt('09:00')->name('check-low-stock-books');

// 3. 매주 월요일 새벽 02:00 주간 베스트셀러 집계 캐시 갱신
Schedule::command('shop:generate-bestsellers')
    ->weeklyOn(1, '02:00')
    ->onOneServer(); // 서버가 여러 대여도 한 대에서만 단독 실행
```

---

### 3단계: 스케줄 목록 및 실시간 실행 검증

등록된 스케줄 목록을 Artisan 명령어로 확인합니다.

```bash
php artisan schedule:list
```

출력 예시:
```text
  00:00  App\Console\Commands\CancelUnpaidOrdersCommand ........... Next Due: 21 hours from now
  09:00  Closure at routes/console.php:28 .......................... Next Due: 6 hours from now
  02:00  Mon shop:generate-bestsellers ............................. Next Due: 3 days from now
```

개발 환경에서 크론처럼 1분마다 스케줄을 감시하며 실행하는 커맨드:

```bash
php artisan schedule:work
```

특정 스케줄 커맨드 강제 즉시 실행 테스트:

```bash
php artisan schedule:test --name="shop:cancel-unpaid-orders"
```

---

### 4단계: 운영 서버(Ubuntu/Linux) 크론 등록

운영 서버에서는 시스템 크론탭에 단 한 줄만 등록하면 끝납니다:

```bash
crontab -e
```

다음 라인을 추가합니다:

```bash
* * * * * cd /home/deploy/jinyshop && php artisan schedule:run >> /dev/null 2>&1
```

> 💡 **스케줄러 동작 원리:**  
> 리눅스 크론은 매 분마다 `schedule:run`을 깨웁니다. 라라벨 스케줄러가 깨어나서 현재 시각(예: 00:00, 월요일 02:00 등)에 일치하는 등록된 작업들만 골라서 실행합니다!

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. 스케줄 실행 빈도 메소드 모음

| 메소드 | 실행 주기 |
| :--- | :--- |
| `->everyMinute()` | 매 1분마다 |
| `->everyFiveMinutes()` | 매 5분마다 |
| `->hourly()` | 매 시간 정각에 |
| `->daily()` | 매일 자정 00:00에 |
| `->dailyAt('13:00')` | 매일 13:00에 |
| `->twiceDaily(1, 13)` | 하루 두 번 (01:00, 13:00) |
| `->weekdays()` | 평일(월~금)에만 |
| `->weekly()` | 매주 일요일 00:00에 |
| `->monthly()` | 매월 1일 00:00에 |
| `->cron('0 0 * * *')` | 표준 5필드 크론 표현식 직접 지정 |

### 2. 유지보수 모드에서의 스케줄러 동작

서버 점검 중(`php artisan down`)일 때 배치 작업이 돌면 안 된다면 기본적으로 스케줄러는 멈춥니다. 만약 점검 중에도 반드시 돌아야 하는 작업이 있다면 `->evenInMaintenanceMode()`를 체이닝하면 됩니다.

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **중복 실행 방지(withoutOverlapping)의 데드락 방지:**  
   `->withoutOverlapping()`만 적어두면 작업이 예기치 않게 강제 종료(SIGKILL)되었을 때 락(Lock) 파일이 영구히 남아 다음 날부터 스케줄이 영원히 돌지 않는 사고가 날 수 있습니다. 반드시 만료 시간(`withoutOverlapping(60)`)을 인자로 지정하세요!
2. **단일 서버 실행(onOneServer)의 필수 조건:**  
   AWS EC2나 오토스케일링 환경에서 서버 5대가 동시에 같은 스케줄을 돌려 5번 중복 취소되는 것을 방지하는 `onOneServer()`는 Redis나 Memcached 같은 **중앙 캐시 드라이버**가 연동되어 있어야 락을 공유할 수 있습니다.

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 여러 대의 웹 서버가 로드밸런서 뒤에 있을 때, 스케줄 작업이 딱 한 대의 서버에서만 실행되도록 보장하는 메소드는 무엇일까요?
   - 정답: `->onOneServer()`
2. **과제:** 매월 마지막 날 23시 59분에 이번 달 최다 서평을 남긴 독자 3명을 선정해 적립금 5,000원을 지급하는 월간 이벤트 스케줄(`monthlyOn(...)`)을 작성해 보세요!
{% endraw %}
