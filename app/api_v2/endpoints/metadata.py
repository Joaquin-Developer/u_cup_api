from typing import List
from fastapi import APIRouter

from core.database import get_session
from schemas import fases, metadata
from models.metadata import Metadata
from models.fase import Fase

router = APIRouter()


@router.get("/", response_model=metadata.Metadata)
def get_metadata():
    with get_session() as session:
        result = session.query(Metadata.name, Metadata.abr_name).one()
    return metadata.Metadata(name=result.name, abr_name=result.abr_name)


@router.get("/fases", response_model=List[fases.Fase])
def get_fases_metadata():
    with get_session() as session:
        results = session.query(Fase.id, Fase.nombre, Fase.ida_vuelta).all()

    return [
        fases.Fase(id=res.id, nombre=res.nombre, ida_vuelta=res.ida_vuelta)
        for res in results
    ]
