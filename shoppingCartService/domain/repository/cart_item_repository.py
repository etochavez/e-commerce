from sqlmodel.ext.asyncio.session import AsyncSession
from db.tables.cart_items import CartItem
from infraestructure.schemas.cart_items import CartItemRead, CartItemCreate


class CartItemRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, car_item_create: CartItemCreate, cart_id: int) -> CartItemRead:
        item_data = car_item_create.dict()
        item_data['cart_id'] = cart_id
        db_cart_item = CartItem.from_orm(item_data)
        try:
            self._session.add(db_cart_item)
            await self._session.commit()
            await self._session.refresh(db_cart_item)

            return CartItemRead(**db_cart_item.dict())
        except Exception as e:
            print(f"SQLAlchemyError: {e}")
