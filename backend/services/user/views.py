import os
from typing import Any

import aiofiles
import fastapi as fa
from fastapi_users import models
from fastapi_users.authentication import Strategy
from fastapi_users.router import ErrorCode
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from services.user import db_handlers as db_hand
from services.user.schemas import UserPatch, UserLogin
from services.user.utils.authentication_backend import AppAuthenticationBackend
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
    user_manager: UserManager,
):
    if patch_data.avatar_url:
        folder_path = os.path.join(
            config.BASE_DIR, config.STATIC_DIR, config.AVATARS_FOLDER
        )
        file_name = (
            f"{current_user.email}"
            f".{patch_data.avatar_url.filename.split('.')[-1]}"
        )
        file_url = os.path.join(folder_path, file_name)
        async with aiofiles.open(file_url, "wb") as p_f:
            await p_f.write(patch_data.avatar_url.file.read())
        patch_data.avatar_url = file_url

    user = await user_manager.update(
        patch_data, current_user, safe=True, request=request
    )
    return user.__dict__


async def get_user(
    id: int,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await db_hand.get_current_by_id(session, id)
    if not user:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    return user


async def get_users(
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    users = await db_hand.get_users(session)
    return users
