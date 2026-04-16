from fastapi import Depends, HTTPException
from httpx import AsyncClient

from src.config import settings
from src.core.infrastructures import http_client
from src.core.types import IDModel
from src.services.account.create.api_input import IAPICreateUser
from src.services.account.create.db_input import IDBCreateUser
from src.services.account.create.uow import CreateUserUOW

class CreateUserService:

    def __init__(
            self, _uow: CreateUserUOW = Depends(),
            _http_client: AsyncClient = Depends(http_client),
    ):
        self._uow = _uow
        self._http_client = _http_client

    async def call(self, model: IAPICreateUser):
        _model = IDBCreateUser(**model.model_dump())
        user_id = await self._uow.call(_model)
        response = await self._http_client.post(
            f"{settings.SERVICE_PROFILES_URL}/profiles",
            json={"id": user_id, "email": model.email},
        )
        if response.status_code != 201:
            data = response.json()
            raise HTTPException(status_code=response.status_code, detail=data.get("detail"))

        return IDModel(id=user_id)
