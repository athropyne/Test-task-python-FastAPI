from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.cart.list.service import GetCartService

async def get_cart_handler(
        client_id: ID = Depends(TokenManager.id),
        service: GetCartService = Depends()
):
    return await service.call(client_id)