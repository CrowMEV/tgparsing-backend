from typing import Generic

from fastapi import APIRouter
from fastapi_users import FastAPIUsers, models

from user.routes import get_auth_router
from user.utils.authentication import AppAuthenticationBackend


class FastApiUsers(FastAPIUsers, Generic[models.UP, models.ID]):

    def get_auth_router(
            self, backend: AppAuthenticationBackend,
            requires_verification: bool = False
    ) -> APIRouter:
        return get_auth_router(
            backend,
            self.get_user_manager,
            self.authenticator,
            requires_verification,
        )
