import typing

import fastapi as fa

import services.telegram.account.schemas as tg_schemas
from services.telegram.account import views
from services.telegram.account.ws import auth_account
from services.user.utils import permissions as perms
from settings import config

tgaccount_router = fa.APIRouter(
    prefix="/tgaccount",
    tags=["TgAccount"],
    dependencies=[fa.Depends(perms.is_admin), fa.Depends(perms.is_superuser)],
)
tgaccount_router.add_api_route(
    path="/",
    endpoint=views.get_accounts,
    methods=["GET"],
    name=config.TG_GET_ALL,
    response_model=typing.List[tg_schemas.TgAccountRead],
)
tgaccount_router.add_api_route(
    path="/{id_row}",
    endpoint=views.get_tgaccount_by_id,
    methods=["GET"],
    name=config.TG_GET,
    response_model=tg_schemas.TgAccountRead,
)
tgaccount_router.add_api_route(
    path="/{id_row}",
    endpoint=views.update_tgaccount,
    methods=["PATCH"],
    name=config.TG_UPDATE,
    response_model=tg_schemas.TgAccountRead,
)
tgaccount_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_tgaccount,
    methods=["DELETE"],
    name=config.TG_DELETE,
)

# tgaccount_router.add_websocket_route(
#     path="/auth",
#     endpoint=auth_account
# )
