from typing import Optional
from uuid import UUID
from sqlmodel import select, delete, update
from sqlmodel.ext.asyncio.session import AsyncSession
from db.tables.cart_items import CartItem
from db.tables.carts import Cart
from infraestructure.schemas.cart_items import CartItemRead, CartItemCreate


class CartItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, car_item_create: CartItemCreate, cart_id: int) -> CartItemRead:
        item_data = car_item_create.dict()
        item_data['cart_id'] = cart_id
        db_cart_item = CartItem.from_orm(item_data)
        self._session.add(db_cart_item)
        await self._session.commit()
        await self._session.refresh(db_cart_item)

        return CartItemRead(**db_cart_item.dict())

    async def get_by_cart_id_and_cart_item_uuid(self, cart_id: int, cart_item_uuid: UUID) -> Optional[CartItem]:
        stmt = select(CartItem).where(CartItem.cart_id == cart_id).where(CartItem.item_uuid == cart_item_uuid)
        results = await self._session.exec(stmt)
        return results.first()

    async def get_by_cart_item_uuid(self, cart_item_uuid: UUID) -> Optional[CartItem]:
        stmt = select(CartItem).where(CartItem.item_uuid == cart_item_uuid)
        results = await self._session.exec(stmt)
        return results.first()

    async def update(self, cart_item: CartItem, values: dict) -> CartItemRead:
        for key, value in values.items():
            setattr(cart_item, key, value)

        await self._session.commit()
        await self._session.refresh(cart_item)
        return CartItemRead(**cart_item.dict())

    async def get_by_cart_id(self, cart_id: int) -> Optional[list[CartItemRead]]:
        stmt = select(CartItem).where(CartItem.cart_id == cart_id)
        results = await self._session.exec(stmt)
        cart_items = results.all()
        return [CartItemRead(**cart_item.dict()) for cart_item in cart_items]

    async def delete(self, cart_item_uuid: UUID, user_id: UUID) -> None:
        stmt = delete(CartItem).where(
            CartItem.cart_id == select(Cart.id).where(Cart.user_id == user_id)
        ).where(CartItem.item_uuid == cart_item_uuid)
        await self._session.exec(stmt)
        await self._session.commit()

    async def update_quantity(self, cart_item_uuid: UUID, quantity: int, user_id: UUID) -> CartItem | None:
        stmt = update(CartItem).values(quantity=quantity).where(
            CartItem.cart_id == select(Cart.id).where(Cart.user_id == user_id)
        ).where(CartItem.item_uuid == cart_item_uuid)

        await self._session.exec(stmt)
        await self._session.commit()

        return await self.get_by_cart_item_uuid(cart_item_uuid)
