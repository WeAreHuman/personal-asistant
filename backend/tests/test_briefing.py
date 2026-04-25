from unittest.mock import AsyncMock, patch


def test_get_daily_briefing(client, auth_headers):
    mock_weather = {
        "city": "New York",
        "temperature": 72.0,
        "feels_like": 70.0,
        "description": "partly cloudy",
        "humidity": 55,
        "wind_speed": 8.0,
        "mock": True,
    }
    mock_briefing = "Good morning! You have 0 tasks today."

    with patch(
        "app.routers.briefing.get_current_weather",
        new_callable=AsyncMock,
        return_value=mock_weather,
    ), patch(
        "app.routers.briefing.generate_daily_briefing",
        new_callable=AsyncMock,
        return_value=mock_briefing,
    ):
        response = client.get("/api/v1/briefing/daily", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "briefing" in data
    assert "weather" in data


def test_get_suggestions(client, auth_headers):
    mock_suggestions = [
        "Review your task list",
        "Schedule deep work time",
        "Follow up on deadlines",
    ]

    with patch(
        "app.routers.briefing.generate_task_suggestions",
        new_callable=AsyncMock,
        return_value=mock_suggestions,
    ):
        response = client.get("/api/v1/briefing/suggestions", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) == 3
