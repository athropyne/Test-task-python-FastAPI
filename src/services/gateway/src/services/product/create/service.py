from fastapi import Depends, HTTPException
from httpx import AsyncClient

from src.config import settings
from src.core.infrastructures import http_client
from src.services.product.create.api_input import IAPICreateProduct

class CreateProductService:
    def __init__(self,_http_client: AsyncClient = Depends(http_client)):
        self._http_client = _http_client


    async def call(self, model: IAPICreateProduct):
        response = await self._http_client.post(
            f"{settings.SERVICE_PRODUCTS_URL}/products",
            json=model.model_dump()
        )
        if response.status_code != 201:
            data = response.json().get("detail")
            raise HTTPException(status_code=response.status_code, detail=data)
        return response.json()
