import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.payment.routes import router as payment_router
from services.role.routes import router as role_router
from services.tariff.routes import router as tariff_router
from settings import config
from services.user.schemas import UserCreate, UserRead
from services.user.utils.authentication_backend import auth_backend
from services.user.utils.fastapiusers import fastapi_users


MEDIA_DIR = os.path.join(config.BASE_DIR, config.STATIC_DIR)


app = FastAPI(title="TgParsing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").strip().split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(
        auth_backend, requires_verification=config.IS_VERIFIED
    ),
    prefix="/user",
    tags=["user"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/user",
    tags=["user"],
)
app.include_router(
    fastapi_users.get_users_router(
        UserRead, requires_verification=config.IS_VERIFIED
    ),
    prefix="/user",
    tags=["user"],
)
app.include_router(payment_router)
app.include_router(role_router)
app.include_router(tariff_router)
