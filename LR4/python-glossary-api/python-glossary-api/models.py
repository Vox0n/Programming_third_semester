from sqlalchemy import Column, Integer, String, Text
from database import Base


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, index=True, nullable=False)
    definition = Column(Text, nullable=False)
    category = Column(String, default="general")
    example = Column(Text, nullable=True)