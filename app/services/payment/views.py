from decimal import Decimal
from typing import Annotated, Any

import fastapi as fa
import services.payment.db_handlers as db_hand
import services.payment.schemas as payment_schemas
from database.db_async import get_async_session
from services.payment.utils.robokassa import (
    calculate_signature,
    generate_payment_link,
)
from services.role.schemas import RoleNameChoice
from services.user.db_handlers import get_current_by_id, update_user
from services.user.dependencies import get_current_user
from services.user.models import User
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession


async def get_payment_link(
    create_schema: payment_schemas.PaymentCreate,
    user: User = fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    payment_data = {
        "user_id": user.id,
        "amount": create_schema.amount,
        "action": payment_schemas.PaymentChoice.DEBIT,
    }
    payment = await db_hand.add_payment(session, payment_data)
    url_data = {
        "inv_id": payment.id,
        "amount": create_schema.amount,
        "email": create_schema.email or user.email,
    }
    url = generate_payment_link(url_data)
    return url


async def result_callback(
    out_sum: Annotated[Decimal, fa.Form(alias="OutSum")],
    out_sum2: Annotated[Decimal, fa.Form(alias="out_summ")],
    inv_id: Annotated[int, fa.Form(alias="InvId")],
    signature: Annotated[str, fa.Form(alias="SignatureValue")],
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    if out_sum != out_sum2:
        raise fa.HTTPException(status_code=400, detail="Суммы не совпадают")
    signature_2 = calculate_signature(
        out_sum, inv_id, config.RK_CHECK_PASS_2ND
    )
    if signature.lower() != signature_2:
        raise fa.HTTPException(status_code=400, detail="Хэшы не совпадают")
    payment = await db_hand.get_payment_by_id(session, inv_id)
    if not payment:
        raise fa.HTTPException(status_code=400, detail="Тикет не найден")
    user = await get_current_by_id(session, payment.user_id)
    if not user:
        raise fa.HTTPException(
            status_code=400, detail="Пользователь не найден"
        )
    await update_user(session, user.id, {"balance": user.balance + out_sum})
    await db_hand.upd_payment(session, inv_id, {"status": True})
    return f"OK{inv_id}"


async def get_payments(
    get_data: payment_schemas.PaymentsGetAll = fa.Depends(),
    session: AsyncSession = fa.Depends(get_async_session),
    user: User = fa.Depends(get_current_user),
) -> Any:
    data = {
        key: value
        for key, value in get_data.dict().items()
        if value is not None
    }
    if user.role.name == RoleNameChoice.USER:
        data["user_id"] = user.id
    payments = await db_hand.get_payments(session, data)
    return payments
