from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class DBSettings(BaseSettings):
    DB_PORT: str
    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str
    DB_HOST: str
    DB_ENGINE: str


class Settings(BaseSettings):
    DATA_BASE: DBSettings = DBSettings()
    SECRET: str
    COOKIES_LIFETIME: int


settings = Settings()