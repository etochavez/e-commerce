from uuid import UUID
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from db.tables.carts import Cart
from infraestructure.schemas.carts import CartRead, CartCreate


class CartRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: UUID) -> Cart:
        try:
            db_cart = Cart.from_orm(CartCreate(user_id=user_id))
            self._session.add(db_cart)
            await self._session.commit()
            await self._session.refresh(db_cart)

            return db_cart
        except Exception as e:
            print(f"SQLAlchemyError: {e}")

    async def get(self, user_id: UUID) -> Optional[CartRead]:
        statement = (
            select(Cart)
            .where(Cart.user_id == user_id)
        )
        try:
            result = await self._session.exec(statement)
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError: {e}")
            return None

        cart = result.first()
        if not cart:
            return None

        return CartRead(**cart.dict())
