from fastapi import Depends, HTTPException
from httpx import AsyncClient
from starlette import status

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import ID
from src.services.order.create.dto import DTOCreateOrder

class CreateOrderService:

    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self, client_id: ID):
        response = await self._http_client.get(
            f"{settings.SERVICE_CARTS_URL}/carts/{client_id}",
        )
        if response.status_code != 200:
            data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=data.get("detail"),
            )
        data = response.json()

        if len(data["products"]) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Корзина пуста",
            )
        model = DTOCreateOrder(**data)
        response = await self._http_client.post(
            f"{settings.SERVICE_ORDERS_URL}/orders",
            json=model.model_dump()
        )
        if response.status_code != 202:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return response.json()
