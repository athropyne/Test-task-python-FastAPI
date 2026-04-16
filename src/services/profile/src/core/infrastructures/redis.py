from loguru import logger
from redis.asyncio import ConnectionPool, Redis


class RedisClient:
    def __init__(self,
                 host: str,
                 port: int,
                 login: str | None,
                 password: str | None,
                 db: int):
        if login is not None or password is not None:
            self.pool = ConnectionPool(
                host=host,
                port=port,
                username=login,
                password=password,
                db=db,
                decode_responses=True
            )
        else:
            self.pool = ConnectionPool(host=host, port=port, db=db, decode_responses=True)
        self.client = Redis(connection_pool=self.pool)

    async def __call__(self):
        return self.client