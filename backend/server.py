import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database.models.user_model import User
from settings import config
from user.dependencies import get_user_manager
from user.schemas import UserCreate, UserRead
from user.utils.authentication import auth_backend
from user.utils.fastapiusers import FastApiUsers


fastapi_users = FastApiUsers[User, int](
    get_user_manager,
    [auth_backend],
)

MEDIA_DIR = os.path.join(config.BASE_DIR, config.STATIC_DIR)


app = FastAPI(title="TgParsing")
app.mount(
    '/static',
    StaticFiles(directory=MEDIA_DIR),
    name='static'
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").strip().split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/user",
    tags=["user"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/user",
    tags=["user"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead),
    prefix="/user",
    tags=["user"],
)
