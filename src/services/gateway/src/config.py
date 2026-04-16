from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000

    POSTGRES_HOST: str = "gateway_postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "gateway"

    TOKEN_SECRET_KEY: str = "supersecret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 36000
    REFRESH_TOKEN_EXPIRE_HOURS: int = 2400

    REDIS_LOGIN: str | None = None
    REDIS_PASSWORD: str | None = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    RMQ_BROKER_HOST: str = "rabbitmq"
    RMQ_BROKER_PORT: int = 5672
    RMQ_BROKER_LOGIN: str = "guest"
    RMQ_BROKER_PASSWORD: str = "guest"

    SERVICE_PROFILES_URL: str = "http://profile-service:8001"
    SERVICE_PRODUCTS_URL: str = "http://product-service:8002"
    SERVICE_CARTS_URL: str = "http://cart-service:8003"
    SERVICE_ORDERS_URL: str = "http://order-service:8004"

settings = Settings()
