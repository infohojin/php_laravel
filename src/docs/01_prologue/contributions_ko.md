---
layout: docs
title: "기여 안내"
---

{% raw %}
# 기여 안내

- [버그 신고](#bug-reports)
- [지원 질문](#support-questions)
- [어느 지점?](#which-branch)
- [컴파일된 자산](#compiled-assets)
- [AI 생성 기여](#ai-generated-contributions)
- [보안 취약점](#security-vulnerabilities)
- [코딩 스타일](#coding-style)
    - [PHPDoc](#phpdoc)
    - [스타일CI](#styleci)
- [행동강령](#code-of-conduct)

<a name="bug-reports"></a>
## 버그 신고

활발한 협업을 장려하기 위해 Laravel은 GitHub 문제가 아닌 문제를 해결하는 풀 요청을 강력히 권장합니다. 대부분의 자사 패키지에서는 GitHub 문제가 비활성화되어 있습니다.

문제를 발견한 경우 문제를 해결하는 풀 요청을 작성하세요. 풀 요청에는 제목과 문제 및 해결 방법에 대한 명확한 설명이 포함되어야 합니다. 또한 가능한 많은 관련 정보와 문제를 보여주는 코드 샘플을 포함해야 합니다. 끌어오기 요청의 목표는 자신과 다른 사람들이 문제를 쉽게 이해하고 수정 사항을 확인할 수 있도록 하는 것입니다.

문제 해결 방법을 모르는 경우 코딩 에이전트에게 문제를 설명하고 이를 사용하여 끌어오기 요청을 시도하세요.

풀 요청은 "검토 준비 완료"("초안" 상태 아님)로 표시되고 새로운 기능에 대한 모든 테스트가 통과된 경우에만 검토됩니다. "초안" 상태로 남아 있는 오래 지속되는 비활성 풀 요청은 며칠 후에 종료됩니다.

Laravel 소스 코드는 GitHub에서 관리되며 각 Laravel 프로젝트에 대한 저장소가 있습니다.

<div class="content-list" markdown="1">

- [라라벨 AI SDK](https://github.com/laravel/ai)
- [라라벨 애플리케이션](https://github.com/laravel/laravel)
- [라라벨 아트](https://github.com/laravel/art)
- [라라벨 부스트](https://github.com/laravel/boost)
- [라라벨 문서](https://github.com/laravel/docs)
- [라라벨 더스크](https://github.com/laravel/dusk)
- [라라벨 캐셔 스트라이프](https://github.com/laravel/cashier)
- [라라벨 캐셔 패들](https://github.com/laravel/cashier-paddle)
- [라라벨 에코](https://github.com/laravel/echo)
- [라라벨 특사](https://github.com/laravel/envoy)
- [라라벨 폴리오](https://github.com/laravel/folio)
- [라라벨 프레임워크](https://github.com/laravel/framework)
- [라라벨 호라이즌](https://github.com/laravel/horizon)
- [라라벨 여권](https://github.com/laravel/passport)
- [라라벨 페넌트](https://github.com/laravel/pennant)
- [라라벨 파인트](https://github.com/laravel/pint)
- [라라벨 프롬프트](https://github.com/laravel/prompts)
- [라라벨 리버브](https://github.com/laravel/reverb)
- [라라벨 세일](https://github.com/laravel/sail)
- [라라벨 성소](https://github.com/laravel/sanctum)
- [라라벨 스카우트](https://github.com/laravel/scout)
- [라라벨 소셜라이트](https://github.com/laravel/socialite)
- [라라벨 망원경](https://github.com/laravel/telescope)
- [Laravel Livewire 스타터 키트](https://github.com/laravel/livewire-starter-kit)
- [Laravel React 스타터 키트](https://github.com/laravel/react-starter-kit)
- [Laravel Svelte 스타터 키트](https://github.com/laravel/svelte-starter-kit)
- [Laravel Vue 스타터 키트](https://github.com/laravel/vue-starter-kit)

</div>

<a name="support-questions"></a>
## 지원 질문

Laravel의 GitHub 문제 추적기는 Laravel 도움말이나 지원을 제공하기 위한 것이 아닙니다. 대신 다음 채널 중 하나를 사용하세요.

<div class="content-list" markdown="1">

- [GitHub 토론](https://github.com/laravel/framework/discussions)
- [라라캐스트 포럼](https://laracasts.com/discuss)
- [Laravel.io 포럼](https://laravel.io/forum)
- [StackOverflow](https://stackoverflow.com/questions/tagged/laravel)
- [불협화음](https://discord.gg/laravel)
- [라라챗](https://larachat.co)
- [IRC](https://web.libera.chat/?nick=artisan&channels=#laravel)

</div>

<a name="which-branch"></a>
## 어느 지점인가요?

**모든** 버그 수정은 버그 수정을 지원하는 최신 버전(현재 `13.x`)으로 전송되어야 합니다. 향후 릴리스에만 존재하는 기능을 수정하지 않는 한 버그 수정은 **절대로** `master` 브랜치로 전송되어서는 안 됩니다.

현재 릴리스와 **완전히 이전 버전과 호환**되는 **사소한** 기능은 최신 안정 브랜치(현재 `13.x`)로 전송될 수 있습니다.

**주요** 새로운 기능이나 주요 변경 사항이 포함된 기능은 항상 향후 릴리스가 포함된 `master` 브랜치로 전송되어야 합니다.

<a name="compiled-assets"></a>
## 컴파일된 자산

`laravel/laravel` 저장소의 `resources/css` 또는 `resources/js`에 있는 대부분의 파일과 같이 컴파일된 파일에 영향을 주는 변경 사항을 제출하는 경우 컴파일된 파일을 커밋하지 마십시오. 크기가 크기 때문에 관리자가 현실적으로 검토할 수 없습니다. 이는 Laravel에 악성 코드를 주입하는 방법으로 악용될 수 있습니다. 이를 방어적으로 방지하기 위해 모든 컴파일된 파일은 Laravel 관리자에 의해 생성되고 커밋됩니다.

<a name="ai-generated-contributions"></a>
## AI 생성 기여

Laravel에 제출된 모든 풀 요청에 감사드립니다. 그러나 사려 깊은 사람의 검토와 고려 없이 주로 AI를 통해 생성된 상당한 기여는 허용되지 않습니다.

프레임워크에 대한 크거나 복잡한 기여를 지원하기 위해 AI 도구를 사용하기로 선택한 경우 제출하기 전에 결과 코드를 철저하게 검토하고 테스트하고 이해해야 합니다**.

풀 요청 설명은 **반드시** 기여자가 전적으로 작성해야 합니다. AI가 생성한 설명이 포함된 풀 요청은 종료됩니다.

**대량 열기 문제나 전적으로 AI로 생성된 풀 요청은 용납되지 않습니다.** 이러한 풀 요청은 검토 없이 닫히고 기여하는 사용자는 저장소에서 차단될 수 있습니다.

우리는 기여자가 기존 코드베이스에 익숙해지고, 커뮤니티에 참여하고, 해결 중인 문제에 대한 자신의 이해와 신중한 고려를 반영하는 끌어오기 요청을 제출하도록 권장합니다.

<a name="security-vulnerabilities"></a>
## 보안 취약점

Laravel에서 보안 취약점을 발견한 경우 보안 팀(<a href="mailto:security@laravel.com">security@laravel.com</a>)으로 이메일을 보내주세요. 모든 보안 취약점은 즉시 해결됩니다.

<a name="coding-style"></a>
## 코딩 스타일

Laravel은 [PSR-2](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-2-coding-style-guide.md) 코딩 표준과 [PSR-4](https://github.com/php-fig/fig-standards/blob/master/accepted/PSR-4-autoloader.md) 자동 로딩 표준을 따릅니다.

<a name="phpdoc"></a>
### PHPDoc

다음은 유효한 Laravel 문서 블록의 예입니다. `@param` 속성 뒤에는 두 개의 공백, 인수 유형, 두 개의 추가 공백, 마지막으로 변수 이름이 옵니다.

```php
/**
 * Register a binding with the container.
 *
 * @param  string|array  $abstract
 * @param  \Closure|string|null  $concrete
 * @param  bool  $shared
 * @return void
 *
 * @throws \Exception
 */
public function bind($abstract, $concrete = null, $shared = false)
{
    // ...
}

```

기본 유형 사용으로 인해 `@param` 또는 `@return` 속성이 중복되는 경우 제거할 수 있습니다.

```php
/**
 * Execute the job.
 * [tl! remove]
 * @return void [tl! remove]
 */
public function handle(AudioProcessor $processor): void
{
    // ...
}

```

그러나 기본 유형이 일반 유형인 경우 `@param` 또는 `@return` 속성을 사용하여 일반 유형을 지정하십시오.

```php
/**
 * Get the attachments for the message.
 * [tl! add]
 * @return array<int, \Illuminate\Mail\Mailables\Attachment> [tl! add]
 */
public function attachments(): array
{
    return [
        Attachment::fromStorage('/path/to/file'),
    ];
}

```

<a name="styleci"></a>
### 스타일CI

코드 스타일이 완벽하지 않아도 걱정하지 마세요! [StyleCI](https://styleci.io/)는 풀 요청이 병합된 후 모든 스타일 수정 사항을 Laravel 저장소에 자동으로 병합합니다. 이를 통해 우리는 코드 스타일이 아닌 기여 내용에 집중할 수 있습니다.

<a name="code-of-conduct"></a>
## 행동 강령

Laravel의 행동 강령은 Ruby의 행동 강령에서 파생되었습니다. 행동 강령을 위반하는 경우 Taylor Otwell(taylor@laravel.com)에게 보고할 수 있습니다.

<div class="content-list" markdown="1">

- 참가자들은 반대 의견에 대해 관용적이어야 합니다.
- 참가자는 자신의 언어와 행동에 인신공격이나 인신비하적인 발언이 없는지 확인해야 합니다.
- 참가자는 타인의 말과 행동을 해석할 때 항상 좋은 의도를 가지고 있어야 합니다.
- 괴롭힘으로 간주될 수 있는 행위는 용납되지 않습니다.

</div>
{% endraw %}
