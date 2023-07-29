from email import message as em
from typing import Any

import aiosmtplib as asmp
from aiosmtplib.errors import SMTPException
from services.user import db_handlers as db_hand
from services.user.models import User
from services.user.utils import security
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession


async def send_mail(email, url) -> Any:
    message = em.EmailMessage()
    message["From"] = config.EMAIL_FROM
    message["To"] = email
    message["Subject"] = config.EMAIL_SUBJECT
    message.set_content(
        f"Для подтверждения регистрации перейдите по ссылке {url}"
    )
    host = config.EMAIL_HOST
    port = config.EMAIL_PORT
    username = config.EMAIL_USERNAME
    password = config.EMAIL_PASSWORD
    try:
        await asmp.send(
            message,
            hostname=host,
            port=port,
            username=username,
            password=password,
        )
        return {"detail": "Письмо успешно отправлено"}
    except SMTPException:
        return {"detail": "Подтверждающее письмо не отправлено"}


async def get_user_from_token(
    session: AsyncSession,
    token: str,
) -> User | None:
    data = security.decode_token(token)
    email = data["email"]
    user = await db_hand.get_user_by_email(session, email)
    return user
