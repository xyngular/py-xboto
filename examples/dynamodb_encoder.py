from decimal import Decimal

from pydantic import BaseModel
from xyn_aws.dynamodb import dynamodb_encoder


class Order(BaseModel):
    product: str
    price: Decimal


order = Order(product="Xyng", price=Decimal("51.99"))
print(order)
# product='Xyng' price=Decimal('51.99')

order_json = order.json(encoder=dynamodb_encoder)
print(order_json)
# {"product": "Xyng", "price": "51.99"}
