from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel

from src.core.types import ID

class Product(BaseModel):
    product_id: ID
    price: int
    quantity: int

class OrderCreatedEvent(BaseModel):
    id: ID
    user_id: ID
    created_at: datetime
    products: List[Product]
    transaction_id: UUID
