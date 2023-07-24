from typing import List

import fastapi as fa

from services.user import schemas as user_schemas
from services.user import views
from services.user.dependencies import get_current_user
from services.user.utils.permissions import is_admin, user_read
from settings import config
from utils.responses import HTTP_201, HTTP_401


user_router = fa.APIRouter(prefix="/user", tags=["User"])

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
    dependencies=[fa.Depends(user_read)],
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
    path="/me",
    methods=["PATCH"],
    endpoint=views.patch_current_user,
    name=config.USER_PATCH,
    response_model=user_schemas.UserRead,
)
user_router.add_api_route(
    path="/{id_row}",
    methods=["GET"],
    endpoint=views.get_user_by_id,
    name=config.USER_BY_ID,
    response_model=user_schemas.UserRead,
    dependencies=[fa.Depends(user_read)],
)
user_router.add_api_route(
    path="/pass",
    methods=["POST"],
    endpoint=views.check_password,
    name=config.USER_CHECK_PASSWORD,
)

user_router.add_api_route(
    path="/verify/",
    methods=["PATCH"],
    endpoint=views.verify_user,
    name=config.USER_VERIFY,
)

user_router.add_api_route(
    path="/delete",
    methods=["DELETE"],
    endpoint=views.delete_non_active_users,
    name=config.USER_DELETE_NON_ACTIVE,
    dependencies=[fa.Depends(is_admin)],
)
