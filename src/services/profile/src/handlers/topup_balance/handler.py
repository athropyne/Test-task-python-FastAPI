from fastapi import Depends

from src.core.types import ID
from src.handlers.topup_balance.api_input import IAPIAmount
from src.handlers.topup_balance.service import TopUpBalanceService

async def topup_balance_handler(
        model: IAPIAmount,
        user_id: ID,
        service: TopUpBalanceService = Depends(),
):
    await service.call(user_id, model)
