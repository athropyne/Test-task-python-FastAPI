from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.order.list.service import GetOrderListService

async def get_order_list_handler(
        client_id:  ID = Depends(TokenManager.id),
        service: GetOrderListService = Depends()
):
    return await service.call(client_id)