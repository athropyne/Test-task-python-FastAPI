from fastapi import Depends
from faststream.rabbit.publisher import RabbitPublisher

from src.handlers.calculate_balance.exc import NotEnoughMoney
from src.handlers.calculate_balance.publisher import no_enough_money_publisher, money_has_been_debited_publisher
from src.handlers.calculate_balance.uow import CalculateBalanceUOW
from src.handlers.event import OrderCreatedEvent

class CalculateBalanceService:

    def __init__(
            self, _uow: CalculateBalanceUOW = Depends(),
            _no_enough_money_publisher: RabbitPublisher = Depends(lambda: no_enough_money_publisher),
            _money_has_been_debited_publisher: RabbitPublisher = Depends(lambda: money_has_been_debited_publisher),
    ):
        self._uow = _uow
        self._no_enough_money_publisher = _no_enough_money_publisher
        self._money_has_been_debited_publisher = _money_has_been_debited_publisher

    async def call(self, model: OrderCreatedEvent):
        try:
            await self._uow.call(model)
            await self._money_has_been_debited_publisher.publish(model.model_dump())
        except NotEnoughMoney: await self._no_enough_money_publisher.publish(model.model_dump())

class CommitBalanceService:

    def __init__(self, _uow: CalculateBalanceUOW = Depends()):
        self._uow = _uow

    async def call(self, model: OrderCreatedEvent):
        await self._uow.commit(model)

class RollbackBalanceService:

    def __init__(self, _uow: CalculateBalanceUOW = Depends()):
        self._uow = _uow

    async def call(self, model: OrderCreatedEvent):
        await self._uow.rollback(model)
