from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
import services.tariff.db_handlers as tariff_db
from services.tariff.models import Tariff, TariffLimitPrice
import services.tariff.schemas as tariff_schemas


async def get_tariff_list_view(
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariffs = await tariff_db.get_tariffs(session)
    return tariffs


async def get_tariff_view(
        tariff_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff: Tariff | None = await tariff_db.get_tariff_by_id(
        session, tariff_id
    )
    if not tariff:
        raise HTTPException(status_code=404, detail='Tariff not found')
    return tariff


async def create_tariff_view(
        tariff_schema: tariff_schemas.TariffPostModel,
        session: AsyncSession = Depends(get_async_session),
) -> Any:
    check_tariff: Tariff | None = await tariff_db.get_tariff_by_name(
        session, tariff_schema.name
    )
    if check_tariff:
        raise HTTPException(
            status_code=400,
            detail="tariff name must be unique"
        )
    tariff: Tariff = await tariff_db.create_tariff(
        session, tariff_schema.dict()
    )
    return tariff


async def change_tariff_view(
        tariff_id: int,
        tariff_schema: tariff_schemas.TariffPatchModel,
        session: AsyncSession = Depends(get_async_session)
):
    check_tariff: Tariff | None = await tariff_db.get_tariff_by_id(
        session, tariff_id
    )
    if not check_tariff:
        raise HTTPException(
            status_code=404, detail='Tariff not found'
        )
    patch_data: dict = {
        key: value
        for key, value in tariff_schema.dict().items()
        if value is not None
    }
    changed_tariff: Tariff = await tariff_db.change_tariff(
        session, tariff_id, patch_data
    )
    return changed_tariff


async def delete_tariff_view(
        tariff_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    await tariff_db.delete_tariff_by_id(session, tariff_id)
    return {'detail': 'success'}


# Tariff prices
async def tariff_prices_list_view(
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    prices = await tariff_db.tariff_prices_list(session)
    return prices


async def get_tariff_prices_view(
        tariff_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    prices = await tariff_db.get_tariff_prices(session, tariff_id)
    return prices


async def get_tariff_price_view(
        tariff_price_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff_price: TariffLimitPrice | None = (
        await tariff_db.get_tariff_price_by_id(session, tariff_price_id)
    )
    if not tariff_price:
        raise HTTPException(status_code=404, detail='Tariff price not found')
    return tariff_price


async def create_tariff_price_view(
        tariff_price_schema: tariff_schemas.TariffLimitPostModel,
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff: Tariff | None = await tariff_db.get_tariff_by_id(
        session, tariff_price_schema.tariff
    )
    if not tariff:
        raise HTTPException(status_code=404, detail='tariff not found')
    tariff_price: TariffLimitPrice = await tariff_db.create_tariff_price(
        session, tariff_price_schema.dict()
    )
    return tariff_price


async def change_tariff_price_view(
        tariff_price_id: int,
        tariff_price_schema: tariff_schemas.TariffLimitPatchModel,
        session: AsyncSession = Depends(get_async_session)
):
    check_tariff_price: TariffLimitPrice | None = (
        await tariff_db.get_tariff_price_by_id(session, tariff_price_id)
    )
    if not check_tariff_price:
        raise HTTPException(
            status_code=404, detail='Tariff price not found'
        )
    check_tariff: Tariff | None = await tariff_db.get_tariff_by_id(
        session, tariff_price_schema.tariff
    )
    if not check_tariff:
        raise HTTPException(
            status_code=404, detail='Tariff not found'
        )
    patch_data: dict = {
        key: value
        for key, value in tariff_price_schema.dict().items()
        if value is not None
    }
    changed_tariff_price: TariffLimitPrice = (
        await tariff_db.change_tariff_price(
            session, tariff_price_id, patch_data
        )
    )
    return changed_tariff_price


async def delete_tariff_price_view(
        tariff_price_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> Any:
    await tariff_db.delete_tariff_price(session, tariff_price_id)
    return {'detail': 'success'}
