from pathlib import Path
from typing import Literal, Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    BASE_DIR: Path = Path(__file__).parent

    # run server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=True)

    # fastapi app
    APP_NAME: str = "TgParsing"
    SECRET: str = Field(default="secret")
    DB_ECHO: bool = Field(default=True)

    # redis
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_DB: int = Field(default=0)

    # celery
    BROKER_HOST: str = Field(default="localhost")
    BROKER_PORT: int = Field(default=6379)

    # parser server
    PARSER_SERVER: str = Field(default="http://localhost:8001")

    # cookie
    COOKIE_NAME: str = Field(default="TgParsing")
    COOKIE_SECURE: bool = Field(default=False)
    COOKIE_AGE: int = Field(default=86400, ge=1, le=86400)
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
    STATIC_DIR_NAME: str = Field(default="static")
    AVATARS_FOLDER: str = Field(default="users_avatars")
    BASE_AVATAR_NAME: str = Field(default="base_avatar.png")

    @property
    def static_dir_url(self) -> Path:
        return Path(self.STATIC_DIR_NAME)

    @property
    def base_avatar_url(self) -> Path:
        return (
            self.static_dir_url / self.AVATARS_FOLDER / self.BASE_AVATAR_NAME
        )

    # files
    FILES_DIR: str = Field(default="files")

    @property
    def files_dir_url(self) -> Path:
        return self.BASE_DIR / self.FILES_DIR

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
    USER_CHECK_PASSWORD: str = Field(default="check_password")
    USER_PATCH_BY_ADMIN: str = Field(default="user_admin_patch")
    # role
    ROLE_GET: str = Field(default="role_get")
    ROLE_ADD: str = Field(default="role_add")
    ROLE_DELETE: str = Field(default="role_delete")
    ROLE_PATCH: str = Field(default="role_patch")
    ROLE_GET_ALL: str = Field(default="role_get_all")
    # payment
    PAYMENT_ADD: str = Field(default="payment_get_link")
    PAYMENTS_GET: str = Field(default="payments_get")
    # robokassa settings
    RK_CHECK_LOGIN: str = Field(default="")
    RK_PAYMENT_URL: str = Field(default="")
    RK_CHECK_PASS_1ST: str = Field(default="")
    RK_CHECK_PASS_2ND: str = Field(default="")
    RK_TEST_MODE: int = Field(default=0)
    # tariffs
    TARIFF_GET_ALL: str = Field(default="tariff_get_all")
    TARIFF_GET: str = Field(default="tariff_get")
    TARIFF_ADD: str = Field(default="tariff_add")
    TARIFF_PATCH: str = Field(default="tariff_patch")
    TARIFF_DELETE: str = Field(default="tariff_delete")
    # telegram accounts
    TGACCOUNT_GET_ALL: str = Field(default="tg_get_all")
    TGACCOUNT_GET: str = Field(default="tg_get")
    TGACCOUNT_DELETE: str = Field(default="tg_delete")
    # chat_members
    MEMBER_BY_ID: str = Field(default="member_by_id")
    MEMBER_CREATE: str = Field(default="member_add")
    MEMBER_PATCH: str = Field(default="member_patch")
    MEMBER_DELETE: str = Field(default="member_delete")
    MEMBER_GET_ALL: str = Field(default="member_all")
    # tasks
    TASK_GET_ALL: str = Field(default="task_get_all")
    TASK_ME_DOWNLOAD_FILE: str = Field(default="task_me_download_file")
    TASK_ME_DELETE: str = Field(default="task_me_delete")
    TASK_ME_GET_ALL: str = Field(default="task_me_get_all")
    # parcered_chats
    CHAT_BY_ID: str = Field(default="chat_by_id")
    CHAT_CREATE: str = Field(default="chat_add")
    CHAT_GET_ALL: str = Field(default="chat_all")
    CHAT_DELETE: str = Field(default="chat_delete")
    # parser
    PARSER_MEMBERS: str = Field(default="parser_members")
    PARSER_ACTIVE_MEMBERS: str = Field(default="parser_active_members")


config = Config()
