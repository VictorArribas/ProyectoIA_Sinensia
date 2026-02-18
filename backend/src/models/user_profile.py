"""
UserProfile Model - User's fitness profile data
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
import enum

from src.core.database import Base


class FitnessObjective(str, enum.Enum):
    """User's fitness goal"""

    HYPERTROPHY = "hypertrophy"  # Hipertrofia (muscle gain)
    CUTTING = "cutting"  # Definición (fat loss)
    STRENGTH = "strength"  # Fuerza
    RECOMPOSITION = "recomposition"  # Recomposición corporal


class ExperienceLevel(str, enum.Enum):
    """User's training experience"""

    BEGINNER = "beginner"  # Principiante
    INTERMEDIATE = "intermediate"  # Intermedio
    ADVANCED = "advanced"  # Avanzado


class UserProfile(Base):
    """
    User's fitness profile - biometric data and training parameters
    One-to-one relationship with User
    """

    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Biometric data
    age = Column(Integer, nullable=False)
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)

    # Fitness parameters
    objective = Column(Enum(FitnessObjective), nullable=False)
    experience_level = Column(Enum(ExperienceLevel), nullable=False)
    training_days_per_week = Column(Integer, nullable=False)

    # Equipment availability (JSON array of strings)
    equipment_available = Column(JSON, nullable=False)  # ["dumbbells", "barbell", "cables", "machines"]

    # Injury history (JSON array of strings)
    injury_history = Column(JSON, nullable=True, default=list)  # ["lower back", "shoulder"]

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, objective={self.objective}, experience={self.experience_level})>"
