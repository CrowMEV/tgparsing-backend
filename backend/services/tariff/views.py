from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import services.tariff.db_handlers as db_hand
import services.tariff.schemas as tariff_schemas
from database.db_async import get_async_session


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
    changed_tariff = await db_hand.change_tariff(session, id_row, patch_data)
    return changed_tariff


async def delete_tariff(
    id_row: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    check_tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not check_tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    await db_hand.delete_tariff_benefits(session, id_row)
    await db_hand.delete_tariff_by_id(session, id_row)
    return {"detail": "Тариф успешно удалён"}


# benefits
async def benefits_list(
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    benefits = await db_hand.get_benefits(session)
    return benefits


async def benefit_get(
    id_row: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    benefit = await db_hand.get_benefit_by_id(session, id_row)
    if not benefit:
        raise HTTPException(status_code=404, detail="Преимущество не найдено")
    return benefit


async def benefit_create(
    benefit_schema: tariff_schemas.BenefitRequest,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    check_benefit = await db_hand.get_benefit_by_name(
        session, benefit_schema.name
    )
    if check_benefit:
        raise HTTPException(
            status_code=400, detail="Преимущество уже существует"
        )
    benefit = await db_hand.create_benefit(session, benefit_schema.dict())
    return benefit


async def benefit_update(
    id_row: int,
    benefit_schema: tariff_schemas.BenefitRequest,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    check_benefit = await db_hand.get_benefit_by_id(session, id_row)
    if not check_benefit:
        raise HTTPException(status_code=404, detail="Преимущество не найдено")
    update_data = {
        key: value for key, value in benefit_schema.dict().items() if value
    }
    benefit = await db_hand.change_benefit(session, id_row, update_data)
    return benefit


async def benefit_delete(
    id_row: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    check_benefit = await db_hand.get_benefit_by_id(session, id_row)
    if not check_benefit:
        raise HTTPException(status_code=404, detail="Преимущество не найдено")
    await db_hand.delete_benefit_by_id(session, id_row)
    return {"detail": "Преимущество успешно удалено"}


# tariff benefits
async def get_tariff_benefits(
    id_row: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    check_tariff = await db_hand.get_tariff_by_id(session, id_row)
    if not check_tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    benefits = await db_hand.tariff_benefits(session, id_row)
    return benefits


async def add_benefit_tariff(
    tariff_benefit_schema: tariff_schemas.TariffBenefitCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Any:
    check_tariff = await db_hand.get_tariff_by_id(
        session, tariff_benefit_schema.tariff_id
    )
    if not check_tariff:
        raise HTTPException(status_code=404, detail="Тариф не найден")
    check_benefit = await db_hand.get_benefit_by_id(
        session, tariff_benefit_schema.benefit_id
    )
    if not check_benefit:
        raise HTTPException(status_code=404, detail="Преимущество не найдено")
    check_tariff_benefit = await db_hand.get_tariff_benefit(
        session,
        tariff_benefit_schema.tariff_id,
        tariff_benefit_schema.benefit_id,
    )
    if check_tariff_benefit:
        raise HTTPException(
            status_code=400, detail="Преимущество уже связано на тариф"
        )
    tariff_benefit = await db_hand.create_tariff_benefit(
        session, tariff_benefit_schema.dict()
    )
    return tariff_benefit


async def delete_benefit_tariff(
    id_row: int, session: AsyncSession = Depends(get_async_session)
) -> Any:
    tariff_benefit = await db_hand.get_tariff_benefit_by_id(session, id_row)
    if not tariff_benefit:
        raise HTTPException(
            status_code=404, detail="Преимущество не связано на тариф"
        )
    await db_hand.delete_tariff_benefit(session, id_row)
    return {"detail": "Преимущество успешно отвязано"}
