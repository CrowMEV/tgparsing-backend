from typing import Sequence

from fastapi import HTTPException
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from services.telegram.models import TgAccount
import services.telegram.schemas as tg_schemas


async def get_tgaccount(
        session: AsyncSession,
        id_account: int
) -> TgAccount:
    stmt = sa.select(TgAccount).where(TgAccount.id == id_account)
    result = await session.execute(stmt)
    selected_account = result.scalars().first()
    if not selected_account:
        raise HTTPException(status_code=400, detail="error id")
    return selected_account


async def get_tgaccounts(
        session: AsyncSession,
        work: tg_schemas.WorkChoice,
        blocked: tg_schemas.BlockChoice,
        by_geo: tg_schemas.GeoChoice,
) -> Sequence[TgAccount]:
    stmt = sa.select(TgAccount)

    if (work != tg_schemas.WorkChoice.EMPTY or
        blocked != tg_schemas.BlockChoice.EMPTY or
        by_geo != tg_schemas.GeoChoice.EMPTY):
        opt = {}
        if work != tg_schemas.WorkChoice.EMPTY:
            opt['work'] = work
        if blocked != tg_schemas.BlockChoice.EMPTY:
            opt['blocked'] = blocked
        if by_geo != tg_schemas.GeoChoice.EMPTY:
            opt['by_geo'] = by_geo
            
        stmt = stmt.filter_by(**opt)
    
    result = await session.execute(stmt)
    tg_accounts = result.scalars().fetchall()
    return tg_accounts


async def create_tgaccount(
    session: AsyncSession, api_id: int, api_hash: str, session_string: str
) -> TgAccount:
    stmt = insert(TgAccount).values(
        api_id = api_id,
        api_hash = api_hash,
        session_string = session_string
    ).returning(TgAccount)
    result = await session.execute(stmt)
    tg_account = result.scalars().first()
    await session.commit()
    await session.refresh(tg_account)
    return tg_account


async def update_tgaccount(
        session: AsyncSession,
        id_account: int,
        data: dict
) -> TgAccount:
    stmt = (
        sa.update(TgAccount).where(TgAccount.id == id_account).values(**data).returning(TgAccount)
    )
    result = await session.execute(stmt)
    tgaccount = result.scalars().first()
    await session.commit()
    return tgaccount


async def delete_tgaccount(
        session: AsyncSession,
        id_account: int
):
    stmt = sa.select(TgAccount).where(TgAccount.id == id_account)
    result = await session.execute(stmt)
    selected_account = result.scalars().first()
    if not selected_account:
        raise HTTPException(status_code=400, detail="error id")
    await session.delete(selected_account)
    await session.commit()
