"""
User Model - Authentication
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from src.core.database import Base


class User(Base):
    """
    User account for authentication
    Stores email and password hash only
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    workout_plans = relationship(
        "WorkoutPlan", back_populates="user", cascade="all, delete-orphan"
    )
    workout_logs = relationship(
        "WorkoutLog", back_populates="user", cascade="all, delete-orphan"
    )
    nutrition_plans = relationship(
        "NutritionPlan", back_populates="user", cascade="all, delete-orphan"
    )
    chat_sessions = relationship(
        "ChatSession", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
