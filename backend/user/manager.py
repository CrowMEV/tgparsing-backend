from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from user.dependencies import get_user_db
from user.schemas import UserCreate
from database.models.user_model import User
from settings import config


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = config.FASTAPI_SECRET
    verification_token_secret = config.FASTAPI_SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
