---
layout: docs
title: "04강: 에이전트 개발(Agentic Dev) & Laravel Boost 연동"
---

{% raw %}
# 04강: 에이전트 개발(Agentic Dev) & Laravel Boost 연동

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 라라벨 13의 공식 AI 에이전트 개발 가이드, Laravel Boost를 활용한 프로젝트 컨텍스트 연동  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [에이전트 개발 (Agentic Development)](../docs/02_getting_started/ai_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 요즘 AI 코딩 도구들이 정말 똑똑하잖아요. 그런데 AI한테 '라라벨 13으로 도서 쇼핑몰 만들어줘'라고 시키면, 종종 라라벨 8이나 9 시절의 옛날 문법을 알려주거나 없는 함수를 지어내서 헷갈려요!"

🐱 **지니**: "도로시의 관찰력이 아주 예리하구나! 일반적인 범용 LLM은 수년 전 과거 데이터를 학습했기 때문에, 라라벨 13의 최신 슬림 아키텍처나 신규 문법을 잘 모를 수 있단다. 그래서 라라벨 팀에서는 공식적으로 **Agentic Development(에이전트 개발)** 지침과 **Laravel Boost** 도구를 발표했지! 프로젝트의 모델 구조, 최신 문서 컨텍스트를 AI 에이전트에게 주입하여 거짓말(환각) 없이 100% 라라벨 13 표준 코드를 작성하도록 만드는 비결이란다!"

🐶 **토토**: "멍멍! AI가 우리 지니샵의 `Book` 모델과 `Order` 모델을 완벽하게 이해하고 코드를 짜주니까 개발 속도가 10배 빨라진다멍! 도로시의 코딩 조수가 하나 더 생긴 셈이다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨 공식 문서가 권장하는 AI 에이전트 협업 원칙(Agentic Development)을 학습합니다.
2. AI가 우리 프로젝트를 정확히 이해할 수 있도록 시스템 프롬프트 및 컨텍스트 규칙을 구성합니다.
3. 지니샵 도서 모델 설계를 위한 AI 프롬프트 엔지니어링 실습을 진행합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 프로젝트 루트에 `.cursorrules` 또는 `AGENTS.md` 지침 마련

AI 코딩 어시스턴트(Cursor, Copilot, Antigravity 등)가 항상 라라벨 13 표준을 따르도록 프로젝트 루트에 지침 파일을 정의합니다.

```markdown
# JinyShop Laravel 13 Development Rules for AI Agents

## Tech Stack
- Framework: Laravel 13.x (PHP 8.2+)
- Project: JinyShop (Online Bookstore E-Commerce)
- Frontend: Blade Templates + Tailwind CSS + Alpine.js
- Testing: Pest PHP

## Architecture Principles
1. Always use modern Laravel 13 syntax. (No app/Http/Kernel.php; use bootstrap/app.php).
2. Follow Eloquent Active Record conventions:
   - Use casts() method instead of protected $casts property.
   - Use Form Request classes for input validation.
   - Guard against N+1 queries using Eager Loading (with()).
3. Keep controllers thin; delegate domain logic to Services or Actions.
4. Always write clean, PSR-12 compliant code verified by Laravel Pint.
```

---

### [Step 2] 도서 쇼핑몰 스키마 설계를 위한 AI 대화 실습

지니샵의 도서(`Book`) 엔티티를 설계하기 위해 AI에게 라라벨 13 문법 기반의 마이그레이션과 모델 생성을 요청해 봅니다.

> **실제 프롬프트 예시:**
> ```text
> 라라벨 13 문법에 맞추어 온라인 서점 지니샵(JinyShop)의 books 테이블 마이그레이션과
> Book Eloquent 모델 코드를 작성해 줘.
> 
> [요구 조건]
> 1. 컬럼: isbn(13자리 고유), title, slug, price, sale_price, stock_quantity, format(paperback/ebook), status, published_at
> 2. casts() 메서드를 사용하여 published_at은 datetime, format은 Enum으로 캐스팅
> 3. 소프트 삭제(SoftDeletes) 트레이트 적용
> 4. 가격(price)을 원화 포맷('15,000원')으로 반환하는 접근자(Accessor) 정의
> ```

---

### [Step 3] AI가 생성한 코드 검토 및 Pint 정렬

AI가 코드를 작성한 후에는 반드시 개발자가 직접 다음 사항을 점검하고 Pint를 실행합니다:

```bash
# 1. 문법 검사 및 코드 스타일 교정
./vendor/bin/pint

# 2. 아티산으로 구문 오류(Syntax Error) 없는지 확인
php artisan route:list
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### AI 시대의 올바른 개발자 자세 (Human-in-the-Loop)
- 라라벨 창시자 테일러 오트웰(Taylor Otwell)은 AI 도구를 사용할 때 가장 중요한 것은 **"라라벨의 기본 원리를 정확히 아는 개발자의 감수성"**이라고 강조합니다.
- AI가 제안한 코드가 서비스 컨테이너, 미들웨어 생명주기, Eloquent 관계 규약에 맞는지 분별할 수 있어야만 진정한 시니어 개발자로 도약할 수 있습니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **AI가 옛날 문법을 알려줄 땐 어떻게 하나요?**  
>    "라라벨 13의 `bootstrap/app.php`와 `casts()` 메서드 문법을 적용해줘"라고 버전을 콕 짚어서 지시하라멍!
> 
> 2. **AI가 `.env` 파일의 비밀 키를 물어봐요!**  
>    절대로 실제 DB 비밀번호나 결제 Secret Key를 프롬프트에 넣으면 안 된다멍! 항상 `dummy_secret` 같은 가짜 값을 쓰라멍!

---

## 💡 6. 4강 자가진단 과제

1. 지니샵 프로젝트에 사용할 도서 카테고리(`Category`) 모델과 마이그레이션 스키마를 AI와 페어 프로그래밍하여 초안을 작성해 보세요.
2. 작성된 코드를 `./vendor/bin/pint`로 돌려서 아무런 에러 없이 완벽히 통과하는지 확인하세요.
{% endraw %}
