from pydantic import BaseModel


class Fase(BaseModel):
    """Schema para metadata de las fases"""
    id: int
    nombre: str
    ida_vuelta: bool
