from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql://postgres:postgres@localhost:5432/personal_assistant"
    )
    # IMPORTANT: Override SECRET_KEY with a strong random value in production.
    # Generate one with: python -c "import secrets; print(secrets.token_hex(32))"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENAI_API_KEY: str = ""
    WEATHER_API_KEY: str = ""
    WEATHER_API_URL: str = "https://api.openweathermap.org/data/2.5"
    APP_NAME: str = "Personal Assistant AI"
    # Comma-separated list of allowed CORS origins. Use "*" only in development.
    CORS_ORIGINS: str = "*"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
