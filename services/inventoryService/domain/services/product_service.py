from uuid import UUID
from application.models.product import ProductModel
from core.config import settings
from infraestructure.repository.product_repository import ProductRepository


class ProductService:
    def __init__(self) -> None:
        self._product_repository = ProductRepository(settings.async_database_engine)

    async def update_or_create(self, product_model: ProductModel) -> ProductModel:
        product = await self._product_repository.get_product_by_uuid(
            product_model.uuid
        )

        if not product:
            product = await self._product_repository.add_product(product_model)
        else:
            product = await self._product_repository.update_quantity(product, product_model.quantity)

        return product

    async def get_quantity(self, uuid: UUID) -> int:
        return await self._product_repository.get_quantity(uuid.hex)
