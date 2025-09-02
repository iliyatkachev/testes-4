from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date, Numeric, CheckConstraint, Index
from .database import Base

class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[str] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    type: Mapped[str] = mapped_column(String(32), index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    subcategory: Mapped[str] = mapped_column(String(64), index=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2))
    comment: Mapped[str | None] = mapped_column(String(512), nullable=True)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="amount_non_negative"),
        Index("idx_entries_cat_subcat", "category", "subcategory"),
    )
