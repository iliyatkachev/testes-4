from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from typing import Optional
from . import models, schemas

def create_entry(db: Session, data: schemas.EntryCreate) -> models.Entry:
    entry = models.Entry(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

def get_entry(db: Session, entry_id: int) -> Optional[models.Entry]:
    return db.get(models.Entry, entry_id)

def update_entry(db: Session, entry_id: int, data: schemas.EntryUpdate) -> Optional[models.Entry]:
    entry = db.get(models.Entry, entry_id)
    if not entry:
        return None
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(entry, k, v)
    db.commit()
    db.refresh(entry)
    return entry

def delete_entry(db: Session, entry_id: int) -> bool:
    entry = db.get(models.Entry, entry_id)
    if not entry:
        return False
    db.delete(entry)
    db.commit()
    return True

def list_entries(db: Session, *, date_from=None, date_to=None, status=None, type=None, category=None, subcategory=None, limit=50, offset=0):
    stmt = select(models.Entry)
    conds = []
    if date_from: conds.append(models.Entry.date >= date_from)
    if date_to: conds.append(models.Entry.date <= date_to)
    if status: conds.append(models.Entry.status == status)
    if type: conds.append(models.Entry.type == type)
    if category: conds.append(models.Entry.category == category)
    if subcategory: conds.append(models.Entry.subcategory == subcategory)
    if conds: stmt = stmt.where(and_(*conds))
    stmt = stmt.order_by(models.Entry.date.desc(), models.Entry.id.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()
