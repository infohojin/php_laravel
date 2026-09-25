---
layout: docs
title: "11주차 03강: 메일(Mail)과 다채널 알림(Notifications) 시스템 구축"
---

{% raw %}
# 📖 11주차 03강: 메일(Mail)과 다채널 알림(Notifications) 시스템 구축

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 고객을 위한 감성적인 마크다운 주문 확인서 메일(`OrderReceiptMail`)과 관리자 및 고객을 위한 다채널 알림(이메일, 웹 인앱 알림, 슬랙 웹훅) 시스템을 구현하고 큐를 통해 백그라운드 발송합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 책을 주문하면 깔끔한 영수증 메일을 보내주고 싶어. HTML 이메일 템플릿을 직접 테이블 태그로 짜려고 하니까 아웃룩, 지메일, 애플메일마다 깨져서 미칠 것 같아!"  
🐱 **지니**: "도로시, 라라벨에는 반응형 이메일 표준을 완벽히 지켜주는 **마크다운(Markdown) Mailable**이 준비되어 있단다! `@component('mail::message')`와 마크다운 표 문법 몇 줄이면 모바일에서도 완벽하게 렌더링되는 최고급 영수증 메일이 완성되지."  
🐶 **토토**: "멍멍! 게다가 고객에게는 이메일을 보내고, 쇼핑몰 화면 상단 종 모양 아이콘에는 인앱 알림을 띄우고, 관리자에게는 슬랙(Slack)으로 동시에 쏘고 싶다면? **라라벨 알림(Notifications)**의 `via()` 한 방이면 끝난다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **메일 전송 환경 설정:** 로컬 테스트용 `log` 또는 Mailpit(`smtp` 포트 1025) 환경 구축
2. **마크다운 Mailable 클래스 생성:** `OrderReceiptMail`을 작성하고 브라우저에서 실시간 프리뷰 렌더링
3. **비동기 큐 메일 발송:** `Mail::to()->queue()`를 통해 응답 지연 없이 메일 발송
4. **다채널 알림(`Notification`) 구현:**
   - Database 채널: 독자의 마이페이지 읽지 않은 알림 뱃지 카운트
   - Mail 채널: 주문 확인서 전달
   - Slack 채널: 관리자 전용 채널에 고액 주문 발생 경보 웹훅 전송

---

## 🛠️ 단계별 실습 절차

### 1단계: 메일러 설정 (.env & Mailpit)

로컬 개발 환경에서는 실제 이메일이 발송되는 대신 로그 파일에 기록되거나, 로컬 가상 메일함(Mailpit)으로 전달되도록 `.env`를 설정합니다.

```env
# Mailpit 로컬 테스트 환경
MAIL_MAILER=smtp
MAIL_HOST=127.0.0.1
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS="no-reply@jinyshop.test"
MAIL_FROM_NAME="지니샵 도서몰"
```

> 🐶 **토토의 팁!**  
> "가장 쉬운 개발 테스트는 `MAIL_MAILER=log`로 두는 거야! 그러면 발송된 이메일 전문이 `storage/logs/laravel.log` 파일에 텍스트로 고스란히 찍힌다멍!"

---

### 2단계: 주문 확인서 Mailable 생성

마크다운 템플릿 옵션(`--markdown`)과 함께 Mailable 클래스를 생성합니다.

```bash
php artisan make:mail OrderReceiptMail --markdown=emails.orders.receipt
```

`app/Mail/OrderReceiptMail.php` 파일을 엽니다. 라라벨 11의 최신 `Envelope`, `Content`, `Attachments` 문법으로 작성되어 있습니다:

