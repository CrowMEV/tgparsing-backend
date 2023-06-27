from typing import Any

import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

import services.tgmember.db_handlers as db_hand
import services.tgmember.schemas as tgm_schemas
from database.db_async import get_async_session


async def get_members(
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    members = await db_hand.get_members(session)
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


async def create_member(
    member: tgm_schemas.ChatMember,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    exist_member = await db_hand.get_member_by_username(
        session, member.username
    )
    if exist_member:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Участник уже записан"
        )
    await db_hand.create_member(session, member.dict())
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Запись успешно добавлена"},
    )


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


async def create_chat(
    chat: tgm_schemas.ParseredChat,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    exist_chat = await db_hand.get_chat_by_name(session, chat.name)
    if exist_chat:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Чат уже есть"
        )
    await db_hand.create_chat(session, chat.dict())
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Запись успешно добавлена"},
    )


async def get_chats_in_member(
    member_username: str,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    exist_member = await db_hand.get_member_by_username(
        session,  member_username,
    )
    if not exist_member:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail="Участник не найден"
        )
    chats_in_member = await db_hand.get_chats_in_member(
        session, member_username
    )
    return chats_in_member


async def create_chat_in_member(
    chat_in_member: tgm_schemas.ChatInMember,
    session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    exist_member = await db_hand.get_member_by_username(
        session, chat_in_member.chat_member_name,
    )
    exist_chat = await db_hand.get_chat_by_name(
        session, chat_in_member.parsered_chat_name
    )
    exist_chat_in_member = await db_hand.get_chat_in_member(
        session,
        chat_in_member.chat_member_name,
        chat_in_member.parsered_chat_name
    )
    if not exist_member:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail="Участник не найден"
        )
    if not exist_chat:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail="Чат не найден"
        )
    if exist_chat_in_member:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Чат уже есть у участника"
        )
    await db_hand.create_chat_in_member(
        session, chat_in_member.dict()
    )
    return JSONResponse(
        status_code=fa.status.HTTP_201_CREATED,
        content={"detail": "Чат успешно добавлен к участнику"},
    )
