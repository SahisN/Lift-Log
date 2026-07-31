from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Secrets(BaseSettings):
    database_url: SecretStr = SecretStr("")
    async_database_url: SecretStr = SecretStr("")


class DatabaseConfig:
    def __init__(self, data: dict[str, Any]):
        self.pool_min_size: int = data.get("default_size", 1)
        self.default_page: int = data.get("default_page", 1)
        self.min_size: int = data.get("min_size", 1)
        self.max_size: int = data.get("max_size", 100)
        self.min_page: int = data.get("min_page", 1)
        self.max_page: int = data.get("max_page", 100)


class Settings:
    def __init__(self, yaml_path: str | Path | None = None):
        raw = self._load_yaml(yaml_path)
        self.secrets = Secrets()
        app_raw = raw.get("app", {})
        self.app_name: str = app_raw.get("name", "")
        self.database = DatabaseConfig(raw.get("database", {}))

    @staticmethod
    def _load_yaml(path: str | Path | None = None) -> dict[str, Any]:
        if path is None:
            candidate = Path(__file__).resolve().parent.parent.parent / "config.yaml"
            if not candidate.exists():
                candidate = Path.cwd() / "config.yaml"

            path = candidate
        with open(path) as file:
            data = yaml.safe_load(file)
            return data if isinstance(data, dict) else {}


@lru_cache(maxsize=1)
def get_settings(yaml_path: str | None = None) -> Settings:
    return Settings(yaml_path)
