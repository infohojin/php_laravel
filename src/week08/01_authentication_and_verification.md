---
layout: docs
title: "01강: 독자 회원가입, Bcrypt 해싱 & 이메일 소유권 인증(`MustVerifyEmail`)"
---

{% raw %}
# 01강: 독자 회원가입, Bcrypt 해싱 & 이메일 소유권 인증(`MustVerifyEmail`)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 가드와 유저 프로바이더 기반 인증 시스템, Bcrypt 비밀번호 안전 해싱, 가입 고객 이메일 소유권 인증 플로우  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [인증 (Authentication)](../docs/06_security/authentication_ko.md), [해싱 (Hashing)](../docs/06_security/hashing_ko.md), [이메일 인증 (Verification)](../docs/06_security/verification_ko.md), [스타터 키트 (Starter Kits)](../docs/02_getting_started/starter-kits_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객들이 지니샵에 가입할 때 비밀번호를 평문으로 데이터베이스에 저장하면 해킹당했을 때 큰일 나잖아요! 그리고 가짜 이메일 주소로 유령 계정을 마구 생성하는 악성 봇들은 어떻게 막을 수 있나요?"

🐱 **지니**: "도로시, 보안은 모든 이커머스의 생명선이란다! 라라벨의 **`Hash::make()`**는 단방향 솔트(Salt)가 적용된 강력한 **Bcrypt** 알고리즘으로 비밀번호를 암호화하여 슈퍼컴퓨터로도 원본을 알아낼 수 없게 만들지. 그리고 모델에 **`MustVerifyEmail`** 인터페이스 한 줄만 붙여주면, 가입 즉시 서명된 인증 메일을 발송하고 메일함을 확인한 진짜 사람만 책을 구매할 수 있도록 검문소를 세워준단다!"

🐶 **토토**: "멍멍! 인증 폼을 일일이 처음부터 다 짜기 힘들 땐 라라벨 공식 스타터 키트인 **Laravel Breeze**를 깔면 5분 만에 로그인, 회원가입, 비밀번호 찾기 화면이 뚝딱 완성된다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 라라벨의 인증 아키텍처(Guards와 User Providers)의 역할을 이해합니다.
2. `User` 모델에 `MustVerifyEmail`을 구현하고 가입 환영 이메일 인증 메커니즘을 구성합니다.
3. 세션 고정(Session Fixation) 공격을 막는 `Auth::login()`과 `$request->session()->regenerate()`를 실습합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `User` 모델에 이메일 인증 인터페이스 활성화

`app/Models/User.php` 파일을 열고 `MustVerifyEmail` 인터페이스를 활성화합니다:

```php
namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail; // 인터페이스 임포트!
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable implements MustVerifyEmail // 계약 구현!
{
    use HasFactory, Notifiable;

    protected $fillable = [
        'name',
        'email',
        'password',
        'is_admin',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed', // 라라벨 13의 자동 해싱 캐스트!
            'is_admin' => 'boolean',
        ];
    }
}
```

> **지니의 핵심 팁:**  
> `'password' => 'hashed'` 캐스트를 선언해 두면, 개발자가 실수로 `Hash::make()`를 빼먹고 평문 비밀번호를 넣더라도 모델이 알아서 안전한 Bcrypt 해시로 변환해 저장한단다!

---

### [Step 2] 독자 회원가입 및 로그인 컨트롤러 구현

`app/Http/Controllers/AuthController.php` 파일을 생성합니다:

```php
namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Auth\Events\Registered;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    /**
     * 독자 회원가입 처리
     */
    public function register(Request $request)
    {
        $validated = $request->validate([
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'email', 'max:255', 'unique:users'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ]);

        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => $validated['password'], // 'hashed' 캐스트로 자동 해싱!
        ]);

        // 🚀 이메일 인증 안내 메일 자동 발송 이벤트 트리거!
        event(new Registered($user));

        // 가입 즉시 자동 로그인
        Auth::login($user);

        return redirect()->route('verification.notice');
    }

    /**
     * 독자 로그인 처리
     */
    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email' => ['required', 'email'],
            'password' => ['required'],
        ]);

        // 세션 고정 공격 방어를 위한 regenerate()
        if (Auth::attempt($credentials, $request->boolean('remember'))) {
            $request->session()->regenerate();

            return redirect()->intended(route('home'))
                ->with('success', '반갑습니다, ' . Auth::user()->name . ' 독자님!');
        }

        return back()->withErrors([
            'email' => '등록된 이메일 또는 비밀번호가 일치하지 않습니다.',
        ])->onlyInput('email');
    }

    /**
     * 로그아웃 처리
     */
    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect('/')->with('success', '안전하게 로그아웃되었습니다.');
    }
}
```

---

### [Step 3] `verified` 미들웨어로 미인증 고객 차단

도서 주문 결제(`GET /checkout`) 화면은 반드시 이메일 인증을 마친 독자만 접근할 수 있도록 라우트를 보호합니다:

```php
// routes/web.php
Route::get('/checkout', function () {
    return "💳 도서 주문서 작성 및 결제 화면입니다.";
})->middleware(['auth', 'verified'])->name('checkout');
```

만약 이메일 인증 링크를 누르지 않은 독자가 결제 버튼을 누르면, 라라벨이 자동으로 `/email/verify` 이메일 확인 안내 페이지로 리다이렉트합니다!

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `Auth::attempt()`의 내부 동작
1. `users` 테이블에서 입력된 `email`로 사용자를 단 1회 조회합니다.
2. 사용자가 존재하면, 입력된 평문 비밀번호와 DB에 저장된 Bcrypt 해시를 `Hash::check()`로 정밀 대조합니다.
3. 일치할 경우 브라우저 세션에 사용자 ID를 안전하게 암호화하여 저장하고 `true`를 반환합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **로컬 개발할 땐 실제 이메일 발송이 번거로워요!**  
>    `.env` 파일에 `MAIL_MAILER=log` 로 설정해두면 발송된 인증 링크가 `storage/logs/laravel.log` 파일에 텍스트로 찍힌다멍! 링크를 클릭하면 1초 만에 인증이 완료된다멍!

---

## 💡 6. 1강 자가진단 과제

1. 새 계정으로 회원가입을 진행하고 `storage/logs/laravel.log`에서 이메일 인증 링크를 찾아 클릭해 보세요.
2. `users` 테이블의 `email_verified_at` 컬럼에 현재 시각이 정상적으로 기록되는지 확인하세요.
{% endraw %}
