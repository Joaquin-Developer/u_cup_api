from typing import List, Dict
from fastapi import APIRouter
import pymysql

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


@router.get("/fase_actual", response_model=Dict[str, str])
def get_fase_actual():
    query = """
        WITH fase_actual AS (
            SELECT nombre
            FROM fases
            WHERE id = (
                SELECT MAX(fase_id) 
                FROM enfrentamientos
            )
        )
        SELECT nombre
        FROM fase_actual
        UNION ALL
        SELECT 'Fase de Grupos'
        FROM dual
        WHERE NOT EXISTS (SELECT * FROM fase_actual)
    """
    # mejorar esto!
    data = execute_query(sql=query, return_data=True)[0][0]

    return {"fase_actual": data}
