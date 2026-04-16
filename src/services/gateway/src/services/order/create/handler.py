from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.order.create.service import CreateOrderService

async def create_order_handler(
        client_id: ID = Depends(TokenManager.id),
        service: CreateOrderService = Depends()
):
    return await service.call(client_id)