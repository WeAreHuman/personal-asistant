from fastapi import APIRouter

from app.services.weather_service import get_current_weather, get_weather_recommendation

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/{city}")
async def weather(city: str):
    data = await get_current_weather(city)
    recommendation = get_weather_recommendation(data)
    return {**data, "recommendation": recommendation}


@router.get("/recommendation/{city}")
async def weather_recommendation(city: str):
    data = await get_current_weather(city)
    return {"city": city, "recommendation": get_weather_recommendation(data)}
