from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Book Catalogue API"
    database_url: str = (
        f"sqlite:///{Path(__file__).resolve().parent.parent / 'data' / 'books.db'}"
    )


settings = Settings()
