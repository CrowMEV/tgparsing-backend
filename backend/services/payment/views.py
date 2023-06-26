import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

import services.payment.db_handlers as db_hand
import services.payment.schemas as payment_schemas
from database.db_async import get_async_session
from services.payment.utils.robokassa import (
    check_result_payment,
    generate_payment_link,
)
from services.user.dependencies import get_current_user


async def get_payment_link(
    schema: payment_schemas.PaymentCreate,
    user=fa.Depends(get_current_user),
    session: AsyncSession = fa.Depends(get_async_session),
) -> str:
    data = {
        "user": user.id,
        "amount": schema.amount,
        "action": payment_schemas.PaymentChoice.DEBIT,
    }
    payment = await db_hand.add_payment(session, data)
    url = generate_payment_link(payment.id, schema)
    return url


async def check_responce(
    schema: payment_schemas.PaymentConfirm = fa.Depends(
        payment_schemas.PaymentConfirm.as_params
    ),
) -> JSONResponse:
    check_result = check_result_payment(schema, strict_check=True)
    if check_result:
        detail = f"OK{schema.inv_id}"
    else:
        detail = "error: bad signature"
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
        await db_hand.upd_payment(session, schema.inv_id, {"status": True})


async def fail_payment() -> None:
    pass
