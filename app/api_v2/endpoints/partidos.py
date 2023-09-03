import logging
from typing import Tuple
import requests
from sqlalchemy.sql import text
from fastapi import APIRouter, HTTPException

from core.database import get_session
from models.partidos import Partido
from models.enfrentamiento import Enfrentamiento
from schemas import fases
from schemas import partidos
from core.settings import settings

logging.basicConfig(level=logging.INFO)

router = APIRouter()


@router.get("/fase_actual", response_model=fases.FaseActual)
def get_fase_actual():
    """
    Obtener cuál es la fase actual
    """
    query = text("""
        WITH fase_actual AS (
            SELECT id, nombre, ida_vuelta
            FROM fases
            WHERE id = (
                SELECT MAX(fase_id) 
                FROM enfrentamientos
            )
        )
        SELECT
            id,
            nombre,
            ida_vuelta
        FROM fase_actual
        UNION ALL
        SELECT
            0 as id,
            'Fase de Grupos' as nombre,
            1 as ida_vuelta
        FROM dual
        WHERE NOT EXISTS (SELECT * FROM fase_actual)
    """)
    with get_session() as session:
        row = session.execute(query).one()
    
    return fases.FaseActual(id=row.id, nombre=row.nombre, ida_vuelta=row.ida_vuelta)


def _update_partido(partido_id: int, partido_data: partidos.PartidoUpdate, fase_id: int) -> Tuple[int, int]:
    """
    Actualizar el resultado de un partido segun la fase
    fase_id: [0, 1, ..., n]
        0 := Fase de Grupos
    """
    with get_session() as session:
        # obtener el partido por su ID:
        if fase_id == 0:
            partido = session.query(Partido).filter(Partido.id == partido_id).first()
        else:
            partido = session.query(Enfrentamiento).filter(Enfrentamiento.id == partido_id).first()

        if not partido:
            raise HTTPException(status_code=404, detail="Partido no encontrado")

        partido.goles_local = partido_data.goles_local
        partido.goles_visitante = partido_data.goles_visitante

        if fase_id != 0:
            partido.penales_local = partido_data.penales_local or "null"
            partido.penales_visitante = partido_data.penales_visitante or "null"

        session.commit()

        # Devuelve los IDs de los equipos involucrados
        return partido.equipo_local_id, partido.equipo_visitante_id


def update_statistics(fase: str, local_id: int, visitante_id: int):
    """
    Llamada al microservicio de estadisticas para actualizar estadisticas
    """
    url = f"{settings.STATISTICS_SERVICE_URL}/estadisticas/{fase}"
    url += f"?equipos_id={local_id}&equipos_id={visitante_id}"

    resp = requests.post(url)
    if resp.status_code != 200:
        logging.warning("No se pudo actualizar las estadisticas")
        logging.info(resp.json())


@router.put("/partido/{partido_id}")
def update_partido(partido_id: int, partido_data: partidos.PartidoUpdate):
    id_fase_actual = get_fase_actual().id
    statistic_fase = "grupo" if id_fase_actual == 0 else "general"

    local_id, visitante_id = _update_partido(partido_id, partido_data, id_fase_actual)
    update_statistics(statistic_fase, local_id, visitante_id)

    return {"message": "Resultado actualizado"}
