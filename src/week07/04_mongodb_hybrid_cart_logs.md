---
layout: docs
title: "04강: NoSQL MongoDB 하이브리드 연동 — 장바구니 클릭스트림 & 로그"
---

{% raw %}
# 04강: NoSQL MongoDB 하이브리드 연동 — 장바구니 클릭스트림 & 로그

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** RDBMS(MySQL)와 NoSQL(MongoDB)의 하이브리드 아키텍처, 비정형 도서 조회 로그 및 장바구니 행동 이력 수집  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [MongoDB (몽고DB 연동)](../docs/07_database/mongodb_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 어떤 책을 몇 초 동안 구경했는지, 어떤 책을 장바구니에 담았다가 다시 뺐는지 같은 행동 로그(Clickstream)를 수집하고 싶어요. 그런데 이런 로그는 하루에도 수백만 건씩 쏟아지고 데이터 형태도 제각각인데, 엄격한 RDBMS 테이블에 다 집어넣으면 DB 용량이 터지지 않을까요?"

🐱 **지니**: "도로시, 바로 그럴 때 최고의 선택이 바로 **하이브리드 데이터베이스 아키텍처**란다! 결제, 주문, 도서 재고처럼 1원의 오차도 없어야 하는 핵심 데이터는 **RDBMS(MySQL/SQLite)**가 맡고, 초당 수천 건씩 발생하는 비정형 행동 로그와 장바구니 클릭 이력은 스키마가 자유로운 **MongoDB(NoSQL)**에 쏙쏙 담는 거지! 라라벨에서는 MongoDB도 Eloquent 문법 그대로 다룰 수 있단다!"

🐶 **토토**: "멍멍! `CartLog::create(['event' => 'item_added', ...])` 처럼 우리가 알던 친숙한 Eloquent 문법으로 몽고DB 문서를 자유자재로 저장할 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨의 다중 데이터베이스 연결(`config/database.php`) 아키텍처를 이해합니다.
2. `mongodb/laravel-mongodb` 패키지를 연동하여 비정형 도서 로그 모델 `CartLog`를 구현합니다.
3. 장바구니 담기 이벤트 발생 시 비정형 메타데이터(IP, 브라우저 환경, 체류 시간, 이전 추천 도서 목록)를 NoSQL에 기록합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `config/database.php`에 MongoDB 연결 구성

`.env` 파일에 몽고DB 접속 정보를 추가합니다:

```ini
# .env
MONGODB_URI="mongodb://127.0.0.1:27017"
MONGODB_DATABASE="jinyshop_logs"
```

`config/database.php`의 `connections` 배열에 몽고DB 드라이버를 등록합니다:

```php
'mongodb' => [
    'driver' => 'mongodb',
    'dsn' => env('MONGODB_URI', 'mongodb://localhost:27017'),
    'database' => env('MONGODB_DATABASE', 'jinyshop_logs'),
],
```

---

### [Step 2] MongoDB 전용 Eloquent 모델 작성

`app/Models/CartLog.php` 모델을 생성합니다. 일반 모델과 달리 MongoDB 전용 기본 클래스를 상속합니다:

```php
namespace App\Models;

use MongoDB\Laravel\Eloquent\Model as MongoModel;

class CartLog extends MongoModel
{
    // 몽고DB 연결 커넥션 지정
    protected $connection = 'mongodb';

    // 몽고DB 컬렉션(테이블) 이름 지정
    protected $collection = 'cart_activity_logs';

    // NoSQL이므로 모든 동적 JSON 속성 저장 허용
    protected $guarded = [];
}
```

---

### [Step 3] 장바구니 담기 시 비정형 행동 로그 기록

`CartService`에 장바구니 담기 시 비정형 메타데이터를 NoSQL에 로깅하는 코드를 추가합니다:

```php
// app/Services/CartService.php 에 로깅 로직 연동
use App\Models\CartLog;

public function add(int $bookId, int $quantity = 1): void
{
    // ... 기존 세션 장바구니 담기 로직 ...

    // NoSQL MongoDB에 비정형 클릭스트림 행동 로그 비동기 기록
    try {
        CartLog::create([
            'event' => 'cart_item_added',
            'book_id' => $bookId,
            'quantity' => $quantity,
            'session_id' => session()->getId(),
            'client_ip' => request()->ip(),
            'user_agent' => request()->userAgent(),
            'metadata' => [
                'referrer' => request()->headers->get('referer'),
                'screen_resolution' => request()->header('sec-ch-ua-platform'),
                'timestamp_utc' => now()->toIso8601String(),
            ],
        ]);
    } catch (\Throwable $e) {
        // 로그 수집 실패가 고객의 쇼핑몰 장바구니 담기를 방해하지 않도록 예외 억제
        \Illuminate\Support\Facades\Log::warning('MongoDB 로그 기록 실패: ' . $e->getMessage());
    }
}
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### RDBMS와 NoSQL의 완벽한 상호보완
- **RDBMS(ACID)**: 데이터 일관성, 복잡한 JOIN, 트랜잭션, 정산 (`orders`, `books`, `users`)
- **NoSQL(MongoDB)**: 스키마 변경이 자유로운 JSON 문서, 수천만 건의 시계열 로그, A/B 테스트 클릭스트림 데이터
- 라라벨은 동일한 Active Record 인터페이스를 유지하면서 두 세계의 장점을 하나의 단일 프로젝트에서 완벽하게 융합해 냅니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **로컬에 MongoDB가 아직 설치되지 않았으면 어떻게 하나요?**  
>    Sail 환경을 쓴다면 `docker-compose.yml`에 `mongo` 컨테이너 한 줄만 추가하면 끝난다멍! 임시 로컬 실습에서는 SQLite 연결을 유지하고 파일 로그(`storage/logs/`)로 대체 테스트할 수도 있다멍!

---

## 💡 6. 4강 자가진단 과제

1. 장바구니 담기 액션이 실행될 때 `CartLog`에 고객의 세션 ID와 책 번호가 JSON 객체 형태로 깔끔하게 꽂히는지 확인하세요.
2. `CartLog::where('event', 'cart_item_added')->count()`로 오늘 서점에서 독자들이 장바구니를 클릭한 총 횟수를 집계해 보세요.
{% endraw %}
