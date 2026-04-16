from src.config import settings
from src.core.infrastructures.fs_broker import RMQBroker
from src.core.infrastructures.postgresql import PostgresqlDB

postgresql = PostgresqlDB(
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    database=settings.POSTGRES_DB,
    debug=True
)

rmq_broker = RMQBroker(
    settings.RMQ_BROKER_LOGIN,
    settings.RMQ_BROKER_PASSWORD,
    settings.RMQ_BROKER_HOST,
    settings.RMQ_BROKER_PORT,
)



