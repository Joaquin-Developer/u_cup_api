import os
from typing import List
from pydantic import BaseSettings, AnyHttpUrl


env = os.getenv("ENV") or "development"
env_dir = os.getenv("ENV_DIR") or os.getcwd()

class Settings(BaseSettings):
    PROJECT_NAME: str = "u_cup_api"
    ENVIRONMENT: str
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_DSN: str
    STATISTICS_SERVICE_URL: str = "http://127.0.0.1:8001"

    class Config:
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings(_env_file=f"{env_dir}/environments/.env.{env}", ENVIRONMENT=env)
