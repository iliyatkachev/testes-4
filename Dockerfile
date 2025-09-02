# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Системные зависимости (psycopg бинарный почти без deps, но добавим gcc на всякий случай)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Копируем метаданные проекта и ставим зависимости
COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir -e .

# Копируем исходники
COPY app /app/app

EXPOSE 8000

# Uvicorn в прод-режиме
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
