from sqlalchemy import CursorResult

from src.core.interfaces import PGConnection
from src.core.types import ID
from src.schema import profiles
from src.handlers.exc import ProfileNotFound
from src.handlers.topup_balance.api_input import IAPIAmount

class TopUpBalanceUOW(PGConnection):

    async def call(self, user_id: ID, model: IAPIAmount):
        stmt = profiles.update().values(balance=profiles.c.balance + model.sum).where(profiles.c.id == user_id)
        cursor: CursorResult = await self().execute(stmt)
        if cursor.rowcount == 0: raise ProfileNotFound

