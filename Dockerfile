FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости для psycopg2 и сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем Python-пакеты
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Копируем весь проект
COPY . .

# Запускаем Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]