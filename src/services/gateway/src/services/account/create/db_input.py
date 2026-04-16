from pydantic import BaseModel, Field

class IDBCreateUser(BaseModel):
    username: str = Field(max_length=150)
    password: str = Field(max_length=128)