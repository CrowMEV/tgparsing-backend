import fastapi as fa
from fastapi.security import APIKeyCookie
from settings import config


api_key = APIKeyCookie(name=config.COOKIE_NAME, auto_error=False)


def set_cookie(response: fa.Response, token: str) -> fa.Response:
    response.set_cookie(
        key=config.COOKIE_NAME,
        value=token,
        max_age=config.COOKIE_AGE,
        secure=config.COOKIE_SECURE,
        httponly=config.COOKIE_HTTPONLY,
        samesite=config.COOKIE_SAME_SITE,
    )
    return response


def drop_cookie(response: fa.Response) -> fa.Response:
    response.delete_cookie(
        key=config.COOKIE_NAME,
        secure=config.COOKIE_SECURE,
        httponly=config.COOKIE_HTTPONLY,
        samesite=config.COOKIE_SAME_SITE,
    )
    return response


async def get_cookie_key(token: str = fa.Security(api_key)) -> str:
    if not token:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
        )
    return token
