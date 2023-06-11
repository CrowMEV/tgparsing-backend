from typing import Tuple

import fastapi as fa
from fastapi_users import models
from fastapi_users.authentication import Authenticator, Strategy
from fastapi_users.manager import UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType

from services.user.utils.responses import resp, login_resp
from settings import config
from services.user import schemas as user_schemas, views
from services.user.utils.authentication_backend import AppAuthenticationBackend
from services.user.utils.manager import UserManager


def get_auth_router(
    backend: AppAuthenticationBackend,
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    authenticator: Authenticator,
    requires_verification: bool = False,
) -> fa.APIRouter:
    """
    Generate a router with login/logout routes for an authentication backend.
    """
    router = fa.APIRouter()
    get_current_user_token = authenticator.current_user_token(
        active=True, verified=requires_verification
    )

    login_responses: OpenAPIResponseType = {
        **login_resp,
        **backend.transport.get_openapi_login_responses_success(),
    }
    logout_responses: OpenAPIResponseType = {
        **resp,
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/login",
        name=config.USER_LOGIN,
        responses=login_responses,
        response_model=user_schemas.UserRead,
    )
    async def user_login(
        request: fa.Request,
        credentials: user_schemas.UserLogin = fa.Body(),
        user_manager: UserManager = fa.Depends(get_user_manager),
        strategy: Strategy[models.UP, models.ID] = fa.Depends(
            backend.get_strategy
        ),
    ):
        response = await views.user_login(
            request,
            backend,
            credentials,
            user_manager,
            strategy,
            requires_verification,
        )

        return response

    @router.post(
        "/logout",
        name=config.USER_LOGOUT,
        responses=logout_responses,
        response_model=user_schemas.SuccessResponse,
    )
    async def logout(
        user_token: Tuple[models.UP, str] = fa.Depends(get_current_user_token),
        strategy: Strategy[models.UP, models.ID] = fa.Depends(
            backend.get_strategy
        ),
    ):
        user, token = user_token
        response = await backend.logout(strategy, user, token)
        return response

    return router


def get_users_router(
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    authenticator: Authenticator,
    requires_verification: bool = False,
) -> fa.APIRouter:
    """Generate a router with the authentication routes."""
    router = fa.APIRouter()

    get_current_active_user = authenticator.current_user(
        active=True, verified=requires_verification
    )

    @router.patch(
        "/patch",
        name=config.USER_PATCH,
        response_model=user_schemas.UserRead,
        dependencies=[fa.Depends(get_current_active_user)],
        responses=resp,
    )
    async def user_patch(
        request: fa.Request,
        patch_data: user_schemas.UserPatch = fa.Depends(
            user_schemas.UserPatch.as_form
        ),
        current_user: models.UP = fa.Depends(get_current_active_user),
        user_manager: UserManager = fa.Depends(get_user_manager),
    ):
        return await views.user_patch(
            request, patch_data, current_user, user_manager
        )

    return router
