from sqlalchemy import select, CursorResult

from src.core.interfaces import PGConnection
from src.handlers.create.event import OrderCreatedEvent
from src.schema import orders, OrderStatus

class ResolveOrderUOW(PGConnection):

    async def _check_commited_services(self, model: OrderCreatedEvent):
        stmt = (
            select(
                orders.c.profile_service_ok,
                orders.c.product_service_ok,
            )
            .where(orders.c.id == model.id)
        )
        cursor: CursorResult = await self().execute(stmt)
        result = cursor.mappings().fetchone()
        return result["profile_service_ok"], result["product_service_ok"]




    async def commit_profile(self, model: OrderCreatedEvent):
        stmt = (
            orders
            .update()
            .values(profile_service_ok=True)
            .where(orders.c.id == model.id)
        )
        await self().execute(stmt)
        return await self._check_commited_services(model)



    async def commit_product(self, model: OrderCreatedEvent):
        stmt = (
            orders
            .update()
            .values(product_service_ok=True)
            .where(orders.c.id == model.id)
        )
        await self().execute(stmt)
        return await self._check_commited_services(model)

    async def commit(self, model: OrderCreatedEvent):
        stmt = (
            orders
            .update()
            .values(status=OrderStatus.READY)
            .where(orders.c.id == model.id)
        )
        await self().execute(stmt)

    async def rollback(self, model: OrderCreatedEvent, reason: str):
        stmt = (
            orders
            .update()
            .values(status=OrderStatus.REJECTED, rejected_reason=reason)
            .where(orders.c.id == model.id)
        )
        await self().execute(stmt)
