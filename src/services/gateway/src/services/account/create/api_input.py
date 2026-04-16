from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer

from src.core.security import PasswordManager

class IAPICreateUser(BaseModel):
    username: str = Field(max_length=150)
    email: EmailStr
    password: str = Field(max_length=128)

    @field_serializer("password")
    def validate_password(self, value):
        return PasswordManager.hash(value)