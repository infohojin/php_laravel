---
layout: docs
title: "08주차: 사용자 인증, 소셜 로그인 & 권한 정책 (Security & Auth)"
---

{% raw %}
# 📖 08주차: 사용자 인증, 소셜 로그인 & 권한 정책 (Security & Auth)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** `MustVerifyEmail` 이메일 인증, `Password::uncompromised()` 보안, 민감 배송지 AES-256 암호화, `ReviewPolicy` 서평 인가, Socialite 소셜 로그인 및 Passport B2B OAuth2 비교  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 고객들이 아이디랑 비밀번호를 입력하고 가입하는 인증 과정은 직접 테이블 만들고 세션 쿠키 구워서 만들어야 해? 그리고 다른 사람의 서평이나 주문서를 훔쳐보는 나쁜 손님은 어떻게 막지?"  
🐱 **지니**: "라라벨에는 **Breeze / Fortify**라는 튼튼한 성벽이 준비되어 있단다! 비밀번호는 안전하게 Bcrypt로 해싱되고, 이메일 소유권도 자동으로 인증하지. 남의 서평을 수정하려는 행위는 **Policy(정책)**라는 문지기를 세워 403 Forbidden으로 단칼에 튕겨내면 된단다!"  
🐶 **토토**: "멍멍! 구글이나 카카오 로그인 버튼 하나 달아주면 손님들이 너무 편해해! Socialite 패키지를 쓰면 5분 만에 연동된다멍!"  

---

## 📑 08주차 상세 강의 목록 (Step-by-Step Lectures)

이번 08주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 독자 회원가입, Bcrypt 해싱 & 이메일 소유권 인증(`MustVerifyEmail`)](./01_authentication_and_verification.md)**
   - 가드(Guards)와 유저 프로바이더 기반 인증 구조
   - `'password' => 'hashed'` 캐스트와 Bcrypt 안전 해싱
   - `MustVerifyEmail` 인터페이스와 이메일 미인증 결제 차단 미들웨어

2. **[02강: 비밀번호 재설정 브로커 & 민감 고객 정보 양방향 암호화(`Crypt`)](./02_passwords_and_encryption.md)**
   - `Password::uncompromised()`를 이용한 다크웹 유출 비밀번호 사전 거부
   - 60분 만료 서명 토큰 기반 비밀번호 찾기/재설정 플로우
   - OpenSSL AES-256-CBC 기반 배송지/연락처 양방향 암호화 및 MAC 변조 방지

3. **[03강: 서평 인가 정책(`ReviewPolicy`) & 관리자 전용 게이트(`Gate`)](./03_authorization_gates_and_policies.md)**
   - 인증(Authentication) vs 인가(Authorization)의 명확한 경계
   - 전역 관리자 접근 제어 `Gate::define('access-admin')`
   - 모델 단위 권한 통제 `ReviewPolicy` 및 Blade `@can('update', $review)`

4. **[04강: Socialite 간편 소셜 로그인 & B2B 제휴사용 Passport OAuth2 아키텍처](./04_socialite_and_oauth_passport.md)**
   - Laravel Socialite를 통한 Google 1초 원클릭 소셜 로그인 파이프라인
   - 신규 고객 자동 가입 및 기존 계정 연동 (`firstOrCreate`)
   - 라라벨 4대 인증 도구 비교: Breeze vs Fortify vs Sanctum vs Passport

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [인증 (Authentication)](../docs/06_security/authentication_ko.md)
- [인가 (Authorization)](../docs/06_security/authorization_ko.md)
- [이메일 인증 (Verification)](../docs/06_security/verification_ko.md)
- [비밀번호 재설정 (Passwords)](../docs/06_security/passwords_ko.md)
- [해싱 (Hashing)](../docs/06_security/hashing_ko.md)
- [암호화 (Encryption)](../docs/06_security/encryption_ko.md)
- [스타터 키트 (Starter Kits)](../docs/02_getting_started/starter-kits_ko.md)
- [Fortify (인증 백엔드)](../docs/11_packages/fortify_ko.md)
- [Socialite (소셜 로그인)](../docs/11_packages/socialite_ko.md)
- [Passport (OAuth2 서버)](../docs/11_packages/passport_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "`.env`의 `APP_KEY`를 실수로 바꿔버리면 암호화된 고객 배송지 주소를 영원히 복호화할 수 없게 되니 절대 변경하면 안 된다멍! 그리고 로컬 테스트할 땐 `MAIL_MAILER=log`로 두면 이메일 링크가 로그 파일에 예쁘게 찍힌다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `User` 모델에 `MustVerifyEmail` 적용 및 가입 후 인증 이메일 발송 확인
- [ ] `Password::uncompromised()`로 유출 비밀번호 방어 테스트
- [ ] 배송지 정보 암호화 저장 및 데이터베이스 암호문 확인
- [ ] `ReviewPolicy` 작성 후 작성자 본인에게만 [수정/삭제] 버튼 노출 확인
- [ ] Socialite 구글 로그인 엔드포인트 및 Passport vs Sanctum 아키텍처 이해
{% endraw %}
