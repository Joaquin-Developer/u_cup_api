from pydantic import BaseModel


class PartidoUpdate(BaseModel):
    goles_local: int
    goles_visitante: int
