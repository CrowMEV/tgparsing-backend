import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.payment.routes import payment_router
from services.role.routes import role_router
from services.tariff.routes import tariff_router
from services.user.routes import user_router
from settings import config


app = FastAPI(title=config.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").strip().split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(role_router)
app.include_router(tariff_router)
app.include_router(payment_router)
