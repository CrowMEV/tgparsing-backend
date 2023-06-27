from typing import List

import fastapi as fa

from services.tgmember import schemas as tgm_schemas
from services.tgmember import views as tgm_views
from settings import config

tgmember_router = fa.APIRouter(prefix="/tgmembers", tags=["TG members"])

tgmember_router.add_api_route(
    path="/",
    endpoint=tgm_views.get_members,
    methods=["GET"],
    name=config.MEMBER_ALL,
    response_model=List[tgm_schemas.ChatMemberRead],
)

tgmember_router.add_api_route(
    path="/{id_row}",
    endpoint=tgm_views.get_member_by_id,
    methods=["GET"],
    name=config.MEMBER_BY_ID,
    response_model=tgm_schemas.ChatMemberRead,
)

tgmember_router.add_api_route(
    path="/",
    endpoint=tgm_views.create_member,
    methods=["POST"],
    name=config.MEMBER_ADD,
    response_model=tgm_schemas.ChatMember,
)

tgmember_router.add_api_route(
    path="/{id_row}",
    endpoint=tgm_views.delete_member,
    methods=["DELETE"],
    name=config.MEMBER_DELETE,
)


chat_router = fa.APIRouter(prefix="/chats", tags=["Parsered chats"])


chat_router.add_api_route(
    path="/",
    endpoint=tgm_views.get_chats,
    methods=["GET"],
    name=config.CHAT_ALL,
    response_model=List[tgm_schemas.ParseredChatRead],
)

chat_router.add_api_route(
    path="/{id_row}",
    endpoint=tgm_views.get_chat_by_id,
    methods=["GET"],
    name=config.CHAT_BY_ID,
    response_model=tgm_schemas.ParseredChatRead,
)

chat_router.add_api_route(
    path="/",
    endpoint=tgm_views.create_chat,
    methods=["POST"],
    name=config.MEMBER_ADD,
    response_model=tgm_schemas.ChatMember,
)

chat_router.add_api_route(
    path="/{id_row}",
    endpoint=tgm_views.delete_chat,
    methods=["DELETE"],
    name=config.CHAT_DELETE,
)

tgmember_router.include_router(chat_router)

chatinmember_router = fa.APIRouter(
    prefix="/chatsinmembers", tags=["Parsered chats in members"]
)
chatinmember_router.add_api_route(
    path="/",
    endpoint=tgm_views.create_chat_in_member,
    methods=["POST"],
    name=config.CHAT_IN_MEMBER_ADD,
)

chatinmember_router.add_api_route(
    path="/{member_username}",
    endpoint=tgm_views.get_chats_in_member,
    methods=["GET"],
    name=config.CHATS_MEMBER_GET_ALL,
)


tgmember_router.include_router(chatinmember_router)
