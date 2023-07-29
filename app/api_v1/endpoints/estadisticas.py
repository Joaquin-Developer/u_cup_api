from typing import List
from fastapi import APIRouter
import pymysql

from schemas.estadisticas import EstadisticasGrupo, EquiposClasificados
from db.db import DATABASE

router = APIRouter()


def execute_query(sql: str, return_data=False):
    """
    Execute sql query in MySQL.
    """
    data = None
    connection = pymysql.connect(**DATABASE)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()

    if return_data:
        data = cursor.fetchall()

    cursor.close()
    connection.close()
    return data


@router.get("/grupos/{grupo_id}", response_model=List[EstadisticasGrupo])
def estadisticas_grupo(grupo_id: int):
    """
    Endpoint para obtener las posiciones por grupo
    (equipo, pts, posicion, goles_favor, goles_contra)
    """
    query = f"""
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
    data = execute_query(sql=query, return_data=True)
    res = []

    for estadistica in data:
        resultado = EstadisticasGrupo(
            grupo=estadistica[0],
            equipo_id=estadistica[1],
            nombre=estadistica[2],
            pts=estadistica[3],
            goles_favor=estadistica[4],
            goles_contra=estadistica[5],
            diferencia=estadistica[6],
        )
        res.append(resultado)
    return res


@router.get("/clasificados", response_model=List[EquiposClasificados])
def equipos_clasificados():
    """
    Endpoint para obtener las posiciones por grupo
    (equipo, pts, posicion, goles_favor, goles_contra)
    """
    query = """
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
    """
    data = execute_query(sql=query, return_data=True)
    res = []

    for estadistica in data:
        resultado = EquiposClasificados(
            grupo=estadistica[0],
            equipo_posicion=estadistica[1],
            equipo_id=estadistica[2],
            nombre=estadistica[3],
            pts=estadistica[4],
            goles_favor=estadistica[5],
            goles_contra=estadistica[6]
        )
        res.append(resultado)
    return res
    