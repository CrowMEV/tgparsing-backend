import fastapi as fa
from services.telegram.tasks import views
from settings import config


task_router = fa.APIRouter(prefix="/tasks", tags=["Tasks"])

task_router.add_api_route(
    path="/",
    endpoint=views.delete_task,
    methods=["DELETE"],
    name=config.TASK_DELETE,
)
task_router.add_api_route(
    path="/download",
    endpoint=views.download_file,
    methods=["GET"],
    name=config.TASK_DOWNLOAD,
)
