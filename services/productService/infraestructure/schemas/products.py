from uuid import UUID
from db.tables.products import ProductBase


class ProductCreate(ProductBase):
    ...


class ProductRead(ProductBase):
    id: UUID


class ProductPatch(ProductBase):
    ...
