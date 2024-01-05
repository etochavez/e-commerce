from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from db.tables.base_class import TimestampModel


class CartItemBase(SQLModel):
    item_uuid: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    quantity: int = Field(nullable=False, gt=0)


class CartItem(CartItemBase, TimestampModel, table=True):
    id: int = Field(default=None, primary_key=True)

    __tablename__ = "cart_items"
