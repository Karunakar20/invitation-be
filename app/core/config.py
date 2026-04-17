from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv


def _repo_root() -> Path:
    # app/core/config.py -> app/core -> app -> repo root
    return Path(__file__).resolve().parents[3]


load_dotenv(dotenv_path=_repo_root() / ".env", override=False)


def _env(name: str, default: str | None = None) -> str | None:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value


@dataclass(frozen=True)
class Settings:
    # App / security
    secret_key: str = _env("SECRET_KEY", "secretkey123")  # keep default for compatibility
    jwt_algorithm: str = _env("JWT_ALGORITHM", "HS256")

    # Database
    db_user: str = _env("DB_USER", _env("POSTGRES_USER", "user"))  # docker-friendly
    db_password: str = _env("DB_PASSWORD", _env("POSTGRES_PASSWORD", "user@1234"))
    db_host: str = _env("DB_HOST", "127.0.0.1")
    db_port: str = _env("DB_PORT", "6000")
    db_name: str = _env("DB_NAME", _env("POSTGRES_DB", "wedding_db"))
    database_url_override: str | None = _env("DATABASE_URL")

    @property
    def database_url(self) -> str:
        if self.database_url_override:
            return self.database_url_override
        password = quote_plus(self.db_password)
        return (
            f"postgresql+psycopg2://{self.db_user}:{password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()

