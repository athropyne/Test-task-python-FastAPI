from fastapi import Depends

from src.services.product.create.api_input import IAPICreateProduct
from src.services.product.create.service import CreateProductService

async def create_product_handler(
        model: IAPICreateProduct,
        service: CreateProductService = Depends(),
):
   return await service.call(model)