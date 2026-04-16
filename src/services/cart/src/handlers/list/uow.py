from sqlalchemy import select, CursorResult

from src.core.interfaces import PGConnection
from src.core.types import ID
from src.schema import products

class GetOrderListByUserIdUOW(PGConnection):

    async def call(self, user_id: ID):
        stmt = (
            select(
                products.c.product_id,
                products.c.price,
                products.c.quantity,
            )
            .where(products.c.user_id == user_id)
        )
        cursor: CursorResult = await self().execute(stmt)
        return cursor.mappings().fetchall()
