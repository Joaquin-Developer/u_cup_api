from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api_v1.api import api_router as api_router_v1
from app.api_v2.api import api_router as api_router_v2
from core.settings import settings


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url="/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(api_router_v1, prefix=settings.API_V1_STR)
app.include_router(api_router_v2, prefix=settings.API_V2_STR)
