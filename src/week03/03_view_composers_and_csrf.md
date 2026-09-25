---
layout: docs
title: "03강: 뷰 컴포저(View Composer) & CSRF 폼 보안 방어"
---

{% raw %}
# 03강: 뷰 컴포저(View Composer) & CSRF 폼 보안 방어

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 뷰 컴포저로 전역 카테고리 메뉴 자동 주입, CSRF 공격 원리 및 `@csrf` / `@method` 폼 보호  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [뷰 (Views)](../docs/04_the_basics/views_ko.md), [CSRF 보호 (CSRF Protection)](../docs/04_the_basics/csrf_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리 서점의 상단 메뉴바에는 'IT/컴퓨터', '인문학', '경제/경영', '소설' 같은 카테고리 목록이 항상 떠 있어야 하잖아요. 그럼 `HomeController`, `BookController`, `CartController`, `OrderController`의 모든 메서드마다 `Category::all()`을 조회해서 뷰에 넘겨줘야 하나요? 코드가 너무 중복될 것 같은데요!"

🐱 **지니**: "도로시가 아주 훌륭한 아키텍처 고민을 했구나! 그렇게 하면 컨트롤러가 지저분해지고 유지보수가 지옥이 된단다. 이럴 때 쓰는 라라벨의 비밀 무기가 바로 **뷰 컴포저(View Composer)**란다! 특정 뷰(예: `<x-layouts.app>`)가 렌더링될 때마다 라라벨이 백그라운드에서 자동으로 카테고리 데이터를 딱 주입해 주지. 컨트롤러는 자기 일만 하면 된단다!"

🐶 **토토**: "멍멍! 그리고 독자가 장바구니에 책을 담거나 주문서를 보낼 때, 폼 태그 안에 `@csrf`를 빼먹으면 **419 Page Expired** 에러가 터진다멍! 나쁜 해커가 고객 몰래 주문 버튼을 클릭하게 만드는 공격을 막아주는 안전벨트다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 컨트롤러 코드 수정 없이 모든 화면의 상단 메뉴에 서점 카테고리 목록을 공급하는 **뷰 컴포저(View Composer)**를 작성합니다.
2. CSRF(Cross-Site Request Forgery, 사이트 간 요청 위조) 공격의 원리를 이해하고 `@csrf` 토큰으로 방어합니다.
3. HTML5 표준이 지원하지 않는 PUT/DELETE 요청을 전달하기 위한 `@method` 스푸핑을 익힙니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 전역 카테고리 뷰 컴포저 클래스 작성

`app/View/Composers/CategoryComposer.php` 파일을 생성합니다.

```php
<?php

namespace App\View\Composers;

use Illuminate\View\View;

class CategoryComposer
{
    /**
     * 데이터를 뷰에 바인딩
     */
    public function compose(View $view): void
    {
        // 실제 운영에서는 4주차에서 배울 Category 모델에서 조회합니다.
        // 현재는 서점 표준 카테고리 배열을 공급합니다.
        $categories = [
            ['id' => 1, 'name' => 'IT / 프로그래밍', 'slug' => 'programming'],
            ['id' => 2, 'name' => '인공지능 / 데이터', 'slug' => 'ai-data'],
            ['id' => 3, 'name' => '경제 / 경영', 'slug' => 'economy'],
            ['id' => 4, 'name' => '인문 / 철학', 'slug' => 'humanities'],
            ['id' => 5, 'name' => '소설 / 에세이', 'slug' => 'novels'],
        ];

        // 뷰 템플릿에 $globalCategories 변수로 자동 전달!
        $view->with('globalCategories', $categories);
    }
}
```

---

### [Step 2] `AppServiceProvider`에 뷰 컴포저 등록

`app/Providers/AppServiceProvider.php`의 `boot()` 메서드에서 마스터 레이아웃에 컴포저를 연결합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Facades\View;
use App\View\Composers\CategoryComposer;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        //
    }

    public function boot(): void
    {
        // 마스터 레이아웃 컴포넌트가 렌더링될 때 CategoryComposer 자동 실행!
        View::composer('components.layouts.app', CategoryComposer::class);
    }
}
```

---

### [Step 3] 헤더 내비게이션에서 카테고리 동적 렌더링

`resources/views/components/layouts/app.blade.php`의 헤더 내비게이션 영역을 수정합니다:

```html
<!-- 상단 카테고리 동적 드롭다운/링크 -->
<nav class="hidden md:flex space-x-3 text-sm font-medium">
    <a href="{{ route('books.index') }}" class="text-white hover:text-indigo-200 py-1">전체보기</a>
    
    <!-- 뷰 컴포저가 주입한 $globalCategories 순회 -->
    @foreach($globalCategories as $cat)
        <a href="{{ route('books.index', ['category' => $cat['slug']]) }}" 
           class="text-indigo-200 hover:text-white px-2 py-1 rounded transition">
            {{ $cat['name'] }}
        </a>
    @endforeach
