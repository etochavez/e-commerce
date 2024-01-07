from db.tables.carts import CartBase


class CartCreate(CartBase):
    ...


class CartRead(CartBase):
    id: int
