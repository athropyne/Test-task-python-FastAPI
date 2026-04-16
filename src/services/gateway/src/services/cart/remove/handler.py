from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.cart.remove.service import RemoveProductFromCartService

async def remove_product_from_cart_handler(
        product_id: ID,
        client_id: ID = Depends(TokenManager.id),
        service: RemoveProductFromCartService = Depends()
):
    await service.call(client_id, product_id)