import fastapi as fa

from services.telegram.bot_server import views
from settings import config


parser_router = fa.APIRouter(prefix="/parser", tags=["Parser"])

parser_router.add_api_route(
    path="/members",
    endpoint=views.get_members,
    description="Получить всех пользователей из списка групп",
    name=config.PARSER_MEMBERS,
)
parser_router.add_api_route(
    "/geomembers",
    endpoint=views.get_members_by_geo,
    methods=["GET"],
    description="Получение пользователей по геолокации"
)
