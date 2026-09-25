---
layout: docs
title: "04강: Vite 번들러, Tailwind CSS & OpenGraph 메타 태그 최적화"
---

{% raw %}
# 04강: Vite 번들러, Tailwind CSS & OpenGraph 메타 태그 최적화

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** Vite 고속 에셋 번들링, Tailwind CSS 빌드, 카카오톡/페이스북 도서 링크 공유용 OpenGraph `<head>` 제어  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [에셋 번들링 (Vite)](../docs/04_the_basics/vite_ko.md), [Mix](../docs/11_packages/mix_ko.md), [Head](../docs/11_packages/head_ko.md), [프론트엔드 (Frontend)](../docs/02_getting_started/frontend_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 여태까지는 CDN 스크립트로 Tailwind CSS를 불러왔는데, 실제 운영 서점에서는 네트워크가 느려지거나 CDN이 장애 나면 화면이 깨지잖아요. 그리고 독자들이 카카오톡이나 트위터에 우리 서점의 책 링크(`http://jinyshop.com/books/1`)를 공유했을 때 책 표지 그림과 책 소개글이 예쁜 카드 형태로 뜨게 만들려면 어떻게 해야 해요?"

🐱 **지니**: "도로시가 프론트엔드 성능과 SEO(검색엔진 최적화)의 핵심을 정확히 짚었구나! 라라벨의 공식 프론트엔드 번들러는 **Vite(비트)**란다. 과거의 Webpack(Laravel Mix)보다 100배 빠른 빌드 속도와 HMR(핫 모듈 리로딩)을 자랑하지. 코드를 고치고 저장하자마자 브라우저가 새로고침 없이 0.01초 만에 갱신된단다. 그리고 소셜 공유 미리보기는 **OpenGraph(OG) 메타 태그**를 동적으로 제어해주면 완성되지!"

🐶 **토토**: "멍멍! 터미널 창 하나를 열어서 `npm run dev`를 켜두면 마법 같은 실시간 개발 모드가 시작된다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. Node.js 패키지를 설치하고 Vite를 통해 Tailwind CSS와 자바스크립트를 빌드합니다.
2. `@vite(['resources/css/app.css', 'resources/js/app.js'])` 지시어로 마스터 레이아웃에 에셋을 연결합니다.
3. 책 상세 페이지마다 고유한 책 제목, 소개글, 표지 이미지를 갖는 **OpenGraph(OG) 소셜 메타 태그**를 동적으로 주입합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] Node 패키지 설치 및 Vite 빌드 환경 준비

지니샵 프로젝트 루트에서 프론트엔드 의존성을 설치합니다:

```bash
# 1. npm 패키지 설치
npm install

# 2. Tailwind CSS 및 Vite 설정 파일 확인
ls tailwind.config.js vite.config.js
```

`vite.config.js` 설정 파일 내용 확인:
```javascript
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true, // 블레이드 파일 수정 시 브라우저 자동 새로고침!
        }),
    ],
});
```

---

### [Step 2] 마스터 레이아웃에 `@vite` 지시어 적용

`resources/views/components/layouts/app.blade.php`의 `<head>` 태그 내부에서 CDN 스크립트를 제거하고 공식 `@vite` 지시어로 교체합니다:

```html
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? '지니샵 — 당신 곁의 온라인 서점' }}</title>

    <!-- 동적 OpenGraph 메타 태그 슬롯 ($head) -->
    @isset($head)
        {{ $head }}
    @else
        <!-- 기본 전역 메타 태그 -->
        <meta property="og:site_name" content="JinyShop (지니샵)">
        <meta property="og:title" content="지니샵 — 당신 곁의 똑똑한 온라인 도서 쇼핑몰">
        <meta property="og:description" content="라라벨과 함께하는 최신 기술 도서 및 인문 교양 서점">
        <meta property="og:image" content="{{ asset('img/default-book-cover.png') }}">
    @endisset

    <!-- 라라벨 공식 Vite 에셋 번들러 로드 -->
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```

