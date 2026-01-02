# Онлайн-платформа обучающих курсов
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Описание
Онлайн-платформа обучающих курсов.

## Основной функционал
- Регистрация и авторизация через JWT-токены
- CRUD для курсов и уроков с разграничением прав доступа
- Платежи пользователей за курсы и уроки
- Подписка на обновления курсов
- Валидация ссылок в уроках (разрешены только YouTube)
- Пагинация списков курсов и уроков
- Тесты с покрытием кода

## Разграничение прав доступа
- ### Обычные пользователи:
  - Могут создавать, редактировать и удалять только свои курсы и уроки
  - Могут подписываться/отписываться от курсов
  - Видят полную информацию только о своём профиле

- ### Модераторы (группа moderators):
  - Могут просматривать и редактировать любые курсы и урок
  - Не могут создавать или удалять курсы/уроки

- ### Неавторизованные пользователи:
  - Доступ только к регистрации и получению токена

# Установка и запуск
```bash
# Клонирование репозитория
git clone <ссылка_на_репозиторий>
cd Online_learning

# Создание виртуального окружения
python -m venv .venv
.\.venv\Scripts\Activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка .env (пример в .env.example)
copy .env.example .env
# Отредактируйте .env под свои данные PostgreSQL

# Миграции
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Заполнение тестовыми платежами
python manage.py populate_payments

# Запуск сервера
python manage.py runserver
```

# Основные эндпоинты
- POST /api/register/ — регистрация пользователя
- POST /api/token/ — получение JWT-токенов
- POST /api/token/refresh/ — обновление токена
- GET /api/me/ — профиль текущего пользователя
- GET/POST /api/courses/ — список и создание курсов
- GET/PUT/PATCH/DELETE /api/courses/{id}/ — работа с курсом
- GET/POST /api/lessons/ — список и создание уроков
- GET/PUT/PATCH/DELETE /api/lessons/{id}/ — работа с уроком
- GET /api/payments/ — список платежей (с фильтрацией и сортировкой)
- POST /api/subscribe/ — подписка/отписка от курса (body: {"course_id": 1})

# Тесты и покрытие
```bash
coverage run manage.py test tests
coverage report
coverage html  # отчёт в htmlcov/index.html
```

# Админ-панель
http://127.0.0.1:8000/admin/
- Создание группы moderators
- Назначение пользователей в группы
- Просмотр и управление всеми моделями

# Локальный запуск с Docker

```bash
docker compose up --build
```
API доступно по http://localhost/
Админка: http://localhost/admin/

## Структура контейнеров
- web: Django + Gunicorn
- db: PostgreSQL
- redis: Redis
- nginx: обратный прокси

# Деплой на сервер

### Настройка сервера
- Ubuntu 24.04 LTS на Yandex Cloud
- Доступ по SSH-ключу (пользователь arhimedko)
- Nginx + Gunicorn + Supervisor
- Приложение доступно по http://89.169.191.228/

### GitHub Actions
- Workflow в `.github/workflows/deploy.yml`
- Запускается при push в develop
- Тесты + coverage
- Деплой по SSH при успешных тестах

### Secrets
- DEPLOY_SSH_KEY
- SERVER_IP
- DEPLOY_USER

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
