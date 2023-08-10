import fastapi as fa
from services.tariff.errors import TARIFF_OPTIONS_ERRORS
from services.telegram.bot_server import views
from services.user.dependencies import CheckParserOptions
from settings import config


parser_router = fa.APIRouter(
    prefix="/parser",
    tags=["Parser"],
    dependencies=[
        fa.Depends(CheckParserOptions(TARIFF_OPTIONS_ERRORS)),
    ],
)

parser_router.add_api_route(
    path="/members",
    endpoint=views.get_members,
    methods=["POST"],
    name=config.PARSER_MEMBERS,
    description="Получить всех пользователей из списка групп",
)
parser_router.add_api_route(
    path="/activemembers",
    endpoint=views.get_active_members,
    methods=["POST"],
    name=config.PARSER_ACTIVE_MEMBERS,
    description="Получить всех пользователей из списка групп, "
    "которые проявляли активность за определенный период",
)
parser_router.add_api_route(
    "/geomembers",
    endpoint=views.get_members_by_geo,
    methods=["POST"],
    description="Получение пользователей по геолокации",
)
# TODO: Раскомментировать в случае реализации поиска чатов по ключевому слову
# parser_router.add_api_route(
#     "/chats",
#     endpoint=views.get_chats_by_word,
#     methods=["POST"],
#     description="Получение чатов по ключевому слову",
# )
