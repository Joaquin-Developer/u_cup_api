from fastapi import APIRouter, HTTPException
import pymysql

from schemas.partidos import PartidoUpdate
from db.db import DATABASE
import app.api_v1.endpoints.fase_final as fase_final


router = APIRouter()


def update_partido_grupo(partido_id: int, partido_data: PartidoUpdate):
    """
    Ruta para actualizar el resultado de un partido
    """
    connection = pymysql.connect(**DATABASE)
    cursor = connection.cursor()

    # Obtener el partido por su ID
    query = f"SELECT * FROM partidos WHERE id = {partido_id}"
    cursor.execute(query)
    partido = cursor.fetchone()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    query = f"""
    UPDATE partidos
    SET
        goles_local = {partido_data.goles_local},
        goles_visitante = {partido_data.goles_visitante}
    WHERE
        id = {partido_id}
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Resultado actualizado"}


def update_partido_fase_final(partido_id: int, partido_data: PartidoUpdate):
    """
    Ruta para actualizar el resultado de un partido de la fase final
    """
    connection = pymysql.connect(**DATABASE)
    cursor = connection.cursor()

    # Obtener el partido por su ID
    query = f"SELECT * FROM enfrentamientos WHERE id = {partido_id}"
    cursor.execute(query)
    partido = cursor.fetchone()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    query = f"""
    UPDATE enfrentamientos
    SET
        goles_local = {partido_data.goles_local},
        goles_visitante = {partido_data.goles_visitante}
    WHERE
        id = {partido_id}
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    return {"message": "Resultado actualizado"}


@router.put("/partidos/{partido_id}")
def update_partido(partido_id: int, partido_data: PartidoUpdate):

    if fase_final.get_fase_actual()["fase_actual"] == "Fase de Grupos":
        update_partido_grupo(partido_id, partido_data)
    else:
        update_partido_fase_final(partido_id, partido_data)
