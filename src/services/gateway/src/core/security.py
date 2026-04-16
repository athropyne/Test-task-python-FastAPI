import datetime

import jwt
import passlib.context
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from src.config import settings
from src.core.types import ID



pwd_context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token/")

class TokenManager:
    @classmethod
    def create(cls, subject: ID, exp: datetime.timedelta, data: dict | None = None) -> str:
        return jwt.encode(
            {
                "sub": str(subject),
                "exp": datetime.datetime.now() + exp,
                "data": data if data is not None else {},
            },
            settings.TOKEN_SECRET_KEY,
            algorithm="HS256")

    @classmethod
    def access(cls, subject: ID, data: dict | None = None) -> str:
        return cls.create(subject, datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES), data)

    @classmethod
    def refresh(cls, subject: ID, data: dict | None = None) -> str:
        return cls.create(subject, datetime.timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS), data)

    @classmethod
    def decode(cls, token: str = Depends(oauth2_scheme)) -> dict:
        try:
            payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен просрочен",
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный токен"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e)
            )

    @classmethod
    def data(cls, token: str = Depends(oauth2_scheme)) -> dict:
        return cls.decode(token)["data"]

    @classmethod
    def id(cls, token: str = Depends(oauth2_scheme)) -> ID:
        return ID(cls.decode(token)["sub"])


class PasswordManager:
    _context = passlib.context.CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def hash(cls, password: str) -> str:
        return cls._context.hash(password)

    @classmethod
    def verify(cls, plain: str, hashed_str: str) -> bool:
        return cls._context.verify(plain, hashed_str)
