from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.models.schedule import Schedule
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.services.ai_service import generate_daily_briefing, generate_task_suggestions
from app.services.weather_service import get_current_weather

router = APIRouter(prefix="/briefing", tags=["briefing"])


@router.get("/daily")
async def daily_briefing(
    city: str = "New York",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    tasks = (
        db.query(Task)
        .filter(
            Task.user_id == current_user.id,
            Task.status != TaskStatus.DONE,
            Task.status != TaskStatus.CANCELLED,
        )
        .limit(10)
        .all()
    )
    now = datetime.now(timezone.utc)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    schedules = (
        db.query(Schedule)
        .filter(
            Schedule.user_id == current_user.id,
            Schedule.start_time >= start_of_day,
            Schedule.start_time <= end_of_day,
        )
        .all()
    )
    weather = await get_current_weather(city)
    user_data = {
        "full_name": current_user.full_name,
        "username": current_user.username,
    }
    tasks_data = [
        {
            "title": t.title,
            "priority": t.priority.value,
            "due_date": str(t.due_date) if t.due_date else None,
        }
        for t in tasks
    ]
    schedules_data = [
        {"title": s.title, "start_time": str(s.start_time)} for s in schedules
    ]
    briefing = await generate_daily_briefing(
        user_data, tasks_data, schedules_data, weather
    )
    return {"briefing": briefing, "weather": weather}


@router.get("/suggestions")
async def task_suggestions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    recent_tasks = (
        db.query(Task)
        .filter(Task.user_id == current_user.id)
        .order_by(Task.created_at.desc())
        .limit(5)
        .all()
    )
    context = {
        "recent_tasks": [
            {"title": t.title, "category": t.category.value} for t in recent_tasks
        ]
    }
    suggestions = await generate_task_suggestions(context)
    return {"suggestions": suggestions}
