from typing import Any

import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession


from database.db_async import get_async_session
# from bot import parsing as ps

import services.tgmember.db_handlers as db_hand
from services.tgmember.models import ChatMember, ParseredChat


async def get_members_list(
        session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    members = await db_hand.get_members(session)
    return members


async def get_member(
        member_id: int,
        session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    member: ChatMember | None = await db_hand.get_member_by_id(
        session, member_id
    )
    if not member:
        raise fa.HTTPException(status_code=404, detail="Member not found")
    return member


async def delete_member(
        member_id: int,
        session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    await db_hand.delete_member(session, member_id)
    return {'detail': 'success'}


async def get_chats_list(
        session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    chats = await db_hand.get_chats(session)
    return chats


async def get_chat(
        chat_id: int,
        session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    chat: ParseredChat | None = await db_hand.get_chat_by_id(
        session, chat_id
    )
    if not chat:
        raise fa.HTTPException(status_code=404, detail="Chat not found")
    return chat


async def delete_chat(
        chat_id: int,
        session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    await db_hand.delete_chat(session, chat_id)
    return {'detail': 'success'}


async def create_members(
    api_id: int,
    api_hash: str,
    session_string: str,
    parsered_chats: list = fa.Query(),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    for chat in parsered_chats:
        members: dict = await ps.start_parser_by_subscribes(
            chat, api_id, api_hash, session_string
        )
        chat_info: dict = await ps.info_chat(
                    chat, api_id, api_hash, session_string
                )
        check_chat: ParseredChat | None = await db_hand.get_chat_by_id(
                    session, chat_info["chat_id"]
                )
        if check_chat:
            raise fa.HTTPException(
                status_code=400,
                detail="chat has already parsed"
            )
        parsered_chat: ParseredChat = await db_hand.create_chat(
                    session, chat_info
                )
        for member in members:
            check_member: ChatMember | None = await db_hand.get_member_by_id(
                session, member["tguser_id"]
            )
            if check_member:
                member_chats: list = check_member.chats
                updated_chat_list: list = member_chats.append(
                    parsered_chat.name
                )
                patch_data: dict = {"chats": updated_chat_list}
                updated_member: ChatMember = await db_hand.update_member(
                    session, check_member.tguser_id, patch_data
                )
                return updated_member
            member["chats"] = list(parsered_chat.name)
            chat_member: ChatMember = await db_hand.create_member(
                session, member)
        return chat_member
