from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore
from typing import Optional

class Settings(BaseSettings):
    GROQ_API_KEY: Optional[str] = None
    GITHUB_TOKEN: Optional[str] = None
    
    # App
    PROJECT_NAME: str = "MentorIQ"
    API_V1_STR: str = "/api"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

settings = Settings()
