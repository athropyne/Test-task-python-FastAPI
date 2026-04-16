from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.profile.topup_balance.api_input import IAPIAmount
from src.services.profile.topup_balance.service import TopUpBalanceService

async def topup_balance_handler(
        model: IAPIAmount,
        client_id: ID = Depends(TokenManager.id),
        service: TopUpBalanceService = Depends()
):
    await service.call(client_id, model)