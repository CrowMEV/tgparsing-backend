import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from services.tgmember.models import ChatMember, ParseredChat


async def get_members(session: AsyncSession) -> Sequence[ChatMember]:
    stmt = sa.select(ChatMember)
    result = await session.execute(stmt)
    members = result.scalars().fetchall()
    return members


async def get_member_by_id(session: AsyncSession,
                           member_id: int) -> ChatMember | None:
    stmt = sa.select(ChatMember).where(ChatMember.tguser_id == member_id)
    result = await session.execute(stmt)
    member = result.scalars().first()
    return member


async def create_member(session: AsyncSession, data: dict) -> ChatMember:
    stmt = (
        sa.insert(ChatMember)
        .values(**data)
        .returning(ChatMember)
    )
    result = await session.execute(stmt)
    member: ChatMember = result.scalars().first()
    await session.commit()
    return member


async def update_member(session: AsyncSession,
                        member_id: int, data: dict) -> ChatMember:
    stmt = (
        sa.update(ChatMember)
        .values(**data)
        .returning(ChatMember)
        .where(ChatMember.tguser_id == member_id)
    )
    result = await session.execute(stmt)
    member = result.scalars().first()
    await session.commit()
    return member


async def delete_member(session: AsyncSession, member_id: int) -> None:
    stmt = (
        sa.delete(ChatMember).where(ChatMember.tguser_id == member_id)
    )
    await session.execute(stmt)
    await session.commit()


async def get_chats(session: AsyncSession) -> Sequence[ParseredChat]:
    stmt = sa.select(ChatMember)
    result = await session.execute(stmt)
    chats = result.scalars().fetchall()
    return chats


async def get_chat_by_id(session: AsyncSession,
                         chat_id: int) -> ParseredChat | None:
    stmt = sa.select(ParseredChat).where(ParseredChat.chat_id == chat_id)
    result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def create_chat(session: AsyncSession, data: dict) -> ParseredChat:
    stmt = (
        sa.insert(ParseredChat)
        .values(**data)
        .returning(ParseredChat)
    )
    result = await session.execute(stmt)
    chat: ParseredChat = result.scalars().first()
    await session.commit()
    return chat


async def delete_chat(session: AsyncSession, chat_id: int) -> None:
    stmt = (
        sa.delete(ParseredChat).where(ParseredChat.chat_id == chat_id)
    )
    await session.execute(stmt)
    await session.commit()
