import asyncio
import logging
from datetime import datetime

from sqlalchemy import select

from app.db.base import async_session
from app.db.models import Task
from app.common.enums import TaskStatusEnum


async def process_task(task_id: int) -> Task:
    async with async_session() as session:
        stmt = await session.execute(select(Task).filter(Task.id == task_id))
        task = stmt.scalars().first()
        try:
            await asyncio.sleep(5)
            task.status = TaskStatusEnum.SUCCESS.value
        except Exception as e:
            task.status = TaskStatusEnum.FAILED.value
            logging.exception(f"Error processing task {task.id}: {e}")

        task.updated_at = datetime.now()
        await session.commit()
