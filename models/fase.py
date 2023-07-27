from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

Base = declarative_base()


class Fase(Base):
    __tablename__ = "fases"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(VARCHAR(20))

    enfrentamientos = relationship("Enfrentamiento", back_populates="fase")
