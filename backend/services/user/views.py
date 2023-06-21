import json
import os
from typing import Any

import aiofiles
import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from database.db_async import get_async_session
from services.user import db_handlers as db_hand
from services.user import schemas as u_schema
from services.user.dependencies import get_current_user
from services.user.models import User
from services.user.utils import security, cookie
from settings import config


async def login(
    form: u_schema.UserLogin,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await db_hand.get_user_by_email(session, form.email)
    if not user or \
            not security.validate_password(
                form.password, user.hashed_password
            ):
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Invalid authentication credentials",
        )
    form.password = user.hashed_password
    access_token = security.create_token(data=form.dict())
    user_json = u_schema.UserRead.from_orm(user).json()
    user_data = json.loads(user_json)
    response = JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content=user_data,
    )
    cookie.set_cookie(response, access_token)
    return response


async def logout() -> fa.Response:
    response = JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Success"}
    )
    cookie.drop_cookie(response)
    return response


async def create_user(
    user: u_schema.UserCreate,
    session: AsyncSession = fa.Depends(get_async_session),
) -> fa.Response:
    exist_user = await db_hand.get_user_by_email(session, user.email)
    if exist_user:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="User with such email already exists"
        )
    user.hashed_password = security.get_hash_password(user.hashed_password)
    await db_hand.add_user(session, user.dict())

    return fa.Response(
        status_code=fa.status.HTTP_201_CREATED,
        content="User has been created successfully"
    )


async def get_user_by_id(
    id: int,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await db_hand.get_current_by_id(session, id)
    if not user:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    return user


async def get_users(
    session: AsyncSession = fa.Depends(get_async_session),
    token: str = fa.Depends(cookie.get_cookie_key),
) -> Any:
    users = await db_hand.get_users(session)
    return users


async def patch_current_user(
    data: u_schema.UserPatch = fa.Depends(u_schema.UserPatch.as_form),
    current_user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    if data.avatar_url:
        folder_path = os.path.join(config.STATIC_DIR, config.AVATARS_FOLDER)
        file_name = (
            f"{current_user.email}"
            f".{data.avatar_url.filename.split('.')[-1]}"
        )
        file_url = os.path.join(folder_path, file_name)
        async with aiofiles.open(file_url, "wb") as p_f:
            await p_f.write(data.avatar_url.file.read())
        data.avatar_url = file_url

    user = await db_hand.update_user(session, current_user.id, data)
    return user.__dict__
