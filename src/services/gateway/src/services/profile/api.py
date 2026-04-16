from pathlib import Path

from fastapi import APIRouter
from starlette import status

from src.core.utils import read_doc
from src.services.profile.get_me.api_output import OAPIMeInfo
from src.services.profile.get_me.handler import get_me_handler
from src.services.profile.topup_balance.handler import topup_balance_handler

profile_router = APIRouter(prefix="/auth", tags=["profile"])

profile_router.add_api_route(
    "/topup/",
    endpoint=topup_balance_handler,
    methods=["POST"],
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Добавить денег",
    description=read_doc(Path("src/services/profile/topup_balance/doc.md"))
)

profile_router.add_api_route(
    "/profile/",
    endpoint=get_me_handler,
    methods=["GET"],
    response_model=OAPIMeInfo,
    status_code=status.HTTP_200_OK,
    summary="Получить информацию о себе",
    description=read_doc(Path("src/services/profile/get_me/doc.md"))
)