# TG Mosaic — нарезка картинки на плитки 100×100 для эмодзи в Telegram

Программа делит горизонтальную картинку на плитки 100×100 пикселей для склейки как эмодзи в Telegram.

## Возможности

- Делит картинку по длине (ширине) на куски по 100 px
- Сохраняет пропорции изображения (не растягивает)
- Высота фиксируется 100 px с пропорциональным масштабированием ширины
- Последний неполный кусок дополняется прозрачностью
- Работает на Windows/Linux (tkinter) и Android (Kivy)

## Установка для Windows/Linux

1. Установите зависимости:
```bash
pip install pillow
```

2. Запустите:
```bash
python tgmosaic.py
```

## Сборка APK для Android

### 🚀 Простой способ (Windows) — GitHub Actions

**Ничего устанавливать не нужно!** Сборка происходит в облаке.

1. Загрузите код на GitHub (см. `BUILD_SIMPLE.md`)
2. Откройте раздел **Actions** в репозитории
3. Нажмите **"Run workflow"**
4. Подождите 30-60 минут
5. Скачайте APK из раздела **Artifacts**

Подробная инструкция: см. `BUILD_SIMPLE.md`

### Альтернативные варианты

- **WSL** (Ubuntu в Windows) — см. `BUILD_WINDOWS.md`
- **Google Colab** — сборка в браузере (см. `BUILD_SIMPLE.md`)
- **Linux/macOS** — используйте buildozer напрямую (см. ниже)

### Сборка на Linux/macOS

```bash
pip install buildozer
sudo apt update  # Ubuntu/Debian
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
buildozer android debug
```

### Сборка APK

1. Перейдите в папку проекта:
```bash
cd tgmosaic
```

2. Инициализируйте buildozer (если нужно):
```bash
buildozer init
```

3. Соберите APK:
```bash
buildozer android debug
```

APK будет в папке `bin/`.

Для release-версии (подписанной):
```bash
buildozer android release
```

### Первая сборка

Первая сборка может занять 30-60 минут, так как Buildozer скачает и соберёт все зависимости (Android SDK, NDK, Python, библиотеки).

## Использование

1. Выберите изображение (кнопка "Обзор")
2. Выберите папку для сохранения плиток
3. Нажмите "Нарезать"
4. Плитки сохранятся как `tile_0.png`, `tile_1.png`, и т.д.

## Структура проекта

- `tgmosaic.py` — основная логика нарезки + GUI на tkinter (Windows/Linux)
- `main.py` — GUI на Kivy для Android
- `buildozer.spec` — конфигурация для сборки APK
- `requirements.txt` — зависимости Python

## Примечания

- На Android плитки сохраняются в `/sdcard/Download/tgmosaic_tiles/` или во внутреннее хранилище приложения
- Для работы на Android нужны разрешения на чтение/запись файлов (запрашиваются автоматически)
