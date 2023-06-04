import os

import aiofiles
import fastapi as fa
from fastapi_users import models
from fastapi_users.authentication import Strategy
from fastapi_users.router import ErrorCode

from services.user.schemas import UserPatch, UserLogin
from services.user.utils.authentication import AppAuthenticationBackend
from services.user.utils.manager import UserManager
from settings import config


async def user_login(
        request: fa.Request,
        backend: AppAuthenticationBackend,
        credentials: UserLogin,
        user_manager: UserManager,
        strategy: Strategy[models.UP, models.ID],
        requires_verification: bool = False,
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


async def user_patch(
        request: fa.Request,
        patch_data: UserPatch,
        current_user: models.UP,
        user_manager: UserManager
):
    if patch_data.avatar_url:
        folder_path = os.path.join(
            config.BASE_DIR, config.STATIC_DIR, config.AVATARS_FOLDER
        )
        file_name = (
            f"{current_user.email}" f".{patch_data.avatar_url.filename.split('.')[-1]}"
        )
        file_url = os.path.join(folder_path, file_name)
        async with aiofiles.open(file_url, "wb") as p_f:
            await p_f.write(patch_data.avatar_url.file.read())
        patch_data.avatar_url = file_url

    user = await user_manager.update(
        patch_data, current_user, safe=True, request=request
    )
    return user.__dict__
