from typing import Any

import services.role.db_handlers as db_hand
import services.role.schemas as role_schemas
from database.db_async import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


async def get_roles(
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    roles = await db_hand.get_roles(session)
    return roles


async def get_role(
    role_schema: role_schemas.RoleGet,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    role = await db_hand.get_role(session, role_schema.name.name)
    return role


async def patch_role(
    role_schema: role_schemas.RolePatch,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    data = {
        key: value
        for key, value in role_schema.dict().items()
        if value is not None
    }
    role = await db_hand.change_role(session, data)
    return role
