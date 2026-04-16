from src.core.interfaces import PGConnection
from src.handlers.create.api_input import IAPICreateProduct
from src.schema import products

class CreateProductUOW(PGConnection):

    async def call(self, model: IAPICreateProduct):
        stmt = products.insert().values(model.model_dump()).returning(products.c.id)
        return await self().scalar(stmt)
