from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    title: str

    model_config = ConfigDict(extra='forbid')

class TaskUpdate(TaskCreate):
    pass

class TaskOut(TaskCreate):
    id: int
    completed: bool
    created_at: datetime

    class Config:
        orm_mode = True
