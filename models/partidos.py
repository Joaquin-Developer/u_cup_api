from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# class Partido(Base):
#     __tablename__ = "partidos"

#     id = Column(Integer, primary_key=True, index=True)
#     local_id = Column(Integer, nullable=False)
#     visitante_id = Column(Integer, nullable=False)
#     grupo_id = Column(Integer, nullable=False)
#     fecha = Column(Date, nullable=True)
#     goles_local = Column(Integer, nullable=True)
#     goles_visitante = Column(Integer, nullable=True)


class Partido(Base):
    __tablename__ = "partidos"

    id = Column(Integer, primary_key=True, index=True)
    local_id = Column(Integer, ForeignKey("equipos.id"))
    visitante_id = Column(Integer, ForeignKey("equipos.id"))
    grupo_id = Column(Integer, ForeignKey("grupos.id"))
    fecha = Column(Date, nullable=True)
    goles_local = Column(Integer, nullable=True)
    goles_visitante = Column(Integer, nullable=True)

    # grupo = relationship("Grupo", back_populates="partidos")
    # local = relationship("Equipo", foreign_keys=[local_id])
    # visitante = relationship("Equipo", foreign_keys=[visitante_id])