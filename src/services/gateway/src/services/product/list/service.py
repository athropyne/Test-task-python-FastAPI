from fastapi import Depends, HTTPException
from httpx import AsyncClient
from starlette import status

from src.config import settings
from src.core.infrastructures import http_client

class GetProductListService:

    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self):
        response = await self._http_client.get(
            f"{settings.SERVICE_PRODUCTS_URL}/products",
        )
        data = response.json()
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code, detail=data.get("detail"))
        return data
