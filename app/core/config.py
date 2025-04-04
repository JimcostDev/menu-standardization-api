from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent

class Settings(BaseSettings):
    MONGODB_URI_DEV_LAB_TEST: str
    MONGODB_NAME: str  
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PROJECT_NAME: str = "FastAPI E-commerce"
    PROJECT_DESCRIPTION: str = "E-commerce API with FastAPI"
    PROJECT_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: str = "http://localhost:4321/"
    
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "config.env",  
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()