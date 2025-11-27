import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.env.prod'),
        env_file_encoding='utf-8',
        extra='ignore',
    )
    DB_URL: str = os.getenv(
        'DB_URL',
        'postgresql+psycopg://user:password@127.0.0.1:5432/database',
    )
    DEBUG: bool = True


@lru_cache
def __get_settings() -> __Settings:
    return __Settings()


settings = __get_settings()
