from pathlib import Path

from fastapi import Depends
from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from starlette import status

from src.core.infrastructures import rmq_broker
from src.core.types import IDModel
from src.core.utils import read_doc
from src.handlers.calculate_product_quantities.service import (
    CalculateProductQuantitiesService,
    CommitProductService,
    RollbackProductService,
)
from src.handlers.create.handler import create_product_handler
from src.handlers.dto import Product
from src.handlers.event import OrderCreatedEvent
from src.handlers.list.handler import get_product_list_handler
from src.handlers.one.handler import get_product_by_id_handler

router = RabbitRouter(url=rmq_broker.url, prefix="/products", tags=["Товары"])

router.add_api_route(
    "",
    methods=["POST"],
    endpoint=create_product_handler,
    status_code=status.HTTP_201_CREATED,
    response_model=IDModel,
    summary="Создать новый товар",
    description=read_doc(Path("src/handlers/create/doc.md")),
)

router.add_api_route(
    "",
    methods=["GET"],
    endpoint=get_product_list_handler,
    status_code=status.HTTP_200_OK,
    response_model=list[Product],
    summary="Получить список товаров",
    description=read_doc(Path("src/handlers/list/doc.md")),
)

router.add_api_route(
    "/{product_id}",
    methods=["GET"],
    endpoint=get_product_by_id_handler,
    status_code=status.HTTP_200_OK,
    response_model=Product,
    summary="Получить информацию о товаре",
    description=read_doc(Path("src/handlers/one/doc.md")),
)


@router.subscriber(
    RabbitQueue("service.product.order.created", routing_key="event.order.created"),
    exchange=rmq_broker.exchange,
)
async def calculate_product_quantities(
        model: OrderCreatedEvent,
        service: CalculateProductQuantitiesService = Depends()
):
    await service.call(model)


@router.subscriber(
    RabbitQueue("service.product.order.commited", routing_key="event.order.commited"),
    exchange=rmq_broker.exchange,
)
async def commit_order(
        model: OrderCreatedEvent,
        service: CommitProductService = Depends(),
):
    await service.call(model)

@router.subscriber(
    RabbitQueue("service.product.order.rejected", routing_key="event.order.rejected"),
    exchange=rmq_broker.exchange,
)
async def reject_order(
        model: OrderCreatedEvent,
        service: RollbackProductService = Depends(),
):
    await service.call(model)



