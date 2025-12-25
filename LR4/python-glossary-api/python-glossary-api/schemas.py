from pydantic import BaseModel
from typing import Optional


class GlossaryTermBase(BaseModel):
    term: str
    definition: str
    category: Optional[str] = "general"
    example: Optional[str] = None


class GlossaryTermCreate(GlossaryTermBase):
    pass


class GlossaryTermUpdate(BaseModel):
    term: Optional[str] = None
    definition: Optional[str] = None
    category: Optional[str] = None
    example: Optional[str] = None


class GlossaryTerm(GlossaryTermBase):
    id: int

    class Config:
        from_attributes = True  # Для совместимости с SQLAlchemy