from fastapi import Depends

from src.handlers.create.api_input import IAPICreateProfile
from src.handlers.create.service import CreateProfileService

async def create_profile_handler(
        model: IAPICreateProfile,
        service: CreateProfileService = Depends(),
):
    return await service.call(model)
