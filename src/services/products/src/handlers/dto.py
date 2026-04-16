from pydantic import BaseModel, Field

from src.core.types import ID

class Product(BaseModel):
    id: ID
    title: str
    description: str
    price: int = Field(..., validation_alias="user_price")
    quantity: int