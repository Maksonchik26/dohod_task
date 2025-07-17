from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from app.db.base import Base, UpdateMixin
from app.common.enums import TaskStatusEnum


class Task(Base, UpdateMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False, default=TaskStatusEnum.CREATED.value)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now(), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now(), server_default=func.now())
