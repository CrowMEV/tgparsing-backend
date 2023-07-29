import fastapi as fa
from database.db_async import get_async_session
from fastapi.responses import FileResponse
from services.telegram.tasks import db_handlers as db_hand
from services.user.dependencies import get_current_user
from services.user.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from utils import files


async def download_file(
    task_name: str = fa.Query(min_length=1),
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
) -> FileResponse:
    task = await db_hand.get_task_by_filter(
        session=session,
        data={
            "title": task_name,
            "user_id": current_user.id,
        },
    )
    if not task:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail="Такой задачи не существует",
        )
    file_url = await files.get_file_url(
        dir_url=str(current_user.id),
        file_name=task_name,
    )
    return FileResponse(
        path=file_url,
        media_type="application/octet-stream",
        filename=file_url.split("/")[-1],
    )


async def delete_task(
    task_name: str = fa.Query(min_length=1),
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
) -> fa.Response:
    task = await db_hand.get_task_by_filter(
        session=session,
        data={
            "title": task_name,
            "user_id": current_user.id,
        },
    )
    if not task:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail="Такой задачи не существует",
        )
    await db_hand.delete_task(
        session=session,
        task_id=task.id,
    )
    await files.delete_file(dir_name=str(current_user.id), file_name=task_name)
    return fa.Response(content="Задача удалена успешно")
