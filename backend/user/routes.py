from typing import Tuple

from fastapi import (
    APIRouter, Depends, HTTPException, Request, status, Body
)

from fastapi_users import models
from fastapi_users.authentication import Authenticator, Strategy
from fastapi_users.manager import UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel

from user.schemas import UserLogin, UserRead, UserLogout
from user.utils.authentication import AppAuthenticationBackend
from user.utils.manager import UserManager

from user import views


def get_auth_router(
    backend: AppAuthenticationBackend,
    get_user_manager: UserManagerDependency[models.UP, models.ID],
    authenticator: Authenticator,
    requires_verification: bool = False,
) -> APIRouter:
    """
    Generate a router with login/logout routes for an authentication backend.
    """
    router = APIRouter()
    get_current_user_token = authenticator.current_user_token(
        active=True, verified=requires_verification
    )

    login_responses: OpenAPIResponseType = {
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.LOGIN_BAD_CREDENTIALS: {
                            "summary": "Bad credentials or "
                                       "the user is inactive.",
                            "value": {
                                "detail": ErrorCode.LOGIN_BAD_CREDENTIALS
                            },
                        },
                        ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                            "summary": "The user is not verified.",
                            "value": {
                                "detail": ErrorCode.LOGIN_USER_NOT_VERIFIED
                            },
                        },
                    }
                }
            },
        },
        **backend.transport.get_openapi_login_responses_success(),
    }

    @router.post(
        "/login",
        name="User login",
        responses=login_responses,
        response_model=UserRead
    )
    async def login(
        request: Request,
        credentials: UserLogin = Body(),
        user_manager: UserManager = Depends(get_user_manager),
        strategy: Strategy[models.UP, models.ID] = Depends(
            backend.get_strategy
        ),
    ):
        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if requires_verification and not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        response = await backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    logout_responses: OpenAPIResponseType = {
        **{
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/logout", name="User logout",
        responses=logout_responses,
        response_model=UserLogout
    )
    async def logout(
        user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
        strategy: Strategy[models.UP, models.ID] = Depends(
            backend.get_strategy
        )
    ):
        user, token = user_token
        response = await backend.logout(strategy, user, token)
        return response


    return router


router = APIRouter(prefix="/roles", tags=["Role"])


router.add_api_route(
    path="/all", endpoint=views.get_roles, methods=["GET"],
)
router.add_api_route(
    path="/", endpoint=views.get_role, methods=["GET"],
)
router.add_api_route(
    path="/", endpoint=views.add_role, methods=["POST"],
)
router.add_api_route(
    path="/", endpoint=views.update_role, methods=["PATCH"],
)
router.add_api_route(
    path="/", endpoint=views.delete_role, methods=["DELETE"],
)
