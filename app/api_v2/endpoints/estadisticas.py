from typing import List
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text
from sqlalchemy import func
from fastapi import APIRouter

from core.database import get_session
from db.session import SessionLocal
from models.estadisticas_grupo import EstadisticasGrupo
from models.grupo import Grupo
from models.equipo import Equipo
from schemas import estadisticas

router = APIRouter()


@router.get("/grupos/{grupo_id}", response_model=List[estadisticas.EstadisticasGrupo])
def estadisticas_grupo(grupo_id: int):
    """
        Get positions by group
    """
    query = """
        select
            g.nombre as grupo,
            e.equipo_id,
            eq.nombre,
            e.pts,
            e.goles_favor,
            e.goles_contra,
            e.diferencia
        from
            estadisticas_grupo e
            join grupos g on e.grupo_id = g.id
            join equipos eq on e.equipo_id = eq.id
        where grupo_id = {grupo_id}
        order by e.pts desc, e.diferencia desc
    """
    query = text(query.format(grupo_id=grupo_id))

    with get_session() as session:
        results = session.execute(query).fetchall()

    return [
        dict(zip(row._mapping.keys(), row))
        for row in results
    ]


@router.get("/clasificados", response_model=List[estadisticas.EquiposClasificados])
def equipos_clasificados():
    """
        Get qualifiers by group
    """
    query = text("""
        with estadisticas as (
            select
                g.nombre as grupo,
                ROW_NUMBER() OVER (PARTITION BY g.nombre ORDER BY e.pts DESC, e.diferencia DESC) AS equipo_posicion,
                e.equipo_id,
                eq.nombre,
                e.pts,
                e.goles_favor,
                e.goles_contra,
                e.diferencia
            from
                estadisticas_grupo e
                join grupos g on e.grupo_id = g.id
                join equipos eq on e.equipo_id = eq.id
            order by e.pts desc, e.diferencia desc
        )
        select e.*
        from estadisticas e
        where e.equipo_posicion <= 2
        order by grupo asc, equipo_posicion asc
    """)

    with get_session() as session:
        results = session.execute(query).fetchall()

    return [
        dict(zip(row._mapping.keys(), row))
        for row in results
    ]
