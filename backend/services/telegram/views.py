from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
import services.telegram.db_handlers as db_handlers


async def get_all_tgacconts(
        session: AsyncSession = Depends(get_async_session)
):
    tg_accounts = await db_handlers.get_all_tgaccounts(session)
    return tg_accounts


async def get_tgacconts(
        session: AsyncSession = Depends(get_async_session),
        in_work: Optional[bool] = False,
        is_blocked: Optional[bool] = False,
        by_geo: Optional[bool] = False
):
    return await db_handlers.get_tgaccounts(
        session, in_work, is_blocked, by_geo
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


async def update_inwork_tgaccount(
        id_account: int,
        in_work: bool,
        session: AsyncSession = Depends(get_async_session)
):
    return await db_handlers.update_inwork_tgaccount(
        session, id_account, in_work
    )


async def update_isblocked_tgaccount(
        id_account: int,
        is_blocked: bool,
        session: AsyncSession = Depends(get_async_session)
):
    return await db_handlers.update_isblocked_tgaccount(
        session, id_account, is_blocked
    )

async def update_bygeo_tgaccount(
        id_account: int,
        by_geo: bool,
        session: AsyncSession = Depends(get_async_session)
):
    return await db_handlers.update_bygeo_tgaccount(
        session, id_account, by_geo
    )


async def update_sessionstring_tgaccount(
        id_account: int,
        session_string: str,
        session: AsyncSession = Depends(get_async_session)
):
    return await db_handlers.update_sessionstring_tgaccount(
        session, id_account, session_string
    )


async def delete_tgaccount(
        id_account: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await db_handlers.delete_tgaccount(
        session, id_account
    )
