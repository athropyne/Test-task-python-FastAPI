from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.cart.update_quantity.api_input import IAPIUpdateQuantityProductInCart
from src.services.cart.update_quantity.service import UpdateQuantityProductInCartService

async def update_quantity_handler(
        product_id: ID,
        model: IAPIUpdateQuantityProductInCart,
        client_id: int = Depends(TokenManager.id),
        service: UpdateQuantityProductInCartService = Depends()
):
    return await service.call(client_id, product_id, model)