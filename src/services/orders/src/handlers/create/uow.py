from sqlalchemy import select, func

from src.core.interfaces import PGConnection
from src.handlers.create.api_input import IAPICreateOrder
from src.handlers.exc import EmptyProductList
from src.schema import orders, products

class CreateOrderUOW(PGConnection):

    async def call(self, model: IAPICreateOrder):
        if len(model.products) == 0: raise EmptyProductList
        stmt = orders.insert().values(user_id=model.user_id).returning(orders.c.id)
        order_id = await self().scalar(stmt)
        products_data = [{"order_id": order_id, **product.model_dump()} for product in model.products]
        stmt = products.insert().values(products_data)
        await self().execute(stmt)

        stmt = (
            select(
                orders,
                func.json_agg(
                    func.json_build_object(
                        "product_id", products.c.product_id,
                        "price", products.c.price,
                        "quantity", products.c.quantity,
                    ),
                ).label("products"),
            )
            .join(products, orders.c.id == products.c.order_id)
            .where(orders.c.id == order_id)
            .group_by(orders)
        )
        cursor = await self().execute(stmt)
        return cursor.mappings().fetchone()
