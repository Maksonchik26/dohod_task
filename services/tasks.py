from crud.tasks import TasksCRUD
from db.models import Task

async def mark_completed(task_id: int, crud: TasksCRUD) -> Task:
    task = await crud.read_one(task_id)
    task.completed = True
    await crud.session.commit()
    await crud.session.refresh(task)
    return task