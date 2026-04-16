from sqlalchemy import select, CursorResult

from src.core.interfaces import PGConnection
from src.core.types import ID
from src.schema import profiles

class GetMeUOW(PGConnection):
    async def call(self, client_id: ID):
        stmt = select(profiles).where(profiles.c.id == client_id)
        cursor: CursorResult = await self().execute(stmt)
        return cursor.mappings().fetchone()