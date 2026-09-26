from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    DATABASE_URL: str = "mysql+aiomysql://root:ani2and2is5@127.0.0.1:3306/BackendTestProject"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int
    class Config:
        env_file = ".env"

settings = Setting()