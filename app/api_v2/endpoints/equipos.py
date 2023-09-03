from typing import List
from fastapi import APIRouter

from schemas import equipo
from core.database import get_session
from models.equipo import Equipo
from models.equipo_grupo import EquipoGrupo
from models.grupo import Grupo

router = APIRouter()


@router.get("/", response_model=List[equipo.Equipo])
def get_equipos():
    with get_session() as session:        
        results = session.query(
            Equipo.id,
            Equipo.nombre,
            Equipo.pts,
            Equipo.goles_favor,
            Equipo.goles_contra,
            Grupo.nombre.label("grupo"),
        ).join(
            EquipoGrupo, Equipo.id == EquipoGrupo.equipo_id
        ).join(
            Grupo, EquipoGrupo.grupo_id == Grupo.id
        ).all()

    return [
        equipo.Equipo(
            id=res.id,
            nombre=res.nombre,
            pts=res.pts,
            goles_favor=res.goles_favor,
            goles_contra=res.goles_contra,
            grupo=res.grupo
        )
        for res in results
    ]

