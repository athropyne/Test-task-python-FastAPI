from fastapi import HTTPException
from loguru import logger
from starlette import status

from src.core.types import ID


class InternalError(HTTPException):
    def __init__(self, detail: str | dict):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


class ClientError(HTTPException):
    def __init__(self, detail: str | dict):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class Conflict(HTTPException):
    def __init__(self, detail: str | dict):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class NotFound(HTTPException):
    def __init__(self, detail: str | dict):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class AccessDenied(HTTPException):
    def __init__(self, detail: str | dict| None = None):
        self.detail = detail
        if detail is None:
            detail = "У вас нет прав на это действие."
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotAuthorized(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class NoDataToUpdate(ClientError):
    def __init__(self):
        super().__init__(detail="Нет данных для обновления")
