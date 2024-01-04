from typing import Optional
from sqlmodel import SQLModel, Field
from db.tables.base_class import TimestampModel


class CartBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_uuid: str = Field(nullable=False)


class Cart(CartBase, TimestampModel, table=True):
    pass

    __tablename__ = "carts"
