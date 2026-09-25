---
layout: docs
title: "Validation"
---

{% raw %}
# Validation

- [Introduction](#introduction)
- [Validation Quickstart](#validation-quickstart)
    - [Defining the Routes](#quick-defining-the-routes)
    - [Creating the Controller](#quick-creating-the-controller)
    - [Writing the Validation Logic](#quick-writing-the-validation-logic)
    - [Displaying the Validation Errors](#quick-displaying-the-validation-errors)
    - [Repopulating Forms](#repopulating-forms)
    - [A Note on Optional Fields](#a-note-on-optional-fields)
    - [Validation Error Response Format](#validation-error-response-format)
- [Form Request Validation](#form-request-validation)
    - [Creating Form Requests](#creating-form-requests)
    - [Authorizing Form Requests](#authorizing-form-requests)
    - [Customizing the Error Messages](#customizing-the-error-messages)
    - [Preparing Input for Validation](#preparing-input-for-validation)
- [Manually Creating Validators](#manually-creating-validators)
    - [Automatic Redirection](#automatic-redirection)
    - [Named Error Bags](#named-error-bags)
    - [Customizing the Error Messages](#manual-customizing-the-error-messages)
    - [Performing Additional Validation](#performing-additional-validation)
- [Working With Validated Input](#working-with-validated-input)
- [Working With Error Messages](#working-with-error-messages)
    - [Specifying Custom Messages in Language Files](#specifying-custom-messages-in-language-files)
    - [Specifying Attributes in Language Files](#specifying-attribute-in-language-files)
    - [Specifying Values in Language Files](#specifying-values-in-language-files)
- [Available Validation Rules](#available-validation-rules)
- [Conditionally Adding Rules](#conditionally-adding-rules)
- [Validating Arrays](#validating-arrays)
    - [Validating Nested Array Input](#validating-nested-array-input)
    - [Error Message Indexes and Positions](#error-message-indexes-and-positions)
- [Validating Files](#validating-files)
- [Validating Passwords](#validating-passwords)
- [Custom Validation Rules](#custom-validation-rules)
    - [Using Rule Objects](#using-rule-objects)
    - [Using Closures](#using-closures)
    - [Implicit Rules](#implicit-rules)

<a name="introduction"></a>
## Introduction



Laravel provides several different approaches to validate your application's incoming data. It is most common to use the `validate` method available on all incoming HTTP requests. However, we will discuss other approaches to validation as well.

Laravel includes a wide variety of convenient validation rules that you may apply to data, even providing the ability to validate if values are unique in a given database table. We'll cover each of these validation rules in detail so that you are familiar with all of Laravel's validation features.

<a name="validation-quickstart"></a>
## Validation Quickstart

To learn about Laravel's powerful validation features, let's look at a complete example of validating a form and displaying the error messages back to the user. By reading this high-level overview, you'll be able to gain a good general understanding of how to validate incoming request data using Laravel:

<a name="quick-defining-the-routes"></a>
### Defining the Routes

First, let's assume we have the following routes defined in our `routes/web.php` file:

```php
use App\Http\Controllers\PostController;

Route::get('/post/create', [PostController::class, 'create']);
Route::post('/post', [PostController::class, 'store']);
```



`GET` 경로는 사용자가 새 블로그 게시물을 작성할 수 있는 폼을 표시하고, `POST` 경로는 새 블로그 게시물을 데이터베이스에 저장합니다.

<a name="quick-creating-the-controller"></a>
### 컨트롤러 생성하기

다음으로, 이러한 경로로 들어오는 요청을 처리하는 간단한 컨트롤러를 살펴보겠습니다. 지금은 `store` 메서드는 비워두겠습니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class PostController extends Controller
{
    /**
     * Show the form to create a new blog post.
     */
    public function create(): View
    {
        return view('post.create');
    }

    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        // Validate and store the blog post...

        $post = /** ... */

        return to_route('post.show', ['post' => $post->id]);
    }
}
```



<a name="quick-writing-the-validation-logic"></a>
### 유효성 검사 로직 작성

이제 새로운 블로그 게시물을 검증하는 로직으로 `store` 메서드를 채울 준비가 되었습니다. 이를 위해 `Illuminate\Http\Request` 객체가 제공하는 `validate` 메서드를 사용할 것입니다. 유효성 검사 규칙을 통과하면 코드가 정상적으로 계속 실행되며, 유효성 검사가 실패하면 `Illuminate\Validation\ValidationException` 예외가 발생하고 적절한 오류 응답이 자동으로 사용자에게 반환됩니다.

전통적인 HTTP 요청 중 유효성 검사가 실패하면 이전 URL로 리디렉션 응답이 생성됩니다. 수신된 요청이 XHR 요청이라면 [유효성 검사 오류 메시지를 포함한 JSON 응답](#validation-error-response-format)이 반환됩니다.

`validate` 메서드를 더 잘 이해하기 위해 `store` 메서드로 다시 돌아가 봅시다:

```php
/**
 * Store a new blog post.
 */
public function store(Request $request): RedirectResponse
{
    $validated = $request->validate([
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ]);

    // The blog post is valid...

    return redirect('/posts');
}
```



보시다시피, 검증 규칙은 `validate` 메서드로 전달됩니다. 걱정하지 마세요 - 사용 가능한 모든 검증 규칙은 [문서화](#available-validation-rules)되어 있습니다. 다시 말하지만, 검증에 실패하면 적절한 응답이 자동으로 생성됩니다. 검증에 성공하면, 우리 컨트롤러는 정상적으로 실행을 계속합니다.

또한, `validateWithBag` 메서드를 사용하여 요청을 검증하고 모든 오류 메시지를 [명명된 오류 가방](#named-error-bags) 안에 저장할 수 있습니다:

```php
$validated = $request->validateWithBag('post', [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```



<a name="stopping-on-first-validation-failure"></a>
#### 첫 번째 검증 실패 시 중단

때때로 첫 번째 검증 실패 후에 속성에 대한 검증 규칙 실행을 중지하고 싶을 수 있습니다. 그렇게 하려면 해당 속성에 `bail` 규칙을 할당하십시오:

```php
$request->validate([
    'title' => ['bail', 'required', 'unique:posts', 'max:255'],
    'body' => ['required'],
]);
```



이 예제에서, `title` 속성의 `unique` 규칙이 실패하면, `max` 규칙은 확인되지 않습니다. 규칙은 할당된 순서대로 검증됩니다.

<a name="a-note-on-nested-attributes"></a>
#### 중첩 속성에 대한 참고 사항

들어오는 HTTP 요청에 "중첩된" 필드 데이터가 포함되어 있는 경우, 이러한 필드를 검증 규칙에서 "점" 문법을 사용하여 지정할 수 있습니다:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'author.name' => ['required'],
    'author.description' => ['required'],
]);
```



반면에, 필드 이름에 실제로 점(.)이 포함되어 있는 경우, 백슬래시를 사용하여 점을 이스케이프함으로써 이것이 '점(dot)' 구문으로 해석되는 것을 명시적으로 방지할 수 있습니다:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'v1\.0' => ['required'],
]);
```



<a name="quick-displaying-the-validation-errors"></a>
### Displaying the Validation Errors

So, what if the incoming request fields do not pass the given validation rules? As mentioned previously, Laravel will automatically redirect the user back to their previous location. In addition, all of the validation errors and [request input](/docs/{{version}}/requests#retrieving-old-input) will automatically be [flashed to the session](/docs/{{version}}/session#flash-data).

An `$errors` variable is shared with all of your application's views by the `Illuminate\View\Middleware\ShareErrorsFromSession` middleware, which is provided by the `web` middleware group. When this middleware is applied an `$errors` variable will always be available in your views, allowing you to conveniently assume the `$errors` variable is always defined and can be safely used. The `$errors` variable will be an instance of `Illuminate\Support\MessageBag`. For more information on working with this object, [check out its documentation](#working-with-error-messages).

So, in our example, the user will be redirected to our controller's `create` method when validation fails, allowing us to display the error messages in the view:

```blade
<!-- /resources/views/post/create.blade.php -->

<h1>Create Post</h1>

@if ($errors->any())
    <div class="alert alert-danger">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif

<!-- Create Post Form -->
```



<a name="quick-customizing-the-error-messages"></a>
#### Customizing the Error Messages

Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command.

Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application.

In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/{{version}}/localization).

> [!WARNING]
> By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

<a name="quick-xhr-requests-and-validation"></a>
#### XHR Requests and Validation

In this example, we used a traditional form to send data to the application. However, many applications receive XHR requests from a JavaScript powered frontend. When using the `validate` method during an XHR request, Laravel will not generate a redirect response. Instead, Laravel generates a [JSON response containing all of the validation errors](#validation-error-response-format). This JSON response will be sent with a 422 HTTP status code.

<a name="the-at-error-directive"></a>
#### The `@error` Directive

You may use the `@error` [Blade](/docs/{{version}}/blade) directive to quickly determine if validation error messages exist for a given attribute. Within an `@error` directive, you may echo the `$message` variable to display the error message:

```blade
<!-- /resources/views/post/create.blade.php -->

<label for="title">Post Title</label>

<input
    id="title"
    type="text"
    name="title"
    class="@error('title') is-invalid @enderror"
/>

@error('title')
    <div class="alert alert-danger">{{ $message }}</div>
@enderror
```



만약 [명명된 오류 가방](#named-error-bags)을 사용하고 있다면, 오류 가방의 이름을 `@error` 지시문에 두 번째 인수로 전달할 수 있습니다:

```blade
<input ... class="@error('title', 'post') is-invalid @enderror">
```



<a name="repopulating-forms"></a>
### 폼 다시 채우기

Laravel이 유효성 검사 오류로 인해 리디렉션 응답을 생성하면, 프레임워크는 자동으로 [모든 요청 입력을 세션에 플래시](/docs/{{version}}/session#flash-data)합니다. 이는 사용자가 제출하려고 했던 폼을 다음 요청에서 쉽게 액세스하고 다시 채울 수 있도록 하기 위해 수행됩니다.

이전 요청에서 플래시된 입력을 가져오려면 `Illuminate\Http\Request`의 인스턴스에서 `old` 메서드를 호출하십시오. `old` 메서드는 이전에 플래시된 입력 데이터를 [세션](/docs/{{version}}/session)에서 가져옵니다:

```php
$title = $request->old('title');
```



Laravel은 또한 전역 `old` 헬퍼를 제공합니다. [Blade 템플릿](/docs/{{version}}/blade) 내에서 이전 입력을 표시하는 경우, 폼을 다시 채우기 위해 `old` 헬퍼를 사용하는 것이 더 편리합니다. 주어진 필드에 대한 이전 입력이 없으면 `null`가 반환됩니다:

```blade
<input type="text" name="title" value="{{ old('title') }}">
```



<a name="a-note-on-optional-fields"></a>
### 선택적 필드에 대한 참고

기본적으로 Laravel은 `TrimStrings` 및 `ConvertEmptyStringsToNull` 미들웨어를 애플리케이션의 전역 미들웨어 스택에 포함합니다. 이 때문에, 유효성 검사기가 `null` 값을 잘못된 것으로 간주하지 않기를 원한다면 "선택적" 요청 필드를 `nullable`로 표시해야 하는 경우가 자주 있습니다. 예를 들어:

```php
$request->validate([
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
    'publish_at' => ['nullable', 'date'],
]);
```



이 예제에서는 `publish_at` 필드가 `null` 또는 유효한 날짜 표현일 수 있음을 지정하고 있습니다. `nullable` 수정자가 규칙 정의에 추가되지 않으면, 검증기는 `null`를 유효하지 않은 날짜로 간주합니다.

<a name="validation-error-response-format"></a>
### 검증 오류 응답 형식

애플리케이션에서 `Illuminate\Validation\ValidationException` 예외를 발생시키고 들어오는 HTTP 요청이 JSON 응답을 기대하는 경우, Laravel은 자동으로 오류 메시지를 형식화하여 `422 Unprocessable Entity` HTTP 응답을 반환합니다.

아래에서는 검증 오류에 대한 JSON 응답 형식의 예제를 확인할 수 있습니다. 중첩된 오류 키는 "dot" 표기법 형식으로 평탄화된다는 점에 유의하십시오:

```json
{
    "message": "The team name must be a string. (and 4 more errors)",
    "errors": {
        "team_name": [
            "The team name must be a string.",
            "The team name must be at least 1 characters."
        ],
        "authorization.role": [
            "The selected authorization.role is invalid."
        ],
        "users.0.email": [
            "The users.0.email field is required."
        ],
        "users.2.email": [
            "The users.2.email must be a valid email address."
        ]
    }
}
```



<a name="form-request-validation"></a>
## 폼 요청 검증

<a name="creating-form-requests"></a>
### 폼 요청 생성

더 복잡한 검증 시나리오의 경우, "폼 요청"을 생성하고자 할 수 있습니다. 폼 요청은 자체 검증 및 인가 로직을 캡슐화하는 커스텀 요청 클래스입니다. 폼 요청 클래스를 생성하려면, `make:request` Artisan CLI 명령어를 사용할 수 있습니다:

```shell
php artisan make:request StorePostRequest
```



생성된 폼 요청 클래스는 `app/Http/Requests` 디렉토리에 배치됩니다. 이 디렉토리가 존재하지 않으면 `make:request` 명령을 실행할 때 생성됩니다. Laravel에서 생성된 각 폼 요청에는 두 가지 메서드가 있습니다: `authorize`와 `rules`.

예상할 수 있듯이, `authorize` 메서드는 현재 인증된 사용자가 요청으로 표현된 작업을 수행할 수 있는지 여부를 결정하는 역할을 하며, `rules` 메서드는 요청 데이터에 적용되어야 하는 검증 규칙을 반환합니다:

```php
/**
 * Get the validation rules that apply to the request.
 *
 * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
 */
public function rules(): array
{
    return [
        'title' => ['required', 'unique:posts', 'max:255'],
        'body' => ['required'],
    ];
}
```



> [!NOTE]
> `rules` 메서드의 시그니처 내에서 필요한 종속성을 타입 힌트로 지정할 수 있습니다. 이는 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 해결됩니다.

그렇다면 유효성 검사 규칙은 어떻게 평가될까요? 컨트롤러 메서드에서 요청을 타입 힌트로 지정하기만 하면 됩니다. 들어오는 폼 요청은 컨트롤러 메서드가 호출되기 전에 검증되므로, 컨트롤러에 불필요하게 유효성 검사 로직을 추가할 필요가 없습니다:

```php
/**
 * Store a new blog post.
 */
public function store(StorePostRequest $request): RedirectResponse
{
    // The incoming request is valid...

    // Retrieve the validated input data...
    $validated = $request->validated();

    // Retrieve a portion of the validated input data...
    $validated = $request->safe()->only(['name', 'email']);
    $validated = $request->safe()->except(['name', 'email']);

    // Store the blog post...

    return redirect('/posts');
}
```



검증에 실패하면 사용자를 이전 위치로 되돌리기 위한 리디렉션 응답이 생성됩니다. 오류는 세션에 저장되어 표시할 수 있습니다. 요청이 XHR 요청인 경우, 검증 오류의 [JSON 표현](#validation-error-response-format)이 포함된 상태 코드 422의 HTTP 응답이 사용자에게 반환됩니다.

> [!NOTE]
> 실시간 폼 요청 검증을 Inertia 기반 Laravel 프론트엔드에 추가해야 하나요? [Laravel Precognition](/docs/{{version}}/precognition)을 확인해보세요.

<a name="performing-additional-validation-on-form-requests"></a>
#### 추가 검증 수행

때때로 초기 검증이 완료된 후 추가 검증을 수행해야 할 필요가 있습니다. 이는 폼 요청의 `after` 메서드를 사용하여 수행할 수 있습니다.

`after` 메서드는 검증이 완료된 후 호출될 콜러블 또는 클로저의 배열을 반환해야 합니다. 제공된 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아 필요한 경우 추가 오류 메시지를 발생시킬 수 있습니다:

```php
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        function (Validator $validator) {
            if ($this->somethingElseIsInvalid()) {
                $validator->errors()->add(
                    'field',
                    'Something is wrong with this field!'
                );
            }
        }
    ];
}
```



앞서 언급한 바와 같이, `after` 메서드가 반환하는 배열에는 호출 가능한 클래스도 포함될 수 있습니다. 이러한 클래스들의 `__invoke` 메서드는 `Illuminate\Validation\Validator` 인스턴스를 받게 됩니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;
use Illuminate\Validation\Validator;

/**
 * Get the "after" validation callables for the request.
 */
public function after(): array
{
    return [
        new ValidateUserStatus,
        new ValidateShippingTime,
        function (Validator $validator) {
            //
        }
    ];
}
```



<a name="request-stopping-on-first-validation-rule-failure"></a>
#### 첫 번째 검증 실패 시 중지

요청 클래스에 `StopOnFirstFailure` 속성을 추가하면, 단일 검증 실패가 발생하면 검증자가 모든 속성의 검증을 중지해야 한다는 것을 알릴 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\StopOnFirstFailure;
use Illuminate\Foundation\Http\FormRequest;

#[StopOnFirstFailure]
class StorePostRequest extends FormRequest
{
    // ...
}
```



<a name="request-failing-on-unknown-fields"></a>
#### 알 수 없는 필드에서 실패하기

요청 클래스에 `FailOnUnknownFields` 속성을 추가하면, Laravel이 요청의 검증 규칙에 정의되지 않은 모든 들어오는 필드를 거부하도록 지시할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\FailOnUnknownFields;
use Illuminate\Foundation\Http\FormRequest;

#[FailOnUnknownFields]
class StorePostRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'title' => ['required', 'string'],
            'body' => ['required', 'string'],
        ];
    }
}
```



또한 `AppServiceProvider`에서 오는 모든 양식 요청에 대해 이 동작을 전역적으로 활성화할 수 있습니다:

```php
use Illuminate\Foundation\Http\FormRequest;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    FormRequest::failOnUnknownFields();
}
```



필요한 경우, 속성에 `false`를 전달하여 특정 요청에 대해 이 동작을 비활성화할 수 있습니다:

```php
#[FailOnUnknownFields(false)]
class PublicWebhookRequest extends FormRequest
{
    // ...
}
```



알 수 없는 필드를 거부하면 예상치 못한 입력 키가 애플리케이션 내부로 흘러들어가는 것을 방지하여 매스 어사인먼트 스타일 문제로부터 추가적인 보호를 제공할 수 있습니다. 그러나 여전히 모델의 `$fillable` / `$guarded` 속성을 구성하고 신뢰할 수 있고 검증된 입력만을 저장해야 합니다.

<a name="customizing-the-redirect-location"></a>
#### 리디렉션 위치 사용자 정의

폼 요청 검증이 실패하면 사용자를 이전 위치로 되돌리기 위해 리디렉션 응답이 생성됩니다. 그러나 이 동작은 자유롭게 사용자 정의할 수 있습니다. 이를 위해 폼 요청에서 `RedirectTo` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectTo;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectTo('/dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```



또는 사용자를 이름이 지정된 라우트로 리디렉션하려면 대신 `RedirectToRoute` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\RedirectToRoute;
use Illuminate\Foundation\Http\FormRequest;

#[RedirectToRoute('dashboard')]
class StorePostRequest extends FormRequest
{
    // ...
}
```



<a name="customizing-the-error-bag"></a>
#### 에러 백 사용자 정의

폼 요청 검증이 실패하면, 에러가 `default` 에러 백에 플래시됩니다. 다른 [명명된 에러 백](#named-error-bags)에 에러를 저장해야 하는 경우, 폼 요청에서 `ErrorBag` 속성을 사용할 수 있습니다:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\Attributes\ErrorBag;
use Illuminate\Foundation\Http\FormRequest;

#[ErrorBag('login')]
class LoginRequest extends FormRequest
{
    // ...
}
```



<a name="authorizing-form-requests"></a>
### 양식 요청 승인

폼 요청 클래스에는 `authorize` 메서드도 포함되어 있습니다. 이 메서드 내에서 인증된 사용자가 실제로 주어진 리소스를 업데이트할 권한이 있는지 확인할 수 있습니다. 예를 들어, 사용자가 실제로 업데이트하려고 하는 블로그 댓글을 소유하고 있는지 확인할 수 있습니다. 가장 가능성이 높은 것은 이 메서드 내에서 [권한 게이트 및 정책](/docs/{{version}}/authorization)과 상호작용하게 될 것입니다:

```php
use App\Models\Comment;

/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    $comment = Comment::find($this->route('comment'));

    return $comment && $this->user()->can('update', $comment);
}
```



모든 폼 요청이 기본 Laravel 요청 클래스를 확장하므로, 현재 인증된 사용자에 접근하기 위해 `user` 메서드를 사용할 수 있습니다. 또한 위 예제에서 `route` 메서드를 호출한 것을 참고하십시오. 이 메서드는 호출되는 라우트에 정의된 URI 매개변수에 접근할 수 있게 해주며, 아래 예제의 `{comment}` 매개변수와 같습니다:

```php
Route::post('/comment/{comment}');
```



따라서 애플리케이션이 [라우트 모델 바인딩](/docs/{{version}}/routing#route-model-binding)을 활용하고 있다면, 요청의 속성으로 해결된 모델에 접근함으로써 코드를 훨씬 더 간결하게 만들 수 있습니다:

```php
return $this->user()->can('update', $this->comment);
```



`authorize` 메서드가 `false`를 반환하면, HTTP 403 상태 코드가 포함된 응답이 자동으로 반환되며 컨트롤러 메서드는 실행되지 않습니다.

요청에 대한 인증 로직을 애플리케이션의 다른 부분에서 처리하려는 경우, `authorize` 메서드를 완전히 제거하거나 단순히 `true`를 반환할 수 있습니다:

```php
/**
 * Determine if the user is authorized to make this request.
 */
public function authorize(): bool
{
    return true;
}
```



> [!NOTE]
> `authorize` 메서드의 시그니처 내에서 필요한 모든 의존성을 타입 힌트로 지정할 수 있습니다. 이들은 Laravel [서비스 컨테이너](/docs/{{version}}/container)를 통해 자동으로 해결됩니다.

<a name="customizing-the-error-messages"></a>
### 오류 메시지 사용자 정의

`messages` 메서드를 재정의하여 폼 요청에서 사용되는 오류 메시지를 사용자 정의할 수 있습니다. 이 메서드는 속성 / 규칙 쌍과 해당 오류 메시지 배열을 반환해야 합니다:

```php
/**
 * Get the error messages for the defined validation rules.
 *
 * @return array<string, string>
 */
public function messages(): array
{
    return [
        'title.required' => 'A title is required',
        'body.required' => 'A message is required',
    ];
}
```



<a name="customizing-the-validation-attributes"></a>
#### 검증 속성 사용자 정의

Laravel의 내장 검증 규칙 오류 메시지 중 다수에는 `:attribute` 자리 표시자가 포함되어 있습니다. 검증 메시지의 `:attribute` 자리 표시자를 사용자 정의 속성 이름으로 바꾸고 싶다면, `attributes` 메서드를 재정의하여 사용자 정의 이름을 지정할 수 있습니다. 이 메서드는 속성 / 이름 쌍의 배열을 반환해야 합니다:

```php
/**
 * Get custom attributes for validator errors.
 *
 * @return array<string, string>
 */
public function attributes(): array
{
    return [
        'email' => 'email address',
    ];
}
```



<a name="preparing-input-for-validation"></a>
### 검증을 위한 입력 준비

검증 규칙을 적용하기 전에 요청에서 데이터를 준비하거나 정리해야 하는 경우, `prepareForValidation` 방법을 사용할 수 있습니다:

```php
use Illuminate\Support\Str;

/**
 * Prepare the data for validation.
 */
protected function prepareForValidation(): void
{
    $this->merge([
        'slug' => Str::slug($this->slug),
    ]);
}
```



마찬가지로, 검증이 완료된 후 요청 데이터를 정규화해야 하는 경우, `passedValidation` 메서드를 사용할 수 있습니다:

```php
/**
 * Handle a passed validation attempt.
 */
protected function passedValidation(): void
{
    $this->replace(['name' => 'Taylor']);
}
```



<a name="manually-creating-validators"></a>
## 검증기 수동 생성

요청에서 `validate` 방법을 사용하고 싶지 않은 경우, `Validator` [파사드](/docs/{{version}}/facades)를 사용하여 검증기 인스턴스를 수동으로 생성할 수 있습니다. 파사드의 `make` 메서드는 새로운 검증기 인스턴스를 생성합니다:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PostController extends Controller
{
    /**
     * Store a new blog post.
     */
    public function store(Request $request): RedirectResponse
    {
        $validator = Validator::make($request->all(), [
            'title' => ['required', 'unique:posts', 'max:255'],
            'body' => ['required'],
        ]);

        if ($validator->fails()) {
            return redirect('/post/create')
                ->withErrors($validator)
                ->withInput();
        }

        // Retrieve the validated input...
        $validated = $validator->validated();

        // Retrieve a portion of the validated input...
        $validated = $validator->safe()->only(['name', 'email']);
        $validated = $validator->safe()->except(['name', 'email']);

        // Store the blog post...

        return redirect('/posts');
    }
}
```



`make` 메서드에 전달되는 첫 번째 인수는 검증 중인 데이터입니다. 두 번째 인수는 데이터에 적용해야 할 검증 규칙의 배열입니다.

요청 검증이 실패했는지 여부를 판단한 후에는 `withErrors` 메서드를 사용하여 오류 메시지를 세션에 플래시할 수 있습니다. 이 메서드를 사용할 때, `$errors` 변수는 리디렉션 후에 자동으로 뷰와 공유되어 사용자가 쉽게 다시 표시할 수 있습니다. `withErrors` 메서드는 검증기, `MessageBag` 또는 PHP `array`를 받아들입니다.

#### 첫 번째 검증 실패에서 멈추기

`stopOnFirstFailure` 메서드는 단일 검증 실패가 발생하면 모든 속성 검증을 중지해야 한다고 검증기에게 알립니다:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```



<a name="automatic-redirection"></a>
### 자동 리디렉션

자동 리디렉션 기능을 제공하는 HTTP 요청의 `validate` 메서드를 활용하면서도 수동으로 검증기 인스턴스를 만들고 싶다면, 기존 검증기 인스턴스에서 `validate` 메서드를 호출할 수 있습니다. 검증이 실패하면 사용자는 자동으로 리디렉션되거나, XHR 요청의 경우 [JSON 응답이 반환됩니다](#validation-error-response-format):

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validate();
```



검증에 실패하면 오류 메시지를 [명명된 오류 가방](#named-error-bags)에 저장하기 위해 `validateWithBag` 방법을 사용할 수 있습니다:

```php
Validator::make($request->all(), [
    'title' => ['required', 'unique:posts', 'max:255'],
    'body' => ['required'],
])->validateWithBag('post');
```



<a name="named-error-bags"></a>
### 명명된 오류 가방

한 페이지에 여러 폼이 있는 경우, 유효성 검사 오류를 포함하는 `MessageBag`에 이름을 지정하여 특정 폼의 오류 메시지를 가져올 수 있습니다. 이를 달성하려면 `withErrors`에 두 번째 인수로 이름을 전달하십시오:

```php
return redirect('/register')->withErrors($validator, 'login');
```



그런 다음 `$errors` 변수에서 명명된 `MessageBag` 인스턴스에 접근할 수 있습니다:

```blade
{{ $errors->login->first('email') }}
```



<a name="manual-customizing-the-error-messages"></a>
### 오류 메시지 사용자 정의

필요한 경우, 검증기 인스턴스가 Laravel에서 제공하는 기본 오류 메시지 대신 사용할 사용자 정의 오류 메시지를 제공할 수 있습니다. 사용자 정의 메시지를 지정하는 몇 가지 방법이 있습니다. 먼저, 사용자 정의 메시지를 `Validator::make` 메서드의 세 번째 인수로 전달할 수 있습니다:

```php
$validator = Validator::make($input, $rules, $messages = [
    'required' => 'The :attribute field is required.',
]);
```



이 예제에서 `:attribute` 자리표시는 검증 중인 필드의 실제 이름으로 대체됩니다. 검증 메시지에서 다른 자리표시자를 사용할 수도 있습니다. 예를 들어:

```php
$messages = [
    'same' => 'The :attribute and :other must match.',
    'size' => 'The :attribute must be exactly :size.',
    'between' => 'The :attribute value :input is not between :min - :max.',
    'in' => 'The :attribute must be one of the following types: :values',
];
```



<a name="specifying-a-custom-message-for-a-given-attribute"></a>
#### 특정 속성에 대한 사용자 정의 메시지 지정

때때로 특정 속성에 대해서만 사용자 정의 오류 메시지를 지정하고 싶을 수 있습니다. 이 경우 "점(dot)" 표기법을 사용할 수 있습니다. 먼저 속성의 이름을 지정하고, 그 다음에 규칙을 지정합니다:

```php
$messages = [
    'email.required' => 'We need to know your email address!',
];
```



<a name="specifying-custom-attribute-values"></a>
#### 사용자 정의 속성 값 지정

Laravel의 내장 오류 메시지 중 많은 수는 `:attribute` 자리 표시자를 포함하며, 이는 검증 중인 필드 또는 속성의 이름으로 대체됩니다. 특정 필드에 대해 이러한 자리 표시자를 대체하는 데 사용되는 값을 사용자 정의하려면 `Validator::make` 메서드의 네 번째 인수로 사용자 정의 속성 배열을 전달할 수 있습니다:

```php
$validator = Validator::make($input, $rules, $messages, [
    'email' => 'email address',
]);
```



<a name="performing-additional-validation"></a>
### 추가 검증 수행

때때로 초기 검증이 완료된 후 추가 검증을 수행해야 할 때가 있습니다. 이는 검증자의 `after` 메서드를 사용하여 수행할 수 있습니다. `after` 메서드는 검증이 완료된 후 호출될 클로저 또는 콜러블 배열을 허용합니다. 주어진 콜러블은 `Illuminate\Validation\Validator` 인스턴스를 받아 필요시 추가 오류 메시지를 발생시킬 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make(/* ... */);

$validator->after(function ($validator) {
    if ($this->somethingElseIsInvalid()) {
        $validator->errors()->add(
            'field', 'Something is wrong with this field!'
        );
    }
});

if ($validator->fails()) {
    // ...
}
```



앞서 언급했듯이, `after` 메서드는 호출 가능한(callable) 배열도 허용하는데, 이는 '유효성 검증 후' 로직이 호출 가능한 클래스로 캡슐화되어 있고, 해당 클래스가 `__invoke` 메서드를 통해 `Illuminate\Validation\Validator` 인스턴스를 받는 경우에 특히 편리합니다:

```php
use App\Validation\ValidateShippingTime;
use App\Validation\ValidateUserStatus;

$validator->after([
    new ValidateUserStatus,
    new ValidateShippingTime,
    function ($validator) {
        // ...
    },
]);
```



<a name="working-with-validated-input"></a>
## 검증된 입력 데이터 다루기

폼 요청이나 수동으로 생성한 검증기 인스턴스를 사용하여 들어오는 요청 데이터를 검증한 후, 실제로 검증을 거친 들어오는 요청 데이터를 가져오고 싶을 수 있습니다. 이는 여러 가지 방법으로 수행할 수 있습니다. 먼저, 폼 요청이나 검증기 인스턴스에서 `validated` 메서드를 호출할 수 있습니다. 이 메서드는 검증된 데이터의 배열을 반환합니다:

```php
$validated = $request->validated();

$validated = $validator->validated();
```



또는 폼 요청(form request)이나 검증기(validator) 인스턴스에서 `safe` 메서드를 호출할 수 있습니다. 이 메서드는 `Illuminate\Support\ValidatedInput` 인스턴스를 반환합니다. 이 객체는 검증된 데이터의 일부 또는 전체 배열을 가져오기 위해 `only`, `except`, `all` 메서드를 제공합니다:

```php
$validated = $request->safe()->only(['name', 'email']);

$validated = $request->safe()->except(['name', 'email']);

$validated = $request->safe()->all();
```



또한, `Illuminate\Support\ValidatedInput` 인스턴스는 배열처럼 반복(iterate)하고 접근할 수 있습니다:

```php
// Validated data may be iterated...
foreach ($request->safe() as $key => $value) {
    // ...
}

// Validated data may be accessed as an array...
$validated = $request->safe();

$email = $validated['email'];
```



검증된 데이터에 추가 필드를 추가하고 싶다면, `merge` 메서드를 호출할 수 있습니다:

```php
$validated = $request->safe()->merge(['name' => 'Taylor Otwell']);
```



검증된 데이터를 [collection](/docs/{{version}}/collections) 인스턴스로 가져오고 싶다면, 다음 `collect` 메서드를 호출할 수 있습니다:

```php
$collection = $request->safe()->collect();
```



<a name="working-with-error-messages"></a>
## 오류 메시지 작업하기

`Validator` 인스턴스에서 `errors` 메서드를 호출한 후, 오류 메시지를 처리하기 위해 다양한 편리한 메서드를 제공하는 `Illuminate\Support\MessageBag` 인스턴스를 받게 됩니다. 모든 뷰에서 자동으로 사용 가능하게 되는 `$errors` 변수 또한 `MessageBag` 클래스의 인스턴스입니다.

<a name="retrieving-the-first-error-message-for-a-field"></a>
#### 필드의 첫 번째 오류 메시지 가져오기

주어진 필드의 첫 번째 오류 메시지를 가져오려면 `first` 메서드를 사용하세요:

```php
$errors = $validator->errors();

echo $errors->first('email');
```



<a name="retrieving-all-error-messages-for-a-field"></a>
#### 필드에 대한 모든 오류 메시지 가져오기

주어진 필드에 대한 모든 메시지 배열을 가져와야 하는 경우, `get` 메서드를 사용하세요:

```php
foreach ($errors->get('email') as $message) {
    // ...
}
```



배열 폼 필드를 검증하는 경우, `*` 문자를 사용하여 배열 요소 각각에 대한 모든 메시지를 가져올 수 있습니다:

```php
foreach ($errors->get('attachments.*') as $message) {
    // ...
}
```



<a name="retrieving-all-error-messages-for-all-fields"></a>
#### 모든 필드에 대한 모든 오류 메시지 가져오기

모든 필드에 대한 모든 메시지 배열을 가져오려면 `all` 메서드를 사용하세요:

```php
foreach ($errors->all() as $message) {
    // ...
}
```



<a name="determining-if-messages-exist-for-a-field"></a>
#### 필드에 메시지가 존재하는지 확인하기

`has` 메서드는 특정 필드에 대한 오류 메시지가 있는지 확인하는 데 사용될 수 있습니다:

```php
if ($errors->has('email')) {
    // ...
}
```



<a name="specifying-custom-messages-in-language-files"></a>
### Specifying Custom Messages in Language Files

Laravel's built-in validation rules each have an error message that is located in your application's `lang/en/validation.php` file. If your application does not have a `lang` directory, you may instruct Laravel to create it using the `lang:publish` Artisan command.

Within the `lang/en/validation.php` file, you will find a translation entry for each validation rule. You are free to change or modify these messages based on the needs of your application.

In addition, you may copy this file to another language directory to translate the messages for your application's language. To learn more about Laravel localization, check out the complete [localization documentation](/docs/{{version}}/localization).

> [!WARNING]
> By default, the Laravel application skeleton does not include the `lang` directory. If you would like to customize Laravel's language files, you may publish them via the `lang:publish` Artisan command.

<a name="custom-messages-for-specific-attributes"></a>
#### Custom Messages for Specific Attributes

You may customize the error messages used for specified attribute and rule combinations within your application's validation language files. To do so, add your message customizations to the `custom` array of your application's `lang/xx/validation.php` language file:

```php
'custom' => [
    'email' => [
        'required' => 'We need to know your email address!',
        'max' => 'Your email address is too long!'
    ],
],
```



<a name="specifying-attribute-in-language-files"></a>
### 언어 파일에서 속성 지정하기

Laravel의 내장 오류 메시지 중 많은 부분에는 `:attribute` 자리 표시자가 포함되어 있으며, 이는 검증 중인 필드나 속성의 이름으로 대체됩니다. 검증 메시지의 `:attribute` 부분을 사용자 정의 값으로 대체하고 싶다면, `lang/xx/validation.php` 언어 파일의 `attributes` 배열에 사용자 정의 속성 이름을 지정할 수 있습니다:

```php
'attributes' => [
    'email' => 'email address',
],
```



> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉터리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하려면 `lang:publish` Artisan 명령을 통해 게시할 수 있습니다.

<a name="specifying-values-in-language-files"></a>
### 언어 파일에서 값 지정하기

Laravel의 일부 내장 검증 규칙 오류 메시지에는 요청 속성의 현재 값으로 대체되는 `:value` 자리 표시자가 포함되어 있습니다. 그러나 경우에 따라 검증 메시지의 `:value` 부분을 값의 사용자 지정 표현으로 대체해야 할 수도 있습니다. 예를 들어, 다음 규칙을 고려해 보십시오. 이 규칙은 `payment_type`가 `cc` 값을 가지면 신용카드 번호가 필요하다고 지정합니다:

```php
Validator::make($request->all(), [
    'credit_card_number' => ['required_if:payment_type,cc']
]);
```



이 검증 규칙이 실패하면 다음 오류 메시지가 생성됩니다:

```text
The credit card number field is required when payment type is cc.
```



결제 유형 값으로 `cc`를 표시하는 대신, `values` 배열을 정의하여 `lang/xx/validation.php` 언어 파일에서 보다 사용자 친화적인 값 표시를 지정할 수 있습니다:

```php
'values' => [
    'payment_type' => [
        'cc' => 'credit card'
    ],
],
```



> [!WARNING]
> 기본적으로 Laravel 애플리케이션 스켈레톤에는 `lang` 디렉토리가 포함되어 있지 않습니다. Laravel의 언어 파일을 사용자 정의하고 싶다면, `lang:publish` Artisan 명령어를 통해 이를 게시할 수 있습니다.

이 값을 정의한 후, 검증 규칙은 다음과 같은 오류 메시지를 생성합니다:

```text
The credit card number field is required when payment type is credit card.
```

<a name="available-validation-rules"></a>
## Available Validation Rules

Below is a list of all available validation rules and their function:

<style>
    .collection-method-list > p {
        columns: 10.8em 3; -moz-columns: 10.8em 3; -webkit-columns: 10.8em 3;
    }

.collection-method-list a {
        display: block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
</style>

#### Booleans

<div class="collection-method-list" markdown="1">

[Accepted](#rule-accepted)
[Accepted If](#rule-accepted-if)
[Boolean](#rule-boolean)
[Declined](#rule-declined)
[Declined If](#rule-declined-if)

</div>

#### Strings

<div class="collection-method-list" markdown="1">

[Active URL](#rule-active-url)
[Alpha](#rule-alpha)
[Alpha Dash](#rule-alpha-dash)
[Alpha Numeric](#rule-alpha-num)
[Ascii](#rule-ascii)
[Confirmed](#rule-confirmed)
[Current Password](#rule-current-password)
[Different](#rule-different)
[Doesnt Start With](#rule-doesnt-start-with)
[Doesnt End With](#rule-doesnt-end-with)
[Email](#rule-email)
[Ends With](#rule-ends-with)
[Enum](#rule-enum)
[Hex Color](#rule-hex-color)
[In](#rule-in)
[IP Address](#rule-ip)
[JSON](#rule-json)
[Lowercase](#rule-lowercase)
[MAC Address](#rule-mac)
[Max](#rule-max)
[Min](#rule-min)
[Not In](#rule-not-in)
[Regular Expression](#rule-regex)
[Not Regular Expression](#rule-not-regex)
[Same](#rule-same)
[Size](#rule-size)
[Starts With](#rule-starts-with)
[String](#rule-string)
[Uppercase](#rule-uppercase)
[URL](#rule-url)
[ULID](#rule-ulid)
[UUID](#rule-uuid)

</div>

#### Numbers

<div class="collection-method-list" markdown="1">

[Between](#rule-between)
[Decimal](#rule-decimal)
[Different](#rule-different)
[Digits](#rule-digits)
[Digits Between](#rule-digits-between)
[Greater Than](#rule-gt)
[Greater Than Or Equal](#rule-gte)
[Integer](#rule-integer)
[Less Than](#rule-lt)
[Less Than Or Equal](#rule-lte)
[Max](#rule-max)
[Max Digits](#rule-max-digits)
[Min](#rule-min)
[Min Digits](#rule-min-digits)
[Multiple Of](#rule-multiple-of)
[Numeric](#rule-numeric)
[Same](#rule-same)
[Size](#rule-size)

</div>

#### Arrays

<div class="collection-method-list" markdown="1">

[Array](#rule-array)
[Array Keys](#rule-array-keys)
[Between](#rule-between)
[Contains](#rule-contains)
[Doesnt Contain](#rule-doesnt-contain)
[Distinct](#rule-distinct)
[In Array](#rule-in-array)
[In Array Keys](#rule-in-array-keys)
[List](#rule-list)
[Max](#rule-max)
[Min](#rule-min)
[Size](#rule-size)

</div>

#### Dates

<div class="collection-method-list" markdown="1">

[After](#rule-after)
[After Or Equal](#rule-after-or-equal)
[Before](#rule-before)
[Before Or Equal](#rule-before-or-equal)
[Date](#rule-date)
[Date Equals](#rule-date-equals)
[Date Format](#rule-date-format)
[Different](#rule-different)
[Timezone](#rule-timezone)

</div>

#### Files

<div class="collection-method-list" markdown="1">

[Between](#rule-between)
[Dimensions](#rule-dimensions)
[Encoding](#rule-encoding)
[Extensions](#rule-extensions)
[File](#rule-file)
[Image](#rule-image)
[Max](#rule-max)
[Min](#rule-min)
[MIME Types](#rule-mimetypes)
[MIME Type By File Extension](#rule-mimes)
[Size](#rule-size)

</div>

#### Database

<div class="collection-method-list" markdown="1">

[Exists](#rule-exists)
[Unique](#rule-unique)

</div>

#### Utilities

<div class="collection-method-list" markdown="1">

[Any Of](#rule-anyof)
[Bail](#rule-bail)
[Exclude](#rule-exclude)
[Exclude If](#rule-exclude-if)
[Exclude Unless](#rule-exclude-unless)
[Exclude With](#rule-exclude-with)
[Exclude Without](#rule-exclude-without)
[Filled](#rule-filled)
[Missing](#rule-missing)
[Missing If](#rule-missing-if)
[Missing Unless](#rule-missing-unless)
[Missing With](#rule-missing-with)
[Missing With All](#rule-missing-with-all)
[Nullable](#rule-nullable)
[Present](#rule-present)
[Present If](#rule-present-if)
[Present Unless](#rule-present-unless)
[Present With](#rule-present-with)
[Present With All](#rule-present-with-all)
[Prohibited](#rule-prohibited)
[Prohibited If](#rule-prohibited-if)
[Prohibited If Accepted](#rule-prohibited-if-accepted)
[Prohibited If Declined](#rule-prohibited-if-declined)
[Prohibited Unless](#rule-prohibited-unless)
[Prohibits](#rule-prohibits)
[Required](#rule-required)
[Required If](#rule-required-if)
[Required If Accepted](#rule-required-if-accepted)
[Required If Declined](#rule-required-if-declined)
[Required Unless](#rule-required-unless)
[Required With](#rule-required-with)
[Required With All](#rule-required-with-all)
[Required Without](#rule-required-without)
[Required Without All](#rule-required-without-all)
[Required Array Keys](#rule-required-array-keys)
[Sometimes](#validating-when-present)

</div>

<a name="rule-accepted"></a>
#### accepted

The field under validation must be `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`. This is useful for validating "Terms of Service" acceptance or similar fields.

<a name="rule-accepted-if"></a>
#### accepted_if:anotherfield,value,...



검증 중인 필드는 다른 검증 중인 필드가 특정 값과 같을 경우 `"yes"`, `"on"`, `1`, `"1"`, `true` 또는 `"true"`이어야 합니다. 이는 "서비스 약관" 동의 또는 유사한 필드를 검증하는 데 유용합니다.

<a name="rule-active-url"></a>
#### active_url

검증 중인 필드는 `dns_get_record` PHP 함수에 따라 유효한 A 또는 AAAA 레코드를 가져야 합니다. 제공된 URL의 호스트 이름은 `parse_url` PHP 함수를 사용하여 추출된 후 `dns_get_record`로 전달됩니다.

`active_url` 및 `email:dns`와 같이 DNS 조회를 수행하는 검증 규칙을 테스트할 때는 `Validator::fakeDnsLookups` 메서드를 사용할 수 있습니다. 이 메서드는 규칙의 다른 검증 동작을 유지하면서 DNS 조회를 가짜로 수행합니다:

```php
use Illuminate\Support\Facades\Validator;

Validator::fakeDnsLookups();
```



<a name="rule-after"></a>
#### 이후:_date_

검증 대상 필드는 지정된 날짜 이후의 값이어야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환되기 위해 `strtotime` PHP 함수로 전달됩니다:

```php
'start_date' => ['required', 'date', 'after:tomorrow']
```



`strtotime`로 평가할 날짜 문자열을 전달하는 대신, 날짜와 비교할 다른 필드를 지정할 수 있습니다:

```php
'finish_date' => ['required', 'date', 'after:start_date']
```



편의를 위해 날짜 기반 규칙은 유창한 `date` 규칙 빌더를 사용하여 작성할 수 있습니다:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->after(today()->addDays(7)),
],
```



`afterToday` 및 `todayOrAfter` 방법은 날짜를 유창하게 표현하는 데 사용할 수 있으며, 각각 오늘 이후이거나 오늘이거나 이후여야 합니다:

```php
'start_date' => [
    'required',
    Rule::date()->afterToday(),
],
```



<a name="rule-after-or-equal"></a>
#### after_or_equal:_date_

검증 대상 필드는 지정된 날짜 이후이거나 같아야 합니다. 자세한 내용은 [after](#rule-after) 규칙을 참조하세요.

편의를 위해, 날짜 기반 규칙은 유창한 `date` 규칙 빌더를 사용하여 구성할 수 있습니다:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->afterOrEqual(today()->addDays(7)),
],
```



<a name="rule-anyof"></a>
#### anyOf

`Rule::anyOf` 검증 규칙은 검증 대상 필드가 주어진 검증 규칙 집합 중 하나라도 충족해야 함을 지정할 수 있습니다. 예를 들어, 다음 규칙은 `username` 필드가 이메일 주소이거나 최소 6자 이상인 대시(-)를 포함한 영숫자 문자열인지 검증합니다:

```php
use Illuminate\Validation\Rule;

'username' => [
    'required',
    Rule::anyOf([
        ['string', 'email'],
        ['string', 'alpha_dash', 'min:6'],
    ]),
],
```



<a name="rule-alpha"></a>
#### 알파

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=) 및 [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=)에 포함된 전체 유니코드 알파벳 문자로만 이루어져야 합니다.

이 검증 규칙을 ASCII 범위(`a-z` 및 `A-Z`)의 문자로 제한하려면 검증 규칙에 `ascii` 옵션을 제공할 수 있습니다:

```php
'username' => ['alpha:ascii'],
```



<a name="rule-alpha-dash"></a>
#### alpha_dash

검증 중인 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 전체 유니코드 알파벳-숫자 문자와 ASCII 대시(`-`) 및 ASCII 밑줄(`_`)로만 구성되어야 합니다.

이 검증 규칙을 ASCII 범위(`a-z`, `A-Z`, `0-9`)의 문자로만 제한하려면, 검증 규칙에 `ascii` 옵션을 제공할 수 있습니다:

```php
'username' => ['alpha_dash:ascii'],
```



<a name="rule-alpha-num"></a>
#### 알파_숫자

검증 대상 필드는 [\p{L}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AL%3A%5D&g=&i=), [\p{M}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AM%3A%5D&g=&i=), 및 [\p{N}](https://util.unicode.org/UnicodeJsps/list-unicodeset.jsp?a=%5B%3AN%3A%5D&g=&i=)에 포함된 전체 유니코드 알파벳-숫자 문자여야 합니다.

이 검증 규칙을 ASCII 범위(`a-z`, `A-Z`, 및 `0-9`)의 문자로 제한하려면, 검증 규칙에 `ascii` 옵션을 제공할 수 있습니다:

```php
'username' => ['alpha_num:ascii'],
```



<a name="rule-array"></a>
#### 배열

검증 대상 필드는 PHP `array` 이어야 합니다.

`array` 규칙에 추가 값이 제공되면, 입력 배열의 각 키는 규칙에 제공된 값 목록 안에 있어야 합니다. 다음 예제에서, 입력 배열의 `admin` 키는 `array` 규칙에 제공된 값 목록에 포함되지 않았기 때문에 유효하지 않습니다:

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```



일반적으로, 배열 내에 존재할 수 있는 배열 키를 항상 지정해야 합니다.

<a name="rule-array-keys"></a>
#### array_keys:_foo_,_bar_,...

검증 중인 필드는 주어진 목록에 포함된 모든 키를 가진 PHP `array`여야 합니다. 최소한 하나의 키가 제공되어야 합니다:

```php
'user' => ['array_keys:name,username'],
```



편의를 위해 `Rule::arrayKeys` 방법을 사용할 수 있습니다:

```php
'user' => [Rule::arrayKeys('name', 'username')],
```



<a name="rule-ascii"></a>
#### ascii

검증 중인 필드에는 완전히 7비트 ASCII 문자만 포함되어야 합니다.

<a name="rule-bail"></a>
#### bail

첫 번째 검증 실패 후에는 필드에 대한 검증 규칙 실행을 중지합니다.

`bail` 규칙은 검증 실패가 발생했을 때 특정 필드에 대한 검증만 중지하지만, `stopOnFirstFailure` 방법은 단일 검증 실패가 발생하면 모든 속성에 대한 검증을 중지해야 함을 검증자에게 알립니다:

```php
if ($validator->stopOnFirstFailure()->fails()) {
    // ...
}
```



<a name="rule-before"></a>
#### 이전:_date_

검증 대상 필드는 지정된 날짜 이전의 값이어야 합니다. 날짜들은 유효한 `DateTime` 인스턴스로 변환되기 위해 PHP `strtotime` 함수로 전달됩니다. 또한, [after](#rule-after) 규칙과 마찬가지로, 검증 대상인 다른 필드의 이름을 `date` 값으로 제공할 수 있습니다.

편의를 위해, 날짜 기반 규칙은 fluent `date` 규칙 빌더를 사용하여 구성할 수도 있습니다:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->before(today()->subDays(7)),
],
```



`beforeToday` 및 `todayOrBefore` 방법은 날짜를 유창하게 표현하는 데 사용할 수 있으며, 각각 오늘 이전이거나 오늘이거나 이전이어야 합니다:

```php
'start_date' => [
    'required',
    Rule::date()->beforeToday(),
],
```



<a name="rule-before-or-equal"></a>
#### before_or_equal:_date_

검증 중인 필드는 지정된 날짜 이전이거나 그 날짜와 같아야 합니다. 날짜는 PHP `strtotime` 함수로 전달되어 유효한 `DateTime` 인스턴스로 변환됩니다. 또한 [after](#rule-after) 규칙과 마찬가지로, 검증 중인 다른 필드의 이름을 `date` 값으로 제공할 수 있습니다.

편의를 위해 날짜 기반 규칙은 유창한 `date` 규칙 빌더를 사용하여 생성할 수도 있습니다:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->beforeOrEqual(today()->subDays(7)),
],
```



<a name="rule-between"></a>
#### 사이:_min_,_max_

검증 대상 필드는 주어진 _min_과 _max_ 사이의 크기를 가져야 합니다(포함). 문자열, 숫자, 배열 및 파일은 [size](#rule-size) 규칙과 동일한 방식으로 평가됩니다.

<a name="rule-boolean"></a>
#### 불리언

검증 대상 필드는 불리언으로 변환될 수 있어야 합니다. 허용되는 입력값은 `true`, `false`, `1`, `0`, `"1"`, `"0"`입니다.

`strict` 매개변수를 사용하여 필드의 값이 `true` 또는 `false`일 경우에만 유효하도록 할 수 있습니다:

```php
'foo' => ['boolean:strict']
```



<a name="rule-confirmed"></a>
#### 확인됨

검증 중인 필드에는 `{field}_confirmation` 필드와 일치하는 필드가 있어야 합니다. 예를 들어, 검증 중인 필드가 `password`인 경우, 입력값에 일치하는 `password_confirmation` 필드가 있어야 합니다.

사용자 정의 확인 필드 이름을 전달할 수도 있습니다. 예를 들어, `confirmed:repeat_username`는 검증 중인 필드와 일치하는 `repeat_username` 필드를 기대합니다.

<a name="rule-contains"></a>
#### 포함됨:_foo_,_bar_,...

검증 중인 필드는 지정된 모든 매개변수 값을 포함하는 배열이어야 합니다. 이 규칙은 종종 배열을 `implode` 해야 하므로, `Rule::contains` 방법을 사용하여 규칙을 유연하게 구성할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::contains(['admin', 'editor']),
    ],
]);
```



<a name="rule-doesnt-contain"></a>
#### _foo_, _bar_ 등을 포함하지 않음,...

검증 대상 필드는 주어진 매개변수 값을 포함하지 않는 배열이어야 합니다. 이 규칙은 종종 배열을 `implode`해야 하므로, `Rule::doesntContain` 메서드를 사용하여 규칙을 유창하게 구성할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'roles' => [
        'required',
        'array',
        Rule::doesntContain(['admin', 'editor']),
    ],
]);
```



<a name="rule-current-password"></a>
#### current_password

검증 중인 필드는 인증된 사용자의 비밀번호와 일치해야 합니다. 규칙의 첫 번째 매개변수를 사용하여 [인증 가드](/docs/{{version}}/authentication)를 지정할 수 있습니다:

```php
'password' => ['current_password:api']
```



<a name="rule-date"></a>
#### 날짜

검증 대상 필드는 `strtotime` PHP 함수에 따라 유효한 상대적이지 않은 날짜여야 합니다.

<a name="rule-date-equals"></a>
#### date_equals:_date_

검증 대상 필드는 지정된 날짜와 같아야 합니다. 날짜는 유효한 `DateTime` 인스턴스로 변환되도록 PHP `strtotime` 함수에 전달됩니다.

<a name="rule-date-format"></a>
#### date_format:_format_,...

검증 대상 필드는 주어진 _formats_ 중 하나와 일치해야 합니다. 필드를 검증할 때는 `date` 또는 `date_format` 중 하나만 사용해야 합니다. 이 검증 규칙은 PHP의 [DateTime](https://www.php.net/manual/en/class.datetime.php) 클래스에서 지원하는 모든 형식을 지원합니다.

편의를 위해, 날짜 기반 규칙은 유연한 `date` 규칙 빌더를 사용하여 구성할 수 있습니다:

```php
use Illuminate\Validation\Rule;

'start_date' => [
    'required',
    Rule::date()->format('Y-m-d'),
],
```



<a name="rule-decimal"></a>
#### 소수점:_최소_,_최대_

검증 대상 필드는 숫자여야 하며 지정된 소수 자릿수를 포함해야 합니다:

```php
// Must have exactly two decimal places (9.99)...
'price' => ['decimal:2']

// Must have between 2 and 4 decimal places...
'price' => ['decimal:2,4']
```



<a name="rule-declined"></a>
#### 거부됨

검증 중인 필드는 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`이어야 합니다.

<a name="rule-declined-if"></a>
#### 거부됨_if:anotherfield,value,...

검증 중인 필드는 다른 필드가 특정 값과 같을 경우 `"no"`, `"off"`, `0`, `"0"`, `false`, 또는 `"false"`이어야 합니다.

<a name="rule-different"></a>
#### different:_field_

검증 중인 필드는 _field_와 다른 값을 가져야 합니다.

<a name="rule-digits"></a>
#### digits:_value_

검증 중인 정수는 정확히 _value_ 자릿수를 가져야 합니다.

<a name="rule-digits-between"></a>
#### digits_between:_min_,_max_

검증 중인 정수는 주어진 _min_과 _max_ 사이의 자릿수를 가져야 합니다.

<a name="rule-dimensions"></a>
#### dimensions

검증 중인 파일은 규칙의 매개변수에 지정된 치수 제약 조건을 충족하는 이미지여야 합니다:

```php
'avatar' => ['dimensions:min_width=100,min_height=200']
```



사용 가능한 제약 조건은 다음과 같습니다: _min_width_, _max_width_, _min_height_, _max_height_, _width_, _height_, _ratio_, _min_ratio_, _max_ratio_.

_ratio_ 제약 조건은 너비를 높이로 나눈 값으로 표시해야 합니다. 이는 `3/2`와 같은 분수나 `1.5`와 같은 부동 소수점으로 지정할 수 있습니다:

```php
'avatar' => ['dimensions:ratio=3/2']
```



_min_ratio_와 _max_ratio_ 제약 조건은 허용 가능한 종횡비 범위를 정의하는 데 사용될 수 있습니다:

```php
'avatar' => ['dimensions:min_ratio=1/2,max_ratio=3/2']
```



이 규칙은 여러 인수를 필요로 하므로, 규칙을 유창하게 구성하기 위해 `Rule::dimensions` 방법을 사용하는 것이 종종 더 편리합니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'avatar' => [
        'required',
        Rule::dimensions()
            ->maxWidth(1000)
            ->maxHeight(500)
            ->ratio(3 / 2),
    ],
]);
```



또한 `minRatio`, `maxRatio` 및 `ratioBetween` 방법을 사용하여 비율 제약을 유창하게 정의할 수 있습니다:

```php
Rule::dimensions()->ratioBetween(min: 1 / 2, max: 3 / 2);
```



<a name="rule-distinct"></a>
#### distinct

배열을 검증할 때, 검증 중인 필드는 중복 값을 가져서는 안 됩니다:

```php
'foo.*.id' => ['distinct']
```



Distinct는 기본적으로 느슨한 변수 비교를 사용합니다. 엄격한 비교를 사용하려면 검증 규칙 정의에 `strict` 매개변수를 추가할 수 있습니다:

```php
'foo.*.id' => ['distinct:strict']
```



규칙이 대소문자 차이를 무시하도록 하려면 검증 규칙의 인수에 `ignore_case`를 추가할 수 있습니다:

```php
'foo.*.id' => ['distinct:ignore_case']
```



<a name="rule-doesnt-start-with"></a>
#### _foo_, _bar_ 등으로 시작하면 안 됩니다.

검증 중인 필드는 주어진 값 중 하나로 시작하면 안 됩니다.

<a name="rule-doesnt-end-with"></a>
#### _foo_, _bar_ 등으로 끝나면 안 됩니다.

검증 중인 필드는 주어진 값 중 하나로 끝나면 안 됩니다.

<a name="rule-email"></a>
#### 이메일

검증 중인 필드는 이메일 주소 형식이어야 합니다. 이 검증 규칙은 이메일 주소를 검증하기 위해 [egulias/email-validator](https://github.com/egulias/EmailValidator) 패키지를 사용합니다. 기본적으로 `RFCValidation` 검증기가 적용되지만, 다른 검증 스타일도 적용할 수 있습니다.

```php
'email' => ['email:rfc,dns']
```



위의 예제는 `RFCValidation` 및 `DNSCheckValidation` 유효성 검사를 적용합니다. 적용할 수 있는 전체 유효성 검사 스타일 목록은 다음과 같습니다:

<div class="content-list" markdown="1">

- `rfc`: `RFCValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일 주소를 검증합니다.
- `strict`: `NoRFCWarningsValidation` - [지원되는 RFC](https://github.com/egulias/EmailValidator?tab=readme-ov-file#supported-rfcs)에 따라 이메일을 검증하며, 경고가 발견되면 실패 처리합니다(예: 끝 위치의 점, 연속된 여러 점).
- `dns`: `DNSCheckValidation` - 이메일 주소의 도메인이 유효한 MX 레코드를 갖고 있는지 확인합니다.
- `spoof`: `SpoofCheckValidation` - 이메일 주소에 유사 문자(homograph) 또는 기만적인 Unicode 문자가 포함되어 있지 않은지 확인합니다.
- `filter`: `FilterEmailValidation` - PHP의 `filter_var` 함수에 따라 이메일 주소가 유효한지 확인합니다.
- `filter_unicode`: `FilterEmailValidation::unicode()` - PHP의 `filter_var` 함수에 따라 이메일 주소가 유효한지 확인하며, 일부 Unicode 문자를 허용합니다.

</div>

편의상, 이메일 유효성 검사 규칙은 플루언트 규칙 빌더를 사용하여 구성할 수 있습니다:

```php
use Illuminate\Validation\Rule;

$request->validate([
    'email' => [
        'required',
        Rule::email()
            ->rfcCompliant(strict: false)
            ->validateMxRecord()
            ->preventSpoofing()
    ],
]);
```



`dns` 검증기는 주소의 도메인이 유효한 MX 레코드를 가지고 있는지 확인하기 위해 실제 DNS 조회를 수행합니다. 개별 메일박스가 존재하는지는 확인하지 않습니다.

테스트가 실제 DNS 조회에 의존하지 않아야 하므로, 다른 요청된 검증(`rfc` 등)이 계속 실행되는 동안 `Validator::fakeDnsLookups` 방법을 사용하여 [DNS 조회를 가짜로](#rule-active-url) 처리할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

Validator::fakeDnsLookups();
```



이렇게 하면 애플리케이션이 기존 검증 규칙을 계속 사용하면서 테스트할 수 있습니다:

```php
'email' => ['required', 'email:rfc,dns'],
```



> [!WARNING]
> `dns` 및 `spoof` 검증기는 PHP `intl` 확장을 필요로 합니다.

<a name="rule-encoding"></a>
#### 인코딩:*encoding_type*

검증 중인 필드는 지정된 문자 인코딩과 일치해야 합니다. 이 규칙은 PHP의 `mb_check_encoding` 함수를 사용하여 주어진 파일이나 문자열 값의 인코딩을 확인합니다. 편의를 위해 Laravel의 유창한 파일 규칙 빌더를 사용하여 `encoding` 규칙을 구성할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['csv'])
            ->encoding('utf-8'),
    ],
]);
```



<a name="rule-ends-with"></a>
#### _foo_, _bar_, ...로 끝나야 함

검증 중인 필드는 주어진 값 중 하나로 끝나야 합니다.

<a name="rule-enum"></a>
#### 열거형

`Enum` 규칙은 클래스 기반 규칙으로, 검증 중인 필드가 유효한 열거형 값을 포함하는지 확인합니다. `Enum` 규칙은 열거형의 이름을 유일한 생성자 인수로 받습니다. 원시 값을 검증할 때에는 `Enum` 규칙에 백업된 Enum을 제공해야 합니다:

```php
use App\Enums\ServerStatus;
use Illuminate\Validation\Rule;

$request->validate([
    'status' => [Rule::enum(ServerStatus::class)],
]);
```



`Enum` 규칙의 `only` 및 `except` 메서드는 어떤 열거형(enum) 케이스가 유효한지 고려할지를 제한하는 데 사용할 수 있습니다:

```php
Rule::enum(ServerStatus::class)
    ->only([ServerStatus::Pending, ServerStatus::Active]);

Rule::enum(ServerStatus::class)
    ->except([ServerStatus::Pending, ServerStatus::Active]);
```



`when` 방법은 `Enum` 규칙을 조건부로 수정하는 데 사용될 수 있습니다:

```php
use Illuminate\Support\Facades\Auth;
use Illuminate\Validation\Rule;

Rule::enum(ServerStatus::class)
    ->when(
        Auth::user()->isAdmin(),
        fn ($rule) => $rule->only(...),
        fn ($rule) => $rule->only(...),
    );
```



<a name="rule-exclude"></a>
#### 제외

검증 중인 필드는 `validate` 및 `validated` 메서드에서 반환되는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-if"></a>
#### _anotherfield_가 _value_인 경우 제외

검증 중인 필드는 _anotherfield_ 필드가 _value_와 같으면 `validate` 및 `validated` 메서드에서 반환되는 요청 데이터에서 제외됩니다.

복잡한 조건부 제외 로직이 필요한 경우, `Rule::excludeIf` 메서드를 사용할 수 있습니다. 이 메서드는 불리언 값이나 클로저를 허용합니다. 클로저가 주어진 경우, 검증 중인 필드를 제외해야 하는지 여부를 나타내기 위해 클로저는 `true` 또는 `false`를 반환해야 합니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeIf(fn () => $request->user()->is_admin)],
]);
```



<a name="rule-exclude-unless"></a>
#### 제외_되지_않으면:_anotherfield_,_value_

검증 중인 필드는 _anotherfield_ 필드가 _value_와 같지 않으면 `validate` 및 `validated` 메소드에서 반환되는 요청 데이터에서 제외됩니다. 만약 _value_가 `null`(`exclude_unless:name,null`)라면, 비교 대상 필드가 `null`이거나 요청 데이터에서 비교 대상 필드가 누락되지 않는 한 검증 중인 필드는 제외됩니다.

복잡한 조건부 제외 로직이 필요한 경우 `Rule::excludeUnless` 메소드를 사용할 수 있습니다. 이 메소드는 불리언 값 또는 클로저를 받습니다. 클로저가 제공되면, 클로저는 검증 중인 필드를 제외하지 않을지 여부를 나타내기 위해 `true` 또는 `false`를 반환해야 합니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::excludeUnless(fn () => $request->user()->is_admin)],
]);
```



<a name="rule-exclude-with"></a>
#### _anotherfield_가 있는 경우 제외

검증 중인 필드는 _anotherfield_ 필드가 존재하는 경우 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exclude-without"></a>
#### _anotherfield_가 없는 경우 제외

검증 중인 필드는 _anotherfield_ 필드가 존재하지 않는 경우 `validate` 및 `validated` 메서드가 반환하는 요청 데이터에서 제외됩니다.

<a name="rule-exists"></a>
#### 존재: _table_, _column_

검증 중인 필드는 지정된 데이터베이스 테이블에 존재해야 합니다.

<a name="basic-usage-of-exists-rule"></a>
#### Exists 규칙의 기본 사용법

```php
'state' => ['exists:states']
```



만약 `column` 옵션이 지정되지 않으면, 필드 이름이 사용됩니다. 따라서 이 경우, 규칙은 `states` 데이터베이스 테이블이 요청의 `state` 속성 값과 일치하는 `state` 열 값을 포함하는지를 검증합니다.

<a name="specifying-a-custom-column-name"></a>
#### 사용자 정의 열 이름 지정

검증 규칙이 사용할 데이터베이스 열 이름을 명시적으로 지정하려면, 데이터베이스 테이블 이름 뒤에 열 이름을 작성하면 됩니다:

```php
'state' => ['exists:states,abbreviation']
```



가끔 `exists` 쿼리에 사용할 특정 데이터베이스 연결을 지정해야 할 수도 있습니다. 이는 연결 이름을 테이블 이름 앞에 붙여서 수행할 수 있습니다:

```php
'email' => ['exists:connection.staff,email']
```



테이블 이름을 직접 지정하는 대신, 테이블 이름을 결정하는 데 사용될 Eloquent 모델을 지정할 수 있습니다:

```php
'user_id' => ['exists:App\Models\User,id']
```



검증 규칙에 의해 실행되는 쿼리를 사용자 지정하고자 하는 경우, `Rule` 클래스를 사용하여 규칙을 유창하게 정의할 수 있습니다.

```php
use Illuminate\Database\Query\Builder;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::exists('staff')->where(function (Builder $query) {
            $query->where('account_id', 1);
        }),
    ],
]);
```



`Rule::exists` 메서드에 의해 생성된 `exists` 규칙에서 사용해야 하는 데이터베이스 열 이름을 `exists` 메서드의 두 번째 인수로 열 이름을 제공하여 명시적으로 지정할 수 있습니다:

```php
'state' => [Rule::exists('states', 'abbreviation')],
```



때때로 데이터베이스에 값 배열이 존재하는지 확인하고 싶을 수 있습니다. 검증할 필드에 `exists` 규칙과 [array](#rule-array) 규칙을 모두 추가하여 이렇게 할 수 있습니다:

```php
'states' => ['array', Rule::exists('states', 'abbreviation')],
```



이 두 규칙이 모두 필드에 할당되면, Laravel은 지정된 테이블에 주어진 모든 값이 존재하는지 확인하기 위해 자동으로 단일 쿼리를 생성합니다.

<a name="rule-extensions"></a>
#### 확장자:_foo_,_bar_,...

검증 중인 파일은 나열된 확장자 중 하나에 해당하는 사용자 지정 확장자를 가져야 합니다.

```php
'photo' => ['required', 'extensions:jpg,png'],
```



> [!WARNING]
> You should never rely on validating a file by its user-assigned extension alone. This rule should typically always be used in combination with the [mimes](#rule-mimes) or [mimetypes](#rule-mimetypes) rules.

<a name="rule-file"></a>
#### file

The field under validation must be a successfully uploaded file.

<a name="rule-filled"></a>
#### filled

The field under validation must not be empty when it is present.

<a name="rule-gt"></a>
#### gt:_field_

The field under validation must be greater than the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

<a name="rule-gte"></a>
#### gte:_field_

The field under validation must be greater than or equal to the given _field_ or _value_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

<a name="rule-hex-color"></a>
#### hex_color

The field under validation must contain a valid color value in [hexadecimal](https://developer.mozilla.org/en-US/docs/Web/CSS/hex-color) format.

<a name="rule-image"></a>
#### image

The file under validation must be an image (jpg, jpeg, png, bmp, gif, or webp).

> [!WARNING]
> By default, the image rule does not allow SVG files due to the possibility of XSS vulnerabilities. If you need to allow SVG files, you may provide the `allow_svg` directive to the `image` rule (`image:allow_svg`).

<a name="rule-in"></a>
#### in:_foo_,_bar_,...

The field under validation must be included in the given list of values. Since this rule often requires you to `implode` an array, the `Rule::in` method may be used to fluently construct the rule:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'zones' => [
        'required',
        Rule::in(['first-zone', 'second-zone']),
    ],
]);
```



`in` 규칙이 `array` 규칙과 결합될 때 입력 배열의 각 값은 `in` 규칙에 제공된 값 목록에 포함되어야 합니다. 다음 예제에서 입력 배열의 `LAS` 공항 코드는 `in` 규칙에 제공된 공항 목록에 포함되어 있지 않기 때문에 유효하지 않습니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$input = [
    'airports' => ['NYC', 'LAS'],
];

Validator::make($input, [
    'airports' => [
        'required',
        'array',
    ],
    'airports.*' => Rule::in(['NYC', 'LIT']),
]);
```



<a name="rule-in-array"></a>
#### in_array:_anotherfield_.*

검증 중인 필드는 _anotherfield_의 값 중 하나에 존재해야 합니다.

<a name="rule-in-array-keys"></a>
#### in_array_keys:_value_.*

검증 중인 필드는 배열이어야 하며, 해당 배열 안에 주어진 _values_ 중 적어도 하나를 키로 가져야 합니다:

```php
'config' => ['array', 'in_array_keys:timezone']
```



<a name="rule-integer"></a>
#### 정수

유효성 검사를 받는 필드는 정수여야 합니다.

필드가 `integer` 유형일 때만 유효한 것으로 간주하도록 `strict` 매개변수를 사용할 수 있습니다. 정수 값을 가진 문자열은 유효하지 않은 것으로 간주됩니다:

```php
'age' => ['integer:strict']
```



> [!WARNING]
> This validation rule does not verify that the input is of the "integer" variable type, only that the input is of a type accepted by PHP's `FILTER_VALIDATE_INT` rule. If you need to validate the input as being a number please use this rule in combination with [the `numeric` validation rule](#rule-numeric).

<a name="rule-ip"></a>
#### ip

The field under validation must be an IP address.

<a name="ipv4"></a>
#### ipv4

The field under validation must be an IPv4 address.

<a name="ipv6"></a>
#### ipv6

The field under validation must be an IPv6 address.

<a name="rule-json"></a>
#### json

The field under validation must be a valid JSON string.

<a name="rule-lt"></a>
#### lt:_field_

The field under validation must be less than the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

<a name="rule-lte"></a>
#### lte:_field_

The field under validation must be less than or equal to the given _field_. The two fields must be of the same type. Strings, numerics, arrays, and files are evaluated using the same conventions as the [size](#rule-size) rule.

<a name="rule-lowercase"></a>
#### lowercase

The field under validation must be lowercase.

<a name="rule-list"></a>
#### list

The field under validation must be an array that is a list. An array is considered a list if its keys consist of consecutive numbers from 0 to `count($array) - 1`.

<a name="rule-mac"></a>
#### mac_address

The field under validation must be a MAC address.

<a name="rule-max"></a>
#### max:_value_

The field under validation must be less than or equal to a maximum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule.

<a name="rule-max-digits"></a>
#### max_digits:_value_

The integer under validation must have a maximum length of _value_.

<a name="rule-mimetypes"></a>
#### mimetypes:_text/plain_,...

The file under validation must match one of the given MIME types:

```php
'video' => ['mimetypes:video/avi,video/mpeg,video/quicktime'],

'media' => ['mimetypes:image/*,video/*'],
```



업로드된 파일의 MIME 유형을 결정하기 위해, 파일의 내용을 읽고 프레임워크가 MIME 유형을 추측하려 시도할 것이며, 이 유형은 클라이언트가 제공한 MIME 유형과 다를 수 있습니다.

<a name="rule-mimes"></a>
#### mimes:_foo_,_bar_,...

유효성 검사를 받는 파일은 나열된 확장자 중 하나에 해당하는 MIME 유형을 가져야 합니다:

```php
'photo' => ['mimes:jpg,bmp,png']
```



Even though you only need to specify the extensions, this rule actually validates the MIME type of the file by reading the file's contents and guessing its MIME type. A full listing of MIME types and their corresponding extensions may be found at the following location:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="mime-types-and-extensions"></a>
#### MIME Types and Extensions

This validation rule does not verify agreement between the MIME type and the extension the user assigned to the file. For example, the `mimes:png` validation rule would consider a file containing valid PNG content to be a valid PNG image, even if the file is named `photo.txt`. If you would like to validate the user-assigned extension of the file, you may use the [extensions](#rule-extensions) rule.

<a name="rule-min"></a>
#### min:_value_

The field under validation must have a minimum _value_. Strings, numerics, arrays, and files are evaluated in the same fashion as the [size](#rule-size) rule.

<a name="rule-min-digits"></a>
#### min_digits:_value_

The integer under validation must have a minimum length of _value_.

<a name="rule-multiple-of"></a>
#### multiple_of:_value_

The field under validation must be a multiple of _value_.

<a name="rule-missing"></a>
#### missing

The field under validation must not be present in the input data.

<a name="rule-missing-if"></a>
#### missing_if:_anotherfield_,_value_,...

The field under validation must not be present if the _anotherfield_ field is equal to any _value_.

<a name="rule-missing-unless"></a>
#### missing_unless:_anotherfield_,_value_

The field under validation must not be present unless the _anotherfield_ field is equal to any _value_.

<a name="rule-missing-with"></a>
#### missing_with:_foo_,_bar_,...

The field under validation must not be present _only if_ any of the other specified fields are present.

<a name="rule-missing-with-all"></a>
#### missing_with_all:_foo_,_bar_,...

The field under validation must not be present _only if_ all of the other specified fields are present.

<a name="rule-not-in"></a>
#### not_in:_foo_,_bar_,...

The field under validation must not be included in the given list of values. The `Rule::notIn` method may be used to fluently construct the rule:

```php
use Illuminate\Validation\Rule;

Validator::make($data, [
    'toppings' => [
        'required',
        Rule::notIn(['sprinkles', 'cherries']),
    ],
]);
```



<a name="rule-not-regex"></a>
#### not_regex:_pattern_

검증 대상 필드는 주어진 정규 표현식과 일치해서는 안 됩니다.

내부적으로, 이 규칙은 PHP `preg_match` 함수를 사용합니다. 지정된 패턴은 `preg_match`에서 요구하는 동일한 형식을 따라야 하며, 유효한 구분자를 포함해야 합니다. 예를 들어: `'email' => ['not_regex:/^.+$/i']`.

<a name="rule-nullable"></a>
#### nullable

검증 대상 필드는 `null`일 수 있습니다.

<a name="rule-numeric"></a>
#### numeric

검증 대상 필드는 [numeric](https://www.php.net/manual/en/function.is-numeric.php)이어야 합니다.

`strict` 매개변수를 사용하여 값이 정수 또는 부동 소수점 타입인 경우에만 필드를 유효한 것으로 간주할 수 있습니다. 숫자 문자열은 유효하지 않은 것으로 간주됩니다:

```php
'amount' => ['numeric:strict']
```



<a name="rule-present"></a>
#### present

The field under validation must exist in the input data.

<a name="rule-present-if"></a>
#### present_if:_anotherfield_,_value_,...

The field under validation must be present if the _anotherfield_ field is equal to any _value_.

<a name="rule-present-unless"></a>
#### present_unless:_anotherfield_,_value_

The field under validation must be present unless the _anotherfield_ field is equal to any _value_.

<a name="rule-present-with"></a>
#### present_with:_foo_,_bar_,...

The field under validation must be present _only if_ any of the other specified fields are present.

<a name="rule-present-with-all"></a>
#### present_with_all:_foo_,_bar_,...

The field under validation must be present _only if_ all of the other specified fields are present.

<a name="rule-prohibited"></a>
#### prohibited

The field under validation must be missing or empty. A field is "empty" if it meets one of the following criteria:

<div class="content-list" markdown="1">

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

</div>

<a name="rule-prohibited-if"></a>
#### prohibited_if:_anotherfield_,_value_,...

The field under validation must be missing or empty if the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria:

<div class="content-list" markdown="1">

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

</div>

If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedIf` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should be prohibited:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedIf(fn () => $request->user()->is_admin)],
]);
```

<a name="rule-prohibited-if-accepted"></a>
#### prohibited_if_accepted:_anotherfield_,...

The field under validation must be missing or empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`.

<a name="rule-prohibited-if-declined"></a>
#### prohibited_if_declined:_anotherfield_,...

The field under validation must be missing or empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

<a name="rule-prohibited-unless"></a>
#### prohibited_unless:_anotherfield_,_value_,...

The field under validation must be missing or empty unless the _anotherfield_ field is equal to any _value_. A field is "empty" if it meets one of the following criteria:

<div class="content-list" markdown="1">

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

</div>

If complex conditional prohibition logic is required, you may utilize the `Rule::prohibitedUnless` method. This method accepts a boolean or a closure. When given a closure, the closure should return `true` or `false` to indicate if the field under validation should not be prohibited:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::prohibitedUnless(fn () => $request->user()->is_admin)],
]);
```



<a name="rule-prohibits"></a>
#### prohibits:_anotherfield_,...

If the field under validation is not missing or empty, all fields in _anotherfield_ must be missing or empty. A field is "empty" if it meets one of the following criteria:

<div class="content-list" markdown="1">

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with an empty path.

</div>

<a name="rule-regex"></a>
#### regex:_pattern_

The field under validation must match the given regular expression.

Internally, this rule uses the PHP `preg_match` function. The pattern specified should obey the same formatting required by `preg_match` and thus also include valid delimiters. For example: `'email' => ['regex:/^.+@.+$/i']`.

<a name="rule-required"></a>
#### required

The field under validation must be present in the input data and not empty. A field is "empty" if it meets one of the following criteria:

<div class="content-list" markdown="1">

- The value is `null`.
- The value is an empty string.
- The value is an empty array or empty `Countable` object.
- The value is an uploaded file with no path.

</div>

<a name="rule-required-if"></a>
#### required_if:_anotherfield_,_value_,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to any _value_.

If you would like to construct a more complex condition for the `required_if` rule, you may use the `Rule::requiredIf` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is required:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredIf(fn () => $request->user()->is_admin)],
]);
```



<a name="rule-required-if-accepted"></a>
#### required_if_accepted:_anotherfield_,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to `"yes"`, `"on"`, `1`, `"1"`, `true`, or `"true"`.

<a name="rule-required-if-declined"></a>
#### required_if_declined:_anotherfield_,...

The field under validation must be present and not empty if the _anotherfield_ field is equal to `"no"`, `"off"`, `0`, `"0"`, `false`, or `"false"`.

<a name="rule-required-unless"></a>
#### required_unless:_anotherfield_,_value_,...

The field under validation must be present and not empty unless the _anotherfield_ field is equal to any _value_. This also means _anotherfield_ must be present in the request data unless _value_ is `null`. If _value_ is `null` (`required_unless:name,null`), the field under validation will be required unless the comparison field is `null` or the comparison field is missing from the request data.

If you would like to construct a more complex condition for the `required_unless` rule, you may use the `Rule::requiredUnless` method. This method accepts a boolean or a closure. When passed a closure, the closure should return `true` or `false` to indicate if the field under validation is not required:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless($request->user()->is_admin)],
]);

Validator::make($request->all(), [
    'role_id' => [Rule::requiredUnless(fn () => $request->user()->is_admin)],
]);
```



<a name="rule-required-with"></a>
#### required_with:_foo_,_bar_,...

The field under validation must be present and not empty _only if_ any of the other specified fields are present and not empty.

<a name="rule-required-with-all"></a>
#### required_with_all:_foo_,_bar_,...

The field under validation must be present and not empty _only if_ all of the other specified fields are present and not empty.

<a name="rule-required-without"></a>
#### required_without:_foo_,_bar_,...

The field under validation must be present and not empty _only when_ any of the other specified fields are empty or not present.

<a name="rule-required-without-all"></a>
#### required_without_all:_foo_,_bar_,...

The field under validation must be present and not empty _only when_ all of the other specified fields are empty or not present.

<a name="rule-required-array-keys"></a>
#### required_array_keys:_foo_,_bar_,...

The field under validation must be an array and must contain at least the specified keys.

<a name="rule-same"></a>
#### same:_field_

The given _field_ must match the field under validation.

<a name="rule-size"></a>
#### size:_value_

The field under validation must have a size matching the given _value_. For string data, _value_ corresponds to the number of characters. For numeric data, _value_ corresponds to a given integer value (the attribute must also have the `numeric` or `integer` rule). For an array, _size_ corresponds to the `count` of the array. For files, _size_ corresponds to the file size in kilobytes. Let's look at some examples:

```php
// Validate that a string is exactly 12 characters long...
'title' => ['size:12'];

// Validate that a provided integer equals 10...
'seats' => ['integer', 'size:10'];

// Validate that an array has exactly 5 elements...
'tags' => ['array', 'size:5'];

// Validate that an uploaded file is exactly 512 kilobytes...
'image' => ['file', 'size:512'];
```



<a name="rule-starts-with"></a>
#### starts_with:_foo_,_bar_,...

검증 대상 필드는 주어진 값 중 하나로 시작해야 합니다.

<a name="rule-string"></a>
#### string

검증 대상 필드는 문자열이어야 합니다. 필드가 `null`도 허용되도록 하려면, 해당 필드에 `nullable` 규칙을 할당해야 합니다.

편의를 위해, 문자열 검증 규칙은 fluent `Rule::string()` 규칙 빌더를 사용하여 구성할 수도 있습니다:

```php
use Illuminate\Validation\Rule;

'title' => [
    'required',
    Rule::string()
        ->min(3)
        ->max(255)
        ->alphaDash(ascii: true),
],
```



문자열 규칙 빌더는 `alpha`, `alphaDash`, `alphaNumeric`, `ascii`, `between`, `doesntEndWith`, `doesntStartWith`, `endsWith`, `exactly`, `lowercase`, `max`, `min`, `startsWith` 및 `uppercase`를 포함한 일반 문자열 제약 조건에 대한 메서드를 제공합니다. 규칙 빌더는 조건 설정이 가능하므로 `when` 및 `unless` 메서드를 사용하여 조건적으로 제약을 적용할 수도 있습니다.

<a name="rule-timezone"></a>
#### 시간대

검증 중인 필드는 `DateTimeZone::listIdentifiers` 메서드에 따라 유효한 시간대 식별자여야 합니다.

[`DateTimeZone::listIdentifiers` 메서드] (https://www.php.net/manual/en/datetimezone.listidentifiers.php)에서 허용되는 인수도 이 검증 규칙에 제공할 수 있습니다:

```php
'timezone' => ['required', 'timezone:all'];

'timezone' => ['required', 'timezone:Africa'];

'timezone' => ['required', 'timezone:per_country,US'];
```



<a name="rule-unique"></a>
#### 고유:_테이블_,_컬럼_

검증 대상 필드는 지정된 데이터베이스 테이블 안에 존재하지 않아야 합니다.

**사용자 정의 테이블 / 컬럼 이름 지정:**

테이블 이름을 직접 지정하는 대신, 테이블 이름을 결정하는 데 사용될 Eloquent 모델을 지정할 수 있습니다:

```php
'email' => ['unique:App\Models\User,email_address']
```



`column` 옵션은 필드에 해당하는 데이터베이스 열을 지정하는 데 사용할 수 있습니다. `column` 옵션이 지정되지 않은 경우, 검증 중인 필드의 이름이 사용됩니다.

```php
'email' => ['unique:users,email_address']
```



**사용자 지정 데이터베이스 연결 지정**

가끔 Validator가 수행하는 데이터베이스 쿼리에 대해 사용자 지정 연결을 설정해야 할 때가 있습니다. 이를 수행하려면 테이블 이름 앞에 연결 이름을 붙이면 됩니다:

```php
'email' => ['unique:connection.users,email_address']
```



**주어진 ID를 무시하도록 고유 규칙 강제 적용하기:**

때때로 고유성 검증 중 특정 ID를 무시하고 싶을 때가 있습니다. 예를 들어, 사용자 이름, 이메일 주소, 위치를 포함하는 "프로필 업데이트" 화면을 생각해보세요. 이메일 주소가 고유한지 확인하고 싶을 것입니다. 하지만 사용자가 이름 필드만 변경하고 이메일 필드는 변경하지 않았다면, 사용자가 이미 해당 이메일 주소의 소유자이므로 검증 오류가 발생하지 않기를 원할 것입니다.

사용자의 ID를 무시하도록 검증기에 지시하기 위해, 우리는 `Rule` 클래스를 사용하여 규칙을 유창하게 정의할 것입니다.

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

Validator::make($data, [
    'email' => [
        'required',
        Rule::unique('users')->ignore($user->id),
    ],
]);
```



> [!WARNING]
> 사용자가 제어하는 요청 입력을 `ignore` 메서드에 전달해서는 안 됩니다. 대신, Eloquent 모델 인스턴스의 자동 증가 ID나 UUID와 같은 시스템에서 생성된 고유 ID만 전달해야 합니다. 그렇지 않으면 애플리케이션이 SQL 인젝션 공격에 취약해질 수 있습니다.

모델 키의 값을 `ignore` 메서드에 전달하는 대신 전체 모델 인스턴스를 전달할 수도 있습니다. Laravel은 자동으로 모델에서 키를 추출합니다:

```php
Rule::unique('users')->ignore($user);
```



만약 테이블이 `id`가 아닌 다른 기본 키 열 이름을 사용한다면, `ignore` 메서드를 호출할 때 열 이름을 지정할 수 있습니다:

```php
Rule::unique('users')->ignore($user->id, 'user_id');
```



기본적으로 `unique` 규칙은 검증 중인 속성의 이름과 일치하는 열의 고유성을 확인합니다. 그러나 `unique` 메서드에 두 번째 인수로 다른 열 이름을 전달할 수 있습니다:

```php
Rule::unique('users', 'email_address')->ignore($user->id);
```



**추가적인 Where 절 추가하기:**

`where` 메서드를 사용하여 쿼리를 사용자 정의함으로써 추가적인 쿼리 조건을 지정할 수 있습니다. 예를 들어, `account_id` 열 값이 `1`인 레코드만 검색하도록 쿼리 조건을 추가해 보겠습니다:

```php
'email' => Rule::unique('users')->where(fn (Builder $query) => $query->where('account_id', 1))
```



**고유성 검사에서 소프트 삭제된 레코드 무시하기:**

기본적으로 고유 규칙은 고유성을 결정할 때 소프트 삭제된 레코드를 포함합니다. 고유성 검사에서 소프트 삭제된 레코드를 제외하려면, `withoutTrashed` 메서드를 호출할 수 있습니다:

```php
Rule::unique('users')->withoutTrashed();
```



모델이 소프트 삭제된 레코드에 대해 `deleted_at`가 아닌 다른 열 이름을 사용하는 경우, `withoutTrashed` 메서드를 호출할 때 열 이름을 제공할 수 있습니다:

```php
Rule::unique('users')->withoutTrashed('was_deleted_at');
```



<a name="rule-uppercase"></a>
#### 대문자

검증 대상 필드는 대문자여야 합니다.

<a name="rule-url"></a>
#### URL

검증 대상 필드는 유효한 URL이어야 합니다.

유효하다고 간주할 URL 프로토콜을 지정하고 싶다면, 프로토콜을 검증 규칙 매개변수로 전달할 수 있습니다:

```php
'url' => ['url:http,https'],

'game' => ['url:minecraft,steam'],
```



<a name="rule-ulid"></a>
#### ulid

검증 중인 필드는 유효한 [범용 고유 사전식 정렬 식별자](https://github.com/ulid/spec) (ULID)이어야 합니다.

<a name="rule-uuid"></a>
#### uuid

검증 중인 필드는 유효한 RFC 9562 (버전 1, 3, 4, 5, 6, 7, 또는 8) 범용 고유 식별자(UUID)이어야 합니다.

또한 주어진 UUID가 버전별 UUID 사양과 일치하는지 검증할 수도 있습니다:

```php
'uuid' => ['uuid:4']
```



<a name="conditionally-adding-rules"></a>
## 규칙을 조건부로 추가하기

<a name="skipping-validation-when-fields-have-certain-values"></a>
#### 특정 값이 있는 경우 필드 검증 건너뛰기

때때로 다른 필드가 특정 값을 가진 경우 특정 필드를 검증하지 않기를 원할 수 있습니다. 이는 `exclude_if` 검증 규칙을 사용하여 수행할 수 있습니다. 이 예에서 `appointment_date` 및 `doctor_name` 필드는 `has_appointment` 필드가 `false` 값을 가지면 검증되지 않습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_if:has_appointment,false', 'required', 'date'],
    'doctor_name' => ['exclude_if:has_appointment,false', 'required', 'string'],
]);
```



또는 다른 필드가 특정 값을 가지지 않는 한 주어진 필드를 검증하지 않도록 `exclude_unless` 규칙을 사용할 수 있습니다:

```php
$validator = Validator::make($data, [
    'has_appointment' => ['required', 'boolean'],
    'appointment_date' => ['exclude_unless:has_appointment,true', 'required', 'date'],
    'doctor_name' => ['exclude_unless:has_appointment,true', 'required', 'string'],
]);
```



<a name="validating-when-present"></a>
#### 존재할 때 검증하기

어떤 상황에서는 검증 중인 데이터에 해당 필드가 존재할 때에만 해당 필드에 대한 검증을 실행하고 싶을 수 있습니다. 이를 빠르게 수행하려면 규칙 목록에 `sometimes` 규칙을 추가하십시오:

```php
$validator = Validator::make($data, [
    'email' => ['sometimes', 'required', 'email'],
]);
```



위의 예제에서, `email` 필드는 `$data` 배열에 존재할 경우에만 검증됩니다.

> [!NOTE]
> 항상 존재해야 하지만 비어 있을 수 있는 필드를 검증하려는 경우, [옵션 필드에 대한 이 노트](#a-note-on-optional-fields)를 확인하십시오.

<a name="complex-conditional-validation"></a>
#### 복잡한 조건부 검증

때때로 더 복잡한 조건 논리에 기반한 검증 규칙을 추가하고 싶을 수 있습니다. 예를 들어, 다른 필드의 값이 100보다 큰 경우에만 특정 필드를 요구하고 싶을 수 있습니다. 또는 다른 필드가 존재할 때만 두 필드가 특정 값을 가져야 할 수도 있습니다. 이러한 검증 규칙을 추가하는 것은 어렵지 않습니다. 먼저, 절대 변하지 않는 _정적 규칙_으로 `Validator` 인스턴스를 생성하십시오:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'email' => ['required', 'email'],
    'games' => ['required', 'integer', 'min:0'],
]);
```



우리의 웹 애플리케이션이 게임 수집가를 위한 것이라고 가정해 봅시다. 게임 수집가가 우리 애플리케이션에 등록하고 100개 이상의 게임을 가지고 있다면, 우리는 그들이 왜 그렇게 많은 게임을 소유하고 있는지 설명하기를 원합니다. 예를 들어, 그들이 게임 재판매 가게를 운영하거나, 단순히 게임 수집을 즐길 수도 있습니다. 이 조건부 요구 사항을 추가하려면 `Validator` 인스턴스에서 `sometimes` 메서드를 사용할 수 있습니다.

```php
use Illuminate\Support\Fluent;

$validator->sometimes('reason', ['required', 'max:500'], function (Fluent $input) {
    return $input->games >= 100;
});
```



`sometimes` 메서드에 전달된 첫 번째 인수는 조건부로 검증하려는 필드의 이름입니다. 두 번째 인수는 추가하려는 규칙 목록입니다. 세 번째 인수로 전달된 클로저가 `true`를 반환하면 규칙이 추가됩니다. 이 메서드를 사용하면 복잡한 조건부 검증을 쉽게 구축할 수 있습니다. 여러 필드에 대한 조건부 검증도 한 번에 추가할 수 있습니다:

```php
$validator->sometimes(['reason', 'cost'], 'required', function (Fluent $input) {
    return $input->games >= 100;
});
```



> [!NOTE]
> 당신의 클로저에 전달된 `$input` 파라미터는 `Illuminate\Support\Fluent`의 인스턴스이며, 검증 중인 입력과 파일에 접근하는 데 사용될 수 있습니다.

<a name="complex-conditional-array-validation"></a>
#### 복잡한 조건 배열 검증

때때로 같은 중첩 배열 내의 다른 필드를 기반으로 필드를 검증하고 싶을 때가 있습니다. 이때 인덱스를 알 수 없는 상황에서, 클로저가 두 번째 인자를 받을 수 있도록 허용할 수 있으며, 이 두 번째 인자는 검증 중인 배열의 현재 개별 항목이 됩니다:

```php
$input = [
    'channels' => [
        [
            'type' => 'email',
            'address' => 'abigail@example.com',
        ],
        [
            'type' => 'url',
            'address' => 'https://example.com',
        ],
    ],
];

$validator->sometimes('channels.*.address', 'email', function (Fluent $input, Fluent $item) {
    return $item->type === 'email';
});

$validator->sometimes('channels.*.address', 'url', function (Fluent $input, Fluent $item) {
    return $item->type !== 'email';
});
```



클로저에 전달된 `$input` 매개변수와 마찬가지로, 속성 데이터가 배열일 경우 `$item` 매개변수는 `Illuminate\Support\Fluent`의 인스턴스입니다. 그렇지 않으면 문자열입니다.

<a name="validating-arrays"></a>
## 배열 유효성 검사

[array validation rule documentation](#rule-array)에서 논의된 바와 같이, `array` 규칙은 허용된 배열 키 목록을 수락합니다. 배열 내에 추가 키가 있는 경우, 유효성 검사는 실패합니다:

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'user' => [
        'name' => 'Taylor Otwell',
        'username' => 'taylorotwell',
        'admin' => true,
    ],
];

Validator::make($input, [
    'user' => ['array:name,username'],
]);
```



일반적으로, 배열 내에 존재할 수 있는 배열 키를 항상 지정해야 합니다. 그렇지 않으면, 검증기의 `validate` 및 `validated` 메서드는 다른 중첩 배열 검증 규칙으로 검증되지 않은 키를 포함하여 배열과 그 모든 키를 포함한 모든 검증된 데이터를 반환합니다.

<a name="validating-nested-array-input"></a>
### 중첩 배열 입력 검증

중첩된 배열 기반 폼 입력 필드를 검증하는 것은 어려울 필요가 없습니다. 배열 내 속성을 검증하기 위해 "점 표기법(dot notation)"을 사용할 수 있습니다. 예를 들어, 들어오는 HTTP 요청에 `photos[profile]` 필드가 포함되어 있다면 다음과 같이 검증할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;

$validator = Validator::make($request->all(), [
    'photos.profile' => ['required', 'image'],
]);
```



배열의 각 요소를 검증할 수도 있습니다. 예를 들어, 주어진 배열 입력 필드에 있는 각 이메일이 고유한지 검증하려면 다음과 같이 할 수 있습니다:

```php
$validator = Validator::make($request->all(), [
    'users.*.email' => ['email', 'unique:users'],
    'users.*.first_name' => ['required_with:users.*.last_name'],
]);
```



마찬가지로, [언어 파일에서 사용자 정의 검증 메시지](#custom-messages-for-specific-attributes)를 지정할 때 `*` 문자를 사용할 수 있어, 배열 기반 필드에 대해 단일 검증 메시지를 사용하는 것이 간편해집니다:

```php
'custom' => [
    'users.*.email' => [
        'unique' => 'Each user must have a unique email address',
    ]
],
```



<a name="accessing-nested-array-data"></a>
#### 중첩 배열 데이터 접근

속성에 대한 검증 규칙을 할당할 때 특정 중첩 배열 요소의 값을 접근해야 할 경우가 있습니다. 이는 `Rule::forEach` 메서드를 사용하여 수행할 수 있습니다. `forEach` 메서드는 배열 속성의 각 반복에 대해 호출될 클로저를 받아들이며, 이 클로저는 속성의 값과 명시적이고 완전히 확장된 속성 이름을 전달받습니다. 클로저는 배열 요소에 할당할 규칙 배열을 반환해야 합니다:

```php
use App\Rules\HasPermission;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

$validator = Validator::make($request->all(), [
    'companies.*.id' => Rule::forEach(function (string|null $value, string $attribute) {
        return [
            Rule::exists(Company::class, 'id'),
            new HasPermission('manage-company', $value),
        ];
    }),
]);
```



<a name="error-message-indexes-and-positions"></a>
### 오류 메시지 인덱스 및 위치

배열을 검증할 때, 애플리케이션에서 표시되는 오류 메시지 내에서 검증에 실패한 특정 항목의 인덱스나 위치를 참조하고 싶을 수 있습니다. 이를 위해 [사용자 정의 검증 메시지](#manual-customizing-the-error-messages) 내에 `:index` (`0`부터 시작), `:position` (`1`부터 시작), 또는 `:ordinal-position` (`1st`부터 시작) 자리 표시자를 포함할 수 있습니다.

```php
use Illuminate\Support\Facades\Validator;

$input = [
    'photos' => [
        [
            'name' => 'BeachVacation.jpg',
            'description' => 'A photo of my beach vacation!',
        ],
        [
            'name' => 'GrandCanyon.jpg',
            'description' => '',
        ],
    ],
];

Validator::validate($input, [
    'photos.*.description' => ['required'],
], [
    'photos.*.description.required' => 'Please describe photo #:position.',
]);
```



위의 예를 기준으로, 검증은 실패하며 사용자에게 다음과 같은 오류가 표시됩니다: "사진 #2를 설명해 주세요."

필요한 경우 `second-index`, `second-position`, `third-index`, `third-position` 등을 통해 더 깊이 중첩된 인덱스와 위치를 참조할 수 있습니다.

```php
'photos.*.attributes.*.string' => 'Invalid attribute for photo #:second-position.',
```



<a name="validating-files"></a>
## 파일 검증

Laravel은 업로드된 파일을 검증하는 데 사용할 수 있는 다양한 검증 규칙을 제공합니다. 예를 들어 `mimes`, `image`, `min`, `max` 등이 있습니다. 파일을 검증할 때 이러한 규칙을 개별적으로 지정할 수 있지만, Laravel은 또한 편리하게 사용할 수 있는 유창한 파일 검증 규칙 빌더를 제공합니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'attachment' => [
        'required',
        File::types(['mp3', 'wav'])
            ->min(1024)
            ->max(12 * 1024),
    ],
]);
```



<a name="validating-files-file-types"></a>
#### 파일 유형 검증

`types` 메서드를 호출할 때 확장자만 지정하면 되지만, 이 메서드는 실제로 파일 내용을 읽고 MIME 유형을 추측하여 파일의 MIME 유형을 검증합니다. MIME 유형과 해당 확장자의 전체 목록은 다음 위치에서 확인할 수 있습니다:

[https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types](https://svn.apache.org/repos/asf/httpd/httpd/trunk/docs/conf/mime.types)

<a name="validating-files-file-sizes"></a>
#### 파일 크기 검증

편의를 위해, 최소 및 최대 파일 크기는 파일 크기 단위를 나타내는 접미사를 포함하여 문자열로 지정할 수 있습니다. `kb`, `mb`, `gb`, `tb` 접미사가 지원됩니다:

```php
File::types(['mp3', 'wav'])
    ->min('1kb')
    ->max('10mb');
```



<a name="validating-files-image-files"></a>
#### 이미지 파일 검증

사용자가 업로드한 이미지를 애플리케이션에서 받는 경우, `File` 규칙의 `image` 생성자 메서드를 사용하여 검증 중인 파일이 이미지(jpg, jpeg, png, bmp, gif 또는 webp)인지 확인할 수 있습니다.

또한, 이미지의 크기를 제한하기 위해 `dimensions` 규칙을 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

Validator::validate($input, [
    'photo' => [
        'required',
        File::image()
            ->min(1024)
            ->max(12 * 1024)
            ->dimensions(Rule::dimensions()->maxWidth(1000)->maxHeight(500)),
    ],
]);
```



> [!NOTE]
> 이미지 크기 검증과 관련된 자세한 정보는 [크기 규칙 문서](#rule-dimensions)에서 확인할 수 있습니다.

> [!WARNING]
> 기본적으로, `image` 규칙은 XSS 취약성 가능성 때문에 SVG 파일을 허용하지 않습니다. SVG 파일을 허용해야 하는 경우, `image` 규칙에 `allowSvg: true`를 전달할 수 있습니다: `File::image(allowSvg: true)`.

<a name="validating-files-image-dimensions"></a>
#### 이미지 크기 검증

이미지의 크기를 검증할 수도 있습니다. 예를 들어, 업로드된 이미지가 최소 1000픽셀 너비와 500픽셀 높이를 만족하는지 검증하려면, `dimensions` 규칙을 사용할 수 있습니다:

```php
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\File;

File::image()->dimensions(
    Rule::dimensions()
        ->maxWidth(1000)
        ->maxHeight(500)
);
```



> [!NOTE]
> 이미지 크기 검증에 관한 더 많은 정보는 [크기 규칙 문서](#rule-dimensions)에서 찾을 수 있습니다.

<a name="validating-passwords"></a>
## 비밀번호 검증

비밀번호가 충분한 복잡성을 가지도록 보장하기 위해, Laravel의 `Password` 규칙 객체를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rules\Password;

$validator = Validator::make($request->all(), [
    'password' => ['required', 'confirmed', Password::min(8)],
]);
```



`Password` 규칙 객체를 사용하면 비밀번호에 최소한 하나의 문자, 숫자, 기호 또는 대소문자가 섞인 문자가 필요하다는 것을 지정하는 등 애플리케이션의 비밀번호 복잡성 요구사항을 쉽게 사용자 정의할 수 있습니다:

```php
// Require at least 8 characters...
Password::min(8);

// Require at most 256 characters...
Password::min(16)->max(256);

// Require at least one letter...
Password::min(8)->letters();

// Require at least one uppercase and one lowercase letter...
Password::min(8)->mixedCase();

// Require at least one number...
Password::min(8)->numbers();

// Require at least one symbol...
Password::min(8)->symbols();
```



또한, `uncompromised` 방법을 사용하여 비밀번호가 공개된 비밀번호 데이터 유출에서 손상되지 않았는지 확인할 수 있습니다:

```php
Password::min(8)->uncompromised();
```



내부적으로, `Password` 규칙 객체는 사용자의 프라이버시나 보안을 침해하지 않으면서 비밀번호가 [haveibeenpwned.com](https://haveibeenpwned.com) 서비스를 통해 유출되었는지 확인하기 위해 [k-익명성](https://en.wikipedia.org/wiki/K-anonymity) 모델을 사용합니다.

기본적으로, 비밀번호가 데이터 유출에서 최소 한 번이라도 나타나면 손상된 것으로 간주됩니다. `uncompromised` 메서드의 첫 번째 인수를 사용하여 이 임계값을 사용자 지정할 수 있습니다:

```php
// Ensure the password appears less than 3 times in the same data leak...
Password::min(8)->uncompromised(3);
```



물론 위의 예제에 있는 모든 메서드를 연결해서 사용할 수 있습니다:

```php
Password::min(8)
    ->max(256)
    ->letters()
    ->mixedCase()
    ->numbers()
    ->symbols()
    ->uncompromised();
```



`toPasswordRulesString` 메서드를 사용하여 `Password` 규칙 객체를 HTML `passwordrules` 속성에 적합한 문자열로 변환할 수 있습니다:

```blade
<input
    type="password"
    name="password"
    autocomplete="new-password"
    passwordrules="{{ Password::defaults()->toPasswordRulesString() }}"
/>
```



<a name="defining-default-password-rules"></a>
#### 기본 비밀번호 규칙 정의

애플리케이션의 한 곳에서 비밀번호에 대한 기본 검증 규칙을 지정하는 것이 편리할 수 있습니다. `Password::defaults` 메서드를 사용하면 이를 쉽게 수행할 수 있으며, 이 메서드는 클로저를 받습니다. `defaults` 메서드에 전달된 클로저는 Password 규칙의 기본 구성을 반환해야 합니다. 일반적으로 `defaults` 규칙은 애플리케이션 서비스 제공자 중 하나의 `boot` 메서드 내에서 호출되어야 합니다:

```php
use Illuminate\Validation\Rules\Password;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Password::defaults(function () {
        $rule = Password::min(8);

        return $this->app->isProduction()
            ? $rule->mixedCase()->uncompromised()
            : $rule;
    });
}
```



그런 다음, 특정 비밀번호가 검증을 받을 때 기본 규칙을 적용하고 싶다면, 인수 없이 `defaults` 메서드를 호출할 수 있습니다:

```php
'password' => ['required', Password::defaults()],
```



가끔 기본 비밀번호 검증 규칙에 추가 검증 규칙을 첨부하고 싶을 때가 있습니다. 이 작업을 수행하려면 `rules` 방법을 사용할 수 있습니다:

```php
use App\Rules\ZxcvbnRule;

Password::defaults(function () {
    $rule = Password::min(8)->rules([new ZxcvbnRule]);

    // ...
});
```



<a name="custom-validation-rules"></a>
## 사용자 정의 유효성 검사 규칙

<a name="using-rule-objects"></a>
### 규칙 객체 사용

Laravel은 다양한 유용한 유효성 검사 규칙을 제공하지만, 때로는 직접 규칙을 지정하고 싶을 수도 있습니다. 사용자 정의 유효성 검사 규칙을 등록하는 한 가지 방법은 규칙 객체를 사용하는 것입니다. 새로운 규칙 객체를 생성하려면 `make:rule` Artisan 명령어를 사용할 수 있습니다. 이 명령어를 사용하여 문자열이 대문자인지 확인하는 규칙을 생성해봅시다. Laravel은 새 규칙을 `app/Rules` 디렉터리에 배치합니다. 이 디렉터리가 존재하지 않으면, 규칙 생성을 위한 Artisan 명령어를 실행할 때 Laravel이 해당 디렉터리를 생성합니다:

```shell
php artisan make:rule Uppercase
```



규칙이 생성되면, 우리는 그 동작을 정의할 준비가 된 것입니다. 규칙 객체에는 단일 메서드가 포함되어 있습니다: `validate`. 이 메서드는 속성 이름, 그 값, 그리고 유효성 검사 오류 메시지와 함께 실패 시 호출되어야 하는 콜백을 받습니다:

```php
<?php

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements ValidationRule
{
    /**
     * Run the validation rule.
     */
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        if (strtoupper($value) !== $value) {
            $fail('The :attribute must be uppercase.');
        }
    }
}
```



규칙이 정의되면, 규칙 객체의 인스턴스를 다른 검증 규칙과 함께 전달하여 검증기에 첨부할 수 있습니다:

```php
use App\Rules\Uppercase;

$request->validate([
    'name' => ['required', 'string', new Uppercase],
]);
```



#### 검증 메시지 번역하기

`$fail` 클로저에 대한 문자 그대로의 오류 메시지를 제공하는 대신, [번역 문자열 키](/docs/{{version}}/localization)를 제공하고 Laravel에게 오류 메시지를 번역하도록 지시할 수도 있습니다:

```php
if (strtoupper($value) !== $value) {
    $fail('validation.uppercase')->translate();
}
```



필요한 경우, `translate` 메서드에 자리 표시자 대체값과 선호하는 언어를 첫 번째 및 두 번째 인수로 제공할 수 있습니다:

```php
$fail('validation.location')->translate([
    'value' => $this->value,
], 'fr');
```



#### 추가 데이터 접근

사용자 정의 검증 규칙 클래스가 검증 중인 다른 모든 데이터에 접근해야 하는 경우, 해당 규칙 클래스는 `Illuminate\Contracts\Validation\DataAwareRule` 인터페이스를 구현할 수 있습니다. 이 인터페이스는 클래스가 `setData` 메서드를 정의하도록 요구합니다. 이 메서드는 Laravel에 의해 자동으로 호출되며(검증이 진행되기 전에), 검증 중인 모든 데이터를 전달받습니다:

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\DataAwareRule;
use Illuminate\Contracts\Validation\ValidationRule;

class Uppercase implements DataAwareRule, ValidationRule
{
    /**
     * All of the data under validation.
     *
     * @var array<string, mixed>
     */
    protected $data = [];

    // ...

    /**
     * Set the data under validation.
     *
     * @param  array<string, mixed>  $data
     */
    public function setData(array $data): static
    {
        $this->data = $data;

        return $this;
    }
}
```



또는, 검증 규칙이 검증을 수행하는 검증기 인스턴스에 접근할 필요가 있는 경우, `ValidatorAwareRule` 인터페이스를 구현할 수 있습니다:

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Validation\Validator;

class Uppercase implements ValidationRule, ValidatorAwareRule
{
    /**
     * The validator instance.
     *
     * @var \Illuminate\Validation\Validator
     */
    protected $validator;

    // ...

    /**
     * Set the current validator.
     */
    public function setValidator(Validator $validator): static
    {
        $this->validator = $validator;

        return $this;
    }
}
```



<a name="using-closures"></a>
### 클로저 사용

응용 프로그램 전체에서 맞춤 규칙의 기능이 한 번만 필요하다면 규칙 객체 대신 클로저를 사용할 수 있습니다. 클로저는 속성의 이름, 속성의 값, 그리고 유효성 검사에 실패할 경우 호출해야 하는 `$fail` 콜백을 받습니다:

```php
use Illuminate\Support\Facades\Validator;
use Closure;

$validator = Validator::make($request->all(), [
    'title' => [
        'required',
        'max:255',
        function (string $attribute, mixed $value, Closure $fail) {
            if ($value === 'foo') {
                $fail("The {$attribute} is invalid.");
            }
        },
    ],
]);
```



<a name="implicit-rules"></a>
### 암묵적인 규칙

기본적으로, 검증 중인 속성이 존재하지 않거나 빈 문자열을 포함하고 있는 경우, 사용자 정의 규칙을 포함한 일반 검증 규칙은 실행되지 않습니다. 예를 들어, [unique](#rule-unique) 규칙은 빈 문자열에 대해 실행되지 않습니다:

```php
use Illuminate\Support\Facades\Validator;

$rules = ['name' => ['unique:users,name']];

$input = ['name' => ''];

Validator::make($input, $rules)->passes(); // true
```



속성이 비어 있어도 사용자 정의 규칙이 실행되려면, 해당 규칙은 속성이 필수임을 의미해야 합니다. 새 암묵적 규칙 객체를 빠르게 생성하려면 `--implicit` 옵션과 함께 `make:rule` Artisan 명령을 사용할 수 있습니다:

```shell
php artisan make:rule Uppercase --implicit
```

> [!WARNING]
> '암시적' 규칙은 속성이 필수임을 _암시_할 뿐입니다. 실제로 속성이 없거나 비어 있는 경우 이를 무효로 할지는 당신에게 달려 있습니다.
{% endraw %}
