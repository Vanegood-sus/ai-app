# Компиляция APK через Google Colab

## Шаги:

1. Открой: https://colab.research.google.com/
2. Создай новый notebook
3. Вставь этот код:

```python
!git clone https://github.com/<твой-репозиторий>/ai-assistant.git
%cd ai-assistant
!apt-get update
!apt-get install -y openjdk-17-jdk
!pip install buildozer cython
!buildozer android debug
!ls -lh bin/*.apk
```

4. Запусти все ячейки
5. APK будет в папке `bin/` - скачай его

## Скачать APK:
```python
from google.colab import files
files.download('bin/aiassistant-1.0-arm64-v8a-debug.apk')
```
