import sqlalchemy as sa
from fastapi import Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from database.models.user_model import Role
from user.schemas import RoleCreate, RoleUpdate
from starlette import status
from fastapi.responses import JSONResponse


async def get_roles(
    session: AsyncSession = Depends(get_async_session),
):
    query = sa.select(Role.name, Role.permissions)
    result = await session.execute(query)
    data = [
        {"name": name, "permissions": permissions}
        for name, permissions in result.all()
    ]
    return {
            "detail": "Success",
            "data": data,
    }


async def get_role(
    role_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_async_session),
):
    query = sa.select(Role.name, Role.permissions).filter(
        Role.id == role_id
    )
    result = await session.execute(query)
    result = result.fetchone()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with id={role_id} does not exist"
        )
    name, permissions = result
    data = {
        "name": name,
        "permissions": permissions,
    }
    return {
        "detail": "Success",
        "data": data,
    }


async def add_role(
    new_role: RoleCreate,
    session: AsyncSession = Depends(get_async_session),
):
    data = new_role.dict()
    existing_role = await session.execute(
        sa.select(Role).filter(Role.name == data["name"])
    )
    if existing_role.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with name \'{data['name']}\' already exists"
        )
    stmt = sa.insert(Role).values(data)

    await session.execute(stmt)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Success"},
    )


async def update_role(
    new_role: RoleUpdate,
    role_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_async_session),
):
    data = new_role.dict()
    stmt = sa.update(Role).where(Role.id == role_id).values(data)
    await session.execute(stmt)
    await session.commit()
    return {
        "detail": "Success",
        "msg": "Role successfully updated",
    }


async def delete_role(
    role_id: int = Query(..., ge=1),
    session: AsyncSession = Depends(get_async_session),
):
    query = sa.select(Role).filter(
        Role.id == role_id
    )
    role = await session.execute(query)
    role = role.fetchone()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with id={role_id} does not exist"
        )
    await session.delete(role[0])
    await session.commit()
    return {
        "detail": "Success",
        "msg": "Role successfully deleted",
    }

