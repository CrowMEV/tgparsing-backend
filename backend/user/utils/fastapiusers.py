from typing import Generic, Type

from fastapi import APIRouter
from fastapi_users import FastAPIUsers, models, schemas

from user.routes import get_auth_router, get_users_router
from user.utils.authentication import AppAuthenticationBackend



class FastApiUsers(FastAPIUsers, Generic[models.UP, models.ID]):

    def get_auth_router(
            self, backend: AppAuthenticationBackend,
            requires_verification: bool = False
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
