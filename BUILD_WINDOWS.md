# Инструкция по сборке APK на Windows

## Быстрый старт с WSL

### 1. Установка WSL

Откройте PowerShell от имени администратора и выполните:

```powershell
wsl --install
```

Или установите Ubuntu из Microsoft Store.

После установки перезагрузите компьютер.

### 2. Откройте Ubuntu (WSL)

В меню Пуск найдите "Ubuntu" и запустите.

### 3. Обновите систему и установите зависимости

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

### 4. Установите Buildozer

```bash
pip3 install --user buildozer
```

Добавьте в PATH (добавьте в ~/.bashrc):
```bash
echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

### 5. Перейдите в папку проекта

```bash
cd /mnt/d/antenio9/html/tgmosaic
```

Или скопируйте проект в WSL:
```bash
cp -r /mnt/d/antenio9/html/tgmosaic ~/tgmosaic
cd ~/tgmosaic
```

### 6. Соберите APK

```bash
buildozer android debug
```

**Первая сборка займёт 30-60 минут** — Buildozer скачает Android SDK, NDK и все библиотеки.

### 7. Найдите готовый APK

После сборки APK будет в папке `bin/`:
```bash
ls -lh bin/*.apk
```

## Альтернатива: GitHub Actions (без установки на компьютер)

1. Создайте репозиторий на GitHub
2. Загрузите туда код
3. Создайте файл `.github/workflows/build.yml`:

```yaml
name: Build APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    - name: Install buildozer
      run: pip install buildozer
    - name: Build APK
      run: buildozer android debug
    - name: Upload APK
      uses: actions/upload-artifact@v2
      with:
        name: apk
        path: bin/*.apk
```

4. Запустите workflow — APK будет доступен для скачивания в разделе Actions

## Проблемы и решения

### Ошибка "command not found: buildozer"
```bash
export PATH=$PATH:~/.local/bin
```

### Ошибка с Java
```bash
sudo update-alternatives --config java
# Выберите Java 11
```

### Не хватает места на диске
Buildozer требует ~10-15 ГБ свободного места. Очистите кэш:
```bash
buildozer android clean
```

### Медленная сборка
Первая сборка всегда долгая. Последующие будут быстрее, так как зависимости уже скачаны.
