import os
from typing import Any

import aiofiles
import fastapi as fa
from database.db_async import get_async_session
from services.user import db_handlers as db_hand
from services.user import schemas as u_schema
from services.user.dependencies import get_current_user
from services.user.models import User
from services.user.utils import cookie, security
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse


async def login(
    form: u_schema.UserLogin,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await db_hand.get_user_by_email(session, form.email)
    if not user or not security.validate_password(
        form.password, user.hashed_password
    ):
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Неверный логин или пароль",
        )
    form.password = user.hashed_password
    response = security.login(user, form.dict())
    return response


async def logout() -> fa.Response:
    response = JSONResponse(
        status_code=fa.status.HTTP_200_OK, content={"detail": "Успешно"}
    )
    cookie.drop_cookie(response)
    return response


async def refresh_user(
    user: User = fa.Depends(get_current_user),
) -> Any:
    data = {"email": user.email, "password": user.hashed_password}
    response = security.login(user, data)
    return response


async def create_user(
    user: u_schema.UserCreate,
    session: AsyncSession = fa.Depends(get_async_session),
) -> fa.Response:
    exist_user = await db_hand.get_user_by_email(session, user.email)
    if exist_user:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с такой почтой уже существует",
        )
    user.hashed_password = security.get_hash_password(user.hashed_password)
    await db_hand.add_user(session, user.dict())
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Пользователь создан успешно"},
    )


async def get_user_by_id(
    id_row: int,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await db_hand.get_current_by_id(session, id_row)
    if not user:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    return user


async def get_users(
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    users = await db_hand.get_users(session)
    return users


async def patch_current_user(
    update_data: u_schema.UserPatch = fa.Depends(u_schema.UserPatch.as_form),
    current_user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    data = update_data.dict()
    if data.get("avatar_url"):
        folder_path = os.path.join(config.STATIC_DIR, config.AVATARS_FOLDER)
        file_name = (
            f"{current_user.email}"
            f".{data['avatar_url'].filename.split('.')[-1]}"
        )
        file_url = os.path.join(folder_path, file_name)
        async with aiofiles.open(file_url, "wb") as p_f:
            await p_f.write(data["avatar_url"].file.read())
        data["avatar_url"] = file_url
    if data.get("hashed_password"):
        data["hashed_password"] = security.get_hash_password(
            data["hashed_password"]
        )
    data = {key: value for key, value in data.items() if value is not None}
    if not data:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для изменений",
        )
    user = await db_hand.update_user(session, current_user.id, data)
    return user


async def check_password(
    password: str = fa.Body(..., embed=True),
    user=fa.Depends(get_current_user),
) -> JSONResponse:
    if not security.validate_password(password, user.hashed_password):
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Неверный пароль",
        )
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Успешно"},
    )


async def patch_user_by_admin(
    id_row: int,
    update_data: u_schema.UserPatch = fa.Depends(u_schema.UserPatch.as_form),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await db_hand.get_current_by_id(session, id_row)
    if not user:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    data = update_data.dict()
    if data.get("avatar_url"):
        folder_path = os.path.join(config.STATIC_DIR, config.AVATARS_FOLDER)
        file_name = (
            f"{user.email}" f".{data['avatar_url'].filename.split('.')[-1]}"
        )
        file_url = os.path.join(folder_path, file_name)
        async with aiofiles.open(file_url, "wb") as p_f:
            await p_f.write(data["avatar_url"].file.read())
        data["avatar_url"] = file_url
    if data.get("hashed_password"):
        data["hashed_password"] = security.get_hash_password(
            data["hashed_password"]
        )
    data = {key: value for key, value in data.items() if value is not None}
    if not data:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для изменений",
        )
    changed_user = await db_hand.update_user(session, id_row, data)
    return changed_user
