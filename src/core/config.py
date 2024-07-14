from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

if not find_dotenv():
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    db_echo: bool
    api_vi_prefix: str = "/api/v_1"

    @property
    def db_url(self):
        # postgresql+psycopg://postgres:postgres@localhost:5432/TG_Bot_MarketCoinBot
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def db_url_test(self):
        # postgresql+psycopg://postgres:postgres@localhost:5432/TG_Bot_MarketCoinBot
        return f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"


settings = Settings()
