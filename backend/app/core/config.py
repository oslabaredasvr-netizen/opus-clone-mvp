from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str | None = None
    gemini_api_key: str | None = None
    supabase_url: str | None = None
    supabase_key: str | None = None
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/0"
    database_url: str = "sqlite:///./app.db"

    class Config:
        env_file = ".env"

settings = Settings()
