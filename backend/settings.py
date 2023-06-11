import os

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    # run server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)

    # fastapi app
    IS_VERIFIED: bool = Field(default=False)
    DB_ECHO: bool = Field(default=True)

    # db
    DB_USER: str = Field(default="tg_db")
    DB_PASSWORD: str = Field(default="tg_db")
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="tg_db")

    @property
    def sync_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    # test db
    TEST_DB_USER: str = Field(default="test_tg_db")
    TEST_DB_PASSWORD: str = Field(default="test_tg_db")
    TEST_DB_HOST: str = Field(default="localhost")
    TEST_DB_PORT: int = Field(default=5432)
    TEST_DB_NAME: str = Field(default="test_tg_db")

    @property
    def test_async_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}"
            f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

    # secrets
    JWT_SECRET: str = Field(default="jwt_secret")
    FASTAPI_SECRET: str = Field(default="fastapi_secret")

    # static
    BASE_DIR: str = os.getcwd()
    STATIC_DIR: str = "static"
    AVATARS_FOLDER: str = "users_avatars"
    BASE_AVATAR_NAME: str = "base_avatar.png"

    @property
    def base_avatar_url(self) -> str:
        return os.path.join(
            self.BASE_DIR,
            self.STATIC_DIR,
            self.AVATARS_FOLDER,
            self.BASE_AVATAR_NAME,
        )

    # url names
    # user
    USER_REGISTER: str = "user_register"
    USER_LOGIN: str = "user_login"
    USER_LOGOUT: str = "user_logout"
    USER_PATCH: str = "user_patch"
    # role
    ROLE_GET: str = "role_get"
    ROLE_ADD: str = "role_add"
    ROLE_DELETE: str = "role_delete"
    ROLE_PATCH: str = "role_patch"
    ROLE_GET_ALL: str = "role_get_all"
    # tg account
    ACCOUNT_GET: str = "account_get"
    ACCOUNT_ADD: str = "account_add"
    ACCOUNT_DELETE: str = "account_delete"
    ACCOUNT_UPDATE: str = "account_update"
    ACCOUNT_GET_ALL: str = "account_get_all"


config = Config()
