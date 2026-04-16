from fastapi import Depends

from src.services.account.create.api_input import IAPICreateUser
from src.services.account.create.service import CreateUserService

async def create_user_handler(
        model: IAPICreateUser,
        service: CreateUserService = Depends()
):
    return await service.call(model)