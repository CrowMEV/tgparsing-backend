import sqlalchemy as sa
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from database.models.role_model import Role

async def get_role_id(
        name: str,
        session: AsyncSession = Depends(get_async_session),
):
    query = sa.select(Role.id).filter(Role.name == name)
    result = await session.execute(query)
    return result.all()
