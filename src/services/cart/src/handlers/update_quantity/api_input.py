from pydantic import BaseModel, Field

class IAPIUpdateQuantity(BaseModel):
    quantity: int = Field(..., gt=0)