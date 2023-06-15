from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
import services.telegram.db_handlers as db_handlers
import services.telegram.schemas as tg_schemas


async def get_tgacconts(
        work: tg_schemas.WorkChoice = tg_schemas.WorkChoice.EMPTY,
        blocked: tg_schemas.BlockChoice = tg_schemas.BlockChoice.EMPTY,
        by_geo: tg_schemas.GeoChoice = tg_schemas.GeoChoice.EMPTY,
        session: AsyncSession = Depends(get_async_session)
):
    return await db_handlers.get_tgaccounts(
        session, work, blocked, by_geo
    )


async def create_tgaccount(
        api_id: int,
        api_hash: str,
        session_string: str,
        session: AsyncSession = Depends(get_async_session)
):
    account = await db_handlers.create_tgaccount(
        session, api_id, api_hash, session_string
    )
    return account


async def update_tgaccount(
        id_account: int,
        tg_schema: tg_schemas.TgAccountPatch,
        session: AsyncSession = Depends(get_async_session)
):
    data = {key: value for key, value in tg_schema.dict().items() if value}
    return await db_handlers.update_tgaccount(
        session, id_account, data)


async def delete_tgaccount(
        id_account: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await db_handlers.delete_tgaccount(
        session, id_account
    )
