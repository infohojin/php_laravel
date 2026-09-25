---
layout: docs
title: "05주차: Eloquent ORM 기초 & 도서 카탈로그 및 페이징"
---

{% raw %}
# 📖 05주차: Eloquent ORM 기초 & 도서 카탈로그 및 페이징

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** Eloquent Active Record 모델, `casts()`와 접근자/뮤테이터, 로컬 쿼리 스코프, 1,000권 도서 페이지네이션 및 소프트 삭제 복구  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니! 데이터베이스에서 책을 가져올 때 길고 복잡한 SQL 문을 직접 쓰지 않고도 `Book::published()->inStock()->get()` 처럼 쓸 수 있다니 마법 같아요!"  
🐱 **지니**: "그게 바로 라라벨이 자랑하는 **Eloquent Active Record 패턴**이란다! 데이터베이스 테이블 한 행이 PHP 객체 하나와 일대일로 연결되어, 메서드 체이닝만으로 정렬과 검색, 수정, 저장을 자유자재로 다룰 수 있지."  
🐶 **토토**: "멍멍! 책을 실수로 삭제해도 `SoftDeletes`를 켜두면 복구할 수 있어! 그리고 책 이름을 영어 URL 슬러그로 바꿀 땐 `Str::slug()`를 쓰면 된다멍!"  

---

## 📑 05주차 상세 강의 목록 (Step-by-Step Lectures)

이번 05주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: Eloquent 모델, `casts()` 메서드 & 가격/할인율 접근자(Accessors)](./01_eloquent_model_and_casts.md)**
   - `Book` 모델 구조와 `$fillable` 보안 가드
   - 라라벨 13 표준 `casts()` 메서드를 통한 날짜/정수 캐스팅
   - 원화 포맷팅(`formatted_price`) 및 실시간 할인율(`discount_rate`) 접근자

2. **[02강: 쿼리 스코프(Query Scopes) & 도서 다중 필터링/정렬 체이닝](./02_query_scopes_and_filtering.md)**
   - 비즈니스 조건 캡슐화: `scopePublished()`, `scopeInStock()`, `scopeDiscounted()`
   - `when()` 플루언트 헬퍼를 활용한 카테고리/검색어 다중 동적 결합
   - 인기순, 신간순, 가격순 다중 정렬 파이프라인

3. **[03강: 대용량 1,000권 페이지네이션(Pagination) & 커서 페이징(Cursor)](./03_pagination_and_cursor.md)**
   - `paginate(12)->withQueryString()`을 이용한 도서 카탈로그 페이징
   - Tailwind CSS 기반 페이지 내비게이션 바 출력
   - 모바일 무한 스크롤을 위한 고성능 `cursorPaginate()` 아키텍처

4. **[04강: SEO 친화적 슬러그(`Str::slug`) & 소프트 삭제(`SoftDeletes`) 복구](./04_soft_deletes_and_slugs.md)**
   - `Str::slug()` 및 모델 라이프사이클 이벤트를 통한 URL 슬러그 자동 생성
   - 라우트 모델 바인딩 커스텀 키 (`/books/{book:slug}`)
   - 소프트 삭제 수명주기: `trashed()`, `restore()`, `forceDelete()`

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [Eloquent 시작하기 (Eloquent)](../docs/08_eloquent_orm/eloquent_ko.md)
- [쿼리 빌더 (Queries)](../docs/07_database/queries_ko.md)
- [페이지네이션 (Pagination)](../docs/07_database/pagination_ko.md)
- [뮤테이터와 캐스트 (Mutators & Casts)](../docs/08_eloquent_orm/eloquent-mutators_ko.md)
- [문자열 조작 (Strings)](../docs/05_digging_deeper/strings_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "검색 쿼리가 포함된 상태에서 2페이지로 넘어갈 때 검색어가 날아가지 않게 하려면 페이징 쿼리 뒤에 꼭 `->withQueryString()`을 체이닝해 줘야 한다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] `Book` 모델에 `$fillable` 및 `casts()` 정의 완료
- [ ] 가격 원화 표시 및 할인율 계산 접근자 동작 검증
- [ ] 5대 쿼리 스코프를 조립하여 도서 다중 필터 검색 테스트
- [ ] 12권 단위 페이지네이션 바 출력 및 페이지 전환 확인
- [ ] 도서 슬러그 라우트 모델 바인딩 및 소프트 삭제 복구(`restore`) 실습 완료
{% endraw %}
