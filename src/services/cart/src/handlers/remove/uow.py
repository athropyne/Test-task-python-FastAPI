from sqlalchemy import CursorResult

from src.core.interfaces import PGConnection
from src.core.types import ID
from src.handlers.exc import ProductNotFound
from src.schema import products

class RemoveProductUOW(PGConnection):

    async def call(self, user_id: ID, product_id: ID):
        stmt = (
            products
            .delete()
            .where(products.c.user_id == user_id)
            .where(products.c.product_id == product_id)
        )
        cursor: CursorResult = await self().execute(stmt)
        if cursor.rowcount == 0: raise ProductNotFound

