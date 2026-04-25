# Personal Assistant AI

An AI-powered personal assistant MVP built with FastAPI, providing daily briefings, task management, schedule tracking, and weather-based recommendations.

## Features

- **JWT Authentication** – Register, login, and manage your profile securely
- **Task Management** – Full CRUD for tasks with categories (Assignment, Job Shift, Internship, Food Bank), priorities, and statuses
- **Schedule Management** – Calendar events with today/date-range filters and recurrence support
- **AI Daily Briefing** – GPT-3.5-powered morning briefing summarising your tasks, schedule, and weather (falls back to a template when no API key is set)
- **Weather Integration** – Current conditions via OpenWeatherMap with clothing recommendations
- **Location Utilities** – Distance calculation and travel time estimates via geopy

## Tech Stack

- **Backend:** Python 3.11, FastAPI, SQLAlchemy 2.0, Alembic
- **Database:** PostgreSQL (production), SQLite in-memory (tests)
- **Auth:** JWT via `python-jose`, bcrypt via `passlib`
- **AI:** OpenAI GPT-3.5-turbo
- **Weather:** OpenWeatherMap API
- **Testing:** pytest, pytest-asyncio, pytest-cov
- **Containerisation:** Docker + docker-compose

## Quick Start

### Prerequisites

- Python 3.11+
- Docker & docker-compose (optional)

### Run with Docker

```bash
cp .env.example .env   # fill in your API keys
docker-compose up --build
```

API available at <http://localhost:8000>
Docs at <http://localhost:8000/docs>

### Run locally

```bash
cd backend
pip install -r requirements.txt -r requirements-dev.txt
cp ../.env.example .env   # fill in values
uvicorn app.main:app --reload
```

### Run tests

```bash
cd backend
pytest tests/ -v --cov=app
```

## Project Structure

```
personal-asistant/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── config.py        # Pydantic Settings
│   │   ├── database.py      # SQLAlchemy engine & session
│   │   ├── dependencies.py  # FastAPI dependency injection
│   │   ├── models/          # SQLAlchemy ORM models
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── routers/         # API route handlers
│   │   ├── services/        # Business logic (AI, weather, auth)
│   │   └── utils/           # Security helpers
│   ├── alembic/             # Database migrations
│   ├── tests/               # pytest test suite
│   ├── Dockerfile
│   └── requirements.txt
├── .github/workflows/ci.yml # GitHub Actions CI
├── docker-compose.yml
├── .env.example
└── CONTRIBUTING.md
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Register a new user |
| POST | `/api/v1/auth/login` | Obtain JWT token |
| GET | `/api/v1/auth/me` | Get current user |
| GET | `/api/v1/tasks` | List tasks (filterable) |
| POST | `/api/v1/tasks` | Create a task |
| GET | `/api/v1/tasks/upcoming` | Tasks due in next 7 days |
| GET | `/api/v1/schedules/today` | Today's schedule |
| GET | `/api/v1/briefing/daily` | AI daily briefing |
| GET | `/api/v1/briefing/suggestions` | AI task suggestions |
| GET | `/api/v1/weather/{city}` | Current weather |

## Environment Variables

See [`.env.example`](.env.example) for all available settings.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT
