from fastapi import Depends, HTTPException
from httpx import AsyncClient

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import ID
from src.services.cart.add.api_input import IAPIAddProduct

class AddProductInCartService:

    def __init__(self, _http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client

    async def call(self, client_id: ID, model: IAPIAddProduct):
        response = await self._http_client.get(
            f"{settings.SERVICE_PRODUCTS_URL}/products/{model.product_id}",
        )
        product_data = response.json()
        if response.status_code != 200: raise HTTPException(
                status_code=response.status_code,
                detail=product_data.get("detail"),
        )
        data = model.model_dump()
        data["user_id"] = client_id
        data["price"] = product_data["price"]
        response = await self._http_client.post(
            f"{settings.SERVICE_CARTS_URL}/carts",
            json=data,
        )
        if response.status_code != 201:
            data = response.json()
            raise HTTPException(
                status_code=response.status_code,
                detail=data.get("detail"),
            )

