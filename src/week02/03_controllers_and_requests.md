---
layout: docs
title: "03강: 컨트롤러(Controller) 아키텍처 & HTTP 요청(Request) 해부"
---

{% raw %}
# 03강: 컨트롤러(Controller) 아키텍처 & HTTP 요청(Request) 해부

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 리소스 컨트롤러(`BookController`), 단일 액션(`__invoke`), `Request` 객체로부터 도서 검색/필터 데이터 안전 추출  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [컨트롤러 (Controllers)](../docs/04_the_basics/controllers_ko.md), [요청 (Requests)](../docs/04_the_basics/requests_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 라우트 파일(`routes/web.php`)에 함수 클로저로 코드를 계속 짜다 보니까 파일이 수백 줄로 길어지고 너무 복잡해졌어요! 도서 목록을 필터링하고 검색하는 로직은 따로 깔끔하게 분리할 수 없나요?"

🐱 **지니**: "당연하지 도로시! 라우트 파일은 도로의 표지판 역할만 해야 한단다. 실제 서점의 주문을 받고 책을 포장하는 주방장 역할은 바로 **컨트롤러(Controller)**가 담당해야 하지! 라라벨의 **리소스 컨트롤러(Resource Controller)**를 쓰면 단 한 줄의 명령어로 CRUD(생성, 조회, 수정, 삭제) 7대 표준 메서드가 깔끔하게 정돈된 클래스를 만들어 준단다."

🐶 **토토**: "멍멍! 고객이 주소창에 `?category=it&keyword=라라벨&in_stock=1` 처럼 다양한 쿼리스트링을 보내올 때, `$request->input()`, `$request->boolean()`, `$request->filled()` 메서드를 쓰면 안전하게 값을 골라낼 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 아티산 명령어로 도서 관리 전용 리소스 컨트롤러 `BookController`를 생성합니다.
2. 베스트셀러 전용 단일 액션(Invokable) 컨트롤러 `BestSellerController`를 작성합니다.
3. `Request` 객체를 주입받아 도서 검색 키워드, 카테고리 필터, 재고 유무 플래그를 정밀하게 추출하고 검증합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 도서 리소스 컨트롤러 생성

터미널에서 아티산 명령어를 실행하여 7대 CRUD 메서드가 포함된 컨트롤러 뼈대를 생성합니다:

```bash
php artisan make:controller BookController --resource
```

생성된 `app/Http/Controllers/BookController.php` 파일을 확인하면 다음 표준 액션들이 준비되어 있습니다:
- `index()`: 도서 목록 조회 (검색 및 필터링)
- `create()`: 신규 도서 등록 폼 화면
- `store(Request $request)`: 신규 도서 저장 처리
- `show(string $id)`: 특정 도서 상세 정보
- `edit(string $id)`: 도서 정보 수정 폼 화면
- `update(Request $request, string $id)`: 도서 정보 수정 처리
- `destroy(string $id)`: 도서 삭제(소프트 삭제) 처리

---

### [Step 2] `BookController@index`에서 Request 파라미터 정밀 추출

도서 목록 조회 메서드에서 고객이 전달한 검색 조건들을 안전하게 파싱하는 로직을 작성합니다.

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class BookController extends Controller
{
    /**
     * 지니샵 도서 카탈로그 목록 (검색 및 필터)
     */
    public function index(Request $request): JsonResponse
    {
        // 1. 문자열 검색어 추출 (공백 트림 및 없을 경우 기본값 null)
        $keyword = $request->string('keyword')->trim()->value();

        // 2. 카테고리 필터 (존재 여부 확인)
        $category = $request->filled('category') ? $request->input('category') : 'all';

        // 3. 재고 있는 책만 보기 플래그 (true/false 불리언 자동 변환)
        $inStockOnly = $request->boolean('in_stock_only', false);

        // 4. 페이지 번호 (정수형 강제 변환)
        $page = $request->integer('page', 1);

        // 5. 정렬 기준 (인기순, 신간순, 가격순)
        $sort = $request->input('sort', 'popular');

        return response()->json([
            'status' => 'success',
            'filters' => [
                'keyword' => $keyword,
                'category' => $category,
                'in_stock_only' => $inStockOnly,
                'page' => $page,
                'sort' => $sort,
            ],
            'sample_books' => [
                ['id' => 1, 'title' => '라라벨 13 마스터 클래스', 'author' => '지니', 'price' => 32000],
                ['id' => 2, 'title' => '도로시의 모던 PHP 탐험', 'author' => '도로시', 'price' => 28000],
            ],
        ]);
    }

    /**
     * 특정 도서 상세 보기
     */
    public function show(string $id): JsonResponse
    {
        return response()->json([
            'id' => (int) $id,
            'title' => '라라벨 13 마스터 클래스',
            'isbn' => '9788966261234',
            'publisher' => '지니출판사',
            'price' => 32000,
            'description' => '초보자도 쉽게 따라 할 수 있는 14주 핸드온 라라벨 완벽 가이드북',
        ]);
    }
}
```

---

### [Step 3] `routes/web.php`에 리소스 라우트 한 줄 등록

이제 `routes/web.php`에서 수십 줄의 개별 라우트 대신 `Route::resource()` 단 한 줄로 연결합니다!

```php
use App\Http\Controllers\BookController;

Route::resource('books', BookController::class);
```

이 한 줄이 다음 7개의 표준 URL 라우트를 일제히 자동 생성해 줍니다:
```bash
php artisan route:list --path=books
```
| HTTP Method | URI | Controller Action | Route Name |
| :--- | :--- | :--- | :--- |
| GET | `books` | `BookController@index` | `books.index` |
| POST | `books` | `BookController@store` | `books.store` |
| GET | `books/create` | `BookController@create` | `books.create` |
| GET | `books/{book}` | `BookController@show` | `books.show` |
| PUT/PATCH | `books/{book}` | `BookController@update` | `books.update` |
| DELETE | `books/{book}` | `BookController@destroy` | `books.destroy` |
| GET | `books/{book}/edit` | `BookController@edit` | `books.edit` |

---

### [Step 4] 단일 액션(Invokable) 컨트롤러 제작

단 하나의 특별한 목적(예: 주간 베스트셀러 10위 집계)만 수행하는 컨트롤러는 `__invoke` 단일 액션 컨트롤러로 분리하면 코드가 극도로 단순해집니다.

```bash
php artisan make:controller BestSellerController --invokable
```

```php
// app/Http/Controllers/BestSellerController.php
namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class BestSellerController extends Controller
{
    public function __invoke(Request $request): JsonResponse
    {
        return response()->json([
            'title' => '🔥 지니샵 실시간 베스트셀러 TOP 3',
            'ranking' => [
                ['rank' => 1, 'title' => '라라벨 13 마스터 클래스', 'sales_count' => 1520],
                ['rank' => 2, 'title' => '도로시의 객체지향 설계 이야기', 'sales_count' => 980],
                ['rank' => 3, 'title' => '토토와 함께하는 TDD 테스트', 'sales_count' => 840],
            ],
        ]);
    }
}
```

`routes/web.php`에 등록할 때는 메서드 이름 없이 컨트롤러 클래스만 넘기면 됩니다:
```php
use App\Http\Controllers\BestSellerController;

Route::get('/bestsellers', BestSellerController::class)->name('bestsellers');
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `Request` 객체의 타입 캐스팅 헬퍼
- 클라이언트가 폼이나 URL로 전달하는 값은 HTTP 프로토콜 특성상 기본적으로 모두 '문자열(String)'입니다.
- 라라벨 13의 `Request` 객체는 개발자가 번거롭게 `(int) $request->input('page')`나 `filter_var()`를 호출하지 않도록, `integer()`, `float()`, `boolean()`, `string()`, `date()` 등의 자동 타입 변환 헬퍼를 기본 제공합니다.
- 이는 타입 안정성(Type Safety)을 극대화하고 예기치 못한 버그를 사전 예방합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`$request->has('category')` vs `$request->filled('category')` 차이가 뭐예요?**  
>    고객이 주소창에 `?category=` 처럼 빈 값을 보냈을 때, `has()`는 키가 있으니 `true`를 뱉지만, `filled()`는 빈 문자열이 아니어야만 `true`를 뱉는다멍! 검색어 필터링에는 꼭 `filled()`를 써야 안전하다멍!

---

## 💡 6. 3강 자가진단 과제

1. 브라우저에서 `http://127.0.0.1:8000/books?keyword=라라벨&category=programming&in_stock_only=true&page=2` 에 접속하여 컨트롤러가 파라미터들을 올바르게 JSON으로 응답하는지 확인하세요.
2. `http://127.0.0.1:8000/bestsellers`에 접속하여 Invokable 컨트롤러가 단일 액션으로 동작하는 것을 확인하세요.
{% endraw %}
