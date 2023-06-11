import typing

from fastapi import APIRouter

from services.telegram import views
from settings import config
import services.telegram.schemas as tg_schemas


router = APIRouter(prefix="/telegram", tags=["TgAccount"])


router.add_api_route(
    path="/get_tgaccounts",
    endpoint=views.get_tgacconts,
    methods=["GET"],
    name=config.ACCOUNT_GET,
    response_model=typing.List[tg_schemas.TgAccountResponse],
)


router.add_api_route(
    path="/create_tgaccount",
    endpoint=views.create_tgaccount,
    methods=["POST"],
    name=config.ACCOUNT_ADD,
    response_model=tg_schemas.TgAccountResponse,
)


router.add_api_route(
    path="/update_tgaccount",
    endpoint=views.update_tgaccount,
    methods=["PATCH"],
    name=config.ACCOUNT_UPDATE,
    response_model=tg_schemas.TgAccountResponse,
)


router.add_api_route(
    path="/delete_tgaccount",
    endpoint=views.delete_tgaccount,
    methods=["DELETE"],
    name=config.ACCOUNT_DELETE
)
