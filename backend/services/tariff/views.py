from typing import Sequence, Any

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
import services.tariff.db_handlers as tariff_db
from services.tariff.models import Tariff
import services.tariff.schemas as tariff_schemas


async def get_tariff_list(
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariffs = await tariff_db.get_tariffs(session)
    return tariffs


async def get_tariff(
        tariff_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff = await tariff_db.get_tariff_by_id(session, tariff_id)
    return tariff


async def create_tariff_view(
        tariff_schema: tariff_schemas.TariffPostModel,
        session: AsyncSession = Depends(get_async_session),
) -> Any:
    tariff: Tariff = await tariff_db.create_tariff(
        session, tariff_schema.dict()
    )
    return tariff
