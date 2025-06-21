from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://username:password@localhost:5432/cujae_calendar_db"
    
    # Application
    app_name: str = "CUJAE Calendar Management System"
    debug: bool = True
    secret_key: str = "your-secret-key-here"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 