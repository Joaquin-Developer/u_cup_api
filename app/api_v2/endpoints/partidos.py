import logging
from typing import List, Tuple
import requests
from sqlalchemy.sql import text
from fastapi import APIRouter, HTTPException

from core.database import get_session
from models.partidos import Partido
from models.grupo import Grupo
from models.equipo import Equipo
from models.enfrentamiento import Enfrentamiento
from schemas import fases
from schemas import partidos
from schemas import resultados as res
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


@router.get("/grupo/{grupo_id}", response_model=List[res.ResultadoGrupo])
def get_partidos_grupo(grupo_id: int):
    """
    Devuelve todos los partidos de un grupo
    """
    with get_session() as session:
        partidos = session.query(
            Partido.fecha,
            Grupo.nombre,
            Equipo.nombre.label("nombre_local"),
            Partido.goles_local,
            Equipo.nombre.label("nombre_visitante"),
            Partido.goles_visitante,
            Partido.status_partido,
        ).join(
            Partido.grupo,
            Partido.grupo_id == Grupo.id,
        ).join(
            Partido.local,
            Partido.local_id == Equipo.id,
        ).join(
            Partido.visitante,
            Partido.visitante_id == Equipo.id,
        ).filter(Grupo.id == grupo_id).order_by(Partido.id.asc())

    return [
        ResultadoGrupo(
            fecha=result.fecha,
            grupo=result.nombre,
            equipo_local=result.nombre_local,
            goles_local=result.goles_local,
            equipo_visitante=result.res.nombre_visitante,
            goles_visitante=result.goles_visitante,
            status_partido=result.status_partido
        )
        for result in partidos
    ]


@router.get("/fase/{fase_id}", response_model=List[res.ResultadosFase])
def get_partidos_fase(fase_id: int):
    """
    Devuelve todos los partidos de una fase, dada la fase_id
    """
    with get_session() as session:
        partidos = session.query(
            Enfrentamiento.fecha,
            Grupo.nombre,
            Equipo.nombre.label("nombre_local"),
            Enfrentamiento.goles_local,
            Equipo.nombre.label("nombre_visitante"),
            Enfrentamiento.goles_visitante,
            Enfrentamiento.status_partido,
        ).join(
            Enfrentamiento.grupo,
            Partido.grupo_id == Grupo.id,
        ).join(
            Partido.local,
            Partido.local_id == Equipo.id,
        ).join(
            Partido.visitante,
            Partido.visitante_id == Equipo.id,
        ).filter(Grupo.id == grupo_id).order_by(Partido.id.asc())

    return [
        res.ResultadoFase(
            fecha=result.fecha,
            grupo=result.nombre,
            equipo_local=result.nombre_local,
            goles_local=result.goles_local,
            equipo_visitante=result.res.nombre_visitante,
            goles_visitante=result.goles_visitante,
            status_partido=result.status_partido,
            penales_local=result.penales_local,
            penales_visitante=result.penales_visitante
        )
        for result in partidos
    ]


@router.get("/equipo/{equipo_nombre}", response_model=List[res.ResultadoEquipo])
def get_partidos_equipo(equipo_nombre: int):
    """
    Dado un equipo (nombre), devuelve todos sus partidos
    """
    query = text(f"""
        with partidos as (
            select
                p.id as id_partido,
                'Fase de Grupos' as fase,
                g.nombre as grupo,
                local.nombre as equipo_local,
                coalesce(p.goles_local, 0) as goles_local,
                vis.nombre as equipo_visitante,
                coalesce(p.goles_visitante, 0) as goles_visitante,
                case when p.goles_local is null then 'NO JUGADO' else 'JUGADO' end as status_partido
            from
                grupos g
                join partidos p on g.id = p.grupo_id
                join equipos local on p.local_id = local.id
                join equipos vis on p.visitante_id = vis.id
            where
                local.nombre = '{equipo_nombre}' or vis.nombre = '{equipo_nombre}'
            union
            select
                e.id as id_partido,
                f.nombre as fase,
                '' as grupo,
                local.nombre as equipo_local,
                coalesce(e.goles_local, 0) as goles_local,
                vis.nombre as equipo_visitante,
                coalesce(e.goles_visitante, 0) as goles_visitante,
                case when e.goles_local is null then 'NO JUGADO' else 'JUGADO' end as status_partido
            from
                enfrentamientos e
                join equipos local on e.local_id = local.id
                join equipos vis on e.visitante_id = vis.id
                join fases f on e.fase_id = f.id
            where
                local.nombre = '{equipo_nombre}' or vis.nombre = '{equipo_nombre}'
        )
        select * from partidos
        order by id_partido asc
    """)

    with get_session() as session:
        results = session.execute(query).fetchall()
    return [
        res.ResultadoEquipo(
            id_partido=result.id_partido,
            fase=result.fase,
            grupo=result.grupo,
            equipo_local=result.equipo_local,
            goles_local=result.goles_local,
            equipo_visitante=result.equipo_visitante,
            goles_visitante=result.goles_visitante,
            status_partido=result.status_partido
        )
        for result in results
    ]
    