from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from src.core.interfaces import PGConnection
from src.handlers.add.api_input import IAPIAddProduct
from src.handlers.exc import ProductAlreadyExists
from src.schema import products

class AddProductUOW(PGConnection):

    async def call(self, model: IAPIAddProduct):
        stmt = products.insert().values(model.model_dump()).returning(products)
        try: await self().execute(stmt)
        except IntegrityError as e:
            raise ProductAlreadyExists if isinstance(e.orig.__cause__, UniqueViolationError) else e
