from pydantic import BaseModel


class ResultadoGrupo(BaseModel):
    """Definición del modelo de salida para los resultados de un grupo"""
    fecha: str
    grupo: str
    equipo_local: str
    goles_local: int
    equipo_visitante: str
    goles_visitante: int
    status_partido: str


class ResultadoFase(BaseModel):
    """Definición del modelo de salida para los resultados de una fase"""
    fecha: str
    fase_nombre: str
    equipo_local: str
    goles_local: int
    equipo_visitante: str
    goles_visitante: int
    status_partido: str


class ResultadoEquipo(BaseModel):
    """Definición del modelo de salida para los resultados de un equipo"""
    id_partido: int
    fase: str
    grupo: str
    equipo_local: str
    goles_local: int
    equipo_visitante: str
    goles_visitante: int
    status_partido: str
