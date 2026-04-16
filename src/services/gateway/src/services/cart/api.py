from pathlib import Path

from fastapi import APIRouter
from starlette import status

from src.core.utils import read_doc
from src.services.cart.add.handler import add_product_in_cart_handler
from src.services.cart.list.handler import get_cart_handler
from src.services.cart.remove.handler import remove_product_from_cart_handler
from src.services.cart.update_quantity.handler import update_quantity_handler

cart_router = APIRouter(prefix="/cart", tags=["Корзина"])

cart_router.add_api_route(
    "/items/",
    methods=["POST"],
    endpoint=add_product_in_cart_handler,
    status_code=status.HTTP_201_CREATED,
    summary="Добавить товар в корзину",
    description=read_doc(Path("src/services/cart/add/doc.md"))
)

cart_router.add_api_route(
    "/",
    methods=["GET"],
    endpoint=get_cart_handler,
    status_code=status.HTTP_200_OK,
    summary="Получить товары в корзине",
    description=read_doc(Path("src/services/cart/list/doc.md")),
)

cart_router.add_api_route(
    "/items/{product_id}/",
    methods=["PATCH"],
    endpoint=update_quantity_handler,
    status_code=status.HTTP_200_OK,
    summary="Изменить количество товара в корзине",
    description=read_doc(Path("src/services/cart/update_quantity/doc.md")),
)

cart_router.add_api_route(
    "/items/{product_id}/",
    methods=["DELETE"],
    endpoint=remove_product_from_cart_handler,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить товар из корзины",
    description=read_doc(Path("src/services/cart/remove/doc.md")),
)