```php
<?php

namespace App\Mail;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Attachment;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class OrderReceiptMail extends Mailable implements ShouldQueue
{
    use Queueable, SerializesModels;

    /**
     * 새 Mailable 인스턴스 생성
     */
    public function __construct(
        public Order $order
    ) {}

    /**
     * 메일 봉투(제목 및 발신자) 정의
     */
    public function envelope(): Envelope
    {
        return new Envelope(
            subject: "[지니샵] 도서 주문 확인서 (주문번호: {$this->order->order_number})",
        );
    }

    /**
     * 메일 본문 마크다운 뷰 정의
     */
    public function content(): Content
    {
        return new Content(
            markdown: 'emails.orders.receipt',
            with: [
                'order' => $this->order,
                'items' => $this->order->items()->with('book')->get(),
            ],
        );
    }

    /**
     * 첨부 파일 정의 (예: PDF 영수증)
     */
    public function attachments(): array
    {
        return [
            // 필요 시 첨부파일 추가: Attachment::fromStorage('receipts/' . $this->order->id . '.pdf')
        ];
    }
}
```

---

### 3단계: 마크다운 메일 템플릿 디자인

`resources/views/emails/orders/receipt.blade.php` 파일을 다음과 같이 작성합니다:

```blade
<x-mail::message>
# 📚 도서 주문이 성공적으로 접수되었습니다!

안녕하세요, **{{ $order->user ? $order->user->name : '고객' }}** 님!  
지니샵을 이용해 주셔서 진심으로 감사드립니다. 고객님께서 주문하신 도서 내역을 안내해 드립니다.

---

### 📦 주문 내역 (주문번호: `{{ $order->order_number }}`)

<x-mail::table>
| 도서명 | 수량 | 단가 | 합계 |
| :--- | :---: | :---: | :---: |
@foreach($items as $item)
| **{{ $item->book->title }}** | {{ $item->quantity }}권 | {{ number_format($item->unit_price) }}원 | {{ number_format($item->quantity * $item->unit_price) }}원 |
@endforeach
</x-mail::table>

### 💰 최종 결제 금액: **{{ number_format($order->total_amount) }}원**
- **배송지 주소:** {{ $order->shipping_address ?? '기본 배송지' }}
- **결제 일시:** {{ $order->created_at->format('Y-m-d H:i') }}

<x-mail::button :url="route('orders.show', $order)">
주문 상세 및 배송 조회하기
</x-mail::button>

지니샵과 함께 지혜롭고 행복한 독서 시간 되시기를 바랍니다! ☕📖

감사합니다,<br>
**{{ config('app.name') }} 팀 드림**
</x-mail::message>
```

---

### 4단계: 브라우저에서 메일 실시간 프리뷰

개발 중에 매번 메일을 쏠 필요 없이 라우트에서 Mailable 인스턴스를 반환하면 웹 브라우저에서 바로 HTML 렌더링 화면을 확인할 수 있습니다!

`routes/web.php`에 프리뷰 라우트를 추가해 보세요:

```php
use App\Mail\OrderReceiptMail;
use App\Models\Order;

Route::get('/mailable/preview', function () {
    $order = Order::with('items.book')->latest()->first();
    return new OrderReceiptMail($order);
});
```

브라우저에서 `http://127.0.0.1:8000/mailable/preview`로 접속하면, 깔끔한 반응형 이메일 디자인이 펼쳐집니다!

---

### 5단계: 다채널 알림(`Notification`) 구현 (DB + Slack + Mail)

고객과 관리자에게 동시에 상황을 전파하는 알림 클래스를 만듭니다.

```bash
php artisan make:notification OrderShippedNotification
```

웹 인앱 알림을 저장할 데이터베이스 테이블 마이그레이션을 생성합니다:

```bash
php artisan notifications:table
php artisan migrate
```

`app/Notifications/OrderShippedNotification.php`를 다음과 같이 작성합니다:

