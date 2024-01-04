from fastapi import FastAPI, status

from db.sessions import create_tables


app = FastAPI()


@app.post("/cart/additem")
async def add_item(item: CartItem):
    return "Item added"
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



# @app.get("/init_tables", status_code=status.HTTP_200_OK, name="init_tables")
# async def init_tables():
#     create_tables()
