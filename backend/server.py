from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from user.utils.authentication import auth_backend
from user.dependencies import get_user_manager
from user.utils.fastapiusers import FastApiUsers
from user.schemas import UserRead, UserCreate
from database.models.user_model import User


fastapi_users = FastApiUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app = FastAPI(title='TgParsing')

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
