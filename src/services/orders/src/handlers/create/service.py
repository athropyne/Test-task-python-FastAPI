from fastapi import Depends
from faststream.rabbit.publisher import RabbitPublisher

from src.core.types import IDModel
from src.handlers.create.api_input import IAPICreateOrder
from src.handlers.create.event import OrderCreatedEvent
from src.handlers.create.publisher import order_created_publisher
from src.handlers.create.uow import CreateOrderUOW

class CreateOrderService:

    def __init__(
            self,
            _uow: CreateOrderUOW = Depends(),
            _publisher: RabbitPublisher = Depends(lambda: order_created_publisher),
    ):
        self._uow = _uow
        self._publisher = _publisher

    async def call(self, model: IAPICreateOrder):
        order = await self._uow.call(model)
        event = OrderCreatedEvent(**order)
        await self._publisher.publish(event.model_dump())
        return IDModel(id=event.id)
