---
layout: docs
title: "13주차: 모바일 연동 RESTful API, Sanctum 토큰 인증, 전문 검색 & AI 도서 요약"
---

{% raw %}
# 📖 13주차: 모바일 연동 RESTful API, Sanctum 토큰 인증, 전문 검색 & AI 도서 요약

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** BookResource JSON API, Sanctum 모바일 토큰 인증, Scout 10ms 도서 전문 검색, Laravel AI SDK 도서 소개글 자동 작성 & MCP  
> **캐릭터:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 우리 지니샵을 스마트폰 전용 앱으로도 출시하고 싶어! 그리고 책 제목이나 본문 키워드로 10ms 만에 찾는 고속 검색창을 만들고, 관리자가 책 제목만 넣으면 AI가 매력적인 책 소개글을 자동으로 써주게 할 수 있을까?"  
🐱 **지니**: "도로시, 상상하는 모든 것이 라라벨에서 가능하단다! **Sanctum**으로 안전한 모바일 API 토큰을 발급하고 **BookResource**로 예쁜 JSON을 내려주면 되지. 검색은 **Laravel Scout**으로 0.01초 만에 책을 찾아내고, 최신 **Laravel AI SDK**와 **MCP**를 연결하면 LLM이 마케팅 소개글을 뚝딱 써준단다!"  
🐶 **토토**: "멍멍! Pennant 피처 플래그로 신규 결제창 A/B 테스트도 하고, Folio로 반짝 할인 이벤트 페이지도 뚝딱 만들자멍!" 

---

## 📑 13주차 상세 강의 목록 (Step-by-Step Lectures)

이번 13주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 모바일 RESTful API 설계, Eloquent API 리소스 & 직렬화(Serialization)](./01_restful_api_and_resources.md)**
   - `php artisan install:api` 및 `routes/api.php` 활성화
   - `Book` 모델 직렬화 제어: 민감 원가 숨김(`$hidden`), 가상 할인율 속성(`$appends`)
   - `BookResource` 규격화, N+1 방지 조건부 관계 로드(`whenLoaded`) 및 페이지네이션 응답

2. **[02강: 라라벨 생텀(Sanctum) 모바일 API 토큰 인증 & 페넌트(Pennant) 피처 플래그](./02_sanctum_token_authentication.md)**
   - `HasApiTokens` 트레이트와 기기별 개인 액세스 토큰 발급 (`POST /api/v1/auth/login`)
   - 토큰별 세부 권한(Abilities) 검증 및 원격 기기 세션 로그아웃
   - Laravel Pennant 피처 플래그를 이용한 신규 결제 화면 50% A/B 테스트 분기

3. **[03강: 라라벨 스카우트(Scout) 전문 검색(Full-text Search) & 폴리오(Folio) 기획전 라우팅](./03_scout_fulltext_search.md)**
   - Laravel Scout 설치 및 `Book` 모델에 `Searchable` 트레이트 연동
   - `toSearchableArray()` 커스터마이징 및 대량 도서 색인(`scout:import`)
   - 10ms 초고속 도서 검색 화면과 Laravel Folio 파일 기반 기획전 페이지 런칭

4. **[04강: 라라벨 AI SDK, 모델 컨텍스트 프로토콜(MCP) & 스마트 도서 에이전트](./04_ai_sdk_and_mcp_integration.md)**
   - 라라벨 공식 AI SDK 연동 및 마케팅 상세 소개글/서평 자동 생성 서비스
   - 관리자 상품 등록 페이지 실시간 비동기 "AI 생성" 버튼 연동
   - AI 에이전트가 지니샵 서고 재고를 조회할 수 있는 MCP Tool 구축 및 Laravel Boost

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [API 리소스 (Eloquent Resources)](../docs/08_eloquent_orm/eloquent-resources_ko.md)
- [직렬화 (Serialization)](../docs/08_eloquent_orm/eloquent-serialization_ko.md)
- [Sanctum (API 토큰 인증)](../docs/11_packages/sanctum_ko.md)
- [Scout (전문 검색)](../docs/11_packages/scout_ko.md)
- [검색 (Search)](../docs/05_digging_deeper/search_ko.md)
- [AI SDK (라라벨 인공지능 SDK)](../docs/09_ai/ai-sdk_ko.md)
- [MCP (모델 컨텍스트 프로토콜)](../docs/09_ai/mcp_ko.md)
- [Boost (라라벨 부스트)](../docs/09_ai/boost_ko.md)
- [Pennant (피처 플래그)](../docs/11_packages/pennant_ko.md)
- [Folio (페이지 기반 라우팅)](../docs/11_packages/folio_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "모바일 API 호출 시 클라이언트가 `Accept: application/json` 헤더를 빼먹으면 에러 시 웹 로그인 화면으로 302 리다이렉트되어 파싱 에러가 난다멍! Scout 검색 인덱스는 도서 모델의 구조가 바뀔 때마다 `scout:flush` 후 `scout:import`로 갱신해 주자멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `GET /api/v1/books` 엔드포인트 및 `BookResource` JSON 응답 규격화 완료
- [ ] Sanctum 모바일 토큰 발급/폐기 및 세부 권한(Abilities) 검증 연동
- [ ] Pennant 피처 플래그를 통한 모바일 A/B 테스트 분기 확인
- [ ] Laravel Scout 도서 전문 검색 인덱싱 및 10ms 고속 검색 화면 구축
- [ ] Laravel Folio를 이용한 봄맞이 북페어 기획전 페이지 런칭
- [ ] Laravel AI SDK 연동 도서 홍보 카피 생성 및 지니샵 MCP 도구 구축
{% endraw %}
