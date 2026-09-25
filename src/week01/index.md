---
layout: docs
title: "01주차: 온라인 서점 프로젝트 킥오프 & 개발 환경 구축"
---

{% raw %}
# 📖 01주차: 온라인 서점 프로젝트 킥오프 & 개발 환경 구축

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** JinyShop 서점 프로젝트 생성, 개발 환경 설정, 슬림 아키텍처 및 라라벨 기본 도구 탐색  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 우리가 직접 만들 온라인 서점 **'지니샵(JinyShop)'** 프로젝트를 시작할 시간이야! 수만 권의 책과 독자들을 맞이하려면 어떤 개발 환경이 가장 좋을까?"  
🐱 **지니**: "안녕 도로시! 라라벨 13의 세계에 온 것을 환영한단다. 우리는 초보자도 손쉽게 다룰 수 있는 **Laravel Sail / Herd**를 기반으로 프로젝트를 시작할 거야. `.env` 파일로 데이터베이스와 앱 환경을 분리하고, 코드 스타일러 **Pint**와 디버거 **Telescope**로 든든한 무기를 챙기자꾸나!"  
🐶 **토토**: "멍멍! `laravel new jinyshop`을 실행할 때 네트워크가 끊기지 않게 조심해! 그리고 `php artisan key:generate`로 암호화 키를 생성하는 것도 잊지 말라멍!" 

---

## 📑 01주차 상세 강의 목록 (Step-by-Step Lectures)

이번 01주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 라라벨 13과의 만남 & 지니샵 프로젝트 생성](./01_kickoff_and_installation.md)**
   - PHP 8.2+ 생태계와 라라벨 13의 설계 철학
   - Composer 및 Laravel Installer 설치
   - `laravel new jinyshop` 명령어와 첫 웰컴 페이지 구동

2. **[02강: 라라벨 13 디렉터리 구조 해부 & 도서 서점 환경 설정 (.env)](./02_directory_and_configuration.md)**
   - 라라벨 13의 슬림(Slim) 디렉터리 구조 완전 정복
   - `bootstrap/app.php` 통합 관제소 원리
   - 지니샵 전용 `.env` 환경 변수 (시간대, 로케일, DB) 커스터마이징 및 캐싱 메커니즘

3. **[03강: 코드 스타일러 Pint & 실시간 디버거 Telescope 세팅](./03_dev_tools_pint_and_telescope.md)**
   - Laravel Pint를 이용한 PSR-12 코드 컨벤션 자동 교정
   - Laravel Telescope 디버깅 도구 설치 및 마이그레이션
   - `http://127.0.0.1:8000/telescope` 대시보드에서 HTTP 요청과 쿼리 실시간 관측

4. **[04강: 에이전트 개발(Agentic Dev) & Laravel Boost 연동](./04_agentic_dev_and_boost.md)**
   - 라라벨 공식 AI 에이전트 협업 가이드
   - `.cursorrules` / `AGENTS.md`를 통한 프로젝트 컨텍스트 주입
   - 도서(`Book`) 모델 스키마 설계를 위한 AI 프롬프트 엔지니어링 실습

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [설치 (Installation)](../docs/02_getting_started/installation_ko.md)
- [환경 설정 (Configuration)](../docs/02_getting_started/configuration_ko.md)
- [디렉터리 구조 (Directory Structure)](../docs/02_getting_started/structure_ko.md)
- [에이전트 개발 (Agentic Development)](../docs/02_getting_started/ai_ko.md)
- [Sail (도커 환경)](../docs/11_packages/sail_ko.md)
- [Pint (코드 스타일러)](../docs/11_packages/pint_ko.md)
- [Telescope (디버깅 어시스턴트)](../docs/11_packages/telescope_ko.md)
- [Valet (macOS 가상 호스트)](../docs/11_packages/valet_ko.md)
- [Homestead (가상머신 환경)](../docs/11_packages/homestead_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "온라인 서점 프로젝트 킥오프 & 개발 환경 구축 단계에서는 오타나 환경 변수 누락을 특히 주의해야 해! 문제가 생기면 `php artisan config:clear`를 실행하거나 `storage/logs/laravel.log` 파일을 확인하면 해결의 실마리를 찾을 수 있다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] Composer 또는 Laravel 인스톨러로 `laravel new jinyshop` 프로젝트 생성
- [ ] `.env` 환경 파일 설정 (`APP_NAME="JinyShop"`, `APP_TIMEZONE=Asia/Seoul`)
- [ ] `./vendor/bin/pint` 실행하여 코드 스타일 검사 완료
- [ ] Laravel Telescope 설치 후 로컬 개발 환경에서 대시보드(`/telescope`) 접속 확인
- [ ] AI 코딩 지원을 위한 에이전트 규칙 파일 설정
{% endraw %}
