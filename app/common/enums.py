from enum import Enum


class TaskStatusEnum(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
