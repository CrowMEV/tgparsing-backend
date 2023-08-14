from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from services.payment.routes import payment_router
from services.role.routes import role_router
from services.tariff.routes import tariff_router
from services.telegram.account.ws.ws import ws_router
from services.telegram.tg_router import tg_router
from services.user.routes import user_router
from settings import config


app = FastAPI(
    title=config.APP_NAME,
    docs_url=config.DOCS_URL,
    redoc_url=config.REDOC_URL,
)

app.mount(
    "/static",
    StaticFiles(directory=config.BASE_DIR / "static"),
    name="static",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.APP_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=config.APP_ALLOWED_HOSTS
)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(tariff_router)
app.include_router(payment_router)
app.include_router(tg_router)
app.include_router(ws_router)
