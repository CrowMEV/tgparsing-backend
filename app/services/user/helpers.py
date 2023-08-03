import aiofiles
import fastapi as fa
from services.user import db_handlers as db_hand
from services.user import schemas as user_schema
from services.user.models import User
from services.user.utils import security
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession


async def update_user(
    session: AsyncSession, user: User, update_data: user_schema.UserPatch
) -> User | None:
    data = update_data.dict()
    if not data:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для изменений",
        )
    if data.get("avatar_url"):
        folder_path = config.static_dir_url / config.AVATARS_FOLDER
        file_name = (
            f"{user.email}" f".{data['avatar_url'].filename.split('.')[-1]}"
        )
        file_url = folder_path / file_name
        async with aiofiles.open(file_url, "wb") as p_f:
            await p_f.write(data["avatar_url"].file.read())
        data["avatar_url"] = str(file_url)
    if data.get("hashed_password"):
        data["hashed_password"] = security.get_hash_password(
            data["hashed_password"]
        )
    user_db = await db_hand.update_user(session, user.id, data)
    return user_db
