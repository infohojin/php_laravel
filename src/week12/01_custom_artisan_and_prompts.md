---
layout: docs
title: "12주차 01강: 대화형 아티산(Artisan) 콘솔, 라라벨 프롬프트(Prompts) & 프로세스(Processes)"
---

{% raw %}
# 📖 12주차 01강: 대화형 아티산(Artisan) 콘솔, 라라벨 프롬프트(Prompts) & 프로세스(Processes)

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 서점 관리자가 터미널에서 화살표 키와 스피너를 이용해 직관적으로 도서 재고를 보충하는 대화형 CLI 커맨드(`shop:restock`)를 제작하고, 라라벨 `Process` 파사드를 통해 외부 CLI 유틸리티를 안전하게 비동기 제어합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 물류 창고 관리자님이 웹 브라우저 로그인해서 책 재고 채우는 게 너무 번거롭다고, 터미널에서 빠르게 `php artisan`으로 재고 채울 수 있게 해달래! 그런데 콘솔 창에서 오타 내서 재고 100만 권 넣으면 어떡하지?"  
🐱 **지니**: "도로시, 바로 그럴 때 라라벨 내장 **Laravel Prompts**를 쓰는 거란다! 단순 텍스트 입력창이 아니라 방향키로 선택하는 셀렉트 메뉴, 자동완성 서제스트, 입력 유효성 검사, 프로그레스 바와 스피너까지 터미널에서 화려한 대화형 인터페이스를 만들 수 있지!"  
🐶 **토토**: "멍멍! 도서 대량 입고 CSV 파일의 무결성을 검사하거나 외부 압축 툴을 돌릴 때는 **라라벨 `Process` 파사드**를 쓰면 백그라운드에서 안전하게 외부 프로세스를 실행하고 결과를 낚아챌 수 있다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **커스텀 아티산 커맨드 생성:** `app/Console/Commands/RestockBookCommand.php` (`shop:restock`)
2. **Laravel Prompts 대화형 기능 구현:**
   - `search()` : 도서 제목 검색 및 키보드 화살표 선택
   - `text()` : 보충 수량 입력 및 유효성 검사 (1~1,000 사이 정수만 허용)
   - `confirm()` : 최종 재고 반영 여부 확인 (Y/n)
   - `spin()` : 재고 반영 및 DB 업데이트 중 로딩 애니메이션 연출
   - `info()`, `table()` : 최종 재고 변동 결과 요약 출력
3. **라라벨 `Process` 파사드 활용:** 외부 시스템 유틸리티(예: `git status`, 백업 스크립트) 비동기 실행 및 출력 캡처

---

## 🛠️ 단계별 실습 절차

### 1단계: 커스텀 아티산 커맨드 생성

Artisan 명령어로 커맨드 스캐폴딩을 생성합니다.

```bash
php artisan make:command RestockBookCommand
```

생성된 `app/Console/Commands/RestockBookCommand.php`를 열고 시그니처와 설명을 정의합니다:

