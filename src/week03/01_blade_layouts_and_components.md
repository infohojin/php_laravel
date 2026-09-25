---
layout: docs
title: "01강: 마스터 레이아웃 `<x-layouts.app>` & 슬롯(Slot) 아키텍처"
---

{% raw %}
# 01강: 마스터 레이아웃 `<x-layouts.app>` & 슬롯(Slot) 아키텍처

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 컴포넌트 기반 Blade 마스터 레이아웃 구축, 헤더/푸터 모듈화, 기본 및 명명된 슬롯(Named Slots)  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [뷰 (Views)](../docs/04_the_basics/views_ko.md), [블레이드 템플릿 (Blade Templates)](../docs/04_the_basics/blade_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리 지니샵 화면을 만들 때, 상단 내비게이션 바(로고, 검색창, 장바구니 아이콘)랑 하단 푸터(회사 정보, 저작권)를 모든 페이지마다 복사해서 붙여넣어야 해요? 만약 로고를 바꾸거나 카테고리 메뉴를 수정해야 하면 수십 개 HTML 파일을 다 열어야 하잖아요!"

🐱 **지니**: "후후, 도로시! 과거 20년 전 웹 개발자들이 하던 고생을 그대로 짚었구나! 라라벨의 **Blade 템플릿 엔진**에는 화면을 레고 블록처럼 조립할 수 있는 **컴포넌트(Component)와 슬롯(Slot)** 시스템이 있단다. `<x-layouts.app>`이라는 마스터 틀 하나만 만들어두고, 각 페이지는 `$slot`이라는 빈 구멍에 자기 내용만 쏙 채워 넣으면 끝이지! 레이아웃을 고치면 서점의 수백 개 페이지가 1초 만에 일제히 바뀐단다."

🐶 **토토**: "멍멍! 구식 라라벨에서 쓰던 `@extends('layouts.app')`과 `@section('content')` 방식보다, 최신 `<x-layouts.app>` 컴포넌트 태그 방식이 훨씬 직관적이고 HTML5 표준 태그처럼 예쁘다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 지니샵 도서 쇼핑몰 전체가 공유할 반응형 마스터 레이아웃 컴포넌트를 작성합니다.
2. 기본 슬롯(`$slot`)과 명명된 슬롯(`$title`, `$header`)의 차이와 사용법을 익힙니다.
3. 컴포넌트 분리를 통해 상단 헤더 내비게이션 바와 하단 푸터를 독립 모듈로 분할합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 마스터 레이아웃 파일 생성

`resources/views/components/layouts/app.blade.php` 파일을 생성합니다.

```html
<!-- resources/views/components/layouts/app.blade.php -->
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? '지니샵 — 당신 곁의 온라인 서점' }}</title>
    <!-- Tailwind CSS CDN (3강에서 Vite 빌드로 교체 예정) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@400;600;700&display=swap');
        body { font-family: 'Pretendard', sans-serif; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 flex flex-col min-h-screen">

    <!-- 1. 서점 상단 글로벌 헤더 -->
    <header class="bg-indigo-900 text-white shadow-md sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-6">
                <a href="{{ route('home') }}" class="text-2xl font-bold tracking-tight flex items-center space-x-2">
                    <span>🐱</span>
                    <span>JinyShop</span>
                </a>
                <nav class="hidden md:flex space-x-4 text-sm font-medium">
                    <a href="{{ route('books.index') }}" class="hover:text-indigo-200 transition">전체 도서</a>
                    <a href="{{ route('books.bestsellers') }}" class="hover:text-indigo-200 transition">베스트셀러</a>
                    <a href="#" class="hover:text-indigo-200 transition">신간 안내</a>
                    <a href="#" class="hover:text-indigo-200 transition">전자책(eBook)</a>
                </nav>
            </div>

            <!-- 검색창 & 장바구니 아이콘 -->
            <div class="flex items-center space-x-4">
                <form action="{{ route('books.index') }}" method="GET" class="relative hidden sm:block">
                    <input type="text" name="keyword" placeholder="도서명, 저자, ISBN 검색..." 
                           class="w-64 bg-indigo-950 text-white placeholder-indigo-300 text-sm rounded-full pl-4 pr-10 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400">
                    <button type="submit" class="absolute right-3 top-2 text-indigo-300">🔍</button>
                </form>
                <a href="#" class="relative p-2 hover:bg-indigo-800 rounded-full transition">
                    🛒 <span class="sr-only">장바구니</span>
                    <span class="absolute top-0 right-0 bg-rose-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center font-bold">3</span>
                </a>
            </div>
        </div>
    </header>

    <!-- 2. 선택적 상단 서브 헤더 (Hero 배너 등) -->
    @isset($header)
        <div class="bg-white border-b border-slate-200 py-6">
            <div class="max-w-7xl mx-auto px-4">
                {{ $header }}
            </div>
        </div>
    @endisset

    <!-- 3. 본문 메인 콘텐츠 (기본 슬롯 $slot 이 삽입되는 곳!) -->
    <main class="flex-grow max-w-7xl mx-auto px-4 py-8 w-full">
        {{ $slot }}
    </main>

    <!-- 4. 서점 글로벌 푸터 -->
    <footer class="bg-slate-900 text-slate-400 py-10 text-sm border-t border-slate-800">
        <div class="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div>
                <p class="font-bold text-white mb-1">지니샵(JinyShop) 온라인 도서 유통 주식회사</p>
                <p>멘토 지니 & 주니어 개발자 도로시 & 개발 보조견 토토</p>
                <p class="text-xs text-slate-500 mt-2">© 2026 JinyShop Inc. All rights reserved.</p>
            </div>
            <div class="flex space-x-6 text-xs">
                <a href="#" class="hover:text-white">이용약관</a>
                <a href="#" class="hover:text-white">개인정보처리방침</a>
                <a href="#" class="hover:text-white">고객센터(1588-0000)</a>
            </div>
        </div>
    </footer>

</body>
</html>
```

---

### [Step 2] 도서 목록 페이지에서 마스터 레이아웃 조립

이제 `resources/views/books/index.blade.php` 파일을 생성하고, `<x-layouts.app>` 컴포넌트로 본문 화면을 감싸줍니다.

```html
<!-- resources/views/books/index.blade.php -->
<x-layouts.app>
    <!-- 명명된 슬롯 $title 주입 -->
    <x-slot:title>
        지니샵 — 실시간 전체 도서 카탈로그
    </x-slot:title>

    <!-- 명명된 슬롯 $header 주입 -->
    <x-slot:header>
        <div class="flex items-center justify-between">
            <div>
                <h1 class="text-2xl font-bold text-slate-900">📚 전체 도서 둘러보기</h1>
                <p class="text-sm text-slate-500 mt-1">개발, 인문, 경영 등 1,000여 권의 엄선된 도서를 만나보세요.</p>
            </div>
            <div class="flex space-x-2">
                <button class="px-3 py-1.5 bg-indigo-50 text-indigo-700 text-xs font-semibold rounded-md border border-indigo-200">인기순</button>
                <button class="px-3 py-1.5 bg-white text-slate-600 text-xs font-semibold rounded-md border border-slate-200">최신순</button>
            </div>
        </div>
    </x-slot:header>

    <!-- 기본 슬롯 $slot 에 주입될 본문 -->
    <div class="bg-white rounded-xl p-8 shadow-sm border border-slate-200">
        <p class="text-slate-600">이곳에 2강에서 제작할 예쁜 도서 카드 그리드가 채워질 예정입니다! 🎉</p>
    </div>
</x-layouts.app>
```

---

### [Step 3] `BookController@index`에서 뷰 반환 및 확인

`app/Http/Controllers/BookController.php`의 `index()` 메서드가 `view('books.index')`를 반환하도록 업데이트합니다:

```php
public function index()
{
    return view('books.index');
}
```

브라우저에서 `http://127.0.0.1:8000/books`에 접속합니다!
세련된 네이비 톤의 지니샵 헤더, 검색창, 장바구니 뱃지, 서브헤더, 본문 카드, 푸터까지 완벽한 레이아웃이 렌더링됩니다.

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 블레이드 컴포넌트의 컴파일 메커니즘
- Blade 파일(`*.blade.php`)은 브라우저로 전송될 때 실시간으로 해석되는 인터프리터 방식이 아닙니다.
- 라라벨은 최초 요청 시 블레이드 문법을 순수 고성능 PHP 코드로 사전 컴파일하여 `storage/framework/views/` 폴더에 캐싱합니다.
- 따라서 복잡한 컴포넌트 중첩 구조라도 순수 PHP를 직접 짠 것과 동일한 초고속 렌더링 성능을 자랑합니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **블레이드 화면을 고쳤는데 변경 사항이 안 보여요!**  
>    뷰 캐시가 엉켰을 때는 터미널에 `php artisan view:clear`를 치면 컴파일된 뷰 캐시가 싹 날아가고 새 화면이 뜬다멍!

---

## 💡 6. 1강 자가진단 과제

1. 마스터 레이아웃 푸터에 본인의 닉네임과 서점 슬로건을 추가해 보세요.
2. `resources/views/home.blade.php` 파일을 새로 만들고, `<x-layouts.app>`으로 감싸서 메인 홈 페이지도 동일한 헤더/푸터가 뜨는지 확인하세요.
{% endraw %}
