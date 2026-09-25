---
layout: docs
title: "14주차 04강: 무중단 엔보이(Envoy) 배포, 패키지 개발 & 릴리스 업그레이드"
---

{% raw %}
# 📖 14주차 04강: 무중단 엔보이(Envoy) 배포, 패키지 개발 & 릴리스 업그레이드

> **실습 프로젝트:** 지니샵(JinyShop) — 온라인 도서 쇼핑몰  
> **학습 목표:** 14주간 완성한 지니샵(JinyShop)을 실제 운영 서버에 무중단(Zero-downtime)으로 안전하게 배포하기 위한 캐시 최적화 및 Envoy 스크립트를 작성하고, 공통 모듈의 독립 패키지화와 라라벨 상위 버전 릴리스 업그레이드 전략을 체득하여 완벽한 프로덕션 런칭을 완료합니다.  
> **등장인물:** 🐱 지니(시니어 멘토), 👧 도로시(주니어 개발자), 🐶 토토(개발 보조견)  

---

## 💬 지니와 도로시의 티키타카 회의

👧 **도로시**: "지니! 드디어 14주 동안 눈물과 땀으로 완성한 우리 지니샵(JinyShop)을 실제 서버에 배포하는 날이야! 그런데 배포할 때 고객들이 접속하고 있는데 `git pull` 받고 마이그레이션 돌리면 화면이 하얗게 깨지지 않을까?"  
🐱 **지니**: "도로시, 진정한 프로는 절대로 서비스를 멈추지 않는 **무중단(Zero-downtime) 배포**를 한단다! 라라벨 공식 SSH 배포 도구인 **라라벨 엔보이(Laravel Envoy)**를 쓰면, 새 버전을 별도 폴더(`releases/20260925`)에 미리 빌드해 두고 심볼릭 링크(`current`)만 0.001초 만에 찰칵 교체하여 단 1초의 중단도 없이 고객에게 최신 버전을 선물하지!"  
🐶 **토토**: "멍멍! 배포 직전에는 `php artisan optimize`로 모든 설정과 라우트를 캐싱하고, 우리가 만든 쿠폰 계산 모듈은 독립된 패키지로 분리해서 오픈소스 생태계에도 멋지게 기여하자멍! 14주간의 대장정이 드디어 완성되었다멍!"  

---

## 🎯 실습 목표 및 서점 시나리오

1. **운영 배포 전 최적화 체크리스트:** `php artisan optimize`, OPcache 튜닝, Composer `--no-dev`
2. **라라벨 엔보이(Envoy) 무중단 배포 스크립트 작성:** `Envoy.blade.php`
   - Git 저장소 클론 -> Composer 의존성 설치 -> DB 마이그레이션 -> 캐싱 -> 심볼릭 링크 원자적 교체
3. **독립 패키지 개발(Package Development):** 지니샵 공통 쿠폰/할인 엔진을 별도 라라벨 패키지(`packages/jinyshop/coupon`)로 분리
4. **라라벨 릴리스 주기(Release Notes) 및 무중단 업그레이드(Upgrade Guide) 전략**
5. **라라벨 오픈소스 프레임워크 기여하기(Contributions)**

---

## 🛠️ 단계별 실습 절차

### 1단계: 프로덕션 배포 전 캐시 최적화 체크리스트

운영 서버에 코드를 올린 직후에는 매 요청마다 수백 개의 PHP 파일을 읽지 않도록 프레임워크를 압축 캐싱해야 합니다:

```bash
# 1. 설정 파일 단일 배열 캐싱
php artisan config:cache

# 2. 라우트 등록 트리 컴파일 캐싱
php artisan route:cache

# 3. 블레이드 템플릿 사전 컴파일 캐싱
php artisan view:cache

# 4. 이벤트 & 리스너 매핑 캐싱
php artisan event:cache

# 라라벨 11에서는 위의 모든 것을 단 한 줄로 일괄 처리 가능!
php artisan optimize
```

Composer 프로덕션 최적화:
```bash
composer install --no-dev --optimize-autoloader
```

> 🐶 **토토의 팁!**  
> "코드를 새로 배포했는데 이전 코드가 계속 도는 것 같다면 `php artisan optimize:clear`를 외치고 다시 `php artisan optimize`를 돌리라멍!"

---

### 2단계: 라라벨 엔보이(Envoy) 무중단 배포 스크립트 작성

엔보이는 블레이드 문법으로 원격 리눅스 서버에 SSH 명령을 내리는 라라벨 공식 배포 유틸리티입니다:

```bash
composer require --dev laravel/envoy
```

프로젝트 루트에 `Envoy.blade.php` 파일을 생성합니다:

