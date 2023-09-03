from pydantic import BaseModel


class Fase(BaseModel):
    """Schema para metadata de las fases"""
    id: int
    nombre: str
    ida_vuelta: bool


class FaseActual(Fase):
    """Schema para datos de fase actual"""

