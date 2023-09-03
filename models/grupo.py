from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from db.base_class import Base


class Grupo(Base):
    __tablename__ = "grupos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(VARCHAR(10))

    # estadisticas = relationship("EstadisticasGrupo", back_populates="grupo")
    

    # equipos = relationship("EquipoGrupo", back_populates="grupo", cascade="all, delete")
    # partidos = relationship("Partido", back_populates="grupo")