```blade
@servers(['web' => 'deployer@123.45.67.89'])

@setup
    $repository = 'git@github.com:jinysite/jinyshop.git';
    $releases_dir = '/var/www/jinyshop/releases';
    $app_dir = '/var/www/jinyshop';
    $release = date('YmdHis');
    $new_release_dir = $releases_dir . '/' . $release;
@endsetup

@story('deploy')
    clone_repository
    run_composer
    update_permissions
    link_shared_storage
    run_migrations
    optimize_caches
    update_symlink
    restart_services
@endstory

@task('clone_repository')
    echo "📦 [1/8] Git 저장소에서 최신 코드를 내려받습니다...";
    [ -d {{ $releases_dir }} ] || mkdir -p {{ $releases_dir }};
    git clone --depth 1 {{ $repository }} {{ $new_release_dir }};
@endtask

@task('run_composer')
    echo "⚙️ [2/8] Composer 프로덕션 의존성을 설치합니다...";
    cd {{ $new_release_dir }};
    composer install --prefer-dist --no-scripts --no-dev -q -o;
@endtask

@task('link_shared_storage')
    echo "🔗 [3/8] 공유 스토리지 및 .env 심볼릭 링크를 연결합니다...";
    rm -rf {{ $new_release_dir }}/storage;
    ln -nfs {{ $app_dir }}/storage {{ $new_release_dir }}/storage;
    ln -nfs {{ $app_dir }}/.env {{ $new_release_dir }}/.env;
@endtask

@task('run_migrations')
    echo "🗄️ [4/8] 데이터베이스 마이그레이션을 안전하게 실행합니다...";
    cd {{ $new_release_dir }};
    php artisan migrate --force;
@endtask

@task('optimize_caches')
    echo "⚡ [5/8] 라라벨 캐시를 최적화합니다...";
    cd {{ $new_release_dir }};
    php artisan optimize;
@endtask

@task('update_symlink')
    echo "🔄 [6/8] 심볼릭 링크를 교체하여 새 버전을 즉시 활성화합니다 (Zero Downtime)...";
    ln -nfs {{ $new_release_dir }} {{ $app_dir }}/current;
@endtask

@task('restart_services')
    echo "🚀 [7/8] PHP-FPM 및 큐 워커를 재시작합니다...";
    sudo systemctl reload php8.3-fpm;
    cd {{ $app_dir }}/current;
    php artisan queue:restart;
    echo "🎉 [8/8] 지니샵 무중단 배포가 완벽하게 완료되었습니다!";
@endtask
```

로컬 터미널에서 단 한 줄로 배포를 실행합니다:

```bash
envoy run deploy
```

Nginx 웹 서버의 웹 루트(`root`)는 `/var/www/jinyshop/current/public`을 가리키고 있으므로, 심볼릭 링크가 바뀌는 0.001초 동안 사용자에게 단 1ms의 중단 시간도 발생하지 않습니다!

---

### 3단계: 지니샵 쿠폰 엔진의 독립 패키지(Package) 분리

지니샵의 도서 할인 쿠폰 계산 로직을 다른 프로젝트에서도 재사용할 수 있도록 `packages/jinyshop/coupon`으로 독립 패키지화합니다.

`packages/jinyshop/coupon/composer.json`:
```json
{
    "name": "jinyshop/coupon",
    "description": "JinyShop Bookstore Advanced Coupon & Discount Engine",
    "type": "library",
    "license": "MIT",
    "autoload": {
        "psr-4": {
            "JinyShop\\Coupon\\": "src/"
        }
    },
    "extra": {
        "laravel": {
            "providers": [
                "JinyShop\\Coupon\\CouponServiceProvider"
            ]
        }
    }
}
```

`packages/jinyshop/coupon/src/CouponServiceProvider.php`:
```php
<?php

namespace JinyShop\Coupon;

use Illuminate\Support\ServiceProvider;

class CouponServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->mergeConfigFrom(__DIR__ . '/../config/coupon.php', 'coupon');

        $this->app->singleton('coupon', function () {
            return new CouponCalculator();
        });
    }

    public function boot(): void
    {
        if ($this->app->runningInConsole()) {
            $this->publishes([
                __DIR__ . '/../config/coupon.php' => config_path('coupon.php'),
            ], 'coupon-config');
        }
    }
}
```

라라벨의 패키지 자동 검색(Package Auto-Discovery) 덕분에, 이 패키지를 설치한 사람은 어떤 설정도 없이 즉시 `Coupon::calculateDiscount($price, $coupon)` 파사드를 사용할 수 있습니다!

---

### 4단계: 라라벨 릴리스 주기 및 업그레이드 전략

1. **라라벨 릴리스 주기:**  
   - 매년 1분기(Q1)에 메이저 버전(10, 11, 12...)이 릴리스됩니다.
   - 버그 수정은 18개월, 보안 패치는 24개월 동안 공식 지원됩니다.
