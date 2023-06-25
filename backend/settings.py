import os
from typing import Optional, Literal

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
    APP_NAME: str = "TgParsing"
    SECRET: str = Field(default="secret")
    DB_ECHO: bool = Field(default=True)

    # cookie
    COOKIE_NAME: str = Field(default="TgParsing")
    COOKIE_SECURE: bool = Field(default=False)
    COOKIE_AGE: int = Field(default=3600, ge=1, le=86400)
    COOKIE_HTTPONLY: bool = Field(default=False)
    COOKIE_SAME_SITE: Optional[Literal["lax", "strict", "none"]] = Field(
        default="lax"
    )

    # jwt
    JWT_ALGORITHM = "HS256"
    JWT_TOKEN_AGE: int = Field(default=3600, ge=1, le=86400)

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
    STATIC_DIR: str = Field(default="static")
    AVATARS_FOLDER: str = Field(default="users_avatars")
    BASE_AVATAR_NAME: str = Field(default="base_avatar.png")

    @property
    def base_avatar_url(self) -> str:
        return os.path.join(
            self.STATIC_DIR,
            self.AVATARS_FOLDER,
            self.BASE_AVATAR_NAME,
        )

    # url names
    # user
    USER_REGISTER: str = Field(default="user_register")
    USER_LOGIN: str = Field(default="user_login")
    USER_LOGOUT: str = Field(default="user_logout")
    USER_PATCH: str = Field(default="user_patch")
    USER_REFRESH_TOKEN: str = Field(default="user_refresh_token")
    USER_ALL: str = Field(default="user_all")
    USER_BY_ID: str = Field(default="user_by_id")
    USER_DELETE: str = Field(default="user_delete")
    # role
    ROLE_GET: str = Field(default="role_get")
    ROLE_ADD: str = Field(default="role_add")
    ROLE_DELETE: str = Field(default="role_delete")
    ROLE_PATCH: str = Field(default="role_patch")
    ROLE_GET_ALL: str = Field(default="role_get_all")
    # payment
    PAYMENT_ADD: str = Field(default="payment_get_link")
    # robokassa settings
    RK_CHECK_LOGIN: str = Field(default="")
    RK_PAYMENT_URL: str = Field(default="")
    RK_CHECK_PASS_1ST: str = Field(default="")
    RK_CHECK_PASS_2ND: str = Field(default="")
    RK_TAX_SYSTEM: str = Field(default="")
    RK_REPLENISHMENT_NAME: str = Field(default="")
    RK_TAX: str = Field(default="")
    # tariffs
    TARIFF_GET: str = Field(default="tariff_get")
    TARIFF_ADD: str = Field(default="tariff_add")
    TARIFF_PATCH: str = Field(default="tariff_patch")
    TARIFF_DELETE: str = Field(default="tariff_delete")
    TARIFF_GET_ALL: str = Field(default="tariff_get_all")
    # tariff_prices
    TARIFF_PRICE_GET: str = Field(default="tariff_price_get")
    TARIFF_PRICE_ADD: str = Field(default="tariff_price_add")
    TARIFF_PRICE_PATCH: str = Field(default="tariff_price_patch")
    TARIFF_PRICES_GET: str = Field(default="tariff_prices_get")
    TARIFF_PRICE_GET_ALL: str = Field(default="tariff_price_get_all")
    TARIFF_PRICE_DELETE: str = Field(default="tariff_price_delete")


config = Config()
