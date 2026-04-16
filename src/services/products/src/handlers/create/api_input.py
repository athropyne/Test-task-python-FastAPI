from pydantic import BaseModel, Field, field_validator, field_serializer

class IAPICreateProduct(BaseModel):
    title: str = Field(max_length=150)
    description: str = Field(max_length=1500)
    cost_price: int
    user_price: int | None = None
    quantity: int = Field(gt=0)


    @field_serializer("user_price")
    def validate_user_price(self, v):
        return v if v is not None else int(self.cost_price + self.cost_price * 0.2)