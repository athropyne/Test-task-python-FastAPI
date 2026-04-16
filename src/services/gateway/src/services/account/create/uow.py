from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from src.core.interfaces import PGConnection
from src.schema import accounts
from src.services.account.create.db_input import IDBCreateUser
from src.services.account.exc import UsernameAlreadyExists

class CreateUserUOW(PGConnection):
    async def call(self, model: IDBCreateUser):
        stmt = accounts.insert().values(**model.model_dump()).returning(accounts.c.id)
        try: return await self().scalar(stmt)
        except IntegrityError as e:
            raise UsernameAlreadyExists if isinstance(e.orig.__cause__, UniqueViolationError) else e