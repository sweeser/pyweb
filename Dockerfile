FROM python:3.9-slim

# Установка переменной окружения для Flask
ENV FLASK_APP=app.py

# Установка рабочей директории
WORKDIR /app

# Копирование всех остальных файлов приложения
COPY . .

# Копирование requirements.txt и установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Запуск приложения
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
