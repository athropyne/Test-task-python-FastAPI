from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine


class PostgresqlDB:

    def __init__(
            self,
            host: str,
            port: int,
            user: str,
            password: str,
            database: str,
            debug: bool = False,
    ):
        self.engine = create_async_engine(
            "postgresql+asyncpg://{}:{}@{}:{}/{}".format(user, password, host, port, database),
            echo=debug,
        )


    async def init(
            self,
            metadata: MetaData,
            clear_db: bool = False,
    ):
        async with self.engine.connect() as conn:
            if clear_db:
                await conn.run_sync(metadata.drop_all)
            await conn.run_sync(metadata.create_all)
            await conn.commit()
        await self.engine.dispose()

    async def drop(
            self,
            metadata: MetaData,
            clear_db: bool = False,
    ):
        async with self.engine.connect() as conn:
            await conn.run_sync(metadata.drop_all)
            await conn.commit()
        await self.engine.dispose()

    async def __call__(self):
        async with self.engine.connect() as connection:
            try:
                yield connection
                await connection.commit()
            except Exception as e:
                await connection.rollback()
                raise e
            finally:
                await connection.close()

# class UnitOfWork:
#     def __init__(self, engine: AsyncEngine):
#         self.engine = engine
#         self.connection = None
#
#     @asynccontextmanager
#     async def __call__(self):
#         async with self.engine.connect() as conn:
#             self.connection = conn
#             self
