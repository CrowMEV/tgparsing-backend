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
from services.user.utils import cookie, email, security
from settings import config


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
    request: fa.Request,
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
    token_date = {
        "email": user.email,
        "password": user.hashed_password
    }
    token = security.create_token(token_date)
    url = request.url_for(config.USER_VERIFY).include_query_params(token=token)
    await email.send_mail(user.email, url)
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Пользователь создан успешно"},
    )


async def verify_user(
    token: str,
    session: AsyncSession = fa.Depends(get_async_session),
) -> fa.Response:
    current_user = await email.get_user_from_token(session, token)
    if not current_user or current_user.is_active:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже был подтвержден ранее или токен устарел",
        )
    verify_date = {"is_active": True}
    await db_hand.update_user(session, current_user.id, verify_date)
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Адрес электронной почты успешно подтвержден"},
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


async def delete_non_active_users(
    session: AsyncSession = fa.Depends(get_async_session)
) -> fa.Response:
    await db_hand.delete_non_active_user(session)
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Неактивирированные пользователи успешно удалены"},
    )
