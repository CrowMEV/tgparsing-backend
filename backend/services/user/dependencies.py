from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db_async import get_async_session
from services.user.models import User
from services.user.utils.manager import UserManager
from services.user.utils.sql_database import AppSQLAlchemyUserDatabase


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield AppSQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
