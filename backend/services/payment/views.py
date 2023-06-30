import decimal
from typing import Any

import fastapi as fa
from fastapi import Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

import services.payment.db_handlers as db_hand
import services.payment.schemas as payment_schemas
from database.db_async import get_async_session
from services.payment.utils.robokassa import (
    check_result_payment,
    generate_payment_link,
)
from services.role.schemas import RoleNameChoice
from services.user.dependencies import get_current_user
from settings import config


async def get_payment_link(
    amount: decimal.Decimal = Body(..., ge=1, decimal_places=2, embed=True),
    user=fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> str:
    payment_data = {
        "user": user.id,
        "amount": amount,
        "action": payment_schemas.PaymentChoice.DEBIT,
    }
    payment = await db_hand.add_payment(session, payment_data)
    url_data = {
        "inv_id": payment.id,
        "amount": amount,
        "email": user.email,
    }
    url = generate_payment_link(url_data)
    return url


async def check_responce(
    schema: payment_schemas.PaymentConfirm = fa.Depends(
        payment_schemas.PaymentConfirm.as_params
    ),
) -> fa.Response:
    check_result = check_result_payment(schema, strict_check=True)
    if check_result:
        detail = f"OK{schema.inv_id}"
    else:
        detail = config.RK_BAD_SIGNATURE
    response = JSONResponse(
        status_code=fa.status.HTTP_200_OK, content={"detail": detail}
    )
    return response


async def confirm_payment(
    schema: payment_schemas.PaymentConfirm = fa.Depends(
        payment_schemas.PaymentConfirm.as_params
    ),
    session: AsyncSession = fa.Depends(get_async_session),
) -> None:
    check_result = check_result_payment(schema)
    if check_result:
        await db_hand.upd_payment(session, schema.inv_id)


async def fail_payment() -> None:
    pass


async def get_payments(
    session: AsyncSession = fa.Depends(get_async_session),
    user=fa.Depends(get_current_user),
) -> Any:
    if user.role.name == RoleNameChoice.USER:
        payments = await db_hand.get_payments(session, user.id)
    else:
        payments = await db_hand.get_payments(session)
    return payments
