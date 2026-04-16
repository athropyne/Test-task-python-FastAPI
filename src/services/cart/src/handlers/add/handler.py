from fastapi import Depends

from src.handlers.add.api_input import IAPIAddProduct
from src.handlers.add.service import AddProductService

async def add_product_in_cart_handler(
        model: IAPIAddProduct,
        service: AddProductService = Depends(),
):
    return await service.call(model)
