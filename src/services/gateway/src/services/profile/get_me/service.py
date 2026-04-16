from fastapi import Depends, HTTPException
from httpx import AsyncClient

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import ID
from src.services.profile.get_me.api_output import OAPIMeInfo

class GetMeService:

    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self, client_id: ID):
        response = await self._http_client.get(
            f"{settings.SERVICE_PROFILES_URL}/profiles/{client_id}",
        )
        data = response.json()
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=data.get("detail"),
            )
        return OAPIMeInfo(**data)
