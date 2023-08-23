from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    USER: str
    PASSWORD: str
    HOST: str

    class Config:
        env_file: str = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
