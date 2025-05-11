import uuid

import fastapi
from fastapi import APIRouter, HTTPException, status

from db import tasks
from task_schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter()


@router.get("/tasks", response_model=list[TaskOut], status_code=status.HTTP_200_OK)
async def get_tasks():
    return [TaskOut(**task) for task in tasks.values()]

@router.get("/tasks/{task_uid}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def get_one_task(task_uid: str):
    task = tasks.get(task_uid)
    if task:
        result = TaskOut(**task)

        return result

    raise HTTPException(status_code=404, detail="Task not found")


@router.post("/tasks", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_task(task_body: TaskCreate):
    task_uid = str(uuid.uuid4())
    task = {"task_uid": task_uid, "title": task_body.title, "completed": False}
    tasks[task_uid] = task
    result = TaskOut(**task)

    return result

@router.patch("/tasks/{task_uid}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def mark_task_completed(task_uid: str):
    task = tasks.get(task_uid)
    if task:
        task["completed"] = True
        result = TaskOut(**task)

        return result

    raise HTTPException(status_code=404, detail="Task not found")

@router.put("/tasks/{task_uid}", response_model=TaskOut, status_code=status.HTTP_200_OK)
async def update_task(task_uid: str, task_body: TaskUpdate):
    task = tasks.get(task_uid)
    if task:
        task["title"] = task_body.title
        result = TaskOut(**task)

        return result

    raise HTTPException(status_code=404, detail="Task not found")


@router.delete("/tasks/{task_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_uid: str):
    task = tasks.pop(task_uid, None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"status": "deleted"}
