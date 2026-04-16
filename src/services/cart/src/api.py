from pathlib import Path

from fastapi import Depends
from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter
from starlette import status

from src.core.infrastructures import rmq_broker
from src.core.utils import read_doc
from src.handlers.add.handler import add_product_in_cart_handler
from src.handlers.clear.service import ClearCartService
from src.handlers.event import OrderCreatedEvent
from src.handlers.list.api_output import OAPICart
from src.handlers.list.handler import get_cart_by_user_id_handler
from src.handlers.remove.handler import remove_product_from_cart_handler
from src.handlers.update_quantity.handler import update_product_quantity_handler

router = RabbitRouter(url=rmq_broker.url, prefix="/carts", tags=["Корзины"])

router.add_api_route(
    "",
    methods=["POST"],
    endpoint=add_product_in_cart_handler,
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    summary="Добавить товар в корзину",
    description=read_doc(Path("src/handlers/add/doc.md")),
)

router.add_api_route(
    "/{user_id}",
    methods=["GET"],
    endpoint=get_cart_by_user_id_handler,
    status_code=status.HTTP_200_OK,
    response_model=OAPICart,
    summary="Получить список товаров в корзине пользователя по ID",
    description=read_doc(Path("src/handlers/list/doc.md")),
)

router.add_api_route(
    "/{user_id}/{product_id}",
    methods=["DELETE"],
    endpoint=remove_product_from_cart_handler,
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Удалить товар из корзины",
    description=read_doc(Path("src/handlers/remove/doc.md")),
)

router.add_api_route(
    "/{user_id}/{product_id}",
    methods=["PATCH"],
    endpoint=update_product_quantity_handler,
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Изменить количество товара в корзине",
    description=read_doc(Path("src/handlers/update_quantity/doc.md")),
)

@router.subscriber(
    RabbitQueue("service.cart.order.accepted", routing_key="event.order.commited"),
    exchange=rmq_broker.exchange,
)
async def clear_cart_by_user_id(
        model: OrderCreatedEvent,
        service: ClearCartService = Depends()
):
    await service.call(model.user_id)


