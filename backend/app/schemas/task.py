import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.task import TaskCategory, TaskPriority, TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    category: TaskCategory = TaskCategory.OTHER
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[TaskCategory] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class TaskResponse(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
