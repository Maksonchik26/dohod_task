from sqlalchemy import select

from crud.common import CRUD
from db.models import Task
from schemas.tasks import TaskCreate, TaskUpdate


class TasksCRUD(CRUD):
    async def read_all (self):
        tasks = await self.session.execute(select(Task))
        result = tasks.scalars().all()

        return result

    async def read_one(self, task_id: int):
        task = await self.session.execute(select(Task).filter(Task.id == task_id))
        result = task.scalars().first()

        return result

    async def create(self, task_data: TaskCreate):
        task = Task(**task_data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def update(self, task_id: int, task_data: TaskUpdate):
        task = await self.read_one(task_id)
        task.update_entity(**task_data.model_dump())
        await self.session.commit()

        return task

    async def mark_as_completed(self, task_id: int):
        task = await self.read_one(task_id)
        task.completed = True

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def delete(self, task_id: int):
        task = await self.read_one(task_id)
        await self.session.delete(task)
        await self.session.commit()
