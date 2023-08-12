from typing import Any

import fastapi as fa
from database.db_async import get_async_session
from services.tariff.db_handlers import update_user_subscribe
from services.user import db_handlers as db_hand
from services.user import helpers
from services.user import schemas as user_schema
from services.user.dependencies import get_current_user
from services.user.models import User
from services.user.utils import cookie, security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse


async def login(
    form: user_schema.UserLogin,
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
    user: user_schema.UserCreate,
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
    update_data: user_schema.UserPatch = fa.Depends(user_schema.UserPatch),
    current_user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await helpers.update_user(
        session=session,
        changing_user=current_user,
        update_data=update_data,
    )
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
    update_data: user_schema.UserPatchByAdmin = fa.Depends(
        user_schema.UserPatchByAdmin
    ),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    db_user = await db_hand.get_current_by_id(session, id_row)
    if not db_user:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    if db_user.role_name.value in ["superuser", "admin"]:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_403_FORBIDDEN,
            detail="Изменение админа или суперпользователя недоступно",
        )
    user = await helpers.update_user(
        session=session,
        changing_user=db_user,
        update_data=update_data,
    )
    return user


async def toggle_tariff_auto_write_off(
    user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    if not user.subscribe:
        raise fa.HTTPException(status_code=400, detail="У вас нет подписки")
    updated_sub = await update_user_subscribe(
        session, user.id, {"auto_debit": not user.subscribe.auto_debit}
    )
    return updated_sub
