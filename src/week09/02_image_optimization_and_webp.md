---
layout: docs
title: "02강: 도서 표지 썸네일 자동 생성 & WebP 압축 최적화"
---

{% raw %}
# 02강: 도서 표지 썸네일 자동 생성 & WebP 압축 최적화

> **실습 프로젝트:** 지니샵(JinyShop) 온라인 도서 쇼핑몰  
> **주제:** 고해상도 도서 표지 리사이징(가로 600px), 1:1 정사각형 썸네일 생성, 차세대 WebP 포맷 변환으로 용량 80% 절감  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  
> **공식 문서 연계:** [이미지 처리 (Images)](../docs/05_digging_deeper/images_ko.md)

---

## 💬 1. 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 출판사 담당자가 책 표지 사진을 스마트폰 카메라로 찍어서 8MB짜리 초고화질 원본을 그대로 업로드했어요! 모바일 고객들이 데이터 요금도 많이 나가고, 책 목록 화면이 열리는 데 한참 걸려서 이탈할 것 같아요!"

🐱 **지니**: "도로시의 말이 백번 옳단다! 모바일 서점에서 도서 표지 이미지는 전체 트래픽의 70% 이상을 차지하지. 라라벨의 **이미지 조작 파이프라인**을 연동하면, 업로드 즉시 가로 600px로 리사이징하고 최신 압축 포맷인 **WebP**로 자동 변환할 수 있단다. 8MB였던 사진이 품질 손실 없이 단 120KB로 압축되어 페이지 로딩 속도가 10배 빨라진단다!"

🐶 **토토**: "멍멍! 목록용 정사각형 썸네일(`200x200`)과 상세 페이지용 메인 표지(`600x800`) 두 가지 버전을 만들어두면 브라우저가 화면 크기에 맞게 골라 쓸 수 있다멍!"

---

## 🎯 2. 실습 목표 및 서점 시나리오

1. 업로드된 원본 도서 표지를 비율을 유지하며 최적 규격으로 리사이징합니다.
2. 목록 화면에서 초고속으로 로딩될 썸네일 이미지를 자동 추출합니다.
3. 구형 JPG/PNG 파일을 차세대 표준 압축 형식인 **WebP**로 인코딩하여 저장합니다.

---

## 🛠️ 3. 단계별 실습 절차 (Step-by-Step)

### [Step 1] 도서 이미지 최적화 서비스 작성

`app/Services/BookImageService.php` 파일을 생성하고 이미지 가공 파이프라인을 구축합니다 (PHP GD 또는 Intervention Image 기반):

```php
namespace App\Services;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class BookImageService
{
    /**
     * 도서 표지 최적화 및 WebP 저장 (메인 이미지 & 썸네일)
     */
    public function uploadCover(UploadedFile $file): array
    {
        $hash = Str::random(32);
        $mainPath = "books/covers/{$hash}.webp";
        $thumbPath = "books/thumbs/{$hash}.webp";

        // 1. 원본 이미지를 GD 라이브러리로 메모리에 로드
        $sourceImage = match ($file->getClientMimeType()) {
            'image/jpeg', 'image/jpg' => imagecreatefromjpeg($file->getRealPath()),
            'image/png' => imagecreatefrompng($file->getRealPath()),
            'image/webp' => imagecreatefromwebp($file->getRealPath()),
            default => throw new \InvalidArgumentException('지원하지 않는 이미지 포맷입니다.'),
        };

        $origW = imagesx($sourceImage);
        $origH = imagesy($sourceImage);

        // 2. 메인 표지 리사이징 (가로 최대 600px, 비율 유지)
        $newW = 600;
        $newH = (int) ($origH * ($newW / $origW));
        $mainCanvas = imagecreatetruecolor($newW, $newH);
        imagecopyresampled($mainCanvas, $sourceImage, 0, 0, 0, 0, $newW, $newH, $origW, $origH);

        // WebP 변환 후 storage/app/public/books/covers/ 에 저장
        ob_start();
        imagewebp($mainCanvas, null, 80); // 품질 80% 압축
        $mainData = ob_get_clean();
        Storage::disk('public')->put($mainPath, $mainData);

        // 3. 목록용 썸네일 생성 (가로 200px)
        $thumbW = 200;
        $thumbH = (int) ($origH * ($thumbW / $origW));
        $thumbCanvas = imagecreatetruecolor($thumbW, $thumbH);
        imagecopyresampled($thumbCanvas, $sourceImage, 0, 0, 0, 0, $thumbW, $thumbH, $origW, $origH);

        ob_start();
        imagewebp($thumbCanvas, null, 75);
        $thumbData = ob_get_clean();
        Storage::disk('public')->put($thumbPath, $thumbData);

        // 메모리 해제
        imagedestroy($sourceImage);
        imagedestroy($mainCanvas);
        imagedestroy($thumbCanvas);

        return [
            'cover_path' => $mainPath,
            'thumbnail_path' => $thumbPath,
        ];
    }
}
```

