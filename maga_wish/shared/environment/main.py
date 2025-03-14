import secrets
from typing import Literal

from pydantic import PostgresDsn, RedisDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    REDIS_SERVER: str
    REDIS_PORT: int = 6379
    REDIS_PATH: str = ""

    PRODUCTS_API_URL: str = "http://challenge-api.luizalabs.com/api/product"

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def REDIS_DATABASE_URI(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_SERVER,
            port=self.REDIS_PORT,
            path=self.REDIS_PATH,
        )

    @property
    def REDIS_DATABASE_URI_STR(self) -> str:
        return str(self.REDIS_DATABASE_URI)


settings = Settings()  # type: ignore
