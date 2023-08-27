from sqlalchemy import Column, Integer, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class EstadisticasGrupo(Base):
    __tablename__ = "estadisticas_grupo"
    equipo_id = Column(Integer, ForeignKey("equipos.id"), primary_key=True, nullable=False)
    grupo_id = Column(Integer, ForeignKey("grupos.id"), primary_key=True, nullable=False)
    
    pts = Column(Integer)
    goles_favor = Column(Integer)
    goles_contra = Column(Integer)
    diferencia = Column(Integer)

    # __table_args__ = (
    #     PrimaryKeyConstraint('equipo_id', 'grupo_id'),
    # )

    grupo = relationship("Grupos", back_populates="estadisticas")
    equipo = relationship("Equipos", back_populates="estadisticas")
