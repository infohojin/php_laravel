---
layout: docs
title: "File Storage"
---

{% raw %}
# File Storage

- [Introduction](#introduction)
- [Configuration](#configuration)
    - [The Local Driver](#the-local-driver)
    - [The Public Disk](#the-public-disk)
    - [Driver Prerequisites](#driver-prerequisites)
    - [Scoped, Read-Only, and Read-Through Filesystems](#scoped-and-read-only-filesystems)
    - [Amazon S3 Compatible Filesystems](#amazon-s3-compatible-filesystems)
- [Obtaining Disk Instances](#obtaining-disk-instances)
    - [On-Demand Disks](#on-demand-disks)
- [Retrieving Files](#retrieving-files)
    - [Downloading Files](#downloading-files)
    - [File URLs](#file-urls)
    - [Temporary URLs](#temporary-urls)
    - [File Metadata](#file-metadata)
- [Storing Files](#storing-files)
    - [Prepending and Appending To Files](#prepending-appending-to-files)
    - [Copying and Moving Files](#copying-moving-files)
    - [Automatic Streaming](#automatic-streaming)
    - [File Uploads](#file-uploads)
    - [File Visibility](#file-visibility)
    - [Image Manipulation](#image-manipulation)
- [Deleting Files](#deleting-files)
- [Directories](#directories)
- [Testing](#testing)
- [Custom Filesystems](#custom-filesystems)

<a name="introduction"></a>
## Introduction

Laravel provides a powerful filesystem abstraction thanks to the wonderful [Flysystem](https://github.com/thephpleague/flysystem) PHP package by Frank de Jonge. The Laravel Flysystem integration provides simple drivers for working with local filesystems, SFTP, and Amazon S3. Even better, it's amazingly simple to switch between these storage options between your local development machine and production server as the API remains the same for each system.

<a name="configuration"></a>
## Configuration

Laravel's filesystem configuration file is located at `config/filesystems.php`. Within this file, you may configure all of your filesystem "disks". Each disk represents a particular storage driver and storage location. Example configurations for each supported driver are included in the configuration file so you can modify the configuration to reflect your storage preferences and credentials.

The `local` driver interacts with files stored locally on the server running the Laravel application, while the `sftp` storage driver is used for SSH key-based FTP. The `s3` driver is used to write to Amazon's S3 cloud storage service.

> [!NOTE]
> You may configure as many disks as you like and may even have multiple disks that use the same driver.



<a name="the-local-driver"></a>
### 로컬 드라이버

`local` 드라이버를 사용할 때, 모든 파일 작업은 `filesystems` 구성 파일에 정의된 `root` 디렉토리를 기준으로 합니다. 기본적으로 이 값은 `storage/app/private` 디렉토리로 설정되어 있습니다. 따라서, 다음 방법은 `storage/app/private/example.txt`에 쓰게 됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('local')->put('example.txt', 'Contents');
```



<a name="the-public-disk"></a>
### 공개 디스크

응용 프로그램의 `filesystems` 구성 파일에 포함된 `public` 디스크는 공개적으로 접근 가능한 파일을 위한 것입니다. 기본적으로 `public` 디스크는 `local` 드라이버를 사용하며 파일을 `storage/app/public`에 저장합니다.

만약 `public` 디스크가 `local` 드라이버를 사용하며 이러한 파일을 웹에서 접근 가능하게 만들고 싶다면, 소스 디렉터리 `storage/app/public`에서 대상 디렉터리 `public/storage`로 심볼릭 링크를 생성해야 합니다:

심볼릭 링크를 생성하려면 `storage:link` Artisan 명령을 사용할 수 있습니다:

```shell
php artisan storage:link
```



파일이 저장되고 심볼릭 링크가 생성되면 `asset` 도우미를 사용하여 파일에 대한 URL을 생성할 수 있습니다:

```php
echo asset('storage/file.txt');
```



`filesystems` 구성 파일에서 추가 심볼릭 링크를 구성할 수 있습니다. 구성된 각 링크는 `storage:link` 명령을 실행할 때 생성됩니다:

```php
'links' => [
    public_path('storage') => storage_path('app/public'),
    public_path('images') => storage_path('app/images'),
],
```



`storage:unlink` 명령은 구성된 심볼릭 링크를 삭제하는 데 사용할 수 있습니다:

```shell
php artisan storage:unlink
```



<a name="driver-prerequisites"></a>
### 드라이버 사전 요구사항

<a name="s3-driver-configuration"></a>
#### S3 드라이버 구성

S3 드라이버를 사용하기 전에, Composer 패키지 관리자를 통해 Flysystem S3 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-aws-s3-v3 "^3.0" --with-all-dependencies
```



S3 디스크 구성 배열은 `config/filesystems.php` 구성 파일에 위치해 있습니다. 일반적으로 S3 정보 및 자격 증명은 `config/filesystems.php` 구성 파일에서 참조하는 다음 환경 변수를 사용하여 구성해야 합니다:

```ini
AWS_ACCESS_KEY_ID=<your-key-id>
AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=<your-bucket-name>
AWS_USE_PATH_STYLE_ENDPOINT=false
```



편의를 위해, 이러한 환경 변수들은 AWS CLI에서 사용하는 명명 규칙과 일치합니다.

<a name="ftp-driver-configuration"></a>
#### FTP 드라이버 구성

FTP 드라이버를 사용하기 전에, Composer 패키지 관리자를 통해 Flysystem FTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-ftp "^3.0"
```



Laravel의 Flysystem 통합은 FTP와 잘 작동하지만, 프레임워크의 기본 `config/filesystems.php` 구성 파일에는 샘플 구성이 포함되어 있지 않습니다. FTP 파일 시스템을 구성해야 하는 경우 아래의 구성 예제를 사용할 수 있습니다:

```php
'ftp' => [
    'driver' => 'ftp',
    'host' => env('FTP_HOST'),
    'username' => env('FTP_USERNAME'),
    'password' => env('FTP_PASSWORD'),

    // Optional FTP Settings...
    // 'port' => env('FTP_PORT', 21),
    // 'root' => env('FTP_ROOT'),
    // 'passive' => true,
    // 'ssl' => true,
    // 'timeout' => 30,
],
```



<a name="sftp-driver-configuration"></a>
#### SFTP 드라이버 구성

SFTP 드라이버를 사용하기 전에, Composer 패키지 관리자를 통해 Flysystem SFTP 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-sftp-v3 "^3.0"
```



라라벨의 Flysystem 통합은 SFTP와 잘 작동합니다. 그러나 샘플 구성은 프레임워크의 기본 `config/filesystems.php` 구성 파일에 포함되어 있지 않습니다. SFTP 파일 시스템을 구성해야 하는 경우, 아래의 구성 예제를 사용할 수 있습니다:

```php
'sftp' => [
    'driver' => 'sftp',
    'host' => env('SFTP_HOST'),

    // Settings for basic authentication...
    'username' => env('SFTP_USERNAME'),
    'password' => env('SFTP_PASSWORD'),

    // Settings for SSH key-based authentication with encryption password...
    'privateKey' => env('SFTP_PRIVATE_KEY'),
    'passphrase' => env('SFTP_PASSPHRASE'),

    // Settings for file / directory permissions...
    'visibility' => 'private', // `private` = 0600, `public` = 0644
    'directory_visibility' => 'private', // `private` = 0700, `public` = 0755

    // Optional SFTP Settings...
    // 'hostFingerprint' => env('SFTP_HOST_FINGERPRINT'),
    // 'maxTries' => 4,
    // 'passphrase' => env('SFTP_PASSPHRASE'),
    // 'port' => env('SFTP_PORT', 22),
    // 'root' => env('SFTP_ROOT', ''),
    // 'timeout' => 30,
    // 'useAgent' => true,
],
```



<a name="scoped-and-read-only-filesystems"></a>
### 스코프 지정, 읽기 전용 및 읽기 통과 파일 시스템

스코프 지정 디스크를 사용하면 모든 경로가 지정된 경로 접두사로 자동으로 시작되는 파일 시스템을 정의할 수 있습니다. 스코프 지정 파일 시스템 디스크를 생성하기 전에 Composer 패키지 관리자를 통해 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-path-prefixing "^3.0"
```



`scoped` 드라이버를 사용하는 디스크를 정의하여 기존 파일 시스템 디스크의 경로 범위 인스턴스를 생성할 수 있습니다. 예를 들어, 기존 `s3` 디스크를 특정 경로 접두사로 범위 지정하는 디스크를 생성할 수 있으며, 그런 다음 범위 지정된 디스크를 사용하는 모든 파일 작업은 지정된 접두사를 사용하게 됩니다:

```php
's3-videos' => [
    'driver' => 'scoped',
    'disk' => 's3',
    'prefix' => 'path/to/videos',
],
```



"읽기 전용" 디스크는 쓰기 작업을 허용하지 않는 파일시스템 디스크를 생성할 수 있게 해줍니다. `read-only` 구성 옵션을 사용하기 전에, Composer 패키지 관리자를 통해 추가 Flysystem 패키지를 설치해야 합니다:

```shell
composer require league/flysystem-read-only "^3.0"
```



다음으로, 하나 이상의 디스크 구성 배열에 `read-only` 구성 옵션을 포함할 수 있습니다:

```php
's3-videos' => [
    'driver' => 's3',
    // ...
    'read-only' => true,
],
```



리드스루 디스크를 사용하면 다운타임 없이 디스크 간 파일을 마이그레이션할 수 있습니다. 파일을 읽을 때, Laravel은 먼저 기본 디스크를 확인합니다. 파일이 오직 대체 디스크에만 존재하는 경우, Laravel은 대체 디스크에서 파일을 읽고 향후 요청을 위해 해당 파일을 기본 디스크로 복사합니다:

```php
'assets' => [
    'driver' => 'read-through',
    'primary' => 's3',
    'fallback' => 'legacy-s3',
],
```



Writes and directory listings target the primary disk. File existence and metadata checks use either disk without copying files to the primary disk. If copying a fallback file to the primary disk fails, the read still succeeds by default. To throw an exception instead, set the `throw_on_promotion_failure` configuration option to `true`.

<a name="amazon-s3-compatible-filesystems"></a>
### Amazon S3 Compatible Filesystems

By default, your application's `filesystems` configuration file contains a disk configuration for the `s3` disk. In addition to using this disk to interact with [Amazon S3](https://aws.amazon.com/s3/), you may use it to interact with any S3-compatible file storage service such as [RustFS](https://github.com/rustfs/rustfs), [DigitalOcean Spaces](https://www.digitalocean.com/products/spaces/), [Vultr Object Storage](https://www.vultr.com/products/object-storage/), [Cloudflare R2](https://www.cloudflare.com/developer-platform/products/r2/), or [Hetzner Cloud Storage](https://www.hetzner.com/storage/object-storage/).

Typically, after updating the disk's credentials to match the credentials of the service you are planning to use, you only need to update the value of the `endpoint` configuration option. This option's value is typically defined via the `AWS_ENDPOINT` environment variable:

```php
'endpoint' => env('AWS_ENDPOINT', 'https://rustfs:9000'),
```



<a name="obtaining-disk-instances"></a>
## 디스크 인스턴스 얻기

`Storage` 퍼사드를 사용하여 구성된 디스크와 상호작용할 수 있습니다. 예를 들어, 기본 디스크에 아바타를 저장하기 위해 퍼사드에서 `put` 메서드를 사용할 수 있습니다. 먼저 `disk` 메서드를 호출하지 않고 `Storage` 퍼사드에서 메서드를 호출하면, 해당 메서드는 자동으로 기본 디스크로 전달됩니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('avatars/1', $content);
```



애플리케이션이 여러 디스크와 상호작용하는 경우 특정 디스크의 파일을 작업하기 위해 `Storage` 퍼사드에서 `disk` 메서드를 사용할 수 있습니다:

```php
Storage::disk('s3')->put('avatars/1', $content);
```



<a name="on-demand-disks"></a>
### 온디맨드 디스크

때때로 애플리케이션의 `filesystems` 설정 파일에 해당 구성 파일이 실제로 존재하지 않더라도 주어진 구성을 사용하여 런타임에 디스크를 생성하고 싶을 수 있습니다. 이를 달성하기 위해, `Storage` 퍼사드의 `build` 메서드에 구성 배열을 전달할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$disk = Storage::build([
    'driver' => 'local',
    'root' => '/path/to/root',
]);

$disk->put('image.jpg', $content);
```



<a name="retrieving-files"></a>
## 파일 가져오기

`get` 메서드는 파일의 내용을 가져오는 데 사용될 수 있습니다. 해당 파일의 원시 문자열 내용이 메서드에 의해 반환될 것입니다. 모든 파일 경로는 디스크의 "루트" 위치를 기준으로 지정해야 한다는 점을 기억하세요:

```php
$contents = Storage::get('file.jpg');
```



조회하려는 파일에 JSON이 포함되어 있는 경우, `json` 방법을 사용하여 파일을 조회하고 그 내용을 디코딩할 수 있습니다:

```php
$orders = Storage::json('orders.json');
```



`exists` 방법은 디스크에 파일이 존재하는지 확인하는 데 사용될 수 있습니다:

```php
if (Storage::disk('s3')->exists('file.jpg')) {
    // ...
}
```



`missing` 방법은 파일이 디스크에서 누락되었는지 여부를 확인하는 데 사용할 수 있습니다:

```php
if (Storage::disk('s3')->missing('file.jpg')) {
    // ...
}
```



<a name="downloading-files"></a>
### 파일 다운로드

`download` 메서드는 사용자의 브라우저가 지정된 경로의 파일을 다운로드하도록 강제하는 응답을 생성하는 데 사용할 수 있습니다. `download` 메서드는 두 번째 인수로 파일 이름을 받아, 사용자가 파일을 다운로드할 때 보게 되는 파일 이름을 결정합니다. 마지막으로, 메서드의 세 번째 인수로 HTTP 헤더 배열을 전달할 수 있습니다:

```php
return Storage::download('file.jpg');

return Storage::download('file.jpg', $name, $headers);
```



<a name="file-urls"></a>
### 파일 URL

주어진 파일의 URL을 얻기 위해 `url` 방법을 사용할 수 있습니다. `local` 드라이버를 사용하는 경우, 일반적으로 주어진 경로 앞에 `/storage`를 붙이고 파일에 대한 상대 URL을 반환합니다. `s3` 드라이버를 사용하는 경우, 전체 자격을 갖춘 원격 URL이 반환됩니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::url('file.jpg');
```



`local` 드라이버를 사용할 때, 공개적으로 접근할 수 있어야 하는 모든 파일은 `storage/app/public` 디렉토리에 배치해야 합니다. 또한, `storage/app/public` 디렉토리를 가리키는 [심볼릭 링크](#the-public-disk)를 `public/storage`에 생성해야 합니다.

> [!WARNING]
> `local` 드라이버를 사용할 때, `url`의 반환 값은 URL 인코딩되지 않습니다. 이로 인해, 항상 유효한 URL을 생성할 수 있는 이름으로 파일을 저장하는 것을 권장합니다.

<a name="url-host-customization"></a>
#### URL 호스트 사용자 정의

`Storage` 퍼사드를 사용하여 생성된 URL의 호스트를 변경하고자 하는 경우, 디스크 구성 배열에서 `url` 옵션을 추가하거나 변경할 수 있습니다:

```php
'public' => [
    'driver' => 'local',
    'root' => storage_path('app/public'),
    'url' => env('APP_URL').'/storage',
    'visibility' => 'public',
    'throw' => false,
],
```



<a name="temporary-urls"></a>
### 임시 URL

`temporaryUrl` 방법을 사용하면 `local` 및 `s3` 드라이버를 사용하여 저장된 파일에 대한 임시 URL을 생성할 수 있습니다. 이 방법은 경로와 URL이 만료될 시점을 지정하는 `DateTime` 인스턴스를 허용합니다:

```php
use Illuminate\Support\Facades\Storage;

$url = Storage::temporaryUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```



<a name="enabling-local-temporary-urls"></a>
#### 로컬 임시 URL 활성화

만약 임시 URL 지원이 `local` 드라이버에 도입되기 전에 애플리케이션 개발을 시작했다면, 로컬 임시 URL을 활성화해야 할 수도 있습니다. 그렇게 하려면 `config/filesystems.php` 구성 파일 내의 `local` 디스크 구성 배열에 `serve` 옵션을 추가하십시오:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app/private'),
    'serve' => true, // [tl! add]
    'throw' => false,
],
```



<a name="s3-request-parameters"></a>
#### S3 요청 매개변수

추가 [S3 요청 매개변수](https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html#RESTObjectGET-requests)를 지정해야 하는 경우, `temporaryUrl` 메서드의 세 번째 인수로 요청 매개변수 배열을 전달할 수 있습니다:

```php
$url = Storage::temporaryUrl(
    'file.jpg',
    now()->plus(minutes: 5),
    [
        'ResponseContentType' => 'application/octet-stream',
        'ResponseContentDisposition' => 'attachment; filename=file2.jpg',
    ]
);
```



<a name="customizing-temporary-urls"></a>
#### 임시 URL 사용자 지정

특정 스토리지 디스크에 대해 임시 URL이 생성되는 방식을 사용자 지정해야 하는 경우, `buildTemporaryUrlsUsing` 메서드를 사용할 수 있습니다. 예를 들어, 일반적으로 임시 URL을 지원하지 않는 디스크를 통해 저장된 파일을 다운로드할 수 있는 컨트롤러가 있는 경우에 유용할 수 있습니다. 일반적으로 이 메서드는 서비스 제공자의 `boot` 메서드에서 호출되어야 합니다:

```php
<?php

namespace App\Providers;

use DateTime;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\URL;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Storage::disk('local')->buildTemporaryUrlsUsing(
            function (string $path, DateTime $expiration, array $options) {
                return URL::temporarySignedRoute(
                    'files.download',
                    $expiration,
                    array_merge($options, ['path' => $path])
                );
            }
        );
    }
}
```



<a name="temporary-upload-urls"></a>
#### 임시 업로드 URL

> [!WARNING]
> 임시 업로드 URL을 생성할 수 있는 기능은 `s3` 및 `local` 드라이버에서만 지원됩니다.

클라이언트 측 애플리케이션에서 파일을 직접 업로드하는 데 사용할 수 있는 임시 URL을 생성해야 하는 경우, `temporaryUploadUrl` 메서드를 사용할 수 있습니다. 이 메서드는 경로와 URL 만료 시간을 지정하는 `DateTime` 인스턴스를 받아들입니다. `temporaryUploadUrl` 메서드는 업로드 URL과 업로드 요청 시 포함해야 하는 헤더를 구조 분해할 수 있는 연관 배열을 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

['url' => $url, 'headers' => $headers] = Storage::temporaryUploadUrl(
    'file.jpg', now()->plus(minutes: 5)
);
```



이 방법은 클라이언트 측 애플리케이션이 Amazon S3와 같은 클라우드 스토리지 시스템에 파일을 직접 업로드해야 하는 서버리스 환경에서 주로 유용합니다.

<a name="file-metadata"></a>
### 파일 메타데이터

파일을 읽고 쓰는 것 외에도, Laravel은 파일 자체에 대한 정보도 제공할 수 있습니다. 예를 들어, `size` 메서드를 사용하여 파일의 크기를 바이트 단위로 가져올 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$size = Storage::size('file.jpg');
```



`lastModified` 메서드는 파일이 마지막으로 수정된 시간의 UNIX 타임스탬프를 반환합니다:

```php
$time = Storage::lastModified('file.jpg');
```



주어진 파일의 MIME 타입은 `mimeType` 방법을 통해 얻을 수 있습니다:

```php
$mime = Storage::mimeType('file.jpg');
```



<a name="file-paths"></a>
#### 파일 경로

주어진 파일의 경로를 가져오기 위해 `path` 방법을 사용할 수 있습니다. `local` 드라이버를 사용하는 경우, 이 방법은 파일의 절대 경로를 반환합니다. `s3` 드라이버를 사용하는 경우, 이 방법은 S3 버킷 내 파일의 상대 경로를 반환합니다:

```php
use Illuminate\Support\Facades\Storage;

$path = Storage::path('file.jpg');
```



<a name="storing-files"></a>
## 파일 저장

`put` 방법은 디스크에 파일 내용을 저장하는 데 사용할 수 있습니다. 또한 `resource` PHP를 `put` 메서드에 전달할 수 있으며, 이 메서드는 Flysystem의 기본 스트림 지원을 사용합니다. 모든 파일 경로는 디스크에 구성된 "루트" 위치를 기준으로 지정해야 합니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents);

Storage::put('file.jpg', $resource);
```



<a name="failed-writes"></a>
#### 쓰기 실패

만약 `put` 메서드(또는 다른 '쓰기' 연산)가 파일을 디스크에 쓸 수 없다면, `false`가 반환됩니다:

```php
if (! Storage::put('file.jpg', $contents)) {
    // The file could not be written to disk...
}
```



원하신다면 파일시스템 디스크의 구성 배열 내에서 `throw` 옵션을 정의할 수 있습니다. 이 옵션이 `true`로 정의되면, `put`와 같은 "쓰기" 메서드는 쓰기 작업이 실패할 경우 `League\Flysystem\UnableToWriteFile` 인스턴스를 발생시킵니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'throw' => true,
],
```



또는 파일시스템 디스크의 구성 배열 내에서 `report` 옵션을 정의할 수 있습니다. 이 옵션이 `true`로 정의되면, Laravel은 '쓰기' 작업이 실패할 때 예외를 발생시키거나 쓰기 작업의 반환 값을 중단하지 않고, 애플리케이션의 예외 처리기를 사용하여 기본 예외를 기록합니다:

```php
'public' => [
    'driver' => 'local',
    // ...
    'report' => true,
],
```



`throw`나 `report` 옵션이 정의되지 않은 경우, 디스크는 실패 시 조용히 `false`를 반환하며 기본 예외는 발생하거나 기록되지 않습니다.

<a name="prepending-appending-to-files"></a>
### 파일에 앞에 추가 및 뒤에 추가하기

`prepend`와 `append` 메서드를 사용하면 파일의 시작 또는 끝에 쓸 수 있습니다:

```php
Storage::prepend('file.log', 'Prepended Text');

Storage::append('file.log', 'Appended Text');
```



<a name="copying-moving-files"></a>
### 파일 복사 및 이동

`copy` 방법은 기존 파일을 디스크의 새 위치로 복사하는 데 사용할 수 있으며, `move` 방법은 기존 파일의 이름을 바꾸거나 새 위치로 이동하는 데 사용할 수 있습니다:

```php
Storage::copy('old/file.jpg', 'new/file.jpg');

Storage::move('old/file.jpg', 'new/file.jpg');
```



파일을 다른 디스크로 복사하거나 이동하려면 `copyToDisk` 및 `moveToDisk` 방법을 사용할 수 있습니다. 세 번째 인수를 제공하지 않으면 원본 파일의 경로가 대상 디스크에서 사용됩니다:

```php
Storage::disk('local')->copyToDisk('s3', 'reports/report.csv');

Storage::disk('local')->moveToDisk(
    's3', 'reports/report.csv', 'archive/report.csv'
);
```



<a name="automatic-streaming"></a>
### 자동 스트리밍

파일을 스토리지로 스트리밍하면 메모리 사용량을 크게 줄일 수 있습니다. Laravel이 주어진 파일을 자동으로 스토리지 위치로 스트리밍하도록 하려면 `putFile` 또는 `putFileAs` 메서드를 사용할 수 있습니다. 이 메서드는 `Illuminate\Http\File` 또는 `Illuminate\Http\UploadedFile` 인스턴스를 받아 원하는 위치로 파일을 자동으로 스트리밍합니다:

```php
use Illuminate\Http\File;
use Illuminate\Support\Facades\Storage;

// Automatically generate a unique ID for filename...
$path = Storage::putFile('photos', new File('/path/to/photo'));

// Manually specify a filename...
$path = Storage::putFileAs('photos', new File('/path/to/photo'), 'photo.jpg');
```



`putFile` 메서드에 대해 몇 가지 중요한 점을 주의할 필요가 있습니다. 디렉토리 이름만 지정했으며 파일 이름은 지정하지 않았다는 점을 유의하세요. 기본적으로 `putFile` 메서드는 파일 이름으로 사용할 고유 ID를 생성합니다. 파일의 확장자는 파일의 MIME 유형을 검사하여 결정됩니다. 파일 경로는 `putFile` 메서드에 의해 반환되므로, 생성된 파일 이름을 포함한 경로를 데이터베이스에 저장할 수 있습니다.

`putFile` 및 `putFileAs` 메서드도 저장된 파일의 "가시성"을 지정할 수 있는 인수를 받습니다. 이는 특히 Amazon S3와 같은 클라우드 디스크에 파일을 저장하고, 생성된 URL을 통해 파일을 공개적으로 접근 가능하게 하고자 할 때 유용합니다.

```php
Storage::putFile('photos', new File('/path/to/photo'), 'public');
```



<a name="file-uploads"></a>
### 파일 업로드

웹 애플리케이션에서 파일을 저장하는 가장 일반적인 사용 사례 중 하나는 사진이나 문서와 같은 사용자가 업로드한 파일을 저장하는 것입니다. Laravel은 업로드된 파일 인스턴스에서 `store` 메서드를 사용하여 파일을 쉽게 저장할 수 있게 해줍니다. 업로드된 파일을 저장하고자 하는 경로와 함께 `store` 메서드를 호출하세요:

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserAvatarController extends Controller
{
    /**
     * Update the avatar for the user.
     */
    public function update(Request $request): string
    {
        $path = $request->file('avatar')->store('avatars');

        return $path;
    }
}
```



이 예제에 대해 몇 가지 중요한 점을 주목할 필요가 있습니다. 디렉터리 이름만 지정했을 뿐 파일 이름은 지정하지 않았음을 주의하세요. 기본적으로 `store` 메서드는 파일 이름으로 사용할 고유 ID를 생성합니다. 파일의 확장자는 파일의 MIME 유형을 확인하여 결정됩니다. 파일 경로는 `store` 메서드에 의해 반환되므로 생성된 파일 이름을 포함한 경로를 데이터베이스에 저장할 수 있습니다.

또한 `Storage` 퍼사드에서 `putFile` 메서드를 호출하여 위 예제와 동일한 파일 저장 작업을 수행할 수 있습니다:

```php
$path = Storage::putFile('avatars', $request->file('avatar'));
```



<a name="specifying-a-file-name"></a>
#### 파일 이름 지정

저장된 파일에 자동으로 파일 이름이 지정되는 것을 원하지 않는 경우, 경로, 파일 이름 및 (선택 사항) 디스크를 인수로 받는 `storeAs` 메서드를 사용할 수 있습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars', $request->user()->id
);
```



위 예제와 동일한 파일 저장 작업을 수행하는 `Storage` 퍼사드에서 `putFileAs` 메서드를 사용할 수도 있습니다:

```php
$path = Storage::putFileAs(
    'avatars', $request->file('avatar'), $request->user()->id
);
```



> [!WARNING]
> 인쇄할 수 없거나 잘못된 유니코드 문자는 파일 경로에서 자동으로 제거됩니다. 따라서 Laravel의 파일 저장 메서드에 전달하기 전에 파일 경로를 정리하는 것이 좋습니다. 파일 경로는 `League\Flysystem\WhitespacePathNormalizer::normalizePath` 메서드를 사용하여 정규화됩니다.

<a name="specifying-a-disk"></a>
#### 디스크 지정

기본적으로 이 업로드된 파일의 `store` 메서드는 기본 디스크를 사용합니다. 다른 디스크를 지정하려면 `store` 메서드의 두 번째 인수로 디스크 이름을 전달하십시오:

```php
$path = $request->file('avatar')->store(
    'avatars/'.$request->user()->id, 's3'
);
```



`storeAs` 방법을 사용하고 있다면, 디스크 이름을 메서드의 세 번째 인수로 전달할 수 있습니다:

```php
$path = $request->file('avatar')->storeAs(
    'avatars',
    $request->user()->id,
    's3'
);
```



<a name="other-uploaded-file-information"></a>
#### 다른 업로드된 파일 정보

업로드된 파일의 원래 이름과 확장자를 확인하고 싶다면, `getClientOriginalName` 및 `getClientOriginalExtension` 메서드를 사용하여 확인할 수 있습니다:

```php
$file = $request->file('avatar');

$name = $file->getClientOriginalName();
$extension = $file->getClientOriginalExtension();
```



그러나 `getClientOriginalName` 및 `getClientOriginalExtension` 방법은 파일 이름과 확장자가 악의적인 사용자에 의해 조작될 수 있으므로 안전하지 않은 것으로 간주된다는 점을 명심하십시오. 이러한 이유로 일반적으로 주어진 파일 업로드에 대한 이름과 확장자를 얻기 위해 `hashName` 및 `extension` 방법을 사용하는 것이 좋습니다:

```php
$file = $request->file('avatar');

$name = $file->hashName(); // Generate a unique, random name...
$extension = $file->extension(); // Determine the file's extension based on the file's MIME type...
```



<a name="file-visibility"></a>
### 파일 가시성

Laravel의 Flysystem 통합에서 "가시성"은 여러 플랫폼에 걸친 파일 권한의 추상화입니다. 파일은 `public` 또는 `private`로 선언될 수 있습니다. 파일이 `public`로 선언되면 일반적으로 다른 사람들이 파일에 접근할 수 있어야 함을 나타냅니다. 예를 들어, S3 드라이버를 사용할 때 `public` 파일의 URL을 가져올 수 있습니다.

파일을 작성할 때 `put` 메서드를 통해 가시성을 설정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::put('file.jpg', $contents, 'public');
```



파일이 이미 저장되어 있는 경우, 그 가시성은 `getVisibility`와 `setVisibility` 메서드를 통해 가져오고 설정할 수 있습니다:

```php
$visibility = Storage::getVisibility('file.jpg');

Storage::setVisibility('file.jpg', 'public');
```



업로드된 파일과 상호 작용할 때, 업로드된 파일을 `public` 가시성으로 저장하기 위해 `storePublicly` 및 `storePubliclyAs` 방법을 사용할 수 있습니다:

```php
$path = $request->file('avatar')->storePublicly('avatars', 's3');

$path = $request->file('avatar')->storePubliclyAs(
    'avatars',
    $request->user()->id,
    's3'
);
```



<a name="image-manipulation"></a>
### 이미지 조작

업로드한 이미지를 저장하기 전에 크기를 조정하거나 자르거나 변환해야 하는 경우, Laravel의 [이미지 조작 기능](/docs/{{version}}/images)을 사용할 수 있습니다:

```php
$path = $request->image('avatar')
    ->cover(400, 400)
    ->toWebp()
    ->storePublicly('avatars', 'public');
```



이미 파일 시스템 디스크 중 하나에 저장된 파일에서 이미지 인스턴스를 생성할 수도 있습니다:

```php
$image = Storage::disk('public')->image('avatars/photo.jpg');
```



<a name="local-files-and-visibility"></a>
#### 로컬 파일과 가시성

`local` 드라이버를 사용할 때, `public` [가시성](#file-visibility)은 디렉토리에 대한 `0755` 권한과 파일에 대한 `0644` 권한으로 변환됩니다. 애플리케이션의 `filesystems` 구성 파일에서 권한 매핑을 수정할 수 있습니다:

```php
'local' => [
    'driver' => 'local',
    'root' => storage_path('app'),
    'permissions' => [
        'file' => [
            'public' => 0644,
            'private' => 0600,
        ],
        'dir' => [
            'public' => 0755,
            'private' => 0700,
        ],
    ],
    'throw' => false,
],
```



<a name="deleting-files"></a>
## 파일 삭제

`delete` 메서드는 삭제할 단일 파일 이름이나 파일 배열을 받습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::delete('file.jpg');

Storage::delete(['file.jpg', 'file2.jpg']);
```



필요한 경우, 파일을 삭제할 디스크를 지정할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

Storage::disk('s3')->delete('path/file.jpg');
```



<a name="directories"></a>
## 디렉토리

<a name="get-all-files-within-a-directory"></a>
#### 디렉토리 내 모든 파일 가져오기

`files` 메서드는 주어진 디렉토리 내 모든 파일의 배열을 반환합니다. 하위 디렉토리를 포함하여 주어진 디렉토리 내 모든 파일 목록을 가져오려면 `allFiles` 메서드를 사용할 수 있습니다:

```php
use Illuminate\Support\Facades\Storage;

$files = Storage::files($directory);

$files = Storage::allFiles($directory);
```



<a name="get-all-directories-within-a-directory"></a>
#### 디렉토리 내 모든 디렉토리 가져오기

`directories` 메서드는 주어진 디렉토리 내 모든 디렉토리의 배열을 반환합니다. 만약 하위 디렉토리를 포함하여 주어진 디렉토리 내 모든 디렉토리 목록을 가져오고 싶다면, `allDirectories` 메서드를 사용할 수 있습니다:

```php
$directories = Storage::directories($directory);

$directories = Storage::allDirectories($directory);
```



<a name="create-a-directory"></a>
#### 디렉토리 생성

`makeDirectory` 메서드는 필요한 모든 하위 디렉토리를 포함하여 지정된 디렉토리를 생성합니다:

```php
Storage::makeDirectory($directory);
```



<a name="delete-a-directory"></a>
#### 디렉토리 삭제

마지막으로, `deleteDirectory` 메서드를 사용하여 디렉토리와 그 안의 모든 파일을 제거할 수 있습니다:

```php
Storage::deleteDirectory($directory);
```



<a name="testing"></a>
## 테스트

`Storage` 퍼사드의 `fake` 메서드를 사용하면 `Illuminate\Http\UploadedFile` 클래스의 파일 생성 유틸리티와 결합하여 파일 업로드 테스트를 훨씬 쉽게 할 수 있는 가짜 디스크를 쉽게 생성할 수 있습니다. 예를 들어:```php tab=Pest
<?php

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

test('albums can be uploaded', function () {
    Storage::fake('photos');

    $response = $this->json('POST', '/photos', [
        UploadedFile::fake()->image('photo1.jpg'),
        UploadedFile::fake()->image('photo2.jpg')
    ]);

    // Assert one or more files were stored...
    Storage::disk('photos')->assertExists('photo1.jpg');
    Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

    // Assert one or more files were not stored...
    Storage::disk('photos')->assertMissing('missing.jpg');
    Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

    // Assert that the number of files in a given directory matches the expected count...
    Storage::disk('photos')->assertCount('/wallpapers', 2);

    // Assert that a given directory is empty...
    Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

    // Assert that the disk contains no files...
    Storage::disk('photos')->assertEmpty();
});
```

```php tab=PHPUnit
<?php

namespace Tests\Feature;

use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class ExampleTest extends TestCase
{
    public function test_albums_can_be_uploaded(): void
    {
        Storage::fake('photos');

        $response = $this->json('POST', '/photos', [
            UploadedFile::fake()->image('photo1.jpg'),
            UploadedFile::fake()->image('photo2.jpg')
        ]);

        // Assert one or more files were stored...
        Storage::disk('photos')->assertExists('photo1.jpg');
        Storage::disk('photos')->assertExists(['photo1.jpg', 'photo2.jpg']);

        // Assert one or more files were not stored...
        Storage::disk('photos')->assertMissing('missing.jpg');
        Storage::disk('photos')->assertMissing(['missing.jpg', 'non-existing.jpg']);

        // Assert that the number of files in a given directory matches the expected count...
        Storage::disk('photos')->assertCount('/wallpapers', 2);

        // Assert that a given directory is empty...
        Storage::disk('photos')->assertDirectoryEmpty('/wallpapers');

        // Assert that the disk contains no files...
        Storage::disk('photos')->assertEmpty();
    }
}
```



기본적으로 `fake` 메서드는 임시 디렉토리의 모든 파일을 삭제합니다. 이 파일들을 유지하고 싶다면 대신 "persistentFake" 메서드를 사용할 수 있습니다. 파일 업로드 테스트에 대한 자세한 내용은 [HTTP 테스트 문서의 파일 업로드 관련 정보](/docs/{{version}}/http-tests#testing-file-uploads)를 참조하십시오.

> [!WARNING]
> `image` 메서드는 [GD 확장](https://www.php.net/manual/en/book.image.php)을 필요로 합니다.

<a name="custom-filesystems"></a>
## 사용자 정의 파일 시스템

Laravel의 Flysystem 통합은 몇 가지 "드라이버"를 기본적으로 지원합니다. 그러나 Flysystem은 이에 제한되지 않으며, 다른 많은 저장 시스템에 대한 어댑터도 갖추고 있습니다. Laravel 애플리케이션에서 이러한 추가 어댑터 중 하나를 사용하려면 사용자 정의 드라이버를 만들 수 있습니다.

사용자 정의 파일 시스템을 정의하려면 Flysystem 어댑터가 필요합니다. 프로젝트에 커뮤니티가 관리하는 Dropbox 어댑터를 추가해봅시다:

```shell
composer require spatie/flysystem-dropbox
```



다음으로, 애플리케이션의 [서비스 제공자](/docs/{{version}}/providers) 중 하나의 `boot` 메서드 내에서 드라이버를 등록할 수 있습니다. 이를 수행하기 위해서는 `Storage` 파사드의 `extend` 메서드를 사용해야 합니다:

```php
<?php

namespace App\Providers;

use Illuminate\Contracts\Foundation\Application;
use Illuminate\Filesystem\FilesystemAdapter;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\ServiceProvider;
use League\Flysystem\Filesystem;
use Spatie\Dropbox\Client as DropboxClient;
use Spatie\FlysystemDropbox\DropboxAdapter;

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
        Storage::extend('dropbox', function (Application $app, array $config) {
            $adapter = new DropboxAdapter(new DropboxClient(
                $config['authorization_token']
            ));

            return new FilesystemAdapter(
                new Filesystem($adapter, $config),
                $adapter,
                $config
            );
        });
    }
}
```

`extend` 메서드의 첫 번째 인수는 드라이버의 이름이고, 두 번째 인수는 `$app`와 `$config` 변수를 받는 클로저입니다. 클로저는 `Illuminate\Filesystem\FilesystemAdapter` 인스턴스를 반환해야 합니다. `$config` 변수에는 지정된 디스크에 대해 `config/filesystems.php`에서 정의된 값들이 들어 있습니다.

확장 프로그램의 서비스 공급자를 생성하고 등록한 후에는 `config/filesystems.php` 구성 파일에서 `dropbox` 드라이버를 사용할 수 있습니다.
{% endraw %}
