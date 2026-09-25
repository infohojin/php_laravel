---
layout: docs
title: "14주차 01강: 단위 & 기능 테스트(Pest/PHPUnit), 데이터베이스 테스트 & 모킹(Mocking)"
---

{% raw %}
# 📖 14주차 01강: 단위 & 기능 테스트(Pest/PHPUnit), 데이터베이스 테스트 & 모킹(Mocking)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 지니샵의 핵심 비즈니스 로직(장바구니 담기, 주문 결제, 재고 차감)을 보장하는 단위/기능 테스트를 작성하고, `RefreshDatabase`를 통한 격리된 인메모리 SQLite 테스트와 `Http::fake()`, `Mail::fake()` 모킹(Mocking) 기법을 마스터합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리가 14주 동안 열심히 만든 지니샵을 드디어 세상에 런칭하는데 너무 무서워! 혹시 고객이 결제할 때 재고가 잘못 깎이거나 결제는 됐는데 주문서가 안 만들어지는 버그가 숨어있으면 어떡해? 매번 손으로 브라우저 켜서 테스트하는 건 한계가 있어!"  
🐱 **지니**: "도로시, 프로 개발자가 두려움 없이 밤에 두 발 뻗고 잘 수 있는 유일한 비결은 바로 **자동화 테스트(Automated Testing)**란다! 테스트 코드 한 번 작성해두면 `php artisan test` 단 1초 만에 100가지 결제 예외 상황을 싹 검사하고 영롱한 초록색 불(Pass)을 띄워주지!"  
🐶 **토토**: "멍멍! 외부 결제 대행사(PG)나 이메일 발송은 돈이 나가거나 시간이 걸리니까 가짜 객체로 대체하는 **모킹(`Http::fake()`, `Mail::fake()`)**을 쓰면 초고속으로 테스트를 돌릴 수 있다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **테스트 환경 구성:** `phpunit.xml` 인메모리 SQLite DB 격리 설정
2. **`RefreshDatabase` 기반 데이터베이스 테스트:** 팩토리(`Book::factory()`)를 이용한 도서 모델 및 할인율 검증
3. **HTTP 기능 테스트(Feature Tests):** `POST /cart` 및 `POST /checkout` 결제 플로우 검증
4. **아티산 콘솔 테스트:** `CancelUnpaidOrdersCommand` 자정 배치 커맨드 실행 검증
5. **모킹(Mocking):** `Http::fake()`로 외부 토스페이먼츠 승인 모의 및 `Event::fake()`, `Mail::fake()` 검증

---

## 🛠️ 단계별 실습 절차

### 1단계: 테스트 환경 설정 (`phpunit.xml`)

루트 디렉토리의 `phpunit.xml` 파일에서 테스트 전용 인메모리 SQLite 데이터베이스 환경 변수를 활성화합니다:

```xml
<php>
    <env name="APP_ENV" value="testing"/>
    <env name="APP_MAINTENANCE_DRIVER" value="file"/>
    <env name="BCRYPT_ROUNDS" value="4"/>
    <env name="CACHE_STORE" value="array"/>
    <env name="DB_CONNECTION" value="sqlite"/>
    <env name="DB_DATABASE" value=":memory:"/>
    <env name="MAIL_MAILER" value="array"/>
    <env name="QUEUE_CONNECTION" value="sync"/>
    <env name="SESSION_DRIVER" value="array"/>
</php>
```

> 💡 **인메모리 SQLite의 위력:**  
> 디스크 I/O 없이 컴퓨터 RAM 메모리 위에서 임시 DB가 생성되었다가 테스트가 끝나면 즉시 휘발되므로, 수백 개의 DB 테스트도 2~3초 만에 번개처럼 통과합니다!

---

### 2단계: 도서 모델 단위 테스트 (Unit Test)

도서의 할인율 계산과 품절 로직을 검증하는 단위 테스트를 생성합니다:

```bash
php artisan make:test BookTest --unit
```

`tests/Unit/BookTest.php`:

```php
<?php

namespace Tests\Unit;

use App\Models\Book;
use PHPUnit\Framework\TestCase;

class BookTest extends TestCase
{
    /**
     * 정상 가격과 판매 가격이 주어졌을 때 할인율 텍스트가 정확히 계산되는지 검증
     */
    public function test_it_calculates_discount_rate_correctly(): void
    {
        $book = new Book([
            'title' => '라라벨 11 실전 마스터',
            'original_price' => 40000,
            'price' => 36000, // 10% 할인
        ]);

        $this->assertEquals('10% 할인', $book->discount_rate_text);
    }

    /**
     * 할인 없이 정가 그대로 판매할 경우 할인율 배지가 null인지 검증
     */
    public function test_it_returns_null_discount_badge_when_no_discount(): void
    {
        $book = new Book([
            'title' => '정가 도서',
            'original_price' => 20000,
            'price' => 20000,
        ]);

        $this->assertNull($book->discount_rate_text);
    }
}
```

