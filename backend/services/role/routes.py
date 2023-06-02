from fastapi import APIRouter
from services.role import views


role_routes = APIRouter(prefix="/roles", tags=["Role"])


role_routes.add_api_route(
    path="/all",
    endpoint=views.get_roles,
    methods=["GET"],
)
role_routes.add_api_route(
    path="/",
    endpoint=views.get_role,
    methods=["GET"],
)
role_routes.add_api_route(
    path="/",
    endpoint=views.add_role,
    methods=["POST"],
)
role_routes.add_api_route(
    path="/",
    endpoint=views.update_role,
    methods=["PATCH"],
)
role_routes.add_api_route(
    path="/",
    endpoint=views.delete_role,
    methods=["DELETE"],
)
