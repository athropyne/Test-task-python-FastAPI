from fastapi.params import Depends

from src.core.types import ID
from src.handlers.get_me.service import GetMeService

async def get_me_handler(
        user_id: ID,
        service: GetMeService = Depends(),
):
    return await service.call(user_id)