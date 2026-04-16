from sqlalchemy import select, CursorResult

from src.core.interfaces import PGConnection
from src.core.types import ID
from src.handlers.exc import ProductNotFound
from src.handlers.update_quantity.api_input import IAPIUpdateQuantity
from src.schema import products

class UpdateProductQuantityUOW(PGConnection):

    async def call(self, user_id: ID, product_id: ID, model: IAPIUpdateQuantity):
        stmt = (
            products
            .update()
            .values(**model.model_dump())
            .where(products.c.product_id == product_id)
            .where(products.c.user_id == user_id)
        )
        cursor: CursorResult = await self().execute(stmt)
        if cursor.rowcount == 0: raise ProductNotFound

