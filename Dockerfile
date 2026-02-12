# Используем Python 3.12
FROM python:3.12-slim

# Рабочая директория в контейнере
WORKDIR /app

# Устанавливаем системные зависимости для сборки пакетов и Kerberos
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    krb5-user \
    libkrb5-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Копируем весь проект
COPY . .

RUN python manage.py collectstatic --noinput

# Открываем порт
EXPOSE 8000

# Команда запуска через gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
