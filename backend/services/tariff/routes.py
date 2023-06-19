from fastapi import APIRouter, Depends

from services.tariff import views
from services.tariff.schemas import TariffResponse
from services.user.utils.permissions import is_superuser
from settings import config

router = APIRouter(prefix="/tariff", tags=["Tariff"])


router.add_api_route(
    path='/',
    endpoint=views.get_tariff_list,
    methods=['GET'],
    name=config.TARIFF_GET_ALL
)

router.add_api_route(
    path='/',
    endpoint=views.create_tariff_view,
    methods=['POST'],
    name=config.TARIFF_ADD,
    dependencies=[Depends(is_superuser)],
    response_model=TariffResponse
)

router.add_api_route(
    path='/{id}',
    endpoint=views.get_tariff,
    methods=['GET'],
    name=config.TARIFF_GET,
    response_model=TariffResponse
)
