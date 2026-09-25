---
layout: docs
title: "예지"
---

{% raw %}
# 예지

- [소개](#introduction)
- [Live Validation](#live-validation)
- 사용 뷰 (#using-vue)
- 반응 사용 (#using-react)
- 알파인 앤 블레이드 사용하기 (#using-alpine)
- [Configuring Axios](#configuring-axios)
- [검증 배열](#validating-arrays)
- [검증 규칙 사용자 지정](#customizing-validation-rules)
- [파일 업로드 처리](#handling-file-uploads)
- [측면효과 관리](#managing-side-effects)
- 테스팅 (#testing)

<a name="introduction"></a>
## 소개

Laravel Precognition 을 사용하면 향후 HTTP 요청의 결과를 예측할 수 있습니다. Precognition 의 주요 사용 사례 중 하나는 애플리케이션의 백엔드 검증 규칙을 복제할 필요 없이 프런트엔드 JavaScript 애플리케이션에 대한 “라이브” 검증을 제공하는 기능입니다。

Laravel 이 “예측 요청” 을 수신하면 경로의 모든 미들웨어를 실행하고 경로의 컨트롤러 종속성을 해결합니다. 여기에는 검증 [form requests](/docs/{{version}}/validation#form-request-validation) 이 포함됩니다. 하지만 실제로 경로의 컨트롤러 메서드를 실행하지는 않습니다。

> [!NOTE]
> Inertia 2.3 부터는 Precognition 지원이 내장되어 있습니다. 자세한 내용은 [Inertia Forms 문서](https://inertiajs.com/forms) 를 참조하세요. 이전 Inertia 버전에는 Precognition 0.x 가 필요합니다。

<a name="live-validation"></a>
## 라이브 검증

<a name="using-vue"></a>
### 뷰 사용하기

Laravel Precognition 을 사용하면 프런트엔드 Vue 애플리케이션에서 검증 규칙을 복제할 필요 없이 사용자에게 라이브 검증 경험을 제공할 수 있습니다. 작동 방식을 설명하기 위해 애플리케이션 내에서 새 사용자를 생성하기 위한 양식을 구축해 보겠습니다。

먼저， 경로에 대한 사전 인식을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 경로 정의에 추가해야 합니다. 또한 경로의 검증 규칙을 호스팅하기 위한 [형식 요청](/docs/{{version}}/validation#form-request-validation) 을 생성해야 합니다：

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```



다음으로, NPM을 통해 Vue용 Laravel Precognition 프론트엔드 헬퍼를 설치해야 합니다:

```shell
npm install laravel-precognition-vue
```



Laravel Precognition 패키지를 설치하면 이제 Precognition의 `useForm` 함수를 사용하여 폼 객체를 생성할 수 있으며, 여기에는 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 제공할 수 있습니다.

그런 다음 실시간 유효성 검사를 활성화하려면 각 입력의 `change` 이벤트에서 폼의 `validate` 메서드를 호출하고, 입력의 이름을 제공합니다:

```vue
<script setup>
import { useForm } from 'laravel-precognition-vue';

const form = useForm('post', '/users', {
    name: '',
    email: '',
});

const submit = () => form.submit();
</script>

<template>
    <form @submit.prevent="submit">
        <label for="name">Name</label>
        <input
            id="name"
            v-model="form.name"
            @change="form.validate('name')"
        />
        <div v-if="form.invalid('name')">
            {{ form.errors.name }}
        </div>

        <label for="email">Email</label>
        <input
            id="email"
            type="email"
            v-model="form.email"
            @change="form.validate('email')"
        />
        <div v-if="form.invalid('email')">
            {{ form.errors.email }}
        </div>

        <button :disabled="form.processing">
            Create User
        </button>
    </form>
</template>
```



이제 사용자가 양식을 작성하면, Precognition은 라우트의 폼 요청에 있는 검증 규칙에 따라 실시간 검증 출력을 제공합니다. 양식의 입력이 변경되면, 디바운스된 'precognitive' 검증 요청이 귀하의 Laravel 애플리케이션으로 전송됩니다. 양식의 `setValidationTimeout` 함수를 호출하여 디바운스 타임아웃을 구성할 수 있습니다:

```js
form.setValidationTimeout(3000);
```



검증 요청이 진행 중일 때, 폼의 `validating` 속성은 `true`가 됩니다:

```html
<div v-if="form.validating">
    Validating...
</div>
```



검증 요청이나 양식 제출 중 반환된 모든 검증 오류는 자동으로 양식의 `errors` 객체에 채워집니다:

```html
<div v-if="form.invalid('email')">
    {{ form.errors.email }}
</div>
```



양식의 `hasErrors` 속성을 사용하여 양식에 오류가 있는지 확인할 수 있습니다:

```html
<div v-if="form.hasErrors">
    <!-- ... -->
</div>
```



입력을 폼의 `valid` 및 `invalid` 함수에 각각 입력 이름을 전달하여 입력이 유효성 검사를 통과했는지 실패했는지도 확인할 수 있습니다:

```html
<span v-if="form.valid('email')">
    ✅
</span>

<span v-else-if="form.invalid('email')">
    ❌
</span>
```



> [!WARNING]
> 폼 입력은 변경되고 검증 응답을 받은 후에야 유효한지 또는 유효하지 않은지 나타납니다.

Precognition으로 폼 입력의 하위 집합을 검증하는 경우, 오류를 수동으로 지우는 것이 유용할 수 있습니다. 이를 위해 폼의 `forgetError` 함수를 사용할 수 있습니다:

```html
<input
    id="avatar"
    type="file"
    @change="(e) => {
        form.avatar = e.target.files[0]

        form.forgetError('avatar')
    }"
>
```



우리가 본 것처럼, 사용자가 입력과 상호작용할 때 개별 입력을 검증하기 위해 입력의 `change` 이벤트에 연결할 수 있습니다. 그러나 사용자가 아직 상호작용하지 않은 입력을 검증해야 할 수도 있습니다. 이는 '마법사'를 만들 때 흔히 발생하는 상황으로, 사용자가 상호작용했는지 여부와 상관없이 모든 표시된 입력을 다음 단계로 넘어가기 전에 검증하고자 할 때 유용합니다.

Precognition을 사용하여 이를 수행하려면, 검증하려는 필드 이름을 `only` 구성 키에 전달하면서 `validate` 메서드를 호출해야 합니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```



물론, 양식 제출에 대한 응답에 반응하여 코드를 실행할 수도 있습니다. 양식의 `submit` 함수는 Axios 요청 프라미스를 반환합니다. 이는 성공적인 제출 시 양식 입력을 초기화하거나, 실패한 요청을 처리하거나, 응답 페이로드에 접근할 수 있는 편리한 방법을 제공합니다:

```js
const submit = () => form.submit()
    .then(response => {
        form.reset();

        alert('User created.');
    })
    .catch(error => {
        alert('An error occurred.');
    });
```



폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성을 확인하여 결정할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```



<a name="using-react"></a>
### React 사용하기

Laravel Precognition을 사용하면 프론트엔드 React 애플리케이션에서 검증 규칙을 중복 작성하지 않고도 사용자에게 실시간 검증 경험을 제공할 수 있습니다. 작동 방식을 설명하기 위해, 애플리케이션 내에서 새 사용자를 생성하는 폼을 만들어 보겠습니다.

먼저, 특정 경로에 대해 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 경로 정의에 추가해야 합니다. 또한 경로의 검증 규칙을 담을 [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해야 합니다:

```php
use App\Http\Requests\StoreUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (StoreUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```



다음으로, NPM을 통해 React용 Laravel Precognition 프론트엔드 헬퍼를 설치해야 합니다:

```shell
npm install laravel-precognition-react
```



Laravel Precognition 패키지가 설치되면, 이제 Precognition의 `useForm` 함수를 사용하여 폼 객체를 생성할 수 있습니다. 이때 HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 제공해야 합니다.

라이브 검증을 활성화하려면 각 입력의 `change` 및 `blur` 이벤트를 청취해야 합니다. `change` 이벤트 핸들러에서 `setData` 함수를 사용하여 폼 데이터를 설정하고, 입력의 이름과 새 값을 전달해야 합니다. 그런 다음 `blur` 이벤트 핸들러에서 폼의 `validate` 메서드를 호출하며, 입력의 이름을 제공해야 합니다:

```jsx
import { useForm } from 'laravel-precognition-react';

export default function Form() {
    const form = useForm('post', '/users', {
        name: '',
        email: '',
    });

    const submit = (e) => {
        e.preventDefault();

        form.submit();
    };

    return (
        <form onSubmit={submit}>
            <label htmlFor="name">Name</label>
            <input
                id="name"
                value={form.data.name}
                onChange={(e) => form.setData('name', e.target.value)}
                onBlur={() => form.validate('name')}
            />
            {form.invalid('name') && <div>{form.errors.name}</div>}

            <label htmlFor="email">Email</label>
            <input
                id="email"
                value={form.data.email}
                onChange={(e) => form.setData('email', e.target.value)}
                onBlur={() => form.validate('email')}
            />
            {form.invalid('email') && <div>{form.errors.email}</div>}

            <button disabled={form.processing}>
                Create User
            </button>
        </form>
    );
};
```



이제 사용자가 양식을 작성하면, Precognition은 라우트의 폼 요청에 있는 검증 규칙에 따라 실시간 검증 출력을 제공합니다. 양식의 입력이 변경되면, 디바운스된 'precognitive' 검증 요청이 귀하의 Laravel 애플리케이션으로 전송됩니다. 양식의 `setValidationTimeout` 함수를 호출하여 디바운스 타임아웃을 구성할 수 있습니다:

```js
form.setValidationTimeout(3000);
```



검증 요청이 진행 중일 때, 폼의 `validating` 속성은 `true`가 됩니다:

```jsx
{form.validating && <div>Validating...</div>}
```



검증 요청이나 양식 제출 중 반환된 모든 검증 오류는 자동으로 양식의 `errors` 객체에 채워집니다:

```jsx
{form.invalid('email') && <div>{form.errors.email}</div>}
```



양식의 `hasErrors` 속성을 사용하여 양식에 오류가 있는지 확인할 수 있습니다:

```jsx
{form.hasErrors && <div><!-- ... --></div>}
```



입력을 폼의 `valid` 및 `invalid` 함수에 각각 입력 이름을 전달하여 입력이 유효성 검사를 통과했는지 또는 실패했는지 확인할 수도 있습니다:

```jsx
{form.valid('email') && <span>✅</span>}

{form.invalid('email') && <span>❌</span>}
```



> [!WARNING]
> 폼 입력은 변경되고 검증 응답을 받은 후에야 유효하거나 유효하지 않은 것으로 표시됩니다.

Precognition으로 폼 입력의 일부 집합을 검증하는 경우, 오류를 수동으로 지우는 것이 유용할 수 있습니다. 이를 위해 폼의 `forgetError` 기능을 사용할 수 있습니다:

```jsx
<input
    id="avatar"
    type="file"
    onChange={(e) => {
        form.setData('avatar', e.target.files[0]);

        form.forgetError('avatar');
    }}
>
```



우리가 본 것처럼, 사용자가 입력과 상호작용할 때 개별 입력을 검증하기 위해 입력의 `blur` 이벤트에 연결할 수 있습니다. 그러나 사용자가 아직 상호작용하지 않은 입력을 검증해야 할 수도 있습니다. 이는 '마법사'를 만들 때 흔히 발생하는 상황으로, 사용자가 상호작용했는지 여부와 상관없이 모든 표시된 입력을 다음 단계로 넘어가기 전에 검증하고자 할 때 유용합니다.

Precognition을 사용하여 이를 수행하려면, 검증하려는 필드 이름을 `only` 구성 키에 전달하면서 `validate` 메서드를 호출해야 합니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다:

```jsx
<button
    type="button"
    onClick={() => form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })}
>Next Step</button>
```



물론, 폼 제출에 대한 응답에 반응하여 코드를 실행할 수도 있습니다. 폼의 `submit` 함수는 Axios 요청 프로미스를 반환합니다. 이는 응답 데이터를 편리하게 접근하거나, 폼 제출이 성공했을 때 폼 입력을 초기화하거나, 요청이 실패했을 때 처리하는 방법을 제공합니다:

```js
const submit = (e) => {
    e.preventDefault();

    form.submit()
        .then(response => {
            form.reset();

            alert('User created.');
        })
        .catch(error => {
            alert('An error occurred.');
        });
};
```



폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성을 검사하여 확인할 수 있습니다:

```html
<button disabled={form.processing}>
    Submit
</button>
```



<a name="using-alpine"></a>
### Alpine과 Blade 사용

Laravel Precognition을 사용하면 프런트엔드 Alpine 애플리케이션에서 유효성 검사 규칙을 중복하지 않고도 사용자에게 실시간 유효성 검사 경험을 제공할 수 있습니다. 작동 방식을 보여주기 위해 애플리케이션 내에서 새 사용자를 생성하는 폼을 만들어 보겠습니다.

먼저, 라우트에 Precognition을 활성화하려면 `HandlePrecognitiveRequests` 미들웨어를 라우트 정의에 추가해야 합니다. 또한 라우트의 유효성 검사 규칙을 담을 [폼 요청](/docs/{{version}}/validation#form-request-validation)을 생성해야 합니다:

```php
use App\Http\Requests\CreateUserRequest;
use Illuminate\Foundation\Http\Middleware\HandlePrecognitiveRequests;

Route::post('/users', function (CreateUserRequest $request) {
    // ...
})->middleware([HandlePrecognitiveRequests::class]);
```



다음으로, NPM을 통해 Alpine용 Laravel Precognition 프론트엔드 헬퍼를 설치해야 합니다:

```shell
npm install laravel-precognition-alpine
```



그런 다음, `resources/js/app.js` 파일에서 Alpine에 Precognition 플러그인을 등록하세요:

```js
import Alpine from 'alpinejs';
import Precognition from 'laravel-precognition-alpine';

window.Alpine = Alpine;

Alpine.plugin(Precognition);
Alpine.start();
```



Laravel Precognition 패키지가 설치되고 등록되면, 이제 Precognition의 `$form` "마법"을 사용하여 폼 객체를 생성할 수 있으며, HTTP 메서드(`post`), 대상 URL(`/users`), 초기 폼 데이터를 제공할 수 있습니다.

실시간 검증을 활성화하려면 폼 데이터를 관련 입력에 바인딩하고 각 입력의 `change` 이벤트를 청취해야 합니다. `change` 이벤트 핸들러에서는 입력 이름을 제공하여 폼의 `validate` 메서드를 호출해야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '',
        email: '',
    }),
}">
    @csrf
    <label for="name">Name</label>
    <input
        id="name"
        name="name"
        x-model="form.name"
        @change="form.validate('name')"
    />
    <template x-if="form.invalid('name')">
        <div x-text="form.errors.name"></div>
    </template>

    <label for="email">Email</label>
    <input
        id="email"
        name="email"
        x-model="form.email"
        @change="form.validate('email')"
    />
    <template x-if="form.invalid('email')">
        <div x-text="form.errors.email"></div>
    </template>

    <button :disabled="form.processing">
        Create User
    </button>
</form>
```



이제 사용자가 양식을 작성하면, Precognition은 라우트의 폼 요청에 있는 검증 규칙에 따라 실시간 검증 출력을 제공합니다. 양식의 입력이 변경되면, 디바운스된 'precognitive' 검증 요청이 귀하의 Laravel 애플리케이션으로 전송됩니다. 양식의 `setValidationTimeout` 함수를 호출하여 디바운스 타임아웃을 구성할 수 있습니다:

```js
form.setValidationTimeout(3000);
```



검증 요청이 진행 중일 때, 폼의 `validating` 속성은 `true`가 됩니다:

```html
<template x-if="form.validating">
    <div>Validating...</div>
</template>
```



검증 요청이나 양식 제출 중 반환된 모든 검증 오류는 자동으로 양식의 `errors` 객체에 채워집니다:

```html
<template x-if="form.invalid('email')">
    <div x-text="form.errors.email"></div>
</template>
```



양식의 `hasErrors` 속성을 사용하여 양식에 오류가 있는지 확인할 수 있습니다:

```html
<template x-if="form.hasErrors">
    <div><!-- ... --></div>
</template>
```



입력을 폼의 `valid` 및 `invalid` 함수에 각각 입력 이름을 전달하여 입력이 유효성 검사를 통과했는지 또는 실패했는지 확인할 수도 있습니다:

```html
<template x-if="form.valid('email')">
    <span>✅</span>
</template>

<template x-if="form.invalid('email')">
    <span>❌</span>
</template>
```



> [!WARNING]
> 폼 입력은 변경되고 검증 응답이 수신된 후에만 유효 또는 무효로 표시됩니다.

보시다시피, 입력의 `change` 이벤트에 연결하여 사용자가 입력과 상호작용할 때 개별 입력을 검증할 수 있습니다. 그러나 사용자가 아직 상호작용하지 않은 입력을 검증해야 할 수도 있습니다. 이는 사용자가 다음 단계로 이동하기 전에 상호작용 여부와 관계없이 모든 표시된 입력을 검증하려고 할 때 '마법사(wizard)'를 만들 때 흔히 발생합니다.

Precognition에서 이를 수행하려면 `validate` 메서드를 호출하고 검증하려는 필드 이름을 `only` 구성 키에 전달해야 합니다. 검증 결과는 `onSuccess` 또는 `onValidationError` 콜백으로 처리할 수 있습니다:

```html
<button
    type="button"
    @click="form.validate({
        only: ['name', 'email', 'phone'],
        onSuccess: (response) => nextStep(),
        onValidationError: (response) => /* ... */,
    })"
>Next Step</button>
```



폼 제출 요청이 진행 중인지 여부는 폼의 `processing` 속성을 검사하여 확인할 수 있습니다:

```html
<button :disabled="form.processing">
    Submit
</button>
```



<a name="repopulating-old-form-data"></a>
#### 이전 폼 데이터 재채우기

위에서 논의한 사용자 생성 예제에서, 우리는 Precognition을 사용하여 실시간 검증을 수행하고 있습니다; 그러나, 폼 제출을 위해 전통적인 서버 측 폼 제출을 수행하고 있습니다. 따라서, 서버 측 폼 제출에서 반환된 모든 "이전" 입력과 검증 오류로 폼이 채워져야 합니다:

```html
<form x-data="{
    form: $form('post', '/register', {
        name: '{{ old('name') }}',
        email: '{{ old('email') }}',
    }).setErrors({{ Js::from($errors->messages()) }}),
}">
```



또는 XHR을 통해 양식을 제출하고 싶다면, 양식의 `submit` 함수를 사용할 수 있으며, 이 함수는 Axios 요청 프라미스를 반환합니다:

```html
<form
    x-data="{
        form: $form('post', '/register', {
            name: '',
            email: '',
        }),
        submit() {
            this.form.submit()
                .then(response => {
                    this.form.reset();

                    alert('User created.')
                })
                .catch(error => {
                    alert('An error occurred.');
                });
        },
    }"
    @submit.prevent="submit"
>
```



<a name="configuring-axios"></a>
### Axios 구성

Precognition 검증 라이브러리는 [Axios](https://github.com/axios/axios) HTTP 클라이언트를 사용하여 애플리케이션의 백엔드로 요청을 보냅니다. 편의를 위해, 필요에 따라 Axios 인스턴스를 애플리케이션에 맞게 사용자 정의할 수 있습니다. 예를 들어, `laravel-precognition-vue` 라이브러리를 사용할 때, 애플리케이션의 `resources/js/app.js` 파일에서 각 나가는 요청에 추가 요청 헤더를 추가할 수 있습니다:

```js
import { client } from 'laravel-precognition-vue';

client.axios().defaults.headers.common['Authorization'] = authToken;
```



또는 이미 애플리케이션용으로 구성된 Axios 인스턴스가 있는 경우, 대신 그 인스턴스를 사용하도록 Precognition에 지시할 수 있습니다:

```js
import Axios from 'axios';
import { client } from 'laravel-precognition-vue';

window.axios = Axios.create()
window.axios.defaults.headers.common['Authorization'] = authToken;

client.use(window.axios)
```



<a name="validating-arrays"></a>
## 배열 검증

배열이나 중첩된 객체 내의 필드를 검증할 때 와일드카드를 사용할 수 있습니다. 각 `*`는 단일 경로 세그먼트와 일치합니다:

```js
// Validate email for all users in an array...
form.validate('users.*.email');

// Validate all fields in a profile object...
form.validate('profile.*');

// Validate all fields for all users...
form.validate('users.*.*');
```



<a name="customizing-validation-rules"></a>
## 검증 규칙 사용자 정의

사전 인지 요청 중 실행되는 검증 규칙은 요청의 `isPrecognitive` 메서드를 사용하여 사용자 정의할 수 있습니다.

예를 들어, 사용자 생성 양식에서 비밀번호가 최종 양식 제출 시에만 "유출되지 않은(uncompromised)" 상태인지 검증하고 싶을 수 있습니다. 사전 인지 검증 요청에서는 단순히 비밀번호가 필수이고 최소 8자 이상인지 검증하면 됩니다. `isPrecognitive` 메서드를 사용하여 양식 요청에서 정의된 규칙을 사용자 정의할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class StoreUserRequest extends FormRequest
{
    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    protected function rules()
    {
        return [
            'password' => [
                'required',
                $this->isPrecognitive()
                    ? Password::min(8)
                    : Password::min(8)->uncompromised(),
            ],
            // ...
        ];
    }
}
```



<a name="handling-file-uploads"></a>
## 파일 업로드 처리

기본적으로, Laravel Precognition은 예측(validation) 요청 중에 파일을 업로드하거나 검증하지 않습니다. 이는 큰 파일이 불필요하게 여러 번 업로드되지 않도록 보장합니다.

이 동작 때문에, 애플리케이션이 [해당 폼 요청의 검증 규칙을 사용자 정의하도록](#customizing-validation-rules) 하여 필드는 전체 폼 제출에만 필요하도록 지정해야 합니다:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array
 */
protected function rules()
{
    return [
        'avatar' => [
            ...$this->isPrecognitive() ? [] : ['required'],
            'image',
            'mimes:jpg,png',
            'dimensions:ratio=3/2',
        ],
        // ...
    ];
}
```



모든 검증 요청에 파일을 포함하고 싶다면, 클라이언트 측 양식 인스턴스에서 `validateFiles` 함수를 호출할 수 있습니다:

```js
form.validateFiles();
```



<a name="managing-side-effects"></a>
## 부작용 관리

경로에 `HandlePrecognitiveRequests` 미들웨어를 추가할 때, 예지적 요청 동안 건너뛰어야 할 _다른_ 미들웨어의 부작용이 있는지 고려해야 합니다.

예를 들어, 각 사용자가 애플리케이션과 가진 총 "상호작용" 수를 증가시키는 미들웨어가 있을 수 있지만, 예지적 요청을 상호작용으로 간주하고 싶지 않을 수 있습니다. 이를 달성하기 위해, 상호작용 수를 증가시키기 전에 요청의 `isPrecognitive` 메서드를 확인할 수 있습니다:

```php
<?php

namespace App\Http\Middleware;

use App\Facades\Interaction;
use Closure;
use Illuminate\Http\Request;

class InteractionMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next): mixed
    {
        if (! $request->isPrecognitive()) {
            Interaction::incrementFor($request->user());
        }

        return $next($request);
    }
}
```



<a name="testing"></a>
## 테스트

테스트에서 선견지명 요청을 하고자 하는 경우, Laravel의 `TestCase`는 `withPrecognition` 도우미를 포함하고 있으며, 이는 `Precognition` 요청 헤더를 추가합니다.

또한, 선견지명 요청이 성공했는지(예: 검증 오류가 반환되지 않았는지) 확인하고자 하는 경우, 응답에서 `assertSuccessfulPrecognition` 메서드를 사용할 수 있습니다:```php tab=Pest
it('validates registration form with precognition', function () {
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();

    expect(User::count())->toBe(0);
});
```

```php tab=PHPUnit
public function test_it_validates_registration_form_with_precognition()
{
    $response = $this->withPrecognition()
        ->post('/register', [
            'name' => 'Taylor Otwell',
        ]);

    $response->assertSuccessfulPrecognition();
    $this->assertSame(0, User::count());
}
```
{% endraw %}
