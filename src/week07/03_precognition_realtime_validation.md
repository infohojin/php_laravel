---
layout: docs
title: "03강: 라라벨 프리코그니션(Precognition) — 실시간 인라인 검증 UX"
---

{% raw %}
# 03강: 라라벨 프리코그니션(Precognition) — 실시간 인라인 검증 UX

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 폼을 제출하기 전에 미리 검증하는 Laravel Precognition 아키텍처, `Precognition: true` 헤더, 실시간 입력창 에러 안내  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Precognition (실시간 유효성 검사)](../docs/11_packages/precognition_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 도서 배송지 주소나 수량을 입력할 때, 폼 제출 버튼을 누르기 전까지는 자기가 오타를 냈는지 알 수 없잖아요. 버튼을 누르고 화면이 새로고침된 뒤에야 빨간 글씨로 '주소가 잘못되었습니다'라고 뜨면 손님 입장에서 너무 답답해요! 사용자가 타이핑하는 도중에 백엔드의 강력한 검증 룰로 즉시 확인해 줄 수는 없나요?"

🐱 **지니**: "도로시, 바로 그 현대적 웹 UX의 정점이 **라라벨 프리코그니션(Precognition, 예지 능력)**이란다! 프론트엔드가 백엔드로 요청을 보낼 때 `Precognition: true`라는 비밀 헤더를 실어 보내면, 라라벨은 백엔드의 Form Request 검증만 은밀히 실행하고 컨트롤러는 실행하지 않은 채 '통과!' 또는 '실패 에러'만 0.05초 만에 알려준단다. 중복 코드 없이 단 하나의 Form Request로 프론트와 백엔드가 완벽히 동기화되지!"

🐶 **토토**: "멍멍! 자바스크립트 쪽에서 복잡한 유효성 검증 정규식을 따로 짤 필요 없이, 라라벨 백엔드의 룰을 그대로 실시간으로 당겨 쓸 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. Laravel Precognition의 동작 원리(HTTP 헤더와 204 No Content / 422 응답)를 이해합니다.
2. Alpine.js 또는 바닐라 자바스크립트로 입력창 블러(`blur`) 시 실시간 유효성 피드백을 구현합니다.
3. 동일한 Form Request 클래스 하나로 일반 제출과 사전 검증을 동시에 처리합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] Precognition 미들웨어 등록

`bootstrap/app.php`에서 Precognition 전용 미들웨어가 웹 그룹에 활성화되어 있는지 확인합니다:

```php
// bootstrap/app.php
use Illuminate\Foundation\Configuration\Middleware;

->withMiddleware(function (Middleware $middleware) {
    // 라라벨 13에서는 웹 라우트에 HandlePrecognitiveRequests 미들웨어가 기본 지원됩니다.
})
```

---

### [Step 2] 주문서 작성 전용 `CheckoutRequest` 생성

고객의 배송지 정보(수령인, 연락처, 주소)를 검증하는 Form Request를 생성합니다:

```bash
php artisan make:request CheckoutRequest
```

```php
// app/Http/Requests/CheckoutRequest.php
namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class CheckoutRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'recipient_name' => ['required', 'string', 'min:2', 'max:20'],
            'recipient_phone' => ['required', 'regex:/^01[0-9]-[0-9]{3,4}-[0-9]{4}$/'],
            'postal_code' => ['required', 'digits:5'],
            'shipping_address' => ['required', 'string', 'min:5'],
        ];
    }

    public function messages(): array
    {
        return [
            'recipient_name.min' => '수령인 성함은 최소 2글자 이상 입력해 주세요.',
            'recipient_phone.regex' => '연락처는 010-0000-0000 형식으로 입력해 주세요.',
            'postal_code.digits' => '우편번호는 5자리 숫자여야 합니다.',
            'shipping_address.min' => '상세 주소를 정확히 입력해 주세요.',
        ];
    }
}
```

---

### [Step 3] 브라우저 개발자 도구(Fetch)로 Precognition 테스트

브라우저 콘솔에서 `Precognition: true` 헤더를 붙여 비동기 검증 요청을 날려봅니다:

```javascript
// 잘못된 전화번호 형식으로 사전 검증 질의
fetch('/checkout/validate', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]').content,
        'Precognition': 'true', // 🚀 프리코그니션 마법 헤더!
        'Precognition-Validate-Only': 'recipient_phone' // 연락처 컬럼만 단독 검증!
    },
    body: JSON.stringify({
        recipient_phone: '12345'
    })
})
.then(res => res.json())
.then(data => console.log('검증 피드백:', data));
```

> **콘솔 출력 결과 (HTTP 422):**
> ```json
> {
>   "message": "연락처는 010-0000-0000 형식으로 입력해 주세요.",
>   "errors": {
>     "recipient_phone": ["연락처는 010-0000-0000 형식으로 입력해 주세요."]
>   }
> }
> ```
> 올바른 전화번호(`010-1234-5678`)를 넣으면 데이터베이스 쓰기 없이 **HTTP 204 No Content (성공)**를 즉시 반환합니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `Precognition-Validate-Only` 헤더의 위력
- 10개의 입력창이 있는 큰 주문서에서 사용자가 '전화번호'를 입력하고 다음 칸으로 탭(Tab) 키를 눌렀을 때, 아직 입력하지도 않은 '주소'나 '우편번호'까지 빨간 에러를 띄우면 사용자가 당황합니다.
- `Precognition-Validate-Only: recipient_phone` 헤더를 함께 전송하면, 라라벨은 다른 규칙들은 모두 무시하고 **오직 사용자가 방금 건드린 입력 필드 하나만 정밀 검증**해 주는 스마트함을 보여줍니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **프리코그니션 중에는 결제 API나 이메일이 발송되면 안 되잖아요!**  
>    컨트롤러 내부에서 `if ($request->isPrecognitive()) { ... }` 조건문을 쓰거나 Form Request를 쓰면, 사전 검증 요청일 때는 비즈니스 로직 실행이 원천 차단되니 안심하라멍!

---

## 💡 6. 3강 자가진단 과제

1. 도서 배송지 입력창에서 전화번호를 한 글자씩 칠 때마다 유효성 에러 메시지가 사라졌다 나타났다 하는 인라인 반응형 폼을 테스트해 보세요.
2. 모든 입력이 올바를 때 HTTP 상태 코드 204가 떨어지는지 브라우저 네트워크 탭에서 확인하세요.
{% endraw %}
