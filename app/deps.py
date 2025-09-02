from fastapi import Query
from pydantic import BaseModel
from typing import Optional
from datetime import date

class PaginationParams(BaseModel):
    limit: int = 50
    offset: int = 0

def pagination_params(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
) -> PaginationParams:
    return PaginationParams(limit=limit, offset=offset)

class FilterParams(BaseModel):
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    status: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
