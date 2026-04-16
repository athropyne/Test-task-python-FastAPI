from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.core.types import ID
from src.schema import OrderStatus

class Product(BaseModel):
    product_id: ID
    price: int
    quantity: int

class OAPIOrder(BaseModel):
    id: ID
    status: OrderStatus
    rejected_reason: str | None
    created_at: datetime
    products: List[Product]
    created_at: datetime