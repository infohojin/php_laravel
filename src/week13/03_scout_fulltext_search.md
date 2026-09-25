---
layout: docs
title: "13주차 03강: 라라벨 스카우트(Scout) 전문 검색(Full-text Search) & 폴리오(Folio) 기획전 라우팅"
---

{% raw %}
# 📖 13주차 03강: 라라벨 스카우트(Scout) 전문 검색(Full-text Search) & 폴리오(Folio) 기획전 라우팅

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 50만 권의 도서 데이터베이스에서 10ms 초고속 검색을 구현하기 위해 라라벨 스카우트(Scout)와 전문 검색 인덱스를 구축하고, Laravel Folio를 활용해 특별 북페어 프로모션 페이지를 파일 기반으로 초고속 런칭합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리 지니샵에 등록된 책이 50만 권을 넘어가니까 검색창에 `LIKE '%라라벨%'`로 검색하면 화면이 3초 동안 멈춰 있어! DB가 풀 테이블 스캔을 하느라 서버가 헉헉거리고 있어!"  
🐱 **지니**: "도로시, 수십만 건 이상의 검색에는 단순 `LIKE` 대신 역색인(Inverted Index) 기반의 **전문 검색(Full-text Search)**과 **라라벨 스카우트(Laravel Scout)**를 써야 한단다! 모델에 `Searchable` 트레이트 하나만 달아두면, 책이 등록/수정/삭제될 때마다 검색 인덱스가 자동으로 실시간 동기화되지!"  
🐶 **토토**: "멍멍! 다음 주에 열리는 '2026 봄맞이 북페어' 프로모션 랜딩 페이지는 컨트롤러 없이 블레이드 파일 하나만 똑 떨어뜨려도 주소가 열리는 **라라벨 폴리오(Laravel Folio)**로 번개처럼 만들어보자멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **라라벨 스카우트 설치:** `composer require laravel/scout` 및 설정 파일 발행
2. **도서 모델에 `Searchable` 트레이트 적용:** 제목, 저자, 출판사, 키워드를 결합한 `toSearchableArray()`
3. **스카우트 인덱싱 배치:** `php artisan scout:import "App\Models\Book"`
4. **고속 검색 실행:** `Book::search($keyword)->paginate(20)`
5. **Laravel Folio 파일 기반 라우팅:** `resources/views/pages/events/spring-bookfair.blade.php` 기획전 페이지 제작

---

## 🛠️ 단계별 실습 절차

### 1단계: Laravel Scout 패키지 설치

터미널에서 Scout를 설치하고 설정 파일을 발행합니다:

```bash
composer require laravel/scout
php artisan vendor:publish --provider="Laravel\Scout\ScoutServiceProvider"
```

`.env`에서 검색 드라이버를 지정합니다. 개발 환경에서는 MySQL/PostgreSQL의 내장 풀텍스트 인덱스를 활용하는 `database` 드라이버를, 대규모 운영 환경에서는 초고속 Rust 기반 검색 엔진인 `meilisearch`를 선택할 수 있습니다:

```env
SCOUT_DRIVER=database
# Meilisearch 사용 시:
# SCOUT_DRIVER=meilisearch
# MEILISEARCH_HOST=http://127.0.0.1:7700
# MEILISEARCH_KEY=masterKey
```

---

### 2단계: 도서 모델에 `Searchable` 트레이트 및 색인 범위 커스텀

`app/Models/Book.php`에 `Searchable` 트레이트를 추가하고, 검색 대상 필드들을 규정합니다:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Laravel\Scout\Searchable;

class Book extends Model
{
    use Searchable;

    /**
     * 검색 엔진에 색인(Index)할 데이터 배열 정의
     */
    public function toSearchableArray(): array
    {
        // 저자 및 출판사 정보 사전 로드
        $this->loadMissing(['authors', 'publisher']);

        return [
            'id' => (int) $this->id,
            'title' => $this->title,
            'subtitle' => $this->subtitle,
            'isbn' => $this->isbn,
            'summary' => $this->summary,
            'description' => strip_tags($this->description), // HTML 태그 제거
            'authors' => $this->authors->pluck('name')->implode(', '),
            'publisher' => $this->publisher?->name,
            'price' => (int) $this->price,
            'is_sold_out' => (bool) $this->is_sold_out,
            'published_year' => (int) $this->published_at?->year,
        ];
    }

    /**
     * 특정 조건의 도서만 검색 엔진에 등록 (예: 비공개 도서는 색인 제외)
     */
    public function shouldBeSearchable(): bool
    {
        return $this->is_active === true;
    }
}
```

---

### 3단계: 기존 도서 데이터 대량 색인(Import)

데이터베이스에 이미 등록되어 있는 수만 권의 도서를 검색 인덱스에 한 번에 집어넣습니다:

```bash
php artisan scout:import "App\Models\Book"
```

진행률이 터미널에 시각적으로 표시되며 모든 도서의 검색 색인이 생성됩니다.

> 🐶 **토토의 팁!**  
> "책을 새로 등록하거나 제목을 수정하면 라라벨 Eloquent 이벤트가 발동하여 스카우트가 알아서 백그라운드 큐로 인덱스를 최신 상태로 유지해 준다멍!"

---

### 4단계: 실시간 도서 검색 컨트롤러 및 뷰 구현

`app/Http/Controllers/BookSearchController.php`:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Book;
use Illuminate\Http\Request;

class BookSearchController extends Controller
{
    public function index(Request $request)
    {
        $query = $request->input('q', '');

        // Scout 고속 검색 실행
        $books = Book::search($query)
            ->where('is_sold_out', false) // 필터링 조건 체이닝
            ->paginate(12)
            ->withQueryString();

        return view('books.search', [
            'books' => $books,
            'query' => $query,
        ]);
    }
}
```

