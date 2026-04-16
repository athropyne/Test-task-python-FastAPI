from fastapi import Depends, HTTPException
from httpx import AsyncClient
from starlette import status

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import ID
from src.services.cart.update_quantity.api_input import IAPIUpdateQuantityProductInCart

class UpdateQuantityProductInCartService:
    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self, client_id: ID, product_id: ID, model: IAPIUpdateQuantityProductInCart):
        response = await self._http_client.patch(
            f"{settings.SERVICE_CARTS_URL}/carts/{client_id}/{product_id}",
            json=model.model_dump(),
        )
        if response.status_code != status.HTTP_200_OK:
            data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=data.get("detail"),
            )