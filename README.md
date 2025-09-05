# DimaTechTest

**Инструкция по запуску в докере:**
1. Клонировать репозиторий -> git clone git@github.com:ELesten/DimaTechTest.git
2. Запустить контейнеры -> docker compose up
3. Перейти по маршруту http://127.0.0.1:8000/api/v1/docs для ознакомления с эндпоинтами. При желании, там же можно авторизоваться и тестировать

**Инструкция по запуску без докера:**
1. Клонировать репозиторий -> git clone git@github.com:ELesten/DimaTechTest.git
2. Создать и настроить виртуальное окружение
3. Установить зависимости -> pip install -r requirements.txt
4. Создать базу данных с переменными из .env файла
5. Применить миграции -> alembic upgrade head
6. Запустить приложение -> uvicorn main:app --reload
7. Перейти по маршруту http://127.0.0.1:8000/api/v1/docs для ознакомления с эндпоинтами. При желании, там же можно авторизоваться и тестировать.

**Тестовые пользователи:**

**admin:**

-email: "admin@example.com"

-password: "admin"

**user**:

-email: "user@example.com"

-password: "user"
