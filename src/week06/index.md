---
layout: docs
title: "06주차: Eloquent 데이터 관계(Relationships) 심화 & N+1 해결"
---

{% raw %}
# 📖 06주차: Eloquent 데이터 관계(Relationships) 심화 & N+1 해결

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **주차 요약:** 저자/출판사 1:N 관계, 주문-도서 N:M 피벗(`order_items`), 서평/이미지 다형성(`morphMany`), N+1 쿼리 폭발 진단과 Eager Loading, 대용량 정산용 LazyCollection  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니 & 도로시 & 토토의 개발 회의

👧 **도로시**: "지니, 큰일 났어요! 도서 목록 화면에 저자 이름과 출판사를 같이 띄웠더니, Telescope에서 SQL 쿼리가 100개 넘게 터져 나와서 페이지가 엄청 느려졌어요!"  
🐱 **지니**: "하하, 도로시가 웹 개발자들의 영원한 숙적인 **'N+1 쿼리 폭발 문제'**를 만났구나! 루프를 돌면서 매번 연관 데이터를 따로 질의하기 때문이란다. 이럴 땐 마법 주문 `with(['author', 'publisher'])`를 써서 **즉시 로딩(Eager Loading)**을 해주면 쿼리 3개로 압축할 수 있단다!"  
🐶 **토토**: "멍멍! 회원은 여러 주문을 하고, 주문은 여러 책을 담으니 N:M 피벗 관계가 필요해! 대량 데이터 정산할 땐 `LazyCollection::cursor()`를 써야 메모리가 안 터진다멍!"  

---

## 📑 06주차 상세 강의 목록 (Step-by-Step Lectures)

이번 06주차는 총 4개의 절차적 실습 강의로 구성되어 있습니다. 순서대로 학습을 진행해 주세요:

1. **[01강: 도서 데이터 관계망 — 1:N 관계 & N:M 주문 피벗(Pivot) 테이블](./01_one_to_many_and_many_to_many.md)**
   - `Author` $\leftrightarrow$ `Book`, `Publisher` $\leftrightarrow$ `Book` 1:N 관계 정의
   - `Order` $\leftrightarrow$ `Book` N:M 관계와 `order_items` 피벗 테이블
   - `withPivot('quantity', 'unit_price')`를 활용한 주문 당시 단가와 수량 로드

2. **[02강: 다형성 관계(Polymorphic Relations) — 서평(Review) & 도서 이미지](./02_polymorphic_reviews_and_images.md)**
   - 책과 저자 모두에게 달리는 카멜레온 다형성 서평(`morphMany`, `morphTo`)
   - `reviews` 단일 테이블 스키마와 `reviewable` 인덱스
   - `Relation::enforceMorphMap()`을 통한 데이터베이스 별칭 매핑 최적화

3. **[03강: N+1 쿼리 폭발의 정체 & 즉시 로딩(Eager Loading) 극적 최적화](./03_n_plus_one_and_eager_loading.md)**
   - Telescope를 이용한 61개 N+1 지연 로딩 쿼리 폭발 재현 및 진단
   - `with(['author', 'publisher'])` 즉시 로딩으로 3개 쿼리 압축 (95% 부하 절감)
   - `withCount('reviews')` 서평 개수 최적화 및 `preventLazyLoading` 안전 가드

4. **[04강: 컬렉션(Collections) 함수형 가공 & OOM 방지 지연 컬렉션(LazyCollection)](./04_collections_and_lazy_collections.md)**
   - 컬렉션 고차 함수(`groupBy`, `map`, `sum`, `sortByDesc`) 도서 통계 집계
   - 10만 건 대용량 주문 처리 시 OOM(Out of Memory) 메모리 고갈 원인
   - PHP 제너레이터 기반 `Book::cursor()`를 이용한 메모리 10MB 미만 스트리밍 정산

---

## 📚 연계 공식 문서 (한국어 번역본 대조 학습)

이번 주차 실습에서 다루는 기능의 공식 문서 원본 내용과 심화 레퍼런스입니다:

- [Eloquent 관계 (Eloquent Relationships)](../docs/08_eloquent_orm/eloquent-relationships_ko.md)
- [Eloquent 컬렉션 (Eloquent Collections)](../docs/08_eloquent_orm/eloquent-collections_ko.md)
- [컬렉션 심화 (Collections)](../docs/05_digging_deeper/collections_ko.md)

---

## 🐶 토토의 실무 꿀팁 & 에러 방지 가이드

> 🐶 **토토의 알짜 팁!**  
> "로컬 개발 중 N+1 실수를 자동으로 잡으려면 `AppServiceProvider`에 `Model::preventLazyLoading(! app()->isProduction())`을 꼭 켜둬! 즉시 로딩을 빼먹는 순간 빨간 에러 화면이 떠서 실수를 원천 차단해 준다멍!"

---

## ✅ 이번 주차 실습 완료 체크리스트

- [ ] 저자-도서, 출판사-도서 1:N 관계 정의 및 Tinker 역방향 탐색 확인
- [ ] `order_items` 피벗 테이블 생성 및 `attach()`로 도서 수량/단가 연동
- [ ] 다형성 서평(`Review`) 작성 및 `enforceMorphMap` 동작 검증
- [ ] 도서 목록 화면에서 Telescope를 통해 N+1 쿼리가 3~4개로 최적화되었는지 확인
- [ ] `Book::cursor()`를 이용한 스트리밍 정산으로 메모리 증가량 0MB 확인
{% endraw %}
