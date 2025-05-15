from fastapi import APIRouter, HTTPException, status, Depends

from crud.tasks import TasksCRUD
from db.models import Task
from schemas.tasks import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(
    prefix='/tasks',
    tags=['platform']
)


@router.get("/", response_model=list[TaskOut], status_code=status.HTTP_200_OK)
async def get_tasks(
        tasks_crud: TasksCRUD = Depends(),
):
    tasks = await tasks_crud.read_all()
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

@router.patch("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def mark_task_completed(
        task_id: int,
        tasks_crud: TasksCRUD = Depends(),
):
    if await tasks_crud.read_one(task_id):
        task = await tasks_crud.mark_as_completed(task_id)

        return task

    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/{task_id}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def update_task(
        task_id: int,
        task_data: TaskUpdate,
        tasks_crud: TasksCRUD = Depends(),
):
    if tasks_crud.read_one(task_id):
        task = await tasks_crud.update(task_id, task_data)

        return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        tasks_crud: TasksCRUD = Depends(),
):
    if tasks_crud.read_one(task_id):
        await tasks_crud.delete(task_id)

        return {"status": "deleted"}

    raise HTTPException(status_code=404, detail="Task not found")
