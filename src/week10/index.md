---
layout: docs
title: "10주차: 라라벨 코어 아키텍처 Deep Dive & 외부 PG사 결제 연동"
---

{% raw %}
# 📖 10주차: 라라벨 코어 아키텍처 Deep Dive & 외부 PG사 결제 연동

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** 서비스 컨테이너 IoC, DI 자동 주입, PaymentGatewayContract 인터페이스 추상화, 파사드 및 외부 통신  
> **캐릭터:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 우리가 서점 결제 모듈을 만드는데, 국내 손님은 토스페이로 결제하고 해외 손님은 스트라이프로 결제하게 하려면 코드를 복잡하게 `if/else`로 도배해야 해?"  
🐱 **지니**: "바로 그럴 때 라라벨의 정수인 **서비스 컨테이너(Service Container)**와 **컨트랙트(Contract)** 인터페이스를 쓰는 거란다! `PaymentGatewayContract` 인터페이스를 규격화해두고 프로바이더에서 동적으로 바인딩하면, 컨트롤러 코드는 단 한 줄도 손대지 않고 결제 대행사를 교체할 수 있단다!"  
🐶 **토토**: "멍멍! 외부 PG사 결제 승인 API를 호출할 때는 라라벨 내장 `Http::timeout(5)->retry(3)` HTTP 클라이언트를 쓰면 네트워크 순시 장애도 끄떡없다멍!" 

---

## 📑 10주차 상세 강의 목록 (Step-by-Step Lectures)

이번 10주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 서비스 컨테이너(IoC/DI) & 결제 인터페이스 추상화](./01_service_container_and_contracts.md)**
   - 라라벨 서비스 컨테이너(IoC)의 의존성 주입 원리
   - `PaymentGatewayContract` 인터페이스 정의 및 DTO(`PaymentResult`) 작성
   - `TossPaymentGateway`와 가상 시뮬레이션용 `MockPaymentGateway` 구현

2. **[02강: 서비스 프로바이더 바인딩 & 환경별 동적 PG 교체](./02_service_providers_binding.md)**
   - `PaymentServiceProvider` 등록 및 `register()` / `boot()` 생명주기
   - 싱글톤(`singleton`) 및 컨텍스추얼 바인딩(`when->needs->give`)
   - `config/shop.php` 설정을 통한 노코드 PG사 스위칭 아키텍처

3. **[03강: 파사드(Facades) 내부 원리와 커스텀 Payment 파사드](./03_facades_internals_and_custom_facade.md)**
   - 파사드의 `getFacadeAccessor()` 동작 메커니즘과 정적 호출 마법
   - `App\Facades\Payment` 제작 및 실시간 IDE 자동완성 PHPDoc 어노테이션
   - 장바구니 주문 결제 컨트롤러(`CheckoutController`) 리팩토링

4. **[04강: HTTP 클라이언트(외부 PG 연동) & Context 추적 로깅](./04_http_client_and_context.md)**
   - 라라벨 `Http` 클라이언트 타임아웃, 재시도(`retry`), 토큰 인증
   - `Context` 파사드를 활용한 주문 ID / 사용자 세션 추적 로깅
   - 결제 승인 완료 뷰 및 모의 결제 완주 테스트

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [서비스 컨테이너 (Service Container)](../docs/03_architecture_concepts/container_ko.md)
- [서비스 프로바이더 (Service Providers)](../docs/03_architecture_concepts/providers_ko.md)
- [파사드 (Facades)](../docs/03_architecture_concepts/facades_ko.md)
- [컨트랙트 (Contracts)](../docs/05_digging_deeper/contracts_ko.md)
- [컨텍스트 (Context)](../docs/05_digging_deeper/context_ko.md)
- [헬퍼 (Helpers)](../docs/05_digging_deeper/helpers_ko.md)
- [HTTP 클라이언트 (HTTP Client)](../docs/05_digging_deeper/http-client_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "서비스 프로바이더를 새로 만들었으면 `bootstrap/providers.php`에 등록되었는지 꼭 확인해야 해! 파사드를 만들고 클래스를 못 찾는 에러가 나면 `composer dump-autoload`를 한 번 날려주면 바로 해결된다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `PaymentGatewayContract` 인터페이스 및 `PaymentResult` DTO 작성
- [ ] `TossPaymentGateway`, `MockPaymentGateway` 구현체 작성
- [ ] `PaymentServiceProvider` 작성 및 환경 설정 바인딩
- [ ] `Payment` 커스텀 파사드 제작 및 `CheckoutController` 연동
- [ ] 라라벨 `Http` 클라이언트 결제 API 승인 및 `Context` 추적 로그 확인
{% endraw %}
