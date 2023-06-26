from typing import Any

import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession

import services.tgmember.db_handlers as db_hand
from database.db_async import get_async_session
from services.tgmember.utils import parsing_invoke as p_inv


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
    return {"detail": "Пользователь успешно удален"}


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
    return {"detail": "Чат успешно удален"}


async def create_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    parsered_chats: list = fa.Query(),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    for chat in parsered_chats:
        members = p_inv.start_parser_by_subscribes(
            chat, api_id, api_hash, session_string
        )
        chat_info = p_inv.info_chat(chat, api_id, api_hash, session_string)
        check_chat = await db_hand.get_chat_by_id(
            session, chat_info["chat_id"]
        )
        if check_chat:
            raise fa.HTTPException(status_code=fa.status.HTTP_400_BAD_REQUEST)
        await db_hand.create_chat(session, chat_info)
        for member in members:
            check_member = await db_hand.get_member_by_id(
                session, member["tguser_id"]
            )
            if check_member:
                member_chats = check_member.chats
                member_chats.append(chat)
                patch_data = {"chats": member_chats}
                await db_hand.update_member(
                    session, check_member.tguser_id, patch_data
                )
            member["chats"] = list(chat)
            await db_hand.create_member(session, member)
    return {"detail": "Парсинг чатов выполнен успешно"}
