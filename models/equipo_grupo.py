from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class EquipoGrupo(Base):
    __tablename__ = "equipos_grupos"

    id = Column(Integer, primary_key=True, index=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    grupo_id = Column(Integer, ForeignKey("grupos.id"))
    equipo_posicion = Column(Integer)

    equipo = relationship("Equipo", back_populates="grupos")
    grupo = relationship("Grupo", back_populates="equipos", secondary="equipos_grupos")
