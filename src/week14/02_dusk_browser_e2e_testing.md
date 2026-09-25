---
layout: docs
title: "14주차 02강: 라라벨 더스크(Dusk)를 이용한 브라우저 E2E 구매 시나리오 자동화"
---

{% raw %}
# 📖 14주차 02강: 라라벨 더스크(Dusk)를 이용한 브라우저 E2E 구매 시나리오 자동화

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 실제 크롬(Chrome) 브라우저를 백그라운드에서 구동하여 사용자의 마우스 클릭, 폼 타이핑, 자바스크립트 모달 팝업, 장바구니 담기부터 최종 결제 완료까지의 전체 구매 여정을 자동 검증하는 E2E(End-to-End) 테스트를 구축합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 백엔드 API 테스트는 다 초록색 불이 들어왔는데, 웹 프론트엔드 자바스크립트나 CSS가 꼬여서 '결제하기' 버튼이 다른 레이어에 가려져 클릭이 안 되거나 모달창이 안 닫히면 손님이 책을 못 사잖아!"  
🐱 **지니**: "도로시, 바로 그럴 때 사람이 직접 브라우저를 누르듯 테스트하는 **라라벨 더스크(Laravel Dusk)**를 쓰는 거란다! 실제 크롬 브라우저가 화면을 열고, 검색어를 치고, 마우스로 장바구니를 클릭하고, 결제 완료 문구가 뜨는지 1픽셀까지 완벽히 감시하지!"  
🐶 **토토**: "멍멍! 테스트 도중 에러가 나면 그 순간 브라우저 화면을 찰칵 캡처해서 스크린샷 이미지(`tests/Browser/screenshots`)로 남겨주니 어디서 버그가 났는지 한눈에 찾아낼 수 있다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **Laravel Dusk 설치 및 크롬 드라이버 구성:** `composer require --dev laravel/dusk`
2. **도서 구매 E2E 시나리오 테스트 작성:** `BookPurchaseTest`
   - 메인 페이지 접속 -> 검색어 "라라벨" 입력
   - 검색 결과에서 도서 상세 페이지 진입
   - 수량 2권 선택 후 장바구니 담기 클릭
   - 주문서 작성 및 결제 승인
   - 주문 완료 메시지 및 주문번호 텍스트 검증
3. **자바스크립트 대기 및 스크린샷 디버깅:** `waitForText()`, `screenshot()`
4. **다중 브라우저 협업 테스트:** 2개의 브라우저를 동시에 띄워 실시간 웹소켓 주문 알림 검증

---

## 🛠️ 단계별 실습 절차

### 1단계: Laravel Dusk 설치 및 크롬 드라이버 준비

터미널에서 개발 의존성으로 Dusk를 설치합니다:

```bash
composer require --dev laravel/dusk
php artisan dusk:install
```

> 💡 **명령어 자동 실행 결과:**  
> - `tests/Browser` 디렉토리 및 `DuskTestCase.php` 생성  
> - 시스템 OS(Mac/Linux/Windows)에 맞는 ChromeDriver 바이너리 자동 다운로드  
> - `.env.dusk.local` 테스트 전용 환경 파일 생성  

---

### 2단계: 도서 구매 E2E 브라우저 테스트 생성

Dusk 테스트 파일을 생성합니다:

```bash
php artisan dusk:make BookPurchaseTest
```

`tests/Browser/BookPurchaseTest.php` 파일을 다음과 같이 작성합니다:

```php
<?php

namespace Tests\Browser;

use App\Models\Book;
use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Laravel\Dusk\Browser;
use Tests\DuskTestCase;

class BookPurchaseTest extends DuskTestCase
{
    use DatabaseMigrations; // Dusk 전용 DB 마이그레이션

    /**
     * 사용자가 메인 페이지에서 도서를 검색하고 결제를 완료하는 전체 E2E 시나리오
     */
    public function test_user_can_search_book_and_complete_order(): void
    {
        // 1. 테스트 시드 데이터 생성
        $user = User::factory()->create([
            'email' => 'buyer@jinyshop.test',
            'password' => bcrypt('password123'),
        ]);

        $book = Book::factory()->create([
            'title' => '라라벨 11 마스터 가이드',
            'price' => 32000,
            'stock' => 15,
            'is_sold_out' => false,
        ]);

        // 2. 브라우저 인스턴스 구동 및 사용자 인터랙션 시뮬레이션
        $this->browse(function (Browser $browser) use ($user, $book) {
            $browser->visit('/login')
                // 로그인 진행
                ->type('email', $user->email)
                ->type('password', 'password123')
                ->press('#btn-login')
                ->assertPathIs('/books')

                // 도서 검색창에 키워드 입력 및 엔터
                ->type('q', '라라벨')
                ->press('#btn-search')
                ->waitForText('라라벨 11 마스터 가이드')

                // 도서 카드 클릭하여 상세 페이지로 이동
                ->clickLink('라라벨 11 마스터 가이드')
                ->assertSee('32,000원')
                ->assertSee('재고: 15권')

                // 수량 2권 선택 후 장바구니 담기
                ->select('quantity', '2')
                ->press('#btn-add-to-cart')

                // 장바구니 팝업 토스트 확인 및 결제 페이지 이동
                ->waitForText('장바구니에 담겼습니다!')
                ->visit('/checkout')

                // 배송지 주소 입력
                ->type('shipping_address', '서울특별시 마포구 월드컵북로 400')
                ->type('recipient_name', '홍길동')
                ->type('recipient_phone', '010-1234-5678')

                // 결제하기 버튼 클릭
                ->press('#btn-pay')

                // 최종 결제 완료 화면 확인
                ->waitForText('도서 주문이 성공적으로 완료되었습니다!', 10)
                ->assertSee('주문번호:')
                ->assertSee('총 결제금액: 64,000원')

                // 성공 증빙 스크린샷 캡처 저장!
                ->screenshot('checkout-success-proof');
        });
    }
}
```

