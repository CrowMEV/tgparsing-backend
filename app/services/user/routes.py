from typing import List

import fastapi as fa
from services.role.schemas import RoleNameChoice
from services.user import schemas as user_schemas
from services.user import views
from services.user.dependencies import check_is_banned, get_current_user
from services.user.utils import permissions as perm
from settings import config
from utils.responses import HTTP_201, HTTP_401


user_router = fa.APIRouter(prefix="/user", tags=["User"])

ADMINS = [
    RoleNameChoice.SUPERUSER,
    RoleNameChoice.ADMIN,
]

user_router.add_api_route(
    path="/",
    methods=["POST"],
    endpoint=views.create_user,
    name=config.USER_REGISTER,
    status_code=201,
    responses={**HTTP_201},  # type: ignore
)
user_router.add_api_route(
    path="/",
    methods=["GET"],
    endpoint=views.get_users,
    name=config.USER_ALL,
    response_model=List[user_schemas.UserRead],
    dependencies=[fa.Depends(perm.RoleChecker(ADMINS))],
)
user_router.add_api_route(
    path="/login",
    methods=["POST"],
    endpoint=views.login,
    name=config.USER_LOGIN,
    response_model=user_schemas.UserRead,
)
user_router.add_api_route(
    path="/logout",
    methods=["POST"],
    endpoint=views.logout,
    name=config.USER_LOGOUT,
    dependencies=[fa.Depends(get_current_user)],
)
user_router.add_api_route(
    "/refresh",
    methods=["GET"],
    endpoint=views.refresh_user,
    name=config.USER_REFRESH_TOKEN,
    response_model=user_schemas.UserRead,
    responses={**HTTP_401},  # type: ignore
)
user_router.add_api_route(
    path="/ban",
    methods=["POST"],
    endpoint=views.set_ban_for_user,
    name=config.USER_DO_BAN,
    response_model=user_schemas.UserRead,
    dependencies=[fa.Depends(perm.RoleChecker(ADMINS))],
    description="This method can use admin and superuser",
)
user_router.add_api_route(
    path="/me",
    methods=["PATCH"],
    endpoint=views.patch_current_user,
    name=config.USER_PATCH,
    response_model=user_schemas.UserRead,
    dependencies=[fa.Depends(check_is_banned)],
)
user_router.add_api_route(
    path="/pass",
    methods=["POST"],
    endpoint=views.check_password,
    name=config.USER_CHECK_PASSWORD,
    dependencies=[fa.Depends(check_is_banned)],
)
user_router.add_api_route(
    path="/{id_row}",
    methods=["GET"],
    endpoint=views.get_user_by_id,
    name=config.USER_BY_ID,
    response_model=user_schemas.UserRead,
    dependencies=[fa.Depends(perm.RoleChecker(ADMINS))],
    description="This method can use admin and superuser",
)
user_router.add_api_route(
    path="/{id_row}",
    methods=["PATCH"],
    endpoint=views.patch_user_by_admin,
    name=config.USER_PATCH_BY_ADMIN,
    response_model=user_schemas.UserRead,
    dependencies=[fa.Depends(perm.RoleChecker(ADMINS))],
    description="This method can use admin and superuser",
)
