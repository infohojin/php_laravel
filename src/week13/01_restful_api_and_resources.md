---
layout: docs
title: "13주차 01강: 모바일 RESTful API 설계, Eloquent API 리소스 & 직렬화(Serialization)"
---

{% raw %}
# 📖 13주차 01강: 모바일 RESTful API 설계, Eloquent API 리소스 & 직렬화(Serialization)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 모바일 앱(iOS/Android)과 외부 제휴사 연동을 위한 규격화된 RESTful JSON API를 구축하고, Eloquent 모델을 안전하고 우아하게 JSON으로 변환하는 API 리소스(`JsonResource`) 및 직렬화(Serialization)를 마스터합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 모바일 앱 개발팀에서 도서 목록 API를 달라고 해서 컨트롤러에서 `return Book::all();`로 넘겨줬더니, 앱 개발자님이 화를 냈어! DB 컬럼명(`publisher_id`, `created_at` 포맷)이 그대로 노출되고 도서 원가(`cost_price`) 같은 관리자용 대외비 필드까지 앱으로 다 새어 나갔대!"  
🐱 **지니**: "도로시, DB 모델을 API 응답에 날것 그대로 뱉는 건 보안상으로도 위험하고 결합도도 너무 높단다! 바로 그럴 때 라라벨의 **API 리소스(JsonResource)**와 **직렬화(Serialization)** 레이어를 두는 거란다. 데이터베이스 스키마와 클라이언트 JSON 스펙 사이에 완벽한 방화벽을 쳐주는 거지!"  
🐶 **토토**: "멍멍! 책의 저자 목록이나 출판사 정보는 N+1 쿼리 방지를 위해 관계가 미리 로드되었을 때만 JSON에 포함시키는 `$this->whenLoaded('authors')` 문법을 쓰면 성능도 짱이다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **라라벨 11 API 라우트 활성화:** `php artisan install:api` 및 `routes/api.php` 구성
2. **모델 직렬화 제어:** `Book` 모델에 `$hidden` (원가 숨김), `$casts`, `$appends` (가상 속성) 설정
3. **규격화된 단일/컬렉션 리소스 작성:** `BookResource`, `AuthorResource`
4. **조건부 관계 및 속성 포함:** `$this->whenLoaded()`, `$this->when()`
5. **API 버전 관리와 페이지네이션 메타데이터 포맷팅:** `GET /api/v1/books`

---

## 🛠️ 단계별 실습 절차

### 1단계: 라라벨 11 API 스캐폴딩 활성화

라라벨 11에서는 기본적으로 `routes/api.php`가 빠져 있으므로 아래 명령어로 API 패키지와 라우트 파일을 생성합니다:

```bash
php artisan install:api
```

명령어가 완료되면 `routes/api.php` 파일이 생성되고 `bootstrap/app.php`에 API 미들웨어 스택이 자동으로 등록됩니다.

---

### 2단계: 모델 직렬화(Serialization) 제어

`app/Models/Book.php` 모델에 민감 필드를 숨기고 포맷팅된 가상 속성을 추가합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    /**
     * JSON 직렬화 시 자동으로 숨길 민감 속성들
     */
    protected $hidden = [
        'cost_price',      // 도서 원가 (서점 영업 비밀)
        'internal_memo',   // 관리자 전용 내부 메모
        'deleted_at',
    ];

    /**
     * JSON 직렬화 시 자동으로 계산되어 포함될 가상 속성
     */
    protected $appends = [
        'discount_rate_text',
        'is_new_release',
    ];

    /**
     * 가상 속성 접근자: 할인율 텍스트 (예: "15% 할인")
     */
    public function getDiscountRateTextAttribute(): ?string
    {
        if ($this->original_price && $this->price < $this->original_price) {
            $rate = round((($this->original_price - $this->price) / $this->original_price) * 100);
            return "{$rate}% 할인";
        }
        return null;
    }

    /**
     * 가상 속성 접근자: 출간 30일 이내 신간 여부
     */
    public function getIsNewReleaseAttribute(): bool
    {
        return $this->published_at && $this->published_at->gt(now()->subDays(30));
    }
}
```

---

### 3단계: API 리소스(JsonResource) 클래스 생성

API 응답 규격을 정의하는 리소스 클래스들을 생성합니다:

```bash
php artisan make:resource BookResource
php artisan make:resource AuthorResource
```

`app/Http/Resources/AuthorResource.php`:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class AuthorResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'profile_photo_url' => $this->profile_photo_url ? url($this->profile_photo_url) : null,
        ];
    }
}
```

