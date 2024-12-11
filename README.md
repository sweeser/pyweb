Отчет по лабораторной работе: Развертывание Flask-приложения с PostgreSQL и Docker Compose
----------------
Цель: развернуть приложения-счетчик, созданного с использованием Flask и PostgreSQL.
----------------
Структура проекта
----------------
app.py: основной файл приложения Flask.
Dockerfile: файл для сборки Docker-образа Flask-приложения.
docker-compose.yml: файл для определения всех сервисов, включая Flask, PostgreSQL и PgAdmin.
requirements.txt: файл с зависимостями Python.
----------------
Шаги выполнения
1. app.py
Создаем приложение которое по запросу на корневом адресе сохраняет время и IP-адрес в базу данных PostgreSQL.
----------------
2. requirements.txt
Создаем файл с зависимостями Python.
----------------
3. Dockerfile
Dockerfile используется для создания Docker-образа приложения Flask. Он устанавливает все необходимые зависимости, копирует файлы приложения и запускает его:
----------------
4. docker-compose.yml
Файл docker-compose.yml используется для определения всех сервисов (база данных, веб-приложение и PgAdmin) и их взаимодействия между собой:
----------------
version: '3'
services:
   db:
      image: postgres:13
      environment:
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
         POSTGRES_DB: counter_db
      ports:
         - "5432:5432"
      volumes:
         - db_data:/var/lib/postgresql/data

   web:
      build: .
      ports:
         - "5000:5000"
      environment:
         DATABASE_URL: postgres://user:password@db:5432/counter_db
      depends_on:
         - db

   pgadmin:
      image: dpage/pgadmin4
      environment:
         PGADMIN_DEFAULT_EMAIL: admin@example.com
         PGADMIN_DEFAULT_PASSWORD: admin
      ports:
         - "8080:80"
      depends_on:
         - db

volumes:
   db_data:
----------------
PgAdmin используется для удобного предоставления содержимого бд.
----------------
docker exec -it flasklab-db-1 bash
----------------
psql -U user -d counter_db
----------------
SELECT * FROM table_counter
----------------
Шаги для развертывания
Сборка и запуск контейнеров 
Выполните следующую команду для сборки и запуска всех контейнеров:
----------------
docker-compose up --build - Эта команда создаст контейнеры для PostgreSQL, веб-приложения Flask и PgAdmin, а также свяжет их в одной сети.
----------------
Доступ к веб-приложению Приложение Flask будет доступно по следующему адресу:
http://localhost:5000/
При переходе по этому адресу будет сделан запрос, который сохранит данные о пользователе и времени запроса в бд.
----------------
Доступ к PgAdmin Для удобного управления базой данных используйте PgAdmin, доступный по следующему адресу:
http://localhost:8080/
----------------
Войдите в систему с учетными данными:
Email: admin@example.com
Password: admin
Добавьте новое подключение к базе данных:
Host name/address: db (это имя сервиса в docker-compose.yml)
Port: 5432
Username: user
Password: password
----------------
Проверка данных в базе
Для проверки данных, сохраненных в базе данных, вы можете использовать интерфейс PgAdmin или выполнить команду для подключения к контейнеру базы данных и использовать psql:
----------------
docker-compose exec db psql -U user -d counter_db
Внутри psql выполните следующий запрос для отображения всех записей:
----------------
SELECT * FROM table_counter;
