from sqlmodel import SQLModel, Field

from db.tables.base_class import UUIDModel


class ProductBase(SQLModel):
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    price: float = Field(nullable=False)


class Product(ProductBase, UUIDModel, table=True):
    pass

    __tablename__ = "products"
