from datetime import datetime, timedelta

import fastapi as fa
from jose import jwt, JWTError
from passlib.context import CryptContext

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


def decode_token(token: str) -> dict | str:
    try:
        data = jwt.decode(
            token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM]
        )
    except JWTError as err:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_403_FORBIDDEN,
            detail="Wrong token or it has expired",
        )
    return data


def get_hash_password(password: str) -> str:
    """Hash password"""
    hash_pass = pwd_context.hash(password)
    return hash_pass


def validate_password(password: str, hashed_password: str) -> bool:
    """Validate password hash with user db hash."""
    return pwd_context.verify(password, hashed_password)