```php
<?php

namespace App\Console\Commands;

use App\Models\Book;
use Illuminate\Console\Command;
use function Laravel\Prompts\search;
use function Laravel\Prompts\text;
use function Laravel\Prompts\confirm;
use function Laravel\Prompts\spin;
use function Laravel\Prompts\info;
use function Laravel\Prompts\table;
use function Laravel\Prompts\warning;

class RestockBookCommand extends Command
{
    /**
     * 콘솔 명령어 시그니처 (옵션 및 인자 지정 가능)
     */
    protected $signature = 'shop:restock {--all : 품절 도서 일괄 보충 모드}';

    /**
     * 콘솔 명령어 설명
     */
    protected $description = '대화형 프롬프트를 통해 도서 재고를 보충합니다.';

    /**
     * 명령어 실행 본문
     */
    public function handle(): int
    {
        info('📚 [지니샵 도서 재고 관리 콘솔 시스템]');

        // 1. 도서 검색 및 대화형 선택
        $bookId = search(
            label: '재고를 보충할 도서명을 검색하세요',
            placeholder: '예: 라라벨, 어린왕자...',
            options: fn (string $value) => strlen($value) > 0
                ? Book::where('title', 'like', "%{$value}%")
                    ->pluck('title', 'id')
                    ->all()
                : []
        );

        if (!$bookId) {
            warning('선택된 도서가 없습니다. 작업을 종료합니다.');
            return self::FAILURE;
        }

        $book = Book::findOrFail($bookId);
        info("선택된 도서: [{$book->title}] (현재 재고: {$book->stock}권)");

        // 2. 보충할 수량 입력 (실시간 유효성 검사)
        $quantity = text(
            label: '추가할 입고 수량을 입력하세요',
            placeholder: '10',
            required: true,
            validate: fn (string $value) => match (true) {
                !ctype_digit($value) => '수량은 숫자만 입력할 수 있습니다.',
                (int) $value <= 0 => '1권 이상 입력해야 합니다.',
                (int) $value > 1000 => '1회 최대 입고량은 1,000권입니다.',
                default => null,
            }
        );

        // 3. 최종 확인 컨펌
        $confirmed = confirm(
            label: "'{$book->title}' 도서에 {$quantity}권을 추가 입고하시겠습니까?",
            default: true
        );

        if (!$confirmed) {
            warning('입고 작업이 취소되었습니다.');
            return self::SUCCESS;
        }

        // 4. 로딩 스피너 연출 및 DB 반영
        $oldStock = $book->stock;

        spin(
            callback: function () use ($book, $quantity) {
                usleep(500000); // 0.5초 대기 (스피너 시각 효과)
                $book->increment('stock', (int) $quantity);
                if ($book->stock > 0 && $book->is_sold_out) {
                    $book->update(['is_sold_out' => false]);
                }
            },
            message: '서고 DB에 재고를 반영하고 있습니다...'
        );

        $book->refresh();

        // 5. 완료 결과 요약 표(Table) 출력
        info('✅ 재고 입고가 성공적으로 완료되었습니다!');
        
        table(
            headers: ['도서 ID', '도서명', '기존 재고', '입고 수량', '최종 재고', '품절 여부'],
            rows: [
                [
                    $book->id,
                    $book->title,
                    $oldStock . '권',
                    '+' . $quantity . '권',
                    $book->stock . '권',
                    $book->is_sold_out ? '품절' : '정상 판매'
                ]
            ]
        );

        return self::SUCCESS;
    }
}
```

---

### 2단계: 터미널에서 대화형 CLI 테스트

터미널에서 방금 만든 커맨드를 직접 실행해 봅니다:

```bash
php artisan shop:restock
```

1. 검색어 입력창에 `라라벨`을 입력하면 자동완성 목록이 뜹니다.
2. 키보드 `↑ / ↓` 방향키와 `Enter`로 책을 선택합니다.
3. 숫자를 입력하고 유효성 검사(문자 입력 시 빨간색 에러 메시지)를 확인합니다.
4. `Y`를 누르면 빙글빙글 도는 스피너 애니메이션 후 깔끔한 터미널 표가 출력됩니다!

---

### 3단계: 프로그레스 바(Progress Bar)를 이용한 대량 재고 업데이트

신간 도서 100권의 재고를 한꺼번에 리셋해야 할 때 사용하는 진행률 표시줄(Progress Bar) 예제입니다:

```php
use function Laravel\Prompts\progress;

$books = Book::where('stock', '<', 5)->get();

progress(
    label: '안전 재고 미달 도서 발주 목록 생성 중...',
    steps: $books,
    callback: function ($book, $progress) {
        // 입고 발주 전송 로직
        usleep(50000);
    }
);
```

---

### 4단계: 라라벨 프로세스(Process) 파사드로 외부 CLI 비동기 제어

