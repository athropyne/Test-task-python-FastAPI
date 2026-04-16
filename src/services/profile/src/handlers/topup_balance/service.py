from fastapi import Depends

from src.core.types import ID
from src.handlers.topup_balance.api_input import IAPIAmount
from src.handlers.topup_balance.uow import TopUpBalanceUOW

class TopUpBalanceService:

    def __init__(self, _uow: TopUpBalanceUOW = Depends()):
        self._uow = _uow

    async def call(self, user_id: ID, model: IAPIAmount):
        await self._uow.call(user_id, model)
