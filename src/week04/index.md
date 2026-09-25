---
layout: docs
title: "04주차: 데이터베이스 마이그레이션과 시딩 (데이터 모델링)"
---

{% raw %}
# 📖 04주차: 데이터베이스 마이그레이션과 시딩 (데이터 모델링)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** SQLite/MySQL 연결, 트랜잭션 ACID, 출판사/저자/카테고리/도서 스키마 마이그레이션, Faker 팩토리 및 1,000권 도서 대량 시딩  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 우리 지니샵에 상품 종류가 수천 개는 될 텐데, DB 테이블을 만들다가 컬럼을 깜빡하면 어떻게 해? DB를 통째로 지우고 다시 만들어야 하나?"  
🐱 **지니**: "걱정 마렴 도로시! 라라벨에는 **마이그레이션(Migration)**이라는 데이터베이스 전용 타임머신이 있단다. 코드 형태로 테이블 변경 이력을 기록하기 때문에 언제든 뒤로 롤백하거나 최신 상태로 되돌릴 수 있지."  
🐶 **토토**: "멍멍! 게다가 Faker 팩토리와 시더(Seeder)를 실행하면, 눈 깜짝할 사이에 1,000개의 알록달록한 한국어 가짜 도서 데이터가 촤르륵 채워진다멍!"  

---

## 📑 04주차 상세 강의 목록 (Step-by-Step Lectures)

이번 04주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 라라벨 데이터베이스 연결 & 트랜잭션(ACID)의 원리](./01_database_config_and_connections.md)**
   - `.env` 데이터베이스 드라이버(SQLite/MySQL) 설정
   - 원시 쿼리 실행 및 `db:show` 점검
   - `DB::transaction()`을 이용한 도서 결제 및 재고 차감의 원자성(ACID) 보장

2. **[02강: 도서 서점 핵심 스키마 마이그레이션(Migration) 설계](./02_bookstore_schema_migrations.md)**
   - `publishers`, `authors`, `categories`, `books` 테이블 스키마 작성
   - 외래키(Foreign Key) 제약조건 및 복합 인덱스 설정
   - `softDeletes()`를 활용한 품절/절판 도서의 소프트 삭제 보존

3. **[03강: Faker 한국어 팩토리 & 1,000권 도서 데이터 생성 공장](./03_faker_model_factories.md)**
   - Eloquent Model Factory와 Faker 한국어 로케일 설정
   - 고유 13자리 ISBN-13, 도서 제목, 정가, 출간일 자동 생성
   - 팩토리 상태(State) 메서드 (`discounted`, `ebook`, `outOfStock`)

4. **[04강: 데이터베이스 시더(Seeder) & 1,000권 도서 한 방 구축 (`migrate:fresh --seed`)](./04_database_seeder_and_fresh.md)**
   - 대분류/소분류 계층형 `CategorySeeder` 구현
   - 15개 출판사, 40명 저자, 1,000권 도서 대량 `BookSeeder`
   - `php artisan migrate:fresh --seed` 원클릭 데이터베이스 완전 초기화

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [데이터베이스 시작하기 (Database)](../docs/07_database/database_ko.md)
- [마이그레이션 (Migrations)](../docs/07_database/migrations_ko.md)
- [시딩 (Seeding)](../docs/07_database/seeding_ko.md)
- [Eloquent 팩토리 (Eloquent Factories)](../docs/08_eloquent_orm/eloquent-factories_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "시더를 실행하다가 외래키 에러가 날 때는, 부모 테이블인 카테고리와 출판사가 먼저 생성된 후에 자식인 책 데이터가 들어가야 해! `DatabaseSeeder.php`의 `$this->call()` 순서를 꼭 확인하라멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `.env` 데이터베이스 드라이버 연결 및 `php artisan db:show` 정상 출력 확인
- [ ] `DB::transaction()` 롤백 시뮬레이션 동작 검증
- [ ] `publishers`, `authors`, `categories`, `books` 4종 마이그레이션 생성 및 `migrate:status` 확인
- [ ] Faker 한국어 팩토리로 도서/저자/출판사 정의 완료
- [ ] `php artisan migrate:fresh --seed`로 1,000권 도서 데이터 일괄 적재 성공
{% endraw %}
