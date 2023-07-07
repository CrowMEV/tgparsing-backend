from fastapi import APIRouter, Depends

from services.tariff import views
from services.tariff.schemas import (
    BenefitResponse,
    TariffBenefitResponse,
    TariffResponse,
)
from services.user.utils.permissions import is_superuser
from settings import config


tariff_router = APIRouter(prefix="/tariff", tags=["Tariff"])
benefits_router = APIRouter(prefix="/benefits", tags=["Benefits"])
tariff_benefits_router = APIRouter(
    prefix="/benefits", tags=["Tariff benefits"]
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
    dependencies=[Depends(is_superuser)],
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
    dependencies=[Depends(is_superuser)],
)

tariff_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_tariff,
    methods=["DELETE"],
    name=config.TARIFF_DELETE,
    dependencies=[Depends(is_superuser)],
)

# benefits
benefits_router.add_api_route(
    path="/",
    endpoint=views.benefits_list,
    methods=["GET"],
    name=config.BENEFIT_GET_ALL,
)

benefits_router.add_api_route(
    path="/",
    endpoint=views.benefit_create,
    methods=["POST"],
    name=config.BENEFIT_ADD,
    response_model=BenefitResponse,
    dependencies=[Depends(is_superuser)],
)

benefits_router.add_api_route(
    path="/{id_row}",
    endpoint=views.benefit_get,
    methods=["GET"],
    name=config.BENEFIT_GET,
    response_model=BenefitResponse,
)

benefits_router.add_api_route(
    path="/{id_row}",
    endpoint=views.benefit_update,
    methods=["PATCH"],
    name=config.BENEFIT_PATCH,
    response_model=BenefitResponse,
    dependencies=[Depends(is_superuser)],
)

benefits_router.add_api_route(
    path="/{id_row}",
    endpoint=views.benefit_delete,
    methods=["DELETE"],
    name=config.BENEFIT_DELETE,
    dependencies=[Depends(is_superuser)],
)

tariff_benefits_router.add_api_route(
    path="/",
    endpoint=views.add_benefit_tariff,
    methods=["POST"],
    name=config.TARIFF_BENEFIT_ADD,
    response_model=TariffBenefitResponse,
    dependencies=[Depends(is_superuser)],
)

tariff_benefits_router.add_api_route(
    path="/{id_row}",
    endpoint=views.get_tariff_benefits,
    methods=["GET"],
    name=config.TARIFF_BENEFIT_GET_ALL,
)

tariff_benefits_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_benefit_tariff,
    methods=["DELETE"],
    name=config.TARIFF_BENEFIT_DELETE,
    dependencies=[Depends(is_superuser)],
)


tariff_router.include_router(tariff_benefits_router)
