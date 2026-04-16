from fastapi import Depends

from src.core.types import IDModel
from src.handlers.create.api_input import IAPICreateProduct
from src.handlers.create.uow import CreateProductUOW

class CreateProductService:

    def __init__(
            self,
            _uow: CreateProductUOW = Depends()
    ):
        self._uow = _uow

    async def call(self, model: IAPICreateProduct):
        product_id = await self._uow.call(model)
        return IDModel(id=product_id)
