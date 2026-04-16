from fastapi import Depends
from sqlalchemy.sql.ddl import CreateIndex

from src.handlers.create.api_input import IAPICreateProduct
from src.handlers.create.service import CreateProductService

async def create_product_handler(
        model: IAPICreateProduct,
        service: CreateProductService = Depends(),
):
    return await service.call(model)
