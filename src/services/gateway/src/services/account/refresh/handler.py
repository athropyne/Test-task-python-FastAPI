from fastapi import Depends

from src.services.account.refresh.api_input import IAPIRefreshToken
from src.services.account.refresh.service import RefreshTokensService

async def refresh_tokens_handler(
        model: IAPIRefreshToken,
        service: RefreshTokensService = Depends()
):
    return await service.call(model)