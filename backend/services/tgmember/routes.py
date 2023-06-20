from fastapi import APIRouter

from services.tgmember import views as tgm_views
from services.tgmember import schemas as tgm_schemas
from settings import config

router = APIRouter()

router.add_api_route(
    path="/",
    endpoint=tgm_views.get_members_list,
    methods=["GET"],
    tags=["parsing"],
    name=config.MEMBER_GET_ALL
)

router.add_api_route(
    path="/{member_id}",
    endpoint=tgm_views.get_member,
    methods=["GET"],
    tags=["parsing"],
    name=config.MEMBER_GET,
    response_model=tgm_schemas.ChatMemberRead
)

router.add_api_route(
    path="/",
    endpoint=tgm_views.create_members,
    methods=["POST"],
    tags=["parsing"],
    response_model=tgm_schemas.ChatMemberRead,
    name=config.MEMBER_ADD
)

router.add_api_route(
    path="/{member_id}",
    endpoint=tgm_views.delete_member,
    methods=["DELETE"],
    tags=["parsing"],
    name=config.MEMBER_DELETE
)

router.add_api_route(
    path="/chats",
    endpoint=tgm_views.get_chats_list,
    methods=["GET"],
    tags=["parsing"],
    name=config.CHAT_GET_ALL
)

router.add_api_route(
    path="/chats/{chat_id}",
    endpoint=tgm_views.get_chat,
    methods=["GET"],
    tags=["parsing"],
    name=config.CHAT_GET,
    response_model=tgm_schemas.ParseredChatRead
)

router.add_api_route(
    path="/chats/{chat_id}",
    endpoint=tgm_views.delete_chat,
    methods=["DELETE"],
    tags=["parsing"],
    name=config.CHAT_DELETE
)
