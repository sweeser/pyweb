from flask import Flask, request
import psycopg2
from psycopg2 import sql
from datetime import datetime

app = Flask(__name__)

# Подключение к базе данных
def get_db_connection():
    connection = psycopg2.connect(
        host="db",
        database="counter_db",
        user="postgres",
        password="postgres"
    )
    return connection

# Создание таблицы, если её еще нет
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS counter (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP,
            client_info TEXT
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

create_table()

@app.route('/')
def hello():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Получаем текущее время и информацию о клиенте
    current_time = datetime.now()
    client_info = request.headers.get('User-Agent')
    
    # Вставляем данные в таблицу
    cursor.execute(
        sql.SQL("INSERT INTO counter (datetime, client_info) VALUES (%s, %s)"),
        [current_time, client_info]
    )
    connection.commit()
    
    # Подсчитываем количество посещений
    cursor.execute("SELECT COUNT(*) FROM counter")
    count = cursor.fetchone()[0]
    
    cursor.close()
    connection.close()
    
    return f'Hello World! I have been seen {count} times.\n'

if __name__ == '__main__':
    app.run(host="0.0.0.0")