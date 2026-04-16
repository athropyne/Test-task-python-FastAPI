from fastapi import Depends
from faststream.rabbit.publisher import RabbitPublisher

from src.handlers.calculate_product_quantities.exc import ThereIsNotEnoughProduct
from src.handlers.calculate_product_quantities.publisher import (
    product_quantities_calculated_publisher,
    there_is_not_enough_product_publisher,
)
from src.handlers.calculate_product_quantities.uow import CalculateProductQuantitiesUOW
from src.handlers.event import OrderCreatedEvent

class CalculateProductQuantitiesService:

    def __init__(
            self,
            _uow: CalculateProductQuantitiesUOW = Depends(),
            _product_quantities_calculated_publisher: RabbitPublisher = Depends(
                lambda: product_quantities_calculated_publisher,
            ),
            _there_is_not_enough_product_publisher: RabbitPublisher = Depends(
                lambda: there_is_not_enough_product_publisher,
            ),
    ):
        self._uow = _uow
        self._product_quantities_calculated_publisher = _product_quantities_calculated_publisher
        self._there_is_not_enough_product_publisher = _there_is_not_enough_product_publisher

    async def call(self, model: OrderCreatedEvent):
        try:
            await self._uow.call(model)
            await self._product_quantities_calculated_publisher.publish(model.model_dump())
        except ThereIsNotEnoughProduct:
            await self._there_is_not_enough_product_publisher.publish(model.model_dump())

class CommitProductService:

    def __init__(self, _uow: CalculateProductQuantitiesUOW = Depends()):
        self._uow = _uow

    async def call(self, model: OrderCreatedEvent):
        await self._uow.commit(model)

class RollbackProductService:

    def __init__(self, _uow: CalculateProductQuantitiesUOW = Depends()):
        self._uow = _uow

    async def call(self, model: OrderCreatedEvent):
        await self._uow.rollback(model)
