import datetime
from typing import Any

import fastapi as fa
import services.tariff.db_handlers as db_hand
import services.tariff.schemas as tariff_schemas
from database.db_async import get_async_session
from services.user.db_handlers import update_user
from services.user.dependencies import get_current_user
from services.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tariff_list(
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    tariffs = await db_hand.get_tariffs(session)
    return tariffs


async def get_tariff(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not tariff:
        raise fa.HTTPException(status_code=404, detail="Тариф не найден")
    return tariff


async def create_tariff(
    tariff_schema: tariff_schemas.TariffPostModel,
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    check_tariff = await db_hand.get_tariff_by_name(
        session, tariff_schema.name
    )
    if check_tariff:
        raise fa.HTTPException(
            status_code=400, detail="Имя тарифа должна быть уникальным"
        )
    tariff = await db_hand.create_tariff(session, tariff_schema.dict())
    return tariff


async def change_tariff(
    id_row: int,
    tariff_schema: tariff_schemas.TariffPatchModel,
    session: AsyncSession = fa.Depends(get_async_session),
):
    check_tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not check_tariff:
        raise fa.HTTPException(status_code=404, detail="Тариф не найден")
    patch_data = {
        key: value
        for key, value in tariff_schema.dict().items()
        if value is not None
    }
    if not patch_data:
        raise fa.HTTPException(
            status_code=400, detail="Пустое поле недопустимо"
        )
    changed_tariff = await db_hand.change_tariff(session, id_row, patch_data)
    return changed_tariff


async def delete_tariff(
    id_row: int, session: AsyncSession = fa.Depends(get_async_session)
) -> Any:
    check_tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not check_tariff:
        raise fa.HTTPException(status_code=404, detail="Тариф не найден")
    await db_hand.delete_tariff_by_id(session, id_row)
    return {"detail": "Тариф успешно удалён"}


async def purchase_tariff(
    id_row: int,
    user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not tariff:
        raise fa.HTTPException(status_code=404, detail="Тариф не найден")
    if user.balance < tariff.price:
        raise fa.HTTPException(
            status_code=404, detail="У вас недостаточно средств на балансе"
        )
    await update_user(
        session, user.id, {"balance": user.balance - tariff.price}
    )
    user_sub = await db_hand.get_user_subscribe(session, user.id)
    if not user_sub:
        create_data: dict = {
            "user_id": user.id,
            "tariff_id": tariff.id,
            "tariff_options": tariff.options,
            "end_date": (
                datetime.datetime.utcnow()
                + datetime.timedelta(tariff.limitation_days)
            ),
        }
        user_sub = await db_hand.create_user_subscribe(session, create_data)
        return user_sub
    update_data: dict = {
        "tariff_id": tariff.id,
        "tariff_options": tariff.options,
        "end_date": (
            datetime.datetime.utcnow()
            + datetime.timedelta(tariff.limitation_days)
        ),
        "active": True,
    }
    user_sub = await db_hand.update_user_subscribe(
        session, user.id, update_data
    )
    return user_sub
