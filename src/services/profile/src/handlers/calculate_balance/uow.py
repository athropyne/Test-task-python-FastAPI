from sqlalchemy import select

from src.core.interfaces import PGConnection
from src.handlers.calculate_balance.exc import NotEnoughMoney
from src.handlers.event import OrderCreatedEvent
from src.schema import debts, profiles, TransactionStatus

class CalculateBalanceUOW(PGConnection):

    async def call(self, model: OrderCreatedEvent):
        stmt = select(profiles.c.balance).where(profiles.c.id == model.user_id)
        balance = await self().scalar(stmt)
        price = sum([product.price * product.quantity for product in model.products])
        if balance < price: raise NotEnoughMoney
        stmt = (
            debts
            .insert()
            .values(
                transaction_id=model.transaction_id,
                amount=price,
                profile_id=model.user_id,
            )
        )
        await self().execute(stmt)
        stmt = (
            profiles
            .update()
            .values(balance=profiles.c.balance - price)
            .where(profiles.c.id == model.user_id)
        )
        await self().execute(stmt)

    async def commit(self, model: OrderCreatedEvent):
        stmt = (
            debts
            .update()
            .values(status=TransactionStatus.SUCCESS)
            .where(debts.c.transaction_id == model.transaction_id)
        )
        await self().execute(stmt)

    async def rollback(self, model: OrderCreatedEvent):
        stmt = (
            select(debts.c.amount)
            .where(debts.c.transaction_id == model.transaction_id)
        )

        amount = await self().scalar(stmt)
        if amount is not None:
            stmt = (
                debts
                .update()
                .values(status=TransactionStatus.FAILED)
                .where(debts.c.transaction_id == model.transaction_id)
            )
            await self().execute(stmt)
            stmt = (
                profiles
                .update()
                .values(balance=profiles.c.balance + amount)
                .where(profiles.c.id == model.user_id)
            )
            await self().execute(stmt)
