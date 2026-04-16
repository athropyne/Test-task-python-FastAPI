from typing import List

from pydantic import BaseModel

from src.core.types import ID

class Product(BaseModel):
    product_id: ID
    price: int
    quantity: int

class DTOCreateOrder(BaseModel):
    user_id: ID
    products: List[Product]