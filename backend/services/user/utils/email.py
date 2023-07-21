from email import message as em

import aiosmtplib as asmp
import fastapi as fa
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from services.user import db_handlers as db_hand
from services.user.models import User
from services.user.utils import security
from settings import config


async def send_mail(
    request: fa.Request,
    email,
    session: AsyncSession,
) -> JSONResponse:
    user = await db_hand.get_user_by_email(session, email)
    if not user:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Пользователя не существует или токен устарел",
        )
    token_date = {
        "email": user.email,
        "password": user.hashed_password
    }
    token = security.create_token(token_date)
    url = request.url_for(config.USER_VERIFY, token=token)
    message = em.EmailMessage()
    message["From"] = config.EMAIL_FROM
    message["To"] = email
    message["Subject"] = config.EMAIL_SUBJECT
    message.set_content(
        f"Для подтверждения регистрации перейдите по ссылке {url}",
    )
    host = config.EMAIL_HOST
    port = config.EMAIL_PORT
    username = config.EMAIL_USERNAME
    password = config.EMAIL_PASSWORD

    await asmp.send(
        message, hostname=host, port=port,
        username=username, password=password)
    return JSONResponse(
        status_code=200,
        content={"message": "Подтверждающее письмо отправлено"}
    )


async def get_user_from_token(
    session: AsyncSession,
    token: str,
) -> User | None:
    data = security.decode_token(token)
    email = data["email"]
    user = await db_hand.get_user_by_email(session, email)
    return user
