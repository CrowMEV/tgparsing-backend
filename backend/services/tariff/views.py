from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import services.tariff.db_handlers as db_hand
import services.tariff.schemas as tariff_schemas
from database.db_async import get_async_session
from services.payment.utils.balance import is_purchasable
from services.payment.views import purchases_payment
from services.user.dependencies import get_current_user


async def get_tariff_list(
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    tariffs = await db_hand.get_tariffs(session)
    return tariffs


async def get_tariff(
    id_row: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    return tariff


async def create_tariff(
    tariff_schema: tariff_schemas.TariffPostModel,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    check_tariff = await db_hand.get_tariff_by_name(
        session, tariff_schema.name
    )
    if check_tariff:
        raise HTTPException(
            status_code=400, detail="Имя тарифа должна быть уникальным"
        )
    tariff = await db_hand.create_tariff(session, tariff_schema.dict())
    return tariff


async def change_tariff(
    id_row: int,
    tariff_schema: tariff_schemas.TariffPatchModel,
    session: AsyncSession = Depends(get_async_session),
):
    check_tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not check_tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    patch_data = {
        key: value for key, value in tariff_schema.dict().items() if value
    }
    if not patch_data:
        raise HTTPException(status_code=400, detail="Пустое поле недопустимо")
    changed_tariff = await db_hand.change_tariff(session, id_row, patch_data)
    return changed_tariff


async def delete_tariff(
    id_row: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    check_tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not check_tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    await db_hand.delete_tariff_by_id(session, id_row)
    return {"detail": "Тариф успешно удалён"}


async def buy_tariff(
    id_row: int,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(get_current_user),
) -> Any:
    tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    check_data = {
        "user": user.id,
        "price": tariff.price,
    }
    if not await is_purchasable(session, check_data):
        return {"detail": "Не хватает доступных средств"}
    return await purchases_payment(tariff, user, session)
