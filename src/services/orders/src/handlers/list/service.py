from fastapi import Depends

from src.core.types import ID
from src.handlers.list.api_output import OAPIOrder
from src.handlers.list.uow import GetOrderListByUserIdUOW

class GetOrderListByUserIdService:
    def __init__(self, _uow: GetOrderListByUserIdUOW = Depends()):
        self._uow = _uow

    async def call(self, user_id:ID):
        order_list = await self._uow.call(user_id)
        return [OAPIOrder(**row) for row in order_list]