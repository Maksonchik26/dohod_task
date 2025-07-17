from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.common.enums import TaskStatusEnum


class TaskCreate(BaseModel):
    title: str

    model_config = ConfigDict(extra='forbid')

class TaskUpdate(TaskCreate):
    pass

class TaskOut(TaskCreate):
    id: int
    status: TaskStatusEnum
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, extra='forbid')
