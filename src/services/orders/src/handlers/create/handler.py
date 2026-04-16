from fastapi import Depends

from src.handlers.create.api_input import IAPICreateOrder
from src.handlers.create.service import CreateOrderService

async def create_order_handler(
        model: IAPICreateOrder,
        service: CreateOrderService = Depends(),
):
    return await service.call(model)
