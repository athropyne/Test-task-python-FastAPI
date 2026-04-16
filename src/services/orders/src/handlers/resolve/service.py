import enum

from fastapi import Depends
from faststream.rabbit.publisher import RabbitPublisher

from src.handlers.create.event import OrderCreatedEvent
from src.handlers.resolve.publisher import commit_order_publisher, reject_order_publisher
from src.handlers.resolve.uow import ResolveOrderUOW

class ServiceName(enum.Enum):
    profile = 0
    product = 1

class ConfirmStepTransactionOrderService:

    def __init__(
            self, _uow: ResolveOrderUOW = Depends(),
            _publisher: RabbitPublisher = Depends(lambda: commit_order_publisher),
    ):
        self._uow = _uow
        self._publisher = _publisher

    async def call(self, model: OrderCreatedEvent, service_name: ServiceName):
        is_profile_ok, is_prodict_ok = None, None
        match service_name:
            case ServiceName.profile:
                is_profile_ok, is_prodict_ok = await self._uow.commit_profile(model)
            case ServiceName.product:
                is_profile_ok, is_prodict_ok = await self._uow.commit_product(model)

        if is_profile_ok is not None and is_prodict_ok is not None and all((is_profile_ok, is_prodict_ok)):
            await self._publisher.publish(model.model_dump())
            await self._uow.commit(model)


class RejectTransactionOrderService:

    def __init__(
            self, _uow: ResolveOrderUOW = Depends(),
            _publisher: RabbitPublisher = Depends(lambda: reject_order_publisher),
    ):
        self._uow = _uow
        self._publisher = _publisher

    async def call(self, model: OrderCreatedEvent, service_name: ServiceName):
        reason = ""
        match service_name:
            case ServiceName.profile: reason = "Не хватает денег на счете"
            case ServiceName.product:reason = "Не хватает товаров на складе"
        await self._uow.rollback(model, reason=reason)
        await self._publisher.publish(model.model_dump())

