from pydantic import BaseModel


class EstadisticasGrupo(BaseModel):
    """Schema para las estadisticas por grupo"""
    grupo: str
    equipo_id: int
    nombre: str
    pts: int
    goles_favor: int
    goles_contra: int
    diferencia: int

class EquiposClasificados(BaseModel):
    """Schema para los clasificados a 8vos de Final."""
    grupo: str
    equipo_posicion: int
    equipo_id: int
    nombre: str
    pts: int
    goles_favor: int
    goles_contra: int