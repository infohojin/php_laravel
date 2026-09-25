---
layout: docs
title: "13주차 02강: 라라벨 생텀(Sanctum) 모바일 API 토큰 인증 & 페넌트(Pennant) 피처 플래그"
---

{% raw %}
# 📖 13주차 02강: 라라벨 생텀(Sanctum) 모바일 API 토큰 인증 & 페넌트(Pennant) 피처 플래그

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 모바일 앱 사용자를 위한 경량 API 토큰 인증(Laravel Sanctum)을 구축하여 기기별 로그인/로그아웃과 세부 권한(Abilities)을 제어하고, Laravel Pennant를 이용해 신규 결제 화면의 A/B 테스트 피처 플래그를 제어합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 모바일 앱 사용자가 로그인했을 때 JWT(Json Web Token)나 OAuth2 복잡한 서버를 직접 구축해야 해? 사용자 기기가 아이폰인지 갤럭시인지 구분해서 원격 로그아웃도 시켜주고 싶은데 너무 복잡해!"  
🐱 **지니**: "도로시, 바로 그럴 때 라라벨 공식 경량 API 인증 도구인 **라라벨 생텀(Laravel Sanctum)**을 쓰는 거란다! `$user->createToken('iPhone 16')` 단 한 줄이면 안전한 해시 기반 개인 액세스 토큰(Personal Access Token)이 발급되고, 기기별 권한 제어와 원격 세션 해제까지 완벽하게 지원하지!"  
🐶 **토토**: "멍멍! 게다가 이번에 모바일 앱 신규 결제창을 일부 고객(50%)에게만 먼저 열어서 구매 전환율을 비교하는 A/B 테스트를 하고 싶다면 **라라벨 페넌트(Pennant)** 피처 플래그가 환상적인 짝꿍이다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **라라벨 생텀 환경 세팅:** `User` 모델에 `HasApiTokens` 트레이트 연동
2. **모바일 로그인 및 토큰 발급:** `POST /api/v1/auth/login` (기기 식별자 및 세부 권한 부여)
3. **토큰별 세부 권한(Abilities) 검증:** `tokenCan('orders:create')` 및 `ability` 미들웨어 적용
4. **원격 기기 로그아웃 및 토큰 만료:** `currentAccessToken()->delete()`
5. **Laravel Pennant를 이용한 신규 결제 플로우 A/B 테스트 연동**

---

## 🛠️ 단계별 실습 절차

### 1단계: Sanctum 패키지 및 User 모델 설정

라라벨 11에서 `php artisan install:api`를 실행했다면 이미 Sanctum이 기본 설치되어 있습니다. `User` 모델에 `HasApiTokens` 트레이트가 포함되어 있는지 확인합니다:

`app/Models/User.php`:

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;
use Laravel\Pennant\Concerns\HasFeatures;

class User extends Authenticatable
{
    use HasApiTokens, Notifiable, HasFeatures;

    // ... 기존 코드 유지
}
```

---

### 2단계: 모바일 로그인 & 토큰 발급 컨트롤러 작성

사용자가 이메일과 비밀번호, 그리고 접속 기기 이름(`device_name`)을 전송하면 인증 후 고유 토큰을 발급하는 컨트롤러를 작성합니다.

`app/Http/Controllers/Api/v1/AuthApiController.php`:

```php
<?php

namespace App\Http\Controllers\Api\v1;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthApiController extends Controller
{
    /**
     * 모바일 앱 로그인 및 토큰 발급
     * POST /api/v1/auth/login
     */
    public function login(Request $request): JsonResponse
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
            'device_name' => 'required|string|max:50', // 예: "Dorothy's iPhone 16"
        ]);

        $user = User::where('email', $request->email)->first();

        if (!$user || !Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['이메일 또는 비밀번호가 일치하지 않습니다.'],
            ]);
        }

        // 1. 일반 독자용 기본 권한(Abilities) 부여
        $abilities = ['books:read', 'orders:create', 'reviews:write'];

        // 관리자인 경우 추가 권한 부여
        if ($user->is_admin) {
            $abilities[] = 'admin:manage';
        }

        // 2. Sanctum 개인 액세스 토큰 발급
        $token = $user->createToken($request->device_name, $abilities);

        return response()->json([
            'message' => '로그인 성공',
            'token_type' => 'Bearer',
            'access_token' => $token->plainTextToken,
            'user' => [
                'id' => $user->id,
                'name' => $user->name,
                'email' => $user->email,
            ],
        ]);
    }

    /**
     * 현재 기기 로그아웃 (현재 토큰 폐기)
     * POST /api/v1/auth/logout
     */
    public function logout(Request $request): JsonResponse
    {
        // 요청에 사용된 현재 토큰만 삭제
        $request->user()->currentAccessToken()->delete();

        return response()->json(['message' => '현재 기기에서 안전하게 로그아웃되었습니다.']);
    }

    /**
     * 모든 다른 기기 원격 일괄 로그아웃
     * POST /api/v1/auth/logout-all
     */
    public function logoutAllDevices(Request $request): JsonResponse
    {
        // 해당 유저의 모든 발급 토큰 일괄 삭제
        $request->user()->tokens()->delete();

        return response()->json(['message' => '모든 연결된 기기에서 일괄 로그아웃되었습니다.']);
    }
}
```

---

### 3단계: Sanctum 보호 라우트 및 권한(Ability) 검증

`routes/api.php`에 `auth:sanctum` 미들웨어로 보호되는 엔드포인트를 등록합니다:

```php
use App\Http\Controllers\Api\v1\AuthApiController;
use App\Http\Controllers\Api\v1\OrderApiController;
use Illuminate\Support\Facades\Route;

