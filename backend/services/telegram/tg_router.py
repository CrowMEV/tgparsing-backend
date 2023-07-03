import fastapi as fa

from services.telegram.account.routes import tgaccount_router
from services.telegram.member.routes import chat_router, member_router
from services.user.utils import permissions as perms


tg_router = fa.APIRouter(prefix="/telegram")

tg_router.include_router(tgaccount_router)
tg_router.include_router(member_router)
tg_router.include_router(chat_router)
