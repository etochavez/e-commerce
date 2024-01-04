from typing import Optional
from sqlmodel import SQLModel, Field
from db.tables.base_class import TimestampModel


class CartItemBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(default=None, nullable=False)
    item_id: int = Field(default=None, nullable=False)
    quantity: str = Field(nullable=False)


class CartItem(CartItemBase, TimestampModel, table=True):
    pass

    __tablename__ = "carts"
