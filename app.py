
import os
from flask import Flask, request
from datetime import datetime
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Получение URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/counter_db")

# Подключение к базе данных
conn = psycopg2.connect(DATABASE_URL)

# Создание таблицы, если она не существует
with conn.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS table_counter (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP NOT NULL,
            client_info TEXT NOT NULL
        );
    """)
    conn.commit()

@app.route('/')
def counter():
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now()

    # Сохранение данных о запросе в базу данных
    with conn.cursor() as cursor:
        insert_query = sql.SQL("""
            INSERT INTO table_counter (datetime, client_info)
            VALUES (%s, %s);
        """)
        cursor.execute(insert_query, (timestamp, user_agent))
        conn.commit()

    return f"Request saved at {timestamp} with client info: {user_agent}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