Route::prefix('v1')->group(function () {
    // 공개 라우트
    Route::post('/auth/login', [AuthApiController::class, 'login']);

    // Sanctum 인증 필요 라우트
    Route::middleware('auth:sanctum')->group(function () {
        Route::post('/auth/logout', [AuthApiController::class, 'logout']);
        Route::post('/auth/logout-all', [AuthApiController::class, 'logoutAllDevices']);

        // 세부 권한(orders:create)이 있는 토큰만 주문 생성 허용
        Route::post('/orders', [OrderApiController::class, 'store'])
            ->middleware('ability:orders:create');
    });
});
```

컨트롤러 내부에서도 직접 토큰 권한을 검사할 수 있습니다:

```php
if ($request->user()->tokenCan('reviews:write')) {
    // 서평 작성 로직 허용
}
```

---

### 4단계: 모바일 로그인 및 API 호출 cURL 테스트

터미널에서 로그인 및 토큰 기반 요청을 테스트합니다:

```bash
# 1. 로그인하여 Bearer 토큰 획득
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"dorothy@jinyshop.test","password":"secretpassword","device_name":"iPhone 16"}' \
  | jq -r '.access_token')

echo "발급된 토큰: $TOKEN"

# 2. Authorization 헤더를 싣고 보호된 API 호출
curl -s -X POST http://127.0.0.1:8000/api/v1/orders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "quantity": 1}' | jq
```

---

### 5단계: 라라벨 페넌트(Pennant) 피처 플래그로 A/B 테스트 연동

모바일 앱의 특정 신규 기능(예: 간편 원클릭 결제 UI)을 50%의 사용자에게만 오픈하는 피처 플래그를 설정합니다:

```bash
composer require laravel/pennant
php artisan vendor:publish --provider="Laravel\Pennant\PennantServiceProvider"
php artisan migrate
```

`app/Providers/AppServiceProvider.php`에 피처 플래그를 정의합니다:

```php
use Laravel\Pennant\Feature;
use App\Models\User;
use Illuminate\Support\Lottery;

public function boot(): void
{
    // 모바일 원클릭 결제 피처 플래그 (50% 확률로 활성화)
    Feature::define('one-click-checkout', fn (User $user) => 
        Lottery::odds(1, 2)->choose()
    );
}
```

API 응답에 사용자의 피처 활성화 여부를 전달하여 모바일 앱 화면 구성을 동적으로 제어합니다:

```php
// UserApiController.php
public function me(Request $request)
{
    $user = $request->user();

    return response()->json([
        'user' => $user,
        'features' => [
            'one_click_checkout' => Feature::active('one-click-checkout'),
        ],
    ]);
}
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. Sanctum의 두 가지 인증 방식 (SPA vs Mobile API)

| 구분 | SPA 세션 인증 (Next.js / Nuxt / Vue) | 모바일/서드파티 API 토큰 인증 (iOS / Android) |
| :--- | :--- | :--- |
| **인증 수단** | 쿠키(Cookie) 기반 세션 (`laravel_session`, XSRF) | `Authorization: Bearer <token>` 헤더 |
| **CSRF 보호** | 필수 (`/sanctum/csrf-cookie` 호출) | 불필요 (토큰 자체로 인증) |
| **토큰 저장소** | 쿠키 암호화 저장 (브라우저 자동 전송) | 모바일 보안 저장소(Keychain, EncryptedSharedPreferences) |
| **적합 대상** | 서브도메인이 동일한 웹 SPA 프론트엔드 | 네이티브 모바일 앱, 외부 제휴사 배치 스크립트 |

### 2. 토큰 만료 시간(Expiration) 설정

기본적으로 Sanctum 토큰은 영구적입니다. 보안 강화를 위해 만료 시간을 두고 싶다면 `config/sanctum.php`에서 분 단위로 지정할 수 있습니다:

```php
'expiration' => 60 * 24 * 30, // 30일 후 자동 만료
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **Bearer 토큰 분실 및 탈취 대처:**  
   토큰 문자열 원본은 최초 발급 시 단 한 번만 반환되며, DB에는 SHA-256 해시값만 저장됩니다. 따라서 사용자가 토큰을 분실하면 재발급해야 하며, 탈취 의심 시 `tokens()->delete()`로 즉시 무효화할 수 있습니다!
2. **`Accept: application/json` 헤더 누락 시 302 리다이렉트 발생:**  
   인증되지 않은 상태로 API에 접근할 때 클라이언트가 `Accept: application/json` 헤더를 보내지 않으면 라라벨이 웹 로그인 화면(`/login`)으로 302 리다이렉트해 버립니다. 모바일 앱 통신 시 반드시 Accept 헤더를 명시하세요!

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** Sanctum 토큰을 가진 사용자가 특정 권한(Ability)을 가지고 있는지 컨트롤러에서 boolean으로 확인하는 메소드는 무엇일까요?
   - 정답: `$user->tokenCan('권한이름')`
2. **과제:** 지니샵 모바일 앱 독자가 내 계정 설정에서 현재 로그인된 모든 기기 목록(기기명, 최근 접속 일시)을 조회하고, 특정 기기 1건만 골라서 원격 강제 로그아웃시키는 API를 구현해 보세요!
{% endraw %}
