from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, briefing, schedules, tasks, weather

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="AI-powered personal assistant API",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(tasks.router, prefix=API_PREFIX)
app.include_router(schedules.router, prefix=API_PREFIX)
app.include_router(briefing.router, prefix=API_PREFIX)
app.include_router(weather.router, prefix=API_PREFIX)


@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.APP_NAME}
