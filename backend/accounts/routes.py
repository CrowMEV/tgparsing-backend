import fastapi as fa
from accounts import views


router = fa.APIRouter(prefix="/accounts", tags=["Accounts"])


router.add_api_route(
    path="/",
    endpoint=views.get_account,
    methods=["GET"],
)

router.add_api_route(
    path="/by_params",
    endpoint=views.get_account_by_params,
    methods=["GET"],
)

router.add_api_route(
    path="/",
    endpoint=views.add_account,
    methods=["POST"],
)

router.add_api_route(
    path="/",
    endpoint=views.update_account,
    methods=["PATCH"],
)
router.add_api_route(
    path="/",
    endpoint=views.delete_account,
    methods=["DELETE"],
)
