from typing import List

import fastapi as fa

from services.user import schemas as user_schemas
from services.user import views
from services.user.dependencies import get_current_user
from services.user.utils.permissions import user_read
from services.user.utils.responses import HTTP_201
from settings import config


user_router = fa.APIRouter(prefix='/user', tags=['User'])

user_router.add_api_route(
    path='/login',
    methods=['POST'],
    endpoint=views.login,
    name=config.USER_LOGIN,
    response_model=user_schemas.UserRead,
)
user_router.add_api_route(
    path='/logout',
    methods=['POST'],
    endpoint=views.logout,
    name=config.USER_LOGOUT,
    dependencies=[fa.Depends(get_current_user)]
)
user_router.add_api_route(
    path='/',
    methods=['POST'],
    endpoint=views.create_user,
    name=config.USER_REGISTER,
    status_code=201,
    responses={**HTTP_201}
)
user_router.add_api_route(
    path='/',
    methods=['GET'],
    endpoint=views.get_users,
    name=config.USER_ALL,
    response_model=List[user_schemas.UserRead],
    dependencies=[fa.Depends(user_read)]
)
user_router.add_api_route(
    path='/{id}',
    methods=['GET'],
    endpoint=views.get_user_by_id,
    name=config.USER_BY_ID,
    response_model=user_schemas.UserRead,
    dependencies=[fa.Depends(user_read)]
)
user_router.add_api_route(
    path='/me',
    methods=["PATCH"],
    endpoint=views.patch_current_user,
    name=config.USER_PATCH,
    response_model=user_schemas.UserRead,
)
