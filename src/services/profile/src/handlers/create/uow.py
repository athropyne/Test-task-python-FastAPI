from asyncpg import UniqueViolationError
from sqlalchemy import select, exists
from sqlalchemy.exc import IntegrityError

from src.core.interfaces import PGConnection
from src.schema import profiles
from src.handlers.create.api_input import IAPICreateProfile
from src.handlers.exc import EmailAlreadyExists

class CreateProfileUOW(PGConnection):
    async def call(self, model: IAPICreateProfile):
        stmt = select(
            exists().where(profiles.c.id == model.id),
            exists().where(profiles.c.email == model.email),
        )
        results = await self().execute(stmt)
        user_id, email = results.fetchone()
        if user_id: raise ProfileIdAlreadyExists
        if email: raise EmailAlreadyExists

        stmt = profiles.insert().values(**model.model_dump())
        try: await self().execute(stmt)
        except IntegrityError as e:
            print(e.orig)
            raise EmailAlreadyExists if isinstance(e.orig.__cause__, UniqueViolationError) else e