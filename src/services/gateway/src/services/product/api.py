from pathlib import Path

from fastapi import APIRouter, Depends
from starlette import status

from src.core.security import TokenManager
from src.core.types import IDModel
from src.core.utils import read_doc
from src.services.product.create.handler import create_product_handler
from src.services.product.list.api_output import Product
from src.services.product.list.handler import get_product_list_handler
from src.services.product.one.handler import get_product_by_id_handler

product_router = APIRouter(prefix="/products", tags=["Товары"])

product_router.add_api_route(
    "/",
    methods=["POST"],
    endpoint=create_product_handler,
    response_model=IDModel,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый товар",
    description=read_doc(Path("src/services/product/create/doc.md")),
)

product_router.add_api_route(
    "/",
    methods=["GET"],
    endpoint=get_product_list_handler,
    response_model=list[Product],
    status_code=status.HTTP_200_OK,
    summary="Получить список продуктов",
    description=read_doc(Path("src/services/product/list/doc.md")),
)

product_router.add_api_route(
    "/{product_id}",
    methods=["GET"],
    endpoint=get_product_by_id_handler,
    response_model=Product,
    status_code=status.HTTP_200_OK,
    summary="Получить продукт по ID",
    description=read_doc(Path("src/services/product/one/doc.md")),
)