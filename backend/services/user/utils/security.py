import json
from datetime import datetime, timedelta

import fastapi as fa
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from passlib.context import CryptContext

from services.user.models import User
from services.user.schemas import UserRead
from services.user.utils.cookie import set_cookie
from settings import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(data: dict) -> str:
    """Create token for user"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=config.JWT_TOKEN_AGE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        data = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
    except JWTError:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_403_FORBIDDEN,
            detail="Неверный токен или он истек",
        ) from None
    return data


def get_hash_password(password: str) -> str:
    """Hash password"""
    hash_pass = pwd_context.hash(password)
    return hash_pass


def validate_password(password: str, hashed_password: str) -> bool:
    """Validate password hash with user db hash."""
    return pwd_context.verify(password, hashed_password)


def login(user: User, data: dict) -> fa.Response:
    access_token = create_token(data)
    user_json = UserRead.from_orm(user).json()
    user_data = json.loads(user_json)
    response = JSONResponse(
        status_code=fa.status.HTTP_200_OK,
        content=user_data,
    )
    set_cookie(response, access_token)
    return response
