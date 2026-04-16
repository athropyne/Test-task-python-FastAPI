from fastapi import Depends

from src.handlers.add.api_input import IAPIAddProduct
from src.handlers.add.uow import AddProductUOW

class AddProductService:

    def __init__(self,_uow: AddProductUOW = Depends()):
        self._uow = _uow

    async def call(self, model: IAPIAddProduct):
        await self._uow.call(model)
