from sqlalchemy import select

from src.core.interfaces import PGConnection
from src.core.types import ID
from src.schema import products

class GetProductByIdUOW(PGConnection):
    async def call(self, product_id: ID):
        stmt = select(products).where(products.c.id == product_id)
        cursor = await self().execute(stmt)
        return cursor.mappings().fetchone()