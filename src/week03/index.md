---
layout: docs
title: "03주차: 블레이드 템플릿 엔진 & 프론트엔드 에셋 번들링 (JinyShop UI/UX)"
---

{% raw %}
# 📖 03주차: 블레이드 템플릿 엔진 & 프론트엔드 에셋 번들링 (JinyShop UI/UX)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** 컴포넌트 기반 Blade 마스터 레이아웃, 도서 카드(`<x-book-card>`), 뷰 컴포저 전역 메뉴, CSRF 폼 방어 및 Vite/Tailwind 에셋 번들링  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 쇼핑몰의 수많은 페이지마다 상단 네비게이션 바랑 푸터 디자인을 매번 복사해서 붙여넣어야 해? 너무 번거로운데..."  
🐱 **지니**: "후후, 그럴 필요 전혀 없단다! 라라벨의 **Blade 템플릿 엔진**에는 `<x-layouts.app>` 같은 컴포넌트 마법 상자가 있거든. 슬롯(Slot) 구멍에 본문 내용만 쏙 집어넣으면 전체 레이아웃이 완성된단다!"  
🐶 **토토**: "멍멍! 폼 태그 안에 `@csrf`를 안 넣으면 419 에러가 나니까 꼭 챙겨야 해! Vite 개발 서버를 켜두면 CSS 고칠 때마다 브라우저가 알아서 0.05초 만에 새로고침 된다멍!"  

---

## 📑 03주차 상세 강의 목록 (Step-by-Step Lectures)

이번 03주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 마스터 레이아웃 `<x-layouts.app>` & 슬롯(Slot) 아키텍처](./01_blade_layouts_and_components.md)**
   - 컴포넌트 기반 Blade 마스터 레이아웃 구조화
   - 글로벌 헤더 내비게이션, 검색창, 장바구니 뱃지, 푸터 모듈화
   - 기본 슬롯(`$slot`)과 명명된 슬롯(`$title`, `$header`) 조립

2. **[02강: 도서 카드 `<x-book-card>` 컴포넌트 & 블레이드 필수 지시어](./02_book_card_and_directives.md)**
   - `@props`를 활용한 독립 도서 카드 컴포넌트 제작
   - 도서 표지, 할인율 뱃지, 종이책/전자책 포맷 분기
   - `@forelse`와 `@empty`를 활용한 검색 결과 0건 대체 화면

3. **[03강: 뷰 컴포저(View Composer) & CSRF 폼 보안 방어](./03_view_composers_and_csrf.md)**
   - 컨트롤러 중복 없는 전역 서점 카테고리 자동 주입
   - `AppServiceProvider` 뷰 컴포저 바인딩
   - CSRF 공격 원리 및 `@csrf`, `@method('PUT')` 폼 보안 지시어

4. **[04강: Vite 번들러, Tailwind CSS & OpenGraph 메타 태그 최적화](./04_vite_tailwind_and_head.md)**
   - 차세대 Vite 번들러와 `@vite` 에셋 연결
   - 실시간 HMR(Hot Module Replacement) 개발 환경
   - 카카오톡/페이스북 도서 링크 공유용 동적 OpenGraph `<head>` 태그 주입

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [뷰 (Views)](../docs/04_the_basics/views_ko.md)
- [블레이드 템플릿 (Blade Templates)](../docs/04_the_basics/blade_ko.md)
- [에셋 번들링 (Vite)](../docs/04_the_basics/vite_ko.md)
- [CSRF 보호 (CSRF Protection)](../docs/04_the_basics/csrf_ko.md)
- [프론트엔드 (Frontend)](../docs/02_getting_started/frontend_ko.md)
- [Mix (레거시 번들러)](../docs/11_packages/mix_ko.md)
- [Head (SPA 메타 태그 제어)](../docs/11_packages/head_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "화면에서 `@vite` 링크가 빨간 에러로 뜨면서 5173 포트를 못 찾을 때는, 터미널 창을 하나 띄워서 `npm run dev`를 켜두거나 `npm run build`를 한 번 실행해주면 에러가 사라진다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `<x-layouts.app>` 마스터 레이아웃 컴포넌트 작성 및 슬롯 렌더링 확인
- [ ] `<x-book-card>` 컴포넌트로 도서 그리드 목록 렌더링
- [ ] `CategoryComposer` 작성 후 전역 카테고리 메뉴 자동 표시 검증
- [ ] 폼 태그에 `@csrf` 적용하여 419 에러 방어 확인
- [ ] `npm run dev` 실행 후 Vite HMR 핫 리로딩 및 OpenGraph 메타 태그 확인
{% endraw %}
