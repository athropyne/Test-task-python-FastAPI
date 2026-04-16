from fastapi.params import Depends

from src.core.security import TokenManager
from src.core.types import ID
from src.services.profile.get_me.service import GetMeService

async def get_me_handler(
        client_id: ID = Depends(TokenManager.id),
        service: GetMeService = Depends(),
):
    return await service.call(client_id)
