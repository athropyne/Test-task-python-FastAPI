from fastapi import Depends

from src.core.types import ID
from src.handlers.exc import ProfileNotFound
from src.handlers.get_me.api_output import OAPIMeInfo
from src.handlers.get_me.uow import GetMeUOW

class GetMeService:

    def __init__(self, _uow: GetMeUOW = Depends()):
        self._uow = _uow

    async def call(self, client_id: ID):
        result = await self._uow.call(client_id)
        if result is None: raise ProfileNotFound
        return OAPIMeInfo(**result)