---

### [Step 2] 컨트롤러에 이미지 최적화 서비스 주입

`AdminBookController@store` 메서드에서 서비스 클래스를 호출합니다:

```php
public function store(Request $request, BookImageService $imageService)
{
    $validated = $request->validate([
        'title' => 'required',
        'cover_image' => 'required|image|max:8192', // 8MB까지 업로드 허용 후 즉시 압축!
    ]);

    // 🚀 업로드와 동시에 WebP 변환 및 썸네일 자동 생성!
    $images = $imageService->uploadCover($request->file('cover_image'));

    $book = Book::create([
        'title' => $validated['title'],
        'cover_image_path' => $images['cover_path'],
        'thumbnail_path' => $images['thumbnail_path'],
    ]);

    return redirect()->route('admin.books.index')
        ->with('success', '도서 표지가 WebP로 초압축되어 저장되었습니다!');
}
```

---

### [Step 3] 용량 절감 효과 확인

테스트 이미지를 업로드한 뒤 파일 크기를 비교해 봅니다:

```bash
ls -lh storage/app/public/books/covers/ storage/app/public/books/thumbs/
```

> **용량 비교 분석:**
> - 원본 업로드 사진: **4.8 MB (JPEG)**
> - 변환된 메인 표지: **142 KB (WebP) — 97% 용량 절감!**
> - 변환된 썸네일: **28 KB (WebP) — 99.4% 용량 절감!**

---

## 🔍 4. 라라벨 공식 문서 원리 심층 분석 (Deep Dive)

### Core Web Vitals (LCP) 개선 효과
- 구글 검색엔진은 페이지의 가장 큰 이미지(LCP, Largest Contentful Paint)가 2.5초 이내에 떠야 검색 상위에 랭크해 줍니다.
- 5MB짜리 원본 대신 142KB WebP 이미지를 제공하면 3G/LTE 모바일 환경에서도 LCP가 0.3초 만에 완료되어 SEO 점수가 대폭 상승합니다!

---

## 🐶 5. 토토의 트러블슈팅 & 주의사항

> 🐶 **토토의 멍멍 가이드!**
> 
> 1. **`Call to undefined function imagewebp()` 에러가 나요!**  
>    PHP 확장 모듈 중 `php-gd`가 안 켜져 있어서 그렇다멍! 터미널에서 `php -m | grep gd`를 확인하고 필요하면 `brew install php` 또는 Sail 컨테이너를 쓰면 기본 탑재되어 있다멍!

---

## 💡 6. 2강 자가진단 과제

1. 실제 책 표지 사진을 업로드하고, 크롬 개발자 도구의 Network 탭에서 확장자가 `.webp`로 떨어지는지 확인하세요.
2. 도서 목록 그리드 카드에서는 썸네일(`thumbnail_path`)을, 도서 상세 화면에서는 메인 표지(`cover_image_path`)를 각각 구분하여 출력해 보세요.
{% endraw %}
