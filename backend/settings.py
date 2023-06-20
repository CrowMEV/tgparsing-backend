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

    # cookie
    COOKIE_SECURE: bool = Field(default=False)
    COOKIE_AGE: int = Field(default=3600, ge=1, le=86400)
    SAME_SITE: str = Field(default="lax")

    # verify token
    TOKEN_AGE: int = Field(default=3600, ge=1, le=86400)

    # user settings
    IS_ACTIVE: bool = Field(default=True)

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
    def test_sync_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}"
            f"@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
        )

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
            # self.BASE_DIR,
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
    USER_REFRESH_TOKEN: str = "user_refresh_token"
    USER_ALL: str = "user_all"
    USER_BY_ID: str = "user_by_id"
    # role
    ROLE_GET: str = "role_get"
    ROLE_ADD: str = "role_add"
    ROLE_DELETE: str = "role_delete"
    ROLE_PATCH: str = "role_patch"
    ROLE_GET_ALL: str = "role_get_all"
    # tariffs
    TARIFF_GET: str = "tariff_get"
    TARIFF_ADD: str = "tariff_add"
    TARIFF_PATCH: str = "tariff_patch"
    TARIFF_DELETE: str = "tariff_delete"
    TARIFF_GET_ALL: str = "tariff_get_all"
    # tariff_prices
    TARIFF_PRICE_GET: str = "tariff_price_get"
    TARIFF_PRICE_ADD: str = "tariff_price_add"
    TARIFF_PRICE_PATCH: str = "tariff_price_patch"
    TARIFF_PRICES_GET: str = "tariff_prices_get"
    TARIFF_PRICE_GET_ALL: str = "tariff_price_get_all"
    TARIFF_PRICE_DELETE: str = "tariff_price_delete"
    # chat_members
    MEMBER_GET: str = "member_get"
    MEMBER_ADD: str = "member_add"
    MEMBER_PATCH: str = "member_patch"
    MEMBER_DELETE: str = "member_delete"
    MEMBER_GET_ALL: str = "member_get_all"
    # parcered_chats
    CHAT_GET: str = "chat_get"
    CHAT_ADD: str = "chat_add"
    CHAT_GET_ALL: str = "chat_get_all"
    CHAT_DELETE: str = "chat_delete"


config = Config()
