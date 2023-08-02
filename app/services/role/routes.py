import fastapi as fa
import services.role.schemas as role_schemas
from services.role import views
from services.user.utils.permissions import RoleChecker
from settings import config


role_router = fa.APIRouter(
    prefix="/role",
    tags=["Role"],
    dependencies=[fa.Depends(RoleChecker(["superuser"]))],
)

role_router.add_api_route(
    path="/{name}",
    endpoint=views.get_role,
    methods=["GET"],
    name=config.ROLE_GET,
    response_model=role_schemas.RoleResponse,
)
role_router.add_api_route(
    path="/",
    endpoint=views.patch_role,
    methods=["PATCH"],
    name=config.ROLE_PATCH,
    response_model=role_schemas.RoleResponse,
)
role_router.add_api_route(
    path="/",
    endpoint=views.get_roles,
    methods=["GET"],
    name=config.ROLE_GET_ALL,
)
