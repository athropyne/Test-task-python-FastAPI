from fastapi import Depends

from src.core.types import ID
from src.handlers.clear.uow import ClearCartUOW

class ClearCartService:

    def __init__(self, _uow: ClearCartUOW = Depends()):
        self._uow = _uow

    async def call(self, user_id: ID):
        await self._uow.call(user_id)
