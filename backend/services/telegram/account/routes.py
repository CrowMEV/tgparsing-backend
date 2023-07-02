import typing

import fastapi as fa

import services.telegram.account.schemas as tg_schemas
from services.telegram.account import views
from services.user.utils import permissions as perms
from settings import config
from utils.responses import HTTP_201


tg_router = fa.APIRouter(
    prefix="/telegram",
    tags=["TgAccount"],
    dependencies=[fa.Depends(perms.is_admin), fa.Depends(perms.is_superuser)],
)

tg_router.add_api_route(
    path="/",
    endpoint=views.get_accounts,
    methods=["GET"],
    name=config.TG_GET_ALL,
    response_model=typing.List[tg_schemas.TgAccountRead],
)
tg_router.add_api_route(
    path="/",
    endpoint=views.create_tgaccount,
    methods=["POST"],
    name=config.TG_CREATE,
    status_code=201,
    responses={**HTTP_201},  # type: ignore
)
tg_router.add_api_route(
    path="/{id_row}",
    endpoint=views.get_tgaccount_by_id,
    methods=["GET"],
    name=config.TG_GET,
    response_model=tg_schemas.TgAccountRead,
)
tg_router.add_api_route(
    path="/{id_row}",
    endpoint=views.update_tgaccount,
    methods=["PATCH"],
    name=config.TG_UPDATE,
    response_model=tg_schemas.TgAccountRead,
)
tg_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_tgaccount,
    methods=["DELETE"],
    name=config.TG_DELETE,
)
