---
layout: docs
title: "14주차: 도서 구매 플로우 테스트 자동화, 브라우저 E2E, 모니터링 & 프로덕션 배포"
---

{% raw %}
# 📖 14주차: 도서 구매 플로우 테스트 자동화, 브라우저 E2E, 모니터링 & 프로덕션 배포

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** Pest/PHPUnit 기능 테스트, Dusk 브라우저 E2E 자동 결제 테스트, Pulse APM 모니터링, Envoy 무중단 배포, 패키지 개발  
> **캐릭터:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니, 토토! 14주 동안 우리가 만든 **지니샵(JinyShop)** 온라인 서점이 드디어 세상에 공개될 준비를 마쳤어! 수많은 독자들이 결제할 때 에러가 나지 않는다고 어떻게 장담할 수 있을까?"  
🐱 **지니**: "도로시, 프로 개발자는 **자동화 테스트**로 증명한단다! Pest/PHPUnit으로 결제/할인 로직을 0.5초 만에 전수 검증하고, **Laravel Dusk**로 가상 브라우저가 직접 장바구니부터 결제까지 자동으로 클릭하며 시험하게 만들자꾸나. 그리고 **Laravel Pulse**로 서버 건강을 지켜보며 **Envoy**로 무중단 배포를 쏘아 올리는 거란다!"  
🐶 **토토**: "멍멍! 모든 테스트 터미널에 영롱한 초록색 불(PASS)이 가득 떴다멍! 지니샵 그랜드 오픈 성공이다멍!" 

---

## 📑 14주차 상세 강의 목록 (Step-by-Step Lectures)

이번 14주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 단위 & 기능 테스트(Pest/PHPUnit), 데이터베이스 테스트 & 모킹(Mocking)](./01_pest_phpunit_testing.md)**
   - 인메모리 SQLite DB 격리 설정 및 `RefreshDatabase`
   - 모델 단위 테스트(Unit) 및 장바구니/주문 결제 전체 시나리오 기능 테스트(Feature)
   - `CancelUnpaidOrdersCommand` 콘솔 명령어 테스트
   - `Http::fake()`, `Mail::fake()`, `Event::fake()` 모킹을 통한 외부 결제망 격리

2. **[02강: 라라벨 더스크(Dusk)를 이용한 브라우저 E2E 구매 시나리오 자동화](./02_dusk_browser_e2e_testing.md)**
   - Laravel Dusk 설치 및 ChromeDriver 연동
   - 헤드리스 크롬 기반 실제 브라우저 사용자 구매 여정 E2E 자동 검증: 검색 -> 상세 -> 장바구니 -> 결제 -> 주문 완료
   - 자바스크립트 대기(`waitForText`), 에러 순간 스크린샷 자동 캡처 및 다중 브라우저 실시간 웹소켓 알림 검증

3. **[03강: 라라벨 펄스(Pulse) 실시간 APM 모니터링 & 옥탄(Octane) 초고속 메모리 상주 서빙](./03_pulse_monitoring_and_octane.md)**
   - Laravel Pulse 오픈소스 APM 대시보드 구축 (`/pulse`)
   - 5대 병목(서버 리소스, Slow Requests, Slow Queries, Slow Jobs, Slow Outgoing Requests) 실시간 관제
   - Laravel Octane (FrankenPHP/Swoole) 메모리 상주형 엔진 연동 및 10배 처리량(10,000 req/s) 벤치마크
   - 옥탄 환경의 메모리 누수 방지 및 상태 리셋(Resetting State) 패턴

4. **[04강: 무중단 엔보이(Envoy) 배포, 패키지 개발 & 릴리스 업그레이드](./04_envoy_deployment_and_releases.md)**
   - 프로덕션 배포 체크리스트 및 캐시 최적화(`php artisan optimize`, OPcache)
   - `Envoy.blade.php` SSH 제로 다운타임 심볼릭 링크(`current`) 무중단 배포 스크립트
   - 지니샵 쿠폰 엔진의 독립 패키지화(`packages/jinyshop/coupon`)
   - 라라벨 릴리스 주기, 11->12 업그레이드 가이드 및 오픈소스 기여(Contributions)
   - 14주간의 지니샵 그랜드 오픈 피날레!

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [테스트 시작하기 (Testing)](../docs/10_testing/testing_ko.md)
- [HTTP 테스트 (HTTP Tests)](../docs/10_testing/http-tests_ko.md)
- [콘솔 테스트 (Console Tests)](../docs/10_testing/console-tests_ko.md)
- [데이터베이스 테스트 (Database Testing)](../docs/10_testing/database-testing_ko.md)
- [모킹 (Mocking)](../docs/10_testing/mocking_ko.md)
- [Dusk (브라우저 테스트)](../docs/10_testing/dusk_ko.md)
- [Pulse (애플리케이션 상태 모니터링)](../docs/11_packages/pulse_ko.md)
- [Octane (고성능 앱 서빙)](../docs/11_packages/octane_ko.md)
- [Envoy (배포 자동화)](../docs/11_packages/envoy_ko.md)
- [패키지 개발 (Package Development)](../docs/05_digging_deeper/packages_ko.md)
- [배포 가이드 (Deployment)](../docs/02_getting_started/deployment_ko.md)
- [릴리스 노트 (Releases)](../docs/01_prologue/releases_ko.md)
- [업그레이드 가이드 (Upgrade)](../docs/01_prologue/upgrade_ko.md)
- [기여 가이드 (Contributions)](../docs/01_prologue/contributions_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "배포 후에는 `storage`와 `bootstrap/cache` 디렉토리에 웹서버(`www-data`) 쓰기 권한이 있는지 꼭 확인해야 해! 큐 워커가 새 코드를 바라보도록 배포 스크립트 끝에서 `php artisan queue:restart`를 날리는 것도 절대 잊지 말라멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `php artisan test`로 도서 주문 및 결제 Feature Test 전수 패스 확인
- [ ] `Http::fake()`로 외부 PG사 결제 승인 API 모킹 테스트 확인
- [ ] Laravel Dusk 브라우저 E2E 테스트로 검색부터 결제 완료까지 자동 검증 및 스크린샷 확인
- [ ] Laravel Pulse APM 대시보드(`/pulse`) 연동 및 느린 쿼리 관제 확인
- [ ] Laravel Octane 메모리 상주 서빙 아키텍처 및 상태 초기화 리스너 이해
- [ ] `Envoy.blade.php` 무중단 배포 스크립트 작성 및 `php artisan optimize` 실행
- [ ] 지니샵(JinyShop) 14주 전 과정 수료 및 최종 배포 런칭 완료!
{% endraw %}
