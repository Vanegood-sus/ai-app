# AI Assistant - Android приложение

## 📱 Описание проекта

Android приложение с AI функциями, использующее Pollinations.ai API:
- 💬 AI чат
- 📸 OCR (распознавание текста)  
- 🔍 Анализ изображений
- 📝 Решение задач с фотографий

## 🏗️ Структура проекта

```
.
├── main.py              # Основное Kivy приложение
├── buildozer.spec       # Конфигурация для APK
├── build_apk.sh         # Скрипт компиляции APK
├── requirements.txt     # Python зависимости
└── README.md           # Полная документация
```

## 🔨 Компиляция APK

### ⚠️ Важно
Компиляция APK на Replit **не работает** из-за:
- Отсутствия Android SDK/NDK
- Нехватки ресурсов (нужно 10GB+)
- Ограничений среды NixOS

### ✅ Рабочие способы:

1. **Локальная компиляция** (Ubuntu/Debian):
   ```bash
   chmod +x build_apk.sh
   ./build_apk.sh
   ```

2. **GitHub Actions** (автоматически):
   - Создайте `.github/workflows/build-apk.yml`
   - Push в GitHub
   - APK появится в разделе Actions

3. **Docker**:
   ```bash
   docker run -v $(pwd):/app kivy/buildozer buildozer android debug
   ```

## 🚀 Использование

После компиляции APK:
1. Скопируйте `bin/*.apk` на телефон
2. Установите (разрешите установку из неизвестных источников)
3. Запустите приложение

## 🛠️ Технологии

- **Python 3.11** - язык программирования
- **Kivy 2.3.0** - GUI framework для Android
- **Pollinations.ai** - бесплатный AI API
- **Buildozer** - инструмент компиляции APK
- **aiohttp** - асинхронные HTTP запросы

## 📝 API

Приложение использует Pollinations.ai API без ключей:
- URL: `https://text.pollinations.ai/openai`
- Бесплатно
- Поддерживает текст и изображения

## 🔧 Разработка

### Тестирование локально
```bash
python main.py
```

### Компиляция APK
```bash
./build_apk.sh
```

## 📚 Документация

Полная документация в [README.md](README.md)

## ⏱️ История изменений

- 2025-01-17: Создан проект на базе Telegram бота
- Заменен g4f на Pollinations.ai API
- Создан GUI интерфейс с Kivy
- Настроен buildozer для APK

## 🎯 Следующие шаги

- [x] Создать Kivy приложение
- [x] Заменить g4f на Pollinations.ai
- [x] Настроить buildozer
- [ ] Протестировать APK на реальном устройстве
- [ ] Добавить кэширование результатов
- [ ] Улучшить UI/UX
