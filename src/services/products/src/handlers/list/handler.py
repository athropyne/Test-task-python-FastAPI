from fastapi import Depends

from src.handlers.list.service import GetProductListService

async def get_product_list_handler(
        service: GetProductListService = Depends(),
):
    return await service.call()
