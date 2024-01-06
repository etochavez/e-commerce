from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field
from db.tables.base_class import TimestampModel


class CartBase(SQLModel):
    user_id: UUID = Field(
        default_factory=None,
        index=True,
        nullable=False,
    )


class Cart(CartBase, TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    __tablename__ = "carts"
