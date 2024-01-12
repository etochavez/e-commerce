from pprint import pprint
from uuid import UUID
from odmantic import AIOEngine
from application.models.product import ProductModel
from domain.exceptions.entity_does_not_exist import EntityDoesNotExist


class ProductRepository:
    def __init__(self, engine: AIOEngine) -> None:
        self._engine = engine

    async def get_product_by_uuid(self, uuid: str) -> ProductModel:
        product = await self._engine.find_one(
            ProductModel,
            ProductModel.uuid == uuid
        )
        return product

    async def get_quantity(self, product_uuid: str) -> int:
        product = await self.get_product_by_uuid(product_uuid)

        if not product:
            raise EntityDoesNotExist

        return product.quantity

    async def add_product(self, product: ProductModel) -> ProductModel:
        return await self._engine.save(product)

    async def update_quantity(self, product, quantity) -> ProductModel:
        product.quantity = quantity
        return await self._engine.save(product)
