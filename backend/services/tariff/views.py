from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import services.tariff.db_handlers as db_hand
import services.tariff.schemas as tariff_schemas
from database.db_async import get_async_session
from services.tariff.models import Tariff, TariffLimitPrice


async def get_tariff_list_view(
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    tariffs = await db_hand.get_tariffs(session)
    return tariffs


async def get_tariff_view(
    tariff_id: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff: Tariff | None = await db_hand.get_tariff_by_id(session, tariff_id)
    if not tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    return tariff


async def create_tariff_view(
    tariff_schema: tariff_schemas.TariffPostModel,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    check_tariff: Tariff | None = await db_hand.get_tariff_by_name(
        session, tariff_schema.name
    )
    if check_tariff:
        raise HTTPException(
            status_code=400, detail="Имя тарифа должно быть уникальным"
        )
    tariff: Tariff = await db_hand.create_tariff(session, tariff_schema.dict())
    return tariff


async def change_tariff_view(
    tariff_id: int,
    tariff_schema: tariff_schemas.TariffPatchModel,
    session: AsyncSession = Depends(get_async_session),
):
    check_tariff = await db_hand.get_tariff_by_id(session, tariff_id)
    if not check_tariff:
        raise HTTPException(status_code=404)
    patch_data = {
        key: value for key, value in tariff_schema.dict().items() if value
    }
    changed_tariff = await db_hand.change_tariff(
        session, tariff_id, patch_data
    )
    return changed_tariff


async def delete_tariff_view(
    tariff_id: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    await db_hand.delete_tariff_by_id(session, tariff_id)
    return {"detail": "success"}


# Tariff prices
async def tariff_prices_list_view(
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    prices = await db_hand.tariff_prices_list(session)
    return prices


async def get_tariff_prices_view(
    tariff_id: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    prices = await db_hand.get_tariff_prices(session, tariff_id)
    return prices


async def get_tariff_price_view(
    tariff_price_id: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff_price: TariffLimitPrice | None = (
        await db_hand.get_tariff_price_by_id(session, tariff_price_id)
    )
    if not tariff_price:
        raise HTTPException(status_code=404, detail="Прайс тарифа не найден")
    return tariff_price


async def create_tariff_price_view(
    tariff_price_schema: tariff_schemas.TariffLimitPostModel,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    tariff: Tariff | None = await db_hand.get_tariff_by_id(
        session, tariff_price_schema.tariff
    )
    if not tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    tariff_price: TariffLimitPrice = await db_hand.create_tariff_price(
        session, tariff_price_schema.dict()
    )
    return tariff_price


async def change_tariff_price_view(
    tariff_price_id: int,
    tariff_price_schema: tariff_schemas.TariffLimitPatchModel,
    session: AsyncSession = Depends(get_async_session),
):
    check_tariff_price: TariffLimitPrice | None = (
        await db_hand.get_tariff_price_by_id(session, tariff_price_id)
    )
    if not check_tariff_price:
        raise HTTPException(status_code=404, detail="Прайс тарифа не найден")
    check_tariff = await db_hand.get_tariff_by_id(
        session, tariff_price_schema.tariff
    )
    if not check_tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    patch_data: dict = {
        key: value
        for key, value in tariff_price_schema.dict().items()
        if value is not None
    }
    changed_tariff_price = await db_hand.change_tariff_price(
        session, tariff_price_id, patch_data
    )
    return changed_tariff_price


async def delete_tariff_price_view(
    tariff_price_id: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    await db_hand.delete_tariff_price(session, tariff_price_id)
    return {"detail": "success"}
