---
layout: docs
title: "Asset Bundling (Vite)"
---

{% raw %}
# Asset Bundling (Vite)

- [Introduction](#introduction)
- [Installation & Setup](#installation)
  - [Installing Node](#installing-node)
  - [Installing Vite and the Laravel Plugin](#installing-vite-and-laravel-plugin)
  - [Configuring Vite](#configuring-vite)
  - [Loading Your Scripts and Styles](#loading-your-scripts-and-styles)
- [Running Vite](#running-vite)
- [Working With JavaScript](#working-with-scripts)
  - [Aliases](#aliases)
  - [Vue](#vue)
  - [React](#react)
  - [Svelte](#svelte)
  - [Inertia](#inertia)
  - [URL Processing](#url-processing)
- [Working With Stylesheets](#working-with-stylesheets)
- [Working With Fonts](#working-with-fonts)
  - [Font Providers](#font-providers)
  - [Local Fonts](#local-fonts)
  - [Font Options](#font-options)
- [Working With Blade and Routes](#working-with-blade-and-routes)
  - [Processing Static Assets With Vite](#blade-processing-static-assets)
  - [Refreshing on Save](#blade-refreshing-on-save)
  - [Aliases](#blade-aliases)
- [Asset Prefetching](#asset-prefetching)
- [Custom Base URLs](#custom-base-urls)
- [Environment Variables](#environment-variables)
- [Disabling Vite in Tests](#disabling-vite-in-tests)
- [Server-Side Rendering (SSR)](#ssr)
- [Script and Style Tag Attributes](#script-and-style-attributes)
  - [Content Security Policy (CSP) Nonce](#content-security-policy-csp-nonce)
  - [Subresource Integrity (SRI)](#subresource-integrity-sri)
  - [Arbitrary Attributes](#arbitrary-attributes)
- [Advanced Customization](#advanced-customization)
  - [Dev Server Cross-Origin Resource Sharing (CORS)](#cors)
  - [Correcting Dev Server URLs](#correcting-dev-server-urls)

<a name="introduction"></a>
## Introduction

[Vite](https://vitejs.dev) is a modern frontend build tool that provides an extremely fast development environment and bundles your code for production. When building applications with Laravel, you will typically use Vite to bundle your application's CSS and JavaScript files into production-ready assets.

Laravel integrates seamlessly with Vite by providing an official plugin and Blade directive to load your assets for development and production.

<a name="installation"></a>
## Installation & Setup



> [!NOTE]
> 다음 문서는 Laravel Vite 플러그인을 수동으로 설치하고 구성하는 방법을 다룹니다. 그러나 Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 이 모든 스캐폴딩이 포함되어 있으며, Laravel과 Vite를 시작하는 가장 빠른 방법입니다.

<a name="installing-node"></a>
### Node 설치

Vite와 Laravel 플러그인을 실행하기 전에 Node.js(16+)와 NPM이 설치되어 있는지 확인해야 합니다:

```shell
node -v
npm -v
```



공식 Node 웹사이트([the official Node website](https://nodejs.org/en/download/))에서 제공하는 간단한 그래픽 설치 프로그램을 사용하여 최신 버전의 Node와 NPM을 쉽게 설치할 수 있습니다. 또는 [Laravel Sail](https://laravel.com/docs/{{version}}/sail)을 사용 중이라면 Sail을 통해 Node와 NPM을 실행할 수 있습니다:

```shell
./vendor/bin/sail node -v
./vendor/bin/sail npm -v
```



<a name="installing-vite-and-laravel-plugin"></a>
### Vite와 Laravel 플러그인 설치

새로운 Laravel 설치 내에서, 애플리케이션 디렉토리 구조의 루트에 `package.json` 파일을 찾을 수 있습니다. 기본 `package.json` 파일에는 Vite와 Laravel 플러그인을 사용하기 시작하는 데 필요한 모든 것이 이미 포함되어 있습니다. NPM을 통해 애플리케이션의 프론트엔드 의존성을 설치할 수 있습니다:

```shell
npm install
```



<a name="configuring-vite"></a>
### Vite 설정

Vite는 프로젝트 루트에 있는 `vite.config.js` 파일을 통해 설정됩니다. 필요에 따라 이 파일을 자유롭게 사용자 정의할 수 있으며, `@vitejs/plugin-react`, `@sveltejs/vite-plugin-svelte` 또는 `@vitejs/plugin-vue`와 같은 애플리케이션에 필요한 다른 플러그인도 설치할 수 있습니다.

Laravel Vite 플러그인은 애플리케이션의 진입점을 지정해야 합니다. 이들은 JavaScript 또는 CSS 파일일 수 있으며, TypeScript, JSX, TSX, Sass와 같은 전처리 언어도 포함됩니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css',
            'resources/js/app.js',
        ]),
    ],
});
```



SPA를 구축하는 경우, Inertia를 사용하여 만든 애플리케이션을 포함하여, Vite는 CSS 진입점을 사용하지 않을 때 가장 잘 작동합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel([
            'resources/css/app.css', // [tl! remove]
            'resources/js/app.js',
        ]),
    ],
});
```



대신, CSS를 JavaScript를 통해 가져와야 합니다. 일반적으로 이는 애플리케이션의 `resources/js/app.js` 파일에서 수행됩니다:

```js
import './bootstrap';
import '../css/app.css'; // [tl! add]
```



Laravel 플러그인은 또한 여러 진입점과 [SSR 진입점](#ssr)과 같은 고급 구성 옵션을 지원합니다.

<a name="working-with-a-secure-development-server"></a>
#### 보안 개발 서버 사용하기

로컬 개발 웹 서버가 HTTPS를 통해 애플리케이션을 제공하는 경우, Vite 개발 서버에 연결할 때 문제가 발생할 수 있습니다.

[Laravel Herd](https://herd.laravel.com)를 사용하여 사이트를 보안 처리했거나 [Laravel Valet](/docs/{{version}}/valet)를 사용하여 애플리케이션에 대해 [secure 명령](/docs/{{version}}/valet#securing-sites)을 실행했다면, Laravel Vite 플러그인은 생성된 TLS 인증서를 자동으로 감지하고 사용합니다.

애플리케이션 디렉토리 이름과 일치하지 않는 호스트를 사용하여 사이트를 보안 처리한 경우, 애플리케이션의 `vite.config.js` 파일에서 호스트를 수동으로 지정할 수 있습니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            detectTls: 'my-app.test', // [tl! add]
        }),
    ],
});
```



다른 웹 서버를 사용할 때는 신뢰할 수 있는 인증서를 생성하고 생성된 인증서를 사용하도록 Vite를 수동으로 구성해야 합니다:

```js
// ...
import fs from 'fs'; // [tl! add]

const host = 'my-app.test'; // [tl! add]

export default defineConfig({
    // ...
    server: { // [tl! add]
        host, // [tl! add]
        hmr: { host }, // [tl! add]
        https: { // [tl! add]
            key: fs.readFileSync(`/path/to/${host}.key`), // [tl! add]
            cert: fs.readFileSync(`/path/to/${host}.crt`), // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```



시스템에 신뢰할 수 있는 인증서를 생성할 수 없는 경우, [@vitejs/plugin-basic-ssl 플러그인](https://github.com/vitejs/vite-plugin-basic-ssl)을 설치하고 구성할 수 있습니다. 신뢰할 수 없는 인증서를 사용할 때는 `npm run dev` 명령을 실행할 때 콘솔의 "Local" 링크를 따라 브라우저에서 Vite 개발 서버의 인증서 경고를 수락해야 합니다.

<a name="configuring-hmr-in-sail-on-wsl2"></a>
#### WSL2에서 Sail로 개발 서버 실행

Windows Subsystem for Linux 2(WSL2)에서 [Laravel Sail](/docs/{{version}}/sail) 내에서 Vite 개발 서버를 실행할 때, 브라우저가 개발 서버와 통신할 수 있도록 `vite.config.js` 파일에 다음 구성을 추가해야 합니다:

```js
// ...

export default defineConfig({
    // ...
    server: { // [tl! add:start]
        hmr: {
            host: 'localhost',
        },
    }, // [tl! add:end]
});
```



개발 서버가 실행되는 동안 파일 변경 사항이 브라우저에 반영되지 않는 경우, Vite의 [server.watch.usePolling 옵션](https://vitejs.dev/config/server-options.html#server-watch)을 구성해야 할 수도 있습니다.

<a name="loading-your-scripts-and-styles"></a>
### 스크립트 및 스타일 로드하기

Vite 진입점을 구성한 후에는, 애플리케이션 루트 템플릿의 `<head>`에 추가하는 `@vite()` Blade 지시어에서 이를 참조할 수 있습니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
```



CSS를 JavaScript를 통해 가져오고 있다면, JavaScript 진입점만 포함하면 됩니다:

```blade
<!DOCTYPE html>
<head>
    {{-- ... --}}

    @vite('resources/js/app.js')
</head>
```



`@vite` 지시어는 Vite 개발 서버를 자동으로 감지하고 Vite 클라이언트를 주입하여 핫 모듈 교체(HMR)를 활성화합니다. 빌드 모드에서는 지시어가 컴파일된 버전 관리된 자산과 가져온 CSS를 포함하여 모든 자산을 로드합니다.

필요한 경우 `@vite` 지시어를 호출할 때 컴파일된 자산의 빌드 경로를 지정할 수도 있습니다:

```blade
<!doctype html>
<head>
    {{-- Given build path is relative to public path. --}}

    @vite('resources/js/app.js', 'vendor/courier/build')
</head>
```



<a name="inline-assets"></a>
#### 인라인 자산

때때로 자산의 버전된 URL에 연결하는 대신 자산의 원시 내용을 포함해야 할 필요가 있을 수 있습니다. 예를 들어, PDF 생성기에 HTML 콘텐츠를 전달할 때 자산 내용을 페이지에 직접 포함해야 할 수 있습니다. `Vite` 퍼사드에서 제공하는 `content` 메서드를 사용하여 Vite 자산의 내용을 출력할 수 있습니다:

```blade
@use('Illuminate\Support\Facades\Vite')

<!doctype html>
<head>
    {{-- ... --}}

    <style>
        {!! Vite::content('resources/css/app.css') !!}
    </style>
    <script>
        {!! Vite::content('resources/js/app.js') !!}
    </script>
</head>
```



<a name="running-vite"></a>
## Vite 실행하기

Vite를 실행하는 방법은 두 가지가 있습니다. `dev` 명령어를 통해 개발 서버를 실행할 수 있으며, 이는 로컬에서 개발할 때 유용합니다. 개발 서버는 파일의 변경 사항을 자동으로 감지하고, 열려 있는 브라우저 창에 즉시 반영합니다.

또는 `build` 명령어를 실행하면 애플리케이션의 자산을 버전 관리하고 번들하여 배포 준비를 할 수 있습니다:

```shell
# Run the Vite development server...
npm run dev

# Build and version the assets for production...
npm run build
```



만약 당신이 WSL2에서 [Sail](/docs/{{version}}/sail) 개발 서버를 실행하고 있다면, 일부 [추가 구성](#configuring-hmr-in-sail-on-wsl2) 옵션이 필요할 수 있습니다.

<a name="working-with-scripts"></a>
## 자바스크립트 작업하기

<a name="aliases"></a>
### 별칭

기본적으로, Laravel 플러그인은 공통 별칭을 제공하여 신속하게 시작하고 애플리케이션의 자산을 편리하게 가져올 수 있도록 도와줍니다:

```js
{
    '@' => '/resources/js'
}
```



`vite.config.js` 구성 파일에 자신의 별칭을 추가하여 `'@'` 별칭을 덮어쓸 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel(['resources/ts/app.tsx']),
    ],
    resolve: {
        alias: {
            '@': '/resources/ts',
        },
    },
});
```



<a name="vue"></a>
### Vue

[Vue](https://vuejs.org/) 프레임워크를 사용하여 프론트엔드를 구축하려는 경우, `@vitejs/plugin-vue` 플러그인도 설치해야 합니다:

```shell
npm install --save-dev @vitejs/plugin-vue
```



그런 다음 플러그인을 `vite.config.js` 구성 파일에 포함할 수 있습니다. Laravel과 함께 Vue 플러그인을 사용할 때 필요한 몇 가지 추가 옵션이 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.js']),
        vue({
            template: {
                transformAssetUrls: {
                    // The Vue plugin will re-write asset URLs, when referenced
                    // in Single File Components, to point to the Laravel web
                    // server. Setting this to `null` allows the Laravel plugin
                    // to instead re-write asset URLs to point to the Vite
                    // server instead.
                    base: null,

                    // The Vue plugin will parse absolute URLs and treat them
                    // as absolute paths to files on disk. Setting this to
                    // `false` will leave absolute URLs un-touched so they can
                    // reference assets in the public directory as expected.
                    includeAbsolute: false,
                },
            },
        }),
    ],
});
```



> [!NOTE]
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)는 이미 적절한 Laravel, Vue, Vite 구성을 포함하고 있습니다. 이 스타터 키트는 Laravel, Vue, Vite로 시작하는 가장 빠른 방법을 제공합니다.

<a name="react"></a>
### React

프론트엔드를 [React](https://reactjs.org/) 프레임워크를 사용하여 구축하려면, `@vitejs/plugin-react` 플러그인도 설치해야 합니다:

```shell
npm install --save-dev @vitejs/plugin-react
```



그런 다음 플러그인을 `vite.config.js` 구성 파일에 포함할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [
        laravel(['resources/js/app.jsx']),
        react(),
    ],
});
```



JSX를 포함하는 모든 파일이 `.jsx` 또는 `.tsx` 확장자를 갖도록 해야 하며, 필요한 경우 [위에 표시된 대로](#configuring-vite) 진입점을 업데이트해야 합니다.

기존 `@vite` 지시문과 함께 추가 `@viteReactRefresh` Blade 지시문도 포함해야 합니다.

```blade
@viteReactRefresh
@vite('resources/js/app.jsx')
```



`@viteReactRefresh` 지시문은 `@vite` 지시문보다 먼저 호출되어야 합니다.

> [!NOTE]
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 적절한 Laravel, React, Vite 구성이 포함되어 있습니다. 이 스타터 키트는 Laravel, React, Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="svelte"></a>
### Svelte

[Сvelte](https://svelte.dev/) 프레임워크를 사용하여 프론트엔드를 구축하려는 경우 `@sveltejs/vite-plugin-svelte` 플러그인도 설치해야 합니다:

```shell
npm install --save-dev @sveltejs/vite-plugin-svelte
```



그런 다음 플러그인을 `vite.config.js` 구성 파일에 포함할 수 있습니다.

```js
import { svelte } from '@sveltejs/vite-plugin-svelte';
import laravel from 'laravel-vite-plugin';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [
    laravel({
      input: ['resources/js/app.ts'],
      ssr: 'resources/js/ssr.ts',
      refresh: true,
    }),
    svelte(),
  ],
});
```



> [!NOTE]
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 올바른 Laravel, Svelte 및 Vite 구성이 포함되어 있습니다. 이 스타터 키트는 Laravel, Svelte, Vite로 시작하는 가장 빠른 방법을 제공합니다.

<a name="inertia"></a>
### Inertia

Laravel Vite 플러그인은 Inertia 페이지 컴포넌트를 해결하는 데 도움이 되는 편리한 `resolvePageComponent` 함수를 제공합니다. 아래는 Vue 3에서 이 헬퍼를 사용하는 예제입니다. 그러나 React 또는 Svelte와 같은 다른 프레임워크에서도 이 함수를 사용할 수 있습니다:

```js
import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import { resolvePageComponent } from 'laravel-vite-plugin/inertia-helpers';

createInertiaApp({
  resolve: (name) => resolvePageComponent(`./Pages/${name}.vue`, import.meta.glob('./Pages/**/*.vue')),
  setup({ el, App, props, plugin }) {
    createApp({ render: () => h(App, props) })
      .use(plugin)
      .mount(el)
  },
});
```



If you are using Vite's code splitting feature with Inertia, we recommend configuring [asset prefetching](#asset-prefetching).

> [!NOTE]
> Laravel's [starter kits](/docs/{{version}}/starter-kits) already include the proper Laravel, Inertia, and Vite configuration. These starter kits offer the fastest way to get started with Laravel, Inertia, and Vite.

<a name="url-processing"></a>
### URL Processing

When using Vite and referencing assets in your application's HTML, CSS, or JS, there are a couple of caveats to consider. First, if you reference assets with an absolute path, Vite will not include the asset in the build; therefore, you should ensure that the asset is available in your public directory. You should avoid using absolute paths when using a [dedicated CSS entrypoint](#configuring-vite) because, during development, browsers will try to load these paths from the Vite development server, where the CSS is hosted, rather than from your public directory.

When referencing relative asset paths, you should remember that the paths are relative to the file where they are referenced. Any assets referenced via a relative path will be re-written, versioned, and bundled by Vite.

Consider the following project structure:

```text
public/
  taylor.png
resources/
  js/
    Pages/
      Welcome.vue
  images/
    abigail.png
```



다음 예제는 Vite가 상대 URL과 절대 URL을 처리하는 방식을 보여줍니다:

```html
<!-- This asset is not handled by Vite and will not be included in the build -->
<img src="/taylor.png">

<!-- This asset will be re-written, versioned, and bundled by Vite -->
<img src="../../images/abigail.png">
```



<a name="working-with-stylesheets"></a>
## 스타일시트 사용하기

> [!NOTE]
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 적절한 Tailwind 및 Vite 구성이 포함되어 있습니다. 또는, 저희 스타터 키트 중 하나를 사용하지 않고 Tailwind와 Laravel을 사용하고자 한다면, [Laravel용 Tailwind 설치 가이드](https://tailwindcss.com/docs/guides/laravel)를 확인하세요.

모든 Laravel 애플리케이션에는 이미 Tailwind와 적절히 구성된 `vite.config.js` 파일이 포함되어 있습니다. 따라서 Vite 개발 서버를 시작하거나 `dev` Composer 명령어를 실행하기만 하면, Laravel과 Vite 개발 서버를 모두 시작할 수 있습니다:

```shell
composer run dev
```



당신의 애플리케이션 CSS는 `resources/css/app.css` 파일 안에 배치될 수 있습니다.

<a name="working-with-fonts"></a>
## 폰트 작업

Laravel Vite 플러그인은 애플리케이션을 위해 최적화된 자체 호스팅 폰트를 제공할 수 있습니다. 폰트가 구성되면, 플러그인은 요청된 폰트 파일을 해결하고, 이를 Vite 자산으로 내보내며, 폰트 CSS를 생성하고, Blade의 [`@fonts` 지시문](/docs/{{version}}/blade#fonts)에서 사용할 수 있는 폰트 매니페스트를 작성합니다.

폰트를 구성하려면, `laravel-vite-plugin/fonts`에서 하나 이상의 제공자(helper)를 가져오고 이를 Laravel 플러그인의 `fonts` 옵션에 추가하세요.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { google } from 'laravel-vite-plugin/fonts';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            fonts: [
                google('Inter', {
                    alias: 'sans',
                    weights: [400, 500, 600, 700],
                    styles: ['normal', 'italic'],
                    subsets: ['latin'],
                    display: 'swap',
                    preload: [
                        { weight: 400 },
                        { weight: 700 },
                    ],
                    fallbacks: ['system-ui', 'sans-serif'],
                }),
            ],
        }),
    ],
});
```



이 예제에서 `Inter` 폰트는 `sans` 별칭을 통해 사용할 수 있습니다. 플러그인은 생성된 폰트 스택을 적용하는 `--font-sans` CSS 변수와 `.font-sans` 유틸리티 클래스를 생성합니다.

<a name="font-providers"></a>
### 폰트 제공자

Laravel Vite 플러그인은 Google Fonts, Bunny Fonts, Fontsource, 그리고 로컬 폰트에 대한 제공자 헬퍼를 포함합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { bunny, fontsource, google, local } from 'laravel-vite-plugin/fonts';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            fonts: [
                google('Inter', { alias: 'sans' }),
                bunny('Figtree', { alias: 'body' }),
                fontsource('JetBrains Mono', { alias: 'mono' }),
                local('Brand Sans', {
                    alias: 'brand',
                    src: 'resources/fonts/brand-sans',
                }),
            ],
        }),
    ],
});
```



`fontsource` 제공자는 설치된 Fontsource 패키지에서 글꼴을 읽습니다. 기본적으로 패키지 이름은 글꼴 패밀리에서 파생되며, 예를 들어 `@fontsource/jetbrains-mono`과 같습니다. 애플리케이션에서 다른 패키지 이름을 사용하는 경우, `package` 옵션을 사용하여 지정할 수 있습니다.

<a name="local-fonts"></a>
### 로컬 글꼴

로컬 글꼴을 사용할 때, `src` 옵션은 단일 글꼴 파일, 디렉토리 또는 글로브 패턴을 가리킬 수 있습니다. 플러그인은 지원되는 글꼴 파일을 발견하고 파일 이름에서 무게(weight)와 스타일을 추론합니다:

```js
local('Brand Sans', {
    alias: 'brand',
    src: 'resources/fonts/brand-sans/*.woff2',
})
```



사용 가능한 변형을 완전히 제어해야 하는 경우, `variants` 옵션을 사용하여 이를 명시적으로 정의할 수 있습니다:

```js
local('Brand Sans', {
    alias: 'brand',
    variants: [
        { src: 'resources/fonts/BrandSans-Regular.woff2', weight: 400 },
        { src: 'resources/fonts/BrandSans-Italic.woff2', weight: 400, style: 'italic' },
        { src: ['resources/fonts/BrandSans-Bold.woff2', 'resources/fonts/BrandSans-Bold.ttf'], weight: 700 },
    ],
})
```



<a name="font-options"></a>
### Font Options

Depending on the provider, font definitions may accept several options that allow you to customize the generated font CSS:

<div class="content-list" markdown="1">

- `alias` defines the name used by Blade's `@fonts` directive and defaults to a slug of the font family.
- `variable` defines the generated CSS variable and defaults to `--font-{alias}`.
- `weights` defines the remote or Fontsource font weights that should be resolved and defaults to `[400]`.
- `styles` defines the remote or Fontsource font styles that should be resolved and defaults to `['normal']`.
- `subsets` defines the remote or Fontsource font subsets that should be resolved and defaults to `['latin']`.
- `display` defines the `font-display` value and defaults to `swap`.
- `preload` controls which WOFF2 font variants should be preloaded. This option may be `true`, `false`, or an array of `{ weight, style }` selectors.
- `fallbacks` defines additional fallback fonts that should be appended to the generated font stack.
- `optimizedFallbacks` attempts to generate metric-adjusted fallback font faces using the optional `fontaine` package and defaults to `true`.

</div>

Optimized fallbacks require the `fontaine` package, which is not installed by default. If you want Laravel to generate metric-adjusted fallback font faces, you should install `fontaine` as a development dependency:

```shell
npm install --save-dev fontaine
```



If `fontaine` is not installed or cannot read a font file, Laravel will skip the optimized fallback for that font and continue using any fonts configured via the `fallbacks` option.

Local fonts are resolved from the `src` or `variants` options described above instead of using `weights`, `styles`, and `subsets`.

<a name="working-with-blade-and-routes"></a>
## Working With Blade and Routes

<a name="blade-processing-static-assets"></a>
### Processing Static Assets With Vite

When referencing assets in your JavaScript or CSS, Vite automatically processes and versions them. In addition, when building Blade-based applications, Vite can also process and version static assets that you reference solely in Blade templates.

However, to accomplish this, you need to make Vite aware of your assets by specifying them in the plugin's `assets` option. This option is intended for static files that you want to reference directly with `Vite::asset`. If you want Laravel to generate font CSS and preload links, use the [`fonts` option](#working-with-fonts) instead.

For example, if you want to process and version all images stored in `resources/images` and all fonts stored in `resources/fonts`, you should add the following to your Vite configuration:

```js
laravel({
    input: 'resources/js/app.js',
    assets: ['resources/images/**', 'resources/fonts/**'],
})
```



이 자산들은 이제 `npm run build`를 실행할 때 Vite에 의해 처리됩니다. 그런 다음 `Vite::asset` 메서드를 사용하여 Blade 템플릿에서 이러한 자산을 참조할 수 있으며, 이 메서드는 주어진 자산의 버전이 지정된 URL을 반환합니다:

```blade
<img src="{{ Vite::asset('resources/images/logo.png') }}">
```



> [!NOTE]
> Laravel Vite 플러그인의 버전 3 이전에는 애플리케이션의 진입점에서 `import.meta.glob`를 사용하여 정적 자산을 가져와야 했습니다. `assets` 옵션은 Vite 8의 변경 사항으로 도입되었습니다.

<a name="blade-refreshing-on-save"></a>
### 저장 시 새로고침

애플리케이션이 Blade를 사용한 전통적인 서버 사이드 렌더링으로 빌드될 때, Vite는 애플리케이션의 뷰 파일을 변경하면 브라우저를 자동으로 새로고침하여 개발 워크플로우를 개선할 수 있습니다. 시작하려면 `refresh` 옵션을 `true`로 지정하면 됩니다.

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: true,
        }),
    ],
});
```



`refresh` 옵션이 `true`일 때, 다음 디렉터리에 파일을 저장하면 `npm run dev`를 실행하는 동안 브라우저가 전체 페이지 새로 고침을 수행합니다:

- `app/Livewire/**`
- `app/View/Components/**`
- `lang/**`
- `resources/lang/**`
- `resources/views/**`
- `routes/**`

애플리케이션 프런트엔드에서 경로 링크를 생성하기 위해 [Ziggy](https://github.com/tighten/ziggy)를 사용하는 경우, `routes/**` 디렉터리를 감시하는 것이 유용합니다.

이 기본 경로가 필요에 맞지 않는다면, 감시할 경로 목록을 직접 지정할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: ['resources/views/**'],
        }),
    ],
});
```



내부적으로, Laravel Vite 플러그인은 [vite-plugin-full-reload](https://github.com/ElMassimo/vite-plugin-full-reload) 패키지를 사용하며, 이 패키지는 이 기능의 동작을 세밀하게 조정할 수 있는 몇 가지 고급 구성 옵션을 제공합니다. 이러한 수준의 맞춤 설정이 필요하다면, `config` 정의를 제공할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            refresh: [{
                paths: ['path/to/watch/**'],
                config: { delay: 300 }
            }],
        }),
    ],
});
```



<a name="blade-aliases"></a>
### 별칭

JavaScript 애플리케이션에서는 자주 참조되는 디렉토리에 [별칭을 만드는 것](#aliases)이 일반적입니다. 하지만, Blade에서 사용하기 위해 별칭을 만들 수도 있으며, 이는 `Illuminate\Support\Facades\Vite` 클래스의 `macro` 메서드를 사용하여 가능합니다. 일반적으로, "매크로"는 [서비스 제공자](/docs/{{version}}/providers)의 `boot` 메서드 내에서 정의되어야 합니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::macro('image', fn (string $asset) => $this->asset("resources/images/{$asset}"));
}
```



한 번 매크로가 정의되면, 템플릿 내에서 이를 호출할 수 있습니다. 예를 들어, 위에서 정의한 `image` 매크로를 사용하여 `resources/images/logo.png`에 위치한 자산을 참조할 수 있습니다:

```blade
<img src="{{ Vite::image('logo.png') }}" alt="Laravel Logo">
```



<a name="asset-prefetching"></a>
## 자산 사전 가져오기

Vite의 코드 분할 기능을 사용하여 SPA를 구축할 때, 필요한 자산은 각 페이지 탐색 시 가져옵니다. 이러한 동작은 UI 렌더링 지연으로 이어질 수 있습니다. 선택한 프런트엔드 프레임워크에서 이것이 문제라면, Laravel은 초기 페이지 로드 시 애플리케이션의 JavaScript 및 CSS 자산을 적극적으로 사전 가져올 수 있는 기능을 제공합니다.

Laravel에서 자산을 적극적으로 사전 가져오도록 지시하려면 [서비스 제공자](/docs/{{version}}/providers)의 `boot` 메서드 내에서 `Vite::prefetch` 메서드를 호출하면 됩니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Vite;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        // ...
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Vite::prefetch(concurrency: 3);
    }
}
```



위 예제에서, 자산은 각 페이지 로드 시 최대 `3`개의 동시 다운로드로 미리 가져옵니다. 애플리케이션의 필요에 맞게 동시성을 수정하거나, 애플리케이션이 모든 자산을 한 번에 다운로드해야 하는 경우 동시성 제한을 지정하지 않을 수 있습니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch();
}
```



기본적으로, 프리패칭은 [페이지 _로드_ 이벤트](https://developer.mozilla.org/en-US/docs/Web/API/Window/load_event)가 발생할 때 시작됩니다. 프리패칭 시작 시점을 사용자 정의하고 싶다면, Vite가 수신할 이벤트를 지정할 수 있습니다:

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Vite::prefetch(event: 'vite:prefetch');
}
```



위 코드를 기준으로, 이제 `window` 객체에서 `vite:prefetch` 이벤트를 수동으로 디스패치할 때 프리페칭이 시작됩니다. 예를 들어, 페이지가 로드된 후 3초 후에 프리페칭이 시작되도록 할 수 있습니다:

```html
<script>
    addEventListener('load', () => setTimeout(() => {
        dispatchEvent(new Event('vite:prefetch'))
    }, 3000))
</script>
```



<a name="custom-base-urls"></a>
## 사용자 정의 기본 URL

Vite로 컴파일된 자산이 CDN과 같이 애플리케이션과 별도의 도메인에 배포되는 경우, 애플리케이션의 `.env` 파일 내에서 `ASSET_URL` 환경 변수를 지정해야 합니다:

```env
ASSET_URL=https://cdn.example.com
```



자산 URL을 구성한 후, 자산에 대한 모든 재작성된 URL은 구성된 값이 접두사로 붙습니다:

```text
https://cdn.example.com/build/assets/app.9dce8d17.js
```



Vite는 [절대 URL을 다시 작성하지 않습니다](#url-processing), 따라서 접두사가 붙지 않는다는 점을 기억하세요.

<a name="environment-variables"></a>
## 환경 변수

애플리케이션의 `.env` 파일에서 `VITE_`를 접두사로 사용하여 환경 변수를 JavaScript에 주입할 수 있습니다:

```env
VITE_SENTRY_DSN_PUBLIC=http://example.com
```



주입된 환경 변수에는 `import.meta.env` 객체를 통해 접근할 수 있습니다:

```js
import.meta.env.VITE_SENTRY_DSN_PUBLIC
```



<a name="disabling-vite-in-tests"></a>
## 테스트에서 Vite 비활성화하기

Laravel의 Vite 통합은 테스트를 실행하는 동안 자산을 해결하려고 시도하며, 이는 Vite 개발 서버를 실행하거나 자산을 빌드해야 함을 요구합니다.

테스트 중에 Vite를 모킹(mocking)하고 싶다면, Laravel의 `TestCase` 클래스를 확장하는 모든 테스트에서 사용할 수 있는 `withoutVite` 메서드를 호출할 수 있습니다:```php tab=Pest
test('without vite example', function () {
    $this->withoutVite();

    // ...
});
```

```php tab=PHPUnit
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_without_vite_example(): void
    {
        $this->withoutVite();

        // ...
    }
}
```



모든 테스트에서 Vite를 비활성화하려면 기본 `TestCase` 클래스의 `setUp` 메서드에서 `withoutVite` 메서드를 호출할 수 있습니다:

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;

abstract class TestCase extends BaseTestCase
{
    protected function setUp(): void// [tl! add:start]
    {
        parent::setUp();

        $this->withoutVite();
    }// [tl! add:end]
}
```



<a name="ssr"></a>
## 서버 사이드 렌더링 (SSR)

Laravel Vite 플러그인은 Vite와 함께 서버 사이드 렌더링을 설정하는 것을 쉽게 만들어 줍니다. 시작하려면 `resources/js/ssr.js`에 SSR 진입점을 생성하고 Laravel 플러그인에 구성 옵션을 전달하여 진입점을 지정하세요:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            ssr: 'resources/js/ssr.js',
        }),
    ],
});
```



SSR 진입점을 다시 빌드하는 것을 잊지 않도록 하기 위해, 애플리케이션의 `package.json`에서 'build' 스크립트를 확장하여 SSR 빌드를 생성하는 것을 권장합니다:

```json
"scripts": {
     "dev": "vite",
     "build": "vite build" // [tl! remove]
     "build": "vite build && vite build --ssr" // [tl! add]
}
```



그런 다음 SSR 서버를 구축하고 시작하려면 다음 명령어를 실행할 수 있습니다:

```shell
npm run build
node bootstrap/ssr/ssr.js
```



[SSR with Inertia](https://inertiajs.com/server-side-rendering)를 사용하고 있다면, 대신 `inertia:start-ssr` Artisan 명령어를 사용하여 SSR 서버를 시작할 수 있습니다:

```shell
php artisan inertia:start-ssr
```



> [!NOTE]
> Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에는 이미 적절한 Laravel, Inertia SSR 및 Vite 구성이 포함되어 있습니다. 이러한 스타터 키트는 Laravel, Inertia SSR 및 Vite를 가장 빠르게 시작할 수 있는 방법을 제공합니다.

<a name="script-and-style-attributes"></a>
## 스크립트 및 스타일 태그 속성

<a name="content-security-policy-csp-nonce"></a>
### 콘텐츠 보안 정책(CSP) 논스

[콘텐츠 보안 정책](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)의 일부로 스크립트 및 스타일 태그에 [논스 속성](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce)을 포함하고자 하는 경우, 사용자 정의 [미들웨어](/docs/{{version}}/middleware) 내에서 `useCspNonce` 메서드를 사용하여 논스를 생성하거나 지정할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Vite;
use Symfony\Component\HttpFoundation\Response;

class AddContentSecurityPolicyHeaders
{
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        Vite::useCspNonce();

        return $next($request)->withHeaders([
            'Content-Security-Policy' => "script-src 'nonce-".Vite::cspNonce()."'",
        ]);
    }
}
```



`useCspNonce` 메서드를 호출한 후, Laravel은 모든 생성된 스크립트 및 스타일 태그에 `nonce` 속성을 자동으로 포함합니다.

다른 곳에서 nonce를 지정해야 하는 경우, Laravel의 [스타터 키트](/docs/{{version}}/starter-kits)에 포함된 [Ziggy `@route` 지시문](https://github.com/tighten/ziggy#using-routes-with-a-content-security-policy)을 포함하여, `cspNonce` 메서드를 사용하여 이를 가져올 수 있습니다:

```blade
@routes(nonce: Vite::cspNonce())
```



이미 Laravel에게 사용하도록 지시하고자 하는 nonce가 있는 경우, nonce를 `useCspNonce` 메서드에 전달할 수 있습니다:

```php
Vite::useCspNonce($nonce);
```



<a name="subresource-integrity-sri"></a>
### 서브리소스 무결성(SRI)

Vite 매니페스트에 자산에 대한 `integrity` 해시가 포함되어 있으면, Laravel은 [서브리소스 무결성](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)을 적용하기 위해 생성하는 모든 스크립트 및 스타일 태그에 `integrity` 속성을 자동으로 추가합니다. 기본적으로 Vite는 매니페스트에 `integrity` 해시를 포함하지 않지만, [vite-plugin-manifest-sri](https://www.npmjs.com/package/vite-plugin-manifest-sri) NPM 플러그인을 설치하여 활성화할 수 있습니다:

```shell
npm install --save-dev vite-plugin-manifest-sri
```



그런 다음 `vite.config.js` 파일에서 이 플러그인을 활성화할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import manifestSRI from 'vite-plugin-manifest-sri';// [tl! add]

export default defineConfig({
    plugins: [
        laravel({
            // ...
        }),
        manifestSRI(),// [tl! add]
    ],
});
```



필요한 경우 무결성 해시를 찾을 수 있는 매니페스트 키도 사용자 정의할 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useIntegrityKey('custom-integrity-key');
```



이 자동 감지를 완전히 비활성화하려면 `useIntegrityKey` 메서드에 `false`를 전달할 수 있습니다:

```php
Vite::useIntegrityKey(false);
```



<a name="arbitrary-attributes"></a>
### 임의 속성

스크립트와 스타일 태그에 [data-turbo-track](https://turbo.hotwired.dev/handbook/drive#reloading-when-assets-change) 속성과 같은 추가 속성을 포함해야 하는 경우, `useScriptTagAttributes` 및 `useStyleTagAttributes` 메서드를 통해 지정할 수 있습니다. 일반적으로 이 메서드는 [서비스 제공자](/docs/{{version}}/providers)에서 호출해야 합니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes([
    'data-turbo-track' => 'reload', // Specify a value for the attribute...
    'async' => true, // Specify an attribute without a value...
    'integrity' => false, // Exclude an attribute that would otherwise be included...
]);

Vite::useStyleTagAttributes([
    'data-turbo-track' => 'reload',
]);
```



속성을 조건부로 추가해야 하는 경우, 자산 소스 경로, 해당 URL, 매니페스트 청크 및 전체 매니페스트를 받을 콜백을 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Vite;

Vite::useScriptTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $src === 'resources/js/app.js' ? 'reload' : false,
]);

Vite::useStyleTagAttributes(fn (string $src, string $url, array|null $chunk, array|null $manifest) => [
    'data-turbo-track' => $chunk && $chunk['isEntry'] ? 'reload' : false,
]);
```



> [!WARNING]
> Vite 개발 서버가 실행되는 동안 `$chunk`와 `$manifest` 인수는 `null`가 됩니다.

<a name="advanced-customization"></a>
## 고급 커스터마이징

기본적으로 Laravel의 Vite 플러그인은 대부분의 애플리케이션에서 작동할 수 있는 합리적인 규칙을 사용합니다. 그러나 때때로 Vite의 동작을 커스터마이징해야 할 수도 있습니다. 추가 커스터마이징 옵션을 활성화하려면, 다음의 메서드와 옵션을 사용할 수 있으며, 이는 `@vite` Blade 지시문을 대신하여 사용할 수 있습니다.

```blade
<!doctype html>
<head>
    {{-- ... --}}

    {{
        Vite::useHotFile(storage_path('vite.hot')) // Customize the "hot" file...
            ->useBuildDirectory('bundle') // Customize the build directory...
            ->useManifestFilename('assets.json') // Customize the manifest filename...
            ->withEntryPoints(['resources/js/app.js']) // Specify the entry points...
            ->createAssetPathsUsing(function (string $path, ?bool $secure) { // Customize the backend path generation for built assets...
                return "https://cdn.example.com/{$path}";
            })
    }}
</head>
```



그런 다음 `vite.config.js` 파일 내에서 동일한 구성을 지정해야 합니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            hotFile: 'storage/vite.hot', // Customize the "hot" file...
            buildDirectory: 'bundle', // Customize the build directory...
            input: ['resources/js/app.js'], // Specify the entry points...
        }),
    ],
    build: {
      manifest: 'assets.json', // Customize the manifest filename...
    },
});
```



<a name="cors"></a>
### 개발 서버 교차 출처 리소스 공유(CORS)

Vite 개발 서버에서 자산을 가져오는 동안 브라우저에서 교차 출처 리소스 공유(CORS) 문제가 발생하는 경우, 개발 서버에 사용자 지정 출처 액세스를 허용해야 할 수 있습니다. Vite는 Laravel 플러그인과 결합하여 다음 출처를 추가 구성 없이 허용합니다:

- `::1`
- `127.0.0.1`
- `localhost`
- `*.test`
- `*.localhost`
- 프로젝트의 `.env` 내 `APP_URL`

프로젝트에 사용자 지정 출처를 허용하는 가장 쉬운 방법은 애플리케이션의 `APP_URL` 환경 변수가 브라우저에서 방문하는 출처와 일치하는지 확인하는 것입니다. 예를 들어, `https://my-app.laravel`를 방문하고 있다면 `.env`를 일치하도록 업데이트해야 합니다:

```env
APP_URL=https://my-app.laravel
```



만약 여러 출처를 지원하는 등 출처에 대해 더 세밀한 제어가 필요하다면, [Vite의 포괄적이고 유연한 내장 CORS 서버 구성](https://vite.dev/config/server-options.html#server-cors)을 활용해야 합니다. 예를 들어, 프로젝트의 `vite.config.js` 파일에 있는 `server.cors.origin` 구성 옵션에서 여러 출처를 지정할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [  // [tl! add]
                'https://backend.laravel',  // [tl! add]
                'http://admin.laravel:8566',  // [tl! add]
            ],  // [tl! add]
        },  // [tl! add]
    },  // [tl! add]
});
```



또한 정규식 패턴을 포함할 수 있으며, 이는 `*.laravel`와 같은 특정 최상위 도메인에 대해 모든 출처를 허용하고 싶은 경우에 유용할 수 있습니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: 'resources/js/app.js',
            refresh: true,
        }),
    ],
    server: {  // [tl! add]
        cors: {  // [tl! add]
            origin: [ // [tl! add]
                // Supports: SCHEME://DOMAIN.laravel[:PORT] [tl! add]
                /^https?:\/\/.*\.laravel(:\d+)?$/, //[tl! add]
            ], // [tl! add]
        }, // [tl! add]
    }, // [tl! add]
});
```



<a name="correcting-dev-server-urls"></a>
### 개발 서버 URL 수정

Vite 생태계 내 일부 플러그인은 슬래시로 시작하는 URL이 항상 Vite 개발 서버를 가리킨다고 가정합니다. 그러나 Laravel 통합의 특성상 이는 사실이 아닙니다.

예를 들어, `vite-imagetools` 플러그인은 Vite가 자산을 제공하는 동안 다음과 같은 URL을 출력합니다:

```html
<img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520">
```



`vite-imagetools` 플러그인은 출력 URL이 Vite에 의해 가로채질 것으로 예상하며, 그 후 플러그인은 `/@imagetools`로 시작하는 모든 URL을 처리할 수 있습니다. 이러한 동작을 기대하는 플러그인을 사용 중이라면, URL을 수동으로 수정해야 합니다. `vite.config.js` 파일에서 `transformOnServe` 옵션을 사용하여 이 작업을 수행할 수 있습니다.

이 특정 예제에서는, 생성된 코드 내 모든 `/@imagetools`의 발생 위치에 개발 서버 URL을 앞에 추가할 것입니다:

```js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import { imagetools } from 'vite-imagetools';

export default defineConfig({
    plugins: [
        laravel({
            // ...
            transformOnServe: (code, devServerUrl) => code.replaceAll('/@imagetools', devServerUrl+'/@imagetools'),
        }),
        imagetools(),
    ],
});
```



이제 Vite가 에셋을 제공하는 동안, Vite 개발 서버를 가리키는 URL을 출력할 것입니다:

```html
- <img src="/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! remove] -->
+ <img src="http://[::1]:5173/@imagetools/f0b2f404b13f052c604e632f2fb60381bf61a520"><!-- [tl! add] -->
```
{% endraw %}
