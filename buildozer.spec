[app]
title = TG Mosaic
package.name = tgmosaic
package.domain = com.tgmosaic
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,Pillow,androidstorage4kivy
# Явно НЕ указываем pyjnius — p4a сам его подтянет, но мы его подменим
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.0
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 34
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.gradle_dependencies = 'com.google.android.material:material:1.9.0'
android.accept_sdk_license = True
android.arch = arm64-v8a

# Отключаем сборку модулей, которые нам не нужны и вызывают ошибки
android.p4a_ignore = grp, lzma, uuid, pycrypto, pycparser
