from src.core.interfaces import PGConnection
from src.core.types import ID
from src.schema import products

class ClearCartUOW(PGConnection):
    async def call(self, user_id: ID):
        stmt = products.delete().where(products.c.user_id == user_id)
        await self().execute(stmt)