2. **무중단 업그레이드 전략:**  
   - [공식 업그레이드 가이드](../docs/01_prologue/upgrade_ko.md)를 꼼꼼히 확인하고 변경된 Breaking Changes를 검토합니다.
   - 자동 마이그레이션 도구인 **Laravel Shift**를 활용하거나 `composer update` 후 `php artisan test`를 돌려 모든 테스트가 녹색 불인지 확인합니다.

---

### 5단계: 오픈소스 라라벨 기여하기 (Contributions)

라라벨 프레임워크나 공식 문서의 오타 또는 새로운 기능을 제안하고 싶다면 [라라벨 깃허브 리포지토리(laravel/framework)](https://github.com/laravel/framework)에 PR을 제출할 수 있습니다:
1. 기능 추가는 `master` 브랜치로, 버그 패치는 현재 안정화 브랜치(예: `11.x`)로 PR을 보냅니다.
2. 반드시 변경 사항을 검증하는 PHPUnit/Pest 테스트 코드를 동봉해야 합니다.
3. 코딩 표준은 `laravel/pint`를 실행하여 100% 라라벨 코드 스타일 규칙을 준수합니다.

---

## 🎊 지니샵(JinyShop) 14주 완성 기념 피날레

🐱 **지니**: "도로시, 토토! 1주차 환경 설정과 아티산 CLI부터 시작해서, 블레이드, Eloquent ORM, 복합 연관관계, 장바구니 세션, 인증/인가, 파일 스토리지, 코어 아키텍처, 비동기 큐/이벤트, 스케줄러, Redis 캐시, Reverb 실시간 웹소켓, Sanctum API, AI SDK, 그리고 자동화 테스트와 무중단 배포까지... 라라벨 공식 문서 103개 전 주제를 완벽하게 녹여낸 1등 온라인 서점 **지니샵(JinyShop)**이 탄생했단다!"  
👧 **도로시**: "지니 선배님 덕분에 단순한 코더가 아니라, 견고하고 아름다운 소프트웨어 아키텍처를 설계하는 진짜 풀스택 엔지니어로 성장할 수 있었어! 너무 감사해!"  
🐶 **토토**: "멍멍! 지니샵 웹사이트에 접속자가 폭주해도 우리는 끄떡없다멍! 배포 성공이다멍!"  

---

## 🔍 라라벨 공식 문서 원리 심층 분석

### 1. OPcache 최적화 설정 (`php.ini`)

배포 서버에서 PHP의 성능을 극대화하려면 바이트코드를 메모리에 영구 저장하는 OPcache 활성화가 필수적입니다:

```ini
opcache.enable=1
opcache.memory_consumption=256
opcache.max_accelerated_files=20000
opcache.validate_timestamps=0 ; 코드 변경 감지 비활성화 (배포 시 PHP-FPM 리로드로 갱신)
```

### 2. 유지보수 모드(Maintenance Mode)의 비밀

만약 대규모 DB 스키마 변경으로 잠시 점검 화면을 띄워야 한다면 `php artisan down`을 실행합니다:

```bash
php artisan down --secret="jinypassword" --render="errors.maintenance"
```
관리자는 브라우저에서 `https://jinyshop.com/jinypassword`로 접속하여 점검 중에도 관리자 화면을 자유롭게 점검할 수 있습니다!

---

## 🐶 토토의 트러블슈팅 & 주의사항

1. **`storage` 폴더 권한 부여:**  
   배포 후 `The stream or file ".../laravel.log" could not be opened: failed to open stream: Permission denied` 에러가 난다면 웹 서버 사용자(`www-data`)에게 쓰기 권한이 없는 것입니다:
   ```bash
   sudo chown -R www-data:www-data storage bootstrap/cache
   sudo chmod -R 775 storage bootstrap/cache
   ```
2. **배포 직후 큐 워커 재시작 필수:**  
   큐 워커(`queue:work`)는 메모리에 이전 코드를 물고 있으므로, 배포 스크립트 끝에서 반드시 `php artisan queue:restart`를 날려주어야 새 코드로 작업을 처리합니다!

---

## 💡 자가진단 퀴즈 & 수료 최종 과제

1. **퀴즈:** 라라벨에서 설정, 라우트, 뷰, 이벤트 캐시를 프로덕션 성능 극대화를 위해 한 번에 묶어서 컴파일해 주는 Artisan 명령어는 무엇일까요?
   - 정답: `php artisan optimize`
2. **수료 최종 과제:** 완성된 지니샵 프로젝트에 `php artisan test`를 실행하여 모든 단위, 기능, 콘솔 테스트가 100% 통과하는지 확인하고, 최종 Git 태그(`v1.0.0`)를 생성하여 성공적인 런칭을 기념해 보세요!
{% endraw %}