`resources/views/books/search.blade.php`:

```blade
@extends('layouts.app')

@section('content')
<div class="max-w-6xl mx-auto px-4 py-8">
    <h1 class="text-3xl font-extrabold mb-6">🔍 도서 검색 결과: "{{ $query }}"</h1>

    @if($books->isEmpty())
        <div class="text-center py-16 bg-white rounded-lg shadow">
            <p class="text-gray-500 text-lg">"{{ $query }}"에 일치하는 도서를 찾을 수 없습니다.</p>
            <p class="text-sm text-gray-400 mt-2">철자나 띄어쓰기를 확인하거나 다른 키워드로 검색해 보세요.</p>
        </div>
    @else
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            @foreach($books as $book)
                <x-book-card :book="$book" />
            @endforeach
        </div>

        <div class="mt-8">
            {{ $books->links() }}
        </div>
    @endif
</div>
@endsection
```

---

### 5단계: 라라벨 폴리오(Folio)를 이용한 이벤트 기획전 고속 서빙

기획전이나 프로모션 랜딩 페이지처럼 컨트롤러를 만들 필요 없이 파일 경로 자체가 URL이 되는 Laravel Folio를 연동합니다:

```bash
composer require laravel/folio
php artisan folio:install
```

`resources/views/pages/events/spring-bookfair.blade.php` 파일을 생성합니다:

```blade
<?php

use function Laravel\Folio\name;
use App\Models\Book;

name('events.spring-bookfair');

// Folio 인라인 데이터 쿼리
$featuredBooks = Book::where('is_bestseller', true)->take(6)->get();

?>

@extends('layouts.app')

@section('content')
<div class="bg-gradient-to-r from-pink-50 to-rose-100 py-12 px-6">
    <div class="max-w-5xl mx-auto text-center">
        <span class="text-rose-600 font-bold uppercase tracking-wider">Special Promotion</span>
        <h1 class="text-4xl font-black text-gray-900 mt-2">🌸 2026 지니샵 봄맞이 북페어</h1>
        <p class="mt-4 text-lg text-gray-600">지친 일상에 봄바람을 불어넣어 줄 베스트셀러 도서 특별 할인전</p>
    </div>
</div>

<div class="max-w-6xl mx-auto px-4 py-12">
    <h2 class="text-2xl font-bold mb-6">🌿 북페어 특별 추천 도서</h2>
    <div class="grid grid-cols-2 md:grid-cols-3 gap-6">
        @foreach($featuredBooks as $book)
            <x-book-card :book="$book" />
        @endforeach
    </div>
</div>
@endsection
```

웹 브라우저에서 `http://127.0.0.1:8000/events/spring-bookfair`로 바로 접속하면, 컨트롤러나 `routes/web.php`에 아무것도 추가하지 않았는데도 즉시 기획전 페이지가 아름답게 렌더링됩니다!

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. Scout의 비동기 큐 동기화 (`SCOUT_QUEUE=true`)

도서 정보가 수정될 때마다 외부 검색 엔진(Meilisearch 등)에 HTTP 요청을 동기적으로 보내면 사용자의 저장 버튼 응답이 둔해집니다. `.env`에 `SCOUT_QUEUE=true`를 선언하면, 모든 색인 작업이 자동으로 비동기 큐로 넘어가 사용자 응답 속도가 0.05초로 유지됩니다!

### 2. 하이라이팅(Highlighting) 지원

Meilisearch 드라이버를 사용할 경우, 검색된 단어 주변에 `<mark>` 태그를 자동으로 둘러주는 하이라이트 기능을 지원합니다:

```php
$results = Book::search('라라벨')->raw();
// $results['hits'][0]['_formatted']['summary'] => "최신 <mark>라라벨</mark> 11 프레임워크..."
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **데이터베이스 풀텍스트 인덱스 누락:**  
   `database` 드라이버를 쓸 때는 마이그레이션에서 `$table->fullText(['title', 'summary']);` 인덱스를 걸어주어야만 에러 없이 고속 검색이 작동합니다!
2. **색인 데이터 초기화 및 재색인:**  
   도서 모델의 `toSearchableArray()` 구조를 변경했다면 반드시 기존 색인을 날리고 다시 생성해야 합니다:
   ```bash
   php artisan scout:flush "App\Models\Book"
   php artisan scout:import "App\Models\Book"
   ```

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 라라벨 모델을 Scout 검색 대상으로 지정하기 위해 모델 클래스에 선언해야 하는 트레이트는 무엇일까요?
   - 정답: `use Laravel\Scout\Searchable;`
2. **과제:** 책의 카테고리(`category_id`)와 최소 가격/최대 가격 범위 필터링을 Scout 검색 쿼리에 함께 적용하는 다면 검색(Faceted Search) 컨트롤러를 작성해 보세요!
{% endraw %}
