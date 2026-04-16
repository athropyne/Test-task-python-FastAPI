from fastapi import Depends

from src.handlers.dto import Product
from src.handlers.list.uow import GetProductListUOW

class GetProductListService:

    def __init__(self, _uow: GetProductListUOW = Depends()):
        self._uow = _uow

    async def call(self):
        products = await self._uow.call()
        output = [Product(**row) for row  in products]
        return output
