from uuid import UUID
from fastapi import Depends
from db.tables.cart_items import CartItem
from domain.repository.cart_item_repository import CartItemRepository
from domain.repository.cart_repository import CartRepository
from infraestructure.dependencies.repository import get_repository
from infraestructure.schemas.cart_items import CartItemCreate, CartItemRead


class CartItemService:

    def __init__(
            self,
            cart_item_repository: CartItemRepository = Depends(get_repository(CartItemRepository)),
            cart_repository: CartRepository = Depends(get_repository(CartRepository))
    ):
        self._cart_item_repository = cart_item_repository
        self._cart_repository = cart_repository

    async def add(self, cart_item_create: CartItemCreate) -> CartItemRead:
        cart = await self._cart_repository.get(cart_item_create.user_id)

        if not cart:
            cart = await self._cart_repository.create(cart_item_create.user_id)

        existing_cart_item = await self._cart_item_repository.get_by_cart_id_and_cart_item_uuid(
            cart_id=cart.id, cart_item_uuid=cart_item_create.item_uuid
        )

        if existing_cart_item:
            new_quantity = existing_cart_item.quantity + cart_item_create.quantity
            return await self._cart_item_repository.update(existing_cart_item, {"quantity": new_quantity})

        return await self._cart_item_repository.create(cart_item_create, cart.id)

    async def get_cart_items(self, user_id: UUID) -> list[CartItemRead]:
        cart = await self._cart_repository.get(user_id)

        return await self._cart_item_repository.get_by_cart_id(cart.id)

    async def delete_cart_items(self, cart_items_uuid: list[UUID], user_id: UUID) -> None:
        for cart_item_uuid in cart_items_uuid:
            await self._cart_item_repository.delete(cart_item_uuid, user_id)

    async def update_quantity(self, cart_item_uuid: UUID, new_quantity: int, user_id: UUID) -> CartItem | None:
        return await self._cart_item_repository.update_quantity(cart_item_uuid, new_quantity, user_id)
