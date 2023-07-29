import fastapi as fa
from services.telegram.account.routes import tgaccount_router
from services.telegram.bot_server.routes import parser_router
from services.telegram.member.routes import chat_router, member_router
from services.telegram.tasks.routes import task_router


tg_router = fa.APIRouter(prefix="/telegram")

tg_router.include_router(tgaccount_router)
tg_router.include_router(member_router)
tg_router.include_router(chat_router)
tg_router.include_router(parser_router)
tg_router.include_router(task_router)
