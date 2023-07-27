from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Enfrentamiento(Base):
    __tablename__ = "enfrentamientos"

    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(Integer, ForeignKey("equipos.id"))
    visitante_id = Column(Integer, ForeignKey("equipos.id"))
    fase_id = Column(Integer, ForeignKey("fases.id"))
    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)

    fase = relationship("Fase", back_populates="enfrentamientos")
    local = relationship("Equipo", foreign_keys=[local_id])
    visitante = relationship("Equipo", foreign_keys=[visitante_id])