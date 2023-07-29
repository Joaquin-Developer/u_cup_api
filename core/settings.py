from typing import List
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "u_cup_api"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    STATISTICS_SERVICE_URL: str = "http://127.0.0.1:8001"


settings = Settings()
