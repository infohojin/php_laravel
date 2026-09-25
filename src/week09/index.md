---
layout: docs
title: "09주차: 파일 스토리지, 미들웨어 & 백오피스 관리자 페이지"
---

{% raw %}
# 📖 09주차: 파일 스토리지, 미들웨어 & 백오피스 관리자 페이지

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** Flysystem 파일 스토리지, `storage:link`, 도서 표지 WebP 리사이징 최적화, 관리자 전용 미들웨어(`EnsureUserIsAdmin`), 백오피스 대시보드 및 Rate Limiting/감사 로깅  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 쇼핑몰 관리자가 상품을 새로 등록할 때 사진을 여러 장 올릴 수 있어야 해. 그런데 고화질 사진을 그대로 올리니까 페이지 용량이 너무 커지고 서버가 버벅거려!"  
🐱 **지니**: "도로시, 라라벨의 **Flysystem 파일 스토리지**와 **Images 파이프라인**을 조합할 차례란다! 업로드된 이미지를 600px 너비로 자동 리사이징하고 최신 WebP 포맷으로 압축하면 용량을 97% 줄일 수 있지. 그리고 관리자 페이지는 미들웨어 성벽 뒤에 숨겨두어야 한단다."  
🐶 **토토**: "멍멍! 봇들이 결제 버튼을 1초에 백 번 누르지 못하게 Rate Limiting 속도 제한도 꼭 걸어야 해! 이상 징후는 `daily` 채널로 삐뽀삐뽀 로깅하자멍!"  

---

## 📑 09주차 상세 강의 목록 (Step-by-Step Lectures)

이번 09주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: Flysystem 파일 스토리지 & 도서 표지 이미지 업로드](./01_filesystem_and_storage_link.md)**
   - 라라벨 파일 스토리지(Flysystem) 아키텍처와 `public` 디스크
   - `php artisan storage:link` 심볼릭 링크 연결 원리
   - `multipart/form-data` 파일 검증 및 고유 해시명 안전 저장

2. **[02강: 도서 표지 썸네일 자동 생성 & WebP 압축 최적화](./02_image_optimization_and_webp.md)**
   - 대용량 도서 표지 리사이징(가로 600px) 및 1:1 정사각형 썸네일 추출
   - 차세대 WebP 포맷 변환으로 파일 용량 97% 극적 절감 (LCP 최적화)
   - `BookImageService` 파이프라인과 다형성 이미지 테이블 연동

3. **[03강: 관리자 전용 미들웨어(`EnsureUserIsAdmin`) & 서점 백오피스 대시보드](./03_admin_middleware_and_backoffice.md)**
   - 커스텀 미들웨어 작성 및 `bootstrap/app.php` 별칭(`admin`) 등록
   - 비인가 사용자 및 일반 독자 403 Forbidden 철통 차단
   - 실시간 도서 재고, 품절 통계, 총누적 매출이 집계되는 관리자 대시보드

4. **[04강: Rate Limiting 악의적 봇 방어 & 감사 로깅/커스텀 에러 페이지](./04_rate_limiting_and_monolog.md)**
   - `RateLimiter`를 이용한 도서 검색 분당 30회 Throttling 차단
   - Monolog 일별 로테이션(`daily`) 보안 감사 로깅
   - 감성적인 커스텀 `404.blade.php` 에러 화면 렌더링

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [파일 스토리지 (File Storage)](../docs/05_digging_deeper/filesystem_ko.md)
- [이미지 처리 (Images)](../docs/05_digging_deeper/images_ko.md)
- [미들웨어 (Middleware)](../docs/04_the_basics/middleware_ko.md)
- [에러 핸들링 (Error Handling)](../docs/04_the_basics/errors_ko.md)
- [로깅 (Logging)](../docs/04_the_basics/logging_ko.md)
- [속도 제한 (Rate Limiting)](../docs/05_digging_deeper/rate-limiting_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "도서 표지가 엑스박스로 보일 때는 `php artisan storage:link`를 잊었거나 `.env`의 `APP_URL`이 실제 브라우저 주소와 다를 때 발생한다멍! 확인해 보라멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `php artisan storage:link` 실행 및 심볼릭 링크 연결 확인
- [ ] 도서 표지 이미지 업로드 및 WebP 썸네일 자동 변환 검증
- [ ] `EnsureUserIsAdmin` 미들웨어로 일반 회원 관리자 페이지 접근 차단 확인
- [ ] 백오피스 대시보드(`/admin/dashboard`) 실시간 집계 카드 출력
- [ ] 도서 검색 Rate Limiting 30회 초과 시 429 에러 및 404 커스텀 화면 확인
{% endraw %}
