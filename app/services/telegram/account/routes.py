import typing

import fastapi as fa
import services.telegram.account.schemas as tg_schemas
from services.role.schemas import RoleNameChoice
from services.telegram.account import views
from services.user.utils import permissions as perm
from settings import config


tgaccount_router = fa.APIRouter(
    prefix="/tgaccount",
    tags=["TgAccount"],
    dependencies=[
        fa.Depends(
            perm.RoleChecker([RoleNameChoice.SUPERUSER, RoleNameChoice.ADMIN])
        )
    ],
)

tgaccount_router.add_api_route(
    path="/",
    endpoint=views.get_accounts,
    methods=["GET"],
    name=config.TGACCOUNT_GET_ALL,
    response_model=typing.List[tg_schemas.TgAccountRead],
)
tgaccount_router.add_api_route(
    path="/{id_row}",
    endpoint=views.get_tgaccount_by_id,
    methods=["GET"],
    name=config.TGACCOUNT_GET,
    response_model=tg_schemas.TgAccountRead,
)
tgaccount_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_tgaccount,
    methods=["DELETE"],
    name=config.TGACCOUNT_DELETE,
)
