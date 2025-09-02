# tests/test_api.py
import pytest
import httpx
from asgi_lifespan import LifespanManager
from fastapi import status
from app.main import app
from app.database import Base, engine

@pytest.fixture(autouse=True, scope="session")
def setup_db():
    # чистая схема перед тестами
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.asyncio
async def test_crud_cycle():
    # Явно запускаем lifespan приложения (startup/shutdown)
    async with LifespanManager(app):
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
            payload = {
                "date": "2025-01-01",
                "status": "business",
                "type": "income",
                "category": "DevOps",
                "subcategory": "Servers",
                "amount": 1000.0,
                "comment": "Income test"
            }
            r = await ac.post("/api/entries", json=payload)
            assert r.status_code == status.HTTP_201_CREATED, r.text
            entry = r.json()

            r = await ac.get(f"/api/entries/{entry['id']}")
            assert r.status_code == 200

            r = await ac.patch(f"/api/entries/{entry['id']}", json={"amount": 1234.0})
            assert r.status_code == 200
            assert float(r.json()["amount"]) == 1234.0

            r = await ac.delete(f"/api/entries/{entry['id']}")
            assert r.status_code == status.HTTP_204_NO_CONTENT
