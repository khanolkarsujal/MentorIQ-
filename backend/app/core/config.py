from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from typing import Optional, List

class Settings(BaseSettings):
    GROQ_API_KEY: Optional[str] = None
    GITHUB_TOKEN: Optional[str] = None
    REDIS_URL: Optional[str] = None
    
    # App
    PROJECT_NAME: str = "MentorIQ"
    API_V1_STR: str = "/api"
    ENV: str = "development"
    
    # CORS — set to your Netlify URL in production .env
    # Example: ALLOWED_ORIGINS=["https://mentorqi1.netlify.app"]
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
