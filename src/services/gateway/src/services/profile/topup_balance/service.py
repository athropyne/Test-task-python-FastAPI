from fastapi import Depends, HTTPException
from httpx import AsyncClient

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import ID
from src.services.profile.topup_balance.api_input import IAPIAmount

class TopUpBalanceService:

    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self, client_id: ID, model: IAPIAmount):
        response = await self._http_client.post(
            f"{settings.SERVICE_PROFILES_URL}/profiles/{client_id}/topup",
            json=model.model_dump()
        )
        if response.status_code != 204:
            data = response.json().get("detail")
            raise HTTPException(status_code=response.status_code, detail=data)


