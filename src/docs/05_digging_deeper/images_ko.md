---
layout: docs
title: "이미지 조작"
---

{% raw %}
# 이미지 조작

- [인트로듀션](#introduction)
- [설치](#installation)
- [구성](#configuration)
- [이미지 읽기](#reading-images)
- [업로드된 파일](#uploaded-files)
- 스토리지 파일 (#storage-files)
- [기타 출처](#other-sources)
- [이미지 조작](#manipulating-images)
- 리사이징 이미지 (#resizing-images)
- [기타 변형](#other-transformations)
- 인코딩 이미지 (#encoding-images)
- 이미지 저장 (#storing-images)
- [이미지 검사](#inspecting-images)
- [이미지 드라이버](#image-drivers)
- 커스텀 이미지 드라이버 (#custom-image-drivers)
- [커스텀 변환](#custom-transformations)

<a name="introduction"></a>
## 소개

Laravel 은 프레임워크 전반에서 찾을 수 있는 동일한 표현 규칙을 사용하여 이미지의 크기를 조정하고， 자르고， 인코딩하고， 저장할 수 있는 원활한 이미지 조작 API 를 제공합니다. Laravel 의 이미지 기능은 [Intervention Image](https://image.intervention.io/) 로 구동되며 GD 및 Imagick PHP 확장을 지원합니다。

이미지 API 는 업로드된 파일， Laravel [파일시스템 디스크](/docs/{{version}}/filesystem) 에 저장된 파일， 로컬 파일， 원격 URL 또는 원시 이미지 바이트로 작업할 때 유용합니다：

```php
use Illuminate\Support\Facades\Image;

$path = Image::fromStorage('avatars/photo.jpg', 'public')
    ->cover(400, 400)
    ->toWebp()
    ->quality(80)
    ->storePublicly('avatars', 'public');

```

> [!WARNING]
> 이미지 조작은 CPU와 메모리를 많이 사용할 수 있습니다. 업로드를 받는 HTTP 요청 동안 수행하는 대신 [대기열 작업](/docs/{{version}}/queues)에서 대규모 이미지 처리 작업을 수행하는 것을 고려하세요.

<a name="installation"></a>
## 설치

Laravel의 이미지 조작 기능을 사용하기 전에 Composer를 통해 Intervention Image 패키지를 설치하세요:

```shell
composer require intervention/image:^4.0

```

응용 프로그램이 사용할 드라이버에 따라 PHP 설치에 GD 또는 Imagick 확장 모듈이 설치되어 있는지 확인해야 합니다.

<a name="configuration"></a>
### 구성

Laravel의 이미지 구성 파일은 `config/images.php`에 위치해 있습니다. 응용 프로그램에 `images` 구성 파일이 없는 경우, `config:publish` Artisan 명령어를 사용하여 이를 퍼블리시할 수 있습니다:

```shell
php artisan config:publish images

```

이미지 구성 파일을 통해 애플리케이션의 기본 이미지 드라이버를 지정할 수 있습니다. 또한 `IMAGE_DRIVER` 환경 변수를 사용하여 기본 드라이버를 지정할 수도 있습니다. 지원되는 드라이버는 `gd`와 `imagick`입니다:

```ini
IMAGE_DRIVER=imagick

```

<a name="reading-images"></a>
## 이미지 읽기

`Image` 외부 인터페이스는 일반적인 소스에서 이미지를 읽기 위한 여러 메서드를 제공합니다. 이미지 내용은 지연 로드되므로, 이미지가 처리되거나 해당 바이트가 요청될 때까지 소스가 일반적으로 읽히지 않습니다.

<a name="uploaded-files"></a>
### 업로드된 파일

`image` 메서드를 사용하여 들어오는 요청에서 업로드된 이미지를 가져올 수 있습니다. 이 메서드는 업로드된 파일에 대해 `Illuminate\Image\Image` 인스턴스를 반환하거나, 파일이 없으면 `null`를 반환합니다:

```php
use Illuminate\Http\Request;

Route::post('/avatar', function (Request $request) {
    $request->validate(['avatar' => ['required', 'image']]);

    $path = $request->image('avatar')
        ->cover(400, 400)
        ->toWebp()
        ->storePublicly('avatars', 'public');

    // ...
});

```

또는 `fromUpload` 메서드를 사용하여 `Illuminate\Http\UploadedFile` 인스턴스로부터 이미지 인스턴스를 생성할 수 있습니다:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromUpload($request->file('avatar'));

```

업로드된 파일에서 이미지가 생성되면, 다음 `file` 메서드를 사용하여 기본 업로드된 파일을 가져올 수 있습니다:

```php
$file = $image->file();

```

<a name="storage-files"></a>
### 저장 파일

`fromStorage` 메서드를 사용하여 애플리케이션의 [파일 시스템 디스크](/docs/{{version}}/filesystem)에 저장된 파일에서 이미지 인스턴스를 생성할 수 있습니다. 첫 번째 인자는 파일 경로이고, 두 번째 인자는 디스크 이름입니다:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromStorage('avatars/photo.jpg', disk: 'public');

```



`image` 방법을 사용하여 파일 시스템 디스크 인스턴스에서 직접 이미지 인스턴스를 생성할 수도 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$image = Storage::disk('public')->image('avatars/photo.jpg');

```

<a name="other-sources"></a>
### 기타 소스

`Image` 외관에는 원시 바이트, 로컬 파일 경로, 원격 URL 및 Base64 인코딩 문자열에서 이미지 인스턴스를 생성하는 메서드도 포함되어 있습니다:

```php
use Illuminate\Support\Facades\Image;

$image = Image::fromBytes($contents);
$image = Image::fromBase64($base64);
$image = Image::fromPath(storage_path('app/avatars/photo.jpg'));
$image = Image::fromUrl('https://example.com/photo.jpg');

```

<a name="manipulating-images"></a>
## 이미지 조작

이미지 인스턴스는 불변입니다. 각 조작 메서드는 변환이 처리 파이프라인에 추가된 새로운 이미지 인스턴스를 반환하므로, 메서드를 유연하게 체인으로 연결할 수 있습니다:

```php
$image = $request->image('avatar')
    ->orient()
    ->cover(400, 400)
    ->sharpen(10);

```

변환은 이미지 파이프라인에 추가된 순서대로 처리되며, 이미지는 마지막에 한 번만 인코딩됩니다.

<a name="resizing-images"></a>
### 이미지 크기 조정

`resize` 메서드는 이미지를 지정된 크기로 조정합니다. 너비와 높이를 모두 제공할 수 있으며, 이름을 지정한 인수를 사용하여 한 개의 치수만 제공할 수도 있습니다:

```php
$image = $image->resize(800, 600);
$image = $image->resize(width: 800);
$image = $image->resize(height: 600);

```



`scale` 방법은 주어진 치수 내에 맞도록 이미지를 비례적으로 축소합니다. 이 방법은 결코 이미지 크기를 증가시키지 않습니다:

```php
$image = $image->scale(800, 600);
$image = $image->scale(width: 800);
$image = $image->scale(height: 600);

```



`cover` 방법은 주어진 크기를 완전히 덮도록 이미지를 크기 조정하고 자릅니다:

```php
$image = $image->cover(400, 400);

```



`contain` 방식은 이미지를 전체적으로 보존하면서 주어진 크기에 맞게 이미지 크기를 조정합니다. 필요할 경우 선택적 배경 색상을 사용하여 빈 공간을 채울 수 있습니다:

```php
$image = $image->contain(400, 400);
$image = $image->contain(400, 400, '#ffffff');
$image = $image->contain(400, 400, 'dominant');

```

빈 공간을 이미지의 지배적인 색상으로 채우기 위해 배경색으로 `dominant`를 지정할 수 있습니다.

`crop` 방법을 사용하여 이미지를 자를 수 있습니다. 처음 두 인수는 원하는 너비와 높이이며, 선택적 세 번째 및 네 번째 인수는 자르기의 `x` 및 `y` 좌표를 지정합니다:

```php
$image = $image->crop(300, 200);
$image = $image->crop(300, 200, x: 50, y: 25);

```

<a name="other-transformations"></a>
### 기타 변환

Laravel은 또한 다양한 추가 이미지 변환 방법도 제공합니다:

```php
$image = $image->orient();
$image = $image->rotate(90);
$image = $image->rotate(90, '#ffffff');
$image = $image->rotate(90, 'dominant');
$image = $image->blur(5);
$image = $image->grayscale();
$image = $image->sharpen(10);
$image = $image->flipVertically();
$image = $image->flipHorizontally();

```



`orient` 메서드는 이미지의 EXIF 방향 데이터를 기준으로 이미지를 회전시킵니다. `rotate` 메서드는 이미지를 지정된 각도만큼 시계 방향으로 회전시키며, 선택적으로 배경색을 지정할 수 있습니다. `blur` 및 `sharpen` 메서드는 `0`와 `100` 사이의 값을 허용합니다.

<a name="conditional-transformations"></a>
#### 조건부 변환

이미지 인스턴스는 Laravel의 `Conditionable` 트레이트를 지원하며, `when` 및 `unless` 메서드를 사용하여 조건부로 변환을 적용할 수 있습니다:

```php
$image = $request->image('avatar')
    ->when($request->boolean('crop'), fn ($image) => $image->cover(400, 400))
    ->unless($request->boolean('preserve_format'), fn ($image) => $image->toWebp());

```

<a name="encoding-images"></a>
## 이미지 인코딩

기본적으로, 처리된 이미지는 원래 형식을 사용하여 인코딩됩니다. 그러나 이미지를 가져오거나 저장하기 전에 다른 지원되는 형식으로 변환할 수 있습니다:

```php
$image = $image->toWebp();
$image = $image->toJpg();
$image = $image->toJpeg();
$image = $image->toPng();
$image = $image->toGif();
$image = $image->toAvif();
$image = $image->toBmp();

```

출력 품질을 설정하기 위해 `quality` 방법을 사용할 수 있습니다. 품질은 `1`와 `100` 사이로 제한됩니다:

```php
$image = $image->toWebp()->quality(80);

```



`optimize` 방법은 이미지를 주어진 형식으로 변환하고 품질을 설정하는 편리한 단축키입니다. 기본적으로 이미지는 품질 `70`로 WebP 이미지로 최적화됩니다:

```php
$image = $image->optimize();

$image = $image->optimize(format: 'jpg', quality: 85);

```

처리된 이미지 내용을 바이트 문자열, Base64로 인코딩된 문자열, 또는 데이터 URI로 가져올 수 있습니다:

```php
$bytes = $image->toBytes();
$base64 = $image->toBase64();
$dataUri = $image->toDataUri();

```

이미지 인스턴스는 데이터 URI를 가져오기 위해 문자열로 캐스팅될 수도 있습니다:

```php
$dataUri = (string) $image;

```

<a name="storing-images"></a>
## 이미지 저장

`store` 방법은 처리된 이미지를 애플리케이션의 파일 시스템 디스크 중 하나에 저장합니다. 업로드된 파일과 마찬가지로, Laravel은 고유한 파일 이름을 생성하고 저장된 경로를 반환합니다. 두 번째 인수는 디스크를 지정하는 데 사용될 수 있습니다:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->store(path: 'avatars', disk: 's3');

```

저장된 파일 이름을 지정하려면 `storeAs` 방법을 사용할 수 있습니다:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storeAs(path: 'avatars', name: 'avatar.jpg', disk: 'public');

```



`storePublicly` 및 `storePubliclyAs` 방법은 이미지를 `public` 가시성으로 저장합니다:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePublicly(path: 'avatars', disk: 'public');

$path = $request->image('avatar')
    ->cover(400, 400)
    ->storePubliclyAs(path: 'avatars', name: 'avatar.webp', disk: 'public');

```

이미지를 저장할 수 없는 경우, 저장 방법은 `false`를 반환합니다.

<a name="inspecting-images"></a>
## 이미지 검사

다음 방법을 사용하여 이미지의 MIME 타입, 확장자, 크기, 너비, 높이 및 주요 색상을 가져올 수 있습니다:

```php
$mimeType = $image->mimeType();
$extension = $image->extension();

[$width, $height] = $image->dimensions();
$width = $image->width();
$height = $image->height();

$dominantColor = $image->dominantColor();

```

이 메서드들은 처리된 이미지에서 작동합니다. 예를 들어, `cover(400, 400)` 호출 후 `width`를 호출하면 `400`를 반환합니다.

<a name="image-drivers"></a>
## 이미지 드라이버

<a name="custom-image-drivers"></a>
### 사용자 정의 이미지 드라이버

Laravel의 이미지 관리자는 Laravel의 기본 `Illuminate\Support\Manager` 클래스를 확장합니다. 이는 이미지 관리자에서 사용할 수 있는 `extend` 메서드와 `Image` 파사드를 사용하여 사용자 정의 이미지 드라이버를 등록할 수 있음을 의미합니다.

사용자 정의 이미지 드라이버는 `Illuminate\Contracts\Image\Driver` 인터페이스를 구현해야 합니다. `process` 메서드는 원본 이미지 내용과 이미지에 적용되어야 하는 순서화된 `Illuminate\Image\ImagePipeline`를 받으며, 처리된 이미지 바이트를 반환해야 합니다:

```php
<?php

namespace App\Images;

use Illuminate\Contracts\Image\Driver;
use Illuminate\Image\ImagePipeline;

class VipsDriver implements Driver
{
    /**
     * Process the given image contents with the specified pipeline.
     */
    public function process(string $contents, ImagePipeline $pipeline): string
    {
        // Apply the pipeline's transformations and output options...

        return $contents;
    }

    /**
     * Register a transformation handler.
     */
    public function transformUsing(string $transformation, callable $callback): static
    {
        // Store the handler so it may be applied while processing the pipeline...

        return $this;
    }
}

```

> [!NOTE]
> 커스텀 이미지 드라이버를 구현하는 방법을 더 잘 이해하려면, 프레임워크의 내장 `Illuminate\Image\Drivers\InterventionDriver` 클래스를 검토할 수 있습니다.

커스텀 드라이버를 구현한 후에는 `Image` 파사드의 `extend` 메서드를 사용하여 등록할 수 있습니다. 일반적으로 이는 서비스 제공자의 `boot` 메서드에서 수행해야 합니다:

```php
use App\Images\VipsDriver;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Support\Facades\Image;

/**
 * Bootstrap any application services.
 */
public function boot(): void
{
    Image::extend('vips', function (Application $app) {
        return new VipsDriver;
    });
}

```

드라이버를 등록한 후, `using` 메서드를 사용하여 특정 이미지에 사용할 수 있습니다:

```php
$image = $request->image('avatar')
    ->using('vips')
    ->cover(400, 400);

```

애플리케이션의 `config/images.php` 구성 파일 또는 `IMAGE_DRIVER` 환경 변수를 사용하여 `default` 옵션으로 사용자 지정 드라이버를 애플리케이션의 기본 이미지 드라이버로 구성할 수도 있습니다:

```ini
IMAGE_DRIVER=vips

```

<a name="custom-transformations"></a>
### 사용자 정의 변환

애플리케이션과 패키지는 `Illuminate\Contracts\Image\Transformation` 계약을 구현하는 클래스를 생성하여 사용자 정의 변환을 정의할 수 있습니다. 그런 다음 사용자 정의 변환을 `transform` 메서드를 사용하여 이미지 파이프라인에 추가할 수 있습니다:

```php
<?php

namespace App\Images\Transformations;

use Illuminate\Contracts\Image\Transformation;

class Pixelate implements Transformation
{
    public function __construct(
        public readonly int $size,
    ) {
        //
    }
}

```

다음으로, `Image` 퍼사드의 `transformUsing` 메서드를 사용하여 변환과 드라이버에 대한 핸들러를 등록합니다. 일반적으로 이것은 서비스 제공자의 `boot` 메서드에서 수행해야 합니다:

```php
use App\Images\Transformations\Pixelate;
use Illuminate\Support\Facades\Image;
use Intervention\Image\Interfaces\ImageInterface;

Image::transformUsing('gd', Pixelate::class, function (ImageInterface $image, Pixelate $transformation) {
    return $image->pixelate($transformation->size);
});

```

변환 핸들러가 등록되면 이미지를 변환에 적용할 수 있습니다:

```php
use App\Images\Transformations\Pixelate;

$image = $request->image('avatar')
    ->transform(new Pixelate(12))
    ->store('avatars');

```
{% endraw %}
