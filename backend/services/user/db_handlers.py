from typing import Sequence

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from services.user.models import User


async def get_users(session: AsyncSession) -> Sequence[User]:
    stmt = sa.select(User)
    result = await session.execute(stmt)
    users = result.scalars().fetchall()
    return users


async def get_current_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = sa.select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    users = result.scalars().first()
    return users
