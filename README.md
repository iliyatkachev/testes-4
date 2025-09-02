# 💸 Тестовое: Веб‑сервис ДДС (Cash Flow)

Приложение на **FastAPI** для управления движением денежных средств (ДДС).  
Включает REST API, фильтрацию, пагинацию, валидацию, простой HTML UI (Jinja2 + HTMX) и тесты.

---

## 🔧 Стек технологий

- **FastAPI** — основной фреймворк (ASGI + OpenAPI)
- **SQLAlchemy 2.0** — ORM
- **Pydantic v2** — схемы, валидация
- **SQLite / PostgreSQL** — выбор БД через `DATABASE_URL`
- **Jinja2 + HTMX** — мини‑UI (таблица, форма)
- **Pytest + httpx + asgi-lifespan** — тесты API
- **Docker / docker-compose** — для локального запуска в изоляции

---

## 🚀 Быстрый старт (локально)

```bash
git clone <your-repo-url>
cd dds_test_project

# Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate

# Установка зависимостей
pip install -e .

# Запуск приложения (по умолчанию с SQLite)
uvicorn app.main:app --reload
# testes-4
