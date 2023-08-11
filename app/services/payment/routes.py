import fastapi as fa
from services.payment import views
from services.role.schemas import RoleNameChoice
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
    dependencies=[
        fa.Depends(
            perm.RoleChecker(
                [
                    RoleNameChoice.SUPERUSER,
                    RoleNameChoice.ADMIN,
                    RoleNameChoice.USER,
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
)
payment_router.add_api_route(
    path="/callback",
    endpoint=views.result_callback,
    methods=["POST"],
    name=config.PAYMENTS_CALLBACK,
)
payment_router.add_api_route(
    path="/fail",
    endpoint=views.fail_url,
    methods=["POST"],
)
