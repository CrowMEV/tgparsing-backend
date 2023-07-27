from typing import Sequence

import sqlalchemy as sa
from services.telegram.member.models import Chat, Member
from sqlalchemy.ext.asyncio import AsyncSession


async def get_members(session: AsyncSession, data: dict) -> Sequence[Member]:
    stmt = sa.select(Member)
    if data:
        stmt = stmt.where(**data)
    result = await session.execute(stmt)
    members = result.scalars().unique().all()
    return members


async def get_member_by_id(
    session: AsyncSession, member_id: int
) -> Member | None:
    stmt = sa.select(Member).where(Member.id == member_id)
    result = await session.execute(stmt)
    member = result.scalars().first()
    return member


async def get_member_by_username(
    session: AsyncSession, username: str
) -> Member | None:
    stmt = sa.select(Member).where(Member.username == username)
    result = await session.execute(stmt)
    member = result.scalars().first()
    return member


async def create_member(session: AsyncSession, data: dict) -> Member:
    member = Member(**data)
    session.add(member)
    await session.commit()
    return member


async def update_member(
    session: AsyncSession, member_id: int, data: dict
) -> Member | None:
    stmt = (
        sa.update(Member)
        .where(Member.id == member_id)
        .values(**data)
        .returning(Member)
    )
    result = await session.execute(stmt)
    await session.commit()
    member = result.scalars().first()
    return member


async def delete_member(session: AsyncSession, member_id: int) -> None:
    stmt = sa.delete(Member).where(Member.id == member_id)
    await session.execute(stmt)
    await session.commit()


async def get_chats(session: AsyncSession) -> Sequence[Chat]:
    stmt = sa.select(Chat)
    result = await session.execute(stmt)
    chats = result.scalars().unique().all()
    return chats


async def get_chat_by_id(session: AsyncSession, chat_id: int) -> Chat | None:
    stmt = sa.select(Chat).where(Chat.id == chat_id)
    result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def get_chat_by_username(
    session: AsyncSession, username: str
) -> Chat | None:
    stmt = sa.select(Chat).where(Chat.username == username)
    result = await session.execute(stmt)
    chat = result.scalars().first()
    return chat


async def create_chat(session: AsyncSession, data: dict) -> Chat:
    chat = Chat(**data)
    session.add(chat)
    await session.commit()
    return chat


async def delete_chat(session: AsyncSession, chat_id: int) -> Chat | None:
    stmt = sa.delete(Chat).where(Chat.id == chat_id).returning(Chat)
    result = await session.execute(stmt)
    await session.commit()
    chat = result.scalars().first()
    return chat
