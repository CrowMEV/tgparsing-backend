import fastapi as fa
from services.payment import views
from services.user.utils.permissions import RoleChecker
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
    dependencies=[fa.Depends(RoleChecker(["superuser", "admin", "user"]))],
)
payment_router.add_api_route(
    path="/create",
    endpoint=views.get_payment_link,
    methods=["POST"],
    name=config.PAYMENT_ADD,
    dependencies=[fa.Depends(RoleChecker(["user"]))],
)
payment_router.add_api_route(
    path="/callback",
    endpoint=views.result_callback,
    methods=["POST"],
    name=config.PAYMENTS_CALLBACK,
)
