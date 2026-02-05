# Простая сборка APK на Windows (без установки Linux)

## Вариант 1: GitHub Actions (Рекомендуется) ⭐

**Ничего устанавливать не нужно!** Сборка происходит в облаке на GitHub.

### Шаги:

1. **Создайте аккаунт на GitHub** (если нет): https://github.com

2. **Создайте новый репозиторий**:
   - Нажмите "New repository"
   - Название: `tgmosaic` (или любое другое)
   - Выберите "Public" или "Private"
   - НЕ ставьте галочки на README, .gitignore и т.д.

3. **Загрузите код в репозиторий**:

   Откройте PowerShell или командную строку в папке проекта:
   ```powershell
   cd D:\antenio9\html\tgmosaic
   
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/ВАШ_ЛОГИН/tgmosaic.git
   git push -u origin main
   ```

   Или используйте GitHub Desktop (проще):
   - Скачайте: https://desktop.github.com
   - File → Add Local Repository
   - Выберите папку `D:\antenio9\html\tgmosaic`
   - Publish repository

4. **Запустите сборку**:
   - Откройте репозиторий на GitHub
   - Перейдите в раздел **Actions**
   - Нажмите **"Run workflow"** → **"Run workflow"**
   - Подождите 30-60 минут (первая сборка)

5. **Скачайте APK**:
   - После завершения сборки откройте последний workflow run
   - В разделе **Artifacts** нажмите **"tgmosaic-apk"**
   - Скачайте ZIP с APK файлом

### Готово! 🎉

APK будет в скачанном ZIP файле. Установите его на Android устройство.

---

## Вариант 2: Онлайн-сервисы

### Google Colab (бесплатно)

1. Откройте: https://colab.research.google.com
2. Создайте новый notebook
3. Выполните команды:

```python
!pip install buildozer
!apt-get update
!apt-get install -y git zip unzip openjdk-11-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Загрузите файлы проекта
from google.colab import files
uploaded = files.upload()

# Распакуйте если нужно
!unzip -q your_project.zip

# Соберите APK
!cd your_project && buildozer android debug

# Скачайте APK
files.download('your_project/bin/*.apk')
```

---

## Вариант 3: Готовый APK

Если нужен готовый APK прямо сейчас, можно:
- Попросить кого-то собрать на Linux
- Использовать онлайн-сервисы сборки APK (платные)
- Использовать готовые решения типа App Inventor (но там нужно переписывать код)

---

## Какой вариант выбрать?

- **GitHub Actions** — самый простой, бесплатный, автоматический
- **Google Colab** — если не хотите создавать репозиторий
- **Готовый APK** — если нужен прямо сейчас

Рекомендую **GitHub Actions** — один раз настроил, и потом можно собирать APK одной кнопкой!
