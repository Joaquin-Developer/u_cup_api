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
        with estadisticas as (
            select
                g.nombre as grupo,
                e.id as equipo_id,
                e.nombre,
                sum(
                    case when e.id = p.local_id then
                        -- partidos local
                        case
                            when p.goles_local > p.goles_visitante then 3
                            when p.goles_local = p.goles_visitante then 1
                            else 0
                        end
                    else
                        -- partidos visitante
                        case
                            when p.goles_visitante > p.goles_local then 3
                            when p.goles_visitante = p.goles_local then 1
                            else 0
                        end
                    end
                ) as pts,
                sum(
                    case when e.id = p.local_id then p.goles_local else p.goles_visitante end
                ) as goles_favor,
                sum(
                    case when e.id != p.local_id then p.goles_local else p.goles_visitante end
                ) as goles_contra 
            from
                equipos e
                join equipos_grupos eg on e.id = eg.equipo_id
                join grupos g on eg.grupo_id = g.id
                join partidos p on e.id = p.local_id or e.id = p.visitante_id
            where eg.grupo_id = {grupo_id}
            group by
                e.id,
                e.nombre
        )
        select
            e.*,
            e.goles_favor - e.goles_contra as diferencia
        from estadisticas e
        order by e.pts desc, (e.goles_favor - e.goles_contra) desc
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
        WITH estadisticas AS (
            with _estadisticas as (
                select
                    g.nombre as grupo,
                    e.id as equipo_id,
                    e.nombre,
                    sum(
                    case when e.id = p.local_id then
                        -- partidos local
                        case
                        when p.goles_local > p.goles_visitante then 3
                        when p.goles_local = p.goles_visitante then 1
                        else 0
                        end
                    else
                        -- partidos visitante
                        case
                        when p.goles_visitante > p.goles_local then 3
                        when p.goles_visitante = p.goles_local then 1
                        else 0
                        end
                    end
                    ) as pts,
                    sum(
                        case when e.id = p.local_id then p.goles_local else p.goles_visitante end
                    ) as goles_favor,
                    sum(
                        case when e.id != p.local_id then p.goles_local else p.goles_visitante end
                    ) as goles_contra 
                from
                    equipos e
                    join equipos_grupos eg on e.id = eg.equipo_id
                    join grupos g on eg.grupo_id = g.id
                    join partidos p on e.id = p.local_id or e.id = p.visitante_id
                group by
                    e.id,
                    e.nombre
            )
            select
                e.*,
                e.goles_favor - e.goles_contra as diferencia
            from _estadisticas e
            order by e.pts desc, (e.goles_favor - e.goles_contra) desc
        ),
        clasificados AS (
            SELECT
                grupo,
                equipo_id,
                nombre,
                pts,
                goles_favor,
                goles_contra,
                ROW_NUMBER() OVER (PARTITION BY grupo ORDER BY pts DESC, (goles_favor - goles_contra) DESC) AS posicion
            FROM estadisticas
        )
        SELECT
            grupo,
            posicion as equipo_posicion,
            equipo_id,
            nombre,
            pts,
            goles_favor,
            goles_contra
        FROM clasificados
        WHERE posicion <= 2;
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
    