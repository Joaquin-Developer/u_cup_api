from typing import List
from fastapi import APIRouter
import pymysql

from schemas.fases import Fase
from schemas.campeonato import CampeonatoMetadata
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


@router.get("/fases", response_model=List[Fase])
def fases_metadata():
    """
    Ruta para obtener metadatos de las fases
    """
    query = """
        select id, nombre, ida_vuelta
        from fases
    """
    data = execute_query(sql=query, return_data=True)
    res = []

    for fase in data:
        res.append(
            Fase(
                id=fase[0],
                nombre=fase[1],
                ida_vuelta=bool(fase[2])
            )
        )
    return res


@router.get("/campeonato", response_model=CampeonatoMetadata)
def campeonato_metadata():
    """
    Ruta para obtener metadatos del campeonato
    """
    query = "select name, abr_name from metadata_cup"
    data = execute_query(sql=query, return_data=True)[0]
    return CampeonatoMetadata(name=data[0], abr_name=data[1])
