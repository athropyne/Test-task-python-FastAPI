from fastapi import Depends

from src.core.types import ID
from src.handlers.update_quantity.api_input import IAPIUpdateQuantity
from src.handlers.update_quantity.service import UpdateQuantityService

async def update_product_quantity_handler(
        user_id:ID,
        product_id:ID,
        model: IAPIUpdateQuantity,
        service: UpdateQuantityService = Depends()
):
    await service.call(user_id, product_id, model)