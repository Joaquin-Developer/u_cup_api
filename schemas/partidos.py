from typing import Optional
from pydantic import BaseModel


class PartidoUpdate(BaseModel):
    goles_local: int
    goles_visitante: int
    penales_local: Optional[int] = None
    penales_visitante: Optional[int] = None
