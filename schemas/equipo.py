from pydantic import BaseModel


class Equipo(BaseModel):
    """Schema para los equipos"""
    id: int
    nombre: str
    pts: int
    goles_favor: int
    goles_contra: int
    grupo: str