---

### 3단계: 장바구니 & 주문 결제 기능 테스트 (Feature Test)

실제 사용자 로그인, 장바구니 담기, 결제 승인, DB 재고 차감까지 일련의 시나리오를 검증하는 Feature Test를 생성합니다:

```bash
php artisan make:test CheckoutFeatureTest
```

`tests/Feature/CheckoutFeatureTest.php`:

```php
<?php

namespace Tests\Feature;

use App\Events\OrderPlaced;
use App\Models\Book;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Http;
use Tests\TestCase;

class CheckoutFeatureTest extends TestCase
{
    use RefreshDatabase; // 매 테스트마다 DB 테이블 자동 생성 및 초기화

    public function test_authenticated_user_can_checkout_books_successfully(): void
    {
        // 1. 이벤트 디스패치 모킹 (실제 큐/메일 발송 방지)
        Event::fake([OrderPlaced::class]);

        // 2. 외부 토스페이먼츠 PG사 결제 승인 API 모킹
        Http::fake([
            'https://api.tosspayments.com/v1/payments/confirm' => Http::response([
                'status' => 'DONE',
                'paymentKey' => 'mock_payment_key_12345',
                'orderId' => 'ORD-TEST-001',
                'totalAmount' => 35000,
            ], 200),
        ]);

        // 3. 테스트 데이터 생성 (독자 1명, 도서 1권 - 재고 10권)
        $user = User::factory()->create();
        $book = Book::factory()->create([
            'title' => '라라벨 아키텍처',
            'price' => 35000,
            'stock' => 10,
            'is_sold_out' => false,
        ]);

        // 4. 회원 로그인 상태로 결제 요청 전송
        $response = $this->actingAs($user)->post('/checkout/process', [
            'book_id' => $book->id,
            'quantity' => 2,
            'shipping_address' => '서울시 강남구 테헤란로 123',
            'payment_key' => 'mock_payment_key_12345',
        ]);

        // 5. HTTP 응답 검증 (주문 완료 페이지로 리다이렉트)
        $response->assertStatus(302);
        $response->assertSessionHas('status', '도서 주문이 성공적으로 완료되었습니다!');

        // 6. 데이터베이스 반영 검증
        // 도서 재고가 10권 -> 8권으로 차감되었는지 검증
        $this->assertDatabaseHas('books', [
            'id' => $book->id,
            'stock' => 8,
        ]);

        // 주문 테이블에 해당 유저의 주문 레코드가 생성되었는지 검증
        $this->assertDatabaseHas('orders', [
            'user_id' => $user->id,
            'total_amount' => 70000,
            'status' => 'paid',
        ]);

        // 7. OrderPlaced 도메인 이벤트가 정확히 1번 발행되었는지 검증
        Event::assertDispatched(OrderPlaced::class);
    }

    public function test_checkout_fails_when_book_is_out_of_stock(): void
    {
        $user = User::factory()->create();
        $soldOutBook = Book::factory()->create([
            'stock' => 0,
            'is_sold_out' => true,
        ]);

        $response = $this->actingAs($user)->post('/checkout/process', [
            'book_id' => $soldOutBook->id,
            'quantity' => 1,
        ]);

        // 품절 도서 주문 시 422 또는 세션 에러 검증
        $response->assertSessionHasErrors(['book_id']);
    }
}
```

---

### 4단계: 아티산 콘솔 명령어 테스트 (Console Test)

12주차에서 작성한 `shop:cancel-unpaid-orders` 스케줄러 커맨드의 동작을 검증합니다:

```bash
php artisan make:test CancelUnpaidOrdersCommandTest
```

`tests/Feature/CancelUnpaidOrdersCommandTest.php`:

