from typing import Optional

from fastapi import Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users import exceptions, models

from user import schemas
from user.schemas import UserLogin
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

    async def authenticate(self, credentials: UserLogin) -> Optional[models.UP]:
        """
        Authenticate and return a user following an email and a password.
        Will automatically upgrade password hash if necessary.
        :param credentials: The user credentials.
        """
        try:
            user = await self.get_by_email(credentials.email)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        return user

    async def update(
        self,
        user_update: schemas.UP,
        user: models.UP,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Update a user.
        Triggers the on_after_update handler on success
        """
        if safe:
            updated_user_data = user_update.create_update_dict()
            updated_user_data = {
                key: value for key, value in updated_user_data.items() if value
            }
        else:
            updated_user_data = user_update.create_update_dict_superuser()
        updated_user = await self._update(user, updated_user_data)
        await self.on_after_update(updated_user, updated_user_data, request)
        return updated_user

    async def create(
        self,
        user_create: schemas.UP,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
