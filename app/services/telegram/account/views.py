from typing import Any

import fastapi as fa
import services.telegram.account.db_handlers as db_hand
import services.telegram.account.schemas as tg_schemas
from database.db_async import get_async_session
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def get_accounts(
    get_data: tg_schemas.TgAccountGetAll = fa.Depends(),
    session: AsyncSession = fa.Depends(get_async_session),
):
    data = {
        key: value
        for key, value in get_data.dict().items()
        if value is not None
    }
    accounts = await db_hand.get_tgaccounts(session, data)
    return accounts


async def get_tgaccount_by_id(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    account = await db_hand.get_tgaccount_by_id(session, id_row)
    if not account:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail="Записи с таким id не существует",
        )
    return account


async def create_tgaccount(
    data: tg_schemas.TgAccountCreate,
    session: AsyncSession = fa.Depends(get_async_session),
) -> fa.Response:
    account = await db_hand.get_tgaccount_by_api_id(session, data.api_id)
    if account:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Аккаунт с таким api id уже существует",
        )
    await db_hand.create_tgaccount(session, data.dict())
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Успешно"},
    )


async def update_tgaccount(
    id_row: int,
    update_data: tg_schemas.TgAccountUpdate = fa.Depends(),
    session: AsyncSession = fa.Depends(get_async_session),
):
    data = {
        key: value
        for key, value in update_data.dict().items()
        if value is not None
    }
    if not data:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для изменения",
        )
    account = await db_hand.update_tgaccount(session, id_row, data)
    return account


async def delete_tgaccount(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> fa.Response:
    account = await db_hand.delete_tgaccount(session, id_row)
    if not account:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Такой записи не существует",
        )
    return JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content={"detail": "Запись удалена успешно"},
    )
