#!/usr/bin/env python3
"""
Тестовый скрипт для проверки установки зависимостей
"""
import sys

print("🔍 Проверка установки зависимостей...")
print()

dependencies = {
    'kivy': 'Kivy GUI framework',
    'aiohttp': 'Async HTTP client',
    'certifi': 'SSL certificates',
    'buildozer': 'APK builder'
}

missing = []
installed = []

for module, description in dependencies.items():
    try:
        __import__(module)
        print(f"✅ {module:15} - {description}")
        installed.append(module)
    except ImportError:
        print(f"❌ {module:15} - {description} (НЕ УСТАНОВЛЕН)")
        missing.append(module)

print()
print(f"📊 Результат: {len(installed)}/{len(dependencies)} установлено")

if missing:
    print()
    print("⚠️  Отсутствуют модули:", ", ".join(missing))
    print("Установите их командой: pip install " + " ".join(missing))
    sys.exit(1)
else:
    print()
    print("✅ Все зависимости установлены!")
    print()
    print("📱 Для компиляции APK:")
    print("   ./build_apk.sh")
    print()
    print("⚠️  ВНИМАНИЕ: Компиляция APK на Replit может не работать.")
    print("   Рекомендуется компилировать локально или через GitHub Actions.")
    print("   См. README.md для подробных инструкций.")
    sys.exit(0)