```php
<?php

namespace Tests\Feature;

use App\Models\Book;
use App\Models\Order;
use App\Models\OrderItem;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class CancelUnpaidOrdersCommandTest extends TestCase
{
    use RefreshDatabase;

    public function test_it_cancels_orders_older_than_24_hours_and_restores_stock(): void
    {
        $book = Book::factory()->create(['stock' => 5]);

        // 25시간 전에 생성된 미결제 주문 생성
        $expiredOrder = Order::factory()->create([
            'status' => 'pending',
            'created_at' => now()->subHours(25),
        ]);

        OrderItem::create([
            'order_id' => $expiredOrder->id,
            'book_id' => $book->id,
            'quantity' => 2,
            'unit_price' => 20000,
        ]);

        // 콘솔 명령어 실행 및 터미널 출력/상태코드 검증
        $this->artisan('shop:cancel-unpaid-orders', ['--hours' => 24])
            ->expectsOutputToContain('미결제 상태인 주문 취소 배치를 시작합니다')
            ->expectsOutputToContain('1건의 미결제 주문이 성공적으로 취소되고 재고가 복구되었습니다')
            ->assertSuccessful();

        // 주문 상태가 cancelled로 변경되었는지 검증
        $this->assertDatabaseHas('orders', [
            'id' => $expiredOrder->id,
            'status' => 'cancelled',
        ]);

        // 도서 재고가 다시 5 + 2 = 7권으로 복원되었는지 검증
        $this->assertEquals(7, $book->fresh()->stock);
    }
}
```

---

### 5단계: 전체 테스트 실행 및 리포트 확인

터미널에서 전체 테스트 스위트를 구동합니다:

```bash
php artisan test
```

출력 예시:
```text
   PASS  Tests\Unit\BookTest
  ✓ it calculates discount rate correctly                                0.02s  
  ✓ it returns null discount badge when no discount                      0.01s  

   PASS  Tests\Feature\CheckoutFeatureTest
  ✓ authenticated user can checkout books successfully                   0.12s  
  ✓ checkout fails when book is out of stock                             0.04s  

   PASS  Tests\Feature\CancelUnpaidOrdersCommandTest
  ✓ it cancels orders older than 24 hours and restores stock             0.05s  

  Tests:    5 passed (14 assertions)
  Duration: 0.35s
```

단 0.35초 만에 지니샵의 결제, 재고, 콘솔 배치가 100% 무결함을 증명했습니다!

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. 다양한 파사드 Fake 모킹 기법

라라벨은 외부 의존성을 격리하기 위한 일관된 `.fake()` 정적 API를 제공합니다:

```php
Mail::fake();      // 실제 메일 발송 차단 -> Mail::assertQueued(OrderReceiptMail::class);
Queue::fake();     // 실제 큐 워커 실행 차단 -> Queue::assertPushed(ProcessBookWatermarkJob::class);
Notification::fake(); // 알림 발송 차단 -> Notification::assertSentTo($user, OrderShippedNotification::class);
Storage::fake('public'); // 실제 로컬 디스크 파일 생성 차단 (메모리 가상 디스크 사용)
```

### 2. Time Traveling (시간 여행 테스트)

"24시간 후 미결제 취소"와 같은 시간 종속적 로직을 테스트하기 위해 라라벨은 시간을 워프시키는 헬퍼를 기본 제공합니다:

```php
$this->travel(25)->hours(); // 현재 시각을 미래 25시간 뒤로 이동!
// 이 상태에서 테스트 수행
$this->travelBack(); // 원래 시간으로 복귀
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **`RefreshDatabase` 사용 시 로컬 DB 날아감 주의:**  
   `phpunit.xml`에 `<env name="DB_CONNECTION" value="sqlite"/>` 설정이 누락되어 있으면, 로컬 개발용 MySQL 데이터베이스의 모든 실데이터가 `migrate:fresh`로 싹 지워지는 끔찍한 사고가 날 수 있습니다. 테스트 실행 전 반드시 테스트 전용 DB 환경 변수를 확인하세요!
2. **`dump()` 대신 `assertSessionHasErrors()` 활용:**  
   테스트가 실패했을 때 `$response->dump()`를 찍어보면 뷰나 에러 메시지를 터미널에 출력해 주어 어디서 검증이 틀렸는지 즉시 파악할 수 있습니다.

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 라라벨 테스트에서 외부 HTTP API 요청을 가로채서 내가 정의한 가짜 응답을 반환하도록 만드는 메소드는 무엇일까요?
   - 정답: `Http::fake([...])`
2. **과제:** 책에 별점과 서평을 등록하는 `POST /books/{book}/reviews` 엔드포인트에 대해, 별점이 1~5점 범위를 벗어났을 때 422 유효성 검사 에러가 발생하는지 검증하는 Feature Test를 작성해 보세요!
{% endraw %}
