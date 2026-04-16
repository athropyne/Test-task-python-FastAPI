from fastapi import Depends

from src.core.types import ID
from src.handlers.dto import Product
from src.handlers.exc import ProductNotFound
from src.handlers.one.uow import GetProductByIdUOW

class GetProductByIdService:
    def __init__(self, _uow: GetProductByIdUOW = Depends()):
        self._uow = _uow

    async def call(self, product_id: ID):
        product = await self._uow.call(product_id)
        if product is None: raise ProductNotFound
        output = Product(**product)
        return output