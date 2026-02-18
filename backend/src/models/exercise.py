"""
Exercise Model - Exercise library with safety notes and technique cues
"""
from sqlalchemy import Column, Integer, String, JSON

from src.core.database import Base


class Exercise(Base):
    """
    Exercise library - pre-populated with 50-100 exercises
    Used by LLM for workout plan generation
    """

    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # Exercise identification
    name = Column(String(100), unique=True, nullable=False, index=True)  # Spanish name
    muscle_groups = Column(JSON, nullable=False)  # ["pectoral", "triceps"]

    # Safety and technique
    safety_notes = Column(String(500), nullable=False)  # Contraindications, injury warnings
    technique_cues = Column(JSON, nullable=False)  # ["mantén escápulas retraídas", "codos 45 grados"]

    # Volume guidelines (JSONB for flexible schema)
    volume_guidelines_json = Column(
        JSON, nullable=False
    )  # {"beginner": "3x8-12", "intermediate": "4x8-12", "advanced": "4-5x6-10"}

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name})>"
