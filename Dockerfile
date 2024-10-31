FROM python:3.8-slim
WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Установка зависимостей
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Копирование файлов приложения
COPY . .

# Запуск приложения
CMD ["flask", "run"]