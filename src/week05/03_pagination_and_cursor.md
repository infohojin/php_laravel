---
layout: docs
title: "03강: 대용량 1,000권 페이지네이션(Pagination) & 커서 페이징(Cursor)"
---

{% raw %}
# 03강: 대용량 1,000권 페이지네이션(Pagination) & 커서 페이징(Cursor)

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 데스크톱 번호 페이징(`paginate`), Tailwind CSS 링크 렌더링, 모바일 무한 스크롤을 위한 고성능 커서 페이징(`cursorPaginate`)  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [페이지네이션 (Pagination)](../docs/07_database/pagination_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 우리가 지난 4주차에 만든 책 데이터가 1,000권이나 되잖아요. 만약 한 화면에 1,000권을 통째로 불러오면 페이지 로딩에 10초가 걸리고 브라우저가 멈출 거예요! 12권씩 예쁜 페이지 번호(`1, 2, 3, 4...`)로 나누어 보려면 어떻게 해야 하나요? 그리고 스마트폰 앱처럼 아래로 내릴 때 계속 추가되는 무한 스크롤도 지원할 수 있나요?"

🐱 **지니**: "도로시, 바로 그것이 웹의 필수 요소인 **페이지네이션(Pagination)**이란다! 다른 프레임워크에서는 전체 개수를 세고, 시작 위치(Offset)를 계산하고, 이전/다음 버튼 HTML을 수백 줄씩 짜야 하지. 하지만 라라벨에서는 단 한 마디! `->paginate(12)`를 붙이고 뷰에서 `{{ $books->links() }}`만 적어주면 끝난단다! 모바일 무한 스크롤에는 수백만 건에서도 0.001초 만에 다음 페이지를 가져오는 **커서 페이지네이션(Cursor Pagination)**을 쓰면 된단다!"

🐶 **토토**: "멍멍! 검색창에 '라라벨'을 치고 2페이지로 넘어갈 때 검색어가 날아가 버리는 참사를 막으려면 꼭 `->withQueryString()`을 붙여줘야 한다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 1,000권의 도서를 12권 단위로 나누어 페이징하는 `LengthAwarePaginator`를 구현합니다.
2. Blade 화면에 Tailwind CSS 스타일의 세련된 페이지네이션 내비게이션 바를 출력합니다.
3. 수백만 건의 대규모 도서에서도 성능 저하가 없는 **커서 페이징(`cursorPaginate`)**을 실습합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] `books/index.blade.php` 하단에 페이지네이션 링크 배치

`resources/views/books/index.blade.php`의 도서 그리드 아래에 페이징 링크 코드를 추가합니다:

```html
<!-- 도서 카드 그리드 하단 -->
<div class="mt-10">
    <!-- 라라벨이 자동으로 생성해주는 세련된 Tailwind CSS 페이징 바! -->
    {{ $books->links() }}
</div>

<!-- 부가 정보 표시 -->
<div class="mt-4 text-center text-xs text-slate-400">
    총 {{ number_format($books->total()) }}권의 도서 중 
    {{ $books->firstItem() }} ~ {{ $books->lastItem() }}권 표시 중 (현재 {{ $books->currentPage() }} / {{ $books->lastPage() }} 페이지)
</div>
```

---

### [Step 2] 브라우저에서 페이지 이동 테스트

브라우저에서 `http://127.0.0.1:8000/books?page=2` 로 이동해 봅니다:

- 하단에 `[이전] 1 [2] 3 4 5 ... 84 [다음]` 버튼이 아름다운 Tailwind 스타일로 자동 생성됩니다.
- 검색어 필터를 넣은 상태(`?keyword=라라벨&sort=price_asc`)에서 3페이지를 클릭해도 `withQueryString()` 덕분에 URL의 모든 검색 파라미터가 그대로 유지됩니다!

---

### [Step 3] 모바일 무한 스크롤을 위한 커서 페이징(Cursor Pagination)

전통적인 `OFFSET` 기반 페이징은 데이터가 수백만 건이 되면 `OFFSET 500000 LIMIT 12` 쿼리를 실행할 때 앞선 50만 건을 모두 디스크에서 읽어야 하므로 심각한 슬로우 쿼리가 발생합니다.

반면 **커서 페이징**은 마지막으로 본 도서의 ID(`WHERE id < ?`)를 기준으로 인덱스를 타기 때문에 1페이지든 100만 페이지든 항상 1ms 만에 응답합니다:

```php
// routes/web.php 에 모바일 API 테스트 라우트 추가
use App\Models\Book;
use Illuminate\Http\Request;

Route::get('/api/mobile/books', function (Request $request) {
    // 12권씩 커서 기반 페이징
    $books = Book::query()
        ->published()
        ->orderBy('id', 'desc')
        ->cursorPaginate(12);

    return response()->json([
        'data' => $books->items(),
        'next_cursor' => $books->nextCursor()?->encode(),
        'prev_cursor' => $books->previousCursor()?->encode(),
        'has_more' => $books->hasMorePages(),
    ]);
});
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### 페이징 뷰 템플릿 커스터마이징
기본 Tailwind 디자인 외에 서점만의 특별한 페이지네이션 디자인을 입히고 싶다면 다음 명령어로 템플릿을 추출(Publish)할 수 있습니다:

```bash
php artisan vendor:publish --tag=laravel-pagination
```
`resources/views/vendor/pagination/` 폴더에 템플릿들이 복사되어 HTML 구조와 색상을 자유롭게 변경할 수 있습니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **커서 페이징할 때는 정렬 컬럼에 주의하세요!**  
>    커서 페이징은 연속성을 추적해야 하므로 정렬 컬럼에 반드시 `id`나 고유(Unique) 컬럼이 포함되어야 한다멍! 그렇지 않으면 무한 루프에 빠질 수 있다멍!

---

## 💡 6. 3강 자가진단 과제

1. 브라우저에서 `http://127.0.0.1:8000/api/mobile/books`를 호출하여 반환된 `next_cursor` 인코딩 문자열을 확인하세요.
2. `http://127.0.0.1:8000/api/mobile/books?cursor=방금복사한커서문자열` 로 접속하여 다음 12권의 책이 즉시 응답되는지 확인해 보세요.
{% endraw %}
