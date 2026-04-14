from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Book Catalogue API"
    app_version: str = "1.1.0"
    database_url: str = (
        f"sqlite:///{Path(__file__).resolve().parent.parent / 'data' / 'books.db'}"
    )
    # If set, POST/PATCH/DELETE require header: X-API-Key: <value>
    api_key: str | None = None


settings = Settings()
