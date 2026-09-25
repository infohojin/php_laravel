---
layout: docs
title: "11주차: 비동기 주문 처리, 결제 승인, 도서 구매 알림 시스템"
---

{% raw %}
# 📖 11주차: 비동기 주문 처리, 결제 승인, 도서 구매 알림 시스템

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** OrderPlaced 도메인 이벤트 발행, 비동기 큐 작업(Job), Horizon 대시보드 모니터링, 구매 확인 메일 및 Cashier 결제  
> **캐릭터:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 고객이 책 5권을 주문하고 결제 버튼을 눌렀는데 화면이 멈춰 있어! 결제사 승인받고, 도서 재고 차감하고, 구매 영수증 PDF 메일 쏘고, 관리자 슬랙 알림 보내는 걸 한꺼번에 하려니 화면이 굳어버렸어!"  
🐱 **지니**: "도로시, **이벤트(Event)**와 **비동기 큐(Queue)** 마법을 쓸 시간이란다! 주문 컨트롤러는 `OrderPlaced` 이벤트만 빵 터뜨리고 손님에게 0.1초 만에 '결제 완료!' 화면을 보여주는 거지. 무거운 메일 발송과 슬랙 전송은 백그라운드 큐 워커들이 뒤에서 차례대로 처리한단다!"  
🐶 **토토**: "멍멍! 라라벨 Horizon 대시보드를 켜두면 지금 큐에서 몇 통의 주문 확인서 메일이 전송 중인지 실시간 그래프로 한눈에 감시할 수 있다멍!" 

---

## 📑 11주차 상세 강의 목록 (Step-by-Step Lectures)

이번 11주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 이벤트(Events)와 리스너(Listeners)를 활용한 주문 완료 도메인 분리](./01_events_and_listeners.md)**
   - 관심사의 분리와 `OrderPlaced` 도메인 이벤트 발행
   - `DeductBookStock`(도서 재고 차감 및 품절 처리), `ClearUserCart`, `LogOrderAudit` 리스너
   - 라라벨 11 자동 이벤트 발견(Event Discovery) 및 이벤트 리스트 검증

2. **[02강: 비동기 큐(Queues) 작업 처리와 라라벨 호라이즌(Horizon) 모니터링](./02_async_queues_and_horizon.md)**
   - 동기(Sync) vs 비동기 큐(Redis/Database) 아키텍처 및 응답 지연 해결
   - 전자책(eBook) 개인화 워터마크 생성 `ProcessBookWatermarkJob` (`ShouldQueue`, `$tries`, `$backoff`)
   - Laravel Horizon 실시간 웹 관제 대시보드 설치 및 실패 작업 재시도

3. **[03강: 메일(Mail)과 다채널 알림(Notifications) 시스템 구축](./03_mailables_and_notifications.md)**
   - 마크다운 기반 `OrderReceiptMail` 반응형 이메일 디자인 및 실시간 브라우저 프리뷰
   - `Mail::to()->queue()` 백그라운드 큐 발송
   - 다채널 알림(인앱 Database 알림 뱃지 + 고객 이메일 + 관리자 Slack 웹훅)

4. **[04강: 라라벨 캐셔(Cashier Stripe & Paddle)를 이용한 정기 구독 및 글로벌 결제](./04_cashier_stripe_paddle.md)**
   - '지니샵 북클럽 멤버십' 월간 정기 구독(Subscription) 비즈니스 모델 구현
   - `Billable` 트레이트, SetupIntent 발급, 신용카드 등록 및 정기 결제
   - 구독 상태 체크(`subscribed`, `onGracePeriod`, `cancelled`) 및 웹훅 보안 처리

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [이벤트 (Events)](../docs/05_digging_deeper/events_ko.md)
- [큐 (Queues)](../docs/05_digging_deeper/queues_ko.md)
- [메일 (Mail)](../docs/05_digging_deeper/mail_ko.md)
- [알림 (Notifications)](../docs/05_digging_deeper/notifications_ko.md)
- [Cashier Stripe (결제)](../docs/11_packages/billing_ko.md)
- [Cashier Paddle (글로벌 결제)](../docs/11_packages/cashier-paddle_ko.md)
- [Horizon (Redis 큐 모니터링)](../docs/11_packages/horizon_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "큐 워커(`queue:work`)를 띄워두고 코드를 고치면 반영되지 않으니 `php artisan queue:restart`를 외치는 습관을 들이자멍! 메일 템플릿을 수정할 때 매번 메일을 쏘지 말고 브라우저 프리뷰 라우트를 열어두면 개발 속도가 10배 빨라진다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `OrderPlaced` 이벤트 디스패치 및 `DeductBookStock` 재고 차감 리스너 분리 완료
- [ ] 전자책 워터마크 비동기 Job(`ProcessBookWatermarkJob`) 작성 및 큐 워커 처리
- [ ] Laravel Horizon 대시보드(`/horizon`) 접속 및 실시간 큐 지표 확인
- [ ] 마크다운 주문 영수증 메일 프리뷰 및 비동기 큐 발송
- [ ] 마이페이지 인앱 알림 뱃지 및 Cashier Stripe 북클럽 구독 라이프사이클 구현
{% endraw %}
