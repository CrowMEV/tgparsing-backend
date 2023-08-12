import fastapi as fa
from services.role.schemas import RoleNameChoice
from services.tariff import views
from services.tariff.schemas import TariffResponse
from services.user.schemas import UserRead
from services.user.utils import permissions as perm
from settings import config


tariff_router = fa.APIRouter(
    prefix="/tariff",
    tags=["Tariff"],
)

tariff_router.add_api_route(
    path="/",
    endpoint=views.get_tariff_list,
    methods=["GET"],
    name=config.TARIFF_GET_ALL,
)

tariff_router.add_api_route(
    path="/",
    endpoint=views.create_tariff,
    methods=["POST"],
    name=config.TARIFF_ADD,
    response_model=TariffResponse,
    dependencies=[
        fa.Depends(
            perm.RoleChecker(
                [
                    RoleNameChoice.SUPERUSER,
                ]
            )
        )
    ],
)

tariff_router.add_api_route(
    path="/{id_row}",
    endpoint=views.change_tariff,
    methods=["PATCH"],
    name=config.TARIFF_PATCH,
    response_model=TariffResponse,
    dependencies=[
        fa.Depends(
            perm.RoleChecker(
                [
                    RoleNameChoice.SUPERUSER,
                ]
            )
        )
    ],
)

tariff_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_tariff,
    methods=["DELETE"],
    name=config.TARIFF_DELETE,
    dependencies=[
        fa.Depends(
            perm.RoleChecker(
                [
                    RoleNameChoice.SUPERUSER,
                ]
            )
        )
    ],
)

tariff_router.add_api_route(
    path="/purchase/{id_row}",
    endpoint=views.purchase_tariff,
    methods=["POST"],
    name=config.TARIFF_PURCHASE,
    response_model=UserRead,
)
