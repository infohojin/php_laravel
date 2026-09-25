---
layout: docs
title: "라라벨 믹스"
---

{% raw %}
# 라라벨 믹스

- [소개](#introduction)

<a name="introduction"></a>
## 소개

> [!WARNING]
> 라라벨 믹스는 더 이상 적극적으로 유지보수되지 않는 레거시 패키지입니다. 현대적인 대안으로 [Vite](/docs/{{version}}/vite)를 사용할 수 있습니다.

[라라벨 믹스](https://github.com/laravel-mix/laravel-mix)는 [Laracasts](https://laracasts.com) 창립자 제프리 웨이가 개발한 패키지로, 여러 일반적인 CSS 및 JavaScript 프리프로세서를 사용하여 Laravel 애플리케이션의 [webpack](https://webpack.js.org) 빌드 단계를 정의하는 유창한 API를 제공합니다.

다시 말해, 믹스를 사용하면 애플리케이션의 CSS 및 JavaScript 파일을 쉽게 컴파일하고 최소화할 수 있습니다. 간단한 메서드 체이닝을 통해 자산 파이프라인을 유창하게 정의할 수 있습니다. 예를 들어:

```js
mix.js('resources/js/app.js', 'public/js')
    .postCss('resources/css/app.css', 'public/css');

```

만약 여러분이 webpack과 자산 컴파일을 시작하는 것에 대해 혼란스럽고 압도된 적이 있다면, Laravel Mix를 좋아하게 될 것입니다. 그러나 애플리케이션을 개발하는 동안 반드시 사용해야 하는 것은 아니며, 원하는 어떤 자산 파이프라인 도구든 사용하거나 아예 사용하지 않아도 됩니다.

> [!NOTE]
> Vite는 새로운 Laravel 설치에서 Laravel Mix를 대체했습니다. Mix 문서는 [공식 Laravel Mix](https://laravel-mix.com/) 웹사이트를 참조하세요. Vite로 전환하고 싶다면, 우리의 [Vite 마이그레이션 가이드](https://github.com/laravel/vite-plugin/blob/main/UPGRADE.md#migrating-from-laravel-mix-to-vite)를 참고하세요.
{% endraw %}
