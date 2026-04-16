import pytest
from httpx import AsyncClient, ASGITransport

from src.app import app
from src.config import settings
from src.core.infrastructures import PostgresqlDB, postgresql, RedisClient, MailService
from src.schema import metadata

@pytest.fixture(scope="function")
async def db():
    _db = PostgresqlDB(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        database=settings.POSTGRES_DB,
    )
    await _db.init(metadata, clear_db=True)
    yield _db
    await _db.drop(metadata)
    await _db.engine.dispose()

@pytest.fixture(scope="function")
async def connection(db):
    async with db.engine.connect() as connection:
        yield connection

@pytest.fixture(scope="function")
async def redis_service():
    redis_client = RedisClient(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        login=settings.REDIS_LOGIN,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
    )
    yield await redis_client()
@pytest.fixture(scope="function")
async def mail_service():
    mail_service = MailService(
        email=settings.EMAIL_ADDRESS,
        password=settings.SMTP_SERVER_PASSWORD,
        smtp_server=settings.SMTP_SERVER_HOST,
        smtp_port=settings.SMTP_SERVER_PORT,
    )
    yield mail_service()
@pytest.fixture
async def client(db):
    app.dependency_overrides[postgresql] = db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
