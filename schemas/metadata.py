from pydantic import BaseModel


class Metadata(BaseModel):
    """Schema para metadata de la competencia"""
    name: str
    abr_name: str
