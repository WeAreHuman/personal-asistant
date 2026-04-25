import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ScheduleCategory(str, enum.Enum):
    ASSIGNMENT = "ASSIGNMENT"
    JOB_SHIFT = "JOB_SHIFT"
    INTERNSHIP = "INTERNSHIP"
    FOOD_BANK = "FOOD_BANK"
    OTHER = "OTHER"


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(Uuid(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    category = Column(
        Enum(ScheduleCategory),
        default=ScheduleCategory.OTHER,
        nullable=False,
    )
    location = Column(String, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="schedules")
