from fastapi_users.authentication import JWTStrategy

from settings import config


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=config.JWT_SECRET, lifetime_seconds=3600)
