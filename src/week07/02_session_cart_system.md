---
layout: docs
title: "02강: 비회원도 가능한 세션(Session) 기반 도서 장바구니 서비스"
---

{% raw %}
# 02강: 비회원도 가능한 세션(Session) 기반 도서 장바구니 서비스

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 세션 드라이버 원리, 도서 장바구니 전용 `CartService`, 담기/수량 변경/삭제 및 장바구니 뷰 구현  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [세션 (Session)](../docs/04_the_basics/session_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! HTTP 프로토콜은 상태가 없는 '무상태(Stateless)'라서, 페이지를 이동할 때마다 고객이 방금 무슨 책을 장바구니에 담았는지 싹 잊어버리잖아요. 아직 로그인도 하지 않은 비회원 손님이 담아둔 책 목록은 브라우저를 닫기 전까지 어디에 안전하게 보관해야 하죠?"

🐱 **지니**: "도로시, 바로 그 역할을 하는 마법 상자가 **세션(Session)**이란다! 고객의 브라우저에는 오직 암호화된 `laravel_session` 쿠키 키 하나만 쥐여주고, 실제 책 목록 데이터는 서버 측 세션 저장소에 안전하게 보관하지. 라라벨의 `session()` 헬퍼를 쓰면 마치 배열을 다루듯 손쉽게 장바구니를 넣고 뺄 수 있단다!"

🐶 **토토**: "멍멍! `config/session.php`에서 세션 저장소를 파일(`file`)에서 데이터베이스(`database`)나 초고속 레디스(`redis`)로 단 1초 만에 바꿀 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 장바구니 비즈니스 로직을 전담하는 순수 서비스 클래스 `CartService`를 작성합니다.
2. 장바구니 담기, 수량 변경, 개별 삭제, 장바구니 비우기 엔드포인트를 구축합니다.
3. 실시간 총 주문 금액과 할인 금액이 계산되어 표시되는 반응형 장바구니 화면을 만듭니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 도서 장바구니 전용 `CartService` 작성

`app/Services/CartService.php` 파일을 생성합니다:

```php
<?php

namespace App\Services;

use App\Models\Book;
use Illuminate\Support\Collection;

class CartService
{
    protected const SESSION_KEY = 'jinyshop_cart';

    /**
     * 장바구니 전체 아이템 조회 (Book 모델 정보와 함께 반환)
     */
    public function getItems(): Collection
    {
        $cartData = session()->get(self::SESSION_KEY, []);
        if (empty($cartData)) {
            return collect();
        }

        // 세션에 저장된 책 ID들을 일괄 조회 (Eager Loading 적용)
        $bookIds = array_keys($cartData);
        $books = Book::whereIn('id', $bookIds)->with('author')->get();

        return $books->map(function (Book $book) use ($cartData) {
            $quantity = $cartData[$book->id]['quantity'];
            $effectivePrice = $book->sale_price ?? $book->price;

            return (object) [
                'book' => $book,
                'quantity' => $quantity,
                'unit_price' => $effectivePrice,
                'subtotal' => $effectivePrice * $quantity,
            ];
        });
    }

    /**
     * 도서 장바구니 추가
     */
    public function add(int $bookId, int $quantity = 1): void
    {
        $cart = session()->get(self::SESSION_KEY, []);

        if (isset($cart[$bookId])) {
            $cart[$bookId]['quantity'] += $quantity;
        } else {
            $cart[$bookId] = ['quantity' => $quantity];
        }

        session()->put(self::SESSION_KEY, $cart);
    }

    /**
     * 수량 직접 변경
     */
    public function update(int $bookId, int $quantity): void
    {
        $cart = session()->get(self::SESSION_KEY, []);

        if ($quantity > 0) {
            $cart[$bookId] = ['quantity' => $quantity];
        } else {
            unset($cart[$bookId]);
        }

        session()->put(self::SESSION_KEY, $cart);
    }

    /**
     * 도서 항목 삭제
     */
    public function remove(int $bookId): void
    {
        $cart = session()->get(self::SESSION_KEY, []);
        unset($cart[$bookId]);
        session()->put(self::SESSION_KEY, $cart);
    }

    /**
     * 장바구니 총 결제 예정 금액
     */
    public function totalPrice(): int
    {
        return $this->getItems()->sum('subtotal');
    }

    /**
     * 총 담긴 도서 수량
     */
    public function totalCount(): int
    {
        return $this->getItems()->sum('quantity');
    }
}
```

---

### [Step 2] `CartController` 생성 및 라우트 연결

```bash
php artisan make:controller CartController
```

```php
// app/Http/Controllers/CartController.php
namespace App\Http\Controllers;

use App\Http\Requests\StoreCartItemRequest;
use App\Services\CartService;
use Illuminate\Http\Request;

class CartController extends Controller
{
    public function index(CartService $cart)
    {
        $items = $cart->getItems();
        $totalPrice = $cart->totalPrice();
        $totalCount = $cart->totalCount();

        return view('cart.index', compact('items', 'totalPrice', 'totalCount'));
    }

    public function store(StoreCartItemRequest $request, CartService $cart)
    {
        $cart->add($request->integer('book_id'), $request->integer('quantity', 1));

        return redirect()->route('cart.index')
            ->with('success', '🛒 도서가 장바구니에 추가되었습니다!');
    }

    public function update(Request $request, int $bookId, CartService $cart)
    {
        $request->validate(['quantity' => 'required|integer|min:1|max:10']);
        $cart->update($bookId, $request->integer('quantity'));

        return back()->with('success', '수량이 변경되었습니다.');
    }

    public function destroy(int $bookId, CartService $cart)
    {
        $cart->remove($bookId);

        return back()->with('success', '도서가 장바구니에서 삭제되었습니다.');
    }
}
```

`routes/web.php`에 연결:
```php
use App\Http\Controllers\CartController;

Route::prefix('cart')->name('cart.')->group(function () {
    Route::get('/', [CartController::class, 'index'])->name('index');
    Route::post('/items', [CartController::class, 'store'])->name('store');
    Route::put('/items/{id}', [CartController::class, 'update'])->name('update');
    Route::delete('/items/{id}', [CartController::class, 'destroy'])->name('destroy');
});
```

---

### [Step 3] 장바구니 화면 Blade 템플릿 작성

`resources/views/cart/index.blade.php` 파일을 생성합니다:

```html
<x-layouts.app>
    <x-slot:title>나의 장바구니 — 지니샵</x-slot:title>

    <div class="max-w-5xl mx-auto py-4">
        <h1 class="text-2xl font-bold text-slate-800 mb-6 flex items-center space-x-2">
            <span>🛒</span>
            <span>장바구니 (총 {{ $totalCount }}권)</span>
        </h1>

        @if($items->isEmpty())
            <div class="bg-white rounded-2xl p-16 text-center border border-slate-200">
                <span class="text-6xl">📚</span>
                <p class="mt-4 text-slate-600 font-semibold text-lg">장바구니에 담긴 책이 없습니다.</p>
                <a href="{{ route('books.index') }}" class="mt-4 inline-block bg-indigo-600 text-white text-sm font-bold px-6 py-2.5 rounded-lg shadow">
                    도서 둘러보기
                </a>
            </div>
        @else
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- 1. 도서 항목 목록 -->
                <div class="lg:col-span-2 space-y-4">
                    @foreach($items as $item)
                        <div class="bg-white rounded-xl p-4 border border-slate-200 shadow-sm flex items-center justify-between">
                            <div>
                                <h3 class="font-bold text-slate-800">
                                    <a href="{{ route('books.show', $item->book->slug) }}" class="hover:text-indigo-600">
                                        {{ $item->book->title }}
                                    </a>
                                </h3>
                                <p class="text-xs text-slate-500 mt-1">{{ $item->book->author->name }} 저 · 단가: {{ number_format($item->unit_price) }}원</p>
                            </div>

                            <div class="flex items-center space-x-4">
                                <!-- 수량 변경 폼 -->
                                <form action="{{ route('cart.update', $item->book->id) }}" method="POST" class="flex items-center space-x-1">
                                    @csrf
                                    @method('PUT')
                                    <input type="number" name="quantity" value="{{ $item->quantity }}" min="1" max="10" class="w-14 border rounded p-1 text-center text-sm">
                                    <button type="submit" class="text-xs bg-slate-100 hover:bg-slate-200 px-2 py-1 rounded">변경</button>
                                </form>

                                <span class="font-bold text-slate-900 w-24 text-right">{{ number_format($item->subtotal) }}원</span>

                                <!-- 삭제 버튼 -->
                                <form action="{{ route('cart.destroy', $item->book->id) }}" method="POST">
                                    @csrf
                                    @method('DELETE')
                                    <button type="submit" class="text-rose-500 hover:text-rose-700 text-sm p-1">✕</button>
                                </form>
                            </div>
                        </div>
                    @endforeach
                </div>

                <!-- 2. 결제 금액 요약 카드 -->
                <div class="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm h-fit">
                    <h2 class="font-bold text-slate-800 text-lg mb-4">주문 결제 금액</h2>
                    <div class="space-y-2 text-sm text-slate-600">
                        <div class="flex justify-between">
                            <span>총 도서 금액</span>
                            <span>{{ number_format($totalPrice) }}원</span>
                        </div>
                        <div class="flex justify-between">
                            <span>배송비</span>
                            <span class="text-emerald-600 font-bold">무료 (3만원 이상)</span>
                        </div>
                    </div>
                    <div class="border-t border-slate-200 my-4 pt-4 flex justify-between font-bold text-lg text-slate-900">
                        <span>최종 결제 금액</span>
                        <span class="text-indigo-600">{{ number_format($totalPrice) }}원</span>
                    </div>
                    <button class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 rounded-xl shadow-lg mt-4 transition">
                        주문서 작성하기 →
                    </button>
                </div>
            </div>
        @endif
    </div>
</x-layouts.app>
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 세션의 수명과 가비지 컬렉션(GC)
- `config/session.php`의 `'lifetime' => 120` 설정에 따라 기본적으로 120분 동안 아무 활동이 없으면 세션이 만료됩니다.
- 고객이 브라우저 창을 닫았을 때 즉시 세션을 파기하고 싶다면 `'expire_on_close' => true`로 변경할 수 있습니다.

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **서버를 재부팅하거나 분산 서버로 확장할 때는 세션이 사라지나요?**  
>    `SESSION_DRIVER=file`은 로컬 단일 서버 전용이다멍! 여러 대의 서버를 돌릴 때는 `SESSION_DRIVER=redis`나 `database`로 설정해야 어떤 서버로 접속해도 장바구니가 유지된다멍!

---

## 💡 6. 2강 자가진단 과제

1. 도서 상세 화면에서 [장바구니 담기]를 눌러 장바구니에 정상적으로 추가되는지 확인하세요.
2. 수량을 3권으로 변경했을 때 소계(`subtotal`)와 최종 결제 금액이 3배로 올바르게 재계산되는지 확인하세요.
3. 항목 삭제(✕)를 누르면 해당 책이 세션에서 말끔히 지워지는지 검증하세요.
{% endraw %}
