---
layout: docs
title: "Blade Templates"
---

{% raw %}
# Blade Templates

- [Introduction](#introduction)
    - [Supercharging Blade With Livewire](#supercharging-blade-with-livewire)
- [Displaying Data](#displaying-data)
    - [HTML Entity Encoding](#html-entity-encoding)
    - [Blade and JavaScript Frameworks](#blade-and-javascript-frameworks)
- [Blade Directives](#blade-directives)
    - [If Statements](#if-statements)
    - [Switch Statements](#switch-statements)
    - [Loops](#loops)
    - [The Loop Variable](#the-loop-variable)
    - [Conditional Classes](#conditional-classes)
    - [Additional Attributes](#additional-attributes)
    - [Including Subviews](#including-subviews)
    - [The `@once` Directive](#the-once-directive)
    - [Raw PHP](#raw-php)
    - [Fonts](#fonts)
    - [Comments](#comments)
- [Components](#components)
    - [Rendering Components](#rendering-components)
    - [Index Components](#index-components)
    - [Passing Data to Components](#passing-data-to-components)
    - [Component Attributes](#component-attributes)
    - [Reserved Keywords](#reserved-keywords)
    - [Slots](#slots)
    - [Inline Component Views](#inline-component-views)
    - [Dynamic Components](#dynamic-components)
    - [Manually Registering Components](#manually-registering-components)
- [Anonymous Components](#anonymous-components)
    - [Anonymous Index Components](#anonymous-index-components)
    - [Data Properties / Attributes](#data-properties-attributes)
    - [Accessing Parent Data](#accessing-parent-data)
    - [Anonymous Component Paths](#anonymous-component-paths)
- [Building Layouts](#building-layouts)
    - [Layouts Using Components](#layouts-using-components)
    - [Layouts Using Template Inheritance](#layouts-using-template-inheritance)
- [Forms](#forms)
    - [CSRF Field](#csrf-field)
    - [Method Field](#method-field)
    - [Validation Errors](#validation-errors)
- [Stacks](#stacks)
- [Service Injection](#service-injection)
- [Rendering Inline Blade Templates](#rendering-inline-blade-templates)
- [Rendering Blade Fragments](#rendering-blade-fragments)
- [Extending Blade](#extending-blade)
    - [Custom Echo Handlers](#custom-echo-handlers)
    - [Custom If Statements](#custom-if-statements)

<a name="introduction"></a>
## Introduction



Blade는 Laravel에 포함된 단순하지만 강력한 템플릿 엔진입니다. 일부 PHP 템플릿 엔진과 달리 Blade는 템플릿에서 일반 PHP 코드를 사용하는 것을 제한하지 않습니다. 사실, 모든 Blade 템플릿은 평범한 PHP 코드로 컴파일되어 수정될 때까지 캐시되므로 Blade는 본질적으로 애플리케이션에 거의 부담을 주지 않습니다. Blade 템플릿 파일은 `.blade.php` 파일 확장자를 사용하며 일반적으로 `resources/views` 디렉토리에 저장됩니다.

Blade 뷰는 글로벌 `view` 헬퍼를 사용하여 라우트나 컨트롤러에서 반환될 수 있습니다. 물론, [views](/docs/{{version}}/views) 문서에서 언급한 바와 같이, 데이터는 `view` 헬퍼의 두 번째 인수를 사용하여 Blade 뷰에 전달될 수 있습니다.

```php
Route::get('/', function () {
    return view('greeting', ['name' => 'Finn']);
});
```



<a name="supercharging-blade-with-livewire"></a>
### 라이브와이어로 블레이드 슈퍼차징하기

블레이드 템플릿을 한 단계 업그레이드하고 동적인 인터페이스를 쉽게 구축하고 싶으신가요? [Laravel Livewire](https://livewire.laravel.com)를 확인해보세요. Livewire를 사용하면 보통 React, Svelte 또는 Vue와 같은 프런트엔드 프레임워크를 통해서만 가능했던 동적 기능이 추가된 블레이드 컴포넌트를 작성할 수 있어, 많은 JavaScript 프레임워크의 복잡함, 클라이언트 사이드 렌더링, 빌드 단계 없이 현대적이고 반응적인 프런트엔드를 구축하는 훌륭한 방법을 제공합니다.

<a name="displaying-data"></a>
## 데이터 표시하기

블레이드 뷰에 전달된 데이터를 중괄호로 감싸서 표시할 수 있습니다. 예를 들어, 다음과 같은 라우트를 가진 경우:

```php
Route::get('/', function () {
    return view('welcome', ['name' => 'Samantha']);
});
```



다음과 같이 `name` 변수의 내용을 표시할 수 있습니다:

```blade
Hello, {{ $name }}.
```



> [!NOTE]
> Blade의 `{{ }}` echo 문은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수로 전송됩니다.

뷰에 전달된 변수의 내용만 표시하는 것으로 제한되지 않습니다. PHP 함수의 결과도 echo할 수 있습니다. 사실, Blade echo 문 안에 원하는 모든 PHP 코드를 넣을 수 있습니다:

```blade
The current UNIX timestamp is {{ time() }}.
```



<a name="html-entity-encoding"></a>
### HTML 엔티티 인코딩

기본적으로, Blade(및 Laravel의 `e` 함수)는 HTML 엔티티를 두 번 인코딩합니다. 만약 두 번 인코딩을 비활성화하고 싶다면, `AppServiceProvider`의 `boot` 메서드에서 `Blade::withoutDoubleEncoding` 메서드를 호출하세요:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Blade::withoutDoubleEncoding();
    }
}
```



<a name="displaying-unescaped-data"></a>
#### 이스케이프되지 않은 데이터 표시

기본적으로, Blade `{{ }}` 문장은 XSS 공격을 방지하기 위해 자동으로 PHP의 `htmlspecialchars` 함수로 처리됩니다. 데이터를 이스케이프하지 않으려면 다음 구문을 사용할 수 있습니다:

```blade
Hello, {!! $name !!}.
```



> [!WARNING]
> 애플리케이션 사용자가 제공한 콘텐츠를 출력할 때는 매우 주의해야 합니다. 사용자 제공 데이터를 표시할 때 XSS 공격을 방지하려면 일반적으로 이스케이프된 중괄호(double curly brace) 구문을 사용해야 합니다.

<a name="blade-and-javascript-frameworks"></a>
### Blade와 JavaScript 프레임워크

많은 JavaScript 프레임워크도 브라우저에 특정 표현식을 표시해야 함을 나타내기 위해 "중괄호"를 사용하므로, 표현식을 변경하지 않고 그대로 두어야 함을 Blade 렌더링 엔진에 알리려면 `@` 기호를 사용할 수 있습니다. 예를 들어:

```blade
<h1>Laravel</h1>

Hello, @{{ name }}.
```



이 예에서, `@` 기호는 Blade에 의해 제거되지만, `{{ name }}` 표현식은 Blade 엔진에 의해 건드려지지 않아서 JavaScript 프레임워크에 의해 렌더링될 수 있습니다.

`@` 기호는 Blade 지시어를 이스케이프하는 데에도 사용할 수 있습니다:

```blade
{{-- Blade template --}}
@@if()

<!-- HTML output -->
@if()
```



<a name="rendering-json"></a>
#### JSON 렌더링

때때로 JavaScript 변수를 초기화하기 위해 배열을 JSON으로 렌더링하려는 의도로 배열을 뷰에 전달할 수 있습니다. 예를 들어:

```blade
<script>
    var app = <?php echo json_encode($array); ?>;
</script>
```



하지만 `json_encode`를 수동으로 호출하는 대신, `Illuminate\Support\Js::from` 메서드를 사용할 수 있습니다. `from` 메서드는 PHP의 `json_encode` 함수와 동일한 인수를 받아들이며, 결과 JSON이 HTML 인용 부호 안에 포함될 수 있도록 올바르게 이스케이프되었는지 확인합니다. `from` 메서드는 주어진 객체나 배열을 유효한 JavaScript 객체로 변환할 JavaScript 문 `JSON.parse` 문자열을 반환합니다:

```blade
<script>
    var app = {{ Illuminate\Support\Js::from($array) }};
</script>
```



Laravel 애플리케이션 스켈레톤의 최신 버전에는 Blade 템플릿 내에서 이 기능에 편리하게 접근할 수 있는 `Js` 퍼사드가 포함되어 있습니다:

```blade
<script>
    var app = {{ Js::from($array) }};
</script>
```



> [!WARNING]
> 기존 변수를 JSON으로 렌더링할 때는 `Js::from` 방법만 사용해야 합니다. Blade 템플릿은 정규 표현식을 기반으로 하며, 복잡한 표현을 지시문에 전달하려고 하면 예상치 못한 실패가 발생할 수 있습니다.

<a name="the-at-verbatim-directive"></a>
#### `@verbatim` 지시문

템플릿의 많은 부분에서 JavaScript 변수를 표시하는 경우, HTML을 `@verbatim` 지시문으로 감싸 각 Blade 에코 문 앞에 `@` 기호를 붙이지 않아도 됩니다:

```blade
@verbatim
    <div class="container">
        Hello, {{ name }}.
    </div>
@endverbatim
```



<a name="blade-directives"></a>
## 블레이드 지시문

템플릿 상속과 데이터 표시 외에도, Blade는 조건문과 반복문과 같은 일반적인 PHP 제어 구조를 위한 편리한 바로가기를 제공합니다. 이러한 바로가기는 PHP 제어 구조와 유사하면서도 매우 깔끔하고 간결하게 작업할 수 있는 방법을 제공합니다.

<a name="if-statements"></a>
### if 문

`if` 문은 `@if`, `@elseif`, `@else`, 그리고 `@endif` 지시문을 사용하여 구성할 수 있습니다. 이러한 지시문은 PHP 대응문과 동일하게 작동합니다:

```blade
@if (count($records) === 1)
    I have one record!
@elseif (count($records) > 1)
    I have multiple records!
@else
    I don't have any records!
@endif
```



편의를 위해, Blade는 또한 `@unless` 지시어를 제공합니다:

```blade
@unless (Auth::check())
    You are not signed in.
@endunless
```



이미 논의된 조건부 지시문 외에도, `@isset` 및 `@empty` 지시문은 각각의 PHP 함수에 대한 편리한 단축키로 사용할 수 있습니다:

```blade
@isset($records)
    // $records is defined and is not null...
@endisset

@empty($records)
    // $records is "empty"...
@endempty
```



<a name="authentication-directives"></a>
#### 인증 지침

`@auth` 및 `@guest` 지침은 현재 사용자가 [인증됨](/docs/{{version}}/authentication) 상태인지 아니면 게스트인지 빠르게 확인하는 데 사용할 수 있습니다:

```blade
@auth
    // The user is authenticated...
@endauth

@guest
    // The user is not authenticated...
@endguest
```



필요한 경우, `@auth` 및 `@guest` 지시어를 사용할 때 확인해야 하는 인증 가드를 지정할 수 있습니다:

```blade
@auth('admin')
    // The user is authenticated...
@endauth

@guest('admin')
    // The user is not authenticated...
@endguest
```



<a name="environment-directives"></a>
#### 환경 지시문

`@production` 지시문을 사용하여 애플리케이션이 운영 환경에서 실행 중인지 확인할 수 있습니다:

```blade
@production
    // Production specific content...
@endproduction
```



또는 `@env` 지시문을 사용하여 애플리케이션이 특정 환경에서 실행 중인지 여부를 확인할 수 있습니다:

```blade
@env('staging')
    // The application is running in "staging"...
@endenv

@env(['staging', 'production'])
    // The application is running in "staging" or "production"...
@endenv
```



<a name="section-directives"></a>
#### 섹션 지시문

`@hasSection` 지시문을 사용하여 템플릿 상속 섹션에 내용이 있는지 확인할 수 있습니다:

```blade
@hasSection('navigation')
    <div class="pull-right">
        @yield('navigation')
    </div>

    <div class="clearfix"></div>
@endif
```



섹션에 내용이 없는지 확인하려면 `sectionMissing` 지시문을 사용할 수 있습니다:

```blade
@sectionMissing('navigation')
    <div class="pull-right">
        @include('default-navigation')
    </div>
@endif
```



<a name="session-directives"></a>
#### 세션 지시문

`@session` 지시문은 [세션](/docs/{{version}}/session) 값이 존재하는지 확인하는 데 사용될 수 있습니다. 세션 값이 존재하면 `@session`와 `@endsession` 지시문 내의 템플릿 내용이 평가됩니다. `@session` 지시문 내용 내에서 `$value` 변수를 출력하여 세션 값을 표시할 수 있습니다:

```blade
@session('status')
    <div class="p-4 bg-green-100">
        {{ $value }}
    </div>
@endsession
```



<a name="context-directives"></a>
#### 컨텍스트 지시어

`@context` 지시어는 [컨텍스트](/docs/{{version}}/context) 값이 존재하는지 확인하는 데 사용될 수 있습니다. 컨텍스트 값이 존재하면, `@context` 및 `@endcontext` 지시어 내의 템플릿 내용이 평가됩니다. `@context` 지시어의 내용 내에서, `$value` 변수를 출력하여 컨텍스트 값을 표시할 수 있습니다:

```blade
@context('canonical')
    <link href="{{ $value }}" rel="canonical">
@endcontext
```



<a name="switch-statements"></a>
### 스위치 문

스위치 문은 `@switch`, `@case`, `@break`, `@default` 및 `@endswitch` 지시어를 사용하여 구성할 수 있습니다:

```blade
@switch($i)
    @case(1)
        First case...
        @break

    @case(2)
        Second case...
        @break

    @default
        Default case...
@endswitch
```



<a name="loops"></a>
### 반복문

조건문 외에도, Blade는 PHP의 반복 구조를 다루기 위한 간단한 지시어를 제공합니다. 다시 말해, 이 지시어 각각은 PHP의 대응하는 기능과 동일하게 작동합니다:

```blade
@for ($i = 0; $i < 10; $i++)
    The current value is {{ $i }}
@endfor

@foreach ($users as $user)
    <p>This is user {{ $user->id }}</p>
@endforeach

@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>No users</p>
@endforelse

@while (true)
    <p>I'm looping forever.</p>
@endwhile
```



> [!NOTE]
> `foreach` 루프를 반복하는 동안, [루프 변수](#the-loop-variable)를 사용하여 루프에 대한 유용한 정보를 얻을 수 있습니다. 예를 들어, 루프의 첫 번째 반복인지 마지막 반복인지 확인할 수 있습니다.

루프를 사용할 때 `@continue` 및 `@break` 지시어를 사용하여 현재 반복을 건너뛰거나 루프를 종료할 수도 있습니다:

```blade
@foreach ($users as $user)
    @if ($user->type == 1)
        @continue
    @endif

    <li>{{ $user->name }}</li>

    @if ($user->number == 5)
        @break
    @endif
@endforeach
```



지시문 선언 내에 계속 조건이나 종료 조건을 포함할 수도 있습니다:

```blade
@foreach ($users as $user)
    @continue($user->type == 1)

    <li>{{ $user->name }}</li>

    @break($user->number == 5)
@endforeach
```



<a name="the-loop-variable"></a>
### 루프 변수

`foreach` 루프를 반복하는 동안, `$loop` 변수가 루프 내부에서 사용 가능합니다. 이 변수는 현재 루프 인덱스와 루프를 통과하는 첫 번째 또는 마지막 반복인지 여부와 같은 유용한 정보를 제공합니다:

```blade
@foreach ($users as $user)
    @if ($loop->first)
        This is the first iteration.
    @endif

    @if ($loop->last)
        This is the last iteration.
    @endif

    <p>This is user {{ $user->id }}</p>
@endforeach
```



중첩 루프에 있는 경우, `parent` 속성을 통해 상위 루프의 `$loop` 변수에 접근할 수 있습니다:

```blade
@foreach ($users as $user)
    @foreach ($user->posts as $post)
        @if ($loop->parent->first)
            This is the first iteration of the parent loop.
        @endif
    @endforeach
@endforeach
```



The `$loop` variable also contains a variety of other useful properties:

<div class="overflow-auto">

| Property           | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `$loop->index`     | The index of the current loop iteration (starts at 0). |
| `$loop->iteration` | The current loop iteration (starts at 1).              |
| `$loop->remaining` | The iterations remaining in the loop.                  |
| `$loop->count`     | The total number of items in the array being iterated. |
| `$loop->first`     | Whether this is the first iteration through the loop.  |
| `$loop->last`      | Whether this is the last iteration through the loop.   |
| `$loop->even`      | Whether this is an even iteration through the loop.    |
| `$loop->odd`       | Whether this is an odd iteration through the loop.     |
| `$loop->depth`     | The nesting level of the current loop.                 |
| `$loop->parent`    | When in a nested loop, the parent's loop variable.     |

</div>

<a name="conditional-classes"></a>
### Conditional Classes & Styles

The `@class` directive conditionally compiles a CSS class string. The directive accepts an array of classes where the array key contains the class or classes you wish to add, while the value is a boolean expression. If the array element has a numeric key, it will always be included in the rendered class list:

```blade
@php
    $isActive = false;
    $hasError = true;
@endphp

<span @class([
    'p-4',
    'font-bold' => $isActive,
    'text-gray-500' => ! $isActive,
    'bg-red' => $hasError,
])></span>

<span class="p-4 text-gray-500 bg-red"></span>
```



마찬가지로, `@style` 지시문은 HTML 요소에 조건부로 인라인 CSS 스타일을 추가하는 데 사용될 수 있습니다:

```blade
@php
    $isActive = true;
@endphp

<span @style([
    'background-color: red',
    'font-weight: bold' => $isActive,
])></span>

<span style="background-color: red; font-weight: bold;"></span>
```



<a name="additional-attributes"></a>
### 추가 속성

편의를 위해, 주어진 HTML 체크박스 입력이 "선택됨"인지 쉽게 표시하기 위해 `@checked` 지시문을 사용할 수 있습니다. 이 지시문은 제공된 조건이 `true`로 평가되면 `checked`를 출력합니다:

```blade
<input
    type="checkbox"
    name="active"
    value="active"
    @checked(old('active', $user->active))
/>
```



마찬가지로, `@selected` 지시문은 주어진 선택 옵션이 '선택됨'인지 여부를 나타내는 데 사용할 수 있습니다.

```blade
<select name="version">
    @foreach ($product->versions as $version)
        <option value="{{ $version }}" @selected(old('version') == $version)>
            {{ $version }}
        </option>
    @endforeach
</select>
```



또한, `@disabled` 지시어는 특정 요소가 '비활성화'되어야 하는지를 나타내는 데 사용될 수 있습니다:

```blade
<button type="submit" @disabled($errors->isNotEmpty())>Submit</button>
```



게다가, `@readonly` 지시어는 특정 요소가 '읽기 전용'인지 여부를 나타내는 데 사용될 수 있습니다.

```blade
<input
    type="email"
    name="email"
    value="email@laravel.com"
    @readonly($user->isNotAdmin())
/>
```



또한, `@required` 지시어는 특정 요소가 '필수'인지 여부를 나타내는 데 사용될 수 있습니다.

```blade
<input
    type="text"
    name="title"
    value="title"
    @required($user->isAdmin())
/>
```



<a name="including-subviews"></a>
### 서브뷰 포함하기

> [!NOTE]
> `@include` 지시문을 자유롭게 사용할 수 있지만, Blade [컴포넌트](#components)는 유사한 기능을 제공하며, 데이터 및 속성 바인딩과 같은 `@include` 지시문보다 여러 가지 이점을 제공합니다.

Blade의 `@include` 지시문을 사용하면 다른 뷰 내에서 Blade 뷰를 포함할 수 있습니다. 부모 뷰에서 사용 가능한 모든 변수는 포함된 뷰에서도 사용 가능하게 됩니다:

```blade
<div>
    @include('shared.errors')

    <form>
        <!-- Form Contents -->
    </form>
</div>
```



포함된 뷰가 부모 뷰에서 사용 가능한 모든 데이터를 상속받더라도, 포함된 뷰에서 사용할 수 있도록 추가 데이터를 배열로 전달할 수도 있습니다:

```blade
@include('view.name', ['status' => 'complete'])
```



존재하지 않는 뷰를 `@include`하려고 하면, Laravel은 오류를 발생시킵니다. 존재할 수도 있고 존재하지 않을 수도 있는 뷰를 포함하려면, `@includeIf` 지시어를 사용해야 합니다:

```blade
@includeIf('view.name', ['status' => 'complete'])
```



주어진 불 표현식이 `true` 또는 `false`로 평가되는지 여부를 확인하고 싶다면 `@includeWhen` 및 `@includeUnless` 지시문을 사용할 수 있습니다:

```blade
@includeWhen($boolean, 'view.name', ['status' => 'complete'])

@includeUnless($boolean, 'view.name', ['status' => 'complete'])
```



주어진 뷰 배열에서 존재하는 첫 번째 뷰를 포함하려면 `includeFirst` 지시어를 사용할 수 있습니다:

```blade
@includeFirst(['custom.admin', 'admin'], ['status' => 'complete'])
```



부모 뷰로부터 어떤 변수도 상속하지 않고 뷰를 포함하고 싶다면, `@includeIsolated` 지시어를 사용할 수 있습니다. 포함된 뷰는 명시적으로 전달한 변수만 접근할 수 있습니다:

```blade
@includeIsolated('view.name', ['user' => $user])
```



> [!WARNING]
> Blade 뷰에서 `__DIR__`와 `__FILE__` 상수를 사용하는 것은 피해야 합니다. 이 상수들은 캐시된, 컴파일된 뷰의 위치를 참조하기 때문입니다.

<a name="rendering-views-for-collections"></a>
#### 컬렉션에 대한 뷰 렌더링

Blade의 `@each` 지시어를 사용하면 루프와 인클루드를 한 줄로 결합할 수 있습니다:

```blade
@each('view.name', $jobs, 'job')
```



`@each` 지시문의 첫 번째 인수는 배열이나 컬렉션의 각 요소에 대해 렌더링할 뷰입니다. 두 번째 인수는 반복하려는 배열이나 컬렉션이며, 세 번째 인수는 뷰 내에서 현재 반복에 할당될 변수 이름입니다. 예를 들어 `jobs` 배열을 반복하는 경우, 일반적으로 뷰 내에서 각 작업에 `job` 변수를 통해 접근하고자 합니다. 현재 반복의 배열 키는 뷰 내에서 `key` 변수로 사용할 수 있습니다.

`@each` 지시문에 네 번째 인수를 전달할 수도 있습니다. 이 인수는 주어진 배열이 비어 있을 경우 렌더링될 뷰를 결정합니다.

```blade
@each('view.name', $jobs, 'job', 'view.empty')
```



> [!WARNING]
> `@each`을 통해 렌더링된 뷰는 부모 뷰의 변수를 상속하지 않습니다. 자식 뷰에서 이러한 변수가 필요하다면 대신 `@foreach`와 `@include` 지시문을 사용해야 합니다.

<a name="the-once-directive"></a>
### `@once` 지시문

`@once` 지시문을 사용하면 템플릿의 일부를 렌더링 사이클당 한 번만 평가되도록 정의할 수 있습니다. 이는 [스택](#stacks)을 사용하여 특정 자바스크립트 코드를 페이지의 헤더로 밀어 넣는 데 유용할 수 있습니다. 예를 들어, 루프 내에서 특정 [컴포넌트](#components)를 렌더링할 때 컴포넌트가 처음 렌더링되는 시점에만 자바스크립트를 헤더로 밀어 넣고 싶을 수 있습니다:

```blade
@once
    @push('scripts')
        <script>
            // Your custom JavaScript...
        </script>
    @endpush
@endonce
```



`@once` 지시어는 종종 `@push` 또는 `@prepend` 지시어와 함께 사용되기 때문에, 귀하의 편의를 위해 `@pushOnce` 및 `@prependOnce` 지시어가 제공됩니다:

```blade
@pushOnce('scripts')
    <script>
        // Your custom JavaScript...
    </script>
@endPushOnce
```



두 개의 별도 Blade 템플릿에서 중복 콘텐츠를 푸시하고 있다면, 콘텐츠가 한 번만 렌더링되도록 `@pushOnce` 지시문에 두 번째 인수로 고유 식별자를 제공해야 합니다:

```blade
<!-- pie-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce

<!-- line-chart.blade.php -->
@pushOnce('scripts', 'chart.js')
    <script src="/chart.js"></script>
@endPushOnce
```



<a name="raw-php"></a>
### 원시 PHP

어떤 상황에서는 PHP 코드를 뷰에 포함하는 것이 유용할 수 있습니다. 템플릿 내에서 일반 PHP 블록을 실행하려면 Blade `@php` 지시어를 사용할 수 있습니다:

```blade
@php
    $counter = 1;
@endphp
```



또는 PHP를 사용하여 클래스를 가져오기만 하면 되는 경우, `@use` 지시어를 사용할 수 있습니다:

```blade
@use('App\Models\Flight')
```



`@use` 지시어에 가져온 클래스를 별칭으로 지정하기 위해 두 번째 인수를 제공할 수 있습니다:

```blade
@use('App\Models\Flight', 'FlightModel')
```



만약 동일한 네임스페이스 안에 여러 클래스가 있다면, 그 클래스들의 임포트를 그룹화할 수 있습니다:

```blade
@use('App\Models\{Flight, Airport}')
```



`@use` 지시문은 또한 `function` 또는 `const` 수정자를 사용하여 가져오기 경로에 접두사를 붙임으로써 PHP 함수와 상수를 가져오는 것을 지원합니다:

```blade
@use(function App\Helpers\format_currency)
@use(const App\Constants\MAX_ATTEMPTS)
```



클래스 임포트와 마찬가지로, 함수와 상수에도 별칭이 지원됩니다:

```blade
@use(function App\Helpers\format_currency, 'formatMoney')
@use(const App\Constants\MAX_ATTEMPTS, 'MAX_TRIES')
```



그룹화된 임포트는 함수와 상수 수정자 모두에서 지원되며, 단일 지시문으로 동일한 네임스페이스에서 여러 심볼을 임포트할 수 있습니다:

```blade
@use(function App\Helpers\{format_currency, format_date})
@use(const App\Constants\{MAX_ATTEMPTS, DEFAULT_TIMEOUT})
```



<a name="fonts"></a>
### 글꼴

[Laravel의 Vite 글꼴 최적화](/docs/{{version}}/vite#working-with-fonts)를 사용할 때, `@fonts` 지시어를 사용하여 애플리케이션 레이아웃에서 구성된 글꼴 사전 로드 링크와 인라인 글꼴 CSS를 렌더링할 수 있습니다:

```blade
<!doctype html>
<head>
    {{-- ... --}}

    @fonts
    @vite('resources/js/app.js')
</head>
```



`@fonts` 지시문은 `vite.config.js` 파일에 구성된 모든 글꼴 패밀리를 렌더링합니다. 이 지시문은 일반적으로 해당 글꼴을 사용하는 콘텐츠보다 먼저 애플리케이션 루트 레이아웃의 `<head>`에 배치해야 합니다.

페이지에서 구성된 글꼴 중 일부만 필요하다면, 하나 이상의 글꼴 별칭을 지시문에 전달할 수 있습니다:

```blade
{{-- Load a single font alias... --}}
@fonts('sans')

{{-- Load multiple font aliases... --}}
@fonts(['sans', 'mono'])
```



폰트 별칭은 Vite 구성에서 폰트를 정의할 때 `alias` 옵션을 사용하여 구성됩니다. `@fonts` 지시문은 `Vite` 파사드가 제공하는 `fonts` 메서드를 호출하며, 이 메서드는 직접 호출될 수도 있습니다:

```blade
{{ Vite::fonts(['sans', 'mono']) }}
```



<a name="comments"></a>
### 주석

Blade는 뷰에서 주석을 정의할 수 있도록 해줍니다. 그러나 HTML 주석과 달리, Blade 주석은 애플리케이션에서 반환되는 HTML에 포함되지 않습니다:

```blade
{{-- This comment will not be present in the rendered HTML --}}
```



<a name="components"></a>
## 구성 요소

구성 요소와 슬롯은 섹션, 레이아웃 및 포함과 유사한 이점을 제공합니다. 그러나 일부는 구성 요소와 슬롯의 개념이 이해하기 더 쉬울 수 있습니다. 구성 요소를 작성하는 데에는 클래스 기반 구성 요소와 익명 구성 요소의 두 가지 접근 방식이 있습니다.

클래스 기반 구성 요소를 만들기 위해서는 `make:component` Artisan 명령어를 사용할 수 있습니다. 구성 요소 사용 방법을 설명하기 위해, 간단한 `Alert` 구성 요소를 만들어 보겠습니다. `make:component` 명령어는 구성 요소를 `app/View/Components` 디렉토리에 배치합니다:

```shell
php artisan make:component Alert
```



`make:component` 명령은 구성 요소를 위한 뷰 템플릿도 생성합니다. 뷰는 `resources/views/components` 디렉토리에 배치됩니다. 자신의 애플리케이션용으로 구성 요소를 작성할 때, 구성 요소는 `app/View/Components` 디렉토리와 `resources/views/components` 디렉토리 내에서 자동으로 발견되므로 일반적으로 추가적인 구성 요소 등록은 필요하지 않습니다.

하위 디렉토리 내에서도 구성 요소를 생성할 수 있습니다:

```shell
php artisan make:component Forms/Input
```



위 명령은 `app/View/Components/Forms` 디렉토리에 `Input` 구성 요소를 생성하며, 뷰는 `resources/views/components/forms` 디렉토리에 배치됩니다.

<a name="manually-registering-package-components"></a>
#### 패키지 구성 요소 수동 등록

자신의 애플리케이션용 구성 요소를 작성할 때 구성 요소는 `app/View/Components` 디렉토리와 `resources/views/components` 디렉토리에서 자동으로 발견됩니다.

그러나 Blade 구성 요소를 사용하는 패키지를 빌드하는 경우, 구성 요소 클래스와 HTML 태그 별칭을 수동으로 등록해야 합니다. 일반적으로 패키지의 서비스 제공자의 `boot` 메서드에서 구성 요소를 등록해야 합니다.

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', Alert::class);
}
```



컴포넌트가 등록되면, 태그 별칭을 사용하여 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```



또는 `componentNamespace` 방법을 사용하여 컨벤션에 따라 컴포넌트 클래스를 자동으로 로드할 수 있습니다. 예를 들어, `Nightshade` 패키지는 `Package\Views\Components` 네임스페이스에 위치한 `Calendar` 및 `ColorPicker` 컴포넌트를 가질 수 있습니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```



이를 통해 `package-name::` 구문을 사용하여 공급업체 네임스페이스로 패키지 구성 요소를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```



Blade는 구성 요소 이름을 파스칼 케이스로 작성하여 이 구성 요소와 연결된 클래스를 자동으로 감지합니다. 하위 디렉터리도 "점" 표기법을 사용하여 지원됩니다.

### 렌더링 구성 요소

구성 요소를 표시하려면 Blade 템플릿 중 하나 내에서 Blade 구성 요소 태그를 사용할 수 있습니다. Blade 구성 요소 태그는 `x-` 문자열로 시작하며, 그 다음에 구성 요소 클래스의 케밥 케이스 이름이 옵니다:

```blade
<x-alert/>

<x-user-profile/>
```



컴포넌트 클래스가 `app/View/Components` 디렉토리 내 더 깊숙이 중첩되어 있는 경우, 디렉토리 중첩을 나타내기 위해 `.` 문자를 사용할 수 있습니다. 예를 들어, 컴포넌트가 `app/View/Components/Inputs/Button.php`에 위치한다고 가정하면 다음과 같이 렌더링할 수 있습니다:

```blade
<x-inputs.button/>
```



컴포넌트를 조건부로 렌더링하고 싶다면, 컴포넌트 클래스에 `shouldRender` 메서드를 정의할 수 있습니다. 만약 `shouldRender` 메서드가 `false`를 반환하면 컴포넌트는 렌더링되지 않습니다:

```php
use Illuminate\Support\Str;

/**
 * Whether the component should be rendered
 */
public function shouldRender(): bool
{
    return Str::length($this->message) > 0;
}
```



<a name="index-components"></a>
### 인덱스 구성 요소

때때로 구성 요소는 구성 요소 그룹의 일부일 수 있으며 관련 구성 요소를 단일 디렉터리 내에 그룹화하고 싶을 수 있습니다. 예를 들어, 다음 클래스 구조를 가진 "카드" 구성 요소를 상상해 보십시오:

```text
App\Views\Components\Card\Card
App\Views\Components\Card\Header
App\Views\Components\Card\Body
```



루트 `Card` 컴포넌트가 `Card` 디렉토리 내에 중첩되어 있으므로 `<x-card.card>`를 통해 컴포넌트를 렌더링해야 할 것처럼 보일 수 있습니다. 그러나 컴포넌트의 파일 이름이 컴포넌트 디렉토리의 이름과 일치하면, Laravel은 자동으로 해당 컴포넌트를 "루트" 컴포넌트로 간주하고 디렉토리 이름을 반복하지 않고도 컴포넌트를 렌더링할 수 있도록 허용합니다:

```blade
<x-card>
    <x-card.header>...</x-card.header>
    <x-card.body>...</x-card.body>
</x-card>
```



<a name="passing-data-to-components"></a>
### 컴포넌트에 데이터 전달하기

HTML 속성을 사용하여 Blade 컴포넌트에 데이터를 전달할 수 있습니다. 하드코딩된 원시 값은 단순한 HTML 속성 문자열을 사용하여 컴포넌트에 전달할 수 있습니다. PHP 표현식 및 변수는 `:` 문자를 접두사로 사용하는 속성을 통해 컴포넌트에 전달해야 합니다:

```blade
<x-alert type="error" :message="$message"/>
```



컴포넌트의 모든 데이터 속성은 클래스 생성자에서 정의해야 합니다. 컴포넌트의 모든 공개 속성은 자동으로 컴포넌트의 뷰에서 사용 가능하게 됩니다. 데이터가 컴포넌트의 `render` 메서드에서 뷰로 전달될 필요는 없습니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

class Alert extends Component
{
    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
        public string $message,
    ) {}

    /**
     * Get the view / contents that represent the component.
     */
    public function render(): View
    {
        return view('components.alert');
    }
}
```



컴포넌트가 렌더링될 때, 변수 이름을 사용하여 변수를 출력함으로써 컴포넌트의 공용 변수 내용을 표시할 수 있습니다:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```



<a name="casing"></a>
#### 대소문자

컴포넌트 생성자 인수는 `camelCase`를 사용하여 지정해야 하며, HTML 속성에서 인수 이름을 참조할 때는 `kebab-case`를 사용해야 합니다. 예를 들어, 다음과 같은 컴포넌트 생성자가 주어진 경우:

```php
/**
 * Create the component instance.
 */
public function __construct(
    public string $alertType,
) {}
```



`$alertType` 인수는 다음과 같이 구성 요소에 제공될 수 있습니다:

```blade
<x-alert alert-type="danger" />
```



<a name="short-attribute-syntax"></a>
#### 짧은 속성 구문

컴포넌트에 속성을 전달할 때, "짧은 속성" 구문을 사용할 수도 있습니다. 속성 이름이 대응하는 변수 이름과 일치하는 경우가 많기 때문에 이것이 자주 편리합니다:

```blade
{{-- Short attribute syntax... --}}
<x-profile :$userId :$name />

{{-- Is equivalent to... --}}
<x-profile :user-id="$userId" :name="$name" />
```



<a name="escaping-attribute-rendering"></a>
#### 속성 렌더링 이스케이프

Alpine.js와 같은 일부 JavaScript 프레임워크도 콜론이 붙은 속성을 사용하기 때문에, Blade에게 해당 속성이 PHP 표현식이 아님을 알리기 위해 이중 콜론(`::`) 접두사를 사용할 수 있습니다. 예를 들어, 다음과 같은 컴포넌트가 있다고 가정할 때:

```blade
<x-button ::class="{ danger: isDeleting }">
    Submit
</x-button>
```



다음 HTML은 Blade에 의해 렌더링됩니다:

```blade
<button :class="{ danger: isDeleting }">
    Submit
</button>
```



<a name="component-methods"></a>
#### 컴포넌트 메서드

컴포넌트 템플릿에서 공개 변수를 사용할 수 있는 것 외에도, 컴포넌트에 있는 모든 공개 메서드를 호출할 수 있습니다. 예를 들어, 다음과 같은 `isSelected` 메서드를 가진 컴포넌트를 상상해 보세요:

```php
/**
 * Determine if the given option is the currently selected option.
 */
public function isSelected(string $option): bool
{
    return $option === $this->selected;
}
```



이 메서드는 메서드 이름과 일치하는 변수를 호출하여 컴포넌트 템플릿에서 실행할 수 있습니다:

```blade
<option {{ $isSelected($value) ? 'selected' : '' }} value="{{ $value }}">
    {{ $label }}
</option>
```



<a name="using-attributes-slots-within-component-class"></a>
#### 컴포넌트 클래스 내에서 속성과 슬롯 접근하기

Blade 컴포넌트는 클래스의 render 메서드 안에서 컴포넌트 이름, 속성, 슬롯에 접근할 수 있도록 합니다. 그러나 이 데이터를 접근하려면, 컴포넌트의 `render` 메서드에서 클로저를 반환해야 합니다:

```php
use Closure;

/**
 * Get the view / contents that represent the component.
 */
public function render(): Closure
{
    return function () {
        return '<div {{ $attributes }}>Components content</div>';
    };
}
```



귀하의 컴포넌트 `render` 메서드가 반환하는 클로저는 `$data` 배열을 유일한 인수로 받을 수도 있습니다. 이 배열에는 컴포넌트에 대한 정보를 제공하는 여러 요소가 포함될 것입니다:

```php
return function (array $data) {
    // $data['componentName'];
    // $data['attributes'];
    // $data['slot'];

    return '<div {{ $attributes }}>Components content</div>';
};
```



> [!WARNING]
> `$data` 배열의 요소는 `render` 메서드가 반환하는 Blade 문자열에 직접 삽입하지 않아야 합니다. 이렇게 하면 악성 속성 내용을 통해 원격 코드 실행이 가능해질 수 있습니다.

`componentName`는 `x-` 접두사 뒤에 HTML 태그에서 사용된 이름과 동일합니다. 따라서 `<x-alert />`의 `componentName`는 `alert`가 됩니다. `attributes` 요소에는 HTML 태그에 존재하는 모든 속성이 포함됩니다. `slot` 요소는 컴포넌트 슬롯의 내용을 가진 `Illuminate\Support\HtmlString` 인스턴스입니다.

클로저는 문자열을 반환해야 합니다. 반환된 문자열이 기존 뷰와 일치하면 해당 뷰가 렌더링되고, 그렇지 않으면 반환된 문자열이 인라인 Blade 뷰로 평가됩니다.

<a name="additional-dependencies"></a>
#### 추가 종속성

컴포넌트가 Laravel의 [서비스 컨테이너](/docs/{{version}}/container)에서 종속성을 필요로 하는 경우, 컴포넌트의 데이터 속성 앞에 나열하면 컨테이너가 자동으로 주입합니다:

```php
use App\Services\AlertCreator;

/**
 * Create the component instance.
 */
public function __construct(
    public AlertCreator $creator,
    public string $type,
    public string $message,
) {}
```



<a name="hiding-attributes-and-methods"></a>
#### 속성 / 메서드 숨기기

일부 공개 메서드나 속성이 컴포넌트 템플릿에 변수로 노출되는 것을 방지하려면, 이를 컴포넌트의 `$except` 배열 속성에 추가할 수 있습니다:

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;

class Alert extends Component
{
    /**
     * The properties / methods that should not be exposed to the component template.
     *
     * @var array
     */
    protected $except = ['type'];

    /**
     * Create the component instance.
     */
    public function __construct(
        public string $type,
    ) {}
}
```



<a name="component-attributes"></a>
### 구성 요소 속성

데이터 속성을 구성 요소에 전달하는 방법을 이미 살펴보았습니다. 하지만 때때로 구성 요소가 작동하는 데 필요한 데이터의 일부가 아닌 추가 HTML 속성(`class` 등)을 지정해야 할 때가 있습니다. 일반적으로 이러한 추가 속성은 구성 요소 템플릿의 루트 요소로 전달하고자 합니다. 예를 들어, `alert` 구성 요소를 다음과 같이 렌더링한다고 가정해 봅시다:

```blade
<x-alert type="error" :message="$message" class="mt-4"/>
```



컴포넌트의 생성자에 포함되지 않은 모든 속성은 자동으로 컴포넌트의 '속성 가방(attribute bag)'에 추가됩니다. 이 속성 가방은 `$attributes` 변수를 통해 컴포넌트에서 자동으로 사용할 수 있습니다. 모든 속성은 이 변수를 출력하여 컴포넌트 내에서 렌더링할 수 있습니다:

```blade
<div {{ $attributes }}>
    <!-- Component content -->
</div>
```



> [!WARNING]
> 현재 구성 요소 태그 내에서 `@env`와 같은 지시문 사용은 지원되지 않습니다. 예를 들어, `<x-alert :live="@env('production')"/>`는 컴파일되지 않습니다.

<a name="default-merged-attributes"></a>
#### 기본 / 병합된 속성

때때로 속성에 대한 기본값을 지정하거나 일부 구성 요소 속성에 추가 값을 병합해야 할 수도 있습니다. 이를 수행하기 위해 속성 백의 `merge` 메서드를 사용할 수 있습니다. 이 메서드는 구성 요소에 항상 적용되어야 하는 기본 CSS 클래스 세트를 정의할 때 특히 유용합니다:

```blade
<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```



이 구성 요소가 다음과 같이 사용된다고 가정하면:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```



컴포넌트의 최종 렌더링된 HTML은 다음과 같이 나타납니다:

```blade
<div class="alert alert-error mb-4">
    <!-- Contents of the $message variable -->
</div>
```



<a name="conditionally-merge-classes"></a>
#### 조건부 병합 클래스

때때로 주어진 조건이 `true` 경우 클래스를 병합하고 싶을 수도 있습니다. 이는 `class` 메서드를 통해 가능하며, 배열 키에는 추가하려는 클래스가 포함되고, 값은 불리언 표현식이 포함된 클래스 배열을 허용합니다. 배열 요소에 숫자 키가 있다면, 항상 렌더링된 클래스 목록에 포함됩니다:

```blade
<div {{ $attributes->class(['p-4', 'bg-red' => $hasError]) }}>
    {{ $message }}
</div>
```



컴포넌트에 다른 속성을 병합해야 하는 경우, `class` 메서드에 `merge` 메서드를 연결할 수 있습니다:

```blade
<button {{ $attributes->class(['p-4'])->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```



> [!NOTE]
> 다른 HTML 요소에서 클래스에 따라 조건부로 컴파일해야 하며 병합된 속성을 받지 않아야 하는 경우, [@class 지시문](#conditional-classes)을 사용할 수 있습니다.

<a name="non-class-attribute-merging"></a>
#### 클래스가 아닌 속성 병합

클래스 속성이 아닌 속성을 병합할 때, `merge` 메서드에 제공된 값은 해당 속성의 "기본" 값으로 간주됩니다. 그러나 `class` 속성과 달리 이러한 속성은 주입된 속성 값과 병합되지 않습니다. 대신 덮어씌워집니다. 예를 들어, `button` 컴포넌트의 구현은 다음과 같을 수 있습니다:

```blade
<button {{ $attributes->merge(['type' => 'button']) }}>
    {{ $slot }}
</button>
```



버튼 컴포넌트를 사용자 정의 `type`로 렌더링하려면, 컴포넌트를 사용할 때 지정할 수 있습니다. 유형이 지정되지 않으면 `button` 유형이 사용됩니다:

```blade
<x-button type="submit">
    Submit
</x-button>
```



이 예제에서 `button` 컴포넌트의 렌더링된 HTML은 다음과 같습니다:

```blade
<button type="submit">
    Submit
</button>
```



`class`가 아닌 다른 속성이 기본 값과 주입된 값을 함께 가지기를 원한다면 `prepends` 메서드를 사용할 수 있습니다. 이 예제에서는 `data-controller` 속성이 항상 `profile-controller`로 시작하며, 추가로 주입된 `data-controller` 값은 이 기본 값 뒤에 배치됩니다:

```blade
<div {{ $attributes->merge(['data-controller' => $attributes->prepends('profile-controller')]) }}>
    {{ $slot }}
</div>
```



<a name="filtering-attributes"></a>
#### 속성 검색 및 필터링

`filter` 메서드를 사용하여 속성을 필터링할 수 있습니다. 이 메서드는 클로저를 받아들이며, 속성 가방에 속성을 유지하려면 `true`를 반환해야 합니다:

```blade
{{ $attributes->filter(fn (string $value, string $key) => $key == 'foo') }}
```



편의를 위해, 주어진 문자열로 시작하는 키를 가진 모든 속성을 가져오기 위해 `whereStartsWith` 방법을 사용할 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model') }}
```



반대로, `whereDoesntStartWith` 방법은 특정 문자열로 시작하는 키를 가진 모든 속성을 제외하는 데 사용될 수 있습니다:

```blade
{{ $attributes->whereDoesntStartWith('wire:model') }}
```



`first` 방법을 사용하면 주어진 속성 백에서 첫 번째 속성을 렌더링할 수 있습니다:

```blade
{{ $attributes->whereStartsWith('wire:model')->first() }}
```



컴포넌트에 속성이 있는지 확인하고 싶다면, `has` 메서드를 사용할 수 있습니다. 이 메서드는 속성 이름을 유일한 인수로 받아들이고, 속성이 존재하는지 여부를 나타내는 불리언 값을 반환합니다:

```blade
@if ($attributes->has('class'))
    <div>Class attribute is present</div>
@endif
```



배열이 `has` 메서드에 전달되면, 메서드는 주어진 모든 속성이 컴포넌트에 존재하는지 여부를 확인합니다:

```blade
@if ($attributes->has(['name', 'class']))
    <div>All of the attributes are present</div>
@endif
```



`hasAny` 방법은 구성 요소에 주어진 속성이 있는지 확인하는 데 사용할 수 있습니다:

```blade
@if ($attributes->hasAny(['href', ':href', 'v-bind:href']))
    <div>One of the attributes is present</div>
@endif
```



`get` 메서드를 사용하여 특정 속성의 값을 가져올 수 있습니다:

```blade
{{ $attributes->get('class') }}
```



`only` 방법은 주어진 키를 가진 속성만 검색하는 데 사용할 수 있습니다:

```blade
{{ $attributes->only(['class']) }}
```



`except` 방법은 지정된 키를 가진 속성을 제외한 모든 속성을 가져오는 데 사용할 수 있습니다:

```blade
{{ $attributes->except(['class']) }}
```



<a name="reserved-keywords"></a>
### 예약어

기본적으로 일부 키워드는 Blade의 내부 사용을 위해 예약되어 있어 컴포넌트를 렌더링할 때 사용됩니다. 다음 키워드는 컴포넌트 내에서 공개 속성이나 메서드 이름으로 정의할 수 없습니다:

<div class="content-list" markdown="1">

- `data`
- `render`
- `resolve`
- `resolveView`
- `shouldRender`
- `view`
- `withAttributes`
- `withName`

</div>

<a name="slots"></a>
### 슬롯

컴포넌트에 추가 콘텐츠를 전달해야 하는 경우가 자주 있습니다. 이때 "슬롯"을 사용합니다. 컴포넌트 슬롯은 `$slot` 변수를 출력하여 렌더링됩니다. 이 개념을 탐구하기 위해, `alert` 컴포넌트가 다음과 같은 마크업을 가지고 있다고 가정해 봅시다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<div class="alert alert-danger">
    {{ $slot }}
</div>
```



우리는 컴포넌트에 콘텐츠를 주입하여 `slot`에 콘텐츠를 전달할 수 있습니다:

```blade
<x-alert>
    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```



때때로 컴포넌트는 컴포넌트 내의 여러 다른 위치에 여러 다른 슬롯을 렌더링해야 할 수 있습니다. 알림 컴포넌트를 수정하여 'title' 슬롯을 주입할 수 있도록 해보겠습니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    {{ $slot }}
</div>
```



`x-slot` 태그를 사용하여 명명된 슬롯의 내용을 정의할 수 있습니다. 명시적인 `x-slot` 태그 안에 포함되지 않은 모든 내용은 `$slot` 변수로 컴포넌트에 전달됩니다:

```xml
<x-alert>
    <x-slot:title>
        Server Error
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```



슬롯이 콘텐츠를 포함하고 있는지 확인하려면 슬롯의 `isEmpty` 메서드를 호출할 수 있습니다:

```blade
<span class="alert-title">{{ $title }}</span>

<div class="alert alert-danger">
    @if ($slot->isEmpty())
        This is default content if the slot is empty.
    @else
        {{ $slot }}
    @endif
</div>
```



또한, `hasActualContent` 방법은 슬롯이 HTML 주석이 아닌 '실제' 내용을 포함하고 있는지 여부를 확인하는 데 사용할 수 있습니다:

```blade
@if ($slot->hasActualContent())
    The scope has non-comment content.
@endif
```



<a name="scoped-slots"></a>
#### 스코프드 슬롯

Vue와 같은 자바스크립트 프레임워크를 사용해 본 적이 있다면, 슬롯 내에서 컴포넌트의 데이터나 메서드에 접근할 수 있는 "스코프드 슬롯"에 익숙할 수 있습니다. Laravel에서 유사한 동작을 구현하려면, 컴포넌트에 public 메서드나 속성을 정의하고 `$component` 변수를 통해 슬롯 내에서 컴포넌트에 접근하면 됩니다. 이 예제에서는 `x-alert` 컴포넌트가 컴포넌트 클래스에 public `formatAlert` 메서드를 정의했다고 가정하겠습니다:

```blade
<x-alert>
    <x-slot:title>
        {{ $component->formatAlert('Server Error') }}
    </x-slot>

    <strong>Whoops!</strong> Something went wrong!
</x-alert>
```



<a name="slot-attributes"></a>
#### 슬롯 속성

Blade 컴포넌트처럼 슬롯에 CSS 클래스 이름과 같은 추가 [속성](#component-attributes)을 지정할 수 있습니다:

```xml
<x-card class="shadow-sm">
    <x-slot:heading class="font-bold">
        Heading
    </x-slot>

    Content

    <x-slot:footer class="text-sm">
        Footer
    </x-slot>
</x-card>
```



슬롯 속성과 상호작용하려면 슬롯 변수의 `attributes` 속성에 접근할 수 있습니다. 속성과 상호작용하는 방법에 대한 자세한 정보는 [컴포넌트 속성](#component-attributes) 문서를 참조하십시오:

```blade
@props([
    'heading',
    'footer',
])

<div {{ $attributes->class(['border']) }}>
    <h1 {{ $heading->attributes->class(['text-lg']) }}>
        {{ $heading }}
    </h1>

    {{ $slot }}

    <footer {{ $footer->attributes->class(['text-gray-700']) }}>
        {{ $footer }}
    </footer>
</div>
```



<a name="inline-component-views"></a>
### 인라인 컴포넌트 뷰

매우 작은 컴포넌트의 경우, 컴포넌트 클래스와 컴포넌트의 뷰 템플릿을 모두 관리하는 것이 번거롭게 느껴질 수 있습니다. 이 이유로, `render` 메서드에서 컴포넌트의 마크업을 직접 반환할 수 있습니다:

```php
/**
 * Get the view / contents that represent the component.
 */
public function render(): string
{
    return <<<'blade'
        <div class="alert alert-danger">
            {{ $slot }}
        </div>
    blade;
}
```



<a name="generating-inline-view-components"></a>
#### 인라인 뷰 컴포넌트 생성

인라인 뷰를 렌더링하는 컴포넌트를 생성하려면 `make:component` 명령을 실행할 때 `inline` 옵션을 사용할 수 있습니다:

```shell
php artisan make:component Alert --inline
```



<a name="dynamic-components"></a>
### 동적 컴포넌트

때때로 컴포넌트를 렌더링해야 하지만 런타임까지 어떤 컴포넌트를 렌더링해야 할지 모를 때가 있습니다. 이러한 상황에서는 Laravel의 내장 `dynamic-component` 컴포넌트를 사용하여 런타임 값이나 변수에 따라 컴포넌트를 렌더링할 수 있습니다:

```blade
// $componentName = "secondary-button";

<x-dynamic-component :component="$componentName" class="mt-4" />
```



<a name="manually-registering-components"></a>
### 컴포넌트 수동 등록

> [!WARNING]
> 컴포넌트를 수동으로 등록하는 다음 문서는 주로 뷰 컴포넌트를 포함하는 Laravel 패키지를 작성하는 사람에게 적용됩니다. 패키지를 작성하지 않는 경우, 이 부분의 컴포넌트 문서는 관련이 없을 수 있습니다.

자신의 애플리케이션용 컴포넌트를 작성할 때, 컴포넌트는 `app/View/Components` 디렉토리와 `resources/views/components` 디렉토리 내에서 자동으로 발견됩니다.

하지만 Blade 컴포넌트를 사용하는 패키지를 빌드하거나 컴포넌트를 일반적이지 않은 디렉토리에 배치하는 경우, Laravel이 컴포넌트를 찾을 수 있도록 컴포넌트 클래스와 해당 HTML 태그 별칭을 수동으로 등록해야 합니다. 일반적으로 패키지의 서비스 프로바이더의 `boot` 메서드에서 컴포넌트를 등록해야 합니다.

```php
use Illuminate\Support\Facades\Blade;
use VendorPackage\View\Components\AlertComponent;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::component('package-alert', AlertComponent::class);
}
```



컴포넌트가 등록되면, 해당 태그 별칭을 사용하여 렌더링할 수 있습니다:

```blade
<x-package-alert/>
```



#### 패키지 구성 요소 자동 로딩

또는 규칙에 따라 구성 요소 클래스를 자동으로 로드하기 위해 `componentNamespace` 방법을 사용할 수 있습니다. 예를 들어, `Nightshade` 패키지에는 `Package\Views\Components` 네임스페이스 내에 위치한 `Calendar` 및 `ColorPicker` 구성 요소가 있을 수 있습니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap your package's services.
 */
public function boot(): void
{
    Blade::componentNamespace('Nightshade\\Views\\Components', 'nightshade');
}
```



이를 통해 `package-name::` 구문을 사용하여 공급업체 네임스페이스로 패키지 구성 요소를 사용할 수 있습니다:

```blade
<x-nightshade::calendar />
<x-nightshade::color-picker />
```



Blade는 이 컴포넌트와 연결된 클래스를 컴포넌트 이름을 파스칼 케이스(Pascal Case)로 변환하여 자동으로 감지합니다. 하위 디렉토리도 "점" 표기법을 사용하여 지원됩니다.

<a name="anonymous-components"></a>
## 익명 컴포넌트

인라인 컴포넌트와 유사하게, 익명 컴포넌트는 단일 파일로 컴포넌트를 관리할 수 있는 메커니즘을 제공합니다. 그러나 익명 컴포넌트는 단일 뷰 파일만 사용하며 관련된 클래스가 없습니다. 익명 컴포넌트를 정의하려면 `resources/views/components` 디렉토리에 Blade 템플릿을 배치하기만 하면 됩니다. 예를 들어, `resources/views/components/alert.blade.php`에 컴포넌트를 정의한 경우, 다음과 같이 간단히 렌더링할 수 있습니다:

```blade
<x-alert/>
```



`.` 문자를 사용하여 구성 요소가 `components` 디렉토리 안쪽에 더 깊이 중첩되어 있는지 표시할 수 있습니다. 예를 들어, 구성 요소가 `resources/views/components/inputs/button.blade.php`에 정의되어 있다고 가정하면, 다음과 같이 렌더링할 수 있습니다:

```blade
<x-inputs.button/>
```



Artisan을 통해 익명 컴포넌트를 생성하려면 `make:component` 명령을 호출할 때 `--view` 플래그를 사용할 수 있습니다:

```shell
php artisan make:component forms.input --view
```



위 명령은 `resources/views/components/forms/input.blade.php`에 Blade 파일을 생성하며, 해당 파일은 `<x-forms.input />`를 통해 컴포넌트로 렌더링할 수 있습니다.

<a name="anonymous-index-components"></a>
### 익명 인덱스 컴포넌트

때때로 컴포넌트가 여러 Blade 템플릿으로 구성될 때, 주어진 컴포넌트의 템플릿을 하나의 디렉터리 내에 그룹화하고 싶을 수 있습니다. 예를 들어, 다음과 같은 디렉터리 구조를 가진 "accordion" 컴포넌트를 상상해 보십시오:

```text
/resources/views/components/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```



이 디렉토리 구조를 통해 아코디언 컴포넌트와 그 아이템을 다음과 같이 렌더링할 수 있습니다:

```blade
<x-accordion>
    <x-accordion.item>
        ...
    </x-accordion.item>
</x-accordion>
```



그러나 `x-accordion`를 통해 아코디언 컴포넌트를 렌더링하기 위해, 우리는 다른 아코디언 관련 템플릿과 함께 `accordion` 디렉토리에 중첩하는 대신 "index" 아코디언 컴포넌트 템플릿을 `resources/views/components` 디렉토리에 배치할 수밖에 없었습니다.

다행히도, Blade는 컴포넌트 디렉토리 안에 컴포넌트의 디렉토리 이름과 일치하는 파일을 배치할 수 있게 해줍니다. 이 템플릿이 존재하면, 디렉토리 내에 중첩되어 있어도 컴포넌트의 "루트" 요소로 렌더링할 수 있습니다. 따라서 위의 예제에서 제공된 동일한 Blade 구문을 계속 사용할 수 있으며, 다만 디렉토리 구조를 다음과 같이 조정할 것입니다:

```text
/resources/views/components/accordion/accordion.blade.php
/resources/views/components/accordion/item.blade.php
```



<a name="data-properties-attributes"></a>
### 데이터 속성 / 특성

익명 컴포넌트에는 관련 클래스가 없기 때문에, 어떤 데이터를 변수로 컴포넌트에 전달해야 하고 어떤 속성을 컴포넌트의 [속성 가방](#component-attributes)에 넣어야 하는지 구분하는 방법이 궁금할 수 있습니다.

컴포넌트의 Blade 템플릿 상단에서 `@props` 지시어를 사용하여 어떤 속성을 데이터 변수로 간주할지 지정할 수 있습니다. 컴포넌트의 다른 모든 속성은 컴포넌트의 속성 가방을 통해 사용할 수 있습니다. 데이터 변수에 기본값을 주고 싶다면, 배열 키로 변수명을, 배열 값으로 기본값을 지정하면 됩니다:

```blade
<!-- /resources/views/components/alert.blade.php -->

@props(['type' => 'info', 'message'])

<div {{ $attributes->merge(['class' => 'alert alert-'.$type]) }}>
    {{ $message }}
</div>
```



위의 컴포넌트 정의를 고려하면, 우리는 다음과 같이 컴포넌트를 렌더링할 수 있습니다:

```blade
<x-alert type="error" :message="$message" class="mb-4"/>
```



<a name="accessing-parent-data"></a>
### 부모 데이터 접근

때때로 자식 컴포넌트 내에서 부모 컴포넌트의 데이터에 접근하고 싶을 때가 있습니다. 이러한 경우, `@aware` 지시어를 사용할 수 있습니다. 예를 들어, 부모 `<x-menu>`와 자식 `<x-menu.item>`로 구성된 복잡한 메뉴 컴포넌트를 만들고 있다고 상상해 보세요:

```blade
<x-menu color="purple">
    <x-menu.item>...</x-menu.item>
    <x-menu.item>...</x-menu.item>
</x-menu>
```



`<x-menu>` 구성 요소는 다음과 같은 구현을 가질 수 있습니다:

```blade
<!-- /resources/views/components/menu/index.blade.php -->

@props(['color' => 'gray'])

<ul {{ $attributes->merge(['class' => 'bg-'.$color.'-200']) }}>
    {{ $slot }}
</ul>
```



`color` 속성이 부모(`<x-menu>`)로만 전달되었기 때문에 `<x-menu.item>` 내에서는 사용할 수 없습니다. 그러나 `@aware` 지시어를 사용하면 `<x-menu.item>` 내에서도 사용할 수 있습니다:

```blade
<!-- /resources/views/components/menu/item.blade.php -->

@aware(['color' => 'gray'])

<li {{ $attributes->merge(['class' => 'text-'.$color.'-800']) }}>
    {{ $slot }}
</li>
```



> [!WARNING]
> `@aware` 지시는 HTML 속성을 통해 명시적으로 부모 컴포넌트에 전달되지 않은 부모 데이터를 액세스할 수 없습니다. 부모 컴포넌트에 명시적으로 전달되지 않은 기본 `@props` 값은 `@aware` 지시어에서 액세스할 수 없습니다.

<a name="anonymous-component-paths"></a>
### 익명 컴포넌트 경로

앞서 논의한 바와 같이, 익명 컴포넌트는 일반적으로 Blade 템플릿을 `resources/views/components` 디렉토리에 배치하여 정의됩니다. 그러나 때때로 기본 경로 외에 Laravel에 다른 익명 컴포넌트 경로를 등록하고 싶을 수도 있습니다.

`anonymousComponentPath` 메서드는 첫 번째 인수로 익명 컴포넌트 위치에 대한 "경로"를 받고, 두 번째 선택적 인수로 컴포넌트를 배치할 "네임스페이스"를 받습니다. 일반적으로 이 메서드는 애플리케이션의 [서비스 제공자](/docs/{{version}}/providers) 중 하나의 `boot` 메서드에서 호출해야 합니다.

```php
/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::anonymousComponentPath(__DIR__.'/../components');
}
```



위의 예제와 같이 지정된 접두사 없이 컴포넌트 경로가 등록되면, 해당 접두사와 상관없이 Blade 컴포넌트에서 렌더링될 수 있습니다. 예를 들어, 위에 등록된 경로에 `panel.blade.php` 컴포넌트가 존재한다면 다음과 같이 렌더링될 수 있습니다:

```blade
<x-panel />
```



접두사 "namespaces"는 `anonymousComponentPath` 메서드의 두 번째 인수로 제공될 수 있습니다:

```php
Blade::anonymousComponentPath(__DIR__.'/../components', 'dashboard');
```



접두사가 제공되면 구성 요소가 렌더링될 때 구성 요소 이름에 구성 요소의 네임스페이스를 접두사로 붙여 해당 '네임스페이스' 내의 구성 요소를 렌더링할 수 있습니다:

```blade
<x-dashboard::panel />
```



<a name="building-layouts"></a>
## 레이아웃 구성

<a name="layouts-using-components"></a>
### 컴포넌트를 사용한 레이아웃

대부분의 웹 애플리케이션은 다양한 페이지에서 동일한 일반 레이아웃을 유지합니다. 모든 뷰에서 전체 레이아웃 HTML을 반복해야 한다면 애플리케이션을 유지 관리하는 것은 매우 번거롭고 어려울 것입니다. 다행히도, 이 레이아웃을 단일 [Blade 컴포넌트](#components)로 정의한 후 애플리케이션 전반에 걸쳐 사용할 수 있어 편리합니다.

<a name="defining-the-layout-component"></a>
#### 레이아웃 컴포넌트 정의

예를 들어, "할 일" 목록 애플리케이션을 만든다고 가정해 봅시다. 다음과 같이 생긴 `layout` 컴포넌트를 정의할 수 있습니다:

```blade
<!-- resources/views/components/layout.blade.php -->

<html>
    <head>
        <title>{{ $title ?? 'Todo Manager' }}</title>
    </head>
    <body>
        <h1>Todos</h1>
        <hr/>
        {{ $slot }}
    </body>
</html>
```



<a name="applying-the-layout-component"></a>
#### 레이아웃 컴포넌트 적용하기

`layout` 컴포넌트가 정의되면, 해당 컴포넌트를 사용하는 Blade 뷰를 만들 수 있습니다. 이 예제에서는 작업 목록을 표시하는 간단한 뷰를 정의하겠습니다:

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```



기억하세요, 컴포넌트에 주입된 콘텐츠는 우리 `layout` 컴포넌트 내의 기본 `$slot` 변수에 제공됩니다. 아시다시피, 우리 `layout`도 `$title` 슬롯이 제공되면 이를 존중하며, 그렇지 않으면 기본 제목이 표시됩니다. 우리는 [컴포넌트 문서](#components)에서 논의된 표준 슬롯 구문을 사용하여 작업 목록 뷰에서 사용자 정의 제목을 주입할 수 있습니다.

```blade
<!-- resources/views/tasks.blade.php -->

<x-layout>
    <x-slot:title>
        Custom Title
    </x-slot>

    @foreach ($tasks as $task)
        <div>{{ $task }}</div>
    @endforeach
</x-layout>
```



이제 레이아웃과 작업 목록 뷰를 정의했으므로, 우리는 단지 경로에서 `task` 뷰를 반환하면 됩니다:

```php
use App\Models\Task;

Route::get('/tasks', function () {
    return view('tasks', ['tasks' => Task::all()]);
});
```



<a name="layouts-using-template-inheritance"></a>
### 템플릿 상속을 사용한 레이아웃

<a name="defining-a-layout"></a>
#### 레이아웃 정의하기

레이아웃은 또한 "템플릿 상속"을 통해 생성할 수 있습니다. 이는 [컴포넌트](#components)가 도입되기 전 애플리케이션을 구축하는 주요 방법이었습니다.

시작하려면 간단한 예제를 살펴보겠습니다. 먼저 페이지 레이아웃을 검토합니다. 대부분의 웹 애플리케이션이 다양한 페이지에서 동일한 일반 레이아웃을 유지하므로, 이 레이아웃을 단일 Blade 뷰로 정의하는 것이 편리합니다:

```blade
<!-- resources/views/layouts/app.blade.php -->

<html>
    <head>
        <title>App Name - @yield('title')</title>
    </head>
    <body>
        @section('sidebar')
            This is the master sidebar.
        @show

        <div class="container">
            @yield('content')
        </div>
    </body>
</html>
```



보시다시피, 이 파일에는 일반적인 HTML 마크업이 포함되어 있습니다. 그러나 `@section` 및 `@yield` 지시문에 주목하십시오. 이름에서 알 수 있듯이 `@section` 지시문은 콘텐츠 섹션을 정의하며, `@yield` 지시문은 주어진 섹션의 내용을 표시하는 데 사용됩니다.

이제 애플리케이션의 레이아웃을 정의했으므로, 레이아웃을 상속하는 자식 페이지를 정의해 보겠습니다.

<a name="extending-a-layout"></a>
#### 레이아웃 확장

자식 뷰를 정의할 때, `@extends` Blade 지시문을 사용하여 자식 뷰가 '상속'할 레이아웃을 지정하십시오. Blade 레이아웃을 확장하는 뷰는 `@section` 지시문을 사용하여 레이아웃의 섹션에 콘텐츠를 삽입할 수 있습니다. 위의 예에서 보듯이, 이러한 섹션의 내용은 `@yield`를 사용하여 레이아웃에 표시됩니다.

```blade
<!-- resources/views/child.blade.php -->

@extends('layouts.app')

@section('title', 'Page Title')

@section('sidebar')
    @@parent

    <p>This is appended to the master sidebar.</p>
@endsection

@section('content')
    <p>This is my body content.</p>
@endsection
```



이 예제에서 `sidebar` 섹션은 레이아웃의 사이드바에 콘텐츠를 덮어쓰지 않고 추가(append)하기 위해 `@@parent` 지시문을 사용하고 있습니다. `@@parent` 지시문은 뷰가 렌더링될 때 레이아웃의 콘텐츠로 대체됩니다.

> [!NOTE]
> 이전 예제와 달리, 이 `sidebar` 섹션은 `@show` 대신 `@endsection`로 끝납니다. `@endsection` 지시문은 섹션을 정의만 하고, `@show`는 섹션을 정의하고 **즉시 출력(yield)** 합니다.

`@yield` 지시문은 두 번째 매개변수로 기본값도 허용합니다. 이 값은 출력되는 섹션이 정의되지 않은 경우 렌더링됩니다:

```blade
@yield('content', 'Default content')
```



<a name="forms"></a>
## 폼

<a name="csrf-field"></a>
### CSRF 필드

애플리케이션에서 HTML 폼을 정의할 때마다, 요청을 [CSRF 보호](/docs/{{version}}/csrf) 미들웨어가 검증할 수 있도록 폼에 숨겨진 CSRF 토큰 필드를 포함해야 합니다. 토큰 필드를 생성하기 위해 `@csrf` Blade 지시문을 사용할 수 있습니다:

```blade
<form method="POST" action="/profile">
    @csrf

    ...
</form>
```



<a name="method-field"></a>
### 메서드 필드

HTML 폼은 `PUT`, `PATCH`, 또는 `DELETE` 요청을 만들 수 없기 때문에, 이러한 HTTP 메서드를 속이기 위해 숨겨진 `_method` 필드를 추가해야 합니다. `@method` 블레이드 지시문이 이 필드를 생성할 수 있습니다:

```blade
<form action="/foo/bar" method="POST">
    @method('PUT')

    ...
</form>
```



<a name="validation-errors"></a>
### 검증 오류

`@error` 지시문은 주어진 속성에 대해 [검증 오류 메시지](/docs/{{version}}/validation#quick-displaying-the-validation-errors)가 존재하는지 빠르게 확인하는 데 사용할 수 있습니다. `@error` 지시문 내에서 `$message` 변수를 출력하여 오류 메시지를 표시할 수 있습니다:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```



`@error` 지시문은 'if' 문으로 컴파일되므로, 속성에 오류가 없을 때 콘텐츠를 렌더링하기 위해 `@else` 지시문을 사용할 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email') is-invalid @else is-valid @enderror"
/>
```



여러 폼이 포함된 페이지에서 검증 오류 메시지를 가져오기 위해 `@error` 지시문에 두 번째 매개변수로 [특정 오류 가방의 이름](/docs/{{version}}/validation#named-error-bags)을 전달할 수 있습니다:

```blade
<!-- /resources/views/auth.blade.php -->

<label for="email">Email address</label>

<input
    id="email"
    type="email"
    class="@error('email', 'login') is-invalid @enderror"
/>

@error('email', 'login')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```



<a name="stacks"></a>
## 스택

Blade는 다른 뷰나 레이아웃에서 어디서든 렌더링할 수 있는 이름 있는 스택에 푸시할 수 있게 해줍니다. 이는 자식 뷰에서 필요한 JavaScript 라이브러리를 지정하는 데 특히 유용할 수 있습니다:

```blade
@push('scripts')
    <script src="/example.js"></script>
@endpush
```



주어진 불리언 표현식이 `true`로 평가될 경우 `@push` 내용을 사용하고 싶다면, `@pushIf` 지시문을 사용할 수 있습니다:

```blade
@pushIf($shouldPush, 'scripts')
    <script src="/example.js"></script>
@endPushIf
```



필요한 만큼 스택에 푸시할 수 있습니다. 스택의 전체 내용을 렌더링하려면 스택 이름을 `@stack` 지시문에 전달하십시오:

```blade
<head>
    <!-- Head Contents -->

    @stack('scripts')
</head>
```



스택의 시작 부분에 내용을 추가하고 싶다면, `@prepend` 지시어를 사용해야 합니다:

```blade
@push('scripts')
    This will be second...
@endpush

// Later...

@prepend('scripts')
    This will be first...
@endprepend
```



스택이 비어 있는지 확인하기 위해 `@hasstack` 지시문을 사용할 수 있습니다:

```blade
@hasstack('list')
    <ul>
        @stack('list')
    </ul>
@endif
```



<a name="service-injection"></a>
## 서비스 주입

`@inject` 지시어는 Laravel [서비스 컨테이너](/docs/{{version}}/container)에서 서비스를 가져오는 데 사용할 수 있습니다. `@inject`에 전달되는 첫 번째 인수는 서비스가 저장될 변수의 이름이고, 두 번째 인수는 해결하려는 서비스의 클래스 또는 인터페이스 이름입니다:

```blade
@inject('metrics', 'App\Services\MetricsService')

<div>
    Monthly Revenue: {{ $metrics->monthlyRevenue() }}.
</div>
```



<a name="rendering-inline-blade-templates"></a>
## 인라인 블레이드 템플릿 렌더링

때때로 원시 블레이드 템플릿 문자열을 유효한 HTML로 변환해야 할 때가 있습니다. 이를 위해 `Blade` 파사드에서 제공하는 `render` 메서드를 사용할 수 있습니다. `render` 메서드는 블레이드 템플릿 문자열과 템플릿에 제공할 선택적 데이터 배열을 받습니다:

```php
use Illuminate\Support\Facades\Blade;

return Blade::render('Hello, {{ $name }}', ['name' => 'Julian Bashir']);
```



Laravel은 Blade 템플릿을 인라인으로 렌더링할 때 이를 `storage/framework/views` 디렉토리에 작성합니다. Blade 템플릿을 렌더링한 후 Laravel이 이러한 임시 파일을 제거하도록 하려면 메서드에 `deleteCachedView` 인수를 제공할 수 있습니다:

```php
return Blade::render(
    'Hello, {{ $name }}',
    ['name' => 'Julian Bashir'],
    deleteCachedView: true
);
```



<a name="rendering-blade-fragments"></a>
## 블레이드 조각 렌더링

[Turbo](https://turbo.hotwired.dev/) 및 [htmx](https://htmx.org/)와 같은 프런트엔드 프레임워크를 사용할 때, 때로는 HTTP 응답 내에서 블레이드 템플릿의 일부만 반환해야 할 필요가 있습니다. 블레이드 "조각"을 사용하면 정확히 그렇게 할 수 있습니다. 시작하려면 블레이드 템플릿의 일부를 `@fragment` 및 `@endfragment` 지시문 안에 배치하세요:

```blade
@fragment('user-list')
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@endfragment
```



그런 다음, 이 템플릿을 사용하는 뷰를 렌더링할 때, `fragment` 메서드를 호출하여 지정된 프래그먼트만 아웃고잉 HTTP 응답에 포함되도록 지정할 수 있습니다:

```php
return view('dashboard', ['users' => $users])->fragment('user-list');
```



`fragmentIf` 방법은 주어진 조건에 따라 뷰의 일부를 조건부로 반환할 수 있게 해줍니다. 그렇지 않으면 전체 뷰가 반환됩니다:

```php
return view('dashboard', ['users' => $users])
    ->fragmentIf($request->hasHeader('HX-Request'), 'user-list');
```



`fragments` 및 `fragmentsIf` 메서드는 응답에서 여러 뷰 프래그먼트를 반환할 수 있게 해줍니다. 프래그먼트들은 함께 연결될 것입니다:

```php
view('dashboard', ['users' => $users])
    ->fragments(['user-list', 'comment-list']);

view('dashboard', ['users' => $users])
    ->fragmentsIf(
        $request->hasHeader('HX-Request'),
        ['user-list', 'comment-list']
    );
```



<a name="extending-blade"></a>
## 블레이드 확장하기

블레이드는 `directive` 메서드를 사용하여 사용자가 직접 정의한 커스텀 지시문을 정의할 수 있게 해줍니다. 블레이드 컴파일러가 커스텀 지시문을 만나면, 지시문이 포함하고 있는 표현식을 사용하여 제공된 콜백을 호출합니다.

다음 예시는 주어진 `$var`를 포맷하는 `@datetime($var)` 지시문을 생성합니다. `$var`는 `DateTime`의 인스턴스여야 합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Support\Facades\Blade;
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
        Blade::directive('datetime', function (string $expression) {
            return "<?php echo ($expression)->format('m/d/Y H:i'); ?>";
        });
    }
}
```



보시다시피, 우리는 전달된 어떤 표현식에도 `format` 메서드를 연결할 것입니다. 따라서 이 예제에서, 이 지시문에 의해 생성되는 최종 PHP는 다음과 같습니다:

```php
<?php echo ($var)->format('m/d/Y H:i'); ?>
```



> [!WARNING]
> Blade 지시문의 로직을 업데이트한 후에는 모든 캐시된 Blade 뷰를 삭제해야 합니다. 캐시된 Blade 뷰는 `view:clear` Artisan 명령을 사용하여 제거할 수 있습니다.

<a name="custom-echo-handlers"></a>
### 사용자 정의 Echo 핸들러

Blade를 사용하여 객체를 "echo"하려고 하면, 객체의 `__toString` 메서드가 호출됩니다. [__toString](https://www.php.net/manual/en/language.oop5.magic.php#object.tostring) 메서드는 PHP에 내장된 "매직 메서드" 중 하나입니다. 그러나 때때로 특정 클래스의 `__toString` 메서드를 제어할 수 없는 경우가 있으며, 예를 들어 상호 작용 중인 클래스가 서드파티 라이브러리에 속하는 경우 등이 있습니다.

이러한 경우, Blade는 해당 객체 유형에 대한 사용자 정의 echo 핸들러를 등록할 수 있도록 합니다. 이를 수행하려면 Blade의 `stringable` 메서드를 호출해야 합니다. `stringable` 메서드는 클로저를 받습니다. 이 클로저는 렌더링할 객체 유형을 타입 힌트로 지정해야 합니다. 일반적으로 `stringable` 메서드는 애플리케이션의 `AppServiceProvider` 클래스의 `boot` 메서드 내에서 호출해야 합니다.

```php
use Illuminate\Support\Facades\Blade;
use Money\Money;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::stringable(function (Money $money) {
        return $money->formatTo('en_GB');
    });
}
```



사용자 정의 에코 핸들러를 정의한 후에는 Blade 템플릿에서 객체를 단순히 에코할 수 있습니다:

```blade
Cost: {{ $money }}
```



<a name="custom-if-statements"></a>
### 맞춤 If 문

맞춤 지시어를 프로그래밍하는 것은 단순한 맞춤 조건문을 정의할 때 때때로 필요 이상으로 복잡할 수 있습니다. 이러한 이유로 Blade는 클로저를 사용하여 맞춤 조건 지시어를 신속하게 정의할 수 있는 `Blade::if` 메서드를 제공합니다. 예를 들어, 애플리케이션에 구성된 기본 "디스크"를 확인하는 맞춤 조건을 정의해 보겠습니다. 우리는 이것을 `AppServiceProvider`의 `boot` 메서드에서 수행할 수 있습니다:

```php
use Illuminate\Support\Facades\Blade;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Blade::if('disk', function (string $value) {
        return config('filesystems.default') === $value;
    });
}
```



커스텀 조건이 정의되면, 이를 템플릿 내에서 사용할 수 있습니다:

```blade
@disk('local')
    <!-- The application is using the local disk... -->
@elsedisk('s3')
    <!-- The application is using the s3 disk... -->
@else
    <!-- The application is using some other disk... -->
@enddisk

@unlessdisk('local')
    <!-- The application is not using the local disk... -->
@enddisk
```
{% endraw %}
