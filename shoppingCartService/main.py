from uuid import UUID
from fastapi import FastAPI, status, Depends, HTTPException
from db.sessions import create_tables
from domain.exceptions.entity_does_not_exist import EntityDoesNotExist
from domain.services.cart_item_service import CartItemService
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
        cart_item_service: CartItemService = Depends(CartItemService),
):
    cart_item = await cart_item_service.add(item)

    return cart_item
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


@app.get(
    "/cart/getItems",
    status_code=status.HTTP_200_OK,
    response_model=list[CartItemRead],
    name="get items"
)
async def get_items(
        user_id: UUID,
        cart_item_service: CartItemService = Depends(CartItemService)
):
    return await cart_item_service.get_cart_items(user_id)

@app.put(
    "/cart/updateItemQuantity",
    status_code=status.HTTP_200_OK,
    response_model=CartItemRead,
    name="update item quantity"
)
async def update_item_quantity(
        item_uuid: UUID,
        new_quantity: int,
        user_id: UUID,
        cart_item_service: CartItemService = Depends(CartItemService),
):
    try:
        updated_cart_item = await cart_item_service.update_quantity(item_uuid, new_quantity, user_id)

        if updated_cart_item:
            return updated_cart_item
        else:
            raise HTTPException(status_code=404, detail="Cart item not found")
    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail="Cart item not found")


@app.delete(
    "/cart/removeItems",
    status_code=status.HTTP_204_NO_CONTENT,
    name="remove items"
)
async def remove_items(
        items_uuid: list[UUID],
        user_id: UUID,
        cart_item_service: CartItemService = Depends(CartItemService)
):
    await cart_item_service.delete_cart_items(cart_items_uuid=items_uuid, user_id=user_id)


@app.get("/init_tables", status_code=status.HTTP_200_OK, name="init_tables")
async def init_tables():
    create_tables()
