import typing as t

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    database_url: SecretStr = Field(validation_alias="DATABASE_URL")
    database_url_sync: SecretStr = Field(validation_alias="DATABASE_URL_SYNC")

    @property
    def async_db_config(self) -> dict[str, t.Any]:
        return {
            "url": self.database_url.get_secret_value(),
            "pool_pre_ping": True,
            "pool_recycle": 1800,
            "pool_timeout": 30,
            "pool_size": 5,
            "max_overflow": 10,
        }


app_settings = Settings()
