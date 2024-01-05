import uuid
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from db.tables.carts import Cart
from domain.exceptions.entity_does_not_exist import EntityDoesNotExist
from infraestructure.schemas.carts import CartRead


class CartRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user_id: uuid) -> Cart:
        db_cart = Cart.from_orm(user_id)
        self._session.add(db_cart)
        await self._session.commit()
        await self._session.refresh(db_cart)

        return db_cart

    async def get(self, user_id: uuid) -> Optional[CartRead]:
        statement = (
            select(Cart)
            .where(Cart.user_id == user_id)
        )
        try:
            result = await self._session.exec(statement)
        except SQLAlchemyError as e:
            print("SQLAlchemyError" + e.__str__())

        print("Result: " + result.__str__())
        if result.first() is None:
            raise EntityDoesNotExist

        return CartRead(**result.first().dict())
