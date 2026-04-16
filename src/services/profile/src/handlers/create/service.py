from fastapi import Depends

from src.handlers.create.api_input import IAPICreateProfile
from src.handlers.create.uow import CreateProfileUOW

class CreateProfileService:

    def __init__(self, _uow: CreateProfileUOW = Depends()):
        self._uow = _uow

    async def call(self, model: IAPICreateProfile):
        await self._uow.call(model)
