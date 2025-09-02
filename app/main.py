# app/main.py
from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import schemas, crud, deps

# --- Lifespan: создаём схему БД на старте приложения ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        # Для тестов дроп делаем в фикстурах
        pass


app = FastAPI(
    title="DDS (Cash Flow) Manager",
    version="0.1.0",
    lifespan=lifespan,
)

# Статика и шаблоны (UI можно отключать переменной USE_TEMPLATES=0)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

USE_TEMPLATES = os.getenv("USE_TEMPLATES", "1") != "0"
templates = None
if USE_TEMPLATES:
    try:
        from fastapi.templating import Jinja2Templates

        templates = Jinja2Templates(directory="app/templates")
    except AssertionError:
        # jinja2 не установлена — отдадим JSON-страницу на "/"
        templates = None


# -------- HTML UI --------
@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    status: Optional[str] = None,
    type: Optional[str] = None,
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    pagination: deps.PaginationParams = Depends(deps.pagination_params),
    db: Session = Depends(get_db),
):
    items = crud.list_entries(
        db,
        date_from=date_from,
        date_to=date_to,
        status=status,
        type=type,
        category=category,
        subcategory=subcategory,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    if not templates:
        # Без шаблонов возвращаем JSON, чтобы тесты/CI не падали
        data = [schemas.EntryOut.model_validate(i, from_attributes=True).model_dump() for i in items]
        return JSONResponse({"entries": data})

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "entries": items,
            "filters": {
                "date_from": date_from,
                "date_to": date_to,
                "status": status,
                "type": type,
                "category": category,
                "subcategory": subcategory,
            },
            "pagination": pagination,
        },
    )


# -------- API --------
@app.post("/api/entries", response_model=schemas.EntryOut, status_code=201)
def create_entry(data: schemas.EntryCreate, db: Session = Depends(get_db)):
    return crud.create_entry(db, data)


@app.get("/api/entries/{entry_id}", response_model=schemas.EntryOut)
def get_entry(entry_id: int, db: Session = Depends(get_db)):
    item = crud.get_entry(db, entry_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@app.patch("/api/entries/{entry_id}", response_model=schemas.EntryOut)
def update_entry(
    entry_id: int,
    payload: dict = Body(...),  # принимаем произвольный JSON, валидируем вручную
    db: Session = Depends(get_db),
):
    data = schemas.EntryUpdate.model_validate(payload)
    item = crud.update_entry(db, entry_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@app.delete("/api/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_entry(db, entry_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return None


@app.get("/api/entries", response_model=list[schemas.EntryOut])
def list_entries(
    filters: deps.FilterParams = Depends(),
    pagination: deps.PaginationParams = Depends(deps.pagination_params),
    db: Session = Depends(get_db),
):
    return crud.list_entries(
        db,
        date_from=filters.date_from,
        date_to=filters.date_to,
        status=filters.status,
        type=filters.type,
        category=filters.category,
        subcategory=filters.subcategory,
        limit=pagination.limit,
        offset=pagination.offset,
    )
