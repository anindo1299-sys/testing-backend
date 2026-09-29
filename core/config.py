from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Setting(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://root:ani2and2is5@127.0.0.1:3306/BackendTestProject"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int
    API_AUTH_KEY: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Setting()