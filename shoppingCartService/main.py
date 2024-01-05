from fastapi import FastAPI, status, Depends, HTTPException

from db.sessions import create_tables
from domain.exceptions.entity_does_not_exist import EntityDoesNotExist
from domain.repository.cart_repository import CartRepository
from infraestructure.dependencies.repository import get_repository
from infraestructure.schemas.cart_items import CartItemRead, CartItemCreate

app = FastAPI()


@app.post(
    "/cart/addItem",
    status_code=status.HTTP_201_CREATED,
    response_model=CartItemRead,
    name="add item"
)
async def add_item(
        item: CartItemCreate,
        cart_repository: CartRepository = Depends(get_repository(CartRepository))
):
    try:
        cart = await cart_repository.get(item.user_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found!"
        )

    return item.__dict__
    # if item.user_id not in carts_db:
    #     carts_db[item.user_id] = ShoppingCart(user_id=item.user_id, items=[])
    #
    # # Check inventory using gRPC call
    # inventory_request = payment_pb2.InventoryCheckRequest(productId=item.product_id)
    # try:
    #     inventory_response = payment_stub.CheckInventory(inventory_request)
    # except grpc.RpcError as e:
    #     raise HTTPException(status_code=500, detail=f"Error checking inventory: {e.details()}")
    #
    # if inventory_response.inventory >= item.quantity:
    #     carts_db[item.user_id].items.append(item)
    #     return {"message": "Item added to the cart successfully"}
    # else:
    #     raise HTTPException(status_code=400, detail="Insufficient inventory")


@app.get("/init_tables", status_code=status.HTTP_200_OK, name="init_tables")
async def init_tables():
    create_tables()
