from fastapi import APIRouter

from app.api_v1.endpoints import metadata, partido, resultados, equipos, estadisticas, fase_final

api_router = APIRouter()

api_router.include_router(partido.router, prefix="/partido", tags=["partido"])
api_router.include_router(resultados.router, prefix="/resultados", tags=["resultados"])
api_router.include_router(equipos.router, prefix="/equipos", tags=["equipos"])
api_router.include_router(estadisticas.router, prefix="/estadisticas", tags=["estadisticas"])
api_router.include_router(fase_final.router, prefix="/fase_final", tags=["fase_final"])
api_router.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
