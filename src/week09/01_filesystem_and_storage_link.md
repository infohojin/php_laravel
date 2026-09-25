---
layout: docs
title: "01강: Flysystem 파일 스토리지 & 도서 표지 이미지 업로드"
---

{% raw %}
# 01강: Flysystem 파일 스토리지 & 도서 표지 이미지 업로드

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 라라벨 Flysystem 파일 시스템 추상화, `public` 디스크와 `storage:link` 심볼릭 링크, 도서 표지 안전 업로드  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [파일 스토리지 (File Storage)](../docs/05_digging_deeper/filesystem_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 관리자가 새 책을 등록할 때 책 표지 사진(JPEG, PNG)을 업로드할 수 있어야 하잖아요. 그런데 업로드된 이미지를 `public/` 폴더에 그대로 넣으면 해커가 악성 PHP 웹셸 스크립트를 올려서 서버를 해킹할 수도 있다고 들었어요! 그리고 나중에 AWS S3 클라우드로 옮기려면 코드를 다 뜯어고쳐야 하나요?"

🐱 **지니**: "도로시의 보안과 확장성에 대한 고민이 아주 훌륭하구나! 라라벨의 **Flysystem 파일 스토리지**는 `local`, `public`, `s3`를 완벽히 추상화해 둔 마법 창고란다! 실제 파일은 외부에서 직접 스크립트 실행이 불가능한 `storage/app/public/` 비밀 창고에 보관하고, 웹 브라우저에는 `php artisan storage:link` 심볼릭 링크를 통해서만 정적 이미지로 안전하게 서빙하지! 로컬에서 짜둔 코드는 설정값 하나만 바꾸면 AWS S3로 단 1초 만에 무수정 이관된단다!"

🐶 **토토**: "멍멍! 파일 업로드 받을 때는 `image|mimes:jpeg,png,webp|max:2048` 검증 규칙을 꼭 걸어서 2MB 이하의 순수 이미지만 받도록 문을 걸어 잠가야 한다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. `php artisan storage:link` 명령어로 웹 공개 심볼릭 링크를 연결합니다.
2. 도서 표지 이미지 업로드 폼과 Form Request 검증을 작성합니다.
3. 고유한 해시 파일명으로 도서 표지를 안전하게 저장하고 브라우저에서 `Storage::url()`로 출력합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 스토리지 심볼릭 링크 연결 (`storage:link`)

터미널에서 다음 명령어를 실행하여 `storage/app/public` 디렉터리를 `public/storage`로 바로가기 링크를 만듭니다:

```bash
php artisan storage:link
```

> **터미널 출력:**
> ```text
>    INFO  The [public/storage] link has been connected to [storage/app/public].
> ```

---

### [Step 2] 도서 등록 폼 파일 업로드 지원 (`enctype`)

`resources/views/admin/books/create.blade.php`에 파일 첨부 가능한 폼을 작성합니다:

```html
<!-- 반드시 enctype="multipart/form-data" 필수! -->
<form action="/admin/books" method="POST" enctype="multipart/form-data" class="space-y-4">
    @csrf

    <div>
        <label class="block text-sm font-medium text-slate-700">도서 제목</label>
        <input type="text" name="title" class="border rounded p-2 w-full" required>
    </div>

    <div>
        <label class="block text-sm font-medium text-slate-700">도서 표지 이미지 (최대 2MB)</label>
        <input type="file" name="cover_image" accept="image/*" class="border rounded p-2 w-full">
        @error('cover_image')
            <p class="text-rose-500 text-xs mt-1">{{ $message }}</p>
        @enderror
    </div>

    <button type="submit" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded">
        도서 등록하기
    </button>
</form>
```

---

### [Step 3] 컨트롤러에서 안전한 도서 표지 저장 처리

`AdminBookController@store` 메서드에서 파일을 검증하고 저장합니다:

```php
namespace App\Http\Controllers;

use App\Models\Book;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class AdminBookController extends Controller
{
    public function store(Request $request)
    {
        // 1. 엄격한 이미지 파일 검증
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'cover_image' => 'nullable|image|mimes:jpeg,png,webp,jpg|max:2048', // 2MB 제한
        ]);

        $coverPath = null;

        // 2. 파일이 첨부되었는지 확인
        if ($request->hasFile('cover_image')) {
            // storage/app/public/books/covers/ 디렉터리에 충돌 없는 고유 해시명으로 자동 저장!
            $coverPath = $request->file('cover_image')->store('books/covers', 'public');
        }

        // 3. 도서 레코드에 저장된 상대 경로 기록
        $book = Book::create([
            'title' => $validated['title'],
            'cover_image_path' => $coverPath,
            // ... 기타 필수값 ...
        ]);

        return redirect()->route('admin.books.index')
            ->with('success', '책과 표지 이미지가 안전하게 저장되었습니다!');
    }
}
```

---

### [Step 4] Blade 화면에서 이미지 표시 (`Storage::url()`)

도서 상세 또는 목록 뷰에서 `Storage::url()` 헬퍼를 통해 브라우저 공개 URL을 생성합니다:

```html
@if($book->cover_image_path)
    <!-- Storage::url()이 자동으로 /storage/books/covers/랜덤해시.jpg 주소 생성 -->
    <img src="{{ Storage::url($book->cover_image_path) }}" alt="{{ $book->title }} 표지" 
         class="w-full aspect-[3/4] object-cover rounded-lg shadow">
@else
    <!-- 기본 플레이스홀더 표지 -->
    <div class="w-full aspect-[3/4] bg-slate-100 flex items-center justify-center text-4xl">
        📖
    </div>
@endif
```

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### `Storage::disk('s3')` 무수정 클라우드 전환
- 로컬에서 테스트할 때는 `FILESYSTEM_DISK=public`으로 로컬 디스크에 저장합니다.
- 실제 서비스 오픈 시 `.env`에서 `FILESYSTEM_DISK=s3`로 바꾸고 AWS 키만 넣어주면, 컨트롤러의 `$request->file('cover_image')->store('books/covers')` 코드는 **단 한 글자도 수정하지 않고** Amazon S3 버킷으로 자동 업로드됩니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **도서 표지가 깨진 엑스박스로 나와요!**  
>    `php artisan storage:link` 심볼릭 링크를 안 걸었기 때문일 확률이 99%다멍! 터미널에서 심볼릭 링크를 생성했는지 꼭 확인하라멍!

---

## 💡 6. 1강 자가진단 과제

1. 실제 이미지 파일을 등록해 보고, `storage/app/public/books/covers/` 폴더에 무작위 영문 해시명의 이미지가 저장되는지 확인하세요.
2. 브라우저에서 이미지 주소를 복사해 새 탭에서 열었을 때 `http://127.0.0.1:8000/storage/books/covers/...` 경로로 정상 표시되는지 검증하세요.
{% endraw %}
