from typing import List
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "u_cup_api"
    API_V1_STR: str = "/api/v1"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []


settings = Settings()
