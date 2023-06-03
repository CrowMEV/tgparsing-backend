import fastapi as fa
from services.account import views


account_routes = fa.APIRouter(prefix="/accounts", tags=["Accounts"])


account_routes.add_api_route(
    path="/",
    endpoint=views.get_account,
    methods=["GET"],
)

account_routes.add_api_route(
    path="/by_params",
    endpoint=views.get_account_by_params,
    methods=["GET"],
)

account_routes.add_api_route(
    path="/",
    endpoint=views.add_account,
    methods=["POST"],
)

account_routes.add_api_route(
    path="/",
    endpoint=views.update_account,
    methods=["PATCH"],
)
account_routes.add_api_route(
    path="/",
    endpoint=views.delete_account,
    methods=["DELETE"],
)
