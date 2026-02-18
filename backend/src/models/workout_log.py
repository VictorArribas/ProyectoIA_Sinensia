"""
WorkoutLog Model - Post-workout fatigue and pain tracking
"""
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from src.core.database import Base


class WorkoutLog(Base):
    """
    Post-workout log - RPE and pain reporting
    Used to calculate fatigue score for next workout
    """

    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Fatigue metrics
    rpe = Column(Integer, nullable=False)  # 1-10 Rate of Perceived Exertion
    pain_reported = Column(Boolean, nullable=False, default=False)
    pain_location = Column(String(100), nullable=True)  # "lower back", "shoulder", null if no pain

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="workout_logs")

    def __repr__(self):
        return f"<WorkoutLog(id={self.id}, user_id={self.user_id}, rpe={self.rpe}, pain={self.pain_reported})>"
