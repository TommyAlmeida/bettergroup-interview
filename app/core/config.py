from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/backend_challenge")
    api_key: str = Field(default="change_me")
    candidate_id: str = Field(default="change_me")
    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings():
    return Settings()
