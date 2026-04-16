from pydantic import BaseModel, Field

class IAPICreateProduct(BaseModel):
    title: str = Field(max_length=150)
    description: str = Field(max_length=1500)
    cost_price: int
    user_price: int | None = None
    quantity: int = Field(gt=0)