---
layout: docs
title: "07주차: 폼 유효성 검사, 세션 상태 관리 & 장바구니 시스템"
---

{% raw %}
# 📖 07주차: 폼 유효성 검사, 세션 상태 관리 & 장바구니 시스템

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** `StoreCartItemRequest` Form Request, `CheckBookStock` 재고 한도 커스텀 룰, 세션 기반 `CartService`, Laravel Precognition 실시간 인라인 검증 및 NoSQL MongoDB 하이브리드 로그  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 고객이 상품 수량에 음수나 문자를 적어 보내면 어쩌죠? 그리고 로그인하지 않은 손님이 담은 장바구니 물건들은 어디에 보관해야 안전할까요?"  
🐱 **지니**: "도로시, 절대로 사용자의 입력을 믿어선 안 된단다! 라라벨의 **Form Request**를 사용하면 컨트롤러에 도달하기 전에 모든 악의적인 입력을 철저히 차단할 수 있지. 그리고 비회원 손님의 장바구니는 암호화된 **세션(Session)** 마법 상자에 안전하게 보관하면 된단다!"  
🐶 **토토**: "멍멍! Precognition을 쓰면 폼을 제출하기 전에도 타이핑하는 즉시 실시간으로 에러를 띄워줄 수 있어! 비정형 장바구니 로그는 MongoDB에 쏙쏙 담아두자멍!"  

---

## 📑 07주차 상세 강의 목록 (Step-by-Step Lectures)

이번 07주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: Form Request 캡슐화 & 재고 한도 커스텀 검증 룰(`CheckBookStock`)](./01_form_validation_and_custom_rules.md)**
   - 컨트롤러에서 검증 로직 분리: `StoreCartItemRequest`
   - 실제 도서 잔여 재고(`stock_quantity`)와 대조하는 커스텀 룰 `CheckBookStock`
   - Blade 화면 `@error` 및 `old('quantity')` 입력 복원

2. **[02강: 비회원도 가능한 세션(Session) 기반 도서 장바구니 서비스](./02_session_cart_system.md)**
   - 세션 드라이버(`file`, `database`, `redis`)의 수명과 동작 원리
   - 도서 장바구니 비즈니스 로직 캡슐화: `CartService` 구현
   - 도서 담기, 수량 실시간 변경, 항목 삭제 및 장바구니 요약 화면

3. **[03강: 라라벨 프리코그니션(Precognition) — 실시간 인라인 검증 UX](./03_precognition_realtime_validation.md)**
   - 폼 제출 없이 입력 중에 사전 검증하는 `Precognition: true` 아키텍처
   - 단일 필드 정밀 검증: `Precognition-Validate-Only` 헤더
   - 동일한 Form Request 하나로 실시간 인라인 피드백 구현

4. **[04강: NoSQL MongoDB 하이브리드 연동 — 장바구니 클릭스트림 & 로그](./04_mongodb_hybrid_cart_logs.md)**
   - RDBMS(MySQL) + NoSQL(MongoDB) 다중 커넥션 하이브리드 설계
   - 비정형 도서 열람 이력 및 장바구니 클릭스트림 수집 모델 `CartLog`
   - Active Record 인터페이스를 유지하며 대규모 비정형 데이터 적재

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [유효성 검사 (Validation)](../docs/04_the_basics/validation_ko.md)
- [세션 (Session)](../docs/04_the_basics/session_ko.md)
- [Precognition (실시간 유효성 검사)](../docs/11_packages/precognition_ko.md)
- [MongoDB (몽고DB 연동)](../docs/07_database/mongodb_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "검증 실패 후 고객이 방금 쳤던 수량이 사라지지 않게 하려면 `<input value="{{ old('quantity', 1) }}">` 처럼 `old()` 헬퍼를 기본값과 함께 꼭 적어주라멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `StoreCartItemRequest` 및 `CheckBookStock` 커스텀 룰 작성 완료
- [ ] 수량 초과 시 상세 화면에 빨간색 한국어 에러 메시지 출력 확인
- [ ] `CartService`를 이용해 세션 장바구니 담기, 수정, 삭제 기능 구현
- [ ] 장바구니 화면에서 총 주문 금액 및 무료 배송 정책 계산 확인
- [ ] Precognition 실시간 검증 헤더 및 NoSQL 로그 연동 테스트 완료
{% endraw %}
