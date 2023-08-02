from typing import Sequence

import sqlalchemy as sa
from services.telegram.tasks.models import Task
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(session: AsyncSession, task_data: dict) -> Task:
    task = Task(**task_data)
    session.add(task)
    await session.commit()
    return task


async def update_task(
    session: AsyncSession, task_id: int, task_data: dict
) -> Task | None:
    stmt = (
        sa.update(Task)
        .where(Task.id == task_id)
        .values(**task_data)
        .returning(Task)
    )
    result = await session.execute(stmt)
    task = result.scalars().first()
    await session.commit()
    return task


async def get_tasks_by_filter(
    session: AsyncSession, data: dict
) -> Sequence[Task]:
    stmt = sa.select(Task).filter_by(**data)
    result = await session.execute(stmt)
    tasks = result.scalars().all()
    return tasks


async def delete_task(session: AsyncSession, task_id: int) -> None:
    stmt = sa.delete(Task).where(Task.id == task_id)
    await session.execute(stmt)
    await session.commit()
