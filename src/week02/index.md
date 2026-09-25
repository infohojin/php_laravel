---
layout: docs
title: "02주차: 요청 라이프사이클 & 라우팅과 컨트롤러 아키텍처"
---

{% raw %}
# 📖 02주차: 요청 라이프사이클 & 라우팅과 컨트롤러 아키텍처

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** 요청 라이프사이클 추적, RESTful 도서 라우팅, 리소스 컨트롤러(`BookController`), 보안 Signed URLs 및 응답/리다이렉트 처리  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 고객이 브라우저 주소창에 `jinyshop.test/books`라고 입력하고 엔터를 치면, 화면이 나오기 전까지 라라벨 내부에서 어떤 모험이 일어나는 거야?"  
🐱 **지니**: "도로시, 그것이 바로 **요청 라이프사이클(Request Lifecycle)**이란다! `public/index.php`라는 현관문으로 들어온 요청은 오토로더를 거쳐 서비스 프로바이더들에 의해 기초 체력이 다져지고, 라우터와 미들웨어라는 검문소를 지나 알맞은 컨트롤러 방으로 안내된단다."  
🐶 **토토**: "멍멍! 라우트 이름(Named Routes)을 `route('books.show', $id)`처럼 지어두면 나중에 URL 주소가 바뀌어도 링크가 깨지지 않는다멍!"  

---

## 📑 02주차 상세 강의 목록 (Step-by-Step Lectures)

이번 02주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 브라우저에서 화면까지 — 라라벨 13 요청 라이프사이클](./01_request_lifecycle.md)**
   - 단일 진입점 `public/index.php`와 부트스트랩
   - 서비스 프로바이더와 미들웨어 파이프라인
   - Telescope를 이용한 요청 처리 시간(ms) 실시간 관측

2. **[02강: 도서 서점 라우팅 설계 & 보안 서명된 URL (Signed URLs)](./02_routing_and_urls.md)**
   - RESTful 도서 라우트 그룹핑 (`prefix`, `name`)
   - 정규식 파라미터 제약조건 (`whereNumber`, `whereAlphaNumeric`)
   - 전자책(eBook) 미리보기 샘플 다운로드를 위한 30분 만료 Signed URL 생성 및 변조 방어

3. **[03강: 컨트롤러(Controller) 아키텍처 & HTTP 요청(Request) 해부](./03_controllers_and_requests.md)**
   - 7대 CRUD 표준 `BookController` 리소스 컨트롤러 생성
   - 주간 베스트셀러 전용 단일 액션 `BestSellerController` (`__invoke`)
   - `Request` 객체로부터 검색어, 카테고리 필터, 불리언 플래그 안전 추출

4. **[04강: 응답(Response)의 다양한 변신 & 리다이렉트와 플래시 메시지](./04_responses_and_redirects.md)**
   - Blade 뷰 반환 및 JSON 모바일 응답
   - 전자책 샘플 PDF 파일 다운로드 (`response()->download()`)
   - Post-Redirect-Get(PRG) 패턴 및 1회성 세션 플래시 메시지(`with('success', ...)`)

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [요청 라이프사이클 (Request Lifecycle)](../docs/03_architecture_concepts/lifecycle_ko.md)
- [라우팅 (Routing)](../docs/04_the_basics/routing_ko.md)
- [컨트롤러 (Controllers)](../docs/04_the_basics/controllers_ko.md)
- [요청 (Requests)](../docs/04_the_basics/requests_ko.md)
- [응답 (Responses)](../docs/04_the_basics/responses_ko.md)
- [URL 생성 (URL Generation)](../docs/04_the_basics/urls_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "라우트를 만들 때는 고정 경로(`/books/bestsellers`)를 와일드카드 경로(`/books/{id}`)보다 항상 위에 적어야 해! 순서가 바뀌면 `bestsellers`라는 글자를 책 ID로 착각하고 404 에러가 나거나 엉뚱한 화면이 뜬다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `public/index.php` 요청 라이프사이클 추적 및 Telescope에서 요청 시간 확인
- [ ] `routes/web.php`에 도서 프리픽스 라우트 그룹 및 Named Routes 등록
- [ ] 30분 유효기간의 eBook 샘플 다운로드 Signed URL 생성 및 파라미터 변조 403 차단 테스트
- [ ] `php artisan make:controller BookController --resource` 생성 및 Request 필터 파싱
- [ ] 도서 상세 화면 Blade 템플릿과 성공 플래시 메시지 표시 확인
{% endraw %}