`app/Http/Resources/BookResource.php`:

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class BookResource extends JsonResource
{
    /**
     * 모델 데이터를 JSON 응답 배열로 변환
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'isbn' => $this->isbn,
            'title' => $this->title,
            'summary' => $this->summary,
            'cover_image' => $this->cover_image ? url($this->cover_image) : null,
            'pricing' => [
                'original_price' => (int) $this->original_price,
                'price' => (int) $this->price,
                'discount_badge' => $this->discount_rate_text,
                'currency' => 'KRW',
            ],
            'stock' => [
                'quantity' => (int) $this->stock,
                'is_in_stock' => $this->stock > 0,
            ],
            'flags' => [
                'is_new' => $this->is_new_release,
                'is_bestseller' => (bool) $this->is_bestseller,
            ],
            // 관계가 컨트롤러에서 Eager Loading(with) 되었을 때만 포함
            'authors' => AuthorResource::collection($this->whenLoaded('authors')),
            'publisher' => $this->whenLoaded('publisher', fn () => [
                'id' => $this->publisher->id,
                'name' => $this->publisher->name,
            ]),
            // 관리자 권한이 있는 요청자에게만 조건부로 상세 메트릭 노출
            'admin_metrics' => $this->when($request->user()?->is_admin, [
                'total_sales_count' => (int) $this->sales_count,
                'view_count' => (int) $this->views,
            ]),
            'published_at' => $this->published_at?->format('Y-m-d'),
        ];
    }
}
```

---

### 4단계: RESTful API 컨트롤러 및 라우트 연동

`app/Http/Controllers/Api/v1/BookApiController.php`를 작성합니다:

```php
<?php

namespace App\Http\Controllers\Api\v1;

use App\Http\Controllers\Controller;
use App\Http\Resources\BookResource;
use App\Models\Book;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\AnonymousResourceCollection;

class BookApiController extends Controller
{
    /**
     * 도서 목록 조회 (검색, 카테고리 필터링, 페이지네이션)
     * GET /api/v1/books
     */
    public function index(Request $request): AnonymousResourceCollection
    {
        $books = Book::with(['authors', 'publisher'])
            ->when($request->category_id, fn ($q, $id) => $q->where('category_id', $id))
            ->where('is_sold_out', false)
            ->latest('published_at')
            ->paginate($request->input('per_page', 15));

        return BookResource::collection($books);
    }

    /**
     * 도서 단건 상세 조회
     * GET /api/v1/books/{book}
     */
    public function show(Book $book): BookResource
    {
        $book->load(['authors', 'publisher', 'reviews.user']);

        return new BookResource($book);
    }
}
```

`routes/api.php`에 버전 라우팅을 등록합니다:

```php
use App\Http\Controllers\Api\v1\BookApiController;
use Illuminate\Support\Facades\Route;

Route::prefix('v1')->group(function () {
    Route::get('/books', [BookApiController::class, 'index']);
    Route::get('/books/{book}', [BookApiController::class, 'show']);
});
```

---

### 5단계: API 응답 JSON 테스트

터미널에서 `curl` 명령어로 API 응답을 테스트합니다:

```bash
curl -s http://127.0.0.1:8000/api/v1/books | jq
```

출력 예시 (규격화된 JSON 응답과 페이지네이션 메타):
```json
{
  "data": [
    {
      "id": 1,
      "isbn": "979-11-90000-01-1",
      "title": "라라벨 11 마스터 가이드",
      "summary": "라라벨 기초부터 실전까지...",
      "pricing": {
        "original_price": 38000,
        "price": 34200,
        "discount_badge": "10% 할인",
        "currency": "KRW"
      },
      "stock": {
        "quantity": 25,
        "is_in_stock": true
      },
      "flags": {
        "is_new": true,
        "is_bestseller": true
      },
      "authors": [
        {
          "id": 5,
          "name": "지니 & 도로시",
          "profile_photo_url": "http://127.0.0.1:8000/storage/authors/5.jpg"
        }
      ],
      "published_at": "2026-09-15"
    }
  ],
  "links": {
    "first": "http://127.0.0.1:8000/api/v1/books?page=1",
    "last": "http://127.0.0.1:8000/api/v1/books?page=10",
    "prev": null,
    "next": "http://127.0.0.1:8000/api/v1/books?page=2"
  },
  "meta": {
    "current_page": 1,
    "from": 1,
    "last_page": 10,
    "per_page": 15,
    "to": 15,
    "total": 150
  }
}
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. `whenLoaded()`의 N+1 쿼리 원천 봉쇄

`$this->whenLoaded('relation')`를 사용하면 관계가 이미 메모리에 로드된 경우에만 해당 리소스를 변환합니다. 만약 `$book->authors` 관계가 Eager Loading 되지 않은 채 접근되면 추가 쿼리를 날리지 않고 아예 JSON 키 자체를 생략하므로, 의도치 않은 N+1 쿼리 폭탄을 완벽히 차단합니다!

### 2. 최상위 래핑(Data Wrapping) 제어

기본적으로 라라벨 API 리소스는 응답을 `{"data": [...]}`로 감싸줍니다. 만약 최상위 `data` 키를 제거하고 배열 그대로 내보내고 싶다면 `AppServiceProvider::boot()`에서 다음과 같이 선언합니다:

```php
use Illuminate\Http\Resources\Json\JsonResource;

public function boot(): void
{
    JsonResource::withoutWrapping();
}
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **Eloquent 모델의 날짜 타임존 포맷팅:**  
   `$this->created_at`을 그대로 내보내면 ISO-8601 문자열(`2026-09-25T02:00:00.000000Z`)로 나가게 됩니다. 모바일 앱과 협의하여 `$this->created_at->format('Y-m-d H:i:s')` 또는 타임스탬프(`timestamp`)로 일관성 있게 규격화해야 파싱 에러를 예방할 수 있습니다!
2. **대용량 컬렉션에서의 메모리 절약:**  
   수천 권의 도서 목록을 내보낼 때는 일반 `paginate()` 대신 커서 기반 `cursorPaginate()`를 리소스와 함께 사용하면 DB 오프셋 부하를 획기적으로 줄일 수 있습니다.

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 사용자가 관리자일 때만 특정 필드를 JSON 결과에 동적으로 포함시키기 위해 리소스 내부에서 사용하는 메소드는 무엇일까요?
   - 정답: `$this->when(조건, 값)`
2. **과제:** 독자가 남긴 서평(`ReviewResource`)을 작성하고, 본인이 작성한 서평인 경우에만 `is_mine => true` 플래그를 추가하도록 구현해 보세요!
{% endraw %}
