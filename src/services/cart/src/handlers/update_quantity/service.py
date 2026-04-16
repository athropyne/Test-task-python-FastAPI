from fastapi import Depends

from src.core.types import ID
from src.handlers.update_quantity.api_input import IAPIUpdateQuantity
from src.handlers.update_quantity.uow import UpdateProductQuantityUOW

class UpdateQuantityService:

    def __init__(self, _uow: UpdateProductQuantityUOW = Depends()):
        self._uow = _uow

    async def call(self, user_id: ID, product_id: ID, model: IAPIUpdateQuantity):
        await self._uow.call(user_id, product_id, model)
