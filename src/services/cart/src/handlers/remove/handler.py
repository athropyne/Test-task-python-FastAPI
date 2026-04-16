from fastapi import Depends

from src.core.types import ID
from src.handlers.remove.service import RemoveProductService

async def remove_product_from_cart_handler(
        user_id: ID,
        product_id: ID,
        service: RemoveProductService = Depends()
):
    await service.call(user_id, product_id)
