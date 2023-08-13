import aiofiles
import fastapi as fa
from services.role import schemas as role_schema
from services.user import db_handlers as db_hand
from services.user import schemas as user_schema
from services.user.models import User
from services.user.utils import security
from settings import config
from sqlalchemy.ext.asyncio import AsyncSession


async def update_user(
    session: AsyncSession,
    changing_user: User,
    update_data: user_schema.UserPatch,
) -> User | None:
    data = {
        key: value
        for key, value in update_data.__dict__.items()
        if value is not None
    }
    if not data:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_400_BAD_REQUEST,
            detail="Нет данных для изменений",
        )
    picture = data.get("avatar_url")
    if not data.get("is_staff") and data.get("is_staff") is not None:
        data["role_name"] = role_schema.RoleNameChoice.USER
    if data.get("role_name") == role_schema.RoleNameChoice.USER:
        data["is_staff"] = False
    if (
        data.get("role_name") != role_schema.RoleNameChoice.USER
        and data.get("role_name") is not None
    ):
        data["is_staff"] = True
    if picture and picture.content_type:
        folder_path = config.static_dir_url / config.AVATARS_FOLDER
        file_name = (
            f"{changing_user.email}"
            f".{data['avatar_url'].filename.split('.')[-1]}"
        )
        file_url = folder_path / file_name
        async with aiofiles.open(file_url, "wb") as p_f:
            await p_f.write(data["avatar_url"].file.read())
        data["avatar_url"] = str(file_url)
    else:
        data.pop("avatar_url", None)
    if data.get("hashed_password"):
        data["hashed_password"] = security.get_hash_password(
            data["hashed_password"]
        )
    user_db = await db_hand.update_user(session, changing_user.id, data)
    return user_db
