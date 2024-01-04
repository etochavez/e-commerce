from typing import Optional

from fastapi import FastAPI, status, Query, Depends, Body

from db.sessions import create_tables
from domain.repository.product_repository import ProductRepository
from infraestructure.dependencies.repositories import get_repository
from infraestructure.schemas.products import ProductRead, ProductCreate

app = FastAPI()


@app.get(
    "/products",
    response_model=list[Optional[ProductRead]],
    status_code=status.HTTP_200_OK,
    name="get_products",
)
async def list_products(
        limit: int = Query(default=10, lte=100),
        offset: int = Query(default=0, ge=0),
        repository: ProductRepository = Depends(get_repository(ProductRepository))
):
    return await repository.list(limit=limit, offset=offset)


@app.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    name="create_product",
)
async def create_transaction(
    product_create: ProductCreate = Body(...),
    repository: ProductRepository = Depends(get_repository(ProductRepository)),
) -> ProductRead:
    return await repository.create(product_create=product_create)


@app.get("/init_tables", status_code=status.HTTP_200_OK, name="init_tables")
async def init_tables():
    create_tables()
