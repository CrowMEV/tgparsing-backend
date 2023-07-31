from typing import Any

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
    tasks = await db_hand.get_tasks_by_filter(
        session=session,
        data={
            "title": task_name,
            "user_id": current_user.id,
        },
    )
    if not tasks:
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
        filename=file_url.name,
    )


async def delete_task(
    task_name: str = fa.Query(min_length=1),
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
) -> fa.Response:
    tasks = await db_hand.get_tasks_by_filter(
        session=session,
        data={
            "title": task_name,
            "user_id": current_user.id,
        },
    )
    if not tasks:
        raise fa.HTTPException(
            status_code=fa.status.HTTP_404_NOT_FOUND,
            detail="Такой задачи не существует",
        )
    task = tasks[0]
    await db_hand.delete_task(
        session=session,
        task_id=task.id,
    )
    await files.delete_file(dir_name=str(current_user.id), file_name=task_name)
    return fa.Response(content="Задача удалена успешно")


async def get_user_tasks(
    session: AsyncSession = fa.Depends(get_async_session),
    current_user: User = fa.Depends(get_current_user),
) -> Any:
    tasks = await db_hand.get_tasks_by_filter(
        session=session,
        data={
            "user_id": current_user.id,
        },
    )
    return tasks


async def get_tasks(
    session: AsyncSession = fa.Depends(get_async_session),
) -> Any:
    tasks = await db_hand.get_tasks_by_filter(
        session=session,
        data={},
    )
    return tasks
