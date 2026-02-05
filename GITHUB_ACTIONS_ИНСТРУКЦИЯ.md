# Что делать на странице GitHub Actions

## На экране «Get started with GitHub Actions»

1. **Нажмите:** «Skip this and set up a workflow yourself»  
   (Пропустить и настроить workflow самостоятельно)

2. Откроется список workflow. Должен появиться **«Build Android APK»** — это наш workflow из папки `.github/workflows/build_apk.yml`.

3. **Если «Build Android APK» есть в списке слева:**
   - Нажмите на него
   - Справа нажмите **«Run workflow»** (Запустить workflow)
   - Ещё раз **«Run workflow»** в выпадающем меню
   - Дождитесь окончания сборки (30–60 минут), затем скачайте APK в разделе **Artifacts**

4. **Если «Build Android APK» нет** (файл workflow не загружен в репозиторий):
   - Нажмите **«New workflow»** (Новый workflow)
   - Слева выберите **«set up a workflow yourself»**
   - В имени файла укажите: `build_apk.yml`  
     (полный путь должен быть: `.github/workflows/build_apk.yml`)
   - Вставьте содержимое из файла `.github/workflows/build_apk.yml` из вашего проекта
   - Нажмите **«Start commit»** → **«Commit new file»**
   - После этого в списке слева появится **«Build Android APK»** — запустите его, как в пункте 3

## Итого

- **Не выбирайте** ни «Simple workflow», ни «Deploy», ни другие шаблоны из списка.
- Нужен только наш workflow **«Build Android APK»**: либо он уже есть (если вы загрузили проект с папкой `.github`), либо его нужно один раз создать вручную, как в пункте 4.
