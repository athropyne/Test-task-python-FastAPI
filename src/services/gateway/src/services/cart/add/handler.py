from fastapi import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.cart.add.api_input import IAPIAddProduct
from src.services.cart.add.service import AddProductInCartService

async def add_product_in_cart_handler(
        model: IAPIAddProduct,
        client_id: ID = Depends(TokenManager.id),
        service: AddProductInCartService = Depends()
):
    return await service.call(client_id, model)