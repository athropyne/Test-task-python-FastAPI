from pathlib import Path

from fastapi import APIRouter
from starlette import status

from src.core.types import IDModel
from src.core.utils import read_doc
from src.services.account.auth.api_output import TokenModel
from src.services.account.auth.handler import auth_user_handler

from src.services.account.create.handler import create_user_handler
from src.services.account.refresh.handler import refresh_tokens_handler

account_router = APIRouter(prefix="/auth", tags=["Учетные записи"])

account_router.add_api_route(
    "/register/",
    methods=["POST"],
    endpoint=create_user_handler,
    status_code=status.HTTP_201_CREATED,
    response_model=IDModel,
    summary="Создать пользователя",
    description=read_doc(Path("src/services/account/create/doc.md")),
)

account_router.add_api_route(
    "/token/",
    methods=["POST"],
    endpoint=auth_user_handler,
    status_code=status.HTTP_200_OK,
    response_model=TokenModel,
    summary="Аутентифицировать пользователя",
    description=read_doc(Path("src/services/account/auth/doc.md")),
)

account_router.add_api_route(
    "/token/refresh/",
    methods=["POST"],
    endpoint=refresh_tokens_handler,
    status_code=status.HTTP_200_OK,
    response_model=TokenModel,
    summary="Обновить токены доступа",
    description=read_doc(Path("src/services/account/refresh/doc.md")),
)
