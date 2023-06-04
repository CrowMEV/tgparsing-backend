from fastapi import APIRouter, Depends

from services.role import views
from services.user.utils.permissions import is_superuser


router = APIRouter(prefix="/role", tags=["Role"])

router.add_api_route(
    path="/",
    endpoint=views.get_role,
    methods=["GET"],
    dependencies=[Depends(is_superuser)],
)
router.add_api_route(
    path="/",
    endpoint=views.add_role,
    methods=["POST"],
    dependencies=[Depends(is_superuser)],
)
router.add_api_route(
    path="/",
    endpoint=views.update_role,
    methods=["PATCH"],
    dependencies=[Depends(is_superuser)],
)
router.add_api_route(
    path="/",
    endpoint=views.delete_role,
    methods=["DELETE"],
    dependencies=[Depends(is_superuser)],
)
router.add_api_route(
    path="/all",
    endpoint=views.get_roles,
    methods=["GET"],
    dependencies=[Depends(is_superuser)],
)
