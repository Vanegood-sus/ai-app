# AI Assistant - Android приложение с Pollinations.ai

Android приложение с функциями:
- 💬 AI чат через Pollinations.ai API
- 📸 OCR - распознавание текста с изображений
- 🔍 Анализ изображений
- 📝 Решение задач с фотографий

## 📦 Файлы проекта

- `main.py` - основное Kivy приложение
- `buildozer.spec` - конфигурация для создания APK
- `requirements.txt` - Python зависимости

## 🔨 Компиляция APK

### Способ 1: Локальная компиляция (Ubuntu/Debian)

```bash
# 1. Установите зависимости
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 2. Установите buildozer
pip3 install --user buildozer cython

# 3. Клонируйте этот проект
git clone <your-repo-url>
cd <project-folder>

# 4. Инициализируйте buildozer (если нужно)
buildozer init

# 5. Компилируйте APK (это займет 20-40 минут при первом запуске)
buildozer -v android debug

# APK файл будет в папке: bin/aiassistant-1.0-arm64-v8a-debug.apk
```

### Способ 2: Через Docker

```bash
# 1. Создайте Dockerfile
cat > Dockerfile << 'EOF'
FROM kivy/buildozer:latest
WORKDIR /app
COPY . /app
RUN buildozer android debug
EOF

# 2. Соберите и скомпилируйте
docker build -t ai-assistant-builder .
docker run -v $(pwd)/bin:/app/bin ai-assistant-builder
```

### Способ 3: Через GitHub Actions (автоматически)

Создайте файл `.github/workflows/build-apk.yml`:

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
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y openjdk-17-jdk
        pip install buildozer cython
    
    - name: Build APK
      run: buildozer -v android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: ai-assistant-apk
        path: bin/*.apk
```

После push в GitHub, APK будет автоматически собран и доступен в разделе Actions.

### Способ 4: Через online сервисы

1. **Replit** (текущий вариант) - компиляция может не работать
2. **Google Colab** - установите buildozer и скомпилируйте там
3. **Kivy Build Service** - https://kivy.org/

## 📱 Установка APK на телефон

1. Скопируйте APK файл на телефон
2. Разрешите установку из неизвестных источников
3. Откройте APK файл и установите

## 🚀 Использование приложения

После установки:

1. **AI Чат** - просто напишите сообщение в текстовое поле
2. **OCR** - нажмите кнопку "📸 OCR" и выберите изображение с текстом
3. **Анализ** - нажмите "🔍 Анализ" и выберите изображение для описания
4. **Решение задач** - нажмите "📝 Решить" и выберите фото с задачей

## 🔧 Технологии

- Python 3.11
- Kivy 2.3.0 (GUI framework)
- aiohttp (async HTTP запросы)
- Pollinations.ai API (бесплатный AI API)
- Buildozer (компиляция в APK)

## ⚠️ Важные замечания

1. **Первая компиляция** занимает 20-40 минут (скачивает Android SDK/NDK)
2. **Нужно минимум 10GB свободного места**
3. **На Replit** компиляция может не работать из-за ограничений
4. **Интернет** - приложению нужен интернет для работы AI API

## 📝 API

Приложение использует бесплатный API Pollinations.ai:
- Endpoint: `https://text.pollinations.ai/openai`
- Модель по умолчанию: `gpt-4o-mini`
- Без ограничений и ключей
- Поддержка изображений и текста

### Доступные модели Pollinations.ai:
- `gpt-4o-mini` (по умолчанию) - быстрая и эффективная
- `gpt-4o` - более мощная модель
- `claude-3-5-sonnet` - от Anthropic
- Другие модели - см. https://pollinations.ai/

### Как изменить модель:
В файле `main.py` измените переменную `API_MODEL`:
```python
class AIAssistantApp(App):
    API_MODEL = "gpt-4o"  # Измените на нужную модель
```

## 🐛 Проблемы при компиляции

### Ошибка: "Command failed: git..."
```bash
buildozer android clean
rm -rf .buildozer
buildozer -v android debug
```

### Ошибка: "SDK not found"
Buildozer автоматически скачает SDK при первом запуске.

### Ошибка: "No space left"
Нужно минимум 10GB свободного места.

## 📧 Контакты

Если нужна помощь - создайте issue в репозитории.
