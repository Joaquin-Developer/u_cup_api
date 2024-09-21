import logging
from typing import List
import requests
from fastapi import APIRouter, HTTPException
import pymysql

from schemas.partidos import PartidoUpdate
from db.db import DATABASE
import app.api_v1.endpoints.fase_final as fase_final
from core.settings import settings


logging.basicConfig(level=logging.INFO)

router = APIRouter()


class Table:
    PARTIDOS = "partidos"
    ENFRENTAMIENTOS = "enfrentamientos"


class StFase:
    GENERAL = "general"
    GRUPO = "grupo"


def _update_partido(partido_id: int, partido_data: PartidoUpdate, table: str):
    """
    Actualizar el resultado de un partido segun la fase
    table: ["partidos", "enfrentamientos"]
    """
    connection = pymysql.connect(**DATABASE)
    cursor = connection.cursor()

    # Obtener el partido por su ID
    query = f"SELECT * FROM {table} WHERE id = {partido_id}"
    cursor.execute(query)
    partido = cursor.fetchone()
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")


    if table == "enfrentamientos":
        p_l = partido_data.penales_local if partido_data.penales_local is not None else "null"
        p_v = partido_data.penales_visitante if partido_data.penales_visitante is not None else "null"
        penales_sql = f"""
        ,
            penales_local = {p_l},
            penales_visitante = {p_v}
        """
    else:
        penales_sql = ""

    query = f"""
    UPDATE {table}
    SET
        goles_local = {partido_data.goles_local},
        goles_visitante = {partido_data.goles_visitante}
        {penales_sql}
    WHERE
        id = {partido_id}
    """
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

    local_id, visitante_id = partido[1], partido[2]
    return local_id, visitante_id


def update_statistics(fase: str, local_id: int, visitante_id: int):
    """
    Llamada al microservicio de estadisticas para actualizar estadisticas
    """
    url = f"{settings.STATISTICS_SERVICE_URL}/estadisticas/{fase}"
    url += f"?equipos_id={local_id}&equipos_id={visitante_id}"

    resp = requests.post(url)
    if resp.status_code != 200:
        logging.warning("No se pudo actualizar las estadisticas")
        logging.warning(resp.json())


def call_load_next_fase_service():
    """
    Llamada al microservicio para cargar partidos de la siguiente fase
    """
    resp = requests.get(settings.LOAD_NEXT_FASE_SERVICE_URL)

    if resp.status_code != 200:
        logging.error("Error en llamada a load_next_fase")
        logging.error(resp.json())


@router.put("/partidos/{partido_id}")
def update_partido(partido_id: int, partido_data: PartidoUpdate):
    fase_actual = fase_final.get_fase_actual()["nombre"]

    table = Table.PARTIDOS if fase_actual == "Fase de Grupos" else Table.ENFRENTAMIENTOS
    statistic_fase = StFase.GRUPO if fase_actual == "Fase de Grupos" else StFase.GENERAL

    local_id, visitante_id = _update_partido(partido_id, partido_data, table)
    update_statistics(statistic_fase, local_id, visitante_id)

    if statistic_fase == StFase.GENERAL:
        call_load_next_fase_service()

    return {"message": "Resultado actualizado"}
