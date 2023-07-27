from typing import List
from fastapi import APIRouter, HTTPException
import pymysql

from schemas.resultados import ResultadoEquipo, ResultadoFase, ResultadoGrupo
from models.partidos import Partido
from models.equipo import Equipo
from models.grupo import Grupo
# from models.equipo_grupo import EquipoGrupo
from db.session import SessionLocal
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


@router.get("/resultados/grupos/{grupo_id}", response_model=List[ResultadoGrupo])
def get_resultados_grupo(grupo_id: int):
    """
    Ruta para obtener todos los resultados por Grupo
    """

    query = f"""
        select
            coalesce(p.fecha, 'SIN DATA') as fecha,
            g.nombre as nombre,
            loc.nombre as nombre_local,
            coalesce(p.goles_local, 0) as goles_local,
            vis.nombre as nombre_visitante,
            coalesce(p.goles_visitante, 0) as goles_visitante,
            case
                when p.goles_local is null then 'NO JUGADO'
                else 'JUGADO'
            end as status_partido
        from
            grupos g
            join partidos p on g.id = p.grupo_id
            join equipos loc on p.local_id = loc.id
            join equipos vis on p.visitante_id = vis.id
        where
            g.id = {grupo_id}
        order by
            p.id asc 
    """
    data = execute_query(sql=query, return_data=True)
    res = []

    for partido in data:
        resultado = ResultadoGrupo(
            fecha=partido[0],
            grupo=partido[1],
            equipo_local=partido[2],
            goles_local=partido[3],
            equipo_visitante=partido[4],
            goles_visitante=partido[5],
            status_partido=partido[6]
        )
        res.append(resultado)
    return res


@router.get("/resultados/fase/{fase_id}", response_model=List[ResultadoFase])
def get_resultados_fase(fase_id: int):
    """
    Ruta para obtener todos los resultados por Fase (8vos, 4tos, etc)
    """

    query = f"""
        select
            coalesce(p.fecha, 'SIN DATA') as fecha,
            f.nombre as fase_nombre,
            loc.nombre as nombre_local,
            coalesce(p.goles_local, 0) as goles_local,
            vis.nombre as nombre_visitante,
            coalesce(p.goles_visitante, 0) as goles_visitante,
            case
                when p.goles_local is null then 'NO JUGADO'
                else 'JUGADO'
            end as status_partido
        from
            fases f
            join enfrentamientos p on f.id = p.fase_id
            join equipos loc on p.local_id = loc.id
            join equipos vis on p.visitante_id = vis.id
        where
            f.id = {fase_id}
        order by
            p.id asc 
    """
    data = execute_query(sql=query, return_data=True)
    res = []

    for partido in data:
        resultado = ResultadoFase(
            fecha=partido[0],
            fase_nombre=partido[1],
            equipo_local=partido[2],
            goles_local=partido[3],
            equipo_visitante=partido[4],
            goles_visitante=partido[5],
            status_partido=partido[6]
        )
        res.append(resultado)
    return res


@router.get("/resultados/equipos/{equipo_nombre}", response_model=List[ResultadoEquipo])
def get_resultados_equipo_nombre(equipo_nombre: str):
    query = f"""
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
    """
    data = execute_query(sql=query, return_data=True)
    res = []

    for partido in data:
        resultado = ResultadoEquipo(
            id_partido=partido[0],
            fase=partido[1],
            grupo=partido[2],
            equipo_local=partido[3],
            goles_local=partido[4],
            equipo_visitante=partido[5],
            goles_visitante=partido[6],
            status_partido=partido[7]
        )
        res.append(resultado)
    return res


# @router.get("/resultados/grupos/{grupo_id}", response_model=List[ResultadoGrupo])
# def get_resultados_grupo(grupo_id: int):
#     """
#     Ruta para obtener todos los resultados por Grupo
#     """
#     db = SessionLocal()
#     grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()
#     if not grupo:
#         raise HTTPException(status_code=404, detail="Grupo no encontrado")

#     resultados = []
#     for partido in grupo.partidos:
#         if partido.goles_local and partido.goles_visitante:
#             resultado = ResultadoGrupo(
#                 partido_id=partido.id,
#                 local=partido.local.nombre,
#                 visitante=partido.visitante.nombre,
#                 goles_local=partido.goles_local,
#                 goles_visitante=partido.goles_visitante,
#             )
#             resultados.append(resultado)
#     db.close()
#     return resultados


# @router.get("/resultados/fases/{fase_id}", response_model=List[ResultadoFase])
# def get_resultados_fase(fase_id: int):
#     """
#     Ruta para obtener todos los resultados por Fase
#     """
#     db = SessionLocal()
#     fase = db.query(Fase).filter(Fase.id == fase_id).first()
#     if not fase:
#         raise HTTPException(status_code=404, detail="Fase no encontrada")

#     resultados = []
#     for enfrentamiento in fase.enfrentamientos:
#         if (
#             enfrentamiento.goles_local is not None
#             and enfrentamiento.goles_visitante is not None
#         ):
#             resultado = ResultadoFase(
#                 partido_id=enfrentamiento.id,
#                 local=enfrentamiento.local.nombre,
#                 visitante=enfrentamiento.visitante.nombre,
#                 goles_local=enfrentamiento.goles_local,
#                 goles_visitante=enfrentamiento.goles_visitante,
#             )
#             resultados.append(resultado)

#     return resultados


# @router.get("/resultados/equipos/{equipo_id}", response_model=List[ResultadoEquipo])
# def get_resultados_equipo(equipo_id: int):
#     """
#     Ruta para obtener los resultados de partidos de un equipo particular
#     """
#     db = SessionLocal()
#     equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
#     if not equipo:
#         raise HTTPException(status_code=404, detail="Equipo no encontrado")

#     resultados = []
#     partidos = (
#         db.query(Partido)
#         .filter(
#             (Partido.local_id == equipo_id)
#             | (Partido.visitante_id == equipo_id)
#         )
#         .all()
#     )
#     for partido in partidos:
#         if partido.goles_local is not None and partido.goles_visitante is not None:
#             resultado = ResultadoEquipo(
#                 partido_id=partido.id,
#                 local=partido.local.nombre,
#                 visitante=partido.visitante.nombre,
#                 goles_local=partido.goles_local,
#                 goles_visitante=partido.goles_visitante,
#             )
#             resultados.append(resultado)

#     return resultados
