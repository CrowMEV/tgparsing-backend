import fastapi as fa
from services.telegram.bot_server import views
from services.user.dependencies import check_is_banned
from services.user.utils import permissions as perm
from settings import config


parser_router = fa.APIRouter(
    prefix="/parser",
    tags=["Parser"],
    dependencies=[fa.Depends(check_is_banned)],
)

parser_router.add_api_route(
    path="/members",
    endpoint=views.get_members,
    methods=["POST"],
    name=config.PARSER_MEMBERS,
    description="Получить всех пользователей из списка групп",
    dependencies=[fa.Depends(perm.CheckParserOptions("members"))],
)
parser_router.add_api_route(
    path="/activemembers",
    endpoint=views.get_active_members,
    methods=["POST"],
    name=config.PARSER_ACTIVE_MEMBERS,
    description="Получить всех пользователей из списка групп, "
    "которые проявляли активность за определенный период",
    dependencies=[fa.Depends(perm.CheckParserOptions("activity"))],
)
parser_router.add_api_route(
    "/geomembers",
    endpoint=views.get_members_by_geo,
    methods=["POST"],
    description="Получение пользователей по геолокации",
    dependencies=[fa.Depends(perm.CheckParserOptions("geo"))],
)
# TODO: Раскомментировать в случае реализации поиска чатов по ключевому слову
# parser_router.add_api_route(
#     "/chats",
#     endpoint=views.get_chats_by_word,
#     methods=["POST"],
#     description="Получение чатов по ключевому слову",
# )
