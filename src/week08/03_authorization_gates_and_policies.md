---
layout: docs
title: "03강: 서평 인가 정책(`ReviewPolicy`) & 관리자 전용 게이트(`Gate`)"
---

{% raw %}
# 03강: 서평 인가 정책(`ReviewPolicy`) & 관리자 전용 게이트(`Gate`)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 인증(Authentication) vs 인가(Authorization), 모델 기반 `ReviewPolicy`, 전역 권한 통제 `Gate`, Blade `@can` 지시어  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [인가 (Authorization)](../docs/06_security/authorization_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 로그인을 했다고 해서 남이 쓴 정성스러운 독자 서평을 마음대로 수정하거나 삭제해 버리면 안 되잖아요! '이 서평은 오직 작성자 본인이나 서점 관리자만 수정할 수 있다'는 규칙은 어떻게 우아하게 코드로 보호하나요?"

🐱 **지니**: "도로시, 바로 그것이 **인가(Authorization, 권한 부여)**의 영역이란다! '당신이 누구인가?'를 확인하는 것이 **인증**이라면, '당신이 이 행동을 할 자격이 있는가?'를 판단하는 것이 바로 **인가**이지. 라라벨의 **정책(Policy)** 클래스를 사용하면 `ReviewPolicy` 안에 단 한 줄의 규칙(`$user->id === $review->user_id`)만 적어두면 끝난단다. 권한이 없는 자가 침범하면 라라벨이 단칼에 **`403 Forbidden`** 방패로 막아내지!"

🐶 **토토**: "멍멍! 화면에서도 `@can('update', $review)` 지시어를 쓰면 본인이 쓴 서평에만 [수정/삭제] 버튼이 보이고, 남의 서평에는 버튼 자체가 아예 안 보인다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 관리자 전용 백오피스 접근을 통제하는 클로저 기반 **Gate(`admin-access`)**를 정의합니다.
2. 서평 수정/삭제 권한을 모델 단위로 제어하는 **`ReviewPolicy`**를 작성합니다.
3. 컨트롤러의 `$this->authorize()`와 Blade의 `@can` 지시어로 완벽한 이중 방어선을 구축합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 관리자 전용 Gate 정의 (`AppServiceProvider`)

`app/Providers/AppServiceProvider.php`에 관리자 권한을 판별하는 전역 Gate를 선언합니다:

```php
// app/Providers/AppServiceProvider.php
use Illuminate\Support\Facades\Gate;
use App\Models\User;

public function boot(): void
{
    // 관리자(Admin) 권한 게이트
    Gate::define('access-admin', function (User $user) {
        return (bool) $user->is_admin;
    });

    // 최고 관리자(Super Admin)는 모든 검사를 자동 패스하는 마스터키!
    Gate::before(function (User $user, string $ability) {
        if ($user->email === 'superadmin@jinyshop.com') {
            return true;
        }
    });
}
```

---

### [Step 2] 서평 정책 클래스 생성 (`ReviewPolicy`)

아티산 명령어로 `Review` 모델에 바인딩된 정책을 생성합니다:

```bash
php artisan make:policy ReviewPolicy --model=Review
```

`app/Policies/ReviewPolicy.php`에서 수정(`update`)과 삭제(`delete`) 권한 규칙을 정의합니다:

```php
namespace App\Policies;

use App\Models\Review;
use App\Models\User;

class ReviewPolicy
{
    /**
     * 서평 수정 권한: 본인 작성자이거나 서점 관리자일 때만 허용!
     */
    public function update(User $user, Review $review): bool
    {
        return $user->id === $review->user_id || $user->is_admin;
    }

    /**
     * 서평 삭제 권한
     */
    public function delete(User $user, Review $review): bool
    {
        return $user->id === $review->user_id || $user->is_admin;
    }
}
```

---

### [Step 3] 컨트롤러에서 권한 인가 강제 (`authorize`)

`ReviewController`의 수정 및 삭제 액션에서 정책을 통과하지 못하면 즉시 403 Forbidden을 던지도록 보호합니다:

```php
// app/Http/Controllers/ReviewController.php
use App\Models\Review;
use Illuminate\Http\Request;

public function update(Request $request, Review $review)
{
    // 🛡️ 정책 인가 검사! 불일치 시 라라벨이 자동으로 403 예외 발생!
    $this->authorize('update', $review);

    $validated = $request->validate([
        'rating' => 'required|integer|min:1|max:5',
        'content' => 'required|string|min:5',
    ]);

    $review->update($validated);

    return back()->with('success', '서평이 성공적으로 수정되었습니다.');
}
```

---

### [Step 4] Blade 화면에서 `@can` 지시어로 조건부 버튼 렌더링

도서 상세 화면의 서평 목록에서, 오직 자신이 작성한 서평에만 [수정], [삭제] 버튼이 노출되도록 제어합니다:

```html
<!-- resources/views/books/show.blade.php 서평 루프 내부 -->
@foreach($book->reviews as $review)
    <div class="border-b border-slate-100 py-3 flex justify-between items-start">
        <div>
            <div class="flex items-center space-x-2">
                <span class="text-amber-500 font-bold">★ {{ $review->rating }}점</span>
                <span class="font-semibold text-slate-800 text-sm">{{ $review->reviewer_name }}</span>
            </div>
            <p class="text-slate-600 text-sm mt-1">{{ $review->content }}</p>
        </div>

        <!-- 🔒 인가된 사람에게만 노출되는 액션 버튼! -->
        @can('update', $review)
            <div class="flex space-x-2 text-xs">
                <button class="text-indigo-600 hover:underline">수정</button>
                <form action="/reviews/{{ $review->id }}" method="POST">
                    @csrf
                    @method('DELETE')
                    <button type="submit" class="text-rose-500 hover:underline">삭제</button>
                </form>
            </div>
        @endcan
    </div>
@endforeach
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `Gate::allows()` vs `$this->authorize()`
- `Gate::allows('update', $review)`는 단순히 `true` 또는 `false` 불리언 값을 반환하므로 조건부 if문에 적합합니다.
- 반면 컨트롤러에서 쓰는 `$this->authorize('update', $review)`는 실패 시 즉시 `AuthorizationException`을 던져 실행 흐름을 중단시키고 브라우저에 **403 Forbidden** 응답을 전송하는 완벽한 보안 차단기 역할을 합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **비로그인(Guest) 손님이 서평 페이지를 보면 에러가 나나요?**  
>    라라벨의 Policy는 비로그인 사용자일 경우 기본적으로 모든 권한을 `false`로 차단하므로 에러 없이 안전하게 버튼이 숨겨진다멍!

---

## 💡 6. 3강 자가진단 과제

1. A 사용자로 로그인하여 서평을 작성한 뒤, 로그아웃하고 B 사용자로 로그인했을 때 A의 서평에 [수정] 버튼이 뜨지 않는지 확인하세요.
2. B 사용자가 Postman으로 A의 서평 수정 엔드포인트(`PUT /reviews/{id}`)를 강제 호출했을 때 **403 Forbidden** 에러로 튕겨 나가는지 검증하세요.
{% endraw %}
