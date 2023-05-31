import os

from pydantic import BaseSettings, Field


class Config(BaseSettings):

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

    # server
    HOST: str = Field(default='0.0.0.0')
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)

    # db
    DB_USER: str = Field(default='tg_db')
    DB_PASSWORD: str = Field(default='tg_db')
    DB_HOST: str = Field(default='localhost')
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default='tg_db')

    # test db
    TEST_DB_USER: str = Field(default='test_tg_db')
    TEST_DB_PASSWORD: str = Field(default='test_tg_db')
    TEST_DB_HOST: str = Field(default='localhost')
    TEST_DB_PORT: int = Field(default=5432)
    TEST_DB_NAME: str = Field(default='test_tg_db')

    # secrets
    JWT_SECRET: str = Field(default='jwt_secret')
    FASTAPI_SECRET: str = Field(default='fastapi_secret')

    # static
    BASE_DIR = os.path.dirname(__file__)
    STATIC_DIR = "static"
    AVATARS_FOLDER = "users_avatars"
    BASE_AVATAR_NAME = "base_avatar.png"

    @property
    def sync_url(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}' \
               f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def async_url(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}' \
               f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def test_async_url(self):
        return f'postgresql+asyncpg://' \
               f'{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}' \
               f'@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'


config = Config()
