---
layout: docs
title: "02강: 도서 카드 `<x-book-card>` 컴포넌트 & 블레이드 필수 지시어"
---

{% raw %}
# 02강: 도서 카드 `<x-book-card>` 컴포넌트 & 블레이드 필수 지시어

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** `@props` 도서 카드 컴포넌트, `@forelse` 빈 목록 처리, `@if` 할인율 뱃지, 도서 포맷(종이책/eBook) 분기  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [블레이드 템플릿 (Blade Templates)](../docs/04_the_basics/blade_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 도서 목록 화면이나 베스트셀러 화면, 추천 도서 목록마다 책 표지, 제목, 저자, 가격, '장바구니 담기' 버튼이 있는 네모난 **도서 카드(Book Card)**가 수십 개씩 반복해서 나오잖아요. 이 카드 UI도 독립된 컴포넌트로 만들어서 데이터를 쏙쏙 꽂아 넣을 수 있나요?"

🐱 **지니**: "물론이지 도로시! 라라벨 Blade의 꽃이 바로 **프롭스(Props) 컴포넌트**란다. `<x-book-card :book="$book" />` 처럼 도서 배열이나 모델 하나만 넘겨주면, 카드가 스스로 제목을 출력하고 할인가를 계산해서 빨간 세일 뱃지까지 달아주지! 게다가 책 검색 결과가 0권일 때는 `@forelse` 지시어가 '일치하는 책이 없습니다'라는 안내 화면을 우아하게 띄워준단다!"

🐶 **토토**: "멍멍! 컴포넌트 파일 맨 위에 `@props(['book', 'featured' => false])`를 선언해주면 기본값까지 똑똑하게 챙길 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 도서 표지, ISBN, 포맷(종이책/전자책), 할인율 뱃지를 포함한 `<x-book-card>` 컴포넌트를 작성합니다.
2. `@forelse`와 `@empty` 지시어로 검색 결과가 없을 때의 대체 화면을 구현합니다.
3. `@auth` 지시어로 로그인한 독자에게만 '위시리스트 찜하기' 하트 버튼을 활성화합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 도서 카드 컴포넌트 작성

`resources/views/components/book-card.blade.php` 파일을 생성합니다.

```html
<!-- resources/views/components/book-card.blade.php -->
@props([
    'book',
    'featured' => false
])

<div class="bg-white rounded-xl border {{ $featured ? 'border-indigo-400 shadow-indigo-100 shadow-lg ring-2 ring-indigo-500/20' : 'border-slate-200 shadow-sm' }} overflow-hidden hover:shadow-md hover:-translate-y-1 transition duration-200 flex flex-col justify-between">
    <div>
        <!-- 1. 도서 표지 영역 (상단 뱃지 포함) -->
        <div class="relative bg-slate-100 aspect-[3/4] flex items-center justify-center overflow-hidden">
            <span class="text-5xl">📖</span>

            <!-- 할인 뱃지 (@if 지시어 활용) -->
            @if(isset($book['discount_rate']) && $book['discount_rate'] > 0)
                <span class="absolute top-2 left-2 bg-rose-500 text-white text-xs font-bold px-2 py-0.5 rounded-full shadow">
                    {{ $book['discount_rate'] }}% 할인
                </span>
            @endif

            <!-- 포맷 뱃지 (종이책 vs 전자책) -->
            <span class="absolute top-2 right-2 text-xs font-semibold px-2 py-0.5 rounded {{ $book['format'] === 'ebook' ? 'bg-sky-100 text-sky-700' : 'bg-amber-100 text-amber-800' }}">
                {{ $book['format'] === 'ebook' ? '⚡ eBook' : '📦 종이책' }}
            </span>
        </div>

        <!-- 2. 도서 정보 본문 -->
        <div class="p-4">
            <div class="text-xs text-slate-400 mb-1">ISBN: {{ $book['isbn'] }}</div>
            <h3 class="font-bold text-slate-800 text-base line-clamp-1 hover:text-indigo-600 transition">
                <a href="{{ route('books.show', $book['id']) }}">{{ $book['title'] }}</a>
            </h3>
            <p class="text-xs text-slate-500 mt-1">
                {{ $book['author'] }} 저 · <span class="text-slate-400">{{ $book['publisher'] }}</span>
            </p>

            <!-- 가격 표시 영역 -->
            <div class="mt-3 flex items-baseline space-x-2">
                @if(isset($book['sale_price']))
                    <span class="text-lg font-bold text-rose-600">{{ number_format($book['sale_price']) }}원</span>
                    <span class="text-xs text-slate-400 line-through">{{ number_format($book['price']) }}원</span>
                @else
                    <span class="text-lg font-bold text-slate-900">{{ number_format($book['price']) }}원</span>
                @endif
            </div>
        </div>
    </div>

    <!-- 3. 카드 하단 액션 버튼 -->
    <div class="p-4 pt-0 flex space-x-2">
        <a href="{{ route('books.show', $book['id']) }}" class="flex-1 text-center py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg transition">
            상세 보기
        </a>
        <button class="px-3 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg transition">
            🛒 담기
        </button>
    </div>
</div>
```

---

### [Step 2] 컨트롤러에서 샘플 도서 목록 주입

`BookController@index` 메서드에서 실감 나는 여러 권의 서점 샘플 도서 배열을 뷰로 전달합니다:

```php
// app/Http/Controllers/BookController.php

public function index()
{
    $books = [
        [
            'id' => 1,
            'isbn' => '9788966261234',
            'title' => '라라벨 13 마스터 클래스',
            'author' => '지니 & 도로시',
            'publisher' => '지니출판사',
            'format' => 'paperback',
            'price' => 35000,
            'sale_price' => 31500,
            'discount_rate' => 10,
            'is_bestseller' => true,
        ],
        [
            'id' => 2,
            'isbn' => '9788966265678',
            'title' => '도로시의 모던 PHP 아키텍처',
            'author' => '도로시',
            'publisher' => '지니출판사',
            'format' => 'ebook',
            'price' => 28000,
            'sale_price' => 22400,
            'discount_rate' => 20,
            'is_bestseller' => false,
        ],
        [
            'id' => 3,
            'isbn' => '9788966269999',
            'title' => '토토의 실전 TDD 자동화',
            'author' => '토토',
            'publisher' => '알고리즘하우스',
            'format' => 'paperback',
            'price' => 30000,
            'sale_price' => null,
            'discount_rate' => 0,
            'is_bestseller' => false,
        ],
    ];

    return view('books.index', compact('books'));
}
```

---

### [Step 3] `books/index.blade.php`에서 도서 그리드 렌더링

`resources/views/books/index.blade.php`를 열고 `@forelse`를 이용해 도서 카드들을 그리드 레이아웃으로 배치합니다.

```html
<x-layouts.app>
    <x-slot:title>
        지니샵 — 실시간 전체 도서 카탈로그
    </x-slot:title>

    <x-slot:header>
        <h1 class="text-2xl font-bold text-slate-900">📚 지니샵 전체 도서 목록</h1>
        <p class="text-sm text-slate-500 mt-1">지니와 도로시가 추천하는 이달의 필독 도서입니다.</p>
    </x-slot:header>

    <!-- 4열 반응형 도서 그리드 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        @forelse($books as $book)
            <!-- 컴포넌트 재사용! :featured 속성 조건부 전달 -->
            <x-book-card :book="$book" :featured="$book['is_bestseller']" />
        @empty
            <div class="col-span-full py-16 text-center bg-white rounded-xl border border-dashed border-slate-300">
                <span class="text-4xl">🔍</span>
                <p class="mt-2 text-slate-600 font-medium">검색 조건에 맞는 도서가 없습니다.</p>
                <p class="text-xs text-slate-400 mt-1">다른 검색어나 카테고리를 선택해 보세요.</p>
            </div>
        @endforelse
    </div>
</x-layouts.app>
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `@forelse` 지시어의 우아함
- 순수 PHP에서는 배열이 비어있는지 확인하기 위해 `if (empty($books)) { ... } else { foreach ($books ...) }` 처럼 중첩 코드를 작성해야 했습니다.
- Blade의 `@forelse ... @empty ... @endforelse` 지시어는 단 하나의 구문으로 루프 순회와 빈 상태(Empty State) 예외 처리를 깔끔하게 해결합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`:book="$book"` 앞에 콜론(`:`)은 왜 붙이나요?**  
>    콜론이 없으면 `book="$book"`이라는 글자 그대로 전달되지만, 콜론(`:`)을 붙이면 뒤따라오는 값을 **PHP 표현식/변수**로 평가하여 실제 도서 객체를 넘겨준다멍!

---

## 💡 6. 2강 자가진단 과제

1. `BookController@index`에서 임의로 `$books = [];` 빈 배열을 전달해 보세요.
2. 브라우저에서 `http://127.0.0.1:8000/books`를 새로고침했을 때 `@empty` 블록의 돋보기 아이콘과 '검색 조건에 맞는 도서가 없습니다' 안내 화면이 뜨는지 확인하세요.
{% endraw %}
