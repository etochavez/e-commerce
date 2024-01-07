from sqlmodel import SQLModel, Field

from db.tables.base_class import StatusEnum, TimestampModel, UUIDModel


class ProductBase(SQLModel):
    name: str = Field(nullable=False)
    inventory: int = Field(nullable=False)
    category: str = Field(nullable=False)
    description: str = Field(nullable=True)
    price: float = Field(nullable=False)


class Product(ProductBase, UUIDModel, TimestampModel, table=True):
    status: StatusEnum = Field(default=StatusEnum.inactive)

    __tablename__ = "products"
