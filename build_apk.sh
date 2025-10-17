#!/bin/bash

echo "🚀 Начинаю компиляцию Android APK..."
echo ""

echo "⚠️  ВНИМАНИЕ:"
echo "Компиляция APK на Replit может не работать из-за ограничений среды."
echo "Рекомендуется компилировать локально на Ubuntu/Debian или через GitHub Actions."
echo ""

read -p "Продолжить попытку компиляции? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Компиляция отменена."
    exit 1
fi

echo ""
echo "📦 Проверка buildozer..."
if ! command -v buildozer &> /dev/null
then
    echo "❌ buildozer не найден. Устанавливаю..."
    pip install --user buildozer cython
fi

echo ""
echo "🔧 Очистка предыдущих сборок..."
buildozer android clean

echo ""
echo "🏗️  Компиляция APK (это может занять 20-40 минут)..."
echo "📥 Buildozer автоматически скачает Android SDK/NDK при первом запуске"
echo ""

buildozer -v android debug

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ APK успешно скомпилирован!"
    echo "📱 Файл находится в папке: bin/"
    ls -lh bin/*.apk
else
    echo ""
    echo "❌ Ошибка при компиляции APK"
    echo ""
    echo "💡 Возможные решения:"
    echo "1. Попробуйте локальную компиляцию на Ubuntu/Debian"
    echo "2. Используйте Docker с образом kivy/buildozer"
    echo "3. Настройте GitHub Actions (см. README.md)"
    echo "4. Используйте Google Colab"
    echo ""
    echo "📖 Подробные инструкции в README.md"
    exit 1
fi
