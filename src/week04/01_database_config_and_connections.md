---
layout: docs
title: "01강: 라라벨 데이터베이스 연결 & 트랜잭션(ACID)의 원리"
---

{% raw %}
# 01강: 라라벨 데이터베이스 연결 & 트랜잭션(ACID)의 원리

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** SQLite / MySQL 연결 구성, 원시 SQL 질의, `DB::transaction()`을 이용한 도서 결제/재고 원자성 보장  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [데이터베이스 시작하기 (Database)](../docs/07_database/database_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 책을 주문하고 결제를 마쳤을 때, `orders` 테이블에 주문 기록은 들어갔는데 갑자기 서버가 꺼져서 `books` 테이블의 재고 수량이 안 줄어들면 어떻게 해요? 반대로 재고는 깎였는데 결제 승인 기록이 사라지면 큰일 나잖아요!"

🐱 **지니**: "도로시, 바로 그것이 모든 금융과 이커머스 시스템의 핵심인 **트랜잭션(Transaction)과 ACID 원칙**이란다! '모두 성공하든지, 아니면 아예 없었던 일로 되돌리든지(All or Nothing)'를 보장해야 하지. 라라벨의 `DB::transaction()` 클로저를 감싸주면, 도서 결제나 재고 차감 도중 1비트의 에러라도 발생할 경우 라라벨이 자동으로 모든 작업을 0.001초 만에 롤백(Rollback)해 준단다!"

🐶 **토토**: "멍멍! 로컬 개발할 땐 복잡한 MySQL 설치 없이 파일 하나짜리 SQLite를 쓰면 가볍고 빠르다멍! `database/database.sqlite` 파일 하나면 준비 끝이다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. `.env` 파일에서 SQLite 및 MySQL 데이터베이스 연결 설정을 이해합니다.
2. `DB::select()`, `DB::insert()` 등 기본 라라벨 쿼리 실행 방식을 익힙니다.
3. 도서 주문 및 재고 차감 과정에서 데이터 정합성을 지켜주는 `DB::transaction()`을 실습합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 데이터베이스 드라이버 설정 (`.env`)

로컬 개발 환경에서는 별도 DB 서버 설치가 필요 없는 초경량 **SQLite**를 사용합니다:

```ini
# .env
DB_CONNECTION=sqlite
# SQLite의 경우 DB_HOST, DB_PORT 등은 주석 처리해도 무방합니다.
```

`database/database.sqlite` 파일이 없다면 생성해 줍니다:
```bash
touch database/database.sqlite
```

---

### [Step 2] 데이터베이스 연결 테스트

터미널에서 아티산 명령어로 DB 연결 상태를 즉시 점검합니다:

```bash
php artisan db:show
```

> **터미널 출력 예시:**
> ```text
>   SQLite 3.x.x .............................................................. 0.05MB
>   Database ........................... /path/to/jinyshop/database/database.sqlite
>   Tables ....................................................................... 0
> ```

---

### [Step 3] `DB::transaction()` 원자성(ACID) 실습

`routes/web.php`에 도서 주문 및 재고 차감을 시뮬레이션하는 테스트 엔드포인트를 만듭니다:

```php
// routes/web.php
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Route;

Route::get('/test-order-transaction', function () {
    try {
        // DB::transaction 은 클로저 내부에서 예외가 던져지면 자동 롤백합니다!
        DB::transaction(function () {
            // 1. 고객 주문 생성 (임시 테이블 가정)
            DB::statement('CREATE TABLE IF NOT EXISTS test_orders (id INTEGER PRIMARY KEY, book_title TEXT, amount INTEGER)');
            DB::insert('INSERT INTO test_orders (book_title, amount) VALUES (?, ?)', ['라라벨 13 마스터 클래스', 35000]);

            // 2. 재고 차감 시뮬레이션 중 고의로 에러 발생 (재고 부족!)
            $stockLeft = 0;
            if ($stockLeft <= 0) {
                throw new \Exception('재고가 부족하여 주문을 완료할 수 없습니다!');
            }
        });

        return "주문 성공!";
    } catch (\Throwable $e) {
        // 트랜잭션 롤백으로 인해 test_orders 테이블에 방금 넣었던 레코드는 자동 취소됩니다!
        return response()->json([
            'status' => 'rollback_success',
            'error_message' => $e->getMessage(),
            'order_count' => DB::select('SELECT COUNT(*) as count FROM test_orders')[0]->count ?? 0,
        ], 400);
    }
});
```

브라우저에서 `http://127.0.0.1:8000/test-order-transaction`을 호출합니다:
```json
{
  "status": "rollback_success",
  "error_message": "재고가 부족하여 주문을 완료할 수 없습니다!",
  "order_count": 0
}
```
> **지니의 관찰:** 고의로 에러를 던졌을 때, `test_orders`에 먼저 삽입되었던 주문 레코드가 흔적도 없이 롤백되어 `order_count: 0`으로 유지되는 것을 확인할 수 있습니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 데드락(Deadlock) 자동 재시도
- 수백 명의 독자가 한정판 책 1권을 동시에 구매하려고 몰리면 데이터베이스 행 락(Row Lock) 경합으로 인해 **데드락(Deadlock)**이 발생할 수 있습니다.
- 라라벨의 `DB::transaction($callback, 5)` 처럼 두 번째 인자에 재시도 횟수를 지정하면, 데드락이 발생했을 때 라라벨이 최대 5회까지 트랜잭션을 자동으로 재실행해 줍니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`Database file does not exist` 에러가 나요!**  
>    SQLite 파일(`database/database.sqlite`)이 생성되지 않았기 때문이라멍! `touch database/database.sqlite`를 실행하고 다시 시도하라멍!

---

## 💡 6. 1강 자가진단 과제

1. `php artisan db:table users` 명령어로 기본 생성된 `users` 테이블 구조를 확인해 보세요.
2. `DB::transaction()`의 재시도 횟수 옵션을 확인하고 공식 문서의 데드락 핸들링 예제를 읽어보세요.
{% endraw %}
