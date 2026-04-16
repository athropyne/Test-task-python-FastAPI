import uuid
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

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
    transaction_id: UUID = Field(default_factory=uuid.uuid4)
