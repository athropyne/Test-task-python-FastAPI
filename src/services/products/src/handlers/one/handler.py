from fastapi import Depends

from src.core.types import ID
from src.handlers.one.service import GetProductByIdService

async def get_product_by_id_handler(
        product_id: ID,
        service: GetProductByIdService = Depends(),
):
    return await service.call(product_id)