from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.tables.base_class import StatusEnum
from db.tables.products import Product
from infraestructure.schemas.products import ProductRead, ProductCreate


class ProductRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list(self, limit: int = 10, offset: int = 0) -> list[ProductRead]:
        statement = (
            (select(Product).where(Product.status != StatusEnum.deleted))
            .offset(offset)
            .limit(limit)
        )
        try:
            results = await self._session.exec(statement)
        except SQLAlchemyError as e:
            print("SQLAlchemyError" + e.__str__())

        return [ProductRead(**transaction.dict()) for transaction in results]

    async def create(self, transaction_create: ProductCreate) -> ProductRead:
        db_transaction = Product.from_orm(transaction_create)
        self._session.add(db_transaction)
        await self._session.commit()
        await self._session.refresh(db_transaction)

        return ProductRead(**db_transaction.dict())
