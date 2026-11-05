from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "grantavik_db"
    db_user: str = "grantavik_app"
    db_password: str

    bootstrap_secret: str | None = None

    jwt_secret: str = Field(min_length=32)
    access_token_minutes: int = Field(default=60, gt=0)


    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        env_prefix="GRANTAVIK_",
    )


settings = Settings()