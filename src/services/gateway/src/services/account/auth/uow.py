from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, CursorResult

from src.core.interfaces import PGConnection
from src.core.security import PasswordManager
from src.schema import accounts
from src.services.account.exc import InvalidUserOrPassword

class AuthUserUOW(PGConnection):

    async def call(self, model: OAuth2PasswordRequestForm):
        stmt = select(accounts.c.id, accounts.c.password).where(accounts.c.username == model.username)
        cursor: CursorResult = await self().execute(stmt)
        result = cursor.fetchone()
        if result is None: raise InvalidUserOrPassword
        user_id, current_password = result
        if not PasswordManager.verify(model.password, current_password): raise InvalidUserOrPassword
        return user_id