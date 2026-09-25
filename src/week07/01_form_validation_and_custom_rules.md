---
layout: docs
title: "01강: Form Request 캡슐화 & 재고 한도 커스텀 검증 룰(`CheckBookStock`)"
---

{% raw %}
# 01강: Form Request 캡슐화 & 재고 한도 커스텀 검증 룰(`CheckBookStock`)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 컨트롤러에서 검증 로직 분리(`StoreCartItemRequest`), 악의적 파라미터 차단, 남은 재고 수량 비교 커스텀 룰  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [유효성 검사 (Validation)](../docs/04_the_basics/validation_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 고객이 책을 장바구니에 담을 때 수량에 `-5`나 `abc` 같은 이상한 값을 써서 보내거나, 재고가 딱 3권 남았는데 100권을 주문하겠다고 우기면 어떻게 막아야 해요? 컨트롤러에 if문으로 검사하려니 코드가 너무 지저분해져요!"

🐱 **지니**: "도로시, 백엔드 개발의 제1철칙은 **'절대로 사용자의 입력을 믿지 마라'**란다! 라라벨의 **Form Request** 클래스를 만들면, 컨트롤러 메서드가 실행되기도 전에 문지기처럼 모든 입력을 철저히 검사해 주지. 그리고 '남은 재고보다 많은 수량을 담을 수 없다' 같은 우리 서점만의 특별한 규칙은 **커스텀 검증 룰(Custom Rule)**로 캡슐화할 수 있단다!"

🐶 **토토**: "멍멍! 검증에 실패하면 라라벨이 자동으로 사용자를 이전 화면으로 돌려보내고(`back()`), `$errors` 가방과 함께 이전 입력값(`old('quantity')`)까지 복원해 준다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 장바구니 담기 요청 전용 Form Request `StoreCartItemRequest`를 생성합니다.
2. 재고 수량 초과를 감지하는 재사용 가능한 커스텀 룰 `CheckBookStock`을 구현합니다.
3. Blade 화면에서 `@error` 지시어로 친절한 한국어 에러 메시지를 띄우는 법을 익힙니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] Form Request 및 커스텀 룰 아티산 생성

```bash
# 1. 폼 리퀘스트 생성
php artisan make:request StoreCartItemRequest

# 2. 재고 검증 커스텀 룰 생성
php artisan make:rule CheckBookStock
```

---

### [Step 2] `CheckBookStock` 커스텀 룰 작성

`app/Rules/CheckBookStock.php` 파일을 열고, 요청한 수량이 도서의 실제 재고(`stock_quantity`)를 넘지 않는지 검사하는 로직을 작성합니다:

```php
namespace App\Rules;

use App\Models\Book;
use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class CheckBookStock implements ValidationRule
{
    protected ?int $bookId;

    public function __construct(?int $bookId)
    {
        $this->bookId = $bookId;
    }

    /**
     * 유효성 검사 실행
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        $book = Book::find($this->bookId);

        if (! $book) {
            $fail('선택하신 도서가 존재하지 않습니다.');
            return;
        }

        // 전자책은 재고 제한 없음
        if ($book->format === 'ebook') {
            return;
        }

        // 품절 체크
        if ($book->stock_quantity <= 0) {
            $fail("[{$book->title}] 도서는 현재 전량 품절되었습니다.");
            return;
        }

        // 요청 수량이 남은 재고 초과 시 에러 메시지 반환
        if ($value > $book->stock_quantity) {
            $fail("[{$book->title}] 도서의 남은 재고는 {$book->stock_quantity}권입니다. (요청: {$value}권)");
        }
    }
}
```

---

### [Step 3] `StoreCartItemRequest` 룰 조립

`app/Http/Requests/StoreCartItemRequest.php`에서 검증 규칙과 커스텀 에러 문구를 정의합니다:

```php
namespace App\Http\Requests;

use App\Rules\CheckBookStock;
use Illuminate\Foundation\Http\FormRequest;

class StoreCartItemRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true; // 모든 고객 허용
    }

    public function rules(): array
    {
        return [
            'book_id' => ['required', 'integer', 'exists:books,id'],
            'quantity' => [
                'required',
                'integer',
                'min:1',
                'max:10', // 1인당 1회 최대 10권 제한
                new CheckBookStock($this->input('book_id')), // 커스텀 룰 주입!
            ],
        ];
    }

    public function messages(): array
    {
        return [
            'book_id.required' => '도서 식별자가 누락되었습니다.',
            'book_id.exists' => '서점에 등록되지 않은 도서입니다.',
            'quantity.required' => '주문 수량을 입력해 주세요.',
            'quantity.min' => '도서는 최소 1권 이상 담아야 합니다.',
            'quantity.max' => '1회 주문 시 최대 10권까지만 담을 수 있습니다.',
        ];
    }
}
```

---

### [Step 4] Blade 화면에서 `@error` 지시어로 에러 피드백

도서 상세 화면의 장바구니 담기 폼에 에러 출력 지시어를 추가합니다:

```html
<!-- resources/views/books/show.blade.php 내부의 장바구니 폼 -->
<form action="/cart/items" method="POST" class="mt-6">
    @csrf
    <input type="hidden" name="book_id" value="{{ $book->id }}">

    <div class="flex items-center space-x-3">
        <label for="qty" class="text-sm font-medium text-slate-700">수량:</label>
        <input type="number" id="qty" name="quantity" 
               value="{{ old('quantity', 1) }}" min="1" max="10"
               class="w-20 border rounded-lg p-2 text-center text-sm @error('quantity') border-rose-500 ring-2 ring-rose-200 @enderror">
        
        <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg shadow">
            🛒 장바구니 담기
        </button>
    </div>

    <!-- 검증 에러 메시지 표시 -->
    @error('quantity')
        <p class="text-rose-600 text-xs font-semibold mt-2 flex items-center">
            ⚠️ {{ $message }}
        </p>
    @enderror
</form>
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 컨트롤러의 극단적 다이어트
Form Request를 사용하면 컨트롤러 메서드는 다음과 같이 단 2줄로 끝납니다:

```php
public function store(StoreCartItemRequest $request, CartService $cart)
{
    // 이 줄에 도달했다는 것은 모든 유효성 검사가 100% 통과했음을 보장함!
    $validated = $request->validated();
    $cart->add($validated['book_id'], $validated['quantity']);

    return back()->with('success', '장바구니에 책이 담겼습니다!');
}
```
검증에 실패하면 라라벨이 컨트롤러를 아예 실행하지 않고 자동으로 이전 화면으로 리다이렉트합니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **검증 실패 후 이전 입력값이 사라져요!**  
>    `<input value="{{ old('quantity') }}">` 처럼 `old()` 헬퍼를 쓰면 고객이 방금 적었던 숫자가 고스란히 남아있어서 손님이 다시 쓰지 않아도 된다멍!

---

## 💡 6. 1강 자가진단 과제

1. 브라우저에서 수량에 `-1`이나 `99`를 입력하고 장바구니 담기를 눌러보세요.
2. 화면에 빨간색 테두리와 함께 "도서는 최소 1권 이상 담아야 합니다" 또는 "1회 주문 시 최대 10권까지만 담을 수 있습니다" 메시지가 뜨는지 확인하세요.
{% endraw %}
