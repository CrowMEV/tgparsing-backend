from typing import Any

import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from services.telegram.member import db_handlers as db_hand
from services.telegram.member import schemas


async def get_members(
    get_data: schemas.GetAllMembers = fa.Depends(),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    data = {
        key: value
        for key, value in get_data.dict().items()
        if value is not None
    }
    members = await db_hand.get_members(session, data)
    return members


async def get_member_by_id(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    member = await db_hand.get_member_by_id(session, id_row)
    if not member:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    return member


async def delete_member(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    await db_hand.delete_member(session, id_row)
    return {"detail": "Запись успешно удалена"}


async def get_chats(
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    chats = await db_hand.get_chats(session)
    return chats


async def get_chat_by_id(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    chat = await db_hand.get_chat_by_id(session, id_row)
    if not chat:
        raise fa.HTTPException(status_code=fa.status.HTTP_404_NOT_FOUND)
    return chat


async def delete_chat(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    await db_hand.delete_chat(session, id_row)
    return {"detail": "Запись успешно удалена"}
