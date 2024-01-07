from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field
from db.tables.base_class import TimestampModel


class CartItemBase(SQLModel):
    item_uuid: UUID = Field(
        default_factory=None,
        index=True,
        nullable=False,
    )
    quantity: int = Field(nullable=False, gt=0)


class CartItem(CartItemBase, TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cart_id: int = Field(default=None, nullable=False, foreign_key="carts.id")

    __tablename__ = "cart_items"
