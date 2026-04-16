from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request

from src.services.account.auth.sevice import AuthUserService

async def auth_user_handler(
        model: OAuth2PasswordRequestForm = Depends(),
        service: AuthUserService = Depends()
):
    return await service.call(model)