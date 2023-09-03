from fastapi import APIRouter

from app.api_v2.endpoints import equipos, estadisticas, partidos, metadata

api_router = APIRouter()

api_router.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
api_router.include_router(estadisticas.router, prefix="/estadisticas", tags=["estadisticas"])
api_router.include_router(equipos.router, prefix="/equipos", tags=["equipos"])
