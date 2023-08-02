import fastapi as fa
from services.payment import views
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
)
payment_router.add_api_route(
    path="/{tariff_id}",
    endpoint=views.get_payment_link,
    methods=["POST"],
    name=config.PAYMENT_ADD,
)
payment_router.add_api_route(
    path="/fail",
    endpoint=views.fail_payment,
    methods=["GET"],
    name=config.PAYMENT_FAIL,
)
payment_router.add_api_route(
    path="/success",
    endpoint=views.success_payment,
    methods=["GET"],
    name=config.PAYMENT_FAIL + "success",
)
