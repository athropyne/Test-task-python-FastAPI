from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8003

    POSTGRES_HOST: str = "carts_postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "carts"

    RMQ_BROKER_HOST: str = "rabbitmq"
    RMQ_BROKER_PORT: int = 5672
    RMQ_BROKER_LOGIN: str = "guest"
    RMQ_BROKER_PASSWORD: str = "guest"
settings = Settings()
