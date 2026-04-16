from pydantic import Field, BaseModel

from src.core.types import ID

class IAPIAddProduct(BaseModel):
    product_id: ID
    quantity: int = Field(gt=0)
