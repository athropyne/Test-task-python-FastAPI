from pydantic import BaseModel, EmailStr

from src.core.types import ID

class OAPIMeInfo(BaseModel):
    id: ID
    email: EmailStr
    balance: int
