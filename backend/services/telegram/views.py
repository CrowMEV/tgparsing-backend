from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.db_async import get_async_session
from database.db_sync import create_db_session
import services.telegram.db_handlers as db_handlers


db_session = create_db_session()


async def get_all_tgacconts():
    tg_accounts = await db_handlers.get_all_tgaccounts(db_session)
    return tg_accounts


async def get_tgacconts(
        in_work: Optional[bool] = False,
        is_blocked: Optional[bool] = False,
        by_geo: Optional[bool] = False
):
    return await db_handlers.get_tgaccounts(
        db_session, in_work, is_blocked, by_geo
    )


async def create_tgaccount(
        api_id: int,
        api_hash: str,
        session_string: str
):
    account = await db_handlers.create_tgaccount(
        db_session, api_id, api_hash, session_string
    )
    return account


async def update_inwork_tgaccount(
        id_account: int,
        in_work: bool
):
    return await db_handlers.update_inwork_tgaccount(
        db_session, id_account, in_work
    )


async def update_isblocked_tgaccount(
        id_account: int,
        is_blocked: bool
):
    return await db_handlers.update_isblocked_tgaccount(
        db_session, id_account, is_blocked
    )

async def update_bygeo_tgaccount(
        id_account: int,
        by_geo: bool
):
    return await db_handlers.update_bygeo_tgaccount(
        db_session, id_account, by_geo
    )


async def update_sessionstring_tgaccount(
        id_account: int,
        session_string: str
):
    return await db_handlers.update_sessionstring_tgaccount(
        db_session, id_account, session_string
    )


async def delete_tgaccount(
        id_account: int
):
    return await db_handlers.delete_tgaccount(
        db_session, id_account
    )
