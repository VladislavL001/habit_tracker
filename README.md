# Habit Tracker API

REST API для отслеживания полезных привычек.

Проект разработан на Django REST Framework в рамках курсовой работы SkyPro.

## Возможности

- Регистрация и авторизация пользователей по JWT
- Создание, просмотр, изменение и удаление привычек
- Просмотр публичных привычек
- Валидация данных согласно требованиям проекта
- Пагинация списка привычек
- Фильтрация привычек
- Автоматическая отправка напоминаний о привычках в Telegram
- Фоновые задачи с использованием Celery
- Периодические задачи с использованием Celery Beat
- Документация API через Swagger
- Автоматическое тестирование проекта
- Проверка качества кода через Flake8
- Сборка Docker-образов
- Автоматический деплой на сервер через GitHub Actions

---

## Стек технологий

- Python 3.14
- Django 6
- Django REST Framework
- PostgreSQL 17
- Redis 7
- Celery
- Celery Beat
- Gunicorn
- Nginx
- drf-spectacular
- Simple JWT
- django-filter
- pyTelegramBotAPI
- Docker
- Docker Compose
- GitHub Actions
- Poetry

---

# Локальная установка

## 1. Клонирование репозитория

```bash
git clone <ссылка_на_репозиторий>
cd habit_tracker
```

## 2. Установка зависимостей

Для установки зависимостей используется Poetry:

```bash
poetry install
```

После установки зависимостей активировать виртуальное окружение:

```bash
poetry shell
```

## 3. Настройка переменных окружения

Создать файл `.env` на основе `.env.template`.

Пример содержимого:

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

Для production необходимо использовать отдельные значения переменных окружения.

## 4. Миграции

```bash
poetry run python manage.py migrate
```

## 5. Создание суперпользователя

```bash
poetry run python manage.py createsuperuser
```

Административная панель:

```text
http://127.0.0.1:8000/admin/
```

## 6. Запуск Django

```bash
poetry run python manage.py runserver
```

---

# Celery

Проект использует Celery для выполнения фоновых задач.

## Celery Worker

```bash
poetry run celery -A config worker --pool=solo --loglevel=info
```

Параметр `--pool=solo` используется для запуска Celery в Windows.

## Celery Beat

```bash
poetry run celery -A config beat --loglevel=info
```

Celery Beat отвечает за выполнение периодических задач.

---

# Docker Compose

Docker Compose запускает все необходимые сервисы проекта.

## Сервисы

- **web** — Django-приложение, запущенное через Gunicorn
- **nginx** — reverse proxy
- **db** — PostgreSQL
- **redis** — Redis
- **celery** — Celery Worker
- **celery-beat** — Celery Beat

Все сервисы запускаются одной командой.

## Запуск

Создать `.env` на основе `.env.template`, затем:

```bash
docker compose up -d --build
```

## Проверка состояния

```bash
docker compose ps
```

## Просмотр логов

```bash
docker compose logs
```

Для отдельного сервиса:

```bash
docker compose logs web
docker compose logs celery
docker compose logs celery-beat
docker compose logs nginx
```

## Остановка

```bash
docker compose down
```

---

# Production

В production используется следующая архитектура:

```text
Client
   |
   v
 Nginx
   |
   v
Gunicorn
   |
   v
Django
   |
   +------> PostgreSQL
   |
   +------> Redis
               |
               +------> Celery Worker
               |
               +------> Celery Beat
```

Nginx принимает внешние HTTP-запросы и передаёт их Django-приложению через Gunicorn.

PostgreSQL используется как основная база данных.

Redis используется в качестве брокера сообщений и backend для Celery.

Celery Worker выполняет фоновые задачи.

Celery Beat запускает периодические задачи.

Запуск production-окружения:

```bash
docker compose up -d --build
```

---

# Документация API

## Swagger

```text
http://127.0.0.1:8000/api/docs/
```

## OpenAPI Schema

```text
http://127.0.0.1:8000/api/schema/
```

---

# API

Основные группы API:

```text
/api/
/api/token/
/api/token/refresh/
/api/schema/
/api/docs/
/users/
```

JWT используется для аутентификации пользователей.

Получение access и refresh токенов:

```text
POST /api/token/
```

Обновление access-токена:

```text
POST /api/token/refresh/
```

---

# Административная панель

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

Создание суперпользователя:

```bash
poetry run python manage.py createsuperuser
```

---

# Тестирование

Запуск тестов:

```bash
poetry run python manage.py test
```

## Проверка покрытия

```bash
poetry run coverage run manage.py test
poetry run coverage report
```

---

# Проверка качества кода

Для проверки качества кода используется Flake8:

```bash
poetry run flake8 .
```

---

# CI/CD

В проекте настроен автоматический pipeline с использованием GitHub Actions.

Pipeline выполняет следующие этапы:

1. Установка зависимостей
2. Запуск тестов
3. Проверка качества кода через Flake8
4. Сборка Docker-образа
5. Публикация Docker-образа
6. Подключение к серверу по SSH
7. Получение актуального кода из Git
8. Пересборка и запуск Docker Compose

Основная последовательность:

```text
Push
  |
  v
Tests
  |
  v
Flake8
  |
  v
Docker Build
  |
  v
Docker Registry
  |
  v
SSH Deploy
  |
  v
Docker Compose
  |
  v
Running Application
```

После успешного выполнения pipeline новая версия приложения автоматически разворачивается на сервере.

---

# Автоматический деплой

Для деплоя используется GitHub Actions и SSH-подключение к серверу.

Во время деплоя выполняются команды:

```bash
cd /opt/habit_tracker
git pull origin feature/coursework
docker compose up -d --build
```

После успешного деплоя сервисы автоматически перезапускаются с новой версией приложения.

---

# Переменные окружения

Проект использует переменные окружения для конфигурации приложения.

| Переменная | Назначение |
|------------|------------|
| `SECRET_KEY` | Секретный ключ Django |
| `DEBUG` | Режим отладки Django |
| `ALLOWED_HOSTS` | Разрешённые хосты |
| `DB_NAME` | Имя базы данных |
| `DB_USER` | Пользователь PostgreSQL |
| `DB_PASSWORD` | Пароль PostgreSQL |
| `DB_HOST` | Адрес PostgreSQL |
| `DB_PORT` | Порт PostgreSQL |
| `REDIS_HOST` | Адрес Redis |
| `REDIS_PORT` | Порт Redis |
| `TELEGRAM_BOT_TOKEN` | Токен Telegram-бота |

Файл `.env` содержит реальные значения переменных окружения и не должен добавляться в репозиторий.

Для настройки проекта используется `.env.template`.

---

# Структура проекта

```text
habit_tracker/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── wsgi.py
│
├── habits/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── filters.py
│   └── tasks.py
│
├── users/
│
├── nginx/
│   └── nginx.conf
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
├── .env.template
└── README.md
```

---

# Запуск проекта одной командой

После настройки `.env` весь проект можно запустить одной командой:

```bash
docker compose up -d --build
```

Проверить состояние:

```bash
docker compose ps
```

После запуска основные сервисы должны находиться в состоянии `Up`.

---

# Автор

**Лабутин Владислав**

Курсовая работа SkyPro.
