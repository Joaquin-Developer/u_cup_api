from sqlalchemy.sql import text
from fastapi import APIRouter

# from models.metadata import Metadata
from core.database import get_session
from schemas import fases

router = APIRouter()


@router.get("/fase_actual", response_model=fases.FaseActual)
def get_fase_actual():
    """
    Obtener cuál es la fase actual
    """
    query = text("""
        WITH fase_actual AS (
            SELECT id, nombre, ida_vuelta
            FROM fases
            WHERE id = (
                SELECT MAX(fase_id) 
                FROM enfrentamientos
            )
        )
        SELECT
            id,
            nombre,
            ida_vuelta
        FROM fase_actual
        UNION ALL
        SELECT
            0 as id,
            'Fase de Grupos' as nombre,
            1 as ida_vuelta
        FROM dual
        WHERE NOT EXISTS (SELECT * FROM fase_actual)
    """)
    with get_session() as session:
        row = session.execute(query).one()
    
    return fases.FaseActual(id=row.id, nombre=row.nombre, ida_vuelta=row.ida_vuelta)
