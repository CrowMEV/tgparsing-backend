from typing import Generic, Type

from fastapi import APIRouter
from fastapi_users import FastAPIUsers, models, schemas

from services.user.dependencies import get_user_manager
from services.user.models import User
from services.user.routes import get_auth_router, get_users_router
from services.user.utils.authentication_backend import (
    AppAuthenticationBackend,
    auth_backend,
)


class FastApiUsers(FastAPIUsers, Generic[models.UP, models.ID]):
    def get_auth_router(
        self,
        backend: AppAuthenticationBackend,
        requires_verification: bool = False,
    ) -> APIRouter:
        """
        Return an auth router for a given authentication backend.
        """
        return get_auth_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )

    def get_users_router(
        self,
        user_schema: Type[schemas.U],
        requires_verification: bool = False,
        **kwargs
    ) -> APIRouter:
        """
        Return a router with routes to manage users.
        """
        return get_users_router(
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )


fastapi_users = FastApiUsers[User, int](
    get_user_manager,
    [auth_backend],
)
