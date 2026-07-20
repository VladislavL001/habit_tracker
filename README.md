# Habit Tracker API

REST API для отслеживания полезных привычек.

Проект разработан на Django REST Framework в рамках курсовой работы SkyPro.

## Возможности

- Регистрация и авторизация пользователей по JWT
- Создание, просмотр, изменение и удаление привычек
- Просмотр публичных привычек
- Валидация данных согласно требованиям
- Пагинация списка привычек
- Фильтрация привычек
- Автоматическая отправка напоминаний в Telegram
- Документация API (Swagger)

---

## Стек технологий

- Python 3.14
- Django 6
- Django REST Framework
- PostgreSQL
- Redis (Memurai для Windows)
- Celery
- drf-spectacular
- SimpleJWT
- django-filter
- pyTelegramBotAPI

---

## Установка проекта

### 1. Клонировать репозиторий

```bash
git clone <ссылка_на_репозиторий>
cd habit_tracker
```

### 2. Установить зависимости

```bash
poetry install
```

### 3. Создать файл `.env`

На основе файла `.env.template`.

Пример:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=habit_tracker
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379

TELEGRAM_BOT_TOKEN=your_bot_token
```

---

### 4. Выполнить миграции

```bash
poetry run python manage.py migrate
```

---

### 5. Создать суперпользователя

```bash
poetry run python manage.py createsuperuser
```

---

### 6. Запустить сервер

```bash
poetry run python manage.py runserver
```

---

## Запуск Celery Worker

```bash
poetry run celery -A config worker --pool=solo --loglevel=info
```

> Для Windows используется параметр `--pool=solo`.

---

## Запуск Celery Beat

```bash
poetry run celery -A config beat --loglevel=info
```

---

## Документация API

Swagger:

```
http://127.0.0.1:8000/api/schema/swagger-ui/
```

OpenAPI Schema:

```
http://127.0.0.1:8000/api/schema/
```

---

## Запуск тестов

```bash
poetry run python manage.py test
```

Проверка покрытия:

```bash
poetry run coverage run manage.py test
poetry run coverage report
```

---

## Автор

Лабутин Владислав