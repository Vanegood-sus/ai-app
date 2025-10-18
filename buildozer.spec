[app]

title = AI Assistant
package.name = aiassistant
package.domain = org.pollinations

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

# ИСПРАВЛЕНО: убран aiohttp, добавлен requests (работает на Android)
requirements = python3,kivy,requests,urllib3,certifi,charset-normalizer,idna,pillow

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA

android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

android.archs = arm64-v8a,armeabi-v7a

android.manifest.intent_filters = 

android.entrypoint = org.kivy.android.PythonActivity
android.app_theme = @android:style/Theme.NoTitleBar

services = 

p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 1

build_dir = ./.buildozer
bin_dir = ./bin