```php
<?php

namespace App\Notifications;

use App\Models\Order;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Messages\SlackMessage;
use Illuminate\Notifications\Notification;

class OrderShippedNotification extends Notification implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public Order $order
    ) {}

    /**
     * 알림을 발송할 채널 배열 반환
     */
    public function via(object $notifiable): array
    {
        // 고객에게는 데이터베이스(인앱)와 메일로 발송
        return ['database', 'mail'];
    }

    /**
     * 메일 채널 알림
     */
    public function toMail(object $notifiable): MailMessage
    {
        return (new MailMessage)
            ->subject("[지니샵] 주문하신 도서가 발송되었습니다!")
            ->greeting("안녕하세요, {$notifiable->name}님!")
            ->line("고객님께서 기다리시던 도서가 오늘 안전하게 택배사로 인계되었습니다.")
            ->action('배송 위치 추적', route('orders.show', $this->order))
            ->line('지니샵 도서를 사랑해 주셔서 감사합니다!');
    }

    /**
     * 데이터베이스 채널 알림 (알림창 뱃지용 데이터)
     */
    public function toDatabase(object $notifiable): array
    {
        return [
            'order_id' => $this->order->id,
            'order_number' => $this->order->order_number,
            'title' => '도서 배송 시작',
            'message' => "주문번호 {$this->order->order_number}의 도서가 출고되었습니다.",
            'url' => route('orders.show', $this->order),
        ];
    }
}
```

---

### 6단계: 알림 전송 및 마이페이지 읽지 않은 알림 뱃지

`User` 모델은 이미 `Notifiable` 트레이트를 가지고 있으므로 다음과 같이 알림을 보낼 수 있습니다:

```php
// 특정 고객에게 알림 전송 (큐를 통해 비동기 발송)
$user->notify(new OrderShippedNotification($order));

// 여러 명의 독자에게 일괄 알림 전송
use Illuminate\Support\Facades\Notification;
Notification::send($users, new OrderShippedNotification($order));
```

블레이드 뷰(`resources/views/partials/header.blade.php`)에서 읽지 않은 알림 뱃지 표시:

```blade
<div class="relative">
    <button class="relative p-2 text-gray-600 hover:text-gray-900">
        🔔 알림
        @if(auth()->user()->unreadNotifications->count() > 0)
            <span class="absolute top-0 right-0 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-red-100 transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
                {{ auth()->user()->unreadNotifications->count() }}
            </span>
        @endif
    </button>
</div>
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. 온디맨드 알림 (On-Demand Notifications)

시스템에 등록된 회원이 아니더라도 외부 고객(이메일만 입력한 비회원)이나 특정 슬랙 웹훅 채널로 즉시 알림을 쏠 수 있는 라라벨의 강력한 문법입니다:

```php
use Illuminate\Support\Facades\Notification;

// 비회원 이메일로 즉시 영수증 알림
Notification::route('mail', 'guest@example.com')
    ->notify(new OrderShippedNotification($order));

// 관리자 슬랙 채널 웹훅으로 실시간 매출 보고
Notification::route('slack', config('services.slack.webhook_url'))
    ->notify(new NewOrderNotification($order));
```

### 2. 읽은 알림 처리 (`markAsRead`)

고객이 알림 목록을 클릭하면 읽음 처리하는 코드는 매우 간결합니다:

```php
// 특정 알림 1건 읽음 처리
$notification = auth()->user()->notifications()->findOrFail($id);
$notification->markAsRead();

// 모든 읽지 않은 알림 한 번에 읽음 처리
auth()->user()->unreadNotifications->markAsRead();
```

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **메일 큐 발송 시 `ShouldQueue` 필수:**  
   `Mail::to()->send()`를 쓰면 사용자가 웹 브라우저에서 2~3초간 대기해야 합니다. 반드시 `Mail::to()->queue()`를 쓰거나 Mailable 클래스에 `implements ShouldQueue`를 선언하세요!
2. **이메일 주소 유효성 검사:**  
   잘못된 이메일 주소로 발송을 시도하면 SMTP 예외가 발생하여 큐 작업이 실패할 수 있습니다. 회원가입 및 주문 시 이메일 유효성 검사 규칙(`'email' => 'required|email:rfc,dns'`)을 철저히 적용해야 합니다.

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** 사용자의 데이터베이스 알림 테이블에서 아직 읽지 않은 알림들의 컬렉션을 가져오는 Eloquent 관계 메소드는 무엇일까요?
   - 정답: `$user->unreadNotifications`
2. **과제:** 책이 발송 완료되었을 때 관리자 슬랙 채널로 "[알림] 주문 ORD-XXXX의 도서가 출고되었습니다!"라는 메시지를 보내는 슬랙 알림 채널을 연동해 보세요!
{% endraw %}
