from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+asyncpg://ledger:ledger@localhost:5432/ledger"
    test_database_url: str = "postgresql+asyncpg://ledger:ledger@localhost:5432/ledger_test"


@lru_cache
def get_settings() -> Settings:
    return Settings()
