from pathlib import Path

from fastapi import Depends
from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from starlette import status

from src.core.infrastructures import rmq_broker
from src.core.types import IDModel
from src.core.utils import read_doc
from src.handlers.create.event import OrderCreatedEvent
from src.handlers.create.handler import create_order_handler
from src.handlers.list.api_output import OAPIOrder
from src.handlers.list.handler import get_order_list_by_user_id_handler
from src.handlers.resolve.service import (
    ConfirmStepTransactionOrderService,
    RejectTransactionOrderService,
    ServiceName,
)

router = RabbitRouter(url=rmq_broker.url, prefix="/orders", tags=["Заказы"])

router.add_api_route(
    "",
    methods=["POST"],
    endpoint=create_order_handler,
    status_code=status.HTTP_202_ACCEPTED,
    response_model=IDModel,
    summary="Создать заказ",
    description=read_doc(Path("src/handlers/create/doc.md")),
)

router.add_api_route(
    "/{user_id}",
    methods=["GET"],
    endpoint=get_order_list_by_user_id_handler,
    status_code=status.HTTP_200_OK,
    response_model=list[OAPIOrder],
    summary="Получить список заказов пользователя",
    description=read_doc(Path("src/handlers/list/doc.md")),
)

@router.subscriber(
    queue=RabbitQueue(
        "service.order.profile.money_has_been_debited",
        routing_key="event.order.profile.money_has_been_debited",
    ),
    exchange=rmq_broker.exchange,
)
async def commit_order_profile(
        model: OrderCreatedEvent,
        service: ConfirmStepTransactionOrderService = Depends(),
):
    await service.call(model, ServiceName.profile)

@router.subscriber(
    queue=RabbitQueue(
        "service.order.products.product_quantities_calculated",
        routing_key="event.order.products.product_quantities_calculated",
    ),
    exchange=rmq_broker.exchange,
)
async def commit_order_product(
        model: OrderCreatedEvent,
        service: ConfirmStepTransactionOrderService = Depends(),
):
    await service.call(model, ServiceName.product)

@router.subscriber(
    queue=RabbitQueue(
        "service.order.profile.not_enough_money",
        routing_key="event.order.profile.not_enough_money",
    ),
    exchange=rmq_broker.exchange,
)
async def reject_order_profile_reason(
        model: OrderCreatedEvent,
        service: RejectTransactionOrderService = Depends(),
):
    await service.call(model, ServiceName.profile)

@router.subscriber(
    queue=RabbitQueue(
        "service.order.products.not_enough_product",
        routing_key="event.order.products.not_enough_product",
    ),
    exchange=rmq_broker.exchange,
)
async def reject_order_store_reason(
        model: OrderCreatedEvent,
        service: RejectTransactionOrderService = Depends(),
):
    await service.call(model, ServiceName.product)
