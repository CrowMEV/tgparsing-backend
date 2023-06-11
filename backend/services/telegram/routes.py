from fastapi import APIRouter, Depends

from services.telegram import views
from settings import config
import services.telegram.schemas as tg_schemas


router = APIRouter(prefix="/telegram", tags=["TgAccount"])


router.add_api_route(
    path="/get_all_tgaccounts",
    endpoint=views.get_all_tgacconts,
    methods=["GET"],
    name=config.ACCOUNT_GET_ALL,
    response_model=tg_schemas.TgAccountRead,
)


router.add_api_route(
    path="/get_tgaccounts",
    endpoint=views.get_tgacconts,
    methods=["GET"],
    name=config.ACCOUNT_GET,
    response_model=tg_schemas.TgAccountRead,
)


router.add_api_route(
    path="/create_tgaccount",
    endpoint=views.create_tgaccount,
    methods=["POST"],
    name=config.ACCOUNT_ADD,
    response_model=tg_schemas.TgAccountResponse,
)


router.add_api_route(
    path="/update_inwork_tgaccount",
    endpoint=views.update_inwork_tgaccount,
    methods=["PATCH"],
    name=config.ACCOUNT_UPDATE,
    response_model=tg_schemas.TgAccountUpdate,
)


router.add_api_route(
    path="/update_isblocked_tgaccount",
    endpoint=views.update_isblocked_tgaccount,
    methods=["PATCH"],
    name=config.ACCOUNT_UPDATE,
    response_model=tg_schemas.TgAccountUpdate,
)


router.add_api_route(
    path="/update_bygeo_tgaccount",
    endpoint=views.update_bygeo_tgaccount,
    methods=["PATCH"],
    name=config.ACCOUNT_UPDATE,
    response_model=tg_schemas.TgAccountUpdate,
)


router.add_api_route(
    path="/update_sessionstring_tgaccount",
    endpoint=views.update_sessionstring_tgaccount,
    methods=["PATCH"],
    name=config.ACCOUNT_UPDATE,
    response_model=tg_schemas.TgAccountUpdate,
)

# delete_tgaccount
router.add_api_route(
    path="/delete_tgaccount",
    endpoint=views.delete_tgaccount,
    methods=["DELETE"],
    name=config.ACCOUNT_DELETE
)