</nav>
```

브라우저를 새로고침하면 `BookController`에 아무런 코드를 적지 않았는데도 상단에 'IT/프로그래밍', '인공지능/데이터' 등 5개 카테고리가 자동으로 나타납니다!

---

### [Step 4] CSRF 토큰 및 HTTP 메서드 스푸핑 실습

도서 수량 수정 및 삭제 폼을 만들 때 필요한 보안 지시어를 확인합니다:

```html
<!-- 장바구니 수량 변경 폼 (PUT 요청 스푸핑) -->
<form action="/cart/items/42" method="POST">
    <!-- 1. CSRF 공격 차단 토큰 (필수!) -->
    @csrf

    <!-- 2. 브라우저의 POST를 PUT으로 승격 -->
    @method('PUT')

    <input type="number" name="quantity" value="2" min="1" class="w-16 border rounded p-1">
    <button type="submit" class="bg-blue-600 text-white px-3 py-1 rounded">수량 변경</button>
</form>

<!-- 도서 삭제 폼 (DELETE 요청 스푸핑) -->
<form action="{{ route('books.destroy', $book['id']) }}" method="POST" onsubmit="return confirm('정말 삭제하시겠습니까?');">
    @csrf
    @method('DELETE')
    <button type="submit" class="text-rose-500 hover:underline text-xs">도서 삭제</button>
</form>
```

> **HTML 소스 보기로 확인한 결과:**
> ```html
> <input type="hidden" name="_token" value="dF8jK9...랜덤해시값...">
> <input type="hidden" name="_method" value="PUT">
> ```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### CSRF 공격 방어 메커니즘
- 악성 사이트가 로그인된 독자의 브라우저 세션을 도용하여 몰래 `POST /cart/checkout`을 요청하더라도, 악성 사이트는 라라벨이 발급한 암호화된 `_token` 값을 알 수 없습니다.
- 라라벨의 `ValidateCsrfToken` 미들웨어는 세션의 토큰과 폼에서 넘어온 토큰이 일치하지 않으면 즉시 요청을 차단하고 `419 Page Expired` 에러를 응답합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **Ajax나 자바스크립트(Fetch)로 비동기 장바구니 담기를 할 때는요?**  
>    `<head>` 태그에 `<meta name="csrf-token" content="{{ csrf_token() }}">`을 심어두고, 자바스크립트 요청 헤더에 `X-CSRF-TOKEN`을 실어 보내면 된다멍!

---

## 💡 6. 3강 자가진단 과제

1. 임의로 폼 태그에서 `@csrf`를 지우고 `POST` 전송을 해보세요. 라라벨에서 `419 Page Expired` 에러 화면이 뜨는지 확인하세요.
2. `CategoryComposer`에 신규 카테고리 `['id' => 6, 'name' => '예술 / 디자인', 'slug' => 'art']`를 추가하고 브라우저를 새로고침하여 메뉴에 즉시 반영되는지 확인하세요.
{% endraw %}