도서 입고 완료 후 물류 서버의 Git 리포지토리 상태를 확인하거나 외부 압축/변환 명령을 내릴 때 사용하는 `Process` 파사드입니다.

`app/Console/Commands/CheckWarehouseStatusCommand.php`:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Process;

class CheckWarehouseStatusCommand extends Command
{
    protected $signature = 'shop:warehouse-status';
    protected $description = '물류 서버 스토리지 및 외부 프로세스 상태를 점검합니다.';

    public function handle(): int
    {
        $this->info('물류 시스템 외부 프로세스 진단 중...');

        // 1. 단일 동기 프로세스 실행 (타임아웃 10초)
        $result = Process::timeout(10)->run('git status --short');

        if ($result->successful()) {
            $this->info("Git 변경사항:\n" . ($result->output() ?: '깨끗함(Clean)'));
        } else {
            $this->error("명령어 실행 실패: " . $result->errorOutput());
        }

        // 2. 비동기 백그라운드 프로세스 풀(Pool) 동시 실행
        $pool = Process::pool(function ($pool) {
            $pool->as('disk')->run('df -h /');
            $pool->as('uptime')->run('uptime');
        })->start()->wait();

        $this->table(
            ['항목', '결과'],
            [
                ['디스크 용량', trim($pool['disk']->output())],
                ['서버 가동 시간', trim($pool['uptime']->output())],
            ]
        );

        return self::SUCCESS;
    }
}
```

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. 라라벨 11의 Artisan 명령어 자동 등록

라라벨 11에서는 `app/Console/Commands/` 디렉토리에 생성된 모든 커맨드가 프레임워크 부팅 시 리플렉션을 통해 자동으로 등록됩니다. 별도의 커맨드 커널(`Kernel.php`) 등록이 전혀 필요하지 않습니다.

### 2. Laravel Prompts의 고급 컴포넌트 모음

| 컴포넌트 | 용도 및 특징 |
| :--- | :--- |
| `text()` | 단일 라인 문자열 입력 (패스워드 입력 시 `password()`) |
| `textarea()` | 장문의 도서 소개글 입력 |
| `select()` | 단일 옵션 키보드 선택 |
| `multiselect()` | 다중 카테고리 체크박스 선택 |
| `suggest()` | 검색어 자동완성 추천 |
| `confirm()` | Yes/No 확인 대화상자 |
| `spin()` | 비동기 작업 로딩 애니메이션 |
| `table()` | 콘솔 표준 ASCII/유니코드 테이블 렌더링 |

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **비대화형(Non-interactive) 환경(CI/CD, 크론)에서의 Prompts 동작:**  
   Docker 빌드나 GitHub Actions 또는 크론탭에서 `shop:restock`을 실행하면 키보드 입력을 받을 수 없어 예외가 발생합니다. 프롬프트는 `--no-interaction` 플래그가 주어졌을 때 기본값을 사용하거나 옵션 인자(`$this->option('all')`)를 우선적으로 처리하도록 방어 코드를 작성해야 합니다!
2. **`Process` 명령어 인젝션 방지:**  
   외부 프로세스 실행 시 사용자 입력을 문자열 그대로 붙이면(`Process::run("rm -rf {$input}")`) 쉘 인젝션 위험이 있습니다. 반드시 배열 형태로 인자를 전달(`Process::run(['ls', '-la', $safePath])`)하세요!

---

## 💡 자가진단 퀴즈 & 실습 과제

1. **퀴즈:** Laravel Prompts에서 사용자가 입력한 값의 유효성을 검사할 때, 유효하지 않으면 반환해야 하는 것은 무엇일까요?
   - 정답: 오류 메시지 문자열 (유효하면 `null` 반환)
2. **과제:** `shop:restock --all` 옵션을 주었을 때, 대화형 프롬프트를 띄우지 않고 현재 품절(`stock == 0`)된 모든 도서에 일괄로 10권씩 재고를 채우는 자동화 분기를 작성해 보세요!
{% endraw %}
