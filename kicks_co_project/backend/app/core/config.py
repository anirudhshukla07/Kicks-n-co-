from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    database_url: str = Field(alias='DATABASE_URL')
    session_cookie_name: str = Field(default='kicks_co_session', alias='SESSION_COOKIE_NAME')
    session_expire_hours: int = Field(default=24, alias='SESSION_EXPIRE_HOURS')
    frontend_url: str = Field(default='http://127.0.0.1:5173', alias='FRONTEND_URL')


@lru_cache
def get_settings() -> Settings:
    return Settings()
