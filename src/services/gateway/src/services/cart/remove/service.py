from fastapi import Depends, HTTPException
from httpx import AsyncClient
from starlette import status

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import ID

class RemoveProductFromCartService:

    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self, client_id: ID, product_id: ID):
       response = await self._http_client.delete(
           f"{settings.SERVICE_CARTS_URL}/carts/{client_id}/{product_id}",
       )
       if response.status_code != status.HTTP_204_NO_CONTENT:
           data = response.json()
           raise HTTPException(
               status_code=response.status_code,
               detail=data.get("detail"),
           )