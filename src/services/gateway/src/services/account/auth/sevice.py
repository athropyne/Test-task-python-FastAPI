from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from src.core.security import TokenManager
from src.services.account.auth.api_output import TokenModel
from src.services.account.auth.uow import AuthUserUOW

class AuthUserService:

    def __init__(self, _uow: AuthUserUOW = Depends()):
        self._uow = _uow

    async def call(self, model: OAuth2PasswordRequestForm):
        user_id = await self._uow.call(model)
        access_token = TokenManager.access(user_id)
        refresh_token = TokenManager.refresh(user_id)
        return TokenModel(access_token=access_token, refresh_token=refresh_token)
