from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.core.types import ID

class Product(BaseModel):
    product_id: ID
    price: int
    quantity: int

class OAPICart(BaseModel):
    user_id: ID
    price: int
    products: List[Product]
