from typing import Optional

from app.config import settings


async def generate_daily_briefing(
    user_data: dict,
    tasks: list,
    schedules: list,
    weather: Optional[dict] = None,
) -> str:
    """Generate AI daily briefing, gracefully handles missing API key."""
    if not settings.OPENAI_API_KEY:
        return _template_briefing(user_data, tasks, schedules, weather)

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

        task_summary = "\n".join(
            [
                f"- {t['title']} ({t['priority']}, due: {t.get('due_date', 'N/A')})"
                for t in tasks[:5]
            ]
        )
        schedule_summary = "\n".join(
            [f"- {s['title']} at {s['start_time']}" for s in schedules[:5]]
        )
        weather_info = (
            f"Weather: {weather.get('description', 'unknown')}, "
            f"{weather.get('temperature', '?')}°F"
            if weather
            else "Weather: not available"
        )

        prompt = (
            f"Generate a friendly, concise daily briefing for "
            f"{user_data.get('full_name', 'the user')}.\n"
            f"Today's tasks:\n{task_summary or 'No tasks'}\n"
            f"Today's schedule:\n{schedule_summary or 'No events'}\n"
            f"{weather_info}\n"
            "Keep it under 150 words, motivating and actionable."
        )

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return response.choices[0].message.content or _template_briefing(
            user_data, tasks, schedules, weather
        )
    except Exception:
        return _template_briefing(user_data, tasks, schedules, weather)


def _template_briefing(
    user_data: dict,
    tasks: list,
    schedules: list,
    weather: Optional[dict] = None,
) -> str:
    name = user_data.get("full_name") or user_data.get("username", "there")
    task_count = len(tasks)
    schedule_count = len(schedules)
    weather_note = ""
    if weather:
        weather_note = (
            f" It's {weather.get('description', 'unclear')} outside "
            f"({weather.get('temperature', '?')}°F)."
        )
    return (
        f"Good morning, {name}!{weather_note} "
        f"You have {task_count} task(s) and {schedule_count} event(s) today. "
        "Stay focused and have a productive day!"
    )


async def generate_task_suggestions(user_context: dict) -> list[str]:
    """Generate AI task suggestions, gracefully handles missing API key."""
    if not settings.OPENAI_API_KEY:
        return _default_suggestions()

    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        tasks = user_context.get("recent_tasks", [])
        task_list = ", ".join([t.get("title", "") for t in tasks[:5]])

        prompt = (
            f"Given these recent tasks: {task_list or 'none'}, "
            "suggest 3 productive tasks for today. "
            "Return as a simple numbered list."
        )
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        content = response.choices[0].message.content or ""
        lines = [
            line.strip().lstrip("123456789.)- ")
            for line in content.split("\n")
            if line.strip()
        ]
        return lines[:3] if lines else _default_suggestions()
    except Exception:
        return _default_suggestions()


def _default_suggestions() -> list[str]:
    return [
        "Review and prioritize your task list",
        "Schedule time for deep work on high-priority items",
        "Follow up on any pending assignments or deadlines",
    ]
