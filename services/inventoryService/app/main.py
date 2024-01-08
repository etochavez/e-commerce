import grpc
from concurrent import futures
import inventory_pb2_grpc
import inventory_pb2


class InventoryServicer(inventory_pb2_grpc.InventoryServiceServicer):
    def __init__(self):
        self.product_inventory = {"123": 1, "456": 2, "789": 3}

    def CheckInventory(self, request, context):
        product_id = request.product_id
        quantity = self.product_inventory.get(product_id, 0)

        return inventory_pb2.CheckInventoryResponse(quantity=quantity)

    def UpdateInventory(self, request, context):
        product_id = request.product_id
        quantity = request.quantity

        if quantity < 0:
            return inventory_pb2.UpdateInventoryResponse(success=False)

        self.product_inventory[product_id] = quantity
        return inventory_pb2.UpdateInventoryResponse(success=True)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryServicer(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
