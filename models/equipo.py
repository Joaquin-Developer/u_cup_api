from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

Base = declarative_base()


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(VARCHAR(100))
    pts = Column(Integer)
    goles_favor = Column(Integer)
    goles_contra = Column(Integer)
    # estadisticas = relationship("EstadisticasGrupo", back_populates="equipo")

    # grupos = relationship("EquipoGrupo", back_populates="equipo")