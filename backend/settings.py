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

    # secrets
    JWT_SECRET: str = Field(default='jwt_secret')
    FASTAPI_SECRET: str = Field(default='fastapi_secret')

    UPLOADED_FILES_PATH = "media/"

    @property
    def sync_url(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}' \
               f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def async_url(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}' \
               f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


config = Config()
