from sqlalchemy import select, func, CursorResult

from src.core.interfaces import PGConnection
from src.core.types import ID
from src.schema import orders, products

class GetOrderListByUserIdUOW(PGConnection):

    async def call(self, user_id: ID):
        stmt = (
            select(
                orders.c.id,
                orders.c.status,
                orders.c.rejected_reason,
                func.json_agg(
                    func.json_build_object(
                        "product_id", products.c.product_id,
                        "price", products.c.price,
                        "quantity", products.c.quantity,
                    ),
                ).label("products"),
                orders.c.created_at,
            )
            .join(products, products.c.order_id == orders.c.id)
            .where(orders.c.user_id == user_id)
            .group_by(
                orders.c.id,
                orders.c.status,
                orders.c.rejected_reason,
                orders.c.created_at,
            )
        )
        cursor: CursorResult = await self().execute(stmt)
        return cursor.mappings().fetchall()
