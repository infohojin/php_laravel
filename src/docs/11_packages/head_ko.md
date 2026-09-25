---
layout: docs
title: "라라벨 헤드"
---

{% raw %}
# 라라벨 헤드

- [소개](#introduction)
- [설치](#installation)
- 퀵스타트 (#quickstart)
- [Resolution Precedence](#resolution-precedence)
- [정의 메타데이터](#defining-metadata)
- [기본값](#defaults)
- 루트 메타데이터 (#route-metadata)
- [런타임 메타데이터](#runtime-metadata)
- [오류 페이지](#error-pages)
- 오픈 그래프 (#open-graph)
- [X / 트위터 카드](#twitter-cards)
- 테마 컬러 (#theme-colors)
- [애플리케이션 메타데이터 및 아이콘](#app-metadata-and-icons)
- 프로그레시브 웹 앱 (#progressive-web-apps)
- 퍼포먼스 및 디스커버리 (#performance-and-discovery)
- 커스텀 태그 (#custom-tags)
- [Schemas](#schemas)
- 브레드크럼브스 (#breadcrumbs)
- [FAQs](#faqs)
- 커스텀 스키마 (#custom-schemas)
- [렌더링](#rendering)
- 블레이드 (#blade)
- 라이브와이어 (#livewire)
- [관성](#inertia)

<a name="introduction"></a>
## 소개

[Laravel Head](https://github.com/laravel/head) 는 제목 및 메타 태그， Open Graph 메타데이터， 정규 URL, 로봇 지침， 성능 힌트 및 구조화된 데이터를 포함하여 애플리케이션의 문서 `<head>` 요소를 관리하기 위한 원활한 API 를 제공합니다. Blade, Livewire 및 Inertia 와 작동합니다。

<a name="installation"></a>
## 설치

Composer 패키지 관리자를 사용하여 Laravel Head 를 설치할 수 있습니다：

```shell
composer require laravel/head
```



<a name="quickstart"></a>
## 빠른 시작

서비스 제공자에 사이트 전체 기본값 등록:

```php
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head
    ->title('Laravel', suffix: ' - Laravel')
    ->description('Build something great.'));
```



런타임에 페이지별 메타데이터 설정:

```php
Head::title($post->title)
    ->description($post->description);
```



해결된 태그를 레이아웃에 렌더링하세요:

```blade
<head>
    @head
</head>
```



<a name="resolution-precedence"></a>
## 우선순위 해상도

페이지 메타데이터는 다섯 계층에서 해상되며, 아래에서 위로 갈수록 우선순위가 높습니다:

1. 페이지 기본값
2. 라우트 그룹 메타데이터
3. 라우트 메타데이터
4. 런타임 메타데이터
5. 오류 메타데이터

상위 계층은 하위 계층을 필드별로 대체합니다. 예를 들어, 런타임 제목은 라우트 제목을 대체하지만 라우트 설명은 대체하지 않습니다. 다음 섹션에서는 각 계층에서 메타데이터를 설정하는 방법을 설명합니다. Blade, Livewire, Inertia에서 해상된 메타데이터를 렌더링하는 방법은 [Rendering](#rendering)을 참조하세요.

<a name="defining-metadata"></a>
## 메타데이터 정의

Laravel Head를 사용하면 사이트 전체 기본값, 라우트 메타데이터, 런타임 호출 및 오류 페이지 정의를 통해 메타데이터를 정의할 수 있습니다.

<a name="defaults"></a>
### 기본값

서비스 프로바이더에서 페이지 기본값을 등록하세요:

```php
use Laravel\Head\Enums\OgType;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(function (HeadBuilder $head) {
    $head
        ->title('Laravel', suffix: ' - Laravel')
        ->description('Build something great.')
        ->canonical()
        ->og(siteName: 'Laravel', type: OgType::Website)
        ->searchableByRobots()
        ->preconnect('https://fonts.example.com');
});
```



기본값은 우선순위가 가장 낮은 페이지 메타데이터 계층입니다. 경로， 런타임 또는 오류 메타데이터가 제목을 설정하지 않으면 `Laravel` 는 있는 그대로 렌더링됩니다. 더 높은 계층이 페이지 제목을 설정하면 상속된 접미사가 적용되므로 `Head::title('About')` 는 `About - Laravel` 를 렌더링합니다. 상속된 접미사나 접두사를 무시해야 하는 제목의 경우 `exact: true` 를 전달합니다。

`Head::canonical()` 를 호출하면 현재 요청 URL 을 사용하여 정규 URL 을 렌더링합니다. 명시적 URL 을 설정하려면 `Head::canonical('/about')` 와 같은 문자열을 전달합니다. 정규 URL 은 기본적으로 `https` 로 정규화됩니다. 요청 스키마를 보존하려면 `forceHttps: false` 를 전달합니다。

로봇 지침은 원시 문자열로， `RobotsRule` 열거 사례로， 또는 두 형식을 혼합한 목록으로 전달될 수 있습니다. 목록은 쉼표로 구분된 지침으로 렌더링되므로 `Head::robots([RobotsRule::NoIndex, RobotsRule::NoFollow])` 는 `noindex, nofollow` 를 렌더링합니다。

편의상 `searchableByRobots` 메서드는 `all` 를 렌더링하고， `hiddenFromRobots` 메서드는 `none` 를 렌더링합니다。

<a name="route-metadata"></a>
### 경로 메타데이터

경로에서 메타데이터를 직접 정의할 수 있습니다. 이는 메타데이터가 미리 알려진 반정적 페이지에 특히 유용합니다。

<a name="routes-and-groups"></a>
#### 경로 및 그룹

```php
Route::view('/contact', 'contact')
    ->name('contact')
    ->withHead(
        title: 'Contact Us',
        description: 'Get in touch.',
    );
```



공유 라우트 메타데이터는 체인 내의 어느 위치에서든 그룹에 적용될 수 있습니다:

```php
Route::withHead(robots: 'noindex, nofollow')
    ->prefix('admin')
    ->name('admin.')
    ->group(function () {
        Route::get('/dashboard', DashboardController::class)
            ->name('dashboard')
            ->withHead(title: 'Dashboard');
    });
```



리소스 및 싱글톤 경로에 대한 메타데이터를 정의할 수도 있습니다:

```php
Route::resource('posts', PostController::class)->withHead(
    robots: 'index, follow',
);

Route::singleton('profile', ProfileController::class)->withHead(
    title: 'Your Profile',
);
```



`withHead` 방법은 Laravel의 기본 라우트 메타데이터 API를 통해 일반 배열을 저장합니다. 이는 `head` 키 하위에 속성을 중첩하여 `metadata` 메서드를 호출하는 것과 동일하므로 메타데이터가 캐시된 라우트와 호환성을 유지합니다.

명명된 인수는 편집기와 정적 분석 도구가 잘못된 이름을 감지할 수 있도록 의도적으로 Laravel Head의 내장 라우트 속성으로 제한됩니다. 커스텀 태그 빌더에 의해 등록된 라우트 속성은 `extensions`를 통해 전달될 수 있습니다:

```php
Route::get('/article', ArticleController::class)->withHead(
    title: 'Article',
    extensions: ['readingTime' => 4],
);
```



<a name="supported-properties"></a>
#### 지원되는 속성

지원되는 경로 속성은 유창한 빌더 메서드와 동일한 이름에 매핑됩니다：

| 카테고리 | 속성 |
| --- | --- |
| 문서 | `title`, `description`, `canonical`, `robots` |
| 애플리케이션 메타데이터 | `themeColor`, `applicationName`, `colorScheme`, `referrer`, `viewport`, `appleWebAppTitle`, `webAppCapable`, `appleWebAppStatusBarStyle` |
| 소셜 | `og`, `ogImage`, `ogVideo`, `ogAudio`, `twitter`, `twitterImage` |
| 성능 | `preload`, `prefetch`, `preconnect`, `dnsPrefetch` |
| 발견 | `alternates`, `feed`, `icon`, `favicon`, `appleTouchIcon`, `appleTouchStartupImage`, `maskIcon`, `manifest` |
| 구조화된 데이터 | `schema` |
| 사용자 지정 태그 | `meta`, `link` |

중첩 옵션 이름은 `forceHttps`, `siteName` 및 `secureUrl` 와 같은 유창한 API 와 동일한 `camelCase` 명명을 사용합니다。

`ogImage`, `preload`, `feed`, `schema`, `icon`, `appleTouchStartupImage` 와 같은 반복 가능한 속성은 단일 값 또는 목록을 허용합니다。

<a name="runtime-metadata"></a>
### 런타임 메타데이터

요청이 도착할 때까지 값을 알 수 없는 경우， 예를 들어 보고 있는 게시물의 제목과 같은 경우， 런타임에서 설정할 수 있습니다：

```php
use Laravel\Head\Facades\Head;

public function __invoke(Post $post): Response
{
    Head::title($post->title);

    // ...
}
```



`Head` 퍼사드를 통해 이루어진 런타임 호출은 요청 종속 데이터에 대한 라우트 메타데이터를 재정의합니다. 컨트롤러와 액션은 이러한 호출이 이루어지는 가장 일반적인 장소입니다:

```php
use App\Models\Post;
use Laravel\Head\Facades\Head;

public function show(Post $post)
{
    Head::title($post->title)
        ->description($post->description);

    return view('posts.show', ['post' => $post]);
}
```



여러 런타임 호출은 실행되는 순서대로 병합됩니다. title, description, canonical URL, robots 지시어와 같은 단일 값 필드의 경우, 나중 호출이 우선합니다. 반복 가능한 필드는 여러 항목을 유지하지만, 동일한 키를 다시 추가하면 이전 항목이 업데이트됩니다. `ogImage` 메서드의 경우, URL이 키입니다:

```php
Head::ogImage('/images/cover.jpg', alt: 'Draft cover')
    ->ogImage('/images/gallery.jpg', alt: 'Gallery image')
    ->ogImage('/images/cover.jpg', alt: 'Final cover', width: 1200, height: 630);
```

```html
<meta property="og:image" content="/images/cover.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Final cover">
<meta property="og:image" content="/images/gallery.jpg">
<meta property="og:image:alt" content="Gallery image">
```



기본값에서 상속된 Open Graph 미디어는 대체 수단으로 작용합니다. 경로, 런타임 또는 오류 메타데이터가 동일한 유형의 자체 미디어를 정의하면 기본 미디어는 병합되는 대신 대체되므로, 페이지의 `og:image`가 사이트 전체 기본 이미지보다 우선합니다.

`when` 및 `unless` 메서드를 사용하여 조건부 메타데이터를 유창하게 정의할 수 있습니다:

```php
Head::title($post->title)
    ->when($post->isDraft(), fn ($head) => $head->hiddenFromRobots());
```



<a name="error-pages"></a>
### 오류 페이지

일반적으로, 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 오류 메타데이터를 등록해야 합니다:

```php
use Laravel\Head\ErrorPages;
use Laravel\Head\Facades\Head;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Head::errors(function (ErrorPages $errors) {
        $errors->defaults(robots: 'noindex, follow');

        $errors->status(
            404,
            title: 'Page Not Found',
            description: 'The page you are looking for could not be found.',
        );
    });
}
```



`defaults`와 `status` 메서드도 `Head::defaults()`에서 사용된 것과 동일한 유창한 빌더 콜백을 허용합니다:

```php
use Laravel\Head\ErrorPages;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::errors(function (ErrorPages $errors) {
    $errors->status(404, fn (HeadBuilder $head) => $head
        ->title('Page Not Found')
        ->description('The page you are looking for could not be found.'));
});
```



등록된 오류 상태에 대한 응답이 렌더링될 때, 해당 메타데이터가 다른 모든 계층보다 우선합니다.

Laravel은 오류 뷰를 렌더링하거나 Inertia의 `handleExceptionsUsing()` 메서드와 같은 응답 단계 훅을 실행할 때 응답 상태를 자동으로 감지합니다. `$exceptions->render()` 콜백 안에서 오류 응답을 렌더링하는 경우, 렌더링 전에 `Head::status(404)`를 호출하여 오류 메타데이터가 적용되도록 하십시오.

<a name="open-graph"></a>
## 오픈 그래프

`og` 메서드를 사용하여 Open Graph 속성을 설정할 수 있습니다. 반복 가능한 미디어는 상위 수준 메서드를 사용하여 추가할 수 있으며, 상위 수준 메서드는 명명된 인수를 직접 받습니다:

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\OgType;

Head::og(type: OgType::Article, title: $post->title)
    ->ogImage($post->hero_image_url)
    ->ogImage(
        $post->gallery_image_url,
        alt: $post->gallery_image_alt,
        width: 1200,
        height: 630,
        type: ImageType::Jpeg,
    );
```



`ogImage`, `ogVideo`, 그리고 `ogAudio` 메서드는 첫 번째 인수로 URL을 받으며, Open Graph 사양에서 지원되는 경우 `alt`, `width`, `height`, `type`, `secureUrl`와 같은 선택적 명명 인수도 함께 받을 수 있습니다.

API가 이미지 `type`를 받는 모든 위치에서 `ImageType` 열거형 케이스로 이미지 MIME 타입을 전달할 수 있으며, 예를 들어 `ImageType::Svg`, `ImageType::Png`, `ImageType::Jpeg`, `ImageType::Webp`가 있습니다.

> [!NOTE]
> 문서 `title`와 `description`는 누락된 `og:title`와 `og:description` 값을 자동으로 채웁니다.

다른 속성이 없는 단일 Open Graph 이미지의 경우, `og` 메서드에 `image` 명명 인수를 전달할 수 있습니다:

```php
Head::og(
    type: OgType::Website,
    title: $page->title,
    description: $page->description,
    image: $page->og_image_url,
);
```



`og(image: ...)`와 `ogImage(...)` 호출은 동일한 기본 이미지 목록에 쓰기 때문에 호출 위치에서 더 표현력이 있는 쪽을 사용하면 됩니다. 제품 또는 기사 속성과 같은 맞춤 Open Graph 확장을 위해 [`meta`](#custom-tags) 메서드를 사용할 수 있습니다.

<a name="twitter-cards"></a>
### X / 트위터 카드

Open Graph에서 사용된 것과 동일한 제목, 설명 및 이미지로 X / 트위터 카드를 렌더링하려면 기본값에 `twitter()`를 등록하세요:

```php
use Laravel\Head\Enums\TwitterCard;
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::defaults(fn (HeadBuilder $head) => $head->twitter(
    card: TwitterCard::SummaryWithLargeImage,
));
```



그런 다음 페이지 수준 메타데이터를 설정합니다:

```php
Head::title('Introducing Laravel Head')
    ->description('A fluent API for Laravel document head metadata.')
    ->ogImage('https://example.com/social.jpg', alt: 'Introducing Laravel Head');
```



이것은 일치하는 트위터 태그를 렌더링합니다:

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Introducing Laravel Head">
<meta name="twitter:description" content="A fluent API for Laravel document head metadata.">
<meta name="twitter:image" content="https://example.com/social.jpg">
<meta name="twitter:image:alt" content="Introducing Laravel Head">
```



개별 페이지를 명시적인 Twitter 값으로 사용자 정의할 수 있습니다:

```php
Head::twitter(title: $post->social_title)
    ->twitterImage($post->social_image_url, alt: $post->title);
```



루트 메타데이터는 `twitter`와 `twitterImage`를 허용합니다.

<a name="theme-colors"></a>
## 테마 색상

테마 색상은 전역, 개별 루트별 또는 런타임에 설정할 수 있습니다:

```php
Head::themeColor('#0f172a');
```



이것은 `<meta name="theme-color">` 태그를 렌더링합니다. 미디어별 테마 색상을 위해 `Media` 열거형을 사용할 수 있습니다:

```php
use Laravel\Head\Enums\Media;

Head::themeColor('#ffffff', media: Media::Light)
    ->themeColor('#111827', media: Media::Dark);
```



`Media` 열거형에는 `Portrait` 및 `Landscape`도 포함됩니다. `media` 인수는 사용자 지정 미디어 쿼리 문자열도 허용합니다.

라우트 메타데이터는 동일한 `camelCase` 키를 통해 단일 테마 색상을 지원합니다:

```php
Route::view('/dashboard', 'dashboard')->withHead(
    themeColor: '#0f172a',
);
```



<a name="app-metadata-and-icons"></a>
## 애플리케이션 메타데이터 및 아이콘

Laravel Head는 일반적인 브라우저 및 애플리케이션 메타데이터를 위한 메서드를 포함합니다:

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\Media;

Head::applicationName('Laravel')
    ->colorScheme('light dark')
    ->referrer('strict-origin-when-cross-origin')
    ->viewport('width=device-width, initial-scale=1')
    ->appleWebAppTitle('Laravel')
    ->webAppCapable()
    ->appleWebAppStatusBarStyle('black')
    ->favicon('/favicon.svg', type: ImageType::Svg)
    ->icon('/favicon-32x32.png', type: ImageType::Png, sizes: '32x32')
    ->appleTouchIcon('/apple-touch-icon.png', sizes: '180x180')
    ->appleTouchStartupImage('/launch.png', media: Media::Portrait)
    ->maskIcon('/safari-pinned-tab.svg', color: '#111827')
    ->manifest('/site.webmanifest');
```



`favicon` 메서드는 `icon` 메서드의 별칭이며 동일한 `type`, `sizes`, `media` 인수를 허용합니다.

라우트 메타데이터는 동일한 이름을 사용합니다:

```php
use Laravel\Head\Enums\ImageType;
use Laravel\Head\Enums\Media;

Route::view('/dashboard', 'dashboard')->withHead(
    applicationName: 'Laravel',
    colorScheme: 'light dark',
    appleWebAppTitle: 'Laravel',
    webAppCapable: true,
    appleWebAppStatusBarStyle: 'black',
    favicon: [
        ['href' => '/favicon.svg', 'type' => ImageType::Svg],
        ['href' => '/favicon-32x32.png', 'type' => ImageType::Png, 'sizes' => '32x32'],
    ],
    appleTouchIcon: ['href' => '/apple-touch-icon.png', 'sizes' => '180x180'],
    appleTouchStartupImage: ['href' => '/launch.png', 'media' => Media::Portrait],
    manifest: '/site.webmanifest',
);
```



<a name="progressive-web-apps"></a>
## 점진적 웹 앱

`pwa` 방법은 설치 가능한 웹 앱에 필요한 공통 문서 `<head>` 태그를 구성합니다:

```php
Head::pwa(
    name: 'Laravel',
    manifest: '/site.webmanifest',
    themeColor: '#0f172a',
    appleTouchIcon: '/apple-touch-icon.png',
    appleWebAppStatusBarStyle: 'black',
);
```



이것은 애플리케이션 이름, 웹 애플리케이션 매니페스트 링크 및 iOS 독립형 메타데이터를 렌더링합니다. 제공된 경우, 테마 색상, Apple 상태 표시줄 스타일, Apple 터치 아이콘도 렌더링됩니다. 웹 애플리케이션 매니페스트 생성과 서비스 워커 등록은 여전히 애플리케이션의 책임입니다.

기본값이나 런타임 메타데이터에서 `pwa` 방법을 사용할 수 있습니다. 라우트 메타데이터는 위에서 표시된 개별 속성을 지원합니다.

<a name="performance-and-discovery"></a>
## 성능 및 검색

Laravel Head는 성능 힌트, 페이지네이션 링크, 로케일 대체 및 피드 검색을 렌더링합니다:

```php
Head::preload(asset('fonts/inter.woff2'), as: 'font', crossorigin: true)
    ->prefetch(asset('images/next.webp'))
    ->preconnect('https://cdn.example.com')
    ->dnsPrefetch('https://analytics.example.com')
    ->paginate($posts)
    ->alternates([
        'en' => 'https://example.com/en/about',
        'fr' => 'https://example.com/fr/about',
        'x-default' => 'https://example.com/about',
    ])
    ->feed('/feed', title: 'Laravel RSS')
    ->feed('/feed.atom', type: 'atom', title: 'Laravel Atom');
```



로컬 자산의 경우, `preloadAsset()`와 `prefetchAsset()`는 `asset()` 헬퍼를 통해 URL을 해결하고 파일 확장자에서 `as` 속성을 감지합니다. 폰트 프리로드는 자동으로 `crossorigin`를 포함하며, 프리로드 명세에서는 동일 출처 폰트에도 이를 요구합니다:

```php
Head::preloadAsset('fonts/inter.woff2')
    ->prefetchAsset('images/next.webp');
```

```html
<link rel="preload" href="https://example.com/fonts/inter.woff2" as="font" crossorigin>
<link rel="prefetch" href="https://example.com/images/next.webp" as="image">
```



명시적으로 `as`를 전달하여 감지를 무시할 수 있습니다. `preloadAsset` 메서드는 브라우저가 이 속성이 없는 사전 로드를 무시하기 때문에 확장에서 `as` 속성을 감지할 수 없으면 예외를 발생시킵니다; `prefetchAsset` 메서드는 단순히 이를 생략합니다.

<a name="custom-tags"></a>
## 사용자 정의 태그

전용 메서드가 없는 태그의 경우 `meta()` 및 `link()`를 사용하세요:

```php
Head::meta('format-detection', 'telephone=no')
    ->meta('article:author', $post->author->name)
    ->link('search', '/opensearch.xml', [
        'type' => 'application/opensearchdescription+xml',
        'title' => 'Laravel Search',
    ])
    ->link('me', 'https://social.example.com/@laravel');
```



브라우저가 일치하는 조건에서만 태그를 적용해야 할 때, 메타 태그에 미디어 쿼리를 포함할 수 있습니다:

```php
use Laravel\Head\Enums\Media;

Head::meta('theme-color', '#ffffff', media: Media::Light)
    ->meta('theme-color', '#111827', media: Media::Dark);
```



`meta` 방법은 일반 메타 태그에 `name` 속성을 사용합니다. 일반적으로 Open Graph(`og:`)나 기사 메타데이터(`article:`)와 같이 `property` 속성을 사용하는 키의 경우, 이 방법은 자동으로 전환됩니다:

```php
Head::meta('description', 'About Laravel')
    ->meta('og:title', 'About Laravel');
```

```html
<meta name="description" content="About Laravel">
<meta property="og:title" content="About Laravel">
```



명시적으로 어느 속성을 선택하려면 `property: true` 또는 `property: false`를 전달할 수 있습니다.

<a name="schemas"></a>
## 스키마

내장 스키마 빌더는 일반적인 JSON-LD 유형을 다룹니다:

```php
use Laravel\Head\Enums\OfferAvailability;
use Laravel\Head\Facades\Schema;

Head::schema(
    Schema::product()
        ->name($product->name)
        ->offers(
            Schema::offer()
                ->price($product->price)
                ->currency('USD')
                ->availability(OfferAvailability::InStock)
        )
);
```



내장된 팩토리 메서드는 `article`, `blogPosting`, `product`, `offer`, `brand`, `breadcrumbs`, `faq`, `organization`, `person`, `webPage`, 그리고 `webSite`입니다. 알 수 없는 팩토리 메서드는 일반 스키마 객체를 생성하므로, 여전히 맞춤 schema.org 타입을 표현할 수 있습니다.

JSON-LD 스키마 데이터가 유효하지 않은 경우, Laravel Head는 비프로덕션 환경에서는 예외를 발생시키고, 프로덕션 환경에서는 경고를 기록합니다.

<a name="breadcrumbs"></a>
### 브레드크럼

브레드크럼 항목은 한 번에 하나씩 또는 일괄적으로 추가할 수 있습니다. 위치는 항목이 추가되는 순서에 따라 자동으로 할당됩니다:

```php
Head::schema(
    Schema::breadcrumbs()->items([
        'Home' => route('home'),
        'Shop' => route('shop.index'),
        'Shoes' => route('shop.category', 'shoes'),
    ])
);
```



단일 빵부스러기 항목을 추가하려면 `item` 방법을 사용할 수 있습니다:

```php
Schema::breadcrumbs()
    ->item('Home', route('home'))
    ->item('Shop', route('shop.index'));
```



<a name="faqs"></a>
### 자주 묻는 질문(FAQs)

FAQ 항목은 동일한 패턴을 따릅니다. `question` 방법을 사용하여 하나씩 추가하거나 `questions` 방법을 사용하여 한 번에 여러 항목을 추가할 수 있습니다:

```php
Head::schema(
    Schema::faq()->questions([
        'What is Laravel Head?' => 'A fluent API for managing the document head.',
        'Is it free?' => 'Yes, it is open source.',
    ])
);
```



<a name="custom-schemas"></a>
### 사용자 정의 스키마

사용자가 명시적으로 사용자 정의 스키마 유형을 등록할 수 있습니다:

```php
use DateTimeInterface;
use Laravel\Head\Facades\Schema;
use Laravel\Head\Schema\SchemaObject;
use Laravel\Head\SchemaType;

#[SchemaType('JobPosting')]
class JobPosting extends SchemaObject
{
    public function title(string $title): static
    {
        return $this->set('title', $title);
    }

    public function datePosted(DateTimeInterface|string $date): static
    {
        return $this->date('datePosted', $date);
    }
}

Schema::register(JobPosting::class);

Head::schema(
    Schema::jobPosting()
        ->title('Senior Laravel Developer')
        ->datePosted(now())
);
```



<a name="rendering"></a>
## 렌더링

Laravel Head는 현재 응답의 페이지 메타데이터를 태그로 변환합니다. 이러한 태그가 렌더링되는 방식은 애플리케이션 스택에 따라 다릅니다.

HTML 렌더러는 `@head` 지시문과 Laravel Head가 Inertia에 `head` prop을 통해 공유하는 렌더링된 요소를 지원합니다. 배열 렌더러는 구조화된 데이터로 해결된 메타데이터가 필요한 애플리케이션에서 `Head::toArray()`를 지원합니다.

<a name="blade"></a>
### 블레이드

레이아웃의 `<head>`에서 `@head` 지시문을 사용하여 누적된 태그를 렌더링합니다:

```blade
<head>
    <meta charset="utf-8">
    @head
</head>
```



`@head` 지시문은 동기적으로 렌더링되므로 레이아웃이 렌더링되기 전에 페이지 메타데이터를 정의해야 합니다.

<a name="livewire"></a>
### 라이브와이어

라이브와이어 애플리케이션은 문서 레이아웃에서 동일한 `@head` 지시문을 사용합니다:

```blade
<head>
    @head
</head>

<body>
    {{ $slot }}

    @livewireScripts
</body>
```



Livewire 전용 설정은 필요하지 않습니다. Laravel 헤드 메타데이터는 요청별로 해결되며, 리졸버는 요청 스코프입니다. 따라서 각 `wire:navigate` 방문은 목적지 경로의 메타데이터를 반영한 새로운 문서를 가져옵니다. `wire:navigate`를 사용하여 방문한 페이지는 컴포넌트 수준의 헤드 코드를 요구하지 않고도 적절한 경로, 런타임 및 오류 메타데이터를 받습니다.

<a name="inertia"></a>
### Inertia

Inertia 자체 구성 요소와 함께 Inertia 루트 템플릿에서 동일한 `@head` 지시문을 사용합니다:

```blade
<html>
<head>
    <meta charset="utf-8">
    @head

    @viteReactRefresh
    @vite(['resources/css/app.css', 'resources/js/app.tsx'])
    <x-inertia::head />
</head>
<body>
    <x-inertia::app />
</body>
</html>
```



Inertia가 설치되면, Laravel Head는 페이지에서 관리되는 head를 각 페이지 객체의 `head` 속성 아래에 렌더링된 요소 문자열 배열로 자동으로 공유합니다:

```json
{
    "props": {
        "head": [
            "<title data-inertia=\"title\">Dashboard - Laravel</title>",
            "<meta data-inertia=\"description\" name=\"description\" content=\"Your application overview.\">"
        ]
    }
}
```



애플리케이션에서 `createInertiaApp()`를 호출하는 모든 곳에서 Inertia의 `serverHead` 옵션을 활성화하세요. 이 옵션은 Inertia 3.5 이상에서 사용 가능합니다:

```js
createInertiaApp({
    // ...
    serverHead: true,
});
```



각 페이지 관리 요소에는 안정적인 `data-inertia` 키가 있습니다. `@head` 디렉티브는 초기 문서를 렌더링하며， 그 후 관성은 해당 요소들을 채택하여 표준 방문， [인스턴트 방문](https://inertiajs.com/docs/v3/the-basics/instant-visits) 및 역방향 및 순방향 탐색 중에 동기화를 유지합니다. 요소들은 초기 HTML 응답에 존재하므로， 크롤러와 링크 미리보기 봇은 JavaScript 를 실행하지 않고도 이를 읽을 수 있습니다. 클라이언트 측 `<Head>` 구성 요소는 필요하지 않습니다。

이는 [서버 측 렌더링 (SSR)](https://inertiajs.com/docs/v3/advanced/server-side-rendering) 과 함께 또는 함께 작동합니다. 애플리케이션에 별도의 SSR 엔트리 포인트가 있는 경우 거기에서도 `serverHead` 를 활성화합니다. Laravel 헤드는 JavaScript SSR 에서 생성된 다른 헤더 요소를 보존하면서 `@head` 와 `<x-inertia::head />` 간의 페이지 관리 요소를 순서에 관계없이 자동으로 중복 제거합니다。

> [!NOTE]
> 기존 Inertia 애플리케이션에 Laravel Head 를 추가할 때， Laravel Head 가 최종 문서 제목을 관리할 수 있도록 `resources/js/app.tsx` 및 `resources/js/ssr.tsx` 에서 제목 콜백을 제거하고， Inertia 의 [`<Head>` 구성 요소](https://inertiajs.com/docs/v3/the-basics/title-and-meta) 에서 관리하는 태그를 Laravel Head 로 이동하여 두 요소가 동일한 요소를 정의하지 않도록 합니다。

`head` 프로퍼는 부분 다시 로드 응답에서 생략되므로 관성은 마지막 전체 페이지 헤더를 유지합니다. 인스턴트 방문도 백그라운드 응답이 도착할 때까지 현재 헤더를 유지합니다。

```php
use Laravel\Head\Facades\Head;

public function boot(): void
{
    Head::inertia(prop: '_head');
}
```



그런 다음 `serverHead: '_head'`로 같은 prop에 Inertia를 지정합니다.

<a name="static-inertia-tags"></a>
#### 정적 Inertia 태그

대부분의 태그는 기본값, 라우트 메타데이터 또는 런타임 메타데이터에 있어야 하며, 그래야 Laravel Head가 각 페이지에 대한 올바른 값을 해결할 수 있습니다. Inertia 글로벌은 첫 번째 HTML 응답에서 렌더링되고 Inertia에 의해 세션 동안 변경되지 않은 문서 태그에만 사용하세요.

`Head::inertiaGlobals()`와 함께 서비스 프로바이더에 등록하세요:

```php
use Laravel\Head\Facades\Head;
use Laravel\Head\HeadBuilder;

Head::inertiaGlobals(function (HeadBuilder $head) {
    $head
        ->viewport('width=device-width, initial-scale=1')
        ->colorScheme('light dark')
        ->icon('/favicon.svg', type: 'image/svg+xml')
        ->appleTouchIcon('/apple-touch-icon.png', sizes: '180x180')
        ->manifest('/site.webmanifest');
});
```

관성 글로벌(Inertia globals)은 `head` 속성에서 제외되며, `data-inertia` 소유 속성 없이 렌더링되고, 첫 번째 응답 이후에는 절대 업데이트되지 않습니다. 이러한 글로벌은 뷰포트, 색상 체계, 파비콘, 터치 아이콘, 매니페스트와 같은 안정적인 브라우저 힌트에 적합합니다. 만약 태그가 페이지별이거나 SEO 관련이거나 나중에 덮어쓸 가능성이 있다면, 대신 `defaults`, 라우트 메타데이터, 또는 런타임 메타데이터에 넣으세요.

렌더링된 태그 대신 구조화된 데이터로 해결된 메타데이터가 필요한 애플리케이션은 `Head::toArray()`를 호출할 수 있습니다. 반환되는 데이터에는 제목, Open Graph 값, JSON-LD 스키마 및 기타 해결된 메타데이터가 포함됩니다.
{% endraw %}
