import aiohttp

from app.config import settings


async def get_current_weather(city: str) -> dict:
    """Fetch current weather, returns mock data if API key missing."""
    if not settings.WEATHER_API_KEY:
        return _mock_weather(city)

    url = f"{settings.WEATHER_API_URL}/weather"
    params = {
        "q": city,
        "appid": settings.WEATHER_API_KEY,
        "units": "imperial",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                params=params,
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                if resp.status != 200:
                    return _mock_weather(city)
                data = await resp.json()
                return {
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                }
    except Exception:
        return _mock_weather(city)


def _mock_weather(city: str) -> dict:
    return {
        "city": city,
        "temperature": 72.0,
        "feels_like": 70.0,
        "description": "partly cloudy",
        "humidity": 55,
        "wind_speed": 8.0,
        "mock": True,
    }


def get_weather_recommendation(weather_data: dict) -> str:
    """Return clothing/gear recommendation based on weather."""
    temp = weather_data.get("temperature", 72)
    description = weather_data.get("description", "").lower()
    wind = weather_data.get("wind_speed", 0)

    recommendations = []

    if "rain" in description or "drizzle" in description or "shower" in description:
        recommendations.append("carry an umbrella")
    if "snow" in description or "blizzard" in description:
        recommendations.append("wear boots and a heavy coat")
    elif temp < 32:
        recommendations.append("wear a heavy winter coat and gloves")
    elif temp < 50:
        recommendations.append("wear a warm jacket")
    elif temp < 65:
        recommendations.append("wear a light jacket or sweater")
    else:
        recommendations.append("dress lightly")

    if wind > 20:
        recommendations.append("it's quite windy outside")

    return " and ".join(recommendations).capitalize() + "."