---

### [Step 3] 도서 상세 페이지에서 동적 OpenGraph 메타 태그 주입

독자가 특정 책(예: '라라벨 13 마스터 클래스') 링크를 카카오톡에 복사했을 때 예쁜 미리보기가 뜨도록 `resources/views/books/show.blade.php`에 `$head` 슬롯을 채워줍니다:

```html
<!-- resources/views/books/show.blade.php -->
<x-layouts.app>
    <x-slot:title>
        {{ $book['title'] }} — 지니샵
    </x-slot:title>

    <!-- SNS 공유를 위한 OpenGraph 동적 메타 태그 주입 -->
    <x-slot:head>
        <meta property="og:type" content="book">
        <meta property="og:title" content="{{ $book['title'] }}">
        <meta property="og:description" content="{{ $book['author'] }} 저 · {{ number_format($book['price']) }}원 · 지금 지니샵에서 빠른 당일 배송으로 만나보세요.">
        <meta property="og:image" content="https://picsum.photos/800/600?random={{ $book['id'] }}">
        <meta property="og:url" content="{{ url()->current() }}">
    </x-slot:head>

    <!-- 본문 도서 상세 정보 -->
    <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <!-- ... 상세 본문 ... -->
    </div>
</x-layouts.app>
```

---

### [Step 4] Vite 개발 서버 가동 및 핫 리로딩(HMR) 체험

새 터미널 탭을 열고 Vite 개발 서버를 실행합니다:

```bash
npm run dev
```

> **터미널 출력:**
> ```text
>   VITE v5.x.x  ready in 180 ms
> 
>   ➜  Local:   http://localhost:5173/
>   ➜  press h + enter to show help
> 
>   LARAVEL v13.x.x  plugin v1.x.x
>   ➜  APP_URL: http://127.0.0.1:8000
> ```

이제 `resources/css/app.css` 파일이나 `show.blade.php` 파일의 글자 색상, 배경색을 수정하고 파일을 저장해 보세요.
브라우저를 수동으로 새로고침하지 않아도 화면이 **즉각 반영(0.05초)**되는 짜릿한 핫 리로딩을 경험할 수 있습니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### Webpack Mix vs Vite 아키텍처 비교
| 비교 항목 | 과거의 Laravel Mix (Webpack) | 최신 Laravel 13 (Vite) |
| :--- | :--- | :--- |
| **번들링 방식** | 모든 파일을 하나로 압축 후 서빙 | 브라우저 네이티브 ES 모듈(ESM) 기반 즉시 서빙 |
| **초기 서버 기동** | 프로젝트가 클수록 수십 초 소요 | **100~200ms 만에 즉각 기동** |
| **코드 수정 반영** | 전체 리빌드로 2~5초 지연 | **수정한 모듈만 0.05초 만에 교체(HMR)** |
| **운영 빌드 명령어**| `npm run prod` | `npm run build` (Rollup 기반 초경량화) |

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **화면에서 `@vite` 링크가 빨간 에러로 뜨면서 5173 포트를 못 찾아요!**  
>    Vite 개발 서버(`npm run dev`)를 켜두지 않아서 그렇다멍! 터미널 창을 하나 띄워서 `npm run dev`를 켜두거나, 배포용으로 `npm run build`를 한 번 실행해주면 에러가 사라진다멍!

---

## 💡 6. 4강 자가진단 과제

1. 터미널에서 `npm run build`를 실행하여 `public/build/assets/` 디렉터리에 캐시 버스팅 해시가 붙은 경량 CSS/JS 번들 파일이 생성되는지 확인하세요.
2. 브라우저에서 `http://127.0.0.1:8000/books/1` 페이지의 소스 보기를 열어 `<head>` 영역에 도서 전용 `og:title`, `og:description` 메타 태그가 정확히 꽂혀 있는지 확인하세요.
{% endraw %}
