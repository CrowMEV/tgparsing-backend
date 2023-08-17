from typing import Any

import fastapi as fa
from database.db_async import get_async_session
from services.role.schemas import RoleNameChoice
from services.tariff.db_handlers import update_user_subscribe
from services.user import db_handlers as user_hand
from services.user import helpers
from services.user import schemas as user_schema
from services.user.dependencies import get_current_user
from services.user.helpers import check_data_exists
from services.user.models import User
from services.user.utils import cookie, security
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse


async def login(
    form: user_schema.UserLogin,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    users = await user_hand.get_users_by_filter(session, {"email": form.email})
    if len(users) < 1 or not security.validate_password(
        form.password, users[0].hashed_password
    ):
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Неверный логин или пароль",
        )
    form.password = users[0].hashed_password
    response = security.login(users[0], form.model_dump())
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
    exist_user = await user_hand.get_users_by_filter(
        session, {"email": user.email}
    )
    if exist_user:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с такой почтой уже существует",
        )
    user.hashed_password = security.get_hash_password(user.hashed_password)
    await user_hand.add_user(session, user.model_dump())
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Пользователь создан успешно"},
    )


async def get_user_by_id(
    id_row: int,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    user = await user_hand.get_current_by_id(session, id_row)
    if not user:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    return user


async def get_users(
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    users = await user_hand.get_users(session)
    return users


async def patch_current_user(
    update_data: user_schema.UserPatch = fa.Depends(),
    current_user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    await check_data_exists(session, "phone_number", update_data.phone_number)
    await check_data_exists(session, "email", update_data.email)
    user = await helpers.update_user(
        session=session,
        changing_user=current_user,
        update_data=update_data.__dict__,
    )
    return user


async def patch_user_by_admin(
    id_row: int,
    update_data: user_schema.UserPatchByAdmin = fa.Depends(),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    db_user = await user_hand.get_current_by_id(session, id_row)
    if not db_user:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Пользователь не найден",
        )
    if db_user.role_name.value == user_schema.RoleNameChoice.SUPERUSER.value:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_403_FORBIDDEN,
            detail="Изменение суперпользователя недоступно",
        )
    await check_data_exists(session, "phone_number", update_data.phone_number)
    await check_data_exists(session, "email", update_data.email)
    user = await helpers.update_user(
        session=session,
        changing_user=db_user,
        update_data=update_data.__dict__,
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


async def set_ban_for_user(
    ban_data: user_schema.UserBanSchema,
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
) -> Any:
    if current_user.id == ban_data.user_id:
        raise fa.HTTPException(
            status_code=400, detail="Нельзя забанить самого себя"
        )
    db_user = await user_hand.get_current_by_id(session, ban_data.user_id)
    if not db_user:
        raise fa.HTTPException(status_code=400, detail="Юзер не найден")
    if ban_data.is_banned and db_user.role_name == RoleNameChoice.SUPERUSER:
        raise fa.HTTPException(
            status_code=400,
            detail="Администратор не может заблокировать суперпользователя",
        )
    update_data = ban_data.model_dump()
    user_id = update_data.pop("user_id")
    if ban_data.is_banned:
        update_data["role_name"] = RoleNameChoice.USER
    banned_user = await user_hand.update_user(session, user_id, update_data)
    return banned_user
