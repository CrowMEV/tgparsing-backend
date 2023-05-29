import sqlalchemy as sa
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from database.models.role_model import Role
from role.schemas import RoleCreate, RoleUpdate

router = APIRouter(prefix="/roles", tags=["Role"])


@router.get("")
async def get_roles(
    session: AsyncSession = Depends(get_async_session),
):
    try:
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
    except Exception as e:
        print(e)
        return {"detail": "Error", "data": None}


@router.get("/{role_id}")
async def get_role(
    role_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = sa.select(Role.name, Role.permissions).filter(
            Role.id == role_id
        )
        result = await session.execute(query)
        name, permissions = result.fetchone()
        data = {
            "name": name,
            "permissions": permissions,
        }
        return {
            "detail": "Success",
            "data": data,
        }
    except Exception as e:
        print(e)
        return {"detail": "Error", "data": None}


@router.post("")
async def add_role(
    new_role: RoleCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        data = new_role.dict()
        stmt = sa.insert(Role).values(data)
        await session.execute(stmt)
        await session.commit()
        return {
            "detail": "Success",
            "data": data,
        }
    except Exception as e:
        print(e)
        return {"detail": "Error", "data": None}


@router.post("/update/{role_id}")
async def update_role(
    role_id: int,
    new_role: RoleUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        data = new_role.dict()
        stmt = sa.update(Role).where(Role.id == role_id).values(data)
        await session.execute(stmt)
        await session.commit()
        return {
            "detail": "Success",
            "data": data,
        }
    except Exception as e:
        print(e)
        return {"detail": "Error", "data": None}


@router.post("/delete/{role_id}")
async def delete_role(
    role_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        stmt = sa.delete(Role).where(Role.id == role_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "detail": "Success",
            "data": None,
        }
    except Exception as e:
        print(e)
        return {"detail": "Error", "data": None}
