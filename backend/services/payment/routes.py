from fastapi import APIRouter, Depends

from services.payment import views
from services.user.utils.permissions import payment_read
from settings import config


payment_router = APIRouter(prefix="/payment", tags=["Payment"])

payment_router.add_api_route(
    path="/",
    endpoint=views.get_payments,
    methods=["GET"],
    name=config.PAYMENTS_GET,
    dependencies=[Depends(payment_read)],
)
payment_router.add_api_route(
    path="/",
    endpoint=views.get_payment_link,
    methods=["POST"],
    name=config.PAYMENT_ADD,
)
payment_router.add_api_route(
    path="/check",
    endpoint=views.check_responce,
    methods=["GET"],
    name=config.PAYMENT_CHK,
)
payment_router.add_api_route(
    path="/success",
    endpoint=views.confirm_payment,
    methods=["GET"],
    name=config.PAYMENT_UPD,
)
payment_router.add_api_route(
    path="/fail",
    endpoint=views.fail_payment,
    methods=["GET"],
    name=config.PAYMENT_FAIL,
)
