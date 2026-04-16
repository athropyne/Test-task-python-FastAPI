from pydantic import BaseModel

class IAPIAmount(BaseModel):
    sum: int