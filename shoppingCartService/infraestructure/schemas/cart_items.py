from uuid import UUID
from db.tables.cart_items import CartItemBase


class CartItemCreate(CartItemBase):
    user_id: UUID


class CartItemRead(CartItemBase):
    id: int


class CartItemPatch(CartItemBase):
    ...
