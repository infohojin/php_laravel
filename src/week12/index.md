---
layout: docs
title: "12주차: 도서 정산 아티산 CLI, 작업 스케줄링, 캐시 & 웹소켓 실시간 알림"
---

{% raw %}
# 📖 12주차: 도서 정산 아티산 CLI, 작업 스케줄링, 캐시 & 웹소켓 실시간 알림

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** 자정 미결제 취소 크론 스케줄러, Prompts 대화형 재고 보충 CLI, Redis 캐싱, Reverb 웹소켓 주문 실시간 알림, 다국어 지원  
> **캐릭터:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 매일 밤 12시에 24시간 동안 입금되지 않은 주문을 취소하고 도서 재고를 자동으로 원복해 줄 순 없을까? 그리고 신간 도서가 나오면 서점 관리자 화면에 새로고침 없이 띵동 알림을 띄우고 싶어!"  
🐱 **지니**: "라라벨 **스케줄러(Scheduler)**에 크론 한 줄만 걸어두면 매일 자정 자동 배치가 작동한단다! 그리고 **Reverb 웹소켓**을 연결하면 새 주문이 들어올 때마다 관리자 모니터에 실시간 팝업이 뜨지. 인기 베스트셀러는 **Redis 캐시**에 담아 100배 빠르게 서빙하렴!"  
🐶 **토토**: "멍멍! 창고 관리자가 터미널에서 화살표 키로 책을 골라 재고를 채우는 Laravel Prompts CLI 커맨드도 만들자멍! 해외 독자를 위해 영문 언어팩도 세팅하자멍!" 

---

## 📑 12주차 상세 강의 목록 (Step-by-Step Lectures)

이번 12주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 대화형 아티산(Artisan) 콘솔, 라라벨 프롬프트(Prompts) & 프로세스(Processes)](./01_custom_artisan_and_prompts.md)**
   - 커스텀 아티산 커맨드(`shop:restock`) 제작 및 시그니처/인자 설정
   - Laravel Prompts: 방향키 검색(`search`), 수량 검증(`text`), 컨펌(`confirm`), 로딩 스피너(`spin`), 요약 테이블(`table`)
   - 라라벨 `Process` 파사드를 이용한 외부 CLI 유틸리티 비동기 실행 풀

2. **[02강: 작업 스케줄링(Task Scheduling)과 자정 배치 자동화](./02_task_scheduling_cron.md)**
   - 라라벨 11 콘솔 스케줄러(`routes/console.php`) 아키텍처
   - 24시간 미결제 주문 일괄 취소 및 재고 원복 배치(`shop:cancel-unpaid-orders`)
   - 중복 실행 방지(`withoutOverlapping`), 백그라운드 병렬 실행, 단일 서버 실행(`onOneServer`) 및 리눅스 크론 등록

3. **[03강: Redis 캐시 아키텍처, 캐시 태그(Cache Tags)와 병렬 동시성(Concurrency)](./03_redis_cache_and_concurrency.md)**
   - Redis 캐시 드라이버 연동 및 `Cache::remember()` 베스트셀러 고속 서빙
   - `Cache::tags(['books', "category:{$id}"])`를 통한 카테고리/베스트셀러 정밀 무효화
   - 라라벨 11 신기능 `Concurrency::run()`으로 외부 3대 택배사 배송 상태 병렬 동시 조회

4. **[04강: 라라벨 리버브(Reverb) 웹소켓 실시간 알림 & 다국어(Localization)](./04_reverb_websocket_and_localization.md)**
   - `php artisan install:broadcasting` 및 초고속 웹소켓 서버 Laravel Reverb 구동
   - `NewBookOrderPlaced` 이벤트와 프론트엔드 Laravel Echo 실시간 주문 토스트 알림 연동
   - 다국어 언어팩(`lang/ko`, `lang/en`, `lang/ja`), 단수/복수형 번역(`trans_choice`) 및 언어 스위처 미들웨어

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [아티산 콘솔 (Artisan)](../docs/05_digging_deeper/artisan_ko.md)
- [프롬프트 (Prompts)](../docs/11_packages/prompts_ko.md)
- [작업 스케줄링 (Scheduling)](../docs/05_digging_deeper/scheduling_ko.md)
- [캐시 (Cache)](../docs/05_digging_deeper/cache_ko.md)
- [Redis (레디스)](../docs/07_database/redis_ko.md)
- [브로드캐스팅 (Broadcasting)](../docs/05_digging_deeper/broadcasting_ko.md)
- [Reverb (웹소켓 서버)](../docs/11_packages/reverb_ko.md)
- [동시성 (Concurrency)](../docs/05_digging_deeper/concurrency_ko.md)
- [프로세스 (Processes)](../docs/05_digging_deeper/processes_ko.md)
- [다국어 지원 (Localization)](../docs/05_digging_deeper/localization_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "대화형 프롬프트(Prompts)는 크론탭이나 배포 파이프라인에서 돌리면 먹통이 되니 `--no-interaction` 처리를 꼭 해두어야 해! 스케줄러 중복 방지는 Redis 캐시가 있어야 `onOneServer()`와 함께 안정적으로 작동한다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `shop:restock` 대화형 CLI 커맨드 작성 및 스피너/테이블 출력 확인
- [ ] `routes/console.php`에 자정 미결제 주문 자동 취소 스케줄 등록 및 `schedule:list` 확인
- [ ] Redis 기반 베스트셀러 캐싱 및 도서 수정 시 `Cache::tags()` 자동 무효화 검증
- [ ] `Concurrency::run()`으로 다중 택배사 배송 상태 병렬 조회 테스트
- [ ] Laravel Reverb 웹소켓 서버 기동 및 주문 발생 시 실시간 토스트 알림 수신
- [ ] 한국어/영어 다국어 언어팩 번역 및 언어 스위칭 확인
{% endraw %}
