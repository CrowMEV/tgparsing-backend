import fastapi as fa
from services.tariff import views
from services.tariff.schemas import TariffResponse
from services.user.utils.permissions import RoleChecker
from settings import config


tariff_router = fa.APIRouter(
    prefix="/tariff",
    tags=["Tariff"],
    dependencies=[fa.Depends(RoleChecker(["superuser"]))],
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
)

tariff_router.add_api_route(
    path="/{id_row}",
    endpoint=views.get_tariff,
    methods=["GET"],
    name=config.TARIFF_GET,
    response_model=TariffResponse,
)

tariff_router.add_api_route(
    path="/{id_row}",
    endpoint=views.change_tariff,
    methods=["PATCH"],
    name=config.TARIFF_PATCH,
    response_model=TariffResponse,
)

tariff_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_tariff,
    methods=["DELETE"],
    name=config.TARIFF_DELETE,
)
