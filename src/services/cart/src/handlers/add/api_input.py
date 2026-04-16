from typing import List

from pydantic import BaseModel, Field

from src.core.types import ID

class IAPIAddProduct(BaseModel):
    user_id: ID
    product_id: ID
    price: int
    quantity: int = Field(gt=0)
