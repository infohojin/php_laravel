---
layout: docs
title: "프론트엔드"
---

{% raw %}
# 프론트엔드

- [소개](#introduction)
- [PHP 사용](#using-php)
    - [PHP 및 블레이드](#php-and-blade)
    - [라이브와이어](#livewire)
    - [스타터 키트](#php-starter-kits)
- [React, Svelte 또는 Vue 사용](#using-react-svelte-or-vue)
    - [관성](#inertia)
    - [스타터 키트](#inertia-starter-kits)
- [번들링 자산](#bundling-assets)

<a name="introduction"></a>
## 소개

Laravel은 [라우팅](/docs/{{version}}/routing), [검증](/docs/{{version}}/validation), [캐싱](/docs/{{version}}/cache), [큐](/docs/{{version}}/queues), [파일 저장소](/docs/{{version}}/filesystem) 등과 같은 최신 웹 애플리케이션을 구축하는 데 필요한 모든 기능을 제공하는 백엔드 프레임워크입니다. 그러나 우리는 애플리케이션의 프런트엔드 구축을 위한 강력한 접근 방식을 포함하여 개발자에게 아름다운 풀 스택 경험을 제공하는 것이 중요하다고 믿습니다.

Laravel을 사용하여 애플리케이션을 구축할 때 프런트엔드 개발을 처리하는 두 가지 주요 방법이 있으며, 어떤 접근 방식을 선택할지는 PHP를 활용하여 프런트엔드를 구축할지 아니면 React, Svelte, Vue와 같은 JavaScript 프레임워크를 사용하여 구축할지에 따라 결정됩니다. 귀하의 애플리케이션에 대한 프런트엔드 개발에 대한 최선의 접근 방식에 관해 정보에 입각한 결정을 내릴 수 있도록 아래에서 이러한 두 가지 옵션에 대해 논의하겠습니다.

<a name="using-php"></a>
## PHP 사용

<a name="php-and-blade"></a>
### PHP 및 블레이드

과거에는 대부분의 PHP 애플리케이션이 요청 중에 데이터베이스에서 검색된 데이터를 렌더링하는 PHP `echo` 문이 산재된 간단한 HTML 템플릿을 사용하여 브라우저에 HTML을 렌더링했습니다.

```blade
<div>
    <?php foreach ($users as $user): ?>
        Hello, <?php echo $user->name; ?> <br />
    <?php endforeach; ?>
</div>

```

Laravel에서는 HTML 렌더링에 대한 이러한 접근 방식을 [views](/docs/{{version}}/views) 및 [Blade](/docs/{{version}}/blade)를 사용하여 계속 구현할 수 있습니다. 블레이드는 데이터 표시, 데이터 반복 등을 위한 편리하고 짧은 구문을 제공하는 매우 가벼운 템플릿 언어입니다.

```blade
<div>
    @foreach ($users as $user)
        Hello, {{ $user->name }} <br />
    @endforeach
</div>

```

이러한 방식으로 애플리케이션을 구축할 때 양식 제출 및 기타 페이지 상호 작용은 일반적으로 서버에서 완전히 새로운 HTML 문서를 수신하고 전체 페이지는 브라우저에 의해 다시 렌더링됩니다. 오늘날에도 많은 애플리케이션은 간단한 블레이드 템플릿을 사용하여 이러한 방식으로 프런트엔드를 구성하는 데 완벽하게 적합할 수 있습니다.

<a name="growing-expectations"></a>
#### 점점 커지는 기대감

그러나 웹 애플리케이션에 대한 사용자 기대가 성숙해짐에 따라 많은 개발자는 더욱 세련되게 느껴지는 상호 작용을 통해 보다 동적인 프런트엔드를 구축해야 할 필요성을 발견했습니다. 이를 고려하여 일부 개발자는 React, Svelte 및 Vue와 같은 JavaScript 프레임워크를 사용하여 애플리케이션의 프런트엔드 구축을 시작하기로 선택합니다.

자신에게 편한 백엔드 언어를 고수하는 것을 선호하는 다른 사람들은 선택한 백엔드 언어를 주로 활용하면서 최신 웹 애플리케이션 UI를 구성할 수 있는 솔루션을 개발했습니다. 예를 들어, [Rails](https://rubyonrails.org/) 생태계에서는 이로 인해 [Turbo](https://turbo.hotwired.dev/) [Hotwire](https://hotwired.dev/) 및 [Stimulus](https://stimulus.hotwired.dev/)와 같은 라이브러리 생성이 촉진되었습니다.

Laravel 생태계 내에서 주로 PHP를 사용하여 현대적이고 동적인 프런트엔드를 생성해야 했기 때문에 [Laravel Livewire](https://livewire.laravel.com) 및 [Alpine.js](https://alpinejs.dev/)가 생성되었습니다.

<a name="livewire"></a>
### 라이브와이어

[Laravel Livewire](https://livewire.laravel.com)는 React, Svelte 및 Vue와 같은 최신 JavaScript 프레임워크로 구축된 프런트엔드처럼 역동적이고 현대적이며 살아있는 느낌을 주는 Laravel 기반 프런트엔드를 구축하기 위한 프레임워크입니다.

Livewire를 사용하면 UI의 개별 부분을 렌더링하고 애플리케이션의 프런트엔드에서 호출하고 상호 작용할 수 있는 메서드와 데이터를 노출하는 Livewire "구성 요소"를 생성하게 됩니다. 예를 들어 간단한 "카운터" 구성 요소는 다음과 같습니다.

```php
<?php

use Livewire\Component;

new class extends Component
{
    public $count = 0;

    public function increment()
    {
        $this->count++;
    }
};
?>

<div>
    <button wire:click="increment">+</button>
    <h1>{{ $count }}</h1>
</div>

```

보시다시피 Livewire를 사용하면 Laravel 애플리케이션의 프런트엔드와 백엔드를 연결하는 `wire:click`와 같은 새로운 HTML 속성을 작성할 수 있습니다. 또한 간단한 블레이드 표현식을 사용하여 구성 요소의 현재 상태를 렌더링할 수 있습니다.

많은 사람들에게 Livewire는 Laravel을 통해 프런트엔드 개발에 혁명을 일으켰으며, 현대적이고 동적인 웹 애플리케이션을 구축하는 동시에 Laravel의 편안함을 유지할 수 있도록 했습니다. 일반적으로 Livewire를 사용하는 개발자는 [Alpine.js](https://alpinejs.dev/)를 활용하여 대화 상자 창을 렌더링하는 등 필요한 경우에만 프런트엔드에 JavaScript를 "뿌립니다".

Laravel을 처음 사용하시는 경우 [views](/docs/{{version}}/views) 및 [Blade](/docs/{{version}}/blade)의 기본 사용법을 익히는 것이 좋습니다. 그런 다음 공식 [Laravel Livewire 문서](https://livewire.laravel.com/docs)를 참조하여 대화형 Livewire 구성 요소를 사용하여 애플리케이션을 한 단계 더 발전시키는 방법을 알아보세요.

<a name="php-starter-kits"></a>
### 스타터 키트

PHP 및 Livewire를 사용하여 프런트엔드를 구축하려는 경우 [Livewire 스타터 키트](/docs/{{version}}/starter-kits)를 활용하여 애플리케이션 개발을 시작할 수 있습니다.

<a name="using-react-svelte-or-vue"></a>
## Using React, Svelte, or Vue

Although it's possible to build modern frontends using Laravel and Livewire, many developers still prefer to leverage the power of a JavaScript framework like React, Svelte, or Vue. This allows developers to take advantage of the rich ecosystem of JavaScript packages and tools available via NPM.

However, without additional tooling, pairing Laravel with React, Svelte, or Vue would leave us needing to solve a variety of complicated problems such as client-side routing, data hydration, and authentication. Client-side routing is often simplified by using opinionated React / Svelte / Vue frameworks such as [Next](https://nextjs.org/) and [Nuxt](https://nuxt.com/); however, data hydration and authentication remain complicated and cumbersome problems to solve when pairing a backend framework like Laravel with these frontend frameworks.

In addition, developers are left maintaining two separate code repositories, often needing to coordinate maintenance, releases, and deployments across both repositories. While these problems are not insurmountable, we don't believe it's a productive or enjoyable way to develop applications.

<a name="inertia"></a>
### Inertia

Thankfully, Laravel offers the best of both worlds. [Inertia](https://inertiajs.com) bridges the gap between your Laravel application and your modern React, Svelte, or Vue frontend, allowing you to build full-fledged, modern frontends using React, Svelte, or Vue while leveraging Laravel routes and controllers for routing, data hydration, and authentication — all within a single code repository. With this approach, you can enjoy the full power of both Laravel and React / Svelte / Vue without crippling the capabilities of either tool.

After installing Inertia into your Laravel application, you will write routes and controllers like normal. However, instead of returning a Blade template from your controller, you will return an Inertia page:

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Inertia\Inertia;
use Inertia\Response;

class UserController extends Controller
{
    /**
     * Show the profile for a given user.
     */
    public function show(string $id): Response
    {
        return Inertia::render('users/show', [
            'user' => User::findOrFail($id)
        ]);
    }
}

```

An Inertia page corresponds to a React, Svelte, or Vue component, typically stored within the `resources/js/pages` directory of your application. The data given to the page via the `Inertia::render` method will be used to hydrate the "props" of the page component:

```jsx
import Layout from '@/layouts/authenticated';
import { Head } from '@inertiajs/react';

export default function Show({ user }) {
    return (
        <Layout>
            <Head title="Welcome" />
            <h1>Welcome</h1>
            <p>Hello {user.name}, welcome to Inertia.</p>
        </Layout>
    )
}

```

As you can see, Inertia allows you to leverage the full power of React, Svelte, or Vue when building your frontend, while providing a light-weight bridge between your Laravel powered backend and your JavaScript powered frontend.

#### Server-Side Rendering

If you're concerned about diving into Inertia because your application requires server-side rendering, don't worry. Inertia offers [server-side rendering support](https://inertiajs.com/server-side-rendering). And, when deploying your application via [Laravel Cloud](https://cloud.laravel.com) or [Laravel Forge](https://forge.laravel.com), it's a breeze to ensure that Inertia's server-side rendering process is always running.

<a name="inertia-starter-kits"></a>
### Starter Kits

If you would like to build your frontend using Inertia and React / Svelte / Vue, you can leverage our [React, Svelte, or Vue application starter kits](/docs/{{version}}/starter-kits) to jump-start your application's development. All of these starter kits scaffold your application's backend and frontend authentication flow using Inertia, React / Svelte / Vue, [Tailwind](https://tailwindcss.com), and [Vite](https://vitejs.dev) so that you can start building your next big idea.

<a name="bundling-assets"></a>
## Bundling Assets

Regardless of whether you choose to develop your frontend using Blade and Livewire or React / Svelte / Vue and Inertia, you will likely need to bundle your application's CSS into production-ready assets. Of course, if you choose to build your application's frontend with React, Svelte, or Vue, you will also need to bundle your components into browser ready JavaScript assets.

By default, Laravel utilizes [Vite](https://vitejs.dev) to bundle your assets. Vite provides lightning-fast build times and near instantaneous Hot Module Replacement (HMR) during local development. In all new Laravel applications, including those using our [starter kits](/docs/{{version}}/starter-kits), you will find a `vite.config.js` file that loads our light-weight Laravel Vite plugin that makes Vite a joy to use with Laravel applications.

The fastest way to get started with Laravel and Vite is by beginning your application's development using [our application starter kits](/docs/{{version}}/starter-kits), which jump-starts your application by providing frontend and backend authentication scaffolding.

> [!NOTE]
> For more detailed documentation on utilizing Vite with Laravel, please see our [dedicated documentation on bundling and compiling your assets](/docs/{{version}}/vite).
{% endraw %}
