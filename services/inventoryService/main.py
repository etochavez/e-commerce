import asyncio
import grpc
from concurrent import futures
import inventory_pb2_grpc
import inventory_pb2
from application.models.product import ProductModel
from application.schemas.product import ProductBase, ProductUpdate
from domain.services.product_service import ProductService


class InventoryServicer(inventory_pb2_grpc.InventoryServiceServicer):
    def __init__(self):
        self._product_service = ProductService()

    async def CheckInventory(self, request, context):
        try:
            product = ProductBase(uuid=request.product_id)
            quantity = await self._product_service.get_quantity(product.uuid)
        except Exception as e:
            quantity = -1

        return inventory_pb2.CheckInventoryResponse(quantity=quantity)

    async def UpdateInventory(self, request, context):
        product_update = ProductUpdate(
            uuid=request.product_id,
            quantity=request.quantity
        )
        product = ProductModel(
            uuid=product_update.uuid.hex,
            quantity=product_update.quantity
        )

        success = True

        try:
            await self._product_service.update_or_create(product)
        except Exception as e:
            success = False

        return inventory_pb2.UpdateInventoryResponse(success=success)


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()

    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    asyncio.run(serve())
