from pydantic import BaseModel, EmailStr, Field, field_validator, field_serializer

from src.core.types import ID

class IAPICreateProfile(BaseModel):
    id: ID
    email: EmailStr
