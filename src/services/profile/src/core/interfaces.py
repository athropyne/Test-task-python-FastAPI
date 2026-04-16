from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from src.core.infrastructures import postgresql

class PGConnection:
    c = None
    def __init__(self, _connection: AsyncConnection = Depends(postgresql)):
        self._c = _connection

    def __call__(self):
        return self._c
