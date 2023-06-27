from typing import Any, Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.tgmember.models import ChatMember, ChatsInMember, ParseredChat


async def get_members(session: AsyncSession) -> Sequence[ChatMember]:
    stmt = sa.select(ChatMember)
    result = await session.execute(stmt)
    members = result.scalars().unique().all()
    return members


async def get_member_by_id(
    session: AsyncSession, member_id: int
) -> ChatMember | None:
    stmt = sa.select(ChatMember).where(ChatMember.tguser_id == member_id)
    result = await session.execute(stmt)
    member = result.scalars().first()
    return member


async def get_member_by_username(
    session: AsyncSession, member_username: str
) -> ChatMember | None:
    stmt = sa.select(ChatMember).where(
        ChatMember.username == member_username
    )
    result = await session.execute(stmt)
    member = result.scalars().first()
    return member


async def create_member(session: AsyncSession, data: dict) -> None:
    member = ChatMember(**data)
    session.add(member)
    await session.commit()


async def update_member(
    session: AsyncSession, member_id: int, data: dict
) -> ChatMember | None:
    stmt = (
        sa.update(ChatMember)
        .where(ChatMember.tguser_id == member_id)
        .values(**data)
        .returning(ChatMember)
    )
    result = await session.execute(stmt)
    await session.commit()
    member = result.scalars().first()
    return member


async def delete_member(session: AsyncSession, member_id: int) -> None:
    stmt = sa.delete(ChatMember).where(ChatMember.tguser_id == member_id)
    await session.execute(stmt)
    await session.commit()


async def get_chats(session: AsyncSession) -> Sequence[ParseredChat]:
    stmt = sa.select(ParseredChat)
    result = await session.execute(stmt)
    chats = result.scalars().unique().all()
    return chats


async def get_chat_by_id(
    session: AsyncSession, chat_id: int
) -> ParseredChat | None:
    stmt = sa.select(ParseredChat).where(ParseredChat.chat_id == chat_id)
    result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def get_chat_by_name(
    session: AsyncSession, chat_name: str
) -> ParseredChat | None:
    stmt = sa.select(ParseredChat).where(ParseredChat.name == chat_name)
    result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def create_chat(session: AsyncSession, data: dict) -> None:
    chat = ParseredChat(**data)
    session.add(chat)
    await session.commit()


async def delete_chat(session: AsyncSession, chat_id: int) -> None:
    stmt = sa.delete(ParseredChat).where(ParseredChat.chat_id == chat_id)
    await session.execute(stmt)
    await session.commit()


async def get_chats_in_member(
    session: AsyncSession, member_username: str
) -> Sequence[ChatsInMember]:
    stmt = sa.select(ChatsInMember).where(
        ChatsInMember.chat_member_name == member_username
    )
    result = await session.execute(stmt)
    chats = result.scalars().unique().all()
    return chats


async def get_chat_in_member(
    session: AsyncSession,
    member_username: str,
    chat_name: str
) -> Any:
    stmt = sa.select(ChatsInMember).where(sa.and_(
        ChatsInMember.chat_member_name == member_username,
        ChatsInMember.parsered_chat_name == chat_name
    ))
    result = await session.execute(stmt)
    chat_in_member = result.scalars().first()
    return chat_in_member


async def create_chat_in_member(
    session: AsyncSession, data: dict
) -> None:
    chat_in_member = ChatsInMember(**data)
    session.add(chat_in_member)
    await session.commit()
