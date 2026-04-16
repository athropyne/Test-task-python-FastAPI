from pathlib import Path

from fastapi import Depends
from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from starlette import status

from src.core.infrastructures import rmq_broker
from src.core.utils import read_doc
from src.handlers.calculate_balance.service import CalculateBalanceService, RollbackBalanceService, CommitBalanceService
from src.handlers.create.handler import create_profile_handler
from src.handlers.event import OrderCreatedEvent
from src.handlers.get_me.api_output import OAPIMeInfo
from src.handlers.get_me.handler import get_me_handler
from src.handlers.topup_balance.handler import topup_balance_handler

router = RabbitRouter(url=rmq_broker.url, prefix="/profiles", tags=["Профили"])

router.add_api_route(
    "",
    methods=["POST"],
    endpoint=create_profile_handler,
    status_code=status.HTTP_201_CREATED,
    summary="Создать профиль",
    description=read_doc(Path("src/handlers/create/doc.md")),
)
router.add_api_route(
    "/{user_id}",
    methods=["GET"],
    endpoint=get_me_handler,
    status_code=status.HTTP_200_OK,
    response_model=OAPIMeInfo,
    summary="Получить информацию о себе",
    description=read_doc(Path("src/handlers/get_me/doc.md")),
)
router.add_api_route(
    "/{user_id}/topup",
    methods=["POST"],
    endpoint=topup_balance_handler,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Добавить денег",
    description=read_doc(Path("src/handlers/topup_balance/doc.md")),
)

@router.subscriber(
    RabbitQueue("service.profile.order.created", routing_key="event.order.created"),
    exchange=rmq_broker.exchange,
)
async def calculate_balance(
        model: OrderCreatedEvent,
        service: CalculateBalanceService = Depends(),
):
    await service.call(model)

@router.subscriber(
    RabbitQueue("service.profile.order.commited", routing_key="event.order.commited"),
    exchange=rmq_broker.exchange,
)
async def commit_order(
        model: OrderCreatedEvent,
        service: CommitBalanceService = Depends(),
):
    await service.call(model)

@router.subscriber(
    RabbitQueue("service.profile.order.rejected", routing_key="event.order.rejected"),
    exchange=rmq_broker.exchange,
)
async def reject_order(
        model: OrderCreatedEvent,
        service: RollbackBalanceService = Depends(),
):
    await service.call(model)
