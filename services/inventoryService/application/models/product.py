from odmantic import Model, Field


class ProductModel(Model):
    uuid: str = Field(unique=True)
    quantity: int

    model_config = {
        "collection": "products"
    }