---

### 3단계: 대화형/헤드리스 모드로 Dusk 실행

터미널에서 Dusk 테스트를 실행합니다:

```bash
php artisan dusk
```

크롬 브라우저가 화면 없이 초고속으로 뜨거나(Headless), 실제 창이 번쩍이며 사용자가 마우스를 움직이듯 타이핑과 클릭이 자동으로 일어납니다!

출력 예시:
```text
   PASS  Tests\Browser\BookPurchaseTest
  ✓ user can search book and complete order                              4.12s  

  Tests:    1 passed (8 assertions)
  Duration: 4.85s
```

테스트 완료 후 `tests/Browser/screenshots/checkout-success-proof.png` 파일을 열어보면, 주문 완료 화면이 고화질 이미지로 캡처되어 있는 것을 확인할 수 있습니다!

---

### 4단계: 다중 브라우저 협업 테스트 (관리자 실시간 주문 수신 검증)

Dusk는 브라우저를 2개 이상 동시에 띄울 수 있습니다. 독자가 주문을 넣는 순간 관리자 브라우저에 실시간 웹소켓 토스트 알림이 뜨는지 검증할 수 있습니다:

```php
public function test_admin_receives_realtime_order_notification(): void
{
    $this->browse(function (Browser $buyer, Browser $admin) {
        // 관리자 브라우저: 대시보드 로그인 후 대기
        $admin->loginAs($this->adminUser)
              ->visit('/admin/dashboard');

        // 구매자 브라우저: 주문 결제 실행
        $buyer->loginAs($this->buyerUser)
              ->visit('/checkout')
              ->press('#btn-pay');

        // 관리자 브라우저에서 화면 새로고침 없이 실시간 토스트가 떴는지 검증!
        $admin->waitForText('신규 도서 주문 접수!', 5)
              ->assertSee('홍길동님이 [라라벨 11 마스터 가이드] 외 도서를 주문하셨습니다.');
    });
}
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. Dusk 셀렉터 문법 가이드

Dusk는 CSS 셀렉터뿐만 아니라 가독성을 위한 전용 축약 셀렉터를 지원합니다:

| Dusk 메소드 | 설명 |
| :--- | :--- |
| `->click('@checkout-button')` | `dusk="checkout-button"` 속성을 가진 엘리먼트 클릭 |
| `->waitFor('@order-modal')` | 특정 컴포넌트가 DOM에 렌더링될 때까지 대기 |
| `->drag('#cover-item', '#cart-dropzone')` | 마우스 드래그 앤 드롭 동작 시뮬레이션 |
| `->script('window.scrollTo(0, 500);')` | 브라우저 콘솔 자바스크립트 직접 실행 |

### 2. 페이지 객체(Page Objects) 패턴

수십 개의 화면을 가진 대형 쇼핑몰에서는 URL과 공통 버튼을 페이지 객체(`App\Tests\Browser\Pages\CheckoutPage`)로 캡슐화하여 테스트 코드 중복을 제거할 수 있습니다.

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **`waitForText()` 타임아웃 기본값 조절:**  
   자바스크립트 애니메이션이나 비동기 결제 통신은 1~2초 지연될 수 있습니다. `assertSee()`는 즉시 검사하므로 비동기 화면에서는 반드시 `waitForText('완료 문구', 10)`처럼 최대 대기 시간을 넉넉히 주어야 Flaky(간헐적 실패) 테스트를 방지할 수 있습니다!
2. **로컬 크롬 버전 불일치 해결:**  
   컴퓨터의 구글 크롬 브라우저 버전이 업데이트되어 Dusk ChromeDriver와 버전이 안 맞을 때는 `php artisan dusk:chrome-driver --detect`를 실행하면 현재 설치된 크롬 버전에 딱 맞는 드라이버를 자동 다운로드해 줍니다!

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** Laravel Dusk에서 특정 엘리먼트를 식별하기 위해 HTML 태그에 권장되는 전용 속성 이름은 무엇일까요?
   - 정답: `dusk="엘리먼트명"` (예: `<button dusk="submit-order">`)
2. **과제:** 책 상세 페이지에서 수량을 0 이하로 입력하고 장바구니 버튼을 눌렀을 때, 자바스크립트 Alert 대화상자가 뜨는지 `assertDialogOpened('1권 이상 선택해 주세요')`로 검증하는 Dusk 테스트를 작성해 보세요!
{% endraw %}
