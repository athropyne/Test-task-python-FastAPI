from pydantic import BaseModel, Field

class IAPIUpdateQuantityProductInCart(BaseModel):
    quantity: int = Field(..., gt=0)