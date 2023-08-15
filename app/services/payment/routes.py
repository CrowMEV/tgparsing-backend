from typing import List

import fastapi as fa
import services.payment.schemas as paymant_schema
from services.payment import views
from services.role.schemas import RoleNameChoice
from services.user.dependencies import check_is_banned
from services.user.utils import permissions as perm
from settings import config


payment_router = fa.APIRouter(
    prefix="/payment",
    tags=["Payment"],
)

payment_router.add_api_route(
    path="/",
    endpoint=views.get_payments,
    methods=["GET"],
    name=config.PAYMENTS_GET,
    response_model=List[paymant_schema.PaymentsGetAll],
    dependencies=[
        fa.Depends(
            perm.RoleChecker(
                [
                    RoleNameChoice.SUPERUSER,
                    RoleNameChoice.ADMIN,
                ]
            )
        )
    ],
)
payment_router.add_api_route(
    path="/create",
    endpoint=views.get_payment_link,
    methods=["POST"],
    name=config.PAYMENT_ADD,
    dependencies=[fa.Depends(check_is_banned)],
)
payment_router.add_api_route(
    path="/callback",
    endpoint=views.result_callback,
    methods=["POST"],
    name=config.PAYMENTS_CALLBACK,
)
