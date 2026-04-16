from pydantic import BaseModel, Field

class IAPIAmount(BaseModel):
    sum: int = Field(..., gt=0)
