"""
WorkoutPlan Model - Generated workout plans from LLM
"""
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.core.database import Base


class WorkoutPlan(Base):
    """
    LLM-generated workout plan for user
    Stores structured JSON plan data
    """

    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Plan data (structured JSON from LLM response)
    plan_data = Column(JSON, nullable=False)
    # Example: {"workout_plan": [{"musculo": "...", "ejercicio": "...", ...}], "disclaimer_medico": "..."}

    # Fatigue context
    fatigue_score_used = Column(Integer, nullable=False)  # 0-100 score at generation time

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="workout_plans")

    def __repr__(self):
        return f"<WorkoutPlan(id={self.id}, user_id={self.user_id}, fatigue={self.fatigue_score_used})>"
