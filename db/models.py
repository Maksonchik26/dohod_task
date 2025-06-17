from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from db.base import Base, UpdateMixin


class Task(Base, UpdateMixin):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    completed: Mapped[bool] = mapped_column(nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now(), server_default=func.now())
