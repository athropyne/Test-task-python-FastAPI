from sqlalchemy import select, CursorResult

from src.core.interfaces import PGConnection
from src.schema import products

class GetProductListUOW(PGConnection):

    async def call(self):
        stmt = (
            select(
                products.c.id,
                products.c.title,
                products.c.description,
                products.c.user_price,
                products.c.quantity,
            )
        )
        cursor: CursorResult = await self().execute(stmt)
        return cursor.mappings().fetchall()
