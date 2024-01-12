from uuid import UUID
from pydantic import Field
from application.schemas.base import BaseSchema


class ProductBase(BaseSchema):
    uuid: UUID


class ProductUpdate(ProductBase):
    quantity: int = Field(required=True, gt=0)
