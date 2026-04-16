from fastapi import Depends

from src.core.types import ID
from src.handlers.list.service import GetOrderListByUserIdService

async def get_cart_by_user_id_handler(
        user_id: ID,
        service: GetOrderListByUserIdService = Depends(),
):
    return await service.call(user_id)
