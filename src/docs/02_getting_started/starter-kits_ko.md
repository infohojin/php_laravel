---
layout: docs
title: "스타터 키트"
---

{% raw %}
# 스타터 키트

- [소개](#introduction)
- [스타터 키트를 사용한 애플리케이션 생성](#creating-an-application)
- [사용 가능한 스타터 키트](#available-starter-kits)
- [React](#react)
- Svelte (#svelte)
- [뷰](#vue)
- Livewire (#livewire)
- 스타터 키트 커스터마이징 (#starter-kit-customization)
- [React](#react-customization)
- Svelte (#svelte-customization)
- 뷰 (#vue-customization)
- Livewire (#livewire-customization)
- [인증](#authentication)
- [기능 활성화 및 비활성화](#enabling-and-disabling-features)
- [사용자 생성 및 비밀번호 재설정 사용자 지정](#customizing-actions)
- 2 단계 인증 (#two-factor-authentication)
- [속도 제한](#rate-limiting)
- [Teams](#teams)
- [WorkOS AuthKit 인증](#workos)
- [WorkOS 스타터 키트 구성](#configuring-your-workos-starter-kit)
- [Inertia SSR](#inertia-ssr)
- 커뮤니티 유지 관리 스타터 키트 (#community-maintained-starter-kits)
- [자주 묻는 질문](#faqs)

<a name="introduction"></a>
## 소개

새로운 Laravel 애플리케이션 구축을 시작하는 데 도움이 되도록 [애플리케이션 스타터 키트](https://laravel.com/starter-kits) 를 제공하게 되어 기쁩니다. 이러한 스타터 키트는 다음 Laravel 애플리케이션을 구축하는 데 도움이 되며， 애플리케이션 사용자를 등록하고 인증하는 데 필요한 경로， 컨트롤러 및 뷰가 포함되어 있습니다. 스타터 키트는 [Laravel Fortify](/docs/{{version}}/fortify) 를 사용하여 인증을 제공합니다。

이러한 스타터 키트를 사용하는 것은 환영하지만， 반드시 필요한 것은 아닙니다. Laravel 의 새 사본을 설치하기만 하면 처음부터 자신만의 애플리케이션을 자유롭게 구축할 수 있습니다. 어느 쪽이든 당신이 멋진 무언가를 구축할 것임을 알고 있습니다！

<a name="creating-an-application"></a>
## 스타터 키트를 사용하여 애플리케이션 생성

시작 키트 중 하나를 사용하여 새 Laravel 애플리케이션을 생성하려면 먼저 [PHP 및 Laravel CLI 도구 설치](/docs/{{version}}/installation#installing-php) 를 수행해야 합니다. PHP 및 Composer 가 이미 설치되어 있다면 Composer 를 통해 Laravel 설치 관리자 CLI 도구를 설치할 수 있습니다：

```shell
composer global require laravel/installer
```



그런 다음, Laravel 설치 프로그램 CLI를 사용하여 새로운 Laravel 애플리케이션을 생성합니다. Laravel 설치 프로그램이 선호하는 스타터 키트를 선택하도록 안내할 것입니다:

```shell
laravel new my-app
```



Laravel 애플리케이션을 만든 후에는 NPM을 통해 프론트엔드 종속성을 설치하고 Laravel 개발 서버를 시작하기만 하면 됩니다:

```shell
cd my-app
npm install && npm run build
composer run dev
```

Laravel 개발 서버를 시작하면 웹 브라우저의 [http://localhost:8000](http://localhost:8000) 에서 애플리케이션에 액세스할 수 있습니다。

<a name="available-starter-kits"></a>
## 사용 가능한 스타터 키트

<a name="react"></a>
### 반응

React 스타터 키트는 [Inertia](https://inertiajs.com) 를 사용하여 React 프론트엔드로 Laravel 애플리케이션을 구축할 수 있는 강력하고 현대적인 출발점을 제공합니다。

Inertia 를 사용하면 클래식한 서버 측 라우팅 및 컨트롤러를 사용하여 현대적인 단일 페이지 React 애플리케이션을 구축할 수 있습니다. 이를 통해 Laravel 의 놀라운 백엔드 생산성과 번개처럼 빠른 Vite 컴파일링과 결합된 React 의 프런트엔드 성능을 즐길 수 있습니다。

React 스타터 키트는 React 19, TypeScript, Tailwind 및 [shadcn/ui](https://ui.shadcn.com) 구성 요소 라이브러리를 사용합니다。

<a name="svelte"></a>
### 스벨트

Svelte 스타터 키트는 [Inertia](https://inertiajs.com) 를 사용하여 Svelte 프론트엔드로 Laravel 애플리케이션을 구축할 수 있는 강력하고 현대적인 출발점을 제공합니다。

Inertia 를 사용하면 클래식한 서버 측 라우팅 및 컨트롤러를 사용하여 현대적인 단일 페이지 Svelte 애플리케이션을 구축할 수 있습니다. 이를 통해 Laravel 의 놀라운 백엔드 생산성과 번개처럼 빠른 Vite 컴파일링과 결합된 Svelte 의 프론트엔드 성능을 즐길 수 있습니다。

Svelte 스타터 키트는 Svelte 5, TypeScript, Tailwind 및 [shadcn-svelte](https://www.shadcn-svelte.com/) 컴포넌트 라이브러리를 사용합니다。

<a name="vue"></a>
### 뷰

우리의 Vue 스타터 키트는 [Inertia](https://inertiajs.com) 를 사용하여 Vue 프론트엔드로 Laravel 애플리케이션을 구축하기 위한 훌륭한 출발점을 제공합니다。

Inertia 를 사용하면 클래식한 서버 측 라우팅 및 컨트롤러를 사용하여 현대적인 단일 페이지 Vue 애플리케이션을 구축할 수 있습니다. 이를 통해 Vue 의 프론트엔드 성능과 Laravel 의 놀라운 백엔드 생산성， 그리고 번개처럼 빠른 Vite 컴파일링을 결합하여 즐길 수 있습니다。

Vue 스타터 키트는 Vue Composition API, TypeScript, Tailwind 및 [shadcn-vue](https://www.shadcn-vue.com/) 구성 요소 라이브러리를 활용합니다。

<a name="livewire"></a>
### 라이브와이어

Livewire 스타터 키트는 [Laravel Livewire](https://livewire.laravel.com) 프론트엔드를 사용하여 Laravel 애플리케이션을 구축하기 위한 완벽한 출발점을 제공합니다。

Livewire 는 PHP 만을 사용하여 동적이고 반응적인 프런트엔드 UI 를 구축하는 강력한 방법입니다. 이는 주로 Blade 템플릿을 사용하고 React, Svelte, Vue 와 같은 JavaScript 기반 SPA 프레임워크에 대한 더 간단한 대안을 찾고 있는 팀에 매우 적합합니다。



Livewire 스타터 키트는 Livewire, Tailwind, 그리고 [Flux UI](https://fluxui.dev) 컴포넌트 라이브러리를 활용합니다.

<a name="starter-kit-customization"></a>
## 스타터 키트 커스터마이제이션

<a name="react-customization"></a>
### 리액트

우리의 React 스타터 키트는 Inertia 3, React 19, Tailwind 4, 그리고 [shadcn/ui](https://ui.shadcn.com)로 구축되었습니다. 모든 스타터 키트와 마찬가지로, 모든 백엔드 및 프론트엔드 코드는 애플리케이션 내에 존재하여 완전한 커스터마이징이 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉토리에 위치합니다. 애플리케이션의 외관과 동작을 커스터마이징하기 위해 코드를 자유롭게 수정할 수 있습니다.

```text
resources/js/
├── components/    # Reusable React components
├── hooks/         # React hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```



추가 shadcn 구성 요소를 게시하려면 먼저 [게시하려는 구성 요소를 찾으세요](https://ui.shadcn.com). 그런 다음 `npx`를 사용하여 구성 요소를 게시하세요:

```shell
npx shadcn@latest add switch
```



이 예제에서는 명령어가 Switch 컴포넌트를 `resources/js/components/ui/switch.tsx`에 게시합니다. 컴포넌트가 게시되면, 이를 모든 페이지에서 사용할 수 있습니다:

```jsx
import { Switch } from "@/components/ui/switch"

const MyPage = () => {
  return (
    <div>
      <Switch />
    </div>
  );
};

export default MyPage;
```



<a name="react-available-layouts"></a>
#### 사용 가능한 레이아웃

React 시작 키트에는 선택할 수 있는 두 가지 주요 레이아웃이 포함되어 있습니다: "사이드바" 레이아웃과 "헤더" 레이아웃입니다. 사이드바 레이아웃이 기본이지만, 애플리케이션의 `resources/js/layouts/app-layout.tsx` 파일 상단에서 가져오는 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayoutTemplate from '@/layouts/app/app-sidebar-layout'; // [tl! remove]
import AppLayoutTemplate from '@/layouts/app/app-header-layout'; // [tl! add]
```



<a name="react-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 세 가지 다른 변형이 포함됩니다: 기본 사이드바 변형, "삽입" 변형, 그리고 "플로팅" 변형. `resources/js/components/app-sidebar.tsx` 컴포넌트를 수정하여 원하는 변형을 선택할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```



<a name="react-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

React 스타터 키트에 포함된 로그인 페이지와 회원가입 페이지와 같은 인증 페이지는 "simple", "card", "split"의 세 가지 다른 레이아웃 변형도 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션의 `resources/js/layouts/auth-layout.tsx` 파일 상단에서 가져오는 레이아웃을 수정하면 됩니다:

```js
import AuthLayoutTemplate from '@/layouts/auth/auth-simple-layout'; // [tl! remove]
import AuthLayoutTemplate from '@/layouts/auth/auth-split-layout'; // [tl! add]
```



<a name="svelte-customization"></a>
### 스벨트

우리의 스벨트 스타터 키트는 Inertia 3, Svelte 5, Tailwind, 및 [shadcn-svelte](https://www.shadcn-svelte.com/)로 구성되어 있습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 애플리케이션 내에 존재하여 완전한 커스터마이징이 가능합니다.

대부분의 프론트엔드 코드는 `resources/js` 디렉토리에 위치해 있습니다. 애플리케이션의 외관과 동작을 원하는 대로 커스터마이징하기 위해 코드 수정을 자유롭게 할 수 있습니다:

```text
resources/js/
├── components/    # Reusable Svelte components
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration and Svelte rune modules
├── pages/         # Page components
└── types/         # TypeScript definitions
```



추가 shadcn-svelte 컴포넌트를 게시하려면 먼저 [게시할 컴포넌트를 찾으세요](https://www.shadcn-svelte.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시하세요:

```shell
npx shadcn-svelte@latest add switch
```



이 예제에서는 명령어가 Switch 컴포넌트를 `resources/js/components/ui/switch/switch.svelte`에 게시합니다. 컴포넌트가 게시되면, 이를 모든 페이지에서 사용할 수 있습니다:

```svelte
<script lang="ts">
    import { Switch } from '@/components/ui/switch'
</script>

<div>
    <Switch />
</div>
```



<a name="svelte-available-layouts"></a>
#### 사용 가능한 레이아웃

Svelte 시작 키트에는 선택할 수 있는 두 가지 주요 레이아웃이 포함되어 있습니다: '사이드바' 레이아웃과 '헤더' 레이아웃입니다. 사이드바 레이아웃이 기본값이지만, 애플리케이션의 `resources/js/layouts/AppLayout.svelte` 파일 상단에 가져오는 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.svelte'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.svelte'; // [tl! add]
```



<a name="svelte-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 세 가지 다른 변형이 포함됩니다: 기본 사이드바 변형, "삽입" 변형, 그리고 "플로팅" 변형. `resources/js/components/AppSidebar.svelte` 컴포넌트를 수정하여 원하는 변형을 선택할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```



<a name="svelte-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Svelte 스타터 키트에 포함된 로그인 페이지 및 회원가입 페이지와 같은 인증 페이지는 "간단", "카드", "분할"의 세 가지 다른 레이아웃 변형도 제공합니다.

인증 레이아웃을 변경하려면, 애플리케이션의 `resources/js/layouts/AuthLayout.svelte` 파일 상단에서 가져오는 레이아웃을 수정하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.svelte'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.svelte'; // [tl! add]
```



<a name="vue-customization"></a>
### Vue

우리의 Vue 스타터 키트는 Inertia 3, Vue 3 Composition API, Tailwind, 그리고 [shadcn-vue](https://www.shadcn-vue.com/)로 구축되었습니다. 모든 스타터 키트와 마찬가지로, 백엔드 및 프론트엔드 코드가 모두 애플리케이션 내에 존재하여 완전한 커스터마이징이 가능합니다.

프론트엔드 코드의 대부분은 `resources/js` 디렉토리에 위치해 있습니다. 애플리케이션의 외관과 동작을 커스터마이즈하기 위해 코드를 자유롭게 수정할 수 있습니다:

```text
resources/js/
├── components/    # Reusable Vue components
├── composables/   # Vue composables / hooks
├── layouts/       # Application layouts
├── lib/           # Utility functions and configuration
├── pages/         # Page components
└── types/         # TypeScript definitions
```



추가 shadcn-vue 컴포넌트를 게시하려면 먼저 [게시할 컴포넌트를 찾으세요](https://www.shadcn-vue.com). 그런 다음 `npx`를 사용하여 컴포넌트를 게시하세요:

```shell
npx shadcn-vue@latest add switch
```



이 예제에서는 명령어가 Switch 컴포넌트를 `resources/js/components/ui/Switch.vue`에 게시합니다. 컴포넌트가 게시되면, 이를 모든 페이지에서 사용할 수 있습니다:

```vue
<script setup lang="ts">
import { Switch } from '@/components/ui/switch'
</script>

<template>
    <div>
        <Switch />
    </div>
</template>
```



<a name="vue-available-layouts"></a>
#### 사용 가능한 레이아웃

Vue 시작 키트에는 선택할 수 있는 두 가지 주요 레이아웃이 포함되어 있습니다: "사이드바" 레이아웃과 "헤더" 레이아웃입니다. 사이드바 레이아웃이 기본이지만, 애플리케이션의 `resources/js/layouts/AppLayout.vue` 파일 상단에서 가져오는 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다:

```js
import AppLayout from '@/layouts/app/AppSidebarLayout.vue'; // [tl! remove]
import AppLayout from '@/layouts/app/AppHeaderLayout.vue'; // [tl! add]
```



<a name="vue-sidebar-variants"></a>
#### 사이드바 변형

사이드바 레이아웃에는 세 가지 다른 변형이 포함되어 있습니다: 기본 사이드바 변형, "인세트" 변형, 그리고 "플로팅" 변형. `resources/js/components/AppSidebar.vue` 컴포넌트를 수정하여 원하는 변형을 선택할 수 있습니다:

```text
<Sidebar collapsible="icon" variant="sidebar"> [tl! remove]
<Sidebar collapsible="icon" variant="inset"> [tl! add]
```



<a name="vue-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

Vue 스타터 키트에 포함된 로그인 페이지와 회원가입 페이지와 같은 인증 페이지는 "simple", "card", "split"의 세 가지 다른 레이아웃 변형도 제공합니다.

인증 레이아웃을 변경하려면 애플리케이션 `resources/js/layouts/AuthLayout.vue` 파일 상단에서 불러오는 레이아웃을 수정하세요:

```js
import AuthLayout from '@/layouts/auth/AuthSimpleLayout.vue'; // [tl! remove]
import AuthLayout from '@/layouts/auth/AuthSplitLayout.vue'; // [tl! add]
```



<a name="livewire-customization"></a>
### 라이브와이어

우리의 라이브와이어 스타터 키트는 Livewire 4, Tailwind, 및 [Flux UI](https://fluxui.dev/)로 제작되었습니다. 모든 스타터 키트와 마찬가지로, 백엔드와 프론트엔드 코드가 모두 애플리케이션 내에 존재하여 완전한 커스터마이징이 가능합니다.

프론트엔드 코드의 대부분은 `resources/views` 디렉토리에 위치해 있습니다. 애플리케이션의 외형과 동작을 커스터마이징하기 위해 코드를 자유롭게 수정할 수 있습니다:

```text
resources/views
├── components            # Reusable components
├── flux                  # Customized Flux components
├── layouts               # Application layouts
├── pages                 # Livewire pages
├── partials              # Reusable Blade partials
├── dashboard.blade.php   # Authenticated user dashboard
├── welcome.blade.php     # Guest user welcome page
```



<a name="livewire-available-layouts"></a>
#### 사용 가능한 레이아웃

Livewire 시작 키트에는 선택할 수 있는 두 가지 기본 레이아웃이 포함되어 있습니다: "사이드바" 레이아웃과 "헤더" 레이아웃입니다. 사이드바 레이아웃이 기본값이지만, 애플리케이션의 `resources/views/layouts/app.blade.php` 파일에서 사용되는 레이아웃을 수정하여 헤더 레이아웃으로 전환할 수 있습니다. 또한, `container` 속성을 메인 Flux 컴포넌트에 추가해야 합니다:

```blade
<x-layouts::app.header>
    <flux:main container>
        {{ $slot }}
    </flux:main>
</x-layouts::app.header>
```



<a name="livewire-authentication-page-layout-variants"></a>
#### 인증 페이지 레이아웃 변형

라이브와이어 스타터 키트에 포함된 인증 페이지, 예를 들어 로그인 페이지와 회원가입 페이지는 세 가지 다른 레이아웃 변형도 제공합니다: "simple", "card", 그리고 "split".

인증 레이아웃을 변경하려면 애플리케이션의 `resources/views/layouts/auth.blade.php` 파일에서 사용되는 레이아웃을 수정하세요:

```blade
<x-layouts::auth.split>
    {{ $slot }}
</x-layouts::auth.split>
```



<a name="authentication"></a>
## Authentication

All starter kits use [Laravel Fortify](/docs/{{version}}/fortify) to handle authentication. Fortify provides routes, controllers, and logic for login, registration, password reset, email verification, and more.

Fortify automatically registers the following authentication routes based on the features that are enabled in your application's `config/fortify.php` configuration file:

<div class="overflow-auto">

| Route                              | Method | Description                         |
| ---------------------------------- | ------ | ----------------------------------- |
| `/login`                           | `GET`    | Display login form                  |
| `/login`                           | `POST`   | Authenticate user                   |
| `/logout`                          | `POST`   | Log user out                        |
| `/register`                        | `GET`    | Display registration form           |
| `/register`                        | `POST`   | Create new user                     |
| `/forgot-password`                 | `GET`    | Display password reset request form |
| `/forgot-password`                 | `POST`   | Send password reset link            |
| `/reset-password/{token}`          | `GET`    | Display password reset form         |
| `/reset-password`                  | `POST`   | Update password                     |
| `/email/verify`                    | `GET`    | Display email verification notice   |
| `/email/verify/{id}/{hash}`        | `GET`    | Verify email address                |
| `/email/verification-notification` | `POST`   | Resend verification email           |
| `/user/confirm-password`           | `GET`    | Display password confirmation form  |
| `/user/confirm-password`           | `POST`   | Confirm password                    |
| `/two-factor-challenge`            | `GET`    | Display 2FA challenge form          |
| `/two-factor-challenge`            | `POST`   | Verify 2FA code                     |

</div>

The `php artisan route:list` Artisan command can be used to display all of the routes in your application.

<a name="enabling-and-disabling-features"></a>
### Enabling and Disabling Features

You can control which Fortify features are enabled in your application's `config/fortify.php` configuration file:

```php
use Laravel\Fortify\Features;

'features' => [
    Features::registration(),
    Features::resetPasswords(),
    Features::emailVerification(),
    Features::twoFactorAuthentication([
        'confirm' => true,
        'confirmPassword' => true,
    ]),
],
```



To disable a feature, comment out or remove that feature entry from the `features` array. For example, remove `Features::registration()` to disable public registration.

When using the [React](#react), [Svelte](#svelte) or [Vue](#vue) starter kits, you will also need to remove any references to the disabled feature's routes in your frontend code. For example, if you disable email verification, you should remove the imports and references to the `verification` routes in your React, Svelte, or Vue components. This is necessary because these starter kits use Wayfinder for type-safe routing, which generates route definitions at build time. If you reference routes that no longer exist, your application will fail to build.

<a name="customizing-actions"></a>
### Customizing User Creation and Password Reset

When a user registers or resets their password, Fortify invokes action classes located in your application's `app/Actions/Fortify` directory:

<div class="overflow-auto">

| File                          | Description                           |
| ----------------------------- | ------------------------------------- |
| `CreateNewUser.php`           | Validates and creates new users       |
| `ResetUserPassword.php`       | Validates and updates user passwords  |
| `PasswordValidationRules.php` | Defines password validation rules     |

</div>

For example, to customize your application's registration logic, you should edit the `CreateNewUser` action:

```php
public function create(array $input): User
{
    Validator::make($input, [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'max:255', 'unique:users'],
        'phone' => ['required', 'string', 'max:20'], // [tl! add]
        'password' => $this->passwordRules(),
    ])->validate();

    return User::create([
        'name' => $input['name'],
        'email' => $input['email'],
        'phone' => $input['phone'], // [tl! add]
        'password' => Hash::make($input['password']),
    ]);
}
```



<a name="two-factor-authentication"></a>
### 이중 인증

스타터 키트에는 내장된 이중 인증(2FA)이 포함되어 있어 사용자가 TOTP 호환 인증 앱을 사용하여 계정을 보호할 수 있습니다. 2FA는 기본적으로 애플리케이션의 `config/fortify.php` 구성 파일에서 `Features::twoFactorAuthentication()`를 통해 활성화됩니다.

`confirm` 옵션은 2FA가 완전히 활성화되기 전에 사용자가 코드를 확인하도록 요구하며, `confirmPassword`는 2FA를 활성화하거나 비활성화하기 전에 비밀번호 확인을 요구합니다. 자세한 내용은 [포티파이의 이중 인증 문서](/docs/{{version}}/fortify#two-factor-authentication)를 참조하세요.

<a name="rate-limiting"></a>
### 속도 제한

속도 제한은 브루트포스 공격과 반복 로그인 시도가 인증 엔드포인트를 과부하시키는 것을 방지합니다. 애플리케이션의 `FortifyServiceProvider`에서 포티파이의 속도 제한 동작을 사용자 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Cache\RateLimiting\Limit;

RateLimiter::for('login', function ($request) {
    return Limit::perMinute(5)->by($request->email.$request->ip());
});
```

<a name="teams"></a>
## Teams

The React, Svelte, Vue, and Livewire starter kits may also be generated with team support. When the teams feature is enabled, each user belongs to one or more teams and has a current team. During registration, new users are automatically given a personal team. The starter kits also include team management screens for creating teams, switching between teams, inviting members, and updating team details.

When a route is scoped to the current team, the current team's slug is included in the URL. For example, the dashboard route becomes `/{current_team}/dashboard`, while team management pages use routes such as `settings/teams/{team}`. When using the `{current_team}` and `{team}` route parameters, the starter kits automatically ensure that the authenticated user belongs to the requested team before allowing access to the route.

To make generating team-aware URLs more convenient, the starter kits register URL defaults for the authenticated user's current team. This allows calls to helpers such as `route('dashboard')` to automatically include the current team's slug. When a user signs in, registers, or switches teams, the starter kits update the current team and refresh these URL defaults so generated links continue to use the correct team context.

When creating or renaming a team, the starter kits also prevent users from choosing reserved names that could produce unsafe or conflicting route segments. For example, names that would collide with route prefixes such as `settings`, `login`, or `dashboard` may not be used.

<a name="workos"></a>
## WorkOS AuthKit Authentication

By default, the React, Svelte, Vue, and Livewire starter kits all utilize Laravel's built-in authentication system to offer login, registration, password reset, email verification, and more. In addition, we also offer a [WorkOS AuthKit](https://authkit.com) powered variant of each starter kit that offers:

<div class="content-list" markdown="1">

- Social authentication (Google, Microsoft, GitHub, and Apple)
- Passkey authentication
- Email based "Magic Auth"
- SSO

</div>

Using WorkOS as your authentication provider [requires a WorkOS account](https://workos.com). WorkOS offers free authentication for applications up to 1 million monthly active users.

To use WorkOS AuthKit as your application's authentication provider, select the WorkOS option when creating your new starter kit powered application via `laravel new`.



<a name="configuring-your-workos-starter-kit"></a>
### WorkOS 스타터 키트 구성하기

WorkOS 기반 스타터 키트를 사용하여 새 애플리케이션을 만든 후, 애플리케이션의 `.env` 파일에서 `WORKOS_CLIENT_ID`, `WORKOS_API_KEY`, `WORKOS_REDIRECT_URL` 환경 변수를 설정해야 합니다. 이 변수들은 애플리케이션에 대해 WorkOS 대시보드에서 제공된 값과 일치해야 합니다:

```ini
WORKOS_CLIENT_ID=your-client-id
WORKOS_API_KEY=your-api-key
WORKOS_REDIRECT_URL="${APP_URL}/authenticate"
```



Additionally, you should configure the application homepage URL in your WorkOS dashboard. This URL is where users will be redirected after they log out of your application.

<a name="configuring-authkit-authentication-methods"></a>
#### Configuring AuthKit Authentication Methods

When using a WorkOS powered starter kit, we recommend that you disable "Email + Password" authentication within your application's WorkOS AuthKit configuration settings, allowing users to only authenticate via social authentication providers, passkeys, "Magic Auth", and SSO. This allows your application to totally avoid handling user passwords.

<a name="configuring-authkit-session-timeouts"></a>
#### Configuring AuthKit Session Timeouts

In addition, we recommend that you configure your WorkOS AuthKit session inactivity timeout to match your Laravel application's configured session timeout threshold, which is typically two hours.

<a name="inertia-ssr"></a>
### Inertia SSR

The React, Svelte, and Vue starter kits are compatible with Inertia's [server-side rendering](https://inertiajs.com/server-side-rendering) capabilities. To build an Inertia SSR compatible bundle for your application, run the `build:ssr` command:

```shell
npm run build:ssr
```



편의를 위해 `composer dev:ssr` 명령도 사용할 수 있습니다. 이 명령은 애플리케이션에 대한 SSR 호환 번들을 빌드한 후 Laravel 개발 서버와 Inertia SSR 서버를 시작하여 Inertia의 서버 사이드 렌더링 엔진을 사용해 애플리케이션을 로컬에서 테스트할 수 있게 합니다:

```shell
composer dev:ssr
```



<a name="community-maintained-starter-kits"></a>
### 커뮤니티 유지 관리 스타터 키트

Laravel 설치 프로그램을 사용하여 새로운 Laravel 애플리케이션을 생성할 때, Packagist에서 제공되는 커뮤니티 유지 관리 스타터 키트를 `--using` 플래그에 제공할 수 있습니다:

```shell
laravel new my-app --using=example/starter-kit
```



<a name="creating-starter-kits"></a>
#### 스타터 키트 만들기

스타터 키트를 다른 사람들이 사용할 수 있도록 하려면 [Packagist](https://packagist.org)에 게시해야 합니다. 스타터 키트는 필요한 환경 변수를 `.env.example` 파일에 정의해야 하며, 필요한 설치 후 명령은 스타터 키트의 `composer.json` 파일의 `post-create-project-cmd` 배열에 나열되어야 합니다.

<a name="faqs"></a>
### 자주 묻는 질문

<a name="faq-upgrade"></a>
#### 어떻게 업그레이드합니까?

모든 스타터 키트는 다음 애플리케이션을 위한 견고한 출발점을 제공합니다. 코드의 전체 소유권을 가지고 있으므로, 원하는 대로 애플리케이션을 조정하고, 커스터마이즈하고, 빌드할 수 있습니다. 하지만 스타터 키트 자체를 업데이트할 필요는 없습니다.

<a name="faq-enable-email-verification"></a>
#### 이메일 인증을 어떻게 활성화합니까?

이메일 인증은 `App/Models/User.php` 모델에서 `MustVerifyEmail` import의 주석을 제거하고 모델이 `MustVerifyEmail` 인터페이스를 구현하도록 하여 추가할 수 있습니다:

```php
<?php

namespace App\Models;

use Illuminate\Contracts\Auth\MustVerifyEmail;
// ...

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```



등록 후 사용자는 인증 이메일을 받게 됩니다. 사용자의 이메일 주소가 인증될 때까지 특정 경로에 대한 접근을 제한하려면 해당 경로에 `verified` 미들웨어를 추가하세요:

```php
Route::middleware(['auth', 'verified'])->group(function () {
    Route::get('dashboard', function () {
        return Inertia::render('dashboard');
    })->name('dashboard');
});
```



> [!NOTE]
> [WorkOS](#workos) 버전의 스타터 키트를 사용할 때 이메일 인증은 필요하지 않습니다.

<a name="faq-modify-email-template"></a>
#### 기본 이메일 템플릿을 어떻게 수정하나요?

기본 이메일 템플릿을 귀하의 애플리케이션 브랜딩에 더 잘 맞게 맞춤화하고 싶을 수 있습니다. 이 템플릿을 수정하려면 다음 명령어를 사용하여 이메일 뷰를 애플리케이션에 게시해야 합니다:

```shell
php artisan vendor:publish --tag=laravel-mail
```

이것은 `resources/views/vendor/mail`에 여러 파일을 생성합니다. 기본 이메일 템플릿의 모양과 외관을 변경하려면 이러한 파일과 `resources/views/vendor/mail/themes/default.css` 파일을 모두 수정할 수 있습니다.
{% endraw %}
