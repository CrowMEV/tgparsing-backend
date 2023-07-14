from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import services.tariff.db_handlers as db_hand
from database.db_async import get_async_session
from services.tariff.models import Tariff
from services.user.dependencies import get_current_user


async def add_subscribe(
    tariff: Tariff,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
) -> None:
    data = {
        "user_id": user.id,
        "tariff_id": tariff.id,
        "tariff_options": tariff.options,
        "end_date": datetime.now() + timedelta(tariff.limitation_days),
    }
    await db_hand.add_subscribe(session, data)


async def change_subscribe(
    tariff: Tariff,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
) -> None:
    data = {
        "id": user.subscribe.id,
        "tariff_id": tariff.id,
        "tariff_options": tariff.options,
        "end_date": datetime.now() + timedelta(tariff.limitation_days),
    }
    await db_hand.change_subscribe(session, data)
