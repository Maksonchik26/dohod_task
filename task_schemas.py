from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(TaskCreate):
    pass

class TaskOut(TaskCreate):
    task_uid: str
    completed: bool
