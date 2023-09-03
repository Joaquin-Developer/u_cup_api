from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Metadata(Base):
    __tablename__ = "metadata_cup"
    _ = Column(Integer, primary_key=True)
    name = Column(String)
    abr_name = Column(String)
