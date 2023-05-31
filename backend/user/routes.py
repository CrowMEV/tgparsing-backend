import os.path
from typing import Tuple, Optional

import aiofiles
import fastapi as fa
from fastapi.responses import JSONResponse
from fastapi_users import models, exceptions
from fastapi_users.authentication import Authenticator, Strategy
from fastapi_users.manager import UserManagerDependency
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel

from settings import config
from user.schemas import UserLogin, UserRead, SuccessResponse, UserPatch
from user.utils.authentication import AppAuthenticationBackend
from user.utils.manager import UserManager


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
        fa.status.HTTP_400_BAD_REQUEST: {
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
        request: fa.Request,
        credentials: UserLogin = fa.Body(),
        user_manager: UserManager = fa.Depends(get_user_manager),
        strategy: Strategy[models.UP, models.ID] = fa.Depends(
            backend.get_strategy
        ),
    ):
        user = await user_manager.authenticate(credentials)

        if user is None or not user.is_active:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        if requires_verification and not user.is_verified:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
            )
        response = await backend.login(strategy, user)
        await user_manager.on_after_login(user, request, response)
        return response

    logout_responses: OpenAPIResponseType = {
        **{
            fa.status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user."
            }
        },
        **backend.transport.get_openapi_logout_responses_success(),
    }

    @router.post(
        "/logout", name="User logout",
        responses=logout_responses,
        response_model=SuccessResponse
    )
    async def logout(
        user_token: Tuple[models.UP, str] = fa.Depends(get_current_user_token),
        strategy: Strategy[models.UP, models.ID] = fa.Depends(
            backend.get_strategy
        )
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
        # response_model=UserRead,
        dependencies=[fa.Depends(get_current_active_user)],
        name="Patch current user",
        responses={
            fa.status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            },
        },
    )
    async def user_update(
        request: fa.Request,
        firstname: Optional[str] = fa.Form(
            None, min_length=1, regex='^[a-zA-Zа-яА-яёЁ]+$'
        ),
        lastname: Optional[str] = fa.Form(
            None, min_length=1, regex='^[a-zA-Zа-яА-яёЁ]+$'
        ),
        password: Optional[str] = fa.Form(
            None,
            min_length=8,
            regex=r'([0-9]+\S*[A-Z]+|\S[A-Z]+\S*[0-9]+)\S*'
                  r'[!\"`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+'
        ),
        picture: Optional[fa.UploadFile] = fa.Form(None),
        current_user: models.UP = fa.Depends(get_current_active_user),
        user_manager: UserManager = fa.Depends(get_user_manager),
    ):
        data = {
            "firstname": firstname,
            "lastname": lastname,
            "password": password,
        }
        patch_model = UserPatch(
            **data
        )
        try:
            user_data = await user_manager.update(
                patch_model, current_user, safe=True, request=request
            )
            if picture:
                new_name = f"{current_user.email}.{picture.filename.split('.')[-1]}"
                folder_path = os.path.join(
                    config.BASE_DIR, config.STATIC_DIR, config.AVATARS_FOLDER
                )
                async with aiofiles.open(
                    os.path.join(folder_path, new_name), 'wb'
                ) as p_f:
                    await p_f.write(picture.file.read())
            else:
                new_name = config.BASE_AVATAR_NAME
            return JSONResponse(
                status_code=fa.status.HTTP_200_OK,
                content={'filename': new_name},
            )
        except exceptions.InvalidPasswordException as e:
            raise fa.HTTPException(
                status_code=fa.status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                    "reason": e.reason,
                },
            )
        except exceptions.UserAlreadyExists:
            raise fa.HTTPException(
                fa.status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
            )

    return router
