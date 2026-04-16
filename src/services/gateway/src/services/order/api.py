from pathlib import Path

from fastapi import APIRouter
from starlette import status

from src.core.types import IDModel
from src.core.utils import read_doc
from src.services.order.create.handler import create_order_handler
from src.services.order.list.handler import get_order_list_handler

order_router = APIRouter(prefix="/orders", tags=["Заказы"])

order_router.add_api_route(
    "/create/",
    methods=["POST"],
    endpoint=create_order_handler,
    status_code=status.HTTP_202_ACCEPTED,
    response_model=IDModel,
    summary="Сформировать заказ",
    description=read_doc(Path("src/services/order/create/doc.md"))
)


order_router.add_api_route(
    "/",
    methods=["GET"],
    endpoint=get_order_list_handler,
    status_code=status.HTTP_200_OK,
    summary="Получить список заказов",
    description=read_doc(Path("src/services/order/list/doc.md"))
)

