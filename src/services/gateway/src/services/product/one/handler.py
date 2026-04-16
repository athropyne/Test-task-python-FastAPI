from fastapi import Depends

from src.core.types import ID
from src.services.product.one.service import GetProductByIdService

async def get_product_by_id_handler(
        product_id: ID,
        service: GetProductByIdService = Depends()
):
    return await service.call(product_id=product_id)