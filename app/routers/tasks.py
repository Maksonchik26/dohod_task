from datetime import datetime

from fastapi import APIRouter, HTTPException, status, Depends, Response, BackgroundTasks

from app.common.enums import TaskStatusEnum
from app.crud.tasks import TasksCRUD
from app.schemas.tasks import TaskCreate, TaskUpdate, TaskOut
from app.services.tasks import process_task as bg_process_task

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)


@router.get("/", response_model=list[TaskOut], status_code=status.HTTP_200_OK)
async def get_tasks(
        limit: int | None = None,
        offset: int | None = None,
        tasks_crud: TasksCRUD = Depends(),
):
    tasks = await tasks_crud.read_all(limit, offset)
    return tasks

@router.get("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def get_one_task(
        task_id: int,
        tasks_crud: TasksCRUD = Depends(),
):
    task = await tasks_crud.read_one(task_id)

    if task:
        return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(
        task_data: TaskCreate,
        tasks_crud: TasksCRUD = Depends(),
):
    task = await tasks_crud.create(task_data)

    return task


@router.put("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def update_task(
        task_id: int,
        task_data: TaskUpdate,
        tasks_crud: TasksCRUD = Depends(),
):
    if await tasks_crud.read_one(task_id):
        task = await tasks_crud.update(task_id, task_data)

        return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        tasks_crud: TasksCRUD = Depends(),
):
    if await tasks_crud.read_one(task_id):
        await tasks_crud.delete(task_id)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/{task_id}/process", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def process_task(
        background_tasks: BackgroundTasks,
        task_id: int,
        tasks_crud: TasksCRUD = Depends(),
):
    task = await tasks_crud.read_one(task_id)
    task.updated_at = datetime.now()
    task.status = TaskStatusEnum.IN_PROGRESS.value
    await tasks_crud.session.commit()

    background_tasks.add_task(bg_process_task, task_id)

    return task
