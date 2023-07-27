from typing import List
from fastapi import APIRouter
import pymysql

from schemas.equipo import Equipo
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


@router.get("/", response_model=List[Equipo])
def equipos():
    query = """
        select
            e.id,
            e.nombre,
            e.pts,
            e.goles_favor,
            e.goles_contra,
            g.nombre as grupo
        from
            equipos e
            join equipos_grupos eg on e.id = eg.equipo_id
            join grupos g on eg.grupo_id = g.id
    """
    data = execute_query(sql=query, return_data=True)
    res = []

    for resultado in data:
        res.append(
            Equipo(
                id=resultado[0],
                nombre=resultado[1],
                pts=resultado[2],
                goles_favor=resultado[3],
                goles_contra=resultado[4],
                grupo=resultado[5],
            )
        )
    return res
