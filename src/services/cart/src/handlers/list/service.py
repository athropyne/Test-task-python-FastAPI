from fastapi import Depends

from src.core.types import ID
from src.handlers.list.api_output import OAPICart, Product
from src.handlers.list.uow import GetOrderListByUserIdUOW

class GetOrderListByUserIdService:

    def __init__(self, _uow: GetOrderListByUserIdUOW = Depends()):
        self._uow = _uow

    async def call(self, user_id: ID):
        products = await self._uow.call(user_id)
        if len(products) == 0: return OAPICart(user_id=user_id, price=0, products=[])
        products = [Product(**product) for product in products]
        price = sum(product.price * product.quantity for product in products)
        output = OAPICart(user_id=user_id, price=price, products=products)
        return output
