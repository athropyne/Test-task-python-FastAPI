from fastapi import Depends

from src.core.types import ID
from src.handlers.remove.uow import RemoveProductUOW

class RemoveProductService:

    def __init__(self, _uow: RemoveProductUOW = Depends()):
        self._uow = _uow

    async def call(self, user_id: ID, product_id: ID):
        await self._uow.call(user_id, product_id)


