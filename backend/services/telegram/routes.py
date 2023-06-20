import typing

from fastapi import APIRouter

from services.telegram import views
from settings import config
import services.telegram.schemas as tg_schemas


router = APIRouter(prefix="/telegram", tags=["TgAccount"])


router.add_api_route(
    path="/{id_account}",
    endpoint=views.get_tgaccount,
    methods=["GET"],
    name=config.ACCOUNT_GET,
    response_model=tg_schemas.TgAccountRead
)


router.add_api_route(
    path="/",
    endpoint=views.get_tgaccounts,
    methods=["GET"],
    name=config.ACCOUNTS_GET,
    response_model=typing.List[tg_schemas.TgAccountRead],
)


router.add_api_route(
    path="/",
    endpoint=views.create_tgaccount,
    methods=["POST"],
    name=config.ACCOUNT_ADD,
    response_model=tg_schemas.TgAccountRead,
)


router.add_api_route(
    path="/{id_account}",
    endpoint=views.update_tgaccount,
    methods=["PATCH"],
    name=config.ACCOUNT_UPDATE,
    response_model=tg_schemas.TgAccountBase,
)


router.add_api_route(
    path="/{id_account}",
    endpoint=views.delete_tgaccount,
    methods=["DELETE"],
    name=config.ACCOUNT_DELETE
)
