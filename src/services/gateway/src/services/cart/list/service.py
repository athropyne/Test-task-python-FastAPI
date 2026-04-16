from fastapi import Depends
from httpx import AsyncClient

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import ID

class GetCartService:

    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self, client_id: ID):
        response = await self._http_client.get(
            f"{settings.SERVICE_CARTS_URL}/carts/{client_id}",
        )
        data = response.json()
        return data