---
layout: docs
title: "02강: 비밀번호 재설정 브로커 & 민감 고객 정보 양방향 암호화(`Crypt`)"
---

{% raw %}
# 02강: 비밀번호 재설정 브로커 & 민감 고객 정보 양방향 암호화(`Crypt`)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 유출 비밀번호 검사(`Password::uncompromised()`), 토큰 기반 비밀번호 재설정, 고객 배송지 정보 AES-256 양방향 암호화  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [비밀번호 재설정 (Passwords)](../docs/06_security/passwords_ko.md), [암호화 (Encryption)](../docs/06_security/encryption_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 비밀번호를 잊어버렸을 때 '비밀번호 찾기' 링크를 보내주려면 어떻게 해야 해요? 그리고 고객의 실명, 휴대전화 번호, 상세 배송지 주소 같은 개인정보보호법상 민감한 정보는 데이터베이스에 평문으로 두면 해킹당했을 때 큰일 나잖아요! 비밀번호처럼 해싱해버리면 택배 기사님께 주소를 출력해 드릴 수가 없고요!"

🐱 **지니**: "도로시의 보안 감각이 일취월장했구나! 비밀번호는 **단방향 해싱(복호화 불가)**이 맞지만, 배송지 주소나 전화번호는 필요할 때 복호화해서 읽어야 하므로 **양방향 암호화(Encryption)**를 써야 한단다! 라라벨의 `Crypt` 파사드는 미국 정부 표준인 **OpenSSL AES-256-CBC** 알고리즘과 메시지 인증 코드(MAC)를 사용하여, `.env`의 `APP_KEY`를 모르면 데이터베이스 관리자도 주소를 절대 훔쳐볼 수 없게 암호화해 준단다!"

🐶 **토토**: "멍멍! 모델에서 `'shipping_address' => 'encrypted'` 라고 캐스팅 한 줄만 적어두면, 저장할 때 알아서 암호화되고 불러올 때 알아서 복호화된다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 이미 다크웹 등에 유출된 적이 있는 취약한 비밀번호를 사전 차단하는 `Password::uncompromised()` 규칙을 실습합니다.
2. 60분 만료 서명 토큰 기반의 비밀번호 재설정(Password Reset) 플로우를 구축합니다.
3. 고객의 민감한 도서 배송지 정보를 AES-256으로 암호화하여 저장하고 안전하게 복호화합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 강력한 비밀번호 규칙 적용 (`Password::min(8)`)

가입 및 비밀번호 변경 폼에서 해킹당하기 쉬운 단순 비밀번호를 엄격히 필터링합니다:

```php
use Illuminate\Validation\Rules\Password;

$request->validate([
    'password' => [
        'required',
        'confirmed',
        Password::min(8)
            ->letters()        // 문자 포함
            ->mixedCase()      // 대소문자 혼합
            ->numbers()        // 숫자 포함
            ->symbols()        // 특수문자 포함
            ->uncompromised(), // 🚀 HaveIBeenPwned 유출 DB와 대조하여 유출된 비밀번호 즉시 거부!
    ],
]);
```

> **토토의 감탄:** `Password::uncompromised()`는 `password123` 처럼 과거 다른 사이트에서 유출된 유명한 비밀번호를 k-익명성(k-Anonymity) 기법으로 즉각 감지해 낸다멍!

---

### [Step 2] 고객 배송지 정보 양방향 암호화 모델링

`User` 모델에 고객의 기본 배송지 주소와 비상 연락처를 암호화하여 저장하도록 설정합니다:

```php
// app/Models/User.php
protected function casts(): array
{
    return [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',
        
        // 🔒 민감 정보 양방향 암호화 캐스트!
        'phone_number' => 'encrypted',
        'default_shipping_address' => 'encrypted',
    ];
}
```

---

### [Step 3] Tinker에서 암호화 저장 및 복호화 검증

```bash
php artisan tinker
```

```php
// 1. 사용자 정보에 민감 배송지 입력 후 저장
$user = App\Models\User::first();
$user->phone_number = '010-1234-5678';
$user->default_shipping_address = '서울특별시 강남구 테헤란로 123 지니빌딩 401호';
$user->save();

// 2. 실제 데이터베이스 테이블에 저장된 원시 값 조회 (DB 파사드 활용)
$raw = DB::table('users')->where('id', $user->id)->first();
echo "DB에 저장된 암호문: " . substr($raw->default_shipping_address, 0, 40) . "... (외계어로 암호화됨)" . PHP_EOL;

// 3. 모델을 통해 조회할 때 (라라벨이 자동 복호화!)
$freshUser = App\Models\User::find($user->id);
echo "자동 복호화된 주소: " . $freshUser->default_shipping_address . PHP_EOL;
```

> **출력 결과:**
> ```text
> DB에 저장된 암호문: eyJpdiI6InB...k3YjkiLCJ2YWx1ZSI6IjF2... (완벽한 암호화 문자열)
> 자동 복호화된 주소: 서울특별시 강남구 테헤란로 123 지니빌딩 401호
> ```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### MAC(Message Authentication Code) 변조 방지
- 라라벨의 `Crypt::encrypt()`는 단순 암호화만 하는 것이 아니라, 암호문에 대한 SHA-256 기반의 디지털 서명(MAC)을 함께 부착합니다.
- 악의적인 공격자가 데이터베이스에 침투하여 암호문 중 1바이트라도 임의로 조작하면, 복호화 시도시 `DecryptException`을 발생시켜 변조된 데이터의 실행을 완벽히 차단합니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`.env` 파일의 `APP_KEY`를 바꾸면 어떻게 되나요?**  
>    절대 안 된다멍! `APP_KEY`를 바꿔버리면 이전에 암호화된 고객들의 모든 주소와 전화번호를 영원히 복호화할 수 없게 된다멍! `APP_KEY`는 서버의 가장 소중한 마스터 보물이다멍!

---

## 💡 6. 2강 자가진단 과제

1. `Crypt::encryptString("지니의 비밀 메모")`로 암호화된 문자열을 만든 뒤, `Crypt::decryptString()`으로 원문이 정확히 복원되는지 확인하세요.
2. `User` 모델에서 `phone_number`가 데이터베이스 툴에서는 암호문으로 보이고 코드에서는 정상 전화번호로 읽히는지 검증하세요.
{% endraw %}
