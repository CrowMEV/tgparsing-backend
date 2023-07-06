from typing import Any, Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.telegram.member.models import Chat, Member


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
#
#
# async def update_member(
#     session: AsyncSession, member_id: int, data: dict
# ) -> Member | None:
#     stmt = (
#         sa.update(Member)
#         .where(Member.tguser_id == member_id)
#         .values(**data)
#         .returning(Member)
#     )
#     result = await session.execute(stmt)
#     await session.commit()
#     member = result.scalars().first()
#     return member
#
#
# async def delete_member(session: AsyncSession, member_id: int) -> None:
#     stmt = sa.delete(Member).where(Member.tguser_id == member_id)
#     await session.execute(stmt)
#     await session.commit()


async def get_chats(session: AsyncSession) -> Sequence[Chat]:
    stmt = sa.select(Chat)
    result = await session.execute(stmt)
    chats = result.scalars().unique().all()
    return chats


async def get_chat_by_id(
    session: AsyncSession, chat_id: int
) -> Chat | None:
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


async def delete_chat(session: AsyncSession, chat_id: int) -> None:
    stmt = sa.delete(Chat).where(Chat.id == chat_id).returning(Chat)
    result = await session.execute(stmt)
    await session.commit()
    chat = result.scalars().first()
    return chat
#
#
# async def get_chats_in_member(
#     session: AsyncSession, member_username: str
# ) -> Sequence[chats_members]:
#     stmt = sa.select(chats_members).where(
#         chats_members.chat_member_name == member_username
#     )
#     result = await session.execute(stmt)
#     chats = result.scalars().unique().all()
#     return chats
#
#
# async def get_chat_in_member(
#     session: AsyncSession,
#     member_username: str,
#     chat_name: str
# ) -> Any:
#     stmt = sa.select(chats_members).where(sa.and_(
#         chats_members.chat_member_name == member_username,
#         chats_members.parsered_chat_name == chat_name
#     ))
#     result = await session.execute(stmt)
#     chat_in_member = result.scalars().first()
#     return chat_in_member
#
#
# async def create_chat_in_member(
#     session: AsyncSession, data: dict
# ) -> None:
#     chat_in_member = chats_members(**data)
#     session.add(chat_in_member)
#     await session.commit()
