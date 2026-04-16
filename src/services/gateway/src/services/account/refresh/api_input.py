from pydantic import BaseModel

class IAPIRefreshToken(BaseModel):
    refresh_token: str