from pydantic import BaseModel

from src.core.types import ID

class Product(BaseModel):
    id: ID
    title: str
    description: str
    price: int
    quantity: int