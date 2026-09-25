---
layout: docs
title: "04강: Socialite 간편 소셜 로그인 & B2B 제휴사용 Passport OAuth2 아키텍처"
---

{% raw %}
# 04강: Socialite 간편 소셜 로그인 & B2B 제휴사용 Passport OAuth2 아키텍처

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** Laravel Socialite(구글/카카오 1초 원클릭 로그인), 헤드리스 인증 Fortify, 외부 제휴사 연동을 위한 Passport OAuth2 서버 비교  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [Socialite (소셜 로그인)](../docs/11_packages/socialite_ko.md), [Fortify (인증 백엔드)](../docs/11_packages/fortify_ko.md), [Passport (OAuth2 서버)](../docs/11_packages/passport_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객들이 회원가입할 때 복잡하게 이메일이랑 비밀번호 8자리를 치는 걸 귀찮아해서 그냥 나가버려요! '구글로 1초 만에 시작하기'나 '카카오 로그인' 버튼을 달아줄 수는 없나요? 그리고 나중에 대형 공공도서관이나 기업 서적 제휴사들이 우리 지니샵 시스템과 B2B로 안전하게 연동하려면 어떤 인증 표준을 써야 해요?"

🐱 **지니**: "도로시가 독자들의 편의성과 엔터프라이즈 B2B 시장까지 내다보았구나! 개인 독자를 위한 간편 로그인은 **Laravel Socialite** 패키지를 쓰면 단 2개의 라우트와 10줄의 코드로 구글, 깃허브, 카카오 OAuth2 연동을 끝낼 수 있단다. 그리고 대기업이나 외부 기관과 제휴할 때는 **Laravel Passport**를 써서 우리 지니샵을 네이버나 구글처럼 독립된 정식 **OAuth2 인증 서버**로 격상시킬 수 있지!"

🐶 **토토**: "멍멍! SPA나 모바일 앱 개발할 때 화면 없이 순수 백엔드 인증 로직만 필요하다면 **Laravel Fortify**를 쓰는 것도 똑똑한 방법이다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. Laravel Socialite를 활용해 소셜 로그인 리다이렉트 및 콜백 수신 파이프라인을 구축합니다.
2. 소셜 계정으로 처음 접속한 독자를 자동으로 회원가입시키고 기존 계정과 연동(`firstOrCreate`)합니다.
3. 라라벨의 3대 인증 생태계(Breeze vs Fortify vs Passport vs Sanctum)의 적재적소 선택 기준을 정립합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] Laravel Socialite 패키지 설치

터미널에서 공식 소셜 로그인 패키지를 설치합니다:

```bash
composer require laravel/socialite
```

`config/services.php`에 OAuth 클라이언트 키를 등록합니다:

```php
// config/services.php
'google' => [
    'client_id' => env('GOOGLE_CLIENT_ID'),
    'client_secret' => env('GOOGLE_CLIENT_SECRET'),
    'redirect' => env('APP_URL') . '/auth/google/callback',
],
'github' => [
    'client_id' => env('GITHUB_CLIENT_ID'),
    'client_secret' => env('GITHUB_CLIENT_SECRET'),
    'redirect' => env('APP_URL') . '/auth/github/callback',
],
```

---

### [Step 2] 소셜 로그인 컨트롤러 및 라우트 구현

```bash
php artisan make:controller SocialAuthController
```

```php
// app/Http/Controllers/SocialAuthController.php
namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Str;
use Laravel\Socialite\Facades\Socialite;

class SocialAuthController extends Controller
{
    /**
     * 1. 소셜 프로바이더 로그인 페이지로 리다이렉트
     */
    public function redirect(string $provider)
    {
        return Socialite::driver($provider)->redirect();
    }

    /**
     * 2. 로그인 완료 후 인증 토큰 콜백 수신
     */
    public function callback(string $provider)
    {
        try {
            // 소셜 프로바이더로부터 독자 프로필 획득
            $socialUser = Socialite::driver($provider)->user();

            // 이메일 기준으로 기존 회원을 찾거나 신규 독자 자동 생성!
            $user = User::firstOrCreate(
                ['email' => $socialUser->getEmail()],
                [
                    'name' => $socialUser->getName() ?? $socialUser->getNickname() ?? '지니샵 독자',
                    'password' => Str::random(24), // 랜덤 비밀번호로 보호
                    'email_verified_at' => now(),  // 소셜 인증 완료 계정은 즉시 인증 처리!
                ]
            );

            // 로그인 세션 발급
            Auth::login($user, remember: true);

            return redirect()->route('home')
                ->with('success', "🎉 {$provider} 계정으로 안전하게 로그인되었습니다!");
        } catch (\Throwable $e) {
            return redirect()->route('home')
                ->with('error', '소셜 로그인 중 오류가 발생했습니다: ' . $e->getMessage());
        }
    }
}
```

`routes/web.php`에 연결:
```php
use App\Http\Controllers\SocialAuthController;

Route::get('/auth/{provider}/redirect', [SocialAuthController::class, 'redirect'])->name('social.redirect');
Route::get('/auth/{provider}/callback', [SocialAuthController::class, 'callback'])->name('social.callback');
```

---

### [Step 3] Blade 로그인 화면에 원클릭 소셜 버튼 배치

```html
<!-- 구글 간편 로그인 버튼 -->
<a href="{{ route('social.redirect', 'google') }}" 
   class="w-full flex items-center justify-center space-x-3 py-2.5 border border-slate-300 rounded-xl hover:bg-slate-50 transition shadow-sm font-medium text-slate-700 text-sm">
    <span>🌐</span>
    <span>Google 계정으로 1초 만에 시작하기</span>
</a>
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 라라벨 인증 도구 4대 천왕 비교
| 도구 | 주요 용도 및 아키텍처 | 적합한 시나리오 |
| :--- | :--- | :--- |
| **Laravel Breeze** | Blade / Vue / React 기반의 가볍고 직관적인 스타터 키트 | 대부분의 표준 웹 쇼핑몰 (지니샵 채택) |
| **Laravel Fortify** | 뷰가 없는 순수 백엔드 인증 컨트롤러 (2FA 이중 인증 내장) | 커스텀 모바일 앱 백엔드, 독자적인 프론트엔드 분리 팀 |
| **Laravel Sanctum** | SPA 쿠키 인증 및 모바일 앱용 경량 API 토큰 발급 | 지니샵 모바일 앱 및 가벼운 내부 API (13주차 실습) |
| **Laravel Passport** | 완전한 RFC 6749 OAuth2 서버 (Client Credentials, Refresh Token) | 공공도서관, 대학, B2B 제휴사 전용 대규모 API 게이트웨이 |

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **소셜 로그인 시 `InvalidStateException` 에러가 나요!**  
>    CSRF 공격 방지용 `state` 세션 쿠키가 누락되었기 때문이다멍! 로컬 테스트 중 도메인이 바뀌거나 시크릿 모드에서 브라우저 쿠키를 차단하지 않았는지 확인하라멍!

---

## 💡 6. 4강 자가진단 과제

1. `Socialite::driver('github')->stateless()->user()`를 사용하는 이유(REST API나 모바일 앱 환경)를 공식 문서에서 찾아보세요.
2. Sanctum과 Passport의 결정적 차이(가벼운 단일 앱 토큰 vs 제3자 인가 OAuth2 서버)를 정리해 보세요.
{% endraw %}
