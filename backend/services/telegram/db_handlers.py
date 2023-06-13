from typing import Sequence

from fastapi import HTTPException
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from services.telegram.models import TgAccount
import services.telegram.schemas as tg_schemas


async def get_tgaccounts(
        session: AsyncSession,
        work: tg_schemas.WorkChoice = tg_schemas.WorkChoice.EMPTY,
        blocked: tg_schemas.BlockChoice = tg_schemas.BlockChoice.EMPTY,
        by_geo: tg_schemas.GeoChoice = tg_schemas.GeoChoice.EMPTY,
) -> Sequence[TgAccount]:
    stmt = sa.select(TgAccount)

    opt = {}
    if work != tg_schemas.WorkChoice.EMPTY:
        opt['work'] = work
    if blocked != tg_schemas.BlockChoice.EMPTY:
        opt['blocked'] = blocked
    if by_geo != tg_schemas.GeoChoice.EMPTY:
        opt['by_geo'] = by_geo
        
    if opt:
        stmt = stmt.filter_by(**opt)
    
    result = await session.execute(stmt)
    tg_accounts = result.scalars().fetchall()
    return tg_accounts


async def create_tgaccount(
    session: Session, api_id: int, api_hash: str, session_string: str
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
        work: tg_schemas.WorkChoice = tg_schemas.WorkChoice.EMPTY,
        blocked: tg_schemas.BlockChoice = tg_schemas.BlockChoice.EMPTY,
        by_geo: tg_schemas.GeoChoice = tg_schemas.GeoChoice.EMPTY,
        session_string: str = ''
) -> TgAccount:
    stmt = sa.select(TgAccount).where(TgAccount.id == id_account)
    result = await session.execute(stmt)
    selected_account = result.scalars().first()

    if not selected_account:
        raise HTTPException(status_code=400, detail="error id")

    if work != tg_schemas.WorkChoice.EMPTY:
        selected_account.work = work
    if blocked != tg_schemas.BlockChoice.EMPTY:
        selected_account.blocked = blocked
    if by_geo != tg_schemas.GeoChoice.EMPTY:
        selected_account.by_geo = by_geo
    if session_string:
        selected_account.session_string = session_string
    
    await session.commit()
    await session.refresh(selected_account)
    return selected_account


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
