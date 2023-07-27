from typing import List

import fastapi as fa
from services.telegram.member import schemas, views
from settings import config


member_router = fa.APIRouter(prefix="/members", tags=["TG members"])

member_router.add_api_route(
    path="/",
    endpoint=views.get_members,
    methods=["GET"],
    name=config.MEMBER_GET_ALL,
    response_model=List[schemas.ChatMemberRead],
)
member_router.add_api_route(
    path="/{id_row}",
    endpoint=views.get_member_by_id,
    methods=["GET"],
    name=config.MEMBER_BY_ID,
    response_model=schemas.ChatMemberRead,
)
member_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_member,
    methods=["DELETE"],
    name=config.MEMBER_DELETE,
)


chat_router = fa.APIRouter(prefix="/chats", tags=["Parsered chats"])

chat_router.add_api_route(
    path="/",
    endpoint=views.get_chats,
    methods=["GET"],
    name=config.CHAT_GET_ALL,
    response_model=List[schemas.ParsedChatRead],
)
chat_router.add_api_route(
    path="/{id_row}",
    endpoint=views.get_chat_by_id,
    methods=["GET"],
    name=config.CHAT_BY_ID,
    response_model=schemas.ParsedChatRead,
)
chat_router.add_api_route(
    path="/{id_row}",
    endpoint=views.delete_chat,
    methods=["DELETE"],
    name=config.CHAT_DELETE,
)
