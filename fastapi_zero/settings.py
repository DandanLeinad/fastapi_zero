from fastapi_zero.settings import Settings
from pydantic_settings import BaseSettings, SettingsConfigDict

settings = Settings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    DATABASE_URL: str
    SECRET_KEY: str = settings.SECRET_KEY
    ALGORITHM: str = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRATION_MINUTES: int = (
        settings.ACCESS_TOKEN_EXPIRATION_MINUTES
    )
