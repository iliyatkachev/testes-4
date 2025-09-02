from __future__ import annotations
from pydantic import BaseModel, Field, field_validator
from pydantic.config import ConfigDict
from datetime import date
from typing import Optional, Literal

Status = Literal["business", "personal", "tax"]
Type = Literal["income", "expense"]

class EntryBase(BaseModel):
    date: date
    status: Status
    type: Type
    category: str = Field(..., min_length=1, max_length=64)
    subcategory: str = Field(..., min_length=1, max_length=64)
    amount: float = Field(..., ge=0)
    comment: Optional[str] = Field(None, max_length=512)

    @field_validator("category", "subcategory")
    @classmethod
    def strip_spaces(cls, v: str) -> str:
        return v.strip()

class EntryCreate(EntryBase):
    pass

class EntryUpdate(BaseModel):
    # ВАЖНО: все поля — с default=None, чтобы были реально опциональными для PATCH
    date: Optional[date] = None
    status: Optional[Status] = None
    type: Optional[Type] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)
    comment: Optional[str] = None

class EntryOut(EntryBase):
    id: int
    # Pydantic v2 стиль — убирает предупреждение про class-based Config
    model_config = ConfigDict(from_attributes=True)
